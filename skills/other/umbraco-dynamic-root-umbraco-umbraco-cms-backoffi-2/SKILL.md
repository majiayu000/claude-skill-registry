---
name: umbraco-dynamic-root
description: Implement dynamic root origins and query steps in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Dynamic Root

## What is it?
Dynamic Roots allow content pickers to have a starting point (origin) that is determined dynamically rather than being a fixed node. This includes two extension types:
- **Dynamic Root Origin**: Defines where the picker starts (e.g., current page, site root, nearest ancestor of type)
- **Dynamic Root Query Step**: Defines navigation steps from the origin (e.g., find nearest ancestor, get children of type)

These enable flexible content picker configurations that adapt based on context.

## Documentation
Always fetch the latest docs before implementing:

- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Content Picker**: https://docs.umbraco.com/umbraco-cms/fundamentals/backoffice/property-editors/built-in-umbraco-property-editors/content-picker
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What starting point logic? What query steps needed?
3. **Generate files** - Create manifest(s) based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Dynamic Root Origin Manifest
```typescript
import type { ManifestDynamicRootOrigin } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestDynamicRootOrigin = {
  type: 'dynamicRootOrigin',
  alias: 'My.DynamicRootOrigin.SiteRoot',
  name: 'Site Root Origin',
  meta: {
    originAlias: 'SiteRoot',
    label: 'Site Root',
    description: 'Start from the root of the current site',
    icon: 'icon-home',
  },
};

export const manifests = [manifest];
```

### Dynamic Root Query Step Manifest
```typescript
import type { ManifestDynamicRootQueryStep } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestDynamicRootQueryStep = {
  type: 'dynamicRootQueryStep',
  alias: 'My.DynamicRootQueryStep.NearestBlog',
  name: 'Nearest Blog Query Step',
  meta: {
    queryStepAlias: 'NearestBlog',
    label: 'Nearest Blog',
    description: 'Find the nearest blog ancestor',
    icon: 'icon-article',
  },
};

export const manifests = [manifest];
```

### Multiple Origins and Steps
```typescript
import type { ManifestDynamicRootOrigin, ManifestDynamicRootQueryStep } from '@umbraco-cms/backoffice/extension-registry';

const originManifests: ManifestDynamicRootOrigin[] = [
  {
    type: 'dynamicRootOrigin',
    alias: 'My.DynamicRootOrigin.CurrentPage',
    name: 'Current Page Origin',
    meta: {
      originAlias: 'CurrentPage',
      label: 'Current Page',
      description: 'Start from the page being edited',
      icon: 'icon-document',
    },
  },
  {
    type: 'dynamicRootOrigin',
    alias: 'My.DynamicRootOrigin.Parent',
    name: 'Parent Page Origin',
    meta: {
      originAlias: 'Parent',
      label: 'Parent Page',
      description: 'Start from the parent of current page',
      icon: 'icon-arrow-up',
    },
  },
];

const queryStepManifests: ManifestDynamicRootQueryStep[] = [
  {
    type: 'dynamicRootQueryStep',
    alias: 'My.DynamicRootQueryStep.Children',
    name: 'Children Query Step',
    meta: {
      queryStepAlias: 'Children',
      label: 'Children',
      description: 'Get all child pages',
      icon: 'icon-tree',
    },
  },
  {
    type: 'dynamicRootQueryStep',
    alias: 'My.DynamicRootQueryStep.Ancestors',
    name: 'Ancestors Query Step',
    meta: {
      queryStepAlias: 'Ancestors',
      label: 'Ancestors',
      description: 'Get ancestor pages',
      icon: 'icon-navigation-up',
    },
  },
];

export const manifests = [...originManifests, ...queryStepManifests];
```

### Backend Implementation Required

Dynamic roots require backend C# implementation to handle the actual query logic:

```csharp
// Example C# implementation for a custom origin
public class SiteRootDynamicRootOrigin : IDynamicRootOrigin
{
    public string OriginAlias => "SiteRoot";

    public Task<Guid?> GetOriginAsync(Guid contentKey, string? entityType)
    {
        // Return the site root GUID based on the content's position
        // Implementation depends on your site structure
        return Task.FromResult<Guid?>(GetSiteRootForContent(contentKey));
    }
}

// Example C# implementation for a custom query step
public class NearestBlogQueryStep : IDynamicRootQueryStep
{
    public string QueryStepAlias => "NearestBlog";

    public Task<IEnumerable<Guid>> ExecuteAsync(Guid originKey, string? entityType)
    {
        // Find nearest blog ancestor from the origin
        // Return matching content GUIDs
        return Task.FromResult(FindNearestBlogAncestors(originKey));
    }
}

// Register in Composer
public class DynamicRootComposer : IComposer
{
    public void Compose(IUmbracoBuilder builder)
    {
        builder.DynamicRootSteps()
            .AddOrigin<SiteRootDynamicRootOrigin>()
            .AddQueryStep<NearestBlogQueryStep>();
    }
}
```

## Origin Meta Properties

| Property | Description |
|----------|-------------|
| `originAlias` | Unique identifier matching backend implementation |
| `label` | Display name in picker configuration |
| `description` | Help text explaining the origin |
| `icon` | Icon shown in configuration UI |

## Query Step Meta Properties

| Property | Description |
|----------|-------------|
| `queryStepAlias` | Unique identifier matching backend implementation |
| `label` | Display name in picker configuration |
| `description` | Help text explaining the query step |
| `icon` | Icon shown in configuration UI |

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
