---
name: gmail-starred
description: Gmail のスター付きメッセージ一覧を取得する。「スター付きメール」「スター一覧」「Gmail スター付き」「星付きメール」「スターを見たい」などで起動。
allowed-tools: [Read, Bash]
---

# Gmail Starred

Gmail のスター付きメッセージ一覧を取得します。

## 実行方法

### アクティブプロファイルのスター付き一覧

```bash
python plugins/shiiman-google/skills/gmail-starred/scripts/google_gmail.py starred
```

### 最大件数を指定

```bash
python plugins/shiiman-google/skills/gmail-starred/scripts/google_gmail.py starred --max 50
```

### JSON 形式で出力

```bash
python plugins/shiiman-google/skills/gmail-starred/scripts/google_gmail.py --format json starred
```

## 出力項目

- id: メッセージID
- subject: 件名
- from: 送信者
- date: 受信日時

## 関連操作

- 本文を読む: メッセージID を指定して `gmail-read` を実行
- スターを外す: `gmail-star --remove` を実行
