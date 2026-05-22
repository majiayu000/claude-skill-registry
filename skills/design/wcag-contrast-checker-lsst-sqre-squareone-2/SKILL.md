---
name: wcag-contrast-checker
description: |
  Check WCAG color contrast ratios between two colors. Accepts any CSS color format
  (hex, rgb, rgba, hsl, hsla, named colors) and returns the contrast ratio along with
  WCAG compliance levels (AA/AAA for normal and large text).
allowed-tools:
  - Bash(uv run --script check_contrast.py:*)
---

# WCAG Contrast Checker

This skill checks the color contrast ratio between two colors to ensure they meet WCAG accessibility standards. It accepts colors in various CSS formats (hex, rgb, rgba, hsl, hsla, named colors) and returns the contrast ratio along with compliance levels for normal and large text.

### Supported Color Formats

- **Hex**: `#fff`, `#ffffff`, `#333`
- **RGB**: `rgb(255, 0, 0)`, `rgb(51, 51, 51)`
- **RGBA**: `rgba(255, 0, 0, 0.5)` (alpha is ignored for contrast calculation)
- **HSL**: `hsl(120, 100%, 50%)`
- **HSLA**: `hsla(120, 100%, 50%, 0.8)` (alpha is ignored)
- **Named colors**: `white`, `black`, `red`, `blue`, `lightgray`, etc.

## WCAG Standards

### Level AA (Minimum)

- **Normal text** (< 18pt or < 14pt bold): Requires **4.5:1** contrast ratio
- **Large text** (≥ 18pt or ≥ 14pt bold): Requires **3:1** contrast ratio

### Level AAA (Enhanced)

- **Normal text** (< 18pt or < 14pt bold): Requires **7:1** contrast ratio
- **Large text** (≥ 18pt or ≥ 14pt bold): Requires **4.5:1** contrast ratio

## Dependencies

- Python 3.8+
- `pip install colour>=0.1.5` (for CSS color parsing and manipulation)
- `uv` (for running the Python script)

Dependencies are automatically handled by `uv run` with inline script metadata.

## Examples

Check contrast between black text and white background:

```
uv run --script check_contrast.py --foreground "#000" --background "#fff"
```

Check contrast using named colors:

```
uv run --script check_contrast.py --foreground "darkblue" --background "lightgray"
```

Check contrast using rgb format:

```
uv run --script check_contrast.py --foreground "rgb(51, 51, 51)" --background "rgb(255, 255, 255)"
```

## Tips

- The tool accepts any valid CSS color format including hex, rgb, rgba, hsl, hsla, and named colors
- WCAG AA requires 4.5:1 for normal text and 3:1 for large text
- WCAG AAA requires 7:1 for normal text and 4.5:1 for large text
- Large text is defined as 18pt+ or 14pt+ bold

## Troubleshooting

### Invalid Color Format

If you get a color parsing error, ensure your color is in a valid CSS format:

```bash
# ✗ Wrong
--foreground "333"

# ✓ Correct
--foreground "#333"
```

## Technical Details

The script implements the WCAG 2.0 contrast ratio formula:

1. **Relative Luminance Calculation**: Converts sRGB values to linear RGB and applies the luminance formula
2. **Contrast Ratio**: `(L1 + 0.05) / (L2 + 0.05)` where L1 is the lighter color
3. **Compliance Check**: Compares ratio against WCAG thresholds
