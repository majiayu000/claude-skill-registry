---
name: umbraco-granular-user-permissions
description: Implement granular user permissions in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Granular User Permissions

## What is it?
Granular User Permissions allow you to create custom permission controls for specific entity types in Umbraco. Unlike general entity permissions that apply to all instances, granular permissions can be configured per-entity, allowing fine-grained access control. This is commonly used for document permissions where different users can have different permissions on different content nodes.

## Documentation
Always fetch the latest docs before implementing:

- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry
- **User Permissions**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types

## Reference Example

The Umbraco source includes a working example:

**Location**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/user-permission/`

This example demonstrates granular user permission implementation. Study this for production patterns.

## Related Foundation Skills

- **Conditions**: When controlling permission visibility
  - Reference skill: `umbraco-conditions`

- **Context API**: When accessing user or workspace context
  - Reference skill: `umbraco-context-api`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What entity type? What permissions? What schema type?
3. **Generate files** - Create manifest + element based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestGranularUserPermission } from '@umbraco-cms/backoffice/user-permission';

export const manifests: Array<ManifestGranularUserPermission> = [
  {
    type: 'userGranularPermission',
    alias: 'My.GranularPermission.Custom',
    name: 'Custom Granular Permission',
    weight: 100,
    forEntityTypes: ['my-entity-type'],
    element: () => import('./my-granular-permission.element.js'),
    meta: {
      schemaType: 'MyPermissionPresentationModel',
      label: 'Custom Permissions',
      description: 'Configure custom permissions for this entity',
    },
  },
];
```

### Element Implementation (my-granular-permission.element.ts)
```typescript
import { html, customElement, property, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('my-granular-permission')
export class MyGranularPermissionElement extends UmbLitElement {
  @property({ attribute: false })
  value: unknown;

  @state()
  private _permissions: string[] = [];

  override render() {
    return html`
      <uui-box headline="Custom Permissions">
        <uui-checkbox
          label="Can Edit"
          @change=${(e: Event) => this.#onPermissionChange('edit', (e.target as HTMLInputElement).checked)}
        ></uui-checkbox>
        <uui-checkbox
          label="Can Delete"
          @change=${(e: Event) => this.#onPermissionChange('delete', (e.target as HTMLInputElement).checked)}
        ></uui-checkbox>
      </uui-box>
    `;
  }

  #onPermissionChange(permission: string, enabled: boolean) {
    if (enabled) {
      this._permissions = [...this._permissions, permission];
    } else {
      this._permissions = this._permissions.filter(p => p !== permission);
    }
    this.dispatchEvent(new CustomEvent('change', { detail: { permissions: this._permissions } }));
  }
}

export default MyGranularPermissionElement;
```

## Interface Reference

```typescript
interface ManifestGranularUserPermission extends ManifestElement {
  type: 'userGranularPermission';
  forEntityTypes?: Array<string>;
  meta: MetaGranularUserPermission;
}

interface MetaGranularUserPermission {
  schemaType: string;      // API schema type for serialization
  label?: string;          // Display label (can use localization key)
  labelKey?: string;       // Localization key for label
  description?: string;    // Description text
  descriptionKey?: string; // Localization key for description
}
```

## Common Entity Types

- `document` - Content nodes
- `media` - Media items
- `member` - Members

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
