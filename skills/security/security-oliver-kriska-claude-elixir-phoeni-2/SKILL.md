---
name: security
description: Enforce Elixir/Phoenix security — auth, OAuth, sessions, CSRF, XSS, SQL
  injection, input validation, secrets. Use when editing auth files, login flows,
  RBAC, or API keys.
---

# Elixir/Phoenix Security Reference

> **Ash projects**: `AshAuthentication` has its own strategy/token patterns — use the `ash-framework` skill. CSRF, XSS, and secret management patterns below still apply.

Quick reference for security patterns in Elixir/Phoenix.

## Iron Laws — Never Violate These

1. **VALIDATE AT BOUNDARIES** — Never trust client input. All data through changesets
2. **NEVER INTERPOLATE USER INPUT** — Use Ecto's `^` operator, never string interpolation
3. **NO String.to_atom WITH USER INPUT** — Atom exhaustion DoS. Use `to_existing_atom/1`
4. **AUTHORIZE EVERYWHERE** — Check in contexts AND re-validate in LiveView events
5. **ESCAPE BY DEFAULT** — Never use `raw/1` with untrusted content
6. **SECRETS NEVER IN CODE** — All secrets in `runtime.exs` from env vars
7. **LIVEVIEW EVENT PARAMS ARE UNTRUSTED** — Users can alter forms, hooks, and every `phx-value-*` in DevTools. Validate and authorize against server-side state before acting

## Quick Patterns

### Timing-Safe Authentication

```elixir
def authenticate(email, password) do
  user = Repo.get_by(User, email: email)

  cond do
    user && Argon2.verify_pass(password, user.hashed_password) ->
      {:ok, user}
    user ->
      {:error, :invalid_credentials}
    true ->
      Argon2.no_user_verify()  # Timing attack prevention
      {:error, :invalid_credentials}
  end
end
```

### LiveView Authorization (CRITICAL)

```elixir
# `id` is client input even when it came from phx-value-id.
# RE-AUTHORIZE IN EVERY EVENT HANDLER
def handle_event("delete", %{"id" => id}, socket) do
  post = Blog.get_post!(id)

  # Don't trust that mount authorized this action!
  with :ok <- Bodyguard.permit(Blog, :delete_post, socket.assigns.current_user, post) do
    Blog.delete_post(post)
    {:noreply, stream_delete(socket, :posts, post)}
  else
    _ -> {:noreply, put_flash(socket, :error, "Unauthorized")}
  end
end
```

Rendered LiveView events can expose IDs in HTML and websocket payloads. That is
not automatically a vulnerability: treat IDs as public identifiers, never as
proof of access. Use opaque references only when the identifier itself must not
be disclosed, and still perform server-side authorization.

### SQL Injection Prevention

```elixir
# ✅ SAFE: Parameterized queries
from(u in User, where: u.name == ^user_input)

# ❌ VULNERABLE: String interpolation
from(u in User, where: fragment("name = '#{user_input}'"))
```

## Quick Decisions

### What to validate?

- **All user input** → Ecto changesets
- **File uploads** → Extension + magic bytes + size
- **Paths** → `Path.safe_relative/2` for traversal
- **Atoms** → `String.to_existing_atom/1` only

### What to escape?

- **HTML output** → Auto-escaped by default (`<%= %>`)
- **User HTML** → HtmlSanitizeEx with scrubber
- **Never** → `raw/1` with untrusted content

## Anti-patterns

| Wrong | Right |
|-------|-------|
| `"SELECT * FROM users WHERE name = '#{name}'"` | `from(u in User, where: u.name == ^name)` |
| `String.to_atom(user_input)` | `String.to_existing_atom(user_input)` |
| `<%= raw @user_comment %>` | `<%= @user_comment %>` |
| Hardcoded secrets in config | `runtime.exs` from env vars |
| Auth only in mount | Re-auth in every `handle_event` |
| Trusting `phx-value-*` or hidden IDs | Load server-side state and authorize it |

## References

For detailed patterns, see:

- `references/authentication.md` - phx.gen.auth, MFA, sessions
- `references/authorization.md` - Bodyguard, scopes, LiveView auth
- `references/input-validation.md` - Changesets, file uploads, paths
- `references/security-headers.md` - CSP, CSRF, rate limiting, headers
- `references/oauth-linking.md` - OAuth account linking, token management
- `references/rate-limiting.md` - Composite key strategies, Hammer patterns
- `references/advanced-patterns.md` - SSRF prevention, secrets management, supply chain
