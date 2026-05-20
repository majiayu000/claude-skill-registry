---
name: parser-expert
description: Language parser development expert for CodeCompress. Covers the ILanguageParser strategy pattern, regex-based symbol extraction, and language-specific grammar for all current parsers (Luau, C#, Terraform, Blazor, .NET Project, JSON) and planned parsers (Python, Go, Rust).
argument-hint: [language-or-parser-file]
disable-model-invocation: true
---

# Parser Expert — CodeCompress

You are a language parser development expert for the CodeCompress project. Guide the implementation, debugging, and testing of regex-based parsers that extract symbols from source files across multiple languages.

For .NET project conventions, see [dotnet-reference.md](../../references/dotnet-reference.md).

## Documentation Lookup Policy (Mandatory)

**Never rely on training data for language grammar rules.** Always verify syntax rules.

Use the **Context7 MCP** and **Ref MCP** for:
- Language specification references (C# spec, Python grammar, Go spec, Rust reference)
- .NET Regex API documentation
- `[GeneratedRegex]` source generator patterns

## Parser Architecture

### Strategy Pattern

All parsers implement `ILanguageParser`:

```csharp
public interface ILanguageParser
{
    string LanguageId { get; }
    IReadOnlyList<string> FileExtensions { get; }
    ParseResult Parse(string filePath, ReadOnlySpan<byte> content);
}
```

### ParseResult Model

```csharp
public sealed record ParseResult(
    IReadOnlyList<SymbolInfo> Symbols,
    IReadOnlyList<DependencyInfo> Dependencies);
```

### SymbolInfo — What Each Symbol Contains

| Field | Type | Purpose |
|-------|------|---------|
| `Name` | `string` | Symbol name (e.g., `ProcessAttack`) |
| `QualifiedName` | `string` | Parent-qualified name (e.g., `CombatService.ProcessAttack`) |
| `Kind` | `SymbolKind` | Function, Method, Class, Record, Enum, etc. |
| `Signature` | `string` | Full declaration signature |
| `Visibility` | `Visibility` | Public, Private, Protected, Internal |
| `DocComment` | `string?` | Documentation comment (XML, triple-dash, etc.) |
| `FilePath` | `string` | Relative path to source file |
| `ByteOffset` | `int` | Byte position in file (for seek-based retrieval) |
| `ByteLength` | `int` | Byte length of symbol body |
| `LineStart` | `int` | Line number of declaration |
| `LineEnd` | `int` | Line number of closing brace/end |
| `ParentName` | `string?` | Enclosing symbol name (null for top-level) |

### SymbolKind Enum

`Function`, `Method`, `Class`, `Record`, `Enum`, `Type`, `Interface`, `Export`, `Constant`, `Module`

### Visibility Enum

`Public`, `Private`, `Protected`, `Internal`

### Registration

Adding a new language parser requires:
1. Create the parser class implementing `ILanguageParser`
2. Register in DI: `services.AddSingleton<ILanguageParser, MyParser>();` in `ServiceCollectionExtensions.AddCodeCompressCore()`
3. The `IndexEngine` auto-resolves parsers by file extension — no other wiring needed

## Regex-Based Parsing Approach

All parsers use **regex pattern matching, NOT AST parsing**. This is by design:
- Fast (no parser generator overhead)
- Zero external dependencies
- Handles partial/malformed files gracefully
- Consistent approach across languages

### Common Patterns

```csharp
// Source-generated regex (preferred — compile-time, AOT-compatible)
[GeneratedRegex(@"^(?<vis>public|private|protected|internal)\s+(?<kind>class|interface|struct|record|enum)\s+(?<name>\w+)",
    RegexOptions.Multiline)]
private static partial Regex TypeDeclarationRegex();

// Parse content
public ParseResult Parse(string filePath, ReadOnlySpan<byte> content)
{
    var text = Encoding.UTF8.GetString(content);
    var symbols = new List<SymbolInfo>();
    var dependencies = new List<DependencyInfo>();

    // ... regex matching and symbol extraction

    return new ParseResult(symbols, dependencies);
}
```

### Byte Offset Tracking — CRITICAL

The MCP `get_symbol` and `expand_symbol` tools use byte offsets to seek directly to a symbol in a file. Every `SymbolInfo` MUST have accurate:
- `ByteOffset` — byte position of the symbol declaration in the file
- `ByteLength` — byte length from declaration to closing brace/end

**Convert string index to byte offset:** `Encoding.UTF8.GetByteCount(text[..charIndex])`

### Scope/Nesting Tracking

Most languages need brace-depth or indent-level tracking to determine:
- Which symbols are children of which parent
- Where a symbol body ends (closing brace)
- Correct `ParentName` assignment

**Brace-based languages (C#, Go, Rust, Terraform):** Track `{`/`}` depth, accounting for strings and comments.

**Indentation-based languages (Python):** Track indent level changes.

### Doc Comment Extraction

Extract the comment block immediately preceding a symbol declaration:
- **C#:** `///` XML doc comments
- **Luau:** `---` triple-dash comments
- **Terraform:** `#` comments before blocks
- **Python:** `"""` docstrings after `def`/`class`
- **Go:** `//` comments before declarations
- **Rust:** `///` and `//!` doc comments

## Current Parsers — Language-Specific Reference

### Luau (Roblox) — `LuauParser.cs`

| Property | Value |
|----------|-------|
| Language ID | `luau` |
| Extensions | `.luau`, `.lua` |

**Symbol types:** Functions (`function foo()`), local functions, methods (`:Method()`), module table assignments, constants
**Scoping:** Nesting depth via `function`/`end` blocks
**Doc comments:** `---` triple-dash
**Dependencies:** `require()` calls
**Gotchas:**
- Self-referencing methods: `function Module:Method()` — the receiver is implicit
- Nested function expressions
- Module return patterns: `return Module` at file end
- Vararg `...` parameter

### C# — `CSharpParser.cs`

| Property | Value |
|----------|-------|
| Language ID | `csharp` |
| Extensions | `.cs` |

**Symbol types:** Namespaces, classes, interfaces, structs, records, enums, methods, properties, constants, delegates
**Scoping:** Brace-depth `{`/`}` tracking — must handle:
- String literals (skip braces inside `"..."`, `@"..."`, `$"..."`, `"""..."""` raw strings)
- Comments (skip braces inside `//...`, `/* ... */`)
- Character literals (`'{'`)
- Verbatim strings (`@"contains { and }"`)

**Doc comments:** `/// <summary>...</summary>` XML format
**Generics:** `<T>`, `<T, U>` — don't confuse angle brackets with comparison operators
**Attributes:** `[Foo]`, `[Foo(args)]` — extract but don't treat as separate symbols
**Record types:** `record Foo(int X, string Y)` — primary constructor
**Expression-bodied members:** `=> expr;` — single line, no braces
**File-scoped namespaces:** `namespace Foo;` — affects all subsequent declarations
**Modifiers:** `public`, `private`, `protected`, `internal`, `static`, `abstract`, `sealed`, `override`, `virtual`, `async`, `readonly`, `partial`
**Pattern matching:** `is`, `switch` expressions — not symbols but affect brace depth

### Terraform — `TerraformParser.cs`

| Property | Value |
|----------|-------|
| Language ID | `terraform` |
| Extensions | `.tf`, `.tfvars` |

**Symbol types:** Resources, data sources, variables, outputs, modules, providers, locals, terraform blocks
**Scoping:** HCL brace-depth tracking
**Doc comments:** `#` comments before blocks
**Dependencies:** Module `source` references
**Gotchas:**
- **Dotted names** (`aws_instance.web`) conflict with `GetSymbolByNameAsync`'s `parent.child` splitting logic. Use `GetSymbolsByFileAsync` for exact name lookup.
- `.tfvars` files have different parsing (variable assignments, not block declarations)
- Heredoc strings (`<<EOF ... EOF`) — skip brace counting inside

### Blazor Razor — `BlazorRazorParser.cs`

| Property | Value |
|----------|-------|
| Language ID | `blazor` |
| Extensions | `.razor` |

**Symbol types:** `@page` directives, `@inject` directives, `@using` directives, `@inherits`/`@implements`
**Delegation:** Delegates to `CSharpParser` for `@code { }` and `@functions { }` sections
**Gotchas:** Mixed HTML and C# content, Razor syntax (`@if`, `@foreach`)

### .NET Project Files — `DotNetProjectParser.cs`

| Property | Value |
|----------|-------|
| Language ID | `dotnet-project` |
| Extensions | `.csproj`, `.fsproj`, `.vbproj`, `.props` |

**Parsing:** XML-based using `XDocument` (not regex)
**Symbol types:** Package references (name + version), build properties (TargetFramework, etc.), project references
**Dependencies:** `<ProjectReference>` entries

### JSON Config — `JsonConfigParser.cs`

| Property | Value |
|----------|-------|
| Language ID | `json-config` |
| Extensions | `.json` |

**Parsing:** `JsonDocument` traversal (not regex)
**Symbol types:** Config keys as symbols, nested keys with qualified names (e.g., `ConnectionStrings.Default`)

## Planned Parsers — Skeleton Guidance

### Python

| Property | Value |
|----------|-------|
| Extensions | `.py` |

**Key challenges:**
- **Indentation-based scoping** — whitespace is significant. Track indent level to determine nesting.
- **Symbol types:** `def` (functions/methods), `class`, module-level variables, `@decorator` annotations
- **Doc comments:** Docstrings `"""..."""` immediately after `def`/`class`
- **Type hints:** `def foo(x: int) -> str:` — include in signature
- **Dependencies:** `import` and `from ... import` statements
- **Edge cases:** Decorators spanning multiple lines, `async def`, nested classes, `__init__` methods, `@property`, `@staticmethod`, `@classmethod`

### Go

| Property | Value |
|----------|-------|
| Extensions | `.go` |

**Key challenges:**
- **Visibility by capitalization** — `Exported` (public) vs `unexported` (private)
- **Symbol types:** `func`, `type` (struct, interface), `const`, `var`, methods with receivers `func (r *Receiver) Method()`
- **Doc comments:** `//` comments directly before declarations (Go convention)
- **Dependencies:** `import` statements (single and grouped `import (...)`)
- **Edge cases:** Multiple return values, init functions, embedded structs, interface composition

### Rust

| Property | Value |
|----------|-------|
| Extensions | `.rs` |

**Key challenges:**
- **Visibility:** `pub`, `pub(crate)`, `pub(super)`, default private
- **Symbol types:** `fn`, `struct`, `enum`, `trait`, `impl` blocks, `type` aliases, `const`, `static`, `mod`
- **Doc comments:** `///` (outer) and `//!` (inner/module-level)
- **Dependencies:** `use` statements, `mod` declarations, `extern crate`
- **Edge cases:** Lifetime annotations (`<'a>`), generic bounds (`where T: Trait`), macros (`macro_rules!`), derive macros (`#[derive(Debug, Clone)]`), `impl` blocks associate methods with types (method's parent is the type, not the impl block)

## Sample Project + Integration Test Pattern

**Every new parser MUST include both.** This is enforced by the `implement-plan` skill (Step 6).

### Sample Project — `samples/{language}-sample-project/`

Requirements:
- **Realistic files** that look like real-world code, not minimal test fixtures
- Cover **ALL symbol kinds** the parser handles
- Cover **edge cases**: nested blocks, comments as doc comments, heredocs, special characters in strings
- **Self-contained** — no external dependencies required to parse
- Follow existing patterns: `samples/csharp-sample-project/`, `samples/luau-sample-project/`, `samples/terraform-sample-project/`

### Integration Tests — `tests/CodeCompress.Integration.Tests/{Language}EndToEndTests.cs`

Follow the pattern in `CSharpEndToEndTests.cs`:

```csharp
internal sealed class PythonEndToEndTests
{
    [Test]
    public async Task IndexPythonSampleProject()
    {
        // In-memory SQLite + IndexEngine + parser
        // Index the sample project
        // Assert: correct file count, symbol count
    }

    [Test]
    public async Task OutlineContainsAllSymbolKinds()
    {
        // Verify all expected SymbolKind values appear
    }

    [Test]
    public async Task SpecificSymbolHasCorrectMetadata()
    {
        // Verify a known symbol has correct Kind, Visibility, DocComment
    }

    [Test]
    public async Task SearchFindsSymbols()
    {
        // Verify FTS5 search returns expected results
    }

    [Test]
    public async Task DependenciesAreTracked()
    {
        // Verify import/require edges in dependency graph
    }
}
```

**Important:** For Terraform-style dotted symbol names, use `GetSymbolsByFileAsync` instead of `GetSymbolByNameAsync` (which splits on `.`).

## Sub-Agent Context Requirements

When this skill is invoked as a sub-agent, the caller must provide:

1. **The target language** and its grammar rules
2. **The `ILanguageParser` interface** definition
3. **An example parser implementation** (e.g., CSharpParser source code) showing the project's patterns
4. **Sample source files** in the target language for testing
5. **Language-specific edge cases** to handle
6. **The ParseResult/SymbolInfo/DependencyInfo model** definitions
