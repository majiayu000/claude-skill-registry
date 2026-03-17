---
name: Market Research and Competitive Analysis
description: TAM/SAM/SOM calculation, competitor analysis, and market trends identification. Use when analyzing markets, validating business ideas, or entering new markets.
allowed-tools: WebFetch, Read, Write, Bash
---

# 🔍 Market Research and Competitive Analysis

**Version**: 2.0.0
**Last Updated**: 2025-11-22
**Priority**: ⭐⭐⭐ (P2 Level - Business)
**Purpose**: 市場調査、競合分析、ビジネスアイデア検証

---

## 📋 概要

TAM/SAM/SOM算出、20社以上の競合分析、5大市場トレンド特定、
顧客ニーズ評価を通じた市場検証を提供します。

---

## 🎯 P0: 呼び出しトリガー

| トリガー | 例 |
|---------|-----|
| 市場分析 | "analyze the market" |
| 競合調査 | "who are our competitors?" |
| アイデア検証 | "validate this business idea" |
| 新市場参入 | "entering new markets" |

---

## 🔧 P1: 分析フレームワーク

### 市場規模（TAM/SAM/SOM）

| 市場 | 算出方法 | データソース |
|------|---------|-------------|
| **TAM** | 業界全体 × 単価 | 業界レポート、統計 |
| **SAM** | TAM × 地域/セグメント | 市場調査、政府統計 |
| **SOM** | SAM × 想定シェア | 競合分析、販売計画 |

### 競合分析（3層20社）

| 層 | 定義 | 企業数 |
|----|------|--------|
| Tier 1 | 直接競合 | 5-7社 |
| Tier 2 | 間接競合 | 8-10社 |
| Tier 3 | 代替品 | 5-7社 |

---

## 🚀 P2: 分析パターン

### Pattern 1: 競合ポジショニングマトリクス

```
          高価格
              │
    Premium   │   Luxury
              │
  ─────────────┼───────────── 高機能
              │
    Budget    │   Value
              │
          低価格
```

### Pattern 2: SWOT分析

| 内部 | 強み(S) | 弱み(W) |
|------|---------|---------|
| 外部 | 機会(O) | 脅威(T) |

### Pattern 3: 5 Forces分析

| Force | 評価 | 影響度 |
|-------|------|--------|
| 新規参入脅威 | 中 | ★★☆ |
| 代替品脅威 | 高 | ★★★ |
| 買い手交渉力 | 低 | ★☆☆ |
| 売り手交渉力 | 中 | ★★☆ |
| 業界内競争 | 高 | ★★★ |

---

## ⚡ P3: トレンド分析

### 5大トレンド特定

| # | トレンド | 影響 | 対応 |
|---|---------|------|------|
| 1 | AI活用拡大 | 高 | 機能統合 |
| 2 | リモートワーク定着 | 高 | UI/UX改善 |
| 3 | サステナビリティ | 中 | ESG対応 |
| 4 | サブスク疲れ | 中 | 価格戦略見直し |
| 5 | 規制強化 | 低 | コンプライアンス |

---

## ✅ 成功基準

| 成果物 | 基準 |
|--------|------|
| TAM/SAM/SOM | 数値根拠あり |
| 競合分析 | 20社以上 |
| トレンド | 5項目以上 |
| SWOT | 各象限3項目以上 |

---

## 🔗 関連Skills

- **Business Strategy**: 戦略立案
- **Growth Analytics**: データ分析
- **Content Marketing**: 市場コミュニケーション
