---
name: slides-list
description: Google Slides の一覧を取得する。「スライド一覧」「Slides 一覧」「Google Slides 一覧」「Slides を見たい」「プレゼンテーション一覧」などで起動。
allowed-tools: [Read, Bash]
---

# Slides List

Google Slides の一覧を取得します。

## 実行方法

### 基本的な一覧取得

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.presentation'"
```

### 最大件数を指定

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py search --query "mimeType='application/vnd.google-apps.presentation'" --max 50
```

### JSON 形式で出力

```bash
python plugins/shiiman-google/skills/drive-list/scripts/google_drive.py --format json search --query "mimeType='application/vnd.google-apps.presentation'"
```

## 出力項目

- id: プレゼンテーションID
- name: プレゼンテーション名
- modifiedTime: 更新日時
- webViewLink: 閲覧URL

## 関連操作

- 検索: `drive-search` コマンドでキーワード検索
- 作成: `slides-create` スキルで新規プレゼンテーション作成
