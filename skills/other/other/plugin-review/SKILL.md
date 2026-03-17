---
name: plugin-review
description: "Tiered plugin quality review with dependency-aware
  scoping. Use when: reviewing plugin changes, preparing PRs,
  pre-release validation. Do not use when: single skill analysis
  (use /analyze-skill), creating new skills (use /create-skill)."
category: plugin-management
tags:
- review
- quality
- validation
- testing
- architecture
dependencies:
- skills-eval
- hooks-eval
- rules-eval
tools:
- validate_plugin.py
- skill_analyzer.py
- generate_dependency_map.py
progressive_loading: true
---

# Plugin Review

Tiered quality review of plugins with dependency-aware scoping.

## Table of Contents

- [Tiers](#tiers)
- [Orchestration](#orchestration)
- [Scope Detection](#scope-detection)
- [Module Loading](#module-loading)
- [Verdict](#verdict)
- [Output Format](#output-format)

## Tiers

| Tier | Trigger | Scope | Depth | Duration |
|------|---------|-------|-------|----------|
| branch | Default | Affected + related | Quick gates | ~2 min |
| pr | Before merge | Affected + related | Standard | ~5 min |
| release | Before version bump | All 17 plugins | Full | ~15 min |

## Orchestration

1. **Detect scope**: parse `--tier` flag, find affected
   plugins from git diff, resolve related plugins from
   `docs/plugin-dependencies.json`
2. **Plan**: build check matrix (tier x plugin x role)
3. **Execute**: run checks per tier definition
4. **Report**: per-plugin table, aggregate verdict

## Scope Detection

Affected plugins: `git diff main --name-only` filtered to
`plugins/*/`.

Related plugins: load `docs/plugin-dependencies.json`,
look up each affected plugin's reverse index to find
dependents. Mark as "related" (lighter checks).

If `--tier release` or no git diff available, scope to
all plugins.

## Module Loading

- **Always**: this SKILL.md (orchestration logic)
- **branch tier**: load `modules/tier-branch.md`
- **pr tier**: load `modules/tier-branch.md` then
  `modules/tier-pr.md`
- **release tier**: load all tier modules plus
  `modules/tier-release.md`
- **When resolving deps**: load
  `modules/dependency-detection.md`

## Verdict

| Result | Meaning |
|--------|---------|
| PASS | All checks green |
| PASS-WITH-WARNINGS | Non-blocking issues |
| FAIL | Blocking issues found |

## Output Format

```
Plugin Review (<tier> tier)
Affected: <list>
Related:  <list> (<reason>)

Plugin          test  lint  type  reg   verdict
<name>          PASS  PASS  PASS  PASS  PASS
...

Verdict: <PASS|WARN|FAIL> (N/N plugins healthy)
```

PR and release tiers add scorecard sections.
