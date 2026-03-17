---
name: umbraco-theme
description: Implement themes in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Theme

## What is it?
Themes in Umbraco allow you to customize the visual appearance of the backoffice. They can override CSS custom properties to change colors, typography, and other visual elements. This enables dark mode, high contrast, custom branding, or any other visual theme. Users can select themes from their profile settings.

## Documentation
Always fetch the latest docs before implementing:

- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry
- **Themes**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types

## Related Foundation Skills

- **Extension Registry**: When registering themes
  - Reference skill: `umbraco-extension-registry`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What colors? Dark/light? Brand colors?
3. **Generate files** - Create manifest + CSS based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestTheme } from '@umbraco-cms/backoffice/extension-registry';

export const manifests: Array<ManifestTheme> = [
  {
    type: 'theme',
    alias: 'My.Theme.Dark',
    name: 'My Dark Theme',
    css: () => import('./dark-theme.css?inline'),
  },
];
```

### CSS Theme File (dark-theme.css)
```css
:root {
  /* Background colors */
  --uui-color-surface: #1e1e1e;
  --uui-color-surface-alt: #252526;
  --uui-color-surface-emphasis: #2d2d30;

  /* Text colors */
  --uui-color-text: #d4d4d4;
  --uui-color-text-alt: #9d9d9d;

  /* Primary/accent colors */
  --uui-color-default: #3c3c3c;
  --uui-color-positive: #4ec9b0;
  --uui-color-warning: #dcdcaa;
  --uui-color-danger: #f14c4c;

  /* Interactive colors */
  --uui-color-interactive: #569cd6;
  --uui-color-interactive-emphasis: #9cdcfe;

  /* Border colors */
  --uui-color-border: #3c3c3c;
  --uui-color-border-standalone: #454545;

  /* Header */
  --uui-color-header-surface: #1e1e1e;
  --uui-color-header-contrast: #d4d4d4;

  /* Selected states */
  --uui-color-selected: #264f78;
  --uui-color-selected-contrast: #ffffff;
}
```

### High Contrast Theme (high-contrast-theme.css)
```css
:root {
  /* High contrast for accessibility */
  --uui-color-surface: #000000;
  --uui-color-surface-alt: #0a0a0a;

  --uui-color-text: #ffffff;
  --uui-color-text-alt: #e0e0e0;

  --uui-color-border: #ffffff;
  --uui-color-border-standalone: #ffffff;

  --uui-color-interactive: #ffff00;
  --uui-color-interactive-emphasis: #00ffff;

  --uui-color-focus: #ff00ff;
}
```

### Brand Theme (brand-theme.css)
```css
:root {
  /* Custom brand colors */
  --uui-color-current: #your-brand-primary;
  --uui-color-current-contrast: #ffffff;
  --uui-color-current-standalone: #your-brand-darker;

  /* Header with brand color */
  --uui-color-header-surface: #your-brand-primary;
  --uui-color-header-contrast: #ffffff;

  /* Interactive elements use brand */
  --uui-color-interactive: #your-brand-primary;
  --uui-color-interactive-emphasis: #your-brand-lighter;
}
```

## Interface Reference

```typescript
interface ManifestTheme extends ManifestPlainCss {
  type: 'theme';
}

interface ManifestPlainCss {
  type: string;
  alias: string;
  name: string;
  css: () => Promise<{ default: string } | string>;
}
```

## Common CSS Custom Properties

### Surfaces
- `--uui-color-surface` - Main background
- `--uui-color-surface-alt` - Alternative background
- `--uui-color-surface-emphasis` - Emphasized background

### Text
- `--uui-color-text` - Primary text
- `--uui-color-text-alt` - Secondary text

### Status Colors
- `--uui-color-positive` - Success states
- `--uui-color-warning` - Warning states
- `--uui-color-danger` - Error/danger states

### Interactive
- `--uui-color-interactive` - Links, buttons
- `--uui-color-interactive-emphasis` - Hover states
- `--uui-color-selected` - Selected items

### Header
- `--uui-color-header-surface` - Header background
- `--uui-color-header-contrast` - Header text

## Best Practices

- Test themes with all UI components
- Ensure sufficient contrast for accessibility
- Consider dark/light mode variants
- Use CSS custom properties for consistency

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
