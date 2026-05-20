---
name: vigilante-local-service-dependencies
description: Prepare local service dependencies for an implementation worktree by preferring repository-native startup flows before falling back to compatible local mechanisms.
---

# Vigilante Local Service Dependencies

## Overview
Use this skill from an implementation workflow when the assigned repository needs local services before app startup, builds, migrations, or tests can run. Keep the core Vigilante scheduler ignorant of stack-specific orchestration details by doing service preparation here, inside the worktree, from repository context.

## Inputs
Require or infer these inputs before acting:

- repository path
- assigned worktree path
- service intent or failing command context
- repository docs or scripts that describe local setup
- optional preferred service types such as `postgres`, `mysql`, `mariadb`, or `mongodb`

## Goals
- Prefer repository-provided service startup mechanisms when they are discoverable and usable.
- Fall back to a local compatible mechanism only when the repository does not provide a workable path.
- Return structured output that the parent implementation flow can use for later commands and cleanup.
- Keep scope focused on local development dependencies, especially common database-backed environments.

## Detection Order
1. Search the repository for native service-management workflows first.
- Check `README*`, `docs/`, `AGENTS.md`, `Taskfile*`, `Makefile*`, package scripts, and repo scripts for setup or startup commands.
- Check for repository-owned `vigilante docker compose` or `docker-compose` flows before generating anything new.
- Prefer commands the repository already documents for development or test setup.

2. Validate the native option before using it.
- Confirm required tools exist, such as `vigilante docker`, `vigilante docker compose`, `make`, `task`, `npm`, `pnpm`, `yarn`, or project scripts.
- If a documented path is incomplete or obviously stale, say so and continue to the next viable option.

3. Fall back only when necessary.
- If the repository has no usable local-service path, choose a compatible local mechanism with minimal new surface area.
- Docker Compose is an allowed fallback, not the defining abstraction.
- Namespace fallback artifacts, service names, ports, and temporary files to the worktree or issue session when possible.

## Execution Rules
- Work only inside the assigned worktree unless an existing repo-owned command clearly operates from the repository root.
- Reuse repository environment files, scripts, and task runners when available.
- Keep generated artifacts explicit and local to the session.
- Surface the exact command used to start services.
- Wait for readiness when practical; do not claim success immediately after spawning a process if the service is not yet accepting connections.

## Structured Output Contract
When you finish, return a concise structured summary that the parent workflow can reuse. Use this shape in plain text or JSON-like form:

- `status`: `ready`, `not_needed`, or `failed`
- `services`: started or detected services
- `mechanism`: `repo_native`, `repo_compose`, `repo_script`, `repo_task_runner`, or `generated_fallback`
- `commands`: startup and readiness commands that were used
- `connection`: host, port, database, username, URL, or env hints when available
- `cleanup`: expected stop or teardown command, or `none`
- `artifacts`: files created or reused for this session
- `notes`: concise caveats for the parent workflow

## Failure Reporting
When service preparation fails, explain which category applies:

- missing local tooling
- unsupported repository setup
- startup failure
- readiness or connection failure

Include the failing command, the missing prerequisite or observed error, and the next most reasonable remediation step.

## Practical Defaults
- Prioritize common local databases first: Postgres, MySQL, MariaDB, and MongoDB.
- If the repository already provides an application stack startup flow, use that instead of re-creating only the database layer unless the issue clearly needs the narrower setup.
- If services are already running and usable, report `status: ready` with `mechanism: repo_native` or the closest truthful mechanism instead of restarting them.

## Guardrails
- Do not hard-code a single Docker Compose lifecycle into Vigilante core behavior.
- Do not assume every repository uses containers.
- Do not silently generate infrastructure when the repository already documents a supported path.
- Do not hide cleanup expectations.
