---
name: auto-context
model: fast
description: Automatically read relevant context before major actions. Loads TODO.md, roadmap.md, handoffs, task plans, and other project context files so the AI operates with full situational awareness. Use when starting a task, implementing a feature, refactoring, debugging, planning, or resuming a session.
---

# Auto-Context — Situational Awareness Protocol (Meta-Skill)

Before you act, understand where you are. This skill ensures the AI loads critical project context automatically before any major action, preventing wasted effort, duplicate work, and misaligned implementations.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install auto-context
```


---

## When to Activate

This skill triggers automatically based on the current action. Do not wait for the user to ask — proactively load context when any of these conditions are met.

| Trigger | Why | Minimum Context |
|---------|-----|-----------------|
| Starting a new task | Understand priorities, avoid conflicts | Critical + High |
| Implementing a feature | Know the plan, constraints, recent changes | Critical + High |
| Refactoring code | Understand what changed recently, what's planned | Critical + High + Medium |
| Debugging an issue | Check recent changes, known issues, discoveries | Critical + High + Medium |
| Planning or scoping work | Full picture of roadmap, backlog, progress | All levels |
| Session start or resume | Rebuild mental model from last session state | Critical + High |
| Before a handoff | Ensure nothing is missed in transition | All levels |

---

## Context Files to Read

Read these files in priority order. Stop early if the task is narrow and lower-priority files are clearly irrelevant.

| Priority | File | Purpose | Read When |
|----------|------|---------|-----------|
| Critical | `TODO.md` | Current tasks, backlog, and priorities | Always |
| Critical | `roadmap.md` | Phase status, milestones, project direction | Always |
| High | `task_plan.md` | Active task breakdown and implementation plan | File exists |
| High | `.cursor/handoffs/*.md` | Recent handoff notes (read last 3 by date) | File exists |
| Medium | `findings.md` | Research results, discoveries, decisions made | Relevant to task |
| Medium | `CHANGELOG.md` | Recent changes and their rationale | Relevant to task |
| Low | `.cursor/sessions/*.md` | Session summaries (read last 2 by date) | Planning or debugging |

### Alternate Locations

Some projects use different paths. Check these fallbacks if primary paths are empty:

| Primary | Fallback |
|---------|----------|
| `TODO.md` | `docs/TODO.md`, `ai/TODO.md` |
| `roadmap.md` | `docs/roadmap.md`, `ROADMAP.md` |
| `task_plan.md` | `docs/task_plan.md`, `.cursor/task_plan.md` |
| `findings.md` | `docs/findings.md`, `.cursor/findings.md` |

---

## Context Loading Strategy

### Step 1: Load Critical Files (Always)

```
Read TODO.md → Extract: current task, next priorities, blockers
Read roadmap.md → Extract: current phase, active milestone, upcoming deadlines
```

If either critical file is missing, warn the user:
> "No TODO.md found. Consider creating one to track tasks."

### Step 2: Load High-Priority Files (If They Exist)

```
Read task_plan.md → Extract: implementation steps, acceptance criteria
Glob .cursor/handoffs/*.md → Read last 3 by modification date
```

### Step 3: Load Medium/Low Files (If Relevant)

Only read these when the current task benefits from historical context:

- **Debugging?** — Read `findings.md` and `CHANGELOG.md`
- **Planning?** — Read everything including session files
- **Quick fix?** — Skip medium and low entirely

### Step 4: Synthesize and Present

After loading, produce a context summary (see format below) before proceeding with the task.

---

## Staleness Detection

Check modification dates on all loaded files. Flag files that may contain outdated information.

| Age | Status | Action |
|-----|--------|--------|
| < 24 hours | Fresh | Use as-is |
| 1-7 days | Current | Use as-is, note the age |
| 7-30 days | Stale | Warn: "{file} last updated {N} days ago — verify before relying on it" |
| > 30 days | Outdated | Warn: "{file} is {N} days old and may no longer reflect project state" |

To check file ages on macOS:

```bash
stat -f "%m %N" TODO.md roadmap.md task_plan.md findings.md CHANGELOG.md 2>/dev/null
```

On Linux:

```bash
stat -c "%Y %n" TODO.md roadmap.md task_plan.md findings.md CHANGELOG.md 2>/dev/null
```

---

## Context Summary Format

After loading context, present a concise summary using this template. Keep it tight — the goal is awareness, not repetition.

```markdown
## Context Loaded

**Current Phase:** {phase from roadmap}
**Active Milestone:** {milestone and progress}

**Current Task:** {from TODO.md or task_plan.md}
- Status: {in-progress / blocked / not started}
- Blockers: {any blockers, or "none"}

**Recent Changes:**
- {last 2-3 items from CHANGELOG or handoffs}

**Relevant Findings:**
- {key discoveries that affect the current task, or "none"}

**Stale Warnings:**
- {any staleness warnings, or "all context is fresh"}
```

If no context files exist at all, output:

```markdown
## Context Loaded

No project context files found. Operating without historical context.
Consider creating TODO.md and roadmap.md to enable context-aware assistance.
```

---

## Integration Points

This skill connects to other workflow commands and should run as a precursor.

| Command | How Auto-Context Integrates |
|---------|-----------------------------|
| `/start-task` | Loads full context before beginning work; populates task plan |
| `/intent` | Reads roadmap and TODO to validate intent against project direction |
| `/workflow` | Provides the "understand" phase of any workflow automatically |
| `/progress` | Uses TODO.md and task_plan.md to assess completion status |
| `/handoff-and-resume` | Reads last handoff to rebuild state on resume |
| `/session-summary` | Cross-references loaded context with session actions for accuracy |

### Execution Order

```
User triggers action
  → Auto-Context activates (this skill)
    → Context summary presented
      → Primary skill/command executes with full awareness
```

---

## Quick Reference

```
Context Loading Checklist:
  1. Read TODO.md (critical)
  2. Read roadmap.md (critical)
  3. Read task_plan.md (if exists)
  4. Read last 3 handoffs (if exist)
  5. Check file staleness
  6. Read findings/changelog (if relevant)
  7. Present context summary
  8. Proceed with task
```

---

## NEVER Do

1. **NEVER skip critical files to save time** — leads to duplicate work and conflicting implementations
2. **NEVER load every file regardless of task** — wastes tokens and dilutes focus with irrelevant info
3. **NEVER ignore staleness warnings** — stale context causes decisions based on outdated assumptions
4. **NEVER read files without summarizing** — raw file dumps overwhelm; always synthesize first
5. **NEVER assume context from memory alone** — sessions are stateless; always re-read files
6. **NEVER silently proceed when no context exists** — user should know they're operating blind
7. **NEVER read handoffs/sessions beyond the limit** — last 3 handoffs and last 2 sessions are sufficient
