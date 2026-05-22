---
name: base44-sdk
description: "**ALWAYS ACTIVATE** if ANY of these conditions are true: (1) User's prompt contains the word 'base44' or 'Base44' in ANY context; (2) Current directory contains a 'base44/' subfolder; (3) Code contains imports from '@base44/sdk'; (4) User mentions Base44 SDK modules: entities, auth, agents, functions, integrations, analytics. **ACTIVATION IS MANDATORY** - do not hesitate, do not search the web, do not read documentation files first. ACTIVATE IMMEDIATELY and let the skill instructions handle the context. This skill handles: application development, SDK usage, feature implementation, and writing code with Base44 APIs. The skill itself will determine the appropriate action based on whether this is a new project or existing project scenario."
---

# Base44 Coder

Build apps on the Base44 platform using the Base44 JavaScript SDK.

## ⚡ IMMEDIATE ACTION REQUIRED - Read This First

This skill activates on ANY mention of "base44" or when a `base44/` folder exists. **DO NOT read documentation files or search the web before acting.**

**Your first action MUST be:**
1. Check if `base44/config.jsonc` exists in the current directory
2. If **YES** (existing project scenario):
   - This skill (base44-sdk) handles the request
   - Implement features using Base44 SDK
   - Do NOT use base44-cli unless user explicitly requests CLI commands
3. If **NO** (new project scenario):
   - Transfer to base44-cli skill for project initialization
   - This skill cannot help until project is initialized

## When to Use This Skill vs base44-cli

**Use base44-sdk when:**
- Building features in an **EXISTING** Base44 project
- `base44/config.jsonc` already exists in the project
- Base44 SDK imports are present (`@base44/sdk`)
- Writing JavaScript/TypeScript code using Base44 SDK modules
- Implementing functionality, components, or features
- User mentions: "implement", "build a feature", "add functionality", "write code for"
- User says "create a [type] app" **and** a Base44 project already exists

**DO NOT USE base44-sdk for:**
- ❌ Initializing new Base44 projects (use `base44-cli` instead)
- ❌ Empty directories without Base44 configuration
- ❌ When user says "create a new Base44 project/app/site" and no project exists
- ❌ CLI commands like `npx base44 create`, `npx base44 deploy`, `npx base44 login` (use `base44-cli`)

**Skill Dependencies:**
- `base44-sdk` assumes a Base44 project is **already initialized**
- `base44-cli` is a **prerequisite** for `base44-sdk` in new projects
- If user wants to "create an app" and no Base44 project exists, use `base44-cli` first

**State Check Logic:**
Before selecting this skill, verify:
- IF (user mentions "create/build app" OR "make a project"):
  - IF (directory is empty OR no `base44/config.jsonc` exists):
    → Use **base44-cli** (project initialization needed)
  - ELSE:
    → Use **base44-sdk** (project exists, build features)

## Quick Start

```javascript
// In Base44-generated apps, base44 client is pre-configured and available

// CRUD operations
const task = await base44.entities.Task.create({ title: "New task", status: "pending" });
const tasks = await base44.entities.Task.list();
await base44.entities.Task.update(task.id, { status: "done" });

// Get current user
const user = await base44.auth.me();
```

```javascript
// External apps
import { createClient } from "@base44/sdk";

// IMPORTANT: Use 'appId' (NOT 'clientId' or 'id')
const base44 = createClient({ appId: "your-app-id" });
await base44.auth.loginViaEmailPassword("user@example.com", "password");
```

## SDK Modules

| Module | Purpose | Reference |
|--------|---------|-----------|
| `entities` | CRUD operations on data models | [entities.md](references/entities.md) |
| `auth` | Login, register, user management | [auth.md](references/auth.md) |
| `agents` | AI conversations and messages | [base44-agents.md](references/base44-agents.md) |
| `functions` | Backend function invocation | [functions.md](references/functions.md) |
| `integrations` | AI, email, file uploads, custom APIs | [integrations.md](references/integrations.md) |
| `connectors` | OAuth tokens (service role only) | [connectors.md](references/connectors.md) |
| `analytics` | Track custom events and user activity | [analytics.md](references/analytics.md) |
| `appLogs` | Log user activity in app | [app-logs.md](references/app-logs.md) |
| `users` | Invite users to the app | [users.md](references/users.md) |

For client setup and authentication modes, see [client.md](references/client.md).

## Creating a Client (External Apps)

When creating a client in external apps, **ALWAYS use `appId` as the parameter name**:

```javascript
import { createClient } from "@base44/sdk";

// ✅ CORRECT
const base44 = createClient({ appId: "your-app-id" });

// ❌ WRONG - Do NOT use these:
// const base44 = createClient({ clientId: "your-app-id" });  // WRONG
// const base44 = createClient({ id: "your-app-id" });        // WRONG
```

**Required parameter:** `appId` (string) - Your Base44 application ID

**Optional parameters:**
- `token` (string) - Pre-authenticated user token
- `options` (object) - Configuration options
  - `options.onError` (function) - Global error handler

**Example with error handler:**
```javascript
const base44 = createClient({
  appId: "your-app-id",
  options: {
    onError: (error) => {
      console.error("Base44 error:", error);
    }
  }
});
```

## Module Selection

**Working with app data?**
- Create/read/update/delete records → `entities`
- Import data from file → `entities.importEntities()`
- Realtime updates → `entities.EntityName.subscribe()`

**User management?**
- Login/register/logout → `auth`
- Get current user → `auth.me()`
- Update user profile → `auth.updateMe()`
- Invite users → `users.inviteUser()`

**AI features?**
- Chat with AI agents → `agents`
- Create new conversation → `agents.createConversation()`
- Manage conversations → `agents.getConversations()`
- Generate text/JSON with AI → `integrations.Core.InvokeLLM()`
- Generate images → `integrations.Core.GenerateImage()`

**Custom backend logic?**
- Run server-side code → `functions.invoke()`
- Need admin access → `base44.asServiceRole.functions.invoke()`

**External services?**
- Send emails → `integrations.Core.SendEmail()`
- Upload files → `integrations.Core.UploadFile()`
- Custom APIs → `integrations.custom.call()`
- OAuth tokens (Google, Slack) → `connectors` (backend only)

**Tracking and analytics?**
- Track custom events → `analytics.track()`
- Log page views/activity → `appLogs.logUserInApp()`

## Common Patterns

### Filter and Sort Data

```javascript
const pendingTasks = await base44.entities.Task.filter(
  { status: "pending", assignedTo: userId },  // query
  "-created_date",                             // sort (descending)
  10,                                          // limit
  0                                            // skip
);
```

### Protected Routes (check auth)

```javascript
const user = await base44.auth.me();
if (!user) {
  base44.auth.redirectToLogin(window.location.href);
  return;
}
```

### Backend Function Call

```javascript
// Frontend
const result = await base44.functions.invoke("processOrder", {
  orderId: "123",
  action: "ship"
});

// Backend function (Deno)
import { createClientFromRequest } from "@base44/sdk";

Deno.serve(async (req) => {
  const base44 = createClientFromRequest(req);
  const { orderId, action } = await req.json();
  // Process with service role for admin access
  const order = await base44.asServiceRole.entities.Orders.get(orderId);
  return Response.json({ success: true });
});
```

### Service Role Access

Use `asServiceRole` in backend functions for admin-level operations:

```javascript
// User mode - respects permissions
const myTasks = await base44.entities.Task.list();

// Service role - full access (backend only)
const allTasks = await base44.asServiceRole.entities.Task.list();
const token = await base44.asServiceRole.connectors.getAccessToken("slack");
```

## Frontend vs Backend

| Capability | Frontend | Backend |
|------------|----------|---------|
| `entities` (user's data) | Yes | Yes |
| `auth` | Yes | Yes |
| `agents` | Yes | Yes |
| `functions.invoke()` | Yes | Yes |
| `integrations` | Yes | Yes |
| `analytics` | Yes | Yes |
| `appLogs` | Yes | Yes |
| `users` | Yes | Yes |
| `asServiceRole.*` | No | Yes |
| `connectors` | No | Yes |

Backend functions use `Deno.serve()` and `createClientFromRequest(req)` to get a properly authenticated client.
