---
name: drive-list
description: Google Drive のファイル一覧を取得する。「Drive 一覧」「ドライブのファイルを見たい」「最近のファイル」「Drive の一覧を出して」「ファイルリスト」「Google Drive 一覧」「ドライブを表示」などで起動。
allowed-tools: [Read, Bash]
---

# Drive List

Google Drive のファイル一覧を取得します。

## 実行方法

### アクティブプロファイルで一覧を取得

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py list
```

### プロファイル指定で一覧を取得

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py list --profile <profile-name>
```

### 最大件数を指定

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py list --max 50
```

### JSON 形式で出力

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_drive.py --format json list
```

## 出力項目

- id: ファイルID
- name: ファイル名
- mimeType: ファイル種類
- modifiedTime: 更新日時
- webViewLink: URL

## 関連操作

- 検索する: `drive-search` を実行
- 共有設定を確認: `drive-get-permissions` を実行
- 共有する: `drive-share` を実行

## 注意事項

- トークン未作成の場合は「Google ログイン」と言って認証を行ってください
