---
name: zenn-textlint-workarounds
description: "Use when textlint produces false positives on Zenn articles. prh hyphen loop, :::message, and --fix workarounds."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-13"
---
# Zenn記事の textlint 誤検出ワークアラウンド

**Extracted:** 2026-02-13
**Context:** Zenn記事を textlint + prh + markdownlint で lint する際の既知の誤検出と回避策

## Problem 1: prh 長音記号の誤検出ループ

prh ルール `サーバ => サーバー` が、すでに正しい「サーバー」の中の「サーバ」部分文字列にマッチする。

- `textlint --fix` を実行すると「サーバー」→「サーバーー」に二重化
- 手動で戻しても次の `--fix` で再発
- 同様のパターン: `ユーザ => ユーザー` など長音記号追加系ルール全般

### Solution

「サーバー」を使わない表現に言い換える。

```markdown
# NG: prh が誤検出する
自宅のMacがそのままサーバーになる。

# OK: 言い換えで回避
自宅のMacをそのまま使う。
```

### 根本対策（未実施）

prh.yml でネガティブルックアヘッドを使う:

```yaml
# 現状（誤検出する）
- expected: サーバー
  pattern: サーバ

# 改善案（未検証）
- expected: サーバー
  pattern: サーバ(?!ー)
```

## Problem 2: `:::message` と textlint の非互換

Zenn の `:::message...:::` 構文の閉じ `:::` を textlint が「文末に句点がない」と誤検出する。

```
156:3  error  文末が"。"で終わっていません。  ja-technical-writing/ja-no-mixed-period
```

### Solution

`:::message` の代わりに blockquote (`>`) を使う。

```markdown
# NG: textlint が ::: を文として検出
:::message
**Tips**: ここに補足テキスト。
:::

# OK: blockquote なら textlint は問題なし
> **Tips**: ここに補足テキスト。
```

**トレードオフ**: `:::message` は Zenn 上で黄色い背景ボックスとして表示されるが、blockquote は灰色の引用表示になる。視覚的な差異を許容できる場合のみこの回避策を使う。

## Problem 3: textlint --fix の二重適用

`textlint --fix` は prh ルールを機械的に適用するため、上記 Problem 1 と組み合わさると破壊的な変更が起きる。

### Solution

- `textlint --fix` 実行後は必ず diff を確認する
- 特に prh の auto-fix 結果は目視チェック必須
- lint-staged + husky 環境では `--fix` が自動実行されないことを確認

## When to Use

- Zenn 記事を書いて textlint を通す時
- pre-commit hook で textlint エラーが出てコミットできない時
- prh ルールに長音記号パターンを追加する時
