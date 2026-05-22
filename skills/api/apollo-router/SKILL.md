---
name: apollo-router
description: >
  Version-aware guide for configuring and running Apollo Router for federated GraphQL supergraphs.
  Generates correct YAML for both Router v1.x and v2.x. Use this skill when:
  (1) setting up Apollo Router to run a supergraph,
  (2) configuring routing, headers, or CORS,
  (3) implementing custom plugins (Rhai scripts or coprocessors),
  (4) configuring telemetry (tracing, metrics, logging),
  (5) troubleshooting Router performance or connectivity issues.
license: MIT
compatibility: Linux/macOS/Windows. Requires a composed supergraph schema from Rover or GraphOS.
metadata:
  author: apollographql
  version: "2.2.1"
allowed-tools: Bash(router:*) Bash(./router:*) Bash(rover:*) Bash(curl:*) Bash(docker:*) Read Write Edit Glob Grep
---

# Apollo Router Config Generator

Apollo Router is a high-performance graph router written in Rust for running Apollo Federation 2 supergraphs. It sits in front of your subgraphs and handles query planning, execution, and response composition.

**This skill generates version-correct configuration.** Router v1 and v2 have incompatible config schemas in several critical sections (CORS, JWT auth, connectors). Always determine the target version before generating any config.

## Step 1: Version Selection

Ask the user **before generating any config**:

```
Which Apollo Router version are you targeting?

  [1] Router v2.x (recommended — current LTS, required for Connectors)
  [2] Router v1.x (legacy — end-of-support announced, security patches only)
  [3] Not sure — help me decide
```

If the user picks **[3]**, display:

```
Quick guide:

  • Pick v2 if: you're starting fresh, using Apollo Connectors for REST APIs,
    or want backpressure-based overload protection.
  • Pick v1 if: you have an existing deployment and haven't migrated yet.
    Note: Apollo ended active support for v1.x. The v2.10 LTS (Dec 2025)
    is the current baseline. Migration is strongly recommended.

  Tip: If you have an existing router.yaml, you can auto-migrate it:
    router config upgrade router.yaml
```

Store the selection as `ROUTER_VERSION=v1|v2` to gate all subsequent template generation.

## Step 2: Environment Selection

Ask: **Production** or **Development**?

- **Production**: security-hardened defaults (introspection off, sandbox off, homepage off, subgraph errors hidden, auth required, health check on)
- **Development**: open defaults (introspection on, sandbox on, errors exposed, text logging)

Load the appropriate base template from:
- `templates/{version}/production.yaml`
- `templates/{version}/development.yaml`

## Step 3: Feature Selection

Ask which features to include:

- [ ] JWT Authentication
- [ ] CORS (almost always yes for browser clients)
- [ ] Operation Limits
- [ ] Traffic Shaping / Rate Limiting
- [ ] Telemetry (Prometheus, OTLP tracing, JSON logging)
- [ ] APQ (Automatic Persisted Queries)
- [ ] Connectors (REST API integration — Router v2 only; GA key is `connectors`, early v2 preview key was `preview_connectors`)
- [ ] Subscriptions
- [ ] Header Propagation

## Step 4: Gather Parameters

For each selected feature, collect required values.

- Use section templates from `templates/{version}/sections/` for `auth`, `cors`, `headers`, `limits`, `telemetry`, and `traffic-shaping`.
- For Connectors in v2, use `templates/v2/sections/connectors.yaml` as the source.
- For APQ and subscriptions, copy the snippet from the selected base template (`templates/{version}/production.yaml` or `templates/{version}/development.yaml`) or from references.
- Only offer Connectors when `ROUTER_VERSION=v2`.

### CORS
- List of allowed origins (never use `"*"` for production)

### JWT Authentication
- JWKS URL
- Issuer(s) — note: v1 uses singular `issuer`, v2 uses plural `issuers` array

### Connectors (v2 only)
- Subgraph name and source name (used as `connectors.sources.<subgraph>.<source>`)
- Optional `$config` values for connector runtime configuration
- If migrating old v2 preview config, rename `preview_connectors` to `connectors`

### Operation Limits
Present the tuning guidance:

```
Operation depth limit controls how deeply nested a query can be.

  Router default: 100 (permissive — allows very deep queries)
  Recommended starting point: 50

  Lower values (15–25) are more secure but will reject legitimate queries
  in schemas with deep entity relationships or nested fragments.
  Higher values (75–100) are safer for compatibility but offer less
  protection against depth-based abuse.

  Tip: Run your router in warn_only mode first to see what depths your
  real traffic actually uses, then tighten:
    limits:
      warn_only: true

What max_depth would you like? [default: 50]
```

The same principle applies to `max_height`, `max_aliases`, and `max_root_fields`.

### Telemetry
- OTEL collector endpoint (default: `http://otel-collector:4317`)
- Prometheus listen port (default: `9090`)
- Trace sampling rate (default: `0.1` = 10%)

### Traffic Shaping
- Client-facing rate limit capacity (default: 1000 req/s)
- Router timeout (default: 60s)
- Subgraph timeout (default: 30s)

## Step 5: Generate Config

1. Load the correct version template from `templates/{version}/`
2. Assemble section templates for supported sectioned features, then merge base-template snippets for APQ/subscriptions as needed
3. Inject user-provided parameters
4. Add a comment block at the top stating the target version

## Step 6: Validate

Run the [post-generation checklist](validation/checklist.md):

- [ ] All env vars referenced in config are documented
- [ ] CORS origins don't include wildcards (production)
- [ ] Rate limiting is on `router:` (client-facing), not only `all:` (subgraph)
- [ ] JWT uses `issuers` (v2) not `issuer` (v1), or vice versa
- [ ] If production: introspection=false, sandbox=false, subgraph_errors=false
- [ ] Health check is enabled
- [ ] Homepage is disabled (production)
- [ ] Run: `router config validate <file>` if Router binary is available

## Required Validation Gate (always run)

After generating or editing any `router.yaml`, you MUST:

1. Run `validation/checklist.md` and report pass/fail for each checklist item.
2. Run `router config validate <path-to-router.yaml>` if Router CLI is available.
3. If Router CLI is unavailable, state that explicitly and still complete the checklist.
4. Do not present the configuration as final until validation is completed.

## Step 7: Conditional Next Steps Handoff

After answering any Apollo Router request (config generation, edits, validation, or general Router guidance), decide whether the user already has runnable prerequisites:

- GraphOS-managed path: `APOLLO_KEY` + `APOLLO_GRAPH_REF`, or
- Local path: a composed `supergraph.graphql` plus reachable subgraphs

If prerequisites are already present, do not add extra handoff text.

If prerequisites are missing or unknown, end with a concise **Next steps** handoff (1-3 lines max) that is skill-first and command-free:

1. Suggest the `rover` skill to compose or fetch the supergraph schema.
2. Suggest continuing with `apollo-router` once the supergraph is ready to validate and run with the generated config.
3. If subgraphs are missing, suggest `apollo-server`, `graphql-schema`, and `graphql-operations` skills to scaffold and test.

Do not include raw shell commands in this handoff unless the user explicitly asks for commands.

## Quick Start (skill-first)

1. Use this `apollo-router` skill to generate or refine `router.yaml` for your environment.
2. Choose a runtime path:
   - GraphOS-managed path: provide `APOLLO_KEY` and `APOLLO_GRAPH_REF` (no local supergraph composition required).
   - Local supergraph path: use `graphql-schema` + `apollo-server` to define/run subgraphs, then use `graphql-operations` for smoke tests, then use the `rover` skill to compose or fetch `supergraph.graphql`.
3. Use this `apollo-router` skill to validate readiness (`validation/checklist.md`) and walk through runtime startup inputs.

Default endpoint remains `http://localhost:4000` when using standard Router listen defaults.

If the user asks for executable shell commands, provide them on request. Otherwise keep Quick Start guidance skill-oriented.

## Running Modes

| Mode | Command | Use Case |
|------|---------|----------|
| Local schema | `router --supergraph ./schema.graphql` | Development, CI/CD |
| GraphOS managed | `APOLLO_KEY=... APOLLO_GRAPH_REF=my-graph@prod router` | Production with auto-updates |
| Development | `router --dev --supergraph ./schema.graphql` | Local development |
| Hot reload | `router --hot-reload --supergraph ./schema.graphql` | Schema changes without restart |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `APOLLO_KEY` | API key for GraphOS |
| `APOLLO_GRAPH_REF` | Graph reference (`graph-id@variant`) |
| `APOLLO_ROUTER_CONFIG_PATH` | Path to `router.yaml` |
| `APOLLO_ROUTER_SUPERGRAPH_PATH` | Path to supergraph schema |
| `APOLLO_ROUTER_LOG` | Log level (off, error, warn, info, debug, trace) |
| `APOLLO_ROUTER_LISTEN_ADDRESS` | Override listen address |

## Reference Files

- [Configuration](references/configuration.md) — YAML configuration reference
- [Headers](references/headers.md) — Header propagation and manipulation
- [Plugins](references/plugins.md) — Rhai scripts and coprocessors
- [Telemetry](references/telemetry.md) — Tracing, metrics, and logging
- [Connectors](references/connectors.md) — Router v2 connectors configuration
- [Troubleshooting](references/troubleshooting.md) — Common issues and solutions
- [Divergence Map](divergence-map.md) — v1 ↔ v2 config differences
- [Validation Checklist](validation/checklist.md) — Post-generation checks

## CLI Reference

```
router [OPTIONS]

Options:
  -s, --supergraph <PATH>    Path to supergraph schema file
  -c, --config <PATH>        Path to router.yaml configuration
      --dev                  Enable development mode
      --hot-reload           Watch for schema changes
      --log <LEVEL>          Log level (default: info)
      --listen <ADDRESS>     Override listen address
  -V, --version              Print version
  -h, --help                 Print help
```

## Ground Rules

- ALWAYS determine the target Router version (v1 or v2) before generating config
- DEFAULT to v2 for new projects
- ALWAYS include a comment block at top of generated config stating the target version
- ALWAYS use `--dev` mode for local development (enables introspection and sandbox)
- ALWAYS disable introspection, sandbox, and homepage in production
- PREFER GraphOS managed mode for production (automatic updates, metrics)
- USE `--hot-reload` for local development with file-based schemas
- NEVER expose `APOLLO_KEY` in logs or version control
- USE environment variables (`${env.VAR}`) for all secrets and sensitive config
- PREFER YAML configuration over command-line arguments for complex setups
- TEST configuration changes locally before deploying to production
- WARN if user enables `allow_any_origin` or wildcard CORS in production
- RECOMMEND `router config upgrade router.yaml` for v1 → v2 migration instead of regenerating from scratch
- MUST run `validation/checklist.md` after every router config generation or edit
- MUST run `router config validate <file>` when Router CLI is available
- MUST report when CLI validation could not run (for example, Router binary missing)
- MUST append a brief conditional handoff when runtime prerequisites are missing or unknown
- MUST make this handoff skill-first and avoid raw shell commands unless the user explicitly requests commands
- MUST keep Quick Start guidance skill-first and command-free unless the user explicitly requests commands
- MUST state that Rover is required only for the local supergraph path; GraphOS-managed runtime does not require local Rover composition
- USE `max_depth: 50` as the default starting point, not 15 (too aggressive) or 100 (too permissive)
- RECOMMEND `warn_only: true` for initial limits rollout to observe real traffic before enforcing
