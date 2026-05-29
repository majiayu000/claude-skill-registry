---
name: sync-comparisons
description: Sync cross-agent comparison (Dimension 8) across all analysis docs
---

# Sync Comparisons

Update Dimension 8 (Cross-Agent Comparison) sections across all analysis docs so every analyzed agent references every other analyzed agent.

## Trigger

- `/sync-comparisons` — sync all analyzed agents' Dimension 8
- `/sync-comparisons <agent>` — only update the specified agent's Dimension 8

## Prerequisites

At least 2 analyzed agents must exist (`docs/*.md` excluding `TEMPLATE.md`).

## Workflow

### 1. Collect Analyzed Agents

List all `docs/*.md` files (exclude `TEMPLATE.md`). Each filename `docs/<name>.md` corresponds to an analyzed agent. Verify the file has substantive content (not just an empty template).

### 2. Read Core Characteristics

For each analyzed agent's doc, extract key traits from these dimensions:

| Source Dimension | What to Extract |
|------------------|-----------------|
| Dimension 1 (Overview) | 语言、架构定位、项目类型 |
| Dimension 2 (Agent Loop) | 循环模式（单轮/多轮/事件驱动） |
| Dimension 3 (Tool 系统) | 工具注册/调用机制 |
| Dimension 5 (Context 策略) | 上下文管理方式 |
| Dimension 6 (错误处理) | 错误恢复策略 |
| Dimension 7 (关键创新) | 核心特色/独特设计 |

### 3. Check Coverage

For each agent (or the specified agent), check its Dimension 8 section (`## 8.` to next `##` or EOF):
- Which other analyzed agents are already referenced?
- Which are missing?

If all agents are already covered, report "already up to date" and skip.

### 4. Update Missing References

For each agent with missing references in Dimension 8:

- **If Dimension 8 only has generic comparison** (e.g. "vs 通用 Agent 模式" without referencing specific agents): replace with concrete comparisons against all analyzed agents
- **If Dimension 8 already has some agent comparisons but is missing others**: add the missing agents to the existing comparison structure
- **Preserve existing content**: do not modify or remove existing comparison text, only **add** missing agent columns/sections

### 5. Comparison Format

Use a multi-column comparison table when the number of agents (including self) is **4 or fewer**:

```markdown
| 维度 | agent-a | agent-b | agent-c |
|------|---------|---------|---------|
| 语言 | Python | Rust | TypeScript |
| Agent Loop | ... | ... | ... |
| Tool 系统 | ... | ... | ... |
| Context 策略 | ... | ... | ... |
| 编辑方式 | ... | ... | ... |
| 安全/错误处理 | ... | ... | ... |
| 扩展性 | ... | ... | ... |
| LLM 支持 | ... | ... | ... |
```

When agents exceed 4, use multiple **pairwise "vs" sections** instead:

```markdown
### vs agent-b

（对比要点...）

### vs agent-c

（对比要点...）
```

### 6. Update Summary

After the comparison table/sections, update or add a summary paragraph that:
- Highlights the most significant differences
- Notes complementary strengths
- Covers all compared agents (not just the newly added ones)

## Comparison Dimensions

The comparison should cover these aspects (as table rows or discussion points):

| 维度 | 说明 |
|------|------|
| 语言 | 实现语言和技术栈 |
| Agent Loop | 循环架构（单轮请求/多轮对话/事件驱动/ReAct） |
| Tool 系统 | 工具定义、注册、调用方式 |
| Context 策略 | 上下文窗口管理（截断/压缩/摘要/repomap） |
| 编辑方式 | 代码编辑策略（search-replace/diff/whole-file/patch） |
| 安全/错误处理 | 权限控制、沙箱、错误恢复 |
| 扩展性 | 插件/扩展机制 |
| LLM 支持 | 支持的模型和切换方式 |

## Output Requirements

- Write in Chinese, code identifiers in English (matching project conventions)
- Focus on **differences**, not feature lists — describe how each agent's approach differs
- Reference `docs/codex-cli.md` Dimension 8 as a style reference for good comparison tables
- Each comparison point should be concise (1-2 sentences per cell)

## After Sync

1. Run `npm run lint` to verify check #6 (跨 Agent 对比覆盖) passes
2. No need to update `agents.yaml` status — this is a doc maintenance task
