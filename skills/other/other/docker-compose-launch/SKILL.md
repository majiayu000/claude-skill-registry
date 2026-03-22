---
name: docker-compose-launch
description: Launch worktree-scoped local services for issue implementation when a monorepo skill requires database dependencies.
---

# Docker Compose Launch

## Overview
Use this skill only when the selected implementation workflow explicitly needs local services before app startup, migrations, or tests can run. Keep all service startup scoped to the assigned worktree and treat Docker Compose as a reusable helper for local implementation and test dependencies only.

## Invocation Contract
The parent implementation skill should pass or infer this contract before acting:

- `required`: `true` or `false`
- `worktree_path`: absolute path to the assigned worktree
- `service_types`: one or more of `mysql`, `mariadb`, `postgres`, or `mongodb`
- `reason`: short explanation of which app, package, migration, or test command needs the services
- `preferred_mechanism`: repository-native compose file, repo script, or fallback compose generation

If `required` is `false`, return `status: not_needed` and do nothing else.

## Execution Rules
- Prefer repository-owned `docker-compose.yml`, `docker-compose.yaml`, `compose.yml`, or `compose.yaml` files before generating new files.
- Prefer repository scripts or task-runner commands that already wrap Compose when they are documented and usable.
- Namespace any generated project name, file, network, volume, or container identifiers to the assigned worktree.
- Wait for service readiness before reporting success.
- Surface the exact startup and teardown commands that were used.

## Structured Result
Return a concise structured summary using these fields:

- `status`: `ready`, `not_needed`, or `failed`
- `services`: services that were started or detected
- `mechanism`: `repo_compose`, `repo_script`, or `generated_fallback`
- `commands`: startup, readiness, and teardown commands
- `connection`: host, port, database, username, URL, or env hints when available
- `cleanup`: explicit stop command, or `none`
- `artifacts`: compose files or env files created or reused
- `notes`: concise caveats or follow-up steps

## Guardrails
- Do not launch services outside the assigned worktree scope.
- Do not assume every repository needs Docker Compose.
- Do not replace a documented repository-native startup flow with a generated one unless the native path is unusable.
- Do not claim success until the requested service is accepting connections.
