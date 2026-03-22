---
name: ppw:reviewer-simulation
description: >-
  Simulate peer review of academic papers with structured feedback.
  Produces bilingual review report with scoring and actionable suggestions.
  Triggers on "review", "peer review", "simulate reviewer",
  "审稿", "模拟评审".
triggers:
  primary_intent: simulate peer review of academic paper
  examples:
    - "Review this paper"
    - "审稿这篇论文"
    - "Give me a peer review of my draft"
    - "模拟评审我的论文"
    - "Simulate a reviewer for my CEUS submission"
    - "帮我做一个模拟审稿"
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
input_modes:
  - file
  - pasted_text
output_contract:
  - review_report
---

## Purpose

This Skill simulates peer review of academic papers, producing a structured bilingual review report. It assesses the paper across five dimensions (Novelty, Methodology, Writing Quality, Presentation, Significance) with 1-10 scoring, identifies major and minor concerns with actionable three-part feedback (problem, why it matters, suggestion), and delivers a verdict recommendation. When a target journal is specified, journal-specific expectations are woven into review comments. The report follows real journal review conventions and includes inline Chinese translations for every concern and the verdict.

## Core Prompt

> Source: [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) — 论文整体以 Reviewer 视角进行审视

````markdown
# Role
你是一位以严苛、精准著称的资深学术审稿人，熟悉计算机科学领域顶级会议的评审标准。你的职责是作为守门员，确保只有在理论创新、实验严谨性和逻辑自洽性上均达到最高标准的研究才能被接收。

# Task
请深入阅读并分析我上传的【PDF论文文件】。基于我指定的【投稿目标】，撰写一份严厉但具有建设性的审稿报告。

# Constraints
1. 评审基调（严苛模式）：
   - 默认态度：请抱着拒稿的预设心态进行审查，除非论文的亮点足以说服你改变主意。
   - 拒绝客套：省略所有无关痛痒的赞美，直接切入核心缺陷。你的目标是帮作者发现可能导致拒稿的致命伤，而不是让作者开心。

2. 审查维度：
   - 原创性：该工作是实质性的突破还是边际增量？如果是后者，直接指出。
   - 严谨性：数学推导是否有跳跃？实验对比是否公平（Baseline 是否齐全）？消融实验是否充分支撑了核心主张？
   - 一致性：引言中声称的贡献在实验部分是否真的得到了验证？

3. 格式要求：
   - 严禁列表化滥用：在陈述复杂逻辑时，请使用连贯段落。
   - 保持 LaTeX 纯净：不要使用无关的格式指令。

4. 输出格式：
   - Part 1 [The Review Report]：模拟真实的顶会审稿意见（使用中文）。包含以下板块：
     * Summary: 一句话总结文章核心。
     * Strengths: 简要列出 1-2 点真正有价值的贡献。
     * Weaknesses (Critical): 必须列出 3-5 个可能导致直接拒稿的致命问题（如：缺乏核心 Baseline，原理存在逻辑漏洞，创新点被过度包装）。
     * Rating: 给出预估评分（1-10分，其中 Top 5% 为 8分以上）。
   - Part 2 [Strategic Advice]：针对作者的中文改稿建议。
     * 直击痛点：用中文解释 Part 1 中的 Critical Weaknesses 到底因何而起。
     * 行动指南：具体建议作者该补什么实验、该重写哪段逻辑、或该如何降低审稿人的攻击欲。
   - 除以上两部分外，不要输出任何多余的对话。

# Execution Protocol
在输出前，请自查：
1. 你的语气是否太温和了？如果是，请重新审视那些模糊的实验结果，并提出尖锐的质疑。
2. 你指出的问题是否具体？不要说"实验不够"，要说"缺少在 ImageNet 数据集上的鲁棒性验证"。
````

## Trigger

**Activates when the user asks to:**
- Review, peer-review, or simulate reviewer feedback for a paper
- 审稿、模拟评审、模拟审稿人反馈

**Example invocations:**
- "Review this paper" / "审稿这篇论文"
- "Give me a peer review of my draft" / "模拟评审我的论文"
- "Simulate a reviewer for my CEUS submission"
- "帮我做一个模拟审稿"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `direct` | Yes | Single-pass read-analyze-report workflow, produces complete review |
| `batch` | | Not supported -- review requires full-paper context |

**Default mode:** `direct`. User says "review this paper" and gets a complete review report.

**Mode inference:** Default is always `direct`. There is no partial or iterative review mode.

## References

### Required (always loaded)

| File | Purpose |
|------|---------|
| `references/expression-patterns.md` | Academic expression patterns overview for writing quality assessment |

### Leaf Hints (loaded based on paper sections)

| File | When to Load |
|------|--------------|
| `references/expression-patterns/introduction-and-gap.md` | Assessing introduction or background sections |
| `references/expression-patterns/methods-and-data.md` | Assessing methods or data sections |
| `references/expression-patterns/results-and-discussion.md` | Assessing results or discussion sections |
| `references/expression-patterns/conclusions-and-claims.md` | Assessing conclusion sections |
| `references/expression-patterns/geography-domain.md` | Paper involves spatial, urban, or planning topics |

### Journal Template (conditional)

- When user specifies a target journal, load `references/journals/[journal].md`.
- If template missing, **refuse**: "Journal template for [X] not found. Available: CEUS."
- Journal preferences inform review comments where relevant, but core dimensions and weights remain unchanged across all journals.

### Loading Rules

- Load expression patterns overview at the start.
- Load section-specific leaves during analysis based on paper sections encountered.
- Anti-AI patterns are NOT loaded by default. This is a review skill, not a detection skill.
- If an expression pattern leaf is missing, proceed with general writing quality assessment and warn the user.

## Ask Strategy

**Before starting, ask about:**
1. Target journal (if not specified) -- determines whether journal-specific criteria appear in review
2. Input source: file path or pasted text (if ambiguous from trigger)

**Rules:**
- Never ask more than 2 questions before producing the review.
- In `direct` mode, skip pre-questions if the user provided enough context in the trigger.
- Use Structured Interaction when available; fall back to plain-text questions otherwise.

## Workflow

### Step 0: Workflow Memory Check

- Read `.planning/workflow-memory.json`. If file missing or empty, skip to Step 1.
- Check if the last 1-2 log entries form a recognized pattern with `ppw:reviewer-simulation` that has appeared >= threshold times in the log. See `skill-conventions.md > Workflow Memory > Pattern Detection` for the full algorithm.
- If a pattern is found, present recommendation via AskUserQuestion:
  - Question: "检测到常用流程：[pattern]（已出现 N 次）。是否直接以 direct 模式运行 ppw:reviewer-simulation？"
  - Options: "Yes, proceed" / "No, continue normally"
- If user accepts: set mode to `direct`, skip Ask Strategy questions.
- If user declines or AskUserQuestion unavailable: continue in normal mode.

### Step 1: Collect Context

- Load `references/expression-patterns.md` overview.
- If target journal specified, load `references/journals/[journal].md`. If template missing, **refuse** with message: "Journal template for [X] not found. Available: CEUS."
- Read user input: file via Read tool, or pasted text from conversation.
- **Guard -- full paper required:** If input is partial (only introduction, only methods, etc.), refuse with message: "This Skill requires the full paper for review. Please provide the complete manuscript."
- **Guard -- minimum length:** If input is under ~300 words, warn: "Text appears too short for a full paper review. Provide the complete manuscript."
- **Record workflow:** Append `{"skill": "ppw:reviewer-simulation", "ts": "<ISO timestamp>"}` to `.planning/workflow-memory.json`. Create file as `[]` if missing. Drop oldest entry if log length >= 50.

### Step 2: Analyze Paper

- **Follow the Core Prompt constraints above** as the primary instruction set — especially the 严苛模式 review stance.
- Read the full paper to understand claims, evidence structure, and writing quality.
- Load relevant expression pattern leaves based on paper sections encountered (introduction-and-gap.md for intro, methods-and-data.md for methods, etc.) to inform Writing Quality dimension.
- If journal template loaded, cross-reference journal-specific expectations and note where the paper falls short of journal fit.
- Assess across all five dimensions:
  1. **Novelty** -- Is the contribution genuinely new? Incremental or transformative?
  2. **Methodology** -- Is the experimental design sound? Baselines adequate? Ablation studies present?
  3. **Writing Quality** -- Expression clarity, academic register, AI-sounding patterns, terminology consistency
  4. **Presentation** -- Figure/table quality, section organization, flow between sections
  5. **Significance** -- Does the work matter? Practical or theoretical impact?
- **IMPORTANT:** Generate concerns FIRST, then derive dimension scores from the concerns. This prevents score-concern inconsistency.

### Step 3: Generate Review Report

- **Opt-out check:** Before generating the report, scan the user's original trigger prompt for any of these phrases (case-insensitive, exact phrase match): `english only`, `no bilingual`, `only english`, `不要中文`. If any phrase is detected: omit all `> **[Chinese]** ...` blockquotes from the report -- produce English-only concerns, questions, and verdict. If none detected: include Chinese blockquotes as normal.

Write the review report in the following locked structure:

```markdown
# Peer Review Report

**Paper:** [title or filename]
**Target Journal:** [journal name or "General"]
**Date:** [date]

## Scoring Overview

| Dimension | Score (1-10) | Justification |
|-----------|:---:|---------------|
| Novelty | X | [one-line justification] |
| Methodology | X | [one-line justification] |
| Writing Quality | X | [one-line justification] |
| Presentation | X | [one-line justification] |
| Significance | X | [one-line justification] |

## Major Concerns

### Major Concern N: [Descriptive Title]

**Section:** [section name, e.g., "Results (Section 4)"]

**Problem:** [description of the issue]

**Why this matters:** [impact on quality or publishability]

**Suggestion:** [one-sentence directional guidance]

> **[Chinese]** [Chinese translation of all three parts]

## Minor Concerns

### Minor Concern N: [Descriptive Title]

[Same three-part structure with inline Chinese translation]

## Questions for Authors

1. [Question with enough context]
   > **[Chinese]** [Chinese translation]

## Verdict

**Recommendation:** [Accept / Minor Revision / Major Revision / Reject]

[One-sentence summary of the overall assessment]

> **[Chinese]** [Chinese translation of recommendation and summary]
```

**Chinese translation rules:**
- Use inline blockquote format (`> **[Chinese]** ...`) immediately after each concern's English text.
- Preserve domain terminology precisely in Chinese (e.g., "ablation study" as "消融实验", not a generic paraphrase).
- Each Chinese blockquote covers all three parts (problem, why, suggestion) in a single block.
- The Verdict section also receives an inline Chinese translation.

### Step 4: Output

- **File input:** Write the review report to `{input_filename_without_ext}_review.md` in the same directory as the input file. If input filename is unclear, use `review-report.md`.
- **Pasted text input:** Present the complete review report directly in conversation.
- Report the total number of major concerns, minor concerns, and questions identified.

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| Review report | Markdown file or conversation output | Always |
| Scoring overview | 5-dimension table with 1-10 scores | Always |
| Concern count | Summary line (N major, N minor, N questions) | Always reported |

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Input is partial (only one section) | Refuse: "This Skill requires the full paper for review." |
| Input too short (< 300 words) | Warn: "Text appears too short for a full paper review." |
| Input language is Chinese | Warn and suggest Translation Skill first; proceed if user confirms |
| Journal template missing when journal specified | Refuse: "Journal template for [X] not found. Available: CEUS." |
| No significant weaknesses found | Produce report with high scores; note strengths rather than fabricating concerns |
| Paper clearly outside journal scope | Flag as a Major Concern about journal fit |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| Structured Interaction unavailable | Ask 1-2 plain-text questions (journal + input source) |
| Expression pattern reference missing | Proceed with general writing quality assessment; warn user |
| Journal template missing (no journal specified) | Ask once; if declined, review with general academic criteria |
| Write tool fails for output file | Present report in conversation instead |

---

*Skill: reviewer-simulation-skill*
*Conventions: references/skill-conventions.md*
