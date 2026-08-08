---
name: agents-project-memory
description: Configure CLAUDE.md/AGENTS.md/CODEX.md for persistent agent context. Use when setting coding standards or architecture docs for a codebase.
---

# Project Memory for Claude Code + Codex (Jan 2026)

Configure project memory so Claude Code and Codex get stable, scoped instructions across sessions while keeping token cost low. Use a single source of truth: keep `AGENTS.md` as primary and symlink `CLAUDE.md` to it.

## Quick Reference

| Memory Type | Typical Location | Purpose |
|------------|------------------|---------|
| Managed policy | OS-dependent (see official docs) | Organization-wide standards (security, compliance) |
| Project memory | `./AGENTS.md` (primary) + `./CLAUDE.md` (symlink → AGENTS.md) | Shared project context and conventions |
| Project rules | `./.claude/rules/*.md` | Modular, topic-focused rules (testing, security, style) |
| User memory | `~/.claude/CLAUDE.md` | Personal preferences across projects |
| Project memory (local) | `./CLAUDE.local.md` (git-ignored) | Local-only, project-specific preferences |

### How Loading Works (High Level)

**Claude Code (CLAUDE.md symlink)**:
- **Recursive loading**: from the current working directory up to (but not including) filesystem root (`/`).
- **On-demand loading**: nested `CLAUDE.md` files under the cwd are loaded only when Claude reads files in those subtrees.
- **Imports**: `@path/to/file` pulls in additional context (max depth: 5; `~` supported).

**Codex (AGENTS.md primary)**:
- Reads `AGENTS.md` in the repo root or working directory.
- Keep it concise; mirror the same content as `CLAUDE.md` when supporting both tools.

## Workflow (Best Practice)

1. Start with a minimal primary memory file (AGENTS.md, 50–120 lines): what the project is, how it's shaped, and the "must not break" rules.
2. Move long or fragile guidance into `.claude/rules/` (one topic per file).
3. Use `@imports` as navigation for detailed docs instead of copying them into memory.
4. Treat memory like code: PR review, ownership, and periodic cleanup (remove dead rules).
5. For UI changes, confirm the specific values (colors, prices, text) before starting implementation to avoid rework.
6. For feature delivery, prefer one worktree per feature, run project quality gates, then open one focused PR.


## Execution Workflow (Worktree + Gate + PR)

When repositories include a workflow script (for example `scripts/git/feature-workflow.sh`), prefer this sequence for AI coding sessions:

```bash
# 1) Create isolated branch/worktree
./scripts/git/feature-workflow.sh start <feature-slug>
cd .worktrees/<feature-slug>

# 2) Implement + commit
git add -A
git commit -m "feat: <summary>"

# 3) Run project quality gate (example)
../../scripts/git/feature-workflow.sh gate

# 4) Open PR (gate may run again)
../../scripts/git/feature-workflow.sh pr --title "feat: <summary>"
```

If no helper script exists, use native git worktrees and apply the same policy:
- one feature per worktree
- one focused PR per feature
- run repo-specific gate(s) before PR creation

## Rules With Optional Path Scope

Create `.claude/rules/testing.md`, `.claude/rules/security.md`, etc. If a rule only applies to a slice of the repo, scope it:

```yaml
---
paths:
  - "src/api/**/*.ts"
---
```

## Commands (Claude Code)

- `> /memory` to view and directly edit memories.
- `> /init` to bootstrap project memory (see official docs for current behavior).

## Commands (Codex)

- Edit `AGENTS.md` directly; no special memory command is required.

## Cross-Platform Strategy (AGENTS.md + CLAUDE.md)

If you support multiple coding assistants, keep one canonical file and mirror it:

- macOS/Linux: `CLAUDE.md` should be a symlink to `AGENTS.md`.
- Windows: prefer copying (or a small sync script) over symlinks unless Developer Mode is enabled.

Avoid tool-specific claims in the memory file; keep it portable and strictly project-focused.

## Token-Budget Profile for Project Memory

When sessions repeatedly include very large memory payloads, apply this compact profile.

### Compact Profile Rules

1. Keep `AGENTS.md` short (target 50-120 lines).
2. Move long catalogs/checklists to skill docs and reference them by path.
3. Keep one canonical policy statement per topic; link instead of repeating.
4. Prefer "read-on-demand" instructions over embedding full inventories in every session.
5. Maintain a short runtime memory and a fuller reference doc when needed.

### Suggested Split

- `AGENTS.md` (runtime): project goal, hard constraints, workflow rules, critical safety constraints.
- `docs/*` or skill references: long lists, examples, optional playbooks, large inventories.

### Quality Gate

If startup memory exceeds practical context budgets, trim before adding new rules.


## Validation (Fast Checks)

- Run the bundled linter: `bash frameworks/shared-skills/skills/agents-project-memory/scripts/lint_claude_memory.sh .`
- Manually scan for unresolved `@imports` and secrets before merging memory changes.

## Resources

| Resource | Purpose |
|----------|---------|
| [references/memory-patterns.md](references/memory-patterns.md) | Patterns and anti-patterns |
| [references/memory-examples.md](references/memory-examples.md) | Full examples by stack |
| [references/large-codebase-strategy.md](references/large-codebase-strategy.md) | 100K–1M LOC strategy |
| [data/sources.json](data/sources.json) | Official links |

## Related Skills

| Skill | Purpose |
|-------|---------|
| [agents-skills](../agents-skills/SKILL.md) | Skill creation patterns |
| [agents-subagents](../agents-subagents/SKILL.md) | Agent/subagent setup |
| [docs-codebase](../docs-codebase/SKILL.md) | Repo documentation patterns |

## Fact-Checking

- Use web search/web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.
