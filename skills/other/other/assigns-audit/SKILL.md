---
name: lv:assigns
description: "Diagnostic audit of LiveView socket assigns — inventories every assign with memory footprint estimates, detects missing temporary_assigns, finds unused assigns, and flags unbounded lists needing streams. Use when investigating LiveView memory bloat, auditing assign efficiency, or explicitly requested via /lv:assigns. NOT for broad LiveView patterns or building features."
effort: medium
argument-hint: path/to/live_view.ex
allowed-tools: Read, Grep, Glob, Bash
---

# LiveView Assigns Audit

Analyze LiveView socket assigns for memory efficiency, clarity, and best practices.

## Iron Laws - Never Violate These

1. **Use streams for lists > 100 items** - Never store large lists directly in assigns
2. **Use temporary_assigns for transient data** - Flash messages, temp errors, notifications
3. **Preload only needed fields** - Don't store full Ecto schemas when only needing subset
4. **Initialize all assigns in mount** - Never access assigns that might not exist
5. **NEVER modify assigns or code during audit** — this is a read-only diagnostic; report findings only

## Quick Audit Commands

### Extract All Assigns

```bash
grep -E "assign\(|assign_new\(" path/to/live_view.ex
```

### Find Large Data Patterns

```bash
# Lists stored in assigns
grep -E "assign.*\[\]|assign.*Repo\.all" path/to/live_view.ex

# Full schema storage
grep -E "assign.*Repo\.get|assign.*%.*\{\}" path/to/live_view.ex
```

## Audit Checklist

### 1. Memory Issues

| Pattern | Problem | Solution |
|---------|---------|----------|
| `assign(:items, Repo.all(...))` | Unbounded list | Use `stream/3` |
| `assign(:user, Repo.get!(...))` | Full schema | Select only needed fields |
| `assign(:file_data, binary)` | Large binary | Store reference, not data |
| Nested preloads | Excessive data | Preload only what's rendered |

### 2. Missing temporary_assigns

Should use `temporary_assigns`:

- Flash messages
- Form errors after submission
- One-time notifications
- Upload progress

```elixir
def mount(_params, _session, socket) do
  {:ok, socket, temporary_assigns: [flash_message: nil]}
end
```

### 3. Unused Assigns

Search for assigns defined but never used in templates:

```bash
# Find assigns
grep -oE "assign\(:(\w+)" live_view.ex | sort -u

# Compare with template usage
grep -oE "@\w+" template.html.heex | sort -u
```

### 4. Missing Initialization

```elixir
# BAD: @items might not exist
def render(assigns) do
  ~H"<%= for item <- @items do %>"
end

# GOOD: Initialize in mount
def mount(_params, _session, socket) do
  {:ok, assign(socket, items: [])}
end
```

## Memory Estimation

For each assign, estimate memory footprint:

| Data Type | Approx Size | Concern Level |
|-----------|-------------|---------------|
| Integer | 8 bytes | Low |
| String (100 chars) | ~200 bytes | Low |
| List of 100 maps | ~10-50 KB | Medium |
| List of 1000 items | ~100-500 KB | High |
| Binary (image) | Varies | Critical |
| Full Ecto schema | ~1-5 KB each | Medium |

## Usage

Run `/lv:assigns path/to/live_view.ex` to generate an assigns inventory with memory estimates and optimization recommendations.
