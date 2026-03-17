---
name: development-guidelines
description: プロジェクトの開発ガイドライン（docs/development-guidelines.md）を新規作成/更新する。「コーディング規約を作って」「開発ルールを整理」「コード規約」「レビューガイドライン」「テスト方針を決めて」などの依頼時に使用。コーディング規約と開発プロセスの2本立てで、具体例と理由、測定可能な基準を含める。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Development Guidelines Skill

プロジェクトの開発ガイドラインを整備する。

## 前提（推奨）
- `docs/architecture.md`（技術スタック）
- `docs/repository-structure.md`（ディレクトリ構造）

## 既存ドキュメント優先順位
1. 既存 `docs/development-guidelines.md`（最優先：構造・方針を維持して更新）
2. このスキルのガイド（補助）

## 入出力

| 種別 | パス |
|------|------|
| 入力 | `docs/architecture.md` |
| 入力 | `docs/repository-structure.md` |
| 入力 | `docs/development-guidelines.md`（既存あれば優先） |
| 出力 | `docs/development-guidelines.md` |

## 参照ファイル

| ファイル | 読むタイミング |
|----------|----------------|
| `references/template.md` | 新規作成時のベース |
| `references/guide.md` | 詳細ルール・レビュー観点 |

## 手順

### 1. 既存ドキュメント確認
既存 `docs/development-guidelines.md` があれば先に読む（構造維持）

### 2. 新規作成の場合
`references/template.md` で骨組みを作る

### 3. 整合性確認
`docs/architecture.md` / `docs/repository-structure.md` と整合させる

### 4. ガイドライン作成

| セクション | 内容 | 必須 |
|-----------|------|------|
| コーディング規約 | 命名・フォーマット・型定義 | ✅ |
| エラーハンドリング | Result型・例外処理方針 | ✅ |
| テストガイドライン | Unit/Integration/E2E方針 | ✅ |
| Git運用 | ブランチ戦略・コミットルール | ✅ |
| コードレビュー | レビュー観点・承認基準 | ✅ |
| CI/CD | 自動化パイプライン | ✅ |

### 5. 品質チェック
`references/guide.md` のチェックリストで確認

## 境界（やらないこと）
- **技術選定** → `architecture-design` スキル
- **ディレクトリ構造** → `repository-structure` スキル
- **要件定義** → `prd-writing` スキル
