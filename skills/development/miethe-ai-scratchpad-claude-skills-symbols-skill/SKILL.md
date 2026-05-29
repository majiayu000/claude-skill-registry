---
name: symbols
description: Token-efficient codebase navigation through intelligent symbol loading and querying. Use this skill when implementing new features (find existing patterns), exploring codebase structure, searching for components/functions/types, or understanding architectural layers. Reduces token usage by 60-95% compared to loading full files. Layer split enables 50-80% additional backend efficiency.
---

# Symbols - Intelligent Codebase Symbol Analysis

## Overview

Enable token-efficient navigation through pre-generated symbol graphs chunked by domain and separated from test files. Query symbols by name, kind, path, layer tag, or architectural layer without loading entire files. Load only the context needed for the current task. Reduces token usage by 95-99% compared to loading full files.

<!-- Template Variables:
- {{PROJECT_NAME}} - Project or organization name
- {{PROJECT_PATHS}} - Project directory structure
- {{SYMBOL_FILES}} - Symbol file locations and domain mappings
- {{PROJECT_ARCHITECTURE}} - System architecture description
- {{LAYER_ARCHITECTURE}} - Detailed architectural layers breakdown
- {{PROJECT_EXAMPLES}} - Real code examples from the project
-->

**Key Benefits:**
- 60-95% reduction in token usage vs loading full codebase
- Progressive loading strategy (load only what's needed)
- Domain-specific chunking for targeted context (configured per project)
- Layer split for 50-80% token reduction in backend work (load only specific architectural layers)
- Architectural layer tags for precise filtering (router, service, repository, component, hook, etc.)
- Architectural layer awareness for validating patterns
- Test file separation (loaded only when debugging)
- Precise code references with file paths and line numbers
- Complete codebase coverage including frontend and backend

## Symbol System Lifecycle

The symbols system follows a clear lifecycle from configuration to querying:

### 1. Configuration (symbols.config.json)
The **source of truth** for your project structure. Defines:
- Which directories to scan (e.g., `apps/web`, `services/api`)
- Where to output symbol files (e.g., `ai/symbols-web.json`)
- Domain structure (UI, Web, API, Shared, etc.)
- Layer definitions (router, service, repository, component, etc.)

### 2. Extraction (extract_* scripts)
**Tools that USE the config** to generate symbols:
- `extract_symbols_typescript.py` - Extracts TypeScript/React symbols
- `extract_symbols_python.py` - Extracts Python symbols
- Scripts READ the config to know WHAT to scan
- You RUN scripts manually, passing directory paths as arguments
- Example: `python extract_symbols_typescript.py {{PROJECT_PATHS.web}} --output={{SYMBOL_FILES.web}}`

### 3. Layer Tagging (add_layer_tags.py)
Assigns architectural layer tags based on file path patterns:
- File path patterns determine layer based on {{PROJECT_ARCHITECTURE}}
- Adds `layer` field to all symbols for precise filtering
- Example layers vary by project (e.g., router, service, repository, component, hook, test)

### 4. Chunking (split_api_by_layer.py) - OPTIONAL
Splits large backend domains into layer-specific files for token efficiency:
- **When**: Backend APIs with many symbols benefit most
- **How**: Reads layer tags, creates 5+ separate files per layer
- **Result**: Load only routers OR services OR schemas (not all backend)
- **Efficiency**: 50-80% token reduction for backend-focused work

### 5. Querying (symbol_tools.py)
Load and query symbols efficiently:
- Load domain-specific symbols (e.g., `load_domain("ui")`)
- Load layer-specific symbols (e.g., `load_api_layer("services")`)
- Query by name, kind, path, layer (e.g., `query_symbols(name="Button")`)
- Get context with relationships (e.g., `get_symbol_context(name="Service")`)

**Key Insight**: Config defines structure → Scripts extract using config → Layer tags enable filtering → Chunking optimizes loading → Tools query efficiently

## When to Use

Use this skill when:
- **Before implementing new features** - Find existing patterns to follow
- **Exploring codebase structure** - Understand how code is organized
- **Searching for code** - Locate components, functions, hooks, services, or types
- **Token-efficient context loading** - Avoid loading entire files or directories
- **Understanding architectural layers** - Verify Router → Service → Repository patterns
- **Cross-domain development** - Work across UI, API, and Shared code
- **Debugging** - Load relevant symbols including tests

Do NOT use this skill for:
- Reading actual file contents (use Read tool instead)
- Making code changes (symbols are read-only references)
- Runtime analysis (symbols are static analysis only)

## Key Capabilities

### Token-Efficient Layer Access

**Layer Split:**
- Backend domains can be divided into architectural layers for targeted loading
- Load only the layer you need: routers, services, repositories, schemas, cores (or project-specific layers)
- 50-80% token reduction vs loading entire domain

**Common Layer Types:**
- Routers/Controllers - HTTP endpoints and route handlers
- Services - Business logic layer
- Repositories - Data access layer
- Schemas/DTOs - Data transfer objects and request/response types
- Cores/Models - Domain models, core utilities, database entities

**Benefits:**
- Backend service dev: Load only service symbols instead of entire backend
- API endpoint work: Load only router symbols instead of entire backend
- DTO/schema work: Load only schema symbols instead of entire backend
- Typical reduction: 80-90% token savings

### Schema Standardization

**All symbols include:**
- Required fields: name, kind, path, line, signature, summary, layer
- Optional fields: parent, docstring, category
- Architectural layer tags for precise filtering

### Complete Coverage

Symbol files provide complete codebase coverage organized by domain:

**Frontend domains:**
- UI components and primitives
- Web/mobile application code (pages, routes, app-specific features)

**Backend domains:**
- API with layer-based access (targeted loading by architectural layer)
- Separate test file loading for debugging

Domain structure is configured in `symbols.config.json` and tailored to your project architecture.

## Core Capabilities

### 1. Query Symbols

Query symbols by name, kind, domain, or path without loading the entire symbol graph.

**When to use**: Find specific symbols, search by partial name, filter by type or location.

**How to use**:

Execute the Python function from `scripts/symbol_tools.py`:

```python
from symbol_tools import query_symbols

# Find all React components with "{{PROJECT_EXAMPLES.component}}" in the name
results = query_symbols(name="{{PROJECT_EXAMPLES.component}}", kind="component", domain="ui", limit=10)

# Find authentication-related functions
results = query_symbols(name="auth", kind="function", path="{{PROJECT_PATHS.api}}")

# Get all custom hooks (summary only for quick scan)
results = query_symbols(kind="hook", domain="ui", summary_only=True)
```

**Parameters**:
- `name` (optional) - Symbol name (supports partial/fuzzy matching)
- `kind` (optional) - Symbol kind: component, hook, function, class, interface, type, method
- `domain` (optional) - Domain filter (configured per project: e.g., ui, web, api, shared, mobile)
- `path` (optional) - File path pattern (e.g., "components", "hooks", "services")
- `limit` (optional) - Maximum results to return (default: 20)
- `summary_only` (optional) - Return only name and summary (default: false)

**Returns**: List of matching symbols with file path, line number, domain, and summary.

### 2. Load Domain

Load complete symbol set for a specific domain (UI, Web, API, or Shared).

**When to use**: Need broader context for a domain, implementing features that touch multiple files within a domain.

**How to use**:

```python
from symbol_tools import load_domain

# Load UI symbols for UI component work (excludes tests)
ui_context = load_domain(domain="ui", include_tests=False, max_symbols=100)

# Load Web symbols for frontend app development
web_context = load_domain(domain="web", include_tests=False, max_symbols=100)

# Load API symbols with tests for debugging
api_context = load_domain(domain="api", include_tests=True)

# Load first 50 shared symbols for quick reference
shared_context = load_domain(domain="shared", max_symbols=50)
```

**Parameters**:
- `domain` (required) - Domain to load (configured per project: e.g., ui, web, api, shared, mobile)
- `include_tests` (optional) - Include test file symbols (default: false)
- `max_symbols` (optional) - Limit number of symbols returned (default: all)

**Returns**: Dict with domain, type, totalSymbols count, and symbols array.

**Token efficiency**: Load 50-100 symbols (~10-15KB) instead of full domain (~250KB)

**Note for Backend Domains:** For token efficiency, consider using `load_api_layer()` instead to load only the specific architectural layer you need (e.g., routers, services, repositories, schemas).

### 2.1. Load API Layer

Load symbols from a specific architectural layer for token-efficient backend development.

**When to use**: Backend development requiring only one architectural layer (e.g., routers, services, repositories, schemas). Provides 50-80% token reduction vs loading entire backend domain.

**How to use**:

```python
from symbol_tools import load_api_layer

# Load only service layer for backend development
services = load_api_layer("services")

# Load schemas for DTO work
schemas = load_api_layer("schemas", max_symbols=100)

# Load routers for endpoint development
routers = load_api_layer("routers")

# Load repositories for data access patterns
repositories = load_api_layer("repositories")

# Load cores for models and utilities
cores = load_api_layer("cores", max_symbols=200)
```

**Parameters**:
- `layer` (required) - Architectural layer to load (configured per project: e.g., routers, services, repositories, schemas, cores)
- `max_symbols` (optional) - Limit number of symbols returned (default: all)

**Returns**: Dict with layer, totalSymbols count, and symbols array.

**Token efficiency examples**:
- Backend service development: Load only service symbols instead of entire backend = **80-85% reduction**
- API endpoint work: Load only router symbols instead of entire backend = **85-90% reduction**
- DTO/schema work: Load only schema symbols instead of entire backend = **85-90% reduction**

**Common Layer Types** (configured per project):
- `routers` / `controllers` - HTTP endpoints, route handlers, validation
- `services` - Business logic, DTO mapping, orchestration
- `repositories` - Database operations, data access patterns
- `schemas` / `dtos` - Request/response data transfer objects
- `cores` / `models` - Domain models, core utilities, database entities

### 3. Search Patterns

Advanced pattern-based search with architectural layer tags for precise filtering.

**When to use**: Find symbols matching regex patterns, filter by architectural layer tag, validate layered architecture patterns.

**How to use**:

```python
from symbol_tools import search_patterns

# Find all service layer classes
services = search_patterns(pattern="Service", layer="service", domain="api")

# Find router endpoints
routers = search_patterns(pattern="router|Router", layer="router")

# Find React components following naming pattern
components = search_patterns(pattern="^[A-Z].*Card", layer="component", domain="ui")

# Find middleware implementations
middleware = search_patterns(layer="middleware", domain="api")

# Find all observability-tagged code
telemetry = search_patterns(layer="observability", domain="api")
```

**Parameters**:
- `pattern` (optional) - Search pattern (supports regex)
- `layer` (optional) - Architectural layer tag (configured per project, common types: router, service, repository, schema, model, component, hook, page, util, test)
- `priority` (optional) - Priority filter: high, medium, low
- `domain` (optional) - Domain filter (configured per project: e.g., ui, web, api, shared, mobile)
- `limit` (optional) - Maximum results (default: 30)

**Returns**: List of matching symbols with layer tag, domain, and summary.

**Layer Tags**: All symbols include a `layer` field enabling precise architectural filtering. Common backend layers: router, service, repository, schema, model, core, auth, middleware. Common frontend layers: component, hook, page, util. Test layer: test.

### 4. Get Symbol Context

Get full context for a specific symbol including definition location and related symbols.

**When to use**: Need detailed information about a specific symbol, want to find related symbols (props interfaces, same-file symbols).

**How to use**:

```python
from symbol_tools import get_symbol_context

# Get full context for a component (includes props interface)
context = get_symbol_context(name="{{PROJECT_EXAMPLES.component}}", include_related=True)

# Get service definition with related symbols
service = get_symbol_context(
    name="{{PROJECT_EXAMPLES.service}}",
    file="{{PROJECT_PATHS.api}}/services/user_service.py",
    include_related=True
)
```

**Parameters**:
- `name` (required) - Exact symbol name
- `file` (optional) - File path if name is ambiguous
- `include_related` (optional) - Include related symbols (imports, usages, props) (default: false)

**Returns**: Dict with symbol info and optionally related symbols array.

**Relationship detection**: Automatically finds props interfaces for components, same-file symbols.

### 5. Update Symbols

Trigger symbol graph regeneration when code changes require updated symbols.

**When to use**: After significant code changes, when symbol files are out of sync with codebase.

**Primary approach - Use symbols-engineer agent**:

```markdown
Task("symbols-engineer", "Update symbols for the API domain after schema changes")
Task("symbols-engineer", "Perform incremental symbol update for recent file changes")
Task("symbols-engineer", "Regenerate full symbol graph and re-chunk by domain")
```

The `symbols-engineer` agent handles orchestration of the update workflow.

**Manual extraction workflow**:

If manually updating symbols:

1. **Review configuration** - Check `symbols.config.json` for domain paths and output files

2. **Extract symbols** - Run extraction scripts pointing to specific directories:

```bash
# Extract TypeScript/React symbols
python .claude/skills/symbols/scripts/extract_symbols_typescript.py {{PROJECT_PATHS.web}} --output={{SYMBOL_FILES.web}}

# Extract Python symbols
python .claude/skills/symbols/scripts/extract_symbols_python.py {{PROJECT_PATHS.api}} --output={{SYMBOL_FILES.api}}

# The scripts READ symbols.config.json to understand project structure
# But you MUST specify input directory and output file as arguments
```

3. **Add layer tags** (if needed):

```bash
python .claude/skills/symbols/scripts/add_layer_tags.py {{SYMBOL_FILES.api}}
```

4. **Chunk by layer** (OPTIONAL, for backend token efficiency):

```bash
# Split large API domain into layer-specific files
python .claude/skills/symbols/scripts/split_api_by_layer.py {{SYMBOL_FILES.api}} --output-dir={{PROJECT_PATHS.symbolsDir}}/
```

Creates layer-specific files based on {{PROJECT_ARCHITECTURE}}:
- `symbols-api-routers.json` - Router/controller layer only (or equivalent in your architecture)
- `symbols-api-services.json` - Service layer only (or equivalent in your architecture)
- `symbols-api-repositories.json` - Repository layer only (or equivalent in your architecture)
- `symbols-api-schemas.json` - Schema/DTO layer only (or equivalent in your architecture)
- `symbols-api-cores.json` - Core utilities and models (or equivalent in your architecture)

**Result**: 50-80% token reduction when loading backend symbols (load only the layer you need).

**Extraction requirements**:
- Scripts read `symbols.config.json` to understand {{PROJECT_NAME}} project structure
- You must specify input directory path and output file when running
- Example: `python extract_symbols_typescript.py {{PROJECT_PATHS.web}} --output={{SYMBOL_FILES.web}}`
- The config tells scripts WHICH directories to scan, but paths are passed as arguments

**Alternative - Programmatic API**:

```python
from symbol_tools import update_symbols

# Incremental update for recent changes
result = update_symbols(mode="incremental")

# Full regeneration (use sparingly)
result = update_symbols(mode="full", chunk=True)

# Update specific domain only
result = update_symbols(mode="domain", domain="ui")
```

**Parameters**:
- `mode` (optional) - Update mode: full, incremental, domain (default: incremental)
- `domain` (optional) - Specific domain to update (for domain mode)
- `files` (optional) - Specific files to update (for incremental mode)
- `chunk` (optional) - Re-chunk symbols after update (default: true)

**Note**: The programmatic API provides the interface but typically delegates to symbols-engineer agent for orchestration.

## Quick Start Workflow

### Frontend Development Workflow

```python
from symbol_tools import query_symbols, load_domain, get_symbol_context

# 1. Find existing React hooks in frontend app
hooks = query_symbols(kind="hook", domain="web", limit=20)

# 2. Find similar components in UI library
similar = query_symbols(name="Card", kind="component", domain="ui", limit=10)

# 3. Load web domain context for frontend patterns
web_symbols = load_domain(domain="web", max_symbols=100)

# 4. Find existing API hooks (useQuery, useMutation, etc)
api_hooks = query_symbols(path="hooks/queries", domain="web")

# 5. Check shared types and interfaces
types = query_symbols(path="types", kind="interface", domain="web")
```

**Result**: ~100 symbols loaded (~15KB) instead of full codebase = 95-97% reduction

### Backend Development Workflow

```python
from symbol_tools import load_api_layer, search_patterns, query_symbols

# Targeted layer loading (recommended)

# 1. Load only service layer for backend development
services = load_api_layer("services", max_symbols=50)

# 2. Load schemas for DTO patterns
schemas = load_api_layer("schemas", max_symbols=30)

# 3. Find similar routers in router layer
routers = load_api_layer("routers", max_symbols=20)

# Alternative: Pattern-based search across layers

# 4. Find service layer patterns
service_patterns = search_patterns(pattern="Service", layer="service", domain="api")

# 5. Find router endpoints
router_patterns = search_patterns(pattern="router", layer="router", domain="api")
```

**Result**: ~100 symbols loaded (~20KB) for targeted backend context = **80-90% token reduction** vs loading full backend domain

### Debugging Workflow

```python
from symbol_tools import get_symbol_context, load_domain, query_symbols

# 1. Load component and related symbols
component = get_symbol_context(name="Button", include_related=True)

# 2. Load test context to understand test cases
tests = load_domain(domain="ui", include_tests=True, max_symbols=30)

# 3. Search for related hooks in frontend app
hooks = query_symbols(path="hooks", name="user", kind="hook", domain="web")

# 4. Find state management patterns
state = query_symbols(path="contexts", kind="function", domain="web")

# 5. Find API client integration points
api_clients = query_symbols(path="lib/api", kind="function", domain="web")
```

**Result**: Full context including tests and frontend patterns loaded (~20KB instead of reading all files)

## Progressive Loading Strategy

Follow this three-tier approach for optimal token efficiency:

**Tier 1: Essential Context (25-30% of budget)**
- Load 10-20 symbols directly related to current task
- Focus on interfaces, types, and primary components/services
- Use: `query_symbols(name="Button", limit=10)`

**Tier 2: Supporting Context (15-20% of budget)**
- Load related patterns and utilities
- Include cross-domain interfaces
- Use: `load_domain(domain="shared", max_symbols=50)`

**Tier 3: On-Demand Context (remaining budget)**
- Specific lookups when needed
- Deep dependency analysis
- Use: `get_symbol_context(name="Service", include_related=True)`

## Programmatic Symbol Extraction

Symbol extraction is performed programmatically using domain-specific scripts that read `symbols.config.json` to understand project structure.

### Configuration and Scripts Relationship

**symbols.config.json is the SOURCE OF TRUTH:**

- Defines which directories contain code to scan
- Specifies where to output symbol files
- Maps domains to directory paths
- Defines layer classification patterns

**Extraction scripts are TOOLS that USE this config:**

- Read the config to understand project structure
- You RUN scripts manually (or via automation)
- You MUST pass input directory path and output file as arguments
- Example: `python extract_symbols_typescript.py apps/web --output=ai/symbols-web.json`

### Available Extraction Scripts

**Python Symbol Extractor** (`scripts/extract_symbols_python.py`):

- Extracts Python modules, classes, functions, methods
- Pulls function signatures and docstrings
- Filters out test files and internal imports
- Reads `symbols.config.json` for project structure
- You must specify input directory and output file

Usage:

```bash
python .claude/skills/symbols/scripts/extract_symbols_python.py services/api/app --output=ai/symbols-api.json
```

**TypeScript/JavaScript Symbol Extractor** (`scripts/extract_symbols_typescript.py`):

- Extracts TypeScript interfaces, types, functions, classes
- Extracts React components and hooks
- Parses JSDoc comments for summaries
- Reads `symbols.config.json` for project structure
- You must specify input directory and output file

Usage:

```bash
python .claude/skills/symbols/scripts/extract_symbols_typescript.py apps/web --output=ai/symbols-web.json
```

**Layer Tag Assignment** (`scripts/add_layer_tags.py`):

- Assigns architectural layer tags based on file path patterns
- Patterns defined in script (e.g., `app/api/*` → router layer)
- Adds `layer` field to all symbols for filtering
- Run after extraction to enable layer-based querying

Usage:

```bash
python .claude/skills/symbols/scripts/add_layer_tags.py ai/symbols-api.json
```

**Layer-Based Chunking** (`scripts/split_api_by_layer.py`):

- **OPTIONAL** - Recommended for large backend APIs only
- Splits symbol files into layer-specific files
- Happens AFTER extraction and layer tagging
- Creates 5+ separate files (routers, services, repositories, schemas, cores)
- Enables loading only the layer you need (50-80% token reduction)

Usage:

```bash
python .claude/skills/symbols/scripts/split_api_by_layer.py ai/symbols-api.json --output-dir=ai/
```

Output files:

- `symbols-api-routers.json` - HTTP endpoints only
- `symbols-api-services.json` - Business logic only
- `symbols-api-repositories.json` - Data access only
- `symbols-api-schemas.json` - DTOs only
- `symbols-api-cores.json` - Models and utilities only

**How layer chunking works:**

1. Layer assignment happens first (via `add_layer_tags.py`)
2. Assignment is based on file path patterns (configured in the script)
3. Example patterns:

   - `app/api/*` or `app/routers/*` → router layer
   - `app/services/*` → service layer
   - `app/repositories/*` → repository layer
   - `app/schemas/*` or `app/dtos/*` → schema layer

4. `split_api_by_layer.py` reads these layer tags and groups symbols
5. Creates separate JSON files per layer for targeted loading

**Symbol Merger** (`scripts/merge_symbols.py`):

- Merges programmatically extracted symbols into existing graphs
- Handles incremental updates
- Maintains symbol relationships and cross-references
- Validates for consistency and duplicates

Usage:

```bash
python .claude/skills/symbols/scripts/merge_symbols.py --domain=api --input=extracted_symbols.json
```

### Workflow: Manual Symbol Update

1. **Check configuration** - Review `symbols.config.json` for domain paths and outputs
2. **Extract symbols** - Run domain-specific extractor with input/output paths
3. **Add layer tags** - Run `add_layer_tags.py` to assign architectural layers
4. **Chunk by layer** (OPTIONAL) - Run `split_api_by_layer.py` for backend token efficiency
5. **Validate** - Query symbols to verify accuracy and completeness

**Example full workflow:**

```bash
# 1. Extract Python symbols from API
python scripts/extract_symbols_python.py {{PROJECT_PATHS.api}} --output={{SYMBOL_FILES.api}}

# 2. Add layer tags
python scripts/add_layer_tags.py {{SYMBOL_FILES.api}}

# 3. OPTIONAL: Chunk by layer for token efficiency
python scripts/split_api_by_layer.py {{SYMBOL_FILES.api}} --output-dir={{PROJECT_PATHS.symbolsDir}}/

# Result: 5 layer-specific files + original file (based on {{PROJECT_ARCHITECTURE}})
# Load only the layer you need (80-90% token reduction vs full domain)
```

**Recommended**: Use `symbols-engineer` agent to orchestrate this workflow automatically.

## Symbol Structure Reference

Symbols are stored in domain-specific JSON files in the `{{PROJECT_PATHS.symbolsDir}}/` directory. All symbols include a `layer` field for architectural filtering based on {{PROJECT_ARCHITECTURE}}.

**Symbol files are organized by domain as configured in `symbols.config.json`.**

**Domain Organization (configured per project):**
- Domains are defined in `symbols.config.json` based on your project structure
- Common patterns: UI components, Web/Mobile apps, Backend API, Shared utilities
- {{PROJECT_NAME}} specific domains are configured in your `symbols.config.json`

**Backend Layer Files** (when using layer-based split for token efficiency):
- Layer organization matches {{PROJECT_ARCHITECTURE}}
- Example layer files (adapt to your architecture):
  - `symbols-{domain}-routers.json` - HTTP endpoints and route handlers (or equivalent)
  - `symbols-{domain}-services.json` - Business logic layer (or equivalent)
  - `symbols-{domain}-repositories.json` - Data access layer (or equivalent)
  - `symbols-{domain}-schemas.json` - DTOs and request/response types (or equivalent)
  - `symbols-{domain}-cores.json` - Domain models, core utilities (or equivalent)

**Test symbol files** (loaded separately, on-demand for debugging):
- `symbols-{domain}-tests.json` - Test helpers, fixtures, and test cases

**Note**: Actual file names, symbol counts, and organization depend on your {{PROJECT_NAME}} configuration in `symbols.config.json`. See {{SYMBOL_FILES}} for your project's specific symbol file locations.

**Symbol structure example**:
```json
{
  "name": "{{PROJECT_EXAMPLES.component}}",
  "kind": "component",
  "file": "{{PROJECT_PATHS.ui}}/components/{{PROJECT_EXAMPLES.component}}.tsx",
  "line": 15,
  "domain": "frontend",
  "layer": "component",
  "summary": "Reusable component with variants (example from {{PROJECT_NAME}})"
}
```

**Symbol kinds**:
- `component` - React components
- `hook` - React hooks (useState, useEffect, custom hooks)
- `function` - Regular functions and arrow functions
- `class` - Class declarations
- `method` - Class methods
- `interface` - TypeScript interfaces
- `type` - TypeScript type aliases

**Layer tags** (all symbols include one, based on {{PROJECT_ARCHITECTURE}}):
- Backend layers vary by architecture (examples: `router`, `service`, `repository`, `schema`, `model`, `core`)
- Frontend layers vary by architecture (examples: `component`, `hook`, `page`, `util`)
- Test layer: `test`
- Your project's specific layers are defined in `symbols.config.json` and match {{LAYER_ARCHITECTURE}}

## Resources

### scripts/symbol_tools.py

Python implementation of all symbol query functions. Contains:
- `query_symbols()` - Query by name, kind, domain, path
- `load_domain()` - Load complete domain context
- `load_api_layer()` - Load specific API architectural layer
- `search_patterns()` - Pattern-based search with layer awareness
- `get_symbol_context()` - Get specific symbol with related symbols
- `update_symbols()` - Trigger regeneration

Execute directly or import functions as needed:

```bash
# Run examples
python .claude/skills/symbols/scripts/symbol_tools.py
```

```python
# Import in code
from symbol_tools import query_symbols, load_domain, load_api_layer
```

### references/usage_patterns.md

Detailed examples and patterns for common development scenarios:
- Frontend development examples
- Backend API development examples
- Cross-domain development patterns
- Debugging workflows
- Token efficiency guidelines
- Integration patterns with agents

Read this reference for comprehensive examples of each workflow type.

### references/architecture_integration.md

Deep dive into architecture integration:
- Symbol structure specification
- Layered architecture mapping based on {{PROJECT_ARCHITECTURE}}
- Symbol relationship analysis
- Development workflow integration
- Regeneration and update strategies
- Slash command integration
- Agent integration patterns
- Configuration reference

Read this reference to understand how symbols map to {{PROJECT_NAME}}'s architectural patterns defined in {{LAYER_ARCHITECTURE}}.

## Project Integration

### Slash Commands

The symbols skill can integrate with project-specific slash commands:
- `/symbols-query` - Query implementation
- `/symbols-search` - Search implementation
- `/load-symbols` - Domain loading implementation
- `/symbols-update` - Update implementation
- `/symbols-chunk` - Chunking implementation

### Related Agents

Common agent patterns that use symbols:
- `symbols-engineer` - Expert in symbol optimization and graph management
- `codebase-explorer` - Uses symbols for efficient code discovery
- Frontend/backend engineers - Use symbols for targeted context loading

### Architecture Integration

Symbols understand and validate {{PROJECT_NAME}}'s layered architecture as defined in {{PROJECT_ARCHITECTURE}}.

**Architecture layers are configured per project** based on {{LAYER_ARCHITECTURE}}:

**Example backend layers** (adapt to your architecture):
- **Router/Controller layer** - HTTP endpoints, validation, request handling
- **Service layer** - Business logic, orchestration, DTO mapping
- **Repository layer** - Database operations, data access patterns
- **Schema/DTO layer** - Request/response data structures
- **Model layer** - Domain models and database entities

**Example frontend layers** (adapt to your architecture):
- **Component layer** - UI components and design system primitives
- **Hook layer** - React hooks, state management, data fetching
- **Page layer** - Application pages, routes, views
- **Util layer** - Shared utilities and helpers

**Your project's specific layers** are defined in `symbols.config.json` and match your architecture.

Use `search_patterns()` with `layer` parameter to filter by architectural layer.

## Performance

**Symbol Coverage** (varies by project):
- Symbol counts and file sizes depend on codebase size and configuration
- All symbols include layer tags for precise filtering
- Domain-specific organization enables targeted loading
- Test symbols separated for on-demand debugging

**Token Efficiency Gains**:
- Full codebase loading: Large (avoid when possible)
- Domain-specific files: Targeted to your task (50-80% reduction)
- Layer-specific files: Even more targeted (70-90% reduction vs full domain)
- Typical query: 10-20 symbols (~2-5KB, 95-99% reduction)
- Layer-filtered queries: 5-15 symbols (~1-3KB, 99%+ reduction)

**Progressive Loading Example**:
1. Essential context: 20 symbols = ~5KB (95-99% reduction vs full codebase)
2. Supporting context: +30 symbols = ~12KB total (95-97% reduction)
3. On-demand lookup: +10 symbols = ~15KB total (95-97% reduction)

**Backend Development Example**:
- Loading entire backend domain: Large
- Loading single layer (e.g., services): 70-90% smaller
- **Typical efficiency gain: 80-90% token reduction**

**Comparison to loading full files**:
- Loading full files for context: ~200KB+
- Using domain-specific symbols: ~15KB (93% reduction)
- Using layer-specific symbols: ~10KB (95% reduction)
