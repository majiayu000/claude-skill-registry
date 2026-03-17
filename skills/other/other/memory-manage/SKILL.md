---
name: memory-manage
description: Unified memory management - CLAUDE.md updates and documentation generation with interactive routing. Triggers on "memory manage", "update claude", "update memory", "generate docs", "更新记忆", "生成文档".
allowed-tools: Task(*), Bash(*), AskUserQuestion(*), Read(*)
---

# Memory Management Skill

Unified entry point for project memory (CLAUDE.md) updates and documentation (API.md/README.md) generation. Routes to specialized sub-commands via arguments or interactive needs assessment.

## Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│  Memory Manage (Router)                               │
│  → Parse input → Detect mode → Route to phase         │
└───────────────┬──────────────────────────────────────┘
                │
        ┌───────┴───────┐
        ↓               ↓
  ┌───────────┐   ┌───────────┐
  │ CLAUDE.md │   │  Docs     │
  │  管理     │   │  生成     │
  └─────┬─────┘   └─────┬─────┘
        │               │
   ┌────┼────┐     ┌────┴────┐
   ↓    ↓    ↓     ↓         ↓
 Full Related Single Full  Related
 全量  增量   单模块  全量    增量
```

## Execution Flow

### Step 1: Parse Input & Route

Detect execution mode from user input:

**Auto-Route Rules** (priority order):

| Signal | Route | Examples |
|--------|-------|---------|
| Explicit sub-command token | → Direct dispatch | `update-full --tool qwen` |
| Keyword: full, 全量, all, entire + update/claude | → update-full | "全量更新claude" |
| Keyword: related, changed, 增量, diff + update/claude | → update-related | "更新变更模块" |
| Keyword: single, module, 单模块 + path-like token | → update-single | "更新 src/auth 模块" |
| Keyword: docs, documentation, 文档 + full/all/全量 | → docs-full | "全量生成文档" |
| Keyword: docs, documentation, 文档 + related/changed/增量 | → docs-related | "增量生成文档" |
| Ambiguous or no arguments | → **AskUserQuestion** | `/memory-manage` |

Valid sub-command tokens: `update-full`, `update-related`, `update-single`, `docs-full`, `docs-related`

**Direct dispatch examples**:
```
input = "update-full --tool qwen"
  → subcommand = "update-full", remainingArgs = "--tool qwen"
  → Read phases/01-update-full.md, execute

input = "update-single src/auth --tool gemini"
  → subcommand = "update-single", remainingArgs = "src/auth --tool gemini"
  → Read phases/03-update-single.md, execute
```

**When ambiguous or no arguments**, proceed to Step 2.

### Step 2: Interactive Needs Assessment

**Q1 — 确定内容类别**:

```
AskUserQuestion({
  questions: [{
    question: "你要管理哪类内容？",
    header: "类别",
    multiSelect: false,
    options: [
      {
        label: "CLAUDE.md (项目记忆)",
        description: "更新模块指令文件，帮助Claude理解代码库结构和约定"
      },
      {
        label: "项目文档 (API+README)",
        description: "生成API.md和README.md到.workflow/docs/目录"
      }
    ]
  }]
})
```

**Q2a — CLAUDE.md 管理范围** (用户选了 CLAUDE.md):

```
AskUserQuestion({
  questions: [{
    question: "CLAUDE.md 更新范围？",
    header: "范围",
    multiSelect: false,
    options: [
      {
        label: "增量更新 (Recommended)",
        description: "仅更新git变更模块及其父级，日常开发首选"
      },
      {
        label: "全量更新",
        description: "更新所有模块，3层架构bottom-up，适合重大重构后"
      },
      {
        label: "单模块更新",
        description: "指定一个模块，Explore深度分析后生成说明书式文档"
      }
    ]
  }]
})
```

Route mapping:
- "增量更新" → `update-related` → Ref: phases/02-update-related.md
- "全量更新" → `update-full` → Ref: phases/01-update-full.md
- "单模块更新" → `update-single` → continue to Q3

**Q2b — 文档生成范围** (用户选了项目文档):

```
AskUserQuestion({
  questions: [{
    question: "文档生成范围？",
    header: "范围",
    multiSelect: false,
    options: [
      {
        label: "增量生成 (Recommended)",
        description: "仅为git变更模块生成/更新文档，日常开发首选"
      },
      {
        label: "全量生成",
        description: "所有模块+项目级文档(ARCHITECTURE.md等)，适合初始化"
      }
    ]
  }]
})
```

Route mapping:
- "增量生成" → `docs-related` → Ref: phases/05-docs-related.md
- "全量生成" → `docs-full` → Ref: phases/04-docs-full.md

**Q3 — 补充路径** (仅 update-single 需要，且无路径参数时):

```
AskUserQuestion({
  questions: [{
    question: "请指定要更新的模块路径：",
    header: "路径",
    multiSelect: false,
    options: [
      {
        label: "src",
        description: "src 目录"
      },
      {
        label: ".",
        description: "项目根目录"
      }
    ]
  }]
})
```

用户可选 "Other" 输入自定义路径。

### Step 3: Execute Selected Phase

Based on routing result, read and execute the corresponding phase:

**Phase Reference Documents** (read on-demand when phase executes):

| Mode | Document | Purpose |
|------|----------|---------|
| update-full | [phases/01-update-full.md](phases/01-update-full.md) | Full CLAUDE.md update, 3-layer architecture, batched agents |
| update-related | [phases/02-update-related.md](phases/02-update-related.md) | Git-changed CLAUDE.md update, depth-first |
| update-single | [phases/03-update-single.md](phases/03-update-single.md) | Single module CLAUDE.md, Explore + handbook style |
| docs-full | [phases/04-docs-full.md](phases/04-docs-full.md) | Full API.md + README.md generation |
| docs-related | [phases/05-docs-related.md](phases/05-docs-related.md) | Git-changed docs generation, incremental |

## Shared Configuration

### Tool Fallback Hierarchy

All sub-commands share the same fallback:

```
--tool gemini  →  [gemini, qwen, codex]  // default
--tool qwen    →  [qwen, gemini, codex]
--tool codex   →  [codex, gemini, qwen]
```

### Common Parameters

| Parameter | Description | Default | Used By |
|-----------|-------------|---------|---------|
| `--tool <gemini\|qwen\|codex>` | Primary CLI tool | gemini | All |
| `--path <dir>` | Target directory | . | update-full, docs-full |
| `<path>` (positional) | Module path | _(required)_ | update-single |

### Batching Thresholds

| Sub-Command | Direct Execution | Agent Batch | Batch Size |
|-------------|-----------------|-------------|------------|
| update-full | <20 modules | ≥20 modules | 4/agent |
| update-related | <15 modules | ≥15 modules | 4/agent |
| update-single | always single | N/A | 1 |
| docs-full | <20 modules | ≥20 modules | 4/agent |
| docs-related | <15 modules | ≥15 modules | 4/agent |

## Core Rules

1. **Route before execute**: Determine sub-command before any execution
2. **Phase doc is truth**: All execution logic lives in phase docs, router only dispatches
3. **Read on-demand**: Only read the selected phase doc, never load all
4. **Pass arguments through**: Forward remaining args unchanged to sub-command
5. **User confirmation**: Each sub-command handles its own plan presentation and y/n confirmation

## Error Handling

| Error | Resolution |
|-------|------------|
| Unknown sub-command | Fall through to interactive flow |
| Phase doc not found | Abort with file path error |
| Missing path for update-single | Prompt via Q3 |
| Sub-command execution fails | Follow phase doc's own error handling |
