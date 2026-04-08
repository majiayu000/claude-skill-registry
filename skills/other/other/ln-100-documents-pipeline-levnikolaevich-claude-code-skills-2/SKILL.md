---
name: ln-100-documents-pipeline
description: "Creates complete project documentation system (project docs, reference, tasks, tests). Use when bootstrapping docs from scratch or regenerating all."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

**Type:** L1 Top Orchestrator
**Category:** 1XX Documentation Pipeline

# Documentation Pipeline (Orchestrator)

This skill orchestrates the creation of a complete documentation system by invoking one L2 coordinator plus 3 L2 workers. The coordinator (ln-110) delegates to 5 L3 workers for project docs; other L2 workers handle reference, tasks, and test domains. Each component validates its own output, and the orchestrator owns the final docs-quality acceptance gate.

## Purpose

Top-level orchestrator that creates a complete project documentation system in one invocation. Chains ln-110 coordinator + ln-120/130/140 workers sequentially, then runs global cleanup (deduplication, orphan reporting, cross-link validation).

## Runtime Contract

**MANDATORY READ:** Load `shared/references/coordinator_runtime_contract.md`, `shared/references/docs_pipeline_runtime_contract.md`, `shared/references/docs_generation_summary_contract.md`

Runtime family: `docs-pipeline-runtime`

Identifier:
- `docs-pipeline`

Phases:
1. `PHASE_0_CONFIG`
2. `PHASE_1_LEGACY_SCAN`
3. `PHASE_2_CONFIRMATION`
4. `PHASE_3_DELEGATE`
5. `PHASE_4_QUALITY_GATE`
6. `PHASE_5_CLEANUP`
7. `PHASE_6_SELF_CHECK`

Component summary contract:
- `ln-110`, `ln-120`, `ln-130`, `ln-140` write or return `docs-generation` envelopes
- `ln-100` consumes those summaries plus docs-quality checkpoints as orchestration SSOT

## Architecture

```
ln-100-documents-pipeline (L1 Top Orchestrator - this skill)
|- ln-110-project-docs-coordinator (L2 Coordinator)
|  |- ln-111-root-docs-creator (L3 Worker) -> 5 docs
|  |- ln-112-project-core-creator (L3 Worker) -> 3 docs
|  |- ln-113-backend-docs-creator (L3 Worker) -> 2 conditional
|  |- ln-114-frontend-docs-creator (L3 Worker) -> 1 conditional
|  `- ln-115-devops-docs-creator (L3 Worker) -> 1 always + 1 conditional
|- ln-120-reference-docs-creator (L2 Worker)
|- ln-130-tasks-docs-creator (L2 Worker)
`- ln-140-test-docs-creator (L2 Worker - optional)
```

## When to Use This Skill

This skill should be used when:
- Start a new IT project and need complete documentation system at once
- Use automated workflow instead of manually invoking multiple workers
- Create entire documentation structure (`AGENTS.md` + `CLAUDE.md` -> `docs/`) in one go
- Prefer orchestrated CREATE path over manual skill chaining
- Need automatic global cleanup (deduplication, orphaned files, consolidation)

**Alternative**: If you prefer granular control, invoke workers manually:
1. [ln-110-project-docs-coordinator](../ln-110-project-docs-coordinator/SKILL.md) - Root + Project docs (coordinates 5 L3 workers)
2. [ln-120-reference-docs-creator](../ln-120-reference-docs-creator/SKILL.md) - reference/ structure
3. [ln-130-tasks-docs-creator](../ln-130-tasks-docs-creator/SKILL.md) - tasks/README.md + kanban
4. [ln-140-test-docs-creator](../ln-140-test-docs-creator/SKILL.md) - tests/README.md (optional)

**MANDATORY READ:** Load `shared/references/docs_quality_contract.md`.

**Note**: Each worker validates its own local output in Phase 2/3. The orchestrator still owns the final docs-quality manifest, verification, and repair loop before cleanup can continue.

## Workflow

The skill follows a 5-phase orchestration workflow: **Legacy Migration (optional)** -> User confirmation -> Invoke coordinator + workers sequentially -> Global cleanup -> Summary.

---

### Phase 0: Legacy Migration (OPTIONAL)

**Objective**: Detect existing documentation in non-standard formats, extract valuable content, and prepare for migration.

**Trigger**: Always runs at pipeline start. User can skip if no legacy docs or wants to keep existing structure.

**Process**:

**0a. Legacy Detection**:
- Scan project for non-standard documentation using patterns from `references/legacy_detection_patterns.md`:
  - **Root .md files**: `ARCHITECTURE.md`, `REQUIREMENTS.md`, `STACK.md`, `API.md`, `DATABASE.md`, `DEPLOYMENT.md`
  - **Legacy folders**: `documentation/`, `doc/`, `wiki/`, `docs/` with wrong structure
  - **README.md sections**: `## Architecture`, `## Tech Stack`, `## Requirements`, etc.
  - **CONTRIBUTING.md sections**: `## Development`, `## Code Style`, `## Coding Standards`
- Build `legacy_manifest`: list of { path, detected_type, target_doc, confidence }
- If no legacy docs found -> skip to Phase 1

**0b. Content Extraction**:
- For each detected legacy file:
  - Parse markdown structure (headers, lists, code blocks)
  - Apply type-specific extractor (**MANDATORY READ:** Load `references/legacy_detection_patterns.md`):
    - `architecture_extractor` -> { layers[], components[], diagrams[] }
    - `requirements_extractor` -> { functional[], non_functional[] }
    - `tech_stack_extractor` -> { frontend, backend, database, versions }
    - `principles_extractor` -> { principles[], anti_patterns[] }
    - `api_spec_extractor` -> { endpoints[], authentication }
    - `database_schema_extractor` -> { tables[], relationships[] }
    - `runbook_extractor` -> { prerequisites[], install_steps[], env_vars[] }
    - `infrastructure_extractor` -> { servers[], domains[], ports[], services[], artifacts{}, cicd{} }
  - Score content quality (0.0-1.0)
- Store in `extracted_content` object

**0c. User Confirmation**:
- Display detected legacy files:
  ```
  Legacy Documentation Detected:

  | File | Type | Confidence | Target |
  |------|------|------------|--------|
  | README.md (## Architecture) | architecture | HIGH | docs/project/architecture.md |
  | docs/ARCHITECTURE.md | architecture | HIGH | docs/project/architecture.md |
  | CONTRIBUTING.md (## Development) | principles | MEDIUM | docs/principles.md |

  Migration Options:
  1. MIGRATE (recommended): Extract -> Inject -> Archive -> Delete
  2. ARCHIVE ONLY: Backup without extraction
  3. SKIP: Leave legacy as-is (may cause duplication)

  Choose option (1/2/3): _
  ```
- If user selects "1" (MIGRATE):
  - Optional: "Review extracted content before injection? (yes/no)"
  - Confirm: "Proceed with migration and archive legacy files?"
- If user selects "2" (ARCHIVE ONLY):
  - Confirm: "Archive legacy files to .archive/? Content will NOT be extracted."
- If user selects "3" (SKIP):
  - Warn: "Legacy files will remain. This may cause duplication issues."
  - Proceed to Phase 1

**0d. Backup and Archive**:
- Create `.archive/legacy-{timestamp}/` directory
- Structure:
  ```
  .archive/
  `- legacy-YYYY-MM-DD-HHMMSS/
      |- README_migration.md        # Rollback instructions
      |- original/                  # Exact copies of legacy files
      |  |- README.md
      |  |- ARCHITECTURE.md
      |  `- documentation/
      `- extracted/                 # Extracted content (for reference)
          |- architecture_content.md
          `- principles_content.md
  ```
- Copy all legacy files to `original/`
- Save extracted content to `extracted/`
- Generate `README_migration.md` with rollback instructions

**0e. Content Injection**:
- Build `migration_context` from extracted content:
  ```json
  {
    "LEGACY_CONTENT": {
      "legacy_architecture": { "sections": [...], "diagrams": [...] },
      "legacy_requirements": { "functional": [...] },
      "legacy_principles": { "principles": [...] },
      "legacy_tech_stack": { "frontend": "...", "backend": "..." },
      "legacy_api": { "endpoints": [...] },
      "legacy_database": { "tables": [...] },
      "legacy_runbook": { "install_steps": [...] },
      "legacy_infrastructure": { "servers": [...], "domains": [...], "ports": {} }
    }
  }
  ```
- Merge into Context Store for ln-110:
  - `contextStore.LEGACY_CONTENT = migration_context`
  - Workers use LEGACY_CONTENT as base content (priority over template defaults)
- Priority order: **Legacy content > Auto-discovery > Template defaults**

**0f. Cleanup (Legacy Files)**:
- For root-level files (README.md, CONTRIBUTING.md):
  - Do NOT delete
  - Remove migrated sections using Edit tool
  - Add links to new locations:
    - `## Architecture` -> replace with link: `[Architecture](docs/project/architecture.md)`
    - `## Tech Stack` -> replace with link: `[Tech Stack](docs/project/tech_stack.md)`
- For standalone legacy files (ARCHITECTURE.md, documentation/):
  - Delete files (already backed up)
  - Log: "Deleted: ARCHITECTURE.md (migrated to docs/project/architecture.md)"
- Clean empty legacy directories

**Output**: `migration_summary` { migrated_count, archived_count, skipped_count, legacy_content }

### Phase 1: User Confirmation

**Objective**: Check existing files, explain workflow, and get user approval.

**Process**:

0. **Migration Summary** (if Phase 0 ran):
   - Show: "Migrated {N} legacy documents"
   - Show: "Archived to .archive/legacy-{date}/"
   - Show: "LEGACY_CONTENT prepared for workers"

1. **Pre-flight Check** (scan existing documentation):
   - Use Glob tool to check all potential files:
     - **Root docs** (5 files): `AGENTS.md`, `CLAUDE.md`, `docs/README.md`, `docs/documentation_standards.md`, `docs/principles.md`
     - **Reference structure** (5 items): `docs/reference/README.md`, `docs/reference/adrs/`, `docs/reference/guides/`, `docs/reference/manuals/`, `docs/reference/research/`
     - **Tasks docs** (2 files): `docs/tasks/README.md`, `docs/tasks/kanban_board.md`
     - **Project docs** (up to 8 files): `docs/project/requirements.md`, `architecture.md`, `tech_stack.md`, `api_spec.md`, `database_schema.md`, `design_guidelines.md`, `infrastructure.md`, `runbook.md`
     - **Test docs** (2 files): `docs/reference/guides/testing-strategy.md`, `tests/README.md`
   - Count existing vs missing files
   - Show user summary:
     ```
     Documentation Status:
     Found: X existing files
     Missing: Y files

     Pipeline will create ONLY missing files.
     Existing files will be preserved (no overwrites).
     ```

2. Show user what will be created:
   - Root + Project documentation (`AGENTS.md` + `CLAUDE.md` + `docs/README.md` + `documentation_standards.md` + `principles.md` + `docs/project/` via ln-110-project-docs-coordinator)
   - Reference structure (docs/reference/ via ln-120-reference-docs-creator)
   - Task management docs (docs/tasks/ via ln-130-tasks-docs-creator)
   - Test documentation (tests/ via ln-140-test-docs-creator - optional)
   - Estimated time: 15-20 minutes with interactive dialog

3. Ask: "Proceed with creating missing files? (yes/no)"

4. Ask: "Include test documentation (tests/README.md)? (yes/no)"

**Output**: File scan summary + user approval + test docs preference

---

### Phase 2: Invoke Coordinator + Workers Sequentially

**Objective**: Create complete documentation system by invoking L2 coordinator + 4 L2 workers in order.

**Process** (AUTOMATIC invocations with Skill tool):

**2a. Create Root + Project Documentation**:
- **Invocation**: `Skill(skill: "ln-110-project-docs-coordinator")` -> AUTOMATIC
- **Input**: Pass `LEGACY_CONTENT` from Phase 0 (if migration was performed)
- **Behavior**: Coordinator gathers context ONCE, then delegates to 5 L3 workers:
  - ln-111-root-docs-creator -> 5 root docs (uses LEGACY_CONTENT.legacy_principles if available)
  - ln-112-project-core-creator -> 3 core docs (uses LEGACY_CONTENT.legacy_architecture, legacy_requirements, legacy_tech_stack)
  - ln-113-backend-docs-creator -> 2 conditional (uses LEGACY_CONTENT.legacy_api, legacy_database)
  - ln-114-frontend-docs-creator -> 1 conditional (if hasFrontend)
  - ln-115-devops-docs-creator -> 2 docs: 1 always + 1 conditional (uses LEGACY_CONTENT.legacy_runbook, legacy_infrastructure)
- **Output**: Root docs (`AGENTS.md` + `CLAUDE.md` + `docs/README.md` + `docs/documentation_standards.md` + `docs/principles.md`) + Project docs (`docs/project/requirements.md`, `architecture.md`, `tech_stack.md`, `infrastructure.md` + conditional: `api_spec.md`, `database_schema.md`, `design_guidelines.md`, `runbook.md`)
- **Store**: Save `context_store` from ln-110 result (contains TECH_STACK for ln-120)
- **Validation**: Each L3 worker validates output (SCOPE, metadata markers, top sections, Maintenance)
- **Verify**: All documents exist before continuing

**2b. Create Reference Structure + Smart Documents**:
- **Invocation**: `Skill(skill: "ln-120-reference-docs-creator")` -> AUTOMATIC
- **Input**: Pass `context_store` from ln-110 (TECH_STACK enables smart document creation)
- **Output**: `docs/reference/README.md` + `adrs/`, `guides/`, `manuals/`, `research/` directories + **justified ADRs/Guides/Manuals**
- **Smart Creation**: Creates documents only for nontrivial technology choices (see ln-120 justification rules)
- **Validation**: ln-120 validates output in Phase 2/3
- **Verify**: Reference hub exists before continuing

**2c. Create Task Management Docs**:
- **Invocation**: `Skill(skill: "ln-130-tasks-docs-creator")` -> AUTOMATIC
- **Output**: `docs/tasks/README.md` + optionally `kanban_board.md` (if user provides Linear config)
- **Validation**: ln-130 validates output in Phase 2/3
- **Verify**: Tasks README exists before continuing

**2d. Create Test Documentation (Optional)**:
- **Condition**: If user approved test docs in Phase 1
- **Invocation**: `Skill(skill: "ln-140-test-docs-creator")` -> AUTOMATIC
- **Output**: `tests/README.md` (test documentation with Story-Level Test Task Pattern)
- **Validation**: ln-140 validates output in Phase 2/3
- **Skip**: If "no" -> can run ln-140-test-docs-creator later manually

**2e. Extract Skills from Documentation (Optional)**:
- **Condition**: User approved skill extraction in Phase 1, or invoked manually later
- **Invocation**: `Skill(skill: "ln-160-docs-skill-extractor")` -> AUTOMATIC
- **Input**: All docs created by ln-110 through ln-140
- **Output**: `.claude/commands/*.md` files extracted from procedural documentation sections
- **Skip**: If not approved -> can run ln-160-docs-skill-extractor later manually

**Output**: Complete documentation system with coordinator + 4 workers completed and validated

## Worker Invocation (MANDATORY)

## TodoWrite format (mandatory)
Add ALL invocations to todos before starting:
```
- Invoke ln-110-project-docs-coordinator (pending)
- Invoke ln-120-reference-docs-creator (pending)
- Invoke ln-130-tasks-docs-creator (pending)
- Invoke ln-140-test-docs-creator (pending)
- Run Global Cleanup (Phase 3) (pending)
- Show Summary (Phase 4) (pending)
```
Mark each as in_progress when starting, completed when worker returns success.

---

### Phase 3: Global Cleanup and Consolidation

**Objective**: Remove duplicates, orphaned files, consolidate knowledge across ALL documentation.

**Trigger**: Only after ALL workers complete Phase 2/3 validation.

**Process**:

**3a. Build docs-quality manifest**

Create one normalized manifest from worker outputs before any cleanup:

1. Collect `created_files`, `skipped_files`, and `quality_inputs` from ln-110, ln-120, ln-130, and ln-140
2. Merge `quality_inputs.doc_paths` and `quality_inputs.owners`, deduplicate paths, and fail fast if any worker omitted the normalized return contract
3. Write the explicit manifest with the shared verifier:
   ```bash
   node {skills_repo_root}/skills-catalog/shared/scripts/docs-quality/cli.mjs manifest \
     --project-root . \
     --files "AGENTS.md,CLAUDE.md,docs/README.md,docs/project/requirements.md" \
     --output docs/project/.audit/ln-100/docs-quality-manifest.json
   ```
4. Keep the manifest as the Single Source of Truth for all Phase 3 quality decisions

**3b. Run centralized docs-quality verifier**

Run the shared verifier against the manifest:

```bash
node {skills_repo_root}/skills-catalog/shared/scripts/docs-quality/cli.mjs verify \
  --project-root . \
  --manifest docs/project/.audit/ln-100/docs-quality-manifest.json \
  --output docs/project/.audit/ln-100/docs-quality-report.json
```

Verifier checks come from the shared docs-quality contract/rules and include:
- SCOPE tags in required docs
- Maintenance section + markers
- Forbidden placeholders and leaked template metadata
- Broken internal links
- Disallowed code fences
- Stale inline dates
- Non-official stack documentation links

**Gate:** No HIGH/CRITICAL findings may remain before Phase 3 cleanup proceeds.

**3c. Bounded repair loop**

If verifier reports HIGH/CRITICAL findings:

1. **Pass 1 - deterministic inline fixes**:
   - Add missing SCOPE tags
   - Add or complete `## Maintenance`
   - Normalize broken internal links when target is obvious
   - Refresh stale generated dates
   - Remove leaked template metadata and unresolved markers
   - Replace illegal fenced code with tables, commands, or links
2. **Pass 2 - owner-scoped semantic repair**:
   - Group remaining findings by `quality_inputs.owners[path]`
   - Re-invoke only the owning worker with the scoped findings for its files
   - Do not rerun unrelated workers
3. Re-run the verifier after each repair pass
4. Stop after 2 repair iterations total
5. If any HIGH/CRITICAL findings remain, fail the pipeline instead of emitting low-quality docs

Record the verifier summary and doc-registry output in the Phase 5 final output.

**3d. Scan for duplicate content**

1. **Read all .md files in docs/**
   - Use Glob tool: `pattern: "docs/**/*.md"`
   - Store list of all documentation files

2. **Identify duplicate sections:**
   - For each file:
     - Read file content
     - Extract section headers (##, ###)
     - Extract section content (text between headers)
   - Compare sections across files:
     - If 2+ sections have:
       - Same heading (case-insensitive)
       - >80% content similarity (simple word overlap check)
     - Mark as duplicate

3. **Determine canonical version:**
   - Rules for canonical location:
     - "Development Principles" -> principles.md (always canonical)
     - "Testing Strategy" -> testing-strategy.md (always canonical)
     - "Linear Configuration" -> tasks/kanban_board.md (always canonical)
     - For other duplicates: Keep in FIRST file encountered (alphabetical order)

4. **Remove duplicates:**
   - For each duplicate section:
     - Use Edit tool to delete from non-canonical files
     - Use Edit tool to add link to canonical location:
       ```markdown
       Canonical source: [Development Principles](../principles.md#development-principles)
       ```
   - Track count of removed duplicates

5. **Log results:**
   - "Removed {count} duplicate sections"
   - List: "{section_name} removed from {file} (canonical: {canonical_file})"

**3e. Report unexpected files (advisory)**

1. **List all .md files in docs/**
   - Use Glob tool: `pattern: "docs/**/*.md"`

2. **Check against expected structure** (files created by workers + user-created reference docs)

3. **Report findings (DO NOT move/delete/archive):**
   - List unexpected files with advisory message
   - User decides what to do with them
   - Log: "{count} unexpected files found (not in expected structure) -> listed for user review"

**3f. Consolidate knowledge**

1. **Identify scattered information:**
   - Known patterns:
     - Linear config scattered: kanban_board.md + tasks/README.md
     - Development principles scattered: AGENTS.md + principles.md + architecture.md
     - Testing info scattered: testing-strategy.md + tests/README.md + architecture.md

2. **For each scattered concept:**
   - Determine Single Source of Truth (SSoT):
     - Linear config -> kanban_board.md
     - Development principles -> principles.md
     - Testing strategy -> testing-strategy.md

3. **Update non-SSoT files:**
   - Use Edit tool to replace duplicate content with link:
     ```markdown
     Canonical source: [Linear Configuration](../tasks/kanban_board.md#linear-configuration)
     ```
   - Track consolidation count

4. **Log results:**
   - "Consolidated {count} scattered concepts"
   - List: "{concept} consolidated to {SSoT_file}"

**3g. Cross-link validation**

1. **Scan all .md files for internal links:**
   - For each file:
     - Read content
     - Extract all markdown links: `[text](path)`
     - Filter internal links (relative paths, not http://)

2. **Verify link targets exist:**
   - For each link:
     - Resolve relative path
     - Check if target file exists (Glob tool)
     - If missing: Mark as broken

3. **Fix broken links:**
   - For each broken link:
     - If target was archived: Update link to archive path
     - If target never existed: Remove link (convert to plain text)
   - Track fix count

4. **Add missing critical links:**
   - **AGENTS.md -> docs/README.md:**
     - Read AGENTS.md
     - Check for link to docs/README.md
     - If missing: Add in "Documentation Hub" section
   - **docs/README.md -> section READMEs:**
     - Check for links to project/, reference/, tasks/, tests/ READMEs
     - If missing: Add
   - Track added links count

5. **Log results:**
   - "Fixed {count} broken links"
   - "Added {count} missing critical links"
   - List changes

**3h. Final report**

```
Global Cleanup Complete:

Structure:
- Removed {N} duplicate sections (canonical: principles.md)
- Found {N} unexpected files (listed for user review)
- Consolidated {N} scattered concepts

Links:
- Fixed {N} broken links
- Added {N} missing critical links:
  - list of added links
```

**Output**: All documentation cleaned up, duplicates removed, unexpected files reported, knowledge consolidated, cross-links validated

---

### Phase 4: Summary and Next Steps

**Objective**: Provide complete overview of created system.

**Process**:
1. List all created files with sizes:
   - `AGENTS.md` (canonical project entry point)
   - `CLAUDE.md` (thin Anthropic compatibility shim)
   - `docs/README.md` (root documentation hub)
   - `docs/documentation_standards.md` (60 universal requirements)
   - `docs/principles.md` (11 development principles)
   - `docs/project/requirements.md`, `architecture.md`, `tech_stack.md` + conditional documents (3-7 total)
   - `docs/reference/README.md` (reference hub with empty adrs/, guides/, manuals/, research/ directories)
   - `docs/tasks/README.md` + optionally `kanban_board.md`
   - `tests/README.md` (if created)

2. Show documentation system features:
   - SCOPE tags (document boundaries defined)
   - Maintenance sections (update triggers + verification)
   - README hub (central navigation)
   - DAG structure (Directed Acyclic Graph navigation)
   - Living documentation ready
   - Deduplicated content (canonical sources only)
   - Validated cross-links (no broken links)

3. Recommend next steps:
   - "Review generated documentation (AGENTS.md/CLAUDE.md -> docs/)"
   - "Run ln-210-epic-coordinator to decompose scope into Epics"
   - "Share documentation with technical stakeholders"

4. Summarize the docs-quality gate:
   - `Verifier score: X/10`
   - `Repair passes used: 0-2`
   - `Remaining warnings: list LOW/MEDIUM only`

**Output**: Summary message with file list, verifier status, and recommendations

---

## Complete Output Structure

```
project_root/
|- AGENTS.md                         # Canonical project entry point (map-first root)
|- CLAUDE.md                         # Thin Anthropic compatibility shim
|- docs/
|  |- README.md                     # Root documentation hub (general standards)
|  |- documentation_standards.md    # 60 universal requirements (Claude Code + industry standards)
|  |- principles.md                 # 11 development principles (Standards First, YAGNI, KISS, DRY, etc.)
|  |- project/
|  |  |- requirements.md           # Functional Requirements (NO NFR per project policy)
|  |  |- architecture.md           # arc42-based architecture with C4 Model
|  |  |- tech_stack.md             # Technology versions, Docker config
|  |  |- api_spec.md               # API endpoints (conditional)
|  |  |- database_schema.md        # Database schema (conditional)
|  |  |- design_guidelines.md      # UI/UX system (conditional)
|  |  |- infrastructure.md         # Infrastructure inventory (always)
|  |  `- runbook.md                # Operations guide (conditional)
|  |- reference/
|  |  |- README.md                 # Reference documentation hub (registries)
|  |  |- adrs/                     # Empty, ready for ADRs
|  |  |- guides/                   # Empty, ready for guides
|  |  |- manuals/                  # Empty, ready for manuals
|  |  `- research/                 # Empty, ready for research
|  |- tasks/
|  |  |- README.md                 # Task management system rules
|  |  `- kanban_board.md           # Linear integration (optional)
`- tests/
   `- README.md                    # Test documentation (optional)
```

---

## Integration with Project Workflow

**Recommended workflow for new projects:**

1. **ln-100-documents-pipeline** (this skill) - Create complete documentation system
2. **ln-210-epic-coordinator** - Decompose scope into Epics (Linear Projects)
3. **ln-220-story-coordinator** - Create User Stories for each Epic (automatic decomposition + replan)
4. **ln-300-task-coordinator** - Break down Stories into implementation tasks (automatic decomposition + replan)
5. **ln-310-multi-agent-validator** - Verify Stories before development
6. **ln-400-story-executor** - Orchestrate Story implementation
7. **Story quality gate** - Review completed Stories

---

## Trade-offs

**Trade-offs:**
- Less granular control (can't skip coordinator phases)
- Longer execution time (15-20 minutes)
- Global cleanup runs even if only one file was created

**When to use manual approach instead:**
- Need one specific ADR/guide/manual -> use shared/templates/ + shared/references/documentation_creation.md

---

## Documentation Standards

All documents created by this pipeline MUST follow these rules:

| Rule | Description | Enforcement |
|------|-------------|-------------|
| **NO_CODE Rule** | Documents describe contracts, not implementations | No code blocks >5 lines; use tables/ASCII/links |
| **Stack Adaptation** | Links must match project TECH_STACK | .NET -> Microsoft docs, JS -> MDN |
| **Format Priority** | Tables/ASCII > Lists (enumerations only) > Text | Tables for params, config, alternatives |

These standards are enforced by L3 workers (ln-111-115), ln-120/130/140, and the shared docs-quality gate.

---

## Error Handling

If any invoked skill fails:
1. Notify user which skill failed
2. Show error message from failed skill
3. Recommend manual invocation for debugging
4. List already completed steps (partial progress)

---

## Technical Implementation Notes

**Skill Invocation:**
- Uses **Skill tool** with command parameter
- Waits for each skill to complete before proceeding
- Verifies output files exist before moving to next phase

**File Verification:**
- Uses **Glob** tool to check docs/project/ structure
- Lists file sizes for user confirmation
- Warns if expected files missing

**Global Cleanup:**
- Uses **Glob** tool to find all .md files
- Uses **Read** tool to analyze content
- Uses **Edit** tool to remove duplicates and add links
- Reports unexpected files (advisory, no auto-archive)

**Docs-Quality Gate:**
- Uses `shared/scripts/docs-quality/cli.mjs` to build a manifest from worker outputs
- Uses the shared verifier before cleanup and again after repair passes
- Fails fast on unresolved HIGH/CRITICAL findings instead of emitting low-quality documentation

**Standards Compliance:**
- All output follows same standards as underlying skills
- ISO/IEC/IEEE 29148:2018 (Requirements)
- ISO/IEC/IEEE 42010:2022 (Architecture)
- arc42 + C4 Model + Michael Nygard's ADR Format

---

## Critical Rules

- **Idempotent:** Creates only missing files; existing files are preserved without overwrite
- **Sequential invocation:** Workers must be invoked in order (ln-110 -> ln-120 -> ln-130 -> ln-140); each verified before next
- **Docs-quality gate mandatory:** Phase 3 must build manifest -> run verifier -> execute bounded repair loop before cleanup continues
- **Global cleanup mandatory:** Phase 3 (deduplication, orphan reporting, SSoT consolidation, cross-link validation) runs only after docs-quality gate passes
- **User confirmation required:** Pre-flight check and explicit approval before any file creation
- **NO_CODE Rule:** All generated documents use tables/ASCII/links; no code blocks >5 lines

## Phase 5: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `planning-coordinator`. Run after all phases complete. Output to chat using the `planning-coordinator` format.

## Reference Files

- Legacy detection patterns: `references/legacy_detection_patterns.md`
- Worker skills: `ln-110-project-docs-coordinator`, `ln-120-reference-docs-creator`, `ln-130-tasks-docs-creator`, `ln-140-test-docs-creator`
- Shared docs-quality contract: `shared/references/docs_quality_contract.md`
- Shared verifier CLI: `shared/scripts/docs-quality/cli.mjs`

## Definition of Done

Before completing work, verify ALL checkpoints:

**Legacy Migration (Phase 0 - if applicable):**
- [ ] Legacy detection patterns applied (Glob + Grep)
- [ ] Legacy manifest built: { path, type, confidence, target }
- [ ] User selected migration option (MIGRATE / ARCHIVE / SKIP)
- [ ] If MIGRATE: Content extracted using type-specific extractors
- [ ] Backup created: `.archive/legacy-{timestamp}/original/`
- [ ] Extracted content saved: `.archive/legacy-{timestamp}/extracted/`
- [ ] README_migration.md generated with rollback instructions
- [ ] LEGACY_CONTENT prepared for Context Store
- [ ] Legacy files cleaned up (sections removed from README.md, standalone files deleted)

**User Confirmation (Phase 1):**
- [ ] Migration summary shown (if Phase 0 ran)
- [ ] Workflow explained to user (coordinator + 4 workers: ln-110 -> ln-120 -> ln-130 -> ln-140)
- [ ] User approved: "Proceed with complete documentation system creation? (yes/no)"
- [ ] Test docs preference captured: "Include test documentation? (yes/no)"

**Coordinator + Workers Invoked Sequentially (Phase 2):**
- [ ] ln-110-project-docs-coordinator invoked -> Output verified: Root docs (`AGENTS.md` + `CLAUDE.md` + `docs/README.md` + `docs/documentation_standards.md` + `docs/principles.md`) + Project docs (`docs/project/requirements.md`, `architecture.md`, `tech_stack.md` + conditional 3-7 files)
- [ ] ln-120-reference-docs-creator invoked -> Output verified: `docs/reference/README.md` + directories (adrs/, guides/, manuals/, research/) + justified ADRs/Guides/Manuals based on TECH_STACK
- [ ] ln-130-tasks-docs-creator invoked -> Output verified: `docs/tasks/README.md` + optionally `kanban_board.md`
- [ ] ln-140-test-docs-creator invoked (if enabled) -> Output verified: `tests/README.md`
- [ ] Each component validated its own output (SCOPE, metadata markers, top sections, Maintenance, POSIX compliance)
- [ ] Each worker returned normalized `created_files`, `skipped_files`, `quality_inputs`, and `validation_status`

**File Verification Complete:**
- [ ] All expected files exist (Glob tool used to verify structure)
- [ ] File sizes listed for user confirmation
- [ ] Warning displayed if expected files missing

**Global Cleanup Complete (Phase 3):**
- [ ] 3a: Manifest built from normalized worker outputs
- [ ] 3b: Shared verifier executed against the manifest
- [ ] 3c: Bounded repair loop completed; no HIGH/CRITICAL findings remain
- [ ] 3d: Duplicate sections identified and removed (>80% similarity)
- [ ] 3d: Links added to canonical locations (principles.md, testing-strategy.md, kanban_board.md)
- [ ] 3e: Unexpected files reported (advisory, no auto-archive)
- [ ] 3f: Scattered concepts consolidated to Single Source of Truth (SSoT)
- [ ] 3g: Internal links validated (broken links fixed, critical links added)
- [ ] 3h: Final report generated (quality gate summary, counts, lists, actions)

**Summary Displayed (Phase 4):**
- [ ] All created files listed with sizes
- [ ] Documentation system features highlighted (SCOPE, metadata markers, Quick Navigation, Agent Entry, Maintenance, README hubs, DAG structure, deduplicated content, validated links)
- [ ] Docs-quality verifier summary shown (score, repair passes, remaining LOW/MEDIUM warnings)
- [ ] Next steps recommended (ln-210-epic-coordinator)

**Error Handling (if applicable):**
- [ ] If any worker failed: User notified which worker failed, error message shown, manual invocation recommended, partial progress listed

**Output:** Complete documentation system (`AGENTS.md` + `CLAUDE.md` + docs/ with README.md, documentation_standards.md, principles.md + optionally tests/) with global cleanup (no duplicates, orphaned files reported, consolidated knowledge, validated cross-links)

---

**Version:** 8.1.0
**Last Updated:** 2025-01-12
