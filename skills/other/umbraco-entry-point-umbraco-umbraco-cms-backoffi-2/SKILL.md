---
name: umbraco-entry-point
description: Implement entry points in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Entry Point

## What is it?
Entry Points are extensions that execute JavaScript code when the Umbraco backoffice starts up. The Backoffice Entry Point runs after user authentication and is used for initialization logic, loading external libraries, registering UI extensions dynamically, or including global CSS. An optional `onUnload` function handles cleanup.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/backoffice-entry-point
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What initialization is needed? Any external libraries? Cleanup required?
3. **Generate files** - Create manifest + entry point based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (umbraco-package.json)
```json
{
  "name": "My Package",
  "extensions": [
    {
      "type": "backofficeEntryPoint",
      "alias": "My.EntryPoint",
      "name": "My Entry Point",
      "js": "/App_Plugins/MyPackage/index.js"
    }
  ]
}
```

### Implementation (index.ts)
```typescript
import type { UmbEntryPointOnInit } from '@umbraco-cms/backoffice/extension-api';

export const onInit: UmbEntryPointOnInit = (host, extensionRegistry) => {
  console.log('My package initialized');

  // Register extensions dynamically
  extensionRegistry.register({
    type: 'dashboard',
    alias: 'My.Dashboard',
    name: 'My Dashboard',
    element: () => import('./dashboard.js'),
    meta: {
      label: 'My Dashboard',
      pathname: 'my-dashboard'
    }
  });
};

// Optional cleanup
export const onUnload = () => {
  console.log('My package unloaded');
};
```

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
