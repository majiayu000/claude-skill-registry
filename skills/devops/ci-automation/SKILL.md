---
name: ci-automation
version: 0.7.0
description: Run CI quality gates with optional auto-fix and PR creation.
entry_point: /ci-automation
---

# CI Automation Skill

Coordinates pull → build → test → fix → PR. Keeps instructions lean; heavy details live in references and contracts file. Agent Runner is required for all agent calls (registry-enforced, audited).

## Commands
- `/ci-automation` (flags: `--build`, `--test`, `--dest`, `--src`, `--allow-warnings`, `--yolo`, `--help`)

## Agents (v0.1.0)
- `ci-validate-agent`: pre-flight checks (clean repo, config present, auth available)
- `ci-pull-agent`: pull target branch, handle simple conflicts
- `ci-build-agent`: run build, classify failures
- `ci-test-agent`: run tests, classify failures/warnings
- `ci-fix-agent`: apply straightforward fixes
- `ci-root-cause-agent`: summarize unresolved issues, recommend actions
- `ci-pr-agent`: commit/push/PR when gates pass

## Flow
0. Validate via Agent Runner → `ci-validate-agent`
1. Pull via Agent Runner → `ci-pull-agent` (dest inferred from tracking; `--dest` overrides)
2. Build via Agent Runner → `ci-build-agent`
3. On build fail: Agent Runner → `ci-fix-agent` (only straightforward fixes), repeat
4. Test via Agent Runner → `ci-test-agent`
5. On test/warn fail: Agent Runner → `ci-fix-agent` if straightforward, else `ci-root-cause-agent`
6. If clean and confirmed (or `--yolo`): Agent Runner → `ci-pr-agent` to commit/push/PR

## Config
Preferred: `.claude/ci-automation.yaml` (fallback: `.claude/config.yaml`) with `upstream_branch`, `build_command`, `test_command`, `warn_patterns`, `allow_warnings`, `auto_fix_enabled`, `pr_template_path`, `repo_root`. Detect stack (e.g., .NET/Python/Node) and prompt to save suggested commands.

## Safety
- No force-push; respect protected branches.
- Default is conservative: auto-fix only; stop before commit/PR unless clean and confirmed.
- `--yolo`: allow commit/push/PR after gates pass.
- Warnings block PR unless `--allow-warnings` or config override.
- Explicit confirmation for PRs to main/master unless `--dest main` provided.
- Audit: Agent Runner logs to `.claude/state/logs/ci-automation/`.

## References
- `.claude/references/ci-automation-commands.md`
- `.claude/references/ci-automation-checklists.md`
- `.claude/references/ci-automation-contracts.md`

## Size Guidance
- Keep SKILL.md under ~2KB: overview, flags, agent list, flow summary, contracts, config, safety, references.
