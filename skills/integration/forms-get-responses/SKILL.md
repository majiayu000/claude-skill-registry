---
name: forms-get-responses
description: Google Forms の回答を取得する。「フォームの回答」「回答結果を見せて」「フォーム回答取得」「アンケート結果」「回答一覧」「フォームの結果」などで起動。
allowed-tools: [Read, Bash]
---

# Forms Get Responses

Google Forms の回答を取得します。

## 引数

- フォームID (必須): 回答を取得するフォームのID

## オプション

- `--max <number>`: 最大取得件数（デフォルト: 50）

## 実行方法

```bash
python plugins/shiiman-google/skills/forms-list/scripts/google_forms.py responses --form-id <form-id>
```

### 最大件数を指定

```bash
python plugins/shiiman-google/skills/forms-list/scripts/google_forms.py responses --form-id <form-id> --max 100
```

## 出力項目

- responseId: 回答ID
- createTime: 回答日時
- answers: 各質問への回答内容
