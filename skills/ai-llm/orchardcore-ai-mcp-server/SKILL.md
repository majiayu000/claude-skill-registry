---
name: orchardcore-ai-mcp-server
description: Skill for configuring the CrestApps MCP Server feature in Orchard Core. Covers server authentication, exposing tools, adding MCP prompts and resources through the UI, and custom MCP resource types.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core MCP Server - Prompt Templates

## Configure an MCP Server

You are an Orchard Core expert. Generate configuration and admin guidance for exposing Orchard Core AI capabilities through the CrestApps MCP Server feature.

### Guidelines

- Use feature ID `CrestApps.OrchardCore.AI.Mcp.Server`.
- The MCP server exposes Orchard AI tools, MCP prompts, MCP resources, and templated resources.
- The server uses SSE transport.
- Prefer authenticated access in production.
- Prompts and resources can be managed from the admin UI.
- Resource URIs are auto-constructed by the system from `{source}://{itemId}/{path}`.

### Feature Overview

| Feature | Feature ID | Description |
|---------|-----------|-------------|
| MCP Server | `CrestApps.OrchardCore.AI.Mcp.Server` | Expose Orchard Core as an MCP-compatible server |

### Enable the MCP Server Feature

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

### Supported MCP Capabilities

| Capability | Description |
|------------|-------------|
| Tools | Exposes registered Orchard AI tools as MCP tools |
| Prompts | Exposes MCP prompts through `ListPrompts` and `GetPrompt` |
| Resources | Exposes static resources through `ListResources` and `ReadResource` |
| Templated Resources | Exposes variable-based resource templates through `ListResourceTemplates` |

### Authentication Modes

| Mode | Description | Recommended Use |
|------|-------------|-----------------|
| `OpenId` | Uses OpenID Connect via the API scheme | Production |
| `ApiKey` | Uses a configured API key | Simple server-to-server integrations |
| `None` | No authentication | Local development only |

### OpenId Configuration

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

When `RequireAccessPermission` is `true`, callers must have the `AccessMcpServer` permission.

### ApiKey Configuration

```json
{
  "OrchardCore": {
    "CrestApps_AI": {
      "McpServer": {
        "AuthenticationType": "ApiKey",
        "ApiKey": "{{McpServerApiKey}}"
      }
    }
  }
}
```

Accepted `Authorization` header formats include:

- `Bearer <key>`
- `ApiKey <key>`
- raw key value

### Development-Only Configuration

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

### Server Endpoint

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/mcp/sse` | `POST` | MCP SSE endpoint |

### Add MCP Prompts via Admin UI

1. Navigate to **Artificial Intelligence → MCP Prompts**.
2. Click **Add Prompt**.
3. Fill in:
   - **Name**: The unique MCP prompt identifier.
   - **Display Text**: Friendly admin name.
   - **Description**: Optional description for clients.
4. Add one or more **Messages**.
   - Each message includes a **Role** such as `system` or `user`.
   - Each message includes **Content**.
5. Save the prompt.

Clients can discover prompts with `ListPrompts` and fetch their messages with `GetPrompt`.

### Add MCP Resources via Admin UI

1. Navigate to **Artificial Intelligence → MCP Resources**.
2. Click **Add Resource**.
3. Choose a **Resource Type** such as File, Media, Content Item, Content Type, Recipe Schema, or Recipe Step Schema.
4. Fill in:
   - **Display Text**
   - **Path**
   - **Name**
   - **Title** (optional)
   - **Description** (optional)
   - **MIME Type**
5. Save the resource.

### Resource Path Rules

- You only enter the **path** portion in the UI.
- The full URI is generated automatically as `{source}://{itemId}/{path}`.
- Templated resources can use variables such as `{fileName}`, `{contentType}`, or `{stepName}` depending on the resource type.

### Built-In Resource Types

| Type | Supported Variables | Description |
|------|---------------------|-------------|
| `file` | `{providerName}`, `{fileName}` | File provider access |
| `media` | `{path}` | Orchard media library |
| `content-item` | `{contentItemId}`, `{contentItemVersionId}` | Specific content item |
| `content-type` | `{contentType}` | Published items by content type |
| `recipe-schema` | none | Full JSON schema for all recipe steps |
| `recipe-step-schema` | `{stepName}` | JSON schema for one recipe step |
| `recipe` | `{recipeName}` | Recipe content by name |
| `ftp` | `{path}` | FTP or FTPS resource access |
| `sftp` | `{path}` | SFTP resource access |

### Recipe Example for MCP Resources

```json
{
  "steps": [
    {
      "name": "McpResource",
      "Resources": [
        {
          "Source": "file",
          "DisplayText": "Configuration File",
          "Resource": {
            "Uri": "file://configs/{providerName}/{fileName}",
            "Name": "config-file",
            "Description": "Application configuration",
            "MimeType": "application/json"
          }
        }
      ]
    }
  ]
}
```

### Register a Custom Resource Type

```csharp
services.AddMcpResourceType<DatabaseResourceTypeHandler>("database", entry =>
{
    entry.DisplayName = S["Database"];
    entry.Description = S["Query data from databases."];
    entry.SupportedVariables =
    [
        new McpResourceVariable("table") { Description = S["The database table name."] },
        new McpResourceVariable("id") { Description = S["The row ID to fetch."] },
    ];
});
```

```csharp
public sealed class DatabaseResourceTypeHandler : McpResourceTypeHandlerBase
{
    public DatabaseResourceTypeHandler() : base("database") { }

    protected override Task<ReadResourceResult> GetResultAsync(
        McpResource resource,
        IReadOnlyDictionary<string, string> variables,
        CancellationToken cancellationToken)
    {
        variables.TryGetValue("table", out var table);
        variables.TryGetValue("id", out var id);
        // Query your data source here.
    }
}
```

### External Client Connection Example

```json
{
  "mcpServers": {
    "orchard-core": {
      "transport": {
        "type": "sse",
        "url": "https://your-orchard-site.com/mcp/sse",
        "headers": {
          "Authorization": "Bearer <token-or-api-key>"
        }
      }
    }
  }
}
```

### Security Best Practices

- Use `OpenId` in production whenever possible.
- Store API keys in environment variables or secrets.
- Grant `AccessMcpServer` only to trusted identities.
- Remember that exposed tools still respect Orchard Core permissions.
- Keep tenant isolation in mind; MCP operates in a tenant context.
