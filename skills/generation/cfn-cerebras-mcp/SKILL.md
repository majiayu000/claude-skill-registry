---
name: cfn-cerebras-mcp
description: "FAST code generation via mcp__cerebras-mcp__write tool using Z.ai glm-4.6. Use for rapid test generation, boilerplate creation, and bulk code tasks in main chat. Prompt must be SHORTER than output. Ideal for tests, CRUD, migrations, and repetitive patterns."
version: 2.0.0
tags: [mcp, code-generation, fast, zai, glm-4.6, tests, main-chat]
---

# Cerebras MCP Code Generation

**FAST** code generation via `mcp__cerebras-mcp__write` tool using Z.ai glm-4.6 model.

## When to Use

Use for **rapid test and code generation** when speed matters more than nuance:
- ✅ **Test files** - unit tests, integration tests, test fixtures
- ✅ **Boilerplate** - CRUD endpoints, data models, components
- ✅ **Bulk creation** - multiple similar files quickly
- ✅ **Migrations** - database migrations, schema updates
- ❌ **NOT for** complex architecture, security code, nuanced logic

**Rule**: Prompt must be SHORTER than expected output (blueprint style).

## Usage

```
mcp__cerebras-mcp__write:
  file_path: /absolute/path/to/file.ts
  prompt: |
    Function: validateEmail(email: string): boolean
    Steps:
    - Regex test /^[^@]+@[^@]+\.[^@]+$/
    - Return boolean result
    Imports: none
    Errors: none
  context_files:
    - /path/to/related/file.ts
```

## Prompt Format (Blueprint Style)

```
File: /path/to/file.ts
Function: functionName(params): returnType
Steps:
- Step 1
- Step 2
Imports: import { X } from './y'
Errors: throw new Error("message")
```

## Rules

1. **Prompt < Output**: Blueprint must be shorter than generated code
2. **Always include context_files**: When code needs imports from existing files
3. **Absolute paths only**: Use full paths, not relative
4. **One file per call**: Generate/modify single file

## Bad vs Good

**Bad** (verbose):
```
I need you to create a function that validates email addresses.
The function should take an email string as input and return true
if valid or false if invalid...
```

**Good** (blueprint):
```
Function: validateEmail(email: string): boolean
- Regex: /^[^@]+@[^@]+\.[^@]+$/
- Return: true if match, false otherwise

## Known Issues

- ℹ️ **Documentation Only**: This skill describes the MCP tool that's available in the main chat interface
- ℹ️ **No Separate Implementation**: There is no separate script to invoke - the tool is used directly
- ℹ️ **Main Chat Only**: This MCP tool is only available in the main chat, not within spawned agents
```
