---
name: type-safety-patterns
description: |
  TypeScript厳格モードによる型安全性設計を専門とするスキル。
  型推論、型ガード、ジェネリック、識別可能ユニオンのパターンを体系的に設計します。

  Anchors:
  • 『Effective TypeScript』（Dan Vanderkam） / 適用: 型設計原則 / 目的: 型安全性最大化
  • TypeScript Handbook / 適用: 型システム理解 / 目的: 正確な型設計

  Trigger:
  TypeScript型設計時、型ガード実装時、ジェネリック設計時、ユニオン型設計時に使用
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Type Safety Patterns スキル

## 概要

TypeScript厳格モードによる型安全性設計を専門とするスキル。型推論分析、型ガード設計、ジェネリック型パターン、識別可能ユニオン設計を通じて、コンパイル時に型エラーを検出し、ランタイムエラーを防止します。

## ワークフロー

### Phase 1: 型推論分析

**目的**: 既存コードの型推論状況を把握し、問題箇所を特定

**アクション**:

1. `references/Level1_basics.md` と `references/strict-mode-guide.md` を確認
2. `agents/type-inference-analysis.md` を参照し、any型やワイドニング問題を検出
3. 改善が必要な箇所をリストアップ

### Phase 2: 型安全性設計

**目的**: 型ガードとパターンを設計し、型安全性を向上

**アクション**:

1. `agents/type-guard-design.md` を参照し、型ガードを設計
2. `agents/generic-type-patterns.md` で再利用可能なジェネリックを設計
3. `agents/discriminated-union-design.md` で識別可能ユニオンを設計

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/check-type-safety.mjs` で型安全性を確認
2. `scripts/validate-skill.mjs` でスキル構造を確認
3. `scripts/log_usage.mjs` を実行して記録を残す

## Task仕様（ナビゲーション）

型安全性設計の各タスクと対応するエージェント・リソースの対応表

| Task                 | エージェント                           | 思考様式         | 説明                           |
| -------------------- | -------------------------------------- | ---------------- | ------------------------------ |
| 型推論分析           | `agents/type-inference-analysis.md`    | Dan Vanderkam    | 型推論状況を分析し問題を特定   |
| 型ガード設計         | `agents/type-guard-design.md`          | Anders Hejlsberg | 安全な型ナローイングを実現     |
| ジェネリック設計     | `agents/generic-type-patterns.md`      | Matt Pocock      | 再利用可能なジェネリックを設計 |
| 識別可能ユニオン設計 | `agents/discriminated-union-design.md` | Basarat Ali Syed | 網羅性チェック付きユニオン設計 |

### ワークフロー順序

```
type-inference-analysis → type-guard-design → generic-type-patterns → discriminated-union-design
```

1. **type-inference-analysis**: 型推論結果を分析し、any型やワイドニング問題を検出
2. **type-guard-design**: ユニオン型を安全に絞り込む型ガードを設計
3. **generic-type-patterns**: 再利用可能なジェネリック型と関数を設計
4. **discriminated-union-design**: 網羅性チェック付きの識別可能ユニオンを設計

## ベストプラクティス

### すべきこと

- strictモードを有効にし、すべての厳格オプションを使用
- any型を避け、unknown型とType Guardを組み合わせて使用
- 型推論を活用し、明示的な型注釈を最小化
- 識別可能ユニオンでexhaustive checkを実装

### 避けるべきこと

- as型アサーションの乱用
- any型の明示的使用
- strictモードの無効化
- 型安全性を犠牲にした妥協

## リソース参照

### references/（詳細知識）

| リソース             | パス                                                                                     | 読込条件             |
| -------------------- | ---------------------------------------------------------------------------------------- | -------------------- |
| Level1 基礎          | [references/Level1_basics.md](references/Level1_basics.md)                               | 初回整理時           |
| Level2 実務          | [references/Level2_intermediate.md](references/Level2_intermediate.md)                   | 型設計時             |
| Level3 応用          | [references/Level3_advanced.md](references/Level3_advanced.md)                           | 詳細分析時           |
| Level4 専門          | [references/Level4_expert.md](references/Level4_expert.md)                               | 改善ループ時         |
| strictモード設定     | [references/strict-mode-guide.md](references/strict-mode-guide.md)                       | 初期設定時           |
| 型ガードパターン     | [references/type-guard-patterns.md](references/type-guard-patterns.md)                   | 型ナローイング設計時 |
| ジェネリックパターン | [references/generics-patterns.md](references/generics-patterns.md)                       | 汎用型設計時         |
| 識別可能ユニオン     | [references/discriminated-union-patterns.md](references/discriminated-union-patterns.md) | 網羅性チェック設計時 |

### scripts/（決定論的処理）

| スクリプト                      | 機能                         |
| ------------------------------- | ---------------------------- |
| `scripts/check-type-safety.mjs` | 型安全性チェック             |
| `scripts/log_usage.mjs`         | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`    | スキル構造の検証             |

### assets/（テンプレート・素材）

| アセット                       | 用途                       |
| ------------------------------ | -------------------------- |
| `assets/type-safe-patterns.ts` | 型安全パターンテンプレート |

## 変更履歴

| Version | Date       | Changes                                                   |
| ------- | ---------- | --------------------------------------------------------- |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様対応、4エージェント体制、Task仕様ナビ追加 |
| 1.0.0   | 2025-12-24 | 初期リリース                                              |
