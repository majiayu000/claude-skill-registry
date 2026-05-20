---
version: 4.1.0-fractal
name: conductor-status
description: Display project status, active tracks, and next actions
metadata:
  argument-hint: "[track-id] [--detailed]"
---

# Conductor Status

Display the current status of the Conductor project, including overall progress, active tracks, and next actions.

## Use this skill when

- Working on conductor status tasks or workflows
- Needing guidance, best practices, or checklists for conductor status

## Do not use this skill when

- The task is unrelated to conductor status
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Pre-flight Checks

1. Verify Conductor is initialized:
   - Check `conductor/product.md` exists
   - Check `conductor/tracks.md` exists
   - If missing: Display error and suggest running `/conductor:setup` first

2. Check for any tracks:
   - Read `conductor/tracks.md`
   - If no tracks registered: Display setup complete message with suggestion to create first track

## Data Collection

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [1. Project Information](./sub-skills/1-project-information.md)
### 2. [2. Tracks Overview](./sub-skills/2-tracks-overview.md)
### 3. [3. Detailed Track Analysis](./sub-skills/3-detailed-track-analysis.md)
### 4. [4. Blocker Detection](./sub-skills/4-blocker-detection.md)
### 5. [Full Project Status (no argument)](./sub-skills/full-project-status-no-argument.md)
### 6. [Single Track Status (with track-id argument)](./sub-skills/single-track-status-with-track-id-argument.md)
### 7. [No Tracks Found](./sub-skills/no-tracks-found.md)
### 8. [Conductor Not Initialized](./sub-skills/conductor-not-initialized.md)
### 9. [Track Not Found (with argument)](./sub-skills/track-not-found-with-argument.md)
### 10. [Task Counting](./sub-skills/task-counting.md)
### 11. [Phase Detection](./sub-skills/phase-detection.md)
### 12. [Progress Bar](./sub-skills/progress-bar.md)
