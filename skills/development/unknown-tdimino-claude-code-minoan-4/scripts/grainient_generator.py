#!/usr/bin/env python3
"""
Grainient Generator

Generate customized dark-mode landing pages with grainient.supply's 16 visual effects.

Usage:
    python grainient_generator.py --mode hero --output hero.html
    python grainient_generator.py --mode bento --accent "#FF6B35" --output showcase.html
    python grainient_generator.py --mode page --output landing.html
    python grainient_generator.py --mode catalog --output catalog.html
"""

import argparse
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
TEMPLATES_DIR = SCRIPT_DIR.parent / "assets" / "templates"

MODES = {
    "hero": "hero-section.html",
    "bento": "bento-showcase.html",
    "ticker": "ticker-landing.html",
    "page": "dark-page.html",
    "catalog": "effects-catalog.html",
}

# Default grainient color tokens
DEFAULTS = {
    "accent": "#C2F13C",
    "bg": "#000000",
    "surface": "#141414",
    "elevated": "#1A1A1A",
}


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Convert hex color to rgba string."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def apply_theme(content: str, args) -> str:
    """Replace color tokens in template content with user-specified values."""

    # Only modify if non-default values provided
    if args.accent != DEFAULTS["accent"]:
        # Replace hex accent
        content = content.replace("#C2F13C", args.accent)
        content = content.replace("#c2f13c", args.accent.lower())

        # Replace rgb accent
        content = content.replace("rgb(194, 241, 60)", f"rgb({int(args.accent[1:3], 16)}, {int(args.accent[3:5], 16)}, {int(args.accent[5:7], 16)})")

        # Replace rgba accent variants
        content = content.replace(
            "rgba(194, 241, 60, 0.4)",
            hex_to_rgba(args.accent, 0.4)
        )
        content = content.replace(
            "rgba(194, 241, 60, 0.2)",
            hex_to_rgba(args.accent, 0.2)
        )
        content = content.replace(
            "rgba(194, 241, 60, 0.3)",
            hex_to_rgba(args.accent, 0.3)
        )

        # Replace lighter accent in gradient buttons
        # Compute a lighter version for the gradient top
        r = int(args.accent[1:3], 16)
        g = int(args.accent[3:5], 16)
        b = int(args.accent[5:7], 16)
        light_r = min(255, r + 60)
        light_g = min(255, g + 40)
        light_b = min(255, b + 120)
        light_hex = f"#{light_r:02X}{light_g:02X}{light_b:02X}"
        content = content.replace("#EBFFB4", light_hex)

        # Replace logo/icon gradient stops
        content = content.replace("#AADB1F", args.accent)

    if args.bg != DEFAULTS["bg"]:
        content = content.replace("--grn-bg: #000000", f"--grn-bg: {args.bg}")

    if args.surface != DEFAULTS["surface"]:
        content = content.replace("--grn-surface: #141414", f"--grn-surface: {args.surface}")
        content = content.replace("rgb(20, 20, 20)", f"rgb({int(args.surface[1:3], 16)}, {int(args.surface[3:5], 16)}, {int(args.surface[5:7], 16)})")

    return content


def generate(args) -> str:
    """Load template and apply customizations."""

    template_name = MODES.get(args.mode)
    if not template_name:
        print(f"Error: Unknown mode '{args.mode}'. Available: {', '.join(MODES.keys())}")
        sys.exit(1)

    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        print(f"Error: Template not found: {template_path}")
        print(f"Available templates: {', '.join(f.name for f in TEMPLATES_DIR.glob('*.html'))}")
        sys.exit(1)

    content = template_path.read_text(encoding="utf-8")
    content = apply_theme(content, args)

    # Update title
    title_map = {
        "hero": "Grainient Hero",
        "bento": "Grainient Showcase",
        "ticker": "Grainient Gallery",
        "page": "Grainient Landing Page",
        "catalog": "Grainient Effects Catalog",
    }
    content = re.sub(
        r"<title>.*?</title>",
        f"<title>{title_map.get(args.mode, 'Grainient')}</title>",
        content,
    )

    return content


def main():
    parser = argparse.ArgumentParser(
        description="Generate grainient-style dark-mode landing pages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --mode hero --output hero.html
  %(prog)s --mode bento --accent "#FF6B35" --output showcase.html
  %(prog)s --mode page --output landing.html
  %(prog)s --mode catalog --output catalog.html
        """,
    )

    parser.add_argument(
        "--mode",
        required=True,
        choices=list(MODES.keys()),
        help="Output mode: hero, bento, ticker, page, catalog",
    )
    parser.add_argument(
        "--accent",
        default=DEFAULTS["accent"],
        help=f"Accent hex color (default: {DEFAULTS['accent']})",
    )
    parser.add_argument(
        "--bg",
        default=DEFAULTS["bg"],
        help=f"Background hex color (default: {DEFAULTS['bg']})",
    )
    parser.add_argument(
        "--surface",
        default=DEFAULTS["surface"],
        help=f"Surface hex color (default: {DEFAULTS['surface']})",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    # Validate hex colors
    for name in ("accent", "bg", "surface"):
        val = getattr(args, name)
        if not re.match(r"^#[0-9A-Fa-f]{6}$", val):
            print(f"Error: --{name} must be a 6-digit hex color (e.g., #C2F13C)")
            sys.exit(1)

    content = generate(args)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        print(f"Generated: {output_path} ({len(content):,} bytes)")
    else:
        print(content)


if __name__ == "__main__":
    main()
