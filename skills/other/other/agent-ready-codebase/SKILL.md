---
name: agent-ready-codebase
description: This skill should be used when auditing a codebase for AI agent readiness, or when guiding improvements to make a codebase work well with agentic coding tools. It applies when users ask to evaluate test coverage, file structure, type system usage, dev environment speed, or automated enforcement -- the five pillars that determine how effectively coding agents can operate in a project. Triggers on "audit my codebase", "make this agent-ready", "improve for AI agents", "agent-friendly", or questions about why agents struggle with a codebase.
---

# Agent-Ready Codebase

## Overview

When agents struggle with a codebase, they are reflecting and amplifying the codebase's existing weaknesses. This skill evaluates codebases against five principles that determine agent effectiveness, and provides concrete guidance to improve each one. It adapts to the project's language and stack.

Based on ["AI Is Forcing Us To Write Good Code"](https://bits.logic.inc/p/ai-is-forcing-us-to-write-good-code).

## Mode Selection

Determine which mode to operate in based on context:

- **Audit**: The user has an existing codebase and wants to know where it stands. Evaluate all five principles and produce a scorecard with specific findings.
- **Guide**: The user wants to improve a specific principle or set up a new project. Provide targeted, actionable steps for their stack.

If the mode is unclear, ask.

## The Five Principles

1. **100% Test Coverage** -- Force every line of code to demonstrate its behavior with an executable example
2. **Thoughtful File Structure** -- Make the filesystem a navigable interface for agents
3. **End-to-End Types** -- Eliminate illegal states and shrink the agent's search space
4. **Fast, Ephemeral, Concurrent Dev Environments** -- Keep feedback loops short and enable parallel agent workflows
5. **Automated Enforcement** -- Remove degrees of freedom from the agent via linters, formatters, and hooks

## Audit Workflow

To audit a codebase, work through these steps:

### 1. Detect the Stack

Identify the primary language, test framework, build system, and database by examining project files (e.g. `package.json`, `go.mod`, `Gemfile`, `pyproject.toml`, `Cargo.toml`). This determines which tooling recommendations apply.

### 2. Evaluate Each Principle

Read `references/checklist.md` for detailed criteria per principle. For each principle, determine the current state:

- **Test Coverage**: Run or inspect coverage tooling. Look for CI enforcement. Report the current percentage and whether uncovered lines are identifiable.
- **File Structure**: Sample the directory tree. Measure file sizes. Flag catch-all files (`utils`, `helpers`, `common`). Assess whether filenames communicate domain purpose.
- **Type System**: Check for strict mode, semantic type names, API contract schemas, database constraints. Identify `any`/untyped gaps.
- **Dev Environments**: Check for single-command setup, test suite runtime, port/DB isolation, worktree or container support.
- **Automated Enforcement**: Check for linter/formatter configs, CI pipelines, git hooks, agent hooks.

### 3. Produce the Scorecard

Present findings as a table with one row per principle:

| Principle | Rating | Key Finding |
|---|---|---|
| Test Coverage | Strong / Adequate / Weak | e.g. "87% coverage, no CI enforcement" |
| File Structure | Strong / Adequate / Weak | e.g. "3 files over 500 lines, 2 catch-all utils files" |
| Types | Strong / Adequate / Weak | e.g. "Strict TS, but no API schema generation" |
| Dev Environments | Strong / Adequate / Weak | e.g. "Manual 8-step setup, no concurrent support" |
| Enforcement | Strong / Adequate / Weak | e.g. "ESLint configured but not in CI" |

### 4. Prioritize Improvements

Rank the weakest principles and suggest concrete next steps for the top 2-3. Each recommendation should reference the project's actual stack and tooling.

## Guide Workflow

When guiding improvements to a specific principle:

1. Read `references/checklist.md` for the relevant section
2. Assess current state of that principle in the project
3. Provide a concrete, ordered list of changes for the project's stack
4. Where possible, show exact commands or config snippets

## Key Insight: Why 100% Coverage

The most counterintuitive principle deserves emphasis. At 100% line coverage:

- There is a **phase change**: uncovered lines are always from recent changes, removing all ambiguity about what needs testing
- The coverage report becomes a **simple todo list** of tests still needed
- It is **not about proving "no bugs"** -- it forces the author to demonstrate how every line behaves
- Unreachable code surfaces immediately and gets deleted
- Code reviews become easier because reviewers see concrete behavior examples
- Once achieved, 100% is remarkably easy to maintain -- the coverage report enumerates exactly what lines need testing

## Resources

### references/

- `checklist.md` -- Detailed evaluation criteria for each of the five principles, including stack-specific tooling, key indicators (Strong/Adequate/Weak), and guidance. Load this file when performing an audit or providing detailed guidance on any principle.
