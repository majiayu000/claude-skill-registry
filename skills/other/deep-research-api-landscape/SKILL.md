---
name: deep-research-api-landscape
description: "Use when building automated research systems. Official Deep Research APIs (OpenAI, Gemini, Perplexity) over browser automation."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-13"
---
# Deep Research API Landscape (2026)

**Extracted:** 2026-02-13
**Context:** AIによる自動リサーチシステムを構築する際の技術選定

## Problem
Deep Research品質のリサーチを自動化したい場合、
Playwright + ヘッドレスブラウザでWeb UIを操作する方法が
思い浮かびやすいが、ToSリスクと脆弱性がある。

## Solution
2026年時点で、主要3社が公式Deep Research APIを提供している。
ブラウザ自動化は不要。

| サービス | API | モデル | 特徴 |
|---------|-----|--------|------|
| OpenAI | `/responses` endpoint | `o3-deep-research-2025-06-26` | MCP連携、信頼サイト制限 |
| Gemini | Interactions API | Gemini 3 Pro | 最大60分調査、public beta |
| Perplexity | `sonar-deep-research` | Opus 4.5 | SimpleQA 93.9%精度 |

追加候補:
- Tavily Research API（private beta、SOTA性能）
- Exa Research API（セマンティック検索特化、SimpleQA 94.9%）

## Key Links
- OpenAI: https://platform.openai.com/docs/guides/deep-research
- Gemini: https://ai.google.dev/gemini-api/docs/deep-research
- Perplexity: https://docs.perplexity.ai/getting-started/models/models/sonar-deep-research

## When to Use
- リサーチ自動化システムの技術選定時
- 「Playwrightでディープリサーチを自動化したい」という要望が出た時
- APIベースの情報収集パイプラインを設計する時
