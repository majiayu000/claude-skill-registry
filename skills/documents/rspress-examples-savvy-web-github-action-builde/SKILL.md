---
name: rspress-examples
description: Generate Twoslash code examples for RSPress documentation. Use when
  adding type-rich, interactive code examples to documentation pages.
allowed-tools: Read, Glob, Grep, Edit, Write
context: fork
agent: rspress-doc-agent
---

# Generate Twoslash Code Examples

Generates type-rich Twoslash code examples for RSPress documentation pages.

## Overview

This skill creates complete, compilable TypeScript code examples with:

1. Full type checking via Twoslash
2. Auto-loaded dependencies from package.json
3. Progressive complexity (basic → advanced)
4. Cut notations to hide boilerplate
5. Proper imports and complete programs

## Quick Start

**Generate basic usage example:**

```bash
/rspress-examples effect-type-registry --api=TypeRegistry --scenario=basic
```

**Generate advanced example:**

```bash
/rspress-examples rspress-plugin-api-extractor --api=PluginConfig --scenario=advanced
```

**Generate error handling example:**

```bash
/rspress-examples website --api=BlogPost --scenario=error-handling
```

## How It Works

### 1. Parse Parameters

- `module`: Module name from design.config.json [REQUIRED]
- `--api`: API item to demonstrate (class, function, interface) [REQUIRED]
- `--scenario`: Example scenario (basic, advanced, error-handling, integration)
  [REQUIRED]
- `--output`: Output file path (optional)
- `--dry-run`: Preview without writing (optional)

### 2. Load Configuration

Reads `design.config.json` to find module configuration.

Reads `rspress.config.ts` to determine:

- Available dependencies (autoDetectDependencies)
- Package name and version
- Existing examples structure

### 3. Read API Documentation

Finds API documentation for the specified item:

- Reads auto-generated API docs
- Extracts signatures, types, parameters
- Identifies related types and interfaces

### 4. Generate Example Code

Creates complete TypeScript program:

**Basic Scenario:**

- Minimal working example
- Core functionality demonstrated
- Simple, clear code

**Advanced Scenario:**

- Complex configuration
- Multiple features combined
- Realistic use case

**Error Handling Scenario:**

- Try-catch blocks
- Error type handling
- Recovery strategies

**Integration Scenario:**

- Multiple APIs working together
- Real-world workflow
- Complete solution

### 5. Add Twoslash Annotations

Enhances code with Twoslash features:

- Hover comments for type inference
- Error annotations for expected errors
- Cut notations to hide boilerplate
- Meta tags for special rendering

### 6. Validate Compilation

Ensures code compiles:

- All imports resolve
- Types are correct
- No compilation errors
- Twoslash annotations work

### 7. Insert into Documentation

Updates or creates documentation page:

- Adds example to existing page
- Creates new example page if needed
- Updates navigation metadata
- Adds cross-references

## Code Block Structure

All generated examples follow this pattern:

````markdown
```typescript twoslash vfs
import { API } from "module-name";

// Additional imports as needed

// ---cut-before---
// Boilerplate hidden from users

// Main example code visible to users

// ---cut-after---
// Verification code hidden from users
```
````

## Supporting Documentation

- `instructions.md` - Detailed generation process
- `examples.md` - Sample outputs for each scenario

## Success Criteria

- ✅ Code compiles without errors
- ✅ All imports are explicit
- ✅ Example demonstrates intended use case
- ✅ Twoslash annotations work
- ✅ Code is properly formatted

## Integration Points

- Uses `.claude/design/design.config.json`
- Reads `rspress.config.ts` for dependencies
- Reads API docs from `{siteDocs}/api/`
- Updates documentation pages

## Related Skills

- `/rspress-guide` - Generate learning guides
- `/rspress-page` - Scaffold RSPress pages
- `/rspress-review` - Review code examples
- `/rspress-nav` - Update navigation
