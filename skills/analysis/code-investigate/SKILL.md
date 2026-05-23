---
name: code-investigate
description: Dual-perspective code investigation. Claude explores independently, then Codex explores independently (no feeding), finally integrate both conclusions.
allowed-tools: Read, Grep, Glob, Bash, mcp__codex__codex
context: fork
---

# Code Investigate Skill

## Trigger

- Keywords: investigate code, how feature works, trace implementation, dual confirmation, deep dive, how code works, what this code does, code research

## When NOT to Use

- Just need quick lookup (use Grep/Glob directly)
- Code review (use codex-review)
- System verification (use feature-verify)
- Git history tracking (use git-investigate)

## Core Principle

```
Codex must explore independently. Feeding Claude's conclusions to Codex is prohibited.
```

```
┌─────────────────┐     ┌─────────────────┐
│ Claude Explores  │     │ Codex Explores   │
│ Independently    │     │ Independently    │
│   (Phase 1-2)   │     │    (Phase 3)     │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
   ┌───────────┐           ┌───────────┐
   │ Claude    │           │ Codex     │
   │ Conclusion│           │ Conclusion│
   └─────┬─────┘           └─────┬─────┘
         │                       │
         └───────────┬───────────┘
                     ▼
              ┌─────────────┐
              │ Consolidated│
              │   Report    │
              │  (Phase 4)  │
              └─────────────┘
```

## Workflow

| Phase | Name            | Action                              | Output                      |
| ----- | --------------- | ----------------------------------- | --------------------------- |
| 1     | Claude Explore  | Grep/Glob/Read to search code       | Related files list          |
| 2     | Claude Conclude | Analyze logic, form understanding   | Initial conclusion (internal)|
| 3     | Codex Explore   | Invoke Codex MCP to explore independently | Codex analysis report  |
| 4     | Integrate       | Compare both perspectives, mark differences | Consolidated report   |

## Codex Invocation Rules

### Required Parameters

| Parameter         | Value       | Description     |
| ----------------- | ----------- | --------------- |
| `sandbox`         | `read-only` | Force read-only |
| `approval-policy` | `never`     | Auto-execute    |
| `cwd`             | Project root| Exploration start point |

### Correct Approach

```typescript
mcp__codex__codex({
  prompt: `# Code Investigation Task

## Question
${userQuestion}

## Project Info
- Path: ${cwd}
- Tech Stack: {FRAMEWORK} + TypeScript + {DATABASE}

Please **independently explore** the codebase and answer:
1. What files are related?
2. How does the core logic work?
3. What is the data flow?
4. What are the key dependencies?

Please grep/read and explore on your own, then provide your analysis.`,
  cwd: '/path/to/project',
  sandbox: 'read-only',
  'approval-policy': 'never',
});
```

### Prohibited Approaches

| Pattern            | Problem                           | Example                                     |
| ------------------ | --------------------------------- | ------------------------------------------- |
| Feeding conclusion | Claude's findings leak to Codex   | `Claude found these files: ${findings}`     |
| Leading question   | Presupposes answer                | `I think the problem is in cache, verify`   |
| Scope restriction  | Prevents independent exploration  | `Only look at src/service/`                 |

## Verification Checklist

| Check                     | Standard                                      |
| ------------------------- | --------------------------------------------- |
| Claude independent conclusion | Phase 2 forms conclusion, not output to user |
| Codex prompt is clean     | Contains only question + project path, no Claude findings |
| Report perspectives separated | Claude / Codex conclusions presented separately |
| Integration is complete   | Marks agreement, differences, possible gaps   |

## References

| File                            | Purpose              | When to Read       |
| ------------------------------- | -------------------- | ------------------ |
| `references/prompts.md`         | Codex prompt templates | Before Phase 3   |
| `references/output-template.md` | Report format        | During Phase 4     |

## Examples

### Feature Investigation

```
Input: Investigate how order processing works
Phase 1: Grep "processOrder" -> Read src/service/order/*.ts
Phase 2: Form understanding: Controller -> Service -> Repository write
Phase 3: Codex explores independently (only given question + path)
Phase 4: Consolidated report -> mark both perspectives
```

### Mechanism Understanding

```
Input: How does the API caching mechanism work?
Phase 1: Grep "cache" + "portfolio" -> Read related files
Phase 2: Understand Redis TTL + fallback mechanism
Phase 3: Codex investigates independently
Phase 4: Compare differences -> output consolidated report
```

### Problem Diagnosis

```
Input: Why is token price sometimes null?
Phase 1: Search price-related logic + error handling
Phase 2: Identify possible fallback paths
Phase 3: Codex diagnoses independently
Phase 4: Synthesize both findings -> list possible causes
```
