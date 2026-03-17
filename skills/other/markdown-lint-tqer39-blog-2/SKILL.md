---
name: markdown-lint
description: Markdown ファイル編集後のリント実行。Markdown を作成・編集したら必ず実行。
---

# Markdown Lint

Markdown ファイルを作成・編集した後に lint を実行するスキル。

## 重要

**Markdown ファイル (*.md) を作成・編集した場合は、必ずこのスキルに従って lint を実行すること。**

## 実行コマンド

```bash
just lint
```

## 対象ファイル

- `*.md` (すべての Markdown ファイル)
- 例: `README.md`, `DEVELOPMENT.md`, `CHANGELOG.md`
- 例: `.claude/skills/**/SKILL.md`
- 例: `apps/blog/src/contents/*.md`

## 手順

1. Markdown ファイルを作成・編集
2. `just lint` を実行してエラーを確認
3. エラーがあれば修正
4. 再度 `just lint` で確認（すべて Passed になるまで繰り返す）

## よくあるエラーと修正方法

| エラー   | 原因                           | 修正方法                         |
| -------- | ------------------------------ | -------------------------------- |
| MD041    | 最初の行が見出しでない         | `# タイトル` を先頭に追加        |
| MD040    | コードブロックに言語指定がない | ` ```bash ` のように言語を指定   |
| textlint | 日本語の文法エラー             | エラーメッセージに従って修正     |
| cspell   | 不明な単語                     | `cspell.json` の `words` に追加  |

## 注意事項

- YAML front-matter がある場合、見出しはその直後に記述
- コードブロックには必ず言語を指定（`text` でも可）
- 日本語の助詞の重複に注意（textlint が検出）
