---
name: find-todos
description: Locate development tasks and TODO comments across the codebase
disable-model-invocation: false
---

# Find Development Tasks

I'll locate all TODO comments and unfinished work markers in your codebase.

## Token Optimization

**Target Reduction:** 70% (2,000-3,000 → 600-900 tokens)

**Optimization Status:** ✅ Optimized (Phase 2 Batch 3D-F, 2026-01-26)

### Key Optimizations

1. **Pure Grep-Based Search (No File Reading)**
   - Use Grep tool exclusively for TODO/FIXME/HACK/XXX/NOTE detection
   - Pattern: `"TODO|FIXME|HACK|XXX|NOTE"` with case-insensitive search
   - Grep provides file location, line numbers, and surrounding context
   - **NEVER use Read tool** - grep output contains all necessary information
   - **Saves:** 1,000-1,500 tokens per search

2. **Git Diff Scoping (Smart Defaults)**
   - Default behavior: Search only files changed in current branch
   - Use `git diff --name-only main...HEAD` to get changed files
   - Pass file list to Grep tool with path restriction
   - Fall back to full codebase search only if no git repo or explicit request
   - **Saves:** 500-1,000 tokens for large codebases

3. **Head Limit on Results**
   - Limit grep output to first 50 TODO comments using `head_limit: 50`
   - Prevents overwhelming results in large codebases
   - Most actionable TODOs are in recently changed files anyway
   - User can request "show all" if needed for comprehensive audit
   - **Saves:** 500-1,000 tokens for codebases with many TODOs

4. **Early Exit Detection**
   - Check if grep finds any TODOs before processing results
   - If no TODOs found: Immediately report "No TODOs found" and exit
   - Avoid creating empty task lists or unnecessary analysis
   - **Saves:** 200-400 tokens when no TODOs present

5. **Progressive Disclosure (Priority-Based)**
   - Sort results by marker type: FIXME/HACK/XXX first, then TODO, then NOTE
   - Show critical items (FIXME/HACK) in detail with context
   - Summarize lower-priority items (TODO/NOTE) concisely
   - Ask user if they want full details on non-critical items
   - **Saves:** 300-500 tokens by focusing on high-priority items

6. **Result Caching**
   - Cache TODO inventory at `.claude/cache/find-todos/todo-inventory.json`
   - Format: `{"file": "path", "line": 42, "type": "TODO", "comment": "text", "context": "code"}`
   - Subsequent skills (`fix-todos`, `todos-to-issues`) reuse cached data
   - Cache expires after 1 hour or when git HEAD changes
   - **Saves:** 500-1,000 tokens for dependent skills

### Usage Patterns

**Minimal scope (200-300 tokens):**
```bash
find-todos path/to/specific/file.ts
```

**Changed files only (400-600 tokens):**
```bash
find-todos
```

**Full codebase audit (600-900 tokens):**
```bash
find-todos --all
```

### Expected Token Usage

| Scenario | Before | After | Savings |
|----------|--------|-------|---------|
| Specific file | 800-1,000 | 200-300 | 70% |
| Changed files (default) | 1,500-2,000 | 400-600 | 70% |
| Full codebase | 2,500-3,000 | 600-900 | 70% |
| No TODOs found | 600-800 | 100-200 | 75% |

### Caching Behavior

- **Cache location:** `.claude/cache/find-todos/`
- **Cached data:** TODO inventory by file with line numbers and context
- **Shared with:** `/fix-todos`, `/create-todos`, `/todos-to-issues` skills
- **Cache invalidation:** 1 hour timeout or git HEAD change
- **Cache benefits:** Enables zero-cost TODO lookups for dependent skills

I'll use the Grep tool to efficiently search for task markers with context:
- Pattern: "TODO|FIXME|HACK|XXX|NOTE"
- Case insensitive search across all source files
- Show surrounding lines for better understanding

For each marker found, I'll show:
1. **File location** with line number
2. **The full comment** with context
3. **Surrounding code** to understand what needs to be done
4. **Priority assessment** based on the marker type

When I find multiple items, I'll create a todo list to organize them by priority:
- **Critical** (FIXME, HACK, XXX): Issues that could cause problems
- **Important** (TODO): Features or improvements needed
- **Informational** (NOTE): Context that might need attention

I'll also identify:
- TODOs that reference missing implementations
- Placeholder code that needs replacement
- Incomplete error handling
- Stubbed functions awaiting implementation

After scanning, I'll ask: "Convert these to GitHub issues?"
- Yes: I'll create properly categorized issues
- Todos only: I'll maintain the local todo list
- Summary: I'll provide organized report

**Important**: I will NEVER:
- Add "Created by Claude" or any AI attribution to issues
- Include "Generated with Claude Code" in descriptions
- Modify repository settings or permissions
- Add any AI/assistant signatures or watermarks

This helps track and prioritize unfinished work systematically.