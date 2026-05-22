---
name: tech-debt-analyzer
description: Analyze and prioritize technical debt with refactoring recommendations. Use when evaluating code quality or planning debt reduction.
---

# Tech Debt Analyzer Skill

技術的負債を分析し、優先順位を付けるスキルです。

## 主な機能

- **コード複雑度**: サイクロマティック複雑度
- **重複コード**: コピペ検出
- **古い依存関係**: アップデート必要な dependencies
- **TODO/FIXME**: 未解決タスク
- **テストカバレッジ**: カバレッジ不足箇所
- **優先順位付け**: 影響度とコストで評価

## 分析レポート例

```markdown
# 技術的負債分析レポート

## サマリー
- **総負債スコア**: 157ポイント
- **推定解消時間**: 8週間
- **Critical**: 3件
- **High**: 12件
- **Medium**: 25件

## Critical 負債 (即時対応必須)

### 1. 古いNode.jsバージョン (v14)
- **影響**: セキュリティリスク、パフォーマンス低下
- **コスト**: 2日
- **優先度**: 🔴 Critical
- **アクション**: Node.js 18にアップグレード

### 2. テストカバレッジ不足 (42%)
- **影響**: バグリスク増加
- **コスト**: 2週間
- **優先度**: 🔴 Critical
- **アクション**: カバレッジ80%を目標にテスト追加

### 3. 脆弱な依存関係 (lodash 4.17.15)
- **影響**: CVE-2020-8203
- **コスト**: 1時間
- **優先度**: 🔴 Critical
- **アクション**: npm update lodash

## High 負債

### コード複雑度
- **ファイル**: `src/order/processor.ts`
- **複雑度**: 45 (推奨: <10)
- **コスト**: 3日
- **アクション**: リファクタリング

### 重複コード
- **箇所**: 15箇所
- **重複率**: 23%
- **コスト**: 1週間
- **アクション**: 共通化

## 推奨実行順序

1. 脆弱性修正 (1時間)
2. Node.jsアップグレード (2日)
3. Critical な複雑コードのリファクタリング (1週間)
4. テストカバレッジ向上 (2週間)
5. 重複コード解消 (1週間)
```

## バージョン情報
- Version: 1.0.0
