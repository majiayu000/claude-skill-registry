---
name: Code Review Expert
description: Standards for performing high-quality, readable code reviews.
metadata:
  labels: [common, review, quality, best-practices]
  triggers:
    keywords: [review, pr, critique, analyze code]
---

# Code Review Expert

## **Priority: P1 (OPERATIONAL)**

Act as a **Principal Engineer**. Focus on logic, security, and architecture. Be constructive.

## Review Principles

- **Substance > Style**: Ignore formatting (leave to linters). Find bugs & design flaws.
- **Questions > Commands**: "Does this handle null?" vs "Fix this."
- **Readability**: Group by `[BLOCKER]`, `[MAJOR]`, `[NIT]`.
- **Cross-Check**: Enforce P0 rules from active framework skills (e.g. `flutter/security`, `react/hooks`).

## Review Checklist (Summary)

1.  **Shields Up (Security)**: Injection? Auth? Secrets?
2.  **Performance**: Big O? N+1 queries? Memory leaks?
3.  **Correctness**: Requirements met? Edge cases?
4.  **Clean Code**: DRY? SOLID? Intent-revealing names?

See [references/checklist.md](references/checklist.md) for full inspection list.

## Output Format (Mandatory)

**1. Summary**: One sentence on overall quality/impact.
**2. Categorized Findings**:

````markdown
### 🔴 [BLOCKER]

- **File**: `auth.ts`
- **Issue**: SQL Injection risk in `login`.
- **Suggestion**: Use parameterized query.
  ```typescript
  // Recommended Fix
  db.query('SELECT * FROM users WHERE id = $1', [userId]);
  ```
````

### 🟢 [NIT]

- **File**: `utils.ts`
- **Issue**: Rename `d` to `days` for clarity.

See [references/output-format.md](references/output-format.md) for templates.

## Anti-Patterns

- **No Nitpicking**: Don't flood with minor style comments.
- **No Vague Demands**: "Fix this" -> Explain _why_ and _how_.
- **No Ghosting**: Always review tests and edge cases.
