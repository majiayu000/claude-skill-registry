---
name: gh-bootstrap
description: 一站式 GitHub 仓库配置初始化工具。
allowed-tools: Task, AskUserQuestion, Read, Bash, Glob, Grep, Write
---

# gh-bootstrap

一站式 GitHub 仓库配置初始化工具，将项目配置时间从数小时缩短到几分钟。

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  gh-bootstrap Skill Architecture                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SKILL.md (入口)                                                 │
│       ↓                                                          │
│  Phase 1: Detection   →  扫描项目，识别语言/框架/现有配置         │
│       ↓                                                          │
│  Phase 2: Collection  →  交互式收集配置 (AskUserQuestion)         │
│       ↓                                                          │
│  Phase 3: Conflict    →  检测冲突，制定处理策略                   │
│       ↓                                                          │
│  Phase 4: Execution   →  下载模板 + 直接复制（仅替换变量）      │
│       ↓                                                          │
│  Phase 5: Report      →  生成执行报告和后续建议                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Key Design Principles

1. **阶段化执行**: 复杂任务分解为 5 个有序阶段
2. **关注点分离**: `phases/`(逻辑) + `specs/`(配置) + `templates/`(视图)
3. **交互式配置**: 全程通过 AskUserQuestion 与用户对话
4. **运行时下载**: 不预存模板，按需从推荐仓库下载
5. **直接复制模板**: 从下载的模板原样复制，仅替换变量占位符（禁止重写）

## CRITICAL CONSTRAINTS

**⚠️ 禁止自行编写配置文件！必须遵循以下规则：**

### 必须在开头询问用户使用语言环境
在开头调用问答式表单，询问用户的沟通语言（决定了与你沟通），询问用户编写后续模板使用的语言（Issue模板之类）
若用户确认了使用中文 or Chinese 你必须在后续的所有模板的编写都尽量以中文友好

### 强制执行顺序
```
Read specs/template-catalog.md → git clone 模板仓库 → Read 模板文件 → 直接复制 + 变量替换 → Write 输出
```

### 必须遵守的规则

1. **必须先读取 template-catalog.md**: 在下载任何模板之前，必须先读取 `specs/template-catalog.md` 获取精确的文件路径映射
2. **必须下载模板**: 在生成任何配置文件之前，必须先从 `template-catalog.md` 中下载对应的推荐仓库
3. **必须直接复制**: 读取模板后，**原样复制**内容到目标文件，仅替换变量占位符
4. **禁止凭空生成**: 不允许跳过下载步骤直接写文件，即使 Claude 知道如何编写

### 严格禁止的行为

- ❌ 跳过下载直接写文件
- ❌ "参考模板后重新编写"
- ❌ "根据最佳实践优化模板"
- ❌ "简化/重构模板步骤"
- ❌ 凭记忆/知识生成配置内容
- ❌ 删除模板中"看起来不需要"的步骤

### 必须执行的操作

- ✅ 复制模板的结构和逻辑
- ✅ **必须替换**所有变量占位符（`{{projectName}}`、`{{description}}`、`{{author}}` 等）
- ✅ **必须替换** GitHub 信息（`{{owner}}`、`{{repo}}`、badges URL 等）
- ✅ **必须调整**版本号（`node-version`、`python-version` 等）为检测到的版本
- ✅ **必须填充**组件特定配置（token 名称、平台账号等）
- ✅ 保留所有 `${{ secrets.* }}`、`${{ github.* }}` 表达式（这些是 GitHub Actions 语法）
- ✅ 保留所有 Action 版本号 `@v4`

### 变量替换是强制的

**模板中的变量占位符必须全部替换，不能留空！** 这些变量在 Phase 2 收集阶段必须全部确定。

**违反以上规则将导致工作流失效！详见 [04-execution.md](phases/04-execution.md)**

## Execution Flow

```
用户触发 gh-bootstrap
     │
     ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Phase 1    │ ──▶ │  Phase 2    │ ──▶ │  Phase 3    │
│  Detection  │     │  Collection │     │  Conflict   │
│  项目检测    │     │  配置收集    │     │  冲突检测    │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
     ┌────────────────────────────────────────┘
     ▼
┌─────────────┐     ┌─────────────┐
│  Phase 4    │ ──▶ │  Phase 5    │
│  Execution  │     │  Report     │
│  执行生成    │     │  报告总结    │
└─────────────┘     └─────────────┘
```

## Output Structure

```
{project-root}/
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── dependabot.yml
│   ├── labels.yml
│   └── CODEOWNERS
├── README.md
├── LICENSE
├── .gitignore
└── CONTRIBUTING.md
```

## Reference Documents

| Document | Purpose |
|----------|---------|
| [phases/01-detection.md](phases/01-detection.md) | 智能项目检测 |
| [phases/02-collection.md](phases/02-collection.md) | 交互式配置收集 |
| [phases/03-conflict.md](phases/03-conflict.md) | 冲突检测与处理 |
| [phases/04-execution.md](phases/04-execution.md) | 模板下载与直接复制 |
| [phases/05-report.md](phases/05-report.md) | 执行报告 |
| [specs/detection-rules.md](specs/detection-rules.md) | 检测规则定义 |
| [specs/presets.md](specs/presets.md) | 预设配置定义 |
| [specs/template-catalog.md](specs/template-catalog.md) | 推荐模板仓库目录 |