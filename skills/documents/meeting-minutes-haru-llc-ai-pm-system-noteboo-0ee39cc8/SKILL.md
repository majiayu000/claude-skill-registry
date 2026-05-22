---
name: meeting-minutes
description: PMBOK準拠の定例議事録を作成する。会議後の議事録作成、アクションアイテム整理時に使う。
phase: executing
pmbok-area: communications
---

## 目的

定例会議の内容を構造化し、意思決定・アクションアイテム・リスクを明確に記録する。

## トリガー語

- 「議事録を作成」
- 「会議のメモを整理」
- 「定例会議の記録」
- 「ミーティングノートを作成」

---

## 入力で最初に聞くこと

| # | 質問 | 必須 |
|---|------|------|
| 1 | **プロジェクト名**は？ | ✓ |
| 2 | **会議名称**は？（例: 第N回 定例会議） | ✓ |
| 3 | **会議日**は？ | ✓ |
| 4 | **参加者**は？ | - |
| 5 | **アジェンダ**は？ | - |

---

## 手順

### Step 1: 基本情報の確認
- プロジェクト名、会議名称、会議日を確認

### Step 2: 議事録の生成
- 12セクション構成で生成
- Decision Log、Action Items、RAIDを明確化

### Step 3: アクションアイテムの整理
- SMART原則でタスクを記載
- RACI（責任分担）を明記

### Step 4: 保存
- `workspace/{ProjectName}/docs/minutes/YYYYMMDD_議事録.md` に保存

---

## 成果物

| 成果物 | 保存先 |
|--------|--------|
| 定例議事録 | `workspace/{ProjectName}/docs/minutes/YYYYMMDD_議事録.md` |

---

## 検証（完了条件）

- [ ] 日時・参加者が記載されている
- [ ] 意思決定事項がDecision Logに記録されている
- [ ] アクションアイテムに担当・期限が設定されている
- [ ] 次回会議の予定が記載されている

---

## 参照

- Command: `.claude/commands/02_aipjm_03_executing_01_minutes.md`
