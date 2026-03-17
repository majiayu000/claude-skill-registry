---
name: drive-share
description: Google Drive のファイルを共有する。「ファイルを共有」「共有設定」「共有して」「リンク共有」「アクセス権を追加」「閲覧権限を付与」などで起動。
allowed-tools: [Read, Bash]
---

# Drive Share

Google Drive のファイルを共有します。

## 引数

- ファイルID (必須): 共有するファイルのID

## 実行方法

### 特定ユーザーに共有（閲覧権限）

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py share --file-id <file-id> --email <user@example.com> --role reader --type user
```

### 特定ユーザーに共有（編集権限）

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py share --file-id <file-id> --email <user@example.com> --role writer --type user
```

### リンクを知っている全員に共有

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py share --file-id <file-id> --type anyone --role reader
```

### 共有通知メールを送信しない

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py share --file-id <file-id> --email <user@example.com> --no-notify
```

## オプション

- `--file-id <id>`: ファイルID（必須）
- `--email <address>`: 共有先メールアドレス（user/group タイプの場合必須）
- `--role <role>`: 権限
  - `reader`: 閲覧のみ
  - `writer`: 編集可能
  - `commenter`: コメント可能
- `--type <type>`: 共有タイプ
  - `user`: 個人
  - `group`: グループ
  - `anyone`: リンクを知っている全員
- `--no-notify`: 共有通知メールを送信しない

## 関連操作

- 現在の共有設定を確認: `drive-get-permissions` を実行

## 注意事項

- トークン未作成の場合は「Google ログイン」と言って認証を行ってください
