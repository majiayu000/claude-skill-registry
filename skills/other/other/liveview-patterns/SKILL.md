---
name: liveview-patterns
description: "Provide LiveView implementation patterns — real-time notifications with PubSub subscriptions, file upload handlers, reusable modal components, form events with phx-change/phx-submit, async data loading with assign_async, stream-based lists. Use when implementing PubSub notifications, adding file uploads to forms, building LiveView components, or debugging handle_event lifecycle. NOT for writing ExUnit tests (testing), controllers, REST APIs, or Ecto queries."
effort: medium
user-invocable: false
---

# LiveView Patterns Reference

Reference for building with Phoenix LiveView 1.0/1.1.

## Iron Laws — Never Violate These

1. **NO DATABASE QUERIES IN DISCONNECTED MOUNT** — Queries run TWICE (HTTP + WebSocket). Use `assign_async`
2. **ALWAYS USE STREAMS FOR LISTS** — Regular assigns = O(n) memory per user. Streams = O(1)
3. **CHECK connected?/1 BEFORE SUBSCRIPTIONS** — Prevents double subscriptions
4. **EXTRACT VARIABLES BEFORE assign_async CLOSURE** — Closures copy entire referenced variables
5. **LOAD PRIMARY DATA IN mount/3, PAGINATION IN handle_params/3** — handle_params runs on EVERY URL change
6. **NEVER PASS SOCKET TO BUSINESS LOGIC** — Extract data before calling contexts
7. **CHECK CHANGESET ERRORS BEFORE UI DEBUGGING** — Silent form save = check `{:error, changeset}` first, not viewport/JS
8. **HIDDEN INPUTS FOR ALL REQUIRED EMBEDDED FIELDS** — Every required field in an embedded schema MUST have a `hidden_input` if not directly editable
9. **NEVER USE `assign_new` FOR LIFECYCLE VALUES** — `assign_new` skips the function if key exists. Use `assign/3` for locale, current user, or any value refreshed every mount

## Memory Impact

| Pattern | 3K items | 10K users × 10K items |
|---------|----------|----------------------|
| Regular assigns | ~5.1 MB | ~10+ GB |
| Streams | ~1.1 MB | Minimal (O(1)) |

**Decision**: Lists with >100 items → Use streams, not assigns

## Quick Patterns

### Async Assigns (CRITICAL)

```elixir
def mount(%{"slug" => slug}, _session, socket) do
  # Extract needed values BEFORE the closure
  scope = socket.assigns.current_scope

  {:ok,
   socket
   |> assign_async(:org, fn -> {:ok, %{org: fetch_org(scope, slug)}} end)}
end
```

### Streams for Lists

```elixir
def mount(_params, _session, socket) do
  {:ok, stream(socket, :items, Items.list_items())}
end

# Insert/update/delete
stream_insert(socket, :items, item, at: 0)
stream_delete(socket, :items, item)
```

### PubSub with connected? check

```elixir
def mount(_params, _session, socket) do
  if connected?(socket), do: Chat.subscribe(room_id)
  {:ok, socket}
end
```

## Navigation Decision Tree

```
Same LiveView, different params? → patch / push_patch
Different LiveView, same live_session? → navigate / push_navigate
Different live_session or non-LiveView? → href / redirect
```

## Component Decision Tree

```
Does component need BOTH internal state AND event handling?
│
├── YES → Does it encapsulate APPLICATION logic (not just DOM)?
│   ├── YES → Use LiveComponent ✅
│   └── NO → Refactor to function component with parent handling
│
└── NO → Use Function Component ✅
```

**Official guidance**: "Prefer function components over live components"

## Common Anti-patterns

| Wrong | Right |
|-------|-------|
| DB queries without `assign_async` | Use `assign_async` for all queries |
| `assign(socket, items: list)` for lists | `stream(socket, :items, list)` |
| PubSub subscribe without `connected?` | `if connected?(socket), do: subscribe()` |
| Passing socket to context functions | Extract `socket.assigns` first |
| Business logic in `handle_event` | Delegate to context |
| `assign_new` for locale/user in hooks | `assign/3` (must run every mount) |

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/async-streams.md` - assign_async, stream_async, streams
- `${CLAUDE_SKILL_DIR}/references/forms-uploads.md` - Forms, validation, file uploads
- `${CLAUDE_SKILL_DIR}/references/components.md` - Function components, LiveComponents
- `${CLAUDE_SKILL_DIR}/references/pubsub-navigation.md` - PubSub, navigation, JS commands
- `${CLAUDE_SKILL_DIR}/references/js-interop.md` - Third-party JS libraries, phx-update="ignore", hooks
- `${CLAUDE_SKILL_DIR}/references/channels-presence.md` - Phoenix Channels, Presence, token auth
