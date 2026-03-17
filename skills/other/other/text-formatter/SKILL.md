---
name: text-formatter
description: Transform and optimize text content with intelligent formatting. Output BBCode + Markdown hybrid format optimized for forums. Triggers on "format text", "text formatter", "排版", "格式化文本", "BBCode".
allowed-tools: Task, AskUserQuestion, Read, Write, Bash, Glob
---

# Text Formatter

Transform and optimize text content with intelligent structure analysis. Output format: **BBCode + Markdown hybrid** optimized for forum publishing.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Text Formatter Architecture (BBCode + MD Mode)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1: Input Collection  → 接收文本/文件                       │
│           ↓                                                      │
│  Phase 2: Content Analysis  → 分析结构、识别 Callout/Admonition  │
│           ↓                                                      │
│  Phase 3: Format Transform  → 转换为 BBCode+MD 格式              │
│           ↓                                                      │
│  Phase 4: Output & Preview  → 保存文件 + 预览                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Key Design Principles

1. **Single Format Output**: BBCode + Markdown hybrid (forum optimized)
2. **Pixel-Based Sizing**: size=150/120/100/80 (not 1-7 levels)
3. **Forum Compatibility**: Only use widely-supported BBCode tags
4. **Markdown Separators**: Use `---` for horizontal rules (not `[hr]`)
5. **No Alignment Tags**: `[align]` not supported, avoid usage

---

## Format Specification

### Supported BBCode Tags

| Tag | Usage | Example |
|-----|-------|---------|
| `[size=N]` | Font size (pixels) | `[size=120]Title[/size]` |
| `[color=X]` | Text color (hex/name) | `[color=#2196F3]Blue[/color]` 或 `[color=blue]` |
| `[b]` | Bold | `[b]Bold text[/b]` |
| `[i]` | Italic | `[i]Italic[/i]` |
| `[s]` | Strikethrough | `[s]deleted[/s]` |
| `[u]` | Underline | `[u]underlined[/u]` |
| `[quote]` | Quote block | `[quote]Content[/quote]` |
| `[code]` | Code block | `[code]code[/code]` |
| `[img]` | Image | `[img]url[/img]` |
| `[url]` | Link | `[url=link]text[/url]` |
| `[list]` | List container | `[list][*]item[/list]` |
| `[spoiler]` | Collapsible content | `[spoiler=标题]隐藏内容[/spoiler]` |

### HTML to BBCode Conversion

| HTML Input | BBCode Output |
|------------|---------------|
| `<mark>高亮</mark>` | `[color=yellow]高亮[/color]` |
| `<u>下划线</u>` | `[u]下划线[/u]` |
| `<details><summary>标题</summary>内容</details>` | `[spoiler=标题]内容[/spoiler]` |

### Unsupported Tags (Avoid!)

| Tag | Reason | Alternative |
|-----|--------|-------------|
| `[align]` | Not rendered | Remove or use default left |
| `[hr]` | Shows as text | Use Markdown `---` |
| `<div>` | HTML not supported | Use BBCode only |
| `[table]` | Limited support | Use list or code block |

### Size Hierarchy (Pixels)

| Element | Size | Color | Usage |
|---------|------|-------|-------|
| **Main Title** | 150 | #2196F3 | Document title |
| **Section Title** | 120 | #2196F3 | Major sections (## H2) |
| **Subsection** | 100 | #333 | Sub-sections (### H3) |
| **Normal Text** | (default) | - | Body content |
| **Notes/Gray** | 80 | gray | Footnotes, metadata |

### Color Palette

| Color | Hex | Semantic Usage |
|-------|-----|----------------|
| **Blue** | #2196F3 | Titles, links, info |
| **Green** | #4CAF50 | Success, tips, features |
| **Orange** | #FF9800 | Warnings, caution |
| **Red** | #F44336 | Errors, danger, important |
| **Purple** | #9C27B0 | Examples, code |
| **Gray** | gray | Notes, metadata |

---

## Mandatory Prerequisites

> Read before execution:

| Document | Purpose | Priority |
|----------|---------|----------|
| [specs/format-rules.md](specs/format-rules.md) | Format conversion rules | **P0** |
| [specs/element-mapping.md](specs/element-mapping.md) | Element type mappings | P1 |
| [specs/callout-types.md](specs/callout-types.md) | Callout/Admonition types | P1 |

---

## Execution Flow

```
┌────────────────────────────────────────────────────────────────┐
│  Phase 1: Input Collection                                      │
│  - Ask: paste text OR file path                                │
│  - Output: input-config.json                                   │
├────────────────────────────────────────────────────────────────┤
│  Phase 2: Content Analysis                                      │
│  - Detect structure: headings, lists, code blocks, tables      │
│  - Identify Callouts/Admonitions (>[!type])                    │
│  - Output: analysis.json                                       │
├────────────────────────────────────────────────────────────────┤
│  Phase 3: Format Transform                                      │
│  - Apply BBCode + MD rules from specs/format-rules.md          │
│  - Convert elements with pixel-based sizes                     │
│  - Use Markdown --- for separators                             │
│  - Output: formatted content                                   │
├────────────────────────────────────────────────────────────────┤
│  Phase 4: Output & Preview                                      │
│  - Save to .bbcode.txt file                                    │
│  - Display preview                                              │
│  - Output: final file                                          │
└────────────────────────────────────────────────────────────────┘
```

## Callout/Admonition Support

支持 Obsidian 风格的 Callout 语法，转换为 BBCode quote：

```markdown
> [!NOTE]
> 这是一个提示信息

> [!WARNING]
> 这是一个警告信息
```

转换结果：

```bbcode
[quote]
[size=100][color=#2196F3][b]📝 注意[/b][/color][/size]

这是一个提示信息
[/quote]
```

| Type | Color | Icon |
|------|-------|------|
| NOTE/INFO | #2196F3 | 📝 |
| TIP/HINT | #4CAF50 | 💡 |
| SUCCESS | #4CAF50 | ✅ |
| WARNING/CAUTION | #FF9800 | ⚠️ |
| DANGER/ERROR | #F44336 | ❌ |
| EXAMPLE | #9C27B0 | 📋 |

## Directory Setup

```javascript
const timestamp = new Date().toISOString().slice(0,10).replace(/-/g, '');
const workDir = `.workflow/.scratchpad/text-formatter-${timestamp}`;

Bash(`mkdir -p "${workDir}"`);
```

## Output Structure

```
.workflow/.scratchpad/text-formatter-{date}/
├── input-config.json       # 输入配置
├── analysis.json           # 内容分析结果
└── output.bbcode.txt       # BBCode+MD 输出
```

## Reference Documents

| Document | Purpose |
|----------|---------|
| [phases/01-input-collection.md](phases/01-input-collection.md) | 收集输入内容 |
| [phases/02-content-analysis.md](phases/02-content-analysis.md) | 分析内容结构 |
| [phases/03-format-transform.md](phases/03-format-transform.md) | 格式转换 |
| [phases/04-output-preview.md](phases/04-output-preview.md) | 输出和预览 |
| [specs/format-rules.md](specs/format-rules.md) | 格式转换规则 |
| [specs/element-mapping.md](specs/element-mapping.md) | 元素映射表 |
| [specs/callout-types.md](specs/callout-types.md) | Callout 类型定义 |
| [templates/bbcode-template.md](templates/bbcode-template.md) | BBCode 模板 |
