---
name: directory-structure-enforcement-hooks
description: "Use when Claude Code creates files in wrong locations despite CLAUDE.md rules. PreToolUse + Stop hook 3-layer defense."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-13"
---
# Directory Structure Enforcement via Hooks

**Extracted:** 2026-02-13
**Context:** Claude Code hooks を使ってディレクトリ構造ルールを自動強制する

## Problem
Claude が docs/ に間違った場所・命名でファイルを作るドリフトを防止したい。
CLAUDE.md にルールを書いても守られないことがある。

## Solution
3層防御:

1. **PreToolUse hook** (`docs-prewrite.sh`): Write/Edit 時にリアルタイムでバリデーション
   - exit 0 = 許可、exit 2 = ブロック、stderr = 警告
   - stdin から JSON を読み、`tool_input.file_path` を検査

2. **Stop hook** (`driftcheck.sh`): セッション終了時に全体スキャン
   - mv や外部プロセスによる変更も捕捉
   - 常に exit 0（セッション終了をブロックしない）

3. **hooks.json matcher 除外**: 既存の汎用ブロッカーと競合しないよう除外条件を追加

## Key Design Decisions
- ブロック (exit 2) vs 警告 (stderr + exit 0) を違反の深刻度で使い分ける
- 許可リストはスクリプト内にハードコード（設定ファイルを増やさない）
- driftcheck は常に exit 0 でセッション終了を妨げない

## When to Use
- プロジェクトにディレクトリ構造ルールがあるとき
- Claude が勝手にファイルを作る問題が繰り返されるとき
