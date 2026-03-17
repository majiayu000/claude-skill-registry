---
name: dev-server
description: Create and manage Python backend services using uv, FastAPI, Pydantic, SQLAlchemy, and AI libraries. Use this skill when the user asks to build a backend, API, or server-side application.
metadata:
  author: Yuga Sun
  version: "2026.01.29"
---

# Server Development Skill

## Instructions

Use this skill to scaffold and maintain backend services in the `server/` directory. Follow the stack preferences and configuration details below.

### Quick Start

1.  **Initialize**: `uv init`.
2.  **Manager**: Use `uv` for all dependency operations.
3.  **Framework**: Setup `FastAPI` with `Pydantic`.
4.  **Database**: configure `SQLAlchemy` (Async) + `Alembic`.

## Core Stack Preferences

### Project Management (uv)

Use **uv** for all Python project management (scaffolding, dependency management, virtual environments).

| Command | Description |
|---------|-------------|
| `uv init` | Initialize a new project |
| `uv add <pkg>` | Add dependency |
| `uv add --dev <pkg>` | Add development dependency |
| `uv run <cmd>` | Run command in virtual environment |
| `uv venv` | Create virtual environment |

### Project Location

The backend project should be initialized in the `server/` directory.

### Framework (FastAPI)

Use **FastAPI** for building APIs.

-   Use `APIRouter` for modularizing routes.
-   Use `pydantic-settings` for configuration management.

### Database (SQLAlchemy + Alembic)

Use **SQLAlchemy 2.0+** with **AsyncIO** support.
Use **Alembic** for database migrations.

### AI & LLM (LiteLLM + Docling)

-   **LiteLLM**: For standardized access to various LLM providers.
-   **Docling**: For parsing and processing documents.

---

## References

### Setup & Configuration

| Topic | Description | Reference |
|-------|-------------|-----------|
| Project Setup | Using uv, strict python versioning, and environment variables | [setup](references/setup.md) |
| API Development | FastAPI structure, error handling, and validation | [api](references/api.md) |

### Data & Architecture

| Topic | Description | Reference |
|-------|-------------|-----------|
| Database Access | Async SQLAlchemy strategies and Alembic migrations | [database](references/database.md) |
| AI Integration | using LiteLLM and Docling for AI features | [ai](references/ai.md) |
