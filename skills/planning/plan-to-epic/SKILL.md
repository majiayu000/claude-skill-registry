---
name: plan-to-epic
description: Parse an implementation plan into a Beads epic with scoped tasks, three-field separation, and automatic dependency inference. Use after writing-plans produces a plan.
disable-model-invocation: true
---

# Plan to Epic

Convert an implementation plan into a Beads epic with properly scoped, dependency-linked tasks.

## Arguments

- First argument: path to implementation plan (required)
- `--design <path>`: path to design doc (optional, for architecture context)
- `--epic-title <title>`: override epic title (optional)

## Process

### Phase 0: Read & Parse

1. Read the implementation plan at the given path
2. If `--design` provided, read the design doc too
3. Extract: Goal, Architecture, Tech Stack from the plan header
4. Identify all Tasks (look for `### Task N:` headings)

### Phase 1: Scope Validation

For each task, apply the **one-sentence scoping test**:
> "Can you describe this task in one sentence without using 'and' to join unrelated capabilities?"

If a task fails this test, split it into multiple tasks.

### Phase 2: Three-Field Separation

For each task, produce three fields:

| Field | Content | Purpose |
|-------|---------|---------|
| **Description** | Implementation steps, file paths, commands, code snippets, test commands | What to DO |
| **Design** | Architecture decisions, component relationships, data flow from design doc | WHY we're doing it this way |
| **Notes** | Source document path + line numbers, context7 references, relevant CLAUDE.md rules | WHERE to look for more info |

### Phase 3: Dependency Inference

Detect dependencies automatically:
1. **File overlap**: If Task B modifies a file that Task A creates -> B depends on A
2. **Explicit references**: Scan for "after Task N" or "requires Task N" patterns
3. **Phase ordering**: Tasks in later plan sections depend on earlier sections' tasks

### Phase 4: Create Beads Epic

```bash
# Create the epic
bd create "<Goal from plan header>" --type epic -p 1

# For each task (example):
bd create "<Task title>" --parent <epic-id> -d "<Description field>"

# Set dependencies
bd dep add <child-id> <parent-id>
```

### Phase 4.5: DAG Cycle Detection

After creating all tasks and dependencies, validate the dependency graph has no cycles:

```bash
# Verify no circular dependencies
bd dep cycles 2>&1
```

If a cycle is detected:
1. Identify the offending dependency edge
2. Remove the circular dependency by restructuring task order
3. Log a warning: "Removed circular dependency: <child> -> <parent>"
4. Re-verify until clean

If `bd dep check` is not available, manually inspect by traversing the dependency chain for each task (max depth 10). If a task is encountered twice, there is a cycle.

### Phase 5: Summary

Output a table:
```
Epic: <id> -- <title>
Tasks: <count>
Dependencies: <count edges>

Task Graph:
  bd-XX: Setup (no deps)
  bd-YY: Implementation (blocked by bd-XX)
  bd-ZZ: Testing (blocked by bd-YY)
```

## Tips

- Use `bd create ... -d "$(cat <<'EOF' ... EOF)"` for multi-line descriptions
- Keep descriptions self-contained -- a subagent should be able to execute without the original plan
- Embed completion criteria in every task description
- Include verification commands (test, lint, typecheck) in every task
