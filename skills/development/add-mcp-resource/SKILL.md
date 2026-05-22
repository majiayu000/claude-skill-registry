---
name: add-mcp-resource
description: Add a new resource or resource template to an existing FastMCP server
argument-hint: "[resource-uri]"
---

# Add MCP Resource

Add a new resource or resource template to an existing FastMCP server.

## Usage

```bash
/add-mcp-resource [resource-uri]
```

## Arguments

- `[resource-uri]`: Optional - URI pattern for the resource (will prompt if not provided)

## Execution Instructions for Claude Code

When this command is run:

1. **Locate the FastMCP server** in the current project
2. **Determine resource type** (static or template)
3. **Gather resource requirements** through interactive questions
4. **Generate resource code** based on configuration
5. **Add resource to server** by modifying existing files

## Interactive Session Flow

### 1. Locate Server

```
Looking for FastMCP server...

Found: src/server.ts

Is this the correct server file? (yes/no):
```

### 2. Resource Type

```
What type of resource do you want to add?

1. Static resource - Fixed URI (e.g., "file:///config/settings.json")
2. Resource template - Dynamic URI with parameters (e.g., "user://{id}/profile")

Select (1-2):
```

### 3. Static Resource Configuration

For static resources:

```
Resource URI:
Example: "file:///logs/app.log", "config://settings", "docs://readme"

URI:
```

```
Resource name (human-readable):
Example: "Application Logs", "Server Configuration"

Name:
```

```
MIME type:
1. text/plain
2. application/json
3. text/markdown
4. text/html
5. Other (specify)

Select (1-5):
```

```
Description (optional):
```

### 4. Resource Template Configuration

For resource templates:

```
URI template pattern:
Use {parameter} syntax for dynamic parts.

Examples:
- "file:///logs/{name}.log"
- "user://{userId}/profile"
- "docs://{category}/{page}"

URI template:
```

```
Resource name:
Example: "User Profiles", "Log Files"

Name:
```

```
Let's define the template parameters.

Parameter: {name}
  Description:
  Required? (yes/no):

  Add auto-completion? (yes/no):
```

If auto-completion:
```
How should auto-completion work?

1. Static list of values
2. Dynamic lookup (I'll implement)
3. Prefix matching (e.g., "Ex" -> "Example")

Select (1-3):
```

### 5. Content Type

```
What type of content does this resource return?

1. Text content
2. Binary content (base64 blob)
3. Multiple items (array of content)

Select (1-3):
```

### 6. Data Source

```
Where does the resource data come from?

1. File system
2. Database
3. External API
4. In-memory/computed
5. Other

Select (1-5):
```

## Generated Code Examples

### Static Resource (Text)

```typescript
server.addResource({
  uri: "{{uri}}",
  name: "{{name}}",
  mimeType: "{{mimeType}}",
  description: "{{description}}",
  async load() {
    // TODO: Implement data loading
    const content = await readFile("path/to/file");
    return {
      text: content,
    };
  },
});
```

### Static Resource (Binary)

```typescript
server.addResource({
  uri: "{{uri}}",
  name: "{{name}}",
  mimeType: "{{mimeType}}",
  async load() {
    // TODO: Load binary data
    const buffer = await readFile("path/to/file");
    return {
      blob: buffer.toString("base64"),
    };
  },
});
```

### Static Resource (Multiple Items)

```typescript
server.addResource({
  uri: "{{uri}}",
  name: "{{name}}",
  mimeType: "{{mimeType}}",
  async load() {
    // Return multiple content items
    return [
      { text: "First section content" },
      { text: "Second section content" },
      { text: "Third section content" },
    ];
  },
});
```

### Resource Template (Basic)

```typescript
server.addResourceTemplate({
  uriTemplate: "{{uriTemplate}}",
  name: "{{name}}",
  mimeType: "{{mimeType}}",
  arguments: [
    {{#each parameters}}
    {
      name: "{{name}}",
      description: "{{description}}",
      required: {{required}},
    },
    {{/each}}
  ],
  async load(args) {
    const { {{parameterNames}} } = args;

    // TODO: Load resource based on parameters
    return {
      text: `Content for ${JSON.stringify(args)}`,
    };
  },
});
```

### Resource Template with Auto-Completion (Static)

```typescript
server.addResourceTemplate({
  uriTemplate: "{{uriTemplate}}",
  name: "{{name}}",
  mimeType: "text/plain",
  arguments: [
    {
      name: "{{paramName}}",
      description: "{{paramDescription}}",
      required: true,
      complete: async (value) => {
        // Static list of completions
        const options = ["option1", "option2", "option3"];
        const filtered = options.filter(opt =>
          opt.toLowerCase().includes(value.toLowerCase())
        );
        return { values: filtered };
      },
    },
  ],
  async load(args) {
    return {
      text: `Content for ${args.{{paramName}}}`,
    };
  },
});
```

### Resource Template with Dynamic Completion

```typescript
server.addResourceTemplate({
  uriTemplate: "{{uriTemplate}}",
  name: "{{name}}",
  mimeType: "application/json",
  arguments: [
    {
      name: "{{paramName}}",
      description: "{{paramDescription}}",
      required: true,
      complete: async (value) => {
        // Dynamic lookup from database/API
        const results = await searchItems(value);
        return {
          values: results.map(r => r.name),
        };
      },
    },
  ],
  async load(args) {
    const item = await findItem(args.{{paramName}});
    if (!item) {
      return { text: "Not found" };
    }
    return {
      text: JSON.stringify(item, null, 2),
    };
  },
});
```

### Resource from File System

```typescript
import { readFile } from "fs/promises";
import { join } from "path";

server.addResourceTemplate({
  uriTemplate: "file:///logs/{name}.log",
  name: "Log Files",
  mimeType: "text/plain",
  arguments: [
    {
      name: "name",
      description: "Name of the log file",
      required: true,
      complete: async (value) => {
        // List available log files
        const files = await readdir("/var/logs");
        const logFiles = files
          .filter(f => f.endsWith(".log"))
          .map(f => f.replace(".log", ""));
        return {
          values: logFiles.filter(f => f.includes(value)),
        };
      },
    },
  ],
  async load(args) {
    const filePath = join("/var/logs", `${args.name}.log`);
    const content = await readFile(filePath, "utf-8");
    return { text: content };
  },
});
```

### Resource from Database

```typescript
server.addResourceTemplate({
  uriTemplate: "user://{userId}/profile",
  name: "User Profiles",
  mimeType: "application/json",
  arguments: [
    {
      name: "userId",
      description: "User ID",
      required: true,
    },
  ],
  async load(args) {
    const user = await db.users.findById(args.userId);
    if (!user) {
      return { text: JSON.stringify({ error: "User not found" }) };
    }
    return {
      text: JSON.stringify({
        id: user.id,
        name: user.name,
        email: user.email,
        createdAt: user.createdAt,
      }, null, 2),
    };
  },
});
```

### Resource from External API

```typescript
server.addResourceTemplate({
  uriTemplate: "weather://{city}",
  name: "Weather Data",
  mimeType: "application/json",
  arguments: [
    {
      name: "city",
      description: "City name",
      required: true,
    },
  ],
  async load(args) {
    const response = await fetch(
      `https://api.weather.example/v1/${encodeURIComponent(args.city)}`
    );

    if (!response.ok) {
      return { text: JSON.stringify({ error: "City not found" }) };
    }

    const data = await response.json();
    return {
      text: JSON.stringify(data, null, 2),
    };
  },
});
```

## File Placement

```
Where should the resource code be added?

1. Inline in server.ts
2. New file in resources/ directory
3. Existing resources file

Select (1-3):
```

## Implementation Notes

1. **Find existing server**: Locate FastMCP server files
2. **Check for resources directory**: Create if needed
3. **Generate imports**: Add necessary imports
4. **Insert code**: Add resource at appropriate location
5. **Match style**: Preserve existing code formatting
6. **Summary**: Show generated resource and URI pattern
