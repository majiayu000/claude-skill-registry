---
name: brainstorming-communication
description: "Use when the user is exploring ideas and hasn't decided on a direction yet. Provide information without forcing choices."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-13"
---
# Brainstorming Communication Pattern

**Extracted:** 2026-02-13
**Context:** ユーザーがアイデア検討・方向性を模索している段階

## Problem
ブレインストーミング段階のユーザーに選択肢（AskUserQuestion）を
連発すると、思考を狭められたと感じて拒否される。
「まだ決めてない」「まず説明して」「選択肢を押し付けないで」という
反応が繰り返し発生した。

## Solution
1. 情報を提示する → 選択を迫らず自由に反応させる
2. ユーザーの発言を待つ → その発言に応じて深掘りする
3. 選択肢は「ユーザーが方向性を示した後」に初めて使う
4. 要約ではなく詳細な説明を求められたら、省略せず丁寧に書く

## Anti-Patterns（やってはいけないこと）
- リサーチ結果を出した直後に「どれがいい？」と聞く
- 3-4個の選択肢で方向性を絞ろうとする
- 「まだ決めていない」への対応として別の選択肢を出す

## When to Use
- ユーザーが「考えたい」「検討中」「まだ決めてない」と言っている時
- 新プロジェクトのアイデア出し・方向性検討フェーズ
- ユーザーが自由に思考を広げたい段階
