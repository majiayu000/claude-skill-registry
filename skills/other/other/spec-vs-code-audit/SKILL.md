---
name: vibe-spec-vs-code-audit
description: Compares specification documents against implementation code to find divergences. Use when implementation of a spec or design doc is claimed complete.
user-invocable: true
---

# vibe-spec-vs-code-audit

Specs drift from code. Code drifts from specs. This skill catches the gaps.

## When to Use This Skill

- Implementation of a spec/design doc is claimed complete
- After a major refactor that should still conform to a spec
- During periodic compliance checks
- When debugging unexpected behavior (maybe the code doesn't match the spec)

## When NOT to Use This Skill

- No spec or design doc exists (nothing to compare against)
- The spec is explicitly marked as aspirational/future
- Code was intentionally diverged with documented reasons

## Steps

1. **Identify the spec** — Find the specification document (design doc, PRD section, API spec, etc.)

2. **Identify the implementation** — Find the code files that implement this spec

3. **Line-by-line comparison** — For each requirement/section in the spec:
   - Find the corresponding code
   - Check: Does the code match the spec exactly?
   - If divergent: Record as a GAP

4. **Classify each gap**:
   - **ID**: GAP-[section]-[number] (e.g., GAP-AUTH-001)
   - **Type**: Missing (spec says X, code has nothing) / Incorrect (spec says X, code does Y) / Extra (code has X, spec doesn't mention it)
   - **Severity**: Critical (breaks core functionality) / High (wrong behavior) / Medium (incomplete) / Low (cosmetic)

5. **Report**:

## Output Format

### Spec vs Code Audit

**Spec**: [document name/path]
**Implementation**: [code path(s)]
**Gaps Found**: X (Y critical, Z high)

| GAP ID | Type | Severity | Spec Says | Code Does |
|--------|------|----------|-----------|-----------|
| GAP-AUTH-001 | Missing | Critical | "Tokens expire after 24h" | No expiration logic found |

### Top 3 Risks
1. [Most dangerous gap]

### Recommended Fix Order
1. [Fix critical gaps first]
