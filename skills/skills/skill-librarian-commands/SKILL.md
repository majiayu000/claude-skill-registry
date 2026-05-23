---
name: skill-librarian-commands
description: |
  スキルライブラリの管理、検索、一覧表示、構造検証を行うコマンド群を提供するスキル。
  スキルの発見、品質検証、使用状況の記録を効率化し、スキルエコシステムの健全性を維持する。

  Anchors:
  • The Pragmatic Programmer (Hunt & Thomas) / 適用: 自動化・ツール設計 / 目的: 効率的なスキル管理
  • 18-skills.md / 適用: スキル構造・検証基準 / 目的: 品質基準の担保
  • Unix Philosophy / 適用: 小さなツールの組み合わせ / 目的: 柔軟なコマンド設計

  Trigger:
  Use when listing skills, validating skill structure, searching for skills, or managing skill metadata.
  skill list, skill search, skill validation, skill management, librarian commands
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Skill Librarian Commands

## 概要

スキルライブラリの管理・検索・検証を行うコマンド群を提供するスキル。
スキルの発見性向上、品質維持、使用状況追跡をサポートする。

---

## ワークフロー

```
list-skills → search-skills → validate-skill → record-usage
```

### Task 1: スキル一覧（list-skills）

利用可能なスキルの一覧を表示する。

**Task**: `agents/list-skills.md` を参照

### Task 2: スキル検索（search-skills）

キーワードや条件でスキルを検索する。

**Task**: `agents/search-skills.md` を参照

### Task 3: スキル検証（validate-skill）

スキルの構造が18-skills.md仕様に準拠しているか検証する。

**Task**: `agents/validate-skill.md` を参照

### Task 4: 使用記録（record-usage）

スキルの使用状況を記録する。

**Task**: `agents/record-usage.md` を参照

---

## Task仕様（ナビゲーション）

| Task           | 責務           | 入力              | 出力             |
| -------------- | -------------- | ----------------- | ---------------- |
| list-skills    | スキル一覧表示 | なし/フィルタ条件 | スキル一覧       |
| search-skills  | スキル検索     | 検索キーワード    | 該当スキルリスト |
| validate-skill | 構造検証       | スキルパス        | 検証レポート     |
| record-usage   | 使用記録       | スキル名・結果    | LOGS.md更新      |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照
**注記**: 1 Task = 1 責務。必要なコマンドのみ実行する。

---

## コマンドリファレンス

### スキル一覧表示

```bash
node .claude/skills/skill-librarian-commands/scripts/list-skills.mjs
node .claude/skills/skill-librarian-commands/scripts/list-skills.mjs --format table
node .claude/skills/skill-librarian-commands/scripts/list-skills.mjs --filter "database"
```

### スキル検証

```bash
node .claude/skills/skill-librarian-commands/scripts/validate-skill.mjs .claude/skills/<skill-name>
node .claude/skills/skill-librarian-commands/scripts/validate-skill.mjs .claude/skills/<skill-name> --verbose
```

### 使用記録

```bash
node .claude/skills/skill-librarian-commands/scripts/log_usage.mjs --skill <skill-name> --result success
node .claude/skills/skill-librarian-commands/scripts/log_usage.mjs --skill <skill-name> --result failure --reason "エラー詳細"
```

---

## ベストプラクティス

### すべきこと

| 推奨事項                             | 理由                       |
| ------------------------------------ | -------------------------- |
| 新規スキル作成後は必ず検証を実行する | 品質基準の担保             |
| スキル使用後は使用記録を残す         | フィードバックループの維持 |
| 定期的にスキル一覧を確認する         | 重複スキルの発見           |
| 検索機能で類似スキルを確認する       | 再発明の防止               |

### 避けるべきこと

| 禁止事項                   | 問題点                 |
| -------------------------- | ---------------------- |
| 検証なしでスキルを公開する | 品質基準違反のリスク   |
| 使用記録を残さない         | 改善のためのデータ不足 |
| スキル名の重複を放置する   | 発見性の低下           |

---

## リソース参照

### scripts/（決定論的処理）

| スクリプト           | 用途           | 使用例                                               |
| -------------------- | -------------- | ---------------------------------------------------- |
| `list-skills.mjs`    | スキル一覧表示 | `node scripts/list-skills.mjs --format table`        |
| `validate-skill.mjs` | 構造検証       | `node scripts/validate-skill.mjs .claude/skills/xxx` |
| `log_usage.mjs`      | 使用記録       | `node scripts/log_usage.mjs --skill xxx --result ok` |

### references/（詳細知識）

| リソース         | パス                                                                       | 読込条件                       |
| ---------------- | -------------------------------------------------------------------------- | ------------------------------ |
| コマンド詳細     | [references/command-reference.md](references/command-reference.md)         | コマンドオプション詳細が必要時 |
| スキル構造ガイド | [references/skill-structure-guide.md](references/skill-structure-guide.md) | 検証基準の詳細が必要時         |

### assets/（テンプレート）

| アセット                      | 用途                             |
| ----------------------------- | -------------------------------- |
| `assets/resource-template.md` | リソースファイル作成テンプレート |

---

## 変更履歴

| Version | Date       | Changes                        |
| ------- | ---------- | ------------------------------ |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様準拠で全面改訂 |
| 1.0.0   | 2025-12-24 | 初版作成                       |
