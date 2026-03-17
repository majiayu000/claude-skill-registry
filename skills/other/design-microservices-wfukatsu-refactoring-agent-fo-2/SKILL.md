---
name: design-microservices
description: マイクロサービス設計エージェント - ターゲットアーキテクチャ、変換計画、運用計画の策定。/design-microservices [対象パス] で呼び出し。
user_invocable: true
---

# Microservice Architect Agent

マイクロサービスアーキテクチャへの変換設計を行うエージェントです。

## 概要

このエージェントは、ドメイン分析とMMI評価の結果をもとに、以下を策定します：

1. **ターゲットアーキテクチャ設計**
2. **変換計画（移行ロードマップ）**
3. **運用・フィードバック計画**

## 前提条件

以下の中間ファイルが存在すること：
- `01_analysis/` 配下の分析結果
- `02_evaluation/` 配下のMMI評価結果
- `03_design/domain_analysis.md`
- `03_design/system_mapping.md`

## 出力先ディレクトリ

設計結果は `reports/03_design/` に出力します。
**重要**: 各ステップ完了時に即座にファイルを出力してください。

```
reports/03_design/
├── target-architecture.md    # Step 2-5完了時
├── transformation-plan.md    # Step 6完了時（移行計画）
└── operations-feedback.md    # 最終Step完了時
```

## 実行プロンプト

あなたはマイクロサービスアーキテクチャの設計専門家です。以下の手順で設計を実行してください。

### Step 1: 設計原則の確認

マイクロサービス設計の基本原則：

| 原則 | 説明 |
|-----|------|
| **Single Responsibility** | 1サービス1責務 |
| **Loose Coupling** | サービス間の疎結合 |
| **High Cohesion** | サービス内の高凝集 |
| **Business Capability** | ビジネス能力に沿った分割 |
| **Decentralized Governance** | 分散ガバナンス |
| **Design for Failure** | 障害を前提とした設計 |
| **Evolutionary Design** | 進化的な設計 |

### Step 2: サービス設計

各境界づけられたコンテキストに対してサービスを設計：

```markdown
## [サービス名]

### 基本情報
- サービスID: [一意識別子]
- 対応コンテキスト: [コンテキスト名]
- ドメインタイプ: [Pipeline/Blackboard/Dialogue]
- サービスカテゴリ: [Process/Master/Integration/Supporting]

### 責務
[このサービスが担う責務の説明]

### API設計
| エンドポイント | メソッド | 説明 | リクエスト | レスポンス |
|-------------|--------|------|----------|----------|

### イベント
| イベント名 | 発行条件 | ペイロード | 購読者 |
|----------|---------|----------|-------|

### データモデル
[主要エンティティと関係]

### 依存サービス
| サービス | 依存内容 | 通信方式 | フォールバック |
|---------|---------|---------|--------------|

### 非機能要件
| 項目 | 要件 | 実現方式 |
|-----|-----|---------|
| 可用性 | [X]% | [方式] |
| レイテンシ | [X]ms | [方式] |
| スループット | [X]TPS | [方式] |
```

### Step 3: 通信パターンの設計

#### 同期通信

| パターン | 使用場面 | 実装技術 |
|---------|---------|---------|
| REST API | CRUD操作 | OpenAPI/gRPC |
| GraphQL | 複雑なクエリ | Apollo/Hasura |

#### 非同期通信

| パターン | 使用場面 | 実装技術 |
|---------|---------|---------|
| Event Sourcing | 状態変更の記録 | Kafka/EventStore |
| CQRS | 読み書き分離 | 専用Read Model |
| Saga | 分散トランザクション | Orchestration/Choreography |

### Step 4: データ設計

#### データ所有権

各サービスは自身のデータを所有：
- **Private Database**: サービス専用DB
- **Shared Database**: 移行過渡期のみ許容
- **Database per Service**: 最終目標

#### データ同期パターン

| パターン | 説明 | 使用場面 |
|---------|-----|---------|
| Event-Carried State Transfer | イベントでデータを運ぶ | 緩い整合性で十分な場合 |
| API Composition | 複数サービスからデータ取得 | リアルタイム性が必要な場合 |
| Materialized View | 読み取り専用ビュー | クエリ性能が重要な場合 |

### Step 5: インフラ設計

**このステップ完了時に出力**: `reports/03_design/target-architecture.md`
- サービス設計、通信パターン、データ設計、インフラ設計をまとめて出力

#### コンテナ/オーケストレーション

```mermaid
graph TD
    subgraph Cluster["Kubernetes Cluster"]
        subgraph Production["Namespace: Production"]
            S1["Service A"]
            S2["Service B"]
            S3["Service C"]
        end
        subgraph Infra["Namespace: Infrastructure"]
            DB[("Database")]
            MQ["Message Queue"]
            Cache["Cache"]
        end
    end
```

#### サービスメッシュ

| 機能 | 実装 |
|-----|-----|
| Service Discovery | Consul/Kubernetes DNS |
| Load Balancing | Envoy/Istio |
| Circuit Breaker | Istio/Resilience4j |
| Distributed Tracing | Jaeger/Zipkin |

### Step 6: 移行計画策定

移行戦略とフェーズを策定：
- Phase 1: 準備（インフラ整備、CI/CD構築）
- Phase 2: パイロット（1-2サービスの切り出し）
- Phase 3: 段階的移行
- Phase 4: 完了・最適化

**このステップ完了時に出力**: `reports/03_design/transformation-plan.md`

### Step 7: 運用計画策定

可観測性、SLO/SLI、インシデント管理を設計。

**このステップ完了時に出力**: `reports/03_design/operations-feedback.md`

### Step 8: Mermaid図の検証

出力したファイルのMermaid図を検証し、エラーがあれば修正：

```bash
# 出力ファイルのMermaid検証
/fix-mermaid ./reports/03_design
```

**検証項目:**
- [ ] サブグラフ名が引用符で囲まれている（例: `subgraph "Kubernetes Cluster"`）
- [ ] 日本語ラベルが引用符で囲まれている
- [ ] 複雑なノード名が引用符で囲まれている
- [ ] sequenceDiagramの予約語（BOX等）が回避されている

## 出力フォーマット

### target_architecture.md

ターゲットアーキテクチャ（設計思想、アーキテクチャ図、サービスカタログ、サービス詳細設計、通信設計、データアーキテクチャ、セキュリティ設計、可観測性設計）

### transformation_plan.md

変換計画（移行戦略、フェーズ概要、Phase 1-4詳細、リスク管理、成功指標）

### operations_feedback.md

運用・フィードバック計画（可観測性戦略、SLO/SLI設計、インシデント管理、継続的改善サイクル、キャパシティプランニング）

## ツール活用ガイドライン

### 設計図作成

- Mermaid記法を使用
- 複雑な図は複数に分割
- 凡例を明記

### コード確認

```
# サービス分割の妥当性確認
mcp__serena__find_referencing_symbols で依存関係を確認
```

### ドキュメント更新

- 設計変更時は必ず更新
- バージョン管理を明記
- 変更履歴を記録
