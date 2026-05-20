---
name: prh-hyphen-regex-escape
description: "Use when adding hyphenated terms to prh spelling dictionaries on Node.js 20+. Unicode regex flag incompatibility."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-12"
---
# prh ハイフン含むパターンの正規表現エラー

**Extracted:** 2026-02-12
**Context:** textlint-rule-prh を Node.js 20+ 環境で使用し、ハイフン含む用語を表記ゆれ辞書に登録する場合

## Problem

`prh.yml` にハイフンを含むパターン（例: `Claude-first`, `cli-first`, `pdf-to-anki`）を記載すると、textlint 実行時に以下のエラーが発生する:

```
SyntaxError: Invalid regular expression: /Claude\-first/gmu: Invalid escape
```

**根本原因:**
1. prh は文字列パターンを内部的に正規表現に変換する際、ハイフン `-` を `\-` にエスケープする
2. prh は正規表現に `gmu` フラグを自動付加する
3. Node.js 20+ の unicode フラグ (`u`) では、キャラクタークラス (`[...]`) 外の `\-` は無効なエスケープシーケンスとして扱われる
4. 結果、`SyntaxError` が発生する

**追加の罠: specs 検証エラー**

ハイフン問題を regex リテラル (`/pattern/`) で回避しても、`specs` の `from` にハイフン含む文字列を書くと別のエラーが発生する:

```
Error: spec failed. "claude-native", expected "Claude-Native", but got "claude-native"
```

パターンがハイフン部分にマッチしないため、置換が行われず検証が失敗する。

## Solution

**ハイフンを含むパターンは prh に登録しない。** ハイフンなしのバリエーションのみを対象にする。

```yaml
# BAD: ハイフン含むパターン → SyntaxError
- expected: Claude-Native
  patterns:
    - Claude-first    # ← \- エスケープでクラッシュ
    - cli-first       # ← 同上

# GOOD: ハイフンなしのバリエーションのみ
- expected: Claude-Native
  patterns:
    - Claude based
    - claude native

- expected: CLI-First
  patterns:
    - CLI first
```

**理由:** `Claude-first` → `Claude-Native` のようなハイフン付き誤表記の検出は、prh では技術的に困難。editor エージェントや手動レビューで補完する。

## When to Use

- `textlint-rule-prh` の辞書（`prh.yml`）を作成・編集するとき
- 特にハイフン含む正式表記（`Claude-Native`, `CLI-First` 等）の表記ゆれを登録しようとするとき
- Node.js 20+ 環境（unicode regex が厳密化された環境）
