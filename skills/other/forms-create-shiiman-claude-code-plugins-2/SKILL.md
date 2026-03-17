---
name: forms-create
description: Google Forms フォームを新規作成する。「フォーム作成」「Forms 作成」「新しいフォーム」「アンケート作成」「フォームを作って」などで起動。
allowed-tools: [Read, Bash]
---

# Forms Create

Google Forms フォームを新規作成します。

## 実行方法

### 基本的な作成

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_forms.py create --name "フォーム名"
```

### 説明付きで作成

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_forms.py create --name "フォーム名" --description "フォームの説明"
```

## ユーザー入力の解釈

- フォーム名を聞き出す
- 説明があれば --description で指定

## 出力項目

- id: フォームID
- name: フォーム名
- editUrl: 編集URL
- responseUrl: 回答URL
