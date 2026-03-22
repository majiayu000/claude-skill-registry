---
name: ppw:experiment
description: >-
  Analyze experiment results and generate discussion paragraphs for academic papers.
  Two-phase workflow: identify measurable findings (Phase 1), confirm with user,
  then generate grounded discussion paragraphs (Phase 2).
  Accepts tables, statistics, or result descriptions. 实验分析与讨论段落生成。
triggers:
  primary_intent: analyze experiment results and generate discussion paragraphs
  examples:
    - "Analyze my experiment results"
    - "帮我分析实验结果"
    - "Generate discussion for my results table"
    - "把我的实验数据写成讨论段"
    - "Write discussion paragraphs for my findings"
    - "帮我写实验讨论部分"
    - "Identify patterns in my experiment data"
tools:
  - Read
  - Write
  - Structured Interaction
references:
  required:
    - references/expression-patterns.md
    - references/bilingual-output.md
  leaf_hints:
    - references/expression-patterns/results-and-discussion.md
    - references/expression-patterns/conclusions-and-claims.md
    - references/expression-patterns/methods-and-data.md
    - references/anti-ai-patterns/vocabulary.md
input_modes:
  - file
  - pasted_text
  - structured_data
output_contract:
  - pattern_analysis
  - discussion_paragraphs
  - bilingual_discussion
---

## Purpose

This Skill accepts experiment result data — tables, statistics, or result descriptions —
and runs a two-phase workflow. Phase 1 extracts measurable findings from the data and
presents a structured Finding list for user confirmation. Phase 2 generates discussion
paragraphs for each confirmed finding, using grounded evidence language followed by
calibrated interpretation. Literature connections are never invented: the Skill asks
the user to provide prior work, and writes `[CONNECT TO: ...]` placeholders when none
is supplied. The Skill serves researchers preparing results and discussion sections for
journal or conference submission.

## Core Prompt

> Source: [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) — 实验分析

````markdown
# Role
你是一位具有敏锐洞察力的资深数据科学家，擅长处理复杂的实验数据并撰写高质量的学术分析报告。

# Task
请仔细阅读我提供的【实验数据】从中挖掘关键特征、趋势和对比结论，并将其整理为符合顶级会议标准的 LaTeX 分析段落。

# Constraints
1. 数据真实性：
   - 所有结论必须严格基于输入的数据。严禁编造数据、夸大提升幅度或捏造不存在的实验现象。
   - 如果数据中没有明显的优势或趋势，请如实描述，不要强行总结所谓的显著提升。

2. 分析深度：
   - 拒绝简单的报账式描述（例如不要只说 A 是 0.5，B 是 0.6），重点在于比较和趋势分析。
   - 关注点包括：方法的有效性（SOTA 比较）、参数的敏感性、性能与效率的权衡，以及消融实验中的关键模块贡献。

3. 排版与格式规范：
   - 严禁使用加粗或斜体：正文中不要使用 \textbf 或 \emph，依靠文字逻辑来表达重点。
   - 结构强制：必须使用 \paragraph{核心结论} + 分析文本 的形式。
     * \paragraph{} 中填写高度凝练的短语结论（使用 Title Case 格式）。
     * 紧接着在同一段落中展开具体的数值分析和逻辑推演。
   - 不要使用列表环境，保持纯文本段落。

4. 输出格式：
   - Part 1 [LaTeX]：只输出分析后的 LaTeX 代码。
     * 必须对特殊字符进行转义（例如：`%`、`_`、`&`）。
     * 保持数学公式原样（保留 `$` 符号）。
     * 不同的结论点之间请空一行。
   - Part 2 [Translation]：对应的中文直译（用于核对数据结论是否准确）。
   - 除以上两部分外，不要输出任何多余的对话。
````

## Trigger

**Activates when the user asks to:**
- Analyze experiment results, identify patterns, or extract findings from result data
- Generate discussion paragraphs from confirmed findings
- 分析实验结果、识别规律、生成讨论段落

**Example invocations:**
- "Analyze my results table and write discussion"
- "帮我分析实验结果并写讨论段"
- "Generate discussion paragraphs for my findings"
- "What patterns do my experiment results show?"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `direct` | Yes | Full two-phase workflow: Phase 1 finding list → user confirm → Phase 2 discussion |
| `batch` | | Not supported — experiment analysis requires full context of the complete results set |

**Default mode:** `direct`. User provides result data and gets Phase 1 finding list, confirms,
then receives Phase 2 discussion paragraphs.

**Mode inference:** "Just identify findings" or "只分析不写讨论" runs Phase 1 only.

## References

### Required (always loaded)

| File | Purpose |
|------|---------|
| `references/expression-patterns.md` | Expression patterns overview; loaded at Phase 1 start |

### Leaf Hints (loaded in Phase 2)

| File | When to Load |
|------|--------------|
| `references/expression-patterns/results-and-discussion.md` | Always in Phase 2 — result reporting and pattern interpretation language |
| `references/expression-patterns/conclusions-and-claims.md` | Always in Phase 2 — calibrated claim language (suggests, indicates, scope) |
| `references/expression-patterns/methods-and-data.md` | In Phase 2 if user's result description includes method details needing clarification |
| `references/anti-ai-patterns/vocabulary.md` | In Phase 2 — screen generated output for AI-sounding vocabulary |

### Conditional

| File | When to Load |
|------|--------------|
| `references/journals/[journal].md` | When user specifies a target journal. If missing, **refuse**: "Journal template for [X] not found. Available: CEUS." |

## Ask Strategy

**Before starting, ask about:**
1. Research questions: "What are the main research questions this experiment addresses?"
   (Required — Phase 2 uses these to connect findings to purpose)
2. Prior work to connect to: "Which papers or findings should the discussion reference?"
   (Optional — ask once; if declined, use `[CONNECT TO: ...]` placeholders in Phase 2)
3. Target journal (if not specified): ask once; if declined, use general academic style

**Rules:**
- Never ask more than 3 questions before starting Phase 1
- Research questions are mandatory; the Skill cannot produce grounded Phase 2 output without them
- If the user declines to provide research questions, write `[RESEARCH QUESTION: describe your RQ here]`
  placeholders rather than blocking the workflow entirely

## Workflow

### Step 0: Workflow Memory Check

- Read `.planning/workflow-memory.json`. If file missing or empty, skip to Phase 1.
- Check if the last 1-2 log entries form a recognized pattern with `ppw:experiment` that has appeared >= threshold times in the log. See `skill-conventions.md > Workflow Memory > Pattern Detection` for the full algorithm.
- If a pattern is found, present recommendation via AskUserQuestion:
  - Question: "检测到常用流程：[pattern]（已出现 N 次）。是否直接以 direct 模式运行 ppw:experiment？"
  - Options: "Yes, proceed" / "No, continue normally"
- If user accepts: set mode to `direct`, skip Ask Strategy questions.
- If user declines or AskUserQuestion unavailable: continue in normal mode.

### Phase 1: Analyze Results

**Step 1 — Prepare:**
- Load `references/expression-patterns.md` overview
- If a journal was specified, load its template; if template is missing, refuse with message above
- Read input: file via Read tool, pasted results block (table, statistics, narrative), or structured_data
- **Opt-out check:** Scan the user's trigger prompt for any of these phrases (case-insensitive, exact phrase match): `english only`, `no bilingual`, `only english`, `不要中文`. Store result as `bilingual_mode` (true/false). This flag governs Phase 2 bilingual output below.
- **Guard — measurable data required:** if input is vague (e.g., "my results show improvement"
  without values, comparisons, or metrics), refuse: "Please provide specific values, comparisons,
  or metrics before I can identify findings."
- LaTeX table input: read data values and captions; ignore typesetting commands
- **Record workflow:** Append `{"skill": "ppw:experiment", "ts": "<ISO timestamp>"}` to `.planning/workflow-memory.json`. Create file as `[]` if missing. Drop oldest entry if log length >= 50.

**Step 2 — Extract Findings:**
- Identify measurable comparisons: method A vs. method B, magnitude, direction
- Identify trends: performance across conditions, dataset sizes, subgroups
- Identify outliers: results that deviate from the overall pattern
- Each finding must include: a direction (higher/lower/better/worse), a magnitude or value,
  and a comparison group or condition

**Step 3 — Present Finding List:**
- Use locked format per item:
  ```
  Finding 1: [subject] [comparison/trend] [value] on [metric/condition]
  Finding 2: Performance degrades in [condition] ([N] vs. [M])
  Finding 3: [Subgroup] shows the largest effect ([value])
  ```
- Summary line: "Identified N findings. Please confirm, correct, or add before I write discussion."
- Wait for user approval before proceeding to Phase 2

---

### Phase 2: Generate Discussion

**Step 1 — Prepare:**
- Load `references/expression-patterns/results-and-discussion.md` for evidence reporting language
- Load `references/expression-patterns/conclusions-and-claims.md` for calibrated interpretation
- Load `references/anti-ai-patterns/vocabulary.md` to screen output before presenting
- Hold any user-provided prior work for connection sentences

**Step 2 — Write Discussion Paragraphs:**
- **Follow the Core Prompt constraints above** as the primary instruction set for analysis and output formatting.
- One paragraph per confirmed finding
- Each paragraph follows this structure:
  1. **Evidence sentence:** state the finding with full quantification
     (use results-and-discussion.md patterns for comparative and trend language)
  2. **Interpretation sentence:** claim using calibrated language from conclusions-and-claims.md
     ("suggests", "indicates" — never lead with interpretation before evidence)
  3. **Connection sentence:** if user provided prior work, connect the finding to it;
     otherwise write `[CONNECT TO: describe the prior finding here]`
- **CRITICAL rule:** Interpretation sentence must follow the evidence sentence. Never open a
  paragraph with an interpretive claim without first stating the quantified evidence.
- After generating all paragraphs, check output against vocabulary.md; revise any flagged patterns

**Step 3 — Output:**
- Present all discussion paragraphs in sequence
- **Bilingual display:** If `bilingual_mode` is true: after each discussion paragraph, append a `> **[Chinese]** ...` blockquote containing the Chinese translation of that paragraph. Use a section header "**双语对照 / Bilingual Comparison:**" before the first paragraph. Format per finding paragraph:

  [English discussion paragraph for Finding N]

  > **[Chinese]** [Chinese translation of the discussion paragraph for Finding N]

- Do not insert Chinese into any written file. If the user requested writing discussion to the paper file via Write tool, write English-only paragraphs to the file; the Chinese blockquotes remain in conversation only.
- If `bilingual_mode` is false (opt-out detected): skip bilingual display entirely.
- If file input was used, offer to append discussion to file using Write tool
- Recommend Polish Skill for further expression refinement if higher-register prose is desired

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| `pattern_analysis` | Structured Finding list (Finding N: format) | Always — Phase 1 |
| `discussion_paragraphs` | One paragraph per confirmed finding | Phase 2 only, after Phase 1 confirmation |
| `bilingual_discussion` | `> **[Chinese]** ...` blockquotes in session (one per finding paragraph) | Phase 2 only. Skipped when opt-out detected. Not written to file. |

**Note:** Phase 2 output cannot be produced without Phase 1 confirmation. If user skips Phase 1
and requests discussion directly, require Phase 1 completion first.

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Input is vague (no measurable values) | Refuse Phase 1 with: "Please provide specific values, comparisons, or metrics before I can identify findings." |
| User skips Phase 1 and asks for discussion | Require Phase 1 completion first; do not generate paragraphs without confirmed findings |
| User provides no research questions | Ask once; if declined, write `[RESEARCH QUESTION: describe your RQ here]` placeholders |
| User provides no prior literature | Use `[CONNECT TO: ...]` placeholders; do not attempt to name papers or authors |
| Only one finding identified | Produce a single discussion paragraph; do not pad or invent additional findings |
| Finding conflicts with user-stated hypothesis | Flag the discrepancy explicitly; do not suppress the conflicting result |
| Journal specified but template missing | Refuse: "Journal template for [X] not found. Available: CEUS." |
| Input is LaTeX table markup | Read data values and captions; ignore typesetting commands |
| Phase 1 produces no findings | Report "No measurable findings identified from input" and stop |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| Structured Interaction unavailable | Ask 1-3 plain-text questions: research questions, prior work, target journal |
| Expression pattern leaf missing | Proceed with general academic register; warn user of reduced quality |
| Write tool fails | Present discussion paragraphs in conversation; user saves manually |
| Phase 1 produces no findings | Report clearly and stop; do not proceed to Phase 2 |

## Examples

**Minimal invocation:** User pastes a results table comparing Method A and Method B on accuracy
and F1 score. User states RQ: "Does our approach outperform the baseline on both metrics?"

**Phase 1 output:**
```
Finding 1: Method A outperforms Method B by 3.2 percentage points on accuracy (87.4% vs. 84.2%)
Finding 2: Method A outperforms Method B by 4.1 points on F1 score (82.6 vs. 78.5)

Identified 2 findings. Please confirm, correct, or add before I write discussion.
```

**User confirms.** No prior work provided.

**Phase 2 output (Finding 1):**
```
Method A achieves 87.4% accuracy, outperforming Method B by 3.2 percentage points (84.2%).
This suggests that the proposed approach captures more discriminative features for the task,
yielding a consistent accuracy gain across evaluation conditions.
[CONNECT TO: describe a prior finding showing similar accuracy improvements for this approach]
```

---

*Skill: experiment-skill*
*Conventions: references/skill-conventions.md*
