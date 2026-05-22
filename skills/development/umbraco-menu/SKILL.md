---
name: umbraco-menu
description: Implement menus in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Menu

## What is it?
Menus are extension components that display throughout the Umbraco backoffice interface, including in sidebars and button flyouts. They serve as containers for one or more menu item extensions, enabling organized navigation and action grouping. Menu items are configured separately and can be added to existing menus or custom menus.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/menu
- **Menu Items**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/menu-item
- **Tutorial**: https://docs.umbraco.com/umbraco-cms/tutorials/extending-the-help-menu
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - New menu or extend existing? What items? Where displayed?
3. **Generate files** - Create manifest for menu + menu items based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Custom Menu (umbraco-package.json)
```json
{
  "type": "menu",
  "alias": "My.Menu",
  "name": "My Menu"
}
```

### Menu Item for Custom Menu (manifest.ts)
```typescript
export const manifests = [
  {
    type: "menuItem",
    kind: "link",
    alias: "My.MenuItem",
    name: "My Menu Item",
    weight: 100,
    meta: {
      menus: ["My.Menu"],
      label: "My Item",
      icon: "icon-document",
      href: "/my-link"
    }
  }
];
```

### Extending Existing Menu (Help Menu Example)
```json
{
  "type": "menuItem",
  "kind": "link",
  "alias": "My.MenuItem.Help",
  "name": "Custom Help Item",
  "weight": 300,
  "meta": {
    "menus": ["Umb.Menu.Help"],
    "label": "My Documentation",
    "icon": "icon-help",
    "href": "https://my-docs.com"
  }
}
```

### TypeScript Import (Help Menu)
```typescript
import { UMB_HELP_MENU_ALIAS } from "@umbraco-cms/backoffice/help";

const manifest = {
  type: "menuItem",
  kind: "link",
  alias: "My.MenuItem.Help",
  name: "My Help Item",
  meta: {
    menus: [UMB_HELP_MENU_ALIAS],
    label: "Documentation",
    icon: "icon-book"
  }
};
```

## Common Built-in Menus

- **Umb.Menu.Help** - Help menu in header
- **Umb.Menu.Content** - Content section menu
- **Umb.Menu.Media** - Media section menu
- **Umb.Menu.Settings** - Settings section menu

## Key Properties

- **type**: `"menu"` for menu container, `"menuItem"` for items
- **alias**: Unique identifier
- **menus**: Array of menu aliases this item should appear in
- **weight**: Controls ordering (higher = later in list)
- **kind**: Menu item type (`"link"`, `"default"`, etc.)

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
