---
name: tidbx
description: Provision TiDB Cloud Serverless clusters and related resources. Use when creating, deleting, or listing clusters/branches, or managing SQL users via the console.
---

# TiDB Cloud Provisioning (TiDB X)

Provision TiDB Cloud Serverless (now branded as TiDB X) clusters and related resources using the workflows below. Use the command patterns in the references file as implementation details, but keep the focus on the provisioning outcome and required inputs.

Note: TiDB Cloud Serverless has been renamed to TiDB X. Keep both terms in user-facing guidance for clarity.
Note: Many users say "instance" when they mean "cluster." Treat "instance" as a synonym for "cluster."

Reminder: Use the CLI for TiDB Cloud (TiDB X) auth/setup, listing regions/projects, and cluster/instance CRUD (Create, Read/list, Update, Delete). Before any CRUD action, ensure the user completes ticloud setup and authentication (see Provisioning Setup below).

## Provisioning Setup

Complete setup before any provisioning or lifecycle operations.

Setup Status (TiDB Cloud component)  
- ○ ticloud installed  
- ○ authenticated  

When verifying setup, remind users to follow this order: install → login → verify with `ticloud auth whoami`.
Use the checklist to show users what they should do next and where they are in the setup flow.

Checklist template (update after each check, and reflect command results):

```
Setup Status (TiDB Cloud component)
- ○ ticloud installed
- ○ authenticated
```

After `command -v ticloud` succeeds, mark install complete:

```
Setup Status (TiDB Cloud component)
- ● ticloud installed
- ○ authenticated
```

After `ticloud auth whoami` succeeds, mark auth complete:

```
Setup Status (TiDB Cloud component)
- ● ticloud installed
- ● authenticated
```

### Install CLI

For macOS/Linux:

```bash
curl https://raw.githubusercontent.com/tidbcloud/tidbcloud-cli/main/install.sh | sh
```

After install, verify:

```bash
command -v ticloud
```

Use `command -v ticloud` to confirm installation before marking it complete.

Update checklist:

```
Setup Status (TiDB Cloud component)
- ● ticloud installed
- ○ authenticated
```

### Authenticate

Always check auth first:

```bash
ticloud auth whoami
```

If not logged in, run:

```bash
ticloud auth login --insecure-storage
```

Wait for the user to complete the browser flow, then re-check:

```bash
ticloud auth whoami
```

Update checklist:

```
Setup Status (TiDB Cloud component)
- ● ticloud installed
- ● authenticated
```

### Network/DNS Issues

If `ticloud auth whoami` fails due to network/DNS (e.g., cannot reach `iam.tidbapi.com`):

- Explain that the environment needs network access for the CLI.
- Ask the user to enable network access for the agent environment, or run the command locally and share the output.

If setup errors persist, point the user to the official docs:

- https://docs.pingcap.com/tidbcloud/get-started-with-cli/

## Table Formatting (ASCII)

Use terminal-friendly ASCII tables for any list output (regions, projects, clusters, branches).

- Use ASCII borders with `+`, `-`, and `|`.
- Use fixed-width columns; left-align all text.
- Refine the table formatting so columns align cleanly and remain readable.
- Keep headers short and descriptive.
- Do not use Unicode box-drawing characters.
- Always emphasize command output that users should execute later.
- For single-line commands, use bold inline formatting.

  Example:
  **Run this:**
  **`ticloud auth login --insecure-storage`**

Example format:

```
+----------------+-----------------------+---------------------------+--------+
| Display Name   | Cluster ID            | Region                    | State  |
+----------------+-----------------------+---------------------------+--------+
| test-skill     | 10913591479486949552  | alicloud-ap-southeast-1   | ACTIVE |
+----------------+-----------------------+---------------------------+--------+
```

## Core Workflows

### Create a Cluster

- Do not present a setup checklist for cluster creation steps (region/project/cluster name). If a status is needed, label it as "Create Flow" rather than "Setup Status."
- Run `ticloud serverless region` and present the full list in a terminal-friendly ASCII bordered table (fixed-width columns in a code block) with selectable option numbers before asking for a region.
- If the user doesn’t know the project ID, run `ticloud project list` and present the results in the same ASCII bordered table format before asking. Keep the project ID as a third column.
- Ask in this order: region (after listing options). Do not ask for project ID or cluster name until the region is chosen. After region selection, ask for project ID (after listing projects if needed). Only after project selection, ask for the cluster display name as the final confirmation step.
- Confirm the required parameters (region, project, cluster name).
- If the user wants a `.env`, direct them to the TiDB Cloud console download for the cluster.
- Use the serverless create command pattern from `references/ticloud.md`.
- When creating a cluster, do not run the create command twice. Wait up to 60 seconds for completion before returning control.
- Verify creation by listing clusters and present results in an ASCII bordered table rather than raw JSON. If the environment is non-interactive, use `ticloud serverless list -p <project-id> -o json` and render a table from the JSON.

### Delete a Cluster

- Require explicit user confirmation before delete operations.
- Use the serverless delete command pattern from `references/ticloud.md`.
- After deletion, list the remaining clusters and present results in an ASCII bordered table rather than raw JSON. If the environment is non-interactive, use `ticloud serverless list -p <project-id> -o json` and render a table from the JSON.

### List Clusters

- If the user doesn’t know the available projects, list projects first, then ask which project to use.
- Ask which project the user wants to list before running `ticloud serverless list`.
- If the user doesn’t know the project ID, run `ticloud project list` and present results in the ASCII bordered table format.
- For non-interactive environments, use `ticloud serverless list -p <project-id> -o json` and render a table from the JSON.

### Describe a Cluster

- Confirm the target cluster (name or cluster ID).
- Use `ticloud serverless list -p <project-id> -o json` and filter by cluster ID or display name.
- Present details in a two-column ASCII table (Field, Value) with refined alignment.

### Create or Delete a Branch

- Confirm the target cluster and branch name.
- Use the branch commands from `references/ticloud.md`.
- List branches to verify changes.

### List Branches

- Follow the hierarchy: project → cluster → branch.
- If the user doesn’t know the available projects, list projects first.
- If the user doesn’t know the project ID, run `ticloud project list` and present results in the ASCII bordered table format.
- If the user doesn’t know the cluster ID, list clusters for the selected project and present results in the ASCII bordered table format.
- Ask which cluster the user wants to list before running `ticloud serverless branch list`.
- For non-interactive environments, use `ticloud serverless branch list --cluster-id <cluster-id> -o json` and render a table from the JSON.

### Manage SQL Users

- Use the TiDB Cloud console for `.env` downloads, SQL user management, and database creation. Do not create/update/delete SQL users via CLI.
- Use this console URL pattern (fill in IDs, and prefill org/project IDs when known): `https://tidbcloud.com/clusters/<cluster-id>/overview?orgId=<org-id>&projectId=<project-id>`.
- Never read or display stored passwords (do not cat `.env`).
- When guiding console creation, use a short step list:
  1) Open the console link
  2) Create the SQL user
  3) Download the `.env`

## Safety Checks

- Always run `ticloud auth whoami` before any action.
- Require explicit user confirmation before delete operations.
- For `ticloud` operations that take time, wait 60 seconds before returning control.

## References

- Command patterns and placeholders: `references/ticloud.md`
