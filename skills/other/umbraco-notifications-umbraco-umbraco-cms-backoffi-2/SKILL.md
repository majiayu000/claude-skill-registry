---
name: umbraco-notifications
description: Understand and use notifications in Umbraco backoffice (foundational concept)
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Notifications

## What is it?
Notifications provide user feedback in the Umbraco backoffice through the `UMB_NOTIFICATION_CONTEXT`, which is consumed via the Context API. The `peek()` method displays temporary toast-style notifications with different types (positive, negative, warning). Notifications appear in the UI temporarily and automatically dismiss, making them ideal for action confirmations and error messages.

## Documentation
Always fetch the latest docs before implementing:

- **Context API**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/context-api
- **Consume Context**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/context-api/consume-a-context
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What type? Success/error/warning? Simple or custom content?
3. **Generate code** - Implement notification usage based on latest docs
4. **Explain** - Show what was created and when notifications appear

## Minimal Examples

### Basic Notification
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

  showSuccess() {
    this.#notificationContext?.peek('positive', {
      data: { message: 'Operation completed successfully!' }
    });
  }
}
```

### Notification Types
```typescript
// Success notification
this.#notificationContext?.peek('positive', {
  data: { message: 'Saved successfully!' }
});

// Error notification
this.#notificationContext?.peek('danger', {
  data: { message: 'Something went wrong!' }
});

// Warning notification
this.#notificationContext?.peek('warning', {
  data: { message: 'Please review your changes.' }
});
```

### Notification with Headline
```typescript
this.#notificationContext?.peek('positive', {
  data: {
    headline: 'Success!',
    message: 'Your document has been published.'
  }
});
```

### Using in Controller
```typescript
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import { UMB_NOTIFICATION_CONTEXT } from '@umbraco-cms/backoffice/notification';

export class MyController extends UmbControllerBase {
  async performAction() {
    try {
      // Do something
      const context = await this.getContext(UMB_NOTIFICATION_CONTEXT);
      context?.peek('positive', {
        data: { message: 'Action completed!' }
      });
    } catch (error) {
      const context = await this.getContext(UMB_NOTIFICATION_CONTEXT);
      context?.peek('danger', {
        data: {
          headline: 'Error',
          message: error.message
        }
      });
    }
  }
}
```

### Button with Notification
```typescript
import { html } from '@umbraco-cms/backoffice/external/lit';
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

  #onClick() {
    this.#notificationContext?.peek('positive', {
      data: { message: 'Button clicked!' }
    });
  }

  render() {
    return html`
      <uui-button @click=${this.#onClick}>
        Click me
      </uui-button>
    `;
  }
}
```

### Async Operation with Notification
```typescript
async saveData() {
  try {
    const response = await fetch('/api/save', {
      method: 'POST',
      body: JSON.stringify(this.data)
    });

    if (response.ok) {
      this.#notificationContext?.peek('positive', {
        data: {
          headline: 'Saved',
          message: 'Your changes have been saved.'
        }
      });
    } else {
      this.#notificationContext?.peek('danger', {
        data: {
          headline: 'Save Failed',
          message: 'Could not save your changes.'
        }
      });
    }
  } catch (error) {
    this.#notificationContext?.peek('danger', {
      data: {
        headline: 'Error',
        message: 'An unexpected error occurred.'
      }
    });
  }
}
```

### Notification in Action Handler
```typescript
import { UmbMenuItemAction } from '@umbraco-cms/backoffice/menu';
import { UMB_NOTIFICATION_CONTEXT } from '@umbraco-cms/backoffice/notification';

export class MyAction extends UmbMenuItemAction {
  async execute() {
    const context = await this.getContext(UMB_NOTIFICATION_CONTEXT);

    context?.peek('positive', {
      data: { message: 'Action executed!' }
    });
  }
}
```

### Validation with Notification
```typescript
validateAndSave() {
  if (!this.title) {
    this.#notificationContext?.peek('warning', {
      data: {
        headline: 'Validation Error',
        message: 'Title is required.'
      }
    });
    return;
  }

  if (this.title.length < 3) {
    this.#notificationContext?.peek('warning', {
      data: {
        message: 'Title must be at least 3 characters.'
      }
    });
    return;
  }

  this.save();
}
```

## Notification Types

**positive** - Success messages (green)
```typescript
peek('positive', { data: { message: 'Success!' } })
```

**danger** - Error messages (red)
```typescript
peek('danger', { data: { message: 'Error occurred!' } })
```

**warning** - Warning messages (orange/yellow)
```typescript
peek('warning', { data: { message: 'Please review!' } })
```

## Key Concepts

**UMB_NOTIFICATION_CONTEXT**: Global context for notifications

**peek() Method**: Display temporary notification

**Toast Style**: Auto-dismissing UI notifications

**Data Structure**:
- `headline` (optional) - Bold title text
- `message` (required) - Notification body text

**Context Consumption**: Use `consumeContext()` for subscription or `getContext()` for one-time use

**Use Cases**:
- Save confirmations
- Error messages
- Validation warnings
- Action feedback
- Operation status

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
