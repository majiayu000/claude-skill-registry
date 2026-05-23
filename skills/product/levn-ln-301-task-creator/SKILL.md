---
name: ln-301-task-creator
description: Creates ALL task types (implementation, refactoring, test). Generates task documents from templates, validates type rules, creates in Linear, updates kanban. Invoked by orchestrators.
---

# Universal Task Creator

Worker that generates task documents and creates Linear issues for implementation, refactoring, or test tasks as instructed by orchestrators.

## Purpose & Scope
- Owns all task templates and creation logic (Linear + kanban updates)
- Generates full task documents per type (implementation/refactoring/test)
- Enforces type-specific hard rules (no new tests in impl, regression strategy for refactoring, risk matrix and limits for test)
- Drops NFR bullets if supplied; only functional scope becomes tasks
- Never decides scope itself; uses orchestrator input (plans/results)

## Task Storage Mode

| Aspect | Linear Mode | File Mode |
|--------|-------------|-----------|
| **Create task** | `create_issue(parentId, state: "Backlog")` | `Write("docs/tasks/epics/.../tasks/T{NNN}-{slug}.md")` |
| **Task ID** | Linear issue ID (e.g., PROJ-123) | File-based (e.g., T001, T002) |
| **Status** | Linear state field | `**Status:** Backlog` in file |
| **Kanban** | Auto-synced | Must update `kanban_board.md` manually |

**File Mode task creation:**
1. Determine next task number: count existing `T*.md` files + 1
2. Generate filename: `T{NNN}-{slug}.md` (e.g., `T003-implement-auth-service.md`)
3. Write task file using template
4. Add link to `kanban_board.md` under Story in Backlog section

## Invocation (who/when)
- **ln-300-task-coordinator:** CREATE (no tasks) or ADD (appendMode) for implementation tasks.
- **Orchestrators (other groups):** Create refactoring or test tasks as needed.
- Never called directly by users.

## Inputs
- Common: `taskType`, teamId, Story data (id/title/description with AC, Technical Notes, Context).
- Implementation CREATE: idealPlan (1-6 tasks), guideLinks.
- Implementation ADD: appendMode=true, newTaskDescription, guideLinks.
- Refactoring: codeQualityIssues, refactoringPlan, affectedComponents.
- Test: manualTestResults, testPlan (E2E 2-5, Integration 0-8, Unit 0-15, Priority ≤15), infra/doc/cleanup items.

## Workflow (concise)
1) **DRY Check (Codebase Scan):** For EACH Task in plan:
   - Extract keywords: function type, component name, domain from Task description
   - Scan codebase: `Grep(pattern="[keyword]", path="src/", output_mode="files_with_matches")` for similar functionality
   - **IF similar code found** (≥70% keyword match):
     - Add `⚠️ DRY Warning` section to Task description BEFORE Implementation Plan:
       ```markdown
       > [!WARNING]
       > **DRY Check:** Similar functionality detected in codebase
       > - Existing: src/services/auth/validateToken.ts:15-42
       > - Similarity: 85% (function name, domain match)
       > - **Recommendation:** Review existing implementation before creating new code
       >   - Option 1: Reuse existing function (import and call)
       >   - Option 2: Extend existing function with new parameters
       >   - Option 3: Justify why reimplementation needed (document in Technical Approach)
       ```
   - **IF no duplication** → Proceed without warning
   - Rationale: Prevents code duplication BEFORE implementation starts
2) **Template select:** Load template based on taskType (see "Template Loading" section).
3) **Generate docs:** Fill sections for each task in plan/request using provided data, guide links, and DRY warnings.
4) **Validate type rules:** Stop with error if violation (see table below).
5) **Preview:** Show titles/goals/estimates/AC/components, DRY warnings count, and totals.
6) **Confirmation required:** Proceed only after explicit confirm.
7) **Create issues:** Call Linear create_issue with parentId=Story, state=Backlog; capture URLs.
8) **Update kanban:** Add under Story in Backlog with correct Epic/indent.
9) **Return summary:** URLs, counts, hours, guide link count, DRY warnings count; next steps (validator/executor).

## Type Rules (must pass)
| taskType | Hard rule | What to verify |
|----------|-----------|----------------|
| implementation | No new test creation | Scan text for "write/create/add tests" etc.; allow only updating existing tests |
| refactoring | Regression strategy required | Issues listed with severity; plan in 3 phases; regression strategy (Baseline/Verify/Failure); preserve functionality |
| test | Risk-based plan required | Priority ≤15 scenarios; E2E 2-5, Integration 0-8, Unit 0-15, Total 10-28; no framework/library/DB tests |

## Critical Notes
- **MANDATORY:** Always pass `state: "Backlog"` when calling create_issue. Linear defaults to team's default status (often "Postponed") if not specified.
- **DRY Check:** Scan codebase for EACH Task before generation. If similar code found (≥70% keyword match) → add `⚠️ DRY Warning` section with 3 options (reuse/extend/justify). Skip scan for test tasks (no implementation code).
- Foundation-First order for implementation is preserved from orchestrator; do not reorder.
- No code snippets; keep to approach, APIs, and pseudocode only.
- Documentation updates must be included in Affected Components/Docs sections.
- Language preservation: keep Story language (EN/RU) in generated tasks.

**DRY Warning Examples:**
```markdown
Example 1: Email validation (HIGH similarity - 90%)
> [!WARNING]
> **DRY Check:** Similar functionality detected
> - Existing: src/utils/validators/email.ts:validateEmail()
> - Similarity: 90% (exact function name + domain match)
> - **Recommendation:** REUSE existing function (Option 1)

Example 2: User authentication (MEDIUM similarity - 75%)
> [!WARNING]
> **DRY Check:** Partial functionality exists
> - Existing: src/services/auth/login.ts:authenticateUser()
> - Similarity: 75% (domain match, different scope)
> - **Recommendation:** Review existing code, consider EXTEND (Option 2) or JUSTIFY new implementation (Option 3)

Example 3: No duplication (skip warning)
- No similar code found → Proceed without DRY warning
```

## Definition of Done
- **DRY Check complete:** Codebase scanned for EACH Task; similar code detected (Grep); DRY warnings added to Task descriptions if ≥70% similarity found.
- Context check complete (existing components/schema/deps/docs reviewed; conflicts flagged).
- Documents generated with correct template, full sections, and DRY warnings (if applicable).
- Type validation passed (no test creation for impl; regression strategy for refactor; risk matrix/limits for test).
- Preview shown with DRY warnings count and user confirmed.
- Linear issues created with parentId and URLs captured; state=Backlog.
- kanban_board.md updated under correct Epic/Story with indentation.
- Summary returned with URLs, totals, DRY warnings count, and next steps.

## Template Loading

**Templates:** `task_template_implementation.md`, `refactoring_task_template.md`, `test_task_template.md`

**Template Selection by taskType:**
- `implementation` → `task_template_implementation.md`
- `refactoring` → `refactoring_task_template.md`
- `test` → `test_task_template.md`

**Loading Logic (for each template):**
1. Check if `docs/templates/{template}.md` exists in target project
2. IF NOT EXISTS:
   a. Create `docs/templates/` directory if missing
   b. Copy `shared/templates/{template}.md` → `docs/templates/{template}.md`
   c. Replace placeholders in the LOCAL copy:
      - `{{TEAM_ID}}` → from `docs/tasks/kanban_board.md`
      - `{{DOCS_PATH}}` → "docs" (standard)
3. Use LOCAL copy (`docs/templates/{template}.md`) for all operations

**Rationale:** Templates are copied to target project on first use, ensuring:
- Project independence (no dependency on skills repository)
- Customization possible (project can modify local templates)
- Placeholder replacement happens once at copy time

## Reference Files
- Templates (centralized): `shared/templates/task_template_implementation.md`, `shared/templates/refactoring_task_template.md`, `shared/templates/test_task_template.md`
- Local copies: `docs/templates/*.md` (in target project)
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
