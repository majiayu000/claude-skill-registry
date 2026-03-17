---
name: swarm-consensus
description: Implement voting mechanisms (majority, weighted) to resolve inter-agent conflicts.
role: orch-coordinator
triggers:
  - vote
  - consensus
  - conflict resolution
  - majority rule
  - tie breaker
---

# swarm-consensus Skill

This skill allows a group of agents to agree on a decision when opinions differ (e.g., "Should we refactor or patch?").

## 1. Voting Protocols

| Protocol | Description | Use Case |
|---|---|---|
| **Simple Majority** | >50% wins. | General decisions. |
| **Supermajority** | >66% wins. | Irreversible actions (Delete DB, Change Arch). |
| **Weighted Voting** | Expert's vote counts 2x. | Technical disputes (Trust `eng-backend` over `prod-pm`). |
| **Ranked Choice** | Rank A, B, C. | Choosing a library/framework. |

## 2. Process
1.  **Proposal**: Agent A proposes "Refactor Auth module".
2.  **Debate**: Agents B, C, D provide arguments (Pro/Con).
3.  **Vote**: Coordinator calls for votes.
4.  **Tally**: Coordinator counts and declares winner.
5.  **Commit**: All agents accept the result.

## 3. Conflict Patterns
- **The Stalemate**: 50/50 split.
  - *Resolution*: Architecture Decision Record (ADR) + Human Tie-breaker.
- **The Veto**: `ops-security` can veto any Engineering decision if it introduces a vulnerability.

## 4. Automation
- Use `agents/memory/episodic/VOTING_LOG.md` to record decisions.
- Never re-litigate a settled vote in the same session.
