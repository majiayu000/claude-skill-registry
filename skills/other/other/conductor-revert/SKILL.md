---
version: 4.1.0-fractal
name: conductor-revert
description: Git-aware undo by logical work unit (track, phase, or task)
metadata:
  argument-hint: "[track-id | track-id:phase | track-id:task]"
---

# Revert Track

Revert changes by logical work unit with full git awareness. Supports reverting entire tracks, specific phases, or individual tasks.

## Use this skill when

- Working on revert track tasks or workflows
- Needing guidance, best practices, or checklists for revert track

## Do not use this skill when

- The task is unrelated to revert track
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Pre-flight Checks

1. Verify Conductor is initialized:
   - Check `conductor/tracks.md` exists
   - If missing: Display error and suggest running `/conductor:setup` first

2. Verify git repository:
   - Run `git status` to confirm git repo
   - Check for uncommitted changes
   - If uncommitted changes exist:

     ```
     WARNING: Uncommitted changes detected

     Files with changes:
     {list of files}

     Options:
     1. Stash changes and continue
     2. Commit changes first
     3. Cancel revert
     ```

3. Verify git is clean enough to revert:
   - No merge in progress
   - No rebase in progress
   - If issues found: Halt and explain resolution steps

## Target Selection

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [If argument provided:](./sub-skills/if-argument-provided.md)
### 2. [If no argument:](./sub-skills/if-no-argument.md)
### 3. [For Task Revert](./sub-skills/for-task-revert.md)
### 4. [For Phase Revert](./sub-skills/for-phase-revert.md)
### 5. [For Full Track Revert](./sub-skills/for-full-track-revert.md)
### 6. [On Merge Conflict](./sub-skills/on-merge-conflict.md)
### 7. [If reverting entire track:](./sub-skills/if-reverting-entire-track.md)
### 8. [If reverting to incomplete state:](./sub-skills/if-reverting-to-incomplete-state.md)
### 9. [Track Never Committed](./sub-skills/track-never-committed.md)
### 10. [Commits Already Reverted](./sub-skills/commits-already-reverted.md)
### 11. [Remote Already Pushed](./sub-skills/remote-already-pushed.md)
