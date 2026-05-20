---
name: liveview-code-review
description: Reviews Phoenix LiveView code for lifecycle patterns, assigns/streams usage, components, and security. Use when reviewing LiveView modules, .heex templates, or LiveComponents.
---

# LiveView Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| mount, handle_params, handle_event, handle_async | [references/lifecycle.md](references/lifecycle.md) |
| When to use assigns vs streams, AsyncResult | [references/assigns-streams.md](references/assigns-streams.md) |
| Function vs LiveComponent, slots, attrs | [references/components.md](references/components.md) |
| Authorization per event, phx-value trust | [references/security.md](references/security.md) |

## Review Checklist

### Critical Issues
- [ ] No socket copying into async functions (extract values first)
- [ ] Every handle_event validates authorization
- [ ] No sensitive data in assigns (visible in DOM)
- [ ] phx-value data is validated (user-modifiable)

### Lifecycle
- [ ] Subscriptions wrapped in `connected?(socket)`
- [ ] handle_params used for URL-based state
- [ ] handle_async handles :loading and :error states

### Data Management
- [ ] Streams used for large collections (100+ items)
- [ ] temporary_assigns for data not needed after render
- [ ] AsyncResult patterns for loading states

### Components
- [ ] Function components preferred over LiveComponents
- [ ] LiveComponents preserve :inner_block in update/2
- [ ] Slots use proper attr declarations
- [ ] phx-debounce on text inputs

## Valid Patterns (Do NOT Flag)

- **Empty mount returning {:ok, socket}** - Valid for simple LiveViews
- **Using assigns for small lists** - Streams only needed for 100+ items
- **LiveComponent without update/2** - Default update/2 assigns all
- **phx-click without phx-value** - Event may not need data
- **Inline function in heex** - Valid for simple transforms

## Context-Sensitive Rules

| Issue | Flag ONLY IF |
|-------|--------------|
| Missing debounce | Input is text/textarea AND triggers server event |
| Use streams | Collection has 100+ items OR is paginated |
| Missing auth check | Event modifies data AND no auth in mount |

## Critical Anti-Patterns

### Socket Copying (MOST IMPORTANT)

```elixir
# BAD - socket copied into async function
def handle_event("load", _, socket) do
  Task.async(fn ->
    user = socket.assigns.user  # Socket copied!
    fetch_data(user.id)
  end)
  {:noreply, socket}
end

# GOOD - extract values first
def handle_event("load", _, socket) do
  user_id = socket.assigns.user.id
  Task.async(fn ->
    fetch_data(user_id)  # Only primitive copied
  end)
  {:noreply, socket}
end
```

### Missing Authorization

```elixir
# BAD - trusts phx-value without auth
def handle_event("delete", %{"id" => id}, socket) do
  Posts.delete_post!(id)  # Anyone can delete any post!
  {:noreply, socket}
end

# GOOD - verify authorization
def handle_event("delete", %{"id" => id}, socket) do
  post = Posts.get_post!(id)

  if post.user_id == socket.assigns.current_user.id do
    Posts.delete_post!(post)
    {:noreply, stream_delete(socket, :posts, post)}
  else
    {:noreply, put_flash(socket, :error, "Unauthorized")}
  end
end
```

## Before Submitting Findings

Use the issue format: `[FILE:LINE] ISSUE_TITLE` for each finding.

Load and follow [review-verification-protocol](../review-verification-protocol/SKILL.md) before reporting any issue.
