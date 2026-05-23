---
name: umbraco-entity-actions
description: Implement entity actions in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Entity Actions

## What is it?
Entity Actions perform an action on a specific item in Umbraco. They provide a generic extension point for secondary functionality associated with entity types like documents, media, or custom entities. These actions appear in context menus throughout the backoffice and can be controlled by user permissions.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/entity-actions
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Reference Examples

The Umbraco source includes working examples:

**Permission Manipulation**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/manipulate-document-property-value-permissions/`

This example demonstrates entity actions that manipulate document property permissions.

**User Permissions**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/user-permission/`

This example shows entity actions integrated with user permission controls.

## Related Foundation Skills

- **Repository Pattern**: When implementing actions that need data operations
  - Reference skill: `umbraco-repository-pattern`

- **Context API**: When accessing workspace or other contexts from actions
  - Reference skill: `umbraco-context-api`

- **Conditions**: When controlling action visibility based on permissions or state
  - Reference skill: `umbraco-conditions`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What entity type? What action to perform? Permissions needed?
3. **Generate files** - Create manifest + action class based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestEntityAction } from '@umbraco-cms/backoffice/extension-registry';
import { MyEntityAction } from './my-entity-action.js';

const manifest: ManifestEntityAction = {
  type: 'entityAction',
  alias: 'My.EntityAction',
  name: 'My Entity Action',
  weight: 10,
  api: MyEntityAction,
  forEntityTypes: ['document'],
  meta: {
    icon: 'icon-alarm-clock',
    label: 'My Action',
  },
};

export const manifests = [manifest];
```

### Action Implementation (my-entity-action.ts)
```typescript
import { UmbEntityActionBase } from '@umbraco-cms/backoffice/entity-action';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';

export class MyEntityAction extends UmbEntityActionBase<never> {
  constructor(host: UmbControllerHost, args: { unique: string; entityType: string }) {
    super(host, args);
  }

  async execute() {
    // this.unique contains the entity's unique identifier
    console.log('Executing action on:', this.unique);

    // Perform your action here
    alert(`Action executed on ${this.unique}`);
  }
}
```

### Action with Repository
```typescript
import { UmbEntityActionBase } from '@umbraco-cms/backoffice/entity-action';

export class MyEntityAction extends UmbEntityActionBase<MyRepository> {
  constructor(host: UmbControllerHost, args: { unique: string; entityType: string; repositoryAlias: string }) {
    super(host, args);
  }

  async execute() {
    // Access repository via this.repository
    await this.repository?.myCustomMethod(this.unique);
  }
}
```

### Link-based Action (using getHref)
```typescript
export class MyLinkAction extends UmbEntityActionBase<never> {
  async getHref() {
    return `/some/path/${this.unique}`;
  }

  async execute() {
    // Not needed when using getHref
  }
}
```

## Common Entity Types

- `document` - Content nodes
- `media` - Media items
- `member` - Members
- `data-type` - Data types
- `document-type` - Document types
- `media-type` - Media types

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
