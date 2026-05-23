---
name: optimistic-updates
description: |
  楽観的更新（Optimistic Updates）パターンの実装スキル。サーバーレスポンス前にUIを即座更新し、失敗時のロールバック機構を提供することで、レスポンシブなユーザー体験を実現します。

  Anchors:
  • Designing Data-Intensive Applications (Martin Kleppmann) / 適用: 分散システムにおける楽観的並行制御 / 目的: 競合検出とロールバック戦略の設計
  • React Query (TanStack) / 適用: onMutate/onError/onSettledフック / 目的: 楽観的更新とロールバックの自動化
  • SWR Documentation (Vercel) / 適用: optimisticDataとrollbackOnError / 目的: 宣言的な楽観的更新の実装

  Trigger:
  Use when implementing instant UI feedback before server response, hiding CRUD latency, implementing optimistic updates with React Query/SWR, designing rollback strategies, or handling conflict states.
  optimistic update, UI feedback, rollback, React Query, SWR, mutation, conflict resolution

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 楽観的更新パターンスキル

## 概要

楽観的更新（Optimistic Updates）は、サーバーからの応答を待たずにUIを即座に更新するパターンです。ユーザー体験を大幅に向上させますが、失敗時の適切なロールバック処理と競合制御が必要です。

本スキルは、React Query、SWR、その他の状態管理ライブラリを使用した楽観的更新の実装、エラーハンドリング、テスト戦略を包括的にカバーします。

詳細な実装手順は `references/basics.md` を参照してください。

## ワークフロー

### Phase 1: 要件分析と設計

**目的**: 楽観的更新の適用可否を判断し、設計方針を決定する

**アクション**:

1. `references/basics.md` で楽観的更新の基礎概念を確認
2. 対象操作の成功率、重要度、可逆性を評価
3. ロールバック戦略（即座 vs 遅延、完全 vs 部分）を決定
4. 競合制御の必要性を判定

**Task**: `agents/analyze-requirements.md` を参照

**判断ポイント**:

- 成功率が99%以上？ → 楽観的更新適用候補
- 金融トランザクションや不可逆操作？ → 楽観的更新は避ける
- 複数ユーザーの同時編集？ → 競合制御が必須

### Phase 2: 実装

**目的**: 要件に基づいて楽観的更新を実装する

**アクション**:

1. `references/basics.md` で実装パターンを確認
2. React Query/SWRのフックを使用して楽観的更新を実装
3. エラーハンドリングとロールバック機構を実装
4. 競合制御を実装（必要な場合）

**Task**: `agents/implement-optimistic-update.md` を参照

### Phase 3: テストと検証

**目的**: 実装の品質を確保し、エッジケースをカバーする

**アクション**:

1. 正常系のテスト実装（即座更新、サーバー確認）
2. 異常系のテスト実装（ロールバック、エラー通知）
3. 競合状態のテスト（複数ミューテーション同時実行）

**Task**: `agents/validate-and-test.md` を参照

## Task仕様（ナビゲーション）

| Task                        | 起動タイミング | 入力           | 出力             |
| --------------------------- | -------------- | -------------- | ---------------- |
| analyze-requirements        | Phase 1開始時  | 対象操作仕様   | 適用可否レポート |
| implement-optimistic-update | Phase 2開始時  | 設計方針       | 実装済みコード   |
| validate-and-test           | Phase 3開始時  | 実装済みコード | 検証済みシステム |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと ✓

- **適用基準の遵守**: 成功率99%以上、可逆性のある操作にのみ適用
- **完全なロールバック**: 失敗時は完全に元の状態に戻す
- **明確なフィードバック**: 成功、失敗、ロールバックを明確にユーザーに通知
- **競合状態の考慮**: 複数ミューテーションの同時実行をキャンセル/制御
- **段階的な詳細化**: Level1から段階的により複雑なシナリオへ
- **一貫性の維持**: サーバーの真実（Source of Truth）との同期を確保
- **エラーログの記録**: 失敗時のコンテキストとスタックトレースを記録
- **テストの包括性**: 正常系、異常系、競合状態をすべてカバー

### 避けるべきこと ✗

- **重要トランザクションへの適用**: 金融、医療、法的な重要操作には使用しない
- **不可逆操作への適用**: 削除、課金、送信など取り消せない操作は慎重に
- **不完全なロールバック**: 部分的なロールバックで矛盾状態を作らない
- **エラーの無視**: ロールバック失敗時のフォールバック処理を省略しない
- **過度な楽観性**: 成功率が低い（<95%）操作には適用しない
- **競合制御の省略**: 複数ユーザー環境で競合検出を実装しない
- **テストの不足**: ロールバックやエラーケースのテストを省略しない
- **フィードバックの欠如**: ユーザーに状態変化を通知しない

## リソース参照

### references/（詳細知識）

| リソース | パス                                             | 用途           |
| -------- | ------------------------------------------------ | -------------- |
| 基礎知識 | See [references/basics.md](references/basics.md) | 概念とパターン |

### agents/（Task仕様）

| Task                        | 用途             |
| --------------------------- | ---------------- |
| analyze-requirements        | 適用可否判断     |
| implement-optimistic-update | 楽観的更新の実装 |
| validate-and-test           | テストと検証     |

### assets/（テンプレート）

| テンプレート | パス                                        | 用途              |
| ------------ | ------------------------------------------- | ----------------- |
| React Query  | `assets/react-query-optimistic-template.ts` | React Query実装例 |
| SWR          | `assets/swr-optimistic-template.ts`         | SWR実装例         |

### scripts/（決定論的処理）

| スクリプト | パス                                     | 用途               |
| ---------- | ---------------------------------------- | ------------------ |
| 実装検証   | `scripts/validate-optimistic-update.mjs` | パターン検証       |
| 使用記録   | `scripts/log_usage.mjs`                  | フィードバック記録 |

## 変更履歴

| Version | Date       | Changes                              |
| ------- | ---------- | ------------------------------------ |
| 1.2.0   | 2026-01-02 | assets/scripts追加、リソース参照完備 |
| 1.1.0   | 2026-01-02 | description形式更新、basics.md追加   |
| 1.0.0   | 2025-12-31 | 初期実装                             |
