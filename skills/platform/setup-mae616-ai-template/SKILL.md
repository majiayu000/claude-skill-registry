---
user-invocable: true
description: "[セットアップ] 前提の読み込み（推奨）"
---

# [セットアップ] 前提の読み込み（推奨）

まず `CLAUDE.md` を読み込み、全体規約（口調/出力/調査/TDD/セキュリティ等）を把握してください。

次に `doc/input/rdd.md`（先頭のAI用事実ブロック）を読み、技術スタックや制約に応じて `.claude/skills/*` を選択・併用してください。

詳細運用（サンプル運用/依存評価補助/ADR-lite）は `doc/guide/ai_guidelines.md` を参照してください。

## デザイン作業（Figma）をする場合の追加前提
- `/design-ssot` を使う場合、Figma MCP（Dev Mode）が利用可能である必要がある。
- 迷ったら `claude mcp list` を確認し、`figma` が登録されていることを確かめる（未登録/未起動なら `/design-ssot` の事前チェック手順に従う）。
