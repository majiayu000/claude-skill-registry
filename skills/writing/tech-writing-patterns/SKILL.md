---
name: tech-writing-patterns
description: "Use when writing or reviewing technical articles for Zenn/Qiita. Cross-posting, tone adjustment, quality patterns."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-09"
---

# Tech Writing Patterns

**Extracted:** 2026-02-09 (consolidated 2026-02-10)
**Context:** 技術記事の執筆・品質改善・クロスプラットフォーム投稿

---

## 1. Zenn to Qiita Cross-Post

### Problem

Zenn 記事を Qiita に手動でコピペ・フォーマット修正するのが面倒。

### Solution

Parser -> Converter -> Publisher の3段パイプライン。単一ファイル ~170行で実装可能。

```
Zenn 記事 (articles/*.md)
  -> [Parser] python-frontmatter で title, topics, body を解析
  -> [Converter] Zenn 固有記法を標準 Markdown に変換
  -> [Publisher] Qiita API v2 POST
```

### Zenn -> Qiita 変換ポイント

| Zenn | Qiita |
|------|-------|
| `:::message ... :::` | `> blockquote` |
| `:::details title ... :::` | `<details><summary>` |
| `topics: [a, b, c]` | `tags: [{name: "a"}, ...]` (最大5個) |
| frontmatter | 削除 (API ボディに変換) |

### Qiita API v2

```
POST https://qiita.com/api/v2/items
Authorization: Bearer {QIITA_ACCESS_TOKEN}
Body: { title, body, tags: [{name: "..."}], private: false }
Response: 201 -> { url: "https://qiita.com/..." }
```

### Dependencies (minimal)

- `python-frontmatter` - Zenn frontmatter 解析
- `httpx` - HTTP client

---

## 2. 技術記事のトーン調整

### Problem

技術記事の初稿で発生しがちな問題:
- 同じ内容を何度も繰り返す（特にキーメッセージ）
- 感嘆符や形容詞が過剰（「素晴らしい！」「最高の！」）
- 太字の多用で視覚的にうるさい
- 具体的すぎる情報が全体の流れを妨げる

### Solution

#### 繰り返しの削減
- キーメッセージは1回だけ詳しく説明、以降は簡潔に参照
- 同じフレーズの出現回数をGrepで確認

#### トーンダウン
- 感嘆符（！）を削除または句点（。）に変更
- 「素晴らしい」「最高の」「驚くほど」などの形容詞を削除
- 太字（**text**）は本当に重要な箇所だけに使用
- 事実ベースの淡々とした記述に

#### 具体例の一般化
- プロジェクト名や固有名詞は別記事で説明予定なら削除
- コード例から具体的なパスを一般的なパスに変更

#### 不正確な表現の修正
- 事実確認、引用の正確性確認、リンクの妥当性確認

### Key Principles

- 誠実さは保ちつつ、温度感を下げる
- 事実を淡々と述べる
- 読者に判断を委ねる（「素晴らしい」ではなく「良い」）

---

## When to Use

- Zenn 記事を Qiita にクロスポストする時
- 技術記事の初稿を書き終えた後のレビュー
- 記事が感情的すぎる、繰り返しが多いとフィードバックを受けた時
