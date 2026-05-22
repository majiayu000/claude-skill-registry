---
name: gmail-send
description: Gmail でメールを送信する。「メール送信」「メールを送って」「Gmail で送信」「メールを出して」などで起動。
allowed-tools: [Bash]
---

# Gmail Send

Gmail でメールを送信します。

## 実行方法

### メールを送信

```bash
python plugins/shiiman-google/skills/gmail-send/scripts/google_gmail.py send --to "user@example.com" --subject "件名" --body "本文です。"
```

### CC/BCC 付きで送信

```bash
python plugins/shiiman-google/skills/gmail-send/scripts/google_gmail.py send --to "user@example.com" --subject "報告" --body "内容" --cc "cc1@example.com,cc2@example.com" --bcc "bcc@example.com"
```

### HTML メールとして送信

```bash
python plugins/shiiman-google/skills/gmail-send/scripts/google_gmail.py send --to "user@example.com" --subject "お知らせ" --body "<h1>見出し</h1><p>本文</p>" --html
```

## 必要な情報

- **宛先** (必須): 送信先メールアドレス
- **件名** (必須): メールの件名
- **本文** (必須): メールの本文
- CC: カーボンコピー（カンマ区切りで複数指定可）
- BCC: ブラインドカーボンコピー（カンマ区切りで複数指定可）
- HTML: HTMLメールとして送信するかどうか

## ユーザー入力の解釈

ユーザーから以下の情報を聞き出す:
1. 宛先（誰に送るか）
2. 件名（タイトル）
3. 本文（内容）
4. CC/BCC（必要に応じて）

## 出力項目

- to: 宛先
- subject: 件名
- id: メッセージID
- url: 送信済みメールを開くURL
