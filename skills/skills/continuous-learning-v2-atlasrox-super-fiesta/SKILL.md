---
name: continuous-learning-v2
description: Protocol for the AI to self-analyze sessions and record 'instincts' (reusable patterns) for future improvement.
---

# 🧠 Continuous Learning Protocol (v2)

**Goal**: Transform temporary session knowledge into permanent "Instincts" to improve future performance.

## 📝 The Instruction
**When to run**: At the end of every significant task or session, OR when the user types `/learn`.

**Protocol Steps**:

1.  **Analyze Session History**: Review the interaction between you and the user. Look for:
    *   **Corrections**: "No, don't use X, use Y." -> *Strong Signal*
    *   **Preferences**: "I prefer small commits." -> *Medium Signal*
    *   **Patterns**: "We always mock the DB in tests." -> *Project pattern*

2.  **Formulate Instinct**: Create a concise "Instinct" entry following this format:
    ```markdown
    ### [Instinct Title]
    - **Trigger**: When [situation occurs]...
    - **Action**: Always [do this specific thing].
    - **Confidence**: [High/Medium/Low] based on evidence.
    - **Source**: Session [Date/ID]
    ```

3.  **Refine**: Check against existing rules. Is this already covered? Is it a general best practice or specific to this user?

4.  **Save**:
    *   **Read**: `~/.antigravity/instincts/learned.md` (Create if missing).
    *   **Append**: Add your new instinct to the file.
    *   **Report**: Tell the user "I have learned a new instinct: [Title]."

## 💡 Example

**User**: "Please stop using `console.log`, use our logger."
**AI Action**:
1.  Detects correction regarding logging.
2.  Formulates Instinct:
    *   **Title**: Use Project Logger
    *   **Trigger**: When logging information.
    *   **Action**: Use `lib/logger` instead of `console.log`.
    *   **Confidence**: High (Explicit user instruction).
3.  Writes to `learned.md`.

## 🚫 What NOT to learn
*   One-off bugs.
*   Secrets or passwords (NEVER save these).
*   Temporary file paths.
