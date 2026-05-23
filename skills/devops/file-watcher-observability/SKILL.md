---
name: file-watcher-observability
description: |
  ファイル監視システムの可観測性（Observability）を3本柱（Metrics、Logs、Traces）に基づいて実装するスキル。Prometheus/Grafana統合でSLA遵守測定、パフォーマンス監視、障害根本原因分析を支援。

  Anchors:
  • Observability Engineering（Charity Majors） / 適用: 3本柱設計 / 目的: メトリクス・ログ・トレースの統合
  • Google SRE Book / 適用: ゴールデンシグナル / 目的: SLI/SLO設計
  • Prometheus Documentation / 適用: メトリクス命名規則 / 目的: 標準準拠の実装

  Trigger:
  Use when implementing observability for file watcher systems, setting up Prometheus/Grafana monitoring, designing SLI/SLO metrics, or analyzing production performance issues.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
---

# ファイル監視システムの可観測性設計

## 概要

ファイル監視システムに対してMetrics・Logs・Tracesの3本柱を統合し、Prometheus/Grafanaで本番環境のパフォーマンスを定量的に監視・分析するスキル。

## ワークフロー

### Phase 1: メトリクス設計

**目的**: SLA要件からメトリクス定義とSLI/SLOを設計

**アクション**:

1. [references/basics.md](references/basics.md) で可観測性の基本概念を確認
2. ゴールデンシグナル（Latency、Traffic、Errors、Saturation）を定義
3. Prometheus命名規則に準拠したメトリクス名を設計
4. SLI/SLO目標値を明文化

**Task**: [agents/metrics-design.md](agents/metrics-design.md) を参照

### Phase 2: 可観測性セットアップ

**目的**: Prometheus/Grafana/Logs/Tracesの統合実装

**アクション**:

1. [references/patterns.md](references/patterns.md) で実装パターンを確認
2. [assets/metrics-collector.ts](assets/metrics-collector.ts) をカスタマイズ
3. [assets/grafana-dashboard.json](assets/grafana-dashboard.json) でダッシュボード構築
4. アラートルールを定義

**Task**: [agents/observability-setup.md](agents/observability-setup.md) を参照

### Phase 3: 検証と運用

**目的**: 設定の検証と運用開始

**アクション**:

1. `scripts/validate-observability.mjs --all` で設定を検証
2. 本番環境へのデプロイ
3. アラート通知先の設定
4. `scripts/log_usage.mjs --result success` で記録

## Task仕様ナビ

| Task                                                           | 用途           | 入力             | 出力                      |
| -------------------------------------------------------------- | -------------- | ---------------- | ------------------------- |
| [agents/metrics-design.md](agents/metrics-design.md)           | メトリクス設計 | SLA要件          | メトリクス定義書・SLO仕様 |
| [agents/observability-setup.md](agents/observability-setup.md) | セットアップ   | メトリクス定義書 | 設定ファイル群            |

## ベストプラクティス

### すべきこと

- SLA定義を明確にしてからメトリクスを設計する
- ゴールデンシグナル4つを必ずカバーする
- ダッシュボードはオンコール対応者向けに最小限の情報に絞る
- アラート閾値は実運用データに基づいて調整する

### 避けるべきこと

- 測定設計なしで実装を始める
- すべてのメトリクスを取得しようとする（コスト増大）
- ラベルに高カーディナリティ値（ファイルパス等）を使用する
- ダッシュボードを情報過多にする

## リソース参照

### references/（詳細知識）

| リソース     | パス                                             | 内容                               |
| ------------ | ------------------------------------------------ | ---------------------------------- |
| 基本概念     | [references/basics.md](references/basics.md)     | 3本柱・ゴールデンシグナル・SLI/SLO |
| 実装パターン | [references/patterns.md](references/patterns.md) | Prometheus/Grafana設定例           |

### assets/（テンプレート）

| テンプレート           | 用途                      |
| ---------------------- | ------------------------- |
| metrics-collector.ts   | メトリクス収集コード      |
| grafana-dashboard.json | Grafanaダッシュボード設定 |

### scripts/（検証・記録）

| スクリプト                 | 用途           | 使用例                                          |
| -------------------------- | -------------- | ----------------------------------------------- |
| validate-observability.mjs | 設定検証       | `node scripts/validate-observability.mjs --all` |
| log_usage.mjs              | 利用記録       | `node scripts/log_usage.mjs --result success`   |
| health-check.sh            | ヘルスチェック | `./scripts/health-check.sh`                     |

## 変更履歴

| Version | Date       | Changes                                                           |
| ------- | ---------- | ----------------------------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様に完全準拠。agents/を2つに統合、references/を刷新 |
| 1.1.0   | 2025-12-31 | frontmatter改訂、構成再編                                         |
| 1.0.0   | 2025-12-24 | 初版作成                                                          |
