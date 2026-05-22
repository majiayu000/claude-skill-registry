---
name: managing-documentation
description: >
  ドキュメント生成ワークフロー：ADR作成、スキル生成、ルール生成。
  技術ドキュメントのためのテンプレートとプロセスを提供。
  トリガー: ADR, documentation, architecture decision, rulify, skill generation, MADR。
allowed-tools: Read, Write, Grep, Glob, Edit
user-invocable: false
---

# ドキュメント管理

ADR、スキル、ルールのドキュメント生成ワークフロー。

## 目的

個々のコマンドに埋め込まれていたドキュメントワークフローパターンを集約。
コマンドはドキュメントロジックのためにこのスキルを参照する薄いオーケストレーターとなる。

## ワークフローリファレンス

| ワークフロー | リファレンス                                                                                                                            | コマンド |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| ADR作成      | [@../../skills/managing-documentation/references/adr-workflow.md](../../skills/managing-documentation/references/adr-workflow.md)       | /adr     |
| Rulify       | [@../../skills/managing-documentation/references/rulify-workflow.md](../../skills/managing-documentation/references/rulify-workflow.md) | /rulify  |

## クイックリファレンス

### ADR (Architecture Decision Record)

MADRフォーマット (Markdown Any Decision Record):

```markdown
# ADR-NNNN: [タイトル]

## Status

Proposed | Accepted | Deprecated | Superseded

## Context

[課題は何か？]

## Decision

[決定は何か？]

## Consequences

[結果は何か？]
```

### ADR番号付け

```text
場所: ~/.claude/adr/
フォーマット: ADR-NNNN-title.md
次の番号: 既存ファイルから自動検出
```

### Rulifyフロー

```text
ADR (決定) → Rule (強制) → CLAUDE.md (統合)

1. ADRの内容を読み込み
2. 強制可能なルールを抽出
3. rules/にルールファイルを生成
4. CLAUDE.mdの参照を更新
```

### ドキュメントガイドライン

| 原則            | 適用                   |
| --------------- | ---------------------- |
| 明確性 > 完全性 | オッカムの剃刀を適用   |
| EN/JP同期       | 両バージョンは一致必須 |
| 循環参照禁止    | 最大3レベル深さ        |
| Mermaid > ASCII | Mermaid図を使用        |

## テンプレート

### ADRテンプレート

```text
~/.claude/templates/adr/madr-template.md
```

### ルールテンプレート

```text
~/.claude/templates/rules/rule-template.md
```

## 参照

### 原則 (rules/)

- [@../../rules/conventions/DOCUMENTATION.md](../../rules/conventions/DOCUMENTATION.md) - ドキュメントガイドライン
- [@../../rules/conventions/TRANSLATION.md](../../rules/conventions/TRANSLATION.md) - 翻訳ルール

### 関連スキル

- `creating-adrs` - ADR作成の基本

### 使用元コマンド

- `/adr` - ADR作成
- `/rulify` - ADRからルール生成
