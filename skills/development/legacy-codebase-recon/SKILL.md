---
name: legacy-codebase-recon
description: |-
  Investigate unfamiliar legacy code before edits. Triggers: legacy module, unknown repo, risky refactor, trace ownership.
  Triggers:
practices:
- pragmatic-programmer
skill_api_version: 1
metadata:
  tier: judgment
  stability: stable
  dependencies: []
  internal: true
context:
  window: isolated
  intent:
    mode: task
  sections:
    include:
      - TASK
      - INTEL
output_contract: "stdout: legacy recon brief with map, evidence, risks, edit boundary, and validation plan"
user-invocable: false
hexagonal_role: generic
consumes:
  - repo-context
produces:
  - legacy-recon-brief
context_rel: []
---

# Legacy Codebase Recon

Use this skill before changing unfamiliar legacy code. The job is to reduce uncertainty by tracing history, ownership, seams, invariants, dead paths, and behavioral evidence before editing.

The outcome is not a patch. The outcome is a short recon brief that says what is known, what is inferred, what remains unknown, and where an edit can be made with the least risk.

## When To Use

Use this when a task asks for work in an old, inherited, poorly documented, high-risk, or unfamiliar area. It also applies when the requested change crosses ownership boundaries, touches old abstractions, deletes apparently unused code, or depends on behavior that is not already proven by tests.

Do not use this as a substitute for direct implementation when the code is already understood and the edit is local, obvious, and covered by tests.

## Operating Rules

Start by protecting the current worktree. Run a status check and treat uncommitted changes as user work unless the user says otherwise.

Do not edit production code during recon. It is acceptable to run read-only searches, inspect history, run tests, and create temporary local scratch artifacts that are removed before the final answer.

Prefer direct evidence over narrative. Executable code, tests, generated artifacts, runtime behavior, and current schemas outrank stale docs and comments.

Separate facts from inferences. If ownership, intent, or deadness cannot be proven, mark it unknown instead of filling the gap with a plausible story.

## Recon Workflow

1. Define the boundary.

   Identify the requested behavior, candidate files, relevant packages, entrypoints, and nearby tests. Capture the initial state with commands such as `git status --short`, `rg --files`, and targeted `rg` searches.

2. Map the code.

   Find callers, callees, configuration inputs, data models, generated files, migrations, feature flags, queues, external APIs, and persistence boundaries. Name the seams where control or data crosses modules.

3. Trace history and ownership.

   Use focused history commands such as `git log --follow -- <path>`, `git blame -L <range> <path>`, release notes, linked issue IDs, and PR references when available. Record the strongest ownership signal found; otherwise say ownership is unknown.

4. Prove behavior.

   Look for tests, fixtures, snapshots, logs, CLI behavior, API contracts, or production-facing documentation that demonstrate the current behavior. Run narrow tests when practical. If behavior is only implied by code reading, label it as an inference.

5. Extract invariants.

   List the rules that must remain true: schema compatibility, locking and ordering assumptions, idempotency, security checks, lifecycle states, feature flag meanings, error contracts, and backward compatibility obligations.

6. Classify dead paths carefully.

   Treat code as dead only after checking references, dynamic dispatch, build tags, configuration, generated callers, plugin loading, reflection, serialized names, and historical usage. Use confidence labels: confirmed, likely, unlikely, or unknown.

7. Decide edit readiness.

   End with a proposed edit boundary, the validation needed after editing, and the main risks. If the boundary is still unclear, ask for the missing decision instead of making a broad change.

## Evidence Standard

Every claim that affects the edit plan should cite one of:

- A file and line reference.
- A command result.
- A test, fixture, schema, or generated artifact.
- A commit, tag, or release note.
- A clearly labeled inference from multiple weaker signals.

Avoid broad claims such as "unused", "owned by platform", or "safe to remove" unless the evidence supports that level of certainty.

## Output Format

Return this shape before implementation:

```text
## Recon Brief
Objective:
Map:
Behavioral Evidence:
History and Ownership:
Invariants:
Dead or Dormant Paths:
Risks:
Edit Boundary:
Validation Plan:
Open Questions:
```

Keep the brief compact. Use bullets only where they improve scanability, and include file references for the important claims.

## Handoff To Editing

After the brief, proceed to implementation only when the edit boundary is narrow enough to defend. If the user asked for a full end-to-end fix, continue into the edit after recon unless the brief exposes a blocker or a decision that only the user can make.

## Examples

**User says:** "This old billing cleanup path looks unused. Remove it."

Run recon first: find all references, check flags and scheduled jobs, inspect history, identify serialized names or external callers, then report whether removal is confirmed, likely risky, or unresolved.

**User says:** "Patch this legacy parser, I do not know why it works this way."

Trace parser entrypoints, fixtures, grammar assumptions, prior commits, and failing behavior before changing the parser.

## Troubleshooting

| Problem | Response |
|---|---|
| No tests cover the area | State the gap and propose a narrow characterization test or manual reproduction. |
| Ownership is unclear | Cite the strongest available history signal and mark ownership unknown. |
| Search misses dynamic callers | Check configuration, generated code, plugin registries, reflection, serialized names, and build tags. |
| The likely edit is broad | Stop at a smaller edit boundary or ask for a product decision. |
