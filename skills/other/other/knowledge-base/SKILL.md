---
name: knowledge-base
description: 专业的知识库管理系统，旨在解决“知识诅咒”和认知偏差问题。通过显式化隐性知识、扫描代码提取领域概念、整合行业最佳实践，构建结构化的 Markdown 知识库。
---

# Knowledge Base Skill

一个旨在消除认知偏差、显式化隐性知识的知识库管理工具。它结合代码扫描（ace-tool）、网络搜索和结构化文档管理，构建项目的"第二大脑"。

## 核心理念：打破“知识诅咒”

"知识诅咒"（Curse of Knowledge）是指当我们掌握某种知识后，很难想象不懂这种知识的人的状态。在软件工程中，这表现为：
- 资深开发者假设新人“应该知道”某些上下文。
- 代码中充斥着特定领域的缩写和隐喻。
- 架构决策的背景被遗忘，只留下结果。

本技能通过以下方式解决此问题：
1.  **显式化（Explicitness）**：强制将默会知识（Tacit Knowledge）转化为显性知识（Explicit Knowledge）。
2.  **上下文对齐（Context Alignment）**：通过代码扫描提取领域术语，建立统一词汇表。
3.  **认知共识（Cognitive Consensus）**：记录“为什么这样做”而不仅仅是“怎么做”。

## 执行环境

| 路径类型 | 路径 | 说明 |
|---------|------|------|
| **技能目录** | `~/.pi/agent/skills/knowledge-base/` | 脚本和模板位置 |
| **主脚本** | `~/.pi/agent/skills/knowledge-base/lib.ts` | 核心逻辑脚本 |
| **知识库目录** | `./docs/knowledge/` | **项目根目录**下的文档存储位置 |

## 目录结构

```
docs/knowledge/
├── concepts/             # 领域概念与术语 (名词解释)
│   ├── [Term].md         # 一级文档：e.g. "DoubleEntryBookkeeping.md"
│   └── auth/             # 二级分类
│       ├── User.md
│       └── Session.md
│   └── frontend/         # 二级分类
│       ├── responsive/   # 三级分类
│       │   └── design/   # 四级分类
│       │       └── MobileFirst.md
│       └── pwa/          # 三级分类
│           └── advanced/ # 四级分类
│               └── optimization/  # 五级分类
│                   └── ProgressiveWebApp.md
├── guides/               # 操作指南与最佳实践 (How-to)
│   ├── [Topic].md        # 一级文档：e.g. "ErrorHandlingStrategy.md"
│   └── backend/          # 二级分类
│       ├── API.md
│       └── Database.md
│   └── frontend/         # 二级分类
│       └── css/          # 三级分类
│           └── flexbox/  # 四级分类
│               └── ResponsiveLayout.md
├── decisions/            # 认知决策记录 (Why)
│   ├── [Date]-[Topic].md # 一级文档：e.g. "20240101-WhyChooseRestOverGraphQL.md"
│   └── database/         # 二级分类
│       └── 20240101-WhyUsePostgres.md
│   └── frontend/         # 二级分类
│       └── layout/       # 三级分类
│           └── modern/   # 四级分类
│               └── strategies/  # 五级分类
│                   └── 20260107-WhyUseCSSGrid.md
├── external/             # 行业共识与外部参考
│   ├── [Source].md       # e.g. "ReactPatternConsensus.md"
│   └── standards/        # 二级分类
│       └── RESTfulAPI.md
├── GLOSSARY.md           # 专业术语表（自动生成，包含定义摘要）
└── index.md              # 自动生成的知识索引（支持多层级显示）
```

## 命令参考

所有命令建议在**项目根目录**下执行。

```bash
# 1. 初始化
bun ~/.pi/agent/skills/knowledge-base/lib.ts init

# 2. 扫描代码提取概念 (集成 ace-tool)
bun ~/.pi/agent/skills/knowledge-base/lib.ts scan

# 3. 发现项目结构并生成文档清单
bun ~/.pi/agent/skills/knowledge-base/lib.ts discover

# 4. 创建知识条目（支持目录分类）
bun ~/.pi/agent/skills/knowledge-base/lib.ts create term "术语名称" [分类路径]     # alias for concept
bun ~/.pi/agent/skills/knowledge-base/lib.ts create concept "术语名称" [分类路径]
bun ~/.pi/agent/skills/knowledge-base/lib.ts create guide "指南标题" [分类路径]
bun ~/.pi/agent/skills/knowledge-base/lib.ts create decision "决策标题" [分类路径]

# 示例：创建带分类的文档（支持无限层级）
bun ~/.pi/agent/skills/knowledge-base/lib.ts create concept "UserAuthentication" auth/user
bun ~/.pi/agent/skills/knowledge-base/lib.ts create guide "ErrorHandling" backend/api
bun ~/.pi/agent/skills/knowledge-base/lib.ts create decision "WhyUsePostgres" database

# 三级和四级分类示例
bun ~/.pi/agent/skills/knowledge-base/lib.ts create concept "MobileFirst" frontend/responsive/design
bun ~/.pi/agent/skills/knowledge-base/lib.ts create concept "ProgressiveWebApp" frontend/pwa/advanced/optimization
bun ~/.pi/agent/skills/knowledge-base/lib.ts create guide "ResponsiveLayout" frontend/css/flexbox
bun ~/.pi/agent/skills/knowledge-base/lib.ts create decision "WhyUseCSSGrid" frontend/layout/modern/strategies

# 4. 搜索知识库
bun ~/.pi/agent/skills/knowledge-base/lib.ts search "关键词"

# 5. 生成专业术语表 (GLOSSARY.md)
bun ~/.pi/agent/skills/knowledge-base/lib.ts glossary

# 6. 生成/更新索引
bun ~/.pi/agent/skills/knowledge-base/lib.ts index
```

## 核心功能详解

### 1. 智能扫描 (`scan`)
利用 `ace-tool` 分析代码库，识别高频词汇、特定类名和复杂逻辑，自动建议需要创建的“概念文档”。
*   输入：代码库状态
*   输出：推荐创建的概念列表 (`docs/knowledge/suggested_concepts.md`)

### 2. 结构化文档 (`create`)
提供标准化模板，强制包含：
*   **Definition**: 一句话定义（防歧义）。
*   **Context**: 出现的场景。
*   **Anti-patterns**: 常见的误解（解决认知偏差）。
*   **References**: 代码引用或外部链接。

### 3. 行业共识集成
通过 `external` 目录管理通用知识（如 RESTful 规范、React Hooks 规则），避免重复造轮子，明确本项目是遵循标准还是有特殊定制。

### 4. 专业术语表维护 (`glossary`)
自动扫描 `concepts/` 目录下的所有文档，提取定义（Definition）部分，生成扁平化的 `GLOSSARY.md` 表格。
*   **用途**：提供快速查阅的术语字典，适合非技术人员或快速上下文对齐。
*   **格式**：包含 Term (Link), Category, Definition 的 Markdown 表格。

## 最佳实践

1.  **遇到不懂的缩写时**：立即运行 `create concept [缩写]`，查明后填入。
2.  **代码 Review 时**：如果需要解释一段逻辑超过 3 句，创建一个 `guide` 并链接。
3.  **新成员加入时**：让他阅读 `docs/knowledge/index.md`，并要求他记录所有困惑点作为新的 Issue。
