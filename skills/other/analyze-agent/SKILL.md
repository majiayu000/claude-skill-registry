---
name: analyze-agent
description: Systematically analyze an AI agent's source code across 8 core + 4 optional platform dimensions and output structured analysis to docs/<agent>.md
---

# Analyze Agent

Deep-dive analysis of an AI agent's implementation. Reads the agent's source code from `projects/<agent>/` and fills `docs/<agent>.md` using the 8+4 dimension template.

## Trigger

`/analyze-agent <agent-name>`

## Prerequisites

1. The agent's source code must exist at `projects/<agent-name>/`（run `./scripts/manage-submodules.sh add <agent-name>` if not present）
2. The analysis doc `docs/<agent-name>.md` should exist（run `./scripts/new-analysis.sh <agent-name>` if not present）

## Analysis Framework

Analyze the agent across 8 core dimensions (always), plus 4 optional platform dimensions (when applicable).

### Platform Detection

Before starting analysis, check if this is a platform-level agent:
- Read `agents.yaml` for `type: agent-platform` field
- Or detect signals: multi-channel support, gateway architecture, scheduling, persistent memory, companion apps
- If platform agent: fill D1-D12
- If pure coding agent: fill D1-D8 only, delete or mark D9-D12 as "不适用"

### Core Agent Reference

If the platform agent's core coding engine is another agent already analyzed (e.g., OpenClaw uses pi-agent):
- D2-D6 should **reference** the existing analysis (link to `docs/<core-agent>.md`)
- Focus on **customizations and extensions** the platform makes to the core (tool injection, prompt overlay, security overrides)
- Do NOT duplicate the core agent's analysis content

### Dimension 1: Overview & Architecture

- **Goal**: Understand what this agent is, its tech stack, and high-level architecture
- **Strategy**: Read `README.md`, `setup.py`/`pyproject.toml`/`package.json`, entry point files (`main.py`, `__main__.py`, `index.ts`, `cli.ts`)
- **Output**: Project positioning, tech stack, architecture diagram (ASCII/Mermaid), key files table

### Dimension 2: Agent Loop

- **Goal**: Understand the main event loop: input → think → act → observe → ...
- **Strategy**: Find the main loop by searching for patterns: `while`, `loop`, `run()`, `run_one()`, `step()`, `execute()`. Trace from entry point to the core loop.
- **Output**: Loop flow description, termination conditions, key code snippet

### Dimension 3: Tool/Action System

- **Goal**: Understand how tools are defined, registered, and invoked
- **Strategy**: Search for tool registration patterns: decorators (`@tool`, `@command`), registries, command maps. List all available tools/commands.
- **Output**: Registration mechanism, tool list table, tool invocation flow

### Dimension 4: Prompt Engineering

- **Goal**: Understand system prompt structure and dynamic assembly
- **Strategy**: Search for files named `*prompt*`, `*system*`, `*template*`. Find where prompts are assembled and sent to LLM.
- **Output**: System prompt structure, dynamic parts, template file paths

### Dimension 5: Context Management

- **Goal**: Understand how the agent manages limited context window
- **Strategy**: Search for context/window/token management, file selection strategies, history truncation/compression. Look for `repomap`, `summary`, `compress`, `truncat`.
- **Output**: Context window strategy, file/code context strategy, conversation history management

### Dimension 6: Error Handling & Recovery

- **Goal**: Understand how the agent handles LLM output parsing errors, tool failures, and retries
- **Strategy**: Search for `retry`, `error`, `exception`, `fallback`, `recover`. Check how malformed LLM output is handled.
- **Output**: LLM output parsing errors, tool execution failures, retry mechanism

### Dimension 7: Key Innovations

- **Goal**: Identify unique designs and patterns worth borrowing
- **Strategy**: Based on findings from dimensions 1-6, highlight what makes this agent special. Check README for claimed features.
- **Output**: Unique designs, reusable patterns

### Dimension 7.5: MVP Component Map

- **Goal**: 识别构建最小可运行版本需要的组件集合
- **Strategy**: 基于 D1-D7（及 D9-D12 如适用）的发现，对照以下参考类目映射：
  1. 主循环（D2）
  2. Tool 注册与分发（D3）
  3. Prompt 组装（D4）
  4. LLM 调用与响应解析（D2/D6）
  5. 编辑应用（D3）
  平台型 agent 额外参考：
  6. 通道路由（D9）
  7. 记忆检索（D10）
  8. 安全沙箱（D11）
  根据 agent 实际架构调整类目（合并/拆分/新增均可）
- **Language Decision**: 对每个组件判断 Python 是否足够，还是必须用原生语言
  规则：仅当机制根本依赖语言特性时（async runtime、类型系统、FFI、平台 API）才用原生语言
- **Output**: 填写 docs 中 7.5 节的 MVP 组件表

### Dimension 8: Cross-Agent Comparison

- **Goal**: Compare with other analyzed agents
- **Strategy**: Reference existing docs in `docs/` directory. If this is the first agent analyzed, note "first agent" and compare with general patterns.
- **Output**: Comparison table, summary paragraph

### Dimension 9: Channels & Gateway _(platform only)_

- **Goal**: Understand how external channels route messages to the agent
- **Strategy**: Find gateway/server entry points, channel adapters, message normalization layers. Search for `channel`, `gateway`, `webhook`, `socket`, `route`.
- **Output**: Channel architecture, supported channels table, message normalization, multi-modal support (voice, canvas, etc.)

### Dimension 10: Memory & Persistence _(platform only)_

- **Goal**: Understand cross-session memory and persistent storage (distinct from D5 which covers within-session context window)
- **Strategy**: Find storage backends (JSONL, SQLite, vector DB), memory retrieval (embedding search, BM25), session branching. Search for `memory`, `persist`, `store`, `vector`, `embed`, `session`.
- **Output**: Persistence architecture, long-term memory retrieval strategy, state recovery

### Dimension 11: Security Model & Autonomy _(platform only)_

- **Goal**: Understand trust levels, sandboxing, and autonomous execution
- **Strategy**: Find permission gating, Docker/sandbox isolation, scheduling (cron, heartbeat). Search for `permission`, `trust`, `sandbox`, `docker`, `cron`, `schedule`, `agent-to-agent`.
- **Output**: Trust levels, sandboxing strategy, autonomous scheduling, multi-agent collaboration

### Dimension 12: Other Notable Mechanisms _(platform only)_

- **Goal**: Capture unique mechanisms that don't fit D9-D11
- **Strategy**: Review remaining unique features: skills marketplace, companion apps, special UI modes, deployment architecture, onboarding flows. Cross-reference with D7 to avoid duplication.
- **Output**: Mechanism list table, detailed analysis of each

## Key File Discovery Strategy

For each language ecosystem, use these heuristics to find critical files:

**Python agents:**
- Entry: `**/main.py`, `**/__main__.py`, `**/cli.py`
- Config: `setup.py`, `pyproject.toml`, `setup.cfg`
- Core: `**/agent.py`, `**/coder*.py`, `**/runner.py`

**TypeScript/JavaScript agents:**
- Entry: `**/index.ts`, `**/main.ts`, `**/cli.ts`
- Config: `package.json`, `tsconfig.json`
- Core: `**/agent.ts`, `**/core/**`, `**/lib/**`

**Rust agents:**
- Entry: `**/main.rs`, `**/lib.rs`
- Config: `Cargo.toml`
- Core: `**/agent/**`, `**/core/**`

## Output Requirements

1. Fill all 8 core sections in `docs/<agent-name>.md`; for platform agents, also fill D9-D12
2. Include actual code snippets (key fragments, not entire files)
3. Architecture diagram should be ASCII or Mermaid
4. Tool list should be comprehensive
5. Write in Chinese (matching the template style), code/identifiers stay in English
6. Remove all `<!-- comment -->` placeholders and replace with actual content
7. For platform agents referencing a core coding engine: link to existing analysis for D2-D6, focus on customizations

## After Analysis

1. Create or update the demo overview at `demos/<agent-name>/README.md` using the template from `demos/TEMPLATE/AGENT_OVERVIEW.md`（三段式或四段式结构）：
   - MVP 组件: 从 7.5 节表格导出，注明语言
   - 平台机制 _(仅平台型 agent)_: 从 D9-D12 提取值得复现的机制
   - 进阶机制: D7 中值得复现的特色机制
   - 完整串联: mini-<agent> 占位
2. Update `agents.yaml`: change the agent's `status` from `pending` to `in-progress`（分析完成但还没创建 demo）or `done`（全部完成）
3. **Stamp analyzed commit**: read `projects/<agent-name>/` HEAD (`git -C projects/<agent-name> rev-parse HEAD`), update `agents.yaml` with `analyzed_commit` and `analyzed_date` (today's date), and update `docs/<agent-name>.md` header's `> Analyzed at commit:` line
4. Run `npm run progress` to update the CLAUDE.md progress section (or it will auto-update on next commit)
5. Check cross-agent comparison coverage: scan all other `docs/*.md` files (excluding TEMPLATE.md) that have completed analysis. List which docs' Dimension 8 sections do NOT reference the newly analyzed agent. Print a reminder like:

   > 以下文档的跨 Agent 对比（Dimension 8）尚未引用 <new-agent>，建议运行 `/sync-comparisons`：
   > - docs/aider.md
   > - docs/pi-agent.md
