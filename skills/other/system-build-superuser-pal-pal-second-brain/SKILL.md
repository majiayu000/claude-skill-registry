---
name: system-build
description: Specification-driven development toolkit for PAL system building. USE WHEN create spec, specification, feature spec, implementation plan, generate tasks, task breakdown, checklist, clarify requirements, analyze consistency, constitution, system build, build system, develop PAL, document skill, document command, document hook, generate requirements.
user-invocable: false
---

# system-build

Specification-driven development toolkit for structured PAL system building and feature implementation. Provides workflows for creating specifications, planning implementation, generating tasks, and quality validation.

## Workflow Routing

| Workflow | Trigger | File |
| :--- | :--- | :--- |
| **specify** | "create spec", "feature specification", "new feature" | `workflows/specify.md` |
| **clarify** | "clarify spec", "resolve ambiguities", "spec questions" | `workflows/clarify.md` |
| **plan** | "implementation plan", "technical plan", "design plan" | `workflows/plan.md` |
| **tasks** | "generate tasks", "break down plan", "task list" | `workflows/tasks.md` |
| **implement** | "implement feature", "execute tasks", "start implementation" | `workflows/implement.md` |
| **document** | "document feature", "generate requirements", "create docs" | `workflows/document.md` |
| **document_skill** | "document skill", "document command", "document hook", "skill requirements", "command requirements", "hook requirements" | `workflows/document_skill.md` |
| **tasks_to_issues** | "create issues", "export to GitHub" | `workflows/tasks_to_issues.md` |
| **constitution** | "update constitution", "project governance" | `workflows/constitution.md` |

## Templates

Located in `templates/` directory:

- `feature_template.md` - Unified feature file template (v2 format)
- `spec_template.md` - Feature specification structure (v1 format - deprecated)
- `plan_template.md` - Implementation plan structure (v1 format - deprecated)
- `tasks_template.md` - Task breakdown structure (v1 format - deprecated)
- `agent_file_template.md` - Agent file template

See `templates/README.md` for format documentation.

## Workflow Sequence

```
1. specify → Create FEATURE.md with ## Specification section (status: specified)
2. clarify → Resolve ambiguities, update ## Specification (status: clarified, optional)
3. plan → Append ## Implementation Plan section to FEATURE.md (status: planned)
4. tasks → Append ## Tasks section to FEATURE.md (status: tasked)
5. implement → Execute tasks, generate ## Testing Instructions, STOP for UAT (status: implemented)
6. **USER TESTING** → User follows testing instructions, provides feedback
   - PASS → Status becomes 'tested', proceed to step 7
   - FAIL → Feedback captured, new tasks created, loop back to step 5
7. document → Generate requirements documentation, update ## Completion Summary (status: documented)
8. tasks_to_issues → Export to GitHub issues (status: exported)
```

**UAT Phase (Step 6):** The implement workflow generates step-by-step testing instructions based on user stories and acceptance criteria, then STOPS and WAITS for user feedback. This ensures features are validated before documentation.

## Format Versions

This skill supports two feature file formats:

- **v2 (current):** Single `FEATURE.md` file with all sections (Specification, Implementation Plan, Tasks, Testing Instructions, Implementation Notes, Completion Summary)
- **v1 (legacy):** Four separate files (`spec.md`, `plan.md`, `tasks.md`, `checklist.md`)

All workflows detect the format automatically and handle both. New features use v2 format (FEATURE.md).

## Routing Awareness

This skill supports dual-repository workflows:

- **Personal features** → Created in main repo domains (`Domains/{domain}/`)
- **Open-source features** → Created in submodule (`Domains/PALOpenSource/Domains/PALBuilder/`)

Routing is determined during the `specify` workflow and persisted in FEATURE.md frontmatter:

```yaml
routing: personal | open-source
target_path: [resolved path]
```

The `document_skill` and `tasks_to_issues` workflows also respect routing:
- `document_skill` targets requirements in either personal or submodule PALBuilder
- `tasks_to_issues` targets the correct GitHub repository based on routing

**Reference:** `.claude/core/reference/REPO_ROUTING.md` for complete artifact inventory

## Examples

**Example 1: Create a new feature specification**

```
User: "Create a spec for user authentication with OAuth2"
→ Invokes specify workflow
→ Generates branch name and feature directory
→ Creates FEATURE.md using feature_template.md
→ Populates ## Specification section only
→ Status: specified
→ Reports completion with next steps (clarify or plan)
```

**Example 2: Generate implementation plan**

```
User: "Create a plan for the auth feature"
→ Invokes plan workflow
→ Loads ## Specification from FEATURE.md
→ Appends ## Implementation Plan section to FEATURE.md
→ Status: planned
→ Reports completion with next steps (tasks)
```

**Example 3: Break down into tasks**

```
User: "Generate tasks from the plan"
→ Invokes tasks workflow
→ Reads ## Specification and ## Implementation Plan from FEATURE.md
→ Appends ## Tasks section to FEATURE.md with dependencies
→ Status: tasked
→ Returns task count and phases
→ Reports next steps (implement)
```

**Example 4: Implement with UAT**

```
User: "Implement the feature"
→ Invokes implement workflow
→ Reads ## Tasks from FEATURE.md
→ Executes tasks, marks them complete
→ Generates ## Testing Instructions from user stories
→ Status: implemented
→ **STOPS and presents testing instructions to user**
→ User tests and provides feedback:
   - PASS → Status: tested, proceed to document
   - FAIL → Feedback captured, new tasks created, loop back
```
