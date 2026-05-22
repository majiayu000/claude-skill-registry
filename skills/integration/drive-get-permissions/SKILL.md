---
name: drive-get-permissions
description: Google Drive のファイルの共有設定を確認する。「共有状況確認」「誰がアクセスできる」「共有設定を見せて」「アクセス権確認」「権限一覧」「共有中のユーザー」などで起動。
allowed-tools: [Read, Bash]
---

# Drive Get Permissions

Google Drive のファイルの共有設定を確認します。

## 引数

- ファイルID (必須): 共有設定を確認するファイルのID

## 実行方法

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py permissions --file-id <file-id>
```

## 使用例

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py permissions --file-id 1abc...xyz
```

## 出力項目

- role: 権限レベル（owner, writer, reader など）
- type: 共有タイプ（user, group, domain, anyone）
- emailAddress: 共有相手のメールアドレス
