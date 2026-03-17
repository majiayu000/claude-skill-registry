---
name: skill-stocktaking-process
description: "Use when learned skills exceed 10 per location or need consolidation. 4-step stocktaking with character budget awareness."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-09"
---

# Skill Lifecycle Management

**Extracted:** 2026-02-09 (expanded 2026-02-10)
**Context:** スキル/コマンドの監査・整理・無効化・復活の完全ワークフロー

## Architecture Constraints

### Character Budget (CRITICAL)
- `available_skills` セクション: コンテキストウィンドウの **2% (~16,000文字)**
- 各スキル: ~109文字 XML overhead + description長
- 超過時: **警告なしで切り捨て** (GitHub #13099: 63スキル中42個のみ表示)
- 目安: 60+スキル → description 130文字以下

### Progressive Disclosure (3段階ローディング)
1. **Discovery**: name + description のみ (~30-50 tokens/skill)
2. **Activation**: タスク関連時に SKILL.md 全文を読み込み
3. **Deep refs**: 参照ファイルを必要時に読み込み
- `learned/` の plain markdown は progressive disclosure が効かない可能性あり → YAML frontmatter 必須

### Skills vs Commands
| 種別 | 場所 | 無効化方法 |
|------|------|-----------|
| Skills | `~/.claude/skills/` | `disable-model-invocation: true` in SKILL.md |
| Commands | `~/.claude/commands/` | `~/.claude/commands-archive/` に移動 |
| Learned | `~/.claude/skills/learned/` or `.claude/skills/learned/` | ファイル削除 or 移動 |

**Gotcha:** `commands/disabled/` サブディレクトリは効かない（`disabled:xxx` ネームスペースとして表示される）。必ず `commands/` の外に移動すること。

## 3-Tier Skill Organization

| 層 | パス | 用途 |
|----|------|------|
| Global | `~/.claude/skills/learned/` | 全プロジェクト共通パターン |
| Project | `.claude/skills/learned/` | プロジェクト固有パターン |
| Archive | `~/.claude/commands-archive/` | 退避コマンド |

分離基準:
- そのプロジェクトでしか使わない → Project
- 2+プロジェクトで参照される → Global
- 各層10ファイルで棚卸しトリガー

## Problem: Skill Sprawl

Frequent `/learn` usage creates skill file sprawl:
- Similar skills covering sub-steps of the same pipeline
- Small gotcha files that belong as sections in larger skills
- MEMORY.md references grow, approaching the 200-line system limit
- Character Budget 超過でスキルがサイレント切り捨て

## Solution: 4-Step Stocktaking

### Step 1: Inventory and Classify

Read all files in target `learned/` directory and classify by:
- **Project** (which project produced this skill)
- **Domain** (immutability, LLM pipeline, testing, etc.)
- **Granularity** (full pattern vs. single gotcha/tip)

### Step 2: Identify Consolidation Candidates

| Pattern | Example | Action |
|---------|---------|--------|
| **Sub-step of larger pipeline** | pymupdf extraction is Step 1 of long-doc pipeline | Merge into parent |
| **Small gotcha for a topic** | frozen+slots TypeError is a gotcha for immutable accumulator | Add as "Gotcha" section |
| **Same concept, different language** | Swift immutable models + Python immutable accumulator | Keep separate |
| **Truly distinct concerns** | Cost tracking vs. backward compat | Keep separate |

### Step 3: Execute Consolidation

For each merge:
1. Read the target (larger) skill file
2. Integrate content from the smaller file as a new section
3. Delete the absorbed file
4. Verify no information was lost

### Step 4: Update MEMORY.md

- Remove references to deleted files
- Compress verbose entries (details belong in skill files, not MEMORY.md)
- Verify line count stays well under 200

#### MEMORY.md Compression Rules

| 圧縮ルール | Before | After |
|-----------|--------|-------|
| N行の実装詳細 → 1行の機能要約 | Phase別10行ずつの詳細 | `**Feature**: 1行の要約` |
| 設計思想 → スキルファイル参照 | 原則の詳細説明 | `See skill: xxx.md` + 格言1行 |
| 意思決定 → 結論のみ | 検討経緯10行 | `→ スキップ（理由）` 2行 |
| 修正済み問題 → 削除 | Type Hints修正の詳細 | 削除（コードが真実） |
| 未解決問題 → Active Gotchas | JP tokenization未修正 | 「Active Gotchas」に残す |

**原則:** コードが存在する実装詳細はMEMORY.mdに不要。MEMORY.mdには「現在のセッションで知る必要があること」だけを残す。

## Lifecycle Operations

### 標準スキルの無効化
SKILL.md frontmatter に追加:
```yaml
disable-model-invocation: true
```

### コマンドの退避
```bash
mv ~/.claude/commands/xxx.md ~/.claude/commands-archive/
```

### Learned スキルの YAML frontmatter
```yaml
---
name: skill-name
description: "130文字以内の説明"
user-invocable: false
---
```

### 復活
- スキル: `disable-model-invocation: true` を削除
- コマンド: `commands-archive/` から `commands/` に戻す

## Timing Guidelines

| Trigger | Action |
|---------|--------|
| 10 learned skills per location | Full stocktaking |
| MEMORY.md exceeds 100 lines | Compress and move details to skill files |
| Project phase changes | Remove obsolete findings |
| Same topic has 3+ skill files | Consolidate immediately |
| Quarterly | 全スキルレビュー、3ヶ月未参照を退役検討 |
