---
name: custom-hooks-patterns
description: |
  Reactカスタムフックの設計・抽出・合成・テストの実務指針を提供するスキル。
  再利用性と保守性を高めるための判断基準を整理する。

  Anchors:
  • Learning React / 適用: フック設計の基本 / 目的: 再利用可能な設計
  • React公式ドキュメント / 適用: フックルール / 目的: 安全な実装
  • Refactoring / 適用: 抽出判断 / 目的: 重複削減と責務分離

  Trigger:
  Use when designing custom React hooks, extracting reusable logic, composing hooks, or validating hook usage patterns.
  custom hooks, hook composition, hook extraction, hook testing, hook design
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# custom-hooks-patterns

## 概要

Reactカスタムフックの抽出基準・設計パターン・合成パターン・テスト戦略を整理し、再利用性の高いフック設計を支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 抽出対象のロジックと目的を整理する。

**アクション**:

1. 抽出候補を洗い出す。
2. `references/extraction-criteria.md` で抽出基準を確認する。
3. 既存フックの有無を確認する。

**Task**: `agents/analyze-hook-opportunity.md` を参照

### Phase 2: 設計

**目的**: フックの責務とAPIを設計する。

**アクション**:

1. `references/design-patterns.md` で設計パターンを確認する。
2. `references/composition-patterns.md` で合成方針を決める。
3. 入出力と副作用を整理する。

**Task**: `agents/design-hook-composition.md` を参照

### Phase 3: 実装

**目的**: フックを実装し、利用パターンを整える。

**アクション**:

1. `assets/basic-hooks-template.md` と `assets/advanced-hooks-template.md` を参照して実装する。
2. `scripts/analyze-hook-candidates.mjs` で抽出候補の確認を行う。
3. 変更点を記録する。

**Task**: `agents/implement-custom-hook.md` を参照

### Phase 4: 検証と記録

**目的**: 使い勝手・テスト観点を検証し、記録する。

**アクション**:

1. `references/testing-strategies.md` でテスト観点を確認する。
2. `assets/hook-review-checklist.md` でレビューする。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-hook-quality.md` を参照

## Task仕様ナビ

| Task                     | 起動タイミング | 入力         | 出力                       |
| ------------------------ | -------------- | ------------ | -------------------------- |
| analyze-hook-opportunity | Phase 1開始時  | 既存ロジック | 抽出候補メモ、判断理由     |
| design-hook-composition  | Phase 2開始時  | 抽出候補メモ | フック設計書、API方針      |
| implement-custom-hook    | Phase 3開始時  | フック設計書 | 実装メモ、変更内容         |
| validate-hook-quality    | Phase 4開始時  | 実装メモ     | レビューレポート、改善提案 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項               | 理由                 |
| ---------------------- | -------------------- |
| 抽出基準を明確にする   | 責務が曖昧にならない |
| フックAPIを小さくする  | 再利用性が高まる     |
| 合成パターンを採用する | 依存関係が整理される |
| テスト観点を明文化する | 回帰防止になる       |

### 避けるべきこと

| 禁止事項         | 問題点               |
| ---------------- | -------------------- |
| 目的のない抽出   | 依存が増える         |
| 巨大なフック     | 保守性が落ちる       |
| 副作用の隠蔽     | 予期しない挙動になる |
| テストなしの導入 | 品質劣化の原因になる |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                            | 機能                         |
| ------------------------------------- | ---------------------------- |
| `scripts/analyze-hook-candidates.mjs` | 抽出候補の分析               |
| `scripts/validate-skill.mjs`          | スキル構造の検証             |
| `scripts/log_usage.mjs`               | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース     | パス                                                                     | 読込条件   |
| ------------ | ------------------------------------------------------------------------ | ---------- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)               | 初回整理時 |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md)   | 設計時     |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)           | 実装時     |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)               | 検証時     |
| 抽出基準     | [references/extraction-criteria.md](references/extraction-criteria.md)   | Phase 1    |
| 設計パターン | [references/design-patterns.md](references/design-patterns.md)           | Phase 2    |
| 合成パターン | [references/composition-patterns.md](references/composition-patterns.md) | Phase 2    |
| テスト戦略   | [references/testing-strategies.md](references/testing-strategies.md)     | Phase 4    |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)     | 仕様確認時 |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)                 | 互換確認時 |

### assets/（テンプレート・素材）

| アセット                               | 用途                                                        |
| -------------------------------------- | ----------------------------------------------------------- |
| `assets/basic-hooks-template.md`       | 基本フックテンプレート（インデックス）                      |
| `assets/basic-state-hooks.md`          | 状態管理フック（useToggle, useCounter, useInput）           |
| `assets/side-effect-hooks.md`          | 副作用フック（useDebounce, useInterval, useTimeout）        |
| `assets/event-hooks.md`                | イベントフック（useEventListener, useClickOutside）         |
| `assets/browser-api-hooks.md`          | ブラウザAPIフック（useLocalStorage, useMediaQuery）         |
| `assets/utility-hooks.md`              | ユーティリティフック（usePrevious, useMounted）             |
| `assets/advanced-hooks-template.md`    | 高度フックテンプレート（インデックス）                      |
| `assets/data-fetch-hooks.md`           | データフェッチフック（useFetch, useAsync）                  |
| `assets/form-hooks.md`                 | フォームフック（useForm）                                   |
| `assets/advanced-state-hooks.md`       | 高度状態管理フック（useReducerWithMiddleware, useUndoRedo） |
| `assets/websocket-hooks.md`            | WebSocketフック（useWebSocket）                             |
| `assets/hook-review-checklist.md`      | レビュー観点チェック                                        |
| `assets/hook-api-contract-template.md` | API設計テンプレート                                         |

### 運用ファイル

| ファイル     | 目的                       |
| ------------ | -------------------------- |
| `EVALS.json` | レベル評価・メトリクス管理 |
| `LOGS.md`    | 実行ログの蓄積             |

## 変更履歴

| Version | Date       | Changes                                            |
| ------- | ---------- | -------------------------------------------------- |
| 1.2.0   | 2026-01-06 | assets分割（500行制限対応）、9カテゴリファイル作成 |
| 1.1.0   | 2026-01-06 | extraction-criteria.md実装事例追加                 |
| 1.0.0   | 2026-01-01 | 初版作成                                           |
