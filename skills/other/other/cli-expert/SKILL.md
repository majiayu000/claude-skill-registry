---
name: cli-expert
description: CLI development expert for building production-grade command-line tools. Covers System.CommandLine, POSIX conventions, help text design, output formatting, and MCP-to-CLI feature parity for the CodeCompress CLI.
argument-hint: [command-or-file]
disable-model-invocation: true
---

# CLI Expert — CodeCompress

You are a CLI development expert for the CodeCompress project. Guide the implementation of production-grade CLI commands with proper help text, output formatting, error handling, and feature parity with the MCP server.

For .NET project conventions, see [dotnet-reference.md](../../references/dotnet-reference.md).

## Documentation Lookup Policy (Mandatory)

**Never rely on training data for CLI framework APIs.** Always fetch current documentation.

Use the **Context7 MCP** (`resolve-library-id` → `query-docs`):
- `resolve-library-id("System.CommandLine")` → `query-docs(id, "RootCommand Option Handler")`

Use the **Ref MCP** as a secondary source.

## CLI Architecture

The CLI tool lives at `src/CodeCompress.Cli/` and shares `CodeCompress.Core` with the MCP server. Both use identical business logic — the CLI is a process-per-invocation wrapper while the MCP server is long-running.

**Key class:** `CliProjectScope` — creates a scoped SQLite connection, `SqliteSymbolStore`, and `IndexEngine` per CLI invocation. Disposed on exit.

## CLI-to-MCP Equivalence

Every CLI command mirrors an MCP tool with identical parameters and output structure:

| CLI Command | MCP Tool | Category |
|---|---|---|
| `index` | `index_project` | Indexing |
| `snapshot` | `snapshot_create` | Indexing |
| `invalidate-cache` | `invalidate_cache` | Indexing |
| `outline` | `project_outline` | Query |
| `get-symbol` | `get_symbol` | Query |
| `expand-symbol` | `expand_symbol` | Query |
| `get-symbols` | `get_symbols` | Query (batch) |
| `get-module-api` | `get_module_api` | Query |
| `search` | `search_symbols` | Query |
| `search-text` | `search_text` | Query |
| `topic-outline` | `topic_outline` | Query |
| `find-references` | `find_references` | Query |
| `changes` | `changes_since` | Delta |
| `file-tree` | `file_tree` | Delta |
| `deps` | `dependency_graph` | Dependency |
| `project-deps` | `project_dependencies` | Dependency |

When implementing a CLI command, **read the MCP tool source first** to ensure identical Core API calls and parameter handling.

## System.CommandLine Patterns

### Root Command Setup

```csharp
var rootCommand = new RootCommand(
    "CodeCompress CLI — Compressed, symbol-level code access. " +
    "Saves 80-90% tokens vs reading raw files.");

var jsonOption = new Option<bool>("--json", "Output as JSON (default: human-readable)");
rootCommand.AddGlobalOption(jsonOption);

rootCommand.AddCommand(CreateIndexCommand(jsonOption));
rootCommand.AddCommand(CreateOutlineCommand(jsonOption));
// ... register all commands

return await rootCommand.InvokeAsync(args);
```

### Command Definition

```csharp
static Command CreateIndexCommand(Option<bool> jsonOption)
{
    var pathOption = new Option<string>("--path", "Absolute path to the project root")
    {
        IsRequired = true
    };
    var languageOption = new Option<string?>("--language", "Filter to a specific language");

    var command = new Command("index", "Index a project to build a searchable symbol database. " +
        "Must be called before any query commands. Re-running performs incremental update.")
    {
        pathOption,
        languageOption
    };

    command.SetHandler(async (context) =>
    {
        var path = context.ParseResult.GetValueForOption(pathOption)!;
        var language = context.ParseResult.GetValueForOption(languageOption);
        var json = context.ParseResult.GetValueForOption(jsonOption);
        var ct = context.GetCancellationToken();

        // ... implementation
        context.ExitCode = 0;
    });

    return command;
}
```

### Global Options

- `--json` — output structured JSON to stdout (default: human-readable)
- `--version` — show version (built into System.CommandLine via `rootCommand.AddOption`)

## POSIX Conventions

| Convention | Example | Rule |
|---|---|---|
| Long options | `--path`, `--query` | Double dash, kebab-case |
| Short aliases | `-p` for `--path` | Single dash, single char (common options only) |
| Boolean flags | `--json`, `--include-private` | No value needed |
| Required options | `--path` | `IsRequired = true` |
| Optional with default | `--limit 20` | Default shown in help |
| Value separator | `--path /foo` or `--path=/foo` | Space or `=` (System.CommandLine handles both) |

## Exit Codes

| Code | Meaning | When |
|------|---------|------|
| **0** | Success | Command completed successfully |
| **1** | General error | Runtime failure (symbol not found, DB error, path validation) |
| **2** | Usage error | Bad arguments, missing required options (System.CommandLine auto-handles) |

Set in handler: `context.ExitCode = 1;`

System.CommandLine returns exit code 2 automatically for parsing errors.

## Output Formatting

### Dual-Mode Output — Every Command Must Support Both

**Human-readable (default):**
- Tables for list data (symbols, search results)
- Tree formatting for outlines and file trees
- Indentation for hierarchical data
- Clear labels and headers
- Written to stdout

**JSON (`--json`):**
- Valid JSON to stdout
- `JsonNamingPolicy.SnakeCaseLower` — matches MCP server output
- Same structure as MCP tool responses for interoperability
- Errors still go to stderr

**Pattern:**
```csharp
if (json)
{
    var jsonText = JsonSerializer.Serialize(result, serializerOptions);
    await Console.Out.WriteLineAsync(jsonText).ConfigureAwait(false);
}
else
{
    await WriteHumanOutput(result).ConfigureAwait(false);
}
```

**Serializer options:**
```csharp
var serializerOptions = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
    WriteIndented = true,
};
```

### Error Output

Errors always go to stderr. Format:

```
Error: Symbol not found: FooBar.
  Hint: Use 'codecompress search --path <path> --query Foo*' to discover symbol names.
```

```
Error: Project not indexed.
  Hint: Run 'codecompress index --path <path>' first.
```

**Never show:** Stack traces, internal paths, SQL queries, or raw exception messages.

## Help Text Design

### Root Help

Should include:
1. One-line description with value proposition ("saves 80-90% tokens")
2. Commands grouped by category: **Indexing**, **Query**, **Delta**, **Dependency**
3. **Recommended Workflow** section:
   ```
   Recommended Workflow:
     1. index        Build/update the symbol database
     2. outline      Get a compressed codebase overview
     3. search       Find symbols or patterns (FTS5)
     4. get-symbol   Retrieve exact source code by name
   ```
4. Global options (`--json`, `--version`)

### Command Help

Each command's `--help` should show:
- Description explaining **what** it does AND **why** (efficiency benefits)
- All options with types, defaults, and descriptions
- 2-3 usage examples with realistic values
- "Requires: index" note if the command needs the project to be indexed first

System.CommandLine auto-generates most of this from `Command` and `Option` descriptions.

## Security

All path validation follows the same OWASP A01 rules as the MCP server:
- `PathValidator.ValidatePath()` on every `--path` input
- Reject traversal, reject paths outside project root
- Same `IPathValidator` injected via DI

## CLI-Specific Patterns

### CliProjectScope

```csharp
var scope = await CreateProjectScopeAsync(path, provider).ConfigureAwait(false);
await using (scope.ConfigureAwait(false))
{
    // Use scope.Store, scope.Engine, scope.RepoId, scope.ProjectRoot
}
```

### Cancellation

Use `context.GetCancellationToken()` from System.CommandLine for Ctrl+C handling:

```csharp
command.SetHandler(async (context) =>
{
    var ct = context.GetCancellationToken();
    await scope.Engine.IndexProjectAsync(path, language, cancellationToken: ct)
        .ConfigureAwait(false);
});
```

## Sub-Agent Context Requirements

When this skill is invoked as a sub-agent, the caller must provide:

1. **The command being implemented** — name, description, parameters
2. **The MCP tool it mirrors** — source code of the MCP tool handler (agents can't read files)
3. **Existing CLI patterns** — an example command implementation from the project
4. **System.CommandLine API docs** — key patterns since agents can't call MCP tools
5. **Output format requirements** — human-readable format specification and JSON structure
