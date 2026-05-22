---
name: sns-marketing
description: |
  X/Instagram/YouTube/noteのSNSマーケティング運用スキル。4KPI最大化。
  Use when: (1) user says「SNSマーケティング」「X投稿戦略」「Instagram運用」,
  (2) user wants systematic social media marketing,
  (3) user mentions「認知拡大」「リード獲得」「SNS戦略」.
  Do NOT use for: SNSパターン参照のみ（sns-patternsを使用）、
  単発投稿作成（copywriting-helperを使用）。
---

# SNS Marketing Operational Skill System

## 概要

X・Instagram・YouTube・note を対象に、認知・リード・採用・売上の4KPIを最大化するSNSマーケティングを、再現可能なアルゴリズムとして定義し、生成・評価・統制・改善までを自律的かつ安全に運用するスキルシステム。

## ドクトリン（優先順位）

1. **冪等性 (idempotency)** - 同一条件で何度実行しても結果・判断・副作用が破綻しない
2. **説明可能性 (explainability)** - なぜその戦略・生成・却下・改善が行われたかを人間がログから説明できる
3. **ガバナンス強制 (governance_enforcement)** - ルールは「守る」のではなく「破れない」構造で実装する
4. **役割分離 (role_separation)** - 判断・生成・評価・公開を同一主体に集約しない
5. **メトリクス優先 (metrics_first)** - 感想・主観よりメトリクスを優先する
6. **人間オーバーライド (human_override)** - 最終責任は必ず人間が持つ

## 対象プラットフォーム

| Platform | 特徴 | 主要KPI |
|----------|------|---------|
| X (Twitter) | 短文・スレッド・リアルタイム | impressions, engagement_rate |
| Instagram | ビジュアル・ストーリー・リール | reach, saves, engagement_rate |
| YouTube | 動画・検索・アルゴリズム | views, watch_time, subscribers |
| note | 長文記事・有料コンテンツ | views, likes, purchases |

## KPI

| KPI | 日本語 | 説明 |
|-----|--------|------|
| awareness | 認知 | ブランド・サービスの認知度向上 |
| lead | リード | 見込み顧客の獲得 |
| recruitment | 採用 | 人材採用への貢献 |
| sales | 売上 | 直接的な売上・コンバージョン |

## ワークフロー

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Strategist │ → │   Creator   │ → │  Reviewer   │ → │  Publisher  │ → │   System    │
│             │    │             │    │             │    │             │    │             │
│ • 戦略選定  │    │ • コンテンツ │    │ • 品質評価  │    │ • 公開制御  │    │ • メトリクス │
│ • KPI設定   │    │   生成      │    │ • リスク評価│    │ • 権限確認  │    │   収集      │
│ • パターン  │    │ • チェック  │    │ • 承認/却下 │    │ • ログ記録  │    │ • 分析      │
│   選択      │    │   実行      │    │             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
     ↓                  ↓                  ↓                  ↓                  ↓
strategy.json      draft.json         review.json      dispatch_log.json  results.jsonl
```

## コンテンツパターン

| ID | 名称 | 対象Platform | 推奨KPI |
|----|------|--------------|---------|
| educational_thread | 教育的スレッド | X | awareness, lead |
| behind_the_scenes | 舞台裏公開 | Instagram, X | awareness, recruitment |
| value_carousel | 価値提供カルーセル | Instagram | lead, sales |
| long_form_article | 長文記事 | note | awareness, lead, sales |
| short_video_tips | ショート動画Tips | YouTube, Instagram | awareness |

## ディレクトリ構成

```
video-agent/
├── data/sns/
│   ├── drafts/          # 生成されたドラフト
│   ├── approved/        # 承認済みコンテンツ
│   ├── published/       # 公開済み記録
│   ├── rejected/        # 却下されたコンテンツ
│   ├── strategies/      # 戦略定義
│   └── reviews/         # レビュー記録
├── knowledge/sns/
│   ├── platforms.json   # プラットフォーム制約
│   ├── patterns.json    # コンテンツパターン
│   └── risks.json       # リスク定義
├── metrics/sns/
│   └── results.jsonl    # パフォーマンスメトリクス
├── logs/sns/
│   ├── strategy_*.log   # 戦略ログ
│   ├── creator_*.log    # 作成ログ
│   ├── reviewer_*.log   # レビューログ
│   ├── publisher_*.log  # 公開ログ
│   └── workflow_*.log   # ワークフローログ
├── scripts/sns/
│   ├── sns-setup.sh     # セットアップ
│   ├── sns-strategist.sh # 戦略選定
│   ├── sns-creator.sh   # コンテンツ生成
│   ├── sns-reviewer.sh  # 品質レビュー
│   ├── sns-publisher.sh # 公開制御
│   ├── sns-metrics.sh   # メトリクス収集
│   ├── sns-workflow.sh  # ワークフロー統合
│   └── sns-verify.sh    # 検証
└── docs/skills/sns-marketing/
    ├── meta-prompt.yaml # メタプロンプト定義
    └── overview.md      # このドキュメント
```

## 使用方法

### セットアップ

```bash
make sns-setup
make sns-verify
```

### フルワークフロー実行

```bash
# Dry-run（実際には公開しない）
make sns-workflow \
  PLATFORM=x \
  PATTERN=educational_thread \
  KPI=awareness \
  CONTENT="AIエージェント開発の3つのポイント..."

# 実行モード（実際に公開）
make sns-workflow \
  PLATFORM=x \
  PATTERN=educational_thread \
  KPI=awareness \
  CONTENT="..." \
  MODE=execute \
  ROLE=admin
```

### 個別ステップ実行

```bash
# 1. 戦略作成
make sns-strategy \
  PLATFORM=x \
  PATTERN=educational_thread \
  KPI=awareness \
  BRIEF="AIエージェント開発について"

# 2. コンテンツ作成
make sns-create \
  STRATEGY_ID=strategy_x_educational_thread_20241222_123456 \
  CONTENT="スレッド本文..."

# 3. レビュー
make sns-review DRAFT_ID=draft_x_20241222_123456

# 4. 公開
make sns-publish \
  DRAFT_ID=draft_x_20241222_123456 \
  MODE=publish \
  ROLE=admin \
  REASON="定期投稿"
```

### メトリクス確認

```bash
make sns-metrics   # サマリー表示
make sns-analyze   # パフォーマンス分析
make sns-export    # CSV出力
```

## 安全性・倫理ルール

1. **炎上リスクはKPI達成より優先してブロックする**
2. **誤情報・誇張・扇動的表現は禁止**
3. **プラットフォーム規約を常に優先**
4. **自動最適化は無制限に行わない**

## リスクチェック

レビューフェーズで以下をチェック：

| カテゴリ | 重大度 | アクション |
|----------|--------|------------|
| hallucination | critical | reject |
| overclaim | high | reject |
| platform_violation | critical | reject |
| brand_risk | high | reject |
| tone_mismatch | medium | revise |
| sensitivity | critical | reject |

## 成功定義

- **短期**: SNS施策が属人性なく再現可能に回る状態
- **中期**: パターン別KPIの勝ち筋が可視化されている状態
- **長期**: SNSマーケティングが改善可能な経営資産として定着している状態
