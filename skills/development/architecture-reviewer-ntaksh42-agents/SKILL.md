---
name: architecture-reviewer
description: Review software architecture for SOLID principles, design patterns, scalability, and maintainability. Use when evaluating system design or planning refactoring.
---

# Architecture Reviewer Skill

システムアーキテクチャを評価し、設計改善を提案するスキルです。

## 概要

SOLID原則、デザインパターン、マイクロサービス設計等の観点からアーキテクチャをレビューします。

## 主な機能

- **SOLID原則評価**: 単一責任、開放閉鎖、リスコフ置換等
- **デザインパターン**: 適切なパターンの適用状況
- **レイヤー分離**: プレゼンテーション、ビジネス、データ層
- **依存性管理**: 依存性注入、循環依存の検出
- **スケーラビリティ**: 水平・垂直スケーリング
- **マイクロサービス**: サービス境界、通信パターン
- **データベース設計**: 正規化、インデックス、パーティショニング

## 使用方法

```
このアーキテクチャをレビュー：
[アーキテクチャ図またはコード]

評価項目:
- SOLID原則
- スケーラビリティ
- 保守性
```

## レビュー観点

### 1. SOLID原則

**単一責任原則（SRP）**:
```typescript
// ❌ 複数の責任
class User {
  saveToDatabase() {}
  sendEmail() {}
  generateReport() {}
}

// ✅ 単一責任
class User {}
class UserRepository {
  save(user: User) {}
}
class EmailService {
  send(to: string) {}
}
class ReportGenerator {
  generate(user: User) {}
}
```

**依存性逆転（DIP）**:
```python
# ❌ 具象に依存
class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # 具象クラス

# ✅ 抽象に依存
class UserService:
    def __init__(self, database: DatabaseInterface):
        self.db = database  # インターフェース
```

### 2. レイヤー構造

```
┌─────────────────────────────┐
│   Presentation Layer        │  UI, API Endpoints
├─────────────────────────────┤
│   Application Layer         │  Use Cases, Orchestration
├─────────────────────────────┤
│   Domain Layer              │  Business Logic, Entities
├─────────────────────────────┤
│   Infrastructure Layer      │  Database, External APIs
└─────────────────────────────┘
```

### 3. マイクロサービス設計

```
推奨パターン:
- API Gateway: 単一エントリーポイント
- Service Discovery: 動的サービス検出
- Circuit Breaker: 障害の連鎖防止
- Event Sourcing: イベント駆動
- CQRS: コマンドとクエリの分離
```

## 出力例

```markdown
# アーキテクチャレビュー結果

## 総合評価: B+

### 良好な点
✅ クリーンアーキテクチャの採用
✅ 適切な依存性注入
✅ レイヤー分離が明確

### 改善点

#### [HIGH] 循環依存の存在
**場所**: OrderService ↔ PaymentService
**影響**: テスタビリティの低下、デプロイの複雑化
**推奨**: イベント駆動アーキテクチャに変更

#### [MEDIUM] 単一責任原則違反
**場所**: UserController
**問題**: 認証、認可、ビジネスロジックが混在
**推奨**: 責務を分離

### アーキテクチャ提案

1. **イベント駆動への移行**: サービス間の結合度削減
2. **CQRS導入**: 読み書きの分離で性能向上
3. **キャッシュ層追加**: Redis で頻繁な読み取り最適化
```

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22
