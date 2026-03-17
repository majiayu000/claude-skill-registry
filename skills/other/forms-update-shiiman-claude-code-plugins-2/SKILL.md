---
name: forms-update
description: Google Forms に質問を追加する。「質問追加」「Forms 更新」「フォームに質問を追加」「アンケート項目追加」などで起動。
allowed-tools: [Read, Bash]
---

# Forms Update

Google Forms フォームに質問を追加します。

## 実行方法

### テキスト質問追加

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_forms.py add-question --form-id "ID" --question "お名前は？" --type TEXT
```

### 選択式質問追加

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_forms.py add-question --form-id "ID" --question "好きな色は？" --type RADIO --options "赤,青,緑"
```

### 必須質問

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_forms.py add-question --form-id "ID" --question "メールアドレス" --type TEXT --required
```

## 質問タイプ

- `TEXT`: 短いテキスト
- `PARAGRAPH`: 長いテキスト
- `RADIO`: 単一選択（ラジオボタン）
- `CHECKBOX`: 複数選択
- `DROP_DOWN`: ドロップダウン
- `SCALE`: スケール（1-5）
- `DATE`: 日付
- `TIME`: 時刻

## ユーザー入力の解釈

- フォームIDを聞き出すか、事前に forms-list で検索
- 質問文を確認
- 質問タイプを判断（選択肢があれば RADIO/CHECKBOX など）
- 必須かどうかを確認

## 出力項目

- id: フォームID
- status: 追加ステータス
- question: 追加した質問
- type: 質問タイプ
- editUrl: 編集URL
