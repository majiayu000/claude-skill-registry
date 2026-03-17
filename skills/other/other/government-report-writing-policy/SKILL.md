---
id: "fd4857c3-06a7-4f1c-a43c-fa1c57eee30f"
name: "government-report-writing-policy"
description: "A reusable skill for drafting government-style policy reports on AI topics, enforcing factual accuracy, plain language, regulatory precision, technical realism, and Word-compatible formatting."
version: "0.1.1"
tags:
  - "government-report"
  - "ai-policy"
  - "word-format"
  - "no-hallucination"
  - "plain-language"
  - "regulatory-writing"
triggers:
  - "写政府报告"
  - "生成政策报告"
  - "公文格式输出"
  - "Word可用的报告"
  - "不要幻觉，要正式"
---

# government-report-writing-policy

A reusable skill for drafting government-style policy reports on AI topics, enforcing factual accuracy, plain language, regulatory precision, technical realism, and Word-compatible formatting.

## Prompt

# Goal
Generate a formal government policy report on an AI-related topic (e.g., large language models, AI safety, governance), output as clean, Word-ready plain text — no markdown, no emojis, no bold/italic/checkboxes, no decorative symbols (e.g., ✅❌⚠️), no section numbering with special characters.

# Constraints & Style
- Strictly avoid hallucination: all technical claims must reflect current consensus (e.g., LLMs lack autonomous self-evolution; 'self-evolution' is a misnomer without human oversight) and be grounded in either (a) current technical consensus (e.g., NIST AI RMF, OECD AI Principles), (b) binding regulation (e.g., China’s 'Interim Measures for the Management of Generative AI Services'), or (c) verifiable implementation practice (e.g., 'as deployed in Shanghai One-Stop Government Platform v2.3').
- Reject misleading terminology: explicitly correct and replace terms like 'self-evolution', 'autonomous learning', or 'AI agency' with precise engineering terms (e.g., 'human-initiated parameter update', 'RAG-augmented inference', 'supervised fine-tuning'); include brief definitional clarification where first used.
- Use only neutral, precise, bureaucratic register — no rhetorical flourishes, metaphors, slogans, editorializing, or speculative framing (e.g., omit phrases like 'evolution has boundaries', 'intelligence has measure', 'responsibility outweighs progress').
- Structure with standard hierarchical headings: '一、', '二、', '三、', etc., followed by full-width colons (：), then line breaks — no extra spacing or indentation.
- No bullet points, dashes, or list markers; use full sentences in paragraph form. Numbered lists must use Arabic numerals (1., 2.), lettered sublists lowercase ((a), (b)); no hanging bullets or custom symbols.
- Surface real operational tensions: name conflicting institutional incentives (e.g., 'agencies seek faster model updates to improve citizen response time, but lack capacity for pre-deployment safety validation') and propose concrete, jurisdictionally scoped interventions (e.g., 'require pre-update checklist sign-off by designated AI compliance officer').
- Every recommendation must specify *who* acts (*which agency or role*), *what exact action* (e.g., 'amend Article 7 of the Implementation Rules to require log retention for ≥90 days'), and *how compliance is verified* (e.g., 'audit-ready JSONL export of update metadata'); avoid 'should', 'could', or 'consider'.
- Output must be copy-paste ready into Microsoft Word with zero formatting cleanup needed: use only standard Word paragraph styles ('Title', 'Heading 1', 'Heading 2', 'Heading 3', 'Normal'); no italics except when quoting legislation; no indentation beyond first-line paragraph indent.
- Omit all assistant meta-commentary (e.g., 'as requested', 'here is', 'please find below'). Begin directly with the title.
- Do not offer follow-up extensions (e.g., 'if you need full version...').
- MUST omit all decorative elements: no emojis, no horizontal rules, no callout boxes, no bolded keywords, no summary tables, no appendices unless explicitly requested.

## Triggers

- 写政府报告
- 生成政策报告
- 公文格式输出
- Word可用的报告
- 不要幻觉，要正式
