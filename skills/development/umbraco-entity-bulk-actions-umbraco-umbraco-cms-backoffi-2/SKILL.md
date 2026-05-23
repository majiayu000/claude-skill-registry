---
name: umbraco-entity-bulk-actions
description: Implement entity bulk actions in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Entity Bulk Actions

## What is it?
Entity Bulk Actions perform an action on a selection of multiple items at once. They appear in the collection selection toolbar when users select multiple items, enabling batch operations like bulk publishing, deleting, or custom processing across multiple entities simultaneously.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/entity-bulk-actions
- **Collections**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/collections
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Related Foundation Skills

- **Repository Pattern**: When implementing bulk operations that need data access
  - Reference skill: `umbraco-repository-pattern`

- **Conditions**: When controlling bulk action visibility based on collection or permissions
  - Reference skill: `umbraco-conditions`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What collection? What bulk operation? What entity types?
3. **Generate files** - Create manifest + bulk action class based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestEntityBulkAction } from '@umbraco-cms/backoffice/extension-registry';
import { MyBulkAction } from './my-bulk-action.js';

const manifest: ManifestEntityBulkAction = {
  type: 'entityBulkAction',
  alias: 'My.EntityBulkAction',
  name: 'My Bulk Action',
  weight: 10,
  api: MyBulkAction,
  meta: {
    icon: 'icon-check',
    label: 'Process Selected',
  },
  conditions: [
    {
      alias: 'Umb.Condition.CollectionAlias',
      match: 'Umb.Collection.Document',
    },
  ],
};

export const manifests = [manifest];
```

### Bulk Action Implementation (my-bulk-action.ts)
```typescript
import { UmbEntityBulkActionBase } from '@umbraco-cms/backoffice/entity-bulk-action';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';

export class MyBulkAction extends UmbEntityBulkActionBase<never> {
  constructor(host: UmbControllerHost, args: { selection: Array<string> }) {
    super(host, args);
  }

  async execute() {
    // this.selection contains array of unique identifiers
    console.log('Processing items:', this.selection);

    for (const unique of this.selection) {
      // Process each selected item
      console.log('Processing:', unique);
    }

    alert(`Processed ${this.selection.length} items`);
  }
}
```

### Bulk Action with Repository
```typescript
import { UmbEntityBulkActionBase } from '@umbraco-cms/backoffice/entity-bulk-action';

export class MyBulkAction extends UmbEntityBulkActionBase<MyRepository> {
  async execute() {
    // Process all selected items via repository
    for (const unique of this.selection) {
      await this.repository?.processItem(unique);
    }
  }
}
```

### Manifest with Multiple Conditions
```typescript
const manifest: ManifestEntityBulkAction = {
  type: 'entityBulkAction',
  alias: 'My.MediaBulkAction',
  name: 'Process Media',
  api: MyBulkAction,
  meta: {
    icon: 'icon-picture',
    label: 'Optimize Images',
  },
  conditions: [
    {
      alias: 'Umb.Condition.CollectionAlias',
      match: 'Umb.Collection.Media',
    },
  ],
};
```

## Common Collection Aliases

- `Umb.Collection.Document` - Content collection
- `Umb.Collection.Media` - Media collection
- `Umb.Collection.Member` - Member collection

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
