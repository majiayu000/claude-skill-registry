---
name: refactor-ts
description: Guides TypeScript refactoring operations including moving files, moving symbols between files, and renaming symbols across the codebase. Use when user wants to reorganize code structure.
---

# TypeScript Refactoring Skill

This skill guides the use of three TypeScript refactoring tools that automate common code reorganization tasks using ts-morph.

## When to Use

- User wants to move a TypeScript file to a new location
- User wants to extract a symbol (class, function, interface, etc.) to a different file
- User wants to rename a symbol across the entire codebase
- User is reorganizing code structure and needs import updates handled automatically

## Available Operations

### 1. Move File (`npm run move-file`)

Moves a TypeScript file to a new location and updates all import references.

```bash
npm run move-file <source> <destination>
```

**Example:**
```bash
npm run move-file src/game/Player.ts src/game/entities/Player.ts
```

### 2. Move Symbol (`npm run move-symbol`)

Moves a symbol from one file to another, updating imports and copying dependencies.

```bash
npm run move-symbol <sourceFile> <symbolName> <destinationFile>
```

**Supported symbols:** classes, functions, variables, interfaces, enums, type aliases

**Example:**
```bash
npm run move-symbol src/game/Player.ts PlayerState src/game/state/PlayerState.ts
```

### 3. Rename Symbol (`npm run rename-symbol`)

Renames a symbol and updates all references across the codebase.

```bash
npm run rename-symbol <file> <oldName> <newName>
```

**Supported symbols:** classes, functions, variables, interfaces, enums, type aliases

**Example:**
```bash
npm run rename-symbol src/game/Player.ts Player GamePlayer
```

## Process

1. **Identify the operation type** based on what the user wants to do
2. **Determine the arguments** needed for the command
3. **Run the appropriate npm script** with the correct arguments
4. **Verify the changes** by checking that TypeScript compiles without errors

## Common Patterns

- **Extracting a class to its own file:** Use `move-symbol` to move the class, which will create the destination file if needed
- **Reorganizing into subdirectories:** Use `move-file` to relocate files while keeping imports valid
- **Renaming for consistency:** Use `rename-symbol` to update names throughout the codebase
