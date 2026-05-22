---
name: Parser Developer
description: Guides AILANG parser development with conventions and patterns. Use when user wants to modify parser, understand parser architecture, or debug parser issues. Saves 30% of development time by preventing token position bugs.
---

# Parser Developer

Master AILANG parser development with critical conventions that prevent common bugs.

## Quick Start

**⚠️ READ THIS BEFORE WRITING PARSER CODE**

This skill documents critical parser conventions that prevent token position bugs (the #1 time sink in parser development).

**Time savings: ~30%** by avoiding common pitfalls

**Key conventions:**
1. Parser leaves cursor AT last token (not after)
2. Lexer never generates NEWLINE tokens
3. Use `DEBUG_PARSER=1` for token tracing
4. Use `make doc PKG=<package>` for API discovery

## When to Use This Skill

Invoke this skill when:
- User wants to modify the AILANG parser
- User asks about parser architecture or conventions
- User is debugging parser issues
- User needs to understand token positioning
- User wants to add new syntax to AILANG
- User asks "how do I parse...?"

## Critical Convention: Token Position

**CRITICAL:** AILANG parser functions follow this convention:
- **Input:** Parser is AT the first token to parse
- **Output:** Parser is AT the last token of what was parsed (NOT after it)

**Example:**
```go
// To parse "42" followed by a comma:
p.nextToken() // move to 42
expr := p.parseExpression(LOWEST)  // parses "42", leaves cur=42 (NOT comma!)
p.nextToken() // NOW we're at comma ✓
```

**Functions following this convention:**
- `parseExpression()` - Leaves parser AT the last token of the expression
- `parseType()` - Leaves parser AT the last token of the type
- `parsePattern()` - Leaves parser AT the last token of the pattern
- Most parser functions follow this pattern

**When writing new parser functions:**
- ✅ ALWAYS call `p.nextToken()` AFTER calling these functions
- ❌ DON'T call `p.nextToken()` BEFORE - the caller handles positioning
- ✅ Document your function if it deviates from this convention

**See:** [resources/token_positioning.md](resources/token_positioning.md) for detailed examples

## Available Scripts

### `scripts/trace_parser.sh <file.ail>`
Run parser with DEBUG_PARSER=1 to trace token positions.

**Usage:**
```bash
.claude/skills/parser-developer/scripts/trace_parser.sh test.ail
```

**Output:**
```
[ENTER parseExpression] cur=INT(42) peek=COMMA
[EXIT parseExpression] cur=INT(42) peek=COMMA
```

### `scripts/check_ast_types.sh`
List all AST node types in the codebase.

**Usage:**
```bash
.claude/skills/parser-developer/scripts/check_ast_types.sh
```

### `scripts/find_api.sh <package> <symbol>`
Quick API discovery using make doc.

**Usage:**
```bash
.claude/skills/parser-developer/scripts/find_api.sh internal/parser New
```

## Common AST Types

**Quick type lookup:**
```bash
grep "^type.*struct" internal/ast/ast.go | head -20
```

**Expression types:**
- **Literals**: `ast.Literal` with `Kind` field
  - ⚠️ **GOTCHA**: Lexer returns `int64`, not `int` for IntLit
  - ✅ Access: `lit.Value.(int64)`
  - ❌ Wrong: `lit.Value.(int)` (will panic!)
- **Lists**: `ast.List` with `Elements []Expr`
- **Variables**: `ast.Variable` with `Name string`
- **Function calls**: `ast.FuncCall` with `Func Expr, Args []Expr`
- **Lambdas**: `ast.Lambda` with `Params []*ast.Param, Body Expr`
- **Blocks**: `ast.Block` with `Exprs []Expr`

**Type types:**
- **Simple types**: `ast.SimpleType` with `Name string`
- **List types**: `ast.ListType` with `Element Type`
- **Function types**: `ast.FuncType` with `Params []Type, Return Type, Effects *ast.EffectRow`
- **Type applications**: `ast.TypeApp` with `Con string, Args []Type`

**Pattern types:**
- **Variable pattern**: `ast.VarPattern` with `Name string`
- **Constructor pattern**: `ast.ConstructorPattern` with `Name string, Args []Pattern`
- **Literal pattern**: `ast.LiteralPattern` with `Value Literal`
- **Wildcard pattern**: `ast.WildcardPattern` (matches anything)

**See:** [resources/ast_quick_reference.md](resources/ast_quick_reference.md) for complete listing

## Quick Token Lookup

**Check if a keyword exists:**
```bash
grep -i "forall" internal/lexer/token.go
# Output: FORALL token exists!
```

**Common testing keywords (already in lexer):**
- `FORALL`, `EXISTS` - Quantifiers
- `TEST`, `TESTS` - Test blocks
- `PROPERTY`, `PROPERTIES` - Property-based tests
- `ASSERT` - Assertions

**If you see an identifier instead of a keyword:**
- ✅ Use `lexer.FORALL`, not `lexer.IDENT + literal check`
- ❌ Wrong: `p.curTokenIs(lexer.IDENT) && p.curToken.Literal == "forall"`
- ✅ Right: `p.curTokenIs(lexer.FORALL)`

## Debug Mode

**Enable token position tracing:**
```bash
DEBUG_PARSER=1 ailang run test.ail
```

**Output example:**
```
[ENTER parseType] cur=IDENT(int) peek=,
[EXIT parseType] cur=IDENT(int) peek=,
[ENTER parseExpression] cur=IDENT(x) peek=+
[EXIT parseExpression] cur=IDENT(x) peek=+
```

**How it works:**
- Shows ENTER/EXIT for key parser functions
- Displays current (`cur`) and next (`peek`) tokens
- Only logs when `DEBUG_PARSER=1` is set (zero overhead otherwise)
- Output goes to stderr

**See:** [resources/debug_mode.md](resources/debug_mode.md) for troubleshooting guide

## Common Patterns

### Pattern 1: Parsing Optional Sections

**Pattern for parsing optional sections:**

```go
// properties can be in PEEK (no tests) or CUR (after tests)
if p.peekTokenIs(lexer.PROPERTIES) || p.curTokenIs(lexer.PROPERTIES) {
    // If in peek, advance to it
    if p.peekTokenIs(lexer.PROPERTIES) {
        p.nextToken()
    }
    // Now always at PROPERTIES
    properties := p.parsePropertiesBlock()
}
```

**Why:** Previous optional section may or may not advance the parser, so check both positions.

### Pattern 2: Test Error Printing

**❌ WRONG - Errors are hidden:**
```go
if len(p.Errors()) != 0 {
    t.Fatalf("parser had %d errors:", len(p.Errors()))
    // ⚠️ This never executes! t.Fatalf stops immediately
    for _, err := range p.Errors() {
        t.Errorf("  %s", err)
    }
}
```

**✅ CORRECT - Errors are visible:**
```go
if len(p.Errors()) != 0 {
    // Print errors BEFORE Fatalf
    for _, err := range p.Errors() {
        t.Errorf("  %s", err)
    }
    t.Fatalf("parser had %d errors", len(p.Errors()))
}
```

### Pattern 3: String Formatting

**⚠️ CRITICAL: `string(rune(i))` produces unprintable characters!**

```go
// ❌ WRONG - Produces "\x01" instead of "1"
testName := "test_" + string(rune(i+1))  // BUG!

// ✅ CORRECT - Use fmt.Sprintf or strconv
testName := fmt.Sprintf("test_%d", i+1)
testName := "test_" + strconv.Itoa(i+1)
```

**Why**: `rune(1)` is Unicode U+0001 (unprintable), not "1" (U+0031).

**See:** [resources/common_patterns.md](resources/common_patterns.md) for more patterns

## API Discovery Workflow

**When you need to know an API:**

### 1. Check `make doc` (fastest - 30 seconds)

```bash
make doc PKG=internal/parser | grep "parseExpression"
make doc PKG=internal/testing | grep "NewCollector"
```

### 2. Check source files (if you know the file)

```bash
grep "^func New" internal/testing/collector.go
grep "^type.*struct" internal/ast/ast.go
```

### 3. Check test files (shows real usage)

```bash
grep "NewCollector" internal/testing/*_test.go
```

### 4. Check docs/guides/ (for complex workflows)

- [docs/guides/parser_development.md](../../../docs/guides/parser_development.md)
- [docs/CONTRIBUTING.md](../../../docs/CONTRIBUTING.md)

**Time savings:**
- **Before `make doc`**: ~5-10 min per API lookup
- **After `make doc`**: ~30 sec per API lookup
- **Improvement**: ~80% reduction

**See:** [resources/api_discovery.md](resources/api_discovery.md) for constructor tables

## Common Constructors

**Quick reference:**

| Package | Constructor | Signature | Notes |
|---------|-------------|-----------|-------|
| `internal/parser` | `New(lexer)` | Takes lexer instance | Parser |
| `internal/elaborate` | `NewElaborator()` | No arguments | Surface → Core |
| `internal/types` | `NewTypeChecker(core, imports)` | Takes Core prog + imports | Type inference |
| `internal/link` | `NewLinker()` | No arguments | Dictionary linking |
| `internal/testing` | `NewCollector(path string)` | Takes module path | M-TESTING |
| `internal/eval` | `NewEvaluator(ctx)` | Takes EffContext | Core evaluator |

**See:** [resources/api_discovery.md](resources/api_discovery.md) for complete reference

## Pipeline Sequence

**Typical compilation pipeline:**

```go
// Step 1: Parse
l := lexer.New(input, "test.ail")
p := parser.New(l)
file := p.ParseFile()

// Step 2: Elaborate (Surface → Core)
elab := elaborate.NewElaborator()  // ⚠️ No arguments!
coreProg, err := elab.Elaborate(file)

// Step 3: Type check
tc := types.NewTypeChecker(coreProg, nil)  // nil = no imports
typedProg, err := tc.Check()

// Step 4: Link dictionaries
linker := link.NewLinker()
linkedProg, err := linker.Link(typedProg, tc.CoreTI)
```

## Common Field Gotchas

**Use `make doc` to discover struct fields:**

```bash
make doc PKG=internal/ast | grep -A 20 "type FuncDecl"
```

**Common mistakes:**
```go
// ✅ CORRECT
funcDecl.Tests           // []*ast.TestCase (not .Tests.Cases!)
funcDecl.Properties      // []*ast.Property
funcDecl.Params          // []*ast.Param

// ❌ WRONG (fields that don't exist)
funcDecl.InlineTests     // Use .Tests
funcDecl.Tests.Cases     // .Tests is already the slice
```

## Resources

### Detailed Guides

**Token positioning:**
- [resources/token_positioning.md](resources/token_positioning.md) - Detailed examples and edge cases

**AST types:**
- [resources/ast_quick_reference.md](resources/ast_quick_reference.md) - Complete AST node listing

**Common patterns:**
- [resources/common_patterns.md](resources/common_patterns.md) - Parser patterns and anti-patterns

**API discovery:**
- [resources/api_discovery.md](resources/api_discovery.md) - Constructor tables and field reference

**Debug mode:**
- [resources/debug_mode.md](resources/debug_mode.md) - Troubleshooting guide

### Architecture Docs

- **Parser design**: `design_docs/planned/v0_3_15/m-dx9-parser-developer-experience.md`
- **Contributing**: `docs/CONTRIBUTING.md`
- **Lexer/Parser**: `internal/lexer/`, `internal/parser/`

## Critical Warnings

### 1. Lexer Never Generates NEWLINE Tokens

The lexer skips `\n` as whitespace. Even though `lexer.NEWLINE` exists, it's never generated!

**❌ WRONG:**
```go
if p.curTokenIs(lexer.NEWLINE) {  // This is NEVER true!
    ...
}
```

**✅ CORRECT:**
```go
// After RPAREN of Leaf(int), next token is PIPE (not NEWLINE)
if p.curTokenIs(lexer.PIPE) {
    ...
}
```

Multi-line syntax "just works" because the lexer handles it.

### 2. IntLit is int64, not int

```go
// ❌ WRONG - Will panic!
value := lit.Value.(int)

// ✅ CORRECT
value := lit.Value.(int64)
```

### 3. Always Print Errors Before t.Fatalf

`t.Fatalf` stops execution immediately, so print errors first!

## Progressive Disclosure

This skill loads information progressively:

1. **Always loaded**: This SKILL.md file (conventions overview)
2. **Execute as needed**: Scripts in `scripts/` (tracing, API discovery)
3. **Load on demand**: Detailed guides in `resources/`

## Notes

- Parser functions leave cursor AT last token, not after
- Lexer never generates NEWLINE tokens - it skips them
- Use `DEBUG_PARSER=1` for token tracing
- Use `make doc PKG=<package>` for API discovery (80% faster)
- IntLit values are `int64`, not `int`
- Print errors before `t.Fatalf` in tests
