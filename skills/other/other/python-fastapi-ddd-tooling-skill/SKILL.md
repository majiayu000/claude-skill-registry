---
name: python-fastapi-ddd-tooling-skill
description: Guides project tooling for a Python FastAPI + SQLAlchemy DDD/Onion Architecture codebase: uv-based environment setup, Makefile workflows, ruff formatting/linting, mypy typing, pytest, and CI (GitHub Actions), based on the dddpy reference. Use when bootstrapping a repo or tightening developer experience and quality gates.
license: Apache-2.0
metadata:
  author: Takahiro Ikeuchi
  version: "1.0.0"
---

# Tooling & DX for FastAPI DDD Projects (uv / ruff / mypy / CI)

This skill is about **developer experience and quality automation** for a DDD FastAPI project, following the conventions in `dddpy`.

## Goals

- One-command local setup (`make install`)
- Fast feedback loop (`make test`, `make format`, `make dev`)
- Reproducible CI (GitHub Actions + Python matrix)

## Recommended stack (dddpy-style)

- Python `>=3.13`
- `uv` for venv + dependency install + running tools
- `ruff` for formatting/linting
- `mypy` for type checking
- `pytest` for tests

## Makefile workflow (core targets)

Keep a small Makefile that shells out to tools inside `.venv/`:

- `venv`: create `.venv`
- `install`: install editable package + dev deps
- `test`: run mypy + pytest
- `format`: run ruff formatter
- `dev`: run `fastapi dev` via uv

## CI workflow

Run `make install` + `make test` on push/PR with a Python version matrix (e.g., 3.13, 3.14) and install `uv` in CI.

## App bootstrap patterns

- Use FastAPI `lifespan` to create tables on startup and dispose the engine on shutdown.
- Keep SQLAlchemy engine/session setup in `infrastructure/sqlite/database.py` (or equivalent).
- Configure logging once at startup (`logging.config.fileConfig(...)`).

For concrete file templates (Makefile, workflow YAML, bootstrap snippets), read `references/TOOLING.md`.

