---
name: code-generator
description: Generate code implementation from design documents following structured phase-based workflow with token cost estimation and modification previews.
version: 1.0
---

# Code Generator Skill

Structured workflow for implementing code from design documents with clear phase separation, cost estimation, and modification tracking.

## When to Use

Use this skill when you need to:
- Implement a new module or system from a design document
- Add features to existing codebase
- Refactor or replace existing components
- Generate implementation code with clear execution plan

## Core Principles

### 1. Phase-Based Execution
- Break implementation into logical phases
- Each phase has clear dependencies
- Execute sequentially, phase by phase

### 2. Operation Type Declaration
- **Create**: New file that doesn't exist
- **Modify**: Existing file requiring changes
- **Delete**: Remove existing file (rare, requires explicit confirmation)

### 3. Cost Transparency
- Estimate token cost for each operation
- Calculate total cost before execution
- Allow user to adjust scope based on budget

### 4. Modification Preview
- For modify operations, show before/after diff
- Highlight key changes
- No surprises for user

### 5. Capability Boundaries
- **Can Do**: Code generation, file read/write
- **Cannot Do**: Git operations, database changes, compilation, external API calls

## Workflow

### Step 1: Analyze Design Document

Read and understand:
- Architecture overview
- File list and dependencies
- Key design decisions
- Interface contracts

### Step 2: Create Execution Plan

Use this format:

```markdown
## 📋 [ProjectName] Implementation Plan

### Execution Capability Statement

| Operation | Capability |
|-----------|------------|
| Code generation | ✅ Can execute |
| Database operations | ❌ Cannot execute (user handles) |
| Git/SVN operations | ❌ Do not execute |
| Compilation | ❌ Do not execute (user triggers) |

### Phase [N]: [Phase Name]

| Order | File | Path | Operation | Content | Time | Token Cost |
|-------|------|------|-----------|---------|------|------------|
| 1 | `FileName.h` | `Path/` | Create/Modify | Brief description | X min | ~X,XXX |

**Phase Subtotal**: ~X,XXX tokens

### Modification Preview

For modify operations only:

`FileName.h`:
```cpp
// Before: [current state or "None"]
// After: [new code to be added]
```

### Phase Dependencies

```
Phase 1 ──► Phase 2 ──► Phase 3
```

### Total Cost Summary

| Phase | Time | Token Cost |
|-------|------|------------|
| 1 | X min | ~X,XXX |
| 2 | X min | ~X,XXX |
| **Total** | **X hours** | **~XX,XXX** |

### User Confirmation Items

1. [Specific question 1]
2. [Specific question 2]
3. Start confirmation: Reply "批准计划" to begin
```

### Step 3: Execute Phase by Phase

After user approval with "批准计划":

1. **Announce current phase**
2. **Execute operations** in order
3. **Report progress** after each file
4. **Confirm phase completion** before next phase

### Step 4: Completion Report

```markdown
## ✅ Implementation Complete

### Generated Files

| File | Path | Lines |
|------|------|-------|
| `File.h` | `Path/` | XXX |

### Modified Files

| File | Path | Changes |
|------|------|---------|
| `File.cpp` | `Path/` | Added X methods |

### Next Steps (User Action Required)

1. [Database setup, compilation, etc.]

### Token Usage

- **Estimated**: ~XX,XXX
- **Actual**: ~XX,XXX
```

## Token Cost Guidelines

| File Type | Lines | Estimated Tokens |
|-----------|-------|------------------|
| Header (declaration) | 50-100 | 500-1,000 |
| Implementation | 200-300 | 2,000-4,000 |
| Simple modification | - | 300-800 |
| Complex modification | - | 1,000-2,000 |
| CSV/Data file | 20-50 | 200-500 |
| Test file | 100-200 | 1,000-2,000 |

## Template: Complete Example

```markdown
## 📋 PlayerSystem Implementation Plan

### Execution Capability Statement

| Operation | Capability |
|-----------|------------|
| Code generation | ✅ Can execute |
| Database operations | ❌ Cannot execute |
| Git/SVN operations | ❌ Do not execute |
| Compilation | ❌ Do not execute |

### Phase 1: Data Structures

| Order | File | Path | Operation | Content | Time | Token Cost |
|-------|------|------|-----------|---------|------|------------|
| 1 | `SystemDefines.h` | `Project/` | Create | Enums and utilities | 5m | ~500 |
| 2 | `SystemInstance.h` | `Project/` | Create | Struct with Save/Load | 10m | ~800 |

**Phase 1 Subtotal**: ~1,300 tokens

### Phase 2: Core Implementation

| Order | File | Path | Operation | Content | Time | Token Cost |
|-------|------|------|-----------|---------|------|------------|
| 3 | `PlayerSystem.h` | `Project/` | Create | Class declaration | 10m | ~1,000 |
| 4 | `PlayerSystem.cpp` | `Project/` | Create | Core methods | 30m | ~3,500 |

**Phase 2 Subtotal**: ~4,500 tokens

### Phase 3: Integration

| Order | File | Path | Operation | Content | Time | Token Cost |
|-------|------|------|-----------|---------|------|------------|
| 5 | `Player.h` | `Project/` | Modify | Add accessor method | 5m | ~300 |

**Modification Preview**:

`Player.h`:
```cpp
// Before: No System member
class Player {
    // existing members
};

// After: Added System
class Player {
    // existing members
public:
    PlayerSystem& GetSystem() { return mSystem; }
private:
    PlayerSystem mSystem;
};
```

**Phase 3 Subtotal**: ~300 tokens

### Total Cost Summary

| Phase | Time | Token Cost |
|-------|------|------------|
| 1 | 15m | ~1,300 |
| 2 | 40m | ~4,500 |
| 3 | 5m | ~300 |
| **Total** | **1 hour** | **~6,100** |

### User Confirmation

1. Database table: I provide SQL / You create manually
2. Start: Reply "批准计划"
```

## Anti-Patterns

### ❌ Don't
- Start coding without user approval
- Skip modification previews for modify operations
- Omit token cost estimation
- Perform Git/database/compilation operations
- Combine multiple phases without checkpoint

### ✅ Do
- Wait for "批准计划" before execution
- Show before/after for all modifications
- Estimate costs conservatively
- Stay within code generation scope only
- Execute phase by phase with progress reports

## Integration with Other Skills

- **mvp-design**: Use as input (design doc → implementation)
- **code-analysis**: Verify existing files before modification
- **skill-creator**: Extract patterns into reusable skills

## Quick Reference

### Cost Estimation Formula

```
Header file:    10 tokens per line
Implementation: 15 tokens per line
Modification:   20 tokens per line (includes context)
Test file:      12 tokens per line
```

### Modification Preview Format

```cpp
// File: Path/Filename.ext

// Before: [describe current state]
[code snippet or "None - new addition"]

// After: [describe new state]
[code snippet to be added/modified]

// Key changes:
// - Change 1
// - Change 2
```

## Version History

- v1.0 (2026-02-10) - Initial release
  - Phase-based execution model
  - Token cost estimation
  - Modification preview requirement
  - Clear capability boundaries
