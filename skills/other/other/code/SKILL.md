---
name: toolfs-skill
description: Execute WASM-based skills mounted to virtual paths. Use this skill when the user requests skill execution such as "Execute the RAG skill", "Run the analytics skill", or "Call the skill at this path".
metadata:
  author: toolfs
  version: "1.0.0"
  module: skill
---

# ToolFS Skill

Execute WASM-based skills mounted to virtual paths. Skills extend ToolFS functionality with custom handlers that can be mounted to specific paths and executed through the filesystem interface.

## How It Works

1. **Skill Mounting**: Skills are mounted to virtual paths like `/toolfs/<skill_name>`
2. **WASM Execution**: Skills run in a sandboxed WASM environment with resource limits
3. **Request/Response**: Skills receive JSON requests and return JSON responses
4. **Resource Isolation**: Each skill execution is isolated with configurable limits

## Usage

### Execute Skill via Mounted Path

**ToolFS Path:**
```
/toolfs/<skill_mount_path>?text=<query>&<param>=<value>
```

**Example:**
```json
GET /toolfs/rag/skill/search?text=AI%20agents&top_k=5

// Response
{
  "success": true,
  "result": {
    "query": "AI agents",
    "top_k": 5,
    "results": [
      {
        "document": {
          "id": "doc-1",
          "content": "AI agents use tools to interact with their environment...",
          "metadata": {}
        },
        "score": 0.92
      }
    ],
    "count": 1
  },
  "metadata": {
    "skill_name": "rag-skill",
    "skill_version": "1.0.0"
  }
}
```

### Execute Skill via Skill API

**ToolFS Path:**
```
POST /toolfs/skills/execute
```

**Example:**
```json
POST /toolfs/skills/execute
Content-Type: application/json

{
  "operations": [
    {
      "type": "execute_code_skill",
      "skill_path": "/toolfs/rag",
      "query": "vector database",
      "skill_data": {
        "top_k": 10
      }
    }
  ]
}

// Response
{
  "results": [
    {
      "type": "code",
      "source": "/toolfs/rag",
      "content": "...",
      "success": true,
      "code": {
        "name": "rag-skill",
        "version": "1.0.0"
      }
    }
  ]
}
```

### List Skills

**ToolFS Path:**
```
GET /toolfs/skills
```

**Example:**
```json
GET /toolfs/skills

// Response
{
  "skills": [
    {
      "name": "rag-skill",
      "version": "1.0.0",
      "mount_path": "/toolfs/rag",
      "source": "wasm"
    },
    {
      "name": "analytics-skill",
      "version": "2.1.0",
      "mount_path": "/toolfs/analytics",
      "source": "injected"
    }
  ]
}
```

## Skill Request Format

Skills receive requests in JSON format:

```json
{
  "operation": "search",
  "path": "/toolfs/rag/query?text=AI",
  "data": {
    "query": "AI agents",
    "top_k": 5
  }
}
```

## Skill Response Format

Skills must return responses in JSON format:

```json
{
  "success": true,
  "result": {
    // Skill-specific result data
  },
  "error": "error message if failed"
}
```

## When to Use This Skill

Use Skill skill when you need to:

- **Extend Functionality**: Use custom skills for specialized operations
- **RAG Queries**: Execute semantic search via RAG skills
- **Data Processing**: Run analytics or data transformation skills
- **Custom Handlers**: Access custom business logic via skills

Common use cases:
- "Execute the RAG skill to search documents"
- "Run the analytics skill on this data"
- "Call the skill at /toolfs/custom-handler"
- "List all available skills"

## Skill Types

Skills can be:

- **WASM Skills**: Compiled WebAssembly modules for sandboxed execution
- **Injected Skills**: Native Go skills injected at runtime
- **Mounted Skills**: Skills mounted to specific virtual paths

## Output Format

Skill operations return standardized result structures:

```json
{
  "type": "code",
  "source": "/toolfs/<skill_path>",
  "content": "skill result data",
  "metadata": {
    "skill_name": "...",
    "skill_version": "..."
  },
  "success": true,
  "code": {
    "name": "rag-skill",
    "version": "1.0.0",
    "output": {}
  },
  "error": "error message if failed"
}
```

## Present Results to User

When presenting skill execution results:

```
✓ Skill executed successfully

Skill: rag-skill v1.0.0
Path: /toolfs/rag/skill/search

Results:
- Found 1 document matching "AI agents"
- Score: 0.92

Document: doc-1
Content: AI agents use tools to interact with their environment...
```

## Troubleshooting

### Skill Not Found

If a skill execution fails:

1. Verify the skill is mounted at the specified path
2. Check skill metadata via `GET /toolfs/skills`
3. Ensure the skill is properly loaded and initialized
4. Verify the skill path is correct

### Skill Execution Error

If skill execution fails:

1. Check skill logs for detailed error messages
2. Verify input parameters are correct
3. Ensure skill has necessary resources (memory, time)
4. Check if skill is compatible with current ToolFS version

### WASM Sandbox Limits

If execution hits resource limits:

1. Check skill resource configuration
2. Verify skill doesn't exceed memory/time limits
3. Optimize skill code for resource efficiency
4. Adjust sandbox limits if appropriate

## Best Practices

1. **Verify Skill Availability**: Check skill list before execution
2. **Handle Errors**: Always check `success` field in skill responses
3. **Use Metadata**: Leverage skill metadata for version compatibility
4. **Resource Monitoring**: Monitor skill resource usage
5. **Caching**: Cache skill results when appropriate to reduce load

---

*This skill is part of ToolFS. See [main SKILL.md](../SKILL.md) for overview.*

