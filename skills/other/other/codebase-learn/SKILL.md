---
name: codebase-learn
description: Learn codebase structure with tree-sitter + SSL patterns
execution: task
model: inherit
aliases: [learn-codebase, map-code]
---

# Codebase Learn

Two-phase codebase understanding:
1. **C++ tool** (`learn_codebase`): AST extraction, provenance, hierarchical state
2. **Claude**: High-level SSL patterns for architecture and relationships

```ssl
[codebase-learn] tool + understanding

phase1: learn_codebase→tree-sitter→symbols+triplets+hierarchy
  handles: parsing, storage, provenance, staleness tracking
  output: Symbol nodes, file→contains→symbol triplets, ModuleState

phase2: Claude→architecture→SSL patterns
  handles: why, how, relationships between components
  output: Wisdom nodes with [LEARN] markers
```

## Supported Languages

Tree-sitter parsers available:
- **C/C++**: `.c`, `.h`, `.cpp`, `.hpp`, `.cc`, `.cxx`, `.hxx`
- **Python**: `.py`, `.pyw`
- **JavaScript/TypeScript**: `.js`, `.jsx`, `.mjs`, `.ts`, `.tsx`
- **Go**: `.go`
- **Rust**: `.rs`
- **Java**: `.java`
- **Ruby**: `.rb`
- **C#**: `.cs`

## Usage

### Step 1: Run learn_codebase

```bash
chitta learn_codebase --path /path/to/project --project myproject
```

This single command:
- Finds all supported source files (excludes build dirs, node_modules, etc.)
- Extracts symbols with tree-sitter AST
- Creates Symbol nodes with provenance (source_path, hash)
- Creates triplets (file contains symbol, scope contains method)
- Bootstraps hierarchical state (ProjectEssence + ModuleState)
- Registers files for staleness tracking

Output:
```
Learned codebase: myproject

Files: 47 analyzed (of 52 found)
Symbols: 1234 stored
Triplets: 2567 created
Modules: 15 bootstrapped

Hierarchical State Modules:
  Mind @include/chitta/mind.hpp
  Storage @include/chitta/storage.hpp
  ...
```

### Step 2: Add SSL Patterns (Claude)

After learn_codebase runs, I add architectural understanding:

```
[LEARN] [myproject] Mind→orchestrator→recall/observe/grow API
[ε] Central class managing tiered storage + embeddings + graph. @mind.hpp:52
[TRIPLET] Mind uses TieredStorage
[TRIPLET] Mind uses HierarchicalState
[TRIPLET] Mind provides recall

[LEARN] [myproject] HierarchicalState→token compression→3-level injection
[ε] L0=ProjectEssence(50t) + L1=ModuleState(20t) + L2=PatternState(10t)
[TRIPLET] HierarchicalState contains ProjectEssence
[TRIPLET] injection_protocol saves tokens
```

SSL captures what AST can't:
- **Why** a component exists
- **How** components relate architecturally
- **Patterns** and design decisions

## Incremental Updates

When code changes:

```bash
# Re-learn (only re-analyzes changed files with incremental: true default)
chitta learn_codebase --path /path/to/project

# Force full re-index if needed
chitta learn_codebase --path /path/to/project --force true
```

Incremental tracking means:
- Each file hash is stored
- Re-analysis only processes changed files by default
- Use `--force true` to re-index everything

## Token Savings

Traditional: inject full code context (~thousands of tokens)

Smart context approach:
- Codebase overview provides high-level structure
- Symbol search finds specific definitions
- Semantic search with embeddings finds related code
- **Result: targeted context vs full file dumps**

View codebase structure:
```bash
chitta codebase_overview --project myproject
```

## Example: Learning cc-soul

```bash
# Step 1: C++ tool does the heavy lifting
chitta learn_codebase --path /path/to/cc-soul/chitta --project cc-soul

# Step 2: I add architectural SSL
[LEARN] [cc-soul] chitta→semantic memory substrate→tiered storage + SSL + triplets
[ε] C++ daemon: hot/warm/cold storage, JSON-RPC socket, Hebbian learning.
[TRIPLET] chitta contains Mind
[TRIPLET] Mind orchestrates recall
[TRIPLET] Mind orchestrates observe

[LEARN] [cc-soul] provenance→staleness tracking→source_path+hash→Fresh|MaybeStale|Stale
[ε] Two-phase: immediate MaybeStale marking, background verification.
[TRIPLET] Node has provenance
[TRIPLET] provenance tracks staleness
```

## Semantic Enrichment (Background)

The daemon automatically generates semantic descriptions for symbols using OpenCode:

```bash
# Check enrichment status
chitta soul_context  # Shows pending count at startup

# Query described symbols
chitta recall --query "memory storage class" --tag code-intel
```

**Enrichment progress:**
- Daemon processes ~10 symbols every 2 minutes
- Priority: classes → functions → methods
- Each symbol gets a 1-2 sentence description
- Enables semantic search: "persistent storage" → `DuckDBStore @duckdb_store.hpp:45`

**Daemon options:**
```bash
chittad daemon --enrich-interval 2 --enrich-batch 10  # defaults
chittad daemon --no-enrich  # disable enrichment
```

## Benefits

After running:
- `recall("Mind architecture")` → finds Symbol nodes AND architectural SSL
- `recall("memory storage")` → finds enriched code descriptions
- `codebase_overview --project cc-soul` → see full structure at a glance
- `query --subject Mind` → find all Mind relationships
- `search_symbols --query "storage"` → semantic search across symbols

The soul knows both structure (symbols) and meaning (SSL + semantic descriptions).
