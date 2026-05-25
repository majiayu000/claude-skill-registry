---
name: phoenix-contexts
description: "Phoenix context design — creating/splitting contexts, Scope (1.8+), Ecto.Multi, PubSub, routers, plugs, controllers. Use when editing contexts, routers, or designing boundaries."
effort: medium
user-invocable: false
---

# Phoenix Contexts Reference

Reference for designing and implementing Phoenix contexts (bounded contexts).

## Iron Laws — Never Violate These

1. **CONTEXTS OWN THEIR DATA** — Never query another context's schema directly via Repo
2. **SCOPES ARE MANDATORY (Phoenix 1.8+)** — Every context function MUST accept scope as first parameter
3. **THIN CONTROLLERS/LIVEVIEWS** — Controllers translate HTTP, business logic stays in contexts
4. **NO SIDE EFFECTS IN SCHEMAS** — Use `Ecto.Multi` for transactions with side effects

## Context Structure

```
lib/my_app/
├── accounts/           # Context directory
│   ├── user.ex         # Schema
│   ├── scope.ex        # Scope struct (Phoenix 1.8+)
├── accounts.ex         # Context module (public API)
```

## Phoenix 1.8+ Scopes (CRITICAL)

All context functions MUST accept scope as first parameter:

```elixir
def list_posts(%Scope{} = scope) do
  from(p in Post, where: p.user_id == ^scope.user.id)
  |> Repo.all()
end

def create_post(%Scope{} = scope, attrs) do
  %Post{user_id: scope.user.id}
  |> Post.changeset(attrs)
  |> Repo.insert()
  |> broadcast(scope, :created)
end
```

## Quick Decisions

### When to SPLIT contexts?

- Module exceeds ~400 lines
- Functions don't share domain language
- Could theoretically be a separate microservice
- Team member could own it independently

### When to KEEP together?

- Resources share vocabulary and domain concepts
- Functions frequently operate on same data together
- Splitting would create excessive cross-context calls

### Cross-Context References

```elixir
# ✅ Reference by ID, convert at boundary
def create_order(%Scope{} = scope, user_id, product_ids) do
  with {:ok, user} <- Accounts.fetch_user(scope, user_id) do
    do_create_order(scope, user.id, product_ids)
  end
end

# ❌ Reaching into other context's internals
alias MyApp.Accounts.User  # Don't do this
Repo.all(from o in Order, join: u in User, ...)  # Don't query other schemas
```

## Anti-patterns

| Wrong | Right |
|-------|-------|
| Service objects (`UserCreationService`) | Context functions (`Accounts.create_user/2`) |
| Repository pattern wrapping Repo | Repo IS the repository |
| Direct Repo calls in controllers | Delegate to context |
| Schema callbacks with side effects | Use Ecto.Multi |

## Version Notes

- **Phoenix 1.8+**: Uses built-in `%Scope{}` struct for authorization context
- **Phoenix 1.7**: Requires manual authorization context (see `${CLAUDE_SKILL_DIR}/references/scopes-auth.md` "Pre-Scopes Patterns")

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/context-patterns.md` - Full context module, PubSub, Multi, cross-boundary
- `${CLAUDE_SKILL_DIR}/references/scopes-auth.md` - Scope struct, multi-tenant, authorization, plugs
- `${CLAUDE_SKILL_DIR}/references/routing-patterns.md` - Verified routes, pipelines, API auth
- `${CLAUDE_SKILL_DIR}/references/plug-patterns.md` - Function/module plugs, placement, guards
- `${CLAUDE_SKILL_DIR}/references/json-api-patterns.md` - JSON controllers, FallbackController, API auth
