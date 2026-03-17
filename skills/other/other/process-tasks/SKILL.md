---
name: process-tasks
description: Process pending tasks, check Needs_Action folder, complete task requests, move finished work to Done folder, and update activity dashboard. Use when the user asks to "process tasks", "check pending tasks", "handle Needs_Action items", "complete my tasks", "check what needs to be done", or mentions the Needs_Action folder, task processing, or wants to see completed work moved to Done.
---

# Process Tasks Skill

## Purpose
This skill automates the processing of tasks dropped into the Needs_Action folder by the filesystem watcher. It ensures all tasks are handled according to company rules and properly logged.

## Instructions

When this skill is invoked, follow these steps:

### 1. Check for Tasks
- List all files in the `Vault/Needs_Action/` folder
- If the folder is empty, report "No tasks pending" and stop
- If there are files, proceed to process each one

### 2. Process Each Task
For each file in `Vault/Needs_Action`:

a. **Read the file content**
   - Read both the metadata (.md file) and any associated content files
   - Understand what task is being requested

b. **Follow Company Rules**
   - Read and follow all rules in `Vault/Company_Handbook.md`
   - Always be polite
   - Always add timestamps when updating files

c. **Complete the Task**
   - Execute the requested task (summarize, analyze, draft response, etc.)
   - If the task requires creating output, create it in an appropriate location
   - If unclear about the task, ask for clarification

d. **Move to Done**
   - Move the processed file(s) to the `Vault/Done/` folder
   - Keep the original filename

### 3. Update Dashboard
After processing all tasks, update `Vault/Dashboard.md`:

- Add a new entry under the Activity Log section
- Use this format:
  ```
  ### YYYY-MM-DD HH:MM:SS
  **Task Completed**: [Brief description]
  - [Detail 1]
  - [Detail 2]
  - Status: ✓ Complete
  ```
- Use the current timestamp in format: YYYY-MM-DD HH:MM:SS

### 4. Report Summary
After all tasks are processed, provide a summary:
- Number of tasks completed
- Brief description of each task
- Any issues encountered

## Rules to Follow
1. Always be polite in any communication or output
2. Always add timestamps when updating `Vault/Dashboard.md`
3. Preserve file metadata when moving files
4. If a task is unclear, ask before proceeding
5. Log every action taken

## Example Triggers

This skill automatically activates when the user says:
- "Process my tasks"
- "Check the Needs_Action folder"
- "Are there any pending tasks?"
- "Complete the tasks that are waiting"
- "What needs to be done?"
- "Handle my Needs_Action items"

When activated, the skill will:
1. Check `Vault/Needs_Action` folder
2. Find and process all pending tasks
3. Move completed files to `Vault/Done`
4. Update `Vault/Dashboard.md` with timestamped log
5. Report what was accomplished