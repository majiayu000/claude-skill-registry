---
name: handover
description: 保守・運用引継ぎ書を作成する。運用移行、引き継ぎ時に使う。
phase: closing
pmbok-area: integration
---

## 目的

プロジェクト成果物の保守・運用に必要な情報を引き継ぐ。

## トリガー語

- 「引継ぎ書を作成」
- 「運用移行ドキュメント」
- 「ハンドオーバー」

---

## 入力で最初に聞くこと

| # | 質問 | 必須 |
|---|------|------|
| 1 | **プロジェクト名**は？ | ✓ |
| 2 | **引継ぎ先**は？ | ✓ |

---

## 手順

### Step 1: 引継ぎ対象の整理
### Step 2: 運用手順書の作成
### Step 3: 連絡先・エスカレーションパスの整理
### Step 4: 保存
- `workspace/{ProjectName}/docs/Handover.md`

---

## 成果物

| 成果物 | 保存先 |
|--------|--------|
| 引継ぎ書 | `workspace/{ProjectName}/docs/Handover.md` |

---

## 検証（完了条件）

- [ ] 全成果物が一覧化されている
- [ ] 運用手順が記載されている
- [ ] 連絡先が明記されている

---

## 参照

- Command: `.claude/commands/02_aipjm_05_closing_02_handover.md`
