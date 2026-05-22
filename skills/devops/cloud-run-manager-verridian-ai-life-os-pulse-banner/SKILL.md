---
name: Cloud Run Manager
description: Tool suite for deploying and managing Google Cloud Run services. Use for deployments, logging, and service inspection.
---

# Cloud Run Manager Skill

This skill grants access to the Google Cloud Run MCP tools. Use this to manage the lifecycle of containerized applications.

## When to use

- Deploying new services (source or container based).
- Inspecting running services.
- Fetching service logs for debugging.
- Listing projects and services.

## Available Tools (Context Loaded)

The following tools are available via the `cloudrun` MCP server:

### Deployment

- `mcp_cloudrun_create_project`: Initialize a new GCP project.
- `mcp_cloudrun_deploy_container_image`: Deploy an existing image (e.g., from GCR/Artifact Registry).
- `mcp_cloudrun_deploy_local_folder`: Deploy source code directly from a local path.
- `mcp_cloudrun_deploy_file_contents`: Deploy ad-hoc files (useful for quick tests).

### Management & Observability

- `mcp_cloudrun_list_projects`: View available GCP projects.
- `mcp_cloudrun_list_services`: List services in a project.
- `mcp_cloudrun_get_service`: Get detailed status/config of a generic service.
- `mcp_cloudrun_get_service_log`: Retrieve logs and error messages.

## Best Practices

1. **Project ID**: Always confirm the `project` ID with the user or via `list_projects` before deploying.
2. **Region**: Default to `us-central1` if unspecified, or ask the user.
3. **Logs**: usage of `get_service_log` is expensive; request specific timeframes or limits if possible.

## Example Workflow

1. User: "Deploy this folder to Cloud Run."
2. Agent: Calls `mcp_cloudrun_list_projects` to verify destination.
3. Agent: Calls `mcp_cloudrun_deploy_local_folder`.
