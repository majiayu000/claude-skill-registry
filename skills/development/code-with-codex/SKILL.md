---
name: code-with-codex
description: "Write and generate code using memex-cli with Codex backend. Use when (1) Generating code files and scripts, (2) Refactoring existing code, (3) Writing tests, (4) Creating project scaffolds, (5) Implementing algorithms or features, (6) Code review and optimization, (7) Complex multi-file projects."
---

# Code with Codex

Use memex-cli to leverage Codex for code generation with memory and resume support.

---

## Mandatory Execution Protocol

**⚠️ CRITICAL**: Claude MUST complete ALL applicable steps below BEFORE invoking memex-cli. Skipping any step is a protocol violation.

### Step 1: Complexity Assessment (ALL Levels)

**Required for**: L1-L5

Use decision tree to determine complexity level:
```
Start
  ├─ Single file, <100 lines? → L1
  ├─ Reusable functions, no external deps? → L2
  ├─ Production module with tests?
  │   ├─ Standard CRUD/API? → L3
  │   └─ Complex algorithm? → L4
  └─ Multi-module/microservice? → L5
```

**Output**: Determined level (L1-L5) with reasoning.

### Step 2: Task Decomposition (L3+ MANDATORY)

**Required for**: L3, L4, L5

Claude MUST decompose the task into subtasks:
1. Identify all components/modules/files to be created
2. Split into independent subtasks (each <300 lines output)
3. Assign unique task IDs
4. Establish dependency relationships

**Skip condition**: Only if task is truly atomic (single file, single responsibility)

### Step 3: Dependency Analysis (L2+ MANDATORY)

**Required for**: L2, L3, L4, L5

Claude MUST analyze dependencies:
1. **File dependencies**: Which files import/require others?
2. **Task dependencies**: Which tasks must complete before others?
3. **Build DAG**: Create directed acyclic graph of execution order

**Output**: Dependency graph showing parallel groups.

### Step 4: Execution Plan Report (ALL Levels)

**Required for**: L1-L5

Claude MUST report to user before execution:

```markdown
## 📋 Execution Plan Report

### Complexity Assessment
- **Level**: L[X] ([level name])
- **Model**: [selected model]
- **Reasoning**: [why this level]

### Task Decomposition (L3+)
| ID | Description | Est. Lines | Dependencies |
|----|-------------|------------|--------------|
| task-1 | [desc] | ~100 | - |
| task-2 | [desc] | ~150 | task-1 |

### Dependency Graph (L2+)
```
Phase 1 (Parallel):  [task-1] [task-2]
                         ↓       ↓
Phase 2 (Sequential): [task-3 depends on 1,2]
```

### Execution Summary
- **Total subtasks**: N
- **Parallel groups**: M
- **Estimated phases**: P
```

### Step 5: Workdir Resolution (AUTO)

**Required for**: ALL tasks

Claude MUST resolve workdir to project root:

```bash
git rev-parse --show-toplevel
```

**Rule**: `workdir` = Git 项目根目录（绝对路径）

**Output**: Report resolved workdir in Execution Plan.

### Pre-Execution Checklist

Before invoking memex-cli, Claude MUST confirm:

- [ ] ✅ Complexity level determined (L1-L5)
- [ ] ✅ Model selected based on level
- [ ] ✅ (L2+) Dependencies analyzed
- [ ] ✅ (L3+) Task decomposed into subtasks
- [ ] ✅ Workdir resolved (via git root)
- [ ] ✅ Execution plan reported to user

**⛔ VIOLATION**: Directly passing L3/L4/L5 task to Codex without decomposition is a protocol violation. Always decompose first.

---

## Execution Strategy

| Level | Model | files-mode | Dependency Analysis | Task Decomposition | Execution |
|:-----:|-------|:----------:|:-------------------:|:------------------:|:---------:|
| **L1** | `gpt-5.1-codex-mini` | ref | ❌ | ❌ | **Serial** |
| **L2** | `gpt-5.1-codex-max` | ref | ✅ | ❌ | **Parallel** |
| **L3** | `gpt-5.2-codex` | ref | ✅ | ✅ | **Parallel** |
| **L4** | `gpt-5.2` | ref | ✅ | ✅ | **Parallel** |
| **L5** | `gpt-5.2` | ref | ✅ | ✅ | **Parallel** |

---

## Automated Capabilities

| Capability | Description | Active Level |
|------------|-------------|:------------:|
| **Auto Model Selection** | Automatically select optimal model based on complexity | L1-L5 |
| **Auto Grading** | Evaluate task complexity via Decision Tree | L1-L5 |
| **Dependency Analysis** | Analyze task/file dependencies, build DAG | L2+ |
| **Task Decomposition** | Auto-split large tasks into subtasks | L3+ |
| **Parallel Execution** | Execute independent subtasks in parallel | L2+ |

---

## Dependency Analysis Guide (L2+)

System automatically analyzes dependencies between tasks/files and builds execution DAG.

### How It Works

```
Input: Multiple related tasks
         ↓
┌─────────────────────────────┐
│ 1. Parse task descriptions  │
│ 2. Identify file references │
│ 3. Detect implicit deps     │
│ 4. Build dependency graph   │
└─────────────────────────────┘
         ↓
Output: Execution DAG with parallel groups
```

### Dependency Detection Rules

| Type | Detection Method | Example |
|------|------------------|---------|
| **Explicit** | `dependencies` field | `dependencies: task-1, task-2` |
| **File-based** | Output→Input file match | Task A outputs `config.py` → Task B imports it |
| **Import-based** | Module import analysis | `from utils import helper` → depends on utils |
| **Sequential** | Keyword detection | "based on", "after", "using result of" |

### L2 Example: Parallel Validators with Dependencies

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: email-validator
backend: codex
model: gpt-5.1-codex-max
workdir: ./utils
---CONTENT---
编写邮箱验证函数 (validators/email.py)
---END---
---TASK---
id: phone-validator
backend: codex
model: gpt-5.1-codex-max
workdir: ./utils
---CONTENT---
编写手机号验证函数 (validators/phone.py)
---END---
---TASK---
id: validator-index
backend: codex
model: gpt-5.1-codex-max
workdir: ./utils
dependencies: email-validator, phone-validator
---CONTENT---
创建 validators/__init__.py，导出所有验证函数
---END---
EOF
```

**Execution Flow:**
```
┌─────────────────┐  ┌─────────────────┐
│ email-validator │  │ phone-validator │  ← Parallel (no deps)
└────────┬────────┘  └────────┬────────┘
         │                    │
         └──────────┬─────────┘
                    ↓
         ┌─────────────────┐
         │ validator-index │  ← Sequential (depends on both)
         └─────────────────┘
```

---

## Task Decomposition Guide (L3+)

System automatically decomposes large tasks into manageable subtasks.

### How It Works

```
Input: Complex task description
         ↓
┌─────────────────────────────┐
│ 1. Analyze task scope       │
│ 2. Identify components      │
│ 3. Generate subtask list    │
│ 4. Establish dependencies   │
│ 5. Assign to parallel groups│
└─────────────────────────────┘
         ↓
Output: DAG of subtasks
```

### Decomposition Triggers

| Trigger | Detection | Action |
|---------|-----------|--------|
| **Multi-file** | "create X files", file list | Split by file |
| **Multi-component** | "module with A, B, C" | Split by component |
| **Layered** | "model, service, controller" | Split by layer |
| **Test + Impl** | "implement and test" | Split impl → test |

### L3 Example: HTTP Client with Auto-Decomposition

**Input Task:**
```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: http-client-module
backend: codex
model: gpt-5.2-codex
workdir: ./lib
timeout: 180
---CONTENT---
创建完整的 HTTP 客户端模块：
1. 核心客户端类 (http_client.py)
2. 重试策略 (retry.py)
3. 拦截器系统 (interceptors.py)
4. 单元测试 (test_http_client.py)
---END---
EOF
```

**Auto-Decomposed Execution:**
```
Phase 1 (Parallel - No deps):
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ http_client  │  │    retry     │  │   interceptors   │
│    .py       │  │    .py       │  │       .py        │
└──────┬───────┘  └──────┬───────┘  └────────┬─────────┘
       │                 │                   │
       └─────────────────┼───────────────────┘
                         ↓
Phase 2 (Sequential - Depends on all above):
              ┌─────────────────────┐
              │ test_http_client.py │
              └─────────────────────┘
```

### L4/L5 Example: Microservice with Full Decomposition

**Input Task:**
```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: auth-service
backend: codex
model: gpt-5.2
workdir: ./services/auth
timeout: 300
---CONTENT---
设计用户认证微服务：
- 数据模型 (models/)
- 业务逻辑 (services/)
- API 端点 (api/)
- 数据库迁移 (migrations/)
- 完整测试套件 (tests/)
---END---
EOF
```

**Auto-Decomposed Execution:**
```
Phase 1: Foundation (Parallel)
┌──────────┐  ┌──────────┐
│ models/  │  │ schemas/ │
│ user.py  │  │ auth.py  │
└────┬─────┘  └────┬─────┘
     │             │
     └──────┬──────┘
            ↓
Phase 2: Business Logic (Parallel, depends on Phase 1)
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ services/   │  │ services/   │  │ services/   │
│ auth.py     │  │ token.py    │  │ password.py │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        ↓
Phase 3: API Layer (Sequential, depends on Phase 2)
┌─────────────────────────────────┐
│ api/routes.py, api/middleware.py│
└────────────────┬────────────────┘
                 ↓
Phase 4: Database & Tests (Parallel, depends on Phase 3)
┌─────────────┐  ┌─────────────┐
│ migrations/ │  │   tests/    │
└─────────────┘  └─────────────┘
```

---

## Model Selection Guide

| Model | Best For | Complexity |
|-------|----------|------------|
| gpt-5.1-codex-mini | Simple scripts, quick fixes | ⭐ |
| gpt-5.1-codex-max | Utilities, production modules | ⭐⭐-⭐⭐⭐ |
| gpt-5.2-codex | Code review, refactoring, testing | ⭐⭐⭐ |
| gpt-5.2 | Complex algorithms, architecture | ⭐⭐⭐⭐-⭐⭐⭐⭐⭐ |

**Auto selection rules:**
- Model is automatically selected based on task complexity level
- Manual override available via `model` field when needed
- System optimizes for cost-efficiency while maintaining quality

---

## Complexity Levels Overview

### Level 1: Simple Scripts (⭐)

Quick utilities, single-file scripts (20-100 lines). Use `gpt-5.1-codex-mini`.

**Examples:** Batch file rename, CSV processing, disk monitoring

**Quick example:**
```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: batch-rename
backend: codex
model: gpt-5.1-codex-mini
workdir: /path/to/scripts
---CONTENT---
Python脚本：批量重命名文件，添加日期前缀
---END---
EOF
```

➜ **Detailed examples:** [examples/level1-simple-scripts.md](examples/level1-simple-scripts.md)

---

### Level 2: Utility Functions (⭐⭐)

Reusable functions, data transformations (100-300 lines). Use `gpt-5.1-codex-max`.

**Examples:** Data validators, format converters, simple unit tests

**Quick example:**
```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: validators
backend: codex
model: gpt-5.1-codex-max
workdir: /path/to/utils
---CONTENT---
编写邮箱、手机号、身份证号验证函数
---END---
EOF
```

➜ **Detailed examples:** [examples/level2-utilities.md](examples/level2-utilities.md)

---

### Level 3: Complete Modules (⭐⭐⭐)

Production-ready modules with error handling, logging, tests (300-800 lines). Use `gpt-5.2-codex`.

**Examples:** HTTP clients, database helpers, API wrappers

**Special tasks at Level 3:**
- **Code Review:** Analyze code for security/performance issues
- **Refactoring:** Apply design patterns, improve testability
- **Unit Testing:** Comprehensive test coverage (>80%)

**Quick example:**
```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: http-client
backend: codex
model: gpt-5.2-codex
workdir: /path/to/lib
timeout: 120
---CONTENT---
Python HTTP客户端：支持重试、超时、拦截器
---END---
EOF
```

**Code review example:**
```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: review
backend: codex
model: gpt-5.2-codex
files: ./src/auth.py
files-mode: ref
workdir: /path/to/project
---CONTENT---
审查代码：安全隐患、性能瓶颈、改进建议
---END---
EOF
```

➜ **Detailed examples:** [examples/level3-modules.md](examples/level3-modules.md)

---

### Level 4: Complex Algorithms (⭐⭐⭐⭐)

Advanced data structures, optimized algorithms (500-1500 lines). Use `gpt-5.2` with extended timeout.

**Examples:** Skip lists, pathfinding (Dijkstra, A*), expression parsers

**Quick example:**
```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: skiplist
backend: codex
model: gpt-5.2
workdir: /path/to/algorithms
timeout: 180
---CONTENT---
实现跳表：支持插入、删除、搜索，O(log n)复杂度
---END---
EOF
```

➜ **Detailed examples:** [examples/level4-algorithms.md](examples/level4-algorithms.md)

---

### Level 5: System Design & Architecture (⭐⭐⭐⭐⭐)

Multi-module projects, microservices, complete applications (2000+ lines). Use `gpt-5.2` with 300-600s timeout.

**Examples:** Authentication microservices, event-driven systems, full-stack apps

**Quick example:**
```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: auth-service
backend: codex
model: gpt-5.2
workdir: /path/to/services/auth
timeout: 300
---CONTENT---
设计用户认证微服务：JWT、OAuth2、RBAC权限模型
---END---
EOF
```

➜ **Detailed examples:** [examples/level5-architecture.md](examples/level5-architecture.md)

---

## Basic Usage

### Single Task

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: task-id
backend: codex
workdir: /working/directory
model: gpt-5.2-codex
---CONTENT---
[Your task description]
---END---
EOF
```

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Unique task identifier | `impl-auth`, `test-validators` |
| `backend` | Always `codex` for code generation | `codex` |
| `workdir` | Working directory path | `./src`, `/home/user/project` |

### Optional Fields

| Field | Default | Description |
|-------|---------|-------------|
| `model` | gpt-5.2-codex | Model selection (see complexity guide) |
| `timeout` | 300 | Max execution time (seconds) |
| `dependencies` | - | Comma-separated task IDs |
| `files` | - | Source files to reference |
| `files-mode` | ref | `ref` (path only) - unified across all levels |
| `retry` | 0 | Retry count on failure |

---

## Quick Reference

### Complexity Decision Tree

```
Start
  ├─ Single file, <100 lines? → Level 1 (codex-mini)
  ├─ Reusable functions, no external deps? → Level 2 (codex)
  ├─ Production module with tests?
  │   ├─ Standard CRUD/API? → Level 3 (codex-max)
  │   └─ Complex algorithm? → Level 4 (gpt-5.2)
  └─ Multi-module/microservice? → Level 5 (gpt-5.2)
```

### Task Type Classification

| Task Type | Level | Model | Example Link |
|-----------|-------|-------|--------------|
| Batch rename script | 1 | codex-mini | [Level 1](examples/level1-simple-scripts.md) |
| Email validator | 2 | codex-max | [Level 2](examples/level2-utilities.md) |
| HTTP client with retry | 3 | gpt-5.2-codex | [Level 3](examples/level3-modules.md) |
| Code review | 3 | gpt-5.2-codex | [Level 3](examples/level3-modules.md#code-quality-tasks) |
| Refactoring | 3-4 | gpt-5.2-codex / gpt-5.2 | [Level 3](examples/level3-modules.md#example-4-refactoring) |
| Unit testing | 2-3 | codex-max / gpt-5.2-codex | [Level 3](examples/level3-modules.md#example-5-comprehensive-unit-testing) |
| Skip list algorithm | 4 | gpt-5.2 | [Level 4](examples/level4-algorithms.md) |
| Auth microservice | 5 | gpt-5.2 | [Level 5](examples/level5-architecture.md) |

---

## Additional Resources

### Progressive Disclosure Documentation

- **[HOW_TO_USE.md](HOW_TO_USE.md)** - Complete usage guide
  - When to use this skill
  - Relationship with memex-cli
  - Model selection tips
  - Workflow references

- **[references/complexity-guide.md](references/complexity-guide.md)** - Detailed complexity selection
  - In-depth explanation of 5 levels
  - Model performance comparison
  - Decision tree and classification
  - Best practices by task type

- **[examples/](examples/)** - Runnable code examples
  - [level1-simple-scripts.md](examples/level1-simple-scripts.md) - Quick utilities
  - [level2-utilities.md](examples/level2-utilities.md) - Reusable functions
  - [level3-modules.md](examples/level3-modules.md) - Production modules, code review, refactoring
  - [level4-algorithms.md](examples/level4-algorithms.md) - Complex algorithms
  - [level5-architecture.md](examples/level5-architecture.md) - System design

### Advanced Workflows

For multi-task workflows, parallel execution, and resume functionality, refer to memex-cli skill:

- **Multi-task DAG workflows:** [memex-cli/references/advanced-usage.md](../memex-cli/references/advanced-usage.md)
- **Parallel execution patterns:** [memex-cli/examples/parallel-tasks.md](../memex-cli/examples/parallel-tasks.md)
- **Resume interrupted runs:** [memex-cli/examples/resume-workflow.md](../memex-cli/examples/resume-workflow.md)

---

## Tips

1. **Match model to task complexity**
   - Start with lightweight models for simple tasks
   - Upgrade to powerful models only when needed
   - Save costs by not over-provisioning

2. **Use files for context**
   - Code review: `files: ./src/auth.py` (files-mode defaults to `ref`)
   - Refactoring: Reference source files for analysis
   - Unit testing: Reference module to test

3. **Break down large tasks**
   - Split Level 5 projects into parallel Level 3-4 subtasks
   - Use DAG workflows for dependencies
   - See [memex-cli advanced usage](../memex-cli/references/advanced-usage.md)

4. **Include context in prompts**
   - Specify language, framework, coding standards
   - Mention target Python/Node.js version
   - Include expected output format

5. **Leverage examples**
   - Browse [examples/](examples/) directory for similar tasks
   - Copy and customize example commands
   - Follow established patterns

---

## SKILL Reference

- [skills/memex-cli/SKILL.md](../memex-cli/SKILL.md) - Memex CLI full documentation
- [HOW_TO_USE.md](HOW_TO_USE.md) - Detailed usage guide for this skill
