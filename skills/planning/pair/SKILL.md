---
user-invocable: true
description: "[ペアモード] 壁打ち（企画/設計/実装/デザイン）"
---

# [ペアモード] 壁打ち（企画/設計/実装/デザイン）

## 入力: $ARGUMENTS
- モード（必須）: `plan` | `design` | `arch` | `dev`
- 任意: 相談内容（1文でOK）

例:
    plan 新規プロダクトのMVPを決めたい
    design 設定画面の情報設計を壁打ちしたい
    arch 認証基盤の境界をどう切るか相談したい
    dev バグ修正方針と最小テストを一緒に決めたい

---

## 🎯 目的
- 実装前/実装中の意思決定を、短い反復で安全に前進させる
- 推測で断言せず、前提・選択肢・トレードオフを言語化する

---

## 共通前提（参照）
- 口調・出力規約は `CLAUDE.md` に従う。
- プロジェクト固有の事実は `doc/input/rdd.md`（先頭のAI用事実ブロック）を参照する。
- 詳細運用（ADR-lite等）は `doc/guide/ai_guidelines.md` を参照。

---

## モード別の適用skill（ガイド）
- `plan`: `biz-researcher` / `proposition-reviewer` / `persona-designer`
- `design`: `ui-designer` / `usability-psychologist` / （必要なら）`creative-coder`
- `arch`: `architecture-expert` / `security-expert`
- `dev`: `developer-specialist` / （必要なら）`security-expert` / （UI実装なら）`frontend-implementation`

---

## 進め方（固定）
1. まず不足情報を短問で確認（1〜3問）
2. 選択肢を2〜3案提示（トレードオフつき）
3. 推奨案と理由
4. 次の一手（最小タスク 2〜3件）
