---
name: umbraco-bundle
description: Implement bundles in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Bundle

## What is it?
A Bundle is an extension type that points to a single JavaScript file that exports or re-exports Extension Manifests written in JavaScript/TypeScript. It serves as a container for grouping multiple extension manifests together, allowing you to declare manifests in code rather than JSON and organize extensions in a modular way.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/bundle
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What extensions to bundle? TypeScript or JavaScript?
3. **Generate files** - Create manifest + bundle file based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (umbraco-package.json)
```json
{
  "name": "My Package",
  "version": "1.0.0",
  "extensions": [
    {
      "type": "bundle",
      "alias": "My.Package.Bundle",
      "name": "My Package Bundle",
      "js": "/App_Plugins/MyPackage/manifests.js"
    }
  ]
}
```

### Bundle File (manifests.ts)
```typescript
import type { UmbExtensionManifest } from '@umbraco-cms/backoffice/extension-api';

export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'dashboard',
    name: 'My Dashboard',
    alias: 'My.Dashboard',
    element: () => import('./dashboard.js'),
    weight: 900,
    meta: {
      label: 'My Dashboard',
      pathname: 'my-dashboard',
    },
    conditions: [
      {
        alias: 'Umb.Condition.SectionAlias',
        match: 'Umb.Section.Content',
      },
    ],
  },
  {
    type: 'headerApp',
    name: 'My Header App',
    alias: 'My.HeaderApp',
    element: () => import('./header-app.js'),
    meta: {
      label: 'My App',
      icon: 'icon-heart',
    },
  },
];
```

### Re-exporting from Multiple Files
```typescript
// manifests.ts
export * from './dashboards/manifests.js';
export * from './header-apps/manifests.js';
export * from './sections/manifests.js';
```

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
