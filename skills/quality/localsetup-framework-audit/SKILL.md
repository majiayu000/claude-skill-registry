---
name: localsetup-framework-audit
description: "Run doc, link, skill matrix, and version/facts checks before release. Single entrypoint script; output to user-specified path only; no in-repo default. Use when user says 'run audit', 'run framework audit', or before release."
metadata:
  version: "1.0"
compatibility: "Python 3.10+. Depends on localsetup-skill-sandbox-tester tooling (create_sandbox.py, run_smoke.py) for skill matrix; both ship with the framework (framework invariant)."
---

# Framework audit

**Purpose:** One atomic skill and entrypoint to run a release-ready audit: doc checks, link checks, skill matrix (sandbox only), version/facts, and optional maintainer-ref flagging. Output is written only to a user-provided path (CLI or env); no default in-repo. Exit 0 only when there are zero errors.

## When to use

- User says "run audit", "run framework audit", or "before release".
- Pre-release: lock in for release; zero errors and zero unexplained warnings.

## Workflow

1. **Run the entrypoint** from repo root: `python _localsetup/skills/localsetup-framework-audit/scripts/run_framework_audit.py [--output /path/to/report]` or set `LOCALSETUP_AUDIT_OUTPUT` to a writable path. If no output path is given, the script prints a short summary to stdout only; no file is written in the repo.
2. **Phases:** Doc checks (key docs exist), link checks (plain-text refs to docs/ or _localsetup/ reported for conversion to markdown links), skill matrix (sandbox + smoke from smoke list), version/facts (VERSION vs README vs facts.json if present), maintainer refs (hardcoded maintainer-only paths or script names).
3. **Report:** Contains a `requires_review` / `human_decision` section for items that need user resolution. The script is non-interactive; the agent presents the report and asks the user.
4. **Doc-only skills:** The smoke list marks them as `N/A`. The script does not run tooling for those. The **agent** (not the script) produces an enumerated one-sentence/paragraph per logical step and flags logic gaps for user resolution, per SKILL.md of each doc-only skill.

## Smoke list (skill matrix)

- **Path:** `_localsetup/tests/skill_smoke_commands.yaml`
- **Schema:** YAML map: `skill_id` (directory name under _localsetup/skills/) → `command` string or `"N/A"`. Command is run with cwd = sandbox copy of the skill. `N/A` = doc-only; no runnable smoke; audit uses agent step summary only.
- One entry per skill in `_localsetup/skills/*`. The audit script reads this file as single source of truth for which skills have tooling to smoke.

## Dependencies (framework invariant)

- **Sandbox tooling:** The audit may call `_localsetup/skills/localsetup-skill-sandbox-tester/scripts/create_sandbox.py` and `run_smoke.py` to run skill smoke commands in an isolated copy. Both the audit skill and the sandbox-tester skill ship with the framework; no external dependency.

## Tooling

| Item | Purpose |
|------|---------|
| `scripts/run_framework_audit.py` | Single entrypoint: doc, link, skill matrix, version/facts; output path from CLI or env; exit 0 only if no errors. |

**Quick start:**

```bash
# Output to file (e.g. maintainer repo folder)
python _localsetup/skills/localsetup-framework-audit/scripts/run_framework_audit.py --output /path/to/audit_report.md

# Or env
export LOCALSETUP_AUDIT_OUTPUT=/path/to/audit_report.md
python _localsetup/skills/localsetup-framework-audit/scripts/run_framework_audit.py

# Summary only (no file written)
python _localsetup/skills/localsetup-framework-audit/scripts/run_framework_audit.py
```

## Errors vs warnings

- **Error:** Smoke non-zero/crash, syntax/lint failure, missing required doc, broken link that should be fixed. Exit non-zero.
- **Warning:** N/A or item to fix or explicitly accept; logged in report. Zero errors and zero unexplained warnings before release.

## References

- _localsetup/docs/TOOLING_POLICY.md (lint/quality; audit uses for tooling expectations)
- _localsetup/docs/INPUT_HARDENING_STANDARD.md (script follows for all external input)
- _localsetup/tests/skill_smoke_commands.yaml (smoke list path and schema)
