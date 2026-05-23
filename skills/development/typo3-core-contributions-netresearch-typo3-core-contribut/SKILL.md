---
name: typo3-core-contributions
description: "Agent Skill: TYPO3 Core contribution workflow. Use when working with Forge issues, submitting patches to Gerrit, or contributing docs. By Netresearch."
---

# TYPO3 Core Contributions

Guide for TYPO3 Core contribution workflow from account setup to patch submission.

## When to Use

- Forge issue URLs (e.g., `https://forge.typo3.org/issues/105737`)
- Contributing patches, fixing TYPO3 bugs
- Gerrit review workflow, rebasing, CI failures

## Prerequisites

```bash
scripts/verify-prerequisites.sh
```

Check: TYPO3.org account, Gerrit SSH, Git config (email must match Gerrit!)

## Workflow Overview

1. **Setup**: Account → Environment (`scripts/setup-typo3-coredev.sh`)
2. **Branch**: `git checkout -b feature/105737-fix-description`
3. **Develop**: Implement, write tests, validate with typo3-conformance-skill
4. **Commit**: Follow format, include `Resolves: #<issue>` + `Releases:`
5. **Submit**: `git push origin HEAD:refs/for/main`
6. **Update**: Amend + push (preserve Change-Id!)

## Commit Format

```
[TYPE] Subject line (imperative, max 52 chars)

Description explaining how and why.

Resolves: #12345
Releases: main, 13.4, 12.4
```

**Types**: `[BUGFIX]`, `[FEATURE]`, `[TASK]`, `[DOCS]`, `[SECURITY]`, `[!!!]`

## Related Skills

- **typo3-ddev-skill**: Development environment
- **typo3-testing-skill**: Test writing
- **typo3-conformance-skill**: Code quality validation

## References

| Topic | File |
|-------|------|
| Account setup | `references/account-setup.md` |
| Commit format | `references/commit-message-format.md` |
| Gerrit workflow | `references/gerrit-workflow.md` |
| Troubleshooting | `references/troubleshooting.md` |

---

> **Contributing:** https://github.com/netresearch/typo3-core-contributions-skill
