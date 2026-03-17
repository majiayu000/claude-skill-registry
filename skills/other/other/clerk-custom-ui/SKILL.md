---
name: clerk-custom-ui
description: Customize Clerk component appearance - themes, layout, colors, fonts, CSS. Use for appearance styling, visual customization, branding.
allowed-tools: WebFetch
license: MIT
metadata:
  author: clerk
  version: "1.0.0"
---

# Component Customization

> **Prerequisite**: Ensure `ClerkProvider` wraps your app. See `setup/`.

## Component Customization Options

| Task | Documentation |
|------|---------------|
| Appearance prop overview | https://clerk.com/docs/nextjs/guides/customizing-clerk/appearance-prop/overview |
| Layout (structure, logo, buttons) | https://clerk.com/docs/nextjs/guides/customizing-clerk/appearance-prop/layout |
| Themes (pre-built dark/light) | https://clerk.com/docs/nextjs/guides/customizing-clerk/appearance-prop/themes |
| Variables (colors, fonts, spacing) | https://clerk.com/docs/nextjs/guides/customizing-clerk/appearance-prop/variables |
| CAPTCHA configuration | https://clerk.com/docs/nextjs/guides/customizing-clerk/appearance-prop/captcha |
| Bring your own CSS | https://clerk.com/docs/nextjs/guides/customizing-clerk/appearance-prop/bring-your-own-css |

## Appearance Pattern

```typescript
<SignIn
  appearance={{
    variables: {
      colorPrimary: '#0000ff',
      borderRadius: '0.5rem',
    },
    layout: {
      logoImageUrl: '/logo.png',
      socialButtonsVariant: 'iconButton',
    },
  }}
/>
```

### variables (colors, typography, borders)

| Property | Description |
|----------|-------------|
| `colorPrimary` | Primary color throughout |
| `colorBackground` | Background color |
| `borderRadius` | Border radius (default: `0.375rem`) |

### layout (structure, logo, social buttons)

| Property | Description |
|----------|-------------|
| `logoImageUrl` | URL to custom logo |
| `socialButtonsVariant` | `'blockButton'` \| `'iconButton'` \| `'auto'` |
| `socialButtonsPlacement` | `'top'` \| `'bottom'` |

## shadcn Theme

**If the project has `components.json`** (shadcn/ui installed), use the shadcn theme:

```typescript
import { shadcn } from '@clerk/themes'

<ClerkProvider
  appearance={{
    theme: shadcn,
  }}
/>
```

Also import shadcn CSS in your global.css:
```css
@import 'tailwindcss';
@import '@clerk/themes/shadcn.css';
```
## Workflow

1. Identify customization needs (colors, layout, theme, CSS)
2. WebFetch the appropriate documentation from table above
3. Follow official code examples from the docs
4. Apply appearance prop to your Clerk components

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Colors not applying | Use `colorPrimary` not `primaryColor` |
| Logo not showing | Put `logoImageUrl` inside `layout: {}` |
| Social buttons wrong | Add `socialButtonsVariant: 'iconButton'` in `layout` |
| Styling not working | Use appearance prop, not direct CSS (unless with bring-your-own-css) |
