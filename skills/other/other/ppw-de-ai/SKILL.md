---
name: ppw:de-ai
description: >-
  Detect and rewrite AI-generated patterns in English academic text.
  Two-phase workflow: scan with risk tagging, then batch rewrite.
  Triggers on "de-AI", "降AI", "reduce AI traces", "AI检测".
triggers:
  primary_intent: Detect and rewrite AI patterns in academic text
  examples:
    - "De-AI this paragraph"
    - "降AI这段论文"
    - "Check for AI patterns in my paper"
    - "Reduce AI traces in my introduction"
    - "AI检测并改写"
    - "Scan this text for AI-generated phrasing"
    - "帮我降低AI检测分数"
tools:
  - Read
  - Edit
  - Structured Interaction
references:
  required:
    - references/anti-ai-patterns.md
    - references/expression-patterns.md
    - references/bilingual-output.md
  leaf_hints:
    - references/anti-ai-patterns/vocabulary.md
    - references/anti-ai-patterns/sentence-patterns.md
    - references/anti-ai-patterns/transitions-and-tone.md
    - references/expression-patterns/introduction-and-gap.md
    - references/expression-patterns/methods-and-data.md
    - references/expression-patterns/results-and-discussion.md
    - references/expression-patterns/conclusions-and-claims.md
input_modes:
  - file
  - pasted_text
output_contract:
  - detection_report
  - rewritten_text
  - rewrite_report
  - bilingual_conversation
---

## Purpose

This Skill detects AI-generated patterns in English academic text and rewrites flagged passages with explainable, risk-tagged results. It scans text against three pattern dimensions (vocabulary inflation, sentence overclaims, transition smoothing) from the anti-AI patterns library, presents detections grouped by risk level (High Risk / Medium Risk / Optional), and lets users batch-select which items to rewrite. Rewrites restructure expressions rather than just swapping synonyms, preserving academic meaning and quality. For file input, edits are made in-place with LaTeX comment annotations for traceability; for pasted text, results appear in conversation.

## Core Prompt

> Source: [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) — 去 AI 味（LaTeX 英文）

````markdown
# Role
你是一位计算机科学领域的资深学术编辑，专注于提升论文的自然度与可读性。你的任务是将大模型生成的机械化文本重写为符合顶级会议（如 ACL, NeurIPS）标准的自然学术表达。

# Task
请对我提供的【英文 LaTeX 代码片段】进行"去 AI 化"重写，使其语言风格接近人类母语研究者。

# Constraints
1. 词汇规范化：
   - 优先使用朴实、精准的学术词汇。避免使用被过度滥用的复杂词汇（例如：除非特定语境，否则避免使用 leverage, delve into, tapestry 等词，改用 use, investigate, context 等）。
   - 只有在必须表达特定技术含义时才使用术语，避免为了形式上的"高级感"而堆砌辞藻。

2. 结构自然化：
   - 严禁使用列表格式：必须将所有的 item 内容转化为逻辑连贯的普通段落。
   - 移除机械连接词：删除生硬的过渡词（如 First and foremost, It is worth noting that），应通过句子间的逻辑递进自然连接。
   - 减少插入符号：尽量减少破折号（—）的使用，建议使用逗号、括号或从句结构替代。

3. 排版规范：
   - 禁用强调格式：严禁在正文中使用加粗或斜体进行强调。学术写作应通过句式结构来体现重点。
   - 保持 LaTeX 纯净：不要引入无关的格式指令。

4. 修改阈值（关键）：
   - 宁缺毋滥：如果输入的文本已经非常自然、地道且没有明显的 AI 特征，请保留原文，不要为了修改而修改。
   - 正向反馈：对于高质量的输入，应在 Part 3 中给予明确的肯定和正向评价。

5. 输出格式：
   - Part 1 [LaTeX]：输出重写后的代码（如果原文已足够好，则输出原文）。
     * 语言要求：必须是全英文。
     * 必须对特殊字符进行转义（例如：`%`、`_`、`&`）。
     * 保持数学公式原样（保留 `$` 符号）。
   - Part 2 [Translation]：对应的中文直译。
   - Part 3 [Modification Log]：
     * 如果进行了修改：简要说明调整了哪些机械化表达。
     * 如果未修改：请直接输出中文评价："[检测通过] 原文表达地道自然，无明显 AI 味，建议保留。"
   - 除以上三部分外，不要输出任何多余的对话。

# Execution Protocol
在输出前，请自查：
1. 拟人度检查：确认文本语气自然。
2. 必要性检查：当前的修改是否真的提升了可读性？如果是为了换词而换词，请撤销修改并判定为"检测通过"。
````

**AI 味高频词汇参考表：**

````
Accentuate, Ador, Amass, Ameliorate, Amplify, Alleviate, Ascertain, Advocate, Articulate, Bear, Bolster,
Bustling, Cherish, Conceptualize, Conjecture, Consolidate, Convey, Culminate, Decipher, Demonstrate,
Depict, Devise, Delineate, Delve, Delve Into, Diverge, Disseminate, Elucidate, Endeavor, Engage, Enumerate,
Envision, Enduring, Exacerbate, Expedite, Foster, Galvanize, Harmonize, Hone, Innovate, Inscription,
Integrate, Interpolate, Intricate, Lasting, Leverage, Manifest, Mediate, Nurture, Nuance, Nuanced, Obscure,
Opt, Originates, Perceive, Perpetuate, Permeate, Pivotal, Ponder, Prescribe, Prevailing, Profound, Recapitulate,
Reconcile, Rectify, Rekindle, Reimagine, Scrutinize, Substantiate, Tailor, Testament, Transcend, Traverse,
Underscore, Unveil, Vibrant
````

## Trigger

**Activates when the user asks to:**
- Detect, scan, or check for AI-generated patterns in academic text
- Rewrite or reduce AI traces in English writing
- 降AI、检测AI痕迹、降低AI检测分数

**Example invocations:**
- "De-AI this paragraph" / "降AI这段论文"
- "Check my paper for AI patterns" / "AI检测并改写"
- "Scan only -- just show detections" / "只扫描不改写"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `direct` | Yes | Full detect-then-rewrite two-phase workflow with batch selection |
| `batch` | | Same operation across multiple files with same settings |

**Default mode:** `direct`. User says "de-AI this" and gets detect + rewrite.

**Mode inference:** "scan only", "just check", or "只检测" triggers detect-only (skip rewrite phase). "De-AI all sections" or "batch" switches to `batch`.

## References

### Required (always loaded)

| File | Purpose |
|------|---------|
| `references/anti-ai-patterns.md` | Risk model, category map, retrieval contract |
| `references/expression-patterns.md` | Academic expression patterns for rewrite quality |

### Leaf Hints (loaded proactively for detection)

| File | When to Load |
|------|--------------|
| `references/anti-ai-patterns/vocabulary.md` | Always -- loaded proactively for full-text scan |
| `references/anti-ai-patterns/sentence-patterns.md` | Always -- loaded proactively for full-text scan |
| `references/anti-ai-patterns/transitions-and-tone.md` | Always -- loaded proactively for full-text scan |

### Leaf Hints (loaded during rewrite phase)

| File | When to Load |
|------|--------------|
| `references/expression-patterns/introduction-and-gap.md` | Rewriting introduction or background content |
| `references/expression-patterns/methods-and-data.md` | Rewriting methods or data content |
| `references/expression-patterns/results-and-discussion.md` | Rewriting results or discussion content |
| `references/expression-patterns/conclusions-and-claims.md` | Rewriting conclusion content |

### Loading Rules

- Load ALL three anti-AI pattern leaves proactively at the start for full-text scanning.
- Load expression patterns overview at the start; load section-specific leaves during rewrite phase based on detected section type.
- When a target journal is specified, also load `references/journals/[journal].md`. If template missing, **refuse** with message: "Journal template for [X] not found. Available: CEUS."
- If an anti-AI pattern leaf is missing, warn the user and proceed with reduced detection coverage.

## Ask Strategy

**Before starting, ask about:**
1. Target journal (if not specified) -- determines style consideration during rewrite
2. Scope: full paper or specific section (if ambiguous)

**Rules:**
- In `direct` mode, skip pre-questions when the user provides enough context.
- Never ask more than 2 questions before scanning.
- Use Structured Interaction when available; fall back to plain-text questions otherwise.

## Workflow

### Step 0: Workflow Memory Check

- Read `.planning/workflow-memory.json`. If file missing or empty, skip to Phase 1.
- Check if the last 1-2 log entries form a recognized pattern with `ppw:de-ai` that has appeared >= threshold times in the log. See `skill-conventions.md > Workflow Memory > Pattern Detection` for the full algorithm.
- If a pattern is found, present recommendation via AskUserQuestion:
  - Question: "检测到常用流程：[pattern]（已出现 N 次）。是否直接以 direct 模式运行 ppw:de-ai？"
  - Options: "Yes, proceed" / "No, continue normally"
- If user accepts: set mode to `direct`, skip Ask Strategy questions.
- If user declines or AskUserQuestion unavailable: continue in normal mode.

### Phase 1: Detect

**Step 1 -- Prepare:**
- Load all three anti-AI pattern leaves (vocabulary, sentence-patterns, transitions-and-tone).
- If target journal specified, load journal template; if missing, refuse.
- Read user input (file via Read tool, or pasted text from conversation).
- **Opt-out check:** Scan the user's trigger prompt for any of these phrases (case-insensitive, exact phrase match): `english only`, `no bilingual`, `only english`, `不要中文`. Store result as `bilingual_mode` (true/false). This flag governs Phase 2 bilingual output below.
- **Record workflow:** Append `{"skill": "ppw:de-ai", "ts": "<ISO timestamp>"}` to `.planning/workflow-memory.json`. Create file as `[]` if missing. Drop oldest entry if log length >= 50.

**Step 2 -- Scan:**
- **Follow the Core Prompt constraints above** as the primary instruction set for detection and rewrite.
- Scan full text against all three pattern dimensions in a single pass.
- For each match, check domain term protection: if the flagged term is standard domain terminology used in context (e.g., "landscape" in a geography paper, "robust" in a statistics paper), mark as SKIPPED with reason.
- For Optional-tier matches: only flag if the pattern appears 3+ times in the text. Single occurrences are suppressed to reduce noise.

**Step 3 -- Present Detection Report:**
- Summary line: "Found N AI patterns (X High Risk / Y Medium Risk / Z Optional)" plus count of skipped domain terms.
- Detailed list grouped by risk level (High first, then Medium, then Optional). Each item shows:

```
[#N] [HIGH RISK] Vocabulary Inflation
  Original: "This groundbreaking approach transforms the analytical framework"
  Pattern: "groundbreaking" -- promotional, exaggerated vocabulary (vocabulary.md)
  Suggestion: "This useful approach improves the analytical framework"
```

**Step 4 -- User Selection:**
- Ask which items to rewrite:
  - "Fix all High Risk"
  - "Fix High + Medium"
  - "Fix all"
  - Specific items by number: "fix 1, 3, 7"

### Phase 2: Rewrite

**Step 1 -- Group and Rewrite:**
- Group selected items by paragraph. When multiple items appear in the same paragraph, rewrite them together in one pass to maintain coherence.
- Load relevant expression pattern leaves based on section type for higher quality alternatives beyond the anti-AI replacement column.
- Restructure expressions -- do not just swap synonyms. Preserve academic meaning and quality.
- If target journal specified, consider journal style preferences during rewrite.

**Step 2 -- Apply Changes:**
- **File input:** Use Edit tool for in-place modifications. Add `% [De-AI] Original: <original text>` LaTeX comment on the line immediately before each rewritten passage.
  - Multi-line originals: each line gets its own `% [De-AI] Original:` prefix.
  - If existing `% [De-AI] Original:` annotations found, clean them up before adding new ones.
- **Pasted text:** Present rewritten version in conversation with before/after comparison for each changed passage.

**Step 3 -- Rewrite Report:**

| Field | Content |
|-------|---------|
| Total rewrites | Applied N of M detected items |
| By category | Vocabulary inflation: count, Sentence overclaim: count, Transition smoothing: count |
| Skipped items | Optional below threshold, domain terms protected |
| Word count delta | +/- N words |

**Step 4 -- Bilingual Display:**
- If `bilingual_mode` is true and input was a file: for each paragraph that was rewritten in Step 1, display a `> **[Chinese]** ...` blockquote in conversation showing the Chinese translation of the rewritten English text.
- Use a section header in conversation: "**双语对照 / Bilingual Comparison:**" before the first blockquote.
- Format per paragraph:

  > **[Chinese]** [Chinese translation of the rewritten paragraph]

- Do not insert Chinese into the .tex file. The file remains English-only and submission-ready.
- If `bilingual_mode` is false (opt-out detected): skip this step entirely.
- Pasted text input: if `bilingual_mode` is true, append the `> **[Chinese]** ...` blockquote immediately after each rewritten paragraph in the conversation diff output.

**Step 5 -- Summary:**
- If further polishing is needed, recommend: "Consider running the Polish Skill for additional refinement."

## LaTeX Annotation Format

- Format: `% [De-AI] Original: <original text>` on the line immediately before the replacement.
- Multi-line originals: each line gets its own `% [De-AI] Original:` prefix.
- Annotations are valid LaTeX comments -- the file compiles with them present.
- Cleanup: after user confirms acceptance, remove all lines matching `^% \[De-AI\] Original:`.
- If existing `% [De-AI] Original:` annotations are found, clean them up before adding new ones.

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| Detection report | Structured markdown (summary + detailed list) | Always (Phase 1) |
| Rewritten text | In-place LaTeX with annotations (file) or conversation diff (pasted) | Phase 2 |
| Rewrite report | Structured markdown table | After Phase 2 |
| Word count delta | Integer | After Phase 2 |
| `bilingual_conversation` | `> **[Chinese]** ...` blockquotes in session | Phase 2 rewritten paragraphs only. Skipped when opt-out detected. |

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No AI patterns detected | Report "No AI patterns detected" and exit; do not proceed to rewrite |
| Input too short (< 3 sentences) | Warn detection may be unreliable on short text; proceed if user confirms |
| All detections are domain terms (all skipped) | Report "N patterns matched but all identified as domain terminology -- no rewrites needed" |
| Existing `% [De-AI] Original:` annotations | Clean up old annotations before running new scan |
| Input language is not English | Warn and suggest running Translation Skill first |
| Journal template missing when journal specified | Refuse: "Journal template for [X] not found. Available: CEUS." |
| Very long input (10+ pages) | Process in sections; maintain cross-section awareness |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| Structured Interaction unavailable | Ask 1-2 plain-text questions (journal + scope) |
| Anti-AI pattern leaf missing | Warn user, proceed with available modules (reduced detection coverage) |
| Expression pattern leaf missing | Use overview entrypoint for general rewrite patterns |
| Target journal not specified | Ask once; if declined, use general academic style for rewrites |
| File is read-only or Edit fails | Present changes as a diff in conversation; user applies manually |

---

*Skill: de-ai-skill*
*Conventions: references/skill-conventions.md*
