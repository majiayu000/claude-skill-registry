---
name: shell-review
description: |
  Audit shell scripts for correctness, portability, and common pitfalls.

  Triggers: shell script, bash, sh, script review, pipeline, exit code
  Use when: reviewing shell scripts, CI scripts, hook scripts, wrapper scripts
  DO NOT use when: creating new scripts - use attune:workflow-setup
category: build
tags: [shell, bash, posix, scripting, ci, hooks]
tools: [Read, Grep, Bash]
complexity: intermediate
estimated_tokens: 200
progressive_loading: true
dependencies: [pensive:shared, imbue:evidence-logging]
modules:
  - exit-codes
  - portability
  - safety-patterns
---

# Shell Script Review

Audit shell scripts for correctness, safety, and portability.

## Quick Start

```bash
/shell-review path/to/script.sh
```

## When to Use

- CI/CD pipeline scripts
- Git hook scripts
- Wrapper scripts (run-*.sh)
- Build automation scripts
- Pre-commit hook implementations

## Required TodoWrite Items

1. `shell-review:context-mapped`
2. `shell-review:exit-codes-checked`
3. `shell-review:portability-checked`
4. `shell-review:safety-patterns-verified`
5. `shell-review:evidence-logged`

## Workflow

### Step 1: Map Context (`shell-review:context-mapped`)

Identify shell scripts:
```bash
# Find shell scripts
find . -name "*.sh" -type f | head -20
# Check shebangs
grep -l "^#!/" scripts/ hooks/ 2>/dev/null | head -10
```

Document:
- Script purpose and trigger context
- Integration points (make, pre-commit, CI)
- Expected inputs and outputs

### Step 2: Exit Code Audit (`shell-review:exit-codes-checked`)

@include modules/exit-codes.md

### Step 3: Portability Check (`shell-review:portability-checked`)

@include modules/portability.md

### Step 4: Safety Patterns (`shell-review:safety-patterns-verified`)

@include modules/safety-patterns.md

### Step 5: Evidence Log (`shell-review:evidence-logged`)

Use `imbue:evidence-logging` to record findings with file:line references.

Summarize:
- Critical issues (failures masked, security risks)
- Major issues (portability, maintainability)
- Minor issues (style, documentation)

## Output Format

```markdown
## Summary
Shell script review findings

## Scripts Reviewed
- [list with line counts]

## Exit Code Issues
### [E1] Pipeline masks failure
- Location: script.sh:42
- Pattern: `cmd | grep` loses exit code
- Fix: Use pipefail or capture separately

## Portability Issues
[cross-platform concerns]

## Safety Issues
[unquoted variables, missing set flags]

## Recommendation
Approve / Approve with actions / Block
```

## Exit Criteria

- Exit code propagation verified
- Portability issues documented
- Safety patterns checked
- Evidence logged
