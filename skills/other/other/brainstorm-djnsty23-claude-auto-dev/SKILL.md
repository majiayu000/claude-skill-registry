---
name: brainstorm
description: Scans codebase, proposes improvements and features autonomously. Use when unsure what to work on next.
triggers:
  - brainstorm
  - generate
allowed-tools: Bash, Read, Grep, Glob, Task, TaskCreate, TaskUpdate, TaskList, Write, Edit, WebSearch
model: opus
user-invocable: true
argument-hint: "[focus area]"
---

# Brainstorm

Scan, analyze, and propose — without asking what to focus on.

## Existing Tasks
!`node -e "try{const p=require('./prd.json');const sp=p.sprints?p.sprints[p.sprints.length-1]:p;Object.entries(sp.stories||p.stories||{}).forEach(([k,v])=>console.log(k,v.passes===true?'done':v.passes==='deferred'?'deferred':'pending',v.title))}catch(e){}"`

## Usage

| Command | Behavior |
|---------|----------|
| `brainstorm` | Full: architecture scan + feature ideas → present findings |
| `brainstorm apply` | Create prd.json stories from last scan results |
| `brainstorm auth` | Targeted: ideas for auth specifically |
| `brainstorm features` | Skip quality scan, only feature ideas |

## Phase 1: Architecture Scan (Parallel)

Launch 4 scans simultaneously using Task tool with `run_in_background: true`.

These scans look for real issues, not linter warnings:

```typescript
// Scan 1: Dead code — unused exports, unreferenced components, orphan routes
Task({ subagent_type: "Explore", run_in_background: true,
  prompt: `Find dead code in [PROJECT_PATH]/src:
  1. Components in src/components/ or src/app/ not imported anywhere else
  2. Exported functions/constants not imported by any other file
  3. Route segments (page.tsx) that import deleted/missing components
  Cross-reference: for each export, grep for its name across src/. Report only confirmed unused.` })

// Scan 2: Console statements + error handling gaps
Task({ subagent_type: "Explore", run_in_background: true,
  prompt: `In [PROJECT_PATH]/src (skip test/spec files):
  1. Count console.log/warn/error statements — report top 5 files by count
  2. Find empty catch blocks (catch that do nothing or just console.log)
  3. Find API calls (fetch, axios, supabase.from) without error handling
  Report: count per category, top offenders with file:line.` })

// Scan 3: Bundle + complexity — what actually costs users
Task({ subagent_type: "Explore", run_in_background: true,
  prompt: `In [PROJECT_PATH]/src:
  1. Files over 300 lines — report file path and line count
  2. For each large file: is it a single component that could be split? Or cohesive logic that should stay together? Check if it has multiple exported components or clearly separable sections.
  3. Check for client-side data fetching in page.tsx/layout.tsx that could be server-side (useEffect + fetch patterns in 'use client' pages)
  Report only genuinely splittable files, not cohesive ones.` })

// Scan 4: Dependency audit
Task({ subagent_type: "Explore", run_in_background: true,
  prompt: `In [PROJECT_PATH]:
  1. Read package.json dependencies. For each dependency, grep src/ to check if it's actually imported. Report unused deps.
  2. Find hardcoded colors (text-white, bg-black, #hex, rgb) — skip node_modules, skip test files, skip shadcn/ui component defaults
  3. Check for 'any' type usage in .ts/.tsx files
  Report: unused deps list, hardcoded color count + top files, any type count.` })
```

## Phase 2: Feature Ideation

After scans complete, read project context:
- `CLAUDE.md` — goals, roadmap, known issues
- `README.md` — what the app does
- `package.json` — name, description

Then **walk the user journey** to find gaps:
1. Landing/onboarding — what's the first experience?
2. Core workflow — what does the user do most? Where's the friction?
3. Output/sharing — can users share results? Export? Collaborate?
4. Retention — what brings users back?

Use WebSearch to check 2-3 competitors: "what features do [similar apps] offer?"

Propose only features that pass these filters:
- **Feasible now** — don't propose features for placeholder/coming-soon pages
- **Not already done** — verify the feature doesn't already exist before proposing
- **Specific** — "Add Cmd+K search modal" not "Improve UX"
- **Proportional** — don't propose 6 stories for a clean codebase. 0-3 is fine.

## Phase 3: Present Findings

Present a findings table. Do not auto-create stories.

Validate every finding before including it:
- Claiming "0 tests"? Check test directories, playwright config, jest config first.
- Claiming a file should be split? Check if it has multiple exported components or is actually cohesive.
- Claiming a feature is missing? Grep for it first — it might already exist.

```
Brainstorm Complete
===================
Scanned [N] files in [T] seconds.

| # | Category | Finding | Priority |
|---|----------|---------|----------|
| 1 | Dead Code | 3 unused components in src/components/ | High |
| 2 | Quality  | 12 console.logs in production code | Medium |
| 3 | Perf     | Dashboard page.tsx fetches client-side, could be server prefetch | High |
| 4 | Feature  | Competitor X has [feature] — worth adding | Medium |

Codebase health: [honest assessment — "clean, no urgent issues" is valid]

Say "brainstorm apply" to create stories, or pick specific items.
```

If the codebase is genuinely clean, say so. Do not invent work to fill a table.

### Auto Mode Exception

If `.claude/auto-active` exists (running in auto mode), skip the presentation and create stories directly in prd.json. Auto mode's IDLE detection depends on story creation to continue the loop.

### brainstorm apply

When user says `brainstorm apply`:
1. Read prd.json (or create with `sprint: "S1"` if none exists)
2. Deduplicate against existing stories (match first 25 chars of title)
3. Create stories with ID format `S{sprint}-{number}`
4. Report: "Created X stories, skipped Y duplicates"

## Targeted Mode

When user says `brainstorm X`:
- Skip quality scan entirely
- Read files related to X topic
- Propose 3-5 specific ideas for X
- Present findings (do not auto-create stories)

## Deduplication

Before creating any story, check for existing tasks:

```typescript
const existing = await TaskList();

function isDuplicate(newTitle: string): boolean {
  return existing.some(task =>
    task.subject.toLowerCase().includes(newTitle.toLowerCase().slice(0, 20)) ||
    newTitle.toLowerCase().includes(task.subject.toLowerCase().slice(0, 20))
  );
}

if (!isDuplicate("Add keyboard shortcuts")) {
  TaskCreate({ subject: "Add keyboard shortcuts (Cmd+K)", ... });
}
```

Report skipped duplicates: "Skipped 2 ideas (already in task list)"

## Design System Awareness

Before proposing UI features:
- Check existing component structure (extend vs. replace)
- Ensure proposals use design tokens, not hardcoded colors
- Reference `design` skill for aesthetic consistency

## Rules

- Analyze and propose — do not ask "what do you want?"
- Quality over quantity — 2 real findings beat 6 padded ones
- Validate before claiming — grep to confirm, don't assume
- Skip shadcn/ui colors (library defaults, not project issues)
- Deduplicate against existing tasks before creating
- "Codebase is clean, nothing to propose" is a valid outcome
