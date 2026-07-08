---
name: agf-code-map
description: Deeply Understand (codemap) — 持久化代码图谱 + 变更影响分析 + 理解地图。接手遗留项目 Day-1 / PR 影响分析 / 解释陌生代码 / PRD·ADR 前现状理解时用。编排 tools/codemap/ 的 codemap CLI
---

# agf-code-map（Deeply Understand / codemap）

[ADR-021](../../../docs/adr/021-code-understanding-engine.md) Deeply Understand 代码理解引擎的 AGF 入口。Python 原生（`tools/codemap/`），SQLite 持久图谱 + tree-sitter 多语言 + 反向 BFS 影响分析 + 静态 HTML dashboard。**替换 `agf-understand`**（M8 验证后删 `agf-understand.js`）。

## 何时用

- **接手遗留项目 Day-1**：`codemap build` + `onboard` + `dashboard`
- **PR / 改动影响分析**：`codemap diff`（→ code-reviewer 审查清单）
- **解释陌生文件/函数**：`codemap explain`
- **PRD/ADR 前现状理解**：`codemap understand`（接管 agf-understand 的理解地图）

## 命令（tools/codemap/ 下 `uv run codemap <subcmd>`）

- `build [path]` — 全量建图 → `.agf/code-map.db`
- `update` — 增量（git diff + 双指纹）
- `diff [--base <ref>] [--hop N]` — 变更影响分析（反向 import BFS + 风险评分）
- `explain <target>` — 节点深度解释（邻居 + 源码片段）
- `onboard` — 项目概览 + 复杂度热点 + 高扇入
- `understand [topic]` — 理解地图（目录子系统 + 核心依赖 + 风险点）
- `context "<query>"` — 相关子图（给 agent 注入）
- `search "<query>"` — 检索（默认 FTS5 关键词；跑过 `embed` 后自动启用 semantic 余弦，三态降级）
- `embed` — 生成节点 embedding 存 `.agf/code-map.db`（需 `uv sync --extra semantic`；jina-code-v2，首次下载 ~90MB + torch；未装/未跑则 search 自动降级 FTS，功能不中断）
- `dashboard [--out <path>]` — 静态 HTML 图（cytoscape，浏览器 open）

## 语言覆盖

首发 7 语言：Python / TS / JS / SQL / YAML / JSON / Java（04 设计）。Swift/WXML 诚实缺口（04 §6）。

## 纪律（08）

- DU 是**事实层**（确定性代码事实），**不碰** `docs/specs/` / `docs/adr/` / `docs/design/DESIGN.md` / OpenAPI 契约
- 产物 `.agf/*` gitignored（派生缓存，可重建）；消费层报告落 `docs/reviews/`
- DU **不投票** verdict（ADR-010 不变）——给 reviewer 事实参考，verdict 仍从 findings 推导
