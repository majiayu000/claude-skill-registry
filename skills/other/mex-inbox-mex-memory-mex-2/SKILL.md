---
name: mex-inbox
description: Prepare and manage governed MEX Inbox proposals for durable Spec-family knowledge. Use when the user clearly asks to capture, create, save, or draft a MEX product Spec, requirement, constraint, acceptance criterion, or durable product-spec decision for team review, or explicitly invokes /mex-inbox or $mex-inbox. Do not use for email inboxes, generic notes, vague brainstorming, OpenAPI or test specs mentioned only by the word "spec," architecture pages, conventions, patterns, Workstreams, Relays, arbitrary Wiki pages, or generic memory.
---

# MEX Inbox

Prepare governed Spec-memory proposals. Treat Inbox as a proposal workflow, not email and not a general Wiki mutation system.

## Keep the scope honest

- Create exactly one `spec.create` or `spec.update` change per draft.
- Support only `spec`, `requirement`, `constraint`, and `acceptance_criterion` entities.
- Reject unsupported durable knowledge honestly. Do not silently translate architecture, conventions, patterns, Workstreams, Relays, or arbitrary Wiki pages into Specs.
- Require a clear durable claim. Do not capture unresolved brainstorming as team memory.

## Prepare a draft

1. Distill the durable knowledge, rationale, and useful evidence from the conversation.
2. Decide whether it creates a new Spec-family entity or updates an existing exact entity.
3. For an update, resolve the canonical target and current revisions before drafting. Never guess an ID or revision.
4. Preserve useful files, code, commits, entities, and external links as evidence only when actually available. Never invent provenance, authors, dates, events, or history.
5. Build one request against the action-scoped runtime contract.
6. Run the exact preview flow and summarize the human effect before technical details.
7. When the user already asked to create, save, or draft it, apply that exact successful checkout-local draft preview without asking again.
8. Return `/inbox?view=drafts&draft=<id>` and state that the draft is checkout-local, nothing was published or shared, and review or publication happens in Hub.

Read [references/cli-workflows.md](references/cli-workflows.md) before executing any Inbox mutation. Load only the operation being performed.

## Apply the approval policy

- Proceed with read-only list, show, and target resolution.
- Treat an explicit create/save/draft request as authorization only for the local draft preview and exact apply.
- Preview a local draft deletion, explain that the checkout-local draft will be removed, and obtain fresh confirmation before applying.
- For publish, approve, reject, withdraw, mark stale, or repair: create a semantic preview, explain the local-versus-Git-tracked effect, and wait for fresh explicit confirmation. Apply the exact preview unchanged only after confirmation.
- Keep Git commit, push, pull, and staging separate from every MEX authorization.
- Never approve or publish merely because this skill activated.

## Report effects precisely

- Lead with what the proposal means to a person. Do not expose envelopes, hashes, revision machinery, or raw diffs unless diagnosis requires them.
- After a local draft write, say exactly what changed and that it remains checkout-only.
- After a canonical write, say which Git-tracked MEX artifacts were written to the working tree and that commit/push is still required to share them. Never claim that MEX committed or pushed.
- When MEX context materially affects the answer, add one concise acknowledgement: `MEX context used: <specific records/files/entities consulted>.`
