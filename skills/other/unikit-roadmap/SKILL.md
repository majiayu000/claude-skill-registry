---
name: unikit-roadmap
description: >-
  Create or update a strategic project roadmap with major milestones.
  Generates .unikit/ROADMAP.md — a high-level checklist of project goals.
  Use when user says "roadmap", "project plan", "milestones", "what to build next",
  "strategic goals", or wants to see big-picture progress. Also use when the user
  asks to check which milestones are done or wants to plan the overall project direction.
argument-hint: "[check | project vision or requirements]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git *)
  - AskUserQuestion
  - Agent
disable-model-invocation: true
user-invocable: true
metadata:
  author: unikit
  version: "1.1"
  category: planning
---

# Roadmap — Strategic Project Planning

Create and maintain a high-level project roadmap with major milestones.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

## Workflow

### Step 0: Load Project Context

**Read `.unikit/DESCRIPTION.md`** if it exists to understand:
- Tech stack (engine, framework, DI, async patterns)
- Project architecture and conventions
- Non-functional requirements

**Read `.unikit/ARCHITECTURE.md`** if it exists to understand:
- Chosen architecture pattern and folder structure
- Module boundaries and communication patterns

**Read `.unikit/skill-context/unikit-roadmap/SKILL.md`** — MANDATORY if the file exists.

This file contains project-specific rules accumulated by `/unikit-evolve` from patches,
codebase conventions, and tech-stack analysis. These rules are tailored to the current project.

**How to apply skill-context rules:**
- Treat them as **project-level overrides** for this skill's general instructions
- When a skill-context rule conflicts with a general rule written in this SKILL.md,
  **the skill-context rule wins** (more specific context takes priority)
- When there is no conflict, apply both: general rules from SKILL.md + project rules from skill-context
- Do NOT ignore skill-context rules even if they seem to contradict this skill's defaults —
  they exist because the project's experience proved the default insufficient
- **CRITICAL:** skill-context rules apply to ALL outputs of this skill — including the ROADMAP.md
  template. The template in this SKILL.md is a **base structure**. If a skill-context rule says
  "roadmap MUST include X" or "milestones MUST have Y" — you MUST augment the template accordingly.
  Generating a roadmap that violates skill-context rules is a bug.

**Enforcement:** After generating any output artifact, verify it against all skill-context rules.
If any rule is violated — fix the output before presenting it to the user.

### Step 1: Determine Mode

If argument is `check` → Mode 3: Check Progress (requires ROADMAP.md)

Otherwise check if `.unikit/ROADMAP.md` exists:
- **Does NOT exist** → Mode 1: Create Roadmap
- **Exists** → Mode 2: Update Roadmap

---

### Mode 1: Create Roadmap (First Run)

**1.1: Gather Input**

If user provided arguments — first classify each argument:
- **File path** (contains `/`, `\`, or ends with a known extension like `.md`, `.txt`, `.json`, `.pdf`, `.docx`) → treat as a **reference document**. Read the file content and use it as context for generating milestones. Store the path for the References section.
- **Plain text** → treat as vision/description input for milestones.

Arguments can be mixed — e.g., a description string plus one or more file paths.

If reference documents were detected:
- Read each document via `Read` tool
- Extract key goals, requirements, features, and priorities from the document content
- Use extracted information as primary input for milestone generation
- Track which milestones were derived from which documents — this mapping will be recorded in the `## References` section

If only plain text arguments provided:
- Use as primary input for milestones

If no arguments:
- Ask interactively:

```
AskUserQuestion: What are the major goals for this project?

Options:
1. Let me describe the vision
2. Analyze codebase and suggest milestones
3. Both — I'll describe, you'll add what's missing
```

Based on choice:
- Describe vision → ask follow-up about priorities (next question)
- Analyze codebase → proceed to Step 1.2 (Explore Codebase), auto-generate milestones
- Both → ask for description, then enrich with codebase analysis

If user chooses option 1 or 3, ask follow-up:

```
AskUserQuestion: Any priorities or deadlines?

Options:
1. Yes, let me specify
2. No, just order by logical sequence
3. Skip — I'll reprioritize later
```

Based on choice:
- Yes → ask user for priorities/deadlines, incorporate into milestone ordering
- No → order milestones by logical dependency sequence
- Skip → proceed without priority ordering

**1.2: Explore Codebase**

Scan the project to understand what's already built:
- `Glob` for project structure (key directories, modules)
- `Grep` for implemented features (controllers, systems, views, installers)
- Check git log for completed work: `git log --oneline -20`

**1.3: Generate ROADMAP.md**

Create `.unikit/ROADMAP.md` using the format defined in the **ROADMAP.md Format** section below.

**Rules for milestones:**
- Each milestone is a **high-level goal**, not a granular task (that's `/unikit-plan`)
- 5-15 milestones is the sweet spot — fewer means too vague, more means too granular
- Order by logical sequence (dependencies first)
- Mark already-completed milestones as `[x]` and add them to the Completed table
- Use today's date for milestones detected as already done

**1.4: Confirm with user**

Show the generated roadmap and ask:

```
AskUserQuestion: Here's the proposed roadmap. What would you like to do?

Options:
1. Looks good — save it
2. Add more milestones
3. Remove/modify some milestones
4. Rewrite — let me give better input
```

Based on choice:
- Save → write to `.unikit/ROADMAP.md`
- Add more → ask for additional milestones, regenerate, re-confirm
- Remove/modify → ask which to change, apply edits, re-confirm
- Rewrite → ask for new input, regenerate from scratch

---

### Mode 2: Update Roadmap (Subsequent Run)

**2.1: Read Current State**

- Read `.unikit/ROADMAP.md`
- Read `.unikit/DESCRIPTION.md` for context
- Explore codebase briefly to check what's changed since last update

**2.2: Determine Action**

If user provided arguments — classify each argument (same rules as Mode 1 Step 1.1):
- **File path** → read document, use content as context, add to `## References` section (append to existing references, avoid duplicates)
- **Plain text** → treat as new milestones or change instructions

If arguments contain reference documents:
- Read each document, extract goals/requirements
- Generate new milestones from the document content and append to the roadmap
- Add document paths to the References section

If only plain text arguments:
- Apply the requested changes directly

If no arguments:
- Analyze current state and present options:

```
AskUserQuestion: What would you like to do with the roadmap?

Options:
1. Review progress — check what's done, mark completed milestones
2. Add new milestones
3. Reprioritize — reorder existing milestones
4. Rewrite — major revision of the roadmap
```

Based on choice:
- Review progress → scan codebase for completed milestones, propose updates (Step 2.3)
- Add milestones → ask for new milestones, append to roadmap (Step 2.4)
- Reprioritize → present current order, ask for new order (Step 2.5)
- Rewrite → major revision, ask for new vision

**2.3: Review Progress (if chosen)**

- Scan codebase for evidence of completed milestones
- For each unchecked milestone, check if the work appears done
- Propose marking completed milestones:

```
AskUserQuestion: These milestones appear to be done:
- **Milestone Name** — [evidence: files exist, systems implemented, etc.]

Mark them as completed?

Options:
1. Yes — mark all as completed
2. No — skip
```

Based on choice:
- Yes → change `- [ ]` to `- [x]` for listed milestones, add to Completed table with today's date
- No → skip, proceed to next step

If confirmed:
- Change `- [ ]` to `- [x]` in the Milestones section
- Add entry to Completed table with today's date
- Move completed milestones below unchecked ones (or keep in place — user preference)

**2.4: Add New Milestones (if chosen)**

- Ask user to describe new milestones
- Insert them in logical order among existing milestones
- Update `.unikit/ROADMAP.md`

**2.5: Reprioritize (if chosen)**

- Show current order
- Ask user for new order or let them describe priority changes
- Reorder milestones in `.unikit/ROADMAP.md`

**2.6: Save Changes**

Update `.unikit/ROADMAP.md` with all modifications.

Show summary:
```
## Roadmap Updated

Total milestones: N
✅ Completed: X/N
▶ Next up: **Milestone Name**

To start working on the next milestone:
/unikit-plan <milestone description>  → creates plan
/unikit-implement                     → executes the plan
```

---

### Mode 3: Check Progress (`/unikit-roadmap check`)

Automated scan — analyze the codebase, detect completed milestones, and propose marking them (with user confirmation).

**Requires** `.unikit/ROADMAP.md` to exist. If it doesn't — tell the user to run `/unikit-roadmap` first.

**3.1: Read roadmap and project context**

- Read `.unikit/ROADMAP.md`
- Read `.unikit/DESCRIPTION.md` for tech stack context

**3.2: Analyze each unchecked milestone**

For every `- [ ]` milestone:
- Determine what evidence would prove it's done (files, systems, models, configs, tests)
- Use `Glob` and `Grep` to search for that evidence
- Check `git log --oneline --all -30` for related commits
- Score: **done** (strong evidence), **partial** (some work started), **not started**

**3.3: Report findings**

```
## Roadmap Progress Check

✅ Done (ready to mark):
- **Trading System** — found: TradeController, TradeOffer, trade installers, tests
- **Customer Behaviour** — found: CustomerFSM, NodeCanvas trees, customer spawning

🔄 In Progress:
- **Mini-Games System** — found: MiniGameLauncher exists but SliderGame incomplete

⏳ Not Started:
- **Night Market**
- **Dynamic Events**

Mark completed milestones? (2 milestones)
```

**3.4: Apply changes (if confirmed)**

- Mark done milestones `[x]`
- Add entries to Completed table with today's date
- Leave partial and not-started milestones unchanged

Show updated summary:
```
✅ Completed: X/N milestones
▶ Next up: **Milestone Name**
```

---

## ROADMAP.md Format

```markdown
# Project Roadmap

> <project vision — one-liner>

## Milestones

- [ ] **Name** — short description
- [ ] **Name** — short description
- [x] **Name** — short description

## References

| Document | Description | Milestones |
|----------|-------------|------------|
| `relative/path/to/document.md` | Brief description of contents | Milestone A, Milestone B |

## Completed

| Milestone | Date |
|-----------|------|
| Name | YYYY-MM-DD |
```

**References section rules:**
- Include `## References` only when reference documents were provided as arguments
- If no documents were passed — omit the section entirely (do not include an empty table)
- Store paths relative to the project root
- Description column: a short summary of what the document covers (extracted during reading)
- Milestones column: comma-separated names of milestones that were derived from or informed by this document. When generating milestones from a document, track which milestones came from which source. A milestone may appear in multiple rows if it was informed by several documents.
- On subsequent updates (Mode 2): append new documents, never remove existing references unless user explicitly asks. When new milestones are added from existing references, update the Milestones column accordingly.

## Critical Rules

1. **Milestones are high-level** — each represents a major feature or capability, not a task
2. **ROADMAP.md is the source of truth** — always read before modifying
3. **Never remove milestones silently** — always confirm with user before removing
4. **Completed table tracks history** — every checked milestone gets a date entry
5. **NO implementation** — this skill only plans, use `/unikit-plan` to start a feature and `/unikit-implement` to execute
6. **Ownership boundary** — this command owns `.unikit/ROADMAP.md`. `/unikit-implement` may only mark milestones completed when implementation evidence is clear
7. **Respond in the configured language** — use `language.ui` from `.unikit/config.yaml` (default: English) for all user-facing messages
8. **References are append-only** — never remove document references unless explicitly asked by the user
9. **References require documents** — only add the `## References` section when actual documents were provided; never generate it with empty content
