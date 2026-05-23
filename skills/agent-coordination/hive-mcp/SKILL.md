---
name: hive-mcp
description: Use the Agent Hive MCP (Model Context Protocol) server for programmatic project management. Use this skill when working with MCP tools to list projects, claim/release projects, update status, add notes, or query dependencies through the MCP interface.
---

# Hive MCP Server

The Hive MCP server exposes Agent Hive functionality as MCP tools, enabling AI agents like Claude to programmatically manage projects through standardized tool interfaces.

## Overview

MCP (Model Context Protocol) provides a standardized way for AI agents to interact with external tools. The Hive MCP server exposes project management operations as callable tools.

## Setup

### Configuration

Add the Hive MCP server to your Claude configuration:

**For Claude Desktop (`~/.config/claude/claude_desktop_config.json`):**

```json
{
  "mcpServers": {
    "hive": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.hive_mcp"],
      "cwd": "/path/to/agent-hive",
      "env": {
        "HIVE_BASE_PATH": "/path/to/agent-hive",
        "COORDINATOR_URL": "http://localhost:8080"
      }
    }
  }
}
```

**For DevContainer (`.devcontainer/devcontainer.json`):**

```json
{
  "mcpServers": {
    "hive": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.hive_mcp"]
    }
  }
}
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HIVE_BASE_PATH` | Root path of the hive | Current directory |
| `COORDINATOR_URL` | URL of coordination server | Not set (optional) |

## Available Tools

### Project Discovery

#### `list_projects`
List all projects in the hive with their metadata.

```json
{
  "name": "list_projects",
  "arguments": {}
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "count": 3,
    "projects": [
      {
        "project_id": "demo",
        "status": "active",
        "owner": null,
        "priority": "medium",
        "tags": ["example"]
      }
    ]
  }
}
```

#### `get_ready_work`
Get projects ready for an agent to claim.

```json
{
  "name": "get_ready_work",
  "arguments": {}
}
```

Returns projects that are:
- Status: `active`
- Not blocked
- No current owner
- Dependencies satisfied

#### `get_project`
Get full details of a specific project.

```json
{
  "name": "get_project",
  "arguments": {
    "project_id": "demo"
  }
}
```

**Response includes:**
- All metadata fields
- Full markdown content
- Dependency information

### Project Ownership

#### `claim_project`
Claim a project by setting ownership.

```json
{
  "name": "claim_project",
  "arguments": {
    "project_id": "demo",
    "agent_name": "claude-sonnet-4"
  }
}
```

**Success response:**
```json
{
  "success": true,
  "data": {
    "project_id": "demo",
    "owner": "claude-sonnet-4"
  }
}
```

**Failure (already claimed):**
```json
{
  "success": false,
  "error": "Project already claimed by grok-beta"
}
```

#### `release_project`
Release ownership of a project.

```json
{
  "name": "release_project",
  "arguments": {
    "project_id": "demo"
  }
}
```

### Status Management

#### `update_status`
Update the status of a project.

```json
{
  "name": "update_status",
  "arguments": {
    "project_id": "demo",
    "status": "completed"
  }
}
```

**Valid statuses:**
- `active` - Ready for work
- `pending` - Not yet started
- `blocked` - Waiting for external input
- `completed` - All tasks done

#### `add_note`
Add a timestamped note to Agent Notes section.

```json
{
  "name": "add_note",
  "arguments": {
    "project_id": "demo",
    "agent": "claude-sonnet-4",
    "note": "Completed research phase. Found 5 relevant sources."
  }
}
```

### Dependency Analysis

#### `get_dependencies`
Get dependency information for a project.

```json
{
  "name": "get_dependencies",
  "arguments": {
    "project_id": "demo"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "is_blocked": false,
    "reasons": [],
    "blocking_projects": [],
    "in_cycle": false,
    "cycle": []
  }
}
```

#### `get_dependency_graph`
Get full dependency graph for all projects.

```json
{
  "name": "get_dependency_graph",
  "arguments": {}
}
```

### Coordinator Integration

These tools require `COORDINATOR_URL` to be configured.

#### `coordinator_status`
Check if coordination server is available.

```json
{
  "name": "coordinator_status",
  "arguments": {}
}
```

#### `coordinator_claim`
Claim via coordination server (prevents conflicts).

```json
{
  "name": "coordinator_claim",
  "arguments": {
    "project_id": "demo",
    "agent_name": "claude-sonnet-4",
    "ttl_seconds": 3600
  }
}
```

#### `coordinator_release`
Release claim via coordination server.

```json
{
  "name": "coordinator_release",
  "arguments": {
    "project_id": "demo"
  }
}
```

#### `coordinator_reservations`
Get all active reservations.

```json
{
  "name": "coordinator_reservations",
  "arguments": {}
}
```

## Tool Reference

| Tool | Description | Required Args |
|------|-------------|---------------|
| `list_projects` | List all projects | None |
| `get_ready_work` | Find claimable projects | None |
| `get_project` | Get project details | `project_id` |
| `claim_project` | Claim ownership | `project_id`, `agent_name` |
| `release_project` | Release ownership | `project_id` |
| `update_status` | Change project status | `project_id`, `status` |
| `add_note` | Add agent note | `project_id`, `agent`, `note` |
| `get_dependencies` | Check blocking status | `project_id` |
| `get_dependency_graph` | Full dependency view | None |
| `coordinator_status` | Coordinator health | None |
| `coordinator_claim` | Real-time claim | `project_id`, `agent_name` |
| `coordinator_release` | Real-time release | `project_id` |
| `coordinator_reservations` | Active reservations | None |

## Response Format

All tools return a standardized response:

```json
{
  "success": true|false,
  "data": { ... },      // Present on success
  "error": "message"    // Present on failure
}
```

## Workflow Example

### Starting Work on a Project

```
1. list_projects()           # See what's available
2. get_ready_work()          # Find claimable projects
3. get_project("my-proj")    # Review project details
4. claim_project("my-proj", "claude-sonnet-4")
5. [Do the work]
6. add_note("my-proj", "claude-sonnet-4", "Completed task X")
7. update_status("my-proj", "completed")
8. release_project("my-proj")
```

### With Coordinator (Parallel-Safe)

```
1. coordinator_status()      # Verify coordinator is up
2. coordinator_claim("my-proj", "claude-sonnet-4", 3600)
3. claim_project("my-proj", "claude-sonnet-4")  # Also update AGENCY.md
4. [Do the work]
5. release_project("my-proj")
6. coordinator_release("my-proj")
```

## Best Practices

1. **Check ready work first** - Use `get_ready_work` to find available projects
2. **Read before claiming** - Use `get_project` to understand the work
3. **Use coordinator for parallel agents** - Prevents race conditions
4. **Add notes for transparency** - Document your progress
5. **Release when done** - Don't hold claims unnecessarily
6. **Handle errors gracefully** - Check `success` field in responses

## Troubleshooting

### "Project not found"
Verify project_id matches exactly (case-sensitive).

### "Project already claimed"
Another agent owns the project. Use `get_project` to see current owner.

### "Coordinator unavailable"
- Check `COORDINATOR_URL` is set
- Verify coordinator server is running
- Test with `coordinator_status` tool

### "Failed to update project"
- Verify AGENCY.md file exists
- Check file permissions
- Ensure path is within HIVE_BASE_PATH
