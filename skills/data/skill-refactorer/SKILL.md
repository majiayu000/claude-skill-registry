---
name: skill-refactorer
description: |
  SKILL.mdファイルを整理・圧縮するスキル。
  7つのリファクタリングパターンをチェックリストとして適用し、
  SKILL.mdをオーケストレータとして100行未満に圧縮する。

  Trigger:
  スキル整理, SKILL.md圧縮, スキルリファクタ, skill refactor, refactor skill
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# SKILL.md整理（skill-refactorer）

## 7パターン

詳細・チェック項目は [references/patterns.md](.claude/skills/skill-refactorer/references/patterns.md) を、自然に必ず参照。

| # | パターン | 要点 |
|---|----------|------|
| 1 | 圧縮 | 詳細（コード例・実例・基準等）を外部に委譲、100行未満に |
| 2 | DRY化 | 繰り返しを冒頭定義+テーブルに集約 |
| 3 | LLM行動制御 | 「自分でやらない」明示+呼び出しコード |
| 4 | ゲート条件 | 各ステップ末尾にファイル存在チェック |
| 5 | 責務分離 | 詳細をagents/・references/に移し、小タスクも切り出し |
| 6 | 廃止・整理 | 未使用参照・冗長例を削除 |
| 7 | 構造化 | オーケストレータとして再構成 |

---

## 実行手順

### Step 1: 現状分析

1. Read で対象SKILL.mdを読み込む
2. Read で `references/patterns.md` を読み込む
3. **AskUserQuestion** で対象SKILL.mdの問題点をユーザーと共有:
   - 行数、コード例の有無、繰り返し構造、ゲート条件の有無
   - 7パターンのうちどれが該当するかチェックリストで提示

### Step 2: 整理方針の合意

1. 各パターンの適用箇所を具体的に提示
2. **AskUserQuestion** で方針確認:
   - 削除するセクション
   - agents/に切り出すセクション
   - 新規作成するagent.md

### Step 3: 適用

1. SKILL.mdを書き換え（Edit/Write）
2. 必要に応じてagent.mdを新規作成
3. **AskUserQuestion** で結果確認

---

## 完了条件

- [ ] SKILL.mdが100行未満
- [ ] 7パターンのチェック項目をすべて確認済み
- [ ] ユーザーが承認済み
