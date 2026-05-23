---
name: chain-of-thought
description: |
  複雑な問題を分解し、推論の流れを整理して短い根拠サマリーを作成するスキル。
  前提整理、論点分解、選択肢比較、判断理由の要約を通じて、説明責任のあるアウトプットを作る。

  Anchors:
  • The Pragmatic Programmer / 適用: 問題分解 / 目的: 実践的な整理
  • Thinking, Fast and Slow / 適用: 判断バイアス確認 / 目的: 判断根拠の明確化
  • Critical Thinking / 適用: 論点整理 / 目的: 根拠の一貫性

  Trigger:
  Use when structuring reasoning, summarizing decision rationale, clarifying assumptions, or documenting a step-by-step analysis.
allowed-tools:
  - bash
  - node
---

# Chain Of Thought

## 概要

推論の分解と整理を行い、根拠を簡潔に説明できるサマリーを作成する。
詳細は `references/` に外部化し、必要時に参照する。

- サマリーテンプレ: `assets/reasoning-summary-template.md`

## ワークフロー

### Phase 1: 問題のフレーミング

**目的**: 目的/制約/前提を明確にする

**アクション**:

1. `references/Level1_basics.md` で基礎概念を確認
2. ゴールと制約を整理
3. 前提と未確定事項を整理

**Task**: `agents/analyze-problem-framing.md`

### Phase 2: 論点分解

**目的**: 論点と検討順序を整理する

**アクション**:

1. `references/Level2_intermediate.md` を参照
2. 主要論点を分割し、検討順序を決定
3. 重要な判断分岐をメモ

**Task**: `agents/structure-reasoning-outline.md`

### Phase 3: 判断根拠の整理

**目的**: 選択肢と根拠を簡潔に整理する

**アクション**:

1. `references/Level3_advanced.md` を参照
2. 選択肢の比較とトレードオフを整理
3. `assets/reasoning-summary-template.md` で要約

**Task**: `agents/summarize-decision-rationale.md`

### Phase 4: 検証と記録

**目的**: 一貫性を検証し記録する

**アクション**:

1. `references/Level4_expert.md` で検証観点を確認
2. 根拠の矛盾/抜け漏れを確認
3. `scripts/validate-skill.mjs` で構造検証
4. `scripts/log_usage.mjs` で記録

**Task**: `agents/validate-reasoning-quality.md`

## Task仕様ナビ

| Task     | 役割           | 入力             | 出力             | 参照先                                 | 実行タイミング |
| -------- | -------------- | ---------------- | ---------------- | -------------------------------------- | -------------- |
| 問題整理 | 目的/制約整理  | 課題情報         | 前提メモ         | `references/Level1_basics.md`          | Phase 1        |
| 論点分解 | 論点/順序整理  | 前提メモ         | 論点アウトライン | `references/Level2_intermediate.md`    | Phase 2        |
| 根拠整理 | 判断理由の要約 | 論点アウトライン | 根拠サマリー     | `assets/reasoning-summary-template.md` | Phase 3        |
| 検証     | 一貫性チェック | 根拠サマリー     | 検証メモ         | `references/Level4_expert.md`          | Phase 4        |

## ベストプラクティス

### すべきこと

- 前提と制約を明確にする
- 論点を分割し順序を決める
- 選択肢とトレードオフを記録する
- 根拠を短く要約する

### 避けるべきこと

- 前提を省略して結論だけ出す
- 論点の優先順位を付けない
- 判断根拠を曖昧にする

## リソース参照

### 参照資料

- `references/Level1_basics.md`: 基礎概念
- `references/Level2_intermediate.md`: 論点分解
- `references/Level3_advanced.md`: 根拠整理
- `references/Level4_expert.md`: 検証/改善
- `references/legacy-skill.md`: 旧版要約（移行時のみ）

### スクリプト

- `scripts/log_usage.mjs`: 実行ログ記録
- `scripts/validate-skill.mjs`: スキル構造検証

### テンプレート

- `assets/reasoning-summary-template.md`: 根拠サマリー

## 変更履歴

| Version | Date       | Changes                                  |
| ------- | ---------- | ---------------------------------------- |
| 2.1.0   | 2025-12-31 | 18-skills準拠、Task仕様追加、scripts整備 |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に完全準拠               |
| 1.0.0   | 2025-12-24 | 初版作成                                 |
