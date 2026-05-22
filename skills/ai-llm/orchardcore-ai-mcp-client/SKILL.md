---
name: orchardcore-ai-mcp-client
description: Skill for configuring CrestApps MCP client connections in Orchard Core. Covers SSE and Stdio transports, authentication, recipes, and assigning MCP connections to AI experiences.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core MCP Client - Prompt Templates

## Configure MCP Clients

You are an Orchard Core expert. Generate admin, configuration, and recipe guidance for connecting Orchard Core to external MCP servers through the CrestApps MCP client features.

### Guidelines

- Use `CrestApps.OrchardCore.AI.Mcp` for remote MCP servers over SSE.
- Use `CrestApps.OrchardCore.AI.Mcp.Stdio` for local MCP servers over standard input/output.
- Remote SSE connections are managed under **Artificial Intelligence → MCP Connections**.
- Sensitive secrets are encrypted at rest using ASP.NET Core Data Protection.
- Do not export encrypted values and do not commit plaintext secrets.

### Feature Overview

| Transport | Feature ID | Description |
|-----------|-----------|-------------|
| SSE | `CrestApps.OrchardCore.AI.Mcp` | Connect to remote MCP servers over HTTP/SSE |
| Stdio | `CrestApps.OrchardCore.AI.Mcp.Stdio` | Connect to local MCP servers over stdin/stdout |

### Enable the SSE MCP Client

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI",
        "CrestApps.OrchardCore.AI.Mcp"
      ],
      "disable": []
    }
  ]
}
```

### Add a Remote MCP Connection via Admin UI

1. Navigate to **Artificial Intelligence → MCP Connections**.
2. Click **Add Connection**.
3. Under **Server Sent Events (SSE)**, click **Add**.
4. Enter:
   - **Display Text**
   - **Endpoint** such as `https://localhost:1234/`
   - **Authentication** method
5. Save the connection.

### SSE Authentication Types

| Type | Description |
|------|-------------|
| `Anonymous` | No authentication |
| `ApiKey` | Sends an API key using a configurable header and optional prefix |
| `Basic` | Uses HTTP basic authentication |
| `OAuth2ClientCredentials` | Uses OAuth 2.0 client credentials |
| `OAuth2PrivateKeyJwt` | Uses a private key JWT client assertion |
| `OAuth2MutualTls` | Uses mTLS with a client certificate |
| `CustomHeaders` | Sends raw headers as JSON |

### SSE Recipe Example

```json
{
  "steps": [
    {
      "name": "McpConnection",
      "connections": [
        {
          "DisplayText": "Example server",
          "Properties": {
            "SseMcpConnectionMetadata": {
              "Endpoint": "https://localhost:1234/",
              "AuthenticationType": "ApiKey",
              "ApiKeyHeaderName": "Authorization",
              "ApiKeyPrefix": "Bearer",
              "ApiKey": "your-api-key-here"
            }
          }
        }
      ]
    }
  ]
}
```

### Enable the Stdio MCP Client

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI",
        "CrestApps.OrchardCore.AI.Mcp",
        "CrestApps.OrchardCore.AI.Mcp.Stdio"
      ],
      "disable": []
    }
  ]
}
```

### Add a Local MCP Connection via Admin UI

1. Navigate to **Artificial Intelligence → MCP Connections**.
2. Click **Add Connection**.
3. Under **Standard Input/Output (Stdio)**, click **Add**.
4. Enter:
   - **Display Text**: `Global Time Capabilities`
   - **Command**: `docker`
   - **Command Arguments**: `["run", "-i", "--rm", "mcp/time"]`
5. Save the connection.

### Stdio Recipe Example

```json
{
  "steps": [
    {
      "name": "McpConnection",
      "connections": [
        {
          "DisplayText": "Global Time Capabilities",
          "Properties": {
            "StdioMcpConnectionMetadata": {
              "Command": "docker",
              "Arguments": [
                "run",
                "-i",
                "--rm",
                "mcp/time"
              ]
            }
          }
        }
      ]
    }
  ]
}
```

### Assign MCP Connections to AI Experiences

After creating a connection, assign it where needed:

- **AI Profiles**: select connections under the **Capabilities** tab.
- **AI Templates**: select connections under the **Capabilities** tab for profile-source templates.
- **Chat Interactions**: select connections under the **Capabilities** area of the interaction editor.

### Security Notes

- Sensitive values such as API keys, client secrets, private keys, and certificates are encrypted at rest.
- Sensitive values are not exported in deployment packages.
- Do not commit raw secrets in recipes.
- Use secure secret storage for production deployments.

### Best Practices

- Use SSE for remote MCP services shared across environments.
- Use Stdio for local tools, containers, and offline utilities.
- Give connections descriptive names so editors can choose correctly.
- Prefer standard authentication types over custom headers unless required.
