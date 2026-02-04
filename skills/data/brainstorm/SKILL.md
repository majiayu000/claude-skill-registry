---
name: brainstorm
description: Scan codebase, propose improvements AND features autonomously
aliases: ["what next", "whatnext", "what-next"]
allowed-tools: Bash, Read, Grep, Glob, Task, TaskCreate, TaskUpdate, TaskList, Write, Edit
model: opus
user-invocable: true
---

# Brainstorm

**Philosophy:** User doesn't know what to focus on. YOU scan, analyze, propose, and create stories - without asking.

## Usage

| Command | Behavior |
|---------|----------|
| `brainstorm` | Full: quality scan + feature ideas |
| `brainstorm auth` | Targeted: ideas for auth specifically |
| `brainstorm features` | Skip quality scan, only feature ideas |

## Phase 1: Quality Scan (Parallel)

Launch 4 scans simultaneously using Task tool with `run_in_background: true`:

```typescript
Task({ subagent_type: "Explore", model: "haiku", run_in_background: true,
  prompt: "Find TODOs/FIXMEs in [PROJECT_PATH]. Report: count, file:line, content." })

Task({ subagent_type: "Explore", model: "haiku", run_in_background: true,
  prompt: "Find console.log statements in [PROJECT_PATH] (skip test files). Report: count, files." })

Task({ subagent_type: "Explore", model: "haiku", run_in_background: true,
  prompt: "Find hardcoded colors (text-white, bg-black, #hex, rgb) in [PROJECT_PATH]. Report: count, files." })

Task({ subagent_type: "Explore", model: "haiku", run_in_background: true,
  prompt: "Find large files (>300 lines) and 'any' type usage in [PROJECT_PATH]. Report: file, lines, issues." })
```

## Phase 2: Feature Ideation (Autonomous)

After scans complete, read project context:
- `CLAUDE.md` - goals, roadmap, known issues
- `README.md` - what the app does
- `package.json` - name, description, dependencies

Then analyze and propose 3-8 features:
- **Missing features** - what similar apps have that this doesn't
- **UX improvements** - based on component structure found
- **Integration opportunities** - based on installed packages
- **Performance wins** - based on patterns observed

**Be specific:** "Add Cmd+K search modal" not "Improve UX"

## Phase 3: Present Everything

```
Brainstorm Complete
═══════════════════
Scanned 247 files in 45 seconds.

Quality Issues
┌──────────────────┬───────┬──────────────────┐
│ Category         │ Count │ Status           │
├──────────────────┼───────┼──────────────────┤
│ TODOs/FIXMEs     │ 0     │ ✅ Clean         │
│ console.log      │ 12    │ ⚠️ In 4 files    │
│ Hardcoded colors │ 6     │ ⚠️ In shadcn/ui  │
│ Large files      │ 3     │ ⚠️ >500 lines    │
└──────────────────┴───────┴──────────────────┘

Feature Ideas
┌───┬─────────────────────────────────┬────────┐
│ # │ Idea                            │ Effort │
├───┼─────────────────────────────────┼────────┤
│ 1 │ Add keyboard shortcuts (Cmd+K) │ Medium │
│ 2 │ Offline mode (PWA ready)        │ High   │
│ 3 │ Export to PDF                   │ Low    │
└───┴─────────────────────────────────┴────────┘

Create stories?
- "quality" → cleanup tasks only
- "features" → feature tasks only
- "all" → everything
```

## Targeted Mode

When user says `brainstorm X`:
- Skip quality scan entirely
- Read files related to X topic
- Propose 3-5 specific ideas for X
- Immediately create stories

## Rules

- **Never ask "what do you want?"** - analyze and propose
- **Don't over-generate** - 3-8 feature ideas max
- **Be specific** - concrete features, not vague improvements
- **Note effort** - Low/Medium/High for each
- **Skip shadcn/ui colors** - note them but don't prioritize (library defaults)
- **Auto-create for top recommendation** - then offer more

## Token Cost

- 4 parallel Haiku scans: ~20K tokens
- Context reads: ~5K tokens
- Time: 30-60 seconds
- Much cheaper than reading entire codebase
