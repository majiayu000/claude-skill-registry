---
name: zod-validation
description: |
  Zodライブラリによるランタイムバリデーション、スキーマ定義、TypeScript型推論を専門とするスキル。
  型安全なバリデーションロジックを設計・実装し、API・フォーム・ドメイン層での検証を網羅する。

  Anchors:
  • Zod Official Documentation / 適用: スキーマAPI・バリデーション / 目的: 公式パターン準拠
  • Effective TypeScript (Dan Vanderkam) / 適用: 型設計・型推論 / 目的: ランタイム安全性担保
  • @hookform/resolvers / 適用: フォーム統合 / 目的: React Hook Form連携

  Trigger:
  Use when implementing runtime validation with Zod, defining TypeScript schemas, integrating form validation (react-hook-form), or validating API requests/responses. Keywords: zod, schema, safeParse, refine, z.infer, zodResolver.
allowed-tools:
  - Bash
  - Edit
  - Glob
  - Grep
  - Read
  - Write
  - Task
---

# Zod Validation

## 概要

Zodライブラリによるランタイムバリデーションとスキーマ定義を専門とするスキル。
TypeScriptの型推論と組み合わせて、コンパイル時とランタイムの両方で型安全性を確保する。

## ワークフロー

### Phase 1: スキーマ設計

**目的**: データ構造からZodスキーマを設計する

**アクション**:

1. バリデーション対象のデータ構造を分析
2. TypeScript型からZodスキーマへマッピング
3. 制約（min/max/regex/refine）を追加
4. 再利用可能なスキーマパターンを適用
5. `z.infer<typeof schema>` で型推論を確認

**Task**: `agents/schema-designer.md` を参照

### Phase 2: バリデーション実装

**目的**: 設計したスキーマでバリデーションロジックを実装する

**アクション**:

1. parse/safeParseの適切な選択
2. エラーハンドリングの実装
3. カスタムバリデーション（refine/superRefine）の実装
4. エラーメッセージのフォーマット

**Task**: `agents/validation-implementer.md` を参照

### Phase 3: 統合

**目的**: フレームワークやAPIにバリデーションを統合する

**アクション**:

- **フォーム統合**: react-hook-form + zodResolver
- **API統合**: リクエスト/レスポンス検証

**Task**: `agents/form-integrator.md` または `agents/api-validator.md` を参照

### Phase 4: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-schema.mjs` でスキーマ構造を確認
2. `scripts/validate-skill.mjs` でスキル構造を確認
3. `scripts/log_usage.mjs` で記録を残す

## Task仕様ナビ

| Task               | リソース                         | 説明                                 |
| ------------------ | -------------------------------- | ------------------------------------ |
| スキーマ設計       | agents/schema-designer.md        | データ構造からZodスキーマを設計      |
| バリデーション実装 | agents/validation-implementer.md | スキーマを使用したバリデーション実装 |
| フォーム統合       | agents/form-integrator.md        | react-hook-form等との統合            |
| API検証            | agents/api-validator.md          | APIリクエスト/レスポンス検証         |

## ベストプラクティス

### すべきこと

- **型推論を活用する**: `z.infer<typeof schema>` を使用して型安全性を確保
- **safeParseを使用する**: ユーザー入力には例外をスローしないsafeParseを使用
- **エラーメッセージをカスタマイズする**: ユーザーフレンドリーなメッセージを定義
- **スキーマを再利用する**: 共通パターンは抽出して再利用（extend, merge, pick, omit）
- **段階的バリデーション**: 複雑なバリデーションはrefine/superRefineで実装
- 詳細は `references/schema-patterns.md` と `references/validation-patterns.md` を参照

### 避けるべきこと

- **parseを直接使用しない**: ユーザー入力にはsafeParseを使用（例外回避）
- **バリデーションロジックを分散させない**: 一箇所にまとめる
- **非同期バリデーションを過度に使用しない**: パフォーマンスへの影響を考慮
- **エラーハンドリングを省略しない**: すべてのバリデーション結果を処理
- **any型を使用しない**: `z.any()` の使用は最小限に

## リソース参照

### agents/（Task仕様書）

| ファイル                         | 説明                           |
| -------------------------------- | ------------------------------ |
| agents/schema-designer.md        | スキーマ設計のTask仕様書       |
| agents/validation-implementer.md | バリデーション実装のTask仕様書 |
| agents/form-integrator.md        | フォーム統合のTask仕様書       |
| agents/api-validator.md          | API検証のTask仕様書            |

### references/（詳細知識）

| ファイル                           | 説明                           |
| ---------------------------------- | ------------------------------ |
| references/schema-patterns.md      | スキーマパターンと実装例       |
| references/validation-patterns.md  | バリデーションパターンと実践例 |
| references/integration-patterns.md | フレームワーク統合パターン     |

### scripts/（検証・ロギング）

| スクリプト            | 説明                  | 使用法                                           |
| --------------------- | --------------------- | ------------------------------------------------ |
| `validate-schema.mjs` | Zodスキーマの構造検証 | `node scripts/validate-schema.mjs <schema-file>` |
| `validate-skill.mjs`  | スキル構造の検証      | `node scripts/validate-skill.mjs`                |
| `log_usage.mjs`       | 使用統計とログ記録    | `node scripts/log_usage.mjs --help`              |

### assets/（テンプレート）

| テンプレート                        | 説明                     | 用途                |
| ----------------------------------- | ------------------------ | ------------------- |
| assets/schema-template.ts           | 基本スキーマテンプレート | 新規スキーマ作成    |
| assets/api-schema-template.ts       | APIスキーマテンプレート  | API検証実装         |
| assets/form-validation-template.tsx | フォーム統合テンプレート | react-hook-form連携 |

## 変更履歴

| Version | Date       | Changes                                                                     |
| ------- | ---------- | --------------------------------------------------------------------------- |
| 4.0.0   | 2026-01-01 | 18-skills.md完全準拠: 4エージェント体制、統合パターン追加、テンプレート拡充 |
| 3.0.0   | 2026-01-01 | 18-skills.md仕様準拠：agents/追加、references/整理、ワークフロー刷新        |
| 2.0.0   | 2025-12-31 | YAML frontmatter最適化、Task仕様ナビ追加                                    |
| 1.0.0   | 2025-12-24 | 初版作成                                                                    |
