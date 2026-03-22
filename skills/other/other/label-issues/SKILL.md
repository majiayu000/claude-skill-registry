---
name: label-issues
description: ラベル未付与の GitHub Issue に種別・優先度ラベルを付与する。「ラベルがついてない Issue にラベルをつけて」「Issue のラベル整理して」のようなリクエストで使う。
context: fork
agent: general-purpose
allowed-tools: Bash(gh issue list:*), Bash(gh issue edit:*)
---

# Label Issues Skill

ラベルが付与されていない既存の Open Issue を特定し、適切なラベルを付与する。

## 前提条件

- `gh` CLI が認証済みであること

## 手順

### 1. ラベル未付与 Issue の特定

```bash
gh issue list --state open --json number,title,labels,body --limit 100 --jq '.[] | select(.labels | length == 0)'
```

Dependency Dashboard（Renovate）など自動管理されている Issue は対象外とする。

### 2. ラベルの判定と付与

Issue のタイトルと本文を読み、以下のルールに基づいて適切なラベルを判定する。

**種別ラベル（必須・1つ選択）:**

| 内容の種別 | ラベル |
|-----------|--------|
| バグ報告・不具合修正 | `Type: Bug` |
| 新しい機能の追加 | `Type: Feature` |
| 既存機能の改善・拡張 | `Type: Enhancement` |
| コードの整理・改善 | `Type: Refactoring` |
| テストの追加・改善 | `Type: Test` |
| ドキュメントの追加・改善 | `Type: Document` |
| リリース作業 | `Type: Publishing` |

**優先度ラベル（必須・1つ選択）:**

| 優先度 | ラベル | 基準 |
|--------|--------|------|
| 高 | `Priority: High` | ユーザーに直接影響する、またはバグの温床となりうる |
| 中 | `Priority: Medium` | 品質向上に寄与するが、緊急性は低い |
| 低 | `Priority: Low` | あると良いが、なくても問題ない |

**その他のラベル（任意）:**

Issue の内容に応じて、`Close: Duplicate` や `Close: WontFix` などの既存ラベルが適切な場合は付与する。

### 3. ラベルの付与

```bash
gh issue edit <issue-number> --add-label "<ラベル1>,<ラベル2>"
```

### 4. 結果の報告

ラベルを付与した Issue の一覧を以下の形式で報告する:

| # | タイトル | 付与したラベル |
|---|---------|--------------|
| #XX | <タイトル> | <付与したラベル> |

対象がない場合は「ラベル未付与の Issue はありませんでした」と報告する。

## 注意事項

- 既にラベルが付いている Issue のラベルは変更しない（この手順はラベル未付与の Issue のみが対象）
- 判断に迷う場合は `Type: Enhancement` + `Priority: Medium` をデフォルトとする
- ラベルがリポジトリに存在しない場合は付与せず、その旨を報告する（ラベルは別リポジトリで Terraform 管理されている）
