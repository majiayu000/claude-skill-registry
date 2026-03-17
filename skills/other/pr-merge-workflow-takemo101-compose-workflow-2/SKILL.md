---
name: pr-merge-workflow
description: PRの作成からマージ、クリーンアップ、ロールバックまでの標準フローを定義
---

# PRマージワークフロー

> **責任範囲**: PR作成 → CIチェック → マージ → クリーンアップ
> 
> | このスキル | ci-workflow |
> |-----------|-------------|
> | PR作成テンプレート | CIポーリング・ログ分析 |
> | マージ戦略選択 | 失敗時の自動修正 |
> | ロールバック手順 | リトライ管理（3回） |
> | クリーンアップ | 成功時の自動マージ呼び出し |

---

## PR作成

### 基本コマンド

```bash
gh pr create --title "<タイトル>" --body "$(cat <<'EOF'
## Summary
<1-3 bullet points summarizing changes>

## Related Issues
Closes #XX

## Changes
- <specific change 1>
- <specific change 2>

## Testing
- [ ] Tests passed
- [ ] Lint passed
- [ ] Manual verification (if applicable)
EOF
)"
```

### 必須要素

| 要素 | 説明 | 例 |
|------|------|-----|
| `Closes #XX` | Issue自動クローズ | `Closes #42` |
| Summary | 変更概要（1-3行） | バグ修正、機能追加等 |
| Changes | 具体的な変更リスト | ファイル、関数等 |

---

## CIチェック待機

PR作成後、CIが完了するまで待機する。

```bash
# CI完了まで待機（必須）
gh pr checks <pr-number> --watch
```

**重要**: CIが失敗した場合はマージせず、修正を行う。

---

## PRマージ

### 標準マージコマンド

```bash
# CI成功後にマージ + ブランチ削除
gh pr merge <pr-number> --merge --delete-branch
```

### マージ戦略

| 戦略 | 用途 | コマンド |
|------|------|---------|
| `--merge` | 通常（履歴保持） | `gh pr merge --merge` |
| `--squash` | WIPコミットが多い場合 | `gh pr merge --squash` |
| `--rebase` | 線形履歴が必要な場合 | `gh pr merge --rebase` |

### Worktreeエラー対応

`--delete-branch` がworktreeエラーで失敗する場合：

```bash
# 1. ブランチ削除なしでマージ
gh pr merge <pr-number> --merge

# 2. 後でブランチを手動削除
git push origin --delete <branch-name>
```

---

## マージ後クリーンアップ

### 必須手順

```bash
# 1. Issue自動クローズを確認（Closes #XX使用時）
gh issue view <issue-number>  # Should show "CLOSED"

# 2. 環境削除（コンテナ・ファイル・JSON一括削除）
bash .opencode/skill/delete-environment/scripts/delete_env.sh <env_id>
```

### GitHub Issue ラベル更新

環境削除後、Issue のラベルを更新します（{{skill:github-issue-state-management}} API）：

```bash
bash .opencode/skill/github-issue-state-management/scripts/issue-state.sh merged <issue-number>
```

---

## ロールバック手順

マージ後に問題が発覚した場合：

### 1. 問題の切り分け

| 問題の種類 | 対応 |
|-----------|------|
| 軽微なバグ | 新しいPRで修正 |
| 重大なバグ | git revert でロールバック |
| セキュリティ問題 | 即座にロールバック |

### 2. Revertコマンド

```bash
# 通常のコミット
git revert <commit-hash>

# マージコミット
git revert -m 1 <merge-commit-hash>

# Revert用PRを作成
gh pr create --title "revert: <original PR title>" --body "## Rollback
Reverts PR #<original-pr-number>

**Reason**: <問題の説明>
"

# 緊急時は管理者権限でマージ
gh pr merge <pr-number> --admin --merge
```

---

## チェックリスト

### PR作成前
- [ ] 実装完了
- [ ] テスト通過
- [ ] Lint通過
- [ ] 品質レビュー通過（9点以上）

### PR作成時
- [ ] `Closes #XX` でIssue参照
- [ ] Summary記載
- [ ] 変更リスト記載

### マージ前
- [ ] CI全て通過
- [ ] コードレビュー承認

### マージ後
- [ ] Issue自動クローズ確認
- [ ] 環境削除（`delete_env.sh` 実行）
- [ ] Issue ラベル更新（`env:merged`）

---

## 関連ドキュメント

| ドキュメント | 内容 |
|-------------|------|
| {{skill:ci-workflow}} | CI監視・修正フロー |
| {{skill:github-issue-state-management}} | 環境状態管理 |
| {{skill:delete-environment}} | 環境削除手順 |
| {{skill:quality-review-flow}} | 品質レビュー基準 |

---

## CLIスクリプト

**PRマージ完全フローの自動化スクリプト：**

```bash
bash .opencode/skill/pr-merge-workflow/scripts/pr-merge-full.sh <pr-number> [env-id]
```

| 引数 | 説明 | 必須 |
|------|------|------|
| `pr-number` | PR番号 | ✅ |
| `env-id` | container-use環境ID（クリーンアップ用） | - |

**処理フロー：**
1. CI完了待機（ci-wait.sh呼び出し）
2. PRマージ（`gh pr merge --merge --delete-branch`）
3. Issue ラベル更新（`env:merged`）
4. 環境削除（env-id指定時）

**使用例：**
```bash
bash .opencode/skill/pr-merge-workflow/scripts/pr-merge-full.sh 42 abc-123-def
```
