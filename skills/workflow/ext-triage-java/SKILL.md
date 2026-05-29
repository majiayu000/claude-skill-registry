---
name: ext-triage-java
description: Triage extension for Java findings during plan-finalize phase
allowed-tools: Read
---

# Java Triage Extension

Provides decision-making knowledge for triaging Java-related findings during the finalize phase.

## Purpose

This skill is a **triage extension** loaded by the plan-finalize workflow skill when processing Java-related findings. It provides domain-specific knowledge for deciding whether to fix, suppress, or accept findings.

**Key Principle**: This skill provides **knowledge**, not workflow control. The finalize skill owns the process.

## When This Skill is Loaded

Loaded via `resolve-workflow-skill-extension --domain java --type triage` during finalize phase when:

1. Build/test verification produces findings
2. Sonar analysis reports issues
3. PR review comments reference Java code
4. Lint/format checks fail

## Standards

| Document | Purpose |
|----------|---------|
| [suppression.md](standards/suppression.md) | Java suppression syntax (@SuppressWarnings, NOSONAR) |
| [severity.md](standards/severity.md) | Java-specific severity guidelines and decision criteria |

## Extension Registration

Registered in marshal.json under the java domain:

```json
"java": {
  "workflow_skill_extensions": {
    "triage": "pm-dev-java:ext-triage-java"
  }
}
```

## Quick Reference

### Suppression Methods

| Finding Type | Syntax |
|--------------|--------|
| Sonar rule | `@SuppressWarnings("java:S1234")` |
| Deprecation | `@SuppressWarnings("deprecation")` |
| Unchecked cast | `@SuppressWarnings("unchecked")` |
| Null warning | `@SuppressWarnings("null")` or JSpecify annotations |
| All warnings | `// NOSONAR` (line comment, use sparingly) |

### Decision Guidelines

| Severity | Default Action |
|----------|----------------|
| BLOCKER | **Fix** (mandatory) |
| CRITICAL | **Fix** (mandatory for vulnerabilities) |
| MAJOR | Fix or suppress with justification |
| MINOR | Fix, suppress, or accept |
| INFO | Accept (low priority) |

### Acceptable to Accept

- Generated code in `**/generated/**`
- Test data builders with intentionally permissive patterns
- Legacy code with documented migration plan
- Framework-mandated patterns (e.g., Serializable)
- Documented false positives

## Related Documents

- [workflow-extension-api:triage-extension](../../../pm-workflow/skills/workflow-extension-api/standards/extensions/triage-extension.md) - Triage extension contract
- [pm-dev-java:java-core](../java-core/SKILL.md) - Core Java patterns
