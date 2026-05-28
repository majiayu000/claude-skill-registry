---
name: remove-hook
description: プロジェクトからフックを削除する。「フック削除」「フックを消して」「hook を削除」「フックを外して」「フック解除」「hook 削除」「フックを取り除いて」などで起動。
allowed-tools: [Read, Write, AskUserQuestion]
---

# Remove Hook

プロジェクトからフックを削除します。

## 実行手順

1. まず `list-hooks` スキルと同様にフック一覧を表示
2. ユーザーに削除対象を確認:
   - イベント名（例: PreToolUse）
   - フック番号（例: 1）
   - ソースファイル（settings.json または settings.local.json）
3. 確認後、該当するフックを削除
4. 削除完了メッセージを表示

### 削除確認フォーマット

```markdown
## フック削除

以下のフックを削除しますか？

| 項目 | 値 |
|------|-----|
| イベント | PreToolUse |
| マッチャー | Write |
| タイプ | command |
| コマンド | prettier --write "$FILE" |
| ソース | settings.json |

削除を実行する場合は「はい」と入力してください。
```

### 削除処理

1. 対象ファイル（`.claude/settings.json` または `.claude/settings.local.json`）を読み込み
2. `hooks` セクションから該当エントリを削除
3. フック配列が空になった場合はイベントキーごと削除
4. `hooks` オブジェクトが空になった場合は `hooks` キーごと削除
5. ファイルを保存

### 出力フォーマット（削除完了時）

```markdown
## 削除完了

以下のフックを削除しました:

- イベント: PreToolUse
- マッチャー: Write
- ソース: settings.json

現在のフック数: 2件
```

### 重要な注意事項

- ✅ 削除前に必ず確認を求める
- ✅ settings.local.json のフックも削除可能
- ✅ 削除後にフック数を表示
- ✅ JSON フォーマットを維持（インデント等）
- ❌ 複数フックの一括削除は行わない（1つずつ確認）
