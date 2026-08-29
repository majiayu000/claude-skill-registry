---
name: interview-framework-codex
description: Internal Ralph Specum contract for Codex phase interviews, skill manifests, approval, and delegation gates. Phase coordinators load this skill directly; users do not invoke it as a workflow phase.
metadata:
  surface: internal
---

# Codex interview framework

Run every normal-mode `start`, `triage`, `research`, `requirements`, `design`, and `tasks` phase through `references/algorithm.md` and `references/domain-modeling.md`.

## Completion criterion

Delegate only after all of these conditions hold for one identity tuple:

- `phase`, `interviewId`, `discoveryRevision`, and `contextDigest` match in state and in the delegation packet.
- The selected skill manifest has status `complete` or `partial_warned`.
- The phase interview has status `complete` or `skipped` after explicit final approval.
- `phase_gate.py check-delegation` succeeds.

Quick mode uses the same identity tuple. It requires a current `complete` or `partial_warned` manifest plus an interview receipt with status `bypassed_quick` and `quickAuthorization.source: "--quick"`. Quick mode bypasses interview questions only. Discovery, contract load, parent delegation provenance, artifact-agent reload, and `check-agent-write` still apply.

## Hard boundaries

- Ask only critical user decisions that can change phase scope, externally visible behavior, acceptance, architecture, sequencing, or material risk.
- Inspect code, configuration, state, prior artifacts, and selected skill contracts for facts. Do not ask the user for discoverable facts or setup and administration choices.
- Ask the whole currently unblocked critical frontier. Split a frontier only when Codex's native user-input tool limit requires another batch. The current limit is three questions per call.
- Put the recommended option first and state its tradeoff. Offer only viable alternatives.
- Persist each partial answer before asking the next frontier.
- Treat control-only replies such as `apply the changes`, `continue`, `proceed`, and `go ahead` as no answer to an active interview question.
- Treat bare `skip` during an active question as an instruction to finish the remaining interview with stated defaults and assumptions. Present the final approval gate before delegation.
- Delegate in the same turn after the user explicitly chooses `approve and delegate`.
- During artifact review, treat `apply the changes` as a revision request. Delegate the revision and remain at the artifact approval gate.
- Apply domain-language modeling during the grill. Challenge conflicting or vague terms, use concrete boundary scenarios, and record resolved domain terms without creating an ADR.

## Preload boundary

Load selected skill bodies and required current-work references as contracts. During preload, collect constraints, vocabulary, checks, and conflicts. Start no task action prescribed by a loaded domain skill until the phase interview is approved and the delegation gate passes.

If this core skill, its algorithm reference, or its domain-modeling reference cannot be read and hashed, record `phaseSkillLoad.status: "core_failed"`, report the failure, and stop. Record domain-skill load failures in `warnings` and `failures`, use `partial_warned`, and continue. Turn unresolved material conflicts between loaded contracts into first-layer interview decisions.
