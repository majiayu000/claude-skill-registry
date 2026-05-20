---
name: ce-rtd-writer
description: >
  Write or revise RTD pages with audience-aware structure, CE-first examples, and
  correct toctree integration.
---

# CE RTD Writer

Use this skill when adding or rewriting docs pages under `docs/`.

## Core asset

- `assets/rtd_page_template.md` - default authoring template.

## Workflow

1. Identify audience and placement:
- choose target hub (`get-started`, `practitioner`, `researcher`,
  `contributor`, etc.)
- identify parent index/toctree update requirements

2. Start from template:

```bash
Copy-Item .claude/skills/ce-rtd-writer/assets/rtd_page_template.md `
  docs/<target>/<new-page>.md
```

3. Author content with CE-first correctness:
- public APIs only
- explicit uncertainty semantics
- runnable command/code examples
- audience-appropriate depth (STD-004)

4. Wire navigation:
- add page to relevant index/toctree
- ensure canonical cross-links to related docs

5. Self-audit:
- run `ce-rtd-auditor` checks before finalizing
- fix all blocker/high issues

## Output contract

Deliver:

1. new/updated page(s)
2. toctree/index updates
3. concise change summary with audience impact

## Constraints

- Avoid evaluation-specific skill planning.
- Prefer edits that preserve existing public API stability and doc consistency.
