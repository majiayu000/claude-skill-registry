---
name: product-vision
description: |
  プロダクトビジョン策定、OKR設定、ロードマップ作成を専門とするスキル。長期的な製品戦略を明確化し、チームとステークホルダーの方向性を一致させます。

  Anchors:
  • Inspired (Marty Cagan) / 適用: プロダクト戦略とビジョン設定 / 目的: 魅力的で実現可能なビジョンの策定
  • Measure What Matters (John Doerr) / 適用: OKRフレームワーク / 目的: 目標設定と成果測定の体系化
  • Product Roadmaps Relaunched (C. Todd Lombardo et al.) / 適用: 戦略的ロードマップ策定 / 目的: 優先順位付けと実行計画の明確化

  Trigger:
  Use when defining product vision, creating vision boards, setting OKRs, building product roadmaps, aligning stakeholders on product strategy, establishing long-term product direction, or facilitating strategic planning sessions.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Product Vision

## 概要

プロダクトビジョンの策定、OKR設定、ロードマップ作成を体系的に支援するスキル。長期的な製品戦略を明確化し、チームとステークホルダーの方向性を統一します。

## ワークフロー

### Phase 1: ビジョン定義

**目的**: 製品の長期的な方向性と価値提案を明確化

**アクション**:

1. 対象製品の現状と目指す姿を整理
2. ユーザー価値と事業価値を特定
3. ビジョンボードを作成
4. `assets/vision-board-template.md` を活用

**Task**: `agents/define-vision.md` を参照

### Phase 2: OKR設定

**目的**: 四半期ごとの目標と成果指標を設定

**アクション**:

1. ビジョンから具体的な目標（Objectives）を導出
2. 測定可能な成果指標（Key Results）を定義
3. `assets/okr-template.md` で構造化
4. `scripts/validate-okr.mjs` で検証

**Task**: `agents/set-okrs.md` を参照

### Phase 3: ロードマップ作成

**目的**: 実装優先順位と時系列計画を策定

**アクション**:

1. OKR達成のための主要イニシアチブを特定
2. 優先順位付けと時期を決定
3. `assets/roadmap-template.md` で可視化
4. 依存関係とリスクを明記

**Task**: `agents/create-roadmap.md` を参照

### Phase 4: ステークホルダー調整

**目的**: チームと経営陣の方向性を統一

**アクション**:

1. ステークホルダーマップを作成
2. レビューセッションを実施
3. フィードバックを反映
4. 合意形成と承認獲得

**Task**: `agents/align-stakeholders.md` を参照

## Task仕様ナビ

| Task               | 起動タイミング | 入力             | 出力            |
| ------------------ | -------------- | ---------------- | --------------- |
| define-vision      | Phase 1開始時  | 製品情報         | ビジョンボード  |
| set-okrs           | Phase 2開始時  | ビジョンボード   | OKRドキュメント |
| create-roadmap     | Phase 3開始時  | OKR              | ロードマップ    |
| align-stakeholders | Phase 4開始時  | 戦略ドキュメント | 承認済み戦略    |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

- ビジョンは簡潔で記憶に残るものにする（1-2文）
- OKRは野心的だが達成可能な目標を設定する（0.7スコアを目指す）
- Key Resultsは測定可能な指標で定義する
- ロードマップは柔軟性を持たせる（日付より順序を重視）
- ステークホルダーを早期に巻き込む
- 定期的にレビューし、必要に応じて調整する

### 避けるべきこと

- 曖昧で解釈の余地が大きいビジョン
- 達成不可能な目標設定
- 測定できないKey Results
- 詳細すぎるロードマップ（機能リスト化）
- 一方的な決定（フィードバック無視）
- 設定後の放置（レビュー無し）

## リソース参照

### references/（詳細知識）

| リソース             | パス                                  | 用途                           |
| -------------------- | ------------------------------------- | ------------------------------ |
| 基礎知識             | `references/basics.md`                | プロダクトビジョンの基礎       |
| ビジョンボード作成   | `references/vision-board.md`          | ビジョンボード作成の詳細ガイド |
| OKRフレームワーク    | `references/okr-framework.md`         | OKR設定の詳細                  |
| ロードマップ策定     | `references/roadmap-planning.md`      | ロードマップ作成の実務指針     |
| ステークホルダー調整 | `references/stakeholder-alignment.md` | 調整と合意形成の方法           |

### assets/（テンプレート）

| テンプレート               | 用途                           |
| -------------------------- | ------------------------------ |
| `vision-board-template.md` | ビジョンボード作成テンプレート |
| `okr-template.md`          | OKR設定テンプレート            |
| `roadmap-template.md`      | ロードマップ作成テンプレート   |

### scripts/（検証・自動化）

| スクリプト           | 用途           | 使用例                                                          |
| -------------------- | -------------- | --------------------------------------------------------------- |
| `validate-okr.mjs`   | OKR構造検証    | `node scripts/validate-okr.mjs path/to/okr.md`                  |
| `log_usage.mjs`      | 使用記録       | `node scripts/log_usage.mjs --result success --phase "Phase 2"` |
| `validate-skill.mjs` | スキル構造検証 | `node scripts/validate-skill.mjs`                               |

## 変更履歴

| Version | Date       | Changes                                        |
| ------- | ---------- | ---------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様に完全準拠、構造を全面的に改善 |
| 1.1.0   | 2025-12-31 | Task仕様ナビ追加、ベストプラクティス充実化     |
| 1.0.0   | 2025-12-30 | 初版作成                                       |
