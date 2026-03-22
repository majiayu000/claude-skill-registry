---
name: create-issues-from-plans
description: 実装プランの「今後の展望」セクションから新規 GitHub Issue を作成する。プランから Issue を起こしたいとき、展望を Issue 化したいときに使う。「プランから Issue 作って」「今後の展望を Issue にして」のようなリクエストで使う。
context: fork
agent: general-purpose
allowed-tools: Read, Glob, Bash(gh issue list:*), Bash(gh issue create:*), Bash(gh issue edit:*), Bash(gh api:*)
---

# Create Issues from Plans Skill

実装プランの「今後の展望」セクションを読み取り、既存 Issue と重複しないものを新規 Issue として作成する。

## 前提条件

- `gh` CLI が認証済みであること
- `.claude/outputs/plans/` ディレクトリに `PLAN-*.md` ファイルが存在すること

## 手順

### 1. 実装プランの読み込み

`.claude/outputs/plans/` ディレクトリが存在する場合、`PLAN-*.md` ファイルを読み込み、「今後の展望」セクションを抽出する。

ディレクトリやファイルが存在しない場合は、「実装プランが見つかりませんでした」と報告して終了する。

### 2. 既存 Issue との重複チェック

抽出した各展望項目について、既存の Open/Closed Issue と重複していないかを確認する。

```bash
gh issue list --state all --json number,title,body,state --limit 200
```

重複判定の基準:
- Issue のタイトルが同じ、またはほぼ同一の内容を指している
- Issue の本文に同じ機能・改善が記載されている
- 完全一致でなくても、実質的に同じ作業を指している場合は重複とみなす

### 3. 新規 Issue の作成

重複していない展望項目について、Issue を作成する。

プランのファイル名は `PLAN-<Issue番号>-<タイトル>.md` の形式であるため、ファイル名から元の Issue 番号を抽出し、Issue 本文で紐づける。

```bash
gh issue create --title "<タイトル>" --label "<ラベル>" --body "$(cat <<'EOF'
## 概要

<展望項目の内容を具体的に記述>

## 背景

#<元Issue番号> の実装プランにおける今後の展望から抽出。

---
🤖 *Created by Claude Code (Issue Triage)*
EOF
)"
```

**ラベルの割り当てルール（必須）:**

展望項目の内容に応じて、適切なラベルを**必ず**付与する:

| 内容の種別 | ラベル |
|-----------|--------|
| 新しい機能の追加 | `Type: Feature` |
| 既存機能の改善・拡張 | `Type: Enhancement` |
| コードの整理・改善 | `Type: Refactoring` |
| テストの追加・改善 | `Type: Test` |
| ドキュメントの追加・改善 | `Type: Document` |

さらに、優先度ラベルも付与する:

| 優先度 | ラベル | 基準 |
|--------|--------|------|
| 高 | `Priority: High` | ユーザーに直接影響する、またはバグの温床となりうる |
| 中 | `Priority: Medium` | 品質向上に寄与するが、緊急性は低い |
| 低 | `Priority: Low` | あると良いが、なくても問題ない |

### 4. 作成した Issue のマイルストーン割り当て

作成した Issue にも、ラベルに基づいて適切なマイルストーンを割り当てる。

マイルストーンの割り当てルールは `balance-milestones` スキルのルールに従う。

### 5. 結果の報告

作成した Issue の一覧を以下の形式で報告する:

| # | タイトル | ラベル | マイルストーン | 元プラン |
|---|---------|--------|---------------|---------|
| #XX | <タイトル> | <ラベル> | <マイルストーン> | PLAN-XX |

対象がない場合は「新規作成すべき Issue はありませんでした」と報告する。

## 注意事項

- 新規 Issue には**必ず**ラベルを付けること（ラベルなしの Issue は作成しない）
- 既存 Issue と重複する展望項目は Issue 化しない
- すべての操作は `gh` CLI を通じて行う
