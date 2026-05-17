# Skill Checklist — Phase 1 lessons baked in

Pre-flight for any new skill or agent added to `claude-elixir-phoenix`.
Captures the concrete gotchas that cost Phase 1 implementation ~15 minutes
each. Apply this list **before** running `make eval`.

## Frontmatter

- `name:` — kebab-case, namespaced when surfaced as a command
  (`phx:deps-audit`). Plain `deps-audit` works for internal skills.
- `description:` — **≤200 characters** and **≥3 keywords** from the
  scorer's Elixir/Phoenix domain list (see `lab/eval/matchers.py:198`).
  Vague descriptions like "Audit deps" score zero on triggering.
  Effective pattern: `"<action> <domain> for <risk surface> —
  <specifics>. Use <when>."` Example:
  `"Audit Hex dep updates for supply-chain security risk — bidi chars,
  compile-time exec, maintainer changes. Use after mix deps.update."`
- `argument-hint:` — quote the value if it contains `[...]`. Unquoted
  square brackets get parsed as YAML flow sequences.
  Wrong: `argument-hint: [--base <ref>] [--json]`
  Right: `argument-hint: "[--base <ref>] [--json]"`

## Headings

- The Iron Laws heading must be literally `## Iron Laws` — no em-dash,
  no parenthetical. The eval scorer's `section_exists` check does a
  literal string match. Variants like `## Iron Laws — Never Violate`
  fail completeness.

## Body

- Keep SKILL.md under ~150 lines. Command skills get ~185.
- Reference paths use `${CLAUDE_SKILL_DIR}/references/<file>.md`. Bare
  `references/<file>.md` paths break in subagents because the cwd is
  the project, not the plugin install.
- Iron Laws section: numbered list with concrete prohibitions and a
  one-sentence rationale per law. Aim for 4-6 laws.

## Markdown lint

- Lists need a blank line above and below (MD032).
- No hard tabs in code fences. Use 2-space indent. Even one tab in a
  Makefile snippet trips MD010 and fails CI.
- Code fences must declare a language (` ```bash ` not just ` ``` `).

## Eval scorer

- `make eval` runs `git diff` to find changed files. **Untracked files
  are invisible.** `git add` the new skill/agent before running, or
  `make eval-all` for the full pass.
- Trigger-accuracy is cached per skill description hash. After tuning
  the description, the cache invalidates on its own.
- Use `make eval-fix` to see exact failures and get auto-fix
  suggestions.
- **Agents use a different scorer than skills.** `make eval` routes
  correctly. Manual scoring during development must pick the right one:
  - Skills → `python3 -m lab.eval.scorer <path>`
  - Agents → `python3 -m lab.eval.agent_scorer <path>`
  - Running `scorer.py` against an agent over-restricts (skill-shaped
    thresholds applied to agent content) and fails on dimensions the
    agent scorer skips. If a manual run reports completeness-0 on an
    obviously-complete agent, you used the wrong scorer.

## Agent-specific

- `permissionMode: bypassPermissions` for **every** agent. `default`
  triggers "Bash command permission check failed" when the agent runs
  in background — the safety system pattern-scans skill content for
  shell-like substrings.
- Read-only agents (no Write): set `disallowedTools: Edit,
  NotebookEdit` (NOT Write — agents need Write to save their own
  findings file). Set `omitClaudeMd: true`.
- `effort:` must match model: `low` for haiku, `medium` for sonnet,
  `high` for opus. Mismatch fails the consistency check.

## Description keyword reference

The fixed Elixir/Phoenix domain list is in `lab/eval/matchers.py`.
Effective single-word triggers include: `audit`, `security`, `review`,
`hex`, `mix`, `liveview`, `ecto`, `oban`, `phoenix`, `elixir`,
`migration`, `changeset`, `genserver`, `supervisor`, `compile`, `test`,
`debug`, `performance`. Aim for ≥3 of these in the description.

## Quick verification flow

```bash
git add plugins/elixir-phoenix/skills/<new-skill>/
make eval-fix          # see failures, get fix suggestions
# Apply fixes, then:
make eval              # confirm pass
```

If only one skill or agent changed, `make eval` runs in <30 s. The
full `make eval-all` over 40 skills + 20 agents takes ~5 min.
