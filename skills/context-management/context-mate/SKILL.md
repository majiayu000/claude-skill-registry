---
name: context-mate
description: |
  Entry point to the Context Mate toolkit - skills, agents, and commands that work with Claude Code's
  natural flow. Project lifecycle (/explore-idea → /plan-project → /wrap-session), session handoff
  across context windows, developer agents for specialized tasks, and quality auditing.

  Use when: starting new projects, understanding the toolkit, needing workflow guidance.
  "It's all about the context, maaate!"
---

# Context Mate

A toolkit that works with Claude Code's natural flow. Use what helps, ignore what doesn't.

---

## When This Skill Activates

When context-mate is invoked, **analyze the project first** before recommending tools.

### Step 1: Quick Project Scan

Check for these files (use Glob, don't read contents yet):

| File/Pattern | Indicates |
|--------------|-----------|
| `SESSION.md` | Session tracking active |
| `IMPLEMENTATION_PHASES.md` | Phased planning in use |
| `PROJECT_BRIEF.md` | Project explored/planned |
| `CLAUDE.md` or `.claude/` | AI context exists |
| `.claude/rules/` | Correction rules present |
| `package.json` or `requirements.txt` | Has dependencies |
| `tests/` or `*.test.*` | Has test infrastructure |

### Step 2: Git State (if git repo)

```bash
git status --short            # Uncommitted changes?
git log --oneline -3          # Recent commit messages?
```

### Step 3: Assess Stage and Recommend

**Project Stages:**

| Stage | Signs | Recommend |
|-------|-------|-----------|
| **New Project** | No CLAUDE.md, no phases | `/explore-idea` or `/plan-project` |
| **Active Development** | SESSION.md or phases exist | `/continue-session`, developer agents |
| **Maintenance Mode** | Docs exist, no SESSION.md | `/plan-feature` for new work, `project-health` for audits |
| **Mid-Session** | Uncommitted changes + SESSION.md | Continue current work, `/wrap-session` when done |

### Step 4: Brief Output

Tell the user:
1. **What's already set up** (e.g., "You have SESSION.md and phases - mid-project")
2. **What would help now** (e.g., "Run `/continue-session` to resume")
3. **What's available but not in use** (e.g., "No tests yet - `test-runner` available")

**Example:**

> **Project Analysis**
>
> ✓ `CLAUDE.md` - AI context configured
> ✓ `SESSION.md` - Session tracking active (Phase 2 in progress)
> ✓ `.claude/rules/` - 3 correction rules
> ○ No test files detected
>
> **Recommendations:**
> - Run `/continue-session` to resume Phase 2 work
> - Use `commit-helper` agent when ready to commit
> - Consider `test-runner` agent when adding tests

Keep it under 10 lines. Don't overwhelm - just highlight what's relevant.

---

**The name has a double meaning:**
1. Your friendly **context companion** (the toolkit)
2. *"It's all about the context, maaate!"* (the philosophy)

This isn't "The Correct Way To Do Things" - these tools exist because context windows are real constraints, not because we're dictating methodology.

---

## Quick Reference

### Commands (type these)

| Command | What it does |
|---------|--------------|
| `/explore-idea` | Start with a vague idea |
| `/plan-project` | Plan a new project |
| `/plan-feature` | Plan a specific feature |
| `/wrap-session` | End work session |
| `/continue-session` | Resume from last session |
| `/docs-init` | Create project docs |
| `/docs-update` | Update docs after changes |
| `/reflect` | Review what you've done |
| `/release` | Prepare for deployment |

### Agents (Claude uses these automatically)

| Agent | What it does |
|-------|--------------|
| `commit-helper` | Writes commit messages |
| `code-reviewer` | Reviews code quality |
| `debugger` | Investigates bugs |
| `test-runner` | Runs/writes tests |
| `build-verifier` | Checks dist matches source |
| `documentation-expert` | Creates/updates docs |
| `orchestrator` | Coordinates multi-step work |

### Skills (background knowledge)

| Skill | What it provides |
|-------|------------------|
| `project-planning` | Phase-based planning templates |
| `project-session-management` | SESSION.md patterns |
| `docs-workflow` | Doc maintenance commands |
| `deep-debug` | Multi-agent debugging |
| `project-health` | AI-readability audits |
| `developer-toolbox` | The 7 agents above |

---

## The Toolkit at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT LIFECYCLE                        │
├─────────────────────────────────────────────────────────────┤
│  /explore-idea → /plan-project → [work] → /wrap-session    │
│       ↓              ↓              ↓           ↓          │
│  PROJECT_BRIEF   PHASES.md     SESSION.md   git checkpoint │
│                                     ↓                      │
│                              /continue-session             │
│                                     ↓                      │
│                              [resume work]                 │
│                                     ↓                      │
│                    /reflect → /release                     │
└─────────────────────────────────────────────────────────────┘
```

---

## When To Use What

| You want to... | Use this |
|----------------|----------|
| Explore a vague idea | `/explore-idea` |
| Plan a new project | `/plan-project` |
| Plan a specific feature | `/plan-feature` |
| End a work session | `/wrap-session` |
| Resume after a break | `/continue-session` |
| Create/update docs | `/docs-init`, `/docs-update` |
| Debug something stubborn | `deep-debug` skill |
| Review code quality | `code-reviewer` agent |
| Run tests with TDD | `test-runner` agent |
| Prepare a git commit | `commit-helper` agent |
| Verify build output | `build-verifier` agent |
| Check docs are AI-readable | `context-auditor` agent |
| Validate workflows work | `workflow-validator` agent |
| Check session handoff quality | `handoff-checker` agent |

---

## Component Skills

### Project Lifecycle (project-workflow)

Nine integrated commands for the complete project lifecycle:

| Command | Purpose |
|---------|---------|
| `/explore-idea` | Brainstorm and validate project concepts |
| `/plan-project` | Generate phased implementation plan |
| `/plan-feature` | Plan a specific feature addition |
| `/docs-init` | Create initial project documentation |
| `/docs-update` | Update docs after changes |
| `/wrap-session` | End session with git checkpoint |
| `/continue-session` | Resume from SESSION.md |
| `/reflect` | Review progress and plan next steps |
| `/release` | Prepare for deployment/release |

**Invoke**: `Skill(skill: "project-workflow")`

### Session Management (project-session-management)

Track progress across context windows using SESSION.md with git checkpoints.

- Converts IMPLEMENTATION_PHASES.md into actionable tracking
- Creates semantic git commits as recovery points
- Documents concrete next actions for resumption
- Prevents context loss between sessions

**Invoke**: `Skill(skill: "project-session-management")`

### Developer Agents (developer-toolbox)

Seven specialized agents for common development tasks:

| Agent | Use For |
|-------|---------|
| `commit-helper` | Generate meaningful commit messages |
| `code-reviewer` | Security, quality, architecture review |
| `debugger` | Systematic bug investigation |
| `test-runner` | TDD workflows, test creation |
| `build-verifier` | Verify dist/ matches source |
| `documentation-expert` | Create/update project docs |
| `orchestrator` | Coordinate multi-step projects |

**Invoke**: `Skill(skill: "developer-toolbox")`

### Deep Debugging (deep-debug)

Multi-agent investigation for stubborn bugs that resist normal debugging.

- Spawns parallel investigation agents
- Cross-references findings
- Handles browser/runtime issues
- Best when going in circles on a bug

**Invoke**: `Skill(skill: "deep-debug")`

### Quality Auditing (project-health)

Three agents for AI-readability and workflow quality:

| Agent | Purpose |
|-------|---------|
| `context-auditor` | Check if docs are AI-readable (score 0-100) |
| `workflow-validator` | Verify documented processes work (score 0-100) |
| `handoff-checker` | Validate session continuity quality (score 0-100) |

**Invoke**: `Skill(skill: "project-health")`

### Documentation Lifecycle (docs-workflow)

Four commands for documentation management:

| Command | Purpose |
|---------|---------|
| `/docs` | Quick doc lookup |
| `/docs-init` | Create initial docs |
| `/docs-update` | Update after changes |
| `/docs-claude` | Generate AI-optimized CLAUDE.md |

**Invoke**: `Skill(skill: "docs-workflow")`

---

## Core Concepts

### Sessions ≠ Phases

**Sessions** are context windows (2-4 hours of work before context fills up).

**Phases** are work units (logical groupings like "Phase 1: Database Setup").

A phase might span multiple sessions. A session might touch multiple phases. They're independent concepts.

### Checkpointed Progress

Git commits serve as **semantic checkpoints**, not just version control:

```bash
# Bad: commits as save points
git commit -m "WIP"
git commit -m "more changes"

# Good: commits as progress markers
git commit -m "Complete Phase 1: Database schema and migrations"
git commit -m "Phase 2 partial: Auth middleware working, UI pending"
```

When resuming via `/continue-session`, these commits tell the story of where you are.

### Progressive Disclosure

Skills load incrementally to preserve context:

1. **Metadata** (~50 tokens) - Always in context, triggers skill loading
2. **SKILL.md body** (<5k words) - Loaded when skill activates
3. **Bundled resources** - Loaded as needed (templates, references, scripts)

This means a 50-skill toolkit only costs ~2,500 tokens until you actually use something.

### Skills Teach, Rules Correct

Two complementary knowledge systems:

| | Skills | Rules |
|-|--------|-------|
| **Location** | `~/.claude/skills/` | `.claude/rules/` (project) |
| **Content** | Rich bundles | Single markdown files |
| **Purpose** | Teach how to use X | Correct outdated patterns |
| **Example** | How to set up Tailwind v4 | Fix v3 syntax Claude might suggest |

Rules are project-portable - they travel with the repo so any Claude instance gets the corrections.

### Sub-agents for Isolation

Heavy tasks (code review, debugging, testing) run in sub-agents to:

- Keep verbose output out of main context
- Allow parallel execution
- Provide specialized tool access
- Return concise summaries

---

## Getting Started

### New Project

```
/explore-idea    # Optional: clarify what you're building
/plan-project    # Generate phased plan
                 # Work on Phase 1...
/wrap-session    # End with checkpoint
```

### Resuming Work

```
/continue-session    # Reads SESSION.md, suggests next steps
                     # Continue working...
/wrap-session        # Checkpoint again
```

### Adding a Feature

```
/plan-feature    # Plan the specific feature
                 # Implement...
/wrap-session    # Checkpoint
```

### Debugging Session

```
# If normal debugging isn't working:
Skill(skill: "deep-debug")
# Spawns investigation agents
```

---

## The Philosophy

**Context windows are real.** They fill up. Work gets lost. Sessions end.

These tools don't fight that - they work with it:

- **SESSION.md** captures state for next session
- **Git checkpoints** create recovery points
- **Sub-agents** keep heavy work isolated
- **Progressive disclosure** preserves context budget

Use what helps. Ignore what doesn't.

*It's all about the context, maaate.*
