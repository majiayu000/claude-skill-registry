---
name: ohspec
description: Use when 需要生成 RFC 技术规范、进行需求分析、设计 API 契约，或需要 OHSpec 多代理编排输出。Triggers on "RFC", "需求分析", "API 契约", "设计规范", "OHSpec", "/ohspec".
allowed-tools: Task, AskUserQuestion, Read, Write, Glob, Grep, Bash
---

# OHSpec - 需求分析与设计规范

AI辅助需求分析与设计规范生成，强调多代理编排、结构化产物和质量门禁。

## Architecture
架构概览与职责划分。

```
+-------------------------------------------------------------------+
| Orchestrator (你)                                                  |
| - 协调流程 / 复杂度路由 / 质量门禁 / 维护三文件                     |
+-------------------------------+-----------------------------------+
| Subagents                     | Artifacts                         |
| Dispatcher / 需求分析师 /     | rfc.md / findings.json /           |
| 架构设计师 / 质量审查员       | progress.json                      |
+-------------------------------+-----------------------------------+
| Optional export: /ohspec:export -> rfc.digest.json + tasks.json    |
+-------------------------------------------------------------------+
```

**角色职责**：
1. 协调工作流：启动专家子代理，管理阶段转换，确保质量门禁
2. 委托执行：优先委托（Claude Code/Task 子代理环境）；Task 不可用时启用 Codex 兼容回退
3. 管理上下文：将繁重工作委托给子代理，保持主上下文清洁
4. 确保质量：执行强制检查，验证输出，维护 RFC 标准

**关键产物**：`rfc.md`、`findings.json`、`progress.json`（三文件是 scan-of-record 与质量审计入口）。

## Execution Flow

```
用户需求
  -> 初始化三文件（rfc.md/findings.json/progress.json）
  -> PRECHECK：快速需求预检（30秒过滤不可行需求）
  -> ASSESS：确定工具与 scan scope，写入 progress.json + audit_log
  -> 快速意图澄清（≤2问题，确保扫描准确性）
  -> Dispatcher 基线扫描（scan-of-record）
  -> 深度技术澄清（基于扫描结果）
  -> 复杂度路由 + 路由信号
  -> analyze -> design -> precheck -> audit
  -> RFC 输出
  -> 可选 /ohspec:export 生成机读件
```

**复杂度路由**：
| 级别 | 特征 | 模式 |
|------|------|------|
| SIMPLE | 单文件，<50行 | 快速通道 |
| MEDIUM | 多文件，单子系统 | 标准流程 |
| COMPLEX | 跨子系统，架构级 | 完整流程 + spike |

**路由信号**：
| 信号 | 动作 |
|------|------|
| `SKIP_ANALYZE` | 需求明确、单文件 → 跳过 analyze |
| `LOAD_DIPLOMAT` | 跨子系统依赖 → 加载 Diplomat |
| `TRIGGER_SPIKE` | 技术不确定 → 触发 Spike |
| `SIMPLIFY_CLARIFY` | 详细需求 → 简化澄清 |

## ⚠️ Mandatory Prerequisites

> **⛔ 禁止跳过**：在执行任何操作之前，必须完整阅读以下文档。P1 表示触发该模式前必须读。

### 工作流 (必读)

| Document | Purpose | Priority |
|----------|---------|----------|
| [workflows/main.md](workflows/main.md) | 主工作流程 | **P0 - 最高** |
| [workflows/requirement-precheck.md](workflows/requirement-precheck.md) | 快速需求预检 | **P0 - 最高** |
| [workflows/assess.md](workflows/assess.md) | ASSESS 阶段（代码库评估） | **P0 - 最高** |
| [workflows/precheck.md](workflows/precheck.md) | RFC 预检规则 | **P0 - 最高** |
| [workflows/export.md](workflows/export.md) | 手动导出机读件 | **P0 - 最高** |
| [workflows/spike.md](workflows/spike.md) | Spike 验证流程 | P1（触发 TRIGGER_SPIKE 时） |
| [workflows/resume.md](workflows/resume.md) | Resume 模式 | P1（中断恢复时） |

### 规范文档 (必读)

| Document | Purpose | Priority |
|----------|---------|----------|
| [docs/phases.md](docs/phases.md) | 阶段详细定义 | **P0 - 最高** |
| [docs/quality-gates.md](docs/quality-gates.md) | 质量门禁标准 | **P0 - 最高** |
| [docs/rfc-format.md](docs/rfc-format.md) | RFC 格式规范 | **P0 - 最高** |
| [docs/routing-signals.md](docs/routing-signals.md) | 路由信号机制 | **P0 - 最高** |
| [docs/subagent-contract.md](docs/subagent-contract.md) | 子代理契约与摘要规范 | P1（启用子代理时） |
| [docs/error-handling.md](docs/error-handling.md) | 错误处理策略 | P1（发生异常时） |

### 模板文件 (必读)

| Document | Purpose | Priority |
|----------|---------|----------|
| [templates/rfc.md](templates/rfc.md) | RFC 模板 | **P0 - 最高** |
| [templates/findings.json](templates/findings.json) | 扫描发现模板 | **P0 - 最高** |
| [templates/progress.json](templates/progress.json) | 进度与门禁模板 | **P0 - 最高** |
| [templates/rfc-minimal.md](templates/rfc-minimal.md) | 快速通道 RFC | P1（快速通道） |
| [templates/project-context.md](templates/project-context.md) | 项目上下文输入 | P1（需要补齐上下文时） |
| [templates/context-pack.json](templates/context-pack.json) | 上下文打包格式 | P1（需要打包上下文时） |
| [templates/project-knowledge.json](templates/project-knowledge.json) | 知识结构模板 | P1（需要结构化知识时） |
| [templates/checkpoint.json](templates/checkpoint.json) | 断点续写状态 | P1（中断恢复时） |

### Scripts (必读)

| Document | Purpose | Priority |
|----------|---------|----------|
| `.ohspec/scripts/precheck_rfc.py`（优先；未初始化则用 `scripts/precheck_rfc.py` 或先 bootstrap） | RFC 结构预检 | **P0 - 最高** |
| [scripts/export_digest.py](scripts/export_digest.py) | 导出机读件 | **P0 - 最高** |
| [scripts/bootstrap_project.py](scripts/bootstrap_project.py) | 初始化项目上下文 | P1（首次落盘项目时） |

## 语言要求

**强制**：所有交付物必须使用**简体中文**（RFC、findings.json、progress.json、审查报告）。

**例外**：代码标识符遵循项目约定。

## 快速开始

```bash
/ohspec "为音频服务增加 3D 音效开关"
```

## 核心规则（必须遵守）

1. **默认委托 Dispatcher 执行基线扫描（scan-of-record）；Task 不可用时使用 Codex 兼容回退**
2. **初始化三文件**：`rfc.md`、`findings.json`、`progress.json` 必须先落盘再扫描
3. **所有详细扫描结果写入 findings.json**
4. **子代理返回 JSON 摘要（≤500 tokens）**
5. **每阶段结束更新 progress.json**
6. **DFX 必须量化，禁止模糊描述**
7. **禁止开放式问题，必须选项式**
8. **机读件不写进 RFC**：通过 `/ohspec:export` 手动生成 `rfc.digest.json`（可选 `tasks.json`）
9. **澄清/门禁提问工具优先级**：Codex CLI 用 `request_user_input`；Claude Code CLI 用 `AskUserQuestion`；若工具不可用/被禁用，输出“选项式问题 + 影响 + 建议”的文本并暂停，**不得进入 plan/design/audit**
10. **禁止假设**：找不到证据就补扫或阻断，不得编造设置键/接口/默认值

### Codex 兼容回退（Task 不可用）

当无法使用 Task 子代理时（例如 Codex 环境），允许编排器执行**最小化 scan-of-record**：
- 优先使用 `rg`（其次 `ag`/`grep`）做关键词预过滤，快速定位候选关键文件
- **必须排除生成物目录**：避免把历史 RFC/缓存当作“证据”并拉爆上下文（示例：`rg --glob '!**/.ohspec/**' --glob '!**/.claude/ohspec/**' --glob '!**/node_modules/**' --glob '!**/dist/**' --glob '!**/build/**' ...`）
- 先落盘三文件（rfc.md/findings.json/progress.json），再开始任何扫描
- **ASSESS 必须先落盘**：在进入任何内容级扫描前，先用 ASSESS 选定工具与 scan_scope，并写入 `progress.json.tooling` + `phases.assess` + `audit_log`
- 产出必须写入 `findings.confirmed.key_files`（≥3 且覆盖入口/配置/依赖或测试/可观测）
- 同时写入 `findings.confirmed.facts`（SIMPLE ≥ 1；MEDIUM/COMPLEX ≥ 3，项目事实：配置/存储/权限/错误码/线程模型/可观测等，每条附证据锚点）
- **禁止假设**：找不到证据就补扫/阻断，不得编造设置键/接口/默认值
- **第一分钟基线**：开始深度 Read/设计推演前，必须先把 key_files+facts 落盘（否则中断会导致三文件“空壳”）
- 记录到 `progress.json.tooling` 与 `audit_log`

## 阶段定义

| 阶段 | 目标 | 专家 | 输出 |
|------|------|------|------|
| assess | 评估代码库规模，决策扫描策略 | 编排器 | 扫描策略 |
| analyze | 理解需求，澄清歧义 | 需求分析师 | RFC §1-§2 |
| design | 设计方案，定义接口 | 架构设计师 | RFC §3-§5 |
| precheck | 自动验证结构和覆盖 | 编排器 | 预检报告 |
| audit | 质量审查，评分决策 | 质量审查员 | 审查报告 |

### 阶段定义（扩展）

| 阶段 | 目标 | 触发条件 | 输出 |
|------|------|----------|------|
| requirement_precheck | 快速需求预检，过滤不可行/信息不足需求 | 所有任务 | 可行性判断 |
| assess | 评估代码库规模，决策扫描策略 | requirement_precheck 通过 | 扫描策略 |
| intent_clarify | 快速意图澄清，确保扫描准确 | assess 完成 | 意图理解 |
| dispatcher | 基线扫描（scan-of-record） | intent_clarify 完成 | key_files + facts |
| analyze | 深度技术澄清，输出 RFC §1-§2 | dispatcher 完成 | RFC §1-§2 |

## 专家团队

**核心专家**：Dispatcher、需求分析师、架构设计师、质量审查员

**扩展专家**：Diplomat（跨子系统）、API设计师、Prototyper（spike验证）

## 质量门禁

**必须满足**：
- 5 个 RFC 章节完整
- 8 个 DFX 维度量化
- 4 种场景类型覆盖（Gherkin格式）
- 无模糊描述

## RFC 格式

**ID格式**：`RFC-{YYYYMMDD}-{slug}-{hash4}`

**目录（推荐）**：`.ohspec/rfcs/{RFC-ID}/`  
**兼容（历史）**：`.claude/ohspec/rfcs/{RFC-ID}/`

## Reference Documents

**工作流**：
- [workflows/main.md](workflows/main.md) - 主工作流程
- [workflows/requirement-precheck.md](workflows/requirement-precheck.md) - 快速需求预检
- [workflows/assess.md](workflows/assess.md) - ASSESS 阶段（代码库评估）
- [workflows/precheck.md](workflows/precheck.md) - RFC 预检规则
- [workflows/export.md](workflows/export.md) - 手动导出机读件（digest/tasks）
- [workflows/resume.md](workflows/resume.md) - Resume 模式
- [workflows/spike.md](workflows/spike.md) - Spike 验证流程

**文档**：
- [docs/phases.md](docs/phases.md) - 阶段详细定义
- [docs/routing-signals.md](docs/routing-signals.md) - 路由信号机制
- [docs/quality-gates.md](docs/quality-gates.md) - 质量门禁标准
- [docs/rfc-format.md](docs/rfc-format.md) - RFC 格式规范
- [docs/implementation-guide.md](docs/implementation-guide.md) - 实现指南
- [docs/resume-mode.md](docs/resume-mode.md) - Token 优化技术
- [docs/best-practices.md](docs/best-practices.md) - 最佳实践
- [docs/error-handling.md](docs/error-handling.md) - 错误处理策略
- [docs/subagent-contract.md](docs/subagent-contract.md) - 子代理契约与摘要规范

**模板**：
- [templates/rfc.md](templates/rfc.md)
- [templates/rfc-minimal.md](templates/rfc-minimal.md)
- [templates/findings.json](templates/findings.json)
- [templates/progress.json](templates/progress.json)
- [templates/project-context.md](templates/project-context.md)
- [templates/context-pack.json](templates/context-pack.json)
- [templates/project-knowledge.json](templates/project-knowledge.json)
- [templates/checkpoint.json](templates/checkpoint.json)

**脚本**：
- `.ohspec/scripts/precheck_rfc.py`（优先；未初始化则用 `scripts/precheck_rfc.py` 或先 bootstrap）
- [scripts/export_digest.py](scripts/export_digest.py)
- [scripts/bootstrap_project.py](scripts/bootstrap_project.py)
