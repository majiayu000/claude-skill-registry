---
name: aiken-dex-security-audit-operator
description: "Operator skill: run local Aiken build/test commands and capture evidence for the audit. Manual invoke only."
metadata:
  manual: "true"
---

# aiken-dex-security-audit-operator

## Rule

This is for "hands-on-keyboard" runs (aiken check/build) and collecting logs. Only run commands the user explicitly requests.

## Procedure

1. Confirm repo path + commit
   - `git rev-parse --short HEAD`
2. Record tool versions
   - `aiken --version`
3. Run checks
   - `aiken check`
   - `aiken build`
4. If tests fail: capture failing test/property name, file/line, and minimal repro info.
5. Feed outputs into the audit report evidence section.
