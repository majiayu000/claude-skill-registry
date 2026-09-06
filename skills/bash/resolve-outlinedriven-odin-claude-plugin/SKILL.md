---
name: resolve
description: 'Use when addressing review feedback: analyze mode classifies comment validity, reception mode applies accepted items with tests and drafts pushback. Not for GitHub PR threads: use resolve-pr-feedback.'
---

# Resolve

## Contract

| Field | Bound contract |
|---|---|
| Trigger | addressing review feedback or analyzing whether a comment is valid; for GitHub PR threads use resolve-pr-feedback |
| Authority | Reversible local. Mode analyze is read-only. Mode reception writes only local source files, test files, and pushback drafts; rollback is version control or undo. No remote mutation. |
| Side effect | analyze: classification and proposed solutions in chat, no code edits. reception: local edits, tests, and a draft file; no GitHub reply, CI trigger, or issue |
| Done | every comment is classified; analyze: VALID ISSUE / NOT AN ISSUE / NEEDS CLARIFICATION with evidence and a recommended solution for each VALID ISSUE. reception: each item is clarified, implemented locally with its own test, or answered by a drafted pushback |

## Inputs

- Mode: `analyze` or `reception`. Required. Default `analyze` when the user asks only whether comments are valid.
- Feedback: the raw review comment(s), PR thread, or inline suggestion. Required.
- Code under review: the relevant source files or their location. Required.
- PR or issue thread: the full review context. Optional; use when available.

## Procedure

1. Parse every review comment into an isolated unit. Do not combine, rephrase, or infer unstated items. Done when: each comment stands as a separate item, or the run stops with "No comments supplied" on an empty or unparseable list.

2. Read the referenced code. Mode analyze: use only read-only tools (`grep`, `read`, `glob`, or shell equivalents such as `eza`, `rg`, `fd`, `head`, `tail`); never invoke `bash` write operations (`mkdir`, `touch`, `rm`, `cp`, `mv`, `git add`, `git commit`, `npm install`, redirects `>`, `>>`, or file-creating heredocs) or any tool with write, rename, delete, or staging arguments. Mode reception: read freely; writes are confined to steps 5 and 6. Done when: the code context for each item is read, or the item is marked unreadable.

3. Clarify each item to a concrete statement. Mode reception: resolve the precise intent from context or by asking the user; stop on any item that cannot be resolved to an implementable statement. Done when: every item is a concrete, assessable statement.

4. Classify each item. Done when: every item carries exactly one classification with evidence.
   - Mode analyze:
     - VALID ISSUE: the concern is confirmed by the code. Propose three distinct solutions with trade-offs and name the recommended one with justification.
     - NOT AN ISSUE: the concern is not supported by the code or contradicts project patterns. Supply evidence from the code.
     - NEEDS CLARIFICATION: the comment cannot be assessed without additional context. State exactly what is missing.
     - Stop before proposing solutions for any comment classified NOT AN ISSUE or NEEDS CLARIFICATION.
   - Mode reception:
     - Accepted: the suggestion aligns with the codebase and the user's intent.
     - Questionable: the suggestion is technically incorrect, out of scope, or conflicts with design intent.

5. Mode reception: apply accepted items one at a time. Apply the change to the relevant source file, write or update a test that covers the change, and verify the test passes before moving to the next item. Done when: each accepted item is implemented with a passing test.

6. Mode reception: draft factual pushback for questionable items in a local draft file. State the specific reason the suggestion is not accepted, such as a design conflict, incorrect assumption, or scope mismatch. Do not post it. Done when: each questionable item has a drafted reply.

7. Stop. Do not post any GitHub reply, open any issue, trigger any CI pipeline, or otherwise mutate any remote system. Done when: no remote state has changed.

## Failure and recovery
- Empty input: return "No comments supplied" and stop.
- Inaccessible code: if the referenced location cannot be read, classify the comment NEEDS CLARIFICATION in analyze mode, or report it unclarified in reception mode, with the specific access failure as the missing context.
- Unresolvable ambiguity: analyze: classify NEEDS CLARIFICATION; do not guess intent or invent a fix. reception: stop and report which item cannot be clarified to a concrete statement; do not implement it.
- Partial-result rule: if one comment cannot be processed, continue with the remaining comments and report the failure for the unprocessed one. Do not claim the whole batch succeeded.
- User rejects an accepted item (reception): skip that item; continue with the remaining items.
- Implementation blocked (reception): report the specific technical obstacle; do not widen scope.
- Test fails (reception): fix the implementation, not the test. If the test is wrong, report it and stop.
- Remote mutation attempted: refuse; log the blocked action.
- Non-converged result: any unresolved failure produces a report listing unresolved items and blocked actions. The done predicate does not hold.

## Output
- Mode analyze: per comment, in order: Comment, Status (VALID ISSUE | NOT AN ISSUE | NEEDS CLARIFICATION), then the status-specific block: for VALID ISSUE three numbered Solutions with trade-offs and the Recommended pick; for NOT AN ISSUE the Reason and Evidence; for NEEDS CLARIFICATION the exact Missing information. Stop after the last comment; emit no summary or overall-PR content.
- Mode reception: a local report listing every feedback item, its classification (accepted or questionable), the actions taken for each accepted item, and the location of any drafted pushback. No remote state is changed.
