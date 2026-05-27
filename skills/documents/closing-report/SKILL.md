---
name: closing-report
description: 終結報告書を作成する。プロジェクト完了時の最終報告、振り返り時に使う。
phase: closing
pmbok-area: integration
---

## 目的

プロジェクトの成果・教訓を文書化し、正式に終結する。

## トリガー語

- 「終結報告書を作成」
- 「プロジェクト完了報告」
- 「クロージングレポート」

---

## 入力で最初に聞くこと

| # | 質問 | 必須 |
|---|------|------|
| 1 | **プロジェクト名**は？ | ✓ |
| 2 | **完了日**は？ | ✓ |

---

## 手順

### Step 1: 成果物の確認
### Step 2: 目標達成度の評価
### Step 3: 教訓のまとめ
### Step 4: 保存
- `workspace/{ProjectName}/docs/ClosingReport.md`

---

## 成果物

| 成果物 | 保存先 |
|--------|--------|
| 終結報告書 | `workspace/{ProjectName}/docs/ClosingReport.md` |

---

## 検証（完了条件）

- [ ] 全成果物が納品済み
- [ ] 目標達成度が評価されている
- [ ] 教訓が記録されている
- [ ] ステークホルダー承認を得ている

---

## 参照

- Command: `.claude/commands/02_aipjm_05_closing_01_closing_report.md`
