---
name: python-modern-tooling
description: Use when choosing the right modern Python tooling workflow for a project or script (uv setup, quality tools, CLI, logging, packaging) or when unsure which Python tooling skill applies.
---

# Python Modern Tooling

## Overview

Route requests to the narrowest skill that matches the task. Core principle: keep the umbrella lean and delegate details.

## Quick Reference

| Need | Use this skill |
| --- | --- |
| Init project, add deps, run commands | `python-uv-project-setup` |
| Lint/format/type-check/test/CI | `python-quality-tooling` |
| Build a CLI with Typer | `python-cli-typer` |
| Choose/configure logging or loguru | `python-logging` |
| Build/publish packages with uv | `python-packaging-uv` |

## Routing Rules

- If the task mentions install, dependency, run, or missing package: use `python-uv-project-setup`.
- If the task mentions ruff, ty, pytest, coverage, or CI: use `python-quality-tooling`.
- If the task mentions CLI, commands, Typer: use `python-cli-typer`.
- If the task mentions logging, loguru, handlers, formatters: use `python-logging`.
- If the task mentions packaging, build, publish, dist: use `python-packaging-uv`.

## Example

User: "Missing fastapi and tests fail. How should I install it?"

Route to: `python-uv-project-setup` (dependency management and run rules).

## Common Mistakes

- Providing detailed commands here instead of routing to the focused skill.
- Mixing multiple workflows in one response.

## Red Flags

- Suggesting `pip install` or direct `python`/`pytest` execution here.
