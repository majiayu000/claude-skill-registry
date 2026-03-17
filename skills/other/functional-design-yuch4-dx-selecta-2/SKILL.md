---
name: functional-design
description: PRD（プロダクト要求定義書）から機能設計書（docs/functional-design.md）を作成する。「機能設計して」「設計書を作って」「PRDを設計に落として」「コンポーネント設計」「データモデル設計」「シーケンス図を書いて」「ER図を作って」などの依頼時に使用。システム構成図・データモデル・コンポーネント責務・ユースケースフロー・エラー設計を出力。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Functional Design Skill

PRD（何を作るか）を設計（どう実現するか）に落とし込む。

## 入出力

| 種別 | パス |
|------|------|
| 入力 | `docs/product-requirements.md`（必須） |
| 入力 | `docs/functional-design.md`（既存あれば優先） |
| 出力 | `docs/functional-design.md` |

## 参照ファイル

| ファイル | 読むタイミング |
|----------|----------------|
| `references/template.md` | 新規作成時のベース |
| `references/guide.md` | 必須項目・レビュー観点の確認時 |

## 手順

### 1. PRD読解
`docs/product-requirements.md` を読み、以下を抽出：
- P0（MVP）機能の要件・受け入れ条件
- ターゲットユーザーのワークフロー
- 成功指標（KPI）
- 非機能要件（あれば）

### 2. 既存設計の確認
- `docs/functional-design.md` が存在する？
  - **Yes** → 構造を維持して差分更新
  - **No** → `references/template.md` をコピーして新規作成

### 3. 設計項目の作成

P0機能ごとに以下を埋める（詳細は `references/guide.md` 参照）：

| 項目 | 形式 | 必須 |
|------|------|------|
| システム構成図 | Mermaid graph TB | ✅ |
| データモデル | TypeScript interface | ✅ |
| ER図 | Mermaid erDiagram | 複数エンティティ時 |
| コンポーネント設計 | 責務・インターフェース | ✅ |
| ユースケースフロー | Mermaid sequenceDiagram | ✅ |
| エラーハンドリング | 表形式 | ✅ |
| アルゴリズム設計 | 計算式・実装例 | 複雑ロジック時 |
| API設計 | エンドポイント定義 | Web API時 |
| 画面遷移 | Mermaid stateDiagram | UI有時 |

### 4. PRDとのトレーサビリティ確保
- 各設計セクションに「対応するPRD機能」を明記
- 例: `## 診断機能の設計（PRD: 1. 診断）`

### 5. セルフレビュー

`references/guide.md` のレビュー観点でチェック：
- [ ] PRD P0要件をすべてカバーしているか
- [ ] データモデルに型・制約・nullable が明記されているか
- [ ] Mermaidに実コンポーネント名が入っているか
- [ ] エラーハンドリングが網羅されているか

### 6. 出力
`docs/functional-design.md` を作成/更新し、変更点をサマリ提示

## 境界（やらないこと）
- **要件定義** → `prd-writing` スキル
- **技術選定の深い根拠** → `architecture-design` スキル
- **実装** → 開発タスクとして別途実施
