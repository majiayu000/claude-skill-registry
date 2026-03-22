---
name: ce-rtd-auditor
description: >
  Audit RTD documentation for navigation, technical accuracy, audience fit, and ADR
  or standards consistency.
---

# CE RTD Auditor

Use this skill to perform a critical docs audit across `docs/`.

Load `references/rtd_audit_checklist.md` before producing findings.

## Audit scope

- changed docs pages
- related index/toctree pages
- linked API and ADR references
- command/code snippet correctness

## Workflow

1. Identify targets:

```bash
rg --files docs
rg -n "{doc}|toctree|WrapCalibratedExplainer|ce_agent_utils" docs
```

2. Validate navigation and discoverability:
- page is included in the appropriate toctree/index
- page title and sectioning are clear and stable

3. Validate technical correctness:
- examples use public API (`WrapCalibratedExplainer`, `ce_agent_utils`)
- no private-member guidance
- uncertainty semantics and CE-first lifecycle are consistent

4. Validate governance alignment:
- ADR and standards references exist and are relevant
- no stale or contradictory policy claims

5. Validate links and references:
- internal `{doc}` targets resolve
- markdown links point to real pages/files

## Output contract

Return findings first, ordered by severity:

1. blocker
2. high
3. medium
4. low

Each finding must include:
- path + line reference
- issue summary
- impact
- precise fix recommendation

## Constraints

- Do not propose evaluation-specific skill expansion.
- Prioritize user-facing correctness over wording-only edits.
