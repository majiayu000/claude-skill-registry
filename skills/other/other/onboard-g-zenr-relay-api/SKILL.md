---
name: onboard
description: Generate a developer onboarding guide for new team members (Sofia Nakamura's workflow)
disable-model-invocation: true
---

Generate an onboarding guide for: $ARGUMENTS

If no specific audience, create a general developer onboarding guide.

## Step 1 — Read the Codebase
Understand the current state by reading:
- Project README — overview and setup
- `CLAUDE.md` — coding standards
- The app factory — structure and lifespan
- The config file — all configuration options
- The env example file — environment setup
- The personas documentation — team roles and responsibilities
- The test conftest — test infrastructure

## Step 2 — Generate Onboarding Guide

### Quick Start
Read the project README and project config for setup steps. Generate a concise quickstart covering:
1. Clone and set up the environment
2. Install dependencies
3. Configure environment
4. Run in dev/mock mode
5. Run tests and type checker

### Architecture Overview
Explain the layered architecture (see Layers in project config):
- Layer boundaries and dependency flow
- Dependency injection pattern
- Primary protocol/interface abstraction

### Key Files to Read First
List the most important files for understanding the codebase (derive from the Layers table in project config).

### Coding Standards Summary
- `from __future__ import annotations` in every file
- Typed exceptions from the exception hierarchy
- Pydantic models for all API shapes
- Thin route handlers — logic in the service class
- Three-path test coverage (success, validation, service/device error)
- `hmac.compare_digest()` for secrets
- Audit logging on all state changes

### Available Skills
List all `/skill` commands available in Claude Code for this project.

### Team Personas
Brief summary of each persona and their area of ownership (see Personas in project config).

### Common Tasks
- "Add a new endpoint" → `/add-endpoint`
- "Add a full feature" → `/add-feature`
- "Write tests" → `/test`
- "Fix a bug" → `/fix-issue`
- "Review code" → `/review`
- "Deploy check" → `/deploy-check`

## Step 3 — Output
Write the guide as clear, concise markdown. Target audience: a developer joining the team who has framework experience but has never seen this codebase.