---
name: plugin-dev-workflow
description: "Guide plugin development workflow — editing skills, agents, hooks, or eval framework in this repo. Use when modifying files in plugins/elixir-phoenix/, lab/eval/, or lab/autoresearch/. Ensures changes pass eval, lint, and tests before committing."
effort: medium
---

# Plugin Development Workflow

This repo is the Elixir/Phoenix Claude Code plugin. When editing plugin
files, follow this workflow to ensure quality.

## Before You Start

Run `make help` to see all available commands:

```bash
make eval          # Quick: lint + score changed skills/agents
make eval-all      # Full: all 40 skills + 20 agents
make eval-fix      # Auto-fix + show failures
make test          # 52 pytest tests for eval framework
make ci            # Full CI pipeline
```

## Scoring Individual Files (CLI)

IMPORTANT: Always use `-m` module syntax, never run scorer.py directly.

```bash
# Score ONE skill (use -m, NOT direct file path)
python3 -m lab.eval.scorer plugins/elixir-phoenix/skills/verify/SKILL.md

# Score ONE skill with pretty output
python3 -m lab.eval.scorer plugins/elixir-phoenix/skills/verify/SKILL.md --pretty

# Score all skills
python3 -m lab.eval.scorer --all

# Score ONE agent
python3 -m lab.eval.agent_scorer plugins/elixir-phoenix/agents/verification-runner.md

# Score all agents
python3 -m lab.eval.agent_scorer --all
make ci            # Full CI pipeline
```

## When Editing Skills (plugins/elixir-phoenix/skills/*/SKILL.md)

1. **Read CLAUDE.md** conventions (size limits, frontmatter requirements)
2. Make your changes
3. Run `make eval` — it auto-detects changed skills and scores them
4. If FAIL: check the dimension that failed, fix it
5. Run `make lint` to verify markdown formatting
6. Commit

**Skill requirements** (eval checks all of these):

- Frontmatter: name, description, effort. Description must start with action verb + include "Use when..."
- Iron Laws section with 1+ numbered items
- Under 185 lines (command skills) or 150 lines (reference skills)
- No section exceeds 45 lines
- All `/phx:` references point to existing skills
- All `references/*.md` paths exist
- No dangerous code patterns outside Iron Laws sections
- Code examples present (1+ fenced code blocks)
- "Use when..." in description (for trigger accuracy)

## When Editing Agents (plugins/elixir-phoenix/agents/*.md)

1. Make your changes
2. Run `make eval-agents` to score all agents
3. Agent requirements:
   - `permissionMode: bypassPermissions` (always — background agents need it)
   - `disallowedTools: Write, Edit, NotebookEdit` for review/analysis agents
   - model matches effort: haiku=low, sonnet=medium, opus=high
   - Under 300 lines (specialist) or 535 lines (orchestrator)

## When Editing Eval Framework (lab/eval/*.py)

1. Make your changes
2. Run `make test` — 52 pytest tests must pass
3. Run `make eval-all` — verify no skills/agents regressed
4. If adding new matchers: add tests in `lab/eval/tests/test_matchers.py`

## When Editing Hooks (plugins/elixir-phoenix/hooks/scripts/*.sh)

1. Make your changes
2. Run `make lint` (markdown in hook comments)
3. Test the hook manually (hooks run on Edit/Write/Bash events)
4. Check CLAUDE.md hook documentation is still accurate

## Autoresearch (Self-Improvement Loop)

If `make eval-fix` shows failures, it suggests an autoresearch command:

```bash
# Copy-paste the suggested command from eval-fix output
claude -p 'Run autoresearch. Score all skills...' --allowedTools 'Edit,Read,Write,Bash,Glob,Grep'
```

This runs the autoresearch loop: find weakest skill → fix ONE issue → re-score → keep/revert.

## Pre-Commit Checklist

Before committing any plugin changes:

- [ ] `make lint` passes
- [ ] `make eval` passes (changed files)
- [ ] `make test` passes (if eval framework changed)
- [ ] CHANGELOG.md updated (if user-visible change)
- [ ] Version bumped in plugin.json (if releasing)

## References

- CLAUDE.md — full conventions, size limits, checklist
- `lab/eval/` — scoring framework (24 matchers, 8 dimensions)
- `lab/autoresearch/` — self-improvement loop
- `lab/findings/interesting.jsonl` — log interesting discoveries here
