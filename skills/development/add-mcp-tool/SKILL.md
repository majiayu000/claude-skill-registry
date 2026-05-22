---
name: add-mcp-tool
description: Add a new tool to an existing FastMCP server with guided configuration
argument-hint: "[tool-name]"
---

# Add MCP Tool

Add a new tool to an existing FastMCP server with interactive configuration.

## Usage

```bash
/add-mcp-tool [tool-name]
```

## Arguments

- `[tool-name]`: Optional - Name for the new tool (will prompt if not provided)

## Execution Instructions for Claude Code

When this command is run:

1. **Locate the FastMCP server** in the current project
2. **Gather tool requirements** through interactive questions
3. **Generate tool code** based on configuration
4. **Add tool to server** by modifying existing files or creating new ones

## Interactive Session Flow

### 1. Locate Server

First, find the FastMCP server in the project:

```
Looking for FastMCP server...

Found: src/server.ts

Is this the correct server file? (yes/no):
```

If not found:
```
I couldn't find a FastMCP server. Please provide the path to your server file:
```

### 2. Tool Basics

```
Let's add a new tool to your MCP server.

Tool name (lowercase, use hyphens):
Example: "fetch-data", "create-file", "query-database"

Tool name:
```

```
Tool description (shown to LLM clients):
Example: "Fetches data from the specified API endpoint"

Description:
```

### 3. Parameters

```
Does this tool require parameters?

1. No parameters
2. Simple parameters (strings, numbers, booleans)
3. Complex parameters (objects, arrays, enums)

Select (1-3):
```

If parameters needed:
```
Let's define the parameters one by one.

Parameter 1:
  Name:
  Type (string/number/boolean/array/object):
  Required? (yes/no):
  Description:

Add another parameter? (yes/no):
```

For enum types:
```
Enum values (comma-separated):
Example: "json,xml,csv"

Values:
```

### 4. Return Type

```
What does this tool return?

1. Simple text response
2. Multiple content items
3. Image content
4. Audio content
5. Resource reference
6. Custom structure

Select (1-6):
```

### 5. Tool Features

```
Which features do you need?

[ ] Logging (log.info, log.error, etc.)
[ ] Progress reporting (for long operations)
[ ] Streaming output (for text generation)
[ ] Authorization check (canAccess)
[ ] Error handling with UserError

Select features (comma-separated numbers, or 'none'):
```

### 6. Tool Annotations

```
Optional annotations for LLM clients:

Read-only hint (tool doesn't modify state)? (yes/no) [default: no]:

Open-world hint (tool accesses external systems)? (yes/no) [default: no]:

Streaming hint (tool produces streaming output)? (yes/no) [default: no]:
```

## Generated Code Examples

### Simple Tool (no parameters)

```typescript
server.addTool({
  name: "{{tool-name}}",
  description: "{{description}}",
  execute: async () => {
    return "Result here";
  },
});
```

### Tool with Parameters

```typescript
server.addTool({
  name: "{{tool-name}}",
  description: "{{description}}",
  parameters: z.object({
    {{#each parameters}}
    {{name}}: z.{{type}}(){{#if description}}.describe("{{description}}"){{/if}}{{#unless required}}.optional(){{/unless}},
    {{/each}}
  }),
  execute: async (args) => {
    const { {{parameterNames}} } = args;

    // TODO: Implement tool logic
    return "Processed: " + JSON.stringify(args);
  },
});
```

### Tool with Logging

```typescript
server.addTool({
  name: "{{tool-name}}",
  description: "{{description}}",
  parameters: z.object({
    url: z.string().describe("URL to fetch"),
  }),
  execute: async (args, { log }) => {
    log.info("Starting operation", { url: args.url });

    try {
      // TODO: Implement logic
      const result = await fetchData(args.url);
      log.info("Operation completed successfully");
      return result;
    } catch (error) {
      log.error("Operation failed", { error: String(error) });
      throw error;
    }
  },
});
```

### Tool with Progress Reporting

```typescript
server.addTool({
  name: "{{tool-name}}",
  description: "{{description}}",
  parameters: z.object({
    items: z.array(z.string()).describe("Items to process"),
  }),
  execute: async (args, { reportProgress }) => {
    const total = args.items.length;
    const results: string[] = [];

    for (let i = 0; i < total; i++) {
      await reportProgress({ progress: i, total });

      // TODO: Process each item
      results.push("Processed: " + args.items[i]);
    }

    await reportProgress({ progress: total, total });
    return results.join("\n");
  },
});
```

### Tool with Streaming Output

```typescript
server.addTool({
  name: "{{tool-name}}",
  description: "{{description}}",
  parameters: z.object({
    prompt: z.string().describe("Input prompt"),
  }),
  annotations: {
    streamingHint: true,
  },
  execute: async (args, { streamContent }) => {
    // Stream content progressively
    await streamContent({ type: "text", text: "Processing...\n" });

    // TODO: Generate content
    const chunks = ["First ", "part, ", "second ", "part."];
    for (const chunk of chunks) {
      await streamContent({ type: "text", text: chunk });
      await new Promise(r => setTimeout(r, 100));
    }

    return; // Return undefined when using streaming
  },
});
```

### Tool with Authorization

```typescript
server.addTool({
  name: "{{tool-name}}",
  description: "{{description}}",
  canAccess: (auth) => {
    // Return true if user is authorized
    return auth?.role === "admin";
  },
  execute: async (args, { session }) => {
    // Tool is only executed if canAccess returns true
    return "Welcome, " + session.id;
  },
});
```

### Tool with UserError

```typescript
import { UserError } from "fastmcp";

server.addTool({
  name: "{{tool-name}}",
  description: "{{description}}",
  parameters: z.object({
    id: z.string().describe("Resource ID"),
  }),
  execute: async (args) => {
    // Validate input
    if (!args.id.match(/^[a-z0-9-]+$/)) {
      throw new UserError("Invalid ID format. Use lowercase letters, numbers, and hyphens only.");
    }

    // Check resource exists
    const resource = await findResource(args.id);
    if (!resource) {
      throw new UserError(`Resource not found: ${args.id}`);
    }

    return JSON.stringify(resource);
  },
});
```

### Tool with Image Content

```typescript
import { imageContent } from "fastmcp";

server.addTool({
  name: "{{tool-name}}",
  description: "{{description}}",
  parameters: z.object({
    imageId: z.string().describe("Image identifier"),
  }),
  execute: async (args) => {
    // Return image from URL
    return imageContent({
      url: `https://example.com/images/${args.imageId}.png`,
    });

    // Or from file path:
    // return imageContent({ path: `/path/to/${args.imageId}.png` });

    // Or from buffer:
    // return imageContent({ buffer: imageBuffer });
  },
});
```

### Tool with Multiple Content Types

```typescript
server.addTool({
  name: "{{tool-name}}",
  description: "{{description}}",
  execute: async () => {
    return {
      content: [
        { type: "text", text: "Here's the analysis:" },
        { type: "text", text: "Line 1: Found 5 issues" },
        { type: "text", text: "Line 2: 3 warnings" },
      ],
    };
  },
});
```

## File Placement Options

```
Where should the tool code be added?

1. Inline in server.ts (simple projects)
2. New file in tools/ directory (recommended for organization)
3. Existing tools file (specify which)

Select (1-3):
```

## Implementation Notes

1. **Find existing server**: Use Glob/Grep to locate FastMCP server files
2. **Parse existing structure**: Understand current tool organization
3. **Generate imports**: Add necessary imports (z, UserError, imageContent, etc.)
4. **Insert code**: Add tool at appropriate location
5. **Preserve formatting**: Match existing code style
6. **Summary**: Show the generated tool and file location
