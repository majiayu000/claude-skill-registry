---
name: Sales and CRM Management
description: Complete sales funnel design, B2B sales playbook, CRM setup, and customer success management. Use when building sales processes or reducing churn.
allowed-tools: Read, Write, WebFetch, Bash
---

# 💰 Sales and CRM Management

**Version**: 2.0.0
**Last Updated**: 2025-11-22
**Priority**: ⭐⭐⭐ (P2 Level - Business)
**Purpose**: セールスファネル、B2B営業プレイブック、CRM、カスタマーサクセス

---

## 📋 概要

完全なセールスファネル設計、BANTによるB2B営業、CRMパイプライン、
カスタマーヘルススコアリングを提供します。

---

## 🎯 P0: 呼び出しトリガー

| トリガー | 例 |
|---------|-----|
| 営業プロセス | "build our sales process" |
| チャーン削減 | "how to reduce churn?" |
| LTV向上 | "increase customer LTV" |
| 営業最適化 | "optimizing sales operations" |

---

## 🔧 P1: セールスファネル

### ファネルステージ

| Stage | 目的 | 転換率目標 | アクション |
|-------|------|-----------|-----------|
| **Awareness** | 認知 | - | コンテンツ、広告 |
| **Interest** | 興味 | 30% | リード獲得 |
| **Consideration** | 検討 | 40% | デモ、資料 |
| **Intent** | 意思 | 50% | 提案、見積 |
| **Purchase** | 購入 | 60% | 契約 |
| **Loyalty** | 継続 | 90% | サクセス |

---

## 🚀 P2: B2B営業プレイブック

### BANT資格確認

| 要素 | 質問例 | 重み |
|------|--------|------|
| **B**udget | 予算は確保されていますか？ | 25% |
| **A**uthority | 最終決裁者は誰ですか？ | 25% |
| **N**eed | 解決したい課題は？ | 30% |
| **T**imeline | 導入時期の目標は？ | 20% |

### パイプラインステージ

| Stage | 定義 | 確度 |
|-------|------|------|
| Lead | 問い合わせ | 10% |
| MQL | マーケティング認定 | 20% |
| SQL | 営業認定 | 40% |
| Proposal | 提案中 | 60% |
| Negotiation | 交渉中 | 80% |
| Closed Won | 成約 | 100% |
| Closed Lost | 失注 | 0% |

---

## ⚡ P3: カスタマーサクセス

### ヘルススコア（0-100）

| 指標 | 重み | 計算方法 |
|------|------|---------|
| 利用頻度 | 30% | DAU/MAU |
| 機能活用 | 25% | 使用機能数 |
| サポート履歴 | 20% | チケット傾向 |
| 契約状況 | 15% | 更新/拡張 |
| NPS | 10% | スコア |

### リスク対応

| スコア | リスク | アクション |
|--------|--------|-----------|
| 80-100 | 低 | 拡張提案 |
| 60-79 | 中 | プロアクティブ連絡 |
| 40-59 | 高 | 緊急介入 |
| 0-39 | 危険 | 経営エスカレーション |

### Churn Prevention

```
チャーン兆候:
- ログイン頻度 ↓50%
- 主要機能利用 ↓30%
- サポート問い合わせ ↑
- 請求失敗

対策:
1. 即時アラート
2. CS担当割り当て
3. 原因ヒアリング
4. 改善提案
5. 特別オファー検討
```

---

## 📊 KPI管理

### 営業KPI

| メトリクス | 目標 | 測定 |
|-----------|------|------|
| MQL→SQL転換率 | 30% | 週次 |
| SQL→成約率 | 25% | 月次 |
| 平均商談期間 | 30日 | 月次 |
| ARPU | ¥10,000 | 月次 |

### CS KPI

| メトリクス | 目標 | 測定 |
|-----------|------|------|
| Churn Rate | <5% | 月次 |
| NRR | >110% | 月次 |
| NPS | >40 | 四半期 |
| CSAT | >4.5/5 | 継続 |

---

## ✅ 成功基準

| 成果物 | 基準 |
|--------|------|
| ファネル設計 | 6ステージ |
| プレイブック | BANT含む |
| CRMパイプライン | 7ステージ |
| ヘルススコア | 5指標 |

---

## 🔗 関連Skills

- **Growth Analytics**: 営業データ分析
- **Business Strategy**: 全体戦略
- **Content Marketing**: リード獲得
