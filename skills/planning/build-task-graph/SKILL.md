---
name: build-task-graph
description: Build task dependency graph YAML from interface and pseudocode
user-invocable: false
allowed-tools:
  - mcp__plugin_mermaid-collab_mermaid__*
  - Read
  - Glob
---

# Build Task Graph

Create the task dependency graph from interface and pseudocode documents.

## When Invoked

After rough-draft-skeleton completes, before rough-draft-handoff.

## Process

### Step 1: Read Interface and Pseudocode Documents

Read all interface-item-N.md and pseudocode-item-N.md documents:

```
Tool: mcp__plugin_mermaid-collab_mermaid__list_documents
Args: { "project": "<cwd>", "session": "<session>" }
```

Filter for interface-* and pseudocode-* documents and read each.

### Step 2: Extract File Changes

For each item's interface document:
1. Find "File Structure" section
2. Extract all file paths (new and modified)
3. Note which files depend on others (imports, references)

### Step 3: Build Task List

For each file:
1. Create task ID from file path (e.g., src/auth/service.ts → auth-service)
2. Set files array
3. Generate test file paths:
   - {dir}/{name}.test{ext}
   - {dir}/__tests__/{name}.test{ext}
4. Extract description from interface doc
5. Analyze dependencies:
   - If file imports from another file, add dependency
   - If pseudocode mentions "after X", add dependency

### Step 4: Identify Parallel Tasks

Mark tasks as parallel: true if:
- No dependencies
- Or all dependencies are from previous waves

### Step 5: Calculate Execution Waves

Group tasks by wave:
- Wave 1: Tasks with no dependencies
- Wave N: Tasks depending only on waves 1 to N-1

### Step 6: Check File Conflicts

Identify tasks that modify the same file:
- Warn about conflicts
- Suggest ordering to avoid merge issues

### Step 7: Create task-graph.md

```
Tool: mcp__plugin_mermaid-collab_mermaid__create_document
Args: {
  "project": "<cwd>",
  "session": "<session>",
  "name": "task-graph",
  "content": "<task graph content>"
}
```

## Output Format

```markdown
# Task Dependency Graph

## YAML Task Graph

```yaml
tasks:
  - id: task-id
    files: [path/to/file.ts]
    tests: [path/to/file.test.ts]
    description: What this task implements
    parallel: true
    depends-on: [other-task-id]
```

## Execution Waves

**Wave 1 (no dependencies):**
- task-1
- task-2

**Wave 2 (depends on Wave 1):**
- task-3

## File Conflict Analysis

[Note any files modified by multiple tasks]

## Summary

- Total tasks: N
- Total waves: M
- Max parallelism: P
```

## Completion

At the end of this skill's work, call complete_skill:

```
Tool: mcp__plugin_mermaid-collab_mermaid__complete_skill
Args: { "project": "<cwd>", "session": "<session>", "skill": "build-task-graph" }
```

**Handle response:**
- If `action == "clear"`: Invoke skill: collab-clear
- If `next_skill` is not null: Invoke that skill
- If `next_skill` is null: Workflow complete
