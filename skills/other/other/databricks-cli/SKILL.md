---
name: databricks-cli
description: Expert guidance for using the Databricks CLI to manage Databricks workspaces, clusters, jobs, pipelines, Unity Catalog, SQL warehouses, serving endpoints, secrets, bundles, and all other Databricks resources. Use this skill when running databricks commands, managing Databricks infrastructure, deploying bundles, querying serving endpoints, managing Unity Catalog objects, or automating Databricks workflows. Trigger keywords include "databricks", "databricks cli", "dbfs", "unity catalog", "databricks bundle", "databricks jobs", "databricks clusters", "sql warehouse", "serving endpoint", "databricks secrets".
---

# Databricks CLI

Comprehensive reference for the Databricks CLI (v0.205+). Covers authentication, all command groups, flags, and common patterns.

## Command syntax

```
databricks <command-group> [<command>] [<subcommand>] [args] [--flags]
```

Get help at any level with `-h` or `--help`.

## Authentication

### OAuth U2M (interactive, recommended)

```bash
# Workspace-level
databricks auth login --host https://<workspace>.cloud.databricks.com

# Account-level
databricks auth login --host https://accounts.cloud.databricks.com --account-id <id>
```

Saves credentials to `~/.databrickscfg` as a named profile. Tokens auto-refresh and expire in under an hour.

### OAuth M2M (service principals)

Add to `~/.databrickscfg`:

```ini
[my-sp-profile]
host = https://<workspace>.cloud.databricks.com
client_id = <service-principal-client-id>
client_secret = <service-principal-oauth-secret>
```

### Credential resolution order

1. Bundle settings files (if running from bundle directory)
2. Environment variables (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`, etc.)
3. `.databrickscfg` profiles

### Profile management

```bash
databricks auth profiles          # List all profiles
databricks auth env -p PROD       # Show profile settings
databricks auth token -p PROD     # Show current token
databricks auth describe          # Current auth config details
```

Use `-p <profile>` or `--profile <profile>` on any command. Default profile is `DEFAULT`.

## Global flags

| Flag                | Description                               |
| ------------------- | ----------------------------------------- |
| `--debug`           | Enable debug logging                      |
| `-h, --help`        | Display help                              |
| `-o, --output`      | Output format: `text` or `json`           |
| `-p, --profile`     | Config profile from `~/.databrickscfg`    |
| `--log-file`        | Log output file path                      |
| `--log-format`      | `text` or `json`                          |
| `--log-level`       | Logging verbosity                         |
| `--progress-format` | `default`, `append`, `inplace`, or `json` |
| `-t, --target`      | Bundle target                             |

## JSON input

Use `--json` with inline JSON or file reference:

```bash
# Inline (Linux/macOS)
databricks jobs create --json '{"name": "my-job", ...}'

# From file
databricks jobs create --json @job-config.json
```

Filter JSON output with `jq`:

```bash
databricks clusters get <id> | jq -r .cluster_name
```

## Direct REST API access

```bash
databricks api get /api/2.0/clusters/list
databricks api post /api/2.0/clusters/create --json '{"cluster_name": "test", ...}'
databricks api post /api/2.0/clusters/edit --json @edit-cluster.json
```

Supports: `get`, `post`, `put`, `patch`, `delete`, `head`.

## Command groups

For detailed subcommands, flags, and examples, see the reference files below.

### Compute and runtime

- **clusters** - Cluster lifecycle (create, start, edit, resize, terminate, delete, pin). See [references/compute.md](references/compute.md).
- **cluster-policies** - Cluster configuration rules.
- **libraries** - Install/uninstall packages on clusters. See [references/compute.md](references/compute.md).
- **instance-pools** - Manage cloud instance pools.
- **instance-profiles** - IAM instance profile administration (AWS).
- **policy-families** - Available policy templates.

### Jobs and pipelines

- **jobs** - Job lifecycle and run management (create, run-now, submit, cancel, repair, list-runs). See [references/jobs-pipelines.md](references/jobs-pipelines.md).
- **pipelines** - Lakeflow / DLT pipeline management and deployment. See [references/jobs-pipelines.md](references/jobs-pipelines.md).

### Workspace and files

- **fs** - File operations on Unity Catalog volumes and DBFS (cat, cp, ls, mkdir, rm). See [references/workspace.md](references/workspace.md).
- **workspace** - Notebooks and folders (import, export, list, delete, mkdirs). See [references/workspace.md](references/workspace.md).
- **repos** - Git repository management. See [references/workspace.md](references/workspace.md).
- **secrets** - Secret scopes, secrets, and ACLs. See [references/workspace.md](references/workspace.md).
- **git-credentials** - Personal access token registration for Git.

### Unity Catalog

- **catalogs** - Create, list, update, delete catalogs. See [references/unity-catalog.md](references/unity-catalog.md).
- **schemas** - Manage schemas within catalogs.
- **tables** - Table metadata (get, list, delete, exists).
- **volumes** - File storage with governance. See [references/unity-catalog.md](references/unity-catalog.md).
- **grants** - Data access authorisation. See [references/unity-catalog.md](references/unity-catalog.md).
- **credentials**, **storage-credentials** - Authentication for external storage.
- **connections** - External data source linkage.
- **functions** - User-defined function management.
- **metastores** - Top-level container management.
- **registered-models**, **model-versions** - MLflow registry in UC.
- **online-tables** - Low-latency data access.
- **quality-monitors** - Data quality metric tracking.

### SQL and analytics

- **warehouses** - SQL warehouse lifecycle (create, start, stop, edit, permissions). See [references/sql-analytics.md](references/sql-analytics.md).
- **queries** - SQL query CRUD. See [references/sql-analytics.md](references/sql-analytics.md).
- **alerts** - SQL alert management.
- **dashboards**, **lakeview** - Dashboard operations.
- **query-history** - Query execution history.
- **data-sources** - Data source listing.

### ML and serving

- **serving-endpoints** - Model endpoint deployment, querying, and AI Gateway. See [references/ml-serving.md](references/ml-serving.md).
- **experiments** - MLflow experiment and run management.
- **model-registry** - Model version and transition management.
- **feature-engineering** - Databricks Feature Store operations.
- **vector-search-endpoints**, **vector-search-indexes** - Embedding search infrastructure.

### Identity and access

- **auth** - Authentication management. See [references/identity.md](references/identity.md).
- **current-user** - Authenticated user info.
- **users**, **groups**, **service-principals** - Identity management.
- **permissions** - Access control for any resource type. See [references/identity.md](references/identity.md).

### Bundles (infrastructure as code)

- **bundle** - Deploy, run, validate, and manage Databricks Asset Bundles. See [references/bundles.md](references/bundles.md).
- **sync** - Local-to-workspace directory synchronisation.

### Account administration

- **account** - Multi-workspace account-level management (identity, Unity Catalog, billing, networking, OAuth). See [references/account.md](references/account.md).

### Utilities

- **completion** - Shell autocompletion setup.
- **labs** - Community extension management.
- **version** - CLI version information.
- **configure** - Legacy configuration command.

## Common patterns

### Wait vs no-wait

Long-running operations (cluster start, job run) block by default. Use `--no-wait` to return immediately, `--timeout` to set a deadline:

```bash
databricks clusters start <id> --no-wait
databricks jobs run-now <job-id> --timeout 30m
```

### Permission management

Most resource types support four permission commands:

```bash
databricks <resource> get-permission-levels <id>
databricks <resource> get-permissions <id>
databricks <resource> set-permissions <id> --json @perms.json
databricks <resource> update-permissions <id> --json @perms.json
```

### Pagination

List commands with large result sets support pagination:

```bash
databricks jobs list --limit 10 --page-token <token>
```

### Proxy support

Set `HTTPS_PROXY` environment variable to route requests through a proxy.
