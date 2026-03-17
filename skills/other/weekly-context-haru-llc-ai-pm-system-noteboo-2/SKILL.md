---
name: weekly-context
description: 週次コンテキストを生成する。NotebookLM連携、週次サマリー自動生成時に使う。
phase: cross-cutting
pmbok-area: communications
---

## 目的

週次の進捗・課題・アクションをNotebookLM等のナレッジベースに連携するためのコンテキストを生成する。

## トリガー語

- 「週次コンテキストを生成」
- 「NotebookLM用サマリー」
- 「今週のまとめを作成」

---

## 入力で最初に聞くこと

| # | 質問 | 必須 |
|---|------|------|
| 1 | **プロジェクト名**は？ | ✓ |
| 2 | **報告期間**は？ | ✓ |

---

## 手順

### Step 1: 週次レポートの収集
### Step 2: 要点の抽出
### Step 3: NotebookLM用フォーマットに変換
### Step 4: 保存
- `workspace/{ProjectName}/context/YYMMDD_weekly_context.md`

---

## 成果物

| 成果物 | 保存先 |
|--------|--------|
| 週次コンテキスト | `workspace/{ProjectName}/context/YYMMDD_weekly_context.md` |

---

## 検証（完了条件）

- [ ] 主要進捗が含まれている
- [ ] リスク・課題が反映されている
- [ ] NotebookLMで読み込み可能

---

## 参照

- Command: `.claude/commands/02_aipjm_06_cross_02_weekly_context.md`
