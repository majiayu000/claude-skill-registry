---
name: .claude/skills/database-seeding/SKILL.md
description: |
  旧版のdatabase-seedingスキル概要。開発/テスト/本番の初期データ投入、環境分離、
  シード戦略の整理を目的としていた。

  旧リソース:
  - `.claude/skills/database-seeding/references/seed-strategies.md`
  - `.claude/skills/database-seeding/references/data-generation.md`
  - `.claude/skills/database-seeding/references/environment-separation.md`
  - `.claude/skills/database-seeding/assets/seed-file-template.ts`

  Use only for compatibility checks with legacy outputs.
---

# 旧スキルメモ

## 概要

旧版は「シード戦略の選定」「環境分離」「テストデータ生成」の3点を中心に整理していた。
新構成ではPhase分割と検証フローを明確化して再構成済み。

## 旧ワークフロー要約

1. シード対象の整理
2. 戦略選定と環境分離
3. シード実装と検証

## 参照メモ

- 旧版の詳細は `references/seed-strategies.md` と `references/data-generation.md` に反映済み。
- 旧テンプレートは `assets/seed-file-template.ts` に移行済み。
