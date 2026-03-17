---
name: Article Illustrator
model: reasoning
description: >
  When the user wants to add illustrations to an article or blog post. Triggers
  on: "illustrate article", "add images to article", "generate illustrations",
  "article images", or requests to visually enhance written content. Analyzes
  article structure, identifies positions for visual aids, and generates
  illustrations using a Type x Style two-dimension approach.
version: 1.0.0
tags: [writing, illustration, images, articles, content]
---

# Article Illustrator

Analyze articles, identify optimal illustration positions, and generate images using a Type x Style consistency system.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install article-illustrator
```


## NEVER Do

- Illustrate metaphors literally (e.g., if article says "chainsaw cutting watermelon," visualize the underlying concept instead)
- Generate generic decorative images that don't connect to content
- Skip the settings confirmation step (Step 3)
- Begin generating before confirming type, density, and style with the user
- Create illustrations without justifying each position by content needs

## Two Dimensions

| Dimension | Controls | Examples |
|-----------|----------|----------|
| **Type** | Information structure, layout | infographic, scene, flowchart, comparison, framework, timeline |
| **Style** | Visual aesthetics, mood | notion, warm, minimal, blueprint, watercolor, elegant, editorial, scientific |

Types and styles combine freely: `--type infographic --style blueprint`

### Type Selection Guide

| Type | Best For |
|------|----------|
| `infographic` | Data, metrics, technical articles |
| `scene` | Narratives, personal stories, emotional content |
| `flowchart` | Tutorials, workflows, processes |
| `comparison` | Side-by-side, before/after, options |
| `framework` | Methodologies, models, architecture |
| `timeline` | History, progress, evolution |

### Style Selection Guide

| Style | Best For |
|-------|----------|
| `notion` (Default) | Knowledge sharing, SaaS, productivity |
| `elegant` | Business, thought leadership |
| `warm` | Personal growth, lifestyle, education |
| `minimal` | Philosophy, core concepts |
| `blueprint` | Architecture, system design |
| `watercolor` | Lifestyle, travel, creative |
| `editorial` | Tech explainers, journalism |
| `scientific` | Academic, technical research |

Full style specs and compatibility matrix: [references/styles.md](references/styles.md)

### Auto Selection by Content

| Content Signals | Type | Style |
|-----------------|------|-------|
| API, metrics, data, numbers | infographic | blueprint, notion |
| Story, emotion, journey | scene | warm, watercolor |
| How-to, steps, workflow | flowchart | notion, minimal |
| vs, pros/cons, before/after | comparison | notion, elegant |
| Framework, model, architecture | framework | blueprint, notion |
| History, timeline, progress | timeline | elegant, warm |

## Workflow

### Step 1: Pre-check

1. **Determine input type** — file path or pasted content
2. **Determine output directory** — check preferences or ask user:
   - `{article-dir}/` — same directory
   - `{article-dir}/illustrations/` — illustrations subdirectory (recommended)
   - `illustrations/{topic-slug}/` — independent directory
3. **Check existing images** — if images exist, ask: supplement / overwrite / regenerate
4. **Confirm article update method** (file input only) — update original or create `{name}-illustrated.md` copy
5. **Load preferences** — check for EXTEND.md in project or user home

### Step 2: Analyze Content

| Analysis | Description |
|----------|-------------|
| Content type | Technical / Tutorial / Methodology / Narrative |
| Core arguments | 2-5 main points to visualize |
| Visual opportunities | Positions where illustrations add value |
| Recommended type | Based on content signals |
| Recommended density | Based on length and complexity |

**Illustrate:** core arguments (required), abstract concepts, data comparisons, processes/workflows.

**Skip:** literal metaphors, decorative scenes, generic illustrations.

### Step 3: Confirm Settings (Required)

Use a structured question with 3-4 questions in ONE call:

- **Q1 — Type**: recommended option + alternatives
- **Q2 — Density**: minimal (1-2), balanced (3-5, recommended), rich (6+)
- **Q3 — Style**: recommended based on type/content compatibility matrix
- **Q4 — Language** (only if source language differs from user language)

### Step 4: Generate Outline

Save as `outline.md` with YAML frontmatter (type, density, style, count) and per-illustration details: position, purpose, visual content, filename.

### Step 5: Generate Images

1. Create prompts following [references/prompt-construction.md](references/prompt-construction.md)
2. Save prompts to `prompts/illustration-{slug}.md`
3. Generate sequentially, reporting progress after each
4. On failure: retry once, then log and continue

### Step 6: Finalize

Insert image references after corresponding paragraphs:

```markdown
![description](illustrations/{slug}/NN-{type}-{slug}.png)
```

Output a summary with article path, settings, image count, and positions.

## Output Structure

```
illustrations/{topic-slug}/
├── source-{slug}.{ext}
├── outline.md
├── prompts/
│   └── illustration-{slug}.md
└── NN-{type}-{slug}.png
```

## Prompt Construction Principles

Good illustration prompts must include:

1. **Layout structure first** — describe composition, zones, flow direction
2. **Specific data/labels** — use actual numbers, terms from the article
3. **Visual relationships** — how elements connect to each other
4. **Semantic colors** — meaning-based choices (red=warning, green=efficient)
5. **Style characteristics** — line treatment, texture, mood
6. **Aspect ratio** — end with ratio and complexity level

Avoid: vague descriptions, literal metaphor illustrations, missing labels, generic decorative elements.

Full templates by type: [references/prompt-construction.md](references/prompt-construction.md)

## Type x Style Compatibility

| | notion | warm | minimal | blueprint | watercolor | elegant | editorial | scientific |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| infographic | ++ | + | ++ | ++ | + | ++ | ++ | ++ |
| scene | + | ++ | + | - | ++ | + | + | - |
| flowchart | ++ | + | + | ++ | - | + | ++ | + |
| comparison | ++ | + | ++ | + | + | ++ | ++ | + |
| framework | ++ | + | ++ | ++ | - | ++ | + | ++ |
| timeline | ++ | + | + | + | ++ | ++ | ++ | + |

`++` highly recommended | `+` compatible | `-` not recommended

## Usage Examples

```bash
# Auto-select type and style
illustrate path/to/article.md

# Specify type
illustrate path/to/article.md --type infographic

# Specify type and style
illustrate path/to/article.md --type flowchart --style notion

# Specify density
illustrate path/to/article.md --density rich
```

## Extension Support

Custom configurations via EXTEND.md files:

- **Project level**: `.article-illustrator/EXTEND.md`
- **User level**: `$HOME/.config/article-illustrator/EXTEND.md`

Supports: watermark, preferred type/style, custom styles, language, output directory.

## Modification

| Action | Steps |
|--------|-------|
| **Edit** | Update prompt, regenerate, update reference |
| **Add** | Identify position, create prompt, generate, update outline, insert |
| **Delete** | Delete files, remove reference, update outline |

## References

| File | Content |
|------|---------|
| [references/usage.md](references/usage.md) | Command syntax, options, input modes |
| [references/styles.md](references/styles.md) | Style gallery, compatibility matrix, auto-selection |
| [references/prompt-construction.md](references/prompt-construction.md) | Prompt templates for each illustration type |
| `references/styles/<style>.md` | Full specifications for each visual style |
| `references/config/preferences-schema.md` | EXTEND.md configuration schema |
| `references/config/first-time-setup.md` | First-time preference setup flow |
| [prompts/system.md](prompts/system.md) | System prompt reference |
