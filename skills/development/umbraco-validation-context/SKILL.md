---
name: umbraco-validation-context
description: Implement form validation using UmbValidationContext in Umbraco backoffice
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Validation Context

## What is it?

UmbValidationContext provides a centralized validation system for forms in the Umbraco backoffice. It manages validation messages using JSON Path notation, supports both client-side and server-side validation, and enables reactive error counting for tabs and sections. This is essential for multi-step forms, workspace editors, and any UI that requires comprehensive validation feedback.

## Documentation

Always fetch the latest docs before implementing:

- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Reference Examples

The Umbraco source includes working examples:

**Validation Context Dashboard**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/validation-context/`

This example demonstrates multi-tab form validation with error counting.

**Custom Validation Workspace Context**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/custom-validation-workspace-context/`

This example shows workspace-level validation patterns.

## Related Foundation Skills

- **State Management**: For observing validation state changes
  - Reference skill: `umbraco-state-management`

- **Context API**: For consuming validation context
  - Reference skill: `umbraco-context-api`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What fields? What validation rules? Multi-tab form?
3. **Generate files** - Create form element with validation context
4. **Explain** - Show what was created and how validation works

---

## Basic Setup

```typescript
import { html, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import {
  UMB_VALIDATION_CONTEXT,
  umbBindToValidation,
  UmbValidationContext,
} from '@umbraco-cms/backoffice/validation';
import type { UmbValidationMessage } from '@umbraco-cms/backoffice/validation';

@customElement('my-validated-form')
export class MyValidatedFormElement extends UmbLitElement {
  // Create validation context for this component
  readonly validation = new UmbValidationContext(this);

  @state()
  private _name = '';

  @state()
  private _email = '';

  @state()
  private _messages?: UmbValidationMessage[];

  constructor() {
    super();

    // Observe all validation messages
    this.consumeContext(UMB_VALIDATION_CONTEXT, (validationContext) => {
      this.observe(
        validationContext?.messages.messages,
        (messages) => {
          this._messages = messages;
        },
        'observeValidationMessages'
      );
    });
  }

  override render() {
    return html`
      <uui-form>
        <form>
          <div>
            <label>Name</label>
            <uui-form-validation-message>
              <uui-input
                type="text"
                .value=${this._name}
                @input=${(e: InputEvent) => (this._name = (e.target as HTMLInputElement).value)}
                ${umbBindToValidation(this, '$.form.name', this._name)}
                required
              ></uui-input>
            </uui-form-validation-message>
          </div>

          <div>
            <label>Email</label>
            <uui-form-validation-message>
              <uui-input
                type="email"
                .value=${this._email}
                @input=${(e: InputEvent) => (this._email = (e.target as HTMLInputElement).value)}
                ${umbBindToValidation(this, '$.form.email', this._email)}
                required
              ></uui-input>
            </uui-form-validation-message>
          </div>

          <uui-button look="primary" @click=${this.#handleSave}>Save</uui-button>
        </form>
      </uui-form>

      <pre>${JSON.stringify(this._messages ?? [], null, 2)}</pre>
    `;
  }

  async #handleSave() {
    const isValid = await this.validation.validate();
    if (isValid) {
      // Form is valid, proceed with save
      console.log('Form is valid!');
    }
  }
}
```

---

## Multi-Tab Form with Error Counting

```typescript
import { html, customElement, state, when } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UmbValidationContext, umbBindToValidation } from '@umbraco-cms/backoffice/validation';

@customElement('my-tabbed-form')
export class MyTabbedFormElement extends UmbLitElement {
  readonly validation = new UmbValidationContext(this);

  @state() private _tab = '1';
  @state() private _totalErrors = 0;
  @state() private _tab1Errors = 0;
  @state() private _tab2Errors = 0;

  // Form fields
  @state() private _name = '';
  @state() private _email = '';
  @state() private _city = '';
  @state() private _country = '';

  constructor() {
    super();

    // Observe total errors
    this.observe(
      this.validation.messages.messagesOfPathAndDescendant('$.form'),
      (messages) => {
        this._totalErrors = [...new Set(messages.map((x) => x.path))].length;
      }
    );

    // Observe Tab 1 errors (using JSON Path prefix)
    this.observe(
      this.validation.messages.messagesOfPathAndDescendant('$.form.tab1'),
      (messages) => {
        this._tab1Errors = [...new Set(messages.map((x) => x.path))].length;
      }
    );

    // Observe Tab 2 errors
    this.observe(
      this.validation.messages.messagesOfPathAndDescendant('$.form.tab2'),
      (messages) => {
        this._tab2Errors = [...new Set(messages.map((x) => x.path))].length;
      }
    );
  }

  override render() {
    return html`
      <uui-box>
        <p>Total errors: ${this._totalErrors}</p>

        <uui-tab-group @click=${this.#onTabChange}>
          <uui-tab ?active=${this._tab === '1'} data-tab="1">
            Tab 1
            ${when(
              this._tab1Errors,
              () => html`<uui-badge color="danger">${this._tab1Errors}</uui-badge>`
            )}
          </uui-tab>
          <uui-tab ?active=${this._tab === '2'} data-tab="2">
            Tab 2
            ${when(
              this._tab2Errors,
              () => html`<uui-badge color="danger">${this._tab2Errors}</uui-badge>`
            )}
          </uui-tab>
        </uui-tab-group>

        ${when(this._tab === '1', () => this.#renderTab1())}
        ${when(this._tab === '2', () => this.#renderTab2())}

        <uui-button look="primary" @click=${this.#handleSave}>Save</uui-button>
      </uui-box>
    `;
  }

  #renderTab1() {
    return html`
      <uui-form>
        <form>
          <label>Name</label>
          <uui-form-validation-message>
            <uui-input
              .value=${this._name}
              @input=${(e: InputEvent) => (this._name = (e.target as HTMLInputElement).value)}
              ${umbBindToValidation(this, '$.form.tab1.name', this._name)}
              required
            ></uui-input>
          </uui-form-validation-message>

          <label>Email</label>
          <uui-form-validation-message>
            <uui-input
              type="email"
              .value=${this._email}
              @input=${(e: InputEvent) => (this._email = (e.target as HTMLInputElement).value)}
              ${umbBindToValidation(this, '$.form.tab1.email', this._email)}
              required
            ></uui-input>
          </uui-form-validation-message>
        </form>
      </uui-form>
    `;
  }

  #renderTab2() {
    return html`
      <uui-form>
        <form>
          <label>City</label>
          <uui-form-validation-message>
            <uui-input
              .value=${this._city}
              @input=${(e: InputEvent) => (this._city = (e.target as HTMLInputElement).value)}
              ${umbBindToValidation(this, '$.form.tab2.city', this._city)}
              required
            ></uui-input>
          </uui-form-validation-message>

          <label>Country</label>
          <uui-form-validation-message>
            <uui-input
              .value=${this._country}
              @input=${(e: InputEvent) => (this._country = (e.target as HTMLInputElement).value)}
              required
            ></uui-input>
          </uui-form-validation-message>
        </form>
      </uui-form>
    `;
  }

  #onTabChange(e: Event) {
    this._tab = (e.target as HTMLElement).getAttribute('data-tab') ?? '1';
  }

  async #handleSave() {
    const isValid = await this.validation.validate();
    if (!isValid) {
      console.log('Form has validation errors');
    }
  }
}
```

---

## Server-Side Validation Errors

Add server validation errors after an API call:

```typescript
async #handleSave() {
  // First validate client-side
  const isValid = await this.validation.validate();
  if (!isValid) return;

  try {
    // Call API
    const response = await this.#saveToServer();

    if (!response.ok) {
      // Add server validation errors
      const errors = await response.json();

      for (const error of errors.validationErrors) {
        this.validation.messages.addMessage(
          'server',                    // Source
          error.path,                  // JSON Path (e.g., '$.form.name')
          error.message,               // Error message
          crypto.randomUUID()          // Unique key
        );
      }
    }
  } catch (error) {
    console.error('Save failed:', error);
  }
}
```

---

## Key APIs

### UmbValidationContext

```typescript
// Create context
const validation = new UmbValidationContext(this);

// Validate all bound fields
const isValid = await validation.validate();

// Access messages manager
validation.messages;
```

### Validation Messages

```typescript
// Add a message
validation.messages.addMessage(source, path, message, key);

// Remove messages by source
validation.messages.removeMessagesBySource('server');

// Observe messages for a path and descendants
this.observe(
  validation.messages.messagesOfPathAndDescendant('$.form.tab1'),
  (messages) => { /* handle messages */ }
);

// Observe all messages
this.observe(
  validation.messages.messages,
  (messages) => { /* handle all messages */ }
);
```

### umbBindToValidation Directive

```typescript
// Bind an input to validation
${umbBindToValidation(this, '$.form.fieldName', fieldValue)}
```

---

## JSON Path Notation

Validation uses JSON Path to identify fields:

| Path | Description |
|------|-------------|
| `$.form` | Root form object |
| `$.form.name` | Name field |
| `$.form.tab1.email` | Email field in tab1 |
| `$.form.items[0].value` | First item's value |
| `$.form.items[*].name` | All item names |

---

## Validation Message Interface

```typescript
interface UmbValidationMessage {
  source: string;    // 'client' | 'server' | custom
  path: string;      // JSON Path
  message: string;   // Error message text
  key: string;       // Unique identifier
}
```

---

## Best Practices

1. **Use JSON Path hierarchy** - Organize paths by tab/section for easy error counting
2. **Wrap inputs** - Use `<uui-form-validation-message>` around inputs
3. **Clear server errors** - Remove old server errors before new validation
4. **Unique keys** - Use `crypto.randomUUID()` for server error keys
5. **Observe specific paths** - Use `messagesOfPathAndDescendant` for scoped error counts
6. **Show counts on tabs** - Display error badges to guide users to problems

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
