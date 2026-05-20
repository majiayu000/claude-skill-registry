---
name: color-accessibility
description: Design color palettes that are accessible to all users including those with color blindness. Ensure sufficient contrast, meaningful use of color, and inclusive design.
---

# Color Accessibility

## Overview

Accessible color design ensures all users, including those with color vision deficiency, can access and understand information.

## When to Use

- Creating color palettes
- Designing data visualizations
- Testing interface designs
- Status indicators and alerts
- Form validation states
- Charts and graphs

## Instructions

### 1. **Color Contrast Standards**

```yaml
WCAG Contrast Ratios:

WCAG AA (Minimum):
  - Normal text: 4.5:1
  - Large text (18pt+): 3:1
  - UI components & graphical elements: 3:1
  - Focus indicators: 3:1

WCAG AAA (Enhanced):
  - Normal text: 7:1
  - Large text: 4.5:1
  - Better for accessibility

---

Testing Contrast:

Tools:
  - WebAIM Contrast Checker
  - Color Contrast Analyzer
  - Figma plugins
  - Browser DevTools

Formula (WCAG):
  Contrast = (L1 + 0.05) / (L2 + 0.05)
  Where L = relative luminance

Example Pairs:

Good (Pass AA):
  - Black (#000000) on White (#FFFFFF) = 21:1 ✓
  - White on Dark Blue (#003366) = 12.6:1 ✓
  - Dark Gray (#333333) on Light Gray (#EEEEEE) = 10:1 ✓

Poor (Fail):
  - Light Gray (#CCCCCC) on White (#FFFFFF) = 1.3:1 ✗
  - Yellow (#FFFF00) on White (#FFFFFF) = 1.07:1 ✗
```

### 2. **Color Vision Deficiency Simulation**

```python
# Design for color vision deficiency

class ColorAccessibility:
    COLOR_DEFICIENCY_TYPES = {
        'Protanopia': 'Red-blind (1% male)',
        'Deuteranopia': 'Green-blind (1% male)',
        'Tritanopia': 'Blue-yellow blind (very rare)',
        'Monochromacy': 'Complete color blindness (very rare)'
    }

    def simulate_vision_deficiency(self, color, deficiency_type):
        """Simulate how color appears to different eyes"""
        # Color blind simulation
        simulated_colors = {
            'normal': color,
            'protanopia': self.apply_protanopia_filter(color),
            'deuteranopia': self.apply_deuteranopia_filter(color),
            'tritanopia': self.apply_tritanopia_filter(color)
        }
        return simulated_colors

    def check_palette_accessibility(self, color_palette):
        """Validate entire palette for accessibility"""
        issues = []

        # Check contrast ratios
        for color_pair in self.generate_pairs(color_palette):
            contrast = self.calculate_contrast(color_pair[0], color_pair[1])
            if contrast < 4.5:
                issues.append({
                    'type': 'Low contrast',
                    'colors': color_pair,
                    'ratio': contrast,
                    'severity': 'Critical'
                })

        # Check color blind differentiation
        for deficiency in self.COLOR_DEFICIENCY_TYPES:
            simulated = self.simulate_for_deficiency(color_palette, deficiency)
            if not self.are_colors_distinguishable(simulated):
                issues.append({
                    'type': 'Color blindness',
                    'deficiency': deficiency,
                    'severity': 'High'
                })

        return {
            'palette': color_palette,
            'issues': issues,
            'is_accessible': len(issues) == 0,
            'recommendations': self.generate_recommendations(issues)
        }

    def generate_recommendations(self, issues):
        """Suggest palette improvements"""
        return [
            'Use patterns or icons to differentiate (not just color)',
            'Increase contrast ratios',
            'Use tested accessible color combinations',
            'Test with color blindness simulator before launch'
        ]
```

### 3. **Accessible Color Usage**

```yaml
Color Usage Guidelines:

Status Indicators:

Error:
  Color: #D32F2F (red)
  Contrast: 4.5:1 minimum
  Additional: Error icon, text "Error"
  Don't: Use ONLY red, no other indication

Success:
  Color: #388E3C (green)
  Contrast: 4.5:1 minimum
  Additional: Checkmark icon, text "Success"
  Don't: Use ONLY green

Warning:
  Color: #F57C00 (orange)
  Contrast: 4.5:1 minimum
  Additional: Warning icon, text "Warning"
  Don't: Use ONLY orange

Info:
  Color: #1976D2 (blue)
  Contrast: 4.5:1 minimum
  Additional: Info icon, text "Info"
  Don't: Use ONLY blue

---

Data Visualization:

Charts & Graphs:
  - Use 8+ color combinations for color blindness
  - Include patterns or textures
  - Label elements directly (not legend only)
  - Use colorblind-friendly palettes

Recommended Palettes:
  - ColorBrewer (designed for accessibility)
  - Okabe-Ito palette
  - Paul Tol colors

Heat Maps:
  - Sequential palettes only
  - Avoid red-green combinations
  - Test with simulator

---

UI Component States:

Button States:
  - Default: Primary color
  - Hover: Slightly darker
  - Disabled: Gray with reduced contrast
  - Focus: Outline indicator (not color alone)
  - Active: Darker shade

Form Validation:
  - Invalid: Red + error icon + message
  - Valid: Green + checkmark icon (optional)
  - Required: No special color, use text label

Interactive Elements:
  - Focus: Visible outline or ring
  - Selected: Checkmark or checkmark icon + color
  - Hover: Underline + color change
  - Don't: Use color alone to indicate state
```

### 4. **Testing & Validation**

```javascript
// Test color accessibility

class ColorAccessibilityTesting {
  testColorPalette(palette) {
    return {
      contrast_test: this.validateContrast(palette),
      colorblind_test: this.simulateColorBlindness(palette),
      usage_test: this.testColorUsage(palette),
      tools_used: [
        'WebAIM Contrast Checker',
        'Color Oracle simulator',
        'WAVE accessibility checker'
      ]
    };
  }

  validateContrast(palette) {
    const results = [];

    for (let color of palette) {
      const contrast = this.calculateLuminance(color);
      results.push({
        color: color,
        luminance: contrast,
        passes_aa: contrast >= 4.5,
        passes_aaa: contrast >= 7.0
      });
    }

    return results;
  }

  simulateColorBlindness(palette) {
    return {
      protanopia: this.convertToProtanopia(palette),
      deuteranopia: this.convertToDeuteranopia(palette),
      tritanopia: this.convertToTritanopia(palette),
      all_distinguishable: this.checkDistinguishability(palette)
    };
  }
}
```

## Best Practices

### ✅ DO
- Ensure 4.5:1 contrast minimum (WCAG AA)
- Test with color blindness simulator
- Use patterns or icons with color
- Label states with text, not color alone
- Test with real users with color blindness
- Document color usage in design system
- Choose accessible color palettes
- Use sequential colors for ordered data
- Validate all color combinations
- Include focus indicators

### ❌ DON'T
- Use color alone to convey information
- Create low-contrast text
- Assume users see colors correctly
- Use red-green combinations
- Forget about focus states
- Mix too many colors (>5-8)
- Use pure red and pure green together
- Skip contrast testing
- Assume AA is sufficient (AAA better)
- Ignore color blindness in testing

## Color Accessibility Tips

- 8% of males have red-green color blindness
- Deuteranopia and protanopia are most common
- Always test with simulator (Color Oracle, Coblis)
- Use patterns to differentiate, not just color
- Test colors in context (not in isolation)
