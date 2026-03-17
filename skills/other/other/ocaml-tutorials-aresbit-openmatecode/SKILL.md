---
name: ocaml-tutorials
description: Creating OCaml library tutorials using .mld documentation format with MDX executable examples. Use when discussing tutorials, documentation, .mld files, MDX, or interactive documentation.
license: ISC
---

# OCaml Tutorial Creation

## When to Use This Skill

Invoke this skill when:
- Creating tutorials for OCaml libraries
- Working with .mld documentation format
- Setting up MDX for executable examples
- Discussing interactive documentation

## Overview

OCaml tutorials should:
- Introduce concepts gently
- Use executable code examples via MDX
- Progress from simple to complex
- Include practical patterns and use cases

## File Structure

### Required Components

1. **doc/ directory** in project root
2. **tutorial.mld** - Main tutorial content
3. **index.mld** - Documentation index
4. **dune** - Build rules

### doc/dune Configuration

```dune
(mdx
 (files tutorial.mld)
 (libraries your_library_name))

(documentation
 (package your_package_name)
 (mld_files index tutorial))
```

### dune-project Updates

Enable MDX:

```dune
(using mdx 0.4)
```

Add MDX as doc dependency:

```dune
(package
 (name your_package)
 (depends
  ...
  (mdx :with-doc)
  (odoc :with-doc)))
```

## .mld Format

### Document Structure

```
{0 Topic Name Tutorial}

Introduction text.

{1 Section Title}

Section content.

{2 Subsection Title}

Subsection content.
```

### Executable Code Blocks

Use `{@ocaml[...]}` for executable examples:

```
{@ocaml[
# let x = 1 + 1;;
val x : int = 2
]}
```

- Lines starting with `#` are input
- Following lines are expected output
- MDX verifies output at build time
- Use `;;` to terminate expressions

### Non-Executable Code

Use `{v ... v}` for verbatim blocks:

```
{v
name: Alice
age: 30
v}
```

### Cross-References

```
{!Library.function_name}          - Function reference
{!Library.Module.type_name}       - Type reference
{{!Library}API reference}         - Link with custom text
```

### Lists

```
{ul
{- Item one}
{- Item two}
}

{ol
{- First item}
{- Second item}
}
```

### Formatting

```
{b bold text}
{i italic text}
```

## Tutorial Content Guidelines

### Structure

1. **Setup** - How to load the library
2. **Basic Usage** - Simplest examples
3. **Core Concepts** - Main types and functions
4. **Common Patterns** - Real-world usage
5. **Advanced Features** - Complex functionality
6. **Error Handling** - How errors work
7. **Summary** - Quick reference

### Setup Section

```
{1 Setup}

{@ocaml[
# #require "library_name";;
# open Library;;
]}
```

### Best Practices

1. **Show output** - Include expected output in examples
2. **Use consistent naming** - Variables carry through examples
3. **Build complexity gradually** - Each example builds on previous
4. **Explain the "why"** - Not just syntax, but when to use features
5. **Reference documentation** - Link to API docs

## Verification

```bash
dune build @check    # Verify syntax
dune build @doc      # Build documentation
dune runtest         # Run MDX tests (if configured)
```

## Common Issues

### Unresolved References
Use fully qualified names: `{!Library.of_string}` not `{!of_string}`

### MDX Not Found
Enable in dune-project: `(using mdx 0.4)`

### Output Mismatch
Run code manually, update expected output. Use `<abstr>` for abstract values.
