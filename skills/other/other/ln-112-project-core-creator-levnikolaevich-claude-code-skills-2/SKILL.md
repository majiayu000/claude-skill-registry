---
name: ln-112-project-core-creator
description: "Creates core project docs (requirements, architecture, tech stack, patterns catalog). Use for any project regardless of type."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Project Core Documentation Creator

**Type:** L3 Worker

L3 Worker that creates 4 core project documentation files. These are ALWAYS created regardless of project type.

## Purpose & Scope
- Creates 4 core project documentation files (required for all projects)
- Receives Context Store from ln-110-project-docs-coordinator
- Heavy use of auto-discovery (architecture needs full project scan)
- Replaces placeholders with project-specific data
- Self-validates structure and content (16+ questions)
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

**MANDATORY READ:** Load `shared/references/docs_quality_contract.md`, `shared/references/docs_quality_rules.json`, and `shared/references/markdown_read_protocol.md`.

## Documents Created (4)

| File | Target Sections | Questions | Auto-Discovery |
|------|-----------------|-----------|----------------|
| docs/project/requirements.md | Functional Requirements (FR-XXX-NNN format) | Q23 | Low |
| docs/project/architecture.md | 11 arc42 sections with C4 diagrams | Q24-Q34 | High |
| docs/project/tech_stack.md | Frontend, Backend, Database, Additional | Q35-Q38 | High |
| docs/architecture/patterns_catalog.md | Pattern summary, 4-score model, trend tracking | — | High |

## Workflow

### Phase 1: Receive Context
1. Parse full Context Store from coordinator
2. Validate required keys (PROJECT_NAME, TECH_STACK)
3. Extract architecture-specific data (SRC_STRUCTURE, DEPENDENCIES)

### Phase 2: Create Documents
For each document (requirements.md, architecture.md, tech_stack.md, patterns_catalog.md):
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
     - For `patterns_catalog.md`:
       - Copy template from `shared/templates/patterns_template.md`
       - **Auto-detect patterns in codebase:**
         - Grep("Queue|Worker|Job|Bull") → Job Processing
         - Grep("EventEmitter|publish|subscribe") → Event-Driven
         - Grep("Cache|Redis|Memcached") → Caching
         - Grep("CircuitBreaker|Retry") → Resilience
       - Add detected patterns as "Status: Detected" (not yet audited)
       - Link to existing ADRs if pattern names match
       - Mark: `<!-- Auto-detected by ln-112, audit with ln-640 -->`
   - Replace `{{PLACEHOLDER}}` with Context Store values
   - Preserve the shared opening contract: `SCOPE`, `DOC_KIND`, `DOC_ROLE`, `READ_WHEN`, `SKIP_WHEN`, `PRIMARY_SOURCES`
   - Preserve the standard top sections: `Quick Navigation`, `Agent Entry`, `Maintenance`
   - Generate C4 diagrams from SRC_STRUCTURE (for architecture.md, if no legacy diagrams)
   - Insert ADR links (for architecture.md Section 8)
   - Never leave template markers in published project docs
   - If data is missing: omit the claim or use a concise neutral fallback, but do NOT emit `[TBD: ...]`

### Phase 3: Self-Validate
For each created document:
1. Check SCOPE tag and metadata markers in the opening block
2. Check required top sections (`Quick Navigation`, `Agent Entry`, `Maintenance`)
3. Check required sections (from questions_core.md)
4. Validate specific format requirements:
   - requirements.md: FR-XXX identifiers, MoSCoW labels
   - architecture.md: 11 sections, C4 diagrams, ADR references
   - tech_stack.md: versions, rationale for each technology
5. Check docs-quality contract compliance (no forbidden placeholders, no leaked template metadata, valid doc kind/role)
6. Auto-fix issues where possible

### Phase 4: Return Status
Return to coordinator:
```json
{
  "created_files": ["docs/project/requirements.md", "docs/project/architecture.md", "docs/project/tech_stack.md", "docs/architecture/patterns_catalog.md"],
  "skipped_files": [],
  "quality_inputs": {
    "doc_paths": ["docs/project/requirements.md", "docs/project/architecture.md", "docs/project/tech_stack.md", "docs/architecture/patterns_catalog.md"],
    "owners": {
      "docs/project/requirements.md": "ln-112-project-core-creator",
      "docs/project/architecture.md": "ln-112-project-core-creator",
      "docs/project/tech_stack.md": "ln-112-project-core-creator",
      "docs/architecture/patterns_catalog.md": "ln-112-project-core-creator"
    }
  },
  "validation_status": "passed",
  "diagrams_generated": 3
}
```

## Critical Notes
- **Idempotent:** Never overwrite existing files
- **Heavy auto-discovery:** architecture.md requires deep project analysis
- **C4 diagrams:** Generated from SRC_STRUCTURE in Mermaid format
- **ADR integration:** Section 8 links to docs/reference/adrs/
- **arc42 compliance:** ISO/IEC/IEEE 42010:2022 structure
- **Publishable output:** Core project docs must not contain `[TBD: ...]`, `TODO`, or leaked template metadata

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

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/docs_generation_summary_contract.md`

Accept optional `summaryArtifactPath`.

Summary kind:
- `docs-generation`

Required payload semantics:
- `worker = "ln-112"`
- `status`
- `created_files`
- `skipped_files`
- `quality_inputs`
- `validation_status`
- `warnings`

Write the summary to the provided artifact path or return the same envelope in structured output.

## Definition of Done
- [ ] Context Store received and validated
- [ ] 4 core documents created (or skipped if exist)
- [ ] C4 diagrams generated (Context, Container, Component)
- [ ] ADR links populated
- [ ] Patterns auto-detected and added to catalog
- [ ] Self-validation passed (metadata markers, top sections, format)
- [ ] **Actuality verified:** all document facts match current code (paths, functions, APIs, configs exist and are accurate)
- [ ] Status returned

## Reference Files
- Templates: `references/templates/requirements_template.md`, `architecture_template.md`, `tech_stack_template.md`
- Patterns template: `shared/templates/patterns_template.md`
- Questions: `references/questions_core.md` (Q23-Q38)

---
**Version:** 2.2.0
**Last Updated:** 2025-01-12
