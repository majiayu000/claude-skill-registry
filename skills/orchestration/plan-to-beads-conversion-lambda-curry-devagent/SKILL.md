---

name: Plan-to-Beads Conversion

description: >-
  Set up a Ralph execution loop in Beads by mapping a DevAgent plan into a Beads epic
  and tasks with the correct fields, dependencies, and routing labels. Use when:
  (1) Preparing Beads for Ralph autonomous execution, (2) Assigning correct routing
  labels and agents, (3) Ensuring dependencies and report tasks are wired, (4)
  Embedding plan references, quality gates, and context into Beads fields.

---

# Plan-to-Beads Conversion (Ralph Loop Setup)

Set up a Ralph execution loop in Beads by converting a DevAgent plan into an epic + tasks with correct fields, dependencies, and routing labels. This skill is focused on **Beads setup and routing correctness**; the workflow defines the step-by-step process.

## When to Use
- After a plan is drafted/approved and before `start-ralph-execution`.
- When you need correct Beads metadata so Ralph can route tasks to agents reliably.

## Inputs
- Plan path (DevAgent plan markdown)
- Beads prefix (from `bd config get issue_prefix`)
- Ralph config mapping (`.devagent/plugins/ralph/tools/config.json`)

## Core Principles
- **Routing depends on labels.** Every direct epic child must have exactly one routing label from the config mapping.
- **Dependencies are edges, not fields.** You can add them after creation with `bd dep add` (default blocking edge). `bd update` cannot add deps.
- **Traceability is mandatory.** Always include the plan path in epic description and task notes.
- **Manual extraction by default.** Avoid ad-hoc parsing scripts unless explicitly requested.
- **Resumable beats “one big command”.** Always use an idempotent, stepwise approach: create issues individually first, then link dependencies in a second pass. This avoids brittleness from timeouts, partial execution, or environment differences.

## Beads Field Mapping (Plan → Beads)

### Epic (Parent Task)
- **Title:** Plan title from `# <Task Name> Plan`
- **Description:** Must include:
  - `Plan document: <absolute-path>`
  - `Final Deliverable: <Summary or Functional Narrative>`
  - `Final Quality Gates: <detected commands>`

### Tasks (Direct Epic Children)
- **Description:** Combine objective + impacted files + references + testing criteria.
- **Design:** Capture constraints, patterns, and relevant rules (RR7, Storybook, etc.).
- **Notes:** Always include plan path and any warnings/risks.
- **Acceptance:** Semicolon-separated list from plan acceptance criteria.

### Subtasks (Optional)
- Only if the plan explicitly includes them; otherwise skip.
- Leave unlabeled unless you want separate routing.

## Routing Labels (Critical)
Ralph routes work by reading the **first matching label** on each direct epic child task.

### Label Mapping (Use Exactly One)
- `engineering`: code changes, config, scripts, Storybook setup
- `qa`: testing, validation, running checks, evidence capture
- `design`: UX or visual decision-only tasks
- `project-manager`: explicit PM checkpoints, final report task

**Policy:** Do not create epic children without one of the labels above. Use `project-manager` for coordination/doc-only tasks.

**Rule:** direct epic children must have exactly one routing label. Subtasks should be unlabeled unless you want separate routing.

**Beads CLI note (source of many drift bugs):**
- When creating issues, the correct flag is `bd create --labels <label>` (not `--label`).
- Beads supports multiple labels, but for Ralph routing you should pass exactly one label for direct epic children.
- If you need to fix labels after creation, prefer replacing them explicitly:
  ```bash
  bd update <TASK_ID> --set-labels <label> --json
  ```

## Dependencies & Parent Linkage
- **Create-first, link-second (required):**
  - Create the epic and all direct children first (IDs + fields + exactly one routing label).
  - Then add dependency edges with `bd dep add <task-id> <depends-on-id>` (defaults to a blocking dependency).
  - Rationale: `bd create` can be run reliably one task at a time, and dependency linking can be retried independently if something interrupts the session.
- **Parent linkage (safe by default):**
  - Prefer hierarchical IDs (`<epic>.<task>`) for readability.
  - **Still:** After creating each direct epic child (and the report task), explicitly set the parent so epic-scoped queries work reliably:
    ```bash
    bd update <TASK_ID> --parent <EPIC_ID> --json
    ```
  - Why: `bd ready --parent <EPIC_ID>` and other parent-scoped filters often rely on the explicit `parent` field, not just ID structure.

## Resumable Procedure (Recommended)
- **Create issues individually** (epic first, then each direct child task).
- **Link dependencies after all creates** using `bd dep add <task-id> <depends-on-id>`.
- After any interruption, rerun starting from the first missing ID; linking deps can always be retried.
- Verify at the end:
  - `bd show <epic-id> --json`
  - `bd dep tree <epic-id>`
  - `bd ready --parent <epic-id> --limit 200 --json`

## Required Final Report Task
Always add a final task: **“Generate Epic Revise Report”**.
- Depends on all top-level tasks.
- Label: `project-manager`.
- Acceptance criteria include generating the revise report and updating epic status.

## Quality Gates
- Detect from repo `package.json` using the **Quality Gate Detection** skill.
- Include them in the epic description.
- Do not invent gates that do not exist.

## Ralph Readiness Checklist
- Epic created with plan reference + deliverable summary + quality gates.
- All direct epic children present and **exactly one valid routing label** applied.
- Dependencies set correctly; `bd ready --parent <EPIC_ID> --limit 200` shows expected tasks.
- `.devagent/plugins/ralph/tools/config.json` includes valid `git` and `ai_tool` sections.
- Working branch exists and matches config before starting execution.

## Notes on Extraction
Manual extraction from the plan is the default. The setup workflow defines the process and required fields; avoid ad-hoc parsing scripts unless explicitly requested.

## References
- Workflow: `.devagent/plugins/ralph/workflows/setup-ralph-loop.md`
- Beads CLI usage: `.devagent/plugins/ralph/skills/beads-integration/SKILL.md`
- Quality gates: `.devagent/plugins/ralph/skills/quality-gate-detection/SKILL.md`
- Ralph config: `.devagent/plugins/ralph/tools/config.json`

**Epic (Parent Task):**

The epic description must be comprehensive and include:
1. Plan document reference
2. Final deliverable summary (from plan's "Summary" section in PART 1)
3. Final quality gates that must pass

```json
{
  "id": "<epic-id>",
  "title": "<plan-title>",
  "description": "Plan document: <absolute-path-to-plan>\n\nFinal Deliverable: [extract from plan's Summary section in PART 1, or Functional Narrative if Summary is not descriptive enough]\n\nFinal Quality Gates:\n- All tests passing (npm test)\n- Lint clean (npm run lint)\n- Typecheck passing (npm run typecheck)\n- [Include any additional gates from quality-gates.json template]",
  "status": "open"
}
```

**Instructions for Epic Description:**
1. Read the plan document to extract:
   - Summary section (PART 1) - use this for "Final Deliverable" if it clearly describes the end result
   - If Summary is too high-level, use the Functional Narrative section to describe what the final output should be
2. Reference the quality gates template (`.devagent/plugins/ralph/quality-gates/typescript.json` or project-specific template) to list all quality gates that must pass
3. Format as a clear, multi-line description that agents can reference when working on tasks

**Main Tasks:**

Construct the `description` field by combining context fields.

```json
{
  "id": "<epic-id>.<number>",
  "title": "<task-title>",
  "description": "Objective: <objective>\n\nImpacted Modules/Files:\n<impacted-modules>\n\nReferences:\n<references>\n\nTesting Criteria:\n<testing-criteria>",
  "acceptance_criteria": ["<criterion-1>", "<criterion-2>", ...],
  "priority": "normal",
  "status": "open",
  "parent_id": "<epic-id>",
  "depends_on": ["<epic-id>.<dependency-number>", ...],
  "notes": "Plan document: <absolute-path-to-plan>"
}
```

**Subtasks:**

```json
{
  "id": "<epic-id>.<task-number>.<subtask-number>",
  "title": "<subtask-title>",
  "description": "",
  "acceptance_criteria": [],
  "priority": "normal",
  "status": "open",
  "parent_id": "<epic-id>.<task-number>",
  "depends_on": [],
  "notes": "Plan document: <absolute-path-to-plan>"
}
```

**Important:** Always include the absolute path to the source plan document in:
- Epic `description` field
- Each task's `notes` field (for both main tasks and subtasks)

This ensures agents can unambiguously reference the specific plan document when working on tasks.

### Labeling Rules (Routing)

Ralph routes tasks based on **labels** attached to the epic’s direct child tasks.

- **Direct epic children:** Must have **exactly one** routing label from the keys in `.devagent/plugins/ralph/tools/config.json` → `agents`.
- **Subtasks:** Unlabeled by default (context-only). Only add a label if you intentionally want distinct routing.
- **Fallback:** If you cannot confidently pick a specialized label, use `project-manager`.
- **Explicit PM checkpoints:** Use `project-manager` only for phase check-ins or final reviews.

**Implementation note:** This conversion output may not embed labels directly. If labels are applied during `bd create`, ensure the one-level labeling rule is followed there.

### UI-Sensitivity Heuristic (Design Task Creation)

Use the signals below to decide when a plan is UI-sensitive and merits a design task (keep this judgment contextual).

**UI-sensitive signals (lightweight heuristic):**
- Impacted files include UI extensions: `.tsx`, `.jsx`, `.css`, `.scss`, `.sass`, `.less`, `.html`
- Plan text mentions UI/UX keywords: `UI`, `UX`, `design`, `component`, `layout`, `visual`, `styling`, `page`, `screen`, `modal`, `drawer`, `navbar`, `table`, `chart`, `responsive`, `mobile`, `accessibility`, `storybook`
- Acceptance criteria describe visual states, layout changes, or component variants
- Plan involves building new components or component variants

**Design task deliverables (embed in description/design field):**
- Intent + observable acceptance (testable UI behavior)
- Component inventory/reuse list with code references
- Storybook stories when available (do not set up Storybook in the task; create a follow-up task if missing)
- Minimum artifact when Storybook is missing: lightweight mockup or annotated screenshot + acceptance bullets + component inventory

**Notes:** Design output must live in the design task comments with links to artifacts (Storybook paths, screenshots, mockups).

### Step 4: Resolve Dependencies

For each task with dependencies:

1. Parse dependency text to extract task numbers
2. Map task numbers to generated task IDs
3. Populate `depends_on` array with dependency task IDs
4. If dependencies reference tasks not yet created, ensure topological ordering

### Step 5: Append Epic Report Task (Quality Gate)

**Objective:** Ensure every Epic concludes with a mandatory revise report that runs only after all tasks are complete.

**Instructions:**

1. Determine the highest task number (N) from the parsed plan.
2. Create a final task with number N+1.
3. **ID:** `<epic-id>.<N+1>`
4. **Title:** "Generate Epic Revise Report"
5. **Label:** "project-manager" (this task uses the project-manager agent for final review)
6. **Description:** "Auto-generated epic quality gate. This task runs only after all other epic tasks are closed or blocked.

**Steps:**
1. Verify that all child tasks have status 'closed' or 'blocked' (no 'open', 'in_progress' tasks remain)
2. Generate the revise report: `devagent ralph-revise-report <epic-id>`
3. **Epic Status Management:**
   - If ALL tasks are closed (no blocked tasks): Close the epic with `bd update <epic-id> --status closed` and close this report task
   - If ANY tasks are blocked: **Do not block the epic.** Keep the epic `open`, leave this report task `open`, and add a comment explaining which tasks remain blocked and what to re-check on the next run"
6. **Acceptance Criteria:** ["All child tasks are closed or blocked", "Report generated in .devagent/workspace/reviews/", "Epic closed only when all tasks are closed; report task left open with blocker summary when blocked tasks remain"]
7. **Dependencies:** Array containing IDs of ALL other top-level tasks (e.g., `["<epic-id>.1", "<epic-id>.2", ...]`). This ensures the task only becomes ready when all dependencies are complete.
8. **Notes:** Include plan document path: `"Plan document: <absolute-path-to-plan>"`
9. Add this task to the `tasks` array.
10. **Manual backfill:** If an epic is missing the report task, add it using the steps above (set dependencies and parent). Do not add a router-driven auto-close backstop; the report task is the only canonical epic closer.
11. **Post-close policy:** If new tasks are added after an epic is closed, do not auto-reopen the epic (manual only).

### Step Ordering and Numbering (Important)

If you rely on string sorting, hierarchical IDs will sort incorrectly once task numbers exceed 9 (for example, `<epic-id>.10` comes before `<epic-id>.2`).

- **Always** preserve plan order by comparing hierarchical numeric segments (split on `.` and compare numbers).
- This affects both:
  - **Execution order** (when selecting the “first” ready task)
  - **UI ordering** (task boards/lists that display tasks)

### Step 6: Generate Complete Payload

**Full JSON Structure:**

```json
{
  "metadata": {
    "source_plan": "<absolute-path-to-plan>",
    "generated_at": "<ISO-8601-UTC-timestamp>Z"
  },
  "ralph_integration": {
    "ready_command": "bd ready --parent <EPIC_ID> --limit 200",
    "status_updates": {
      "in_progress": "in_progress",
      "closed": "closed"
    },
    "progress_comments": true
  },
  "epics": [
    {
      "id": "<epic-id>",
      "title": "<plan-title>",
      "description": "",
      "status": "open"
    }
  ],
  "tasks": [
    /* array of task objects */
  ]
}
```

### Step 6: Write Output

Write the complete JSON payload to:

- Path: `<output-dir>/beads-payload.json`
- Format: Pretty-printed JSON with 2-space indentation
- Encoding: UTF-8

## Edge Cases

**Missing Sections:**

- If "Implementation Tasks" section not found, report error and stop
- If individual tasks lack required fields (Objective, Acceptance Criteria), use empty values

**Dependency Resolution:**

- If dependency references non-existent task, log warning and omit dependency
- If "None" specified for dependencies, use empty array

**Empty Lists:**

- If no subtasks, omit subtask generation
- If no acceptance criteria, use empty array
- If no dependencies, use empty array

**Special Characters:**

- Preserve markdown formatting in descriptions (can be cleaned later by Beads)
- Handle unicode characters in titles and descriptions

## Validation

Before writing output, validate:

1. At least one task exists (epic alone is invalid)
2. All task IDs are unique
3. All dependency references resolve to existing task IDs
4. All tasks have valid parent_id references
5. JSON structure matches Beads schema

## Reference Documentation

- **Beads Schema**: See `templates/beads-schema.json` in this plugin for field definitions
- **Plan Template**: See `.devagent/core/templates/plan-document-template.md` for plan structure
- **Example Plans**: See `.devagent/workspace/tasks/active/*/plan/*.md` for real plan examples
