---
name: generate-book
description: 書籍タイトルからscrapsファイルを生成します
allowed-tools: WebSearch, WebFetch, Write
---

$ARGUMENTS タイトルの書籍scrapsファイルを生成します

# 手順

1. $ARGUMENTS タイトルでWeb検索をし、公式出版社ページ（タイトルの言語に対応）の情報を読み取り
2. 1から以下の情報を特定
   - タイトル（ファイル名に使用）
   - サブタイトル
   - 著者
   - 訳者（存在する場合）
   - 書籍画像URL
   - 出版社ページのOGPタイトル
   - 出版社ページのURL
   - 目次（部、章、節）
3. `mcp__plugin_mcp-server_scraps__list_tags` でタグ一覧を取得し、書籍の内容に適したタグを選択（Bookは必須、他は内容に応じて追加）
4. `mcp__plugin_mcp-server_scraps__search_scraps` でタイトルの重複を確認し、配置場所を決定
   - 重複あり: `scraps/Book/{タイトル}.md`
   - 重複なし: `scraps/{タイトル}.md`
5. 以下のフォーマットでファイルを生成
6. `mcp__plugin_mcp-server_scraps__search_scraps` で関連scrapsを検索し、リンクを貼るべき箇所を提案

# 出力フォーマット

```markdown
## {サブタイトル}

### Authors:
{著者}
{訳者}

#[[Book]] {関連タグ}

![]({書籍画像URL})

[{出版社ページOGPタイトル}]({出版社ページURL})

## {部タイトル}

### {章タイトル}

-

### {章タイトル}

-
```

## フォーマット注意事項

- サブタイトルがない場合はh2見出しを省略
- 訳者がない場合はその行を省略
- 目次はh2以降の見出しを用いてレイヤを表現（部→h2、章→h3、節→h4）
- 各章見出しの下に箇条書きプレースホルダ `- ` を1行置く（読書時の引用メモ・リンク追記用）
- 取得できなかった項目は省略
- タグは `#[[Book]]` を必須とし、書籍内容に関連するタグを半角スペース区切りで追加（例: `#[[Book]] #[[Security]] #[[Testing]]`）
