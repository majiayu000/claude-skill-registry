---
name: umbraco-controllers
description: Understand and create controllers in Umbraco backoffice (foundational concept)
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Controllers

## What is it?
Controllers are separate classes that contain or reuse logic across elements while maintaining connection to an element's lifecycle. A Controller is assigned to a Host Element and supports lifecycle methods (hostConnected, hostDisconnected, destroy) for managing side effects, timers, subscriptions, and cleanup. Controllers can host other controllers, enabling composition and reuse of functionality.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/umbraco-controller
- **Write Custom Controller**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/umbraco-controller/write-your-own-controller
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - Need custom controller? What lifecycle events? What cleanup needed?
3. **Generate code** - Implement controller extending UmbControllerBase based on latest docs
4. **Explain** - Show what was created and how to host it

## Minimal Examples

### Basic Custom Controller
```typescript
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';

export class MyController extends UmbControllerBase {
  constructor(host: UmbControllerHost) {
    super(host);
    // Auto-registers with host
  }

  override hostConnected() {
    super.hostConnected();
    console.log('Controller connected!');
  }

  override hostDisconnected() {
    super.hostDisconnected();
    console.log('Controller disconnected!');
  }

  override destroy() {
    super.destroy();
    console.log('Controller destroyed!');
  }
}
```

### Timer Controller Example
```typescript
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';

export class TimerController extends UmbControllerBase {
  #timer?: number;
  #secondsAlive = 0;

  constructor(host: UmbControllerHost) {
    super(host);
  }

  override hostConnected() {
    super.hostConnected();
    // Start timer when element connects to DOM
    this.#timer = window.setInterval(this.#onInterval, 1000);
  }

  override hostDisconnected() {
    super.hostDisconnected();
    // Clean up timer when element disconnects
    if (this.#timer) {
      clearInterval(this.#timer);
    }
  }

  #onInterval = () => {
    this.#secondsAlive++;
    console.log(`Controller active for ${this.#secondsAlive} seconds`);
  };

  override destroy() {
    super.destroy();
    if (this.#timer) {
      clearInterval(this.#timer);
    }
  }

  getSecondsAlive(): number {
    return this.#secondsAlive;
  }
}
```

### Hosting a Controller in Element
```typescript
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { TimerController } from './timer-controller.js';

export class MyElement extends UmbLitElement {
  #timerController = new TimerController(this);

  render() {
    return html`
      <div>
        Active for: ${this.#timerController.getSecondsAlive()}s
      </div>
    `;
  }
}
```

### Manual Registration (Not Recommended)
```typescript
export class MyManualController {
  #host: UmbControllerHost;

  constructor(host: UmbControllerHost) {
    this.#host = host;
    // Manual registration required
    this.#host.addUmbController(this);
  }

  hostConnected() {
    console.log('Connected');
  }

  destroy() {
    // Manual deregistration required
    this.#host.removeUmbController(this);
  }
}
```

### Controller with Context Access
```typescript
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import { UMB_NOTIFICATION_CONTEXT } from '@umbraco-cms/backoffice/notification';

export class NotificationController extends UmbControllerBase {
  async showSuccess(message: string) {
    // Controllers can access contexts via getContext
    const context = await this.getContext(UMB_NOTIFICATION_CONTEXT);
    context?.peek('positive', { data: { message } });
  }
}
```

## Key Concepts

**Host Element**: Web component that hosts the controller (all Umbraco Elements can be hosts)

**Lifecycle Methods**:
- `hostConnected()` - Called when host element connects to DOM
- `hostDisconnected()` - Called when host element disconnects from DOM
- `destroy()` - Called when controller is permanently destroyed

**Auto-Registration**: Extending `UmbControllerBase` automatically registers/deregisters

**Controller Composition**: Controllers can host other controllers

**Context Access**: Controllers can consume contexts via `getContext()` and `consumeContext()`

**Use Cases**:
- Managing subscriptions and cleanup
- Handling timers and intervals
- Coordinating side effects
- Reusing logic across multiple elements
- Managing API calls and data fetching

**API Calls**: When making API calls from controllers, NEVER use raw `fetch()`. Always use a generated OpenAPI client configured with Umbraco's auth context. See the `umbraco-openapi-client` skill for setup.

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
