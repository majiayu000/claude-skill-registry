---
name: mcp-efficiency
description: Token-efficient codebase exploration using MCP servers (Serena, Context7, JetBrains, Claude-mem). Reduces token usage by 80-90% through structured queries. Use ALWAYS before reading files to minimize context window usage.
---

# MCP Efficiency

Master MCP tools to reduce token usage while improving code understanding.

---

## CRITICAL: search_for_pattern Token Limits

> **WARNING: Improper use of `search_for_pattern` causes 20k+ token responses!**

### MANDATORY Parameters for search_for_pattern

| Parameter | REQUIRED | Default Danger |
|-----------|----------|----------------|
| `relative_path` | ALWAYS set | Full codebase = 50k+ tokens |
| `context_lines_after` | `0-2` max | High values = exponential growth |
| `max_answer_chars` | `3000-5000` | No limit = unbounded output |

### Quick Examples

```python
# BAD - Will return 20k+ tokens:
search_for_pattern(substring_pattern=r"import.*Dto")
search_for_pattern(substring_pattern=r".*Mapper\.kt")  # Wrong tool!

# GOOD - Scoped and limited:
search_for_pattern(
    substring_pattern=r"@Service",
    relative_path="module-core-domain/",
    context_lines_after=1,
    max_answer_chars=3000
)
```

### Use Correct Tool

| Need | WRONG | CORRECT |
|------|-------|---------|
| Find files | `search_for_pattern(r".*\.kt")` | `find_file(file_mask="*.kt")` |
| Signatures | `search_for_pattern` | `find_symbol(include_body=False)` |
| Structure | `search_for_pattern` | `get_symbols_overview` |

---

## Serena Infrastructure (Project-Specific)

### Cache Structure

```
.serena/
├── cache/
│   ├── documents/              # Document index for token-efficient search
│   │   └── document_index.json # Indexed docs with tag/title/content search
│   ├── kotlin/                 # Kotlin symbol cache (basecamp-server)
│   ├── python/                 # Python symbol cache (parser, connect, cli)
│   │   ├── document_symbols.pkl
│   │   └── raw_document_symbols.pkl
│   └── typescript/             # TypeScript symbol cache (basecamp-ui)
├── memories/                   # Project patterns and knowledge
│   ├── server_patterns.md      # Spring Boot/Kotlin patterns
│   ├── ui_patterns.md          # React/TypeScript patterns
│   ├── cli_patterns.md         # Python CLI patterns
│   ├── cli_test_patterns.md    # pytest/fixture patterns
│   ├── parser_patterns.md      # Flask/SQLglot patterns
│   └── connect_patterns.md     # Integration patterns
└── project.yml                 # Project configuration
```

### Make Commands (Cache Sync)

| Command | Purpose |
|---------|---------|
| `make serena-server` | Update basecamp-server symbols, docs & memories |
| `make serena-ui` | Update basecamp-ui symbols, docs & memories |
| `make serena-parser` | Update basecamp-parser symbols, docs & memories |
| `make serena-connect` | Update basecamp-connect symbols, docs & memories |
| `make serena-cli` | Update interface-cli symbols, docs & memories |
| `make serena-update-all` | Force update all projects |
| `make serena-status` | Check cache status |
| `make doc-search q="query"` | Search documentation index (94% savings) |

### Post-Implementation Cache Sync

After making significant changes, sync the Serena cache:

```bash
# After server changes
make serena-server

# After UI changes
make serena-ui

# After CLI changes
make serena-cli

# Check cache status
make serena-status
```

## Why This Matters

| Approach | Tokens | Use Case |
|----------|--------|----------|
| Read full file | 5000+ | Rarely needed |
| Serena overview | 200-500 | Structure understanding |
| Serena find_symbol | 100-300 | Specific signatures |
| Context7 docs | 500-1000 | Framework patterns |

**Rule**: Never read a file until MCP tools fail to answer the question.

## Document Search (NEW - Priority 0)

**BEFORE using Serena symbol queries**, search project documentation for patterns/context:

### Quick Search (CLI)

```bash
# Search indexed documentation
python3 scripts/serena/document_indexer.py --search "hexagonal architecture" --max-results 5
```

### Token Comparison

| Documentation Need | Old Way | New Way | Savings |
|-------------------|---------|---------|---------|
| Find architecture pattern | Read PATTERNS.md (5000 tokens) | Doc search (300 tokens) | 94% |
| Check entity rules | Read README.md (3000 tokens) | Doc search (400 tokens) | 87% |
| API reference | Read multiple docs (8000 tokens) | Doc search (500 tokens) | 94% |

### Document Search Workflow

```python
# Step 1: Search document index FIRST
# CLI: python3 scripts/serena/document_indexer.py --search "repository pattern"

# Step 2: Read only relevant section (from search results)
# If result shows: line_start=45, line_end=80
Read(file_path="project-basecamp-server/docs/PATTERNS.md", offset=45, limit=35)

# Step 3: Then use Serena for code exploration
serena.get_symbols_overview("module-core-domain/repository/")
```

### When to Use Document Search

| Need | Use Document Search First? |
|------|---------------------------|
| Architecture patterns | YES - search `tag:architecture` |
| Implementation guide | YES - search `tag:implementation` |
| API endpoint info | YES - search `tag:api` |
| Test patterns | YES - search `tag:testing` |
| Specific code implementation | NO - use Serena directly |
| Framework best practices | NO - use Context7 |

> See `doc-search` skill for comprehensive guide.

## MCP Server Reference

| Server | Purpose | Best For |
|--------|---------|----------|
| **serena** | Semantic code analysis | Symbol navigation, references, refactoring, memory |
| **context7** | Framework docs | Best practices, API usage |
| **jetbrains** | IDE integration | Inspections, refactoring, run configurations |
| **claude-mem** | Cross-session memory | Past decisions, timeline, batch queries |

### Server Strengths

**Serena** (30+ languages via LSP):
- Symbol-level code understanding (not just text search)
- Project memory for patterns and decisions
- Semantic editing (insert_after_symbol, replace_symbol_body)

**JetBrains** (IDE 2025.2+):
- IntelliJ inspections (errors, warnings, code smells)
- Rename refactoring (understands code structure)
- Run configurations and terminal commands

**claude-mem** (Cross-session):
- Search past work across all sessions
- Timeline context around decisions
- Batch fetch for efficiency

## Serena Workflow (Primary)

### Step 1: Understand Structure

```python
# Get file overview (no body content)
serena.get_symbols_overview(relative_path="src/services/")

# Result: Lists classes, functions with signatures only
# Token cost: ~200-500 (vs 5000+ for full file)
```

### Step 2: Find Specific Symbols

```python
# Find by name pattern
serena.find_symbol(
    name_path_pattern="UserService",
    depth=1,                    # Include immediate children
    include_body=False          # Signatures only
)

# Find with body (when needed)
serena.find_symbol(
    name_path_pattern="UserService/createUser",
    include_body=True           # Get implementation
)
```

### Step 3: Trace Dependencies

```python
# Who calls this method?
serena.find_referencing_symbols(
    name_path="createUser",
    relative_path="src/services/UserService.kt"
)

# Result: All callers with file:line references
```

### Step 4: Pattern Search (TOKEN CRITICAL)

**WARNING**: `search_for_pattern` can easily return 20k+ tokens with wrong settings!

```python
# BAD: Returns 20k+ tokens (all controller bodies)
serena.search_for_pattern(
    substring_pattern=r"@RequestMapping.*",
    context_lines_after=10  # NEVER use high context!
)

# GOOD: Minimal output (~500 tokens)
serena.search_for_pattern(
    substring_pattern=r"@Transactional",
    restrict_search_to_code_files=True,
    context_lines_before=0,   # Default: 0
    context_lines_after=1,    # Just the class/method signature
    relative_path="module-core-domain/",  # ALWAYS scope!
    max_answer_chars=3000     # Limit output size
)
```

**Pattern Search Rules:**
1. **ALWAYS** set `context_lines_before=0` and `context_lines_after<=2`
2. **ALWAYS** specify `relative_path` to scope the search
3. **ALWAYS** use `max_answer_chars` to limit output
4. **PREFER** `find_symbol` over `search_for_pattern` when looking for code structure

### Step 5: Memory Management

```python
# Read project-specific patterns (ALWAYS do this first!)
serena.read_memory(memory_file_name="cli_patterns")
serena.read_memory(memory_file_name="server_patterns")

# List all available memories
serena.list_memories()

# Write new patterns/decisions for future reference
serena.write_memory(
    memory_file_name="new_feature_patterns",
    content="# Feature Patterns\n..."
)

# Edit existing memory
serena.edit_memory(
    memory_file_name="cli_patterns",
    needle="old_pattern",
    repl="new_pattern",
    mode="literal"  # or "regex"
)
```

### Step 6: Semantic Editing

```python
# Replace entire symbol body (method, class, function)
serena.replace_symbol_body(
    name_path="UserService/createUser",
    relative_path="src/services/user.py",
    body="def createUser(self, data: dict) -> User:\n    ..."
)

# Insert code after a symbol
serena.insert_after_symbol(
    name_path="UserService",
    relative_path="src/services/user.py",
    body="\n\ndef new_helper_function():\n    pass"
)

# Insert code before a symbol
serena.insert_before_symbol(
    name_path="UserService",
    relative_path="src/services/user.py",
    body="# New import\nfrom typing import Optional\n"
)

# Rename symbol across codebase
serena.rename_symbol(
    name_path="createUser",
    relative_path="src/services/user.py",
    new_name="create_user"
)
```

### Step 7: Think Tools (Self-Reflection)

```python
# Use after gathering information
serena.think_about_collected_information()

# Use before making code changes
serena.think_about_task_adherence()

# Use when believing task is complete
serena.think_about_whether_you_are_done()
```

## Context7 Workflow (Framework Docs)

### Resolve Library First

```python
# Step 1: Get library ID
context7.resolve-library-id(
    query="How to configure transactions in Spring Boot",
    libraryName="spring-boot"
)
# Returns: /spring/spring-boot
```

### Query Documentation

```python
# Step 2: Get specific docs
context7.query-docs(
    libraryId="/spring/spring-boot",
    query="transaction propagation and isolation levels"
)
```

### Common Library IDs

| Library | ID |
|---------|-----|
| Spring Boot | `/spring/spring-boot` |
| React | `/facebook/react` |
| TanStack Query | `/tanstack/query` |
| Typer | `/tiangolo/typer` |
| pytest | `/pytest-dev/pytest` |

## JetBrains Integration

### Text & Regex Search

```python
# Text search (fast, index-based)
jetbrains.search_in_files_by_text(
    searchText="@Repository",
    fileMask="*.kt",
    directoryToSearch="src/"
)

# Regex search (pattern matching)
jetbrains.search_in_files_by_regex(
    regexPattern=r"class\s+\w+Service",
    fileMask="*.kt",
    directoryToSearch="src/",
    caseSensitive=True
)
```

### Code Inspection & Problems

```python
# Get errors/warnings using IntelliJ inspections
jetbrains.get_file_problems(
    filePath="src/services/UserService.kt",
    errorsOnly=False,  # Include warnings
    timeout=5000       # ms
)
# Returns: severity, description, line/column for each issue
```

### Symbol Info & Quick Docs

```python
# Get symbol documentation at position
jetbrains.get_symbol_info(
    filePath="src/services/UserService.kt",
    line=42,
    column=15
)
# Returns: name, signature, type, documentation
```

### Refactoring

```python
# Context-aware rename (updates ALL references)
jetbrains.rename_refactoring(
    pathInProject="src/services/UserService.kt",
    symbolName="createUser",
    newName="createNewUser"
)
# Much smarter than search-replace - understands code structure!

# Reformat file with IDE rules
jetbrains.reformat_file(path="src/services/UserService.kt")
```

### Run Configurations

```python
# List available run configs
jetbrains.get_run_configurations()
# Returns: config names, command lines, env vars

# Execute a run configuration
jetbrains.execute_run_configuration(
    configurationName="Run Tests",
    timeout=60000,  # ms
    maxLinesCount=500
)
```

### Terminal Integration

```python
# Execute shell command in IDE terminal
jetbrains.execute_terminal_command(
    command="./gradlew test",
    timeout=120000,
    maxLinesCount=1000,
    executeInShell=True  # Use user's shell env
)
```

### File Operations

```python
# Find files by glob pattern
jetbrains.find_files_by_glob(
    globPattern="**/test_*.py",
    subDirectoryRelativePath="tests/"
)

# Fast file name search (index-based)
jetbrains.find_files_by_name_keyword(
    nameKeyword="Service",
    fileCountLimit=50
)

# Create file with content
jetbrains.create_new_file(
    pathInProject="src/new_feature/service.py",
    text="# New service\n...",
    overwrite=False
)

# Get directory tree
jetbrains.list_directory_tree(
    directoryPath="src/",
    maxDepth=3
)
```

### Project Info

```python
# Get project dependencies
jetbrains.get_project_dependencies()

# Get project modules
jetbrains.get_project_modules()

# Get VCS roots (multi-repo support)
jetbrains.get_repositories()

# Get open files in editor
jetbrains.get_all_open_file_paths()
```

## Claude-mem (Cross-Session Memory)

### Search Past Work

```python
# Search all past sessions
claude-mem.search(
    query="authentication decision",
    project="dataops-platform",  # Required
    limit=20,
    type="observations"  # observations, sessions, prompts
)

# Filter by observation type
claude-mem.search(
    query="bug",
    obs_type="bugfix",  # bugfix, feature, decision, discovery, change
    project="dataops-platform",
    limit=20
)

# Date-filtered search
claude-mem.search(
    type="observations",
    dateStart="2025-12-01",
    dateEnd="2025-12-31",
    project="dataops-platform"
)
```

### Timeline Context

```python
# Get context around a specific observation
claude-mem.timeline(
    anchor=11131,        # Observation ID
    depth_before=3,      # Items before
    depth_after=3,       # Items after
    project="dataops-platform"
)

# Auto-find anchor from query
claude-mem.timeline(
    query="authentication",
    depth_before=5,
    depth_after=5,
    project="dataops-platform"
)

# Get context around observation ID
claude-mem.get_context_timeline(
    anchor=11131,
    depth_before=3,
    depth_after=3
)
```

### Batch Fetching (10-100x Faster!)

```python
# ALWAYS use for 2+ observations (single HTTP request)
claude-mem.get_observations(
    ids=[11131, 10942, 10855],
    orderBy="date_desc",
    project="dataops-platform"
)

# Single observation (only when exactly 1 needed)
claude-mem.get_observation(id=11131)

# Fetch session details
claude-mem.get_session(id=2005)

# Fetch prompt details
claude-mem.get_prompt(id=5421)
```

### Recent Context

```python
# Get most recent observations
claude-mem.get_recent_context(
    project="dataops-platform",
    limit=10
)
```

### Workflow Pattern

```
1. Search → Get index of results with IDs
2. Timeline → Get context around top results
3. Review → Pick relevant IDs from titles/dates
4. Batch Fetch → Get full details only for needed IDs
```

## Decision Tree

```
Need documentation/patterns? (FIRST!)
├── What's the project architecture?
│   └── doc-search "architecture" → read section
├── What implementation patterns exist?
│   └── doc-search "pattern" + project name → read section
├── How should I implement feature X?
│   └── doc-search "implementation guide" → read section
└── What are the testing conventions?
    └── doc-search "testing" → read section

Need to understand code?
├── What's in this file/directory?
│   └── serena.get_symbols_overview
├── How is X implemented?
│   └── serena.find_symbol(include_body=True)
├── Who uses X?
│   └── serena.find_referencing_symbols
├── Where is pattern X used?
│   └── serena.search_for_pattern OR jetbrains.search_in_files_by_regex
├── What's the best practice for X?
│   └── context7.query-docs
├── What did we decide before?
│   └── claude-mem.search → timeline → get_observations
└── Is there a problem in this file?
    └── jetbrains.get_file_problems

Need to edit code?
├── Rename a symbol everywhere?
│   ├── serena.rename_symbol (LSP-based)
│   └── jetbrains.rename_refactoring (IDE-based)
├── Replace entire method/class?
│   └── serena.replace_symbol_body
├── Add new code after existing symbol?
│   └── serena.insert_after_symbol
└── Reformat file?
    └── jetbrains.reformat_file

Need project info?
├── What memories exist for this project?
│   └── serena.list_memories → read_memory
├── What run configurations are available?
│   └── jetbrains.get_run_configurations
├── What are the project dependencies?
│   └── jetbrains.get_project_dependencies
└── What happened in past sessions?
    └── claude-mem.get_recent_context
```

## Progressive Disclosure Pattern

Always start narrow, expand only if needed:

```python
# Level 1: Structure only (cheapest)
serena.get_symbols_overview(relative_path="src/services/")

# Level 2: Signatures (if class identified)
serena.find_symbol("UserService", depth=1, include_body=False)

# Level 3: Specific method body (if needed)
serena.find_symbol("UserService/createUser", include_body=True)

# Level 4: Full file read (last resort)
Read(file_path="src/services/UserService.kt")
```

## Common Mistakes

| Mistake | Token Cost | Better Approach |
|---------|------------|-----------------|
| Read file first | High | Use serena.get_symbols_overview |
| Read all files in directory | Very High | Use serena.find_symbol with pattern |
| Multiple full file reads | Extreme | Use serena.find_referencing_symbols |
| Google for framework docs | Time waste | Use context7.query-docs |
| Ask user about past decision | Slow | Use claude-mem.search |

## search_for_pattern Token Cost Examples

| Query | Context | Scope | Est. Tokens |
|-------|---------|-------|-------------|
| `@RequestMapping` | 0/0 | controller/ | ~800 |
| `@RequestMapping` | 0/1 | controller/ | ~1,500 |
| `@RequestMapping` | 2/10 | controller/ | **~21,000** |
| `@RequestMapping` | 2/10 | (none) | **~50,000+** |
| `@Service` | 0/0 | service/ | ~400 |
| `@Service` | 0/0 | (none) | ~2,000 |

**Rule of Thumb:** Every +1 to `context_lines_after` = ~2x token cost

## MCP-First Checklist

Before reading ANY file, ask:

- [ ] Can `get_symbols_overview` answer this?
- [ ] Can `find_symbol` with signatures answer this?
- [ ] Do I need the full body, or just the signature?
- [ ] Is this a framework question? (use context7)
- [ ] Did we discuss this before? (use claude-mem)

## Token Savings Examples

| Task | Without MCP | With MCP | Savings |
|------|-------------|----------|---------|
| Find class structure | 5000 tokens | 300 tokens | 94% |
| Find all usages | 15000 tokens | 800 tokens | 95% |
| Understand API pattern | 3000 tokens | 500 tokens | 83% |
| Check framework docs | N/A | 600 tokens | Faster |
| Search past decisions | N/A | 200 tokens | Instant |
| Run IDE inspections | Manual | 100 tokens | Automatic |

---

## Quick Reference: All MCP Tools

### Serena (Semantic Code Analysis)

| Tool | Purpose |
|------|---------|
| `get_symbols_overview` | File/directory structure overview |
| `find_symbol` | Search symbols by name/pattern |
| `find_referencing_symbols` | Find all references to a symbol |
| `search_for_pattern` | Regex search across codebase |
| `replace_symbol_body` | Replace entire symbol definition |
| `insert_before_symbol` | Insert code before a symbol |
| `insert_after_symbol` | Insert code after a symbol |
| `rename_symbol` | Refactor symbol name globally |
| `read_memory` | Load project-specific patterns |
| `write_memory` | Save patterns for future |
| `edit_memory` | Update existing memory |
| `list_memories` | List available memories |
| `list_dir` | Directory listing |
| `find_file` | Find files by mask |
| `think_about_*` | Self-reflection tools |

### JetBrains (IDE Integration)

| Tool | Purpose |
|------|---------|
| `search_in_files_by_text` | Fast text search (indexed) |
| `search_in_files_by_regex` | Pattern-based search |
| `get_file_problems` | IntelliJ inspections (errors/warnings) |
| `get_symbol_info` | Quick docs at position |
| `rename_refactoring` | Context-aware rename |
| `reformat_file` | Apply IDE formatting |
| `get_run_configurations` | List run configs |
| `execute_run_configuration` | Run a configuration |
| `execute_terminal_command` | Run shell command |
| `find_files_by_glob` | Glob pattern file search |
| `find_files_by_name_keyword` | Keyword file search |
| `list_directory_tree` | Directory tree view |
| `create_new_file` | Create file with content |
| `get_project_dependencies` | List dependencies |
| `get_project_modules` | List modules |
| `get_repositories` | List VCS roots |

### Claude-mem (Cross-Session Memory)

| Tool | Purpose |
|------|---------|
| `search` | Search past work (required: project) |
| `timeline` | Context around observation |
| `get_observations` | Batch fetch (10-100x faster) |
| `get_observation` | Single observation |
| `get_session` | Session details |
| `get_prompt` | Prompt details |
| `get_recent_context` | Recent observations |
| `get_context_timeline` | Timeline around ID |

### Context7 (Framework Docs)

| Tool | Purpose |
|------|---------|
| `resolve-library-id` | Get library ID for docs |
| `query-docs` | Query framework documentation |

---

## Sources

- [JetBrains MCP Server Documentation](https://www.jetbrains.com/help/idea/mcp-server.html)
- [Serena GitHub Repository](https://github.com/oraios/serena)
- [Serena Tools Documentation](https://oraios.github.io/serena/01-about/035_tools.html)
- [IntelliJ IDEA 2025.1 MCP Blog](https://blog.jetbrains.com/idea/2025/05/intellij-idea-2025-1-model-context-protocol/)
