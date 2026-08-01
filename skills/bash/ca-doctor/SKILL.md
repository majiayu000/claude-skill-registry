---
name: ca-doctor
description: Verify the active host install, package, command ownership, enforcement, wrapper self-test, and active-dispatch coverage gap. Read-only.
argument-hint: (none)
---

# /ca-doctor — install health

Silent dormancy is the worst failure shape this plugin has: the gates look installed but never fire.
This command proves the active host is healthy and reports every non-OK finding with an exact
remediation.

## Flow

1. The `/ca-doctor` alias has already run the extension's structured Pi doctor report before sending
   this generated skill. Present the `<codearbiter-doctor-report>` block below verbatim.
2. The report inspects, without granting trust: active Git package origin/version, exact Pi CLI and
   module package identity, stable Pi/Node/Python support, shared-core and bridge paths, command and
   native-equivalent skill-expansion ownership, child/ambient-marker state, and final wrapper sources.
3. Its `wrapper-self-test` row submits only `git add --all --dry-run` directly to the stored governed
   Pi bash wrapper. The exact shared-core `[H-03]` block is healthy and cannot stage files; execution
   or a different block is unhealthy. This self-test does not traverse Pi's active dispatcher. Do not
   rerun or respell it.
4. Its `active-dispatch` row remains degraded because supported Pi 0.80.5/0.80.10 public extension
   APIs cannot submit that deterministic call through the active dispatcher. PI-AC-28 remains blocked
   until supported-version real-host promotion/CI evidence closes the gap.

## Remediation ladder

1. Restart Pi so package resources and final wrappers register in one fresh process.
2. Reinstall `ca-pi` from the approved pinned Git tag. For project-local packages, inspect `/trust`
   and grant trust only if you accept that source; codeArbiter never grants it.
3. If dormancy was intended, `/ca-init` opts the repository in.

## When NOT to use

- Scaffold state only → `/ca-init --check`.
- Project progress, not install health → `/ca-status`.

## Hard gate

Read-only. MUST NOT create markers, stage files, grant trust, weaken a block, or retry the
wrapper self-test with different spelling. MUST preserve the degraded active-dispatch diagnosis until
supported-version real-host promotion/CI evidence closes PI-AC-28.
