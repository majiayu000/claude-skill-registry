---
name: pawl-review
description: Run one fresh, read-only, nonce-bound
---
# Pawl Review

Run a single independent reviewer execution. This skill owns the immutable
request, transport-neutral lane result, and evidence handoff. `ao pawl` owns
diversity, panel judgment, commit binding, and admission. A reviewer never fixes
the subject and the author never counts as its own reviewer.

## Route

- Use for a fresh-context or multi-model pawl lane after deterministic tests
  have produced a reviewable commit and diff.
- Use NTM when an attachable warm pane materially helps; use cold Codex/AGY
  adapters when it does not. Gas City may implement the same port inside an
  explicitly selected quest.
- Agent Mail is optional coordination for separate live actors. One local lane
  does not need identity, reservations, or acknowledgements.

## Immutable request

Construct `review-request.v1` with subject id, reviewed `head_sha`, acceptance
contract path and SHA-256, diff path and SHA-256, author context/family,
diversity mode, nonce, evidence directory, and `read_only=true`. Validate both
files against their digests immediately before dispatch. A path without a
content digest is mutable input and must not run.

## Lane execution

1. Discover the selected adapter's live capabilities before changing state.
2. Start a fresh reviewer context. Bind the request fields verbatim and permit
   writes only beneath the evidence directory.
3. Observe terminal state and collect the transcript plus a nonempty evidence
   artifact. Do not infer engagement or success from send acknowledgement.
4. Emit `review-lane-result.v1`: lane/family/context ids, echoed nonce,
   read-only attestation, evidence path, findings, and either CONFIRMED or
   REFUTED semantic judgment.
5. Validate evidence after resolving symlinks. It must be a nonempty regular
   file contained beneath the request evidence directory, and reviewer context
   must differ from author context.

Transport failure is not judgment. Provider loss, timeout, missing evidence,
or malformed markers produce a transport-class result with no semantic
disposition. Never manufacture REFUTED, lower the requested tier, or write a
panel verdict to keep the loop moving.

## Handoff

Hand the validated lane result and evidence path to `ao pawl`. Stop there. The
membrane may CONFIRM, REFUTE, HOLD, or request another lane; this skill has no
authority to choose.

See [the executable behavior contract](references/pawl-review.feature).
