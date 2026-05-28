---
name: ext-outline-docs
description: Outline extension for documentation domain
allowed-tools: Read
---

# Documentation Outline Extension

> Extension for phase-2-outline in documentation domain.

Provides domain-specific knowledge for deliverable creation in documentation tasks. This is a knowledge document loaded as context - it does not replace the workflow.

## Domain Detection

This domain is relevant when:
1. `doc/` or `docs/` directory exists
2. Request mentions "AsciiDoc", "ADR", "interface specification", "documentation"
3. Files have `.adoc` extension
4. Request mentions updating README or technical documentation

## Domain Constraints

### Component Rules
- AsciiDoc files MUST have blank line before lists
- Cross-references MUST use `xref:` syntax
- ADRs MUST follow numbered naming: `ADR-NNN-title.adoc`
- Interface specs MUST follow numbered naming: `IF-NNN-title.adoc`
- All documents should have proper heading hierarchy

### Dependency Rules
- Documentation changes do NOT require unit tests
- Changes to `doc/` directory do NOT trigger build verification
- ADR changes require review of supersedes/superseded-by links
- Interface spec changes may require code traceability updates

### Verification Rules
- AsciiDoc validation: Check for proper formatting and structure
- Link verification: Validate all internal cross-references
- Verification commands:
  - ADRs: Check ADR numbering sequence and status consistency
  - Interfaces: Check interface numbering and completeness

## Deliverable Patterns

### Grouping Strategy
| Scenario | Grouping |
|----------|----------|
| Single document update | One deliverable |
| ADR creation with related updates | One deliverable for all related ADRs |
| Interface spec with code traceability | One deliverable for spec, separate for code |
| Documentation sync with code | Doc deliverable depends on code deliverable |

### Change Type Mappings
| Request Pattern | change_type | execution_mode |
|-----------------|-------------|----------------|
| "add", "create", "new" ADR/doc | create | automated |
| "update", "fix" documentation | modify | automated |
| "supersede" ADR | modify | automated |
| "reorganize" docs | refactor | manual |

### Standard File Structures
- ADRs: `doc/adr/ADR-NNN-{title}.adoc`
- Interfaces: `doc/interfaces/IF-NNN-{title}.adoc`
- Architecture: `doc/architecture/{topic}.adoc`
- General: `doc/{topic}/`
- README: `README.md` or `README.adoc`

## Impact Analysis Patterns

### Detection Commands
| Change Type | Discovery Command |
|-------------|-------------------|
| Broken xrefs | `grep -r 'xref:' doc/*.adoc` |
| ADR supersedes | `grep -r 'Superseded by' doc/adr/` |
| Interface refs | `grep -r 'IF-[0-9]' doc/` |
| README links | `grep -r '\[.*\](.*\.adoc)' README.md` |

### Discovery Script
For comprehensive documentation analysis:
```bash
# Find all AsciiDoc files
find doc/ -name "*.adoc" -type f

# Check ADR sequence
ls -1 doc/adr/ADR-*.adoc 2>/dev/null | sort

# Check interface specs
ls -1 doc/interfaces/IF-*.adoc 2>/dev/null | sort
```

### Batch Analysis Guidelines
- Process related documents together (e.g., ADR and its superseded docs)
- Check cross-references when modifying any document
- Validate heading hierarchy in modified documents

## Related Skills

| Skill | Purpose |
|-------|---------|
| `pm-documents:cui-documentation` | General documentation standards |
| `pm-documents:adr-management` | ADR CRUD and formatting |
| `pm-documents:interface-management` | Interface spec CRUD and formatting |
