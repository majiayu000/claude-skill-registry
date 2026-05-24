---
name: dr-synthesize
description: >
  dr-explore が作った run（evidence.jsonl / sources）を検証・統合して、
  レポート（report.md）と実装計画（implementation_plan.md）を作る。
disable-model-invocation: true
argument-hint: "[run_path] | focus=summary|decision|implementation | audience=internal|external"
allowed-tools: Read, Write, Grep, Glob, Bash(python:*)
---

# dr-synthesize (ultrathink)

## 目的
- dr-explore で収集した証拠を検証・統合し、意思決定可能なレポートを作る
- 実装が必要な場合は implementation_plan.md を生成する
- 矛盾・不確実性・未解決論点を明示する

## 入力

| パラメータ | 説明 | デフォルト |
|-----------|------|-----------|
| run_path | runディレクトリのパス | 最新run |
| focus | summary/decision/implementation | summary |
| audience | internal/external | internal |

## 実行手順

### Step 1: runディレクトリの検証
```bash
# 必須ファイルの存在確認
research/runs/<run>/
├── input.yaml        # 必須
├── evidence.jsonl    # 必須
└── sources/          # 推奨
```

### Step 2: 証拠の分析

1. `input.yaml` と `evidence.jsonl` を読み、調査目的と範囲を復元
2. 主張をグループ化し、支持する証拠IDを紐付け
3. 矛盾する証拠を特定し、`contradictions` として記録
4. 信頼度の低い証拠（score <= 2）は補足情報として扱う
5. 未検証の主張は `predictions` として残し、断定しない

### Step 3: report.md 生成

```markdown
# [topic] 調査レポート

## Executive Summary
- 調査目的
- 主要発見（3-5点）
- 推奨アクション

## Key Findings

### 発見1: [タイトル]
**主張**: ...

**根拠**:
- [ev-001] URL - 引用
- [ev-003] URL - 引用

**信頼度**: 高/中/低
**注記**: ...

### 発見2: ...

## Evidence Table

| ID | Type | URL | 要旨 | 信頼度 |
|----|------|-----|------|--------|
| ev-001 | docs | ... | ... | 5 |
| ev-002 | news | ... | ... | 4 |

## Contradictions & Unknowns

### 矛盾点
- [ev-005] vs [ev-008]: ...

### 未解決論点
- Q1: ...
- Q2: ...

### 予測（未検証）
- P1: ... （根拠: ev-010）

## Recommendations
1. [検証可能なアクション]
2. [検証可能なアクション]

## Next Steps
- 追加取得すべき一次情報
- 検証が必要な仮説
```

### Step 4: implementation_plan.md 生成（focus=implementation の場合）

```markdown
# 実装計画: [topic]

## System Overview

### 全体アーキテクチャ
```
[収集] → [正規化] → [蓄積] → [検索/RAG] → [評価] → [配信]
```

### コンポーネント図
- connectors: 外部データソース接続
- crawler: Webスクレイピング
- normalizer: データ正規化・重複排除
- storage: 永続化層
- rag: ベクトル検索・回答生成
- dashboard: 可視化
- alerting: 通知

## Data Model

### evidence テーブル
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | 主キー |
| source_type | ENUM | news/sns/paper/docs/code/dataset/other |
| source_url | TEXT | ソースURL |
| ... | ... | ... |

### entity テーブル
- 人物/組織/プロダクト等の正規化

### claim テーブル
- 主張と証拠の紐付け

### run テーブル
- 調査実行の履歴

## Task Breakdown

### Phase 1: PoC（1-2週間目安）
- [ ] 基本connectors（RSS + WebSearch）
- [ ] 最小normalizer
- [ ] SQLite storage
- [ ] CLIインターフェース

### Phase 2: MVP（3-4週間目安）
- [ ] 追加connectors（SNS/News API）
- [ ] ベクトル検索（Qdrant/Pinecone）
- [ ] 基本dashboard
- [ ] テスト整備

### Phase 3: Production（5-8週間目安）
- [ ] 本番インフラ（Docker/K8s）
- [ ] 監視・アラート
- [ ] CI/CD
- [ ] ドキュメント整備

## Test Plan

### 再現性テスト
- 同じinputで同じevidenceが取得できる

### 回帰テスト
- 既存機能が壊れない

### データ品質テスト
- evidence.jsonlのスキーマ検証
- 重複排除の動作確認

## Operations

### スケジューリング
- cron / queue ベースの定期実行

### 監視
- エラーログ
- 収集成功率
- レイテンシ

### 秘密情報管理
- .env / secrets manager
- コミット禁止（.gitignore）
```

### Step 5: 追加ファイル生成（必要に応じて）

- `risks.md` - リスク分析
- `competitors.md` - 競合分析
- `timeline.md` - 時系列整理

## 出力（必須）
- `report.md` - 調査レポート
- `implementation_plan.md` - 実装計画（focus=implementation時）
- `changelog.md` - 追記（統合作業のログ）

## 品質基準

### レポートの必須要素
- [ ] Executive Summary がある
- [ ] すべての主張に証拠IDが紐付いている
- [ ] 矛盾・未解決論点が明示されている
- [ ] 次のアクションが具体的である

### 実装計画の必須要素
- [ ] 段階的なPhase分けがある
- [ ] タスクがチェックリスト化されている
- [ ] テスト計画がある
- [ ] 運用設計がある
