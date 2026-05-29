---
name: zenn-markdownlint-config
description: "Use when setting up markdownlint-cli2 for a Zenn content repository. Zenn-specific rule overrides for false positives."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-12"
---
# Zenn 記事向け markdownlint-cli2 設定パターン

**Extracted:** 2026-02-12
**Context:** Zenn コンテンツリポジトリに markdownlint-cli2 を導入する場合

## Problem

markdownlint のデフォルトルールが Zenn 記事の規約と衝突し、大量の誤検出（191 件 → 42 件に調整）が発生する。

主な衝突:
- **MD025** (single-h1): Zenn は frontmatter の `title` を H1 として扱うため、本文中の `#` 見出しが全て「重複 H1」と判定される
- **MD041** (first-line-h1): frontmatter が先頭にあるため、最初の行が見出しでないと判定される
- **MD060** (table-column-style): Zenn 記事ではコンパクトなテーブル記法が一般的
- **MD013** (line-length): 日本語テキストは行が長くなりがち

## Solution

`.markdownlint-cli2.jsonc` を以下のように設定:

```jsonc
{
  "config": {
    "MD025": false,           // Zenn frontmatter が H1 扱い
    "MD041": false,           // frontmatter が先頭
    "MD060": false,           // コンパクトテーブル許可
    "MD013": false,           // 日本語の長い行を許可
    "MD033": {                // Zenn で使う HTML 要素を許可
      "allowed_elements": ["details", "summary", "br", "sup", "sub"]
    },
    "MD024": { "siblings_only": true },
    "MD026": { "punctuation": ".,;:!" },  // 日本語句読点は許可
    "MD012": { "maximum": 2 },
    "MD003": { "style": "atx" }
  },
  "globs": ["articles/**/*.md", "books/**/*.md"],
  "ignores": ["node_modules", "drafts", ".zenn"]
}
```

**ポイント:**
- `drafts/` を ignores に含めることで下書きはチェック対象外
- `MD033` で `details`/`summary` を許可（Zenn の `:::details` が HTML に変換される場合がある）
- 残る警告（MD031, MD032, MD034, MD040 等）は記事の実質的な品質問題なので有効のまま

## When to Use

- Zenn コンテンツリポジトリに markdownlint-cli2 を新規導入するとき
- 既存の markdownlint 設定で Zenn 記事に大量の誤検出が出るとき
