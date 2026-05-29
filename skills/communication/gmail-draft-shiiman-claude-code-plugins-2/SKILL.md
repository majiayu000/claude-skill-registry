---
name: gmail-draft
description: Gmail で下書きを作成する。「下書き作成」「メールの下書き」「下書きを保存」「下書きで保存」などで起動。
allowed-tools: [Bash]
---

# Gmail Draft

Gmail で下書きを作成します。送信前に確認したい場合に便利です。

## 実行方法

### 下書きを作成

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py draft --to "user@example.com" --subject "件名" --body "本文です。"
```

### CC/BCC 付きで下書き作成

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py draft --to "user@example.com" --subject "報告" --body "内容" --cc "cc1@example.com"
```

### HTML 形式の下書き

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py draft --to "user@example.com" --subject "お知らせ" --body "<h1>見出し</h1><p>本文</p>" --html
```

## 必要な情報

- **宛先** (必須): 送信先メールアドレス
- **件名** (必須): メールの件名
- **本文** (必須): メールの本文
- CC: カーボンコピー（カンマ区切りで複数指定可）
- BCC: ブラインドカーボンコピー（カンマ区切りで複数指定可）
- HTML: HTMLメールとして作成するかどうか

## ユーザー入力の解釈

ユーザーから以下の情報を聞き出す:
1. 宛先（誰に送るか）
2. 件名（タイトル）
3. 本文（内容）
4. CC/BCC（必要に応じて）

## 出力項目

- to: 宛先
- subject: 件名
- id: 下書きID
- url: 下書きを開くURL（編集・送信可能）
