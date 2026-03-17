---
name: umbraco-entity-create-option-action
description: Implement entity create option actions in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Entity Create Option Action

## What is it?
Entity Create Option Actions add customizable options when creating entities. These options appear in a create options dialog when the "Create" entity action is selected, allowing users to choose between different creation methods or paths. This enables extensibility where other developers can add their own creation options to existing workflows.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/entity-create-option-action
- **Entity Actions**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/entity-actions
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Related Foundation Skills

- **Modals**: When the create option opens a modal dialog
  - Reference skill: `umbraco-modals`

- **Routing**: When the create option navigates to a different view
  - Reference skill: `umbraco-routing`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What entity type? What creation options needed? What happens on selection?
3. **Generate files** - Create manifest + action class based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestEntityCreateOptionAction } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestEntityCreateOptionAction = {
  type: 'entityCreateOptionAction',
  alias: 'My.EntityCreateOptionAction',
  name: 'My Create Option',
  weight: 100,
  api: () => import('./my-create-option-action.js'),
  forEntityTypes: ['user'],
  meta: {
    icon: 'icon-add',
    label: 'Create with Template',
    additionalOptions: false,
  },
};

export const manifests = [manifest];
```

### Action Implementation (my-create-option-action.ts)
```typescript
import { UmbEntityCreateOptionActionBase } from '@umbraco-cms/backoffice/entity-create-option-action';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';

export class MyCreateOptionAction extends UmbEntityCreateOptionActionBase {
  constructor(host: UmbControllerHost, args: { unique: string | null; entityType: string }) {
    super(host, args);
  }

  override async execute() {
    // Perform custom creation logic
    console.log('Creating with custom option for entity type:', this.entityType);

    // Could open a modal, navigate somewhere, or perform API calls
    alert('Custom create option executed!');
  }
}

export default MyCreateOptionAction;
```

### Create Option with Modal
```typescript
import { UmbEntityCreateOptionActionBase } from '@umbraco-cms/backoffice/entity-create-option-action';
import { UMB_MODAL_MANAGER_CONTEXT } from '@umbraco-cms/backoffice/modal';

export class MyCreateOptionAction extends UmbEntityCreateOptionActionBase {
  override async execute() {
    const modalManager = await this.getContext(UMB_MODAL_MANAGER_CONTEXT);

    const modal = modalManager.open(this, MY_CREATE_MODAL, {
      data: {
        entityType: this.entityType,
        parentUnique: this.unique,
      },
    });

    await modal.onSubmit();
  }
}
```

### Create Option with Navigation
```typescript
import { UmbEntityCreateOptionActionBase } from '@umbraco-cms/backoffice/entity-create-option-action';

export class MyCreateOptionAction extends UmbEntityCreateOptionActionBase {
  override async getHref() {
    // Return a URL to navigate to instead of execute()
    return `/section/my-section/workspace/my-workspace/create/${this.unique}`;
  }

  override async execute() {
    // Not called when getHref() returns a value
  }
}
```

## Meta Properties

- `icon` - Icon to display for the option
- `label` - Display label for the option
- `additionalOptions` - If true, shows as a secondary/additional option

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
