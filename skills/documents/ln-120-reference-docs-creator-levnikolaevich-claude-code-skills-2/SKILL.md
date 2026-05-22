---
name: ln-120-reference-docs-creator
description: Creates reference documentation structure + smart documents (ADRs/Guides/Manuals) based on TECH_STACK. Only creates justified documents (nontrivial technology choices). L2 Worker in ln-100-documents-pipeline.
---

# Reference Documentation Creator

This skill creates the reference documentation structure (docs/reference/) and **smart documents** (ADRs, Guides, Manuals) based on project's TECH_STACK. Documents are created only when justified (nontrivial technology choices with alternatives).

## When to Use This Skill

**This skill is a L2 WORKER** invoked by **ln-100-documents-pipeline** orchestrator.

This skill should be used directly when:
- Creating only reference documentation structure (docs/reference/)
- Setting up directories for ADRs, guides, and manuals
- NOT creating full documentation structure (use ln-100-documents-pipeline for complete setup)

## Inputs

**From ln-100 (via ln-110 Context Store):**
```json
{
  "context_store": {
    "PROJECT_NAME": "my-project",
    "TECH_STACK": {
      "frontend": "React 18",
      "backend": "Express 4.18",
      "database": "PostgreSQL 15",
      "orm": "Prisma 5.0",
      "auth": "JWT",
      "cache": "Redis 7"
    },
    "DEPENDENCIES": [...],
    "flags": { "hasBackend": true, "hasDatabase": true, "hasFrontend": true }
  }
}
```

**TECH_STACK** is used for smart document creation in Phase 2.

## How It Works

The skill follows a 4-phase workflow: **CREATE STRUCTURE** → **SMART DOCUMENT CREATION** → **VALIDATE STRUCTURE** → **VALIDATE CONTENT**. Phase 2 creates documents only for justified technology choices.

---

### Phase 1: Create Structure

**Objective**: Establish reference documentation directories and README hub.

**Process**:

**1.1 Check & create directories**:
- Check if `docs/reference/adrs/` exists → create if missing
- Check if `docs/reference/guides/` exists → create if missing
- Check if `docs/reference/manuals/` exists → create if missing
- Check if `docs/reference/research/` exists → create if missing
- Log for each: "✓ Created docs/reference/[name]/" or "✓ docs/reference/[name]/ already exists"

**1.2 Check & create README**:
- Check if `docs/reference/README.md` exists
- If exists:
  - Skip creation
  - Log: "✓ docs/reference/README.md already exists, proceeding to validation"
- If NOT exists:
  - Copy template: `ln-112-reference-docs-creator/references/reference_readme_template.md` → `docs/reference/README.md`
  - Replace placeholders:
    - `{{VERSION}}` — "1.0.0"
    - `{{DATE}}` — current date (YYYY-MM-DD)
    - `{{ADR_LIST}}` — kept as placeholder (filled in Phase 4)
    - `{{GUIDE_LIST}}` — kept as placeholder (filled in Phase 4)
    - `{{MANUAL_LIST}}` — kept as placeholder (filled in Phase 4)
  - Log: "✓ Created docs/reference/README.md from template"

**1.3 Output**:
```
docs/reference/
├── README.md         # Created or existing
├── adrs/            # Empty, ready for ADRs
├── guides/          # Empty, ready for guides
├── manuals/         # Empty, ready for manuals
└── research/        # Empty, ready for research documents
```

---

### Phase 2: Smart Document Creation

**Objective**: Create ADRs, Guides, and Manuals for justified technology choices. Skip trivial/obvious selections.

**2.1 Check Context Store**:
- If no `context_store` provided → skip Phase 2, proceed to Phase 3
- If no `TECH_STACK` in context_store → skip Phase 2, proceed to Phase 3
- Log: "Context Store received with TECH_STACK: [categories count]"

**2.2 Load Justification Rules**:
- Read `references/tech_justification_rules.md`
- Parse category → justified/skip conditions

**2.3 Analyze TECH_STACK for ADRs**:

For each category in TECH_STACK (frontend, backend, database, orm, auth, cache):

1. **Check if justified** (from justification rules):
   - `frontend`: Justified if React/Vue/Angular/Svelte (multiple options exist)
   - `backend`: Justified if Express/Fastify/NestJS/Koa (multiple options exist)
   - `database`: Justified if PostgreSQL/MySQL/MongoDB (multiple options exist)
   - `auth`: Justified if JWT/OAuth/Session (decision required)
   - `orm`: Justified if Prisma/TypeORM/Sequelize (multiple options exist)
   - `cache`: Justified if Redis/Memcached (decision required)

2. **Skip if trivial**:
   - jQuery-only frontend (no framework choice)
   - Simple http server (no framework)
   - SQLite for dev only
   - No auth required
   - Raw SQL only
   - In-memory cache only

3. **Create ADR if justified**:
   - Determine next ADR number: `adr-NNN-{category}.md`
   - Use template: `shared/templates/adr_template.md`
   - MCP Research: `mcp__context7__resolve-library-id(technology)`
   - Fill template:
     - Title: "ADR-NNN: {Category} Selection"
     - Context: Why decision was needed
     - Decision: Technology chosen with version
     - Rationale: 3 key reasons from research
     - Alternatives: 2 other options with pros/cons
   - Save: `docs/reference/adrs/adr-NNN-{category}.md`
   - Log: "✓ Created ADR for {category}: {technology}"

4. **Skip if not justified**:
   - Log: "⊘ Skipped ADR for {category}: trivial choice"

**2.4 Analyze TECH_STACK for Guides**:

For each technology with complex configuration:

1. **Check if justified**:
   - Has config file with >20 lines
   - Uses custom hooks/middleware/decorators
   - Has 3+ related dependencies

2. **Create Guide if justified**:
   - Determine next guide number: `NN-{technology-slug}-patterns.md`
   - Use template: `shared/templates/guide_template.md`
   - MCP Research: `mcp__Ref__ref_search_documentation("{technology} patterns 2025")`
   - Fill template:
     - Principle: Industry standard from research
     - Our Implementation: How project uses it
     - Patterns table: 3 Do/Don't/When rows
   - Save: `docs/reference/guides/NN-{technology}-patterns.md`
   - Log: "✓ Created Guide for {technology}"

3. **Skip if standard usage**:
   - Log: "⊘ Skipped Guide for {technology}: standard usage"

**2.5 Analyze TECH_STACK for Manuals**:

For each package with complex API:

1. **Check if justified**:
   - Package has >10 exported methods
   - Has breaking changes in current version
   - NOT in trivial list: lodash, uuid, dotenv

2. **Create Manual if justified**:
   - Use template: `shared/templates/manual_template.md`
   - MCP Research: `mcp__context7__get-library-docs(topic: "API")`
   - Fill template:
     - Package info with version
     - 2-3 most used methods
     - Configuration section
   - Save: `docs/reference/manuals/{package}-{version}.md`
   - Log: "✓ Created Manual for {package}"

3. **Skip if trivial API**:
   - Log: "⊘ Skipped Manual for {package}: trivial API"

**2.6 Report Smart Creation**:
```
✅ Smart Document Creation complete:
  - ADRs created: [count] (justified: frontend, backend, database)
  - ADRs skipped: [count] (trivial: cache=in-memory)
  - Guides created: [count]
  - Guides skipped: [count]
  - Manuals created: [count]
  - Manuals skipped: [count]
```

---

### Phase 3: Validate Structure

**Objective**: Ensure reference/README.md complies with structural requirements and auto-fix violations.

**Process**:

**2.1 Check SCOPE tag**:
- Read `docs/reference/README.md` (first 5 lines)
- Check for `<!-- SCOPE: ... -->` tag
- Expected: `<!-- SCOPE: Reference documentation hub (ADRs, Guides, Manuals) with links to subdirectories -->`
- If missing:
  - Use Edit tool to add SCOPE tag at line 1 (after first heading)
  - Track violation: `scope_tag_added = True`

**2.2 Check required sections**:
- Load expected sections from `references/questions.md`
- Required sections:
  - "Architecture Decision Records (ADRs)"
  - "Project Guides"
  - "Package Manuals"
  - "Research"
- For each section:
  - Check if `## [Section Name]` header exists
  - If missing:
    - Use Edit tool to add section with placeholder:
      ```markdown
      ## [Section Name]

      {{PLACEHOLDER}}
      ```
    - Track violation: `missing_sections += 1`

**2.3 Check Maintenance section**:
- Search for `## Maintenance` header
- If missing:
  - Use Edit tool to add at end of file:
    ```markdown
    ## Maintenance

    **Last Updated:** [current date]

    **Update Triggers:**
    - New ADRs added to adrs/ directory
    - New guides added to guides/ directory
    - New manuals added to manuals/ directory

    **Verification:**
    - [ ] All ADR links in registry are valid
    - [ ] All guide links in registry are valid
    - [ ] All manual links in registry are valid
    - [ ] Placeholders {{ADR_LIST}}, {{GUIDE_LIST}}, {{MANUAL_LIST}} synced with files
    ```
  - Track violation: `maintenance_added = True`

**2.4 Check POSIX file endings**:
- Check if file ends with single blank line
- If missing:
  - Use Edit tool to add final newline
  - Track fix: `posix_fixed = True`

**2.5 Report validation**:
- Log summary:
  ```
  ✅ Structure validation complete:
    - SCOPE tag: [added/present]
    - Missing sections: [count] sections added
    - Maintenance section: [added/present]
    - POSIX endings: [fixed/compliant]
  ```
- If violations found: "⚠️ Auto-fixed [total] structural violations"

---

### Phase 4: Validate Content

**Objective**: Ensure each section answers its questions with meaningful content and populate registries from auto-discovery (including documents created in Phase 2).

**Process**:

**4.1 Load validation spec**:
- Read `references/questions.md`
- Parse questions and validation heuristics for all 3 sections

**4.2 Validate sections (parametric loop)**:

Define section parameters:
```
sections = [
  {
    "name": "Architecture Decision Records (ADRs)",
    "question": "Where are architecture decisions documented?",
    "directory": "docs/reference/adrs/",
    "placeholder": "{{ADR_LIST}}",
    "glob_pattern": "docs/reference/adrs/*.md",
    "heuristics": [
      "Contains link: [ADRs](adrs/) or [adrs](adrs/)",
      "Mentions 'Architecture Decision Record' or 'ADR'",
      "Has placeholder {{ADR_LIST}} or actual list",
      "Length > 30 words"
    ]
  },
  {
    "name": "Project Guides",
    "question": "Where are reusable project patterns documented?",
    "directory": "docs/reference/guides/",
    "placeholder": "{{GUIDE_LIST}}",
    "glob_pattern": "docs/reference/guides/*.md",
    "heuristics": [
      "Contains link: [Guides](guides/) or [guides](guides/)",
      "Has placeholder {{GUIDE_LIST}} or actual list",
      "Length > 20 words"
    ]
  },
  {
    "name": "Package Manuals",
    "question": "Where are third-party package references documented?",
    "directory": "docs/reference/manuals/",
    "placeholder": "{{MANUAL_LIST}}",
    "glob_pattern": "docs/reference/manuals/*.md",
    "heuristics": [
      "Contains link: [Manuals](manuals/) or [manuals](manuals/)",
      "Has placeholder {{MANUAL_LIST}} or actual list",
      "Length > 20 words"
    ]
  },
  {
    "name": "Research",
    "question": "Where are research/investigation documents stored?",
    "directory": "docs/reference/research/",
    "placeholder": "{{RESEARCH_LIST}}",
    "glob_pattern": "docs/reference/research/*.md",
    "heuristics": [
      "Contains link: [Research](research/) or [research](research/)",
      "Has placeholder {{RESEARCH_LIST}} or actual list",
      "Length > 20 words"
    ]
  }
]
```

For each section in sections:

1. **Read section content**:
   - Extract section from reference/README.md

2. **Check if content answers question**:
   - Apply validation heuristics
   - If ANY heuristic passes → content valid, skip to next section
   - If ALL fail → content invalid, continue

3. **Auto-discovery** (if content invalid or placeholder present):
   - Scan directory using Glob tool (section.glob_pattern)
   - If files found:
     - Extract filenames
     - Generate dynamic list:
       ```markdown
       - [ADR-001: Frontend Framework](adrs/adr-001-frontend-framework.md)
       - [02-Repository Pattern](guides/02-repository-pattern.md)
       - [Axios 1.6](manuals/axios-1.6.md)
       ```
     - Use Edit tool to replace placeholder with generated list
     - Track change: `sections_populated += 1`
   - If NO files:
     - Keep placeholder as-is
     - Track: `placeholders_kept += 1`

4. **Skip external API calls**:
   - Do NOT use MCP Ref search (template already has format examples)

**4.3 Report content validation**:
- Log summary:
  ```
  ✅ Content validation complete:
    - Sections checked: 4
    - Populated from auto-discovery: [count]
    - Placeholders kept (no files): [count]
    - Already valid: [count]
  ```

---

## Complete Output Structure

```
docs/
└── reference/
    ├── README.md                     # Reference hub with registries
    ├── adrs/                         # Empty or with ADR files
    ├── guides/                       # Empty or with guide files
    ├── manuals/                      # Empty or with manual files
    └── research/                     # Empty or with research files
```

---

## Reference Files Used

### Templates

**Reference README Template**:
- `references/reference_readme_template.md` (v2.0.0) - Reference hub with:
  - SCOPE tags (reference documentation ONLY)
  - Three registry sections with placeholders
  - Maintenance section

**Document Templates** (for Phase 2 Smart Creation):
- `shared/templates/adr_template.md` - Nygard ADR format (7 sections)
- `shared/templates/guide_template.md` - Pattern documentation (Do/Don't/When)
- `shared/templates/manual_template.md` - API reference format
- `shared/templates/research_template.md` - Research/Spike documentation

**Justification Rules**:
- `references/tech_justification_rules.md` - Mapping: category → create/skip conditions

**Validation Specification**:
- `references/questions.md` (v2.0) - Question-driven validation:
  - Q1-Q3: Registry sections (ADRs, Guides, Manuals)
  - Q4-Q7: Smart document validation (ADR context, alternatives, patterns)
  - Auto-discovery hints

---

## Best Practices

- **No premature validation**: Phase 1 creates structure, Phase 3 validates it
- **Smart creation**: Phase 2 creates documents only for justified choices
- **Parametric validation**: Phase 4 uses loop for 3 sections (no code duplication)
- **Auto-discovery first**: Scan actual files before external API calls
- **Idempotent**: ✅ Can run multiple times safely (checks existence before creation)
- **Separation of concerns**: CREATE → SMART DOCS → VALIDATE STRUCTURE → VALIDATE CONTENT

### NO_CODE_EXAMPLES Rule (MANDATORY for Guides)
Guides document **patterns**, NOT implementations:
- **FORBIDDEN:** Full function implementations, code blocks > 5 lines
- **ALLOWED:** Do/Don't/When tables, method signatures (1 line), pseudocode (1-3 lines)
- **INSTEAD OF CODE:** Reference source location: "See src/hooks/usePlan.ts:15-30"
- **TEMPLATE RULE:** guide_template.md includes `<!-- NO_CODE_EXAMPLES: ... -->` tag - FOLLOW IT

### Stack Adaptation Rule (MANDATORY)
- ADRs must reference stack-appropriate alternatives (Compare React vs Vue, not React vs Django)
- Guides must link to correct platform docs (Microsoft for .NET, MDN for JS)

### Format Priority (MANDATORY)
Tables (Do/Don't/When) > ASCII diagrams > Lists > Text

---

## Prerequisites

**Invoked by**: ln-110-documents-pipeline orchestrator

**Requires**:
- `docs/` directory (created by ln-111-project-docs-creator)

**Creates**:
- `docs/reference/` directory structure with README hub
- Validated structure and content (auto-discovery from existing files)

---

## Definition of Done

Before completing work, verify ALL checkpoints:

**✅ Phase 1 - Structure Created:**
- [ ] `docs/reference/` directory exists
- [ ] `docs/reference/adrs/` directory exists
- [ ] `docs/reference/guides/` directory exists
- [ ] `docs/reference/manuals/` directory exists
- [ ] `docs/reference/research/` directory exists
- [ ] `docs/reference/README.md` exists (created or existing)

**✅ Phase 2 - Smart Documents Created (if Context Store provided):**
- [ ] ADRs created for justified technology choices (nontrivial)
- [ ] ADRs skipped for trivial choices (logged)
- [ ] Guides created for technologies with complex config
- [ ] Manuals created for packages with complex API
- [ ] Each created document has real content (not placeholders)

**✅ Phase 3 - Structure Validated:**
- [ ] SCOPE tag present in first 5 lines
- [ ] Four registry sections present (ADRs, Guides, Manuals, Research)
- [ ] Maintenance section present at end
- [ ] POSIX file endings compliant

**✅ Phase 4 - Content Validated:**
- [ ] All sections checked against questions.md
- [ ] Placeholders populated from auto-discovery (including Phase 2 documents)
- [ ] No validation heuristic failures

**✅ Reporting:**
- [ ] Phase 1 logged: creation summary
- [ ] Phase 2 logged: smart creation (created/skipped counts)
- [ ] Phase 3 logged: structural fixes (if any)
- [ ] Phase 4 logged: content updates (if any)

---

## Technical Details

**Standards**:
- Michael Nygard's ADR Format (7 sections)
- ISO/IEC/IEEE 29148:2018 (Documentation standards)

**Language**: English only

---

**Version:** 8.2.0 (Added Stack Adaptation and Format Priority rules)
**Last Updated:** 2025-01-12
