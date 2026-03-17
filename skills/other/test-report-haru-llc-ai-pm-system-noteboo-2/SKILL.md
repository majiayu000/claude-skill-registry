---
name: test-report
description: テスト結果報告書を作成する。テスト完了後の結果報告、品質レビュー時に使う。
phase: executing
pmbok-area: quality
---

## 目的

実施したテストの結果を報告し、品質状況を可視化する。

## トリガー語

- 「テスト報告書を作成」
- 「テスト結果をまとめる」
- 「QAレポート」

---

## 入力で最初に聞くこと

| # | 質問 | 必須 |
|---|------|------|
| 1 | **プロジェクト名**は？ | ✓ |
| 2 | **テスト種別**は？ | ✓ |
| 3 | **テスト期間**は？ | - |

---

## 手順

### Step 1: テスト実行結果の集計
### Step 2: 欠陥分析
### Step 3: 品質判定
### Step 4: 保存
- `workspace/{ProjectName}/docs/TestReport_YYYYMMDD.md`

---

## 成果物

| 成果物 | 保存先 |
|--------|--------|
| テスト結果報告書 | `workspace/{ProjectName}/docs/TestReport_YYYYMMDD.md` |

---

## 検証（完了条件）

- [ ] テスト件数/合否が記載されている
- [ ] 欠陥一覧がある
- [ ] 品質判定結果が明記されている

---

## 参照

- Command: `.claude/commands/02_aipjm_03_executing_02_test_report.md`
