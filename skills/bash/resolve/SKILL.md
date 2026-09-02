---
name: resolve
description: 'Use when addressing review feedback or analyzing whether a comment is valid. Classifies each comment VALID ISSUE / NOT AN ISSUE / NEEDS CLARIFICATION with evidence and a recommended solution. Not for GitHub PR review threads — use resolve-pr-feedback.'
---

# Resolve

## Contract

| Field | Bound contract |
|---|---|
| Trigger | addressing review feedback or analyzing whether a comment is valid; for GitHub PR threads use resolve-pr-feedback |
| Authority | no file, VCS, credential, paid, published, deployed, or remote mutation |
| Side effect | produces analysis and proposed solutions in chat; no code edits and no remote calls |
| Done | each comment classified VALID ISSUE / NOT AN ISSUE / NEEDS CLARIFICATION with evidence and recommended solution |

## Inputs

The user supplies review comments — the text of each comment and any associated code context. The user also supplies the location in the codebase under review, or the model reads it directly using only read-only tools.

## Procedure

1. Parse every review comment into an isolated unit. Stop on an empty or unparseable comment list; return "No comments supplied" without hallucinating any.

2. For each comment, explore the referenced code location using only read-only tools: `grep`, `read`, `glob`, or shell equivalents (`eza`, `rg`, `fd`, `head`, `tail`). Never invoke `bash` with write operations (`mkdir`, `touch`, `rm`, `cp`, `mv`, `git add`, `git commit`, `npm install`, redirect operators `>`, `>>`, or heredocs that create files). Do not use `ast-grep` or any tool with write, rename, delete, or staging arguments.

3. Classify each comment:
   - **VALID ISSUE** — the concern is confirmed by the code. Propose three distinct solutions with trade-offs and name the recommended one with justification.
   - **NOT AN ISSUE** — the concern is not supported by the code or contradicts project patterns. Supply evidence from the code.
   - **NEEDS CLARIFICATION** — the comment cannot be assessed without additional context. State exactly what is missing.

4. Stop before proposing solutions for any comment classified NOT AN ISSUE or NEEDS CLARIFICATION.

## Failure and recovery
- Empty input: return "No comments supplied" and stop.
- Inaccessible code: if the referenced location cannot be read, classify the comment NEEDS CLARIFICATION with the specific access failure as the missing context.
- Unresolvable ambiguity: classify NEEDS CLARIFICATION; do not guess intent or invent a fix.
- Partial-result rule: if one comment cannot be processed, continue with the remaining comments and report the failure for the unprocessed one. Do not claim the whole batch succeeded.
- Non-mutation rule: no edit, write, commit, push, deployment, credential use, or remote call is ever performed.

## Output
Per comment, in order: Comment, Status (VALID ISSUE | NOT AN ISSUE | NEEDS CLARIFICATION), then the status-specific block — for VALID ISSUE three numbered Solutions with trade-offs and the Recommended pick; for NOT AN ISSUE the Reason and Evidence; for NEEDS CLARIFICATION the exact Missing information. Stop after the last comment; emit no summary or overall-PR content.
