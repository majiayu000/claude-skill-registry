---
name: environment
description: This skill should be used when the user asks "what's the config", "show me the configuration", "what variables are set", "environment config", "service config", "railway config", or wants to add/set/delete variables, change build/deploy settings, scale replicas, connect repos, or delete services.
allowed-tools: Bash(railway:*)
---

# Environment Configuration

Read and edit Railway environment configuration using the CLI.

## Prerequisites

Requires Railway CLI **v4.27.3+**. Check with:

```bash
railway --version
```

If below 4.27.3, upgrade:

```bash
railway upgrade
```

## Quick Actions

**When user asks "what's the config" or "show configuration":**

```bash
railway environment config --json
```

Present: source (repo/image), build settings, deploy settings, variables per service.

**When user asks "what variables" or "show env vars":**

Same command — `railway environment config --json` includes variables per service and shared variables.

For **rendered** (resolved) variable values: `railway variables --json`

## When to Use

- User wants to create a new environment
- User wants to duplicate an environment (e.g., "copy production to staging")
- User wants to switch to a different environment
- User asks about current build/deploy settings, variables, replicas, health checks, domains
- User asks to change service source (Docker image, branch, commit, root directory)
- User wants to connect a service to a GitHub repo
- User wants to deploy from a GitHub repo (create empty service first via `new` skill, then use this)
- User asks to change build or start command
- User wants to add/update/delete environment variables
- User wants to change replica count or configure health checks
- User asks to delete a service, volume, or bucket
- Auto-fixing build errors detected in logs

## Create Environment

Create a new environment in the linked project:

```bash
railway environment new <name>
```

Duplicate an existing environment:

```bash
railway environment new staging --duplicate production
```

With service-specific variables:

```bash
railway environment new staging --duplicate production --service-variable api PORT=3001
```

## Switch Environment

Link a different environment to the current directory:

```bash
railway environment <name>
```

Or by ID:

```bash
railway environment <environment-id>
```

## Get Context

**JSON output** — project/environment IDs and service list:

```bash
railway status --json
```

Extract:

- `project.id` — project ID
- `environment.id` — environment ID

**Plain output** — linked service name:

```bash
railway status
```

Shows `Service: <name>` line with the currently linked service.

### Resolve Service ID

Get service IDs from the environment config:

```bash
railway environment config --json | jq '.services | keys'
```

Map service IDs to names via status:

```bash
railway status --json
```

The `project.services` array contains `{ id, name }` for each service. Match against the service keys from `environment config`.

## Read Configuration

Fetch current environment configuration:

```bash
railway environment config --json
```

### Response Structure

```json
{
  "services": {
    "<serviceId>": {
      "source": { "repo": "...", "branch": "main" },
      "build": { "buildCommand": "npm run build", "builder": "NIXPACKS" },
      "deploy": {
        "startCommand": "npm start",
        "multiRegionConfig": { "us-west2": { "numReplicas": 1 } }
      },
      "variables": { "NODE_ENV": { "value": "production" } },
      "networking": { "serviceDomains": {}, "customDomains": {} }
    }
  },
  "sharedVariables": { "DATABASE_URL": { "value": "..." } }
}
```

For complete field reference, see [reference/environment-config.md](references/environment-config.md).

For variable syntax and service wiring patterns, see [reference/variables.md](references/variables.md).

## Get Rendered Variables

`environment config` returns **unrendered** variables — template syntax like `${{shared.DOMAIN}}` is preserved. This is correct for management/editing.

To see **rendered** (resolved) values as they appear at runtime:

```bash
# Current linked service
railway variables --json

# Specific service
railway variables --service <service-name> --json
```

**When to use:**

- Debugging connection issues (see actual URLs/ports)
- Verifying variable resolution is correct
- Viewing Railway-injected values (RAILWAY\_\*)

## Edit Configuration

Pass a JSON patch to `railway environment edit` to apply changes. The patch is merged with existing config and committed immediately, triggering deploys.

```bash
railway environment edit --json <<< '<json-patch>'
```

With a commit message:

```bash
railway environment edit -m "description of change" --json <<< '<json-patch>'
```

### Examples

**Set build command:**

```bash
railway environment edit --json <<< '{"services":{"SERVICE_ID":{"build":{"buildCommand":"npm run build"}}}}'
```

**Add variable:**

```bash
railway environment edit -m "add API_KEY" --json <<< '{"services":{"SERVICE_ID":{"variables":{"API_KEY":{"value":"secret"}}}}}'
```

**Delete variable:**

```bash
railway environment edit --json <<< '{"services":{"SERVICE_ID":{"variables":{"OLD_VAR":null}}}}'
```

**Delete service:**

```bash
railway environment edit --json <<< '{"services":{"SERVICE_ID":{"isDeleted":true}}}'
```

**Set replicas:**

```bash
railway environment edit --json <<< '{"services":{"SERVICE_ID":{"deploy":{"multiRegionConfig":{"us-west2":{"numReplicas":3}}}}}}'
```

**Add shared variable:**

```bash
railway environment edit --json <<< '{"sharedVariables":{"DATABASE_URL":{"value":"postgres://..."}}}'
```

### Batching Multiple Changes

Include multiple fields in a single patch to apply them atomically:

```bash
railway environment edit -m "configure build, start, and env" --json <<< '{"services":{"SERVICE_ID":{"build":{"buildCommand":"npm run build"},"deploy":{"startCommand":"npm start"},"variables":{"NODE_ENV":{"value":"production"}}}}}'
```

## Error Handling

### Command Not Found

If `railway environment edit` is not recognized, upgrade the CLI:

```bash
railway upgrade
```

### Service Not Found

```
Service "foo" not found in project. Available services: api, web, worker
```

### Invalid Configuration

Common issues:

- `buildCommand` and `startCommand` cannot be identical
- `buildCommand` only valid with NIXPACKS builder
- `dockerfilePath` only valid with DOCKERFILE builder

### No Permission

```
You don't have permission to modify this environment. Check your Railway role.
```

### No Linked Project

```
No project linked. Run `railway link` to link a project.
```

## Composability

- **Create service**: Use `service` skill
- **View logs**: Use `deployment` skill
- **Add domains**: Use `domain` skill
- **Deploy local code**: Use `deploy` skill
