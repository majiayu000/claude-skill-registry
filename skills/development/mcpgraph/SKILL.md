---
name: mcpgraph
description: Build no-code MCP servers with tools that compose and orchestrate other
  MCP tools, with data transformation and conditional logic.
---

---
name: mcpgraphtoolkit
description: Build, test, and manage mcpGraph tools using the mcpGraphToolkit MCP server. Discover MCP servers and tools, construct graph nodes with JSONata and JSON Logic, and interact with mcpGraph configurations.  IMPORTANT: Always read this file before creating graph tools using mcpGraphToolkit.
version: 1.0.1
---

# Building mcpGraph Tools with mcpGraphToolkit

This skill teaches you how to use the **mcpGraphToolkit** MCP server to build, debug, test, run, and manage graph tools in an **mcpGraph**.

## What is an **mcpGraph**

An **mcpGraph** is a declarative configuration that defines an MCP (Model Context Protocol) server and its tools, where those tools are implemented as directed graphs. We call those exported tools "graph tools". Each graph tool executes a sequence of nodes that can:
- Call other MCP tools (that are available to the mcpGraph)
- Transform data using JSONata expressions
- Make routing decisions using JSON Logic

**When to use mcpGraph:**
- You need to orchestrate multiple MCP tool calls in sequence
- You want to transform data between tool calls
- You need conditional routing based on data
- You need to compose complex workflows from simpler MCP tools

## Using the **mcpGraphToolkit**

**What you should do:**
- **✅ DO** use `listMcpServers` and `listMcpServerTools` to discover available MCP servers and tools
- **✅ DO** use `getMcpServerTool` to get MCP server tool details and schemas
- **✅ DO** use `addGraphTool` to add graph tools to the mcpGraph (it handles file operations automatically)
- **✅ DO** use `updateGraphTool` and `deleteGraphTool` to manage graph tools
- **✅ DO** use `runGraphTool` to run a graph tool or to test a graph tool before adding it
- **✅ DO** use `listGraphTools` and `getGraphTool` to discover and examine existing graph tools, especially when considering creating a new graph tool

## ⚠️ CRITICAL: Use Only the Provided Tools to interact with an **mcpGraph**

**DO NOT create, edit, or read configuration files directly.** mcpGraphToolkit uses configuration files internally (such as graph configuration files and MCP server configuration files), but you should never attempt to create, edit, or read directly from these files. The toolkit tools provide all the functionality you need to understand and manipulate the state of the mcpGraph.

## Terminology: MCP Servers/Tools vs Graph Tools

**Important:** Understanding the distinction between MCP servers/tools and graph tools is critical.

### MCP Servers and Tools (Available to the Graph)
- **MCP Servers**: External MCP servers that are available to the graph (discovered via `listMcpServers`)
- **MCP Tools**: Tools provided by those MCP servers (discovered via `listMcpServerTools` and `getMcpServerTool`)
- These are the **building blocks** that graph tools can use
- Graph tools can **only** use MCP servers and tools that are available to the graph (as determined by the toolkit's discovery APIs)
- Use `listMcpServers` and `listMcpServerTools` to see what's available before building graph tools

### Graph Tools (What You Create and Manage)
- **Graph Tools**: Tools you create, manage, and run using mcpGraphToolkit
- These are **composed** from MCP tools, transform nodes, and switch nodes
- Once created, graph tools can be called **like MCP tools** using `runGraphTool`
- Graph tools are stored in the graph configuration and can be discovered via `listGraphTools`

**Key Points:**
- Graph tools **orchestrate** MCP tools - they call MCP tools in sequence, transform data, and make routing decisions
- Graph tools can **only** use MCP servers/tools that are available to the graph (check with `listMcpServers` first)
- **Always check** if an existing graph tool already serves your purpose before creating a new one (use `listGraphTools` and `getGraphTool`)
- Graph tools you create become available as callable tools, via `runGraphTool`

## Graph Tool Structure

A graph tool is a `ToolDefinition` with this structure:

```json
{
  "name": "tool_name",
  "description": "Tool description",
  "inputSchema": {
    "type": "object",
    "properties": { ... },
    "required": [ ... ]
  },
  "outputSchema": {
    "type": "object",
    "properties": { ... }
  },
  "nodes": [
    { "id": "entry", "type": "entry", "next": "..." },  // REQUIRED
    // ... worker nodes (mcp, transform, switch) ...
    { "id": "exit", "type": "exit" }  // REQUIRED
  ]
}
```

**Required Components:**
- `name`: Tool identifier (string)
- `description`: Tool description (string)
- `inputSchema`: JSON Schema for tool inputs (REQUIRED - must be object type)
- `outputSchema`: JSON Schema for tool outputs (REQUIRED - must be object type)
- `nodes`: Array of nodes (MUST include exactly one entry node and exactly one exit node)

**Node Types and Required Fields:**

## Node Types

### Entry Node
Entry point that receives tool arguments. **Required in every graph tool.**

- `id`: Node identifier (typically `"entry"`)
- `type`: `"entry"`
- `next`: ID of the first worker node

**Output:** Tool input arguments (passed through as-is)

```json
{
  "id": "entry",
  "type": "entry",
  "next": "list_directory_node"
}
```

### MCP Node
Calls an MCP tool on a server available to the graph. **Type is exactly `"mcp"` (NOT "mcp-tool", "mcp-tool-call", etc).**

- `id`: Node identifier
- `type`: `"mcp"`
- `server`: MCP server name (must be available via `listMcpServers`)
- `tool`: Tool name (must be available via `listMcpServerTools`)
- `args`: Arguments (values starting with `$` are evaluated as JSONata)
- `next`: ID of the next node

**Output:** MCP tool's response (parsed from content)

```json
{
  "id": "list_directory_node",
  "type": "mcp",
  "server": "filesystem",
  "tool": "list_directory",
  "args": {
    "path": { "expr": "$.entry.directory" }
  },
  "next": "count_files_node"
}
```

**Important:** Only use servers/tools discovered via `listMcpServers` and `listMcpServerTools`.

### Transform Node
Applies JSONata expressions to transform data.

- `id`: Node identifier
- `type`: `"transform"`
- `transform.expr`: JSONata expression (string)
- `next`: ID of the next node

**Output:** Result of evaluating the JSONata expression

```json
{
  "id": "count_files_node",
  "type": "transform",
  "transform": {
    "expr": "{ \"count\": $count($split($.list_directory_node.content, \"\\n\")) }"
  },
  "next": "exit"
}
```

### Switch Node
Uses JSON Logic to conditionally route to different nodes.

- `id`: Node identifier
- `type`: `"switch"`
- `conditions`: Array of `{ rule, next }` objects
- `next`: Default next node (used if no conditions match)

**Output:** Node ID of the routed-to node (string)

```json
{
  "id": "switch_node",
  "type": "switch",
  "conditions": [
    {
      "rule": {
        ">": [{ "var": "entry.value" }, 10]
      },
      "next": "high_path"
    },
    {
      "rule": {
        ">": [{ "var": "entry.value" }, 0]
      },
      "next": "low_path"
    }
  ],
  "next": "zero_path"
}
```

**Note:** `var` operations in JSON Logic rules are evaluated using JSONata (see Expressions section).

### Exit Node
Exit point that returns the final result. **Required in every graph tool.**

- `id`: Node identifier (typically `"exit"`)
- `type`: `"exit"`
- **No `next` field** - execution ends here

**Output:** Output from the previous node in execution history

```json
{
  "id": "exit",
  "type": "exit"
}
```

**Critical Rules:**
- Every graph tool MUST have exactly one entry node (typically `id: "entry"`)
- Every graph tool MUST have exactly one exit node (typically `id: "exit"`)
- Entry node receives tool arguments and must have a `next` field pointing to the first worker node
- Exit node returns the final result and has NO `next` field (execution ends here)
- MCP node type is `"mcp"` (NOT "mcp-tool", "mcp-tool-call", or any other variant)
- All tools MUST include both `inputSchema` and `outputSchema` (both must be object type)
- Exit node returns the output from the previous node in the execution history (no special output mechanism needed)

**Example Structure:**
```json
{
  "name": "count_files",
  "description": "Counts files in a directory",
  "inputSchema": {
    "type": "object",
    "properties": {
      "directory": { "type": "string" }
    },
    "required": ["directory"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "count": { "type": "number" }
    }
  },
  "nodes": [
    {
      "id": "entry",
      "type": "entry",
      "next": "list_directory_node"
    },
    {
      "id": "list_directory_node",
      "type": "mcp",
      "server": "filesystem",
      "tool": "list_directory",
      "args": {
        "path": { "expr": "$.entry.directory" }
      },
      "next": "count_files_node"
    },
    {
      "id": "count_files_node",
      "type": "transform",
      "transform": {
        "expr": "{ \"count\": $count($split($.list_directory_node.content, \"\\n\")) }"
      },
      "next": "exit"
    },
    {
      "id": "exit",
      "type": "exit"
    }
  ]
}
```

## mcpGraphToolkit Tools

mcpGraphToolkit provides 12 tools organized into categories:

### Graph Discovery Tools
- **`getGraphServer`**: Get full details of the mcpGraph server metadata (name, version, title, instructions)
- **`listGraphTools`**: List all graph tools in the mcpGraph (name and description)
  - **Always check this first** before creating a new graph tool - an existing graph tool may already serve your purpose
- **`getGraphTool`**: Get full detail of a graph tool from the mcpGraph (including complete node definitions)
  - Use this to understand existing graph tools before creating new ones

### MCP Server Discovery Tools
- **`listMcpServers`**: List all MCP servers available to the graph (name, title, instructions, version)
  - These are the MCP servers that graph tools can use
  - Graph tools can **only** use MCP servers listed here
- **`listMcpServerTools`**: List tools from MCP servers available to the graph (name/description only), optionally filtered by MCP server name
  - These are the MCP tools that graph tools can call
- **`getMcpServerTool`**: Get full MCP server tool details (including input and output schemas)
  - Use this to understand how to call MCP tools from your graph tools

### Graph Tool Management Tools
- **`addGraphTool`**: Add a new tool to the mcpGraph
- **`updateGraphTool`**: Update an existing tool in the mcpGraph
- **`deleteGraphTool`**: Delete a tool from the mcpGraph

### Tool Execution Tools
- **`runGraphTool`**: Run an exported tool from the mcpGraph. Can specify existing tool name or run a tool definition supplied in payload. Supports optional logging collection.

### Expression Testing Tools
- **`testJSONata`**: Test a JSONata expression with context
- **`testJSONLogic`**: Test a JSON Logic expression with context
- **`testMcpTool`**: Test an MCP tool call directly to understand its output structure and behavior

## Graph Structure and Flow

A graph is a directed sequence of nodes that execute in order. Execution flow:
1. Starts at the **entry** node (receives tool arguments)
2. Executes nodes sequentially based on `next` fields
3. **switch** nodes can conditionally route to different nodes
4. Continues until the **exit** node is reached
5. Exit node returns the final result

### Node Connections

Nodes are connected using the `next` field, which specifies the ID of the next node to execute:

```json
{
  "id": "count_files_node",
  "type": "transform",
  "transform": {
    "expr": "{ \"count\": $count($split($.list_directory_node.content, \"\\n\")) }"
    },
    "next": "exit"
}
```

**Switch nodes** use `conditions` with `next` fields (each condition specifies its own `next` node), plus a top-level `next` field as the default:

```json
{
  "id": "switch_node",
  "type": "switch",
  "conditions": [
    {
      "rule": { ">": [{ "var": "entry.value" }, 10] },
      "next": "high_path"
    }
  ],
  "next": "default_path"
}
```

### Execution Context

During execution, each node's output is stored in the execution context. You can access node outputs using JSONata expressions:
- `$.node_id` - Accesses the latest output of a node with ID `node_id`
- `$.entry.paramName` - Accesses a parameter from the entry node

The context is a flat structure: `{ "node_id": output, ... }`

## Expressions

mcpGraph uses two expression languages: **JSONata** for data transformation and **JSON Logic** for conditional routing.

### JSONata

JSONata is used in three places:
1. **Transform node expressions** (`transform.expr`) - Transform data between nodes
2. **MCP tool node arguments** - Any argument value starting with `$` is evaluated as JSONata
3. **JSON Logic `var` operations** - Access context data in switch node conditions

**Basic Syntax:**
- Property access: `$.node_id.property` or `$.entry.paramName`
- Object construction: `{ "key": value }`
- Functions: `$count(array)`, `$split(string, delimiter)`, etc.
- Conditional: `condition ? trueValue : falseValue`

**History Functions (for loops):**
- `$executionCount(nodeName)` - Count executions of a node
- `$nodeExecution(nodeName, index)` - Get specific execution (0 = first, -1 = last)
- `$nodeExecutions(nodeName)` - Get all executions as array
- `$previousNode()` - Get previous node's output

**Examples:**

Transform node:
```json
{
  "transform": {
    "expr": "{ \"count\": $count($split($.list_directory_node.content, \"\\n\")) }"
  }
}
```

MCP node args:
```json
{
  "args": {
    "path": { "expr": "$.entry.directory" }
  }
}
```

In JSON Logic var:
```json
{
  "var": "$.increment_node.counter"
}
```

**Testing:** Use `testJSONata` tool to validate expressions before adding to nodes.

### JSON Logic

JSON Logic is used in switch node conditions for conditional routing.

**Basic Syntax:**
- Comparison: `{ ">": [a, b] }`, `{ "<": [a, b] }`, `{ "==": [a, b] }`
- Logical: `{ "and": [rule1, rule2] }`, `{ "or": [rule1, rule2] }`, `{ "!": rule }`
- Variable access: `{ "var": "path" }` or `{ "var": "$.node_id.property" }`

**Important:** `var` operations are evaluated using JSONata, so you can use full JSONata expressions including history functions.

**Examples:**

Simple comparison:
```json
{
  "rule": {
    ">": [{ "var": "entry.value" }, 10]
  }
}
```

Complex condition:
```json
{
  "rule": {
    "and": [
      { ">": [{ "var": "entry.price" }, 100] },
      { "==": [{ "var": "entry.status" }, "active"] }
    ]
  }
}
```

With JSONata:
```json
{
  "rule": {
    "<": [
      { "var": "$.increment_node.counter" },
      { "var": "$.increment_node.target" }
    ]
  }
}
```

**Testing:** Use `testJSONLogic` tool to validate conditions before adding to switch nodes.

## Understanding MCP Tool Outputs

When an MCP tool executes in a graph node, its output is stored in the execution context using the node ID. However, **the structure of that output varies by tool**, which can cause confusion when building graph tools.

### Output Structure Patterns

Different MCP tools return data in different formats:

1. **Direct/Plain Output** - Tool returns data directly (string, number, object, etc.)
   ```json
   // Tool output stored as:
   { "fetch_url": "Content here..." }

   // Access in JSONata:
   $.fetch_url
   ```

2. **Wrapped Output** - Tool returns an object with nested properties
   ```json
   // Tool output stored as:
   { "get_info": {"content": "File info here..."} }

   // Access in JSONata:
   $.get_info.content
   ```

### How to Determine Output Structure

1. **Use `getMcpServerTool`** - Check the tool's `outputSchema` to understand the expected structure
2. **Use `testMcpTool`** - Test the tool directly to see its actual output (recommended)
3. **Use `runGraphTool` with logging** - Run a minimal graph with just entry → mcp → exit and check `executionHistory`

### Testing MCP Tools with `testMcpTool`

The `testMcpTool` tool allows you to test MCP tool calls directly without creating a full graph tool. This is the fastest way to understand how a tool behaves and what output structure it returns.

**Basic Usage:**
```json
{
  "tool": "testMcpTool",
  "arguments": {
    "server": "fetch",
    "tool": "fetch",
    "args": {
      "url": "https://example.com",
      "raw": true
    }
  }
}
```

**Response:**
```json
{
  "output": "Content type text/plain cannot be simplified...",
  "executionTime": 267
}
```

**With JSONata Expression Evaluation:**
```json
{
  "tool": "testMcpTool",
  "arguments": {
    "server": "filesystem",
    "tool": "write_file",
    "args": {
      "path": { "expr": "$.entry.filename" },
      "content": { "expr": "$.fetch_result" }
    },
    "context": {
      "entry": {"filename": "test.txt"},
      "fetch_result": "Some content here"
    }
  }
}
```

**Response:**
```json
{
  "evaluatedArgs": {
    "path": "test.txt",
    "content": "Some content here"
  },
  "output": {"content": "Successfully wrote to test.txt"},
  "executionTime": 8
}
```

**Key Points:**
- `output` matches what would be available in a graph node's execution context
- The output structure depends on the tool's response format (may be an object, string, or other type)
- Use `getMcpServerTool` to understand the tool's `outputSchema` and expected output structure
- `evaluatedArgs` is included when JSONata expressions are used in `args` and `context` is provided
- `executionTime` shows how long the tool call took in milliseconds

**Why This Matters:**
Understanding the exact output structure is critical when building transform nodes or switch conditions that reference MCP tool outputs. Using `testMcpTool` before building your graph tool saves significant debugging time.

## Building Tools with mcpGraphToolkit

### Workflow

**IMPORTANT:** Follow this workflow exactly. Do not skip steps or try to create files manually.

0. **Check for Existing Graph Tools**
   - **ALWAYS START HERE**: Use `listGraphTools` to see if a graph tool already exists for your purpose
   - Use `getGraphTool` to examine existing graph tools before creating new ones
   - Only create a new graph tool if no existing tool serves your purpose

1. **Discover Available MCP Servers and Tools**
   - **MUST USE** `listMcpServers` to see MCP servers available to the graph (graph tools can only use these servers)
   - **MUST USE** `listMcpServerTools` to see MCP tools available on a server (graph tools can only call these tools)
   - **MUST USE** `getMcpServerTool` to get full tool details (input/output schemas)
   - **RECOMMENDED**: Use `testMcpTool` to understand tool behavior and output structure before using it in a graph
   - **Remember**: Graph tools can only use MCP servers and tools that are available to the graph (as shown by these discovery tools)
   - **DO NOT** attempt to read configuration files to discover MCP servers - use the toolkit discovery tools instead

2. **Test Components**
   - Use `testMcpTool` to test MCP tool calls and understand their output structure
   - Use `testJSONata` to test transform expressions (use actual MCP tool outputs from `testMcpTool` as context)
   - Use `testJSONLogic` to test switch conditions
   - Iterate until all components work correctly

3. **Build Tool Definition**
   - Construct nodes using MCP servers and tools that are available to the graph (from step 1)
   - **Only reference** MCP servers and tools that were discovered via `listMcpServers` and `listMcpServerTools`
   - Use tested expressions in transform and switch nodes
   - Define entry and exit nodes
   - Specify input and output schemas

4. **Test Tool Definition Before Adding**
   - Use `runGraphTool` with `toolDefinition` to test the tool inline (testing from source)
   - Optionally enable `logging: true` to see execution details
   - Verify the tool works correctly
   - **IMPORTANT**: Use the exact same tool definition in Step 5

5. **Add Tool to Graph**
   - **MUST USE** `addGraphTool` to add the tested tool to the graph
   - **CRITICAL**: Use the exact same tool definition from Step 4
   - **DO NOT** create or edit configuration files directly
   - The tool is saved automatically by the toolkit (all file operations are handled internally)

6. **Verify Tool in Graph (Recommended)**
   - Use `runGraphTool` with `toolName` (the tool's name) to test it from the graph
   - This verifies the tool was saved correctly and works when called from the graph
   - Compare results with Step 4 to ensure consistency

7. **Update or Delete Tools**
   - **MUST USE** `updateGraphTool` to modify existing tools (do NOT edit configuration files directly)
   - **MUST USE** `deleteGraphTool` to remove tools (do NOT edit configuration files directly)
   - Changes are saved automatically by the toolkit (all file operations are handled internally)

### Debugging Strategy

When building or debugging graph tools, follow this systematic approach:

1. **Test MCP Tools Individually**
   - Use `testMcpTool` to call the MCP tool directly and see its output structure
   - This helps you understand what data will be available in the execution context
   - Don't guess at output structure - test it first

2. **Test Expressions with Realistic Context**
   - Use outputs from `testMcpTool` as context for `testJSONata` expressions
   - Use actual data structures, not guessed structures
   - This prevents errors like trying to access `$.fetch_url.content` when the tool returns a plain string

3. **Build Incrementally**
   - Start with entry → first_mcp → exit
   - Add one transform or switch node at a time
   - Test after each addition using `runGraphTool` with `logging: true`

4. **Use Debugging Tools**
   - `testMcpTool` - Verify MCP tool calls work and understand output structure
   - `testJSONata` - Validate transform expressions before using them
   - `testJSONLogic` - Validate switch conditions before using them
   - `runGraphTool` with `logging: true` - See all execution steps and node outputs
   - `executionHistory` - Inspect actual node outputs when debugging

**Example: Debugging a Failed Transform**

Error: `"content": "expected string, received undefined"`

Steps:
1. Use `testMcpTool` to see what the MCP tool actually returns
2. Use `testJSONata` with the actual output structure as context:
   ```json
   {
     "tool": "testJSONata",
     "arguments": {
       "expression": "$.fetch_url.content",
       "context": {
         "fetch_url": "actual output from testMcpTool"
       }
     }
   }
   ```
3. Adjust the expression based on the actual structure (e.g., use `$.fetch_url` if it's a plain string)

### Example: Building a File Counter Tool

**Step 0: Check for Existing Tools**
```json
{
  "tool": "listGraphTools",
  "arguments": {}
}
```

**Step 1: Discover Available MCP Servers and Tools**
```json
{
  "tool": "listMcpServers",
  "arguments": {}
}
```

```json
{
  "tool": "listMcpServerTools",
  "arguments": {
    "serverName": "filesystem"
  }
}
```

```json
{
  "tool": "getMcpServerTool",
  "arguments": {
    "serverName": "filesystem",
    "toolName": "list_directory"
  }
}
```

**Step 2: Test MCP Tool and Understand Output Structure**
```json
{
  "tool": "testMcpTool",
  "arguments": {
    "server": "filesystem",
    "tool": "list_directory",
    "args": {
      "path": "/path/to/test/directory"
    }
  }
}
```

This returns the actual output structure. For example, if it returns:
```json
{
  "output": {
    "content": "[FILE] file1.txt\n[FILE] file2.txt\n[FILE] file3.txt\n"
  },
  "executionTime": 15
}
```

Now you know the output structure and can use it in expressions.

**Step 3: Test Expressions with Actual Output Structure**
```json
{
  "tool": "testJSONata",
  "arguments": {
    "expression": "{ \"count\": $count($split($.list_directory_node.content, \"\\n\")) }",
    "context": {
      "list_directory_node": {
        "content": "[FILE] file1.txt\n[FILE] file2.txt\n[FILE] file3.txt\n"
      }
    }
  }
}
```

**Step 4: Test Complete Tool Definition (from source)**

Test your tool definition using `runGraphTool` with `toolDefinition`:

```json
{
  "tool": "runGraphTool",
  "arguments": {
    "toolDefinition": {
      "name": "count_files",
      "description": "Counts files in a directory",
      "inputSchema": {
        "type": "object",
        "properties": { "directory": { "type": "string" } },
        "required": ["directory"]
      },
      "outputSchema": {
        "type": "object",
        "properties": { "count": { "type": "number" } }
      },
      "nodes": [
        {
          "id": "entry",
          "type": "entry",
          "next": "list_directory_node"
        },
        {
          "id": "list_directory_node",
          "type": "mcp",
          "server": "filesystem",
          "tool": "list_directory",
          "args": {
            "path": { "expr": "$.entry.directory" }
          },
          "next": "count_files_node"
        },
        {
          "id": "count_files_node",
          "type": "transform",
          "transform": {
            "expr": "{ \"count\": $count($split($.list_directory_node.content, \"\\n\")) }"
          },
          "next": "exit"
        },
        {
          "id": "exit",
          "type": "exit"
        }
      ]
    },
    "arguments": {
      "directory": "/path/to/directory"
    },
    "logging": true
  }
}
```

**Step 5: Add Tool to Graph**

Once validated, use `addGraphTool` with the **exact same tool definition** from Step 4:

```json
{
  "tool": "addGraphTool",
  "arguments": {
    "tool": {
      /* SAME tool definition from Step 4 */
      "name": "count_files",
      "description": "Counts files in a directory",
      "inputSchema": {
        "type": "object",
        "properties": {
          "directory": {
            "type": "string"
          }
        },
        "required": ["directory"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "count": {
            "type": "number"
          }
        }
      },
      "nodes": [
        {
          "id": "entry",
          "type": "entry",
          "next": "list_directory_node"
        },
        {
          "id": "list_directory_node",
          "type": "mcp",
          "server": "filesystem",
          "tool": "list_directory",
          "args": {
            "path": { "expr": "$.entry.directory" }
          },
          "next": "count_files_node"
        },
        {
          "id": "count_files_node",
          "type": "transform",
          "transform": {
            "expr": "{ \"count\": $count($split($.list_directory_node.content, \"\\n\")) }"
          },
          "next": "exit"
        },
        {
          "id": "exit",
          "type": "exit"
        }
      ]
    }
  }
}
```

**Step 6: Verify Tool in Graph (Recommended)**

Test the tool again, but now using the tool name (running from the graph, not from source):

```json
{
  "tool": "runGraphTool",
  "arguments": {
    "toolName": "count_files",
    "arguments": {
      "directory": "/path/to/directory"
    },
    "logging": true
  }
}
```

This verifies:
- The tool was saved correctly to the graph
- The tool works when called from the graph (not just from source)
- Results match Step 4, confirming consistency

## Resources

- **JSONata Documentation**: https://jsonata.org/
- **JSON Logic Documentation**: https://jsonlogic.com/
- **MCP Specification**: https://modelcontextprotocol.io/

