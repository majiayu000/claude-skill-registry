---
name: explore-first-navigation
description: This skill should be used when the user asks to "find files", "search code", "locate implementation", "understand architecture", "explore codebase", "where is X defined", "how does X work", "find pattern", "show me the structure", or any codebase navigation that involves searching, finding, or understanding code. CRITICALLY, this skill MUST also be used when the agent needs to "investigate root cause", "find where this is defined", "trace the error", "locate the source of", "find related files", "search for references", "understand how X works before implementing", "find the implementation of", "discover what files handle", or ANY internal reasoning that requires exploring the codebase to gather context. MANDATORY for open-ended searches requiring multiple file reads or pattern matching. Delegates exploration to Haiku sub-agents to preserve main context window.
version: 1.1.0
title: "Explore First Navigation"
status: active
---

# Explore-First Navigation

## Core Principle: Delegate Before Direct Search

**MANDATORY**: For any codebase navigation task - whether requested by user OR needed by agent for investigation - launch an Explore agent BEFORE using Glob/Grep/Read directly.

**This applies when YOU (the agent) think:**
- "I need to find where X is defined..."
- "Let me investigate the root cause..."
- "I should understand how this works first..."
- "I need to trace this error to its source..."
- "Let me find related files..."

```python
# ✅ CORRECT: Explore agent for navigation
Task(
    subagent_type="Explore",
    model="haiku",
    prompt="Find all API endpoints in the backend. Return paths, methods, and handlers."
)

# ❌ WRONG: Direct tool usage for exploration
Glob(pattern="**/*.py")  # Loads file list into main context
Grep(pattern="@app.get")  # Results consume main context
Read(file_path="...")     # Full file in main context
```

**Why**: Explore agents use their own context window. Main agent retains 70-80% of context for implementation.

---

## Trigger Conditions (AUTO-DELEGATE)

**ALWAYS use Explore agent in these scenarios:**

### When User Asks:

| Query Pattern | Explore Prompt Template |
|---------------|------------------------|
| "Where is X defined?" | `Find the definition of X. Return file path, line number, and signature.` |
| "How does X work?" | `Analyze the implementation of X. Return key files, data flow, and patterns.` |
| "Find all Y in codebase" | `Search for all instances of Y. Return file paths and context.` |
| "What files handle Z?" | `Identify files responsible for Z. Return paths and responsibilities.` |
| "Show me the structure" | `Map the directory structure. Return layer organization and key files.` |
| "Understand the architecture" | `Analyze codebase architecture. Return layers, patterns, dependencies.` |
| "Search for pattern P" | `Find code matching pattern P. Return matches with file:line references.` |

### When Agent Needs To (SELF-INVOCATION):

| Agent Intent | Explore Prompt Template |
|--------------|------------------------|
| Investigate root cause of bug | `Trace the error flow for [ERROR]. Find origin, propagation path, and handlers.` |
| Understand before implementing | `Analyze existing implementation of [FEATURE]. Return patterns, files, and conventions.` |
| Find where something is defined | `Find definition of [SYMBOL]. Return file:line and dependencies.` |
| Locate related code for changes | `Find all code related to [COMPONENT]. Return files that may need updates.` |
| Trace data flow | `Trace how [DATA] flows through the system. Return path from source to destination.` |
| Find test coverage | `Find tests covering [MODULE]. Return test files and what they verify.` |
| Discover integration points | `Find where [SERVICE] integrates with other components. Return connection points.` |

---

## Quick Reference: Explore Agent Usage

### Basic Exploration (Single Query)

```python
Task(
    subagent_type="Explore",
    model="haiku",  # Cost-effective, fast
    prompt="""MISSION: [Specific search goal]

SEARCH FOR:
- [Pattern or target]

RETURN FORMAT:
{
  "matches": [{"file": "path", "line": N, "context": "..."}],
  "total": N,
  "patterns_detected": []
}

MAX OUTPUT: 500 tokens"""
)
```

### Parallel Exploration (Multiple Concerns)

```python
# Launch simultaneously for different areas
Task(subagent_type="Explore", model="haiku",
     prompt="Find all database models in backend/...")
Task(subagent_type="Explore", model="haiku",
     prompt="Find all API routes in api/...")
Task(subagent_type="Explore", model="haiku",
     prompt="Find all React components in frontend/...")
```

### Architecture Mapping

```python
Task(
    subagent_type="Explore",
    model="haiku",
    prompt="""MISSION: Map codebase architecture

ANALYZE:
1. Directory structure and layer organization
2. Key entry points (main files, routers, handlers)
3. Data flow patterns (frontend → API → DB)
4. Dependency relationships

RETURN AS:
{
  "layers": {"frontend": {...}, "backend": {...}, "shared": {...}},
  "entry_points": ["file1", "file2"],
  "patterns": ["MVC", "MCP", ...]
}"""
)
```

---

## Decision Matrix: Explore vs Direct Tools

| Scenario | Use Explore Agent | Use Direct Tools |
|----------|-------------------|------------------|
| "Find where X is defined" | ✅ | ❌ |
| "Search for pattern in codebase" | ✅ | ❌ |
| "Understand how Y works" | ✅ | ❌ |
| "Read specific file I mentioned" | ❌ | ✅ |
| "Edit line 42 of file.py" | ❌ | ✅ |
| "List files in this exact directory" | ❌ | ✅ |
| "Open-ended exploration" | ✅ | ❌ |
| "Multiple file search" | ✅ | ❌ |
| "Known file, specific line" | ❌ | ✅ |

**Rule of Thumb**: If you don't know the exact file path, use Explore.

---

## Thoroughness Levels

Specify exploration depth in your prompt:

| Level | When to Use | Prompt Addition |
|-------|-------------|-----------------|
| `quick` | Simple file finding | `Thoroughness: quick` |
| `medium` | Pattern search, moderate depth | `Thoroughness: medium` |
| `very thorough` | Architecture analysis, comprehensive | `Thoroughness: very thorough` |

```python
Task(
    subagent_type="Explore",
    prompt="""MISSION: Find all authentication middleware
Thoroughness: very thorough

SEARCH:
- Auth decorators and middleware
- Session handling
- Token validation
- Permission checks

RETURN comprehensive analysis with file paths and relationships."""
)
```

---

## Output Formats for Explore Results

### File Discovery Format
```json
{
  "files": [
    {"path": "src/api/users.py", "relevance": "high", "summary": "User CRUD endpoints"}
  ],
  "total_matches": 5
}
```

### Pattern Search Format
```json
{
  "matches": [
    {"file": "src/api/users.py", "line": 42, "match": "@app.get('/users')", "context": "..."}
  ],
  "pattern": "@app.get",
  "total": 12
}
```

### Architecture Map Format
```json
{
  "layers": {
    "frontend": {"path": "app/", "pattern": "Next.js", "key_files": 15},
    "backend": {"path": "api/", "pattern": "FastAPI", "key_files": 20}
  },
  "dependencies": ["frontend→backend", "backend→database"]
}
```

---

## Integration with Orchestrator

When using `orchestrator-multiagent` skill:

1. **Before Planning (Phase 0-1)**: Use Explore to understand codebase
2. **During Execution (Phase 2)**: Workers have their own context, can explore directly
3. **For Regression Checks**: Use Explore to verify unchanged areas

```python
# Orchestrator delegates exploration before task decomposition
exploration_results = Task(
    subagent_type="Explore",
    model="haiku",
    prompt="Map the authentication system architecture..."
)

# Use results to inform task breakdown
# Main context preserved for planning
```

---

## Common Patterns

### Pattern 1: Find-Then-Read
```python
# Step 1: Explore finds the file
result = Task(subagent_type="Explore", prompt="Find the main router file...")

# Step 2: Read specific file ONLY after knowing path
Read(file_path=result['file'])  # Targeted read, minimal context
```

### Pattern 2: Multi-Layer Search
```python
# Parallel exploration of different layers
Task(subagent_type="Explore", prompt="Find frontend state management...")
Task(subagent_type="Explore", prompt="Find backend data validation...")
Task(subagent_type="Explore", prompt="Find database migration files...")
```

### Pattern 3: Dependency Tracing
```python
Task(
    subagent_type="Explore",
    prompt="""Trace dependencies of UserService:
    1. What does UserService import?
    2. What imports UserService?
    3. What database tables does it access?
    Return dependency graph."""
)
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Direct Glob/Grep for Exploration
```python
# ❌ WRONG - Consumes main context
files = Glob(pattern="**/*.py")  # 500+ file paths in context
matches = Grep(pattern="class.*Service")  # All matches in context
```

### Anti-Pattern 2: Reading Files to "Explore"
```python
# ❌ WRONG - Full file contents in main context
Read(file_path="src/services/user.py")
Read(file_path="src/services/auth.py")
Read(file_path="src/services/payment.py")
# 3 files = ~1500 lines in context
```

### Anti-Pattern 3: Skipping Explore for "Quick" Searches
```python
# ❌ WRONG - "Quick" search that snowballs
Grep(pattern="TODO")  # Start with one search
# "Let me also check..."
Grep(pattern="FIXME")
Grep(pattern="HACK")
# 3 searches = significant context consumption
```

**Correct approach**: Single Explore with multiple patterns
```python
Task(
    subagent_type="Explore",
    prompt="Find all TODO, FIXME, and HACK comments. Return summary by category."
)
```

---

## Context Savings Calculator

| Approach | Estimated Context | Savings |
|----------|-------------------|---------|
| 5 Glob + 10 Read | ~5,000 tokens | Baseline |
| 1 Explore agent | ~200 tokens | **96% reduction** |
| 3 Grep searches | ~1,500 tokens | Baseline |
| 1 Explore (multi-pattern) | ~150 tokens | **90% reduction** |

---

## When NOT to Use Explore

Direct tools are appropriate when:

1. **Exact file known**: User says "edit src/config.py line 10"
2. **Single file read**: User says "show me the contents of README.md"
3. **Targeted edit**: User provides specific file and change
4. **Post-exploration**: After Explore found the target, reading specific file

---

## Additional Resources

### Reference Files
- **`references/explore-prompts.md`** - Extensive prompt templates by use case
- **`references/parallel-patterns.md`** - Advanced parallel exploration

### Examples
- **`examples/architecture-exploration.md`** - Full architecture mapping example
- **`examples/dependency-tracing.md`** - Tracing code dependencies

---

## Quick Checklist

Before any codebase navigation:

- [ ] Is this an open-ended search? → Use Explore
- [ ] Do I need to find multiple files? → Use Explore
- [ ] Am I looking for patterns across codebase? → Use Explore
- [ ] Do I already know the exact file path? → Use Read directly
- [ ] Is user asking about specific line in known file? → Use Read directly

**Default to Explore.** When in doubt, delegate.
