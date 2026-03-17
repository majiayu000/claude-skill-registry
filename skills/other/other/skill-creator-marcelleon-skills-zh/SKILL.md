---
name: skill-creator
description: 创建高效 Skills 的指南。当用户需要创建新的 skill（或更新现有 skill）以通过专业知识、工作流程或工具集成扩展 Claude 的能力时使用此技能。
license: Complete terms in LICENSE.txt
---

# Skill Creator

本 skill 提供创建高效 skills 的指导。

## 关于 Skills

Skills 是模块化的、自包含的软件包，通过提供专业知识、工作流程和工具来扩展 Claude 的能力。可以将它们视为特定领域或任务的"入职指南"——它们将 Claude 从通用助手转变为配备了模型无法完全掌握的程序性知识的专业助手。

### Skills 提供的能力

1. 专业工作流程 - 特定领域的多步骤流程
2. 工具集成 - 使用特定文件格式或 API 的指令
3. 领域专业知识 - 公司特定知识、架构、业务逻辑
4. 捆绑资源 - 用于复杂和重复任务的脚本、参考文档和资源文件

## 核心原则

### 简洁至上

上下文窗口是公共资源。Skills 与 Claude 需要的其他一切共享上下文窗口：系统提示词、对话历史、其他 Skills 的元数据，以及实际的用户请求。

**默认假设：Claude 已经非常智能。** 只添加 Claude 尚未掌握的上下文信息。对每条信息提出质疑："Claude 真的需要这个解释吗？" 以及 "这段文字值得它的 token 成本吗？"

优先使用简洁的示例，而非冗长的解释。

### 设置适当的自由度

根据任务的脆弱性和可变性匹配具体程度：

**高自由度（基于文本的指令）**：当多种方法都有效、决策取决于上下文，或启发式方法指导方案时使用。

**中等自由度（伪代码或带参数的脚本）**：当存在首选模式、可以接受一些变化，或配置影响行为时使用。

**低自由度（特定脚本，少量参数）**：当操作脆弱且容易出错、一致性至关重要，或必须遵循特定顺序时使用。

将 Claude 想象为探索路径：有悬崖的狭窄桥梁需要具体的护栏（低自由度），而开阔的田野允许多条路线（高自由度）。

### Skill 的结构

每个 skill 由一个必需的 SKILL.md 文件和可选的捆绑资源组成：

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter 元数据（必需）
│   │   ├── name: （必需）
│   │   └── description: （必需）
│   └── Markdown 指令（必需）
└── 捆绑资源（可选）
    ├── scripts/          - 可执行代码（Python/Bash 等）
    ├── references/       - 按需加载到上下文的参考文档
    └── assets/           - 输出中使用的文件（模板、图标、字体等）
```

#### SKILL.md（必需）

每个 SKILL.md 包含：

- **Frontmatter**（YAML）：包含 `name` 和 `description` 字段。这些是 Claude 用来判断何时使用该 skill 的唯一字段，因此清晰而全面地描述 skill 是什么以及何时应该使用它非常重要。
- **主体**（Markdown）：使用 skill 的指令和指导。仅在 skill 触发后加载（如果加载的话）。

#### 捆绑资源（可选）

##### Scripts（`scripts/`）

用于需要确定性可靠性或被重复重写的任务的可执行代码（Python/Bash 等）。

- **何时包含**：当相同的代码被重复重写或需要确定性可靠性时
- **示例**：用于 PDF 旋转任务的 `scripts/rotate_pdf.py`
- **优势**：节省 token、确定性、可以在不加载到上下文的情况下执行
- **注意**：脚本可能仍需要被 Claude 读取以进行修补或环境特定的调整

##### References（`references/`）

旨在按需加载到上下文中以指导 Claude 的流程和思考的参考文档和参考资料。

- **何时包含**：用于 Claude 在工作时应该参考的文档
- **示例**：用于财务架构的 `references/finance.md`、公司保密协议模板的 `references/mnda.md`、公司政策的 `references/policies.md`、API 规范的 `references/api_docs.md`
- **用例**：数据库架构、API 文档、领域知识、公司政策、详细的工作流程指南
- **优势**：保持 SKILL.md 精简，仅在 Claude 确定需要时加载
- **最佳实践**：如果文件很大（>10k 字），在 SKILL.md 中包含 grep 搜索模式
- **避免重复**：信息应存在于 SKILL.md 或 references 文件中，而不是两者都有。除非是 skill 的真正核心内容，否则优先使用 references 文件存储详细信息——这样既保持 SKILL.md 精简，又使信息可被发现而不占用上下文窗口。在 SKILL.md 中仅保留基本的程序性指令和工作流程指导；将详细的参考资料、架构和示例移至 references 文件。

##### Assets（`assets/`）

不打算加载到上下文中，而是在 Claude 生成的输出中使用的文件。

- **何时包含**：当 skill 需要将在最终输出中使用的文件时
- **示例**：用于品牌资产的 `assets/logo.png`、PowerPoint 模板的 `assets/slides.pptx`、HTML/React 样板文件的 `assets/frontend-template/`、字体文件的 `assets/font.ttf`
- **用例**：模板、图像、图标、样板代码、字体、被复制或修改的示例文档
- **优势**：将输出资源与文档分离，使 C 能够使用文件而不将其加载到上下文中

#### Skill 中不应包含的内容

Skill 应仅包含直接支持其功能的基本文件。不要创建多余的文档或辅助文件，包括：

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- 等

Skill 应仅包含 AI 助手完成手头任务所需的信息。它不应包含有关创建过程的辅助上下文、设置和测试程序、面向用户的文档等。创建额外的文档文件只会增加混乱和困惑。

### 渐进式披露设计原则

Skills 使用三级加载系统来有效管理上下文：

1. **元数据（name + description）** - 始终在上下文中（约 100 字）
2. **SKILL.md 主体** - 当 skill 触发时（<5k 字）
3. **捆绑资源** - 根据 Claude 的需要（无限制，因为脚本可以在不读取到上下文窗口的情况下执行）

#### 渐进式披露模式

保持 SKILL.md 主体精简且低于 500 行，以最小化上下文膨胀。当接近此限制时，将内容拆分到单独的文件中。当将内容拆分到其他文件时，非常重要的是从 SKILL.md 中引用它们并清楚地描述何时阅读它们，以确保 skill 的读者知道它们的存在以及何时使用它们。

**关键原则：** 当 skill 支持多个变体、框架或选项时，在 SKILL.md 中仅保留核心工作流程和选择指导。将特定于变体的详细信息（模式、示例、配置）移至单独的参考文件。

**模式 1：带引用的高级指南**

```markdown
# PDF 处理

## 快速入门

使用 pdfplumber 提取文本：
[代码示例]

## 高级功能

- **表单填充**：参见 [FORMS.md](FORMS.md) 获取完整指南
- **API 参考**：参见 [REFERENCE.md](REFERENCE.md) 了解所有方法
- **示例**：参见 [EXAMPLES.md](EXAMPLES.md) 了解常见模式
```

Claude 仅在需要时加载 FORMS.md、REFERENCE.md 或 EXAMPLES.md。

**模式 2：特定领域的组织**

对于具有多个领域的 Skills，按领域组织内容以避免加载不相关的上下文：

```
bigquery-skill/
├── SKILL.md（概述和导航）
└── reference/
    ├── finance.md（收入、计费指标）
    ├── sales.md（商机、销售漏斗）
    ├── product.md（API 使用、功能）
    └── marketing.md（营销活动、归因）
```

当用户询问销售指标时，Claude 仅读取 sales.md。

同样，对于支持多个框架或变体的 skills，按变体组织：

```
cloud-deploy/
├── SKILL.md（工作流程 + 提供商选择）
└── references/
    ├── aws.md（AWS 部署模式）
    ├── gcp.md（GCP 部署模式）
    └── azure.md（Azure 部署模式）
```

当用户选择 AWS 时，Claude 仅读取 aws.md。

**模式 3：条件细节**

显示基本内容，链接到高级内容：

```markdown
# DOCX 处理

## 创建文档

使用 docx-js 创建新文档。参见 [DOCX-JS.md](DOCX-JS.md)。

## 编辑文档

对于简单编辑，直接修改 XML。

**对于修订追踪**：参见 [REDLINING.md](REDLINING.md)
**对于 OOXML 详细信息**：参见 [OOXML.md](OOXML.md)
```

Claude 仅在用户需要这些功能时读取 REDLINING.md 或 OOXML.md。

**重要指南：**

- **避免深度嵌套的引用** - 保持引用从 SKILL.md 的一级深度。所有引用文件都应直接从 SKILL.md 链接。
- **组织较长的引用文件** - 对于超过 100 行的文件，在顶部包含目录，以便 Claude 在预览时可以看到完整的范围。

## Skill 创建流程

Skill 创建包括以下步骤：

1. 通过具体示例理解 skill
2. 规划可重用的 skill 内容（脚本、参考文档、资源文件）
3. 初始化 skill（运行 init_skill.py）
4. 编辑 skill（实现资源并编写 SKILL.md）
5. 打包 skill（运行 package_skill.py）
6. 基于实际使用迭代

按顺序遵循这些步骤，仅在有明确理由不适用时跳过。

### 步骤 1：通过具体示例理解 Skill

仅在 skill 的使用模式已经清楚理解时跳过此步骤。即使在处理现有 skill 时，此步骤仍然有价值。

要创建有效的 skill，需要清楚理解 skill 将如何使用的具体示例。这种理解可以来自直接的用户示例或经过用户反馈验证的生成示例。

例如，在构建图像编辑 skill 时，相关问题包括：

- "图像编辑 skill 应该支持什么功能？编辑、旋转，还有其他吗？"
- "您能给出一些如何使用此 skill 的示例吗？"
- "我可以想象用户要求诸如'移除此图像中的红眼'或'旋转此图像'之类的事情。您还能想象此 skill 被如何使用吗？"
- "用户会说什么来触发此 skill？"

为避免让用户不知所措，避免在单条消息中提出太多问题。从最重要的问题开始，并根据需要跟进以提高效果。

当对 skill 应支持的功能有清晰的认识时，结束此步骤。

### 步骤 2：规划可重用的 Skill 内容

要将具体示例转化为有效的 skill，请通过以下方式分析每个示例：

1. 考虑如何从头开始执行示例
2. 识别在重复执行这些工作流程时有用的脚本、参考文档和资源文件

示例：在构建 `pdf-editor` skill 以处理诸如"帮我旋转这个 PDF"之类的查询时，分析显示：

1. 旋转 PDF 每次都需要重写相同的代码
2. `scripts/rotate_pdf.py` 脚本将有助于存储在 skill 中

示例：在设计 `frontend-webapp-builder` skill 以处理诸如"为我构建一个待办事项应用"或"为我构建一个跟踪步数的仪表板"之类的查询时，分析显示：

1. 编写前端 Web 应用程序每次都需要相同的样板 HTML/React 代码
2. 包含样板 HTML/React 项目文件的 `assets/hello-world/` 模板将有助于存储在 skill 中

示例：在构建 `big-query` skill 以处理诸如"今天有多少用户登录？"之类的查询时，分析显示：

1. 查询 BigQuery 每次都需要重新发现表架构和关系
2. 记录表架构的 `references/schema.md` 文件将有助于存储在 skill 中

要确定 skill 的内容，请分析每个具体示例以创建要包含的可重用资源列表：脚本、参考文档和资源文件。

### 步骤 3：初始化 Skill

此时，是时候实际创建 skill 了。

仅在正在开发的 skill 已经存在且需要迭代或打包时跳过此步骤。在这种情况下，继续下一步。

从头开始创建新 skill 时，请始终运行 `init_skill.py` 脚本。该脚本方便地生成一个新的模板 skill 目录，该目录自动包含 skill 所需的一切，使 skill 创建过程更加高效和可靠。

用法：

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

该脚本将：

- 在指定路径创建 skill 目录
- 生成具有正确 frontmatter 和 TODO 占位符的 SKILL.md 模板
- 创建示例资源目录：`scripts/`、`references/` 和 `assets/`
- 在每个目录中添加可以自定义或删除的示例文件

初始化后，根据需要自定义或删除生成的 SKILL.md 和示例文件。

### 步骤 4：编辑 Skill

在编辑（新生成或现有的）skill 时，请记住该 skill 是为另一个 Claude 实例使用而创建的。包含对 Claude 有益且不明显的信息。考虑哪些程序性知识、特定于领域的细节或可重用资源将帮助另一个 Claude 实例更有效地执行这些任务。

#### 学习经过验证的设计模式

根据您的 skill 需求，参考这些有用的指南：

- **多步骤流程**：参见 references/workflows.md 了解顺序工作流程和条件逻辑
- **特定输出格式或质量标准**：参见 references/output-patterns.md 了解模板和示例模式

这些文件包含有效 skill 设计的既定最佳实践。

#### 从可重用的 Skill 内容开始

要开始实现，请从上述识别的可重用资源开始：`scripts/`、`references/` 和 `assets/` 文件。请注意，此步骤可能需要用户输入。例如，在实现 `brand-guidelines` skill 时，用户可能需要提供要存储在 `assets/` 中的品牌资产或模板，或要存储在 `references/` 中的文档。

添加的脚本必须通过实际运行来测试，以确保没有错误并且输出符合预期。如果有许多类似的脚本，只需要测试一个代表性样本，以确保它们都能工作，同时平衡完成时间。

应删除 skill 不需要的任何示例文件和目录。初始化脚本在 `scripts/`、`references/` 和 `assets/` 中创建示例文件以演示结构，但大多数 skills 不需要所有这些文件。

#### 更新 SKILL.md

**编写指南：** 始终使用祈使句/不定式形式。

##### Frontmatter

使用 `name` 和 `description` 编写 YAML frontmatter：

- `name`：skill 名称
- `description`：这是您的 skill 的主要触发机制，帮助 Claude 理解何时使用该 skill。
  - 包含 Skill 做什么以及使用它的具体触发器/上下文。
  - 在此处包含所有"何时使用"信息 - 不在主体中。主体仅在触发后加载，因此主体中的"何时使用此 Skill"部分对 Claude 没有帮助。
  - `docx` skill 的示例描述："全面的文档创建、编辑和分析，支持修订追踪、评论、格式保留和文本提取。当 Claude 需要处理专业文档（.docx 文件）时使用，用于：(1) 创建新文档，(2) 修改或编辑内容，(3) 使用修订追踪，(4) 添加评论，或任何其他文档任务"

不要在 YAML frontmatter 中包含任何其他字段。

##### 主体

编写使用 skill 及其捆绑资源的指令。

### 步骤 5：打包 Skill

一旦 skill 的开发完成，它必须被打包成可分发的 .skill 文件以与用户共享。打包过程首先自动验证 skill 以确保它满足所有要求：

```bash
scripts/package_skill.py <path/to/skill-folder>
```

可选的输出目录规范：

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

打包脚本将：

1. **验证** skill 自动检查：

   - YAML frontmatter 格式和必需字段
   - Skill 命名约定和目录结构
   - 描述的完整性和质量
   - 文件组织和资源引用

2. **打包** skill（如果验证通过），创建以 skill 命名的 .skill 文件（例如，`my-skill.skill`），其中包含所有文件并维护适当的目录结构以供分发。.skill 文件是带有 .skill 扩展名的 zip 文件。

如果验证失败，脚本将报告错误并退出而不创建包。修复任何验证错误并再次运行打包命令。

### 步骤 6：迭代

测试 skill 后，用户可能会要求改进。这通常在使用 skill 后立即发生，并带有关于 skill 如何执行的新鲜上下文。

**迭代工作流程：**

1. 在实际任务上使用 skill
2. 注意困难或低效率
3. 确定应如何更新 SKILL.md 或捆绑资源
4. 实施更改并再次测试
