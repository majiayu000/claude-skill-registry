---
name: wpf-styling
description: 'Define and evolve WPF XAML styling for the widget host app: control
  styles, templates, visual states, typography, and theme variants. Use when working
  in `App.xaml`, theme dictionaries, `Styles/*.xaml'
---

---
name: wpf-styling
description: Define and evolve WPF XAML styling for the widget host app: control styles, templates, visual states, typography, and theme variants. Use when working in `App.xaml`, theme dictionaries, `Styles/*.xaml`, or control templates to achieve the Fluent-inspired design system with Light/Dark themes.
---

# Wpf Styling

## Overview

Standardize WPF styling and theming so views stay lean and visuals remain consistent across the shell and widget windows.

## Constraints

- Native WPF styles/templates (no WinUI/Windows App SDK)
- Fluent-inspired design system
- Light/Dark themes via ResourceDictionaries
- .NET 8 app

## Definition of done (DoD)

- No hardcoded colors in view XAML (use theme brushes)
- New controls use existing base styles or extend them
- Typography uses defined text styles (Body, Title, Caption)
- Both Light and Dark themes tested visually
- Styles organized: typography in Typography.xaml, controls in Controls.xaml, colors in Themes/*.xaml

## Workflow

1. Identify the target style: base control style, derived variant, or template.
2. Check existing theme/typography resources before creating new ones.
3. Add/adjust styles in `Styles/*.xaml` and keep theme colors in `Themes/*.xaml`.
4. Keep view XAML clean by using keyed styles and implicit styles when safe.

## Style structure

- `Styles/Typography.xaml` for fonts, sizes, weights.
- `Styles/Controls.xaml` for base control styles.
- `Themes/Light.xaml` and `Themes/Dark.xaml` for brushes only.

## Control templates and visual states

- Use `VisualStateManager` only when state transitions are needed.
- Prefer triggers and setters for simple states.
- Keep templates small and parameterize via brushes and thickness resources.

## Typography

- Define a small set of text styles (Body, Title, Caption).
- Apply styles via resource keys to avoid duplicating font settings.

## References

- `references/typography.md` for font scales and text styles.
- `references/control-styles.md` for base button/textbox/list styles.
- `references/theme-brushes.md` for Light/Dark resource keys.
