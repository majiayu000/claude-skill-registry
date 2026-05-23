---
name: adk-frontend
description: Guidelines for building frontend applications that integrate with Botpress ADK bots - covering authentication, type generation, client setup, and calling bot actions
license: MIT
---

# ADK Frontend Integration

Use this skill when users ask questions about building frontend applications that connect to Botpress ADK bots. This covers authentication patterns, type-safe API calls, client configuration, and integrating generated types.

## What is ADK Frontend Integration?

When you build a bot with the Botpress ADK, you often need a frontend application that interacts with it. This skill provides production-tested patterns for:

- **Authentication** - Cookie-based PAT storage with OAuth flow
- **Client Management** - Zustand store pattern for client caching and reuse
- **Type Generation** - Using ADK-generated types for full type safety
- **Action Calls** - Calling bot actions with proper error handling and optimistic updates

### Key Technologies

- **@botpress/client** - Official TypeScript client for Botpress API
- **Triple-slash references** - TypeScript pattern for importing generated types
- **React Query** - For mutations and cache management (optional but recommended)
- **Zustand** - For client state management

---

## When to Use This Skill

Activate this skill when users ask frontend-related questions like:

### Authentication Questions

- "How do I authenticate with Botpress from my frontend?"
- "What are Personal Access Tokens (PATs)?"
- "Should I use cookies or localStorage for tokens?"
- "How do I implement OAuth login flow?"
- "How do I protect routes based on authentication?"
- "How do I handle token expiration?"

### Client Setup Questions

- "How do I initialize the Botpress client?"
- "What's the best way to manage multiple client instances?"
- "Why use a client store?"
- "How do I create workspace-scoped vs bot-scoped clients?"
- "What's the difference between regular client and Zai client?"

### Type Generation Questions

- "How do I get types for my bot's actions?"
- "What are triple-slash references?"
- "How do I import generated types?"
- "Where are the .adk type files?"
- "How do I keep types in sync between bot and frontend?"
- "Why can't TypeScript find my action types?"

### Calling Actions Questions

- "How do I call a bot action from my frontend?"
- "What's the syntax for client.callAction()?"
- "How do I handle errors when calling actions?"
- "How do I implement optimistic updates?"
- "How do I chain multiple action calls?"
- "How do I use React Query with bot actions?"

---

## Available Documentation

Documentation files in `./references/`:

### Core Integration Patterns

- **authentication.md** - Complete authentication system with PATs, cookies, OAuth, route protection
- **botpress-client.md** - Client initialization, Zustand store pattern, Zai client setup
- **calling-actions.md** - Type-safe action calls, mutations, error handling, optimistic updates
- **type-generation.md** - Triple-slash references, generated types, maintaining type safety

---

## How to Answer Frontend Questions

Frontend questions typically fall into these categories:

### 1. Authentication Implementation

When users ask about authentication, reference the complete pattern from `authentication.md`:

**Key Concepts:**

- PAT generation in Botpress Cloud
- Cookie-based storage (not localStorage)
- AuthContext with React Context API
- OAuth callback flow via cli-login
- Route protection with TanStack Router
- Profile fetching from both Botpress API and bot tables

**Response Pattern:**

1. Explain the authentication strategy (cookies vs localStorage)
2. Show the AuthProvider implementation
3. Demonstrate the OAuth flow
4. Provide route protection examples
5. Highlight security best practices

### 2. Client Setup and Management

When users ask about client configuration, reference `botpress-client.md`:

**Key Concepts:**

- Client initialization with apiUrl, workspaceId, token, botId
- Zustand store for client caching
- Dynamic client keys for reuse
- Workspace-scoped vs bot-scoped clients
- Extended timeouts for Zai operations

**Response Pattern:**

1. Show the clientsStore.ts pattern
2. Explain how client caching works
3. Demonstrate getApiClient() usage
4. Show when to use workspace vs bot-scoped clients
5. Explain getZaiClient() for AI operations

### 3. Type Generation and Import

When users ask about types, reference `type-generation.md`:

**Key Concepts:**

- ADK generates types in `.adk/` directory during dev/build
- Triple-slash directives for referencing external types
- Generated files: action-types.d.ts, table-types.d.ts, workflow-types.d.ts
- Creating type aliases for cleaner code
- Keeping types in sync with adk dev

**Response Pattern:**

1. Explain how ADK generates types
2. Show triple-slash reference syntax
3. Demonstrate importing generated types
4. Provide examples of creating type aliases
5. Show how types stay in sync automatically

### 4. Calling Bot Actions

When users ask about calling actions, reference `calling-actions.md`:

**Key Concepts:**

- client.callAction() signature
- Type-safe input/output with BotActionDefinitions
- Service layer pattern for reusable action calls
- Using useMutation for loading states and error handling
- Optimistic updates for instant UI feedback
- Chaining actions (sequential vs parallel)

**Response Pattern:**

1. Show the basic callAction() syntax
2. Demonstrate type-safe service functions
3. Provide useMutation examples
4. Show error handling patterns
5. Explain optimistic updates when relevant

---

## Common Patterns Reference

### Authentication Flow

```typescript
// 1. Cookie helpers
function setCookie(name: string, value: string, days = 365);
function getCookie(name: string): string | null;
function deleteCookie(name: string);

// 2. AuthContext
interface AuthContextType {
  token: string | null;
  isAuthenticated: boolean;
  userProfile: UserProfile | null;
  isLoadingProfile: boolean;
  login: (token: string) => void;
  logout: () => void;
}

// 3. OAuth Flow
// Redirect: https://app.botpress.cloud/cli-login?redirect=...
// Callback: /auth/callback?pat=bp_pat_...
// Store PAT in cookie and navigate to app
```

### Client Store Pattern

```typescript
// stores/clientsStore.ts
const useClientsStore = create<ClientsState>()((set, get) => ({
  APIClients: {},
  getAPIClient: (props) => {
    const key = props?.botId
      ? `${props.workspaceId}-${props.botId}`
      : (props?.workspaceId ?? DEFAULT_API_CLIENT_KEY);

    const cached = get().APIClients[key];
    if (cached) return cached;

    const newClient = new APIClient({
      apiUrl: API_BASE_URL,
      workspaceId: props?.workspaceId,
      token: getPat() ?? "",
      botId: props?.botId,
    });

    set((state) => ({
      APIClients: { ...state.APIClients, [key]: newClient },
    }));

    return newClient;
  },
}));

export const getApiClient = (props?) =>
  useClientsStore.getState().getAPIClient(props);
```

### Type Import Pattern

```typescript
// types/index.ts
/// <reference path="../../../bot/.adk/action-types.d.ts" />
/// <reference path="../../../bot/.adk/table-types.d.ts" />

import type { BotActionDefinitions } from "@botpress/runtime/_types/actions";
import type { TableDefinitions } from "@botpress/runtime/_types/tables";

// Create type aliases
export type SendMessageAction = BotActionDefinitions["sendMessage"];
export type TicketTableRow = TableDefinitions["TicketsTable"]["Output"];
```

### Action Call Pattern

```typescript
// services/bot-service.ts
export async function sendMessage(input: SendMessageAction["input"]) {
  const client = getApiClient({ botId, workspaceId });
  const result = await client.callAction({
    type: "sendMessage",
    input,
  });
  return result.output as SendMessageAction["output"];
}

// Component usage with useMutation
const { mutate: send, isPending } = useMutation({
  mutationFn: sendMessage,
  onSuccess: () => {
    toast.success("Message sent");
    queryClient.invalidateQueries({ queryKey: ["messages"] });
  },
  onError: (error) => {
    toast.error("Failed to send message");
  },
});
```

---

## Examples of Questions This Skill Answers

### Beginner Questions

- "How do I connect my React app to a Botpress bot?"
- "What is a Personal Access Token?"
- "Where do I find my workspace ID and bot ID?"
- "How do I install @botpress/client?"

### Authentication Questions

- "How should I store authentication tokens?"
- "How do I implement login/logout?"
- "How do I protect authenticated routes?"
- "Should I use cookies or localStorage?"
- "How do I handle the OAuth callback?"

### Type Safety Questions

- "How do I get TypeScript types for my bot?"
- "What are triple-slash references?"
- "Why can't TypeScript find my action types?"
- "How do I keep types in sync?"
- "Where are the generated type files?"

### Implementation Questions

- "How do I call a bot action?"
- "How do I query bot tables from my frontend?"
- "How do I handle loading states?"
- "How do I implement optimistic updates?"
- "How do I chain multiple action calls?"

### Advanced Questions

- "How do I use Zai from my frontend?"
- "What's the difference between workspace and bot-scoped clients?"
- "How do I implement client caching?"
- "How do I handle token expiration?"
- "How do I implement retry logic?"

---

## Response Format

When answering:

1. **Start with a concise explanation** (1-2 paragraphs)
2. **Provide working code examples** from the references
3. **Include file references** (e.g., "From authentication.md:60-85")
4. **Highlight security considerations** when relevant
5. **Show common pitfalls** and how to avoid them
6. **Link to related topics** for deeper exploration

### Example Response Structure

```
Question: "How do I authenticate users in my frontend?"

Answer:
The recommended pattern uses cookie-based PAT storage with OAuth flow.
Here's the complete implementation:

1. Cookie Helpers (authentication.md:89-111)
   [code example]

2. AuthContext Setup (authentication.md:64-76)
   [code example]

3. OAuth Flow (authentication.md:473-533)
   [code example]

Key Security Considerations:
- Use SameSite=Lax for CSRF protection
- Always use HTTPS in production
- Never log PATs to console
- Implement token expiration handling

Related Topics:
- Route protection: authentication.md:369-467
- Profile fetching: authentication.md:304-347
- Client initialization: botpress-client.md:29-51
```

---

## Critical Patterns to Always Reference

When answering questions, always verify these patterns against the documentation:

### 1. Client Management

```typescript
// ✅ CORRECT - Use client store
const client = getApiClient({ workspaceId, botId });

// ❌ WRONG - Create new client every time
const client = new Client({ apiUrl, workspaceId, token, botId });
```

### 2. Type Imports

```typescript
// ✅ CORRECT - Triple-slash at top of file
/// <reference path="../../../bot/.adk/action-types.d.ts" />
import type { BotActionDefinitions } from "@botpress/runtime/_types/actions";

// ❌ WRONG - No triple-slash reference
import type { BotActionDefinitions } from "@botpress/runtime/_types/actions";
```

### 3. Action Calls

```typescript
// ✅ CORRECT - Service layer with types
export async function sendMessage(input: SendMessageAction["input"]) {
  const client = getApiClient({ botId, workspaceId });
  const result = await client.callAction({ type: "sendMessage", input });
  return result.output as SendMessageAction["output"];
}

// ❌ WRONG - Direct call in component
const result = await client.callAction({ type: "sendMessage", input: data });
```

### 4. Authentication Storage

```typescript
// ✅ CORRECT - Cookie with SameSite
document.cookie = `token=${value};expires=${expires};path=/;SameSite=Lax`;

// ❌ WRONG - localStorage without security
localStorage.setItem("token", value);
```

---

## Best Practices to Emphasize

When answering, always mention relevant best practices:

### Security

- Always use HTTPS in production
- Use cookies with SameSite protection
- Never log PATs or tokens
- Implement token expiration handling
- Use HttpOnly cookies when possible (SSR)

### Type Safety

- Always use generated types from ADK
- Create type aliases for cleaner code
- Use triple-slash references correctly
- Keep types in sync with adk dev
- Type all action inputs and outputs

### Performance

- Cache clients with Zustand store
- Use workspace-scoped clients when no bot operations needed
- Implement optimistic updates for better UX
- Use React Query for cache management
- Run independent actions in parallel

### Error Handling

- Always handle 401 (expired token) errors
- Provide user feedback on errors
- Implement retry logic for transient failures
- Log errors appropriately (never log tokens)
- Show loading states during async operations

### Code Organization

- Use service layer for action calls
- Centralize types in single file
- Keep authentication logic in context
- Separate client configuration from usage
- Reuse service functions across components

---

## Troubleshooting Common Issues

Be prepared to help with these common problems:

### "Cannot find module '@botpress/runtime/\_types/actions'"

- Check triple-slash reference path
- Verify .adk/ directory exists
- Restart TypeScript server
- Ensure adk dev/build has run

### "Types not updating after bot changes"

- Restart adk dev
- Delete .adk/ and rebuild
- Restart TypeScript server
- Check for bot compilation errors

### "Authentication fails after reload"

- Implement reload retry logic (authentication.md:191-220)
- Check cookie expiration
- Verify token is being retrieved correctly
- Check for CORS issues

### "Client timeout on long operations"

- Use getZaiClient() with extended timeout for AI operations
- Don't use regular client for Zai operations
- Consider breaking into smaller operations

## Summary

This skill covers the complete frontend integration story for Botpress ADK:

**Core Topics:**

1. Authentication with PATs and cookies
2. Client management with Zustand
3. Type generation and import with triple-slash references
4. Calling bot actions with full type safety

**When to Use:**

- Any frontend integration question
- Authentication and security patterns
- Type safety and generated types
- Client setup and configuration
- Action calls and error handling

**Key Principle:**
Always provide production-ready patterns that emphasize type safety, security, and maintainability.
