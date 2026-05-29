---
name: task-manager
description: 统一任务管理技能，使用 GitHub Issues 管理所有 Agent 任务，支持任务创建、更新、追踪和完成
version: 1.0.0
---

# 任务管理技能 (Task Manager)

## 触发条件
当用户提到以下内容时自动触发:
- "任务管理"
- "创建任务"
- "更新任务"
- "任务追踪"
- "完成任务"
- "gh issue"

## 核心能力

### 任务创建

```bash
# 创建标准任务
gh issue create \
  --title "[类型] 任务标题" \
  --body "任务描述" \
  --label "enhancement"

# 创建带里程碑的任务
gh issue create \
  --title "[类型] 任务标题" \
  --body "任务描述" \
  --milestone "Q1-2025" \
  --label "priority/high"
```

### 任务标签体系

| 标签 | 描述 | 使用场景 |
|------|------|----------|
| `enhancement` | 新功能/改进 | 功能开发、优化 |
| `bug` | 缺陷修复 | Bug 修复 |
| `documentation` | 文档更新 | 文档编写 |
| `infrastructure` | 基础设施 | 运维、部署 |
| `security` | 安全相关 | 安全修复 |
| `priority/high` | 高优先级 | 紧急任务 |
| `priority/medium` | 中优先级 | 普通任务 |
| `priority/low` | 低优先级 | 长期任务 |

### 任务类型前缀

| 前缀 | Agent | 示例 |
|------|-------|------|
| `[CEO]` | 首席执行官 | `[CEO] 制定 Q1 战略` |
| `[COO]` | 首席运营官 | `[COO] 市场推广计划` |
| `[CFO]` | 财务总监 | `[CFO] 年度预算` |
| `[CTO]` | 首席技术官 | `[CTO] 架构升级` |
| `[CIO]` | 首席信息官 | `[CIO] 安全审计` |
| `[PM]` | 产品经理 | `[PM] 用户需求分析` |
| `[DESIGN]` | 设计师 | `[DESIGN] UI 更新` |
| `[LEGAL]` | 法务顾问 | `[LEGAL] 合同审核` |
| `[MKT]` | 市场运营 | `[MKT] 社交媒体活动` |

### 任务状态管理

```bash
# 查看所有待办任务
gh issue list --state open

# 查看已关闭任务
gh issue list --state closed

# 查看特定标签任务
gh issue list --label "enhancement"

# 查看特定里程碑任务
gh issue list --milestone "Q1-2025"

# 更新任务状态
gh issue close <issue-number>        # 关闭任务
gh issue reopen <issue-number>       # 重新开启

# 添加标签
gh issue edit <issue-number> --add-label "priority/high"

# 分配任务
gh issue edit <issue-number> --assignee "liubinbin"
```

### 任务详情模板

```
## 任务描述
[描述任务的目标和背景]

## 验收标准
- [ ] 标准 1
- [ ] 标准 2
- [ ] 标准 3

## 相关资源
- 文档链接
- 相关 Issue
- 设计稿

## 预计工时
X 小时

## 实际工时
Y 小时

## 任务状态
- [ ] 待开始
- [ ] 进行中
- [ ] 待审核
- [ ] 已完成
```

## 使用流程

### 1. 日常任务管理

```
每日工作开始:
├── gh issue list --state open               # 查看待办任务
├── 选择优先级最高的任务
└── 开始执行

任务执行中:
├── 更新任务进度 (如需要)
└── 记录实际工时

每日工作结束:
├── 更新任务状态
└── 创建明日任务 (如需要)
```

### 2. 周度任务回顾

```
每周五:
├── gh issue list --state open --label "enhancement"  # 检查功能任务
├── gh issue list --state open --label "bug"          # 检查 Bug
├── 关闭已完成任务
├── 更新待处理任务状态
└── 创建下周任务
```

### 3. 任务规划

```bash
# 创建季度里程碑
gh issue create \
  --title "[规划] Q1 2025 里程碑" \
  --body "第一季度目标设定" \
  --milestone "Q1-2025"

# 关联相关任务
gh issue edit <issue-number> --milestone "Q1-2025"
```

## 各 Agent 任务管理

### CEO Agent 任务

```bash
# 战略规划
gh issue create --title "[CEO] 制定年度战略" --body "..." --label "strategy"

# 重大决策
gh issue create --title "[CEO] 产品方向决策" --body "..." --label "decision"
```

### COO Agent 任务

```bash
# 运营管理
gh issue create --title "[COO] 优化运营流程" --body "..." --label "operations"

# 市场活动
gh issue create --title "[COO] 春节营销活动" --body "..." --label "marketing"
```

### CFO Agent 任务

```bash
# 财务管理
gh issue create --title "[CFO] 年度预算编制" --body "..." --label "finance"

# 成本分析
gh issue create --title "[CFO] Q1 成本分析" --body "..." --label "analysis"
```

### CTO Agent 任务

```bash
# 技术规划
gh issue create --title "[CTO] 技术路线图" --body "..." --label "planning"

# 架构升级
gh issue create --title "[CTO] 微服务改造" --body "..." --label "architecture"
```

### CIO Agent 任务

```bash
# IT 运维
gh issue create --title "[CIO] 服务器监控配置" --body "..." --label "infrastructure"

# 安全合规
gh issue create --title "[CIO] 安全审计" --body "..." --label "security"
```

### 产品经理任务

```bash
# 需求分析
gh issue create --title "[PM] 用户调研" --body "..." --label "research"

# 产品规划
gh issue create --title "[PM] v2.0 功能规划" --body "..." --label "planning"
```

### 设计师任务

```bash
# UI 设计
gh issue create --title "[DESIGN] 首页改版" --body "..." --label "design"

# 交互优化
gh issue create --title "[DESIGN] 登录流程优化" --body "..." --label "ux"
```

### 法务顾问任务

```bash
# 合同审核
gh issue create --title "[LEGAL] 供应商合同审核" --body "..." --label "contract"

# 合规检查
gh issue create --title "[LEGAL] GDPR 合规" --body "..." --label "compliance"
```

### 市场运营任务

```bash
# 内容创作
gh issue create --title "[MKT] 产品介绍文章" --body "..." --label "content"

# 社交媒体
gh issue create --title "[MKT] 小红书推广" --body "..." --label "social"
```

## 批量操作

### 批量创建任务

```bash
# 创建多个任务
gh issue create --title "[TASK] 任务1" --body "..."
gh issue create --title "[TASK] 任务2" --body "..."
gh issue create --title "[TASK] 任务3" --body "..."
```

### 批量更新状态

```bash
# 查看并关闭已完成任务
gh issue list --state open --assignee "liubinbin" --json number,title
# 手动确认后关闭
gh issue close <number>
```

### 任务统计

```bash
# 统计任务数量
gh issue list --state open | wc -l

# 统计各标签任务
gh issue list --state open --label "bug" | wc -l
gh issue list --state open --label "enhancement" | wc -l

# 导出任务列表
gh issue list --state open --json number,title,labels,assignee > tasks.json
```

## 输出模板

### 任务报告模板

```
# 任务报告

## 报告周期
- 开始日期: YYYY-MM-DD
- 结束日期: YYYY-MM-DD

## 任务完成情况
| 任务 | 状态 | 工时 |
|------|------|------|
| XXX | ✅ 完成 | 4h |
| XXX | 🔄 进行中 | 2h |
| XXX | ⏳ 待开始 | - |

## 新建任务
- [ ] 任务1
- [ ] 任务2

## 待处理任务
- [ ] 任务1
- [ ] 任务2

## 下周计划
- [ ] 计划1
- [ ] 计划2
```

## GitHub Actions 集成

```yaml
# .github/workflows/task-management.yml
name: Task Management
on:
  issues:
    types: [opened, closed, labeled]
jobs:
  track-task:
    runs-on: ubuntu-latest
    steps:
      - name: Log task event
        run: |
          echo "Issue ${{ github.event.issue.number }} - ${{ github.event.issue.title }}"
          echo "Action: ${{ github.event.action }}"
          echo "Labels: ${{ join(github.event.issue.labels.*.name, ', ') }}"
```

## 最佳实践

### 任务命名规范
- 使用 `[Agent前缀]` 标识任务来源
- 使用英语描述，简洁明了
- 包含关键信息: 什么+做什么

### 任务描述规范
- 说明任务背景和目标
- 列出具体验收标准
- 预估工时，便于排期

### 任务更新规范
- 每日更新任务进度
- 完成后立即关闭
- 记录实际工时，便于复盘

## KPI 指标

| 指标 | 目标值 | 测量频率 |
|------|--------|----------|
| 任务完成率 | 90%+ | 每周 |
| 按时完成率 | 80%+ | 每周 |
| 平均任务周期 | <3 天 | 每周 |
| 任务工时准确度 | ±20% | 每月 |
