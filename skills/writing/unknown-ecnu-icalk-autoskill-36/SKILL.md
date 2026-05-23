---
id: "3ee815c6-dfc7-4fa0-8a26-260d361d3b7d"
name: "公众号技术传播风格规范"
description: "生成面向中文技术从业者的技术科普类公众号文章，要求语言通俗有力、类比精准、结构清晰，且严格禁用非标准符号（如 emoji、特殊分隔符、装饰性标点）。"
version: "0.1.0"
tags:
  - "content-generation"
  - "technical-writing"
  - "style-guidance"
  - "chinese"
  - "ai-communication"
triggers:
  - "写一篇公众号文章"
  - "生成技术传播文案"
  - "优化技术内容为公众号风格"
  - "去掉emoji写技术稿"
  - "适配中文工程读者"
---

# 公众号技术传播风格规范

生成面向中文技术从业者的技术科普类公众号文章，要求语言通俗有力、类比精准、结构清晰，且严格禁用非标准符号（如 emoji、特殊分隔符、装饰性标点）。

## Prompt

# Goal
Generate a WeChat Official Account (gongzhonghao) article on a technical AI topic for Chinese engineering practitioners — clear, engaging, and production-ready.

# Constraints & Style
- Use only standard ASCII punctuation and Chinese characters; absolutely NO emojis (e.g., 🌱, 📱, ❌, ✅), NO decorative symbols (e.g., "---", "###", ">" used decoratively), NO non-standard bullets or dividers.
- Replace all emoji-driven emphasis with concise verbal emphasis (e.g., replace "📱手机端App..." → "手机端App...").
- Maintain strong rhetorical structure: lead with a vivid metaphor or question, follow with "是什么/为什么/怎么用" logic, include concrete benchmarks or real-world constraints.
- Prioritize analogies grounded in professional experience (e.g., doctors, engineers, teachers) over pop-culture or abstract metaphors.
- All data points (e.g., "37%", "<0.8%", "500条") must be preserved verbatim — no rounding or paraphrasing.
- Preserve all technical terms in original form (e.g., "EWC", "Replay Buffer", "L2P", "LoRA") and retain code identifiers (e.g., `avalanche`, `datasets`, `transformers`).
- Keep section headers minimal and semantic (e.g., "是什么？", "为什么需要？", "怎么用？") — no prefix symbols or styling.
- End with a clear, actionable CTA (e.g., comment prompt, next-episode teaser) — but without emoji or decorative framing.

# Workflow
None — no multi-step agent process was specified or implied. This is a style + constraint transformation, not a procedural workflow.

## Triggers

- 写一篇公众号文章
- 生成技术传播文案
- 优化技术内容为公众号风格
- 去掉emoji写技术稿
- 适配中文工程读者
