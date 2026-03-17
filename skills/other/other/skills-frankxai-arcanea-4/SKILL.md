
---
name: starlight-memex
description: The Memory Management System. Writes back to Semantic and Episodic Vaults.
---

# Starlight Memex (Self-Learning)

Use this skill to **Record Information** into the Starlight Vaults.
This is how the system "Learns".

## 1. The Write Protocol
You have permission to APPEND to:
*   `starlight-protocol/01_INTELLECT/VAULT_MEMORY/EPISODIC/Session_Logs.md`
*   `starlight-protocol/01_INTELLECT/VAULT_MEMORY/SEMANTIC/Patterns.md`

## 2. When to Write
1.  **Success:** "We successfully deployed the Auth module." -> Log to Episodic.
2.  **Pattern:** "The User prefers `lucide-react` icons." -> Log to Semantic.
3.  **Failure:** "The build failed due to circular reference." -> Log to Episodic (so we avoid it next time).

## 3. The Format
*   **Episodic:** `[YYYY-MM-DD HH:MM] [AGENT] [ACTION] -> [RESULT]`
*   **Semantic:** `* **Pattern:** [Description] (Learned: [Date])`

## 4. Automatic Trigger
The `starlight-orchestrator` calls this skill at the end of every major task sequence.
