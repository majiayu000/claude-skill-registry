---
name: ci-cd-compliance
description: CI/CD pipeline requirements and deployment standards. Use when (1) Setting up CI/CD pipelines, (2) Debugging CI failures, (3) Configuring deployment workflows, (4) Managing staging/production releases, (5) Investigating build failures. Covers CI gate requirements, merge policies, auto-deploy to staging, production approval process.
---

# CI/CD Compliance Rules

## CI Gates Sequence

**install → lint/format → typecheck → unit → integration → (optional e2e) → package**

## Merge Policy

* **Merge only if green**
* Auto-deploy to **staging** on merge
* Production requires tag/approval

## CI Failure Handling

When CI fails:
1. **Explain root cause** in PR comment
2. **Include the fix** in the same PR when feasible
3. Don't merge until all gates pass

## IDE Integration

* **AINative / Windsurf / Cursor / Claude Code:** Use built-in code actions and terminal to run tests/linters
* Prefer **unified diffs** in responses so changes are patchable across IDEs
* Attach artifacts (test output, screenshots, logs) whenever you assert a claim

## Reference Files

See `references/pipeline-requirements.md` for detailed CI configuration, gate definitions, and failure debugging guide.
