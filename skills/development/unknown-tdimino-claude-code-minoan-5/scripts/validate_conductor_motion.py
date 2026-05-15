#!/usr/bin/env python3
"""
Conductor Motion Validator

Validates that an HTML file follows conductor-motion conventions:
viewport meta, --cm-* tokens, no frameworks, rAF usage, reduced-motion,
performance.now(), font-smoothing, aria-hidden, visibility API, etc.

Usage:
    python3 validate_conductor_motion.py output.html
    python3 validate_conductor_motion.py *.html
"""

import re
import sys
from pathlib import Path

CHECKS = []


def check(name, severity="error"):
    def decorator(fn):
        CHECKS.append((name, severity, fn))
        return fn
    return decorator


@check("viewport-meta")
def check_viewport(html):
    if '<meta name="viewport"' not in html:
        return "Missing <meta name=\"viewport\"> tag"


@check("cm-tokens")
def check_cm_tokens(html):
    if "--cm-" not in html:
        return "No --cm-* CSS custom properties found"


@check("no-framework-imports")
def check_no_frameworks(html):
    frameworks = ["react", "vue", "svelte", "angular", "jquery"]
    for fw in frameworks:
        if re.search(rf'<script[^>]*{fw}[^>]*>', html, re.IGNORECASE):
            return f"Framework import detected: {fw}"


@check("raf-present", severity="warning")
def check_raf(html):
    has_continuous_loop = bool(re.search(r"function\s+tick\s*\((?:now|timestamp)", html))
    if has_continuous_loop and "requestAnimationFrame" not in html:
        return "Continuous animation loop found but no requestAnimationFrame — expected for frame-synced animation"


@check("reduced-motion")
def check_reduced_motion(html):
    if "prefers-reduced-motion" not in html:
        return "Missing @media (prefers-reduced-motion: reduce) — required for accessibility"


@check("performance-now")
def check_performance_now(html):
    if "performance.now()" not in html and "performance.now" not in html:
        if re.search(r"function\s+tick|rAF|requestAnimationFrame", html):
            if "Date.now()" in html:
                return "Using Date.now() in animation code — use performance.now() instead"


@check("font-smoothing")
def check_font_smoothing(html):
    if "-webkit-font-smoothing" not in html:
        return "Missing -webkit-font-smoothing: antialiased"


@check("aria-hidden-cursors")
def check_aria_cursors(html):
    cursor_patterns = re.findall(r'class="[^"]*cursor[^"]*"', html)
    if cursor_patterns:
        if 'aria-hidden="true"' not in html:
            return "Cursor elements found but no aria-hidden=\"true\" on decorative cursors"


@check("visibility-api")
def check_visibility(html):
    has_animation_loop = bool(re.search(r"setTimeout|setInterval|requestAnimationFrame", html))
    if has_animation_loop and "visibilitychange" not in html and "document.hidden" not in html:
        return "Animation loops present but no Visibility API integration (document.hidden / visibilitychange)"


@check("no-transition-all", severity="error")
def check_transition_all(html):
    matches = re.findall(r"transition:\s*all\b", html)
    if matches:
        return f"Found 'transition: all' ({len(matches)} occurrence{'s' if len(matches) > 1 else ''}) — explicitly list each property"


@check("no-setinterval-animation", severity="warning")
def check_setinterval(html):
    matches = re.findall(r"setInterval\s*\(", html)
    if matches:
        if re.search(r"setInterval[^;]*(?:\.style\.transform|\.style\.opacity|translate)", html, re.DOTALL):
            return "setInterval used for visual animation — use requestAnimationFrame instead"


@check("no-layout-animation", severity="error")
def check_layout_animation(html):
    layout_props = ["height", "top", "left", "margin", "padding"]
    script_sections = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL)
    for script in script_sections:
        for prop in layout_props:
            if re.search(rf"\.style\.{prop}\s*=", script):
                return f"Animating layout property '{prop}' in JS — use transform/opacity instead"
    for script in script_sections:
        has_width_in_raf = re.search(r"function\s+tick\s*\([^)]*\)[^}]*\.style\.width\s*=[^}]*requestAnimationFrame\(tick\)", script, re.DOTALL)
        if has_width_in_raf:
            return "Animating 'width' inside rAF loop — use transform: scaleX() instead"


@check("geist-font", severity="warning")
def check_geist_font(html):
    if "Geist" not in html and "geist" not in html:
        return "Geist font not referenced — expected as primary font"


@check("double-init-guard", severity="warning")
def check_double_init(html):
    has_init = bool(re.search(r"function\s+init|\.forEach\(|querySelectorAll", html))
    if has_init and "initDone" not in html and "Init" not in html:
        return "No double-initialization guard found (dataset.*Init check)"


@check("no-empty-visibility-handler", severity="warning")
def check_empty_visibility(html):
    if re.search(r"visibilitychange['\"],\s*\(\)\s*=>\s*\{\s*\}", html):
        return "Empty visibilitychange handler — must actually pause/resume animation loops"


@check("no-innerhtml-with-variables", severity="warning")
def check_innerhtml(html):
    script_sections = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL)
    for script in script_sections:
        if re.search(r"\.innerHTML\s*=\s*`[^`]*\$\{", script):
            return "Template literal assigned to innerHTML with interpolated variables — use textContent + DOM construction"
        for line in script.split("\n"):
            if ".innerHTML" in line and "=" in line.split(".innerHTML")[1][:5]:
                rhs = line.split(".innerHTML")[1].split("=", 1)[1].strip() if "=" in line.split(".innerHTML")[1] else ""
                if "+" in rhs and "<" in rhs:
                    return "String concatenation with HTML assigned to innerHTML — use textContent + DOM construction"


@check("no-pure-white-text", severity="warning")
def check_pure_white(html):
    style_sections = re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL)
    for style in style_sections:
        if re.search(r"color:\s*#[Ff]{6}\b", style):
            return "Pure white #FFFFFF used as text color — use var(--cm-text) for less eye strain in dark mode"


def validate_file(filepath: Path) -> list[tuple[str, str, str]]:
    html = filepath.read_text()
    results = []
    for name, severity, fn in CHECKS:
        msg = fn(html)
        if msg:
            results.append((name, severity, msg))
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_conductor_motion.py <file.html> [file2.html ...]")
        sys.exit(1)

    files = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.is_file():
            files.append(p)
        else:
            expanded = list(Path(".").glob(arg))
            if expanded:
                files.extend(expanded)
            else:
                print(f"Warning: {arg} not found, skipping")

    if not files:
        print("No files to validate")
        sys.exit(1)

    total_errors = 0
    total_warnings = 0

    for filepath in files:
        results = validate_file(filepath)
        errors = [(n, s, m) for n, s, m in results if s == "error"]
        warnings = [(n, s, m) for n, s, m in results if s == "warning"]

        if not results:
            print(f"  PASS  {filepath}")
        else:
            print(f"\n  {'FAIL' if errors else 'WARN'}  {filepath}")
            for name, severity, msg in results:
                icon = "x" if severity == "error" else "!"
                print(f"    [{icon}] {name}: {msg}")

        total_errors += len(errors)
        total_warnings += len(warnings)

    print(f"\n{'=' * 50}")
    print(f"Files: {len(files)}  Errors: {total_errors}  Warnings: {total_warnings}")

    if total_errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
