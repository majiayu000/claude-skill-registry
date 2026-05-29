---
name: memex-cli
description: "Execute AI tasks (codex/claude/gemini) with memory and resume support via memex-cli stdin protocol."
---

# Memex CLI

A CLI wrapper for AI backends (Codex, Claude, Gemini) with built-in memory and resume capabilities.

## Core Concepts

memex-cli uses **stdin protocol** to define tasks, allowing:
- Multi-backend AI execution (codex, claude, gemini)
- Parallel and sequential task orchestration
- Resume from previous runs with full context
- File loading for context-aware tasks
- Structured output (text or JSONL)

## Basic Task Syntax

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: <task_id>
backend: <backend>
workdir: <working_directory>
---CONTENT---
<prompt>
---END---
EOF
```

### Required Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `id` | Unique task identifier | `implement-auth-20260110` |
| `backend` | AI backend | `codex`, `claude`, `gemini` |
| `workdir` | Working directory path | `./project` or `/home/user/app` |
| `<prompt>` | Task prompt content | Describe what to implement |

### Optional Parameters

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `model` | Specific model name | Backend default | `gpt-5.2`, `gpt-5.1-codex-max` |
| `model-provider` | Model provider | `openai` | For codex backend |
| `dependencies` | Task dependencies | None | `task-a` or `task-a,task-b` |
| `timeout` | Timeout in seconds | 300 | `600` (10 minutes) |
| `retry` | Retry count on failure | 0 | `2` (retry twice) |
| `files` | File paths to load | None | `src/**/*.py` (glob supported) |
| `files-mode` | File handling mode | `embed` | `ref`, `auto` |
| `files-encoding` | File encoding | `utf-8` | `base64`, `auto` |
| `stream-format` | Output format | `text` | `jsonl` |

## Backend Selection

### Codex - Code Generation

Optimized for code implementation and refactoring.

```bash
---TASK---
id: code-gen
backend: codex
workdir: ./project
model: gpt-5.2
---CONTENT---
实现用户认证模块
---END---
```

**Best for:** Code generation, refactoring, test writing

### Claude - Design & Architecture

Optimized for system design and architecture planning.

```bash
---TASK---
id: design
backend: claude
workdir: ./project
---CONTENT---
设计 REST API 架构
---END---
```

**Best for:** System design, architecture, documentation

### Gemini - Multimodal Tasks

Supports image and document analysis.

```bash
---TASK---
id: ux-review
backend: gemini
workdir: ./project
files: ./mockups/*.png
files-mode: embed
---CONTENT---
审查 UX 设计稿
---END---
```

**Best for:** UI/UX review, image analysis, multimodal tasks

## Task ID Patterns

**Recommended patterns:**

```
# Timestamp format (unique)
task-20260110143052
implement-auth-20260110143052

# Semantic format (readable)
design-api
implement-backend
test-integration

# Hierarchical format (organized)
auth.design
auth.implement
auth.test
```

Avoid generic IDs like `task1`, `task2`.

## Multi-Task Execution

Define multiple tasks in one stdin input:

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: task-1
backend: codex
workdir: ./project
---CONTENT---
First task
---END---

---TASK---
id: task-2
backend: codex
workdir: ./project
---CONTENT---
Second task
---END---
EOF
```

**Execution modes:**
- **Parallel** (default) - Tasks without dependencies run simultaneously
- **DAG** (sequential) - Tasks with `dependencies:` run in order

See `references/advanced-usage.md` for detailed multi-task documentation.

## Resume Functionality

Continue from a previous run using `--run-id`:

```bash
# Initial run outputs Run ID
memex-cli run --stdin < task.md
# Output: Run ID: abc123-def456

# Resume from that run
memex-cli resume --run-id abc123-def456 --stdin <<'EOF'
---TASK---
id: continue
backend: codex
workdir: ./project
---CONTENT---
基于之前的实现添加功能
---END---
EOF
```

**Context preservation:**
- Previous task outputs available
- Conversation history maintained
- File changes visible

See `references/advanced-usage.md` for resume strategies.

## Output Formats

### Text Format (Default)

Human-readable with status markers:

```
▶ task-id (backend/model)
[AI output content]
» 写入 file.py
✓ task-id 3.5s
```

**Status markers:** `▶` (start), `✓` (success), `✗` (failed), `⟳` (retry), `»` (action)

### JSONL Format

Machine-readable JSON Lines for programmatic parsing:

```bash
memex-cli run --stdin --stream-format jsonl < tasks.md
```

Output:
```jsonl
{"v":1,"type":"task.start","ts":"2026-01-10T10:00:00Z","run_id":"abc","task_id":"code-gen"}
{"v":1,"type":"assistant.output","ts":"2026-01-10T10:00:01Z",...}
{"v":1,"type":"task.end","ts":"2026-01-10T10:00:03Z",...}
```

See `references/output-formats.md` for complete format specifications.

## Quick Start Examples

**Single task:**
```bash
memex-cli run --stdin < examples/basic-task.md
```

**Parallel tasks:**
```bash
memex-cli run --stdin < examples/parallel-tasks.md
```

**DAG workflow:**
```bash
memex-cli run --stdin < examples/dag-workflow.md
```

All examples are in `examples/` directory with full task definitions.

## Additional Resources

### Reference Documentation

For detailed information on advanced features:

- **`references/output-formats.md`** - Complete output format specifications
  - Text format status markers
  - JSONL event types
  - Parsing examples

- **`references/advanced-usage.md`** - Advanced usage patterns
  - Multi-task parallel execution
  - DAG dependency configuration
  - Resume strategies
  - File loading modes
  - Timeout and retry configuration

- **`references/troubleshooting.md`** - Comprehensive troubleshooting guide
  - Installation and authentication issues
  - Task execution failures
  - File loading problems
  - Dependency and resume errors
  - Performance optimization
  - Advanced debugging techniques

### Working Examples

Ready-to-use task files in `examples/`:

- **`examples/basic-task.md`** - Single task implementation
- **`examples/parallel-tasks.md`** - Independent parallel tasks
- **`examples/dag-workflow.md`** - Complete workflow with dependencies
- **`examples/resume-workflow.md`** - Iterative development with resume

Copy and customize these examples for your projects.

## Common Workflows

### Code Implementation

```bash
# Generate code with Codex
memex-cli run --stdin <<'EOF'
---TASK---
id: implement-feature
backend: codex
workdir: ./project
model: gpt-5.2
---CONTENT---
实现用户认证模块
---END---
EOF
```

### Design Phase

```bash
# Design with Claude
memex-cli run --stdin <<'EOF'
---TASK---
id: design-system
backend: claude
workdir: ./project
---CONTENT---
设计系统架构
---END---
EOF
```

### UX Review

```bash
# Review mockups with Gemini
memex-cli run --stdin <<'EOF'
---TASK---
id: review-ui
backend: gemini
workdir: ./project
files: mockups/*.png
files-mode: embed
---CONTENT---
审查 UI 设计稿
---END---
EOF
```

### Iterative Development

```bash
# 1. Initial implementation
RUN_ID=$(memex-cli run --stdin < task.md | grep "Run ID:" | awk '{print $3}')

# 2. Add features
memex-cli resume --run-id $RUN_ID --stdin < add-features.md

# 3. Fix bugs
memex-cli resume --run-id $RUN_ID --stdin < bugfixes.md
```

## Best Practices

**Task ID naming:**
- Use descriptive, semantic names
- Include timestamps for uniqueness
- Hierarchical naming for organization

**Backend selection:**
- Codex → Code generation
- Claude → Design, architecture
- Gemini → Multimodal, UI/UX

**Dependency management:**
- Keep DAG shallow (2-3 levels)
- Parallelize independent tasks
- Use resume for long workflows

**File loading:**
- Small files (<50 KB) → `files-mode: embed`
- Large files (>50 KB) → `files-mode: ref`
- Mixed sizes → `files-mode: auto`

**Output format:**
- Interactive use → `text` (default)
- Automation → `jsonl` for parsing

## Troubleshooting

**Common issues:**

- **"memex-cli command not found"** → Install: `npm install -g memex-cli`
- **"Backend authentication failed"** → Check API keys configuration
- **"File not found"** → Verify file paths relative to `workdir:`
- **"Circular dependency"** → Restructure task dependencies (no cycles)
- **"Context size exceeded"** → Use `files-mode: ref` or load fewer files

## Summary

memex-cli enables AI-powered development workflows with:
- Multi-backend support (codex, claude, gemini)
- Parallel and sequential task execution
- Resume capability for iterative development
- Flexible file loading with glob patterns
- Structured output (text, JSONL)

Start with `examples/basic-task.md`, then explore advanced patterns in `references/`.
