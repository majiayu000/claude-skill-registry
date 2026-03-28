---
name: phx:quick
description: Implement small Phoenix changes without planning. Use when the user gives a direct instruction to add, update, fix, create, or change something — like adding a field validation, updating router routes, fixing a component for a new prop, creating a migration, or changing a controller response format. Single-file edits under 50 lines. Skip for bug investigation, code review, or large refactors.
effort: low
---

# Quick Mode

Skip the planning ceremony. Get working code fast.

## Usage

```bash
/phx:quick Add pagination to posts
/phx:quick Fix the login redirect bug
/phx:quick Add CSV export to reports
```

## Arguments

`$ARGUMENTS` = What to implement

## How It Differs

| Normal Mode | Quick Mode |
|-------------|------------|
| Spawn research agents | No agents |
| Create plan document | Mental model only |
| Parallel review | Optional single review |
| Multiple iterations | Single pass |

## Workflow

1. **Understand** - Read relevant files (max 3)
2. **Implement** - Write code directly
3. **Verify** - Quick compile check
4. **Done** - No ceremony

## Iron Laws

1. **NEVER skip verification** — run `mix compile --warnings-as-errors` after every change, even in quick mode
2. **DO NOT touch files outside the stated scope** — quick mode means minimal blast radius; if a fix requires changes across multiple domains, escalate to `/phx:plan`
3. **NEVER bypass security checks for speed** — auth, input validation, and XSS rules apply regardless of change size

## Rules in Quick Mode

### Still Enforced (Iron Laws)

- ✓ No process without runtime reason
- ✓ No DB in mount
- ✓ Security basics (no SQL injection, etc.)
- ✓ Run `mix format`

### Skipped

- ✗ Parallel agent research
- ✗ Written plan document
- ✗ Multiple review passes
- ✗ Documentation updates

## When to Use

**Good for:**

- Bug fixes with clear solution
- Small features (<100 lines)
- Refactoring with tests
- Adding fields/columns
- UI tweaks

**Not for:**

- New authentication flows
- Payment integration
- Data migrations
- Architectural changes
- Anything touching security

## Quick Patterns

### Add Field

```bash
/quick Add phone field to users
```

→ Migration + schema + changeset + form field

### Fix Bug

```bash
/quick Fix: posts not showing for admin users
```

→ Find issue + fix + verify

### Add Endpoint

```bash
/quick Add GET /api/health endpoint
```

→ Route + controller + response

## Escape Hatch

If quick mode hits complexity:

```
This needs more planning. Switching to normal mode.
Run /phx:plan [task] for full analysis.
```

## Verification

After quick implementation:

```bash
# Compile check
mix compile --warnings-as-errors

# If touched Ecto
mix ecto.migrate

# Quick test
mix test test/path_test.exs
```

## Example Session

```
User: /phx:quick Add archived_at timestamp to posts

Claude:
1. Reading lib/my_app/blog/post.ex...
2. Creating migration...

# priv/repo/migrations/xxx_add_archived_at_to_posts.exs
def change do
  alter table(:posts) do
    add :archived_at, :utc_datetime
  end
end

3. Updating schema...

# lib/my_app/blog/post.ex
field :archived_at, :utc_datetime

4. Adding to changeset...

def changeset(post, attrs) do
  post
  |> cast(attrs, [:title, :body, :archived_at])
  ...
end

5. Verifying...
$ mix compile --warnings-as-errors ✓
$ mix ecto.migrate ✓

Done. Run `mix test` to verify.
```
