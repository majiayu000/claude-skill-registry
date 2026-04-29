---
name: geo-content-optimizer
description: 'Optimize content for AI citations in ChatGPT, Perplexity, AI Overviews, Gemini, Claude. AI引用优化/GEO优化/AI搜索'
version: "9.9.5"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when optimizing content for AI engines like ChatGPT, Perplexity, AI Overviews, Gemini, Claude, or Copilot. Also for AI citation optimization, generative engine visibility, AI引用优化, AI搜索优化, GEO优化, or 让AI引用我."
argument-hint: "<content URL or text> [target AI engine]"
metadata:
  author: aaron-he-zhu
  version: "9.9.5"
  geo-relevance: "high"
  tags:
    - geo
    - ai-seo
    - ai-citations
    - chatgpt-optimization
    - perplexity-optimization
    - google-ai-overview
    - gemini
    - generative-engine-optimization
    - llm-citations
    - quotable-content
    - AI引用优化
    - GEO优化
    - AI最適化
    - AI최적화
    - optimizacion-ia
  triggers:
    - "optimize for AI"
    - "AI optimization"
    - "get cited by ChatGPT"
    - "GEO optimization"
    - "generative engine optimization"
    - "get cited by AI"
    - "show up in ChatGPT answers"
    - "how to appear in AI answers"
    - "Perplexity optimization"
    - "AI引用优化"
    - "AI搜索优化"
    - "GEO优化"
    - "让AI引用我"
    - "AI不提我的品牌"
    - "AIコンテンツ最適化"
    - "ChatGPT対策"
    - "AI 최적화"
    - "ChatGPT 인용"
    - "optimización para IA"
    - "citación de IA"
    - "otimização para IA"
    - "respostas de IA"
---

# GEO Content Optimizer

Optimizes content for AI-generated answers and citation surfaces such as ChatGPT, Perplexity, Gemini, Claude, and AI Overviews.

## What This Skill Does

Improves structure, authority signals, factual density, quotable statements, source attribution, and overall GEO readiness.

## Quick Start

```text
Optimize this content for GEO/AI citations: [content or URL]
Make this article more likely to be cited by AI systems
Write content about [topic] optimized for both SEO and GEO
Audit this content for GEO readiness and suggest improvements
AI Overview is eating clicks on 12 head queries — build a recovery plan
```

See [references/ai-overview-recovery.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/geo-content-optimizer/references/ai-overview-recovery.md) for the 4-phase playbook (measure → diagnose → rewrite → monitor) tailored to recovery scenarios (as opposed to generic GEO optimization).

## Skill Contract

**Expected output**: a ready-to-use asset or implementation-ready transformation plus a short handoff summary ready for `memory/content/`.

- **Reads**: the brief, target keywords, entity inputs, quality constraints, and prior decisions from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available. **Canonical entity profiles**: if the content mentions a brand / person / product, this skill MUST consult `memory/entities/<slug>.md` (per the [entity-geo handoff schema](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/entity-geo-handoff-schema.md)) to populate `display_name`, `description_short`, `ai_resolution_status` and decide whether disambiguation boilerplate is needed. If the profile is missing or stale (>90 days), declare `DONE_WITH_CONCERNS` and recommend `entity-optimizer` as an open loop.
- **Writes**: a user-facing content, metadata, or schema deliverable plus a reusable summary that can be stored under `memory/content/`.
- **Promotes**: approved angles, messaging choices, missing evidence, and publish blockers to `memory/hot-cache.md`, `memory/decisions.md`, and `memory/open-loops.md`.
- **Next handoff**: use the `Next Best Skill` below when the asset is ready for review or deployment.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

Use `~~AI monitor` and `~~SEO tool` when connected; otherwise ask for target queries, content, engines, competitor examples, and known AI-citation gaps. See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md).

## Instructions

When a user requests GEO optimization, run these five steps:

1. **Load CORE-EEAT GEO-First Targets** — prioritize C02, C09, O03, O05, E01, O02 plus engine-specific preferences.
2. **Analyze Current Content** — score clear definitions, quotable statements, factual density, source citations, Q&A format, authority signals, freshness, and structure clarity.
3. **Apply GEO Techniques** — add standalone 25-50 word definitions, sourced quotable statements, expert/source signals, Q&A/tables/lists, specific data, and visible-content-matching FAQ schema.
4. **Generate GEO Output** — report Changes Made, before/after GEO score, and AI Query Coverage.
5. **CORE-EEAT GEO Self-Check** — verify C02, C04, C09, O02, O03, O05, O06, R01, R02, R04, R07, E01, Exp10, Ept08 with Pass/Warn/Fail.

> **Reference**: See [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/geo-content-optimizer/references/instructions-detail.md) for the full CORE-EEAT GEO target tables, AI engine preferences, analysis templates, optimization report template, self-check matrix, and examples.

## Example

**User**: "Optimize this paragraph for GEO: 'Email marketing is a good way to reach customers. It's been around for a while and many businesses use it.'"

**Output** adds a clear definition, dated/source-backed facts, structured list, quotable statements, and a before/after GEO score. See the full pattern in [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/geo-content-optimizer/references/instructions-detail.md#example).

## GEO Optimization Checklist

> **Reference**: See the GEO Readiness Checklist in [references/geo-optimization-techniques.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/geo-content-optimizer/references/geo-optimization-techniques.md) for the full checklist covering definitions, quotable content, authority, structure, and technical elements.

## Tips for Success

Answer first, be specific, cite dated sources, stay current, match query format, and build authority. Full list in [references/instructions-detail.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/geo-content-optimizer/references/instructions-detail.md#tips-for-success).

### Save Results

On user confirmation, save a dated summary to `memory/content/YYYY-MM-DD-<topic>.md` and promote key conclusions to `memory/hot-cache.md`.

## Reference Materials

- [Instructions Detail](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/geo-content-optimizer/references/instructions-detail.md) - Full 5-step workflow, CORE-EEAT GEO targets, self-check matrix, worked example, tips
- [GEO Optimization Techniques](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/geo-content-optimizer/references/geo-optimization-techniques.md) - Detailed before/after examples, templates, and checklists for each technique
- [AI Citation Patterns](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/geo-content-optimizer/references/ai-citation-patterns.md) - How Google AI Overviews, ChatGPT, Perplexity, and Claude select and cite sources
- [Quotable Content Examples](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/geo-content-optimizer/references/quotable-content-examples.md) - Before/after examples of content optimized for AI citation

## Next Best Skill

- **Primary**: [content-quality-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/content-quality-auditor/SKILL.md) — verify the optimized content is strong enough to ship and cite.
