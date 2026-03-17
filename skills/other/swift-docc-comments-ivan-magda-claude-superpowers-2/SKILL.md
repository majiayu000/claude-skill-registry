---
name: swift-docc-comments
description: Use when writing or enhancing Swift documentation comments for DocC generation, adding inline doc comments to Swift source files, or when user asks for API documentation
allowed-tools: Read, Grep, Glob
---

# Swift DocC Inline Comments

## Overview

Swift DocC inline comments follow a specific structure. Section headers like `## Overview` and `## Topics` belong in `.docc` catalog files, NOT in inline source comments.

## Structure

````
/// Summary (first paragraph - one sentence)
///
/// Discussion paragraphs (no header needed)
///
/// ```swift
/// // Code example
/// ```
///
/// - Parameter name: Description
/// - Returns: Description
/// - Throws: Description
/// - Note: Additional info
````

## Quick Reference

| Element       | Format                | Location                  |
| ------------- | --------------------- | ------------------------- |
| Summary       | First paragraph       | Inline                    |
| Discussion    | Subsequent paragraphs | Inline                    |
| Code examples | Triple backticks      | Inline, before parameters |
| `## Overview` | Section header        | `.docc` catalog ONLY      |
| `## Topics`   | Section header        | `.docc` catalog ONLY      |
| Symbol links  | ` ``SymbolName`` `    | Both                      |

## Correct Format

````swift
/// Brief summary in one sentence.
///
/// Extended discussion explaining behavior, use cases,
/// or important details. No header needed.
///
/// ```swift
/// let example = MyType()
/// example.doSomething()
/// ```
///
/// - Parameter value: What this parameter does.
/// - Returns: What gets returned.
/// - Note: Default value is `.default`.
func method(value: Int) -> String
````

## Common Mistakes

| Wrong                  | Correct                     |
| ---------------------- | --------------------------- |
| `/// ## Overview`      | Just write paragraphs       |
| `/// ## Topics`        | Use `.docc` catalog file    |
| `/// ## Example`       | Just use code block         |
| Parameters before code | Code block, then parameters |

## Red Flags

These indicate wrong format:

- `## Overview` in `///` comments
- `## Topics` in `///` comments
- `## Example` before code blocks
- `- Parameter:` appearing before code examples

## Generate Documentation

```bash
swift package generate-documentation
```
