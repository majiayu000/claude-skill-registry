---
name: orchardcore-ai-a2a-client
description: Skill for configuring the CrestApps A2A Client feature in Orchard Core. Covers adding remote A2A hosts, authentication, assigning agent connections, and how remote agents become tools.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core A2A Client - Prompt Templates

## Configure an A2A Client

You are an Orchard Core expert. Generate configuration and admin guidance for connecting Orchard Core to remote A2A hosts through the CrestApps A2A Client feature.

### Guidelines

- Use feature ID `CrestApps.OrchardCore.AI.A2A`.
- A2A client connections are managed under **Artificial Intelligence → Agent to Agent Hosts**.
- Each connection points to a remote A2A host whose agent card is discovered at `/.well-known/agent-card.json`.
- Remote agent cards are cached for 15 minutes per connection and invalidated when the connection changes.
- Connected remote agents become AI tools available to the model.
- Sensitive authentication values are encrypted at rest with ASP.NET Core Data Protection.

### Feature Overview

| Feature | Feature ID | Description |
|---------|-----------|-------------|
| A2A Client | `CrestApps.OrchardCore.AI.A2A` | Connect to remote A2A hosts and use their agents |

### Enable the A2A Client Feature

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI",
        "CrestApps.OrchardCore.AI.A2A"
      ],
      "disable": []
    }
  ]
}
```

### Add a Connection via Admin UI

1. Navigate to **Artificial Intelligence → Agent to Agent Hosts**.
2. Click **Add Connection**.
3. Enter:
   - **Display Text**: A friendly name such as `Production Agent Hub`.
   - **Endpoint**: The base A2A host URL, such as `https://agents.example.com`.
   - **Authentication**: Choose the authentication method required by the remote host.
4. Save the connection.

The system resolves the agent card automatically from `/.well-known/agent-card.json` on the configured host.

### Supported Authentication Types

| Type | Description |
|------|-------------|
| `Anonymous` | No authentication |
| `ApiKey` | Sends an API key in a configurable header with an optional prefix |
| `Basic` | HTTP basic authentication with username and password |
| `OAuth2ClientCredentials` | OAuth 2.0 client credentials flow |
| `OAuth2PrivateKeyJwt` | OAuth 2.0 client credentials with private key JWT assertion |
| `OAuth2MutualTls` | OAuth 2.0 client credentials with mutual TLS |
| `CustomHeaders` | Arbitrary HTTP headers defined as JSON |

### Assign Agent Connections to AI Profiles

1. Open the AI Profile editor.
2. Go to the **Capabilities** tab.
3. Under **Agent Connections**, check the desired remote A2A hosts.
4. Save the profile.

### Assign Agent Connections to AI Profile Templates

1. Open the AI Template editor for a template whose source is `Profile`.
2. Go to the **Capabilities** tab.
3. Under **Agent Connections**, check the desired connections.
4. Save the template.

### Assign Agent Connections to Chat Interactions

1. Open the Chat Interaction editor.
2. Go to the **Parameters** tab under **Capabilities**.
3. Under **Agent Connections**, select the desired connections.
4. Save the interaction.

### How Remote Agents Work

When a profile or interaction has A2A connections configured:

1. Orchard fetches and caches the remote agent card.
2. Each remote skill is registered as an AI tool.
3. The AI model can invoke those tools through the `A2AAgentProxyTool`.
4. The remote agent response is returned as tool output.

### Built-In A2A Discovery Functions

When the A2A client feature is enabled, these system functions are available:

| Function | Description |
|----------|-------------|
| `listAvailableAgents` | Lists local and remote agents |
| `findAgentForTask` | Finds the best-matching agent for a task |
| `findToolsForTask` | Finds the best-matching AI tools for a task |

### Permissions

| Permission | Description |
|------------|-------------|
| `Manage A2A Connections` | Required to create, edit, and delete A2A connections |

### Best Practices

- Use descriptive connection names so editors can distinguish environments.
- Use authenticated connections for production hosts.
- Assign only the connections a profile actually needs.
- Keep remote host agent descriptions current because they affect tool selection.
