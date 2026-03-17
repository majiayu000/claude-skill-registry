---
name: subproject-register
description: サブプロジェクト管理台帳を作成する。プログラム管理、複数プロジェクト管理時に使う。
phase: cross-cutting
pmbok-area: integration
---

## 目的

複数のサブプロジェクトを一元管理し、進捗・リスクを統合的に把握する。

## トリガー語

- 「サブプロジェクト管理台帳を作成」
- 「プロジェクト一覧を整理」
- 「プログラム管理表」

---

## 入力で最初に聞くこと

| # | 質問 | 必須 |
|---|------|------|
| 1 | **プログラム名**は？ | ✓ |
| 2 | **サブプロジェクト一覧**は？ | - |

---

## 手順

### Step 1: サブプロジェクトの登録
### Step 2: 進捗・ステータスの統合
### Step 3: 依存関係の整理
### Step 4: 保存
- `workspace/{ProgramName}/docs/SubprojectRegister.md`

---

## 成果物

| 成果物 | 保存先 |
|--------|--------|
| サブプロジェクト管理台帳 | `workspace/{ProgramName}/docs/SubprojectRegister.md` |

---

## 検証（完了条件）

- [ ] 全サブプロジェクトが登録されている
- [ ] 進捗率が記載されている
- [ ] 依存関係が明記されている

---

## 参照

- Command: `.claude/commands/02_aipjm_06_cross_01_subproject_reg.md`
