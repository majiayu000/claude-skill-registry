---
name: ext-triage-reqs
description: Triage extension for requirements findings during plan-finalize phase
user-invocable: false
allowed-tools: Read
---

# Requirements Triage Extension

Provides decision-making knowledge for triaging requirements-related findings during the finalize phase.

## Purpose

This skill is a **triage extension** loaded by the plan-finalize workflow skill when processing requirements documentation findings. It provides domain-specific knowledge for deciding whether to fix, suppress, or accept findings.

**Key Principle**: This skill provides **knowledge**, not workflow control. The finalize skill owns the process.

## When This Skill is Loaded

Loaded via `resolve-workflow-skill-extension --domain requirements --type triage` during finalize phase when:

1. AsciiDoc validation errors occur in requirements documents
2. Requirements structure issues are detected
3. Traceability gaps are identified
4. Acceptance criteria format issues are found

## Standards

| Document | Purpose |
|----------|---------|
| [suppression.md](standards/suppression.md) | AsciiDoc comment syntax for suppression |
| [severity.md](standards/severity.md) | Requirements-specific severity guidelines |

## Extension Registration

Registered in marshal.json under the requirements domain:

```json
"requirements": {
  "workflow_skill_extensions": {
    "triage": "pm-requirements:ext-triage-reqs"
  }
}
```

## Quick Reference

### Suppression Methods

| Finding Type | Syntax |
|--------------|--------|
| AsciiDoc lint | `// asciidoc-lint-disable` comment |
| Link validation | `// skip-link-check` comment |
| Structure issue | Document exception in requirements metadata |

### Decision Guidelines

| Severity | Default Action |
|----------|----------------|
| Structure error | **Fix** (requirements must be well-formed) |
| Missing traceability | Fix or document exception |
| Format inconsistency | Fix for consistency |
| Style warning | Accept or fix |

### Acceptable to Accept

- Draft requirements pending review
- Placeholder acceptance criteria in early stages
- Legacy requirements pending migration
- External reference format differences

## Related Documents

- [workflow-extension-api:triage-extension](../../../pm-workflow/skills/workflow-extension-api/standards/extensions/triage-extension.md) - Triage extension contract
- [pm-requirements:requirements-authoring](../requirements-authoring/SKILL.md) - Requirements authoring standards
