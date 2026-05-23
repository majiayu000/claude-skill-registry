---
name: agent-ops-project-sections
description: "Identify and map different sections of a software project (API, frontend, database, CLI, domain). Use for context scoping and architecture documentation."
category: analysis
invokes: [agent-ops-state]
invoked_by: [agent-ops-context-map, agent-ops-idea]
state_files:
  read: [focus.md, constitution.md, map.md]
  write: [focus.md]
---

# Project Section Identification Workflow

## Purpose

Analyze a software project to identify and categorize its logical sections (backend API, frontend, database layer, CLI, domain logic, etc.). This enables:

- **Context scoping**: Focus agent work on specific project areas
- **Architecture documentation**: Generate structured overview
- **Dependency analysis**: Understand how sections relate
- **Instruction optimization**: Input for optimizing prompt/skill context

## When to Use

- Starting work on an unfamiliar codebase
- Need to scope work to a specific layer (e.g., "just the API")
- Generating architecture documentation
- Preparing context for focused implementation
- Input for `agent-ops-context-map` or instruction optimization

## Section Types

| Section Type | Description | Common Indicators |
|--------------|-------------|-------------------|
| `api` | REST/GraphQL endpoints, route handlers | `/api/`, `/routes/`, `controllers/`, OpenAPI specs |
| `frontend` | UI components, pages, client-side code | `/components/`, `/pages/`, `.tsx`, `.vue`, `.svelte` |
| `backend` | Server-side logic, services | `/services/`, `/handlers/`, server entry points |
| `database` | Data access, migrations, models | `/models/`, `/migrations/`, `/repositories/`, ORM files |
| `cli` | Command-line interface | `/cli/`, `__main__.py`, `bin/`, Typer/Click/Commander |
| `domain` | Business logic, core entities | `/domain/`, `/core/`, `/entities/`, pure logic |
| `infrastructure` | Cloud, deployment, CI/CD | `/infra/`, `/deploy/`, `terraform/`, `docker/` |
| `tests` | Test suites | `/tests/`, `*.test.*`, `*.spec.*` |
| `config` | Configuration files | `/config/`, `.env*`, `*.config.*`, `settings.*` |
| `docs` | Documentation | `/docs/`, `*.md`, OpenAPI, JSDoc |
| `scripts` | Build/utility scripts | `/scripts/`, `Makefile`, `package.json` scripts |
| `shared` | Shared utilities, types, constants | `/shared/`, `/common/`, `/utils/`, `/types/` |

## Procedure

### Phase 1: Project Discovery

1. **Scan root directory** for high-level structure
2. **Identify project type** from indicators:
   - `package.json` → Node.js/JavaScript
   - `pyproject.toml` / `setup.py` → Python
   - `*.csproj` / `*.sln` → .NET
   - `go.mod` → Go
   - `Cargo.toml` → Rust
3. **Read existing documentation** (README, constitution.md) for hints
4. **Check for monorepo patterns** (workspaces, multiple packages)

### Phase 2: Section Identification

For each top-level directory and key subdirectories:

1. **Analyze directory name** against section type patterns
2. **Sample file contents** (2-3 files per directory)
3. **Look for imports/dependencies** that indicate purpose
4. **Classify into section type**

**Classification heuristics:**

```
IF contains route definitions AND HTTP methods → api
IF contains React/Vue/Svelte components → frontend  
IF contains ORM models OR SQL → database
IF contains CLI decorators (Typer/Click) → cli
IF contains pure business logic, no I/O → domain
IF contains test files → tests
```

### Phase 3: Dependency Mapping

For each identified section:

1. **Trace imports** to other sections
2. **Identify shared dependencies**
3. **Build dependency graph**

```
api → domain → database
     ↘ shared ↗
frontend → api (HTTP)
cli → domain
```

### Phase 4: Generate Output

Produce structured output in two formats:

#### Format A: Summary Table

```markdown
## Project Sections

| Section | Type | Root Path | Key Files | Dependencies |
|---------|------|-----------|-----------|--------------|
| API Routes | api | src/api/ | routes.py, handlers/ | domain, database |
| Web Frontend | frontend | web/ | App.tsx, components/ | api (HTTP) |
| Data Layer | database | src/models/ | user.py, migrations/ | — |
| CLI | cli | src/cli/ | __main__.py, commands/ | domain |
| Business Logic | domain | src/domain/ | entities/, services/ | shared |
| Utilities | shared | src/shared/ | utils.py, types.py | — |
```

#### Format B: Detailed Map

```markdown
## Section: API Routes

**Type:** api
**Root:** src/api/
**Purpose:** REST API endpoints for issue management

### Key Files
- `routes.py` — Route definitions
- `handlers/issues.py` — Issue CRUD handlers
- `handlers/focus.py` — Focus endpoint

### Dependencies
- `domain` — Business logic for issue operations
- `database` — Data persistence
- `shared` — Common types and utilities

### Entry Points
- `app.py` — FastAPI application instance

### Notes
- Uses FastAPI framework
- OpenAPI spec auto-generated
```

## Output Locations

| Output | Location | Purpose |
|--------|----------|---------|
| Summary | Console / focus.md | Quick reference |
| Detailed map | `.agent/sections.md` | Persistent reference |
| JSON export | `.agent/sections.json` | Programmatic access |

## Integration Points

| Skill | How It Uses Section Data |
|-------|-------------------------|
| `agent-ops-context-map` | Includes section summary in map.md |
| `agent-ops-planning` | Scopes implementation to specific sections |
| `agent-ops-implementation` | Focuses context on relevant section |
| `agent-ops-critical-review` | Reviews by section |

## Scoped Context Mode

After sections are identified, agent can work in **scoped mode**:

```
/agent-scope api
```

This loads only files from the `api` section into context, reducing noise for focused work.

**Scope commands:**
- `/agent-scope <section>` — Focus on one section
- `/agent-scope <section1>,<section2>` — Focus on multiple sections
- `/agent-scope clear` — Return to full project context

## Completion Criteria

- [ ] All major directories classified
- [ ] Section types assigned appropriately
- [ ] Key files identified per section
- [ ] Dependencies mapped between sections
- [ ] Output generated (summary + detailed)
- [ ] Monorepo sub-projects handled (if applicable)

## Anti-patterns (avoid)

- ❌ Classifying every directory (focus on meaningful sections)
- ❌ Ignoring test directories (they provide insight into structure)
- ❌ Assuming single project type (projects can be hybrid)
- ❌ Missing hidden config (`.env`, `.config/`)
- ❌ Treating `node_modules`/`venv` as sections (they're dependencies)

## Examples

### Example 1: Python FastAPI Project

**Input:** Scan `tools/agent-ops-cli/`

**Output:**
```markdown
## Project Sections: agent-ops-cli

| Section | Type | Root Path | Key Files |
|---------|------|-----------|-----------|
| Issues CLI | cli | src/agent_ops_cli/issues/cli.py | commands, queries |
| Issues Core | domain | src/agent_ops_cli/issues/core/ | parser, models |
| TUI | frontend | src/agent_ops_cli/tui/ | app.py, views/ |
| API Server | api | src/agent_ops_cli/api/ | routes/, server.py |
| Knowledge Graph | domain | src/agent_ops_cli/kg/ | graph, query, llm |
| Notifications | infrastructure | src/agent_ops_cli/notify/ | slack, server |
| Tests | tests | tests/ | test_*.py |
```

### Example 2: Scoped Work

**User:** "I need to fix a bug in the API"

**Agent:**
```
Scoping to `api` section...

Loaded context:
- src/agent_ops_cli/api/routes/issues.py
- src/agent_ops_cli/api/routes/focus.py
- src/agent_ops_cli/api/routes/websocket.py
- src/agent_ops_cli/api/server.py

What's the bug you're seeing?
```
