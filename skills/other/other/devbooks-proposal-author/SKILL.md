---
name: devbooks-proposal-author
description: devbooks-proposal-author：撰写变更提案 proposal.md（Why/What/Impact + Debate Packet），作为后续 Design/Spec/Plan 的入口。对设计性决策会呈现选项给用户选择。用户说"写提案/proposal/为什么要改/影响范围/坏味道重构提案"等时使用。
recommended_experts: ["Product Manager", "System Architect"]
allowed-tools:
  - Glob
  - Grep
  - Read
  - Write
  - Edit
---

# DevBooks：提案撰写（Proposal Author）

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

- `<truth-root>`：当前真理目录根
- `<change-root>`：变更包目录根

执行前**必须**按以下顺序查找配置（找到后停止）：
1. `.devbooks/config.yaml`（如存在）→ 解析并使用其中的映射
2. `dev-playbooks/project.md`（如存在）→ Dev-Playbooks 协议，使用默认映射
3. `project.md`（如存在）→ template 协议，使用默认映射
4. 若仍无法确定 → **停止并询问用户**

**关键约束**：
- 如果配置中指定了 `agents_doc`（规则文档），**必须先阅读该文档**再执行任何操作
- 禁止猜测目录根
- 禁止跳过规则文档阅读

## 核心职责

1. **提案撰写**：产出清晰、可审查、可落地的变更提案
2. **设计性决策交互**：对于无法客观判断好坏的设计选择，呈现选项给用户决策，不自行拍板

## 变更包命名规范（强制）

变更包 ID（change-id）**必须**遵循以下命名规范：

### 格式

```
<日期时间>-<动词开头的语义描述>
```

### 规则

| 组成部分 | 规则 | 示例 |
|----------|------|------|
| 日期时间 | `YYYYMMDD-HHMM` 格式 | `20240116-1030` |
| 分隔符 | 日期时间与语义之间用 `-` 分隔 | `-` |
| 语义描述 | **必须以动词开头**，使用小写和连字符 | `add-oauth2`, `fix-login-bug` |

### 示例

```bash
# ✅ 正确
20240116-1030-add-oauth2-support
20240116-1430-fix-user-auth-bug
20240116-0900-refactor-payment-module
20240115-2200-update-api-docs

# ❌ 错误
add-oauth2                    # 缺少日期时间
20240116-oauth2               # 语义不是动词开头
2024-01-16-add-oauth2         # 日期格式错误（不应有 -）
oauth2-20240116               # 顺序错误
```

### 常用动词

| 动词 | 用途 |
|------|------|
| `add` | 添加新功能 |
| `fix` | 修复缺陷 |
| `update` | 更新现有功能 |
| `refactor` | 重构代码 |
| `remove` | 删除功能 |
| `improve` | 提升性能/体验 |
| `migrate` | 迁移数据/系统 |

### 为什么这样命名？

1. **时间戳在前**：归档目录中自动按时间排序
2. **动词开头**：清晰表达变更意图，方便代码审查
3. **小写连字符**：避免跨平台文件名问题

### 创建变更包

在确定 change-id 后，调用脚手架脚本初始化变更包：

```bash
change-scaffold.sh <change-id> --project-root <repo-root> --change-root <change-root> --truth-root <truth-root>
```

## 产物落点

- 提案：`<change-root>/<change-id>/proposal.md`

## 执行方式

1) 先阅读并遵守：`~/.claude/skills/_shared/references/AI行为规范.md`（可验证性 + 结构质量守门）。
2) 严格按完整提示词输出：`references/提案撰写提示词.md`。

---

## 上下文感知

本 Skill 在执行前自动检测上下文，选择合适的运行模式。

检测规则参考：`skills/_shared/上下文检测模板.md`

### 检测流程

1. 检测变更包是否存在
2. 检测 `proposal.md` 是否已存在
3. 若存在，检测是否有 Decision Log（是否已裁决）

### 本 Skill 支持的模式

| 模式 | 触发条件 | 行为 |
|------|----------|------|
| **新建提案** | 变更包不存在或 `proposal.md` 不存在 | 创建完整提案文档 |
| **修订提案** | `proposal.md` 存在，Judge 要求 Revise | 根据裁决意见修改提案 |
| **补充 Impact** | `proposal.md` 存在但缺少 Impact 章节 | 补充影响分析部分 |

### 检测输出示例

```
检测结果：
- 变更包状态：存在
- proposal.md：存在
- 裁决状态：Revise（需要修改）
- 运行模式：修订提案
```

---

## 下一步推荐

**参考**：`skills/_shared/工作流下一步.md`

完成 proposal-author 后，下一步取决于具体情况：

| 条件 | 下一个 Skill | 原因 |
|------|--------------|------|
| 跨模块影响不明确 | `devbooks-impact-analysis` | 先明确影响范围 |
| 高风险/有争议 | `devbooks-proposal-challenger` | 先质疑再继续 |
| 影响明确，准备设计 | `devbooks-design-doc` | 创建设计文档 |

**关键**：绝不在 proposal-author 后直接推荐 `devbooks-test-owner` 或 `devbooks-coder`。工作流顺序是：
```
proposal-author → [impact-analysis] → design-doc → [spec-contract] → implementation-plan → test-owner → coder
```

### 输出模板

完成 proposal-author 后，输出：

```markdown
## 推荐的下一步

**下一步：`devbooks-design-doc`**（最常见）
或
**下一步：`devbooks-impact-analysis`**（如果跨模块影响不明确）
或
**下一步：`devbooks-proposal-challenger`**（如果高风险，可选）

原因：提案已完成。下一步是[明确影响 / 创建设计文档]。

### 如何调用
```
运行 devbooks-<skill-name> skill 处理变更 <change-id>
```
```

---

## Challenger 审视

在完成提案草案后，执行 Challenger 审视，重点检查遗漏的约束与不确定性，并参考完备性方法论。

- 方法论参考：[完备性思维框架](../_shared/references/完备性思维框架.md)
