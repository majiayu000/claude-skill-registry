---
name: forms-list
description: Google Forms の一覧を取得する。「フォーム一覧」「Forms 一覧」「Google Forms 一覧」「Forms を見たい」「アンケート一覧」などで起動。
allowed-tools: [Read, Bash]
---

# Forms List

Google Forms の一覧を取得します。

## 実行方法

### 基本的な一覧取得

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.form'"
```

### 最大件数を指定

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.form'" --max 50
```

### JSON 形式で出力

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py --format json search --query "mimeType='application/vnd.google-apps.form'"
```

## 出力項目

- id: フォームID
- name: フォーム名
- modifiedTime: 更新日時
- webViewLink: 閲覧URL

## 関連操作

- 検索: `drive-search` コマンドでキーワード検索
- 作成: `forms-create` スキルで新規フォーム作成
