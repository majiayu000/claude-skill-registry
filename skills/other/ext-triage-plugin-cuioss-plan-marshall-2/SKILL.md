---
name: ext-triage-plugin
description: Triage extension for marketplace plugin findings during plan-finalize phase
user-invocable: false
allowed-tools: Read
---

# Plugin Development Triage Extension

Provides decision-making knowledge for triaging marketplace plugin development findings during the finalize phase.

## Purpose

This skill is a **triage extension** loaded by the plan-finalize workflow skill when processing plugin development findings (Python scripts, markdown documentation, YAML configurations).

**Key Principle**: This skill provides **knowledge**, not workflow control. The finalize skill owns the process.

## When This Skill is Loaded

Loaded via `resolve-workflow-skill-extension --domain plan-marshall-plugin-dev --type triage` during finalize phase when:

1. Python script tests fail (pytest)
2. Plugin-doctor reports issues
3. Markdown linting issues detected
4. YAML validation errors occur

## Standards

| Document | Purpose |
|----------|---------|
| [suppression.md](standards/suppression.md) | Python and markdown suppression syntax |
| [severity.md](standards/severity.md) | Plugin-specific severity guidelines |

## Extension Registration

Registered in marshal.json under the plugin development domain:

```json
"plan-marshall-plugin-dev": {
  "workflow_skill_extensions": {
    "triage": "pm-plugin-development:ext-triage-plugin"
  }
}
```

## Quick Reference

### Suppression Methods

| Finding Type | Syntax |
|--------------|--------|
| Python linting | `# noqa: E501` or `# noqa` |
| Python typing | `# type: ignore` |
| Pytest skip | `@pytest.mark.skip(reason="...")` |
| Markdown lint | `<!-- markdownlint-disable MD001 -->` |

### Decision Guidelines

| Severity | Default Action |
|----------|----------------|
| Test failure | **Fix** (tests must pass) |
| Plugin-doctor error | **Fix** (quality gate) |
| Script type error | Fix or add type ignore |
| Documentation issue | Fix for consistency |

### Acceptable to Accept

- Markdown formatting in code examples
- Test skip for environment-specific tests
- Type ignores for dynamic patterns
- Plugin-doctor warnings in experimental code

## Related Documents

- [workflow-extension-api:triage-extension](../../../pm-workflow/skills/workflow-extension-api/standards/extensions/triage-extension.md) - Triage extension contract
- [pm-plugin-development:plugin-architecture](../plugin-architecture/SKILL.md) - Plugin patterns
