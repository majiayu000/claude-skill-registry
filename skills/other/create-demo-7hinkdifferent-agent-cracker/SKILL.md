---
name: create-demo
description: Create a minimal reproduction demo for a specific mechanism from an analyzed AI agent (coding or platform)
---

# Create Demo

Create a standalone, minimal demo that reproduces a single core mechanism from an analyzed AI agent. Supports both coding agent mechanisms (D2-D7) and platform mechanisms (D9-D12).

## Trigger

`/create-demo <agent-name> <mechanism>`

Example: `/create-demo aider repomap`
Example: `/create-demo openclaw channel-router`

## Prerequisites

1. Analysis doc must exist at `docs/<agent-name>.md` (run `/analyze-agent` first)
2. The mechanism must be identified in the analysis doc (D2-D7 for coding, D9-D12 for platform)

## Workflow

### Step 1: Read Analysis

Read `docs/<agent-name>.md` and identify the target mechanism:
- What problem does it solve?
- What's the core algorithm/flow?
- What are the key data structures?
- What dependencies does the original use?

### Step 2: Design Simplification

Apply these simplification principles:
- **Single mechanism**: Focus on ONE mechanism only, remove all others
- **Minimal dependencies**: Use the fewest possible libraries
- **No infrastructure**: Remove git integration, database caching, CLI frameworks, config systems
- **Hardcode when possible**: Replace configurable options with sensible defaults
- **语言选择**: 默认 Python。当机制依赖语言特性时用原生语言，README 须含 "为何选择此语言" 节
- **Simple I/O**: Print to stdout, no rich formatting or interactive prompts
- **Inline over import**: If a helper is < 20 lines, inline it rather than importing from another demo

### Step 3: Create File Structure

Create `demos/<agent-name>/<mechanism>/` with the structure matching the chosen language:

**Python:**
```
demos/<agent-name>/<mechanism>/
├── README.md           # From template, filled in
├── requirements.txt    # Only if external deps needed (not for stdlib-only demos)
├── main.py             # Entry point (or split into logical modules)
└── sample_*/           # Sample data/project if needed for demonstration
```

**TypeScript:**
```
demos/<agent-name>/<mechanism>/
├── README.md           # From template, filled in
├── package.json        # Dependencies
├── tsconfig.json       # TypeScript config
├── main.ts             # Entry point
└── sample_*/           # Sample data/project if needed for demonstration
```

**Rust:**
```
demos/<agent-name>/<mechanism>/
├── README.md           # From template, filled in
├── Cargo.toml          # Project config & dependencies
├── src/
│   └── main.rs         # Entry point
└── sample_*/           # Sample data/project if needed for demonstration
```

### Step 4: Write README

Use the template from `demos/TEMPLATE/README.md` and fill in:
- **Goal**: One sentence describing what this demo reproduces
- **原理**: How the mechanism works in the original agent (2-3 paragraphs)
- **运行**: Exact commands to run the demo
- **文件结构**: Actual file tree
- **关键代码解读**: Core algorithm with inline comments
- **与原实现的差异**: What was simplified and what was preserved
- **相关文档**: Must include `基于 commit: <short-sha>` and `核心源码: <原项目中对应的文件路径>` (the source path is used by `/check-updates` to match changes)

### Step 5: Implement Core Logic

Guidelines:
- Target ~100-200 lines of core logic per demo
- LLM 调用按语言选择对应库和运行方式：

| 语言 | 版本要求 | 运行工具 | 运行方式 | LLM 库 | 模型变量 |
|------|---------|---------|---------|--------|---------|
| Python | ≥3.10 | uv | `uv run --with <deps> python main.py` | litellm | `DEMO_MODEL` |
| TypeScript | Node ≥18 | npx | `npx tsx main.ts` | openai SDK | `DEMO_MODEL` |
| Rust | stable | cargo | `cargo run` | reqwest | `DEMO_MODEL` |

- Each demo must be independently runnable
- Include sample data/projects so the demo works out of the box
- Add clear print statements showing what's happening at each step

### Step 5.5: Complete Integration Demo (mini-agent)

When all MVP component demos (and platform mechanism demos if applicable) for an agent are complete, create a combined integration demo:

- **目录**: `demos/<agent>/mini-<agent>/`
- **目标**: 串联所有 MVP 组件（+ 平台机制 demo，如适用）为一个最简可运行 agent
- **核心原则**: **必须 import 兄弟 MVP/平台 demo 的模块**，而非把所有代码重写到一个文件中。mini-agent 本身只实现 Core Loop 逻辑，其余能力全部通过 import 复用
- **行数**: mini-agent 自身 100-200 行（不含导入的模块）
- **前提**: 所有 MVP 组件 demo 已完成；平台型 agent 的平台机制 demo 也需完成
- **语言**: 与多数 MVP 组件一致（混合则用 Python）
- **平台型 agent 特别说明**: 串联 demo 应体现完整的消息流路径——从通道接入到 agent 执行再到响应返回，而非只串联编码部分

**模块提取约定**:
- 每个 MVP demo 应将核心逻辑提取到独立模块文件（如 `prompt-assembly/assembler.py`）
- `main.py` 保留 demo 演示代码，从模块 import 核心类/函数
- mini-agent 通过 `sys.path` 添加兄弟目录来 import 这些模块

**示例（aider）**:
```python
# mini-aider/main.py
from assembler import PromptAssembler       # ← prompt-assembly/
from parser import find_edit_blocks         # ← search-replace/
from replacer import apply_edit             # ← search-replace/
from parsers import generate_reflection     # ← llm-response-parsing/
```

### Step 6: Verify

Run the demo and confirm:
- It executes without errors
- It demonstrates the core mechanism clearly
- Output is understandable to someone learning the mechanism

## Code Style

- Use type hints for function signatures
- Add docstrings for the main functions explaining the mechanism
- Keep classes minimal — prefer functions unless state management is essential
- Name variables to match the original codebase's terminology where possible

## Output

The completed demo directory at `demos/<agent-name>/<mechanism>/`.

## After Creating Demo

1. Update the agent's overview at `demos/<agent-name>/README.md`: mark the mechanism as `[x]` and update the progress line. Format:
   - Coding agents: `MVP: X/N | 进阶: Y/M | 串联: Z/1 | 总计: A/K`
   - Platform agents: `MVP: X/N | 平台: P/Q | 进阶: Y/M | 串联: Z/1 | 总计: A/K`
2. Update `agents.yaml` status if needed (e.g. `pending` → `in-progress`)
3. Run `npm run progress` to update the CLAUDE.md progress section (or it will auto-update on next commit)
4. Confirm the demo README's "相关文档" section includes `基于 commit: <short-sha>` (read from `agents.yaml` `analyzed_commit`). This provides a baseline for `/check-updates` demo impact assessment.
