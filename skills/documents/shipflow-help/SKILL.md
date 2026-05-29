---
name: shipflow-help
description: Cheatsheet for the full task tracking and audit system — skills, modes, prompts, workflows
disable-model-invocation: true
argument-hint: [optional: tasks, audit, workflows, prompts]
---

# Skill System Cheatsheet

Quick reference for all 25 skills, modes, and workflows.

---

## Skills at a Glance

### Task & Workflow

| Skill | Purpose | Arguments |
|-------|---------|-----------|
| `/shipflow-tasks` | Track work, check off items, suggest next | `[focus area]` |
| `/shipflow-priorities` | Re-rank by impact/effort matrix | `impact`, `effort`, `blockers`, `quick-wins` |
| `/shipflow-backlog` | Capture ideas, defer non-urgent | `add "idea"`, `defer`, `review`, `clean` |
| `/shipflow-review` | Session summary, update docs | `daily`, `weekly`, `sprint`, `release` |

### Audit (8 domains)

| Skill | Purpose | Arguments |
|-------|---------|-----------|
| `/shipflow-audit` | Master orchestrator (all 8 domains) | `@file`, `global`, or nothing |
| `/shipflow-audit-code` | Architecture, security, reliability | `@file`, `global`, or nothing |
| `/shipflow-audit-design` | UI/UX, a11y, responsiveness | `@file`, `global`, or nothing |
| `/shipflow-audit-copy` | Copywriting, tone, CTAs | `@file`, `global`, or nothing |
| `/shipflow-audit-seo` | Meta tags, structured data, links | `@file`, `global`, or nothing |
| `/shipflow-audit-gtm` | Go-to-market, conversion, trust | `@file`, `global`, or nothing |
| `/shipflow-audit-translate` | i18n completeness, consistency | `@file`, `global`, or nothing |
| `/shipflow-deps` | Dependencies: vulns, outdated, unused, licenses | `global`, or nothing |
| `/shipflow-perf` | Performance: bundle, CWV, rendering, data | `@file`, `global`, or nothing |

### DevOps & Shipping

| Skill | Purpose | Arguments |
|-------|---------|-----------|
| `/shipflow-ship` | Stage, commit, push | `"commit message"` |
| `/shipflow-check` | Typecheck + lint + build + test | `[check types]`, `fix`, `nofix` |
| `/shipflow-deploy` | Full deploy: check → ship → restart → verify | `skip-check` |
| `/shipflow-status` | Cross-project git dashboard | (none) |

### Scaffolding & Init

| Skill | Purpose | Arguments |
|-------|---------|-----------|
| `/shipflow-init` | Bootstrap new project for ShipFlow | `[project-path]` |
| `/shipflow-scaffold` | Generate files matching project patterns | `<type> <name>` |

### Research & Documentation

| Skill | Purpose | Arguments |
|-------|---------|-----------|
| `/shipflow-research` | Deep web research → saved report | `<topic>` |
| `/shipflow-docs` | Generate/update docs from code | `@file`, `readme`, `api`, `components` |
| `/shipflow-enrich` | Web research + content upgrade | `@file` or `folder/` |

### Upgrades

| Skill | Purpose | Arguments |
|-------|---------|-----------|
| `/shipflow-migrate` | Framework upgrade assistant | `[package@version]` |
| `/shipflow-changelog` | Auto-generate CHANGELOG from git | `[tag]`, `[date]`, `all` |

---

## Audit Modes (3 modes)

```bash
# PAGE MODE — audit a single file
/shipflow-audit-seo @src/pages/index.astro

# PROJECT MODE — audit current project (default)
/shipflow-audit-code

# GLOBAL MODE — audit ALL applicable projects
/shipflow-audit global
/shipflow-audit-seo global
```

**Domain applicability**: Not all audits apply to all projects. Global mode reads `~/shipflow_data/PROJECTS.md` and skips inapplicable domains (e.g., no SEO for `my-robots`, no Deps for `BuildFlowz`).

**8 domains**: Code, Design, Copy, SEO, GTM, Translate, Deps, Perf.

**Scoring**: Every audit scores categories A/B/C/D, fixes issues, logs to `AUDIT_LOG.md`, creates tasks in `TASKS.md`.

---

## Interactive Prompts

Skills auto-detect context and prompt when needed:

### Workspace root detection
Run any skill from `~/` (no project markers) and it asks **"Which project(s)?"** instead of failing.

### Scope selection
| Skill | Prompt | Options |
|-------|--------|---------|
| `/shipflow-review` | "What time scope?" | Daily, Weekly, Sprint, Release |
| `/shipflow-check` | "Which checks?" | Typecheck, Lint, Build, Test, Dependencies |
| `/shipflow-audit` | "Which domains?" | Code, Design, Copy, SEO, GTM, Translate, Deps, Perf |
| `/shipflow-audit global` | "Which projects?" + "Which domains?" | Checkboxes for both |
| `/shipflow-init` | "Confirm domain applicability?" | Checkboxes for 8 domains |

### When prompts are skipped
Provide explicit arguments and prompts don't appear:
```bash
/shipflow-review weekly          # No scope prompt
/shipflow-audit-seo global      # No domain prompt (SEO only)
/shipflow-check typecheck        # No check selection prompt
```

---

## Multi-Project Tracking

### Architecture
```
~/TASKS.md              # Master tracker (symlink to ShipFlow)
~/AUDIT_LOG.md          # Audit history (symlink to ShipFlow)
~/ShipFlow/
├── TASKS.md            # Source of truth (12 projects)
├── AUDIT_LOG.md        # Cross-project audit scores
└── PROJECTS.md         # Project registry + domain matrix (8 domains)
```

### Rules
1. **Master file first**: `/shipflow-tasks`, `/shipflow-priorities`, `/shipflow-backlog` always update `~/TASKS.md`
2. **Local files too**: If a project has its own `TASKS.md`, update both
3. **Dashboard sync**: Update the Dashboard table when project phases change
4. **Prefix items**: Backlog entries include project name (e.g., `- tubeflow: Add dark mode`)

---

## Workflow Cycle

```
/shipflow-backlog  →  /shipflow-priorities  →  /shipflow-tasks  →  (work)  →  /shipflow-review
 capture               rank                    track               code        reflect
```

### Daily (5 min)
```bash
/shipflow-tasks                    # Morning: see what's next
# ... work ...
/shipflow-tasks                    # Evening: check off done items
```

### Weekly (15 min)
```bash
/shipflow-review weekly            # What happened this week
/shipflow-priorities               # Re-rank for next week
/shipflow-backlog review           # Promote ready items
/shipflow-backlog defer            # Clear non-urgent from active
```

### Sprint (30 min)
```bash
/shipflow-review sprint            # Comprehensive review
/shipflow-backlog clean            # Remove stale items
/shipflow-priorities impact        # Plan high-value work
```

### New project
```bash
/shipflow-init /path/to/project    # Bootstrap tracking
/shipflow-audit                    # Initial baseline audit
/shipflow-tasks                    # Start tracking work
```

### Ship something
```bash
/shipflow-check                    # Verify everything passes
/shipflow-ship "Feature description"  # Commit + push
/shipflow-tasks                    # Mark completed, get next
```

### Full deploy
```bash
/shipflow-deploy                   # Check → ship → restart → verify
# or
/shipflow-deploy skip-check        # Skip checks (use with caution)
```

### Framework upgrade
```bash
/shipflow-migrate astro@5          # Research + plan + apply
/shipflow-check                    # Verify build
/shipflow-changelog                # Document the upgrade
/shipflow-ship                     # Commit and push
```

### Full audit
```bash
/shipflow-audit                    # All 8 domains, current project
/shipflow-audit global             # All 8 domains, all projects
/shipflow-audit-code               # Code only, current project
/shipflow-deps global              # Dependencies across all projects
/shipflow-perf @src/pages/index.astro  # Performance for one file
```

### Cross-project overview
```bash
/shipflow-status                   # Git status dashboard for all projects
```

---

## Priority Levels

| Level | Label | When to use |
|-------|-------|-------------|
| P0 | Critical | Blockers, security, high-ROI + low-effort |
| P1 | High | Important features, medium effort |
| P2 | Medium | Standard work, nice improvements |
| P3 | Low | Nice-to-have, can wait |

---

## Audit Scoring

| Grade | Meaning |
|-------|---------|
| A | Excellent — no action needed |
| B | Good — minor improvements |
| C | Needs work — issues found and fixed |
| D | Poor — significant problems |

---

## File Reference

| File | Location | Purpose |
|------|----------|---------|
| `TASKS.md` | `~/` (master) + project dirs | Task tracking |
| `BACKLOG.md` | Project dirs | Deferred ideas |
| `AUDIT_LOG.md` | `~/` (master) + project dirs | Audit score history |
| `CHANGELOG.md` | Project dirs | Release notes |
| `REVIEW-*.md` | Project dirs | Review reports |
| `PROJECTS.md` | `~/ShipFlow/` | Project registry + domain matrix |

---

## Quick Answers

**Too many tasks?** → `/shipflow-priorities effort` then `/shipflow-backlog defer`

**Don't know what's next?** → `/shipflow-priorities blockers`

**New idea mid-work?** → `/shipflow-backlog add "description"`

**End of day?** → `/shipflow-tasks` then `/shipflow-review daily`

**Before deploy?** → `/shipflow-deploy` (runs check + ship + verify automatically)

**Audit everything?** → `/shipflow-audit global` (all 8 domains)

**Which projects need SEO?** → `/shipflow-audit-seo global` (auto-filters)

**New project?** → `/shipflow-init` (bootstrap tracking)

**Outdated dependencies?** → `/shipflow-deps` (full audit) or `/shipflow-check` (quick scan)

**Need to upgrade a framework?** → `/shipflow-migrate package@version`

**Generate docs?** → `/shipflow-docs readme` or `/shipflow-docs api`

**Research a topic?** → `/shipflow-research "topic"`

---

*Run `/shipflow-help` anytime for this reference.*
