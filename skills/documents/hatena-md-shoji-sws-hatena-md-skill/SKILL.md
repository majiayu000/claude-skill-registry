---
name: "hatena-blog-markdown-extractor"
description: "Extract content from Hatena Blog article URLs and convert to Markdown format with frontmatter. Preserves images as absolute URLs and removes sidebars, headers, footers, and ads."
---

# Hatena Blog Markdown Extractor

はてなブログの記事URLからコンテンツをMarkdown形式で抽出するスキルです。

## 機能

- はてなブログの記事URLから本文を抽出
- HTML → Markdown変換
- 画像URLをフルパス(絶対パス)で保持
- サイドバー、ヘッダー、フッター、広告などの不要な要素を自動除去
- フロントマター付きMarkdownファイルを生成

## 使用方法

```bash
# 単一のURLから抽出
/hatena-md <記事URL>

# カスタム出力ディレクトリを指定
/hatena-md <記事URL> <出力ディレクトリ>
```

## 例

```bash
# デフォルトの出力先 (./hatena-posts/) に保存
/hatena-md https://www.simple-web-system.work/entry/2024/10/17/223212

# カスタム出力先に保存
/hatena-md https://www.simple-web-system.work/entry/2024/10/17/223212 ./my-posts
```

## 出力形式

抽出されたMarkdownファイルには以下のフロントマターが付きます:

```markdown
---
title: "記事タイトル"
url: https://www.simple-web-system.work/entry/2024/10/17/223212
extracted: 2025-10-27T09:46:00.000Z
---

記事本文...
```

## 出力先

- デフォルト: `./hatena-posts/`
- ファイル名: 記事タイトル.md (特殊文字は除去・置換されます)

## 注意事項

- Node.jsプロジェクトとしてセットアップされている必要があります
- 実行前に `npm install` と `npm run build` を実行してください
