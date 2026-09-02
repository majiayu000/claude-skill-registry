---
name: issue-intake
description: 'Use when filing an approved task spec as a GitHub issue with a local archive and optional worktree implementer. Don''t use for spec drafting without human interrogation and redaction gates.'
disable-model-invocation: true
---

# Issue intake

## Contract

| Field | Bound contract |
|---|---|
| Trigger | the user runs /issue-intake with a task idea |
| Authority | human-only; require explicit human invocation and preview the filing target and consequence before any remote publication |
| Side effect | a filed GitHub issue plus a local spec archive and an optional worktree implementer |
| Done | the spec is filed and archived with frontmatter, with any requested implementer spawned |

## Inputs

- A task idea, supplied by the user at invocation. Required; if absent, ask before proceeding.
- A target GitHub repository for filing, resolvable from the current `gh` context or stated by the user. Required before any remote mutation.
- An optional request to spawn a worktree implementer bound to the filed issue.

## Procedure

1. Receive the task idea from the `/issue-intake` invocation. If none was supplied, ask the user for one and stop until it is provided. Done when: one task idea is in hand.
2. Interrogate the user to resolve scope: problem statement, acceptance criteria, constraints, and explicit out-of-scope boundaries. Ask targeted questions; stop when the user confirms the spec is complete. Done when: the user confirms the spec covers all four scope dimensions.
3. Draft the spec as a GitHub issue body from the confirmed scope. Done when: the draft issue body states the problem, acceptance criteria, constraints, and out-of-scope boundaries.
4. Apply redaction gates: scan the draft for secrets, credentials, private identifiers, and any content the user has not approved for public publication. Show the user the redacted draft and the list of redactions. Proceed only after explicit human approval of the redacted form. Done when: the user approves the redacted draft.
5. Preview the filing target (repository and issue title) and the consequence: a public GitHub issue will be created. Require explicit human confirmation before filing. Done when: the user confirms the filing target and consequence.
6. File the approved, redacted spec as a GitHub issue in the target repository using the user's authenticated `gh` context. Done when: a GitHub issue URL is returned.
7. Archive the spec locally as a markdown file with YAML frontmatter capturing the issue URL, title, and filing timestamp, under the project's spec archive location. Done when: the local archive file exists with frontmatter.
8. If the user requested an implementer, spawn a worktree implementer bound to the filed issue. Otherwise stop. Done when: the implementer handle is returned, or no implementer was requested and the skill stops.

## Failure and recovery
- Missing task idea or target repository: stop and ask; perform no mutation.
- Redaction gate finds unapproved publishable content: halt filing, surface the content to the user, re-draft after approval. Never file unredacted content.
- Human does not confirm filing: do not file; retain the local draft only; report blocked with the unfiled draft.
- `gh` filing fails: do not record a fabricated issue URL; report the `gh` error and the unfiled draft; retry only after the user resolves authentication or network.
- Worktree implementer spawn fails: the filing and archive are still complete, so the done predicate holds for them; report the spawn failure separately as a non-blocking partial result.

## Output

The filed GitHub issue URL, the local archived spec file path with frontmatter, and the implementer handle (or an explicit statement that no implementer was requested).
