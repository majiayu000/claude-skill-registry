---
name: mcp-resource-patterns
description: >
  Patterns for MCP resources including URIs, templates, subscriptions, dynamic resources,
  context provision, and MIME types. Use when the user is exposing data as MCP resources,
  designing resource URIs, implementing resource templates with parameters, setting up
  resource subscriptions, or providing context to Claude through resources.
---

# MCP Resource Patterns

Patterns for designing and implementing MCP resources. Covers URI design, templates,
subscriptions, dynamic resources, MIME types, and context provision strategies.

## When to Use
- User is exposing data as MCP resources (files, configs, database records)
- User is designing resource URI schemes
- User needs parameterized resource templates
- User wants real-time resource updates via subscriptions
- User is providing contextual data to Claude through resources

## Core Patterns

### Static Resources

Expose fixed data sources that Claude can read for context.

```typescript
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({ name: "my-server", version: "1.0.0" });

// Static resource with a fixed URI
server.resource(
  "project-config",
  "config://project",
  { description: "Project configuration including build settings and dependencies." },
  async (uri) => ({
    contents: [{
      uri: uri.href,
      mimeType: "application/json",
      text: JSON.stringify(await loadProjectConfig(), null, 2)
    }]
  })
);

// Static resource for a text file
server.resource(
  "readme",
  "file:///project/README.md",
  { description: "Project README with setup instructions and architecture overview." },
  async (uri) => ({
    contents: [{
      uri: uri.href,
      mimeType: "text/markdown",
      text: await fs.readFile("README.md", "utf-8")
    }]
  })
);
```

### Resource Templates

Parameterized URIs that resolve to specific resources based on input.

```typescript
// Template with a parameter
server.resource(
  "user-profile",
  new ResourceTemplate("users://{userId}/profile", { list: undefined }),
  { description: "User profile data by user ID." },
  async (uri, { userId }) => {
    const user = await db.users.findById(userId);
    if (!user) {
      return { contents: [] };  // Empty contents signals not found
    }
    return {
      contents: [{
        uri: uri.href,
        mimeType: "application/json",
        text: JSON.stringify({
          id: user.id,
          name: user.name,
          email: user.email,
          role: user.role
        }, null, 2)
      }]
    };
  }
);

// Template with list callback for discovery
server.resource(
  "log-file",
  new ResourceTemplate("logs://{date}/{level}", {
    list: async () => {
      const dates = await getAvailableLogDates();
      return dates.flatMap(date =>
        ["info", "warn", "error"].map(level => ({
          uri: `logs://${date}/${level}`,
          name: `${date} ${level} logs`,
          description: `${level}-level logs from ${date}`
        }))
      );
    }
  }),
  { description: "Application logs filtered by date and level." },
  async (uri, { date, level }) => ({
    contents: [{
      uri: uri.href,
      mimeType: "text/plain",
      text: await readLogFile(date, level)
    }]
  })
);
```

### Resource Subscriptions

Notify clients when resource content changes.

```python
# Python - resource with subscription support
from mcp.server import Server
import mcp.types as types

server = Server("my-server")

@server.list_resources()
async def list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri="metrics://system/health",
            name="System Health",
            description="Real-time system health metrics.",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "metrics://system/health":
        metrics = await collect_system_metrics()
        return json.dumps(metrics)
    raise ValueError(f"Unknown resource: {uri}")

# Notify subscribers when metrics change
async def on_metrics_update():
    await server.request_context.session.send_resource_updated(
        uri="metrics://system/health"
    )
```

### Dynamic Resource Lists

Generate resource lists dynamically based on current state.

```typescript
// List resources dynamically from a database
server.resource(
  "db-table",
  new ResourceTemplate("db://{schema}/{table}", {
    list: async () => {
      const tables = await db.query(
        "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog', 'information_schema')"
      );
      return tables.map(t => ({
        uri: `db://${t.table_schema}/${t.table_name}`,
        name: `${t.table_schema}.${t.table_name}`,
        description: `Database table ${t.table_schema}.${t.table_name}`,
        mimeType: "application/json"
      }));
    }
  }),
  { description: "Database table schema and sample data." },
  async (uri, { schema, table }) => {
    const columns = await db.getColumns(schema, table);
    const sample = await db.query(`SELECT * FROM "${schema}"."${table}" LIMIT 5`);
    return {
      contents: [{
        uri: uri.href,
        mimeType: "application/json",
        text: JSON.stringify({ columns, sample_rows: sample }, null, 2)
      }]
    };
  }
);
```

### MIME Types

Choose the right MIME type for resource content.

```typescript
// Common MIME types for MCP resources
const mimeTypes = {
  "application/json":    "Structured data, API responses, configs",
  "text/plain":          "Logs, raw text, CLI output",
  "text/markdown":       "Documentation, READMEs, notes",
  "text/html":           "Web content (use sparingly)",
  "application/xml":     "XML configs, SOAP responses",
  "text/csv":            "Tabular data, exports",
  "application/pdf":     "Binary documents (base64 encoded)",
  "image/png":           "Screenshots, diagrams (base64 encoded)",
};

// Binary content uses base64 encoding
server.resource("screenshot", "screen://current", {}, async (uri) => ({
  contents: [{
    uri: uri.href,
    mimeType: "image/png",
    blob: await captureScreenBase64()  // base64-encoded string
  }]
}));
```

## Anti-Patterns
- Using opaque IDs in URIs instead of human-readable paths (`res://abc123` vs `users://42/profile`)
- Not implementing the list callback on templates (Claude cannot discover available resources)
- Returning massive resources without summarization (floods context window)
- Using `text/plain` for structured data that should be JSON
- Not handling missing resources (return empty contents, do not throw)
- Exposing sensitive data (secrets, credentials) through resources without access control
- Making resource reads slow by including expensive computations (cache instead)

## Quick Reference

| Concept | Pattern |
|---------|---------|
| Static resource | Fixed URI, single data source |
| Resource template | Parameterized URI with `{param}` syntax |
| List callback | Discovery function returning available resources |
| Subscription | Server pushes updates when content changes |
| Binary content | Use `blob` field with base64, set correct MIME type |

URI scheme conventions:
```
file:///path/to/file          # Local files
db://{schema}/{table}         # Database objects
config://{section}            # Configuration
logs://{date}/{level}         # Log entries
metrics://{category}          # Monitoring data
repo://{owner}/{name}         # Repository data
```

Checklist: human-readable URIs, descriptive descriptions, correct MIME types,
list callbacks for discoverability, concise content, redacted sensitive data.
