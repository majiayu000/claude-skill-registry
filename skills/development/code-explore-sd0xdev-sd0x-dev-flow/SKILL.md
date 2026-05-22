---
name: code-explore
description: Pure Claude code investigation. Fast codebase exploration, trace execution paths, understand architecture, diagnose issues. No Codex dependency.
allowed-tools: Read, Grep, Glob, Bash
context: fork
---

# Code Explore Skill

## Trigger

- Keywords: code explore, code investigation, research code, trace code, feature understanding, quick investigation, code exploration

## When to Use

- Quickly understand how a feature works
- Trace execution paths / data flow
- Diagnose problem root causes
- No dual confirmation needed (no Codex cross-validation)

## When NOT to Use

| Scenario                | Alternative                           |
| ----------------------- | ------------------------------------- |
| Need dual confirmation  | `/code-investigate` (Claude + Codex)  |
| Git history tracking    | `/git-investigate`                    |
| System verification     | `/feature-verify`                     |
| Code review             | `/codex-review-fast`                  |

## Workflow

```
┌──────────────────────────────────────────────────────────┐
│ Phase 1: Locate Entry Point                                │
├──────────────────────────────────────────────────────────┤
│ 1. Grep keywords -> find related files                     │
│ 2. Identify entry points (Controller / Service / Provider) │
│ 3. Build file list                                         │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│ Phase 2: Trace Path                                        │
├──────────────────────────────────────────────────────────┤
│ 1. Start from entry point, Read                            │
│ 2. Identify dependencies -> continue tracing               │
│ 3. Map call chain (A -> B -> C)                            │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│ Phase 3: Understand Logic                                  │
├──────────────────────────────────────────────────────────┤
│ 1. What is the core logic?                                 │
│ 2. How does data flow?                                     │
│ 3. Error handling mechanisms?                              │
│ 4. Key decision points?                                    │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│ Phase 4: Output Report                                     │
├──────────────────────────────────────────────────────────┤
│ 1. Architecture overview (diagram / table)                 │
│ 2. Key files list                                          │
│ 3. Execution flow                                          │
│ 4. Findings / notes                                        │
└──────────────────────────────────────────────────────────┘
```

## Search Strategy

| Target          | Strategy                                                 |
| --------------- | -------------------------------------------------------- |
| Feature entry   | `Grep "export class.*Controller"` / `Grep "@Get\|@Post"` |
| Service layer   | `Grep "export class.*Service"`                           |
| Provider layer  | `Glob "src/provider/**/*.ts"`                            |
| Configuration   | `Read {CONFIG_FILE}`                                     |
| Data models     | `Glob "src/model/**/*.ts"`                               |

## Output Format

```markdown
## Investigation Report: {Topic}

### Architecture Overview

{ASCII or Mermaid diagram}

### Key Files

| File              | Responsibility |
| ----------------- | -------------- |
| `path/to/file.ts` | Description   |

### Execution Flow

1. {Step 1}
2. {Step 2}
3. ...

### Data Flow

{Describe how data flows}

### Findings

- {Important finding 1}
- {Important finding 2}

### Notes

- {Potential issue / edge case}
```

## Examples

### Feature Understanding

```
Input: Investigate how user data queries work
Phase 1: Grep "balance" -> find UserService, UserController
Phase 2: Controller -> Service -> Provider call chain
Phase 3: Understand query + cache mechanism
Phase 4: Output report + flow diagram
```

### Problem Diagnosis

```
Input: Why does this API sometimes return empty?
Phase 1: Grep "getData" + "cache" -> related files
Phase 2: Trace data retrieval path
Phase 3: Identify fallback logic + timeout handling
Phase 4: List possible causes + recommendations
```

### Architecture Understanding

```
Input: What is the overall architecture of the user module?
Phase 1: Glob "src/**/*user*" -> list all related files
Phase 2: Identify layer relationships (Controller -> Service -> Provider)
Phase 3: Understand each layer's responsibilities
Phase 4: Output architecture diagram + module description
```

## Difference from code-investigate

| Dimension    | code-explore           | code-investigate       |
| ------------ | ---------------------- | ---------------------- |
| Speed        | Fast (single view)     | Slow (dual view)       |
| Confirmation | Single perspective     | Cross-validation       |
| Tools        | Pure Claude            | Claude + Codex         |
| Use case     | Quick investigation    | Important decisions    |
