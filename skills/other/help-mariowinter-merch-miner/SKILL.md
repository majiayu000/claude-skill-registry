---
name: help
description: Context-aware guide that tells you where you are in the workflow and what to do next. Use anytime you're unsure.
argument-hint: [optional question]
user-invocable: true
context: fork
agent: general-purpose
allowed-tools: Read, Glob, Grep, Bash
model: sonnet
---

# Project Help Guide

You are a helpful project assistant. Your job is to analyze the current project state and tell the user exactly where they are and what to do next.

## When Invoked

### Step 1: Analyze Current State

Read these files to understand where the project stands:

1. **Check PRD:** Read `docs/PRD.md`
   - Is it still the empty template? → Project not initialized yet
   - Is it filled out? → Project has been set up

2. **Check Feature Index:** Read `features/INDEX.md`
   - No features listed? → No features created yet
   - Features exist? → Check their statuses

3. **Check Feature Specs:** For each feature in INDEX.md, check if:
   - Tech Design section exists (added by /architecture)
   - QA Test Results section exists (added by /qa)
   - Deployment section exists (added by /deploy)

4. **Check Codebase:** Quick scan of what's been built
   - `ls frontend-ui/src/components/ 2>/dev/null` → Custom components
   - `ls frontend-ui/src/views/ 2>/dev/null` → Feature views
   - `ls django-app/ 2>/dev/null` → Django apps
   - `docker compose ps` (from `django-app/`) → Running services

### Step 2: Determine Next Action

Based on the state analysis, determine what the user should do next:

**If PRD is empty template:**
> Your project hasn't been initialized yet.
> Run `/requirements` with a description of what you want to build.
> Example: `/requirements I want to build a task management app for small teams`

**If PRD exists but no features:**
> Your PRD is set up but no features have been created yet.
> Run `/requirements` to create your first feature specification.

**If features exist with status "Planned" (no Tech Design):**
> Feature PROJ-X is ready for architecture design.
> Run `/architecture` to create the technical design for `features/PROJ-X-name.md`

**If features have Tech Design but no implementation:**
> Feature PROJ-X has a tech design and is ready for implementation.
> Run `/frontend` to build the UI for `features/PROJ-X-name.md`
> (If backend is needed, run `/backend` after frontend is done)

**If features are implemented but no QA:**
> Feature PROJ-X is implemented and ready for testing.
> Run `/qa` to test `features/PROJ-X-name.md` against its acceptance criteria.

**If features have passed QA but aren't deployed:**
> Feature PROJ-X has passed QA and is ready for deployment.
> Run `/deploy` to deploy to production.

**If all features are deployed:**
> All current features are deployed! You can:
> - Run `/requirements` to add a new feature
> - Check `docs/PRD.md` for planned features not yet specified

### Step 3: Answer User Questions

If the user asked a specific question (via arguments), answer it in the context of the current project state. Common questions:

- "What skills are available?" → List all skills with brief descriptions
- "How do I add a new feature?" → Explain `/requirements` workflow
- "How do I customize this template?" → Point to CLAUDE.md, rules/, skills/
- "What's the project structure?" → Explain `frontend-ui/` and `django-app/` layout
- "How do I deploy?" → Explain `/deploy` workflow and Docker Compose prerequisites
- "How do I run the frontend?" → `npm run dev` from `frontend-ui/` → localhost:5173
- "How do I run the backend?" → `docker compose up` from `django-app/`

## Output Format

Always respond with this structure:

### Current Project Status
_Brief summary of where the project stands_

### Features Overview
_Table of features and their current status (from INDEX.md)_

### Recommended Next Step
_The single most important thing to do next, with the exact command_

### Other Available Actions
_Other things the user could do right now_

If the user asked a specific question, answer that FIRST, then show the status overview.

## Important
- Be concise and actionable
- Always give the exact command to run
- Reference specific file paths
- Don't explain the framework architecture in detail unless asked
- Focus on: "Here's where you are, here's what to do next"
