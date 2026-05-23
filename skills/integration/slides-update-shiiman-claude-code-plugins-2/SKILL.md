---
name: slides-update
description: Google Slides にスライドを追加する。「スライド追加」「Slides 更新」「スライドを追加して」「ページを追加」などで起動。
allowed-tools: [Read, Bash]
---

# Slides Update

Google Slides プレゼンテーションにスライドを追加します。

## 実行方法

### タイトルと本文付きスライド追加

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_slides.py add-slide --presentation-id "ID" --title "タイトル" --body "本文"
```

### 空白スライド追加

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_slides.py add-slide --presentation-id "ID" --layout BLANK
```

### タイトルのみのスライド

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_slides.py add-slide --presentation-id "ID" --title "タイトル" --layout TITLE
```

## レイアウト種別

- `BLANK`: 空白
- `TITLE`: タイトルのみ
- `TITLE_AND_BODY`: タイトル + 本文（デフォルト）
- `TITLE_AND_TWO_COLUMNS`: タイトル + 2列本文

## ユーザー入力の解釈

- プレゼンテーションIDを聞き出すか、事前に slides-list で検索
- タイトルと本文を確認
- レイアウトの希望を確認

## 出力項目

- id: プレゼンテーションID
- slideId: 追加したスライドID
- status: 追加ステータス
- url: 編集URL
