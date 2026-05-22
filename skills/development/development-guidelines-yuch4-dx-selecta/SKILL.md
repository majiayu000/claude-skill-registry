---
name: development-guidelines
description: プロジェクトの開発ガイドライン（docs/development-guidelines.md）を新規作成/更新する。既存の開発ガイドラインがある場合は最優先し、構造と方針を維持して更新する。内容は「コーディング規約（implementation.md）」と「開発プロセス（process.md）」の2本立てで、具体例と理由、測定可能な基準を含める。
---

# Development Guidelines Skill（骨格）

## 前提（推奨）
- `docs/architecture.md`（技術スタック）
- `docs/repository-structure.md`（ディレクトリ構造）

## 既存ドキュメント優先順位（重要）
1. 既存 `docs/development-guidelines.md`（最優先：構造・方針を維持して更新）
2. このスキルのガイド（補助）

## 参照（同ディレクトリ）
- `./implementation.md`（コーディング規約の詳細）
- `./process.md`（Git運用/テスト/レビュー/自動化など）
- `./template.md`（docs出力テンプレ）

## 入出力
- 出力: `docs/development-guidelines.md` 

## 手順（骨格）
1. 既存 `docs/development-guidelines.md` があれば先に読む（構造維持）
2. 無い場合は `./template.md` で骨組みを作る
3. `docs/architecture.md` / `docs/repository-structure.md` と整合させる
4. `./implementation.md` と `./process.md` の要点を反映し、プロジェクト向けに具体化する 
5. 最終チェック（観点は reference.md を参照）