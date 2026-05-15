#!/usr/bin/env python3
"""Validate a grainient template HTML file for structural correctness."""

import re
import sys
from pathlib import Path


CHECKS = [
    # ─── Required structure ─────────────────────────────────────────
    {
        "name": "Viewport meta tag",
        "pattern": r'<meta\s+[^>]*viewport[^>]*>',
        "required": True,
    },
    {
        "name": "Inter font import or declaration",
        "pattern": r"fonts\.googleapis\.com.*Inter|font-family:.*Inter|@font-face[^}]*Inter",
        "required": True,
    },
    {
        "name": "CSS custom properties (--grn-* tokens)",
        "pattern": r"--grn-(bg|surface|accent|text|border)",
        "required": True,
    },
    {
        "name": "Dark background (--grn-bg or #000)",
        "pattern": r"background:\s*var\(--grn-bg\)|background:\s*#000",
        "required": True,
    },
    {
        "name": "Font smoothing (antialiased)",
        "pattern": r"-webkit-font-smoothing:\s*antialiased",
        "required": True,
    },
    {
        "name": "Custom scrollbar styles",
        "pattern": r"::-webkit-scrollbar|scrollbar-width",
        "required": False,
    },
    {
        "name": "prefers-reduced-motion media query",
        "pattern": r"prefers-reduced-motion",
        "required": True,
    },
    {
        "name": "Spring cubic-bezier preset",
        "pattern": r"cubic-bezier\(0\.34,\s*1\.56|--grn-spring",
        "required": True,
    },
    {
        "name": "Window resize handler or responsive CSS",
        "pattern": r"addEventListener\s*\(\s*['\"]resize['\"]|@media\s*\(",
        "required": True,
    },
    # ─── Mode-specific (optional — pass if mode not detected) ─────
    {
        "name": "WebGL context (shader modes)",
        "pattern": r"getContext\s*\(\s*['\"]webgl2?['\"]|WebGL2RenderingContext",
        "required": False,
    },
    {
        "name": "requestAnimationFrame (animated modes)",
        "pattern": r"requestAnimationFrame\s*\(",
        "required": False,
    },
    {
        "name": "Wheel event listener (smooth scroll)",
        "pattern": r"addEventListener\s*\(\s*['\"]wheel['\"]",
        "required": False,
    },
    {
        "name": "translateY animation (ticker)",
        "pattern": r"translateY\s*\(",
        "required": False,
    },
    {
        "name": "CSS Grid layout (bento)",
        "pattern": r"grid-template-columns|display:\s*grid",
        "required": False,
    },
    {
        "name": "Overflow clip on containers",
        "pattern": r"overflow:\s*clip|overflow:\s*hidden",
        "required": False,
    },
    {
        "name": "Gradient CTA button",
        "pattern": r"linear-gradient\(180deg.*#EBFFB4|linear-gradient\(180deg.*EBFFB4",
        "required": False,
    },
    {
        "name": "Box shadow with glow layers",
        "pattern": r"box-shadow:[\s\S]*?rgba\(194,\s*241,\s*60|box-shadow:[\s\S]*?--grn-accent",
        "required": False,
    },
    {
        "name": "Backdrop filter glassmorphism",
        "pattern": r"backdrop-filter:\s*(var\(--grn-blur|blur\()",
        "required": False,
    },
    {
        "name": "Vignette overlay divs",
        "pattern": r"vignette|linear-gradient\(0deg,\s*transparent",
        "required": False,
    },
    # ─── Anti-pattern checks (inverted — must NOT match) ──────────
    {
        "name": "No React/Vue/Svelte/Angular imports",
        "pattern": r"from\s+['\"]react['\"]|from\s+['\"]vue['\"]|from\s+['\"]svelte|from\s+['\"]@angular",
        "required": True,
        "invert": True,
    },
    {
        "name": "No setInterval for animation",
        "pattern": r"setInterval\s*\([^)]*(?:animate|render|draw|update|tick|frame)",
        "required": True,
        "invert": True,
    },
    {
        "name": "No ease timing function",
        "pattern": r"transition[^;]*:\s*[^;]*\bease\b[^-]",
        "required": True,
        "invert": True,
    },
]


def validate(filepath: str) -> int:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}")
        return 1

    content = path.read_text(encoding="utf-8", errors="replace")
    if not content.strip():
        print(f"Error: File is empty: {filepath}")
        return 1

    print(f"Validating: {path.name}")
    print("=" * 50)

    passed = 0
    failed = 0
    optional_found = 0
    optional_missing = 0

    for check in CHECKS:
        match = re.search(check["pattern"], content, re.IGNORECASE)
        inverted = check.get("invert", False)
        ok = (match is None) if inverted else (match is not None)

        if ok:
            print(f"  \u2713 {check['name']}")
            if check["required"]:
                passed += 1
            else:
                optional_found += 1
        elif check["required"]:
            label = "FORBIDDEN PATTERN" if inverted else "MISSING"
            print(f"  \u2717 {check['name']} ({label})")
            failed += 1
        else:
            print(f"  ~ {check['name']} (optional)")
            optional_missing += 1

    required_total = passed + failed
    print()
    print(f"Required: {passed}/{required_total} passed")
    print(f"Optional: {optional_found} found, {optional_missing} skipped")
    print()

    if failed > 0:
        print(f"FAIL: {failed} required check(s) failed")
        return 1
    else:
        print("PASS: All required checks satisfied")
        return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <html-file> [html-file ...]")
        print(f"       {sys.argv[0]} assets/templates/*.html")
        sys.exit(1)

    exit_code = 0
    for filepath in sys.argv[1:]:
        result = validate(filepath)
        if result != 0:
            exit_code = 1
        print()

    sys.exit(exit_code)
