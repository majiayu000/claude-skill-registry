---
name: github-automation
description: 自动化 GitHub 操作。当用户需要管理仓库、创建 PR、处理 Issue、自动化 CI/CD 或进行代码审查时使用此技能。
allowed-tools: mcp__github__*, Bash, Read, Write, Edit
---

# GitHub 自动化操作

## 功能说明
此技能专门用于自动化 GitHub 平台的各种操作，包括：
- 仓库管理和文件操作
- Pull Request 创建和审查
- Issue 管理和追踪
- 分支管理和合并
- CI/CD 工作流自动化
- 代码搜索和分析

## 使用场景
- "创建一个新的 GitHub 仓库"
- "提交代码并创建 Pull Request"
- "批量处理 GitHub Issues"
- "自动化代码审查流程"
- "搜索代码库中的特定代码"
- "管理 GitHub Actions 工作流"

## 核心功能模块

### 1. 仓库管理
- **创建仓库**：创建新的公开或私有仓库
- **Fork 仓库**：Fork 其他仓库到自己账户
- **搜索仓库**：按关键词搜索仓库
- **文件操作**：读取、创建、更新文件
- **批量提交**：一次提交多个文件

### 2. Pull Request 管理
- **创建 PR**：从分支创建 Pull Request
- **审查 PR**：添加评论和审查意见
- **合并 PR**：合并 Pull Request
- **查看变更**：获取 PR 的文件变更
- **状态检查**：查看 CI/CD 状态

### 3. Issue 管理
- **创建 Issue**：创建新的问题或任务
- **更新 Issue**：修改状态、标签、负责人
- **搜索 Issue**：按条件筛选 Issue
- **添加评论**：在 Issue 中添加讨论
- **批量操作**：批量处理多个 Issue

### 4. 分支管理
- **创建分支**：从指定分支创建新分支
- **查看提交**：列出分支的提交历史
- **分支保护**：配置分支保护规则
- **合并策略**：选择合并方式（merge、squash、rebase）

### 5. 代码搜索
- **搜索代码**：在仓库中搜索代码片段
- **搜索 Issue**：搜索问题和 PR
- **搜索用户**：查找 GitHub 用户
- **高级查询**：使用 GitHub 搜索语法

## 工作流程

### 标准开发流程
1. **创建分支**：从 main 创建功能分支
2. **开发代码**：编写和测试代码
3. **提交变更**：提交文件到分支
4. **创建 PR**：创建 Pull Request
5. **代码审查**：团队审查代码
6. **合并代码**：合并到主分支

### 自动化发布流程
1. **监听事件**：监听 push 或 tag 事件
2. **运行测试**：执行自动化测试
3. **构建项目**：编译和打包
4. **创建 Release**：发布新版本
5. **部署应用**：自动部署到生产环境

### Issue 管理流程
1. **创建 Issue**：报告问题或需求
2. **分配任务**：指定负责人
3. **添加标签**：分类和优先级
4. **跟踪进度**：更新状态
5. **关闭 Issue**：完成后关闭

## 最佳实践

### 提交规范
- 使用清晰的提交信息
- 遵循 Conventional Commits 规范
- 一次提交解决一个问题
- 包含必要的测试和文档

### PR 规范
- 提供详细的 PR 描述
- 关联相关的 Issue
- 确保 CI 检查通过
- 及时响应审查意见
- 保持 PR 大小适中

### 分支策略
- 使用 Git Flow 或 GitHub Flow
- 保护主分支
- 定期同步上游分支
- 及时删除已合并的分支

### 安全实践
- 不提交敏感信息
- 使用 GitHub Secrets 管理密钥
- 启用双因素认证
- 定期审查权限设置

## 常用代码示例

### 1. 创建仓库并提交文件
```javascript
// 创建仓库
const repo = await createRepository({
  name: "my-project",
  description: "项目描述",
  private: false,
  autoInit: true
});

// 批量提交文件
await pushFiles({
  owner: "username",
  repo: "my-project",
  branch: "main",
  files: [
    {
      path: "README.md",
      content: "# My Project\n\n项目说明"
    },
    {
      path: "src/index.js",
      content: "console.log('Hello World');"
    }
  ],
  message: "Initial commit"
});
```

### 2. 创建分支和 Pull Request
```javascript
// 创建新分支
await createBranch({
  owner: "username",
  repo: "my-project",
  branch: "feature/new-feature",
  from_branch: "main"
});

// 提交代码到新分支
await createOrUpdateFile({
  owner: "username",
  repo: "my-project",
  path: "src/feature.js",
  content: "// 新功能代码",
  message: "Add new feature",
  branch: "feature/new-feature"
});

// 创建 Pull Request
await createPullRequest({
  owner: "username",
  repo: "my-project",
  title: "添加新功能",
  head: "feature/new-feature",
  base: "main",
  body: "## 变更说明\n- 添加了新功能\n- 更新了文档"
});
```

### 3. Issue 管理
```javascript
// 创建 Issue
const issue = await createIssue({
  owner: "username",
  repo: "my-project",
  title: "修复登录问题",
  body: "## 问题描述\n用户无法登录\n\n## 复现步骤\n1. 打开登录页面\n2. 输入凭证\n3. 点击登录",
  labels: ["bug", "high-priority"],
  assignees: ["developer1"]
});

// 添加评论
await addIssueComment({
  owner: "username",
  repo: "my-project",
  issue_number: issue.number,
  body: "正在调查此问题"
});

// 更新 Issue
await updateIssue({
  owner: "username",
  repo: "my-project",
  issue_number: issue.number,
  state: "closed",
  labels: ["bug", "fixed"]
});
```

### 4. 代码审查
```javascript
// 获取 PR 详情
const pr = await getPullRequest({
  owner: "username",
  repo: "my-project",
  pull_number: 123
});

// 获取 PR 文件变更
const files = await getPullRequestFiles({
  owner: "username",
  repo: "my-project",
  pull_number: 123
});

// 创建审查
await createPullRequestReview({
  owner: "username",
  repo: "my-project",
  pull_number: 123,
  body: "代码看起来不错，有几点建议",
  event: "COMMENT",
  comments: [
    {
      path: "src/index.js",
      line: 10,
      body: "建议添加错误处理"
    }
  ]
});

// 合并 PR
await mergePullRequest({
  owner: "username",
  repo: "my-project",
  pull_number: 123,
  merge_method: "squash",
  commit_title: "feat: 添加新功能"
});
```

### 5. 搜索和查询
```javascript
// 搜索代码
const codeResults = await searchCode({
  q: "function login repo:username/my-project"
});

// 搜索 Issue
const issueResults = await searchIssues({
  q: "is:open label:bug repo:username/my-project",
  sort: "created",
  order: "desc"
});

// 搜索仓库
const repoResults = await searchRepositories({
  query: "react stars:>1000 language:javascript"
});
```

## GitHub Actions 集成

### 自动化测试
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: npm test
```

### 自动化部署
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        run: ./deploy.sh
```

## 集成场景

### 1. 自动化代码审查
- 监听 PR 创建事件
- 运行代码质量检查
- 自动添加审查评论
- 标记需要改进的地方

### 2. Issue 自动分类
- 监听 Issue 创建
- 分析 Issue 内容
- 自动添加标签
- 分配给合适的人员

### 3. 发布管理
- 监听版本标签
- 生成变更日志
- 创建 GitHub Release
- 通知团队成员

### 4. 依赖更新
- 定期检查依赖更新
- 创建更新 PR
- 运行测试验证
- 自动合并安全更新

## 注意事项
- 遵守 GitHub API 速率限制
- 使用 Personal Access Token 认证
- 正确处理 API 错误和重试
- 保护敏感信息和密钥
- 遵循开源项目贡献指南
