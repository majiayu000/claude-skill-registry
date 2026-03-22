---
name: ppw:translation
description: >-
  Translate Chinese academic text into polished English for journal submission.
  Produces LaTeX output with bilingual comparison. 将中文学术草稿翻译为投稿级英文。
triggers:
  primary_intent: translate Chinese academic draft to English
  examples:
    - "Translate this Chinese draft to English"
    - "翻译这段中文为英文"
    - "Help me translate my paper for CEUS submission"
    - "把这段翻译成学术英文"
    - "Translate my introduction section"
    - "帮我把方法部分翻译成英文"
tools:
  - Read
  - Write
  - Structured Interaction
references:
  required:
    - references/expression-patterns.md
    - references/bilingual-output.md
  leaf_hints:
    - references/expression-patterns/introduction-and-gap.md
    - references/expression-patterns/methods-and-data.md
    - references/expression-patterns/results-and-discussion.md
    - references/expression-patterns/conclusions-and-claims.md
    - references/expression-patterns/geography-domain.md
    - references/anti-ai-patterns.md
input_modes:
  - file
  - pasted_text
output_contract:
  - english_tex
  - bilingual_tex
  - self_check_summary
---

## Purpose

This Skill translates Chinese academic drafts into polished English text ready for journal submission. It produces LaTeX-formatted output that preserves technical terminology, follows the target journal's style preferences, and supports user-provided glossary files for domain-specific term mappings. Every invocation generates two output files: an English-only version and a bilingual paragraph-by-paragraph comparison version with Chinese text in LaTeX comments.

## Core Prompt

> Source: [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) — 中转英

````markdown
# Role
你是一位兼具顶尖科研写作专家与资深会议审稿人（ICML/ICLR 等）双重身份的助手。你的学术品味极高，对逻辑漏洞和语言瑕疵零容忍。

# Task
请处理我提供的【中文草稿】，将其翻译并润色为【英文学术论文片段】。

# Constraints
1. 视觉与排版：
   - 尽量不要使用加粗、斜体或引号，这会影响论文观感。
   - 保持 LaTeX 源码的纯净，不要添加无意义的格式修饰。

2. 风格与逻辑：
   - 要求逻辑严谨，用词准确，表达凝练连贯，尽量使用常见的单词，避免生僻词。
   - 尽量不要使用破折号（—），推荐使用从句或同位语替代。
   - 拒绝使用\item列表，必须使用连贯的段落表达。
   - 去除"AI味"，行文自然流畅，避免机械的连接词堆砌。

3. 时态规范：
   - 统一使用一般现在时描述方法、架构和实验结论。
   - 仅在明确提及特定历史事件时使用过去时。

4. 输出格式：
   - Part 1 [LaTeX]：只输出翻译成英文后的内容本身（LaTeX 格式）。
     * 语言要求：必须是全英文。
     * 特别注意：必须对特殊字符进行转义（例如：将 `95%` 转义为 `95\%`，`model_v1` 转义为 `model\_v1`，`R&D` 转义为 `R\&D`）。
     * 保持数学公式原样（保留 $ 符号）。
   - Part 2 [Translation]：对应的中文直译（用于核对逻辑是否符合原意）。
   - 除以上两部分外，不要输出任何多余的对话或解释。

# Execution Protocol
在输出最终结果前，请务必在后台进行自我审查：
1. 审稿人视角：假设你是最挑剔的 Reviewer，检查是否存在过度排版、逻辑跳跃或未翻译的中文。
2. 立即纠正：针对发现的问题进行修改，确保最终输出的内容严谨、纯净且完全英文化。
````

## Trigger

**Activates when the user asks to:**
- Translate Chinese academic text (draft, paragraph, or section) to English
- Produce English LaTeX output from Chinese input
- 将中文学术内容翻译为英文

**Example invocations:**
- "Translate this Chinese draft to English for CEUS"
- "翻译这段中文为英文"
- "Help me translate my methods section"
- "把 intro.md 翻译成学术英文，目标期刊是 CEUS"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `interactive` | | Confirm section detection and glossary application before translating |
| `guided` | | Multi-pass with confirmation at key checkpoints |
| `direct` | Yes | Single-pass translation, minimal interaction |
| `batch` | | Process multiple sections with same settings |

**Default mode:** `direct` (single-pass, no multi-round pipeline).

**Mode inference:** "step by step" or "confirm before translating" switches to `interactive`. "Translate all sections" or "batch" switches to `batch`.

## References

### Required (always loaded)

| File | Purpose |
|------|---------|
| `references/expression-patterns.md` | Academic expression patterns overview and module index |

### Leaf Hints (loaded when needed)

| File | When to Load |
|------|--------------|
| `references/expression-patterns/introduction-and-gap.md` | Input is introduction or background content |
| `references/expression-patterns/methods-and-data.md` | Input is methods, data, or study area content |
| `references/expression-patterns/results-and-discussion.md` | Input is results or discussion content |
| `references/expression-patterns/conclusions-and-claims.md` | Input is conclusion content |
| `references/expression-patterns/geography-domain.md` | Input involves spatial, urban, or planning content |
| `references/anti-ai-patterns.md` | Vocabulary screening during translation |

### Loading Rules

- Load the expression patterns overview at the start to orient module selection.
- Load leaf files only when the current input matches their scope.
- When a target journal is specified, also load `references/journals/[journal].md`.
- If a reference file is missing, warn the user and proceed with reduced capability (except journal templates; see Fallbacks).

### Reference Selection Logic

1. Scan the input for Chinese section keywords: 引言, 背景, 研究方法, 方法, 数据, 结果, 讨论, 结论.
2. If a clear match is found, load the corresponding leaf module directly.
3. If the input spans multiple sections or is ambiguous, load the overview and use Quick Picks.
4. Always load `geography-domain.md` when the input mentions spatial concepts, cities, districts, or planning-related terms.
5. When a target journal is specified, load its template alongside the expression patterns.

## Ask Strategy

**Before starting, ask about:**
1. Target journal (if not specified in trigger) -- determines style loading
2. Custom glossary file path (if the user has domain-specific term mappings)
3. Which section this text belongs to (only if not obvious from content or headers)

**Rules:**
- In `direct` mode, skip pre-questions when the user provides enough context in the trigger.
- If the user specifies a journal with no template at `references/journals/[journal].md`, refuse and explain: "No template found for [journal]. Please add a template at `references/journals/[journal].md` following the CEUS template format before proceeding."
- Never ask more than 3 questions before producing output.
- Use Structured Interaction when available; fall back to plain-text questions otherwise.

## Workflow

### Step 0: Workflow Memory Check

- Read `.planning/workflow-memory.json`. If file missing or empty, skip to Step 1.
- Check if the last 1-2 log entries form a recognized pattern with `ppw:translation` that has appeared >= threshold times in the log. See `skill-conventions.md > Workflow Memory > Pattern Detection` for the full algorithm.
- If a pattern is found, present recommendation via AskUserQuestion:
  - Question: "检测到常用流程：[pattern]（已出现 N 次）。是否直接以 direct 模式运行 ppw:translation？"
  - Options: "Yes, proceed" / "No, continue normally"
- If user accepts: set mode to `direct`, skip Ask Strategy questions.
- If user declines or AskUserQuestion unavailable: continue in normal mode.

### Step 1: Collect Context

- Ask pre-questions per Ask Strategy (target journal, glossary, section type).
- Load required references: expression patterns overview.
- If target journal specified: Read `references/journals/[journal].md`. If file missing, **stop and refuse** -- instruct user to add the template first.
- If glossary file specified: Read glossary and build term mapping. If file not found, warn and proceed without glossary.
- Detect section type from input content and load the appropriate expression pattern leaf module.
- If content involves geography/urban/spatial topics: also load `geography-domain.md`.
- Load `references/anti-ai-patterns.md` for vocabulary screening.
- **Record workflow:** Append `{"skill": "ppw:translation", "ts": "<ISO timestamp>"}` to `.planning/workflow-memory.json`. Create file as `[]` if missing. Drop oldest entry if log length >= 50.

### Step 2: Translate

- **Follow the Core Prompt constraints above** as the primary instruction set for this step.
- Single-pass translation of Chinese input to English.
- Apply journal style preferences (tone, vocabulary, claim calibration) from loaded journal template.
- Use loaded expression patterns to guide phrasing choices.
- Prioritize glossary terms when a match is found.
- Re-translate all text uniformly, including any inline English fragments, for stylistic consistency.
- Preserve all LaTeX commands verbatim: `$...$`, `$$...$$`, `\begin{...}...\end{...}`, `\cite{...}`, `\ref{...}`, `\label{...}`, and custom commands.
- Avoid high-risk anti-AI vocabulary patterns (e.g., "groundbreaking", "novel", "Moreover, it is worth noting").

### Step 3: Generate Output Files

- **Opt-out check:** Before generating output, scan the user's original trigger prompt for any of these phrases (case-insensitive, exact phrase match): `english only`, `no bilingual`, `only english`, `不要中文`. If any phrase is detected: skip the bilingual file entirely -- produce only `[name]_en.tex`. If none detected: produce both files as normal.
- Write English-only version to `[name]_en.tex` with a header comment:
  ```
  % Translated from: [source file]
  % Target journal: [journal or "General"]
  % Generated: [date]
  ```
- Write bilingual comparison to `[name]_bilingual.tex`:
  - Each paragraph: Chinese text as `%` comment lines, English as body text.
  - Number paragraphs with `% --- Paragraph N ---` markers.
- For pasted text input (no source file): use `translation_en.tex` and `translation_bilingual.tex` in the current working directory.
- Preserve the original input file unchanged.

### Step 4: Self-Check

- Report terminology decisions (especially glossary applications and key term choices).
- Flag uncertain translations with explanation of alternatives considered.
- Note any structural changes (sentence splitting, reordering) and why.
- Warn about potential issues: very long sentences, missing references, ambiguous terms.
- Present self-check in session output (not appended to the .tex files).

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| `english_tex` | LaTeX file (`[name]_en.tex`) | Always produced |
| `bilingual_tex` | LaTeX file (`[name]_bilingual.tex`) | Always produced unless opt-out keyword detected |
| `self_check_summary` | Markdown in session | Always produced |

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Input too short (single sentence) | Translate but warn that limited context may affect expression pattern matching |
| No section headers in input | Ask user which section, or default to overview expression patterns |
| Mixed Chinese-English text | Re-translate everything uniformly for stylistic consistency |
| LaTeX-heavy input (mostly formulas) | Preserve all formulas; translate only surrounding natural language text |
| Pasted text with no filename | Use fallback names: `translation_en.tex` / `translation_bilingual.tex` |
| Journal specified but no template | Refuse translation; instruct user to add template at `references/journals/[journal].md` |
| Glossary file not found at path | Warn user and proceed without glossary |
| Input contains tables or figures | Preserve LaTeX table/figure environments; translate captions and surrounding text |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| Structured Interaction unavailable | Ask 1-3 plain-text questions covering highest-impact gaps |
| Expression pattern leaf missing | Use overview entrypoint and Quick Picks |
| Journal template missing for specified journal | **Refuse translation** -- instruct user to add the template first |
| Anti-AI patterns file missing | Proceed without; rely on journal style preferences for tone guidance |
| Glossary file unreadable | Warn user; proceed with standard terminology choices |

## Examples

**User:** "Translate `sections/intro.md` to English for CEUS submission. Glossary at `glossary.txt`."

**Skill workflow:**
1. Load `references/expression-patterns.md`, then `references/expression-patterns/introduction-and-gap.md` (detected from filename and content keywords).
2. Load `references/journals/ceus.md` for CEUS style rules.
3. Load `glossary.txt` and build term mapping.
4. Load `references/anti-ai-patterns.md` for vocabulary screening.
5. Read `sections/intro.md` and translate in a single pass, applying CEUS tone, glossary terms, and introduction expression patterns.
6. Write `sections/intro_en.tex` (English-only with header comment).
7. Write `sections/intro_bilingual.tex` (Chinese in `%` comments, English as body).
8. Present self-check summary in session:
   - Terminology: "城市热岛" -> "urban heat island" (glossary), "建成环境" -> "built environment" (glossary).
   - Uncertain: "宜居性" translated as "livability" -- verify American vs. British spelling for CEUS.
   - Structure: Paragraph 3 split into two sentences for readability.

---

*Skill: translation-skill*
*Conventions: references/skill-conventions.md*
