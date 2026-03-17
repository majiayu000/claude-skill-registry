---
name: umbraco-property-action
description: Implement property actions in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Property Action

## What is it?
Property Actions are buttons that appear next to property labels in the backoffice, providing secondary functionality for property editors. They expand to show available actions when clicked. Property Actions let you add auxiliary features to existing property editors without modifying the editors themselves - useful for shortcuts, transformations, or context-specific operations.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/property-editors/property-actions
- **Property Editors**: https://docs.umbraco.com/umbraco-cms/customizing/property-editors
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Related Foundation Skills

- **Context API**: When accessing property context to read/modify values
  - Reference skill: `umbraco-context-api`

- **Modals**: When the action opens a modal dialog
  - Reference skill: `umbraco-modals`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - Which property editors to target? What action to perform?
3. **Generate files** - Create manifest + action class based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestPropertyAction } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestPropertyAction = {
  type: 'propertyAction',
  alias: 'My.PropertyAction.Clear',
  name: 'Clear Value',
  api: () => import('./clear-action.js'),
  forPropertyEditorUis: ['Umb.PropertyEditorUi.TextBox', 'Umb.PropertyEditorUi.TextArea'],
  meta: {
    icon: 'icon-trash',
    label: 'Clear',
  },
  weight: 100,
};

export const manifests = [manifest];
```

### Action Implementation (clear-action.ts)
```typescript
import { UmbPropertyActionBase } from '@umbraco-cms/backoffice/property-action';
import { UMB_PROPERTY_CONTEXT } from '@umbraco-cms/backoffice/property';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';

export class ClearPropertyAction extends UmbPropertyActionBase {
  constructor(host: UmbControllerHost, args: any) {
    super(host, args);
  }

  async execute() {
    const propertyContext = await this.getContext(UMB_PROPERTY_CONTEXT);
    propertyContext?.setValue('');
  }
}

export default ClearPropertyAction;
```

### Action That Transforms Value
```typescript
import { UmbPropertyActionBase } from '@umbraco-cms/backoffice/property-action';
import { UMB_PROPERTY_CONTEXT } from '@umbraco-cms/backoffice/property';

export class UppercasePropertyAction extends UmbPropertyActionBase {
  async execute() {
    const propertyContext = await this.getContext(UMB_PROPERTY_CONTEXT);
    const currentValue = propertyContext?.getValue() as string;

    if (currentValue) {
      propertyContext?.setValue(currentValue.toUpperCase());
    }
  }
}

export default UppercasePropertyAction;
```

### Action with Modal
```typescript
import { UmbPropertyActionBase } from '@umbraco-cms/backoffice/property-action';
import { UMB_PROPERTY_CONTEXT } from '@umbraco-cms/backoffice/property';
import { UMB_MODAL_MANAGER_CONTEXT } from '@umbraco-cms/backoffice/modal';

export class PickerPropertyAction extends UmbPropertyActionBase {
  async execute() {
    const propertyContext = await this.getContext(UMB_PROPERTY_CONTEXT);
    const modalManager = await this.getContext(UMB_MODAL_MANAGER_CONTEXT);

    const modal = modalManager.open(this, MY_PICKER_MODAL, {
      data: {
        currentValue: propertyContext?.getValue(),
      },
    });

    const result = await modal.onSubmit();
    if (result?.value) {
      propertyContext?.setValue(result.value);
    }
  }
}

export default PickerPropertyAction;
```

### Target All Property Editors
```typescript
const manifest: ManifestPropertyAction = {
  type: 'propertyAction',
  alias: 'My.PropertyAction.Copy',
  name: 'Copy to Clipboard',
  api: () => import('./copy-action.js'),
  // Omit forPropertyEditorUis to target all editors
  meta: {
    icon: 'icon-documents',
    label: 'Copy',
  },
};
```

## Common Property Editor UI Aliases

- `Umb.PropertyEditorUi.TextBox`
- `Umb.PropertyEditorUi.TextArea`
- `Umb.PropertyEditorUi.RichText`
- `Umb.PropertyEditorUi.Integer`
- `Umb.PropertyEditorUi.Decimal`
- `Umb.PropertyEditorUi.ContentPicker`
- `Umb.PropertyEditorUi.MediaPicker`

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
