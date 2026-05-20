---
name: idea
version: 1.0.0
description: "[Project Management] Capture and structure product ideas as backlog artifacts. Use when capturing new ideas, feature requests, or concepts for future refinement. Triggers on keywords like "capture idea", "new idea", "feature idea", "add to backlog", "quick idea"."
allowed-tools: Read, Write, Grep, Glob, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Capture raw product ideas as structured backlog artifacts with project module context.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference doc:
>
> - `project-structure-reference.md` -- project patterns and structure
>
> If file not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Gather Info** — Ask about the idea, problem, value, and target users
2. **Generate Artifact** — Create idea file with ID (IDEA-YYMMDD-NNN) and draft status
3. **Detect Module** — Auto-match to project module, load feature context from docs
4. **Validate** — Interview user to confirm problem statement, scope, stakeholders
5. **Suggest Next** — Point to `/refine` for PBI creation

**Key Rules:**

- Output to `team-artifacts/ideas/{YYMMDD}-{role}-idea-{slug}.md`
- Validation step is mandatory, not optional
- Auto-detect module silently; only prompt when ambiguous

# Idea Capture

Capture raw ideas as structured artifacts for backlog consideration.

## When to Use

- User has new feature concept
- Stakeholder request needs documentation
- Quick capture without full refinement

## Quick Reference

### Workflow

1. Activate `product-owner` skill
2. Gather idea details (problem, value, scope, target users)
3. Generate artifact with ID and draft status
4. Detect related project module (dynamic discovery)
5. Load feature context from `docs/business-features/`
6. Save artifact to `team-artifacts/ideas/`
7. **Validate idea** (MANDATORY) - Interview user to confirm problem statement, scope, and stakeholders
8. Suggest next: `/refine {idea-file}`

### Output

- **Path:** `team-artifacts/ideas/{YYMMDD}-{role}-idea-{slug}.md`
- **ID Pattern:** `IDEA-{YYMMDD}-{NNN}` (sequential)

### Related

- **Role Skill:** `product-owner`
- **Command:** `/idea`
- **Next Step:** `/refine`

## Template

See: `team-artifacts/templates/idea-template.md`

## Detailed Workflow

### Step 1: Gather Information

- If no title provided, ask: "What's the idea in one sentence?"
- Ask: "What problem does this solve?"
- Ask: "Who benefits from this?"
- Ask: "Any initial scope thoughts?"

### Step 2: Generate Artifact

- Create idea file using template
- Generate ID: `IDEA-{YYMMDD}-{NNN}` (sequential)
- Set status: `draft`

### Step 3: Capture Details

- Document problem statement
- List expected value
- Identify target users

### Step 4: Detect Project Module

**Dynamic Discovery:**

1. Run: `Glob("docs/business-features/*/README.md")`
2. Extract module names from paths (e.g., ServiceB, ServiceA, SupportingServices)
3. Match idea keywords against module keywords (reference: `.claude/skills/shared/module-detection-keywords.md`)

**Detection Approach (silent auto-detect):**

- Auto-detect without showing confidence levels
- Only prompt when ambiguous or no clear match
- Multi-module: Load ALL detected modules

**If module detected:**

1. Read `docs/business-features/{module}/README.md` (first 200 lines for overview)
2. Extract feature list from Quick Navigation section
3. Add to idea frontmatter:
    - `module: {detected_module}`
    - `related_features: [Feature1, Feature2]`

**If ambiguous/not detected:**

- Run Glob to get current module list
- Prompt: "Which project module?" + list Glob results + "Cross-cutting/Infrastructure"

**Multi-module detection:**

- If 2+ modules detected, load ALL modules (no primary prompt)
- Add all to `related_features` list

### Step 5: Load Feature Context

Once module detected:

1. Read module README overview section (~2K tokens)
2. Identify closest matching feature(s) from feature list
3. Read corresponding feature doc or `.ai.md` file (3-5K tokens)
4. Extract:
    - Related entities
    - Existing business rules (BR-{MOD}-XXX)
    - Test case patterns (TC-{MOD}-XXX)

**Token Budget:** Target 8-12K tokens total for feature context.

### Step 6: Save Artifact

- Path: `team-artifacts/ideas/{YYMMDD}-{role}-idea-{slug}.md`
- Role: Infer from context or ask
- Include domain context if detected

### Step 7: Suggest Next Step

- Output: "Idea captured! To refine into a PBI, run: `/refine {filename}`"
- If domain module detected: "Module context from {module} will be used during refinement."

## Validation Step (MANDATORY)

After capturing the idea, validate with user. **This step is NOT optional.**

### Question Categories

| Category         | Example Question                                      |
| ---------------- | ----------------------------------------------------- |
| **Problem**      | "Is the problem statement clear and user-focused?"    |
| **Value**        | "What's the expected business value or user benefit?" |
| **Scope**        | "Any scope boundaries to clarify now?"                |
| **Stakeholders** | "Who else should review this idea?"                   |

### Process

1. Generate 2-3 questions focused on problem clarity, scope, and stakeholders
2. Use `AskUserQuestion` tool to interview with specific questions:
    - "Is the problem statement clear and user-focused?"
    - "Any scope boundaries to clarify now?"
    - "Who else should review this idea?"
3. Document in idea artifact under `## Validation Summary`
4. Update idea based on answers

### Validation Output Format

```markdown
## Validation Summary

**Validated:** {date}

### Confirmed

- {decision}: {user choice}

### Action Items

- [ ] {follow-up if any}
```

## Domain Context Output Format

When a project module is detected, include this section in the idea artifact:

```markdown
## Domain Context (Project Features)

### Module

{module_name}

### Related Features

- {Feature1} - [docs link]
- {Feature2} - [docs link]

### Domain Entities

- **Primary:** {Entity1}, {Entity2}
- **Related:** {Entity3}

### Existing Business Rules

- BR-{MOD}-XXX: {Brief description}
```

## Example

```bash
/idea "Dark mode toggle for settings"
```

Creates: `team-artifacts/ideas/260119-po-idea-dark-mode-toggle.md`

```bash
/idea "Add goal progress tracking notification"
```

Creates with ServiceB context: `team-artifacts/ideas/260119-po-idea-goal-progress-notification.md`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
