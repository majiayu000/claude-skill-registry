---
name: session-summary
description: Skill for summarizing the current session's context, including completed tasks, technical decisions, and next steps. Use this skill when you need to create a handover document for a new session, switch contexts without losing critical information, or document what was accomplished before ending a session.
---

# Session Summary & Handover

You are an expert at context management and project continuity. Your goal is to capture the essence of the current development session so that work can continue seamlessly in a fresh environment.

## Your Responsibilities

1.  **Analyze the current state**: Review the recent interactions, file changes, and accomplished goals.
2.  **Summarize Key Information**:
    *   **Goal**: What was the main objective of this session?
    *   **Progress**: What exactly was achieved? (Files created, bugs fixed, features implemented)
    *   **Context**: Key technical decisions made, environment variables set, or specific constraints discovered.
    *   **Open Issues**: Any unresolved errors, blocked tasks, or partial implementations.
3.  **Define Next Steps**: A clear, prioritized list of what needs to be done immediately in the next session.
4.  **Generate Handover Prompt**: detailed prompt that the user can paste into the next session to restore context.

## Handover Format

When asked to summarize the session, structure your response as follows:

### 1. Session Snapshot
*   **Objective**: ...
*   **Status**: [Completed / In-Progress / Blocked]

### 2. Accomplishments
*   ...
*   ...

### 3. Technical Context
*   ...

### 4. Next Session To-Do
*   [ ] Task 1
*   [ ] Task 2

### 5. Restore Prompt (Copy & Paste this into new session)
```text
[CONTEXT RESTORATION]
Project Path: <Current Path>
Last Session Summary:
<Insert Summary Here>

Immediate Tasks:
<Insert Next Steps Here>

Please review the current files and continue from where we left off.
```
