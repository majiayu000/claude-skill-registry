---
name: quality-plan
description: 品質マネジメント計画書を作成する。品質基準、品質保証計画の策定時に使う。
phase: planning
pmbok-area: quality
---

## 目的

プロジェクトの品質基準・品質保証・品質管理のアプローチを定義する。

## トリガー語

- 「品質計画を作成」
- 「品質管理計画を策定」
- 「QMS計画」

---

## 入力で最初に聞くこと

| # | 質問 | 必須 |
|---|------|------|
| 1 | **プロジェクト名**は？ | ✓ |
| 2 | **品質基準**は？（社内規程/ISO等） | - |

---

## 手順

### Step 1: 品質目標の定義

### Step 2: 品質メトリクスの設定

### Step 3: 品質保証活動の計画

### Step 4: 品質管理活動の計画

### Step 5: 保存
- `workspace/{ProjectName}/docs/QualityPlan.md`

---

## 成果物

| 成果物 | 保存先 |
|--------|--------|
| 品質計画書 | `workspace/{ProjectName}/docs/QualityPlan.md` |

---

## 検証（完了条件）

- [ ] 品質目標が測定可能
- [ ] 品質メトリクスが定義されている
- [ ] レビュープロセスが明記されている

---

## 参照

- Command: `.claude/commands/02_aipjm_02_planning_09_quality_plan.md`
