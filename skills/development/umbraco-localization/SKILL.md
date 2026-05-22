---
name: umbraco-localization
description: Understand and use localization in Umbraco backoffice (foundational concept)
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Localization

## What is it?
Localization enables UI translation through localization files managed by the Extension Registry, with English as the fallback language. The Localization Controller (automatically available in Umbraco Elements via `this.localize`) provides access to translated strings using keys. Custom translations can be added via the Extension Registry and referenced in manifests using the `#` prefix.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/localization
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - Using built-in keys or custom? Need pluralization? Dynamic values?
3. **Generate code** - Implement localization based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Using Localize Controller (Umbraco Element)
```typescript
import { html, customElement } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('my-element')
export class MyElement extends UmbLitElement {
  render() {
    return html`
      <uui-button .label=${this.localize.term('general_close')}>
        ${this.localize.term('general_close')}
      </uui-button>
      <p>${this.localize.term('general_welcome')}</p>
    `;
  }
}
```

### Using Localize Element
```typescript
render() {
  return html`
    <button>
      <umb-localize key="dialog_myKey">Default Text</umb-localize>
    </button>
  `;
}
```

### Manual Localize Controller
```typescript
import { UmbLocalizationController } from '@umbraco-cms/backoffice/localization-api';
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';

export class MyController extends UmbControllerBase {
  #localize = new UmbLocalizationController(this);

  render() {
    return html`
      <uui-button .label=${this.#localize.term('general_close')}>
      </uui-button>
    `;
  }
}
```

### Custom Localization File
```javascript
// en.js
export default {
  myExtension: {
    welcomeMessage: 'Welcome to my extension!',
    itemCount: 'You have {0} items',
    goodbye: 'Goodbye, {0}!',
  },
};
```

### Registering Custom Localizations
```typescript
// manifest.ts
export const manifests = [
  {
    type: 'localization',
    alias: 'My.Localization.En',
    name: 'English Localization',
    meta: {
      culture: 'en',
    },
    js: () => import('./localization/en.js'),
  },
];
```

### Using Custom Keys
```typescript
render() {
  return html`
    <h1>${this.localize.term('myExtension_welcomeMessage')}</h1>
    <p>${this.localize.term('myExtension_itemCount', 5)}</p>
  `;
}
```

### Localization with Arguments
```javascript
// Localization file with function
export default {
  section: {
    numberOfItems: (count) => {
      if (count === 0) return 'Showing nothing';
      if (count === 1) return 'Showing only one item';
      return `Showing ${count} items`;
    },
  },
};
```

```typescript
// Usage
render() {
  return html`
    <umb-localize
      key="section_numberOfItems"
      .args=${[this._itemCount]}
    ></umb-localize>
  `;
}
```

### Localize in Manifest
```json
{
  "type": "dashboard",
  "alias": "My.Dashboard",
  "name": "My Dashboard",
  "meta": {
    "label": "#welcomeDashboard_label",
    "pathname": "welcome"
  }
}
```

### Common Built-in Keys
```typescript
// General
this.localize.term('general_close')
this.localize.term('general_cancel')
this.localize.term('general_save')
this.localize.term('general_delete')
this.localize.term('general_welcome')

// Actions
this.localize.term('actions_create')
this.localize.term('actions_edit')
this.localize.term('actions_remove')

// Dialogs
this.localize.term('dialog_confirm')
this.localize.term('dialog_cancel')
```

### Debug Mode
```html
<!-- Shows the key alias instead of value for troubleshooting -->
<umb-localize key="myExtension_welcomeMessage" debug="true"></umb-localize>
```

### Multiple Languages
```typescript
// en.js
export default {
  greeting: 'Hello',
};

// da.js (Danish)
export default {
  greeting: 'Hej',
};

// Register both
export const manifests = [
  {
    type: 'localization',
    alias: 'My.Localization.En',
    meta: { culture: 'en' },
    js: () => import('./localization/en.js'),
  },
  {
    type: 'localization',
    alias: 'My.Localization.Da',
    meta: { culture: 'da' },
    js: () => import('./localization/da.js'),
  },
];
```

## Key Concepts

**Localize Controller**: Auto-available in Umbraco Elements via `this.localize`

**Translation Keys**: Use underscore notation (e.g., `general_close`, `myExtension_welcomeMessage`)

**Fallback**: English (en) is the default fallback when translations are missing

**Arguments**: Pass dynamic values using `.args` attribute or second parameter to `term()`

**Manifest Localization**: Prefix values with `#` to reference translation keys

**Debug Mode**: Use `debug="true"` to show key aliases for troubleshooting

**File Structure**:
- One file per language (en.js, da.js, etc.)
- Export default object with nested keys
- Register via Extension Registry

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
