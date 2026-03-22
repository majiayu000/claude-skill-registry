---
name: spec-driven-documentation
description: >
  Automated documentation generation, auditing, and remediation with structural
  anti-skip enforcement. Supports 3 workflows: Generation (greenfield/brownfield),
  Audit (4-dimension DevEx scoring), and Fix (automated/interactive remediation).
  Uses Execute-Verify-Gate pattern at every step. Designed to prevent token
  optimization bias through lean orchestration, fresh-context subagent delegation,
  per-phase reference loading, and binary CLI gate enforcement. Use when generating
  project documentation, updating docs after story completion, or analyzing
  documentation coverage.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Bash(devforgeai-validate:*)
  - Bash(git:*)
  - Bash(pandoc:*)
  - Bash(wkhtmltopdf:*)
  - Bash(mkdir:*)
  - Skill
model: claude-opus-4-6
effort: High
---

# Spec-Driven Documentation

Automated documentation generation, auditing, and remediation integrated into the DevForgeAI SDLC workflow.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Execution Model

This skill expands inline. After invocation, execute Phase 00 Initialization immediately. Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively for results
- [ ] Asking "should I execute this?"

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase 00 Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Fresh-context subagent execution** - Subagents run in isolated context without accumulated bias
2. **Binary CLI gates** - `devforgeai-validate` CLI commands cannot be forged by LLM
3. **Hook enforcement** - Shell scripts in `.claude/hooks/` run outside LLM control
4. **Step registry + artifact verification** - Phase checkpoint files track every mandatory step

**Execute-Verify-Gate Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform
- **VERIFY:** How to confirm the action happened (Glob, Grep, exit code, Task result)
- **RECORD:** CLI command to record completion (`devforgeai-validate phase-record`)

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

---

## Workflow Modes

| Mode | Trigger | Phase Sequence | Phase Count |
|------|---------|----------------|-------------|
| **Generation** | Story ID provided OR `--mode=greenfield/brownfield` | 01, 02, G03-G10 | 10 |
| **Audit** | `--audit=dryrun` | 01, 02, A03-A07 | 7 |
| **Fix** | `--audit-fix` | 01, 02, F03-F08 | 8 |

---

## Parameter Extraction

Extract parameters from conversation context. See `references/parameter-extraction.md` for the extraction algorithm.

## Command Integration

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$STORY_ID` | /document | Story identifier (STORY-NNN) or empty |
| `$DOC_TYPE` | /document | readme, api, architecture, roadmap, all |
| `$MODE` | /document | greenfield, brownfield |
| `$EXPORT_FORMAT` | /document | markdown, html, pdf |
| `$AUDIT_MODE` | /document | dryrun or null |
| `$AUDIT_FIX` | /document | true or false |
| `$FINDING_FILTER` | /document | F-NNN or all |

---

## Phase 00: Initialization [INLINE]

**Generate Session ID:**
```
SESSION_ID = "DOC-{YYYY-MM-DD}-{NNN}"
# Example: DOC-2026-03-18-001
# NNN increments per day based on existing state files
```

**Determine Workflow Type:**
```
IF $AUDIT_MODE is set (dryrun):
    WORKFLOW_TYPE = "audit"
    WORKFLOW_FLAG = "--workflow=doc-audit"
ELIF $AUDIT_FIX is true:
    WORKFLOW_TYPE = "fix"
    WORKFLOW_FLAG = "--workflow=doc-fix"
ELSE:
    WORKFLOW_TYPE = "generation"
    WORKFLOW_FLAG = "--workflow=doc-gen"
```

**CLI Initialization:**
```bash
devforgeai-validate phase-init ${SESSION_ID} ${WORKFLOW_FLAG} --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${SESSION_ID}` to get CURRENT_PHASE. |
| 2 | Invalid session ID | HALT. Must match DOC-YYYY-MM-DD-NNN pattern. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

**Display Session Banner:**
```
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  Documentation Workflow: {WORKFLOW_TYPE}"
Display: "  Session: {SESSION_ID}"
Display: "  Story: {STORY_ID or 'N/A'}"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## Phase Orchestration Loop

```
# Select phase list based on WORKFLOW_TYPE
IF WORKFLOW_TYPE == "generation":
    PHASE_LIST = ["01", "02", "G03", "G04", "G05", "G06", "G07", "G08", "G09", "G10"]
ELIF WORKFLOW_TYPE == "audit":
    PHASE_LIST = ["01", "02", "A03", "A04", "A05", "A06", "A07"]
ELIF WORKFLOW_TYPE == "fix":
    PHASE_LIST = ["01", "02", "F03", "F04", "F05", "F06", "F07", "F08"]

EXPECTED_COUNT = len(PHASE_LIST)
completed_count = 0

FOR phase_id in PHASE_LIST starting from CURRENT_PHASE:
    prev_id = previous phase in PHASE_LIST (or "00" for first)

    1. ENTRY GATE: devforgeai-validate phase-check ${SESSION_ID} --from={prev_id} --to={phase_id} ${WORKFLOW_FLAG}
       IF exit != 0: HALT

    2. LOAD: Read(file_path="phases/{phase_files[phase_id]}")

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-RECORD triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction tells you what CLI command to call

    4. RECORD: devforgeai-validate phase-record ${SESSION_ID} --phase={phase_id} ${WORKFLOW_FLAG}

    5. EXIT GATE: devforgeai-validate phase-complete ${SESSION_ID} --phase={phase_id} --checkpoint-passed ${WORKFLOW_FLAG}
       IF exit != 0: HALT

    completed_count += 1
```

---

## Phase Tables

### Generation Workflow (10 phases)

| Phase | Name | File |
|-------|------|------|
| 01 | Preflight & Mode Detection | `phases/phase-01-preflight.md` |
| 02 | Workflow Dispatch | `phases/phase-02-dispatch.md` |
| G03 | Discovery & Analysis | `phases/phase-G03-discovery.md` |
| G04 | Content Generation | `phases/phase-G04-content-generation.md` |
| G05 | Template Application | `phases/phase-G05-template-application.md` |
| G06 | Section Integration | `phases/phase-G06-section-integration.md` |
| G07 | Post-Generation Integration | `phases/phase-G07-post-generation.md` |
| G08 | Validation & Quality Check | `phases/phase-G08-validation.md` |
| G09 | Export & Finalization | `phases/phase-G09-export.md` |
| G10 | Completion Summary | `phases/phase-G10-completion.md` |

### Audit Workflow (7 phases)

| Phase | Name | File |
|-------|------|------|
| 01 | Preflight & Mode Detection | `phases/phase-01-preflight.md` |
| 02 | Workflow Dispatch | `phases/phase-02-dispatch.md` |
| A03 | Audit Discovery | `phases/phase-A03-audit-discovery.md` |
| A04 | Audit Analysis | `phases/phase-A04-audit-analysis.md` |
| A05 | Audit Prioritization | `phases/phase-A05-audit-prioritization.md` |
| A06 | Audit Output | `phases/phase-A06-audit-output.md` |
| A07 | Audit Display | `phases/phase-A07-audit-display.md` |

### Fix Workflow (8 phases)

| Phase | Name | File |
|-------|------|------|
| 01 | Preflight & Mode Detection | `phases/phase-01-preflight.md` |
| 02 | Workflow Dispatch | `phases/phase-02-dispatch.md` |
| F03 | Load Findings | `phases/phase-F03-load-findings.md` |
| F04 | Classify Findings | `phases/phase-F04-classify.md` |
| F05 | Preview Changes | `phases/phase-F05-preview.md` |
| F06 | Execute Fixes | `phases/phase-F06-execute.md` |
| F07 | Verify Fixes | `phases/phase-F07-verify.md` |
| F08 | Fix Report | `phases/phase-F08-report.md` |

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement |
|-------|-------------------|-------------|
| G03 | code-analyzer | CONDITIONAL (brownfield only) |
| G04 | documentation-writer | BLOCKING |
| All others | (none) | N/A |

**Deviation Protocol:** Any skip requires explicit user consent via AskUserQuestion.

---

## State Persistence

**Location:** `devforgeai/workflows/${SESSION_ID}-${WORKFLOW_TYPE}-phase-state.json`
**Checkpoints:** `devforgeai/workflows/${SESSION_ID}-checkpoint.json`

---

## Workflow Completion Validation

```
IF completed_count < EXPECTED_COUNT:
    HALT "WORKFLOW INCOMPLETE - {completed_count}/{EXPECTED_COUNT} phases"
IF completed_count == EXPECTED_COUNT:
    "All {EXPECTED_COUNT} phases completed - {WORKFLOW_TYPE} workflow validation passed"
```

---

## Success Criteria

### Generation Workflow
- Documentation files generated/updated
- All required sections present
- Documentation coverage >= 80% (quality gate)
- Mermaid diagrams render correctly (if architecture type)
- Framework constraints respected
- Story file updated (if story-based)
- Export formats created (if requested)

### Audit Workflow
- All docs files inventoried
- 4 dimensions scored with evidence
- Findings classified and prioritized
- `devforgeai/qa/audit/doc-audit.json` written
- Summary report displayed

### Fix Workflow
- Audit file loaded and findings filtered
- User consent obtained before execution
- Fixes applied (automated + interactive)
- Verification passed (orphans, links, facts)
- Fix session appended to doc-audit.json
- Summary report displayed

---

## Reference Files Index

### Phase Files (phases/ directory)

See Phase Tables above for complete listing.

### Supporting References (references/ directory)

| File | Purpose | Loaded By |
|------|---------|-----------|
| parameter-extraction.md | Parameter extraction algorithm | Phase 01 |
| documentation-standards.md | Style guide, formatting, conventions | Phase G04, G08 |
| greenfield-workflow.md | Story extraction, content generation | Phase G03 |
| brownfield-analysis.md | Codebase scanning, gap identification | Phase G03 |
| diagram-generation-guide.md | Mermaid syntax, validation | Phase G04 |
| template-customization.md | Variable substitution, custom templates | Phase G05 |
| post-generation-workflow.md | Module name, section insertion, README/CHANGELOG | Phase G06, G07 |
| anti-aspirational-guidelines.md | Prohibited language, content quality | Phase G04, G08 |
| document-help.md | Quick reference for /document command | On-demand |
| audit-workflow.md | Full 4-dimension scoring rubric | Phase A03, A04 |
| audit-fix-catalog.md | Fix actions per finding type | Phase A05, F03, F04, F06 |

### Template Files (assets/templates/ directory)

| File | Doc Type |
|------|----------|
| readme-template.md | README |
| developer-guide-template.md | Developer Guide |
| api-docs-template.md | API Reference |
| troubleshooting-template.md | Troubleshooting |
| contributing-template.md | Contributing |
| changelog-template.md | Changelog |
| architecture-template.md | Architecture |
| roadmap-template.md | Roadmap |

---

## Integration Points

**From:**
- spec-driven-stories (story specifications)
- spec-driven-architecture (context files)
- spec-driven-dev (completed implementations)

**To:**
- spec-driven-release (documentation quality gate)
- Documentation files (README, guides, API docs)

**Auto-invokes:**
- documentation-writer subagent (prose generation, Phase G04)
- code-analyzer subagent (codebase analysis, Phase G03, brownfield only)

---

**Created:** 2026-03-18
**Migrated from:** devforgeai-documentation v1.1.0
**Status:** Production Ready
**Version:** 1.0.0
