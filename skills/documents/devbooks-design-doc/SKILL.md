---
name: devbooks-design-doc
description: devbooks-design-doc：产出变更包的设计文档（design.md），只写 What/Constraints 与 AC-xxx，不写实现步骤。用户说"写设计文档/Design Doc/架构设计/约束/验收标准/AC/C4 Delta"等时使用。
recommended_experts: ["System Architect", "Product Manager"]
allowed-tools:
  - Glob
  - Grep
  - Read
  - Write
  - Edit
---

# DevBooks：设计文档（Design Doc）

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

## 工作流位置感知（Workflow Position Awareness）

> **核心原则**：Design Doc 在 Proposal 批准后执行，是实现阶段的起点。

### 我在整体工作流中的位置

```
proposal → [Design Doc] → spec-contract → implementation-plan → test-owner → coder → ...
                 ↓
        定义 What/Constraints/AC
```

### Design Doc 的产出

- **What**：做什么（不是怎么做）
- **Constraints**：约束条件
- **AC-xxx**：验收标准（可测试的）

**关键**：Design Doc 不写实现步骤，那是 implementation-plan 的职责。

---

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

- 设计文档：`<change-root>/<change-id>/design.md`

## 文档影响声明（必填）

设计文档中**必须**包含「文档影响」章节，声明本次变更对用户文档的影响。这是确保文档与代码同步的关键机制。

### 模板

```markdown
## Documentation Impact（文档影响）

### 需要更新的文档

| 文档 | 更新原因 | 优先级 |
|------|----------|--------|
| README.md | 新增功能 X 需要说明使用方法 | P0 |
| docs/使用说明书.md | 新增脚本 Y 需要补充用法 | P0 |
| CHANGELOG.md | 记录本次变更 | P1 |

### 无需更新的文档

- [ ] 本次变更为内部重构，不影响用户可见功能
- [ ] 本次变更仅修复 bug，不引入新功能或改变使用方式

### 文档更新检查清单

- [ ] 新增脚本/命令已在使用文档中说明
- [ ] 新增配置项已在配置文档中说明
- [ ] 新增工作流/流程已在指南中说明
- [ ] API/接口变更已在相关文档中更新
```

### 触发规则

以下变更类型**强制要求**更新对应文档：

| 变更类型 | 需更新文档 |
|----------|------------|
| 新增脚本（*.sh） | 使用说明、README |
| 新增 Skill | README、Skills 列表 |
| 修改工作流程 | 相关指南文档 |
| 新增配置项 | 配置文档 |
| 新增命令/CLI 参数 | 使用说明 |
| 对外 API 变更 | API 文档 |

## 架构影响声明（Architecture Impact）（必填）

设计文档中**必须**包含「架构影响」章节，声明本次变更对系统架构的影响。这是确保架构变更走验证闭环的关键机制。

> **设计决策**：C4 架构变更不再由独立的 `devbooks-c4-map` skill 直接写入真理目录，而是作为 design.md 的一部分，在变更验收通过后由 `devbooks-archiver` 合并到真理。

### 模板

```markdown
## Architecture Impact（架构影响）

<!-- 必填：选择以下之一 -->

### 无架构变更

- [x] 本次变更不影响模块边界、依赖方向或组件结构
- 原因说明：<简要说明为什么无架构影响>

### 有架构变更

#### C4 层级影响

| 层级 | 变更类型 | 影响描述 |
|------|----------|----------|
| Context | 无变更 / 新增 / 修改 / 删除 | <描述> |
| Container | 无变更 / 新增 / 修改 / 删除 | <描述> |
| Component | 无变更 / 新增 / 修改 / 删除 | <描述> |

#### Container 变更详情

- [新增/修改/删除] `<container-name>`: <变更描述>

#### Component 变更详情

- [新增/修改/删除] `<component-name>` in `<container>`: <变更描述>

#### 依赖变更

| 源 | 目标 | 变更类型 | 说明 |
|----|------|----------|------|
| `<source>` | `<target>` | 新增/删除/方向改变 | <说明> |

#### 分层约束影响

- [ ] 本次变更遵守现有分层约束
- [ ] 本次变更需要修改分层约束（需在下方说明）

分层约束修改说明：<如有>
```

### 判断规则

执行 design-doc skill 时，**必须检测**以下条件判断是否有架构变更：

| 检测项 | 检测方法 | 有架构变更 |
|--------|----------|------------|
| 新增/删除目录 | 检查变更文件路径 | 可能影响模块边界 |
| 跨模块 import | 检查 import 语句变化 | 可能影响依赖方向 |
| 新外部依赖 | 检查 package.json/go.mod 等 | 影响 Container 层 |
| 新服务/进程 | 检查 Dockerfile/docker-compose | 影响 Container 层 |
| 新 API 端点组 | 检查路由定义 | 可能影响 Component 层 |

### 触发规则

以下变更类型**强制要求**填写架构变更详情：

| 变更类型 | 要求 |
|----------|------|
| 新增模块/目录 | 必须描述 Component 变更 |
| 新增服务/容器 | 必须描述 Container 变更 |
| 修改模块间依赖 | 必须描述依赖变更 |
| 引入新外部系统 | 必须描述 Context 变更 |

---

## 执行方式

1) 先阅读并遵守：`~/.claude/skills/_shared/references/AI行为规范.md`（可验证性 + 结构质量守门）。
2) 严格按完整提示词输出：`references/设计文档提示词.md`。

---

## 上下文感知

本 Skill 在执行前自动检测上下文，选择合适的运行模式。

检测规则参考：`skills/_shared/上下文检测模板.md`

### 检测流程

1. 检测 `proposal.md` 是否存在（设计文档的输入）
2. 检测 `design.md` 是否已存在
3. 若存在，检测完整性（是否有 AC-xxx、是否有 `[TODO]`）

### 本 Skill 支持的模式

| 模式 | 触发条件 | 行为 |
|------|----------|------|
| **新建设计** | `design.md` 不存在 | 创建完整设计文档 |
| **补充设计** | `design.md` 存在但有 `[TODO]` | 补充缺失章节 |
| **添加 AC** | 设计存在但 AC 不完整 | 补充验收标准 |

### 检测输出示例

```
检测结果：
- proposal.md：存在
- design.md：存在，有 5 个 [TODO]
- AC 数量：8 个
- 运行模式：补充设计
```

---

## 下一步推荐

**参考**：`skills/_shared/工作流下一步.md`

完成 design-doc 后，下一步取决于变更范围：

| 条件 | 下一个 Skill | 原因 |
|------|--------------|------|
| 有外部行为/契约变更 | `devbooks-spec-contract` | 必须先定义契约再做计划 |
| 无外部契约变更 | `devbooks-implementation-plan` | 直接进入任务计划 |

**关键**：绝不在 design-doc 后直接推荐 `devbooks-test-owner` 或 `devbooks-coder`。工作流顺序是：
```
design-doc → [spec-contract] → implementation-plan → test-owner → coder
```

### 输出模板

完成 design-doc 后，输出：

```markdown
## 推荐的下一步

**下一步：`devbooks-spec-contract`**（如果有外部行为/契约变更）
或
**下一步：`devbooks-implementation-plan`**（如果无外部契约变更）

原因：设计已完成。下一步是[定义外部契约 / 创建实现计划]。

### 如何调用
```
运行 devbooks-<skill-name> skill 处理变更 <change-id>
```
```

---

## 方法论参考

- 完备性思维框架：[完备性思维框架](../_shared/references/完备性思维框架.md)
