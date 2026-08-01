---
name: unity-csharp-editing
description: 'Supports Unity C# script editing, searching, and refactoring. Enables
  TDD cycle code editing, symbol navigation, reference searching, and structured editing.
  Use when: C# editing, script search, symbo'
---

---
name: unity-csharp-editing
description: Supports Unity C# script editing, searching, and refactoring. Enables TDD cycle code editing, symbol navigation, reference searching, and structured editing. Use when: C# editing, script search, symbol search, refactoring, code indexing, class creation, method addition
allowed-tools: Read, Grep, Glob
---

# Unity C# Script Editing

A guide for efficient editing, searching, and refactoring of Unity C# scripts.

## Quick Start

### 1. Initialize Code Index

On first use or when the index is outdated, build the index first:

```javascript
// Check index status
mcp__unity-mcp-server__get_index_status()

// Build index (first time only, may take a few minutes)
mcp__unity-mcp-server__build_index()
```

### 2. Basic Reading Flow

```javascript
// Get symbol list in file
mcp__unity-mcp-server__get_symbols({
  path: "Assets/Scripts/Player.cs"
})

// Get specific symbol details
mcp__unity-mcp-server__find_symbol({
  name: "PlayerController",
  kind: "class",
  exact: true
})

// Read code
mcp__unity-mcp-server__read({
  path: "Assets/Scripts/Player.cs",
  startLine: 10,
  endLine: 50
})
```

### 3. Basic Editing Flow

```javascript
// Small changes (within 80 characters) → snippet
mcp__unity-mcp-server__edit_snippet({
  path: "Assets/Scripts/Player.cs",
  instructions: [{
    operation: "replace",
    anchor: { type: "text", target: "if (health < 0)" },
    newText: "if (health <= 0)"
  }]
})

// Large changes (method body) → structured
mcp__unity-mcp-server__edit_structured({
  path: "Assets/Scripts/Player.cs",
  symbolName: "PlayerController/TakeDamage",
  operation: "replace_body",
  newText: "{\n    health -= damage;\n    OnDamaged?.Invoke(damage);\n}"
})
```

## Core Concepts

### Code Index

unity-mcp-server provides a code index via built-in C# LSP. Output is **5x more compact** than standard tools, optimizing LLM context.

| Tool | Purpose | Comparison |
|------|---------|------------|
| `find_symbol` | Symbol search | 5x smaller output |
| `find_refs` | Reference search | 3x smaller output |
| `search` | Code search | Instant response |

### namePath (Symbol Path)

Symbols are identified by hierarchical path within file:

```
// Simple class
PlayerController

// Nested member
PlayerController/TakeDamage
PlayerController/health

// Deep nesting
OuterClass/InnerClass/Method
```

### Scope Specification

Narrow search scope for better performance:

- `assets` - Assets/ only
- `packages` - Packages/ only
- `embedded` - Embedded packages only
- `all` - All scope (default)

## Tool Selection Guide

### 80-Character Rule

**The criterion for choosing an editing tool is "whether the diff is within 80 characters"**

#### When to use `edit_snippet`

**Condition**: Diff within 80 characters, 1-2 line changes

```javascript
// ✅ Remove null guard
{ operation: "delete", anchor: { type: "text", target: "if (x == null) return;\n" }}

// ✅ Minor condition fix
{ operation: "replace", anchor: { type: "text", target: "if (x > 10)" }, newText: "if (x > 20)" }

// ✅ Insert log statement
{ operation: "insert", anchor: { type: "text", target: "Process();\n" }, newText: "Debug.Log(\"Processing\");\n" }
```

#### When to use `edit_structured`

**Condition**: Method body replacement, class member addition

```javascript
// ✅ Replace method body
{
  symbolName: "Player/Move",
  operation: "replace_body",
  newText: "{\n    transform.position += direction * speed * Time.deltaTime;\n}"
}

// ✅ Add member to class
{
  symbolName: "Player",
  operation: "insert_after",
  newText: "\n    private float _jumpForce = 5f;\n"
}
```

### Decision Flowchart

```
Is the change within 80 characters?
├─ YES → edit_snippet
└─ NO → Is it entire method/property replacement?
         ├─ YES → edit_structured (replace_body)
         └─ NO → Is it adding to class?
                  ├─ YES → edit_structured (insert_after)
                  └─ NO → Split into multiple snippets
```

## Common Workflows

### TDD Cycle (RED-GREEN-REFACTOR)

#### 1. RED: Write the test

```javascript
// Create test file
mcp__unity-mcp-server__create_class({
  path: "Assets/Tests/PlayerTests.cs",
  className: "PlayerTests",
  namespace: "Tests",
  usings: "NUnit.Framework,UnityEngine"
})

// Add test method
mcp__unity-mcp-server__edit_structured({
  path: "Assets/Tests/PlayerTests.cs",
  symbolName: "PlayerTests",
  operation: "insert_after",
  newText: `
    [Test]
    public void TakeDamage_ReducesHealth()
    {
        var player = new Player(100);
        player.TakeDamage(30);
        Assert.AreEqual(70, player.Health);
    }
`
})
```

#### 2. GREEN: Minimal implementation

```javascript
// Add implementation
mcp__unity-mcp-server__edit_structured({
  path: "Assets/Scripts/Player.cs",
  symbolName: "Player",
  operation: "insert_after",
  newText: `
    public void TakeDamage(int damage)
    {
        Health -= damage;
    }
`
})
```

#### 3. REFACTOR: Improve code

```javascript
// Check compilation state
mcp__unity-mcp-server__get_compilation_state({ includeMessages: true })

// Check impact before refactoring
mcp__unity-mcp-server__find_refs({
  name: "TakeDamage",
  container: "Player"
})
```

### Create New Class

```javascript
// 1. Create class file
mcp__unity-mcp-server__create_class({
  path: "Assets/Scripts/Enemies/Enemy.cs",
  className: "Enemy",
  namespace: "Game.Enemies",
  baseType: "MonoBehaviour",
  usings: "UnityEngine,System"
})

// 2. Add fields and methods
mcp__unity-mcp-server__edit_structured({
  path: "Assets/Scripts/Enemies/Enemy.cs",
  symbolName: "Enemy",
  operation: "insert_after",
  newText: `
    [SerializeField] private int _health = 100;
    [SerializeField] private float _speed = 3f;

    public int Health => _health;

    public void TakeDamage(int damage)
    {
        _health = Mathf.Max(0, _health - damage);
        if (_health == 0) Die();
    }

    private void Die()
    {
        Destroy(gameObject);
    }
`
})

// 3. Update index
mcp__unity-mcp-server__update_index({
  paths: ["Assets/Scripts/Enemies/Enemy.cs"]
})
```

### Refactoring (Symbol Rename)

```javascript
// 1. Check impact
mcp__unity-mcp-server__find_refs({
  name: "oldMethodName",
  container: "ClassName",
  scope: "all"
})

// 2. Execute rename (applies to entire project)
mcp__unity-mcp-server__rename_symbol({
  relative: "Assets/Scripts/Player.cs",
  namePath: "Player/oldMethodName",
  newName: "newMethodName",
  preview: true  // Preview first
})

// 3. Apply if no issues
mcp__unity-mcp-server__rename_symbol({
  relative: "Assets/Scripts/Player.cs",
  namePath: "Player/oldMethodName",
  newName: "newMethodName",
  preview: false
})
```

### Code Search

```javascript
// Pattern search (regex)
mcp__unity-mcp-server__search({
  pattern: "GetComponent<.*>",
  patternType: "regex",
  scope: "assets",
  returnMode: "snippets",
  snippetContext: 2
})

// Search usages of specific class
mcp__unity-mcp-server__find_refs({
  name: "PlayerController",
  kind: "class",
  scope: "all"
})
```

## Advanced Patterns

### Batch Editing (Multiple locations at once)

```javascript
// Edit up to 10 locations at once
mcp__unity-mcp-server__edit_snippet({
  path: "Assets/Scripts/GameManager.cs",
  instructions: [
    { operation: "replace", anchor: { type: "text", target: "Debug.Log" }, newText: "Logger.Info" },
    { operation: "delete", anchor: { type: "text", target: "// TODO: remove\n" }},
    { operation: "insert", anchor: { type: "text", target: "void Start()\n    {" }, newText: "\n        Initialize();" }
  ]
})
```

### Preview Mode

For large or uncertain edits, verify with preview first:

```javascript
// Validate in preview mode
mcp__unity-mcp-server__edit_structured({
  path: "Assets/Scripts/Player.cs",
  symbolName: "Player/Update",
  operation: "replace_body",
  newText: "{ /* new implementation */ }",
  preview: true  // Don't write to file
})

// Apply if no LSP diagnostic errors
mcp__unity-mcp-server__edit_structured({
  // Same parameters with preview: false
})
```

### Symbol Removal

```javascript
// Confirm no references
mcp__unity-mcp-server__find_refs({
  name: "UnusedMethod",
  container: "Player"
})

// Remove if no references
mcp__unity-mcp-server__remove_symbol({
  path: "Assets/Scripts/Player.cs",
  namePath: "Player/UnusedMethod",
  failOnReferences: true,  // Error if referenced
  apply: true
})
```

## Common Mistakes

### 1. Anchor Mismatch

**Problem**: `anchor_not_found` error

```javascript
// ❌ Incorrect whitespace/newlines
anchor: { type: "text", target: "if(x>10)" }

// ✅ Exact match with actual code
anchor: { type: "text", target: "if (x > 10)" }
```

**Solution**: Use `read` to check file contents, copy exact string including whitespace/newlines

### 2. 80-Character Limit Exceeded

**Problem**: `diff exceeds 80 characters` error

```javascript
// ❌ Editing long code with snippet
{ operation: "replace", anchor: {...}, newText: "very long code..." }

// ✅ Use structured for method body replacement
{ symbolName: "Class/Method", operation: "replace_body", newText: "..." }
```

### 3. Code Index Not Built

**Problem**: LSP timeout (60 seconds)

```javascript
// ✅ Always check index status
mcp__unity-mcp-server__get_index_status()

// Build if coverage is low
mcp__unity-mcp-server__build_index()
```

### 4. Multiple Matches

**Problem**: `anchor_not_unique` error

```javascript
// ❌ Anchor too generic
anchor: { type: "text", target: "return;" }

// ✅ Include context for uniqueness
anchor: { type: "text", target: "        return health;\n    }" }
```

### 5. Index Not Updated After Edit

**Problem**: Outdated symbol information returned after editing

```javascript
// ✅ Always update index after editing
mcp__unity-mcp-server__update_index({
  paths: ["Assets/Scripts/Player.cs"]
})
```

## Tool Reference

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `get_symbols` | File symbol list | path |
| `find_symbol` | Symbol search | name, kind, scope, exact |
| `find_refs` | Reference search | name, container, scope |
| `read` | Read code | path, startLine, endLine |
| `search` | Pattern search | pattern, patternType, scope |
| `edit_snippet` | Lightweight edit (within 80 chars) | path, instructions |
| `edit_structured` | Structured edit | path, symbolName, operation, newText |
| `create_class` | Create class | path, className, namespace, baseType |
| `rename_symbol` | Rename | relative, namePath, newName |
| `remove_symbol` | Remove symbol | path, namePath, failOnReferences |
| `get_index_status` | Check index status | - |
| `build_index` | Build index | - |
| `update_index` | Update index | paths |
| `get_compilation_state` | Compilation state | includeMessages |

> **Note**: For architecture patterns (Fail-Fast, UniTask, VContainer, etc.), see parent skill `unity-development`.
