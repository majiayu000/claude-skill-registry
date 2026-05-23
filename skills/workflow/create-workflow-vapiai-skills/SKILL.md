---
name: create-workflow
description: Build visual conversation workflows in Vapi with nodes for conversation steps, tool execution, conditional branching, and handoffs. Use when creating structured multi-step voice interactions that need deterministic flow control beyond what a single assistant prompt provides.
license: MIT
compatibility: Requires internet access and a Vapi API key (VAPI_API_KEY).
metadata:
  author: vapi
  version: "1.0"
---

# Vapi Workflow Creation

Build structured conversation workflows with visual node-based flows. Workflows provide deterministic control over conversation steps, branching logic, and tool execution.

> **Setup:** Ensure `VAPI_API_KEY` is set. See the `setup-api-key` skill if needed.

## When to Use Workflows vs Assistants

| Feature | Assistant | Workflow |
|---------|-----------|----------|
| Simple conversations | Best choice | Over-engineered |
| Multi-step processes | Can work with good prompting | Best choice |
| Deterministic flow | Hard to guarantee | Built-in |
| Conditional branching | Prompt-dependent | Visual nodes |
| Complex state management | Difficult | Native support |

## Quick Start

Workflows are best built in the **Vapi Dashboard** visual editor at https://dashboard.vapi.ai — but they can also be configured via API.

### Dashboard Workflow

1. Go to https://dashboard.vapi.ai
2. Navigate to **Workflows**
3. Click **Create Workflow**
4. Add nodes: Conversation, Tool, Condition, Handoff
5. Connect nodes to define the flow
6. Publish and attach to a phone number or call

### Using a Workflow in a Call

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflowId": "your-workflow-id",
    "phoneNumberId": "your-phone-number-id",
    "customer": {
      "number": "+11234567890"
    }
  }'
```

## Node Types

### Conversation Node

The core building block — the assistant has a conversation within defined boundaries:

- **System prompt** specific to this step
- **Model and voice** configuration
- **Exit conditions** that trigger transitions to other nodes
- **Variables** to extract and pass between nodes

### Tool Node

Execute a tool (API call, function) and use the result in subsequent nodes.

### Condition Node

Branch the flow based on variables or conversation state.

### Handoff Node

Transfer to another workflow, assistant, or phone number.

## Workflow Patterns

### Appointment Scheduling Flow

```
[Greeting] → [Collect Date] → [Check Availability (Tool)] → [Confirm Booking] → [Goodbye]
                                         ↓ (unavailable)
                                 [Suggest Alternatives] → [Confirm Booking]
```

### Lead Qualification Flow

```
[Introduction] → [Ask Budget] → [Ask Timeline] → [Qualify (Condition)]
                                                        ↓ (qualified)
                                                  [Schedule Demo]
                                                        ↓ (not qualified)
                                                  [Send Resources]
```

### Support Triage Flow

```
[Greeting] → [Identify Issue (Condition)]
                  ↓ (billing)        ↓ (technical)        ↓ (other)
            [Billing Flow]    [Tech Support Flow]    [General Help]
```

## Attaching Workflows

### To a Phone Number

```bash
curl -X PATCH https://api.vapi.ai/phone-number/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflowId": "your-workflow-id"
  }'
```

### In an Outbound Call

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflowId": "your-workflow-id",
    "phoneNumberId": "your-phone-number-id",
    "customer": { "number": "+11234567890" }
  }'
```

## References

- [Vapi Workflows Docs](https://docs.vapi.ai/workflows/quickstart) — Official guide
- [Workflow Examples](https://docs.vapi.ai/workflows/examples/appointment-scheduling) — Common patterns

## Additional Resources

This skills repository includes a **Vapi documentation MCP server** (`vapi-docs`) that gives your AI agent access to the full Vapi knowledge base. Use the `searchDocs` tool to look up anything beyond what this skill covers — advanced configuration, troubleshooting, SDK details, and more.

**Auto-configured:** If you cloned or installed these skills, the MCP server is already configured via `.mcp.json` (Claude Code), `.cursor/mcp.json` (Cursor), or `.vscode/mcp.json` (VS Code Copilot).

**Manual setup:** If your agent doesn't auto-detect the config, run:
```bash
claude mcp add vapi-docs -- npx -y mcp-remote https://docs.vapi.ai/_mcp/server
```

See the [README](../README.md#vapi-documentation-server-mcp) for full setup instructions across all supported agents.
