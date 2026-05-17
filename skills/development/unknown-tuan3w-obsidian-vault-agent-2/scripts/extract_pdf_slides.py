#!/usr/bin/env python3
# /// script
# dependencies = ["PyMuPDF>=1.24.0"]
# requires-python = ">=3.10"
# ///
"""Extract pages from a PDF as images for embedding in Obsidian notes.

Uses PyMuPDF (fitz) for fast PDF→PNG conversion.
Falls back to poppler (pdftocairo) if PyMuPDF is unavailable.

Usage:
    uv run extract_pdf_slides.py lecture.pdf --output-dir ./frames --prefix course-L01

Output:
    - PNG images: {prefix}-{page:02d}.png
    - Manifest JSON to stdout: [{filename, page, width, height}, ...]
"""

import argparse
import json
import os
import sys
import subprocess


def extract_with_fitz(pdf_path, output_dir, prefix, dpi=200):
    """Extract using PyMuPDF (fitz) — preferred method."""
    import fitz

    doc = fitz.open(pdf_path)
    manifest = []
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=matrix)
        filename = f"{prefix}-{page_num + 1:02d}.png"
        filepath = os.path.join(output_dir, filename)
        pix.save(filepath)
        manifest.append({
            "filename": filename,
            "page": page_num + 1,
            "width": pix.width,
            "height": pix.height,
        })

    doc.close()
    return manifest


def extract_with_sips(pdf_path, output_dir, prefix, dpi=200):
    """Fallback: use macOS sips + pdftocairo if available."""
    # Try pdftocairo first (from poppler)
    try:
        out_prefix = os.path.join(output_dir, prefix)
        subprocess.run(
            [
                "pdftocairo", "-png", "-r", str(dpi),
                pdf_path, out_prefix
            ],
            check=True, capture_output=True
        )
        # pdftocairo names files as {prefix}-{page}.png (1-indexed)
        manifest = []
        for f in sorted(os.listdir(output_dir)):
            if f.startswith(prefix) and f.endswith(".png"):
                filepath = os.path.join(output_dir, f)
                # Get dimensions via sips
                try:
                    result = subprocess.run(
                        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", filepath],
                        capture_output=True, text=True
                    )
                    lines = result.stdout.strip().split("\n")
                    w = int([l for l in lines if "pixelWidth" in l][0].split()[-1])
                    h = int([l for l in lines if "pixelHeight" in l][0].split()[-1])
                except Exception:
                    w, h = 0, 0

                # Normalize filename to our convention
                page_num = len(manifest) + 1
                new_name = f"{prefix}-{page_num:02d}.png"
                new_path = os.path.join(output_dir, new_name)
                if filepath != new_path:
                    os.rename(filepath, new_path)

                manifest.append({
                    "filename": new_name,
                    "page": page_num,
                    "width": w,
                    "height": h,
                })
        return manifest
    except FileNotFoundError:
        pass

    raise RuntimeError(
        "No PDF renderer available. Install PyMuPDF (pip3 install pymupdf) "
        "or poppler (brew install poppler)."
    )


def main():
    parser = argparse.ArgumentParser(description="Extract PDF pages as images")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--output-dir", default=".", help="Directory for output images")
    parser.add_argument("--prefix", default="slide", help="Filename prefix for images")
    parser.add_argument("--dpi", type=int, default=200, help="Resolution (default: 200)")
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(json.dumps({"error": f"File not found: {args.pdf_path}"}))
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    try:
        manifest = extract_with_fitz(args.pdf_path, args.output_dir, args.prefix, args.dpi)
    except ImportError:
        sys.stderr.write("PyMuPDF not found, trying pdftocairo fallback...\n")
        manifest = extract_with_sips(args.pdf_path, args.output_dir, args.prefix, args.dpi)

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
