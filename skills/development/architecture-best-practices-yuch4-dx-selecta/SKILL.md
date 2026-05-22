---
name: architecture-best-practices
description: >
  プロジェクトで使用しているアーキテクチャの実装ベストプラクティスを調査し、
  docs/best-practices.md にドキュメント化する。技術スタックを自動検出し、
  スタック別のベストプラクティス（コード例・アンチパターン）を出力する。
  「ベストプラクティスをまとめて」「実装パターンを調べて」「コーディングガイドを作成」
  「アーキテクチャの使い方を整理」などの依頼時に発火。
---

# Architecture Best Practices Skill

プロジェクトの技術スタックを検出し、対応する実装ベストプラクティスをドキュメント化する。

## 入出力

| 種別 | パス |
|------|------|
| 入力 | `package.json`, `*.config.*`, `docs/architecture.md` |
| 出力 | `docs/best-practices.md` |

## 参照ファイル

| ファイル | 読むタイミング |
|----------|----------------|
| `./template.md` | 出力時のベース |
| `./references/nextjs-app-router.md` | Next.js App Router 検出時 |
| `./references/supabase.md` | Supabase 検出時 |
| `./references/integration.md` | 複数スタック統合パターン |

## 手順

### 1. 技術スタック検出

以下から技術スタックを特定：
- `package.json` の dependencies/devDependencies
- 設定ファイル（`next.config.*`, `supabase/config.toml` 等）
- `docs/architecture.md`（あれば）
- 既存の `.github/instructions/*.instructions.md`

### 2. 該当する references を読み込む

| スタック | Reference |
|----------|-----------|
| Next.js App Router | `./references/nextjs-app-router.md` |
| Supabase | `./references/supabase.md` |
| 複合 | `./references/integration.md` |

### 3. プロジェクト固有のカスタマイズ

- 既存 instructions との整合性確認
- プロジェクト固有のパターンを抽出
- ディレクトリ構造に合わせたパス例

### 4. ドキュメント生成

`./template.md` をベースに `docs/best-practices.md` を作成:
- 検出したスタック別にセクション構成
- 各パターンに ✅ 推奨例 / ❌ アンチパターン
- 具体的なコード例を含める

## 発火例

- 「ベストプラクティスをまとめて」
- 「実装パターンを整理して」
- 「コーディングガイドを作成して」
- 「Next.jsの使い方をドキュメント化」
- 「Supabaseの実装例をまとめて」

## 境界（やらないこと）

- **アーキテクチャ設計** → `architecture-design` スキル
- **コーディング規約（リント・フォーマット）** → `development-guidelines` スキル
- **新技術の選定** → 要件に応じて別途検討
