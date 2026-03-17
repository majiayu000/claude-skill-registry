---
name: umbraco-global-context
description: Implement global contexts in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Global Context

## What is it?
Global contexts create a shared, type-safe layer of data and functions accessible throughout the backoffice. Unlike scoped contexts (like Workspace Contexts), global contexts persist for the entire backoffice session. Use them for sharing state between extensions, managing centralized services, or coordinating communication. Note: Prefer more specific context types when possible - Umbraco uses global contexts sparingly.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/global-context
- **Context API**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/context-api
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Related Foundation Skills

- **Context API**: For understanding context consumption patterns
  - Reference skill: `umbraco-context-api`

- **State Management**: For reactive state within contexts
  - Reference skill: `umbraco-state-management`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What state to share? What services needed? Could a workspace context work instead?
3. **Generate files** - Create context token + implementation + manifest based on latest docs
4. **Explain** - Show what was created and how to consume the context

## Minimal Examples

### Context Token (my-global-context.token.ts)
```typescript
import { UmbContextToken } from '@umbraco-cms/backoffice/context-api';
import type { MyGlobalContext } from './my-global-context.js';

export const MY_GLOBAL_CONTEXT = new UmbContextToken<MyGlobalContext>(
  'My.GlobalContext'
);
```

### Context Implementation (my-global-context.ts)
```typescript
import { UmbContextBase } from '@umbraco-cms/backoffice/class-api';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';
import { MY_GLOBAL_CONTEXT } from './my-global-context.token.js';

export class MyGlobalContext extends UmbContextBase {
  #currentValue = '';

  constructor(host: UmbControllerHost) {
    super(host, MY_GLOBAL_CONTEXT);
  }

  getValue(): string {
    return this.#currentValue;
  }

  setValue(value: string): void {
    this.#currentValue = value;
  }
}
```

### Manifest (umbraco-package.json)
```json
{
  "name": "My Global Context Package",
  "extensions": [
    {
      "type": "globalContext",
      "alias": "My.GlobalContext",
      "name": "My Global Context",
      "js": "/App_Plugins/MyPackage/my-global-context.js"
    }
  ]
}
```

### Consuming the Context
```typescript
import { UmbElementMixin } from '@umbraco-cms/backoffice/element-api';
import { MY_GLOBAL_CONTEXT } from './my-global-context.token.js';

class MyElement extends UmbElementMixin(LitElement) {
  #myContext?: MyGlobalContext;

  constructor() {
    super();
    this.consumeContext(MY_GLOBAL_CONTEXT, (instance) => {
      this.#myContext = instance;
    });
  }
}
```

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
