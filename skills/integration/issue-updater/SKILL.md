---
name: issue-updater
description: 実装状況に応じて Issue の状態を更新する。「Issue 更新」「Issue を更新」「Issue 状態変更」「Issue をクローズ」「Issue 完了」「チケットを閉じる」「Issue の進捗を更新」などで起動。コメント追加やラベル変更、クローズ処理を実行。
allowed-tools: [Read, Bash]
---

# Issue Updater

実装状況に応じて Issue の状態を更新します。

## ワークフロー

### 1. 対象 Issue の特定

以下から対象 Issue を特定:

- ユーザーの指示（「#5 を更新」）
- 現在のブランチ名（`feature/5` → #5）
- 直前のコンテキスト

### 2. 現在の状態確認

```bash
gh issue view {issue番号} --json title,state,labels,body
```

### 3. 更新内容の確認

ユーザーに更新内容を確認:

- コメント追加
- ラベル変更
- クローズ

### 4. 更新実行

**コメント追加**:

```bash
gh issue comment {issue番号} --body "{comment}"
```

**ラベル追加**:

```bash
gh issue edit {issue番号} --add-label "{label}"
```

**ラベル削除**:

```bash
gh issue edit {issue番号} --remove-label "{label}"
```

**クローズ**:

```bash
gh issue close {issue番号} --comment "{close_comment}"
```

### 5. 結果報告

```
Issue #{issue番号} を更新しました:

- 追加コメント: {comment}
- 状態: オープン → クローズ
```

## 進捗コメントのテンプレート

**作業開始時**:

```markdown
## 作業開始

- 開始日時: {datetime}
- 作業ブランチ: `{branch}`
```

**進捗報告**:

```markdown
## 進捗報告

- 完了: {completed_tasks}
- 残り: {remaining_tasks}
- ブロッカー: {blockers または「なし」}
```

**完了時**:

```markdown
## 完了報告

- 完了日時: {datetime}
- 関連 PR: #{pr_number}
```

## 重要な注意事項

- ✅ 適切なコメントを追加
- ✅ PR マージ時は自動クローズを使用（`Closes #N`）
- ❌ 作業途中で勝手にクローズしない
- ❌ 他人の Issue を無断で更新しない
