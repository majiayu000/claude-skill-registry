---
name: ln-111-root-docs-creator
description: "Creates root documentation files (AGENTS.md, CLAUDE.md, docs/README.md, standards, principles). Use for initial project doc setup."
license: MIT
model: claude-sonnet-4-6
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Root Documentation Creator

**Type:** L3 Worker

L3 Worker that creates 5 root documentation files using templates and Context Store from coordinator.

## Purpose & Scope
- Creates 5 root documentation files (entry points for AI agents)
- Receives Context Store from ln-110-project-docs-coordinator
- Replaces placeholders with project-specific data
- Self-validates structure and content (22 questions)
- Never gathers context itself; uses coordinator input

## Inputs
From coordinator:
- `contextStore`: Key-value pairs with all placeholders
  - PROJECT_NAME, PROJECT_DESCRIPTION
  - TECH_STACK_SUMMARY
  - DEV_COMMANDS (from package.json scripts)
  - DATE (current date)
  - **LEGACY_CONTENT** (optional, from ln-100 Phase 0 migration):
    - `legacy_principles`: { principles[], anti_patterns[], conventions[] }
- `targetDir`: Project root directory

**LEGACY_CONTENT** is used as base content when creating principles.md. Priority: **Legacy > Template defaults**.

**MANDATORY READ:** Load `shared/references/docs_quality_contract.md` and `shared/references/docs_quality_rules.json`.

## Documents Created (5)

| File | Target Sections | Questions |
|------|-----------------|-----------|
| AGENTS.md | Quick Navigation, Agent Entry, Critical Rules, Development Commands, Maintenance | Q1-Q6 |
| CLAUDE.md | Quick Navigation, Agent Entry, Anthropic-specific notes, Maintenance | Q1-Q6 |
| docs/README.md | Quick Navigation, Agent Entry, Documentation Map, Maintenance | Q7-Q13 |
| docs/documentation_standards.md | Quick Reference (60+ requirements), 12 main sections, Maintenance | Q14-Q16 |
| docs/principles.md | Core Principles (8), Decision Framework, Anti-Patterns, Verification, Maintenance | Q17-Q22 |

## Workflow

### Phase 1: Receive Context
1. Parse Context Store from coordinator
2. Validate required keys present (PROJECT_NAME, PROJECT_DESCRIPTION)
3. Set defaults for missing optional keys

### Phase 2: Create Documents
For each document (AGENTS.md, CLAUDE.md, docs/README.md, documentation_standards.md, principles.md):
1. Check if file exists (idempotent)
2. If exists: skip with log
3. If not exists:
   - Copy template from `references/templates/`
   - Enforce the shared header contract:
     - `SCOPE`
     - `DOC_KIND`
     - `DOC_ROLE`
     - `READ_WHEN`
     - `SKIP_WHEN`
     - `PRIMARY_SOURCES`
   - Enforce the shared top-section contract:
     - `## Quick Navigation`
     - `## Agent Entry`
     - `## Maintenance`
   - **Check LEGACY_CONTENT for this document type:**
     - For `principles.md`: If `LEGACY_CONTENT.legacy_principles` exists:
       - Use `legacy_principles.principles[]` as base for "## Core Principles" section
       - Use `legacy_principles.anti_patterns[]` for "## Anti-Patterns" section
       - Use `legacy_principles.conventions[]` for code style rules
       - Augment with template structure (add missing sections)
       - Mark: `<!-- Migrated from legacy documentation -->` at top of relevant sections
     - For other documents: Use template as-is (no legacy content applicable)
   - Replace `{{PLACEHOLDER}}` with Context Store values
   - Never leave template markers in published root docs
   - If data is missing: omit the claim or use a concise neutral fallback, but do NOT emit `[TBD: ...]`
   - Write file

**Root entrypoint rule:**
- `AGENTS.md` is the canonical machine-facing map
- `CLAUDE.md` must stay thin and point to `AGENTS.md`
- Do not duplicate the full project knowledge base in both files

### Phase 3: Self-Validate
For each created document:
1. Check SCOPE tag in first 12 lines
2. Check metadata markers (`DOC_KIND`, `DOC_ROLE`, `READ_WHEN`, `SKIP_WHEN`, `PRIMARY_SOURCES`)
3. Check `Quick Navigation`, `Agent Entry`, and `Maintenance`
4. Check required sections (from questions_root.md)
5. Check docs-quality contract compliance (no forbidden placeholders, no leaked template metadata)
6. Check POSIX endings (single newline at end)
7. Auto-fix issues where possible

### Phase 4: Return Status
Return to coordinator:
```json
{
  "created_files": ["AGENTS.md", "CLAUDE.md", "docs/README.md", "docs/documentation_standards.md", "docs/principles.md"],
  "skipped_files": [],
  "quality_inputs": {
    "doc_paths": ["AGENTS.md", "CLAUDE.md", "docs/README.md", "docs/documentation_standards.md", "docs/principles.md"],
    "owners": {
      "AGENTS.md": "ln-111-root-docs-creator",
      "CLAUDE.md": "ln-111-root-docs-creator",
      "docs/README.md": "ln-111-root-docs-creator",
      "docs/documentation_standards.md": "ln-111-root-docs-creator",
      "docs/principles.md": "ln-111-root-docs-creator"
    }
  },
  "validation_status": "passed"
}
```

## Critical Notes

### Core Rules
- **Idempotent:** Never overwrite existing files; skip and log
- **No context gathering:** All data comes from coordinator's Context Store
- **Publishable output:** Root docs must not contain `[TBD: ...]`, `TODO`, or leaked template metadata
- **Language:** All root docs in English (universal standards)
- **SCOPE tags:** Required in first 10 lines of each file
- **Map-first root model:** `AGENTS.md` is canonical; `CLAUDE.md` is a compatibility shim

### NO_CODE_EXAMPLES Rule (MANDATORY)
Root documents define **navigation and standards**, NOT implementations:
- **FORBIDDEN:** Code blocks, implementation snippets
- **ALLOWED:** Tables, links, command examples (1 line)
- **TEMPLATE RULE:** All templates include `<!-- NO_CODE_EXAMPLES: ... -->` tag - FOLLOW IT

### Stack Adaptation Rule (MANDATORY)
- All external links must match project stack (detected in Context Store)
- .NET project → Microsoft docs; Node.js → MDN, npm docs; Python → Python docs
- Never mix stack references (no Python examples in .NET project)

### Format Priority (MANDATORY)
Tables/ASCII > Lists (enumerations only) > Text (last resort)

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/docs_generation_summary_contract.md`

Accept optional `summaryArtifactPath`.

Summary kind:
- `docs-generation`

Required payload semantics:
- `worker = "ln-111"`
- `status`
- `created_files`
- `skipped_files`
- `quality_inputs`
- `validation_status`
- `warnings`

Write the summary to the provided artifact path or return the same envelope in structured output.

## Definition of Done
- [ ] Context Store received and validated
- [ ] 5 root documents created (or skipped if exist)
- [ ] All placeholders replaced; no `[TBD: ...]` markers or template metadata remain in root docs
- [ ] Self-validation passed (SCOPE, metadata markers, top sections, Maintenance, POSIX)
- [ ] **Actuality verified:** all document facts match current code (paths, functions, APIs, configs exist and are accurate)
- [ ] Status returned

## Reference Files
- Templates: `references/templates/agents_md_template.md`, `claude_md_template.md`, `docs_root_readme_template.md`, `documentation_standards_template.md`, `principles_template.md`
- Questions: `references/questions_root.md` (Q1-Q22)
- **Environment state:** `shared/references/environment_state_contract.md` (detection and bootstrap pattern)

---
**Version:** 2.1.0
**Last Updated:** 2025-01-12
