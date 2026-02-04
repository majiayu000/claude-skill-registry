---
name: docker-compose
description: Multi-service orchestration with Docker Compose, focusing on network isolation, environment-specific profiles, and service discovery. Triggers: docker-compose, container-networking, docker-profiles, service-discovery, yaml-config.
---

# Docker Compose Orchestration

## Overview
Docker Compose simplifies the management of multi-container applications. It enables service discovery through internal hostnames and provides mechanisms for environment-specific configurations using profiles.

## When to Use
- **Local Development**: Spinning up a full stack (frontend, backend, DB) with one command.
- **CI/CD Integration**: Running isolated integration tests in containerized environments.
- **Microservices**: Orchestrating communication between multiple independent services.

## Decision Tree
1. Do you have services only needed for debugging? 
   - YES: Use `profiles` to keep them optional.
2. Do you need to hide a database from the public proxy? 
   - YES: Create isolated custom `networks`.
3. Do you need to connect to a service outside the current YAML file? 
   - YES: Use `external: true` for that network.

## Workflows

### 1. Isolating Internal Services
1. Define `frontend` and `backend` custom networks in the top-level `networks` key.
2. Assign the `proxy` service to the `frontend` network.
3. Assign the `app` service to both `frontend` and `backend`.
4. Assign the `db` service only to the `backend` network to isolate it from the proxy.

### 2. Environment-Specific Overrides with Profiles
1. Add `profiles: [debug]` to an optional service (e.g., `phpmyadmin`) in `compose.yaml`.
2. Run `docker compose up` for standard operations; debug services stay off.
3. Run `docker compose --profile debug up` to include the debugging tools.

### 3. Using Existing External Networks
1. Declare a network in `compose.yaml` with `external: true`.
2. Link local services to this external network in their `networks` section.
3. This allows the Compose stack to communicate with containers managed outside the current project.

## Non-Obvious Insights
- **Service Name as Hostname**: Within the default network, you don't need IPs; containers connect via service names (e.g., `db:5432`).
- **IP Persistence**: Configurations changes cause containers to get new IPs, but the hostname (service name) remains consistent, which is why service discovery is essential.
- **Implicit Enablement**: Services without a `profiles` attribute are always enabled regardless of which profiles are requested.

## Evidence
- "Each container for a service joins the default network and is... discoverable by the service's name." - [Docker Docs](https://docs.docker.com/compose/networking/)
- "Profiles help you adjust your Compose application for different environments... by selectively activating services." - [Docker Docs](https://docs.docker.com/compose/profiles/)
- "Instead of just using the default app network, you can specify your own networks..." - [Docker Docs](https://docs.docker.com/compose/networking/)

## Scripts
- `scripts/docker-compose_tool.py`: Python script to generate dynamic Compose YAML files.
- `scripts/docker-compose_tool.js`: Node.js script for checking service connectivity within a network.

## Dependencies
- `docker-compose`
- `docker` engine

## References
- [references/README.md](references/README.md)