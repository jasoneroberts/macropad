#!/usr/bin/env python3
"""Draws JR_preview.pdf: one page per part with its symbol, footprint and parameters, for reviewing the library.

    python3 pcb/library/src/preview.py [library dir]        (default: pcb/library)

Needs kicad-cli (KiCad 7) on PATH and `pip install cairosvg matplotlib`. Reads JR.kicad_sym, JR.pretty and
JR_parts.csv, so run build_library.py first.
"""
import csv
import io
import os
import subprocess
import sys
import tempfile

import cairosvg
import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402

LIBDIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def svg_png(path, width=2400, pad=20):
    """SVG as an image, cropped to what's drawn (kicad-cli puts a symbol on a whole page)."""
    img = mpimg.imread(io.BytesIO(cairosvg.svg2png(url=path, output_width=width, background_color="white")))
    bg = img[0, 0, :3]
    ink = (abs(img[:, :, :3] - bg).sum(axis=2) > 0.05).nonzero()
    if len(ink[0]):
        y0, y1, x0, x1 = ink[0].min(), ink[0].max(), ink[1].min(), ink[1].max()
        img = img[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad]
    return img


def main():
    rows = list(csv.DictReader(open(os.path.join(LIBDIR, "JR_parts.csv"))))
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["kicad-cli", "sym", "export", "svg", "-o", os.path.join(tmp, "sym"),
                        os.path.join(LIBDIR, "JR.kicad_sym")], check=True, capture_output=True)
        subprocess.run(["kicad-cli", "fp", "export", "svg", "-o", os.path.join(tmp, "fp"), "--layers",
                        "F.Cu,B.Cu,F.Mask,F.SilkS,F.Fab,F.CrtYd,Edge.Cuts", os.path.join(LIBDIR, "JR.pretty")],
                       check=True, capture_output=True)
        with PdfPages(os.path.join(LIBDIR, "JR_preview.pdf")) as pdf:
            for r in rows:
                fig = plt.figure(figsize=(11.69, 8.27))          # A4 landscape
                fig.suptitle(f'{r["Name"]}', fontsize=16, x=0.04, ha="left", y=0.96)
                for i, (title, path) in enumerate((
                        (f'Symbol: {r["Symbol"]}', os.path.join(tmp, "sym", r["Name"].lower() + ".svg")),
                        (f'Footprint: {r["Footprint"]}', os.path.join(tmp, "fp", r["Footprint"] + ".svg")))):
                    ax = fig.add_axes([0.03 + i * 0.49, 0.30, 0.46, 0.60])
                    ax.set_axis_off()
                    ax.set_title(title, fontsize=10, loc="left")
                    if os.path.exists(path):
                        ax.imshow(svg_png(path))
                    else:
                        ax.text(0.5, 0.5, "(no drawing)", ha="center", va="center", transform=ax.transAxes)
                keys = ["Designator", "Value (Comment)", "Description", "Manufacturer", "Manufacturer Part Number",
                        "LCSC", "Used on"]
                tax = fig.add_axes([0.04, 0.03, 0.92, 0.24])
                tax.set_axis_off()
                t = tax.table(cellText=[[k, r.get(k, "")] for k in keys], colWidths=[0.22, 0.78], loc="upper left",
                              cellLoc="left")
                t.auto_set_font_size(False)
                t.set_fontsize(9)
                t.scale(1, 1.35)
                pdf.savefig(fig)
                plt.close(fig)
    print(f"JR_preview.pdf: {len(rows)} parts")


if __name__ == "__main__":
    main()
