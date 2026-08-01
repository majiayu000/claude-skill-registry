---
name: mutual-sync
description: 'Use when user, agent, and codebase may hold different pictures of the current state: before substantive work after a gap, or mid-session when parties talk past each other. Triggers: "mutual sync", "sync up", "are we on the same page", stale user claims about the code, refuted agent assumptions.'
---

# Mutual Sync

Ground the three parties in one shared picture of the current state before proceeding: the user's mental model, the agent's working model, and the actual codebase. A desync is any load-bearing claim about current state that one party holds and another would dispute. Facts are the agent's job; the user is consulted only where the user is the authority.

## Two entry situations, one workflow

- **Pre-work ritual**: invoked before substantive work (a new task, a return after a gap). The claim set seeds from the task: what must be true about the code for the planned work to make sense.
- **Mid-session repair**: invoked when the conversation shows desync: the user references state that no longer holds, or an agent assumption got refuted. The claim set seeds from the contested claims in the conversation.

Detect which situation applies from context; never ask. Same loop either way.

## The sync loop

1. **Resolve scope.** Sync around the named topic, or infer it from the task at hand. Bare invocation with no inferable topic: fire one blocking single-select proposing 2-3 candidate scopes.
2. **Ground the codebase leg.** Verify each claim in the claim set against the repo with targeted reads and greps, topic-scoped, never a whole-repo scan. Then run the repo-delta check: `git log --oneline -15` and `git status --short` (read-only). New commits since the last shared point or a dirty tree go into the ledger as facts; the ground may have moved under both parties.
3. **Exchange claims.** Present the agent's model as short numbered claims, each carrying `file:line` evidence or the label `[unverified]`. Alongside, ask at most 3 targeted questions where the user is the likely authority: intent, external state (deploys, sibling repos, other sessions), recent decisions. Follow the AskUserQuestion contract in `skills/askme/SKILL.md`; use an open question only where the answer is narrative. Never ask the user for a fact a read or grep can answer.
4. **Arbitrate.** Code is the arbiter for anything verifiable in-repo: corrections carry `file:line` evidence and flow both ways; a stale user belief and a wrong agent assumption get the same treatment. The user is the arbiter for intent and for external facts the agent cannot see; record those as trusted-unverified assumptions. If a party disputes a claim after evidence, record the dissent in the ledger and move on; do not re-litigate.
5. **Emit the ledger.** In-chat markdown, three sections:
   - **Agreed facts**: claim plus evidence (`file:line` or `[user-attested]`)
   - **Corrected beliefs**: who held it, what the evidence showed
   - **Open assumptions**: trusted-unverified and disputed items, each with its owner
6. **Confirm.** One blocking single-select: "Shared context confirmed (Recommended)" / "Corrections needed". On corrections, fold them into the claim set and rerun from step 2 for the affected claims only. Do not proceed to substantive work on an unconfirmed ledger.
7. **Offer persistence once.** After confirmation, offer to persist the shared context. If accepted, invoke the `handoff` skill; mutual-sync writes no files of its own.

## Distinction from neighbors

- **vs `askme` / `batch-ask-me`**: those align user and agent on decisions to make; mutual-sync aligns all three parties on facts about current state.
- **vs `drift-detect` / `sync-docs`**: those diff artifacts against code; no user leg, no dialogue.
- **vs `contexts` / `onboard`**: one-way orientation where the agent or user learns the codebase; no mutual verification, no ledger.
- **vs `handoff`**: handoff persists state for the next session; mutual-sync verifies state in this one, and routes persistence to handoff.

## Anti-patterns

- Asking the user for anything a grep can answer.
- Forcing consensus on an external fact the agent cannot verify.
- Whole-repo orientation scans; the sync is topic-scoped plus the delta check.
- Skipping the confirmation gate because the ledger "looks obviously right".
- Writing a new persistence format instead of routing to `handoff`.
