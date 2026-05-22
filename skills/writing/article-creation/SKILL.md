---
name: article-creation
description: 新規ブログ記事の作成。「記事を書きたい」「新しい記事を作成」「ブログ投稿」などのリクエスト時に使用。
---

# Article Creation

新規 Markdown 記事を作成するスキル。

## 記事の配置場所

```text
apps/blog/src/contents/YYYY-MM-DD-slug.md
```

## ファイル名規則

- 形式: `YYYY-MM-DD-slug.md`
- slug: 英数字とハイフンのみ（例: `hello-world`, `nextjs-tips`）
- 日付: 記事の公開日

## Front-matter 構造

```yaml
---
title: "記事タイトル"
date: "YYYY-MM-DD"
published: true
tags: ["Tag1", "Tag2"]
description: "SEO用の記事説明（100-160文字程度）"
---
```

### フィールド説明

| フィールド    | 必須 | 説明                                 |
| ------------- | ---- | ------------------------------------ |
| title         | Yes  | 記事タイトル（日本語可）             |
| date          | Yes  | 公開日（YYYY-MM-DD形式）             |
| published     | Yes  | true: 公開 / false: 下書き           |
| tags          | Yes  | タグの配列（2-5個推奨）              |
| description   | Yes  | SEO用説明文                          |

## 記事テンプレート

```markdown
---
title: "タイトル"
date: "YYYY-MM-DD"
published: false
tags: ["Tag"]
description: "説明"
---

## はじめに

導入文をここに。

## 本文

メインコンテンツ。

### コード例

\`\`\`typescript:example.ts
// コード例
\`\`\`

### 図表（Mermaid）

\`\`\`mermaid
graph TD
    A[開始] --> B[終了]
\`\`\`

## まとめ

締めくくり。
```

## 手順

1. ユーザーからタイトル・テーマを確認
2. slug を提案（英語、ハイフン区切り）
3. 適切なタグを提案
4. テンプレートから記事ファイルを作成
5. `published: false` で作成（ユーザー確認後、true へ変更）
6. `just lint` を実行してエラーがないことを確認

## 注意事項

- 日本語と英語の混在可
- コードブロックにはファイル名を付ける（`:filename.ext`）
- Mermaid 図は適宜活用
- 画像は `/public/images/` に配置し `/images/xxx.png` で参照
