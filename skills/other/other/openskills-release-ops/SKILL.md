---
name: openskills-release-ops
description: Prepare and validate OpenSkills release readiness across runtime, bindings, examples, and regression gates with a deterministic checklist and go/no-go outcome.
---

# OpenSkills Release Ops

Use this skill when preparing a release candidate or validating publish readiness.

## Release Gates

1. Runtime compile and test status
2. Binding build status (TS and Python)
3. Example-agent sanity checks
4. Changelog/version consistency
5. Packaging/publish prerequisites

## Core Verification

```bash
cargo check -p openskills-runtime
cargo test -p openskills-runtime
```

## Evidence Required

- Test command outputs summarized
- Any skipped gates with reason
- Known risks and rollback notes

## Go/No-Go Decision

Return one of:

- `GO` (all required gates pass)
- `GO with risks` (non-blocking issues documented)
- `NO-GO` (blocking issues remain)

Include explicit blockers and exact repro commands.
