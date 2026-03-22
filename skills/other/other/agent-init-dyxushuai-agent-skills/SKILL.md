---
name: agent-init
description: Initialize or improve AGENTS.md files that define how coding agents operate in a repo. Use when asked to set up or replace an agent init command (Codex, Claude), standardize multi-agent behavior, or audit an existing AGENTS.md for clarity, commands, boundaries, and repo-specific context. For Claude Code, also create CLAUDE.md as a symlink to AGENTS.md.
---

# AGENTS.md Guide

## Overview

Provide a repeatable workflow and quality bar for writing or updating AGENTS.md files so agents receive concrete, repo-specific instructions.

## Trigger examples

- "Create an AGENTS.md for this repo and include exact test commands."
- "Replace our agent init command with a proper AGENTS.md file."
- "Audit our existing AGENTS.md for missing boundaries and commands."
- "Update AGENTS.md to reflect the current build and lint commands."
- "Create CLAUDE.md as a symlink to AGENTS.md for Claude Code."

## Core Principles (condensed)

- Be concrete: prefer executable commands and code examples over prose.
- Put commands early and include flags/options.
- Use real code examples over explanations.
- Remove ambiguity: state boundaries and non-goals explicitly.
- Be specific about the tech stack; include versions and key dependencies.
- Define the agent's role/persona and how it fits the team.
- Cover the six core areas: purpose, code organization, run/test/validate, change management, dependencies/environment, and avoid list.
- Use three-tier boundaries: Always / Ask first / Never.
- Start small and iterate as the repo evolves.

## Brainstorming Mode (divergent Q&A)

Use this mode when requirements are unclear or the repo structure will influence the document shape.

- Ask one question at a time. Prefer multiple choice when possible.
- Base questions on the actual repo shape (single app vs monorepo).
- Confirm which agents will consume the docs and their expectations.
- If Claude Code is in scope, plan a CLAUDE.md symlink to AGENTS.md.
- Ask for exact commands (with flags) and a real code example.
- Propose 1-2 AGENTS.md layouts (section order) with tradeoffs, then converge.
- Keep questions short and actionable, then confirm before drafting.
- Read `references/agents-md-brainstorm.md` for question banks and decision heuristics.

## Workflow

### 1) Clarify scope and placement

- Confirm whether the task is to create new docs or revise existing ones.
- Default output is root `AGENTS.md`.
- If the user asks for a different location, confirm the exact path and proceed.
- If Claude Code is in scope, create `CLAUDE.md` as a symlink to `AGENTS.md`.
- Still maintain a single AGENTS.md (no per-agent files unless explicitly requested).
- Confirm which agents will consume the docs and align content with their workflows.
- If the repo uses a different location or filename, ask before proceeding.

### 2) Gather repo-specific facts

Collect only what will make the file actionable:
- Stack and versions (language/runtime/package manager).
- Key directories and ownership.
- Build, test, lint, and format commands.
- Environment variables, secrets, and local setup details.
- Git/PR expectations (branching, commit style, approvals).

### 2a) Shape the doc by repo structure

- If monorepo, add per-app or per-team sections inside AGENTS.md.
- If multiple roles are needed, use role-specific subsections inside AGENTS.md.
- If the repo is small, keep a single concise AGENTS.md.
- If a multi-file layout is requested, confirm the target paths before writing.

### 3) Draft with the six core areas

Write sections that map to the six core areas, keeping each section short and command-focused. Use the template if needed.

### 4) Add concrete commands and examples

- Prefer copy/paste commands over prose.
- Include example file paths and typical change patterns.
- Show expected outputs if ambiguity is likely.
- Include at least one real code example that matches repo style.

### 5) Add boundaries and safety

State what the agent must not do, what requires approval, and any data/credential constraints.

### 6) Review for clarity

- Eliminate vague statements ("run tests" -> specify the exact command).
- Ensure every requirement is tied to a command, path, or policy.
- Keep it short enough to scan quickly.

## Output Requirements

Include, at minimum:
- Role/purpose of the agent and its scope.
- Repo map (key paths, entry points, ownership).
- Run/test/validate commands (copyable, placed early, include flags).
- Tech stack with versions and key dependencies.
- Change management rules (branching, commits, PR expectations).
- Dependencies and environment setup.
- Code style example (real snippet).
- Explicit avoid list and approval gates with Always / Ask first / Never.

## Cross-agent compatibility

- Keep instructions in plain Markdown with explicit commands and paths.
- Avoid agent-specific fields or features unless the target agent requires them.
- Keep a single root AGENTS.md as the source of truth.
- If Claude Code is in scope, create CLAUDE.md as a symlink to AGENTS.md.

## Multi-platform support

- Ask which agents are in scope (Codex, Claude, GitHub Copilot, Cursor, etc.).
- Use one shared AGENTS.md that works across those agents.
- Do not assume tool-specific directories; only update AGENTS.md unless the user asks otherwise.
- When showing examples, label tool-specific details as optional (not required).
- If Claude Code is in scope, add a CLAUDE.md symlink to AGENTS.md.
- If GitHub Copilot coding agent is in scope, consider adding `.github/copilot-instructions.md` and keep it minimal (ideally pointing to AGENTS.md as the source of truth).

## References

- Read `references/agents-md-template.md` when drafting a new file.
- Read `references/agents-md-example.md` for a complete AGENTS.md example.
- Read `references/agents-md-checklist.md` when reviewing or auditing an existing file.
- Read `references/agents-md-brainstorm.md` when running a divergent Q&A gap analysis.
