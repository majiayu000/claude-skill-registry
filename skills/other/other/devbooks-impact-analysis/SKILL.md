---
name: devbooks-impact-analysis
description: devbooks-impact-analysis：跨模块/跨文件/对外契约变更前做影响分析，产出可直接写入 proposal.md 的 Impact 部分（Scope/Impacts/Risks/Minimal Diff/Open Questions）。用户说"做影响分析/改动面控制/引用查找/受影响模块/兼容性风险"等时使用。
recommended_experts: ["System Architect"]
allowed-tools:
  - Glob
  - Grep
  - Read
  - Bash
---

# DevBooks：影响分析（Impact Analysis）

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

## 产物落点

- **必须**写入：`<change-root>/<change-id>/proposal.md` 的 Impact 部分
- 备选：独立 `impact-analysis.md` 文件（后续回填到 proposal.md）

## 输出行为（关键约束）

> **黄金法则**：**直接写入文档，禁止输出到对话窗口**

### 必须遵守

1. **直接写入**：使用 `Edit` 或 `Write` 工具将分析结果直接写入目标文档
2. **禁止回显**：不要在对话中显示完整的分析内容
3. **简短通知**：完成后只需告知用户"影响分析已写入 `<文件路径>`"

### 正确行为 vs 错误行为

| 场景 | ❌ 错误行为 | ✅ 正确行为 |
|------|------------|------------|
| 分析完成 | 在对话中输出完整 Impact 表格 | 使用 Edit 工具写入 proposal.md |
| 通知用户 | 复述分析内容 | "影响分析已写入 `changes/xxx/proposal.md`" |
| 大量结果 | 分页输出到对话 | 全部写入文件，告知文件位置 |

### 示例对话

```
用户：分析一下修改 UserService 的影响

AI：[使用代码检索/引用追踪分析]
    [使用 Edit 工具写入 proposal.md]

    影响分析已写入 `changes/refactor-user/proposal.md` 的 Impact 部分。
    - 直接影响：8 个文件
    - 间接影响：12 个文件
    - 风险等级：中等

    如需查看详情，请打开该文件。
```

## 执行方式

1) 先阅读并遵守：`~/.claude/skills/_shared/references/AI行为规范.md`（可验证性 + 结构质量守门）。
2) 使用 `Grep` 搜索符号引用，`Glob` 查找相关文件。
3) 严格按完整提示词输出影响分析 Markdown：`references/影响分析提示词.md`。

## 输出格式

```markdown
## Impact Analysis

### Scope
- 直接影响：X 个文件
- 间接影响：Y 个文件

### Impacts
| 文件 | 影响类型 | 风险等级 |
|------|----------|----------|
| ... | 直接调用 | 高 |

### Risks
- ...

### Minimal Diff
- ...

### Open Questions
- ...
```

---

## 上下文感知

本 Skill 在执行前自动检测上下文，选择合适的分析范围。

检测规则参考：`skills/_shared/上下文检测模板.md`

### 检测流程

1. 检测变更包是否存在
2. 检测 `proposal.md` 中是否已有 Impact 章节
3. 检测是否有结构化引用追踪能力可用（用于更精确分析）

### 本 Skill 支持的模式

| 模式 | 触发条件 | 行为 |
|------|----------|------|
| **新建分析** | Impact 章节不存在 | 执行完整影响分析 |
| **增量分析** | Impact 已存在，有新变更 | 更新受影响文件列表 |
| **结构化分析** | 结构化引用追踪可用 | 使用调用关系进行精确分析 |
| **文本分析** | 仅文本检索可用 | 使用 Grep 文本搜索分析 |

### 检测输出示例

```
检测结果：
- proposal.md：存在，Impact 章节缺失
- 引用追踪能力：可用
- 运行模式：新建分析 + 结构化分析
```
