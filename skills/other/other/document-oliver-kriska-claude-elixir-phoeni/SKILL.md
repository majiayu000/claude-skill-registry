---
name: phx:document
description: Write @moduledoc and @doc annotations into Elixir source files. Use ONLY when the user explicitly asks to generate documentation for modules, contexts, or schemas.
effort: low
argument-hint: [plan-file OR feature-name]
---

# Document

Generate documentation for newly implemented features.

## Usage

```
/phx:document .claude/plans/magic-link-auth/plan.md
/phx:document magic link authentication
/phx:document  # Auto-detect from recent plan
```

## Iron Laws

1. **Never remove existing documentation** — Existing docs may reflect design intent that isn't obvious from code alone; update rather than replace
2. **@moduledoc on every public module** — Undocumented modules accumulate quickly and create onboarding friction for new team members
3. **ADRs capture the "why", not the "what"** — Code shows what was built; ADRs explain why this approach was chosen over alternatives
4. **Match @doc to function's public API** — Document parameters, return values, and edge cases; callers shouldn't need to read the implementation
5. **DO NOT add @doc to untested code** — documentation implies a stable contract; document only after tests confirm the function behaves as described

## What Gets Documented

| Output | Description |
|--------|-------------|
| `@moduledoc` | For new modules missing documentation |
| `@doc` | For public functions without docs |
| README section | For user-facing features |
| ADR | For significant architectural decisions |

## Workflow

### Step 0: Pre-check (avoid no-op runs)

Run `git diff --name-only HEAD~5 | grep '\.ex$' | head -20` to check for new `.ex` files.

If NO new `.ex` files were added (only modifications), skip the full
audit and report: "No new modules — documentation coverage unchanged."
This prevents 35-message analysis sessions that conclude "PASS" with
zero output (confirmed: session bb0a0454 wasted ~2K tokens on no-op).

1. **Identify** new modules from recent commits or plan file
2. **Check** documentation coverage (`@moduledoc`, `@doc`)
3. **Generate** missing docs using templates
4. **Add** README section if user-facing feature
5. **Create** ADR if architectural decision was made
6. **Write** report to `.claude/plans/{slug}/reviews/{feature}-docs.md`

## When to Generate ADRs

| Trigger | Create ADR |
|---------|-----------|
| New external dependency | Yes |
| New database table | Maybe (if schema non-obvious) |
| New OTP process | Yes (explain why process needed) |
| New context | Maybe (if boundaries non-obvious) |
| New auth mechanism | Yes |
| Performance optimization | Yes |

## Integration with Workflow

```text
/phx:plan → /phx:work → /phx:review
       ↓
/phx:document  ← YOU ARE HERE (optional, suggested after review passes)
```

## References

- `${CLAUDE_SKILL_DIR}/references/doc-templates.md` — @moduledoc, @doc, README, ADR templates
- `${CLAUDE_SKILL_DIR}/references/output-format.md` — Documentation report format
- `${CLAUDE_SKILL_DIR}/references/doc-best-practices.md` — Elixir documentation best practices
- `${CLAUDE_SKILL_DIR}/references/documentation-patterns.md` — Detailed documentation patterns
