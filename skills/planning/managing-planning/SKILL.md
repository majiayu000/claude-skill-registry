---
name: managing-planning
description: >
  プランニングワークフローパターン: SOW生成、Spec作成、Q&A明確化、検証。
  実装前の構造化されたプランニングのためのテンプレートとプロセスを提供。
  Triggers: SOW, Spec, planning, validation, acceptance criteria, requirements, /think, /sow, /spec.
allowed-tools: Read, Write, Grep, Glob, Task
user-invocable: false
---

# プランニングワークフロー管理

SOW、Spec、検証プロセスのためのプランニングワークフローパターン。

## 目的

個別コマンドに埋め込まれていたプランニングワークフローパターンを一元化。
コマンドは薄いオーケストレーターとなり、プランニングロジックはこのスキルを参照。

## ワークフロー参照

| ワークフロー              | 参照                                                                        | コマンド  |
| ------------------------- | --------------------------------------------------------------------------- | --------- |
| SOW生成                   | [@./references/sow-generation.md](./references/sow-generation.md)           | /sow      |
| Spec生成                  | [@./references/spec-generation.md](./references/spec-generation.md)         | /spec     |
| Thinkオーケストレーション | [@./references/think-workflow.md](./references/think-workflow.md)           | /think    |
| 検証                      | [@./references/validation-criteria.md](./references/validation-criteria.md) | /validate |

## クイックリファレンス

### プランニングフロー

```text
/research → /think → /code → /test → /audit → /validate
    │          │
    │          ├── Q&A明確化
    │          ├── SOW生成
    │          └── Spec生成
    │
    └── 調査のみ（実装なし）
```

### SOW構造

| セクション             | 目的                     |
| ---------------------- | ------------------------ |
| エグゼクティブサマリー | 1-2文の概要              |
| 問題分析               | 現状、課題               |
| 前提条件               | 事実、仮定、未知         |
| ソリューション設計     | アプローチ、代替案       |
| 受け入れ基準           | AC-001, AC-002, ...      |
| 実装計画               | フェーズ、進捗マトリクス |
| リスク                 | R-001, R-002, ...        |

### Spec構造

| セクション                 | 目的                         |
| -------------------------- | ---------------------------- |
| 機能要件                   | FR-001, FR-002, ...          |
| データモデル               | TypeScriptインターフェース   |
| 実装                       | フェーズマッピング、コマンド |
| テストシナリオ             | T-001, T-002, ...            |
| 非機能要件                 | NFR-001, NFR-002, ...        |
| トレーサビリティマトリクス | AC → FR → Test → NFR         |

### 信頼度マーカー

| マーカー | 信頼度 | 使用法                    |
| -------- | ------ | ------------------------- |
| [✓]      | ≥95%   | 検証済み（file:line必須） |
| [→]      | 70-94% | 推論（理由を記載）        |
| [?]      | <70%   | 仮説（確認が必要）        |

## テンプレート

### SOWテンプレート

```text
~/.claude/templates/sow/workflow-improvement.md
```

### Specテンプレート

```text
~/.claude/templates/spec/workflow-improvement.md
```

### サマリーテンプレート

```text
~/.claude/templates/summary/review-summary.md
```

## 参照

### 原則 (rules/)

- [@../../rules/core/PRE_TASK_CHECK_RULES.md](../../rules/core/PRE_TASK_CHECK_RULES.md) - 理解度チェック

### 関連スキル

- `orchestrating-workflows` - 実装ワークフロー

### 使用コマンド

- `/think` - 完全なプランニングオーケストレーション
- `/sow` - SOW生成
- `/spec` - Spec生成
- `/validate` - SOW検証
- `/plans` - プランニングドキュメント一覧
