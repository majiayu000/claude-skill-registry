---
name: output-formatting
description: |
  様々な形式での出力フォーマッティングスキル。Markdown、JSON、YAML、表形式など、
  構造化された見やすい出力を作成します。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: コード品質と可読性 / 目的: 読みやすく保守可能な出力設計
  • Technical Writing (Google Developer Documentation Style Guide) / 適用: ドキュメント構造 / 目的: 明確で一貫性のある技術文書フォーマット

  Trigger:
  Use when formatting output, creating structured documents, generating tables, or converting between formats.
  output format, markdown, json, yaml, table, document structure, formatting, presentation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# output-formatting

## 概要

様々な形式での出力フォーマッティングスキル。
Markdown、JSON、YAML、表形式など、構造化された見やすい出力を作成する。

---

## ワークフロー

### Phase 1: 要件分析

**目的**: 出力形式と要件を明確化

**アクション**:

1. 出力先のコンテキスト（ファイル/レポート/API）を確認
2. 必要な形式（Markdown/JSON/YAML/Table）を特定
3. 対象読者とユースケースを整理
4. `references/basics.md` で基礎概念を確認

**Task**: `agents/analyze-format-requirements.md` を参照

### Phase 2: フォーマット設計

**目的**: 適切なフォーマット構造を設計

**アクション**:

1. `references/` で形式別のベストプラクティスを確認
2. `assets/` から適切なテンプレートを選択
3. データ構造とフォーマットのマッピングを設計
4. 可読性と保守性を考慮した構造を決定

**Task**: `agents/design-format-structure.md` を参照

### Phase 3: 出力生成と検証

**目的**: フォーマット済み出力を生成し品質を検証

**アクション**:

1. 設計に基づいて出力を生成
2. `scripts/validate-format.mjs` でフォーマット検証
3. 可読性と一貫性を確認
4. `scripts/log_usage.mjs` で使用記録を保存

**Task**: `agents/generate-and-validate.md` を参照

---

## Task仕様（ナビゲーション）

| Task                        | 起動タイミング | 入力                    | 出力                 |
| --------------------------- | -------------- | ----------------------- | -------------------- |
| analyze-format-requirements | Phase 1開始時  | 要件・コンテキスト情報  | フォーマット要件     |
| design-format-structure     | Phase 2開始時  | フォーマット要件        | フォーマット設計     |
| generate-and-validate       | Phase 3開始時  | フォーマット設計+データ | フォーマット済み出力 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

---

## ベストプラクティス

### すべきこと

| 推奨事項                 | 理由                                   |
| ------------------------ | -------------------------------------- |
| 一貫性のある構造         | 読者が理解しやすく予測可能             |
| 適切なインデントと空白   | 視覚的な階層を明確化                   |
| 形式に応じた命名規則     | JSON: camelCase、YAML: snake_case など |
| セマンティックな構造     | 意味を持つ階層とラベル                 |
| バリデーション可能な形式 | スキーマやルールで検証可能             |

### 避けるべきこと

| 禁止事項                 | 問題点                       |
| ------------------------ | ---------------------------- |
| 過度に深いネスト         | 可読性低下、メンテナンス困難 |
| 不統一な命名規則         | 混乱を招く                   |
| 冗長な情報の重複         | 保守コスト増加               |
| 形式に適さない構造       | パーサーエラー、処理困難     |
| コメントなしの複雑な構造 | 理解困難、ドキュメント不足   |

---

## リソース参照

### references/（詳細知識）

| リソース | パス                                             | 用途       |
| -------- | ------------------------------------------------ | ---------- |
| 基礎知識 | See [references/basics.md](references/basics.md) | 形式と選択 |

### agents/（Task仕様）

| Task                        | 用途                 |
| --------------------------- | -------------------- |
| analyze-format-requirements | フォーマット要件分析 |
| design-format-structure     | 構造設計             |
| generate-and-validate       | 生成と検証           |

### assets/（テンプレート）

| テンプレート     | パス                                 | 用途         |
| ---------------- | ------------------------------------ | ------------ |
| Markdownレポート | `assets/markdown-report-template.md` | レポート作成 |
| JSONスキーマ     | `assets/json-schema-template.json`   | スキーマ定義 |
| YAML設定         | `assets/yaml-config-template.yaml`   | 設定ファイル |

### scripts/（決定論的処理）

| スクリプト       | パス                          | 用途               |
| ---------------- | ----------------------------- | ------------------ |
| フォーマット検証 | `scripts/validate-format.mjs` | JSON/YAML/MD検証   |
| 使用記録         | `scripts/log_usage.mjs`       | フィードバック記録 |

---

## 変更履歴

| Version | Date       | Changes                              |
| ------- | ---------- | ------------------------------------ |
| 1.2.0   | 2026-01-02 | assets/scripts追加、リソース参照完備 |
| 1.1.0   | 2026-01-02 | リソース参照更新、basics.md作成      |
| 1.0.0   | 2025-12-31 | 18-skills.md完全準拠版。初回作成     |
