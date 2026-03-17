---
name: refactor-ts
description: Guides TypeScript refactoring operations including moving files, moving symbols between files, and renaming symbols across the codebase. Use when user wants to reorganize code structure.
---

# TypeScript Refactoring Skill

This skill guides the use of the `refactor-ts` CLI tool for common TypeScript code reorganization tasks.

## When to Use

- User wants to move a TypeScript file to a new location
- User wants to extract a symbol (class, function, interface, etc.) to a different file
- User wants to rename a symbol across the entire codebase
- User is reorganizing code structure and needs import updates handled automatically

## Available Operations

### 1. Move File (`refactor-ts move-file`)

Moves a TypeScript file to a new location and updates all import references.

```bash
npx refactor-ts move-file <source> <destination>
```

**Example:**
```bash
npx refactor-ts move-file src/game/Player.ts src/game/entities/Player.ts
```

### 2. Move Symbol (`refactor-ts move-symbol`)

Moves a symbol from one file to another, updating imports and copying dependencies.

```bash
npx refactor-ts move-symbol <file> <symbol> <destination>
```

**Supported symbols:** classes, functions, variables, interfaces, enums, type aliases

**Example:**
```bash
npx refactor-ts move-symbol src/game/Player.ts PlayerState src/game/state/PlayerState.ts
```

### 3. Rename Symbol (`refactor-ts move-symbol`)

Renames a symbol and updates all references across the codebase. This uses the same `move-symbol` command - when the destination is a name rather than a file path, it performs a rename.

```bash
npx refactor-ts move-symbol <file> <oldName> <newName>
```

**Supported symbols:** classes, functions, variables, interfaces, enums, type aliases

**Example:**
```bash
npx refactor-ts move-symbol src/game/Player.ts Player GamePlayer
```

## Process

1. **Identify the operation type** based on what the user wants to do
2. **Determine the arguments** needed for the command
3. **Run the appropriate command** with the correct arguments
4. **Verify the changes** by checking that TypeScript compiles without errors

## Common Patterns

- **Extracting a class to its own file:** Use `move-symbol` to move the class, which will create the destination file if needed
- **Reorganizing into subdirectories:** Use `move-file` to relocate files while keeping imports valid
- **Renaming for consistency:** Use `move-symbol` with a new name (not a file path) to rename throughout the codebase
