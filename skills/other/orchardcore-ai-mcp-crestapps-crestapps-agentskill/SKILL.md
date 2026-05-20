---
name: orchardcore-ai-mcp
description: Skill for configuring Model Context Protocol (MCP) in Orchard Core using the CrestApps MCP module. Covers MCP client connections (SSE and Stdio transports), MCP server setup to expose Orchard Core as an MCP endpoint, MCP resources, authentication, and custom resource types.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core MCP (Model Context Protocol) - Prompt Templates

## Configure MCP Integration

You are an Orchard Core expert. Generate code, configuration, and recipes for integrating Model Context Protocol (MCP) client and server capabilities into Orchard Core using CrestApps modules.

### Guidelines

- The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) is an open standard for seamless integration between LLM applications and external tools or data sources.
- The CrestApps MCP module provides both client and server features.
- **MCP Client**: Connect Orchard Core to external MCP servers using SSE or Stdio transports, extending AI chat capabilities with external tools.
- **MCP Server**: Expose Orchard Core AI tools and resources to external MCP-compatible clients (AI agents, IDEs, copilots).
- MCP connections can be configured via the admin UI or recipes.
- MCP server authentication supports OpenId, ApiKey, or None (development only).
- Never use `AuthenticationType: "None"` in production environments.
- Install CrestApps packages in the web/startup project.
- Always secure API keys using user secrets or environment variables.

### MCP Features Overview

| Feature | Feature ID | Description |
|---------|-----------|-------------|
| MCP Client (SSE) | `CrestApps.OrchardCore.AI.Mcp` | Connect to remote MCP servers via Server-Sent Events |
| MCP Client (Stdio) | `CrestApps.OrchardCore.AI.Mcp.Local` | Connect to local MCP servers via Standard Input/Output |
| MCP Server | `CrestApps.OrchardCore.AI.Mcp.Server` | Expose Orchard Core as an MCP server endpoint |

## MCP Client: Connecting to External MCP Servers

### Enabling MCP Client Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI",
        "CrestApps.OrchardCore.AI.Chat",
        "CrestApps.OrchardCore.AI.Mcp",
        "CrestApps.OrchardCore.OpenAI"
      ],
      "disable": []
    }
  ]
}
```

### Adding a Remote MCP Connection (SSE Transport) via Admin UI

1. Navigate to **Artificial Intelligence → MCP Connections**.
2. Click **Add Connection**.
3. Under **Server Sent Events (SSE)**, click **Add**.
4. Enter connection details:
   - **Display Text**: A friendly name for the connection.
   - **Endpoint**: The remote MCP server URL (e.g., `https://mcp-server.example.com/`).
   - **Additional Headers**: Supply any required authentication headers.
5. Save the connection.
6. Create or edit an AI profile and select this MCP connection under available tools.

### Adding a Remote MCP Connection via Recipe (SSE)

```json
{
  "steps": [
    {
      "name": "McpConnection",
      "connections": [
        {
          "DisplayText": "Remote AI Tools Server",
          "Properties": {
            "SseMcpConnectionMetadata": {
              "Endpoint": "https://mcp-server.example.com/",
              "AdditionalHeaders": {}
            }
          }
        }
      ]
    }
  ]
}
```

### Adding a Local MCP Connection (Stdio Transport)

The Local MCP Client feature enables connections to MCP servers running locally (e.g., in Docker containers) using Standard Input/Output.

#### Step-by-Step: Connect to a Docker-based MCP Server

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop).
2. Pull the desired MCP Docker image (e.g., `mcp/time`).
3. Navigate to **Artificial Intelligence → MCP Connections**.
4. Click **Add Connection**, then under **Standard Input/Output (Stdio)**, click **Add**.
5. Enter:
   - **Display Text**: `Global Time Capabilities`
   - **Command**: `docker`
   - **Command Arguments**: `["run", "-i", "--rm", "mcp/time"]`
6. Save the connection.

### Adding a Local MCP Connection via Recipe (Stdio)

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

### Enabling MCP Client with Local Stdio Support

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI",
        "CrestApps.OrchardCore.AI.Chat",
        "CrestApps.OrchardCore.AI.Mcp",
        "CrestApps.OrchardCore.AI.Mcp.Local",
        "CrestApps.OrchardCore.OpenAI"
      ],
      "disable": []
    }
  ]
}
```

## MCP Server: Exposing Orchard Core as an MCP Endpoint

### Enabling MCP Server

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI",
        "CrestApps.OrchardCore.AI.Mcp.Server"
      ],
      "disable": []
    }
  ]
}
```

### MCP Server Authentication

The MCP server supports three authentication modes:

| Mode | Description | Use Case |
|------|-------------|----------|
| `OpenId` | OpenID Connect via the "Api" scheme (default) | Production environments |
| `ApiKey` | Predefined API key authentication | Simple integrations, testing |
| `None` | No authentication | Local development only |

### Configuring MCP Server Authentication

**OpenId (Recommended for production):**

```json
{
  "OrchardCore": {
    "CrestApps_AI": {
      "McpServer": {
        "AuthenticationType": "OpenId",
        "RequireAccessPermission": true
      }
    }
  }
}
```

When `RequireAccessPermission` is `true`, users must have the `AccessMcpServer` permission.

**ApiKey (For simple integrations):**

```json
{
  "OrchardCore": {
    "CrestApps_AI": {
      "McpServer": {
        "AuthenticationType": "ApiKey",
        "ApiKey": "your-secure-api-key-here"
      }
    }
  }
}
```

The API key can be provided in the `Authorization` header as: `Bearer <key>`, `ApiKey <key>`, or the raw key.

**None (Local development only — never use in production):**

```json
{
  "OrchardCore": {
    "CrestApps_AI": {
      "McpServer": {
        "AuthenticationType": "None"
      }
    }
  }
}
```

### MCP Server Endpoint

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mcp/sse` | POST | SSE transport for MCP communication |

### Connecting External Clients to Orchard Core MCP Server

**With OpenId:**

```json
{
  "mcpServers": {
    "orchard-core": {
      "transport": {
        "type": "sse",
        "url": "https://your-orchard-site.com/mcp/sse",
        "headers": {
          "Authorization": "Bearer <your-oauth-token>"
        }
      }
    }
  }
}
```

**With ApiKey:**

```json
{
  "mcpServers": {
    "orchard-core": {
      "transport": {
        "type": "sse",
        "url": "https://your-orchard-site.com/mcp/sse",
        "headers": {
          "Authorization": "ApiKey <your-api-key>"
        }
      }
    }
  }
}
```

### Exposed Tools via MCP Server

The MCP server automatically exposes all AI tools registered in Orchard Core, including:

- **Content Management**: Search, create, update, delete, publish/unpublish content (when `OrchardCore.Contents` is enabled)
- **Feature Management**: List, enable, disable features (when `OrchardCore.Features` is enabled)
- **User Management**: Search users, get user information (when `OrchardCore.Users` is enabled)
- **AI Agent Tools**: All tools from the AI Agent module (when `CrestApps.OrchardCore.AI.Agent` is enabled)

### MCP Resources

MCP Resources expose data sources through the MCP protocol. Built-in resource types:

| Type | URI Pattern | Description |
|------|-------------|-------------|
| File | `file://{itemId}/{path}` | Local file system access |
| Content | `content://{itemId}/...` | Orchard Core content items |
| Recipe Schema | `recipe-schema://{itemId}/...` | JSON schema definitions |
| FTP/FTPS | `ftp://{itemId}/{path}` | Remote files via FTP (separate module) |
| SFTP | `sftp://{itemId}/{path}` | Remote files via SSH (separate module) |

### Creating MCP Resources via Recipe

```json
{
  "steps": [
    {
      "name": "McpResource",
      "Resources": [
        {
          "Source": "file",
          "DisplayText": "Application Config",
          "Resource": {
            "Uri": "file://abc123/etc/config.json",
            "Name": "app-config",
            "Description": "Application configuration file",
            "MimeType": "application/json"
          }
        }
      ]
    }
  ]
}
```

### Registering a Custom MCP Resource Type

```csharp
services.AddMcpResourceType<DatabaseResourceTypeHandler>("database", entry =>
{
    entry.DisplayName = S["Database"];
    entry.Description = S["Query data from databases."];
    entry.UriPatterns = ["db://{itemId}/{table}/{id}"];
});
```

Implement the handler:

```csharp
public sealed class DatabaseResourceTypeHandler : IMcpResourceTypeHandler
{
    public string Type => "database";

    public async Task<ReadResourceResult> ReadAsync(
        McpResource resource,
        CancellationToken cancellationToken)
    {
        var uri = new Uri(resource.Resource.Uri);
        // Parse URI and query database.
        // Return ReadResourceResult with content.
        return new ReadResourceResult();
    }
}
```

### Extending Content Resources with Custom Strategies

```csharp
public sealed class SearchContentResourceStrategy : IContentResourceStrategyProvider
{
    public string[] UriPatterns => ["content://{itemId}/{contentType}/search"];

    public bool CanHandle(Uri uri)
    {
        return uri.Segments.Length >= 4 &&
               uri.Segments[^1].TrimEnd('/') == "search";
    }

    public async Task<ReadResourceResult> ReadAsync(
        McpResource resource,
        Uri uri,
        CancellationToken cancellationToken)
    {
        // Implement search logic.
        return new ReadResourceResult();
    }
}
```

Register in `Startup.cs`:

```csharp
services.AddContentResourceStrategy<SearchContentResourceStrategy>();
```

### Security Best Practices

- Always use `OpenId` authentication for MCP server in production.
- Store API keys in user secrets or environment variables, never in source control.
- Grant the `AccessMcpServer` permission only to trusted users and roles.
- Individual tool invocations respect Orchard Core's permission system.
- MCP server operates within a single tenant context for tenant isolation.
- Rotate API keys periodically when using `ApiKey` authentication.

### Discovering More MCP Servers

Explore MCP-compatible tools at:
- [Docker Hub: MCP Images](https://hub.docker.com/search?q=mcp)
- [MCP.so](https://mcp.so/)
- [Glama.ai MCP Servers](https://glama.ai/mcp/servers)
- [MCPServers.org](https://mcpservers.org/)
