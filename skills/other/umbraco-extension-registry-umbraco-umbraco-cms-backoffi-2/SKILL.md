---
name: umbraco-extension-registry
description: Understand and use extension registry in Umbraco backoffice (foundational concept)
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Extension Registry

## What is it?
The Extension Registry is the core system managing all Umbraco backoffice UI elements - almost any UI in the Backoffice is an extension managed by the Extension Registry. The registry allows developers to dynamically add, remove, or modify extensions at runtime using `umbExtensionsRegistry`. Developers have the same possibilities as Umbraco HQ, meaning you can change almost everything that is by default present in Umbraco.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry
- **Register Extensions**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry/register-extensions
- **Replace/Exclude**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry/replace-exclude-or-unregister
- **Extension Manifest**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry/extension-manifest
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - Register, exclude, or replace? Runtime or static? Conditions needed?
3. **Generate code** - Implement registry operations based on latest docs
4. **Explain** - Show what was created and how extensions are managed

## Minimal Examples

### Register Extension (Runtime)
```typescript
import { umbExtensionsRegistry } from '@umbraco-cms/backoffice/extension-registry';

const manifest = {
  type: 'dashboard',
  alias: 'My.Dashboard',
  name: 'My Dashboard',
  element: () => import('./dashboard.element.js'),
  meta: {
    label: 'My Dashboard',
    pathname: 'my-dashboard'
  }
};

umbExtensionsRegistry.register(manifest);
```

### Exclude Extension
```typescript
import { umbExtensionsRegistry } from '@umbraco-cms/backoffice/extension-registry';

// Permanently hide an extension
umbExtensionsRegistry.exclude('Umb.WorkspaceAction.Document.SaveAndPreview');
```

### Unregister Extension
```typescript
import { umbExtensionsRegistry } from '@umbraco-cms/backoffice/extension-registry';

// Remove extension from registry (can be re-registered)
umbExtensionsRegistry.unregister('My.WorkspaceAction.AutoFillWithUnicorns');
```

### Replace Extension (Overwrites)
```typescript
const manifest = {
  type: 'workspaceAction',
  alias: 'My.WorkspaceAction.ExternalPreview',
  name: 'My Custom Preview',
  overwrites: 'Umb.WorkspaceAction.Document.SaveAndPreview',
  element: () => import('./custom-preview.element.js'),
  // ... rest of manifest
};

umbExtensionsRegistry.register(manifest);
```

### Replace Multiple Extensions
```typescript
const manifest = {
  type: 'workspaceAction',
  alias: 'My.CustomSave',
  name: 'My Custom Save',
  overwrites: [
    'Umb.WorkspaceAction.Document.SaveAndPreview',
    'Umb.WorkspaceAction.Document.Save'
  ],
  // ... rest of manifest
};

umbExtensionsRegistry.register(manifest);
```

### Entry Point Registration
```typescript
// entrypoint.ts
import { umbExtensionsRegistry } from '@umbraco-cms/backoffice/extension-registry';

export const onInit = (host: UmbEntryPointOnInitArgs) => {
  // Exclude default dashboard
  umbExtensionsRegistry.exclude('Umb.Dashboard.UmbracoNews');

  // Register custom dashboard
  umbExtensionsRegistry.register({
    type: 'dashboard',
    alias: 'My.CustomDashboard',
    name: 'Custom Dashboard',
    element: () => import('./custom-dashboard.element.js'),
    meta: {
      label: 'Welcome',
      pathname: 'welcome'
    },
    conditions: [
      {
        alias: 'Umb.Condition.SectionAlias',
        match: 'Umb.Section.Content'
      }
    ]
  });
};
```

### Dynamic Registration from Server Data
```typescript
import { umbExtensionsRegistry } from '@umbraco-cms/backoffice/extension-registry';

async function registerDynamicDashboards() {
  // Fetch configuration from server
  const response = await fetch('/api/dashboard-config');
  const dashboards = await response.json();

  // Register each dashboard dynamically
  dashboards.forEach(config => {
    umbExtensionsRegistry.register({
      type: 'dashboard',
      alias: config.alias,
      name: config.name,
      element: () => import(config.elementPath),
      meta: {
        label: config.label,
        pathname: config.pathname
      }
    });
  });
}
```

### Conditional Registration
```typescript
import { umbExtensionsRegistry } from '@umbraco-cms/backoffice/extension-registry';

// Register extension only if condition is met
if (userIsAdmin) {
  umbExtensionsRegistry.register({
    type: 'dashboard',
    alias: 'My.AdminDashboard',
    name: 'Admin Dashboard',
    element: () => import('./admin-dashboard.element.js'),
    meta: {
      label: 'Admin',
      pathname: 'admin'
    }
  });
}
```

### Batch Operations
```typescript
import { umbExtensionsRegistry } from '@umbraco-cms/backoffice/extension-registry';

// Exclude multiple extensions
const extensionsToHide = [
  'Umb.Dashboard.UmbracoNews',
  'Umb.Dashboard.RedirectManagement',
];

extensionsToHide.forEach(alias => {
  umbExtensionsRegistry.exclude(alias);
});

// Register multiple extensions
const myExtensions = [
  { type: 'dashboard', alias: 'My.Dashboard1', /* ... */ },
  { type: 'dashboard', alias: 'My.Dashboard2', /* ... */ },
];

myExtensions.forEach(manifest => {
  umbExtensionsRegistry.register(manifest);
});
```

### View Registered Extensions
Navigate to: **Settings > Extensions Insights** in the backoffice to see all registered extensions.

## Key Concepts

**umbExtensionsRegistry**: Central registry for managing extensions

**register()**: Add new extension at runtime

**exclude()**: Permanently hide extension (never displayed)

**unregister()**: Remove extension from registry (can be re-registered)

**overwrites**: Replace existing extension(s) with custom implementation

**Runtime vs Static**:
- Static: Use `umbraco-package.json` for most extensions
- Runtime: Use `umbExtensionsRegistry` for dynamic/conditional registration

**Entry Point**: Common place to execute registry operations during startup

**Extension Insights**: View all registered extensions at Settings > Extensions Insights

**Use Cases**:
- Hide default Umbraco features
- Register extensions based on server data
- Replace built-in actions with custom logic
- Conditionally enable features
- Dynamic dashboard registration

## Sources
- [Extension Registry | Umbraco CMS](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry)
- [Register an Extension | Umbraco CMS](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry/register-extensions)
- [Replace, Exclude or Unregister | Umbraco CMS](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry/replace-exclude-or-unregister)

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
