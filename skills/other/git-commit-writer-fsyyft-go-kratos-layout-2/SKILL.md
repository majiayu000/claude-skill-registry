---
name: git-commit-writer
description: Git 提交信息智能生成工具。基于 Claude 对代码改动和用户意图的深度分析，自动生成符合项目规范的 commit message，支持四层验证机制确保质量。
---

# Git Commit Writer

## 概述

基于 Claude 智能分析的 Git 提交信息（commit message）生成工具，100% 大模型驱动，无需脚本。

**核心特点**：
- 🤖 **Claude 驱动**：完全依赖 Claude 的理解、分析和判断能力
- 🎯 **智能分析**：自动分析 git diff 和用户意图，识别改动类型和范围
- ✅ **四层验证**：格式、一致性、语言、改动一致性严格验证
- 📝 **直接输出**：简洁高效，直接输出可用的 commit message

**工作原理**：
Claude 分析 git diff + 用户上下文 → 自动判断类型和范围 → 生成符合规范的 commit message → 四层严格验证 → 输出最终结果

## 使用场景

- 日常开发提交
- 代码审查后修正
- 重构后的提交
- 多功能合并提交
- 紧急修复提交

## 快速开始

### 基本用法（默认暂存区模式）

```bash
# 默认：针对当前暂存区中的文件生成 commit message
"帮我为暂存的改动生成 commit message"
"分析暂存区并生成 commit"
```

### 未提交文件模式

```bash
# 如果没有暂存区，但有未提交的文件
"为未提交的改动生成 commit message"
"分析当前工作区的改动"
```

### 分支对比模式

```bash
# 指定分支：对比指定分支的所有变更
"为 develop 分支的变更生成 commit message"
"分析相对于 feature/skill 分支的所有改动"
"对比 master 分支，生成合并 commit message"
```

### 高级用法

```bash
# 结合 git diff 和用户上下文
"我为 web 服务添加了用户认证功能，帮我生成 commit message"
"修复了 data 层的数据库连接问题，生成 commit message"
```

### 最佳实践

- 明确指定分析范围（暂存区/未提交文件/分支）
- 提供简洁的改动意图说明
- 让 Claude 自主判断类型和范围

## 工作流程

### 分析范围判断阶段

```
用户输入分析
  ↓
判断用户是否指定分支？
  ├─ 是 → 进入分支对比模式
  │     ├─ 运行: git diff <target-branch> --name-only
  │     ├─ 运行: git diff <target-branch>
  │     └─ 获取所有变更文件和具体改动内容
  │
  └─ 否 → 进入默认模式
        ├─ 检查暂存区（git diff --staged --name-only）
        │     ├─ 有暂存文件 → 进入暂存区模式
        │     │     ├─ 运行: git diff --staged
        │     │     └─ 分析暂存的改动内容
        │     │
        │     └─ 无暂存文件 → 进入未提交文件模式
        │            ├─ 运行: git diff --name-only
        │            ├─ 运行: git diff
        │            └─ 分析未提交的改动内容
        │
        └─ 收集用户提供的上下文和意图说明
```

### 信息收集阶段

**暂存区模式**：
```
运行 git status → 确认暂存状态
运行 git diff --staged --name-only → 获取变更文件列表
运行 git diff --staged → 分析具体改动内容
识别文件类型和路径
```

**未提交文件模式**：
```
运行 git status → 确认工作区状态
运行 git diff --name-only → 获取变更文件列表
运行 git diff → 分析具体改动内容
识别文件类型和路径
```

**分支对比模式**：
```
运行 git status → 确认当前分支
运行 git diff <target-branch> --name-only → 获取变更文件列表
运行 git diff <target-branch> → 分析具体改动内容
识别文件类型和路径
识别变更涉及的 commit 数量和历史
```

**共同步骤**：
```
收集用户提供的上下文说明和改动意图
统计改动规模（文件数量、行数变化）
识别改动的关键特征
```

### 智能分析阶段

```
分析改动类型（新功能/bug修复/重构/文档等）
识别影响范围（web/task/api/internal 等）
提炼核心业务意图
判断改动的重要性和影响程度
识别与现有功能的关系
```

### 生成候选阶段

```
选择合适的 commit type（feat/fix/docs 等）
确定准确的 scope（标准范围或路径范围）
提炼简洁的中文描述（祈使句、首字母小写、不加句号）
生成完整的 commit message 格式
```

### 四层验证阶段

**第一层：格式验证**
- 检查 `<类型>(<范围>): <描述>` 格式
- 验证类型有效性（11 种之一）
- 验证范围可选性
- 验证描述非空

**第二层：类型-范围一致性验证**
- 检查类型与范围是否匹配
- 参考类型-范围映射表
- 验证逻辑合理性

**第三层：语言和语法验证**
- 检查中文表述规范性
- 检查语法正确性
- 避免口语化表达
- 验证长度要求（50 字以内）

**第四层：代码改动一致性验证**
- 对比 git diff 内容
- 验证 message 与改动是否一致
- 检查是否遗漏重要信息

### 输出结果阶段

```
直接输出最优的 commit message
提供简要的改动分析说明
标注验证通过的所有层级
```

## 四层验证机制

**验证原则**：四层验证必须全部通过，任何一层不通过都必须调整。

### 第一层：格式验证

**验证规则**：必须符合 `<类型>(<范围>): <描述>` 格式

**正则表达式**：`^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]+\))?: .+$`

**通过条件**：
- 类型有效（11 种之一）
- 范围可选（如无范围，格式为 `<类型>: <描述>`）
- 描述不为空且以空格开头

**不通过示例**：
- ❌ `添加用户功能`（缺少类型）
- ❌ `Feat: 添加用户功能`（类型大写）
- ❌ `feat(web)`（缺少描述）

### 第二层：类型-范围一致性验证

**类型-范围映射表**：

| 类型 | 推荐范围 | 可接受范围 | 不可接受范围 |
|------|----------|------------|--------------|
| feat | api, web, task, internal, .claude/skills/* | docs | test, build |
| fix | data, biz, service, server, web, task | internal | docs, build, ci |
| docs | 任意范围（包含具体路径） | - | - |
| style | internal, biz, service, data | - | api, docs |
| refactor | internal, biz, service, data, server | - | docs, test |
| perf | data, biz, service | internal | docs, test |
| test | biz, service, data | internal | docs, api |
| build | Makefile, go.mod, dockerfile | - | internal, biz |
| ci | .github/*, .gitlab-ci.* | - | internal, biz |
| chore | 任意范围（维护性工作） | - | - |
| revert | 与原 commit 相同的范围 | - | - |

**通过条件**：类型和范围必须在上表中匹配

**不通过示例**：
- ❌ `test(api): 添加接口测试`（test 不应在 api）
- ❌ `feat(docs): 添加新功能`（feat 应在代码文件）

### 第三层：语言和语法验证

**中文表述规范**：
- ✅ 使用标准现代汉语
- ✅ 语法正确，表述清晰
- ✅ 使用祈使句（添加、修复、更新、重构等）
- ✅ 首字母小写（除非专有名词）
- ✅ 结尾不加句号
- ❌ 避免口语化（"搞定"、"弄好"、"整一下"）
- ❌ 避免冗余（"了"、"一下"等）

**通过条件检查**：
1. 是否使用中文？
2. 是否使用祈使句？
3. 是否首字母小写？
4. 是否结尾无句号？
5. 是否无口语化表达？
6. 描述长度是否在 50 字以内？

**不通过示例**：
- ❌ `feat: 添加了用户管理功能`（使用"了"）
- ❌ `fix: 修复数据连接的问题`（"的"字冗余）
- ❌ `feat: 添加用户功能。`（结尾有句号）
- ❌ `feat: 搞定数据库连接`（口语化）

### 第四层：代码改动一致性验证

**验证方法**：对比生成的 message 与实际 git diff 内容

**通过条件**：
1. **message 描述的改动类型与 diff 内容一致**
   - feat: diff 中包含新增的函数/方法/接口
   - fix: diff 中包含错误修复或逻辑调整
   - refactor: diff 中主要是结构调整而非功能变化

2. **message 指定的范围与 diff 中变更的文件路径一致**
   - scope 为 web: 变更文件应在 cmd/web/ 或相关
   - scope 为 .claude/skills/*: 变更文件应在该路径下

3. **message 描述的功能与 diff 内容匹配**
   - 描述"添加用户管理"：diff 应包含用户管理相关代码
   - 描述"修复数据库连接"：diff 应包含数据库相关修复

4. **没有遗漏重要信息**
   - Breaking change: 必须在 message 中体现
   - 重大功能: 必须准确描述
   - 安全修复: 必须明确说明

**不通过示例**：
- ❌ diff 显示修改了 10 个文件，但 message 只提到"添加用户功能"（过于笼统）
- ❌ message 说"修复 web 服务崩溃"，但 diff 主要改动在 data 层（范围不符）
- ❌ diff 包含 API 接口变更，但 message 未提及（遗漏重要信息）

**验证流程控制**：
```
第一层验证 → 通过 → 第二层验证 → 通过 → 第三层验证 → 通过 → 第四层验证 → 通过 → 输出
   ↓              ↓              ↓
 不通过          不通过          不通过
   ↓              ↓              ↓
 调整格式      调整类型/范围   优化语言      完善描述
   ↓              ↓              ↓
 重新验证       重新验证       重新验证       重新验证
```

## 核心规范摘要

### Commit 类型列表（11 种）

- **feat**: 新功能
- **fix**: bug 修复
- **docs**: 文档变更
- **style**: 代码格式（不影响功能）
- **refactor**: 重构（不是新功能也不是修复）
- **perf**: 性能优化
- **test**: 测试相关
- **build**: 构建系统或外部依赖
- **ci**: CI 配置和脚本
- **chore**: 其他不修改 src 或 test 文件
- **revert**: 回退之前的 commit

### 范围选择规则

**标准范围**：web, task, api, internal, docs, build, ci, chore

**路径范围**：点号分隔的路径（如 `.claude/skills/go-import-enforcer`）

### 中文表述基本要求

- 必须使用中文
- 祈使句，首字母小写
- 结尾不加句号
- 简洁明了（50 字以内）
- 避免口语化表达

## 常见问题

**Q: 如何处理多种类型的改动？**

A: 识别主要改动类型：
- 70% 以上为一种类型 → 使用该类型
- 功能为主，修复为辅 → 拆分提交（feat + fix）
- 重构为主，新功能为辅 → 拆分提交（refactor + feat）
- 无法明确区分 → chore (需在描述中详细说明)

**Q: 改动涉及多个范围怎么办？**

A: 分析改动涉及的模块：
- 单一职责改动 → 选择最直接的范围
- 跨层改动 → 选择最上层的范围
- 全局性改动 → 不使用范围
- 配置性改动 → build 或 ci

**Q: 如何描述重构性改动？**

A: 判断改动本质：
- 主要是修复 bug → fix
- 主要是改进设计 → refactor
- 修复 + 轻微重构 → fix (在描述中说明)
- 重构 + 顺便修复 → refactor (在描述中说明)

**Q: 如何避免描述过于笼统或过于细节？**

A: 提炼核心意图：
- ✅ "添加用户管理功能"（适中）
- ❌ "添加功能"（过于笼统）
- ❌ "添加了包含增删改查的用户管理功能"（过于细节）

## 参考资料

详细的 commit 规范、丰富示例和决策流程，请参考：

- [commit-standards.md](references/commit-standards.md) - 完整的 commit message 规范定义
- [examples.md](references/examples.md) - 项目实际示例和通用示例
- [decision-workflows.md](references/decision-workflows.md) - 详细的决策流程和特殊场景处理
