---
name: skill-review
description: |
  Audit claude-skills with systematic 9-phase review: standards compliance, official docs verification, code accuracy, cross-file consistency, and version drift detection.

  Use when investigating skill issues, major updates detected, skill not verified >90 days, or before marketplace submission.
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - Edit
  - Write
---

# Skill Review Skill

## Process

Invoke: `/review-skill <skill-name>` or use this skill when detecting outdated patterns

**Production evidence**: better-auth audit (2025-11-08) - found 6 critical issues including non-existent API imports, removed 665 lines incorrect code, implemented v2.0.0

---

## 9-Phase Audit

1. **Pre-Review**: Install skill, check version/date, test discovery
2. **Standards**: Validate YAML, keywords, third-person style, directory structure
3. **Official Docs**: WebFetch/Context7 verify API patterns, GitHub updates, npm versions, production repos
4. **Code Examples**: Verify imports exist, API signatures match, schema consistency, templates work
5. **Cross-File Consistency**: Compare SKILL.md vs README.md, bundled resources match files
6. **Dependencies**: Run `./scripts/check-versions.sh`, check breaking changes, verify "Last Verified"
7. **Categorize**: Severity (🔴 Critical / 🟡 High / 🟠 Medium / 🟢 Low) with evidence (GitHub/docs/npm)
8. **Fix**: Auto-fix unambiguous, ask user for architectural, update all files, bump version
9. **Verify**: Test discovery, templates work, no contradictions, commit with changelog

**Automated** (via `./scripts/review-skill.sh`): YAML syntax, package versions, broken links, TODOs, file org, staleness

**Manual** (AI): API methods vs docs, GitHub issues, production comparisons, code correctness, schema consistency

---

## Severity Classification

🔴 **CRITICAL**: Non-existent API/imports, invalid config, missing dependencies

🟡 **HIGH**: Contradictory examples, inconsistent patterns, outdated major versions

🟠 **MEDIUM**: Stale minors (>90d), missing docs sections, incomplete errors

🟢 **LOW**: Typos, formatting, missing optional metadata

## Fix Decision

**Auto-fix**: Unambiguous (correct import from docs), clear evidence, no architectural impact

**Ask user**: Multiple valid approaches, breaking changes, architectural choices

## Version Bumps

- **Major** (v1→v2): API patterns change
- **Minor** (v1.0→v1.1): New features, backward compatible
- **Patch** (v1.0.0→v1.0.1): Bug fixes only

---

## Example: better-auth Audit (2025-11-08)

**🔴 CRITICAL #1**: Non-existent `d1Adapter` import from `'better-auth/adapters/d1'`
- **Evidence**: Official docs show drizzleAdapter, GitHub has no d1Adapter export, 4 production repos use Drizzle/Kysely
- **Fix**: Replaced with `drizzleAdapter` from `'better-auth/adapters/drizzle'`

**Result**: 3 files deleted (obsolete), 3 created (correct patterns), +1,266 lines, v1.0→v2.0, 3.5 hours

---

## Issues Prevented (10)

1. **Fake API adapters** - Non-existent imports
2. **Stale API methods** - Changed signatures
3. **Schema inconsistency** - Different table names
4. **Outdated scripts** - Deprecated approaches
5. **Version drift** - Packages >90 days old
6. **Contradictory examples** - Multiple conflicting patterns
7. **Broken links** - 404 URLs
8. **YAML errors** - Invalid frontmatter
9. **Missing keywords** - Poor discoverability
10. **Incomplete bundled resources** - Listed files don't exist

---

## Bundled Resources

**Planning**: `~/.claude/skills/../planning/SKILL_REVIEW_PROCESS.md` or repo `planning/SKILL_REVIEW_PROCESS.md` (complete 9-phase guide)

**Scripts**: Repo root `scripts/review-skill.sh` (automated validation)

**Commands**: Repo root `commands/review-skill.md` (slash command, symlinked to `~/.claude/commands/`)

**References**: `references/audit-report-template.md` (output template)

---

**Last Verified**: 2026-01-09 | **Version**: 1.0.1
