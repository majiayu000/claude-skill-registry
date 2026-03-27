---
name: ecto:n1-check
description: "Scan Ecto code for N+1 query anti-patterns: Repo calls inside Enum.map/each/for loops, association access without preload, missing nested preloads. Use when user reports excessive queries in logs, wants an N+1 audit, or asks to find missing preloads. NOT for general Ecto guidance — use ecto-patterns."
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

```bash
# Find Enum.map with Repo calls nearby
grep -B5 -A5 "Enum.map" lib/ -r --include="*.ex" | grep -A5 -B5 "Repo\."

# Find association access patterns
grep -r "\.posts\|\.comments\|\.orders" lib/ --include="*.ex"

# Find Repo calls in loops
grep -B3 "Repo.get\|Repo.one" lib/ -r --include="*.ex" | grep -B3 "for\|Enum"
```

## Analysis Command

For a context module, run:

```bash
grep -n "Repo\." lib/my_app/[context].ex
```

Then verify each query has appropriate preloads.

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/preload-patterns.md` - Efficient preloading strategies
- `${CLAUDE_SKILL_DIR}/references/query-optimization.md` - Query batching techniques
