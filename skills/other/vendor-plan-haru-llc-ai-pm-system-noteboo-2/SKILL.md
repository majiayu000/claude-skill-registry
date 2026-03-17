---
name: vendor-plan
description: ベンダー管理計画書を作成する。調達計画、外注管理計画の策定時に使う。
phase: planning
pmbok-area: procurement
---

## 目的

外部ベンダーの選定・管理・評価の方針を定義する。

## トリガー語

- 「ベンダー計画を作成」
- 「調達計画を策定」
- 「外注管理計画」

---

## 入力で最初に聞くこと

| # | 質問 | 必須 |
|---|------|------|
| 1 | **プロジェクト名**は？ | ✓ |
| 2 | **調達対象**は？ | - |

---

## 手順

### Step 1: 調達スコープの定義

### Step 2: ベンダー選定基準の策定

### Step 3: 管理・評価プロセスの定義

### Step 4: 保存
- `workspace/{ProjectName}/docs/VendorPlan.md`

---

## 成果物

| 成果物 | 保存先 |
|--------|--------|
| ベンダー計画書 | `workspace/{ProjectName}/docs/VendorPlan.md` |

---

## 検証（完了条件）

- [ ] 調達対象が明確
- [ ] 選定基準が定義されている
- [ ] 評価プロセスが明記されている

---

## 参照

- Command: `.claude/commands/02_aipjm_02_planning_10_vendor_plan.md`
