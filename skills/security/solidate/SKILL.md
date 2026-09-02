---
name: solidate
description: 'Use when a user invokes this skill to harden a chosen but tentative artifact into one durable result. Resolves assumptions, names invariants, removes temporary choices, and verifies the stable end state. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Solidate

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants to harden a chosen but tentative artifact into one durable result. |
| Authority | Reversible local write only. No VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Writes the hardened artifact to its existing path via atomic rename. Does not create, move, or delete other files. |
| Done | The chosen artifact is hardened and its stable end state is verified. |

## Inputs

- Artifact (required): the tentative file path supplied by the user. Must exist on disk and be readable as text.
- Assumptions (required): the list of loose or unverified assumptions currently embedded in the artifact.
- Invariants (required): the list of named conditions that must hold true after hardening.
- Temporary choices (required): the list of placeholder or provisional decisions to be resolved and replaced.
- Resolutions (required): for every assumption and every temporary choice, either its resolution or an explicit statement that it is unresolved. Unresolved items block the write.

## Procedure

1. Verify the artifact exists and all inputs are non-empty string collections. Read the artifact path. If the file does not exist or is not readable, stop and report `artifact-not-found`. Confirm each input list (assumptions, invariants, temporary choices) is a non-empty collection of strings. Confirm that every assumption and temporary choice has a corresponding resolution entry. If any input is empty, malformed, or missing a resolution, stop and report `invalid-inputs`. Done when: the artifact is read and all inputs are validated, or the failure class is reported with nothing written.

2. Audit the body and record line ranges for every assumption, temporary choice, and implicit condition. Locate each item within the artifact text and record its line range. Done when: every assumption, temporary choice, and implicit condition carries recorded line ranges.

3. Resolve each item from supplied resolutions or in-artifact evidence. For each assumption, replace it with its supplied resolution or a verified statement derived from in-artifact evidence. For each temporary choice, replace it with its supplied resolution. If any item remains unresolved (no resolution supplied and no in-artifact evidence available), stop and report `blocked-unresolved` with the exact markers. Never write a partially hardened artifact. Name invariants: append or inline an `## Invariants` section listing each invariant with a one-line justification. If the artifact already contains an invariants section, merge without duplication. Done when: every assumption and temporary choice is resolved and every named invariant appears exactly once with a one-line justification, or `blocked-unresolved` is reported with the original untouched.

4. Write the hardened content atomically. Write the hardened content to a sibling temp file (same directory, `.solidate-tmp` suffix), then rename the temp file over the original. The original bytes are retained until the rename succeeds. If the write or rename fails, stop and report `write-failed`; the original artifact is provably unchanged because the rename never happened. Done when: the artifact path holds the hardened content, or `write-failed` is reported with the original unchanged.

5. Re-read and verify the stable end state. Re-read the written file. Confirm: no `[UNRESOLVED` or `[PLACEHOLDER` markers remain; the `## Invariants` section exists and contains every named invariant exactly once; no temporary choice markers remain. If any check fails, stop and report `end-state-unverified` with the failed checks. Done when: the re-read shows no unresolved or placeholder markers, an Invariants section containing every named invariant exactly once, and no temporary choice markers, or `end-state-unverified` names the failed checks.

## Failure and recovery

| Failure class | Condition | Result |
|---|---|---|
| `artifact-not-found` | Artifact path does not exist or is unreadable | Stop; do not write. |
| `invalid-inputs` | Assumptions, invariants, or temporary choices are empty, malformed, or missing resolutions | Stop; do not harden. |
| `blocked-unresolved` | One or more assumptions or temporary choices have no resolution and no in-artifact evidence | Stop; original artifact untouched. Report the exact unresolved items. |
| `write-failed` | Disk write or rename fails | Stop; original artifact provably unchanged because the rename never happened. |
| `end-state-unverified` | Unresolved markers, missing invariants, or remaining placeholders after write | Stop; do not claim done. Report which checks failed. |

## Output

The hardened artifact is written back to its original path and the skill returns one confirmation line in fixed order: `Hardened: <artifact-path>`, assumptions resolved count, invariants named count, temporary choices resolved count, `End state verified: true`. On `end-state-unverified` it lists the failing checks and does not claim the done predicate. On `blocked-unresolved` it lists the unresolved items and confirms the original is untouched.
