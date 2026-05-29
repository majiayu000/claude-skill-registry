---
name: gmail-read
description: Gmail メッセージ本文を表示する。「メール本文」「Gmail 本文を見たい」「メッセージ内容を表示」「メールを開いて」「Gmail を読む」「本文を見せて」「内容確認」などで起動。
allowed-tools: [Read, Bash]
---

# Gmail Read

Gmail メッセージ本文を表示します。

## 引数

- メッセージID (必須): 本文を表示するメッセージのID

## 実行方法

### アクティブプロファイルで本文を取得

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py read --id <message-id>
```

### プロファイル指定で本文を取得

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py read --profile <profile-name> --id <message-id>
```

## 出力項目

- subject: 件名
- from: 送信者
- to: 宛先
- date: 日時
- body: 本文

## 関連操作

- 未読一覧から確認: `gmail-list-unread` を実行してメッセージIDを取得
- スター一覧から確認: `gmail-list-starred` を実行してメッセージIDを取得

## 注意事項

- トークン未作成の場合は「Google ログイン」と言って認証を行ってください
