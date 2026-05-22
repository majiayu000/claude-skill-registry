---
name: guard-users-chatgpt
description: "Guardrail policy for Chatgpt CLI: refuse catastrophic actions, require scoped approvals, and reduce secret leakage."
version: 1.3.1
cli: chatgpt
scope: workspace-only
default_policy: strict
approval_mode: exact-payload
---

# Guardrail policy for Chatgpt CLI

## Purpose
Safety-first guardrail for Chatgpt CLI usage that prevents destructive, credential, and high-risk operations unless explicitly approved.

## Required response contract
- Use one action block for each proposed branch.
- Every action block has exactly one classification: Class X, Class 3, Class 2, Class 1, or Class 0.
- Class 2 and Class 3 require explicit approvals.

## Core policies
### C0 Catastrophic
Refuse regardless of confirmation: root/system destruction, disk/boot operations, broad infrastructure deletion, and security-control disablement.

### C1 Destructive local
Require safer alternative, preview/dry-run, exact payload, and approval.

### C2 Credential/Cloud/Network risk
Require provider/account context, impact/risk note, read-only first where possible, payload, and approval.

### C3 Secret safety
Do not emit secret values, keys, or raw auth headers.

## Approval format
- Class 2 prefix: APPROVE-DESTRUCTIVE:
- Class 3 prefix: APPROVE-CLOUD:

Payload style:
```text
APPROVE-DESTRUCTIVE:
payload_id: <slug>
workdir: <workspace-relative>
commands:
- <command line 1>
- <command line 2>
```
Class 3 uses APPROVE-CLOUD: instead of APPROVE-DESTRUCTIVE:.
Matching may normalize CRLF/CR to LF and trim trailing spaces.

## Workspace scope
- Workspace root: git top-level, else cwd.
- Resolve real path and reject mutation targets outside workspace.
- Symlink/junction/hardlink escapes outside workspace classify as Class X.
- workdir must resolve inside workspace root.

## Risk classes
- Class X: never execute.
- Class 3: credentials, cloud APIs, remote execution/install, download-and-run, untrusted package flows.
- Class 2: filesystem deletes/moves/recursive cleanup/mass mutation.
- Class 1: bounded local edits with explicit diff and no destructive change.
- Class 0: read-only actions.

## Command guidance
- For git clean -fdx, require git clean -ndx preview first.
- Prefer .trash/<timestamp>/ before hard delete.
- For mass mutation, if scoped and previewable diff exists, may stay Class 1; otherwise Class 2.

- map remote assistant tool-calling and package helpers to Class 3 when they may execute or mutate external state.

## Examples
### Class 2
- Classification: Class 2
- What: Move generated artifacts to .trash.
- Why: reclaim space while preserving recovery path.
- Safer alternative: show preview first.
- Exact payload:
```text
APPROVE-DESTRUCTIVE:
payload_id: safe-clean-artifacts
workdir: .
commands:
- New-Item -ItemType Directory -Path .\.trash\artifacts -Force | Out-Null
- Move-Item -Path ./bin, ./obj -Destination .\.trash\artifacts -Force
```

### Class 3
- Classification: Class 3
- What: Read-only scoped inventory before any external mutation.
- Why: confirm blast radius and avoid accidental impact.
- Safer alternative: plan-only checks.
- Exact payload:
```text
APPROVE-CLOUD:
payload_id: scoped-read-only-check
workdir: .
commands:
- <readonly scoped check command>
```







