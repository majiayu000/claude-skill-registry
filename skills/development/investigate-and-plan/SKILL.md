---
name: investigate-and-plan
description: 'name: investigate-and-plan'
---

﻿---
name: investigate-and-plan
description: Investigate errors, incidents, or product ideas using both internet research and repo-wide codebase research, then propose a concrete changeset plan with clarifying questions before any implementation. Use when a user asks to investigate, root-cause, or plan changes, or when an Issue or PR is referenced and needs a plan.
---

# Investigate And Plan

## Overview

Investigate the request, research external sources and the codebase, and produce a plan for a changeset before writing code. Ask open clarifying questions with defaults, then implement only after the plan is agreed.

## Workflow

### 1) Confirm scope and gather context

- Identify the exact error, feature idea, or decision to investigate.
- If a PR or Issue is referenced, use the GitHub CLI to fetch details and comments.
- List the codebase areas to inspect, including backend, frontend, bot, infra, scripts, tests, docs, and configuration.

### 2) Research

- Use web.run for internet research, then cite sources for any external facts.
- Search the codebase broadly with targeted deep dives into relevant subsystems.
- Capture findings, constraints, and risks, including any existing TODOs or comments.

### 3) Propose the changeset

- Provide a concrete plan with files to touch, key edits, data migrations, and test updates.
- Call out assumptions and viable alternatives.
- Ask open questions that block implementation, and provide defaults for each question.
- Do not write code yet.

### 4) Implement after agreement

- Wait for the plan to be accepted or adjusted.
- Implement the agreed changes, keeping the scope aligned to the plan.
- If new information changes the plan, pause and confirm the update.

### 5) Validate

- Run the repo check command, prefer `yarn run check` unless a no-auto-fix run is required.
- Ensure tests, build, lint, end-to-end, and complexity or code stats pass as required by the project.
- Report command outcomes and any remaining gaps.
