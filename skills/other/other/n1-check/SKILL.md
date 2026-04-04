---
name: ecto:n1-check
description: "Scan Ecto code for N+1 anti-patterns — Repo calls in loops, missing preloads, unpreloaded associations. Use when excessive queries reported or wanting an N+1 audit."
effort: medium
allowed-tools: Read, Grep, Glob, Bash
---

# N+1 Query Detection

Identify and fix N+1 query anti-patterns in Ecto/Phoenix applications.

## Iron Laws - Never Violate These

1. **Never access associations without preload** - Always preload before `Enum.map`
2. **No Repo calls inside loops** - Restructure to batch queries
3. **Preload at context boundary** - Load associations in context, not controllers/views
4. **Use joins for filtering** - Use `join` + `preload` when filtering by association

## Detection Patterns

### Pattern 1: Enum.map with Repo

```elixir
# BAD: N+1 queries
users
|> Enum.map(fn user -> Repo.get(Order, user.order_id) end)

# GOOD: Single query with preload
users
|> Repo.preload(:orders)
```

### Pattern 2: Association Access Without Preload

```elixir
# BAD: Lazy loading triggers N queries
for user <- users do
  user.posts  # Triggers query for each user!
end

# GOOD: Eager load first
users = Repo.all(User) |> Repo.preload(:posts)
for user <- users do
  user.posts  # Already loaded
end
```

### Pattern 3: Nested Association Access

```elixir
# BAD: N+1 for nested associations
user.posts |> Enum.map(fn post -> post.comments end)

# GOOD: Nested preload
Repo.preload(user, posts: :comments)
```

## Quick Detection Commands

Use Grep with context lines (`-B 5 -A 5`) to find `Enum.map` near `Repo.` calls in `lib/**/*.ex`.
Use Grep to find association access patterns (`.posts`, `.comments`, `.orders`) in `lib/**/*.ex`.
Use Grep with context (`-B 3`) to find `Repo.get` or `Repo.one` near loop patterns (`for`, `Enum`) in `lib/**/*.ex`.

## Analysis Command

For a context module, run:

Use Grep to find all `Repo.` calls in the context module, then verify each has appropriate preloads.

Then verify each query has appropriate preloads.

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/preload-patterns.md` - Efficient preloading strategies
- `${CLAUDE_SKILL_DIR}/references/query-optimization.md` - Query batching techniques
