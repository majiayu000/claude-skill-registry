---
name: review-doc
description: Review all project documentation for correctness, completeness, and freshness. Spawns a doc-maintainer agent to audit and fix docs.
model: opus
---

# Doc Review - Documentation Quality Audit

Spawns a doc-maintainer agent to comprehensively review all project documentation and fix issues found.

## Workflow

### 1. Spawn doc-maintainer agent

Spawn a `DOC - Maintainer` agent with the following prompt:

```
Perform a comprehensive review of ALL project documentation. This is a
standalone audit — do NOT scope to git diff. Instead, review every
documentation file in the project.

Steps:
1. Discover all documentation files (README.md, CLAUDE.md, CONTRIBUTING.md,
   CHANGELOG.md, doc/, docs/, adr/, and any other .md files)
2. Review each for correctness, completeness, and freshness using your
   full quality checklist (code-documentation consistency, completeness,
   link validation, style consistency, freshness)
3. Fix issues you find autonomously (within your authority)
4. Report what you changed and any issues requiring user approval

If no documentation issues are found, report that and exit.
```

### 2. Report results

After the agent completes, present its findings to the user:
- What was reviewed
- What was changed (if anything)
- Issues requiring user approval (if any)

### 3. Commit (optional)

If changes were made, ask the user if they want to commit. If yes:

```bash
git add [specific files]
git commit -m "$(cat <<'EOF'
docs: review and update project documentation

[Brief description of changes made]
EOF
)"
```
