---
name: ppw:caption
description: >-
  Generate or optimize figure/table captions for academic papers.
  Geography-aware: study area, CRS notation, data source.
  Writes output to .tex file. 图表标题生成与优化。
triggers:
  primary_intent: generate or optimize figure/table caption
  examples:
    - "Write a caption for my figure"
    - "帮我写图表标题"
    - "Optimize this table caption"
    - "优化我的图表说明"
    - "Generate a CEUS-ready figure caption"
    - "帮我生成符合期刊要求的图题"
tools:
  - Read
  - Write
  - Structured Interaction
references:
  required:
    - references/expression-patterns.md
  leaf_hints:
    - references/expression-patterns/geography-domain.md
input_modes:
  - file
  - pasted_text
output_contract:
  - caption_latex
---

## Purpose

This Skill generates or optimizes LaTeX figure and table captions for academic papers. For spatial figures (maps, GIS outputs, aerial photos), the Skill proactively collects study area, data source, and CRS metadata using a geography-aware Ask Strategy. For non-spatial figures and tables, geography questions are skipped entirely. Output is written directly to the user's `.tex` file at the correct `\caption{}` location using the Read-before-Write pattern. When a target journal is specified, caption length and style are adapted to the journal template.

## Core Prompt

> Source: [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) — 生成图的标题 + 生成表的标题

**图标题 Prompt：**

````markdown
# Role
你是一位经验丰富的学术编辑，擅长撰写精准、规范的论文插图标题。

# Task
请将我提供的【中文描述】转化为符合顶级会议规范的【英文图标题】。

# Constraints
1. 格式规范：
   - 如果翻译结果是名词性短语：请使用 Title Case 格式，即所有实词的首字母大写，末尾不加句号。
   - 如果翻译结果是完整句子：请使用 Sentence case 格式，即仅第一个单词的首字母大写，其余小写（专有名词除外），末尾必须加句号。

2. 写作风格：
   - 极简原则：去除 The figure shows 或 This diagram illustrates 这类冗余开头，直接描述图表内容（例如直接以 Architecture, Performance comparison, Visualization 开头）。
   - 去 AI 味：尽量避免使用复杂的生僻词，保持用词平实准确。

3. 输出格式：
   - 只输出翻译后的英文标题文本。
   - 不要包含 Figure 1: 这样的前缀，只输出内容本身。
   - 必须对特殊字符进行转义（例如：`%`、`_`、`&`）。
   - 保持数学公式原样（保留 `$` 符号）。
````

**表标题 Prompt：**

````markdown
# Role
你是一位经验丰富的学术编辑，擅长撰写精准、规范的论文表格标题。

# Task
请将我提供的【中文描述】转化为符合顶级会议规范的【英文表标题】。

# Constraints
1. 格式规范：
   - 如果翻译结果是名词性短语：请使用 Title Case 格式，即所有实词的首字母大写，末尾不加句号。
   - 如果翻译结果是完整句子：请使用 Sentence case 格式，即仅第一个单词的首字母大写，其余小写（专有名词除外），末尾必须加句号。

2. 写作风格：
   - 常用句式：对于表格，推荐使用 Comparison with, Ablation study on, Results on 等标准学术表达。
   - 去 AI 味：尽量避免使用 showcase, depict 等词，直接使用 show, compare, present。

3. 输出格式：
   - 只输出翻译后的英文标题文本。
   - 不要包含 Table 1: 这样的前缀，只输出内容本身。
   - 必须对特殊字符进行转义（例如：`%`、`_`、`&`）。
   - 保持数学公式原样（保留 `$` 符号）。
````

## Trigger

**Activates when the user asks to:**
- Write, generate, or create a caption for a figure or table
- Optimize, improve, or rewrite an existing weak caption
- 写图题、生成图表说明、优化标题、改写图表描述

**Example invocations:**
- "Write a caption for my figure" / "帮我写图表标题"
- "Optimize this table caption" / "优化我的图表说明"
- "Generate a CEUS-ready figure caption" / "帮我生成符合期刊要求的图题"
- "Improve the caption for my map figure"
- "帮我生成符合CEUS要求的图题"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `direct` | Yes | Single-pass caption output after Ask Strategy questions |
| `batch` | | Not supported — each caption requires its own figure/table context |

**Default mode:** `direct`. User provides figure/table context and receives a complete LaTeX caption in one pass.

**Path selection (within direct mode):**
- User provides an existing caption to improve → Optimize path
- User provides content description only → Generate path
- Ambiguous → ask: "Do you have an existing caption to improve, or shall I generate one from your description?"

## References

### Required (always loaded)

| File | Purpose |
|------|---------|
| `references/expression-patterns.md` | Academic expression patterns overview — always loaded as entrypoint |

### Leaf Hints (loaded conditionally)

| File | When to Load |
|------|--------------|
| `references/expression-patterns/geography-domain.md` | When figure type is spatial (map, photo, GIS output); provides study area framing, spatial description patterns, planning language |

### Journal Template (conditional)

- When user specifies a target journal, load `references/journals/[journal].md`.
- If template missing, **refuse**: "Journal template for [X] not found. Available: CEUS."
- If no journal specified, ask once; if declined, use general academic style.

## Ask Strategy

**Before starting, collect:**

1. **Figure or table type** (always required — determines whether spatial questions apply):
   map / chart / diagram / photo / data table?

2. **Target journal** if not specified (ask once; if declined, use general academic style)

3. **If figure type is spatial (map, photo, GIS output):**
   - Study area / city name (e.g., "Beijing Chaoyang District")
   - Data source brief (e.g., "OpenStreetMap 2023", "Landsat-8 imagery")
   - CRS (ask only if user knows it; skip if uncertain — do not press)
   - Key legend items (ask only if map or chart has a visible legend)

4. **If figure type is non-spatial (bar chart, line chart, schematic, data table):**
   Skip all geography questions. Ask only for data source if not mentioned.

**Rules:**
- Never ask more than 3 questions before proceeding
- Missing spatial metadata (CRS, legend): skip the clause gracefully — do NOT insert `[MISSING: ...]` stubs in caption output
- If `.tex` file has multiple `\caption{}` commands: ask which `\label{}` (e.g., `\label{fig:study_area}`) is the target before writing
- In `direct` mode with sufficient context already provided, proceed without pre-questions

## Workflow

### Step 0: Workflow Memory Check

- Read `.planning/workflow-memory.json`. If file missing or empty, skip to Step 1.
- Check if the last 1-2 log entries form a recognized pattern with `ppw:caption` that has appeared >= threshold times in the log. See `skill-conventions.md > Workflow Memory > Pattern Detection` for the full algorithm.
- If a pattern is found, present recommendation via AskUserQuestion:
  - Question: "检测到常用流程：[pattern]（已出现 N 次）。是否直接以 direct 模式运行 ppw:caption？"
  - Options: "Yes, proceed" / "No, continue normally"
- If user accepts: set mode to `direct`, skip Ask Strategy questions.
- If user declines or AskUserQuestion unavailable: continue in normal mode.

### Step 1: Collect Context

- Load `references/expression-patterns.md` overview.
- If journal specified, load `references/journals/[journal].md`. If missing, refuse: "Journal template for [X] not found. Available: CEUS."
- Read user input: if file provided, use Read tool; otherwise accept pasted text description.
- Run Ask Strategy questions to fill any gaps not already answered by input.
- Determine path: if user provides an existing caption to improve → Optimize path; if user provides content description only → Generate path; ask if ambiguous.
- **Record workflow:** Append `{"skill": "ppw:caption", "ts": "<ISO timestamp>"}` to `.planning/workflow-memory.json`. Create file as `[]` if missing. Drop oldest entry if log length >= 50.

### Step 2a: Generate Path (new caption from content description)

- **Follow the Core Prompt constraints above** (figure or table prompt as applicable) as the primary instruction set for caption generation.

- If figure type is spatial: load `references/expression-patterns/geography-domain.md`.
- Apply figure vs. table branching logic:

| Type | Caption Focus |
|------|--------------|
| Map | Spatial extent, CRS (if provided), data source, scale bar mention |
| Chart / Diagram | Variables described, trend or comparison purpose, data source |
| Photo | Subject, location (if provided), data source or photographer credit |
| Table | Row/column semantics, statistical context, units, data source |

- Compose caption using locked three-part LaTeX format:
  `\caption{[Subject / study area]. [Key content description]. [Data source statement].}`
- Adapt length and style to journal template if loaded.

### Step 2b: Optimize Path (improve existing weak caption)

- If figure type is spatial: load `references/expression-patterns/geography-domain.md`.
- Review existing caption for: completeness (subject/content/source), spatial metadata gaps, terminology precision, journal length compliance.
- Rewrite using the same branching logic and three-part format as the Generate path.
- Do not introduce `[MISSING: ...]` placeholders; generate from available content.

### Step 3: Write to File

- Read the target `.tex` file (required before Write — locate `\caption{}` or `\caption[]{}` insertion point).
- If multiple `\caption{}` commands exist in the file: apply Ask Strategy rule to confirm target `\label{}` before writing.
- Replace existing `\caption{}` content (or insert if empty) at the identified location.
- Write updated file.
- If Write tool fails: present final caption in conversation with instructions to paste at `\caption{}` location.

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| `caption_latex` | LaTeX `\caption{...}` string written to `.tex` file | Always — file input and Write succeeds |
| `caption_latex` | LaTeX `\caption{...}` string in conversation | Fallback — Write fails, or pasted text input |

**LaTeX caption format examples:**

Figure (spatial):
```latex
\caption{Distribution of urban green space in Shenzhen Nanshan District. Data derived from OpenStreetMap 2023. Projected in WGS 84 / UTM Zone 50N.}
```

Figure (non-spatial):
```latex
\caption{Comparison of model accuracy across three benchmark datasets. All values are F1 scores. Data from the COCO 2017 validation set.}
```

Table:
```latex
\caption{Descriptive statistics of land use change by category, 2010--2020. All areas reported in km\textsuperscript{2}. Data from the Third National Land Survey.}
```

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Journal specified but template not found | Refuse: "Journal template for [X] not found. Available: CEUS." |
| Figure type is spatial but no study area or data source provided | Generate from available content; skip missing clauses; do NOT use `[MISSING: ...]` |
| `.tex` file has multiple `\caption{}` commands | Ask which `\label{}` is the target before writing |
| User provides both existing caption and content description | Default to Optimize path; confirm if ambiguous |
| Figure type unclear ("my figure") | Ask type before any branching logic |
| Input is only a file path with no description | Read the file; ask for clarification if content is ambiguous |
| Non-standard caption format in journal template | Journal template overrides default three-part format rules |
| User declines to provide CRS | Skip CRS clause entirely; do not leave placeholder |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| Structured Interaction unavailable | Ask 1-3 plain-text questions (figure type, journal, study area if spatial) |
| `geography-domain.md` leaf missing | Proceed with general spatial description; warn user of reduced quality |
| Journal template missing (no journal specified) | Ask once; if declined, use general academic style |
| Write tool fails | Present caption in conversation; advise user to paste at `\caption{}` location |
| `.tex` file not found or unreadable | Present caption in conversation |

## Examples

**Invocation:** "Write a caption for my map figure showing urban heat island distribution in Guangzhou."

**Ask Strategy exchange:**
- Type: map (spatial → geography questions apply)
- Study area: Guangzhou
- Data source: Landsat-8 imagery, 2022
- CRS: user does not know → skipped
- Journal: CEUS

**Generated caption (after loading CEUS template and geography-domain.md):**
```latex
\caption{Spatial distribution of urban heat island intensity in Guangzhou. Land surface temperature derived from Landsat-8 imagery (2022). City boundary data from the National Geomatics Center of China.}
```

**Write step:** Skill reads `paper.tex`, locates `\caption{}` at `\label{fig:uhi}`, replaces content, writes file.

---

*Skill: caption-skill*
*Conventions: references/skill-conventions.md*
