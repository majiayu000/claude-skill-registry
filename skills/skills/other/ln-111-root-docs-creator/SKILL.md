---
name: ln-111-root-docs-creator
description: Creates 4 root documentation files (CLAUDE.md, docs/README.md, documentation_standards.md, principles.md). L3 Worker invoked by ln-110-project-docs-coordinator.
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Root Documentation Creator

L3 Worker that creates 4 root documentation files using templates and Context Store from coordinator.

## Purpose & Scope
- Creates 4 root documentation files (entry points for AI agents)
- Receives Context Store from ln-110-project-docs-coordinator
- Replaces placeholders with project-specific data
- Self-validates structure and content (22 questions)
- Never gathers context itself; uses coordinator input

## Invocation (who/when)
- **ln-110-project-docs-coordinator:** ALWAYS invoked as first worker
- Never called directly by users

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

## Documents Created (4)

| File | Target Sections | Questions |
|------|-----------------|-----------|
| CLAUDE.md | Critical Rules, Documentation Navigation, Development Commands, Maintenance | Q1-Q6 |
| docs/README.md | Overview, Standards, Writing Guidelines, Quick Navigation, Maintenance | Q7-Q13 |
| docs/documentation_standards.md | Quick Reference (60+ requirements), 12 main sections, Maintenance | Q14-Q16 |
| docs/principles.md | Core Principles (8), Decision Framework, Anti-Patterns, Verification, Maintenance | Q17-Q22 |

## Workflow

### Phase 1: Receive Context
1. Parse Context Store from coordinator
2. Validate required keys present (PROJECT_NAME, PROJECT_DESCRIPTION)
3. Set defaults for missing optional keys

### Phase 2: Create Documents
For each document (CLAUDE.md, docs/README.md, documentation_standards.md, principles.md):
1. Check if file exists (idempotent)
2. If exists: skip with log
3. If not exists:
   - Copy template from `references/templates/`
   - **Check LEGACY_CONTENT for this document type:**
     - For `principles.md`: If `LEGACY_CONTENT.legacy_principles` exists:
       - Use `legacy_principles.principles[]` as base for "## Core Principles" section
       - Use `legacy_principles.anti_patterns[]` for "## Anti-Patterns" section
       - Use `legacy_principles.conventions[]` for code style rules
       - Augment with template structure (add missing sections)
       - Mark: `<!-- Migrated from legacy documentation -->` at top of relevant sections
     - For other documents: Use template as-is (no legacy content applicable)
   - Replace `{{PLACEHOLDER}}` with Context Store values
   - Mark `[TBD: X]` for missing data (never leave empty placeholders)
   - Write file

### Phase 3: Self-Validate
For each created document:
1. Check SCOPE tag in first 10 lines
2. Check required sections (from questions_root.md)
3. Check Maintenance section (Update Triggers, Verification, Last Updated)
4. Check POSIX endings (single newline at end)
5. Auto-fix issues where possible

### Phase 4: Return Status
Return to coordinator:
```json
{
  "created": ["CLAUDE.md", "docs/README.md", ...],
  "skipped": [],
  "tbd_count": 3,
  "validation": "OK"
}
```

## Critical Notes

### Core Rules
- **Idempotent:** Never overwrite existing files; skip and log
- **No context gathering:** All data comes from coordinator's Context Store
- **TBD markers:** Use `[TBD: placeholder_name]` for missing data, never `{{PLACEHOLDER}}`
- **Language:** All root docs in English (universal standards)
- **SCOPE tags:** Required in first 10 lines of each file

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

## Definition of Done
- Context Store received and validated
- 4 root documents created (or skipped if exist)
- All placeholders replaced (or marked TBD)
- Self-validation passed (SCOPE, sections, Maintenance, POSIX)
- **Actuality verified:** all document facts match current code (paths, functions, APIs, configs exist and are accurate)
- Status returned to coordinator

## Reference Files
- Templates: `references/templates/claude_md_template.md`, `docs_root_readme_template.md`, `documentation_standards_template.md`, `principles_template.md`
- Questions: `references/questions_root.md` (Q1-Q22)

---
**Version:** 2.1.0
**Last Updated:** 2025-01-12
