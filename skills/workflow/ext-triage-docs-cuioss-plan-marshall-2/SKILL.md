---
name: ext-triage-docs
description: Triage extension for documentation findings during plan-finalize phase
user-invocable: false
allowed-tools: Read
---

# Documentation Triage Extension

Provides decision-making knowledge for triaging documentation-related findings during the finalize phase.

## Purpose

This skill is a **triage extension** loaded by the plan-finalize workflow skill when processing documentation findings (AsciiDoc, ADRs, interface specifications). It provides domain-specific knowledge for deciding whether to fix, suppress, or accept findings.

**Key Principle**: This skill provides **knowledge**, not workflow control. The finalize skill owns the process.

## When This Skill is Loaded

Loaded via `resolve-workflow-skill-extension --domain documentation --type triage` during finalize phase when:

1. AsciiDoc validation errors occur
2. Broken cross-references are detected
3. ADR format issues are found
4. Interface specification validation fails
5. Link validation errors occur

## Standards

| Document | Purpose |
|----------|---------|
| [suppression.md](standards/suppression.md) | AsciiDoc and markdown suppression syntax |
| [severity.md](standards/severity.md) | Documentation-specific severity guidelines |

## Extension Registration

Registered in marshal.json under the documentation domain:

```json
"documentation": {
  "workflow_skill_extensions": {
    "triage": "pm-documents:ext-triage-docs"
  }
}
```

## Quick Reference

### Suppression Methods

| Finding Type | Syntax |
|--------------|--------|
| AsciiDoc lint | `// asciidoc-lint-disable: rule-name` |
| Link check | `// skip-link-check` |
| ADR format | Document in ADR metadata |
| Markdown lint | `<!-- markdownlint-disable MD001 -->` |

### Decision Guidelines

| Severity | Default Action |
|----------|----------------|
| Broken link | **Fix** (mandatory) |
| Invalid cross-reference | **Fix** (mandatory) |
| Format inconsistency | Fix or accept with justification |
| Style warning | Accept (low priority) |

### Acceptable to Accept

- Draft documentation pending review
- External links to third-party sites (with skip annotation)
- Legacy documentation pending migration
- Generated documentation from code
- Historical ADRs with outdated format

## Related Documents

- [workflow-extension-api:triage-extension](../../../pm-workflow/skills/workflow-extension-api/standards/extensions/triage-extension.md) - Triage extension contract
- [pm-documents:ref-documentation](../ref-documentation/SKILL.md) - Documentation standards
