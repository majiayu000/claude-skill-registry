---
name: codebase-layout
description: Codebase organization for pikru. Use when you need to find where specific functionality lives.
---

# Pikru Codebase Organization

## Top-Level Structure

- `src/` - Main pikru library (parsing and rendering)
- `crates/` - Supporting crates
- `vendor/pikchr-c/` - Original C implementation and test files
- `examples/` - Example programs
- `tests/` - Integration tests

## Main Library (`src/`)

### Entry Point
- `src/lib.rs` - Public API, exports key types and functions

### Parsing
- `src/parse.rs` - **Parser implementation** (statement parsing, token handling)
- `src/ast.rs` - **AST types** (Statement, Expr, ObjectClass, etc.)
- `src/types.rs` - **Core types** (ClassName, Direction, EdgePoint, etc.)

### Rendering
- `src/render/mod.rs` - **Main renderer logic**
  - Object placement and geometry
  - Text positioning (**ljust/rjust logic at lines 1265-1550**)
  - Variable scope and context management
- `src/render/eval.rs` - **Expression evaluation** (positions, scalars, variables)
- `src/render/svg.rs` - **SVG generation** (converts shapes to SVG elements)
- `src/render/geometry.rs` - **Shape geometry** (boxes, circles, paths, files)
- `src/render/shapes.rs` - **Shape rendering** (specific shape implementations)
- `src/render/types.rs` - **Render types** (PObject, Style, PositionedText, etc.)
- `src/render/path_builder.rs` - **Path construction** (line/arrow building)
- `src/render/context.rs` - **Render context** (variable scopes, state)
- `src/render/defaults.rs` - **Default values** (line width, font size, etc.)

### Error Handling
- `src/errors.rs` - Error types and reporting
- `src/macros.rs` - Helper macros

## Supporting Crates

### `crates/pikru-compare/`
**SVG comparison utilities for testing**
- `src/lib.rs` - Core comparison logic
  - `compare_outputs()` - **Main comparison function**
  - `CompareResult::is_match()` - Determines if test passes
  - Handles error matching, SVG parsing, tolerance
- Used by: test harness, MCP server

### `crates/pikru-mcp/`
**MCP server for test running**
- `src/tools.rs` - MCP tool implementations
  - `run_pikru_test()` - Run single test, returns comparison
  - `list_pikru_tests()` - List available tests
  - `debug_pikru_test()` - Run with trace output
- `src/main.rs` - MCP server entry point

## Test Files

### Location
`vendor/pikchr-c/tests/*.pikchr` - Test input files from C implementation

### Categories
- `test01`-`test81` - Numbered feature tests
- `autochop*.pikchr` - Arrow chopping tests
- Other specialized tests

## Common Debugging Paths

### Text Positioning Issues
1. Check `src/render/mod.rs:1265-1550` - ljust/rjust calculation
2. Check `src/render/svg.rs:294` - Text anchor assignment
3. Check `src/render/types.rs` - PositionedText structure

### Rendering Issues
1. Check `src/render/shapes.rs` - Shape-specific rendering
2. Check `src/render/geometry.rs` - Geometric calculations
3. Check `src/render/svg.rs` - SVG element generation

### Parsing Issues
1. Check `src/parse.rs` - Parser logic
2. Check `src/ast.rs` - AST node definitions

### Test Comparison Issues
1. Check `crates/pikru-compare/src/lib.rs` - Comparison logic
2. Check tolerance constants (FLOAT_TOLERANCE, SIMILARITY_THRESHOLD)

## Key Code References (cref comments)

Many functions include `// cref:` comments pointing to the original C implementation:
- Format: `// cref: function_name (pikchr.c:line_number)`
- Use these to cross-reference with C implementation when debugging
