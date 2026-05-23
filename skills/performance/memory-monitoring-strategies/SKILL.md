---
name: memory-monitoring-strategies
description: |
  Node.jsアプリケーションのメモリ監視とリーク検出パターン。PM2、V8ヒープ分析、メモリプロファイリングを活用した効率的メモリ管理を提供。

  Anchors:
  • Observability Engineering / 適用: メモリメトリクスとアラート / 目的: 本番監視
  • Systems Performance / 適用: ヒープ分析とプロファイリング / 目的: メモリ最適化
  • Node.js Documentation / 適用: process.memoryUsage、V8ヒープ統計 / 目的: API活用

  Trigger:
  Use when setting up memory monitoring, investigating memory leaks, configuring PM2 memory limits,
  analyzing heap dumps, or designing production memory alerting strategies.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Memory Monitoring Strategies

> **相対パス**: `SKILL.md`
> **読込条件**: スキル使用時（自動）

---

## 概要

Node.js アプリケーションのメモリ監視とリーク検出パターン。

**対象領域**:

| 領域           | 説明                                |
| -------------- | ----------------------------------- |
| メトリクス監視 | RSS/heapUsed/heapTotal/external     |
| リーク検出     | 継続的増加パターン、原因診断        |
| ヒープ分析     | heapdump 取得、Chrome DevTools 分析 |
| PM2 統合       | メモリ制限、カスタムメトリクス      |

---

## ワークフロー

### Phase 1: 監視戦略設計

**Task**: `agents/basic-monitoring-setup.md`

| 入力       | 出力     |
| ---------- | -------- |
| アプリ特性 | 監視戦略 |

**参照**: `references/basics.md`, `references/memory-metrics.md`

### Phase 2: 実装

**Task**: `agents/pm2-memory-monitoring.md`

| 入力     | 出力     |
| -------- | -------- |
| 監視戦略 | 監視実装 |

**参照**: `references/patterns.md`, `assets/`

### Phase 3: リーク検出・分析

**Task**: `agents/memory-leak-detection.md`, `agents/heap-dump-analysis.md`

| 入力       | 出力         |
| ---------- | ------------ |
| メモリ異常 | 原因レポート |

**参照**: `references/heap-analysis.md`, `references/leak-detection.md`

---

## ベストプラクティス

| すべきこと                                     | 避けるべきこと                 |
| ---------------------------------------------- | ------------------------------ |
| 複数メトリクス（RSS, heapUsed, heapTotal）監視 | 単一メトリクスのみ依存         |
| 段階的閾値（Warning + Critical）設定           | 過剰アラート設定               |
| 定期的ヒープダンプ取得                         | 本番でいきなり分析             |
| PM2 メモリ制限との併用                         | リーク原因の推測（裏付けなし） |
| GC 効果の測定                                  | メモリ制限の過度な厳格化       |

---

## Task ナビゲーション

| Task                                    | 目的             | 参照リソース        |
| --------------------------------------- | ---------------- | ------------------- |
| `basic-monitoring-setup.md`             | 基本監視設定     | `memory-metrics.md` |
| `pm2-memory-monitoring.md`              | PM2 監視         | `patterns.md`       |
| `memory-leak-detection.md`              | リーク検出       | `leak-detection.md` |
| `heap-dump-analysis.md`                 | ヒープ分析       | `heap-analysis.md`  |
| `alert-threshold-configuration.md`      | アラート設定     | `memory-metrics.md` |
| `realtime-monitoring-implementation.md` | リアルタイム監視 | `patterns.md`       |

---

## リソース参照

### References

| ファイル            | 内容                               | 読込条件         |
| ------------------- | ---------------------------------- | ---------------- |
| `basics.md`         | メモリ監視基礎概念、メトリクス概要 | 初回使用時       |
| `patterns.md`       | PM2 統合、アラート、GC 監視        | 設計時           |
| `memory-metrics.md` | 各メトリクス詳細定義と閾値設定     | メトリクス設計時 |
| `heap-analysis.md`  | heapdump 取得・DevTools 分析       | リーク調査時     |
| `leak-detection.md` | リーク兆候検出・原因診断           | リーク調査時     |

### Assets

| ファイル                     | 内容                               |
| ---------------------------- | ---------------------------------- |
| `memory-tracker.template.ts` | PM2 カスタムメトリクステンプレート |

### Scripts

| スクリプト           | 用途                   |
| -------------------- | ---------------------- |
| `memory-monitor.mjs` | リアルタイムメモリ監視 |
| `validate-skill.mjs` | スキル検証             |
| `log_usage.mjs`      | 使用記録               |

---

## 関連スキル

- `logging-observability` - オブザーバビリティ設計
- `graceful-shutdown` - 適切なリソースクリーンアップ
- `health-check-implementation` - ヘルスチェック設計
