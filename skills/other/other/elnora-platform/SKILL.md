---
name: elnora-platform
description: >
  Use when the user asks about Elnora platform, Elnora AI, bioprotocol generation,
  platform API, elnora projects, elnora tasks, elnora files, protocol generation,
  platform search, elnora orgs, elnora folders, elnora admin, API keys,
  elnora health, elnora auth, or any task involving the Elnora AI Platform.
  Routes to domain-specific sub-skills for token-efficient guidance.
---

# Elnora Platform

Route Elnora Platform queries to the correct sub-skill. Load only what is needed.

## What is Elnora?

Elnora is an AI-powered platform that helps researchers generate, optimize, and manage bioprotocols for wet-lab experiments. This plugin connects your agent to the Elnora Platform via MCP.

## Authentication

Auth is handled automatically by the MCP connection:

- **OAuth 2.1** (recommended): Browser popup on first use, tokens refresh automatically
- **API Key**: Set as Bearer token in MCP headers (create at platform.elnora.ai > Settings > API Keys)

No manual login required.

## Token Efficiency

All MCP tools support two optional params for reducing token usage:

| Param | Effect |
|-------|--------|
| `compact: true` | Strip null/empty values (~30-40% savings). Always use in agent workflows. |
| `fields: "id,name"` | Return only specified fields. Applied to each item in paginated results. |

## Routing Table

| Need | Sub-skill | Trigger keywords |
|------|-----------|------------------|
| List/get/create/update/archive projects, manage members | `elnora-projects` | project, workspace, create project, members |
| Create/manage/message tasks, protocol generation | `elnora-tasks` | task, protocol, send message, generate |
| Browse/read/upload/create/version/fork files | `elnora-files` | file, content, version history, upload, download, fork |
| Find tasks, files, or content by keyword | `elnora-search` | search, find, query, search file content |
| Manage project folder trees | `elnora-folders` | folder, create folder, move folder |
| Org management, members, billing, invitations, shared library | `elnora-orgs` | organization, org, billing, invite, library |
| Auth, API keys, account, health, diagnostics | `elnora-admin` | api key, health, account, feedback, audit, flags |
| What can the Elnora Agent do? (tools, search, memory) | `elnora-agent` | agent capabilities, agent tools, what can agent do |

## Organization Context

Most org-scoped tools (projects, tasks, files, folders, search) accept an
optional `org_id` parameter (UUID). When provided, the operation targets that
organization instead of the user's active org. The user must be a member of the
target org.

**Workflow for org switching:**
1. Call `elnora_list_orgs` first to discover available org IDs and names
2. Pass the target `org_id` to any org-scoped tool (e.g., `elnora_list_projects`, `elnora_create_task`)
3. By-ID tools (get, update, archive, delete) do NOT need `org_id` — they resolve via ownership

## ID Format

All IDs are UUIDs (e.g., `bfdc6fbd-40ed-4042-9ea7-c79a5ec90085`).

## Pagination

List endpoints return paginated results:

```json
{"items": [...], "page": 1, "pageSize": 25, "totalCount": N, "totalPages": N, "hasNextPage": true}
```

Use `page` and `pageSize` parameters (max 100). Check `hasNextPage` to paginate.

Message endpoints use cursor-based pagination: check `hasMore` and pass `cursor` from `nextCursor`.

## Common Workflow

Projects contain tasks and files. Typical flow:

1. `elnora_list_projects` — get project ID
2. `elnora_create_task` — start a conversation with Elnora AI
3. `elnora_send_message` — describe the protocol you need
4. `elnora_get_task_messages` — read the AI response
5. `elnora_list_files` — browse generated outputs
6. `elnora_get_file_content` — read a protocol file

## Quick Protocol Generation

For one-shot protocol generation, use `elnora_generate_protocol`:

- `description`: What protocol you need (e.g., "HEK 293 cell maintenance protocol")
- Returns the complete generated protocol

## Tool Discovery

Each sub-skill lists its own MCP tools with full parameter docs and workflow recipes. Load the relevant sub-skill from the routing table above to see available tools.
