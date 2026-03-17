---
name: commands
description: Quick reference of all custom skills, agents, and key workflows
user-invocable: true
disable-model-invocation: true
---

# /commands — BrickTrack Skill Reference

Print this cheat sheet for the user. Do NOT execute any skills — just display the reference.

## Development Skills

| Command | Purpose |
|---------|---------|
| `/tdd-workflow` | Full red-green-refactor cycle with test-first development |
| `/new-router` | Scaffold tRPC router + repository + interface + tests |
| `/new-component` | Create React component following project conventions |
| `/new-e2e-test` | Create Playwright E2E test with auth fixture + cleanup |
| `/env-spinup` | Docker + DB + schema push + test validation |

## Workflow Skills

| Command | Purpose |
|---------|---------|
| `/task-complete` | bd close, create PR, merge, worktree cleanup |
| `/document-continue` | Save progress before /clear for context handoff |
| `/phase-transition` | Move between RESEARCH → PLAN → IMPLEMENT → REVIEW → VERIFY |
| `/plan-to-epic` | Parse markdown plan into Beads tasks with auto-dependencies |
| `/ralph-execute` | Autonomous epic execution with subagents + circuit breaker |
| `/ralph-resume` | Resume a PAUSED Ralph session — retry, skip, or abort |
| `/wrap-up` | End-of-session routine: commit, memory review, self-improvement |
| `/commands` | This cheat sheet |

## Quality & Review Skills

| Command | Purpose |
|---------|---------|
| `/promote` | Verify staging → PR develop→main → merge → verify prod |
| `/audit-prod` | Smoke test production pages, console errors, network failures |
| `/eval-report` | Session metrics dashboard (pass@k, error rate, trends) |
| `/agent-shield` | Security scan of .claude/ configuration files |

## Learning & Meta Skills

| Command | Purpose |
|---------|---------|
| `/evolve` | Cluster instincts, promote high-confidence to skills, prune stale |
| `/skill-create` | Auto-generate skills from git history + instincts |
| `/instinct-export` | Export instincts as portable JSONL for cross-project sharing |
| `/instinct-import` | Import instincts from another project's export |
| `/model-routing` | Display subagent model selection strategy + cost reference |

## Search & Navigation Skills

| Command | Purpose |
|---------|---------|
| `/conversation-search` | Search past session history by keyword with date filters |
| `/conversation-fork` | Diverge into alternative approach via stash or worktree |
| `/iterative-retrieve` | 4-phase context retrieval protocol for complex questions |

## Custom Agents (auto-dispatched via Task tool)

| Agent | Trigger |
|-------|---------|
| `code-reviewer` | After implementing features, before PRs |
| `test-writer` | When tests needed for new/existing code |
| `security-reviewer` | After API endpoints, auth changes, payments |
| `database-reviewer` | After schema changes, new queries, migrations |
| `build-error-resolver` | When tsc/build/tests fail |

## Product & Strategy Skills

| Command | Purpose |
|---------|---------|
| `/value-check` | Evaluate whether a feature or product idea delivers discoverable user value |

## New Skills

| Command | Purpose |
|---------|---------|
| `/debt-scan` | Scan for anti-patterns with counts, locations, and trend tracking |
| `/session-search` | Search past session JSONL files by keyword |
| `/review-claudemd` | Audit CLAUDE.md files for dead refs, deprecated APIs, token bloat |
| `/gha` | Trigger/monitor GitHub Actions workflows via gh CLI |
| `/rules-doctor` | Scan .claude/rules/ for broken paths and coverage gaps |
| `/web-fallback` | Resilient web fetch with WebSearch fallback chain |

## Built-in Claude Code Shortcuts

| Shortcut | What it does |
|----------|-------------|
| `ESC ESC` | **Rewind conversation** — undo last exchange. Choose to keep code changes or revert both. Use after fixing side bugs to reclaim context. |
| `/chrome` | Native browser integration for visual verification. Add accessibility tree guidance to CLAUDE.md (use `read_page` + `ref`, not coordinates). |
| `/compact` | Summarize conversation to free context. Prefer `/document-continue` first. |
| `/clear` | Start fresh conversation. Use between unrelated tasks or phase transitions. |
| `Shift+Tab` | Toggle plan mode for architecture-first thinking. |
| `Tab` | Accept autocomplete suggestion. |
| `/plugin` | Open plugin manager — browse, install, manage, update plugins. |
| `/plugin install <name>` | Install a plugin (e.g., `repomix`, `plannotator`, `playground`). |
| `/memory` | View and manage auto-memory entries. Periodically nudge Claude to update these. |

## Verification Techniques

| Technique | When to use |
|-----------|-------------|
| **Playwright MCP** | E2E test verification, browser automation |
| **`/chrome` browser** | Visual verification of UI changes (use `read_page` for element refs) |
| **tmux session** | Verify interactive CLIs — `tmux new -d -s test`, send commands, capture output |
| **Draft PR review** | `gh pr create --draft` — review all changes before marking ready |
| **git bisect** | Find exact commit that broke something — Claude can automate with a test script |

## Shell Aliases (after `source .claude/setup-aliases.sh`)

| Alias | Expands To |
|-------|------------|
| `c` | `claude` |
| `cc` | `claude --continue` |
| `cr` | `claude --resume` |
| `claude-dev` | Claude with development context |
| `claude-review` | Claude with review context |
| `claude-research` | Claude with research context |
| `wt` | `cd ~/worktrees/property-tracker` |
| `bdr` | `bd ready` |
