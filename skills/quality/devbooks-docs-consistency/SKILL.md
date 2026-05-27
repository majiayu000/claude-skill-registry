---
name: devbooks-docs-consistency
description: devbooks-docs-consistency：检查并维护项目文档与代码的一致性，支持增量扫描、自定义规则与完备性检查。可在变更包内按需运行或全局检查。旧名称 devbooks-docs-sync 保留为别名并输出弃用提示。
recommended_experts: ["Technical Writer", "System Architect"]
allowed-tools:
  - Glob
  - Grep
  - Read
  - Edit
  - Write
  - Bash
---

# DevBooks：文档一致性（Docs Consistency）

## 渐进披露
### 基础层（必读）
目标：明确本 Skill 的核心产出与使用范围。
输入：用户目标、现有文档、变更包上下文或项目路径。
输出：可执行产物、下一步指引或记录路径。
边界：不替代其他角色职责，不触碰 tests/。
证据：引用产出物路径或执行记录。

### 进阶层（可选）
适用：需要细化策略、边界或风险提示时补充。

### 扩展层（可选）
适用：需要与外部系统或可选工具协同时补充。

## 推荐 MCP 能力类型
- 代码检索（code-search）
- 引用追踪（reference-tracking）
- 影响分析（impact-analysis）

## 前置：配置发现（协议无关）

执行前**必须**按以下顺序查找配置（找到后停止）：
1. `.devbooks/config.yaml`（如存在）→ 解析并使用其中的映射
2. `dev-playbooks/project.md`（如存在）→ Dev-Playbooks 协议，使用默认映射
3. `project.md`（如存在）→ template 协议，使用默认映射
4. 若仍无法确定 → **停止并询问用户**

---

## 兼容与弃用

- 旧名称：`devbooks-docs-sync`
- 当前名称：`devbooks-docs-consistency`
- 行为：旧名称作为别名继续可用，并输出弃用提示。
- 运行提示：别名通过软链接指向新目录，可执行 `scripts/alias.sh` 输出提示。

弃用提示示例：

```
devbooks-docs-sync 已弃用，请使用 devbooks-docs-consistency。
```

---

## 角色定义

**docs-consistency** 是 DevBooks Apply 阶段的文档一致性检查角色，负责识别文档与代码之间的偏差并生成报告，不直接修改代码。

### 文档分类

| 文档类型 | 目标受众 | 是否由本 Skill 检查 | 示例 |
|----------|----------|:-------------------:|------|
| **活体文档** | 最终用户 | ✅ | README.md, docs/*.md, API.md |
| **历史文档** | 最终用户 | ⚠️（只做最低限度检查） | CHANGELOG.md |
| **概念性文档** | 设计/架构 | ✅（结构性检查） | architecture/*.md |

分类规则可配置，默认规则见 `references/doc-classification.yaml`。

---

## 运行模式

### 模式一：增量扫描（Change-Scoped）

**触发条件**：在变更包上下文中运行。

**行为**：
1. 读取变更范围
2. 仅扫描变更文件
3. 记录 token 消耗与扫描时间
4. 输出检查报告

### 模式二：全量扫描（Global Check）

**触发条件**：用户显式请求全局检查（如 `devbooks-docs-consistency --global`）。

**行为**：
1. 扫描所有用户文档
2. 生成差异报告
3. 输出改进建议

### 模式三：检查模式（Check Only）

**触发条件**：用户使用 `--check` 参数。

**行为**：只检查、不修改，输出报告。

---

## 命令示例

```
# 规则引擎：持续规则
bash scripts/rules-engine.sh --rules references/docs-rules-schema.yaml --input README.md

# 规则引擎：一次性任务
bash scripts/rules-engine.sh --once "remove:@augment" --input README.md

# 文档分类
bash scripts/doc-classifier.sh README.md

# 完备性检查
bash scripts/completeness-checker.sh --input README.md --config references/completeness-dimensions.yaml --output evidence/completeness-report.md

# 作为 G6 Scope Evidence 的机读报告（固定落点）
skills/devbooks-delivery-workflow/scripts/docs-consistency-check.sh <change-id> \
  --project-root . --change-root dev-playbooks/changes --truth-root dev-playbooks/specs
```

---

## 完备性检查

对活体文档执行完备性检查，默认覆盖：环境依赖、安全权限、故障排查、配置说明、API 文档。

- 维度配置：`references/completeness-dimensions.yaml`
- 报告输出：`<change-root>/<change-id>/evidence/completeness-report.md`
- 方法论参考：[完备性思维框架](../_shared/references/完备性思维框架.md)

---

## 风格偏好

风格偏好读取优先级：命令行参数 > 配置文件 > 默认值。

- 文档维护元数据：`dev-playbooks/specs/_meta/docs-maintenance.md`

---

## 输出与报告

默认输出以下报告（变更包上下文）：

- `evidence/gates/docs-consistency.report.json`（机读；供 G6 / archive-decider 消费）
- `evidence/completeness-report.md`
- `evidence/token-usage.log`
- `evidence/scan-performance.log`

---

## 与工作流的集成

在归档阶段由 `devbooks-archiver` 触发，在存量初始化时由 `devbooks-brownfield-bootstrap` 生成文档维护元数据。

当 G6 触发 Scope Evidence Bundle 且判定“docs 一致性为必需项”时（例如 deliverables 涉及 `README.md/docs/**/templates/**`，或存在 `weak_link+docs` 的 `severity=must` 义务）：
- 必须生成 `evidence/gates/docs-consistency.report.json` 且 `status=pass`
- 缺失或 `status!=pass` 将被 `archive-decider.sh` 判定为 fail，从而阻断归档

---

## 元数据

| 字段 | 值 |
|------|-----|
| Skill 名称 | devbooks-docs-consistency |
| 阶段 | Apply（实现后、归档前） |
| 产物 | 文档一致性检查报告 |
| 约束 | 只检查、不修改代码 |

---

*此 Skill 文档遵循 devbooks-* 规范。*
