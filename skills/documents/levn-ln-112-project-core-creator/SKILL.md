---
name: ln-112-project-core-creator
description: Creates 3 core project docs (requirements.md, architecture.md, tech_stack.md). L3 Worker invoked by ln-110-project-docs-coordinator. ALWAYS created.
---

# Project Core Documentation Creator

L3 Worker that creates 3 core project documentation files. These are ALWAYS created regardless of project type.

## Purpose & Scope
- Creates 3 core project documentation files (required for all projects)
- Receives Context Store from ln-110-project-docs-coordinator
- Heavy use of auto-discovery (architecture needs full project scan)
- Replaces placeholders with project-specific data
- Self-validates structure and content (16 questions)
- Never gathers context itself; uses coordinator input

## Invocation (who/when)
- **ln-110-project-docs-coordinator:** ALWAYS invoked as second worker (after ln-111)
- Never called directly by users

## Inputs
From coordinator:
- `contextStore`: Full Context Store with all discovered data
  - PROJECT_NAME, PROJECT_DESCRIPTION
  - TECH_STACK (full object: frontend, backend, database, etc.)
  - DEPENDENCIES (from package.json)
  - SRC_STRUCTURE (folder analysis)
  - EXTERNAL_SYSTEMS (from .env.example)
  - CODE_CONVENTIONS (from eslint, prettier)
  - ADR_LIST (from docs/reference/adrs/)
  - **LEGACY_CONTENT** (optional, from ln-100 Phase 0 migration):
    - `legacy_architecture`: { layers[], components[], diagrams[], data_flow }
    - `legacy_requirements`: { functional[], non_functional[], user_stories[] }
    - `legacy_tech_stack`: { frontend, backend, database, versions }
- `targetDir`: Project root directory

**LEGACY_CONTENT** is used as base content when creating documents. Priority: **Legacy > Auto-discovery > Template defaults**.

## Documents Created (3)

| File | Target Sections | Questions | Auto-Discovery |
|------|-----------------|-----------|----------------|
| docs/project/requirements.md | Functional Requirements (FR-XXX-NNN format) | Q23 | Low |
| docs/project/architecture.md | 11 arc42 sections with C4 diagrams | Q24-Q34 | High |
| docs/project/tech_stack.md | Frontend, Backend, Database, Additional | Q35-Q38 | High |

## Workflow

### Phase 1: Receive Context
1. Parse full Context Store from coordinator
2. Validate required keys (PROJECT_NAME, TECH_STACK)
3. Extract architecture-specific data (SRC_STRUCTURE, DEPENDENCIES)

### Phase 2: Create Documents
For each document (requirements.md, architecture.md, tech_stack.md):
1. Check if file exists (idempotent)
2. If exists: skip with log
3. If not exists:
   - Copy template from `references/templates/`
   - **Check LEGACY_CONTENT for this document type:**
     - For `architecture.md`: If `LEGACY_CONTENT.legacy_architecture` exists:
       - Use `legacy_architecture.layers[]` for "## Building Block View" (Section 5)
       - Use `legacy_architecture.components[]` for component descriptions
       - Use `legacy_architecture.diagrams[]` for existing diagrams (preserve mermaid/images)
       - Use `legacy_architecture.data_flow` for "## Runtime View" (Section 6)
       - Merge with auto-discovered SRC_STRUCTURE (legacy takes priority)
       - Mark: `<!-- Migrated from legacy documentation -->` at top of merged sections
     - For `requirements.md`: If `LEGACY_CONTENT.legacy_requirements` exists:
       - Use `legacy_requirements.functional[]` as base for FR-XXX requirements
       - Use `legacy_requirements.user_stories[]` if FR format not found
       - Augment with template structure (add MoSCoW labels if missing)
     - For `tech_stack.md`: If `LEGACY_CONTENT.legacy_tech_stack` exists:
       - Use `legacy_tech_stack.versions` as base for technology versions
       - Merge with auto-discovered TECH_STACK (legacy versions take priority)
       - Use `legacy_tech_stack.rationale` for decision explanations
   - Replace `{{PLACEHOLDER}}` with Context Store values
   - Generate C4 diagrams from SRC_STRUCTURE (for architecture.md, if no legacy diagrams)
   - Insert ADR links (for architecture.md Section 8)
   - Mark `[TBD: X]` for missing data

### Phase 3: Self-Validate
For each created document:
1. Check SCOPE tag in first 10 lines
2. Check required sections (from questions_core.md)
3. Validate specific format requirements:
   - requirements.md: FR-XXX identifiers, MoSCoW labels
   - architecture.md: 11 sections, C4 diagrams, ADR references
   - tech_stack.md: versions, rationale for each technology
4. Check Maintenance section
5. Auto-fix issues where possible

### Phase 4: Return Status
Return to coordinator:
```json
{
  "created": ["docs/project/requirements.md", ...],
  "skipped": [],
  "tbd_count": 5,
  "validation": "OK",
  "diagrams_generated": 3
}
```

## Critical Notes
- **Idempotent:** Never overwrite existing files
- **Heavy auto-discovery:** architecture.md requires deep project analysis
- **C4 diagrams:** Generated from SRC_STRUCTURE in Mermaid format
- **ADR integration:** Section 8 links to docs/reference/adrs/
- **arc42 compliance:** ISO/IEC/IEEE 42010:2022 structure
- **TBD markers:** Use `[TBD: X]` for missing data

### NO_CODE_EXAMPLES Rule (MANDATORY)
Documents describe **contracts and decisions**, NOT implementations:
- **FORBIDDEN:** Code blocks > 5 lines, function implementations, imports, DI configuration
- **ALLOWED:** Mermaid diagrams, component tables, method signatures (1 line), ADR links
- **INSTEAD OF CODE:** Reference source: "See src/Services/UserService.cs:45"
- **TEMPLATE RULE:** All templates include `<!-- NO_CODE_EXAMPLES: ... -->` tag - FOLLOW IT

### Stack Adaptation Rule (MANDATORY)
- Links must reference stack-appropriate docs (Microsoft for .NET, MDN for JS)
- Never mix stack references (no Python examples in .NET project)

### Format Priority (MANDATORY)
Tables > Mermaid/ASCII diagrams > Lists > Text

## Definition of Done
- Context Store received and validated
- 3 core documents created (or skipped if exist)
- C4 diagrams generated (Context, Container, Component)
- ADR links populated
- Self-validation passed (SCOPE, sections, format)
- Status returned to coordinator

## Reference Files
- Templates: `references/templates/requirements_template.md`, `architecture_template.md`, `tech_stack_template.md`
- Questions: `references/questions_core.md` (Q23-Q38)

---
**Version:** 2.2.0 (Added Stack Adaptation and Format Priority rules)
**Last Updated:** 2025-01-12
