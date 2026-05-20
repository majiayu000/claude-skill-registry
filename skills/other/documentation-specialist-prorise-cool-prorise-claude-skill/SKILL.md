---
description: 创建和维护技术文档、API 文档、代码注释和项目文档。当需要生成、更新或改进文档时使用。
name: documentation-specialist
---
# Documentation Specialist

创建和维护技术文档、API 文档、代码注释和项目文档。当需要生成、更新或改进文档时使用。

## Skill Index

<!-- AUTO-GENERATED-SKILL-INDEX:START -->
以下索引由 `node scripts/update-skill-index.js` 自动生成，用于让 Claude 在顶层专家触发后继续路由到最相关的子技能。

### Claude 使用说明

1. 先将用户当前任务与每个子技能的 `触发语义` 进行语义匹配，不要只看目录名。
2. 一旦找到最相关的子技能，立即打开其 `入口文件` 指向的 `SKILL.md`，把它作为下一层入口。
3. 进入子技能后，再根据该子技能自己的说明按需加载同目录下的 `references/`、`scripts/`、`assets/`，不要在顶层专家中预先展开大段细节。
4. 如果多个子技能都相关，先加载最贴近主目标的那个，再按需补充其他子技能，避免一次性加载过多上下文。
5. 下方 `入口文件` 路径相对于项目根目录，可直接用于 `Read` 操作。

### 子技能索引

#### changelog-automation (1)
- `changelog-generator`
  - 触发语义: 通过分析提交历史、分类更改并将技术提交转换为清晰的、面向客户的发布说明，自动从 git 提交创建面向用户的更新日志。将数小时的手动更新日志编写工作缩短为几分钟的自动生成。
  - 入口文件: `.claude/skills/documentation-specialist/references/domains/changelog-automation/SKILL.md`

#### compliance-copyright (1)
- `copyright-docs`
  - 触发语义: Generate software copyright design specification documents compliant with China Copyright Protection Center (CPCC) standards. Creates complete design documents with Mermaid diagrams based on source code analysis. Use for software copyright registration, generating design specification, creating CPCC-compliant documents, or documenting software for intellectual property protection. Triggers on "软件著作权", "设计说明书", "版权登记", "CPCC", "软著申请".
  - 入口文件: `.claude/skills/documentation-specialist/references/domains/compliance-copyright/SKILL.md`

#### document-formats (4)
- `docx`
  - 触发语义: 全面的文档创建、编辑和分析，支持跟踪更改、评论、格式保留和文本提取。当 Claude 需要处理专业文档（.docx 文件）时：(1) 创建新文档，(2) 修改或编辑内容，(3) 处理跟踪更改，(4) 添加评论，或任何其他文档任务
  - 入口文件: `.claude/skills/documentation-specialist/references/domains/document-formats/docx/SKILL.md`
- `pdf`
  - 触发语义: 全面的 PDF 操作工具包，用于提取文本和表格、创建新 PDF、合并/拆分文档和处理表单。当 Claude 需要填写 PDF 表单或以编程方式大规模处理、生成或分析 PDF 文档时使用。
  - 入口文件: `.claude/skills/documentation-specialist/references/domains/document-formats/pdf/SKILL.md`
- `pptx`
  - 触发语义: 演示文稿创建、编辑和分析。当 Claude 需要处理演示文稿（.pptx 文件）时：(1) 创建新演示文稿，(2) 修改或编辑内容，(3) 处理布局，(4) 添加评论或演讲者备注，或任何其他演示文稿任务
  - 入口文件: `.claude/skills/documentation-specialist/references/domains/document-formats/pptx/SKILL.md`
- `xlsx`
  - 触发语义: 全面的电子表格创建、编辑和分析，支持公式、格式、数据分析和可视化。当 Claude 需要处理电子表格（.xlsx、.xlsm、.csv、.tsv 等）时：(1) 创建带有公式和格式的新电子表格，(2) 读取或分析数据，(3) 在保留公式的同时修改现有电子表格，(4) 在电子表格中进行数据分析和可视化，或 (5) 重新计算公式
  - 入口文件: `.claude/skills/documentation-specialist/references/domains/document-formats/xlsx/SKILL.md`

#### document-generator (1)
- `document-generator`
  - 触发语义: Expert document creation specialist who generates professional PDF, PPTX, DOCX, and XLSX files using code-based approaches with proper formatting, charts, and data visualization.
  - 入口文件: `.claude/skills/documentation-specialist/references/domains/document-generator/SKILL.md`

#### internal-communications (1)
- `internal-comms`
  - 触发语义: 一套资源，帮助我使用公司喜欢的格式编写各种内部通信。每当要求编写某种内部通信（状态报告、领导更新、3P 更新、公司通讯、常见问题、事件报告、项目更新等）时，Claude 应使用此技能。
  - 入口文件: `.claude/skills/documentation-specialist/references/domains/internal-communications/SKILL.md`

#### manual-generation (1)
- `software-manual`
  - 触发语义: Generate interactive TiddlyWiki-style HTML software manuals with screenshots, API docs, and multi-level code examples. Use when creating user guides, software documentation, or API references. Triggers on "software manual", "user guide", "generate manual", "create docs".
  - 入口文件: `.claude/skills/documentation-specialist/references/domains/manual-generation/SKILL.md`

#### technical-writer (1)
- `technical-writer`
  - 触发语义: Expert technical writer specializing in developer documentation, API references, README files, and tutorials. Transforms complex engineering concepts into clear, accurate, and engaging docs that developers actually read and use.
  - 入口文件: `.claude/skills/documentation-specialist/references/domains/technical-writer/SKILL.md`

#### text-formatting (1)
- `text-formatter`
  - 触发语义: Transform and optimize text content with intelligent formatting. Output BBCode + Markdown hybrid format optimized for forums. Triggers on "format text", "text formatter", "排版", "格式化文本", "BBCode".
  - 入口文件: `.claude/skills/documentation-specialist/references/domains/text-formatting/SKILL.md`

#### zk-steward (1)
- `zk-steward`
  - 触发语义: Knowledge-base steward in the spirit of Niklas Luhmann's Zettelkasten. Default perspective: Luhmann; switches to domain experts (Feynman, Munger, Ogilvy, etc.) by task. Enforces atomic notes, connectivity, and validation loops. Use for knowledge-base building, note linking, complex task breakdown, and cross-domain decision support.
  - 入口文件: `.claude/skills/documentation-specialist/references/domains/zk-steward/SKILL.md`

<!-- AUTO-GENERATED-SKILL-INDEX:END -->

## Notes

- 顶层 `SKILL.md` 仅做索引导航，不承载大体量细节内容。
- 详细资料下沉到 `references/domains/`，按树形结构组织。
