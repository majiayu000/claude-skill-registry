---
name: How to Create Claude Code Skill
description: A guide to creating Claude Code Skills.
---


Skills的文件结构有以下几种组织方式：

基本Skill结构
每个Skill都需要一个SKILL.md文件，包含YAML前置元数据1：

---
name: Your Skill Name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
[Clear, step-by-step guidance for Claude to follow]

## Examples
[Concrete examples of using this Skill]
完整的Skill目录结构
随着Skill复杂性的增长，可以包含额外的支持文件2：

my-skill/
├── SKILL.md (required)
├── reference.md (optional documentation)
├── examples.md (optional examples)
├── scripts/
│   └── helper.py (optional utility)
└── templates/
    └── template.txt (optional template)
渐进式披露模式示例
文档展示了一个PDF处理Skill的完整结构3：

pdf/
├── SKILL.md              # Main instructions (loaded when triggered)
├── FORMS.md              # Form-filling guide (loaded as needed)
├── reference.md          # API reference (loaded as needed)
├── examples.md           # Usage examples (loaded as needed)
└── scripts/
    ├── analyze_form.py   # Utility script (executed, not loaded)
    ├── fill_form.py      # Form filling script
    └── validate.py       # Validation script
Skill存储位置
在Claude Code中，Skills可以存储在不同位置2：

个人Skills：

mkdir -p ~/.claude/skills/my-skill-name
项目Skills：

mkdir -p .claude/skills/my-skill-name
文件引用方式
在SKILL.md中可以引用其他文件2：

For advanced usage, see [reference.md](reference.md).

Run the helper script:
```bash
python scripts/helper.py input.txt

## 技术要求

- 保持SKILL.md主体内容在500行以下以获得最佳性能[(4)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#technical-notes)
- YAML前置元数据字段限制：`name`最多64字符，`description`最多1024字符[(4)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#technical-notes)
- 避免深层嵌套引用，保持引用深度在一级以内[(3)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure)

Claude只在需要时读取这些文件，使用渐进式披露来高效管理上下文[(1)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview#skill-structure)。

## 其他要求

推荐的命名示例（动名词形式）：

"Processing PDFs"
"Analyzing spreadsheets"
"Managing databases"
"Testing code"
"Writing documentation"
避免的命名方式：

模糊名称："Helper"、"Utils"、"Tools"
过于通用："Documents"、"Data"、"Files"
Skills的组织结构
对于包含多个相关Skills的项目，可以按功能域组织：

.claude/skills/
├── pdf-processing/
│   └── SKILL.md
├── excel-analysis/
│   └── SKILL.md
├── git-workflow/
│   └── SKILL.md
└── code-review/
    └── SKILL.md
这样的组织方式使得Skills更容易引用、讨论和维护6。