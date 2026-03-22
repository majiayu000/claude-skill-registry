---
id: "672bd950-efc5-4c90-bb4d-70fc933f4ca5"
name: "government-ai-policy-report-writing"
description: "A reusable skill for drafting factual, plain-language, Word-compatible government policy reports and regulatory documents on AI topics — enforcing technical accuracy, strict regulatory alignment, actionable governance insights, and zero technical hallucination within China's official framework."
version: "0.1.2"
tags:
  - "government-report"
  - "ai-policy"
  - "regulatory-compliance"
  - "word-format"
  - "technical-accuracy"
  - "china-regulation"
triggers:
  - "写政府报告"
  - "生成政策建议报告"
  - "正式公文格式"
  - "word格式报告"
  - "不用markdown"
  - "问题犀利"
  - "要有自己的见解"
  - "撰写政务AI监管文件"
  - "起草大模型政策建议"
  - "写政府场景的AI技术说明"
  - "生成合规性公文"
  - "编写面向监管者的AI风险分析"
---

# government-ai-policy-report-writing

A reusable skill for drafting factual, plain-language, Word-compatible government policy reports and regulatory documents on AI topics — enforcing technical accuracy, strict regulatory alignment, actionable governance insights, and zero technical hallucination within China's official framework.

## Prompt

# Goal
Generate a formal government policy report or regulatory document (e.g., internal memo, inter-departmental briefing, or guidance draft) on an AI-related topic, output as clean, Word-ready plain text (no Markdown, no emojis, no bold/italic markup, no horizontal rules, no decorative symbols).

# Constraints & Style
- Strictly avoid hallucinated claims or speculative capabilities: explicitly deny non-existent features (e.g., 'self-evolution', 'autonomous learning', 'emergent reasoning') using definitive, cited language; all technical statements must reflect current consensus and anchor in verifiable regulatory frameworks (e.g., 'LLMs lack autonomous self-evolution'; '《生成式人工智能服务管理暂行办法》第十二条') and national standards (e.g., GB/T).
- Use formal, neutral, bureaucratic Mandarin — no colloquialisms, metaphors, slogans, poetic phrasing, speculative futurism, or journalistic flair; prefer active voice and subject-verb-object syntax; define every non-standard technical term at first use with both Chinese and standardized English (e.g., '量化学习（Quantization-Aware Learning, QAL）') and link to real-world governance impact (e.g., '导致法律条文引用环节出现关键词截断错误').
- Structure with unambiguous hierarchical numbering (e.g., '一、', '1.', '（1）') and plain bullet points (using '•' or '-', not emoji checkmarks ✅); apply consistent paragraph breaks only — no indentation beyond standard Word paragraph spacing; use顿号for enumerations within sentences.
- Enforce Word compatibility: use ASCII characters only; no markdown syntax (**bold**, `code`, > blockquotes, --- dividers), no color, no special symbols, no footnotes, disclaimers, authorship lines, or 'note:' asides — except functional closing '（完）' and a final attribution-anchored '数据来源：' note listing only publicly available, institutional references (e.g., '中国信息通信研究院《2024大模型推理效能白皮书》').
- Prioritize analytical sharpness: identify root causes (not just symptoms), name responsible parties (e.g., 'service providers', 'platform operators'), cite concrete regulatory clauses and national standards, and propose auditable, enforceable mechanisms — not vague principles.
- Distinguish sharply between mandates and recommendations: use '须', '禁止', '应重新提交' for binding requirements; reserve '建议' only for non-binding guidance.
- Omit all non-essential content: no disclaimers, asides, or explanatory parentheses inside the report body; font/spacing guidance may appear *only* as parenthetical instruction at the very end.

# Workflow
1. First, state the core technical fact — clearly negating misused terminology and grounding the discussion in human-controlled processes and binding regulation.
2. Then, diagnose 2–3 concrete, systemic risk points — each tied to a specific actor, failure mode, legal violation, and verifiable source (regulation article, standard clause, audited report, or reproducible benchmark).
3. Next, propose 3–4 targeted, procedural recommendations — each specifying *who must act*, *what exact step must be taken*, *what evidence must be produced*, and *which rule or standard it satisfies* — framed as binding actions, not options.
4. Close with a one-sentence normative anchor: reaffirm the tool-over-agent framing and link technical realism to governance legitimacy; append '数据来源：' with only publicly available institutional references.

## Triggers

- 写政府报告
- 生成政策建议报告
- 正式公文格式
- word格式报告
- 不用markdown
- 问题犀利
- 要有自己的见解
- 撰写政务AI监管文件
- 起草大模型政策建议
- 写政府场景的AI技术说明
