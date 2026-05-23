---
name: add-ws-action
description: Add a new outgoing WebSocket action with typed payload and API exposure
aliases: [new-ws-action, add-websocket-action, create-ws-action]
---

# Add WebSocket Action Skill

## Usage
```
/add-ws-action <actionName>
```

---

## Step 1: Ask Questions

### 1. Action Purpose
```
What does this action do?
Brief description:
```

### 2. Parameters
```
What parameters does the action need?

List each with type:
- param1: string
- param2: number
- etc.
```

### 3. Public API
```
Expose in window.Gemini.WebSocket?

A) Yes - Users can call it
B) No - Internal only (used by features)
```

### 4. Middleware
```
Does this action need middleware?

A) No - Just send
B) Yes - Intercept/modify/block
```

---

## Step 2: Add Message Type

### In `src/websocket/protocol.ts`

```typescript
// 1. Add to enum
export enum ClientToServerMessageType {
    // ... existing
    <ACTION_NAME> = '<actionName>',
}

// 2. Define payload type
export interface <ActionName>Payload {
    param1: string;
    param2: number;
}

// 3. Add to message map (if exists)
export interface ClientToServerMessageMap {
    // ... existing
    [ClientToServerMessageType.<ACTION_NAME>]: <ActionName>Payload;
}
```

---

## Step 3: Add Action to API

### In `src/websocket/api.ts`

```typescript
import { ClientToServerMessageType } from './protocol';
import { send } from './connection';
import type { <ActionName>Payload } from './protocol';

/**
 * <Description of what this action does>
 * @param param1 - Description
 * @param param2 - Description
 */
export function <actionName>(param1: string, param2: number): void {
    send({
        type: ClientToServerMessageType.<ACTION_NAME>,
        data: { param1, param2 } satisfies <ActionName>Payload,
    });
}
```

**Keep API simple** - Users pass parameters, not raw payloads.

---

## Step 4: Expose in Public API (if applicable)

### In `src/api/index.ts`

```typescript
import { <actionName> } from '../websocket/api';

WebSocket: {
    // ... existing
    <actionName>,
}
```

Accessible via `window.Gemini.WebSocket.<actionName>(...)`.

---

## Step 5: Optional - Add Middleware

### Create `src/websocket/middlewares/<actionName>.ts`

```typescript
import { registerMiddleware } from './registry';
import { ClientToServerMessageType } from '../protocol';
import type { ClientToServerMessage } from '../protocol';

let unregister: (() => void) | null = null;

function processMessage(message: ClientToServerMessage): ClientToServerMessage | null {
    if (message.type !== ClientToServerMessageType.<ACTION_NAME>) {
        return message;  // Pass through
    }

    console.log('[<ActionName>] Intercepted:', message.data);

    // Modify
    // return { ...message, data: { ...message.data, modified: true } };

    // Block
    // return null;

    // Pass through
    return message;
}

export function register<ActionName>Middleware(): void {
    if (unregister) return;
    unregister = registerMiddleware(processMessage);
}

export function unregister<ActionName>Middleware(): void {
    unregister?.();
    unregister = null;
}
```

---

## Step 6: Validate

### Protocol
- [ ] Message type added to `ClientToServerMessageType` enum
- [ ] Payload interface defined
- [ ] No hardcoded type strings

### API
- [ ] Action function in `src/websocket/api.ts`
- [ ] Typed parameters (no `unknown` or `any`)
- [ ] Uses `send()` from `connection.ts`
- [ ] JSDoc documentation

### Public API (if applicable)
- [ ] Exposed in `src/api/index.ts`
- [ ] Callable via `window.Gemini.WebSocket.<actionName>()`

### Middleware (if applicable)
- [ ] Returns `message` or `null`, never throws
- [ ] Has register/unregister functions
- [ ] Unregisters on cleanup

---

## References

- Rules: `.claude/rules/websocket/websocket.md`
- Existing actions: `src/websocket/api.ts`
- Protocol: `src/websocket/protocol.ts`
- Middlewares: `src/websocket/middlewares/`
