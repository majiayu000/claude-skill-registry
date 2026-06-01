---
name: vscode-doctor
description: Diagnose slow or freezing VS Code-compatible editors with evidence-first, zero-hardcoded-assumption workflow. Use when the user reports editor lag, typing delay, UI freezes, extension host stalls, file watcher noise, high editor CPU/RSS, or wants a safe editor performance audit.
allowed-tools: Bash, Read
metadata:
  argument-hint: "[workspace-root optional]"
---

# VS Code Doctor

Diagnose editor performance from the current machine state. Do not import old observations, fixed paths, fixed extension names, fixed OS bugs, or fixed generated-directory lists into the diagnosis.

## Non-Negotiables

- No hardcoded local paths. Use the user's stated workspace, discovered editor status, or explicit placeholders.
- No fixed root cause order. Rank only by fresh evidence from this run.
- No fixed extension blocklist. Treat extension names as evidence only when they appear in live output or user-provided screenshots.
- No fixed generated-directory list. Discover ignored/generated paths from the workspace, editor settings, repository metadata, or user-provided patterns.
- No fixed benefit percentages. If there is no before/after baseline, say the impact cannot be reliably quantified.
- No write operations by default. Do not edit settings, disable extensions, delete caches, run system defaults, change environment variables, or kill processes without explicit confirmation.

## Collection

Run the collector with values discovered for this case. Leave unknown values empty instead of inventing them.

```bash
cd <path-to-vscode-doctor-skill>
EDITOR_COMMANDS="<space-separated editor cli commands, if known>" \
EDITOR_PROCESS_QUERY="<process regex, if known>" \
EDITOR_DATA_DIRS="<colon-separated data dirs, if known>" \
EDITOR_SETTINGS_FILES="<colon-separated settings files, if known>" \
EDITOR_LOG_DIRS="<colon-separated log dirs, if known>" \
LOG_FILE_GLOB="<log file glob, if known>" \
LOG_SIGNAL_QUERY="<log regex, if known>" \
GENERATED_DIR_PATTERNS="<colon-separated generated directory names, if user/project supplied>" \
./scripts/collect_vscode_diagnostics.sh "<workspace-root>"
```

Discovery rules:
- If the user gives the opened workspace, pass it as the script argument.
- If the user does not give the workspace, infer it from editor status output, visible state, or ask a concise question.
- If an editor CLI/path/log directory cannot be discovered, skip that probe and state that the evidence is missing.
- If a signal comes from logs, include the log path and timestamp.

## Analysis

Classify each finding by evidence strength:

- **High priority**: current CPU/RSS/log/status evidence directly explains the symptom and the next experiment is low risk.
- **Medium priority**: plausible contributor with partial evidence, or a safe optimization whose current impact is not proven.
- **Low priority**: maintenance or cleanup item without direct evidence of causing the symptom.

Common evidence types to look for, without assuming any one must exist:
- editor main/renderer/extension-host process CPU or RSS
- language service or extension child-process CPU/RSS
- file watcher errors or repeated workspace rescans
- large workspace surface area from editor status, VCS metadata, or ignored/generated paths
- repeated extension-host unresponsive signals
- UI process pressure that correlates with editor renderer activity
- cache or storage size only when it is large enough to plausibly matter

When recommending extension changes:
- Use only extension names seen in live output, user screenshots, or logs.
- Prefer workspace-scoped disablement or profiling over global disablement.
- If the evidence only shows “extension host high,” recommend profiling or bisecting before naming a culprit.

When recommending workspace exclusions:
- Prefer exclusions derived from the project's own ignored/generated paths.
- If you propose a generic pattern, label it as a template for user review, not as evidence.
- Prefer workspace settings over global settings when the issue is tied to one workspace.

## Report Template

Use this concise structure:

```markdown
## Editor Performance Diagnosis

### Evidence
| Signal | Current value | Source | Confidence |
|----|----|----|----|
| ... | ... | ... | high/medium/low |

### Priority
#### High
1. ...

#### Medium
1. ...

#### Low
1. ...

### Options
| Option | When to use | Expected impact | Cost | Verify | Roll back |
|----|----|----|----|----|----|
| ... | ... | Cannot quantify without baseline / based on observed delta | ... | ... | ... |

### Next Step
Ask the user which option to run first. Do not apply changes until they confirm.
```

## Verification

Before claiming improvement, collect a fresh after-snapshot with the same collector inputs used for the baseline. Compare only observed values:

```markdown
## Before / After

| Metric | Before | After | Result |
|----|----:|----:|----|
| ... | ... | ... | improved / unchanged / worse / unknown |

Conclusion:
- Experiment result: ...
- Remaining evidence: ...
- Next step: ...
- Rollback: ...
```

If the before snapshot is missing, write: `缺少调整前 baseline，无法可靠量化收益`.
