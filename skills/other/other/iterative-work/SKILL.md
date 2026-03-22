---
name: iterative-work
description: Implement a feature or fix a bug following a plan, using iterative work.
---

You are given a detailed ticket document with a detailed plan at the bottom (look for a section starting with "# Plan: " or "# Implementation Plan").
Look at the checkboxes and identify which task you need to implement next. If all checkboxes are empty, start with Task 1.

You MUST follow this cycle:
1. You ONLY work on 1 Task at a time. DO NOT plan multiple tasks implementation.
2. After each completed sub-task (checkbox), IMMEDIATELY mark it checked in the feature document
3. When you completed and checked all checkboxes from the Task, run the validation/testing commands
4. After completing the task, spawn a sub-agent to review your changes. The sub-agent prompt is below
5. Address all review findings, then re-run the FULL validation/testing commands (same as step 3)
6. Print the full review text to the user (DO NOT skip addressed/ignored issues) and ask for the user review

If the user instructed you to proceed to the next task, you start following the point 1 from the instruction above again.

### Review Agent Spawning

IMPORTANT: the initial prompt specifies which type of agent you use. If the user said you need to use codex, use this command to spawn a reviewer:

```
codex exec --model gpt-5.3-codex --sandbox workspace-write --full-auto <prompt>
```

If user didn't say anything about the reviewer, you just spawn your sub-agent.

The prompt:

```
Use skill ai-review to review implementation of Task [N] from [current_task_document_path]. Think hard. The changes are uncommited. Return your review output as your response, do not change any files. 
```

Replace [N] and [current_task_document_path] with appropriate values.

## CRITICAL GUIDELINES

- Do NOT create your own execution plan or a TODO list. The exact plan you need to follow is already written in the document.
- Do NOT review your own code. Always spawn a sub-agent to get an independent review.
- You are FORBIDDEN from starting a new task in the same turn you finish the previous one. You MUST report a completion summary to the user and WAIT for a response.
- NEVER skip running tests. If you can't run some tests, report the blocker to the user — do NOT mark the validation checkbox as done. A validation step marked as done means you actually ran the tests and they passed.
- If some tests fail, you must fix the code even if it was a pre-existing fail. If you think it tests outdated/incorrect behavior, consult with the user.

If you finished the last task of the feature, and it's approved by the user, move the plan file to the ai/tickets/completed folder.
