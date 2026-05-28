---
name: ln-100-documents-pipeline
description: Top orchestrator for complete doc system. Delegates to ln-110 coordinator (project docs via 5 L3 workers) + ln-120-150 workers. Phase 4: global cleanup. Idempotent.
---

# Documentation Pipeline (Orchestrator)

This skill orchestrates the creation of a complete documentation system by invoking L2 coordinator + 4 L2 workers. The coordinator (ln-110) delegates to 5 L3 workers for project docs; other L2 workers handle reference/tasks/test/presentation domains. Each component validates its own output.

## Architecture

```
ln-100-documents-pipeline (L1 Top Orchestrator - this skill)
├── ln-110-project-docs-coordinator (L2 Coordinator)
│   ├── ln-111-root-docs-creator (L3 Worker) → 4 docs
│   ├── ln-112-project-core-creator (L3 Worker) → 3 docs
│   ├── ln-113-backend-docs-creator (L3 Worker) → 2 conditional
│   ├── ln-114-frontend-docs-creator (L3 Worker) → 1 conditional
│   └── ln-115-devops-docs-creator (L3 Worker) → 1 conditional
├── ln-120-reference-docs-creator (L2 Worker)
├── ln-130-tasks-docs-creator (L2 Worker)
├── ln-140-test-docs-creator (L2 Worker - optional)
├── ln-150-presentation-creator (L2 Worker)
├── ln-600-docs-auditor (L2 Worker - optional)
└── ln-610-code-comments-auditor (L2 Worker - optional)
```

## When to Use This Skill

This skill should be used when:
- Start a new IT project and need complete documentation system at once
- Use automated workflow instead of manually invoking multiple workers
- Create entire documentation structure (CLAUDE.md → docs/ → presentation/) in one go
- Prefer orchestrated CREATE path over manual skill chaining
- Need automatic global cleanup (deduplication, orphaned files, consolidation)

**Alternative**: If you prefer granular control, invoke workers manually:
1. [ln-110-project-docs-coordinator](../ln-110-project-docs-coordinator/SKILL.md) - Root + Project docs (coordinates 5 L3 workers)
2. [ln-120-reference-docs-creator](../ln-120-reference-docs-creator/SKILL.md) - reference/ structure
3. [ln-130-tasks-docs-creator](../ln-130-tasks-docs-creator/SKILL.md) - tasks/README.md + kanban
4. [ln-140-test-docs-creator](../ln-140-test-docs-creator/SKILL.md) - tests/README.md (optional)
5. [ln-150-presentation-creator](../ln-150-presentation-creator/SKILL.md) - HTML presentation

**Note**: Each worker now validates its own output in Phase 2/3. Orchestrator handles global operations only.

## How It Works

The skill follows a 7-phase orchestration workflow: **Legacy Migration (optional)** → User confirmation → Invoke coordinator + 4 workers sequentially → Global cleanup → **Documentation Audit (optional)** → Summary. Phase 3 (validation) is intentionally skipped - each component validates its own output.

---

### Phase 0: Legacy Migration (OPTIONAL)

**Objective**: Detect existing documentation in non-standard formats, extract valuable content, and prepare for migration.

**Trigger**: Always runs at pipeline start. User can skip if no legacy docs or wants to keep existing structure.

**Process**:

**0.1 Legacy Detection**:
- Scan project for non-standard documentation using patterns from `references/legacy_detection_patterns.md`:
  - **Root .md files**: `ARCHITECTURE.md`, `REQUIREMENTS.md`, `STACK.md`, `API.md`, `DATABASE.md`, `DEPLOYMENT.md`
  - **Legacy folders**: `documentation/`, `doc/`, `wiki/`, `docs/` with wrong structure
  - **README.md sections**: `## Architecture`, `## Tech Stack`, `## Requirements`, etc.
  - **CONTRIBUTING.md sections**: `## Development`, `## Code Style`, `## Coding Standards`
- Build `legacy_manifest`: list of { path, detected_type, target_doc, confidence }
- If no legacy docs found → skip to Phase 1

**0.2 Content Extraction**:
- For each detected legacy file:
  - Parse markdown structure (headers, lists, code blocks)
  - Apply type-specific extractor (see `legacy_detection_patterns.md`):
    - `architecture_extractor` → { layers[], components[], diagrams[] }
    - `requirements_extractor` → { functional[], non_functional[] }
    - `tech_stack_extractor` → { frontend, backend, database, versions }
    - `principles_extractor` → { principles[], anti_patterns[] }
    - `api_spec_extractor` → { endpoints[], authentication }
    - `database_schema_extractor` → { tables[], relationships[] }
    - `runbook_extractor` → { prerequisites[], install_steps[], env_vars[] }
  - Score content quality (0.0-1.0)
- Store in `extracted_content` object

**0.3 User Confirmation**:
- Display detected legacy files:
  ```
  📂 Legacy Documentation Detected:

  | File | Type | Confidence | Target |
  |------|------|------------|--------|
  | README.md (## Architecture) | architecture | HIGH | docs/project/architecture.md |
  | docs/ARCHITECTURE.md | architecture | HIGH | docs/project/architecture.md |
  | CONTRIBUTING.md (## Development) | principles | MEDIUM | docs/principles.md |

  🔄 Migration Options:
  1. MIGRATE (recommended): Extract → Inject → Archive → Delete
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

**0.4 Backup and Archive**:
- Create `.archive/legacy-{timestamp}/` directory
- Structure:
  ```
  .archive/
  └── legacy-YYYY-MM-DD-HHMMSS/
      ├── README_migration.md        # Rollback instructions
      ├── original/                  # Exact copies of legacy files
      │   ├── README.md
      │   ├── ARCHITECTURE.md
      │   └── documentation/
      └── extracted/                 # Extracted content (for reference)
          ├── architecture_content.md
          └── principles_content.md
  ```
- Copy all legacy files to `original/`
- Save extracted content to `extracted/`
- Generate `README_migration.md` with rollback instructions

**0.5 Content Injection**:
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
      "legacy_runbook": { "install_steps": [...] }
    }
  }
  ```
- Merge into Context Store for ln-110:
  - `contextStore.LEGACY_CONTENT = migration_context`
  - Workers use LEGACY_CONTENT as base content (priority over template defaults)
- Priority order: **Legacy content > Auto-discovery > Template defaults**

**0.6 Cleanup (Legacy Files)**:
- For root-level files (README.md, CONTRIBUTING.md):
  - Do NOT delete
  - Remove migrated sections using Edit tool
  - Add links to new locations:
    - `## Architecture` → `See [Architecture](docs/project/architecture.md)`
    - `## Tech Stack` → `See [Tech Stack](docs/project/tech_stack.md)`
- For standalone legacy files (ARCHITECTURE.md, documentation/):
  - Delete files (already backed up)
  - Log: "Deleted: ARCHITECTURE.md (migrated to docs/project/architecture.md)"
- Clean empty legacy directories

**Output**: `migration_summary` { migrated_count, archived_count, skipped_count, legacy_content }

### Phase 1: User Confirmation

**Objective**: Check existing files, explain workflow, and get user approval.

**Process**:

0. **Migration Summary** (if Phase 0 ran):
   - Show: "✓ Migrated {N} legacy documents"
   - Show: "✓ Archived to .archive/legacy-{date}/"
   - Show: "✓ LEGACY_CONTENT prepared for workers"

1. **Pre-flight Check** (scan existing documentation):
   - Use Glob tool to check all potential files:
     - **Root docs** (4 files): `CLAUDE.md`, `docs/README.md`, `docs/documentation_standards.md`, `docs/principles.md`
     - **Reference structure** (5 items): `docs/reference/README.md`, `docs/reference/adrs/`, `docs/reference/guides/`, `docs/reference/manuals/`, `docs/reference/research/`
     - **Tasks docs** (2 files): `docs/tasks/README.md`, `docs/tasks/kanban_board.md`
     - **Project docs** (up to 7 files): `docs/project/requirements.md`, `architecture.md`, `tech_stack.md`, `api_spec.md`, `database_schema.md`, `design_guidelines.md`, `runbook.md`
     - **Presentation** (3 items): `docs/presentation/README.md`, `presentation_final.html`, `assets/` directory
     - **Test docs** (2 files): `docs/reference/guides/testing-strategy.md`, `tests/README.md`
   - Count existing vs missing files
   - Show user summary:
     ```
     📊 Documentation Status:
     ✓ Found: X existing files
     ✗ Missing: Y files

     ⚠️ Pipeline will create ONLY missing files.
     ✅ Existing files will be preserved (no overwrites).
     ```

2. Show user what will be created:
   - Root + Project documentation (CLAUDE.md + docs/README.md + documentation_standards.md + principles.md + docs/project/ via ln-110-project-docs-coordinator)
   - Reference structure (docs/reference/ via ln-120-reference-docs-creator)
   - Task management docs (docs/tasks/ via ln-130-tasks-docs-creator)
   - Test documentation (tests/ via ln-140-test-docs-creator - optional)
   - HTML presentation (docs/presentation/ via ln-150-presentation-creator)
   - Estimated time: 15-20 minutes with interactive dialog

3. Ask: "Proceed with creating missing files? (yes/no)"

4. Ask: "Include test documentation (tests/README.md)? (yes/no)"

**Output**: File scan summary + user approval + test docs preference

---

### Phase 2: Invoke Coordinator + Workers Sequentially

**Objective**: Create complete documentation system by invoking L2 coordinator + 4 L2 workers in order.

**Process** (AUTOMATIC invocations with Skill tool):

**2.1 Create Root + Project Documentation**:
- **Invocation**: `Skill(skill: "ln-110-project-docs-coordinator")` → AUTOMATIC
- **Input**: Pass `LEGACY_CONTENT` from Phase 0 (if migration was performed)
- **Behavior**: Coordinator gathers context ONCE, then delegates to 5 L3 workers:
  - ln-111-root-docs-creator → 4 root docs (uses LEGACY_CONTENT.legacy_principles if available)
  - ln-112-project-core-creator → 3 core docs (uses LEGACY_CONTENT.legacy_architecture, legacy_requirements, legacy_tech_stack)
  - ln-113-backend-docs-creator → 2 conditional (uses LEGACY_CONTENT.legacy_api, legacy_database)
  - ln-114-frontend-docs-creator → 1 conditional (if hasFrontend)
  - ln-115-devops-docs-creator → 1 conditional (uses LEGACY_CONTENT.legacy_runbook)
- **Output**: Root docs (`CLAUDE.md` + `docs/README.md` + `docs/documentation_standards.md` + `docs/principles.md`) + Project docs (`docs/project/requirements.md`, `architecture.md`, `tech_stack.md` + conditional: `api_spec.md`, `database_schema.md`, `design_guidelines.md`, `runbook.md`)
- **Store**: Save `context_store` from ln-110 result (contains TECH_STACK for ln-120)
- **Validation**: Each L3 worker validates output (SCOPE tags, Maintenance sections)
- **Verify**: All documents exist before continuing

**2.2 Create Reference Structure + Smart Documents**:
- **Invocation**: `Skill(skill: "ln-120-reference-docs-creator")` → AUTOMATIC
- **Input**: Pass `context_store` from ln-110 (TECH_STACK enables smart document creation)
- **Output**: `docs/reference/README.md` + `adrs/`, `guides/`, `manuals/`, `research/` directories + **justified ADRs/Guides/Manuals**
- **Smart Creation**: Creates documents only for nontrivial technology choices (see ln-120 justification rules)
- **Validation**: ln-120 validates output in Phase 2/3
- **Verify**: Reference hub exists before continuing

**2.3 Create Task Management Docs**:
- **Invocation**: `Skill(skill: "ln-130-tasks-docs-creator")` → AUTOMATIC
- **Output**: `docs/tasks/README.md` + optionally `kanban_board.md` (if user provides Linear config)
- **Validation**: ln-130 validates output in Phase 2/3
- **Verify**: Tasks README exists before continuing

**2.4 Create Test Documentation (Optional)**:
- **Condition**: If user approved test docs in Phase 1
- **Invocation**: `Skill(skill: "ln-140-test-docs-creator")` → AUTOMATIC
- **Output**: `tests/README.md` (test documentation with Story-Level Test Task Pattern)
- **Validation**: ln-140 validates output in Phase 2/3
- **Skip**: If "no" → can run ln-140-test-docs-creator later manually

**2.5 Create HTML Presentation**:
- **Invocation**: `Skill(skill: "ln-150-presentation-creator")` → AUTOMATIC
- **Output**: `docs/presentation/README.md` + `presentation_final.html` + `assets/`
- **Validation**: ln-150 validates output in Phase 2/3
- **Verify**: Presentation files exist before continuing

**Output**: Complete documentation system with coordinator + 4 workers completed and validated

**TodoWrite format (mandatory):**
Add ALL invocations to todos before starting:
```
- Invoke ln-110-project-docs-coordinator (pending)
- Invoke ln-120-reference-docs-creator (pending)
- Invoke ln-130-tasks-docs-creator (pending)
- Invoke ln-140-test-docs-creator (pending)
- Invoke ln-150-presentation-creator (pending)
- Run Global Cleanup (Phase 4) (pending)
- Run Documentation Audit (Phase 5 - optional) (pending)
```
Mark each as in_progress when starting, completed when worker returns success.

---

### Phase 4: Global Cleanup and Consolidation

**Objective**: Remove duplicates, orphaned files, consolidate knowledge across ALL documentation.

**Trigger**: Only after ALL workers complete Phase 2/3 validation.

**Process**:

**4.1 Scan for duplicate content**

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
     - "Development Principles" → principles.md (always canonical)
     - "Testing Strategy" → testing-strategy.md (always canonical)
     - "Linear Configuration" → tasks/kanban_board.md (always canonical)
     - For other duplicates: Keep in FIRST file encountered (alphabetical order)

4. **Remove duplicates:**
   - For each duplicate section:
     - Use Edit tool to delete from non-canonical files
     - Use Edit tool to add link to canonical location:
       ```markdown
       See [Development Principles](../principles.md#development-principles) for details.
       ```
   - Track count of removed duplicates

5. **Log results:**
   - "✓ Removed {count} duplicate sections"
   - List: "{section_name} removed from {file} (canonical: {canonical_file})"

**4.2 Scan for orphaned files**

1. **List all .md files in docs/**
   - Use Glob tool: `pattern: "docs/**/*.md"`

2. **Check against expected structure:**
   - Expected files (created by workers):
     - docs/CLAUDE.md
     - docs/README.md
     - docs/documentation_standards.md
     - docs/principles.md
     - docs/project/requirements.md
     - docs/project/architecture.md
     - docs/project/tech_stack.md
     - docs/project/api_spec.md (conditional)
     - docs/project/database_schema.md (conditional)
     - docs/project/design_guidelines.md (conditional)
     - docs/project/runbook.md (conditional)
     - docs/reference/README.md
     - docs/reference/adrs/*.md (user-created)
     - docs/reference/guides/*.md (user-created)
     - docs/reference/manuals/*.md (user-created)
     - docs/tasks/README.md
     - docs/tasks/kanban_board.md
     - docs/testing-strategy.md
     - tests/README.md
   - Any file NOT in this list = orphaned

3. **Move orphaned files to archive:**
   - Create `.archive/YYYY-MM-DD/` directory (current date)
   - For each orphaned file:
     - Use Bash tool: `mv {file_path} .archive/YYYY-MM-DD/`
     - Log: "Archived {file_name} (not in expected structure)"
   - Track count

4. **Log results:**
   - "✓ Archived {count} orphaned files to .archive/{date}/"
   - List archived files

**4.3 Consolidate knowledge**

1. **Identify scattered information:**
   - Known patterns:
     - Linear config scattered: kanban_board.md + tasks/README.md
     - Development principles scattered: principles.md + architecture.md + CLAUDE.md
     - Testing info scattered: testing-strategy.md + tests/README.md + architecture.md

2. **For each scattered concept:**
   - Determine Single Source of Truth (SSoT):
     - Linear config → kanban_board.md
     - Development principles → principles.md
     - Testing strategy → testing-strategy.md

3. **Update non-SSoT files:**
   - Use Edit tool to replace duplicate content with link:
     ```markdown
     See [Linear Configuration](../tasks/kanban_board.md#linear-configuration) for team ID and settings.
     ```
   - Track consolidation count

4. **Log results:**
   - "✓ Consolidated {count} scattered concepts"
   - List: "{concept} consolidated to {SSoT_file}"

**4.4 Cross-link validation**

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
   - **CLAUDE.md → docs/README.md:**
     - Read CLAUDE.md
     - Check for link to docs/README.md
     - If missing: Add in "Documentation Hub" section
   - **docs/README.md → section READMEs:**
     - Check for links to project/, reference/, tasks/, tests/ READMEs
     - If missing: Add
   - Track added links count

5. **Log results:**
   - "✓ Fixed {count} broken links"
   - "✓ Added {count} missing critical links"
   - List changes

**4.5 Final report**

```
✅ Global Cleanup Complete:

Structure:
- Removed {N} duplicate sections (canonical: principles.md)
- Archived {N} orphaned files to .archive/YYYY-MM-DD/
  - list of archived files
- Consolidated {N} scattered concepts

Links:
- Fixed {N} broken links
- Added {N} missing critical links:
  - list of added links
```

**Output**: All documentation cleaned up, duplicates removed, orphaned files archived, knowledge consolidated, cross-links validated

---

### Phase 5: Documentation Audit (OPTIONAL)

**Objective**: Audit documentation and code comments quality.

**Trigger**: Only if user requests audit OR pipeline invoked with audit flags.

**Process**:

**5.1 Ask User**:
```
📊 Documentation Audit Options:
1. AUDIT DOCS: Run ln-600-docs-auditor (6 categories)
2. AUDIT COMMENTS: Run ln-610-code-comments-auditor (6 categories)
3. BOTH: Run both auditors
4. SKIP: Continue to summary

Choose option (1/2/3/4): _
```

**5.2 Run Selected Auditors**:
- If AUDIT DOCS selected:
  - **Invocation**: `Skill(skill: "ln-600-docs-auditor")` → AUTOMATIC
  - **Output**: Compliance Score X/10 per category + Findings
- If AUDIT COMMENTS selected:
  - **Invocation**: `Skill(skill: "ln-610-code-comments-auditor")` → AUTOMATIC
  - **Output**: Compliance Score X/10 per category + Findings

**5.3 Show Audit Summary**:
```
📊 Audit Results:
- Documentation Quality: X/10 overall
  - Hierarchy & Links: X/10
  - Single Source of Truth: X/10
  - ...
- Code Comments Quality: X/10 overall
  - WHY not WHAT: X/10
  - Density (15-20%): X/10
  - ...

See full reports above for detailed findings.
```

**Output**: Audit reports with compliance scores and findings

---

### Phase 6: Summary and Next Steps

**Objective**: Provide complete overview of created system.

**Process**:
1. List all created files with sizes:
   - `CLAUDE.md` (project entry point)
   - `docs/README.md` (root documentation hub)
   - `docs/documentation_standards.md` (60 universal requirements)
   - `docs/principles.md` (11 development principles)
   - `docs/project/requirements.md`, `architecture.md`, `tech_stack.md` + conditional documents (3-7 total)
   - `docs/reference/README.md` (reference hub with empty adrs/, guides/, manuals/, research/ directories)
   - `docs/tasks/README.md` + optionally `kanban_board.md`
   - `docs/presentation/README.md` + `presentation_final.html`
   - `tests/README.md` (if created)

2. Show documentation system features:
   - ✅ SCOPE tags (document boundaries defined)
   - ✅ Maintenance sections (update triggers + verification)
   - ✅ README hub (central navigation)
   - ✅ DAG structure (Directed Acyclic Graph navigation)
   - ✅ Living documentation ready
   - ✅ Deduplicated content (canonical sources only)
   - ✅ Validated cross-links (no broken links)

3. Recommend next steps:
   - "Review generated documentation (CLAUDE.md → docs/)"
   - "Open docs/presentation/presentation_final.html in browser"
   - "Run ln-210-epic-coordinator to decompose scope into Epics"
   - "Share documentation with technical stakeholders"

**Output**: Summary message with file list and recommendations

---

## Complete Output Structure

```
project_root/
├── CLAUDE.md                         # ← Project entry point (link to docs/)
├── docs/
│   ├── README.md                     # ← Root documentation hub (general standards)
│   ├── documentation_standards.md    # ← 60 universal requirements (Claude Code + industry standards)
│   ├── principles.md                 # ← 11 development principles (Standards First, YAGNI, KISS, DRY, etc.)
│   ├── project/
│   │   ├── requirements.md           # ← Functional Requirements (NO NFR per project policy)
│   │   ├── architecture.md           # ← arc42-based architecture with C4 Model
│   │   ├── tech_stack.md             # ← Technology versions, Docker config
│   │   ├── api_spec.md               # ← API endpoints (conditional)
│   │   ├── database_schema.md        # ← Database schema (conditional)
│   │   ├── design_guidelines.md      # ← UI/UX system (conditional)
│   │   └── runbook.md                # ← Operations guide (conditional)
│   ├── reference/
│   │   ├── README.md                 # ← Reference documentation hub (registries)
│   │   ├── adrs/                     # ← Empty, ready for ADRs
│   │   ├── guides/                   # ← Empty, ready for guides
│   │   ├── manuals/                  # ← Empty, ready for manuals
│   │   └── research/                 # ← Empty, ready for research
│   ├── tasks/
│   │   ├── README.md                 # ← Task management system rules
│   │   └── kanban_board.md           # ← Linear integration (optional)
│   └── presentation/
│       ├── README.md                 # ← Navigation hub for presentation
│       ├── presentation_final.html   # ← Final standalone HTML (~130-180 KB)
│       └── assets/                   # ← Modular HTML structure
└── tests/
    └── README.md                     # ← Test documentation (optional)
```

---

## Integration with Project Workflow

**Recommended workflow for new projects:**

1. **ln-100-documents-pipeline** (this skill) - Create complete documentation system
2. **ln-210-epic-coordinator** - Decompose scope into Epics (Linear Projects)
3. **ln-220-story-coordinator** - Create User Stories for each Epic (automatic decomposition + replan)
4. **ln-300-task-coordinator** - Break down Stories into implementation tasks (automatic decomposition + replan)
5. **ln-310-story-validator** - Verify Stories before development
6. **ln-400-story-executor** - Orchestrate Story implementation
7. **ln-500-story-quality-gate** - Review completed Stories

---

## Advantages of Orchestrator Approach

**Benefits:**
- ✅ Single command creates complete system
- ✅ No need to remember skill sequence
- ✅ Automated skill chaining
- ✅ Consistent output every time
- ✅ Time-saving (one invocation vs 2-3 manual invocations)
- ✅ **Idempotent**: Safe to run multiple times - preserves existing files, creates only missing ones
- ✅ **Pre-flight check**: Shows file scan summary before execution
- ✅ **Global cleanup**: Automatic deduplication, orphaned files archival, knowledge consolidation
- ✅ **Validated cross-links**: No broken links in documentation

**Trade-offs:**
- ⚠️ Less granular control (can't skip coordinator phases)
- ⚠️ Longer execution time (15-20 minutes)
- ⚠️ Global cleanup runs even if only one file was created

**When to use manual approach instead:**
- Need only HTML rebuild → use [ln-150-presentation-creator](../ln-150-presentation-creator/SKILL.md)
- Need one specific ADR/guide/manual → use [ln-002-best-practices-researcher](../ln-002-best-practices-researcher/SKILL.md)

---

## Documentation Standards

All documents created by this pipeline MUST follow these rules:

| Rule | Description | Enforcement |
|------|-------------|-------------|
| **NO_CODE Rule** | Documents describe contracts, not implementations | No code blocks >5 lines; use tables/ASCII/links |
| **Stack Adaptation** | Links must match project TECH_STACK | .NET → Microsoft docs, JS → MDN |
| **Format Priority** | Tables/ASCII > Lists (enumerations only) > Text | Tables for params, config, alternatives |

These standards are enforced by L3 workers (ln-111-115) and audited by ln-600-docs-auditor.

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
- Uses **Bash** tool to archive orphaned files

**Standards Compliance:**
- All output follows same standards as underlying skills
- ISO/IEC/IEEE 29148:2018 (Requirements)
- ISO/IEC/IEEE 42010:2022 (Architecture)
- arc42 + C4 Model + Michael Nygard's ADR Format

---

## Definition of Done

Before completing work, verify ALL checkpoints:

**✅ Legacy Migration (Phase 0 - if applicable):**
- [ ] Legacy detection patterns applied (Glob + Grep)
- [ ] Legacy manifest built: { path, type, confidence, target }
- [ ] User selected migration option (MIGRATE / ARCHIVE / SKIP)
- [ ] If MIGRATE: Content extracted using type-specific extractors
- [ ] Backup created: `.archive/legacy-{timestamp}/original/`
- [ ] Extracted content saved: `.archive/legacy-{timestamp}/extracted/`
- [ ] README_migration.md generated with rollback instructions
- [ ] LEGACY_CONTENT prepared for Context Store
- [ ] Legacy files cleaned up (sections removed from README.md, standalone files deleted)

**✅ User Confirmation (Phase 1):**
- [ ] Migration summary shown (if Phase 0 ran)
- [ ] Workflow explained to user (coordinator + 4 workers: ln-110 → ln-120 → ln-130 → ln-140 → ln-150)
- [ ] User approved: "Proceed with complete documentation system creation? (yes/no)"
- [ ] Test docs preference captured: "Include test documentation? (yes/no)"

**✅ Coordinator + Workers Invoked Sequentially (Phase 2):**
- [ ] ln-110-project-docs-coordinator invoked → Output verified: Root docs (`CLAUDE.md` + `docs/README.md` + `docs/documentation_standards.md` + `docs/principles.md`) + Project docs (`docs/project/requirements.md`, `architecture.md`, `tech_stack.md` + conditional 3-7 files)
- [ ] ln-120-reference-docs-creator invoked → Output verified: `docs/reference/README.md` + directories (adrs/, guides/, manuals/, research/) + justified ADRs/Guides/Manuals based on TECH_STACK
- [ ] ln-130-tasks-docs-creator invoked → Output verified: `docs/tasks/README.md` + optionally `kanban_board.md`
- [ ] ln-140-test-docs-creator invoked (if enabled) → Output verified: `tests/README.md`
- [ ] ln-150-presentation-creator invoked → Output verified: `docs/presentation/README.md` + `presentation_final.html` + `assets/`
- [ ] Each component validated its own output (SCOPE tags, Maintenance sections, POSIX compliance)

**✅ File Verification Complete:**
- [ ] All expected files exist (Glob tool used to verify structure)
- [ ] File sizes listed for user confirmation
- [ ] Warning displayed if expected files missing

**✅ Global Cleanup Complete (Phase 4):**
- [ ] 4.1: Duplicate sections identified and removed (>80% similarity)
- [ ] 4.1: Links added to canonical locations (principles.md, testing-strategy.md, kanban_board.md)
- [ ] 4.2: Orphaned files archived to `.archive/YYYY-MM-DD/`
- [ ] 4.3: Scattered concepts consolidated to Single Source of Truth (SSoT)
- [ ] 4.4: Internal links validated (broken links fixed, critical links added)
- [ ] 4.5: Final report generated (counts, lists, actions)

**✅ Documentation Audit (Phase 5 - if selected):**
- [ ] User selected audit option (AUDIT DOCS / AUDIT COMMENTS / BOTH / SKIP)
- [ ] If AUDIT DOCS: ln-600-docs-auditor invoked, compliance score displayed
- [ ] If AUDIT COMMENTS: ln-610-code-comments-auditor invoked, compliance score displayed
- [ ] Audit summary shown with scores per category

**✅ Summary Displayed (Phase 6):**
- [ ] All created files listed with sizes
- [ ] Documentation system features highlighted (SCOPE tags, Maintenance sections, README hubs, DAG structure, deduplicated content, validated links)
- [ ] Next steps recommended (ln-210-epic-coordinator)

**✅ Error Handling (if applicable):**
- [ ] If any worker failed: User notified which worker failed, error message shown, manual invocation recommended, partial progress listed

**Output:** Complete documentation system (CLAUDE.md + docs/ with README.md, documentation_standards.md, principles.md + presentation/ + optionally tests/) with global cleanup (no duplicates, no orphaned files, consolidated knowledge, validated cross-links)

---

**Version:** 8.1.0 (Added Documentation Standards section with NO_CODE, Stack Adaptation, Format Priority rules)
**Last Updated:** 2025-01-12
