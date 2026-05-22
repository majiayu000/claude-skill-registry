---
name: umbraco-ufm-component
description: Implement UFM (Umbraco Flavored Markdown) components in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco UFM Component

## What is it?
UFM (Umbraco Flavored Markdown) Components extend Umbraco's markdown rendering with custom syntax. They allow you to create custom markers that transform into HTML when rendered. This is useful for creating dynamic content like localized strings, property values, or custom UI elements within markdown text. UFM components use special syntax markers (like `#` for localization or `=` for values) that get processed into HTML.

## Documentation
Always fetch the latest docs before implementing:

- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry
- **UFM**: https://docs.umbraco.com/umbraco-cms/reference/umbraco-flavored-markdown

## Reference Example

The Umbraco source includes a working example:

**Location**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/ufm-custom-component/`

This example demonstrates a custom UFM component with marker syntax. Study this for production patterns.

## Related Foundation Skills

- **Localization**: When creating localized UFM components
  - Reference skill: `umbraco-localization`

- **Context API**: When accessing data for UFM rendering
  - Reference skill: `umbraco-context-api`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What marker? What output? Dynamic data?
3. **Generate files** - Create manifest + component based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestUfmComponent } from '@umbraco-cms/backoffice/ufm';

export const manifests: Array<ManifestUfmComponent> = [
  {
    type: 'ufmComponent',
    alias: 'My.UfmComponent.Custom',
    name: 'Custom UFM Component',
    api: () => import('./my-ufm-component.js'),
    meta: {
      alias: 'myCustom',  // Usage: {myCustom:value}
      marker: '%',        // Optional: Short marker like {%value}
    },
  },
];
```

### Component Implementation (my-ufm-component.ts)
```typescript
import { UmbUfmComponentBase } from '@umbraco-cms/backoffice/ufm';
import type { UfmToken } from '@umbraco-cms/backoffice/ufm';

export class MyUfmComponent extends UmbUfmComponentBase {
  render(token: UfmToken): string | undefined {
    // token.text contains the text after the marker
    // e.g., {%hello} would have token.text = 'hello'

    return `<span class="my-custom">${token.text}</span>`;
  }
}

export { MyUfmComponent as api };
```

### Component with Custom Element (my-ufm-component.ts)
```typescript
import { html, customElement, property } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UmbUfmComponentBase } from '@umbraco-cms/backoffice/ufm';
import type { UfmToken } from '@umbraco-cms/backoffice/ufm';

// The UFM component that renders to custom element
export class MyUfmComponent extends UmbUfmComponentBase {
  render(token: UfmToken): string | undefined {
    // Output a custom element with the token text as attribute
    return `<my-ufm-element text="${token.text}"></my-ufm-element>`;
  }
}

// The custom element that gets rendered
@customElement('my-ufm-element')
export class MyUfmElement extends UmbLitElement {
  @property()
  text?: string;

  override render() {
    return html`<strong>${this.text}</strong>`;
  }
}

export { MyUfmComponent as api };
```

### Highlight Component Example
```typescript
import { UmbUfmComponentBase } from '@umbraco-cms/backoffice/ufm';
import type { UfmToken } from '@umbraco-cms/backoffice/ufm';

// Usage: {!important text here} or {highlight:important text here}
export class HighlightUfmComponent extends UmbUfmComponentBase {
  render(token: UfmToken): string | undefined {
    return `<mark style="background: yellow; padding: 2px 4px;">${token.text}</mark>`;
  }
}

export { HighlightUfmComponent as api };
```

### Icon Component Example
```typescript
import { UmbUfmComponentBase } from '@umbraco-cms/backoffice/ufm';
import type { UfmToken } from '@umbraco-cms/backoffice/ufm';

// Usage: {@icon-document} renders an Umbraco icon
export class IconUfmComponent extends UmbUfmComponentBase {
  render(token: UfmToken): string | undefined {
    return `<uui-icon name="${token.text}"></uui-icon>`;
  }
}

export { IconUfmComponent as api };
```

## Interface Reference

```typescript
interface ManifestUfmComponent extends ManifestApi<UmbUfmComponentApi> {
  type: 'ufmComponent';
  meta: MetaUfmComponent;
}

interface MetaUfmComponent {
  alias: string;    // Long form: {alias:text}
  marker?: string;  // Short form: {marker text}
}

interface UmbUfmComponentApi extends UmbApi {
  render(token: UfmToken): string | undefined;
}

interface UfmToken {
  text: string;  // The text content after the marker
}
```

## Built-in UFM Components

- `{#key}` or `{umbLocalize:key}` - Localization
- `{=property}` or `{umbValue:property}` - Property values
- `{umbContentName:id}` - Content names
- `{umbLink:url}` - Styled links

## Usage in Markdown

UFM components are used in label descriptions and markdown text:

```json
{
  "type": "propertyEditorUi",
  "meta": {
    "label": "{#myLabel}",
    "description": "Status: {%active} - {!Important note}"
  }
}
```

## Best Practices

- Choose memorable, short markers
- Return safe HTML (escape user input)
- Keep rendering lightweight
- Consider accessibility in output

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
