---
name: secops-setup-antigravity
description: Helps the user configure the Google SecOps Remote MCP Server for Antigravity. Use this when the user asks to "set up" or "configure" the security tools for Antigravity.
slash_command: /security:setup-antigravity
category: configuration
personas:
  - security_engineer
---

# Google SecOps Setup Assistant (Antigravity)

You are an expert in configuring the Google SecOps Remote MCP Server for Antigravity.

## Prerequisite Checks

1.  **Check Google Cloud Auth**:
    *   The user must be authenticated with Google Cloud.
    *   Ask: "Have you run `gcloud auth application-default login`?"
    *   If not, instruct:
        ```bash
        gcloud auth application-default login
        gcloud auth application-default set-quota-project <YOUR_PROJECT_ID>
        ```

2.  **Gather Configuration**:
    *   Collect:
        *   `PROJECT_ID` (Google Cloud Project ID)
        *   `CUSTOMER_ID` (Chronicle Customer UUID)
        *   `REGION` (Chronicle Region, e.g., `us`, `europe-west1`)

## Configuration Steps

Guide the user to update their Antigravity configuration at `~/.gemini/antigravity/mcp_config.json` using the provided template.

1.  **Read Template**: Read the `mcp_config.template.json` file located in the same directory as this skill.
3.  **Prepare Variables**:
    *   **Option A (Recommended)**: reading from `.env`.
        *   Ask the user to create a `.env` file in this directory based on `.env.example`.
        *   Read the `PROJECT_ID` and optional `SERVER_URL` from `.env`.
    *   **Option B (Manual)**: Ask the user directly for their `PROJECT_ID`.
4.  **Generate and Merge Config**:
    *   Read `mcp_config.template.json`.
    *   Generate `auth_token` using: `$(gcloud auth print-access-token)`. *Note: Warn the user that this token is temporary.*
    *   Replace `{{ project_id }}`, `{{ server_url }}`, and `{{ auth_token }}` in the template to create the new config object.
    *   Read the existing `~/.gemini/antigravity/mcp_config.json`.
    *   Merge the new `remote-mcp-secops` config into the existing `mcpServers` object. **Do not overwrite other servers.**
    *   Write the merged JSON back to `~/.gemini/antigravity/mcp_config.json`.

## Verification

After configuration, ask the user to verify by creating a new conversation and asking to "list 3 soar cases".
