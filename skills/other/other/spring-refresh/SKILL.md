---
name: spring-refresh
description: Check Spring Boot skill content freshness against latest research and flag skills needing updates. Use when running /spring-refresh, or when user mentions "refresh spring skills", "spring boot update check", "skill freshness", "stale spring content", "update spring boot skills".
disable-model-invocation: true
---

# Spring Boot Skill Freshness

Check whether Spring Boot skills are current with the latest research docs.

## Arguments

Parse `$ARGUMENTS` for mode:
- **`check`** (default, no args) — Scan and report freshness
- **`refresh`** — Update research docs via deep-research, then report
- **`update <skill-name>`** — Help update a specific skill's content

## Mode: check

1. Run the freshness scanner:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/scan_skill_freshness.py --format json ${CLAUDE_SKILL_DIR}/../..
```

2. Parse the JSON output and present a formatted report with:
   - Research doc staleness table (file, version, last updated, age, status)
   - Skill drift table (name, target version, last modified, research date, drift, status)
   - Summary counts (up-to-date, needs review, needs update)

3. For skills with `NEEDS_REVIEW` or `NEEDS_UPDATE`:
   - List which research docs they depend on
   - Suggest running `/spring-refresh update <skill-name>` for each

## Mode: refresh

1. For each Spring Boot research doc, invoke the Skill tool with `core:deep-research` to refresh:
   - `refresh spring-boot-ecosystem` (for ecosystem-research.md)
   - `refresh spring-boot-ddd-implementation` (for ddd-implementation.md)
   - `refresh spring-boot-security-observability-testing` (for security-observability-testing.md)

2. After all research docs are refreshed, run the `check` mode to produce the updated report.

3. Show a before/after comparison of research doc dates.

**Fallback:** If the deep-research skill is not available, skip the research refresh and run `check` mode only. Inform the user they can manually update research docs.

## Mode: update \<skill-name\>

1. Run `check` mode first to identify drift status for the specified skill.

2. Read the research docs that map to this skill:
   - `spring-boot-ecosystem-research.md` → scanner, verify, web-api, data-ddd, modulith, domain-driven-design
   - `spring-boot-ddd-implementation.md` → domain-driven-design, data-ddd, web-api, modulith
   - `spring-boot-security-observability-testing.md` → security, observability, testing

3. Read the skill's current content: SKILL.md, EXAMPLES.md, TROUBLESHOOTING.md, and all files in references/.

4. Compare research content against skill content. Identify:
   - New APIs or patterns in research not covered in the skill
   - Deprecated patterns in the skill that research has replaced
   - Version-specific changes (e.g., new Spring Boot minor version features)

5. Present proposed changes to the user for confirmation before editing.

6. After updates, bump the `spring-boot-version` field if targeting a new version.

## Output Format

```
## Spring Boot Skill Freshness Report

### Research Documents
| Document | Version | Updated | Age | Status |
|----------|---------|---------|-----|--------|

### Skills
| Skill | Target | Modified | Research | Drift | Status |
|-------|--------|----------|----------|-------|--------|

### Recommendations
- [actionable items]
```

## References

- [EXAMPLES.md](EXAMPLES.md) for usage examples
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Research docs (local): `docs/research/spring-boot-*.md`
- [Research docs on GitHub](https://github.com/joaquimscosta/arkhe-claude-plugins/tree/main/docs/research)
