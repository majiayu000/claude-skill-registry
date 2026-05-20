---
name: webmcp-authentication
description: Implement WebMCP authentication patterns — browser session inheritance, cookie-based auth, role-gated tool registration, and conditional tool exposure. Use when managing which tools are available based on user authentication state.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WebMCP Authentication

## Before writing code

**Fetch live docs**:
1. Fetch `https://webmachinelearning.github.io/webmcp/` for authentication-related sections of the spec
2. Web-search `webmcp authentication session cookies browser agent` for auth pattern guidance
3. Web-search `site:developer.chrome.com webmcp security authentication` for Chrome security model
4. Web-search `site:github.com mcp-b security authentication` for polyfill security guidance

## Conceptual Architecture

### How WebMCP Authentication Works

WebMCP's auth model is fundamentally different from backend API authentication:

1. **No separate agent login** — The agent inherits the user's browser session
2. **Cookies and headers** — Tools' fetch calls automatically include the user's cookies and auth headers
3. **Same-origin policy** — Tools operate within the page's origin, bound by standard browser security
4. **Session-based** — If the user is logged in, tools have the user's permissions; if not, tools have anonymous access

This means the agent **acts as the user**, not as a separate entity with its own credentials.

### Authentication Flow

```
User logs in to site (normal browser auth)
  → Page loads with authenticated session
  → JavaScript checks user auth state
  → If authenticated: register full tool set (search, cart, checkout, account)
  → If anonymous: register limited tool set (search, viewDetails only)
  → Agent discovers available tools based on current auth state
```

### Role-Gated Tool Registration

Register tools conditionally based on user permissions:

```js
// Always register read-only tools
registerPublicTools();

// Register transactional tools only for authenticated users
if (user.isAuthenticated) {
  registerCartTools();
  registerAccountTools();
}

// Register admin tools only for admin users
if (user.role === "admin") {
  registerAdminTools();
}
```

### Auth State Changes

Handle login/logout during an agent session:

```js
// On login
authService.onLogin((user) => {
  registerAuthenticatedTools(user);
});

// On logout
authService.onLogout(() => {
  navigator.modelContext.clearContext();
  registerPublicTools(); // Re-register only anonymous tools
});
```

### Session Expiration

Tools must handle session expiration gracefully:

```js
async execute(input) {
  const res = await fetch("/api/cart", { credentials: "same-origin" });
  if (res.status === 401) {
    return {
      status: "error",
      code: "session_expired",
      message: "Your session has expired. Please log in again."
    };
  }
  return await res.json();
}
```

### Security Considerations

1. **Never expose auth tokens to the agent** — The agent doesn't need to see cookies or tokens; the browser handles them
2. **Server-side validation** — Always validate the session server-side; don't trust client-side auth checks alone
3. **CSRF protection** — Tools making POST requests should include CSRF tokens (the page already has them)
4. **Sensitive tools need confirmation** — Even authenticated users should confirm destructive actions via `requestUserInteraction`
5. **No credential storage** — Never register tools that accept passwords or credentials as parameters

### Multi-Factor Authentication

If an action requires MFA (e.g., changing payment method):

```js
async execute(input, client) {
  // Check if action requires MFA
  const mfaRequired = await fetch("/api/check-mfa-required");
  if (mfaRequired) {
    await client.requestUserInteraction((resolve) => {
      // Site shows MFA challenge (OTP input, biometric prompt, etc.)
      showMfaChallenge(resolve);
    });
  }
  // Proceed with the action
  // ...
}
```

### Best Practices

- Check auth state before registering tools, not during tool execution
- Clear all tools on logout to prevent stale tool exposure
- Return clear, structured error responses for auth failures
- Never pass sensitive user data (email, address, card) as tool input parameters — fetch it server-side
- Log tool invocations with user identity for audit trails
- Handle token refresh transparently within tool callbacks

Fetch the specification for any authentication-specific APIs, secure context requirements, and browser permission model details before implementing.
