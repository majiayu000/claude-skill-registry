---
name: spec-driven-ui
description: >
  Generate front-end UI specifications and code for Web, GUI, or Terminal interfaces
  through a constraint-aware 9-phase workflow with structural anti-skip enforcement.
  Uses Execute-Verify-Record pattern at every step to prevent token optimization bias.
  Supports Web (React, Blazor, ASP.NET, HTML), Desktop GUI (WPF, Tkinter), and Terminal
  interfaces. Validates context files, respects architectural constraints, and interactively
  guides users through technology and styling decisions. Use when stories require UI
  components or when generating visual specifications from requirements. Always use this
  skill when the user runs /create-ui.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Bash(python:*)
  - Bash(devforgeai-validate:*)
  - Skill
model: opus
effort: Medium
---

# Spec-Driven UI Generation

Generate front-end user interface specifications and code through an interactive, constraint-aware 9-phase workflow with structural anti-skip enforcement.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Execution Model

This skill expands inline. After invocation, execute Phase State Initialization immediately. Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively for results
- [ ] Asking "should I execute this?"
- [ ] Skipping a phase because "it seems simple"
- [ ] Combining multiple phases into one
- [ ] Summarizing instead of loading a reference file
- [ ] Skipping verification because "I already wrote the file"

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase State Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Per-phase reference loading** — Each phase loads its reference files FRESH via Read() (not consolidated from memory)
2. **Binary CLI gates** — `devforgeai-validate phase-check/phase-complete/phase-record` (compiled binary, cannot be forged by LLM)
3. **Checkpoint-based state tracking** — Phase state JSON tracks current_phase, phases_completed, steps_completed
4. **Artifact verification** — Phase state file verified via Glob(), outputs verified on disk via Grep()

**Execute-Verify-Record Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform (Read, Write, Glob, Grep, Bash, Task, AskUserQuestion)
- **VERIFY:** How to confirm the action happened (file exists, content matches, exit code, data key populated)
- **RECORD:** CLI command to record completion (`devforgeai-validate phase-record`)

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary. (Reference: RCA-001, RCA-002, STORY-457)

---

## Phase State Initialization

Before any phase executes, initialize phase state tracking.

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-init ${IDENTIFIER} --workflow=ui --project-root=. 2>&1")
```

Where `${IDENTIFIER}` is `${STORY_ID}` (e.g., `STORY-042`) for story mode, or `UI-STANDALONE` for standalone mode.

**VERIFY:** Exit code 0 or 2 (exit code 2 = identifier format not recognized, proceed with backward compatibility).

**If exit code 127:** CLI not installed. Continue without CLI gates but execute ALL phases and steps regardless.

---

## Phase Orchestration

All 9 phases execute for every invocation. There is no mode-conditional phase skipping.

```
active_phases = ["00", "01", "02", "03", "04", "05", "06", "07", "08"]

FOR phase_num in active_phases:
  1. ENTRY GATE: Verify previous phase completed (check phase state or first phase)
  2. LOAD: Read(file_path="src/claude/skills/spec-driven-ui/phases/phase-{phase_num}-{name}.md")
     - If Read fails, try: Read(file_path=".claude/skills/spec-driven-ui/phases/phase-{phase_num}-{name}.md")
  3. EXECUTE: Follow ALL EVR triplets in the phase file — no skipping
  4. RECORD: devforgeai-validate phase-record ${IDENTIFIER} --phase={phase_num} --project-root=. 2>&1
  5. EXIT GATE: Verify phase artifacts exist before proceeding
```

**CRITICAL:** Execute EVERY step in EVERY phase. ALL steps within each phase are mandatory.

---

## Phase Index

| Phase | File | Name | Required Subagents |
|-------|------|------|--------------------|
| 00 | `phases/phase-00-initialization.md` | Initialization | None |
| 01 | `phases/phase-01-context-validation.md` | Context Validation | None |
| 02 | `phases/phase-02-story-analysis.md` | Story Analysis | None |
| 03 | `phases/phase-03-interactive-discovery.md` | Interactive Discovery | None |
| 04 | `phases/phase-04-template-loading.md` | Template Loading | None |
| 05 | `phases/phase-05-code-generation.md` | Code Generation | None |
| 06 | `phases/phase-06-documentation.md` | Documentation | ui-spec-formatter |
| 07 | `phases/phase-07-specification-validation.md` | Specification Validation | None |
| 08 | `phases/phase-08-feedback-completion.md` | Feedback & Completion | None |

---

## Command Integration

This skill is invoked by `/create-ui` with context markers:

### /create-ui context markers:
```
**Mode:** ${MODE}
**Target:** ${STORY_ID or COMPONENT_DESCRIPTION}
```

Where MODE is "story" (with STORY-ID) or "standalone" (with component description text).

---

## Subagent Coordination

**ui-spec-formatter** (Phase 06, Step 6.5)
- Validates generated specifications against framework constraints
- Formats results for user-facing display
- Returns structured JSON with SUCCESS/PARTIAL/FAILED status
- Respects framework guardrails (see `references/ui-result-formatting-guide.md`)

---

## Integration Points

**Invoked by:**
- `/create-ui` command (user-initiated)
- devforgeai-orchestration (when story has UI requirements)
- spec-driven-dev (during implementation)

**Invokes:**
- ui-spec-formatter subagent (Phase 06 Step 6.5)

**Provides output to:**
- spec-driven-dev (UI specs for implementation)
- spec-driven-qa (UI specs for validation)

---

## Reference Files Index

Each phase loads only its required references. No consolidated loading.

| Reference | Loaded By | Purpose |
|-----------|-----------|---------|
| `references/shared-protocols.md` | Phase 00 | EVR pattern documentation, self-check violations |
| `references/parameter-extraction.md` | Phase 00 | Mode detection and parameter extraction |
| `references/context-validation.md` | Phase 01 | Context file verification procedures |
| `references/story-analysis.md` | Phase 02 | Story file parsing and requirements extraction |
| `references/user-input-guidance.md` | Phase 02 | Standalone mode guidance patterns (conditional) |
| `references/interactive-discovery.md` | Phase 03 | AskUserQuestion flow definitions |
| `references/ui-user-input-integration.md` | Phase 03 | User input pattern mappings |
| `references/template-loading.md` | Phase 04 | Framework-to-template mapping |
| `references/web-best-practices.md` | Phase 04 | Web UI best practices (conditional on UI type) |
| `references/gui-best-practices.md` | Phase 04 | Desktop GUI best practices (conditional on UI type) |
| `references/tui-best-practices.md` | Phase 04 | Terminal UI best practices (conditional on UI type) |
| `references/design-system-rules.md` | Phase 04 | 8-point grid, semantic tokens, typography, motion (web + gui only) |
| `references/accessibility-guidelines.md` | Phase 04 | WCAG 2.1 AA compliance, ARIA, keyboard nav (all UI types) |
| `references/component-anatomy.md` | Phase 04 | Smart/Dumb components, file structure, props (web + gui only) |
| `references/devforgeai-integration-guide.md` | Phase 04 | Framework integration patterns |
| `references/code-generation.md` | Phase 05 | Code generation procedures |
| `references/documentation-update.md` | Phase 06 | Documentation and story update procedures |
| `references/ui-spec-formatter-integration.md` | Phase 06 | Subagent invocation protocol |
| `references/ui-result-formatting-guide.md` | Phase 06 | Formatter guardrails and display templates |
| `references/specification-validation.md` | Phase 07 | Validation checklist and user resolution flows |
| `references/error-handling.md` | All | Recovery procedures for common errors |
| `references/ui-generation-examples.md` | Reference | Complete usage examples |

---

## Quality Standards

Generated UI code must:
- Follow coding-standards.md conventions
- Use technologies from tech-stack.md only
- Place files per source-tree.md
- Enforce the 8-point spatial grid and semantic color tokens from `design-system-rules.md`
- Apply the AESTHETIC_VIBE selected in Phase 03 (within design system constraints)
- Meet WCAG 2.1 AA accessibility standards from `accessibility-guidelines.md`
- Structure components per Smart/Dumb patterns from `component-anatomy.md`
- Include accessibility (ARIA, semantic HTML, keyboard navigation)
- Match story acceptance criteria (story mode)
- Apply best practices from type-specific reference files

---

## Success Criteria

| Outcome | Condition |
|---------|-----------|
| SUCCESS | UI spec generated, components created per source-tree.md, no placeholders, all constraints validated, formatter returns SUCCESS |
| PARTIAL | UI spec generated with minor warnings, user accepted PARTIAL status in Phase 07 |
| FAILED | Context files missing, critical constraint violations, or user chose to halt in Phase 07 |

---

## Token Efficiency

**Target:** ~40,000 tokens per component (with EVR enforcement overhead)

**Efficiency achieved through:**
- Native tool usage (Read/Write/Edit not Bash)
- Progressive per-phase reference loading (not consolidated)
- Load only UI type-specific best practices (web OR gui OR tui — not all three)
- Context validation once at Phase 01
- Focused generation per component

---

## Error Handling

**Common errors and recovery:**
1. Context files missing → Direct to `/create-context`
2. Technology conflict with tech-stack.md → AskUserQuestion for resolution
3. Template not found → Validate assets directory, offer alternatives
4. Validation failures → User resolves via Phase 07 AskUserQuestion flows

**See `references/error-handling.md` for complete recovery procedures.**

---

## Change Log

| Date | Story | Change |
|------|-------|--------|
| 2026-03-20 | — | Added design-system-rules.md, accessibility-guidelines.md, component-anatomy.md references (Phase 04 Steps 4.4a-c). Added Aesthetic Vibe discovery (Phase 03 Step 3.7a). Updated Phase 05 code generation to enforce design system, component anatomy, and accessibility constraints. Merged from spec-driven-ui-stitch. |
| 2026-03-18 | — | Created — migrated from devforgeai-ui-generator with EVR anti-skip enforcement |

---

**Created:** 2026-03-18
**Migrated from:** devforgeai-ui-generator
**Pattern:** Spec-driven skill with Execute-Verify-Record anti-skip enforcement
