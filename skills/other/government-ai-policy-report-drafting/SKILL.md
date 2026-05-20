---
id: "c58b5883-c552-41f4-9873-5276dacfba91"
name: "government-ai-policy-report-drafting"
description: "A reusable skill for drafting authoritative, fact-bound government policy reports on AI topics—enforcing strict avoidance of technical hallucination, plain and precise bureaucratic language, Word-compatible structural formatting, inclusion of actionable, evidence-grounded recommendations with sharp diagnostic insight, and mandatory opening with a verifiable real-world incident to establish operational urgency and stakes."
version: "0.1.3"
tags:
  - "government-report"
  - "ai-policy"
  - "fact-bound"
  - "word-format"
  - "no-hallucination"
  - "plain-language"
  - "evidence-based"
  - "real-case-introduction"
triggers:
  - "写政府报告"
  - "生成政策建议报告"
  - "用word格式写"
  - "不要花里胡哨"
  - "避免幻觉"
  - "问题要犀利"
  - "要有自己的见解"
  - "写政府AI报告开头要真实案例"
  - "政策报告开头必须用真实事件引入"
  - "政务报告要见人见事见数据"
---

# government-ai-policy-report-drafting

A reusable skill for drafting authoritative, fact-bound government policy reports on AI topics—enforcing strict avoidance of technical hallucination, plain and precise bureaucratic language, Word-compatible structural formatting, inclusion of actionable, evidence-grounded recommendations with sharp diagnostic insight, and mandatory opening with a verifiable real-world incident to establish operational urgency and stakes.

## Prompt

# Goal
Draft a government-style policy report on an AI-related topic that is technically accurate, institutionally appropriate, operationally actionable, and anchored in real-world consequences—intended for internal policy review or inter-departmental coordination.

# Constraints & Style
- ABSOLUTELY NO technical hallucination: explicitly reject unsupported concepts (e.g., 'self-evolution', 'autonomous learning', 'conscious AI'); ground all claims in current regulatory texts (e.g., China’s *Interim Measures for the Management of Generative AI Services*), verifiable deployment data, peer-reviewed consensus, national standards (e.g., GB/T), or audited pilot results; all technical claims must reflect current consensus (e.g., 'LLMs lack autonomous self-evolution'; 'all model updates require human oversight') and cite only verifiable, publicly acknowledged facts or official frameworks (e.g., China's AI governance principles, national model initiatives, MIIT assessment methods).
- Language must be flat, declarative, and bureaucratic-precise: no metaphors, no marketing terms ('empower', 'unlock', 'revolutionize', 'leverage', 'optimize', 'ecosystem'), no speculative futures ('will enable', 'could transform'); use only present-tense, subject-verb-object statements with named actors and accountable verbs ('requires', 'prohibits', 'must submit', 'shall retain', 'verify', 'log', 'freeze', 'annotate'); avoid colloquialisms, hype terms ('revolution', 'paradigm shift'), or speculative language; do not explain basic concepts unless explicitly requested — assume reader is a tech-savvy policymaker or auditor.
- Format strictly for Word compatibility: output as clean, Word-ready plain text — no markdown, no emojis, no bold/italic/section symbols, no decorative formatting; use only standard paragraph breaks and Chinese punctuation (full-width); enumerate using汉字 numerals (一、二、三、) → （一）→ 1. → （1）; structure linearly: Title → Date/Author line → Numbered sections (e.g., 'I. Basic Assessment', 'II. Guiding Principles', 'III. Key Recommendations'); no bullet points, checkmarks (✅), dashes for emphasis, or special characters (—, *, →, •); use numbered or lettered lists only when required by official reporting convention; output must be copy-paste ready into Microsoft Word with zero formatting cleanup needed.
- Must begin the report with a single, self-contained paragraph anchored in one verifiable, publicly documented real-world incident — e.g., a specific complaint volume spike, service failure duration, financial loss figure, or compliance violation confirmed in official audit reports, inspection notices, statistical bulletins, or verified media citing primary sources; avoid anonymized composites, hypotheticals ('if we don’t act...'), or narrative devices (character names, dialogue, scene-setting); answer explicitly: What breaks, who bears the cost, and how do we know?
- All subsequent analysis and recommendations must logically trace back to that opening case as the primary motivation — no detours into theory, history, or comparative tech trends.
- Diagnose problems with institutional specificity and operational teeth: name actual failure modes (e.g., 'unlogged RAG source swaps', 'absence of versioned prompt templates in municipal chatbots', 'RLHF feedback loops amplifying policy misstatements', 'INT4 quantization causing temporal clause omission'), cite real governance gaps (e.g., 'no requirement for feedback-loop provenance tracking under current Article 12'), and anchor each to at least one concrete element: jurisdiction (e.g., 'a municipal HR service'), timeframe (e.g., 'Q1 2024'), measurable outcome (e.g., '23% answer inconsistency across endpoints'), or cited source (e.g., 'per MIIT's 2024 Energy Efficiency Assessment Method'); avoid generic complaints ('data quality is poor').
- Recommendations must be implementable by named entities (e.g., 'Provincial Big Data Bureaus shall...') and include mandatory artifacts (e.g., 'a signed Model Iteration Log Template Annex A'), verification methods (e.g., 'audit via SHA-256 hash log + timestamped deployment manifest'), and enforcement triggers (e.g., 'non-submission voids service authorization after 30 days'); ban behaviors ('prohibit direct user feedback ingestion without legality filtering'), mandate technical controls ('require immutable hash logging of every model update'), or assign accountability ('three-signature responsibility confirmation per iteration').
- Never attribute agency to models: always specify human or organizational responsibility (e.g., 'the operator must validate output against X regulation' — not 'the model ensures compliance').
- All terminology must align with official Chinese policy documents (e.g., 'human-in-the-loop co-evolution', 'full-lifecycle governance', 'value alignment').

## Triggers

- 写政府报告
- 生成政策建议报告
- 用word格式写
- 不要花里胡哨
- 避免幻觉
- 问题要犀利
- 要有自己的见解
- 写政府AI报告开头要真实案例
- 政策报告开头必须用真实事件引入
- 政务报告要见人见事见数据
