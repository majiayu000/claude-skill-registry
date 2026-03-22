---
name: kit-verify
description: (ePost) Use when preparing a release, running pre-init checks, auditing kit health, or when asked to "verify", "audit kit", "pre-release check"
user-invocable: false
metadata:
  keywords:
    - verify
    - audit
    - pre-release
    - health-check
    - lint
  agent-affinity:
    - epost-kit-designer
    - epost-code-reviewer
  platforms:
    - all
  connections:
    requires: [kit-agents]
---

# Kit Verification Workflow

Pre-release/pre-init audit pipeline. Ensures kit integrity before `epost-kit init` or release.

## When to Use

- Before running `epost-kit init` on a project
- Before creating a release/tag
- After batch-editing skills, agents, or connections
- When CI gate needs to validate kit health

## CLI Command

```bash
epost-kit verify            # full audit, errors block
epost-kit verify --strict   # warnings also block (CI mode)
```

## What It Checks

1. **Reference validation** — all agent/skill/command refs point to valid targets
2. **Connection integrity** — extends/requires/enhances targets exist, no cycles, bidirectional conflicts
3. **Frontmatter completeness** — skills have description, keywords, platforms
4. **Package.yaml sync** — skills on disk match provides.skills declarations
5. **Skill-index staleness** — index count matches actual SKILL.md count
6. **Orphan detection** — skills not referenced by any agent or connection
7. **Dependency graph** — auto-generates `docs/skill-dependency-graph.md` (mermaid)

## Exit Codes

- `0` — pass (may have warnings/info)
- `1` — fail (errors found, or `--strict` with warnings)

## Integration

- Wire as pre-commit hook: `epost-kit verify --strict`
- Wire in CI: `npx epost-kit verify --strict --dir .`
- `epost-kit init` can optionally run verify before generating `.claude/`
