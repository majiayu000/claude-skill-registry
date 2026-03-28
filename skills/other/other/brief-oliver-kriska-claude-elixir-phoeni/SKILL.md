---
name: phx:brief
description: Interactive briefing of an Elixir/Phoenix plan file. Explains reasoning, ecto schema decisions, liveview component choices, and solution shape in progressive sections so developers understand before approving or after completion. Use when team members need to understand a plan without reading the full document.
effort: low
argument-hint: [path to plan file]
---

# Plan Briefing

Interactive walkthrough of a plan's reasoning, decisions, and solution
shape. Designed for developers who need to understand a plan in 1-2
minutes instead of reading the full document.

## Why This Exists

Plans answer "what to do" but bury "why." This skill bridges that
gap with an interactive walkthrough.

## Usage

```
/phx:brief                                    # Latest plan
/phx:brief .claude/plans/user-auth/plan.md    # Specific plan
```

## Arguments

- `$ARGUMENTS` = Path to plan file (optional, auto-detects latest)

## Mode Detection

Read the plan file and determine mode from phase statuses:

- **All phases `[PENDING]`** = Pre-work briefing (what WILL happen)
- **Any phase `[COMPLETED]` or `[IN_PROGRESS]`** = Post-work briefing
  (what WAS done and why)

## Execution Flow

### Step 1: Locate and Load Plan

1. If `$ARGUMENTS` has a path, use it
2. Otherwise, find latest plan:

   ```bash
   ls -t .claude/plans/*/plan.md 2>/dev/null | head -1
   ```

3. If no plan found, tell user and suggest `/phx:plan`
4. Read the plan file

### Step 2: Load Supporting Artifacts

Read what's available (don't fail if missing):

- `.claude/plans/{slug}/summaries/consolidated.md` (research summary)
- `.claude/plans/{slug}/scratchpad.md` (decisions, dead-ends)
- `.claude/plans/{slug}/progress.md` (work log, post-work only)

### Step 3: Present Briefing Sections

Present ONE section at a time, wrapped in the visual briefing block
(see `${CLAUDE_SKILL_DIR}/references/briefing-guide.md` Visual Formatting). After each
section, use `AskUserQuestion` with options:

- If sections remain: **"Next: {title}"**, **"Ask me a question
  about this"**, **"Stop here"**
- If final section: no question needed, show closing message

### Section Flow (Pre-Work Mode)

| # | Title | Source |
|---|-------|--------|
| 1 | What We're Building | Summary + Scope |
| 2 | Key Decisions | Technical Decisions + scratchpad rationale |
| 3 | Solution Shape | Phases overview + Data Model |
| 4 | Risks & Confidence | Risks table + unknowns/spikes |

### Section Flow (Post-Work Mode)

| # | Title | Source |
|---|-------|--------|
| 1 | What Was Built | Summary + completion status |
| 2 | Key Decisions & Why | Technical Decisions + scratchpad |
| 3 | How It Was Built | Phases with implementation notes |
| 4 | Lessons & Patterns | Risks encountered + patterns used |

See `${CLAUDE_SKILL_DIR}/references/briefing-guide.md` for section content templates.

## Iron Laws

1. **ONE section at a time** — never dump all content
2. **User controls pace** — always offer to stop
3. **Explain WHY, not just WHAT** — rationale over listing
4. **Ground in artifacts** — focus on insights specific to this
   plan's research, decisions, and scratchpad entries, not general
   programming concepts
5. **Keep each section under 20 lines** — this is a briefing,
   not a lecture
6. **NEVER skip sections or auto-start work** — briefing is read-only; do not execute plan tasks or launch `/phx:work` without explicit user request

## Closing Message

After final section (or when user stops):

```
That's the briefing! For full details, see:
{plan_path}

Ready to proceed? Try `/phx:work {plan_path}` to start execution.
```

Post-work variant:

```
That's what was built! For full details, see:
{plan_path}

Consider `/phx:compound` to capture key learnings for future reference.
```

## Integration

```text
/phx:plan  -->  /phx:brief (optional)  -->  /phx:work  -->  /phx:brief (optional)
  create       understand before            execute        understand after
```

## Complex Plan Enhancement

For plans with 5+ phases or 4+ key decisions, consider suggesting
visual rendering after Section 3. See
`${CLAUDE_SKILL_DIR}/references/visual-explainer.md` for thresholds and commands.

## Notes

- Runs in main conversation context (not a subagent)
- Model: no special requirement — uses default session model
- No artifacts written — briefing is ephemeral, plan IS the artifact
- Reference file readable since skill runs in user's session
