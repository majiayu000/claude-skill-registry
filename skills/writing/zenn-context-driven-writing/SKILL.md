---
name: zenn-context-driven-writing
description: "Use when preparing context and drafts for experience-based Zenn articles. Parallel research + context file pattern."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-13"
---
# Zenn Article Context-Driven Writing

**Extracted:** 2026-02-13
**Context:** Zenn記事の執筆前にコンテキストを収集・構造化し、ドラフトを生成する

## Problem

Zenn記事を書く際、リサーチ結果・ユーザーの実体験・既存記事との差別化ポイントが
散在していて、ドラフトに一貫性を持たせるのが難しい。

## Solution

### Phase 1: 並列リサーチ（3エージェント同時）

Task toolで3つのresearcherエージェントを**並列起動**:

1. **技術A単体**: 対象技術の機能・特徴・価格（例: Termius）
2. **技術B単体**: 組み合わせ先の技術詳細（例: Claude Code）
3. **組み合わせ**: A×Bの既存記事・コミュニティ反応・差別化ポイント

### Phase 2: ユーザー実体験の取り込み

ユーザーが提供するAI会話ログ（Gemini等との対話）を構造化:

- つまずきポイントを表形式（#, 問題, 原因, 解決）に整理
- 会話フローを時系列でマッピング
- 記事の「オチ」になる気づきを特定

### Phase 3: コンテキストファイル保存

`drafts/article-context_<topic>-<date>.md` に以下を構造化:

1. 記事企画（仮タイトル案、想定読者、核心メッセージ、構成案）
2. 実体験タイムライン
3. 技術コンテキスト
4. 差別化ポイント（既存記事との比較）
5. リサーチ結果（要点のみ、参考記事リスト）

### Phase 4: ドラフト生成

既存記事を2-3本読んでフォーマット・トーンを把握した上で:

- 一人称ナラティブ（「私は〜した」）
- AI会話を対話形式で引用
- つまずきを正直に記録
- 前回記事からの繋がりを意識
- Zenn frontmatter付き

## When to Use

- ユーザーが「Zennの記事のコンテキストを集めて」と依頼した時
- 実体験ベースの技術記事を書く時
- 複数の技術の組み合わせについて記事を書く時
- `~/MyAI_Lab/zenn-content/` で作業する時
