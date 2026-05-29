# Hook Lister

プロジェクトに設定されたフックの一覧を表示するスキル。「フック一覧」「フックを見せて」「設定済みフック」「hooks 確認」「フックリスト」「hook 一覧」「フックを確認」などで起動。

## スキル情報

```yaml
name: hook-lister
description: プロジェクトに設定されたフックの一覧を表示するスキル。「フック一覧」「フックを見せて」「設定済みフック」「hooks 確認」「フックリスト」「hook 一覧」「フックを確認」などで起動。
allowedTools:
  - Read
```

## Claude への指示

### 実行手順

1. 以下のファイルから `hooks` セクションを読み込む:
   - `.claude/settings.json`
   - `.claude/settings.local.json`（存在する場合）
2. イベント別にフックを整形して表示

### フックイベントの種類

| イベント | 説明 | matcher |
|----------|------|---------|
| PreToolUse | ツール実行前（ブロック可能） | 必須 |
| PostToolUse | ツール実行後 | 必須 |
| PostToolUseFailure | ツール実行失敗後 | 必須 |
| UserPromptSubmit | プロンプト送信時 | 不要 |
| Notification | 通知時 | 不要 |
| Stop | レスポンス完了時 | 不要 |
| SubagentStart | サブエージェント開始時 | 不要 |
| SubagentStop | サブエージェント完了時 | 不要 |
| PreCompact | Compact 操作前 | 不要 |
| SessionStart | セッション開始時 | 不要 |
| SessionEnd | セッション終了時 | 不要 |
| PermissionRequest | 権限要求時 | 不要 |

### 出力フォーマット

```markdown
## 設定済みフック

### ソース別

| ソース | 件数 |
|--------|------|
| settings.json | 3 |
| settings.local.json | 1 |

### PreToolUse

| # | マッチャー | タイプ | コマンド/プロンプト | ソース |
|---|-----------|--------|---------------------|--------|
| 1 | Write | command | prettier --write "$FILE" | settings.json |
| 2 | Bash | prompt | 危険なコマンドをチェック | settings.local.json |

### PostToolUse

| # | マッチャー | タイプ | コマンド/プロンプト | ソース |
|---|-----------|--------|---------------------|--------|
| 1 | Write | command | eslint --fix "$FILE" | settings.json |

### SessionStart

| # | タイプ | コマンド/プロンプト | ソース |
|---|--------|---------------------|--------|
| 1 | command | echo "Session started" | settings.json |
```

### 重要な注意事項

- ✅ settings.json と settings.local.json の両方を確認
- ✅ フックがない場合は「フックは設定されていません」と表示
- ✅ 各フックに番号を付与（削除時の参照用）
- ✅ ソースファイルを明示（どのファイルで定義されているか）
- ❌ フックの編集は行わない（表示のみ）
