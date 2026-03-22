---
name: atm10-change-protocol
scope: project
status: scaffold
summary: Thin atm10 overlay for bounded change execution with repo-relative paths, commands, and explicit local approval notes.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0001
  - AOA-T-0002
---

# atm10-change-protocol

## Intent

Use this skill to adapt `aoa-change-protocol` to an `atm10-*` repository without changing the base workflow meaning.

## Trigger boundary

Use this skill when:
- the base `aoa-change-protocol` workflow is already correct, but an `atm10-*` repo needs repo-relative paths, commands, or local approval notes
- a bounded non-trivial change still needs an explicit plan and verification path inside the local repo
- a contributor needs a thin local overlay rather than a fresh workflow design

Do not use this skill when:
- the task really needs a broader playbook or scenario bundle rather than a thin overlay
- the work would introduce new upstream technique meaning instead of adapting the local repo surface
- a more specific risk skill is still the clearer fit, such as `aoa-dry-run-first`, `aoa-safe-infra-change`, or `aoa-approval-gate-check`
- the task does not need repo-relative local adaptation and the base skill can be used directly

## Inputs

- target goal and touched local surface
- repo-relative source-of-truth files
- repo-relative commands or checks
- local approval or review rules
- base skill reference

## Outputs

- bounded local change plan
- repo-relative command or path sketch
- verification note for the local repo surface
- concise handoff on what stays downstream and explicit

## Procedure

1. start from `aoa-change-protocol` rather than rewriting the workflow
2. name the repo-relative files, commands, and approval posture that matter locally
3. keep the adaptation bounded to the local repo surface under change
4. preserve the base `plan -> scoped change -> verify -> report` shape
5. make explicit what still requires downstream human approval or repo-specific judgment

## Contracts

- preserve the base skill meaning
- keep paths and commands repo-relative
- keep local authority explicit
- keep the overlay reviewable and public-safe

## Risks and anti-patterns

- hiding downstream authority inside vague local notes
- turning a thin overlay into repo doctrine or a scenario bundle
- naming local commands without enough verification context
- silently changing the base workflow instead of adapting it

## Verification

- confirm the base skill is still the correct workflow
- confirm repo-relative paths and commands are named explicitly
- confirm approval posture is still downstream and explicit
- confirm the adaptation remains bounded to the local repo surface

## Technique traceability

Manifest-backed techniques:
- AOA-T-0001 from `8Dionysus/aoa-techniques` at `ea49abf4f7e96506feed56eb87a9052cbe4408a5` using path `techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `ea49abf4f7e96506feed56eb87a9052cbe4408a5` using path `techniques/docs/source-of-truth-layout/TECHNIQUE.md` and sections: summary

## Adaptation points

- repo-relative change surfaces
- local commands and verification steps
- local source-of-truth files
- local approval or review notes
