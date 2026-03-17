---
name: ext-triage-js
description: Triage extension for JavaScript/TypeScript findings during plan-finalize phase
user-invocable: false
allowed-tools: Read
---

# JavaScript Triage Extension

Provides decision-making knowledge for triaging JavaScript and TypeScript findings during the finalize phase.

## Purpose

This skill is a **triage extension** loaded by the plan-finalize workflow skill when processing JavaScript/TypeScript-related findings. It provides domain-specific knowledge for deciding whether to fix, suppress, or accept findings.

**Key Principle**: This skill provides **knowledge**, not workflow control. The finalize skill owns the process.

## When This Skill is Loaded

Loaded via `resolve-workflow-skill-extension --domain javascript --type triage` during finalize phase when:

1. ESLint reports rule violations
2. TypeScript compiler reports type errors
3. Jest test failures occur
4. Prettier formatting issues are detected
5. Stylelint reports CSS issues

## Standards

| Document | Purpose |
|----------|---------|
| [suppression.md](standards/suppression.md) | JavaScript suppression syntax (eslint-disable, ts-ignore) |
| [severity.md](standards/severity.md) | JavaScript-specific severity guidelines and decision criteria |

## Extension Registration

Registered in marshal.json under the javascript domain:

```json
"javascript": {
  "workflow_skill_extensions": {
    "triage": "pm-dev-frontend:ext-triage-js"
  }
}
```

## Quick Reference

### Suppression Methods

| Finding Type | Syntax |
|--------------|--------|
| ESLint rule | `// eslint-disable-next-line rule-name` |
| ESLint block | `/* eslint-disable rule-name */` |
| TypeScript error | `// @ts-ignore` or `// @ts-expect-error` |
| Prettier | Not suppressible (fix or configure) |
| Stylelint | `/* stylelint-disable rule-name */` |

### Decision Guidelines

| Severity | Default Action |
|----------|----------------|
| error | **Fix** (blocks build/CI) |
| warn | Fix or suppress with justification |
| off | N/A (disabled rule) |

### Acceptable to Accept

- Generated code in `**/generated/**`, `**/dist/**`
- Third-party type definitions when incompatible
- Legacy JavaScript files pending TypeScript migration
- Test mocks with intentional type violations

## Related Documents

- [workflow-extension-api:triage-extension](../../../pm-workflow/skills/workflow-extension-api/standards/extensions/triage-extension.md) - Triage extension contract
- [pm-dev-frontend:cui-javascript](../cui-javascript/SKILL.md) - Core JavaScript patterns
