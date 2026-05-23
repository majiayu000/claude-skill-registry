---
name: instruction-clarity
description: |
  曖昧な指示を明確・具体的・実行可能な形式へ変換するスキル。「適切に」「よろしく」といった不明瞭な表現を、測定可能な成功基準と段階的ステップへ分解します。

  Anchors:
  • Made to Stick (Heath) / 適用: 簡潔性・具体性の原則 / 目的: 記憶に残る指示設計
  • The Pyramid Principle (Minto) / 適用: 論理構造 / 目的: 結論先行による理解速度向上
  • 5C Principle / 適用: 品質評価 / 目的: Clear, Concise, Complete, Concrete, Correct

  Trigger:
  Use when instructions contain vague terms like "appropriately", "properly", "handle", or when steps lack clear success criteria. Apply before creating prompts, requirements, runbooks, or directive documentation.
  instruction clarity, vague expression, 5C principle, pyramid principle, success criteria
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
---

# 指示明瞭化

## 概要

曖昧な指示を明確・具体的・実行可能な形式へ変換。5C原則とPyramid Principleを用いて、実行者が「次に何をすべきか」を即座に理解できる状態を作ります。

## ワークフロー

### Phase 1: 指示の診断

**Objective**: 5C原則で現状を評価し、不足要素を特定

**Actions**:

1. Run: `node scripts/analyze-instruction.mjs --input <file>`
2. Invoke Task: `agents/diagnose-instruction-quality.md`
3. Reference: `references/basics.md`

**Outputs**: 診断レポート（曖昧箇所・不足要素一覧）

### Phase 2: 明瞭化と再構成

**Objective**: 5C原則を満たす指示へ再構成

**Actions**:

1. Invoke Task: `agents/restructure-instruction.md`
2. Use template: `assets/instruction-template.md`
3. Reference: `references/patterns.md`

**Outputs**: 再構成された指示（結論先行・成功基準付き）

### Phase 3: 検証

**Objective**: 変換後の指示が実行可能か確認

**Actions**:

1. Invoke Task: `agents/validate-instruction-clarity.md`
2. Use checklist: `assets/instruction-checklist.md`
3. Run: `node scripts/log_usage.mjs --result success --phase complete`

**Outputs**: 検証済み指示

## Task仕様ナビ

| Task File                                | When to Use | Inputs       | Outputs      |
| ---------------------------------------- | ----------- | ------------ | ------------ |
| `agents/diagnose-instruction-quality.md` | Phase 1     | 元の指示文   | 診断レポート |
| `agents/restructure-instruction.md`      | Phase 2     | 診断レポート | 再構成指示   |
| `agents/validate-instruction-clarity.md` | Phase 3     | 再構成指示   | 検証済み指示 |

## ベストプラクティス

### すべきこと

- 5C診断を実施してから改善に着手
- 結論先行（Pyramid Principle）で構造化
- 各ステップに成功基準と検証方法を追加
- 実行者のコンテキストを考慮
- 曖昧語を数値・具体例に置換

### 避けるべきこと

- 診断をスキップして直接書き直す
- 元の意図を無視して過度に詳細化
- 成功基準なしで「明確にした」と判断
- 実行者の前提知識を考慮しない

## リソース参照

### 参照資料

| Resource | Path                                                 | Purpose      |
| -------- | ---------------------------------------------------- | ------------ |
| Basics   | See [references/basics.md](references/basics.md)     | 5C原則と基礎 |
| Patterns | See [references/patterns.md](references/patterns.md) | 実務パターン |

### スクリプト

| Script                    | Usage                                                          | Purpose        |
| ------------------------- | -------------------------------------------------------------- | -------------- |
| `analyze-instruction.mjs` | `node scripts/analyze-instruction.mjs --input <file>`          | 曖昧性自動検出 |
| `log_usage.mjs`           | `node scripts/log_usage.mjs --result success --phase complete` | 使用記録       |

### アセット

| Template                   | Purpose              |
| -------------------------- | -------------------- |
| `instruction-template.md`  | 標準指示フォーマット |
| `instruction-checklist.md` | 5C品質チェックリスト |

## 変更履歴

| Version | Date       | Changes                        |
| ------- | ---------- | ------------------------------ |
| 1.1.0   | 2026-01-02 | 18-skills.md仕様準拠、構造改善 |
| 1.0.0   | 2025-12-31 | 初版作成                       |
