---
name: documentation-updates
description: "Use after modifying library skills, library commands, or agents to ensure CHANGELOG, README, and docs are updated"
---

# Documentation Updates

<analysis>
Identify: What library content changed? Scope: library skills (`skills/`), commands (`commands/`), agents (`agents/`).
Exclude: Repo skills (`.claude/skills/`) are internal tooling, no external docs needed.
</analysis>

## Invariant Principles

1. **Library changes require documentation trail** - Every modification to installed content must be traceable through CHANGELOG
2. **Counts must match reality** - README totals reflect actual files, never stale
3. **Generated docs stay fresh** - Run generator after any library content change
4. **Repo skills are invisible** - Internal tooling never touches external docs

## Required Updates Matrix

| Change | CHANGELOG | README | Docs Generator |
|--------|-----------|--------|----------------|
| Add library skill | "Added" section | count++, add table row, add link ref | Run |
| Modify library skill | "Changed" section | Only if description changed | Run |
| Remove library skill | "Removed" section | count--, remove row/link | Run |
| Add/modify command | Appropriate section | Update if count/description affected | Run |

## Verification Checklist

<reflection>
Before PR completion, evidence required for each:
</reflection>

- [ ] CHANGELOG.md has entry under `## [Unreleased]`
- [ ] README.md counts match `ls skills/*/SKILL.md | wc -l` and `ls commands/*.md | wc -l`
- [ ] New items have table rows AND link references
- [ ] `python3 scripts/generate_docs.py` executed
- [ ] Pre-commit hooks committed generated files

## CHANGELOG Entry Format

```markdown
## [Unreleased]

### Added
- **skill-name skill** - one-line description
  - Notable feature bullet

### Changed
- **skill-name skill** - what changed and why

### Removed
- **skill-name skill** - removal rationale
```

## README Link Reference Pattern

```markdown
[skill-name]: https://axiomantic.github.io/spellbook/latest/skills/skill-name/
```

<CRITICAL>
Library content (`skills/`, `commands/`, `agents/`) triggers this skill.
Repo content (`.claude/skills/`) does NOT.
</CRITICAL>
