---
name: project-md-refresh
description: Analyze the current repository and create or refresh .claude/PROJECT.md to match the project. Use when PROJECT.md is missing, stale, or the user asks to generate/update project-specific rules, structure, commands, or architecture details.
---

# PROJECT.md Refresh

## Goal
Create or update `.claude/PROJECT.md` with accurate, evidence-based project details.

## Workflow
1. Locate the base file.
   - If `.claude/PROJECT.md` exists, use it as the base; preserve custom rules and update facts.
   - If missing, create `.claude/` if needed and copy `assets/PROJECT.template.md` to `.claude/PROJECT.md`.

2. Collect signals from the repository.
   - Read `README.md` and any project docs.
   - Identify the stack from config files: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `build.gradle`, `pom.xml`, `Gemfile`, `requirements.txt`, `Makefile`, or `Taskfile`.
   - Extract run/build/test/lint commands from scripts or tooling.
   - Inspect the top-level directory structure and key entrypoints.
   - Locate API routes/controllers and data models (search for `route`, `router`, `controller`, `handler`, `model`, `schema`).
   - Find auth configuration (search for `auth`, `jwt`, `session`, `oauth`).
   - Note environment variable usage (search for `ENV`, `process.env`, `os.environ`, `dotenv`).

3. Update `PROJECT.md` sections.
   - Fill the overview (name, stack, primary language).
   - Summarize core rules and conventions.
   - Document directory structure (top-level + key subdirectories).
   - Document API/data patterns, auth, and docs paths.
   - Add concrete commands for dev/build/lint/test/typecheck.

4. Output.
   - Save `.claude/PROJECT.md`.
   - Provide a short summary and list any gaps/questions.

## Guardrails
- Do not invent details; base every statement on files found.
- If information is missing, add TODOs or ask for confirmation.
- Keep content concise and project-specific.
