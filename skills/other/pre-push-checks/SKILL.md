---
name: pre-push-checks
description: Run all required checks before pushing code. Use before committing or when validating that changes are correct.
metadata:
  author: traceway
  version: "1.0.0"
---

# Pre-Push Checks

Use this skill to run all validation checks before pushing code. Different checks apply depending on what was changed.

## Quick reference

| What changed | Command | Where |
|---|---|---|
| UI (Svelte/TS) | `npm run check` | `ui/` |
| Backend (Encore) | `npm run typecheck` | `backend/app/` |
| Rust crates | `cargo check -p trace -p storage -p daemon` | repo root |
| Rust formatting | `cargo fmt --check` | repo root |
| Rust linting | `cargo clippy -p trace -p storage -p daemon` | repo root |
| Everything | `make check` | repo root |

## Full check sequence

### 1. UI checks (SvelteKit + Svelte 5)

```bash
cd ui && npm run check
```

This runs `svelte-kit sync && svelte-check --tsconfig ./tsconfig.json`. Catches:
- Type errors in Svelte components and TypeScript files
- Invalid Svelte 5 rune usage
- Missing imports, wrong prop types
- a11y warnings (label/select pairs, button elements)

### 2. Backend checks (Encore.ts)

```bash
cd backend/app && npm run typecheck
```

Catches:
- Type errors in API handlers, services, and types
- Invalid Drizzle queries
- Missing Encore config

### 3. Rust checks

```bash
# Type checking (fast)
cargo check -p trace -p storage -p daemon

# Linting (catches common mistakes)
cargo clippy -p trace -p storage -p daemon

# Formatting
cargo fmt --check
```

**Important**: Always skip `memfs` — it requires macFUSE which may not be installed.

To check all Rust crates except memfs:

```bash
make check-all-crates
```

### 4. Run everything

```bash
make check
```

This runs both `cargo check` and `npm run check` for the UI.

## Common issues and fixes

### Svelte: `page.params.id` can be undefined
```typescript
// Wrong
const id = page.params.id;
// Right
const id = page.params.id ?? '';
```

### Svelte: a11y warning on label/select
```svelte
<!-- Wrong -->
<label>Pick one</label>
<select>...</select>

<!-- Right -->
<label for="picker">Pick one</label>
<select id="picker">...</select>
```

### Svelte: filter casting for query strings
```typescript
// Wrong — type error
qs(filter)
// Right
qs((filter ?? {}) as Record<string, string | undefined>)
```

### Rust: unwrap() in production code
```rust
// Wrong
let value = map.get("key").unwrap();
// Right
let value = map.get("key").ok_or(MyError::NotFound("key"))?;
```

## Before committing

1. Run the relevant checks for your changes
2. Verify no secrets are staged (`.env`, credentials, API keys)
3. Use short imperative commit messages (no emoji, no conventional-commit prefixes)
