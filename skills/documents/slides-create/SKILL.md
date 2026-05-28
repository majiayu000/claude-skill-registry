---
name: slides-create
description: Google Slides プレゼンテーションを新規作成する。「プレゼン作成」「Slides 作成」「新しいスライド」「プレゼンを作って」などで起動。
allowed-tools: [Read, Bash]
---

# Slides Create

Google Slides プレゼンテーションを新規作成します。

## 実行方法

### 基本的な作成

```bash
python plugins/shiiman-google/skills/slides-create/scripts/google_slides.py create --name "プレゼンテーション名"
```

### フォルダを指定

```bash
python plugins/shiiman-google/skills/slides-create/scripts/google_slides.py create --name "プレゼンテーション名" --folder-id "フォルダID"
```

## ユーザー入力の解釈

- プレゼンテーション名を聞き出す
- フォルダを指定したい場合は事前に drive-search で検索

## 出力項目

- id: プレゼンテーションID
- name: プレゼンテーション名
- url: 編集URL
