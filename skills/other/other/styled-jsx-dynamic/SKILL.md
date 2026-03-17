---
name: styled-jsx-dynamic
description: Implement dynamic styling in styled-jsx using best practices (CSS variables, className toggling, safe interpolations). Use for hover/active state, variant switches, theming, and runtime sizes/colors.
argument-hint: "[ComponentName or path] [dynamic styling requirement]"
---

# styled-jsx Dynamic Styling Skill

Implement dynamic styles without sacrificing maintainability or safety.

## Prefer this order

1) CSS variables set via style prop
   - style={{ "--accent": color } as React.CSSProperties }
2) className toggling
   - data-state, data-variant
3) Interpolated template literals inside <style jsx> only when needed
   - Keep interpolations small, numeric, or enumerated
   - Never interpolate untrusted strings into selectors or urls

## Output expectations

- Update the component.
- Provide an explanation of why the chosen strategy is best.
- Include minimal test coverage for the dynamic behavior.

## Example patterns

- CSS vars:
   ```css
   <div style={{ "--gap": `${gap}px` } as React.CSSProperties } />
   <style jsx>{`div{ gap: var(--gap, 8px); }`}</style>
   ```

- class toggling:
   ```css
   <div data-open={open ? "true" : "false"} />
   <style jsx>{`div[data-open="true"]{ ... }`}</style>
   ```
