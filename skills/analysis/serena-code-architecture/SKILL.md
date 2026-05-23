---
name: serena-code-architecture
description: Architectural analysis workflow using Serena symbols and Forgetful memory. Use when analyzing project structure, documenting architecture, creating component entities, or building knowledge graphs from code.
license: MIT
metadata:
version: 1.0.0
model: claude-opus-4-5
---

# Architectural Analysis with Serena + Forgetful

This skill guides systematic architectural analysis using Serena's symbol-level understanding, with optional persistence to Forgetful's knowledge graph.

## When to Use This Skill

- Analyzing a new codebase before implementing changes
- Documenting existing architecture for a project
- Creating component entities and relationships in Forgetful
- Understanding dependencies and call hierarchies
- Building a knowledge graph from code structure

## Analysis Workflow

### Phase 1: Project Structure Discovery

Understand the high-level layout:

```python
# Get directory structure
mcp__plugin_serena_serena__list_dir({
  "relative_path": ".",
  "recursive": false
})

# Identify key directories (src/, app/, lib/, etc.)
mcp__plugin_serena_serena__list_dir({
  "relative_path": "src",
  "recursive": true
})
```

**Goal**: Identify entry points, main modules, and organizational patterns.

### Phase 2: Entry Point Analysis

Find the application entry points:

```python
# Look for main/app files
mcp__plugin_serena_serena__search_for_pattern({
  "substring_pattern": "if __name__.*==.*__main__|def main\\(|app\\s*=\\s*FastAPI|createApp",
  "restrict_search_to_code_files": true
})

# Get symbols from entry file
mcp__plugin_serena_serena__get_symbols_overview({
  "relative_path": "src/main.py",
  "depth": 1
})
```

### Phase 3: Core Component Mapping

Identify and analyze major components:

```python
# Find all service/controller/model classes
mcp__plugin_serena_serena__find_symbol({
  "name_path_pattern": "Service",
  "substring_matching": true,
  "include_kinds": [5],  # Class only
  "depth": 1
})

# For each major component, get full structure
mcp__plugin_serena_serena__find_symbol({
  "name_path_pattern": "AuthService",
  "include_body": false,
  "depth": 1  # Get methods
})
```

### Phase 4: Dependency Tracing

Understand how components connect:

```python
# Find who uses AuthService
mcp__plugin_serena_serena__find_referencing_symbols({
  "name_path": "AuthService",
  "relative_path": "src/services/auth.py"
})

# Find what AuthService depends on
mcp__plugin_serena_serena__find_symbol({
  "name_path_pattern": "AuthService/__init__",
  "include_body": true
})
```

### Phase 5: Create Architectural Memories (Optional)

Store findings in Forgetful:

```python
# First, find/create the project
execute_forgetful_tool("list_projects", {"repo_name": "owner/repo"})

# Create memory for architectural insight
execute_forgetful_tool("create_memory", {
  "title": "AuthService: Core authentication component",
  "content": "AuthService handles JWT validation, user sessions, and OAuth flows. Dependencies: UserRepository, TokenService, CacheService. Used by: all API endpoints via middleware.",
  "context": "Discovered during architectural analysis",
  "keywords": ["auth", "jwt", "service", "architecture"],
  "tags": ["architecture", "component"],
  "importance": 8,
  "project_ids": [PROJECT_ID]
})
```

### Phase 6: Entity Graph Creation (Optional)

Create entities for major components:

```python
# Check if entity exists first
execute_forgetful_tool("search_entities", {"query": "AuthService"})

# Create component entity
execute_forgetful_tool("create_entity", {
  "name": "AuthService",
  "entity_type": "other",
  "custom_type": "Service",
  "notes": "Core authentication service - JWT, OAuth, sessions",
  "tags": ["service", "auth"],
  "project_ids": [PROJECT_ID]
})

# Create relationships
execute_forgetful_tool("create_entity_relationship", {
  "source_entity_id": AUTH_SERVICE_ID,
  "target_entity_id": USER_REPO_ID,
  "relationship_type": "depends_on",
  "strength": 0.9
})

# Link entity to memories
execute_forgetful_tool("link_entity_to_memory", {
  "entity_id": AUTH_SERVICE_ID,
  "memory_id": ARCH_MEMORY_ID
})
```

## Relationship Types

Standard relationship types for architecture:

| Type | Use For |
|------|---------|
| `uses` | General usage (A uses B) |
| `depends_on` | Dependency (A requires B) |
| `calls` | Direct function/method calls |
| `extends` | Class inheritance |
| `implements` | Interface implementation |
| `connects_to` | External connections (DB, API) |
| `contains` | Composition (A contains B) |

## Entity Types for Architecture

| Type | Use For |
|------|---------|
| `Service` | Business logic services |
| `Repository` | Data access layer |
| `Controller` | Request handlers |
| `Middleware` | Request/response processing |
| `Model` | Data models/entities |
| `Library` | External dependencies |
| `Framework` | Framework components |

## Example: FastAPI Project Analysis

```python
# 1. Find routers
mcp__plugin_serena_serena__search_for_pattern({
  "substring_pattern": "APIRouter\\(\\)|router\\s*=",
  "restrict_search_to_code_files": true
})

# 2. Analyze router structure
mcp__plugin_serena_serena__get_symbols_overview({
  "relative_path": "src/routers/users.py",
  "depth": 1
})

# 3. Find dependency injection
mcp__plugin_serena_serena__search_for_pattern({
  "substring_pattern": "Depends\\(",
  "restrict_search_to_code_files": true,
  "context_lines_before": 1,
  "context_lines_after": 1
})

# 4. Trace service dependencies
mcp__plugin_serena_serena__find_referencing_symbols({
  "name_path": "get_current_user",
  "relative_path": "src/dependencies/auth.py"
})

# 5. Create architecture memory
execute_forgetful_tool("create_memory", {
  "title": "FastAPI app structure: Routers + Dependencies",
  "content": "App uses router-based organization with dependency injection. Routers: /users, /auth, /products. Dependencies: get_current_user, get_db. All routes require auth except /auth/login.",
  "context": "FastAPI architecture analysis",
  "keywords": ["fastapi", "router", "dependency-injection"],
  "tags": ["architecture", "pattern"],
  "importance": 8,
  "project_ids": [PROJECT_ID]
})
```

## Analysis Checklist

- [ ] Directory structure mapped
- [ ] Entry points identified
- [ ] Major components catalogued
- [ ] Dependencies traced
- [ ] External connections documented
- [ ] Key patterns identified
- [ ] Memories created for insights
- [ ] Entities created for components (if applicable)
- [ ] Relationships mapped (if applicable)

## Tips

1. **Work incrementally** - Don't try to analyze everything at once
2. **Focus on interfaces** - Public methods/APIs matter more than internals
3. **Document decisions** - Create memories for WHY, not just WHAT
4. **Use entities sparingly** - Only major components, not every class
5. **Link across projects** - Architecture patterns often apply elsewhere
