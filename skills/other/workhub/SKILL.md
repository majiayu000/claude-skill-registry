---
name: workhub
description: 工作文档枢纽，强制执行 SSOT（Single Source of Truth）原则，管理 `docs/` 目录下的架构决策、设计文档、Issues（任务规划）、PRs（变更记录）。支持 GitHub 协作开发模式。
---

# Workhub

文档管理与任务跟踪工具，强制执行 SSOT（Single Source of Truth）原则，支持 GitHub 风格的 Issues 和 PRs 工作流。

## 执行环境

| 路径类型 | 路径 | 基准目录 |
|---------|------|---------|
| **技能目录** | `~/.pi/agent/skills/workhub/` | 固定位置 |
| **主脚本** | `~/.pi/agent/skills/workhub/lib.ts` | 技能目录 |
| **模板目录** | `~/.pi/agent/skills/workhub/templates/` | 技能目录 |
| **项目文档目录** | `./docs/` | **工作目录** (执行命令时的当前目录) |

## 重要区分

```
注意：这是两个完全不同的目录！

1. 脚本位置（固定）：~/.pi/agent/skills/workhub/lib.ts
   - 这个文件在技能安装目录中，不会移动

2. 文档位置（可变）：./docs/
   - 这个目录在**执行命令时的当前目录**中
   - 即用户的项目根目录
```

## 标准文档结构

```
docs/
├── adr/                  # 架构决策记录 (Architecture Decision Records)
│   └── yyyymmdd-[decision].md
├── architecture/         # 架构设计文档
│   ├── boundaries.md
│   └── data-flow.md
├── issues/               # 任务跟踪 (GitHub Issues 风格)
│   ├── [模块分类]/        # 可选：按职责模块分类（前端/后端/数据库等）
│   │   └── yyyymmdd-[描述].md
│   └── yyyymmdd-[描述].md  # 或直接在 issues/ 根目录
├── pr/                   # 变更记录 (GitHub PR 风格)
│   ├── [模块分类]/        # 可选：按职责模块分类（前端/后端/数据库等）
│   │   └── yyyymmdd-[描述].md
│   └── yyyymmdd-[描述].md  # 或直接在 pr/ 根目录
└── guides/               # 使用指南
    └── [topic].md
```

**说明：**
- `issues/` 和 `pr/` 目录可以包含子目录分类
- 常见分类方式：按职责模块（前端/后端/数据库/运维）、按功能模块（用户系统/订单系统/支付系统）
- 如果项目规模较小，可以直接在 `issues/` 和 `pr/` 根目录下创建文件
- 如果项目规模较大或有明确模块划分，建议使用子目录分类

## 调用命令

```bash
# 正确方式 1：从项目目录执行（推荐）
cd /path/to/your/project
~/.pi/agent/skills/workhub/lib.ts tree     # 查看文档结构
~/.pi/agent/skills/workhub/lib.ts audit    # 审计文档规范
~/.pi/agent/skills/workhub/lib.ts read conventions  # 读取文档
~/.pi/agent/skills/workhub/lib.ts init     # 初始化文档结构

# 正确方式 2：从技能目录执行
cd ~/.pi/agent/skills/workhub
bun run lib.ts tree
bun run lib.ts audit

# 错误方式：假设 lib.ts 在当前目录
cd /path/to/your/project
bun run lib.ts tree   # 错误：lib.ts 在 ~/.pi/agent/skills/workhub/，不在当前目录！
```

## 文档操作

### 1. 初始化文档结构 (`init`)
创建标准文档目录结构。
```bash
~/.pi/agent/skills/workhub/lib.ts init
```

### 2. 查看文档结构 (`tree`)
显示文档目录树。
```bash
~/.pi/agent/skills/workhub/lib.ts tree
```

### 3. 审计文档规范 (`audit`)
检查 `docs/` 文件夹是否遵循标准文档治理规范。
```bash
~/.pi/agent/skills/workhub/lib.ts audit
```

### 4. 读取文档 (`read`)
通过关键词或相对路径读取文档。
```bash
~/.pi/agent/skills/workhub/lib.ts read conventions
~/.pi/agent/skills/workhub/lib.ts read architecture/boundaries.md
~/.pi/agent/skills/workhub/lib.ts read issues/20250106-添加深色模式.md
```

### 5. 创建 Issue (`create issue`)
创建新的 Issue 文件，自动使用模板。
```bash
# 方式 1：在 issues/ 根目录创建
~/.pi/agent/skills/workhub/lib.ts create issue "添加深色模式"

# 方式 2：在子目录中创建（自动创建目录）
~/.pi/agent/skills/workhub/lib.ts create issue "添加深色模式" 前端
```

### 6. 创建 PR (`create pr`)
创建新的 PR 文件，自动使用模板。
```bash
# 方式 1：在 pr/ 根目录创建
~/.pi/agent/skills/workhub/lib.ts create pr "修复登录bug"

# 方式 2：在子目录中创建（自动创建目录）
~/.pi/agent/skills/workhub/lib.ts create pr "修复登录bug" 后端
```

### 7. 列出 Issues (`list issues`)
列出所有 Issues 及其状态。
```bash
~/.pi/agent/skills/workhub/lib.ts list issues
```

### 8. 列出 PRs (`list prs`)
列出所有 PRs 及其状态。
```bash
~/.pi/agent/skills/workhub/lib.ts list prs
```

### 9. 查看整体状态 (`status`)
显示所有 Issues 和 PRs 的状态概览。
```bash
~/.pi/agent/skills/workhub/lib.ts status
```

### 10. 搜索内容 (`search`)
在 Issues 和 PRs 中搜索关键词。
```bash
~/.pi/agent/skills/workhub/lib.ts search "深色模式"
```

## GitHub 风格工作流

### Issue 工作流

```
1. 创建 Issue 文件 (使用模板)
   方式 1：直接在 issues/ 根目录（适合小型项目）
   → docs/issues/yyyymmdd-[描述].md
   示例: docs/issues/20250106-添加深色模式.md

   方式 2：在子目录中创建（适合有模块划分的项目）
   → docs/issues/[模块分类]/yyyymmdd-[描述].md
   示例: docs/issues/前端/20250106-添加深色模式.md

2. 填写 Goal、Phases、Acceptance Criteria

3. 执行阶段：
   - Read Issue 文件（刷新目标）
   - 完成子任务 → 更新复选框 [x]
   - 遇到错误 → 记录到 "Errors Encountered"
   - 记录 Notes → 保存研究发现

4. 完成后创建 PR 文件
   → docs/pr/yyyymmdd-[描述].md
   或 docs/pr/[模块分类]/yyyymmdd-[描述].md

5. PR 文件关联 Issue 文件名（包含完整路径）
   → 包含回滚计划、测试验证
```

### Issue 模板结构

```markdown
# Issue: [标题]

## 元数据
- 文件名: yyyymmdd-[描述].md
- 状态: 待办 / 进行中 / 已完成
- 优先级: P0 / P1 / P2 / P3

## Goal
[一句话描述最终状态]

## 验收标准
- [ ] WHEN [条件]，系统 SHALL [行为]
- [ ] WHERE [上下文]，系统 SHALL [行为]

## 实施阶段
### Phase 1: 规划和准备
- [ ] [子任务 1]
- [ ] [子任务 2]

### Phase 2: 执行
- [ ] [子任务 3]
- [ ] [子任务 4]

## 关键决策
| 决策 | 理由 |
|------|------|

## 遇到的错误
| 日期 | 错误 | 解决方案 |

## Notes
[研究过程、临时想法]

## Status 更新日志
- [日期]: 状态变更 → [新状态]
```

### PR 模板结构

```markdown
# [Pull Request 标题]

> 简明扼要描述本次变更的核心目的

## 背景与目的 (Why)
<!-- 说明为什么要进行本次变更 -->

## 变更内容概述 (What)
<!-- 列出主要修改点 -->

## 关联 Issue 与 ToDo 条目 (Links)
- **Issues:** `docs/issues/yyyymmdd-[描述].md`
- **ToDo:** [可选] `docs/todolist/xxx系统/yyyymmdd-xxx.md`

## 测试与验证结果 (Test Result)
- [ ] 单元测试通过
- [ ] 集成测试验证
- [ ] 手动回归测试通过

## 风险与影响评估 (Risk Assessment)
<!-- 说明可能的风险点、影响范围 -->

## 回滚方案 (Rollback Plan)
<!-- 如果出现问题，如何快速回退到稳定版本 -->
```

## Markdown 风格

Issues 和 PRs 文件使用 Markdown 格式，支持 Mermaid 图表。

## 核心原则

### 1. SSOT (Single Source of Truth)
- 每个知识领域只有一个权威文档
- Issues 是任务跟踪的唯一来源
- PRs 是变更记录的唯一来源

### 2. 文件系统即记忆
- 大输出内容保存到文件，而非堆砌到上下文
- 工作记忆中只保留文件路径
- 需要时通过 `workhub read` 读取

### 3. 状态管理
- **决策前读取 Issue**：刷新目标，保持注意力
- **行动后更新 Issue**：标记 [x]，更新 Status
- **错误记录**：在 Issue 的 "Errors Encountered" 中记录

### 4. 变更可追溯
- 每个 PR 必须关联 Issue
- Issue 记录完整决策过程
- PR 记录变更细节和回滚计划

## 最佳实践

### 创建 Issue

```bash
# 1. 初始化文档结构（首次）
~/.pi/agent/skills/workhub/lib.ts init

# 2. 创建 Issue 文件（推荐方式）
~/.pi/agent/skills/workhub/lib.ts create issue "添加深色模式" 前端

# 3. 编辑文件，填写 Goal、Phases、Acceptance Criteria
```

### 执行 Issue

```bash
# 1. 读取 Issue（刷新目标）
~/.pi/agent/skills/workhub/lib.ts read issues/前端/20250106-添加深色模式.md

# 2. 完成子任务后更新 Issue
# 编辑文件，标记复选框 [x]

# 3. 遇到错误时记录
# 在 "Errors Encountered" 表格中添加记录

# 4. 研究发现保存到 Notes
```

### 创建 PR

```bash
# 1. 创建 PR 文件（推荐方式）
~/.pi/agent/skills/workhub/lib.ts create pr "添加深色模式" 前端

# 2. 编辑文件，填写变更内容、测试验证、回滚计划

# 3. 关联 Issue 文件名
# 在 "关联 Issue 与 ToDo 条目" 中填写:
# - Issues: docs/issues/前端/20250106-添加深色模式.md
```

### 查看状态

```bash
# 查看所有 Issues
~/.pi/agent/skills/workhub/lib.ts list issues

# 查看所有 PRs
~/.pi/agent/skills/workhub/lib.ts list prs

# 查看整体状态
~/.pi/agent/skills/workhub/lib.ts status
```

### 搜索内容

```bash
# 搜索关键词
~/.pi/agent/skills/workhub/lib.ts search "深色模式"
```

### 状态跟踪

```markdown
## Status 更新日志
- 2025-01-06 10:00: 状态变更 → 进行中，备注: 开始 Phase 2
- 2025-01-06 14:30: 状态变更 → 已完成，备注: 所有测试通过
```

## 错误恢复模式

### 错误方式
```
[执行失败]
[静默重试]
[再次失败]
[继续尝试]
```

### 正确方式
```bash
# 1. 读取 Issue
~/.pi/agent/skills/workhub/lib.ts read issues/20250106-添加深色模式.md

# 2. 在 "Errors Encountered" 中记录
| 日期 | 错误 | 解决方案 |
| 2025-01-06 | FileNotFoundError: config.json | 将创建默认配置 |

# 3. 执行解决方案
# 创建默认配置文件

# 4. 更新 Issue 的 Notes
```

## Quick Reference

| 命令 | 功能 | 示例 |
|------|------|------|
| `init` | 初始化文档结构 | `~/.pi/agent/skills/workhub/lib.ts init` |
| `tree` | 查看文档结构 | `~/.pi/agent/skills/workhub/lib.ts tree` |
| `audit` | 审计文档规范 | `~/.pi/agent/skills/workhub/lib.ts audit` |
| `read` | 读取文档 | `~/.pi/agent/skills/workhub/lib.ts read issues/20250106-添加深色模式.md` |
| `create issue` | 创建 Issue | `~/.pi/agent/skills/workhub/lib.ts create issue "添加深色模式" 前端` |
| `create pr` | 创建 PR | `~/.pi/agent/skills/workhub/lib.ts create pr "修复登录bug" 后端` |
| `list issues` | 列出所有 Issues | `~/.pi/agent/skills/workhub/lib.ts list issues` |
| `list prs` | 列出所有 PRs | `~/.pi/agent/skills/workhub/lib.ts list prs` |
| `status` | 查看整体状态 | `~/.pi/agent/skills/workhub/lib.ts status` |
| `search` | 搜索内容 | `~/.pi/agent/skills/workhub/lib.ts search "深色模式"` |

## 扩展计划

未来可能添加的功能：
- 交互式创建 Issue
- 交互式创建 PR
- 关联 Issue 和 PR

