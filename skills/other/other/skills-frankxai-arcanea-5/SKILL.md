
---
name: starlight-engineering
description: Invoke the Engineering Sub-Swarm (Sentinel, Craftsman, Scaler, Reformer)
---

# Starlight Engineering Swarm

Use this skill to delegate specific engineering tasks to sub-agents.
Do not use `starlight-orchestrator` for granular code tasks; use this instead.

## 1. The Roster
*   **Sentinel (Security):** Audits, Auth, Zod. `starlight-protocol/03_AGENCY/DEPT_ENGINEERING/AGENT_SENTINEL.md`
*   **Craftsman (Frontend):** UI, React, Tailwind. `starlight-protocol/03_AGENCY/DEPT_ENGINEERING/AGENT_CRAFTSMAN.md`
*   **Scaler (Backend):** DB, API, Perf. `starlight-protocol/03_AGENCY/DEPT_ENGINEERING/AGENT_SCALER.md`
*   **Reformer (Refactor):** Cleanup, Debt. `starlight-protocol/03_AGENCY/DEPT_ENGINEERING/AGENT_REFORMER.md`

## 2. The Protocol
1.  **Identify:** "Which specialist does this ticket require?"
2.  **Context:** Load their specific Agent File + Tech Stack.
3.  **Action:** Generate the code/plan.
4.  **Review:** Use `The Principal` (Lyssandria) to audit the output.

## 3. Commands
*   `/eng safe` -> Invokes Sentinel.
*   `/eng ui` -> Invokes Craftsman.
*   `/eng api` -> Invokes Scaler.
*   `/eng fix` -> Invokes Reformer.
