---
name: create-issue
version: "1.0.0"
last-updated: "2026-03-18"
description: |
  Create GitHub issues with intelligent size validation and recommendations.

  TRIGGER when:
  - User wants to create a new issue ("create issue", "new issue")
  - User mentions issue templates ("use bug template", "issue template")
  - User asks about issue size ("estimate issue size", "check if issue too large")
  - User wants batch issue creation ("create multiple issues", "batch create")
  - User mentions deduplication ("check for duplicates", "similar issues exist?")

  DO NOT TRIGGER when:
  - Viewing existing issues (use gh issue view)
  - Editing/updating issues (use gh issue edit)
  - Closing issues (use gh issue close)
  - Discussing issues conceptually without creating
  - Working on existing issues (use /start-issue, /work-issue)
category: project-management
allowed-tools:
  - Bash
  - Read
  - Write
---

# create-issue - 智能 GitHub Issue 创建工具

自动化创建 GitHub issues，并提供智能的尺寸验证、去重检测和模板支持。

## 核心功能

### 1. 尺寸验证和建议（关键功能）

创建 issue 前自动分析任务规模，确保 issue 尺寸合理：

- **理想尺寸**：3-5 个任务，2-3 小时完成
- **推荐限制**：≤8 个任务，≤4 小时
- **硬限制**：≤15 个任务，≤8 小时（超过将阻止创建）

**尺寸分析指标**：
- 任务数量（从 issue body 解析）
- 估算时间/复杂度
- 影响文件数量
- 代码行数估算

**建议类型**：
- ✅ **PASS** - 尺寸理想，可直接创建
- ⚠️ **WARN** - 尺寸偏大，建议拆分
- 🚫 **BLOCK** - 尺寸过大，必须拆分

### 2. 去重检测

自动检测与现有 issues 的相似度：

- 计算标题和内容的相似度分数
- >80% 相似度时警告可能重复
- 提供现有 issue 链接供参考

### 3. 模板支持

从 `.claude/issue-templates/` 加载预定义模板：

- `bug.md` - Bug 报告模板
- `feature.md` - 新功能请求
- `enhancement.md` - 功能改进
- 自定义模板

### 4. 批量创建

从 markdown 文件批量创建 issues：

- 解析 markdown 文件中的多个 issues
- 自动分配标签和优先级
- 生成创建摘要报告

## 使用方法

### 基础创建

```bash
# 创建单个 issue（交互式）
/create-issue

# 使用标题和描述创建
/create-issue --title "Add authentication" --body "Implement JWT auth..."

# 使用模板创建
/create-issue --template feature --title "Add dark mode"

# 批量创建
/create-issue --from issues.md

# 仅估算尺寸（不创建）
/create-issue --estimate-only --title "Refactor database layer"
```

### 高级用法

```bash
# 指定标签和优先级
/create-issue --title "Fix login bug" --labels "bug,P0" --priority high

# 强制创建（跳过尺寸检查）
/create-issue --force --title "Large refactoring"

# 自动拆分过大的 issue
/create-issue --auto-split --title "Implement payment system"

# 仅检查去重
/create-issue --check-duplicate --title "Add dark mode"
```

## 参数说明

| 参数 | 必需 | 描述 | 示例 |
|------|------|------|------|
| `--title` | 是* | Issue 标题 | `--title "Add dark mode"` |
| `--body` | 否 | Issue 描述 | `--body "详细描述..."` |
| `--template` | 否 | 使用模板 | `--template feature` |
| `--labels` | 否 | 标签列表（逗号分隔） | `--labels "bug,P0"` |
| `--priority` | 否 | 优先级 | `--priority high` |
| `--from` | 否 | 从文件批量创建 | `--from issues.md` |
| `--estimate-only` | 否 | 仅估算尺寸 | `--estimate-only` |
| `--force` | 否 | 跳过尺寸检查 | `--force` |
| `--auto-split` | 否 | 自动拆分过大的 issue | `--auto-split` |
| `--check-duplicate` | 否 | 仅检查去重 | `--check-duplicate` |
| `--dry-run` | 否 | 预览不创建 | `--dry-run` |

*注：交互模式下可选

## 尺寸指南

### 为什么要控制 Issue 尺寸？

**问题现象**：
- ❌ Issue 包含 15+ 个任务，开发 2-3 天
- ❌ PR 超过 1000 行代码，审查困难
- ❌ 合并冲突频繁，回滚影响大
- ❌ 测试覆盖不足，质量风险高

**解决方案**：
- ✅ 限制每个 issue 3-5 个任务（理想）
- ✅ 单个 issue ≤4 小时完成（推荐）
- ✅ PR ≤300 行代码，易于审查
- ✅ 快速迭代，降低风险

### 尺寸规则详解

#### 1️⃣ 理想尺寸（PASS）

**标准**：
- 任务数：3-5 个任务
- 时间：2-3 小时
- 代码量：100-200 行
- 文件数：3-5 个文件

**示例**：
```markdown
## Tasks
1. 创建 Login 组件
2. 添加表单验证
3. 集成 API 调用
4. 添加错误处理
5. 编写单元测试
```

**结果**：✅ PASS - 尺寸理想，可直接创建

#### 2️⃣ 推荐限制（WARN）

**标准**：
- 任务数：6-8 个任务
- 时间：3-4 小时
- 代码量：200-300 行
- 文件数：6-8 个文件

**示例**：
```markdown
## Tasks
1. 设计数据库 schema
2. 创建 migration 文件
3. 实现 CRUD API
4. 添加输入验证
5. 实现错误处理
6. 添加日志记录
7. 编写集成测试
8. 更新文档
```

**结果**：⚠️ WARN - 建议拆分为 2 个 issues：
- Issue 1: 数据库设计和 migration（任务 1-2）
- Issue 2: API 实现和测试（任务 3-8）

#### 3️⃣ 硬限制（BLOCK）

**标准**：
- 任务数：>15 个任务
- 时间：>8 小时
- 代码量：>500 行
- 文件数：>15 个文件

**示例**：
```markdown
## Tasks
1. 设计认证系统架构
2. 实现 JWT token 生成
3. 添加 refresh token 机制
4. 实现用户注册流程
5. 添加邮箱验证
6. 实现密码重置
7. 添加第三方登录（Google, GitHub）
8. 实现权限管理系统
9. 添加角色和权限表
10. 实现 RBAC 中间件
11. 添加审计日志
12. 实现会话管理
13. 添加双因素认证
14. 编写集成测试
15. 更新安全文档
16. 性能优化
```

**结果**：🚫 BLOCK - 必须拆分，建议创建 4 个 issues：
- Issue 1: 基础认证（任务 1-4）
- Issue 2: 高级功能（任务 5-7）
- Issue 3: 权限系统（任务 8-10）
- Issue 4: 安全增强（任务 11-16）

### 自动拆分建议

当检测到超大 issue 时，工具会自动生成拆分建议：

```yaml
原始 issue: "实现完整的认证系统"（16 个任务）

拆分建议:
  - issue_1:
      title: "实现基础认证功能"
      tasks: [1, 2, 3, 4]
      priority: P0
      estimate: 3 hours

  - issue_2:
      title: "添加高级认证功能"
      tasks: [5, 6, 7]
      priority: P1
      estimate: 4 hours
      dependencies: [issue_1]

  - issue_3:
      title: "实现权限管理系统"
      tasks: [8, 9, 10]
      priority: P1
      estimate: 3 hours
      dependencies: [issue_1]

  - issue_4:
      title: "增强安全和性能"
      tasks: [11, 12, 13, 14, 15, 16]
      priority: P2
      estimate: 4 hours
      dependencies: [issue_2, issue_3]
```

## 模板系统

### 内置模板

#### Bug 模板 (`bug.md`)

```markdown
## Bug 描述
简要描述 bug

## 复现步骤
1. 访问 /login 页面
2. 输入错误密码
3. 点击登录

## 期望行为
显示错误提示

## 实际行为
应用崩溃

## 环境
- OS: macOS 14
- Browser: Chrome 120
- Version: 1.0.0

## 任务
1. 定位问题根因
2. 修复 bug
3. 添加回归测试
4. 更新错误处理文档
```

#### Feature 模板 (`feature.md`)

```markdown
## 功能描述
详细描述新功能

## 用户价值
为什么需要这个功能

## 用户故事
作为 [用户角色]，我希望 [功能]，以便 [价值]

## 验收标准
- [ ] 标准 1
- [ ] 标准 2
- [ ] 标准 3

## 任务
1. 设计 API
2. 实现后端逻辑
3. 创建前端组件
4. 添加测试
5. 编写文档
```

#### Enhancement 模板 (`enhancement.md`)

```markdown
## 改进内容
详细描述改进点

## 当前问题
现有实现的局限性

## 改进方案
如何解决这些问题

## 影响范围
- 影响的文件
- 影响的功能
- 潜在风险

## 任务
1. 分析现有代码
2. 设计改进方案
3. 实现改进
4. 验证改进效果
```

### 自定义模板

在 `.claude/issue-templates/` 创建自定义模板：

```bash
# 创建自定义模板
cat > .claude/issue-templates/refactoring.md << 'EOF'
## 重构目标
[描述重构目的]

## 现有问题
1. 问题 1
2. 问题 2

## 重构方案
详细方案

## 风险评估
- 风险 1
- 风险 2

## 任务
1. 任务 1
2. 任务 2
3. 任务 3
4. 任务 4

## 验证计划
- [ ] 单元测试覆盖率 >80%
- [ ] 集成测试通过
- [ ] 性能无退化
EOF

# 使用自定义模板
/create-issue --template refactoring --title "重构认证模块"
```

## 去重检测

### 相似度计算

使用多维度相似度算法：

```python
def calculate_similarity(new_issue, existing_issue):
    """计算两个 issue 的相似度分数（0-100）"""

    # 1. 标题相似度（权重 40%）
    title_similarity = cosine_similarity(
        new_issue.title,
        existing_issue.title
    )

    # 2. 内容相似度（权重 40%）
    content_similarity = cosine_similarity(
        new_issue.body,
        existing_issue.body
    )

    # 3. 标签重叠度（权重 20%）
    label_overlap = len(
        set(new_issue.labels) & set(existing_issue.labels)
    ) / len(set(new_issue.labels) | set(existing_issue.labels))

    # 加权平均
    total_similarity = (
        title_similarity * 0.4 +
        content_similarity * 0.4 +
        label_overlap * 0.2
    )

    return total_similarity * 100
```

### 去重规则

| 相似度 | 操作 | 说明 |
|--------|------|------|
| >90% | 🚫 阻止创建 | 几乎完全重复 |
| 80-90% | ⚠️ 强警告 | 高度相似，建议检查 |
| 60-80% | ℹ️ 提示 | 可能相关，供参考 |
| <60% | ✅ 允许创建 | 相似度低，安全 |

### 去重报告示例

```
🔍 去重检测结果

发现 2 个相似的 issues:

1. Issue #123: "Add user authentication" (相似度: 85%)
   https://github.com/user/repo/issues/123
   状态: open
   标签: enhancement, auth

   建议: 这个 issue 可能已经在处理类似问题，建议先检查

2. Issue #456: "Implement login system" (相似度: 72%)
   https://github.com/user/repo/issues/456
   状态: closed
   标签: feature, auth

   提示: 相关的已关闭 issue，可能有参考价值

⚠️ 是否继续创建新 issue? [y/N]
```

## 批量创建

### 输入格式

从 markdown 文件批量创建 issues：

```markdown
# issues.md

---
title: Add dark mode support
labels: feature, P1
template: feature
---

## Description
Implement dark mode for the application

## Tasks
1. Design dark mode color scheme
2. Update CSS variables
3. Add theme toggle component
4. Persist user preference
5. Update documentation

---
title: Fix login validation
labels: bug, P0
template: bug
---

## Description
Login form validation is broken

## Tasks
1. Identify validation logic bug
2. Fix validation
3. Add unit tests
4. Update error messages
```

### 批量创建命令

```bash
# 从文件批量创建
/create-issue --from issues.md

# 预览批量创建（不实际创建）
/create-issue --from issues.md --dry-run

# 批量创建时跳过去重检测
/create-issue --from issues.md --skip-duplicate-check

# 批量创建时自动拆分过大的 issues
/create-issue --from issues.md --auto-split
```

### 批量创建报告

```
📊 批量创建报告

总计: 10 个 issues
✅ 成功: 8 个
⚠️ 跳过: 1 个（去重检测）
🚫 失败: 1 个（尺寸超限）

创建的 issues:
1. #101: Add dark mode support (3 tasks, 2h)
2. #102: Fix login validation (4 tasks, 3h)
3. #103: Optimize database queries (5 tasks, 3h)
...

跳过的 issues:
- "Add user profile" - 与 #89 相似度 87%

失败的 issues:
- "Implement payment system" - 16 个任务，超过硬限制（15）
  建议拆分为 3 个 issues（使用 --auto-split）

总时间估算: 24 小时
平均任务数: 4.2 个/issue
```

## 工作流集成

### 与 work-issue 集成

```bash
# 创建 issue 后立即开始工作
/create-issue --title "Add authentication" && /work-issue #<new-issue-number>

# 或使用管道
/create-issue --title "Add authentication" | xargs /work-issue
```

### 与其他技能集成

```bash
# 创建 issue 后添加到计划
/create-issue --title "Refactor API" && /plan add #<new-issue-number>

# 批量创建后生成概览
/create-issue --from sprint-plan.md && /overview
```

## 配置

### 默认设置

在 `.claude/config/create-issue.yml` 配置默认行为：

```yaml
# .claude/config/create-issue.yml
defaults:
  # 默认标签
  labels: ["enhancement"]

  # 默认优先级
  priority: "P2"

  # 默认模板
  template: "feature"

  # 尺寸检查
  size_check:
    enabled: true
    strict_mode: false  # true 时强制执行硬限制

  # 去重检测
  duplicate_check:
    enabled: true
    threshold: 80  # 相似度阈值

  # 自动拆分
  auto_split:
    enabled: false
    max_tasks_per_issue: 5

# 尺寸限制（可自定义）
size_limits:
  ideal:
    tasks: [3, 5]
    hours: [2, 3]
    lines: [100, 200]
    files: [3, 5]

  recommended:
    tasks: 8
    hours: 4
    lines: 300
    files: 8

  hard:
    tasks: 15
    hours: 8
    lines: 500
    files: 15

# 模板路径
templates_dir: ".claude/issue-templates"

# GitHub 设置
github:
  # 默认仓库（留空使用当前仓库）
  repo: ""

  # 自动分配
  auto_assign: true
  assignee: "@me"
```

## 最佳实践

### 1. 遵循 INVEST 原则

优秀的 issue 应该是：

- **I**ndependent - 独立的（不依赖其他 issue）
- **N**egotiable - 可协商的（可以调整实现方式）
- **V**aluable - 有价值的（提供用户价值）
- **E**stimable - 可估算的（能估算工作量）
- **S**mall - 小的（2-4 小时完成）
- **T**estable - 可测试的（有明确验收标准）

### 2. 编写清晰的任务列表

**好的任务列表**：
```markdown
## Tasks
1. 创建 UserService 类，实现 CRUD 方法
2. 添加输入验证（邮箱、密码格式）
3. 实现错误处理（用户不存在、重复邮箱）
4. 编写单元测试（覆盖率 >80%）
5. 更新 API 文档
```

**不好的任务列表**：
```markdown
## Tasks
1. 用户管理
2. 验证
3. 测试
4. 文档
```

### 3. 使用模板提高效率

```bash
# 为不同类型的 issue 创建专用模板
/create-issue --template bug --title "Fix memory leak"
/create-issue --template feature --title "Add export functionality"
/create-issue --template refactoring --title "Optimize database queries"
```

### 4. 定期检查 issue 尺寸

```bash
# 使用仅估算模式检查 issue 尺寸
/create-issue --estimate-only --from backlog.md

# 分析现有 issues 的尺寸分布
/analyze-issues --size-distribution
```

## 故障排除

### 常见问题

**1. gh CLI 未认证**

```bash
# 解决方案：登录 GitHub
gh auth login
```

**2. 无法检测到仓库**

```bash
# 解决方案：在 git 仓库根目录运行
cd /path/to/your/repo
/create-issue
```

**3. 模板文件不存在**

```bash
# 解决方案：创建模板目录
mkdir -p .claude/issue-templates

# 复制默认模板
cp framework/.claude-template/issue-templates/* .claude/issue-templates/
```

**4. 尺寸检查误报**

```bash
# 解决方案：使用 --force 跳过检查
/create-issue --force --title "Complex but necessary refactoring"

# 或调整配置文件中的限制
vim .claude/config/create-issue.yml
```

## 示例场景

### 场景 1: 创建标准功能 issue

```bash
/create-issue \
  --template feature \
  --title "Add user profile page" \
  --labels "feature,P1" \
  --body "Allow users to view and edit their profile information"
```

**输出**：
```
✅ 尺寸验证通过
   任务数: 4 (理想范围: 3-5)
   估算时间: 3 小时
   预估代码量: 150 行

🔍 去重检测
   未发现相似 issue

📝 创建 issue #267
   https://github.com/user/repo/issues/267

   标题: Add user profile page
   标签: feature, P1
   估算: 3 小时, 4 任务
```

### 场景 2: 自动拆分过大的 issue

```bash
/create-issue \
  --auto-split \
  --title "Implement complete payment system" \
  --body "$(cat payment-requirements.md)"
```

**输出**：
```
⚠️ 尺寸超限检测
   原始任务数: 18 (硬限制: 15)

🔄 自动拆分建议
   将拆分为 3 个 issues:

   1. "Implement payment gateway integration" (6 tasks, 4h)
   2. "Add payment UI and validation" (5 tasks, 3h)
   3. "Implement payment webhooks and notifications" (7 tasks, 4h)

📝 创建 3 个 issues:
   #268: Implement payment gateway integration
   #269: Add payment UI and validation (depends on #268)
   #270: Implement payment webhooks (depends on #268)

✅ 创建完成
   总估算: 11 小时
   建议顺序: #268 → #269, #270
```

### 场景 3: 批量创建 sprint 计划

```bash
# sprint-backlog.md 包含 10 个 issues
/create-issue --from sprint-backlog.md --dry-run
```

**输出**：
```
🔍 预览批量创建（共 10 个 issues）

✅ 通过尺寸检查: 7 个
⚠️ 需要拆分: 2 个
🚫 重复检测: 1 个

详细信息:
1. ✅ "Add export to CSV" (4 tasks, 2h)
2. ✅ "Fix pagination bug" (3 tasks, 2h)
3. ⚠️ "Refactor authentication" (12 tasks, 6h) - 建议拆分为 2 个
4. 🚫 "Add dark mode" - 与 #245 相似度 88%
...

💡 建议:
   - 使用 --auto-split 自动拆分 2 个过大的 issues
   - 检查 #245 避免重复创建

执行创建: /create-issue --from sprint-backlog.md --auto-split
```

## 成功指标

跟踪 create-issue 技能的有效性：

```python
metrics = {
    # 尺寸控制
    "issues_within_ideal_size": ">70%",      # 3-5 个任务
    "issues_within_recommended": ">90%",     # ≤8 个任务
    "avg_tasks_per_issue": "4.5",            # 理想: 3-5

    # 质量改进
    "duplicate_prevention_rate": ">95%",     # 避免重复
    "auto_split_acceptance": ">80%",         # 拆分建议采纳率

    # 效率提升
    "issue_completion_rate": "+15%",         # 完成率提升
    "pr_approval_rate": "+10%",              # PR 通过率提升
    "avg_pr_review_time": "-30%",            # 审查时间减少

    # 工作流影响
    "work_issue_success_rate": ">95%",       # work-issue 成功率
    "merge_conflict_rate": "-40%",           # 冲突减少
}
```

## 版本历史

### v1.0.0 (2026-03-18)

**初始版本**：
- ✅ 尺寸验证和建议系统
- ✅ 去重检测
- ✅ 模板支持（bug, feature, enhancement）
- ✅ 批量创建
- ✅ 自动拆分建议
- ✅ 与 work-issue 集成

**已知限制**：
- 仅支持 GitHub（未来可扩展 GitLab, Bitbucket）
- 尺寸估算基于规则（未来可使用机器学习）
- 相似度计算较简单（未来可使用语义分析）

## 许可证

MIT License - 详见 LICENSE.txt

---

**Version:** 1.0.0
**Last Updated:** 2026-03-10
**Changelog:**
- v1.0.0 (2026-03-10): Initial release - GitHub issue creation with templates and validation
