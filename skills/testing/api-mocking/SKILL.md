---
name: api-mocking
description: |
  E2EテストおよびユニットテストにおけるAPIモック技術スキル。外部API依存を排除し、テストの安定性・速度・信頼性を向上させるための手法とベストプラクティスを提供します。

  📖 参考資料:
  • 『RESTful Web APIs』（Leonard Richardson）/ 適用: APIレスポンスのモック化 / 目的: 外部API依存を排除し、テストの安定性と速度を向上させる
  • 『Mock Service Worker』（Artem Zakharchenko）/ 適用: ネットワークリクエストのインターセプト / 目的: 複雑なAPI統合シナリオでのテスト精度向上
  • 『Testing JavaScript』（Kent C. Dodds）/ 適用: エラーケース（4xx、5xx）のテスト / 目的: エラーハンドリングの包括的な検証

  外部APIへのテスト依存を排除したい時、エラーケースをテストしたい時、ネットワーク遅延をシミュレートしたい時、MSWによるHTTPインターセプトを実装したい時に使用します。

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# APIモック技術スキル

## 概要

E2EテストおよびユニットテストにおけるAPI モック技術の包括的なガイダンス。外部API依存を排除し、テストの安定性・速度・信頼性を向上させるための手法とベストプラクティスを提供します。

詳細な実装手順は以下のレベル別リソースを参照してください：

- **レベル1**: 基礎知識と用語理解
- **レベル2**: MSW統合と基本的なハンドラー実装
- **レベル3**: 高度なシナリオと動的レスポンス
- **レベル4**: パフォーマンス最適化と複雑なシナリオ

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの性質と要件を明確化する

**アクション**:

1. `references/Level1_basics.md` でAPIモックの基礎概念を確認
2. `references/mock-patterns.md` で実装パターンを確認
3. テスト対象のAPI仕様（エンドポイント、レスポンス形式）を整理
4. モック化の範囲（全API、特定エンドポイント、エラーケースなど）を定義

**Task**: `agents/analyze-mocking-context.md` を参照

### Phase 2: スキル適用と実装

**目的**: 要件に基づいてAPIモックを実装する

**アクション**:

1. `references/msw-integration-guide.md` を参照して環境設定
2. `assets/mock-handler-template.ts` を使用してハンドラーを作成
3. エラーケース（4xx、5xx）のレスポンスをモック化
4. ネットワーク遅延をシミュレート（必要な場合）
5. `references/Level2_intermediate.md` の実装チェックリストを確認

**Task**: `agents/implement-mock.md` を参照

### Phase 3: 検証と最適化

**目的**: 実装の品質を確保し、記録を残す

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を検証
2. モックされたテストが期待通りに動作するか確認
3. パフォーマンスへの影響を測定（必要な場合）
4. `scripts/log_usage.mjs` で使用履歴を記録
5. `references/Level3_advanced.md` で最適化の余地を確認

**Task**: `agents/validate-mock.md` を参照

## Task仕様ナビ

| タスク                           | 対象レベル | 主要リソース                             | スクリプト                   | テンプレート               |
| -------------------------------- | ---------- | ---------------------------------------- | ---------------------------- | -------------------------- |
| MSW基本セットアップ              | L1-L2      | `msw-integration-guide.md`               | -                            | `mock-handler-template.ts` |
| GETリクエストのモック化          | L1-L2      | `mock-patterns.md`                       | `generate-mock-handlers.mjs` | `mock-handler-template.ts` |
| POSTリクエストのモック化         | L2         | `mock-patterns.md`                       | `generate-mock-handlers.mjs` | `mock-handler-template.ts` |
| エラーレスポンスのモック         | L2-L3      | `Level2_intermediate.md`                 | -                            | `mock-handler-template.ts` |
| 動的レスポンスの実装             | L3         | `Level3_advanced.md`                     | -                            | -                          |
| ネットワーク遅延シミュレーション | L2-L3      | `mock-patterns.md`                       | -                            | `mock-handler-template.ts` |
| Playwright統合                   | L2-L3      | `msw-integration-guide.md`               | -                            | -                          |
| パフォーマンス最適化             | L3-L4      | `Level3_advanced.md`, `Level4_expert.md` | `validate-skill.mjs`         | -                          |

## ベストプラクティス

### すべきこと ✓

- **外部API依存の排除**: テスト環境では常に外部APIをモック化する
- **エラーケースの包括的なテスト**: 4xx、5xx、タイムアウト、ネットワークエラーを含める
- **レスポンス形式の正確性**: 実API仕様に基づいて正確なレスポンスを作成
- **ネットワーク遅延の現実的なシミュレーション**: 実際のネットワーク遅延を模擬する
- **モックの再利用性**: 複数のテストで使用可能な汎用モックハンドラーを設計
- **段階的な詳細化**: Level1から段階的により複雑なシナリオへ進める
- **スクリプト活用**: `generate-mock-handlers.mjs` で自動生成を検討
- **レベル別ガイドの確認**: タスク複雑度に応じて適切なレベルのリソースを参照

### 避けるべきこと ✗

- **テストでの実API呼び出し**: モック化せずに実APIに依存するテストは作成しない
- **ハードコードされた動的値**: タイムスタンプやIDは動的に生成する
- **不完全なモック**: APIの全エンドポイントをモック化しないまま進める
- **レスポンス形式の不一致**: ドキュメントと異なるレスポンス形式を使用しない
- **モックの過度なカスタマイズ**: テスト毎に異なるモックを作成するのではなく、再利用可能にする
- **エラーハンドリングの軽視**: 正常系のみモック化し、エラー系をテストしない
- **ドキュメント更新の遺漏**: モック仕様変更時にドキュメントを更新しない

## リソース参照

### ドキュメント

| リソース                              | 説明                                             | 対象レベル |
| ------------------------------------- | ------------------------------------------------ | ---------- |
| `references/Level1_basics.md`         | APIモック技術の基礎概念、用語、全体像            | L1         |
| `references/Level2_intermediate.md`   | MSW統合、基本ハンドラー実装、実践的パターン      | L2         |
| `references/Level3_advanced.md`       | 高度なシナリオ、動的レスポンス、最適化           | L3         |
| `references/Level4_expert.md`         | パフォーマンス最適化、複雑な統合、アーキテクチャ | L4         |
| `references/mock-patterns.md`         | 一般的なモックパターンとアンチパターン           | L2-L4      |
| `references/msw-integration-guide.md` | Mock Service Workerの統合ガイド                  | L2-L3      |
| `references/legacy-skill.md`          | 旧バージョンの完全なドキュメント                 | 参考       |

### スクリプト

```bash
# MSWモックハンドラーの自動生成
node .claude/skills/api-mocking/scripts/generate-mock-handlers.mjs --help

# 使用履歴の記録と自動評価
node .claude/skills/api-mocking/scripts/log_usage.mjs --help

# スキル構造の検証
node .claude/skills/api-mocking/scripts/validate-skill.mjs --help
```

### テンプレート

```bash
# MSWモックハンドラーテンプレート
cat .claude/skills/api-mocking/assets/mock-handler-template.ts
```

## 変更履歴

| Version | Date       | Changes                                                                            |
| ------- | ---------- | ---------------------------------------------------------------------------------- |
| 2.0.0   | 2025-12-31 | agents/3ファイル追加、Phase別Task参照を追加                                        |
| 1.0.0   | 2025-12-31 | 18-skills.md仕様への準拠、Anchors/Trigger追加、Task仕様ナビ統合、allowed-tools定義 |
