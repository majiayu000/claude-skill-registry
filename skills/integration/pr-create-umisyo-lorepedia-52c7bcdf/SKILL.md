---
name: pr-create
description: タスク実装完了後にプルリクエストを作成するスキル。実装→テスト→コミット→プッシュ後に「PR作成」「/pr-create」「プルリクエストを作成して」などで使用。
---

# PR Create

タスク実装完了後、CLAUDE.mdの実装フローに従ってプルリクエストを作成するスキル。

## 使用タイミング

- 実装・テスト・コミット・プッシュが完了した後
- PRを作成してセルフレビューに進む前
- Step 5（Push）完了後、Step 6（PR作成）として実行

## 引数

```
/pr-create [--draft]
```

- `--draft`: ドラフトPRとして作成（オプション）

## 前提条件チェック

PR作成前に以下を確認する:

1. **ブランチ確認**: mainブランチではないこと
2. **プッシュ確認**: リモートに最新がプッシュされていること
3. **差分確認**: mainとの差分が存在すること

## 実行手順

### 1. 現在の状態を確認

```bash
# 並列実行で効率化
git status
git branch --show-current
git log origin/main..HEAD --oneline
git diff origin/main...HEAD --stat
```

確認事項:
- 現在のブランチ名
- 未コミットの変更がないこと
- リモートにプッシュ済みであること
- mainからの差分コミット一覧

### 2. PRタイトルと説明を生成

**タイトル形式:**
```
<種類>: <変更内容の要約>
```

種類はブランチ名のプレフィックスから判断:
- `feature/` → `feat:`
- `fix/` → `fix:`
- `refactor/` → `refactor:`
- `docs/` → `docs:`

**説明の構造:**
```markdown
## Summary
<1-3 bullet points>

## Test plan
[Bulleted markdown checklist of TODOs for testing the pull request...]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### 3. PR作成

```bash
gh pr create --title "タイトル" --body "$(cat <<'EOF'
## Summary
- 変更内容の要約1
- 変更内容の要約2

## Test plan
- [ ] テスト項目1
- [ ] テスト項目2

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

ドラフトの場合は `--draft` オプションを追加。

### 4. 次のステップを案内

PR作成後、以下を案内する:
- PRのURL
- 次のステップ: **セルフレビュー・修正サイクル（Step 6）**
- `/codex` スキルを使用してレビューを実行することを促す

## 注意事項

- 未コミットの変更がある場合は、先にコミットを促す
- プッシュされていない場合は、先にプッシュを促す
- mainブランチでは実行しない
- 既存のPRがある場合は、既存のPR URLを案内する

## エラーハンドリング

| エラー | 対応 |
|-------|------|
| mainブランチで実行 | 「作業ブランチに切り替えてください」と案内 |
| 未コミットの変更あり | 「先にコミットしてください」と案内 |
| プッシュされていない | 「先にプッシュしてください」と案内 |
| 差分がない | 「mainとの差分がありません」と案内 |
| 既存PRあり | 既存のPR URLを表示 |

## 実行例

```
User: /pr-create

Assistant:
1. git status でブランチの状態を確認
2. git branch で現在のブランチが feature/add-world-list であることを確認
3. git log origin/main..HEAD でコミット履歴を確認
4. gh pr create でPRを作成:
   - タイトル: feat: ワールド一覧ページを追加
   - 説明: コミット内容から自動生成
5. PR URL: https://github.com/Umisyo/Lorepedia/pull/123
6. 次のステップ: /codex でセルフレビューを実行してください
```
