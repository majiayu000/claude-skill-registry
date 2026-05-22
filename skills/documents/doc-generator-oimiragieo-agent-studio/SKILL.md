---
name: doc-generator
description: Generates comprehensive documentation from code, APIs, and specifications. Creates API documentation, developer guides, architecture docs, and user manuals with examples and tutorials.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Glob, Grep]
best_practices:
  - Extract documentation from code comments
  - Generate OpenAPI/Swagger specs from code
  - Create comprehensive examples
  - Include troubleshooting guides
  - Follow documentation standards
error_handling: graceful
streaming: supported
templates: [api-docs, developer-guide, architecture-docs, user-manual]
---

**Mode: Cognitive/Prompt-Driven** — No standalone utility script; use via agent context.

<identity>
Documentation Generator Skill - Generates comprehensive documentation from code, APIs, and specifications including API docs, developer guides, architecture documentation, and user manuals.
</identity>

<capabilities>
- Generating API documentation
- Creating developer guides
- Documenting architecture
- Creating user manuals
- Generating OpenAPI/Swagger specs
- Updating existing documentation
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify Documentation Type

Determine documentation type:

- **API Documentation**: Endpoint references
- **Developer Guide**: Setup and usage
- **Architecture Docs**: System overview
- **User Manual**: Feature guides

### Step 2: Extract Information

Gather documentation content:

- Read code and comments
- Analyze API endpoints
- Extract examples
- Understand architecture

### Step 3: Generate Documentation

Create documentation:

- Follow documentation templates
- Include examples
- Add troubleshooting
- Create clear structure

### Step 4: Validate Documentation

Validate quality:

- Check completeness
- Verify examples work
- Ensure clarity
- Validate links
  </execution_process>

<integration>
**Integration with Technical Writer Agent**:
- Uses this skill for documentation generation
- Ensures documentation quality
- Validates completeness

**Integration with Developer Agent**:

- Generates API documentation
- Creates inline documentation
- Updates docs with code changes
  </integration>

<best_practices>

1. **Extract from Code**: Use code as source of truth
2. **Include Examples**: Provide working examples
3. **Keep Updated**: Sync docs with code
4. **Clear Structure**: Organize logically
5. **User-Focused**: Write for users, not system
   </best_practices>
   </instructions>

<examples>
<formatting_example>
**API Documentation**

````markdown
# Users API

## Endpoints

### GET /api/users

List all users with pagination.

**Query Parameters:**

- `page` (number): Page number (default: 1)
- `limit` (number): Items per page (default: 10)

**Response:**

```json
{
  "data": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "name": "User Name"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100
  }
}
```
````

**Example:**

```bash
curl -X GET "http://localhost:3000/api/users?page=1&limit=10"
```

````
</formatting_example>

<formatting_example>
**Developer Guide**

```markdown
# Developer Guide

## Getting Started

### Prerequisites
- Node.js 18+
- pnpm 8+

### Installation
```bash
pnpm install
````

### Development

```bash
pnpm dev
```

## Architecture

[Architecture overview]

## Development Workflow

[Development process]

```
</formatting_example>
</examples>

<examples>
<usage_example>
**Example Commands**:

```

# Generate API documentation

Generate API documentation for app/api/users

# Generate developer guide

Generate developer guide for this project

# Generate architecture docs

Generate architecture documentation

# Generate OpenAPI spec

Generate OpenAPI specification from API routes

```
</usage_example>
</examples>

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**
- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
```
