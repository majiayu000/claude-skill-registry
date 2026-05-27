---
name: creating-adrs
description: >
  Structured ADR creation in MADR format. Triggers: ADR, Architecture Decision,
  決定記録, 技術選定, アーキテクチャ決定, design decision, 技術的決定, 設計判断,
  deprecation, 非推奨化, process change, プロセス変更
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, Task]
---

# ADRクリエーター

## 6フェーズプロセス

| フェーズ        | アクション                                                                 |
| --------------- | -------------------------------------------------------------------------- |
| 1. 事前チェック | `ls adr/*.md`、重複チェック、次の番号を取得                                |
| 2. テンプレート | キーワードをテンプレートタイプにマッチ                                     |
| 3. 参照         | プロジェクトドキュメント、Issue、外部リソースを収集                        |
| 4. 検証         | 必須セクションをチェック（Title、Status、Context、Decision、Consequences） |
| 5. インデックス | `adr/README.md`を自動生成                                                  |
| 6. リカバリー   | 欠落ディレクトリ、重複、欠落セクションを処理                               |

## テンプレート選択

| テンプレート         | ユースケース             | 必須セクション                   |
| -------------------- | ------------------------ | -------------------------------- |
| technology-selection | ライブラリ、FW選択       | オプション（最低3つ）、Pros/Cons |
| architecture-pattern | 構造、設計ポリシー       | コンテキスト、結果               |
| process-change       | ワークフロー、ルール変更 | Before/After比較                 |
| deprecation          | 技術の廃止               | 移行計画、タイムライン           |

## ディレクトリ構造

```text
adr/
├── README.md          # 自動生成インデックス
├── 0001-*.md         # 連番
└── 0002-*.md
```

## 参照

| トピック     | リソース                      |
| ------------ | ---------------------------   |
| MADR         | <https://adr.github.io/madr/> |
| コマンド     | `../../commands/adr.md`       |
| テンプレート | `../../templates/adr/`        |
| スクリプト   | `./scripts/`                  |
