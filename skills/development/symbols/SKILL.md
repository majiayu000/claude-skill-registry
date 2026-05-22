---
name: symbols
description: Token-efficient codebase navigation through intelligent symbol loading and querying. Use this skill when implementing new features (find existing patterns), exploring codebase structure, searching for components/functions/types, or understanding architectural layers. Reduces token usage by 60-95% compared to loading full files. Layer split enables 50-80% additional backend efficiency.
---

# Symbols - Intelligent Codebase Symbol Analysis

## Overview

Enable token-efficient navigation through pre-generated symbol graphs chunked by domain and separated from test files. Query symbols by name, kind, path, layer tag, or architectural layer without loading entire files.

**Key Benefits:**
- 60-95% reduction in token usage vs loading full codebase
- Progressive loading strategy (load only what's needed)
- Domain-specific chunking for targeted context (configured per project)
- Layer split for 50-80% token reduction in backend work
- Architectural layer tags for precise filtering (router, service, repository, component, hook, etc.)
- Test file separation (loaded only when debugging)
- Precise code references with file paths and line numbers

<!-- Template Variables:
- SkillMeat - Project or organization name
- { - Project directory structure
- { - Symbol file locations and domain mappings
- Collection (Personal Library) → Projects (Local .claude/ directories) → Deployment Engine → User/Local Scopes - System architecture description
- 1. Source Layer (GitHub, local sources) - Detailed architectural layers breakdown
- See examples/ directory for SkillMeat-specific examples including manifest files, lock files, CLI usage patterns - Real code examples from the project
-->

## Symbol System Lifecycle

The symbols system follows a five-phase lifecycle:

**1. Configuration** - `symbols.config.json` defines project structure (source of truth)
**2. Extraction** - Scripts read config and extract symbols from codebase
**3. Layer Tagging** - Assigns architectural layer tags based on file path patterns
**4. Chunking (Optional)** - Splits large domains into layer-specific files for efficiency
**5. Querying** - Load and query symbols efficiently through `symbol_tools.py`

**Key Flow**: Config defines → Scripts extract → Layer tags enable filtering → Chunking optimizes → Tools query

→ **See `./references/symbol-script-operations.md` for detailed workflows**

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

## Core Functions API

```python
# Query symbols by name, kind, domain, or path
query_symbols(name=None, kind=None, domain=None, path=None, limit=20)

# Load complete symbol set for a domain (excludes tests by default)
load_domain(domain, include_tests=False, max_symbols=None)

# Load symbols from specific architectural layer (50-80% token reduction)
load_api_layer(layer, max_symbols=None)

# Advanced pattern-based search with layer filtering
search_patterns(pattern=None, layer=None, domain=None, limit=30)

# Get full context for specific symbol with relationships
get_symbol_context(name, file=None, include_related=False)
```

**Parameters:**
- `name` - Symbol name (supports partial/fuzzy matching)
- `kind` - Symbol kind: component, hook, function, class, interface, type, method
- `domain` - Domain filter (configured per project: ui, web, api, shared, mobile)
- `path` - File path pattern (e.g., "components", "services")
- `layer` - Architectural layer tag (router, service, repository, component, hook, page, test)
- `limit` - Maximum results to return
- `include_tests` - Include test file symbols
- `include_related` - Include related symbols (props interfaces, same-file symbols)

→ **See `./references/symbol-api-reference.md` for complete documentation**

## Quick Start Examples

**Frontend Pattern:**
```python
from symbol_tools import query_symbols, load_domain
# Find similar components
similar = query_symbols(name="Card", kind="component", domain="ui", limit=10)
# Load web context
web_symbols = load_domain(domain="web", max_symbols=100)
```

**Backend Pattern:**
```python
from symbol_tools import load_api_layer, search_patterns
# Load only service layer (80-90% token reduction)
services = load_api_layer("services", max_symbols=50)
# Find service patterns
patterns = search_patterns(pattern="Service", layer="service", domain="api")
```

**Debugging Pattern:**
```python
from symbol_tools import get_symbol_context, load_domain
# Load component with related symbols
component = get_symbol_context(name="Button", include_related=True)
# Load test context
tests = load_domain(domain="ui", include_tests=True, max_symbols=30)
```

→ **See `./references/symbol-workflows-by-role.md` for complete workflows**

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

## Token Efficiency Summary

**Key Metrics:**
- Full codebase loading: Large (avoid when possible)
- Domain-specific files: 50-80% reduction vs full codebase
- Layer-specific files: 70-90% reduction vs full domain
- Typical query: 10-20 symbols (~2-5KB, 95-99% reduction)
- Layer-filtered queries: 5-15 symbols (~1-3KB, 99%+ reduction)

**Backend Development Example:**
- Loading entire backend domain: Large
- Loading single layer (e.g., services): 70-90% smaller
- **Typical efficiency gain: 80-90% token reduction**

**Progressive Loading Example:**
1. Essential context: 20 symbols = ~5KB (95-99% reduction)
2. Supporting context: +30 symbols = ~12KB total (95-97% reduction)
3. On-demand lookup: +10 symbols = ~15KB total (95-97% reduction)

→ **See `./references/symbol-performance-metrics.md` for benchmarks**

## Symbol Structure

**Required Fields:**
- `name` - Symbol name
- `kind` - Symbol kind (component, function, class, interface, type, hook, method)
- `path` - File path
- `line` - Line number
- `signature` - Function/component signature
- `summary` - Brief description
- `layer` - Architectural layer tag

**Optional Fields:**
- `parent` - Parent symbol (for methods)
- `docstring` - Full documentation
- `category` - Symbol category

**Layer Tags** (all symbols include one):
- Backend: router, service, repository, schema, model, core, auth, middleware
- Frontend: component, hook, page, util
- Test: test

→ **See `./references/symbol-schema-architecture.md` for complete schema**

## Resources

### scripts/symbol_tools.py

Python implementation of all symbol query functions. Execute directly or import:

```bash
python .claude/skills/symbols/scripts/symbol_tools.py
```

```python
from symbol_tools import query_symbols, load_domain, load_api_layer
```

### Supporting Documentation

- **`./references/symbol-api-reference.md`** - Complete API documentation with all parameters and examples
- **`./references/symbol-workflows-by-role.md`** - Role-specific workflows (Frontend, Backend, DevOps, QA)
- **`./references/symbol-script-operations.md`** - Detailed extraction, tagging, and chunking workflows
- **`./references/symbol-performance-metrics.md`** - Performance benchmarks and optimization strategies
- **`./references/symbol-schema-architecture.md`** - Complete schema specification and architecture mapping

### Extraction Scripts

Located in `scripts/`:
- `extract_symbols_typescript.py` - Extract TypeScript/React symbols
- `extract_symbols_python.py` - Extract Python symbols
- `add_layer_tags.py` - Assign architectural layer tags
- `split_api_by_layer.py` - Chunk symbols by layer (OPTIONAL, for backend efficiency)
- `merge_symbols.py` - Merge incremental updates

All scripts read `symbols.config.json` to understand project structure.

### Configuration

- **`symbols.config.json`** - Source of truth for project structure, domain mappings, layer definitions
- **`symbols-config-schema.json`** - Configuration schema validation

## Project Integration

### Slash Commands

- `/symbols-query` - Query symbols efficiently
- `/symbols-search` - Search symbol system
- `/load-symbols` - Initialize symbol system
- `/symbols-update` - Regenerate symbols
- `/symbols-chunk` - Load symbol chunks

### Related Agents

- `symbols-engineer` - Expert in symbol optimization and graph management
- `codebase-explorer` - Uses symbols for efficient code discovery
- Frontend/backend engineers - Use symbols for targeted context loading

### Architecture Integration

Symbols understand and validate SkillMeat's layered architecture as defined in Collection (Personal Library) → Projects (Local .claude/ directories) → Deployment Engine → User/Local Scopes.

**Architecture layers are configured per project** based on 1. Source Layer (GitHub, local sources).

Use `search_patterns()` with `layer` parameter to filter by architectural layer.
