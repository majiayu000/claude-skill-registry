---
name: umbraco-collection-action
description: Implement collection actions in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Collection Action

## What is it?
Collection Actions are buttons that appear in a collection's toolbar, providing actions that can be performed on the collection as a whole (not on individual items - those are Entity Bulk Actions). Common examples include "Create New" buttons or export functionality. Actions can either execute code or navigate to a URL.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/collections
- **Collection View**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/collections/collection-view
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Related Foundation Skills

- **Context API**: For accessing collection context
  - Reference skill: `umbraco-context-api`

- **Modals**: When actions open modal dialogs
  - Reference skill: `umbraco-modals`

- **Conditions**: For controlling when actions appear
  - Reference skill: `umbraco-conditions`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What collection? What action to perform? Navigate or execute?
3. **Generate files** - Create manifest + action class based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestCollectionAction } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestCollectionAction = {
  type: 'collectionAction',
  alias: 'My.CollectionAction.Create',
  name: 'Create Item Action',
  api: () => import('./create-action.js'),
  meta: {
    label: 'Create New',
  },
  conditions: [
    {
      alias: 'Umb.Condition.CollectionAlias',
      match: 'My.Collection',
    },
  ],
};

export const manifests = [manifest];
```

### Action Implementation (create-action.ts)
```typescript
import { UmbCollectionActionBase } from '@umbraco-cms/backoffice/collection';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';

export class CreateAction extends UmbCollectionActionBase {
  constructor(host: UmbControllerHost) {
    super(host);
  }

  async execute() {
    // Perform the action
    console.log('Create action executed');
  }
}

export default CreateAction;
```

### Link-based Action (using getHref)
```typescript
import { UmbCollectionActionBase } from '@umbraco-cms/backoffice/collection';

export class CreateLinkAction extends UmbCollectionActionBase {
  async getHref() {
    // Return URL to navigate to
    return '/section/my-section/workspace/my-workspace/create';
  }

  async execute() {
    // Not called when getHref returns a value
  }
}

export default CreateLinkAction;
```

### Action with Modal
```typescript
import { UmbCollectionActionBase } from '@umbraco-cms/backoffice/collection';
import { UMB_MODAL_MANAGER_CONTEXT } from '@umbraco-cms/backoffice/modal';

export class ExportAction extends UmbCollectionActionBase {
  async execute() {
    const modalManager = await this.getContext(UMB_MODAL_MANAGER_CONTEXT);

    const modal = modalManager.open(this, MY_EXPORT_MODAL, {
      data: {
        collectionAlias: 'My.Collection',
      },
    });

    await modal.onSubmit();
  }
}

export default ExportAction;
```

### Action with Additional Options Indicator
```typescript
const manifest: ManifestCollectionAction = {
  type: 'collectionAction',
  alias: 'My.CollectionAction.CreateWithOptions',
  name: 'Create With Options',
  api: () => import('./create-options-action.js'),
  meta: {
    label: 'Create',
    additionalOptions: true, // Shows indicator that more options are available
  },
  conditions: [
    {
      alias: 'Umb.Condition.CollectionAlias',
      match: 'Umb.Collection.Document',
    },
  ],
};
```

### Action Class with Additional Options
```typescript
import { UmbCollectionActionBase } from '@umbraco-cms/backoffice/collection';

export class CreateWithOptionsAction extends UmbCollectionActionBase {
  async hasAdditionalOptions() {
    return true;
  }

  async execute() {
    // Show options menu or modal
  }
}

export default CreateWithOptionsAction;
```

## Meta Properties

| Property | Description |
|----------|-------------|
| `label` | Required. Button text |
| `href` | Optional static URL (use getHref() for dynamic) |
| `additionalOptions` | Shows dropdown indicator if true |

## Common Collection Aliases for Conditions

- `Umb.Collection.Document`
- `Umb.Collection.Media`
- `Umb.Collection.Member`
- `Umb.Collection.User`
- `Umb.Collection.DataType`

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
