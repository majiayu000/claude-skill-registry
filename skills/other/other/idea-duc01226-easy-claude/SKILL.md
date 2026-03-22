---
name: idea
version: 1.0.0
description: "[Project Management] Capture and structure product ideas as backlog artifacts. Use when capturing new ideas, feature requests, or concepts for future refinement. Triggers on keywords like "capture idea", "new idea", "feature idea", "add to backlog", "quick idea"."
allowed-tools: Read, Write, Grep, Glob, TaskCreate, AskUserQuestion
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

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

## Greenfield Mode

> **Auto-detected:** If no existing codebase is found (no code directories like `src/`, `app/`, `lib/`, `server/`, `packages/`, etc., no manifest files like `package.json`/`*.sln`/`go.mod`, no populated `project-config.json`), this skill switches to greenfield mode automatically. Planning artifacts (docs/, plans/, .claude/) don't count — the project must have actual code directories with content.

**When greenfield is detected:**

1. Skip module auto-detection from existing project (no modules exist yet)
2. Skip "MUST READ project-structure-reference.md" (won't exist)
3. Focus on broader problem-space capture: market gap, competitors, differentiation
4. Output tech-agnostic problem statement (no existing tech stack to reference)
5. Enable web research for market/competitor context (WebSearch)
6. Increase AskUserQuestion frequency — capture vision, constraints, team profile, scale expectations
7. **[CRITICAL] DO NOT ask about tech stack during idea capture.** Tech stack is a research-driven decision that comes AFTER full business analysis (business-evaluation phase). If the user volunteers a tech stack preference, acknowledge it but still defer final decision to the tech stack research phase where it will be properly evaluated with pros/cons, market analysis, and team-fit assessment.

- Validation step is mandatory, not optional
- Auto-detect module silently; only prompt when ambiguous

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

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

See: `.claude/docs/team-artifacts/templates/idea-template.md`

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

### Step 6.5: Idea Discovery Interview (MANDATORY)

Use `AskUserQuestion` to probe the idea with 3-5 structured questions. Each question MUST have 2-4 options with one marked "(Recommended)".

#### Question Categories (pick 3-5 based on idea type):

| Category        | Purpose                           | Example                                      |
| --------------- | --------------------------------- | -------------------------------------------- |
| Problem Clarity | Distinguish problem from solution | "What problem does this solve?" with options |
| User Persona    | Identify primary user             | "Who benefits most?" with role options       |
| Scope           | MVP vs full vision                | "What's the smallest valuable version?"      |
| Testability     | Can we define done?               | "How would you verify this works?"           |
| Impact          | Business value sizing             | "How many users/processes does this affect?" |
| Constraints     | Known blockers                    | "Any technical/business constraints?"        |
| Scale           | Expected load and growth          | "How many users/transactions expected?"      |

> **Greenfield note:** In greenfield mode, do NOT include tech stack questions here. Focus on business problem, users, scale, and constraints. Tech stack is evaluated in a dedicated research phase later.

#### Testability Question (ALWAYS include):

"How would you verify this feature works correctly?"

- Options based on domain: manual test steps, automated test criteria, metric thresholds

Document all answers in the idea artifact under `## Discovery Interview`.

### Step 7: Suggest Next Step

After idea capture, suggest:

1. `/refine` — Refine into PBI (Recommended)
2. `/tdd-spec` — Jump straight to test spec creation
3. `/plan` — Start implementation planning

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

## UI Sketch Output Format

> **MUST READ:** `.claude/skills/shared/ui-wireframe-protocol.md`

When the idea involves UI changes, include this section in the idea artifact:

```markdown
## UI Sketch

### Layout

{Rough ASCII wireframe showing spatial arrangement — see ui-wireframe-protocol.md}

### Key Components

- **{Component}** — {purpose} _(tier: common | domain-shared | page/app)_
- **{Component}** — {purpose} _(tier: common | domain-shared | page/app)_
```

> Classify components per **Component Hierarchy** in `ui-wireframe-protocol.md` — search existing libs before proposing new components.
> If backend-only idea: `## UI Sketch` → `N/A — Backend-only change. No UI affected.`

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

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `idea-to-pbi` workflow** (Recommended) — idea → refine → refine-review → story → story-review → prioritize
> 2. **Execute `/idea` directly** — run this skill standalone

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/refine (Recommended)"** — Transform idea into actionable PBI
- **"/web-research"** — If idea needs market research first
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
