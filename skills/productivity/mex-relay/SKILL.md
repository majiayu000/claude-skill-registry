---
name: mex-relay
description: Prepare and manage durable MEX team handoffs. Use when the user asks to hand work to a person or team, prepare an end-of-session handoff, save what the next engineer needs, create a MEX Relay, take or close a Relay, or explicitly invokes /mex-relay or $mex-relay. Treat Relay as a memory and context baton, not chat, notifications, task assignment, issue tracking, or a Jira replacement; do not activate for ordinary status messages that are not durable handoffs.
---

# MEX Relay

Prepare durable team handoffs that another engineer can continue from. Never represent a Relay as a sent message or notification.

## Prepare a Relay draft

1. Infer the useful session state: a concise summary, current position, completed work, in-progress work, blockers, unresolved questions, next actions, and relevant decisions, files, code, commits, or external links.
2. Resolve intended recipients against active MEX Members. Never fabricate member IDs.
3. Default to a standalone Relay.
4. Include a Workstream only when a real, relevant Workstream already exists. Preserve it as supported typed context; never invent one or turn Relay creation into Workstream creation.
5. Add optional typed context references only when the referenced IDs, paths, commits, or URLs are known. Never invent provenance.
6. Build one request against the action-scoped runtime contract and run the exact preview.
7. When the user already asked to create, save, or draft the handoff, apply that exact checkout-local draft preview without another confirmation.
8. Return `/relays?view=drafts&draft=<id>` and state that the draft is checkout-local and nothing has been delivered or shared.

Read [references/cli-workflows.md](references/cli-workflows.md) before executing any Relay mutation. Load only the operation being performed.

## Apply the approval policy

- Proceed with read-only member, Workstream, draft, and Relay resolution.
- Treat an explicit create/save/draft request as authorization only for the local draft preview and exact apply.
- Preview a local draft deletion, explain its consequence, and obtain fresh confirmation before applying.
- For publish, take, or close: generate a semantic preview, explain the local-versus-Git-tracked effect, and wait for fresh explicit confirmation. Apply the exact preview unchanged only after confirmation.
- Keep Git commit, push, pull, and staging separate from every MEX authorization.
- Never publish, take, or close merely because this skill activated.

## Preserve lifecycle meaning

- Treat taking as the explicit canonical acknowledge action by an intended recipient.
- Treat closing as “this handoff no longer needs attention.” Do not claim it completes a linked task, issue, pull request, or Workstream.
- After publication, say that Git-tracked Relay and Activity records were written to the working tree. Explain that teammates receive them only after commit/push and their own pull or refresh.
- Never claim that MEX sent a notification, committed, pushed, pulled, staged, assigned work, or completed another system's object.
- When MEX context materially affects the answer, add one concise acknowledgement: `MEX context used: <specific records/files/entities consulted>.`
