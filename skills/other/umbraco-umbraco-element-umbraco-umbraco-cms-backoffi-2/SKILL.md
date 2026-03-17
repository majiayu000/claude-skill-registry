---
name: umbraco-umbraco-element
description: Implement Umbraco elements in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Element

## What is it?
An Umbraco Element is a Web Component enhancement that simplifies integration with the Umbraco Backoffice through the UmbElementMixin. It provides methods to consume/provide contexts, observe states, handle localization, and host controllers. UmbElementMixin can be applied to any Web Component-compatible base class, while UmbLitElement is a convenience wrapper combining the mixin with Lit.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/umbraco-element
- **Context API**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/context-api
- **Controllers**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/umbraco-controller
- **Localization**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/localization
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - Using Lit? Need contexts? Need localization? Which base class?
3. **Generate files** - Create element using UmbElementMixin or UmbLitElement based on latest docs
4. **Explain** - Show what was created and how to use it

## Minimal Examples

### Using UmbLitElement (Recommended for Lit)
```typescript
import { html, customElement } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('my-element')
export class MyElement extends UmbLitElement {

  constructor() {
    super();
    // Access built-in features
    this.consumeContext(MY_CONTEXT, (context) => {
      console.log('Context consumed:', context);
    });
  }

  render() {
    return html`
      <div>
        <h3>${this.localize.term('myKey')}</h3>
        <p>My custom element</p>
      </div>
    `;
  }
}

export default MyElement;
```

### Using UmbElementMixin with HTMLElement
```typescript
import { customElement } from '@umbraco-cms/backoffice/external/lit';
import { UmbElementMixin } from '@umbraco-cms/backoffice/element-api';

@customElement('my-element')
export class MyElement extends UmbElementMixin(HTMLElement) {

  constructor() {
    super();
    this.consumeContext(MY_CONTEXT, (context) => {
      // Use context
    });
  }

  connectedCallback() {
    this.innerHTML = `
      <div>
        <h3>My Element</h3>
      </div>
    `;
  }
}

export default MyElement;
```

### Using UmbElementMixin with UI Library Component
```typescript
import { customElement } from '@umbraco-cms/backoffice/external/lit';
import { UmbElementMixin } from '@umbraco-cms/backoffice/element-api';
import { UUIButtonElement } from '@umbraco-cms/backoffice/external/uui';

@customElement('my-custom-button')
export class MyCustomButton extends UmbElementMixin(UUIButtonElement) {

  constructor() {
    super();
    // Now has access to Umbraco contexts and controllers
  }
}

export default MyCustomButton;
```

### Consuming Context
```typescript
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UMB_NOTIFICATION_CONTEXT } from '@umbraco-cms/backoffice/notification';

export class MyElement extends UmbLitElement {

  #notificationContext?: typeof UMB_NOTIFICATION_CONTEXT.TYPE;

  constructor() {
    super();

    this.consumeContext(UMB_NOTIFICATION_CONTEXT, (context) => {
      this.#notificationContext = context;
    });
  }

  showNotification() {
    this.#notificationContext?.peek('positive', {
      data: { headline: 'Success!', message: 'Operation completed' }
    });
  }
}
```

### Using Observable State
```typescript
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UMB_CURRENT_USER_CONTEXT } from '@umbraco-cms/backoffice/current-user';

export class MyElement extends UmbLitElement {

  @state()
  private _userName?: string;

  constructor() {
    super();

    this.consumeContext(UMB_CURRENT_USER_CONTEXT, (context) => {
      this.observe(
        context.currentUser,
        (user) => {
          this._userName = user?.name;
        },
        '_userName'
      );
    });
  }
}
```

## Key Features

- **consumeContext()** - Subscribe to and consume contexts from parent elements
- **provideContext()** - Provide contexts to child elements
- **observe()** - Watch observable state and trigger reactive updates
- **localize** - Built-in localization controller for translations
- **hostController()** - Host and manage controllers within the element

## UmbLitElement vs UmbElementMixin

| Feature | UmbLitElement | UmbElementMixin |
|---------|--------------|-----------------|
| Base | Pre-configured with Lit | Apply to any base class |
| Usage | `extends UmbLitElement` | `extends UmbElementMixin(BaseClass)` |
| Best for | Lit-based components | Custom base classes or UI library components |
| Features | Same features | Same features |

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
