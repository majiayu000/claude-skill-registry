---
name: umbraco-context-api
description: Understand and use Context API in Umbraco backoffice (foundational concept)
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Context API

## What is it?
The Context API is Umbraco's communication system that enables extensions to share data and functionality through the component hierarchy without tight coupling. It uses a provider-consumer pattern where parent elements provide contexts that descendant components can access. Contexts cascade down through the DOM tree and use tokens for type-safe access to services like notifications, workspaces, and user information.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/context-api
- **Consume Context**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/context-api/consume-a-context
- **Provide Context**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/context-api/provide-a-context
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - Need to consume or provide? Which context? One-time or subscription?
3. **Generate code** - Implement context consumption or provision based on latest docs
4. **Explain** - Show what was created and how contexts flow

## Minimal Examples

### Consuming Context (Subscription Pattern)
```typescript
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UMB_NOTIFICATION_CONTEXT } from '@umbraco-cms/backoffice/notification';

export class MyElement extends UmbLitElement {
  #notificationContext?: typeof UMB_NOTIFICATION_CONTEXT.TYPE;

  constructor() {
    super();

    // Subscribe to context - callback runs when context is available
    this.consumeContext(UMB_NOTIFICATION_CONTEXT, (context) => {
      this.#notificationContext = context;
    });
  }

  showMessage() {
    this.#notificationContext?.peek('positive', {
      data: { message: 'Hello from Context API!' }
    });
  }
}
```

### Consuming Context (One-time Pattern)
```typescript
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import { UMB_NOTIFICATION_CONTEXT } from '@umbraco-cms/backoffice/notification';

export class MyService extends UmbControllerBase {
  async showNotification(text: string) {
    // Get context once, use it, then release
    const context = await this.getContext(UMB_NOTIFICATION_CONTEXT);
    context?.peek('positive', { data: { message: text } });
  }
}
```

### Providing Context
```typescript
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UmbContextToken } from '@umbraco-cms/backoffice/context-api';

// Define a context token
export const MY_CUSTOM_CONTEXT = new UmbContextToken<MyCustomContext>(
  'MyCustomContext'
);

export class MyCustomContext {
  getData() {
    return { message: 'Hello from custom context!' };
  }
}

export class MyProviderElement extends UmbLitElement {
  constructor() {
    super();

    // Provide context to all descendants
    this.provideContext(MY_CUSTOM_CONTEXT, new MyCustomContext());
  }
}
```

### Common Built-in Contexts
```typescript
// Notifications
import { UMB_NOTIFICATION_CONTEXT } from '@umbraco-cms/backoffice/notification';

// Current User
import { UMB_CURRENT_USER_CONTEXT } from '@umbraco-cms/backoffice/current-user';

// Modal Manager
import { UMB_MODAL_MANAGER_CONTEXT } from '@umbraco-cms/backoffice/modal';

// Workspace (varies by type)
import { UMB_DOCUMENT_WORKSPACE_CONTEXT } from '@umbraco-cms/backoffice/document';

// Block Entry (for block editors)
import { UMB_BLOCK_ENTRY_CONTEXT } from '@umbraco-cms/backoffice/block';

// Property Dataset (for property editors)
import { UMB_PROPERTY_DATASET_CONTEXT } from '@umbraco-cms/backoffice/property';
```

## Key Concepts

**Context Token**: Type-safe identifier for a context
```typescript
const MY_TOKEN = new UmbContextToken<MyType>('UniqueName');
```

**Provider**: Element that provides context to descendants via `provideContext()`

**Consumer**: Element that accesses context via `consumeContext()` or `getContext()`

**Subscription vs One-time**:
- Use `consumeContext()` when you need the context during initialization
- Use `getContext()` for actions triggered by user interaction

**Hierarchy**: Contexts flow DOWN the DOM tree from provider to consumers

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
