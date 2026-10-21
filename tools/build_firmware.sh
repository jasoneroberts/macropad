#!/bin/bash
# Builds every macropad firmware variant on Linux (how the cloud checks were run).
# On Jase's PC use the west commands in firmware/README.md from an NCS toolchain shell instead.
#
#   bash tools/build_firmware.sh setup   # once: NCS v3.3.0 + the distro's arm-none-eabi-gcc (needs root for apt)
#   bash tools/build_firmware.sh         # all six variants, then copies the concept B images to firmware/prebuilt/
#
# NCS and OUT can be overridden: NCS=~/ncs OUT=~/mp-build bash tools/build_firmware.sh
set -u
APP=$(cd "$(dirname "$0")/../firmware" && pwd)
NCS=${NCS:-$HOME/ncs}
OUT=${OUT:-$HOME/mp-build}

if [ "${1:-}" = setup ]; then
	set -e
	apt-get install -y gcc-arm-none-eabi device-tree-compiler gperf ccache python3-venv
	mkdir -p "$NCS" && cd "$NCS"
	[ -d .venv ] || python3 -m venv .venv
	. .venv/bin/activate
	pip install west
	[ -d .west ] || west init -m https://github.com/nrfconnect/sdk-nrf --mr v3.3.0 .
	west update --narrow -o=--depth=1 -n
	pip install -r zephyr/scripts/requirements-base.txt
	pip install -r nrf/scripts/requirements-build.txt
	echo "NCS ready in $NCS"
	exit 0
fi

# The venv made by "setup"; CI installs west into the user site instead
if [ -f "$NCS/.venv/bin/activate" ]; then
	. "$NCS/.venv/bin/activate"
fi
# The Zephyr SDK is not needed: the distro's GNU Arm compiler is enough for these builds
export ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb GNUARMEMB_TOOLCHAIN_PATH=/usr ZEPHYR_BASE=$NCS/zephyr
mkdir -p "$OUT"
cd "$NCS"
: > "$OUT/summary.txt"

b() { # name board [cmake args...]
	name=$1; board=$2; shift 2
	west build -p always -b "$board" -d "$OUT/$name" "$APP" -- "$@" > "$OUT/$name.log" 2>&1
	rc=$?
	w=$(grep -c "warning:" "$OUT/$name.log")
	mem=$(grep -E "^ +(FLASH|RAM):" "$OUT/$name.log" | awk '{print $1" "$2" "$3" "$6}' | tr '\n' ' ')
	echo "$name rc=$rc warnings=$w $mem" | tee -a "$OUT/summary.txt"
}

b B-dk nrf52840dk/nrf52840
b B-pm promicro_nrf52840/nrf52840/uf2
b A-pm promicro_nrf52840/nrf52840/uf2 -DEXTRA_CONF_FILE=concepts/a.conf -DEXTRA_DTC_OVERLAY_FILE=concepts/a.overlay
b C-pm promicro_nrf52840/nrf52840/uf2 -DEXTRA_CONF_FILE=concepts/c.conf -DEXTRA_DTC_OVERLAY_FILE=concepts/c.overlay
b A-dk nrf52840dk/nrf52840 -DEXTRA_CONF_FILE=concepts/a.conf -DEXTRA_DTC_OVERLAY_FILE=concepts/a_display.overlay
b C-dk nrf52840dk/nrf52840 -DEXTRA_CONF_FILE=concepts/c.conf -DEXTRA_DTC_OVERLAY_FILE=concepts/c_display.overlay

# The one expected warning per build is Kconfig's "Experimental symbol MIPI_DBI is enabled"
if grep -q "rc=[^0]" "$OUT/summary.txt"; then
	echo "Some builds failed; logs are in $OUT"
	exit 1
fi

mkdir -p "$APP/prebuilt"
cp "$OUT/B-pm/firmware/zephyr/zephyr.uf2" "$APP/prebuilt/macropad_B_promicro.uf2"
cp "$OUT/B-dk/merged.hex" "$APP/prebuilt/macropad_B_dk.hex" 2>/dev/null ||
	cp "$OUT/B-dk/firmware/zephyr/zephyr.hex" "$APP/prebuilt/macropad_B_dk.hex"
echo "All built; concept B images copied to $APP/prebuilt/"
