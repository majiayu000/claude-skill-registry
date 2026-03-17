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
| **项目文档目录** | `./docs/` | **工作目录** (执行命令时的当前目录) |

## 标准文档结构

```
docs/
├── adr/                  # 架构决策记录
├── architecture/         # 架构设计文档
├── issues/               # 任务跟踪
│   ├── [模块分类]/        # 可选：按模块分类
│   │   └── yyyymmdd-[描述].md
│   └── yyyymmdd-[描述].md
├── pr/                   # 变更记录
│   ├── [模块分类]/
│   │   └── yyyymmdd-[描述].md
│   └── yyyymmdd-[描述].md
└── guides/               # 使用指南
```

## 调用命令

```bash
# 正确方式：从项目目录执行
cd /path/to/your/project
~/.pi/agent/skills/workhub/lib.ts <command>
```

## 文档操作

### 1. 初始化 (`init`)
创建标准文档目录结构。
```bash
~/.pi/agent/skills/workhub/lib.ts init
```

### 2. 查看结构 (`tree`)
显示文档目录树。
```bash
~/.pi/agent/skills/workhub/lib.ts tree
```

### 3. 审计规范 (`audit`)
检查 `docs/` 文件夹是否遵循标准规范。
```bash
~/.pi/agent/skills/workhub/lib.ts audit
```

### 4. 读取文档 (`read`)
通过关键词或相对路径读取文档。
```bash
~/.pi/agent/skills/workhub/lib.ts read issues/20250106-添加深色模式.md
```

### 5. 创建 Issue (`create issue`)
创建新的 Issue 文件，自动使用模板。
```bash
~/.pi/agent/skills/workhub/lib.ts create issue "添加深色模式" 前端
```

### 6. 创建 PR (`create pr`)
创建新的 PR 文件，自动使用模板。
```bash
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

### 9. 查看状态 (`status`)
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
   → docs/issues/yyyymmdd-[描述].md
   或 docs/issues/[模块分类]/yyyymmdd-[描述].md

2. 填写 Goal、Phases、Acceptance Criteria

3. 执行阶段：
   - Read Issue 文件（刷新目标）
   - 完成子任务 → 更新复选框 [x]
   - 遇到错误 → 记录到 "Errors Encountered"
   - 记录 Notes → 保存研究发现

4. 完成后创建 PR 文件
   → docs/pr/yyyymmdd-[描述].md

5. PR 文件关联 Issue 文件名
   → 包含回滚计划、测试验证
```

### PR 工作流

```
1. 创建 PR 文件 (使用模板)
   → docs/pr/yyyymmdd-[描述].md
   或 docs/pr/[模块分类]/yyyymmdd-[描述].md

2. 填写背景、变更内容、测试验证、回滚计划

3. 关联 Issue 文件名
   → 在 "关联 Issue" 中填写完整路径

4. 代码审查和合并
   → 记录审查日志
   → 更新最终状态
```

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

# 2. 创建 Issue 文件
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
```

### 创建 PR

```bash
# 1. 创建 PR 文件
~/.pi/agent/skills/workhub/lib.ts create pr "添加深色模式" 前端

# 2. 编辑文件，填写变更内容、测试验证、回滚计划

# 3. 关联 Issue 文件名
# 在 "关联 Issue" 中填写完整路径
```

### 错误恢复模式

```bash
# 1. 读取 Issue
~/.pi/agent/skills/workhub/lib.ts read issues/20250106-添加深色模式.md

# 2. 在 "Errors Encountered" 中记录
| 日期 | 错误 | 解决方案 |
| 2025-01-06 | FileNotFoundError | 创建默认配置 |

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
| `read` | 读取文档 | `~/.pi/agent/skills/workhub/lib.ts read issues/xxx.md` |
| `create issue` | 创建 Issue | `~/.pi/agent/skills/workhub/lib.ts create issue "描述" [分类]` |
| `create pr` | 创建 PR | `~/.pi/agent/skills/workhub/lib.ts create pr "描述" [分类]` |
| `list issues` | 列出所有 Issues | `~/.pi/agent/skills/workhub/lib.ts list issues` |
| `list prs` | 列出所有 PRs | `~/.pi/agent/skills/workhub/lib.ts list prs` |
| `status` | 查看整体状态 | `~/.pi/agent/skills/workhub/lib.ts status` |
| `search` | 搜索内容 | `~/.pi/agent/skills/workhub/lib.ts search "关键词"` |

## 扩展计划

未来可能添加的功能：
- 交互式创建 Issue
- 交互式创建 PR
- 关联 Issue 和 PR