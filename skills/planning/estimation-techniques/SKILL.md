---
name: estimation-techniques
description: |
  ストーリーポイント、プランニングポーカー、相対見積もりを用いたアジャイル見積もり技法。
  チーム合意に基づく予測可能性と柔軟性を両立する見積もりプロセスを実践する。

  Anchors:
  • Agile Estimating and Planning (Mike Cohn) / 適用: 見積もり手法全般 / 目的: ストーリーポイント理論
  • Scrum Guide / 適用: スプリント計画 / 目的: ベロシティ運用
  • Planning Poker実践ガイド / 適用: セッション進行 / 目的: アンカリング防止

  Trigger:
  Use when estimating user stories, running planning poker sessions, tracking velocity, or improving estimation accuracy.
  見積もり, ストーリーポイント, プランニングポーカー, ベロシティ, 相対見積もり, スプリント計画, 工数見積もり

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 見積もり技法スキル

## 概要

アジャイル開発における見積もり技法を体系化したスキル。Mike Cohnの理論に基づき、ストーリーポイント、プランニングポーカー、ベロシティ追跡を一貫したプロセスとして実践する。

## ワークフロー

### Phase 1: 見積もり計画

**目的**: 見積もりセッションの準備と設計

**アクション**:

1. プロジェクトコンテキストを分析
2. 見積もり手法を選定（Planning Poker、T-Shirt Sizing等）
3. 見積もりスケールを決定（フィボナッチ数列）
4. 基準ストーリーを選定
5. セッション計画を策定

**Task**: `agents/estimation-planning.md` を参照

### Phase 2: プランニングポーカー実施

**目的**: チーム合意に基づく見積もりの実行

**アクション**:

1. セッション開始（ルール説明）
2. ストーリー説明と質疑応答
3. 独立思考と同時開示
4. 差異の議論と再見積もり
5. 合意形成と結果記録

**Task**: `agents/poker-facilitation.md` を参照

### Phase 3: ベロシティ追跡

**目的**: チームの見積もり精度とキャパシティ把握

**アクション**:

1. スプリント完了ポイントを記録
2. ベロシティのトレンド分析
3. 予測可能性の評価
4. 見積もり精度の計測

**Task**: `agents/velocity-tracking.md` を参照

### Phase 4: 不確実性管理

**目的**: 見積もりの不確実性を可視化・管理

**アクション**:

1. 確信度の評価
2. コーン・オブ・アンサータンティの適用
3. リスク・バッファの設定
4. 再見積もりの判断

**Task**: `agents/uncertainty-management.md` を参照

## Task仕様（ナビゲーション）

| Task                   | 起動タイミング | 入力                     | 出力                   |
| ---------------------- | -------------- | ------------------------ | ---------------------- |
| estimation-planning    | Phase 1開始時  | プロジェクトコンテキスト | 見積もり計画書         |
| poker-facilitation     | Phase 2開始時  | 見積もり計画書           | 見積もり済みバックログ |
| velocity-tracking      | Phase 3開始時  | スプリント実績           | ベロシティレポート     |
| uncertainty-management | Phase 4開始時  | 見積もりデータ           | 不確実性レポート       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- フィボナッチ数列（1, 2, 3, 5, 8, 13, 21）を使用
- 基準ストーリーを常に参照可能に
- 同時開示でアンカリングを防止
- 大きな差異（3段階以上）は必ず議論
- ベロシティは3スプリント以上の平均を使用

### 避けるべきこと

- 時間単位での見積もり（相対値を使う）
- 個人の見積もりを強制
- 過去の見積もり値への固執
- ベロシティの無理な増加目標
- 見積もり精度の個人責任化

## リソース参照

### references/（詳細知識）

| リソース             | パス                                                                     | 用途                 |
| -------------------- | ------------------------------------------------------------------------ | -------------------- |
| 見積もり手法ガイド   | See [references/estimation-methods.md](references/estimation-methods.md) | 手法選定と基準       |
| ベロシティ追跡ガイド | See [references/velocity-guide.md](references/velocity-guide.md)         | メトリクス運用       |
| 不確実性管理ガイド   | See [references/uncertainty-guide.md](references/uncertainty-guide.md)   | リスク・バッファ設計 |

### scripts/（決定論的処理）

| スクリプト      | 用途               | 使用例                                        |
| --------------- | ------------------ | --------------------------------------------- |
| `log_usage.mjs` | フィードバック記録 | `node scripts/log_usage.mjs --result success` |

### assets/（テンプレート）

| テンプレート              | 用途                 |
| ------------------------- | -------------------- |
| `estimation-worksheet.md` | 見積もりワークシート |
| `velocity-tracker.md`     | ベロシティ追跡シート |

## 変更履歴

| Version | Date       | Changes                            |
| ------- | ---------- | ---------------------------------- |
| 2.0.0   | 2026-01-01 | 18-skills.md完全準拠版として再構築 |
| 1.1.0   | 2025-12-24 | 初版作成                           |
