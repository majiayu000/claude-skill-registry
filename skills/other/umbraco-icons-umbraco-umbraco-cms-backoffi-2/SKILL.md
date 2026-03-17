---
name: umbraco-icons
description: Implement custom icons in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Icons

## What is it?
Icons are custom visual elements that extension authors can register for use throughout the Umbraco backoffice. Custom icons are registered through the manifest and can then be used in any extension that accepts an icon property. Icons are defined as SVG content exported from JavaScript modules.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/icons
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Reference Example

The Umbraco source includes a working example:

**Location**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/icons/`

This example demonstrates how to register and use custom SVG icons. Study this for production patterns.

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What icons needed? SVG source available?
3. **Generate files** - Create manifest + icon files based on latest docs
4. **Explain** - Show what was created and how to use the icons

## Minimal Examples

### Manifest (umbraco-package.json)
```json
{
  "name": "My Icons Package",
  "extensions": [
    {
      "type": "icons",
      "alias": "My.Icons",
      "name": "My Custom Icons",
      "js": "/App_Plugins/MyPackage/icons.js"
    }
  ]
}
```

### Icons Registry (icons.ts)
```typescript
export default [
  {
    name: 'my-custom-icon',
    path: () => import('./icons/my-custom-icon.js'),
  },
  {
    name: 'my-other-icon',
    path: () => import('./icons/my-other-icon.js'),
  },
];
```

### Icon File (icons/my-custom-icon.ts)
```typescript
export default `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
</svg>`;
```

### Using Custom Icons
```typescript
// In any extension manifest
const manifest = {
  type: 'headerApp',
  kind: 'button',
  alias: 'My.HeaderApp',
  name: 'My App',
  meta: {
    label: 'My App',
    icon: 'my-custom-icon',  // Use your custom icon
  },
};
```

### In HTML Templates
```html
<umb-icon name="my-custom-icon"></umb-icon>
```

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
