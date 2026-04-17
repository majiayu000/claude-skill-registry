---
name: hermes-skill-source-classification
description: Diagnose Hermes `hermes skills list` source labels (`builtin` vs `local`) and avoid false sync decisions.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Hermes skill source classification

Use this when `hermes skills list` shows `source=builtin` for skills that also exist in local skill directories.

## Key finding

Hermes source labeling is name-manifest based:
- if a skill name appears in `~/.hermes/skills/.bundled_manifest`, the CLI may label it as `builtin`
- this can happen even when a local copy exists at `~/.hermes/skills/<category>/<name>/`

So `builtin` does not always mean “no local copy”.

## Verification workflow

1) Check label:
```bash
hermes skills list --source all | grep -E '<skill-name>'
```

2) Check bundled manifest hit:
```bash
grep -nE '^<skill-name>:' ~/.hermes/skills/.bundled_manifest
```

3) Check both physical paths:
```bash
test -f ~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md && echo bundled_exists
test -f ~/.hermes/skills/<category>/<skill-name>/SKILL.md && echo local_exists
```

## Sync decision rule

For repo/local sync scripts, do not use only `--source local` as truth.
Use a combined rule:
- source label
- local path existence
- repo path existence

## Pitfall

A skill may be misclassified as repo-only if your script trusts source label alone.
This can trigger unnecessary sync prompts.
