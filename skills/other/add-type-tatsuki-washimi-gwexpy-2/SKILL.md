---
name: add_type
description: gwexpyに新しい配列型（Array/Series/Field）とコレクションを実装する
---

# Implement GWExPy Type

gwexpy に新しい配列・フィールド型を追加し、クラス階層、メタデータ管理、ドキュメント基準との整合性を保ちます。

## Quick Workflow

```
1. Plan & Design → 2. Implement Core → 3. Add Collections → 4. Integration → 5. Test & Document
```

## Type Categories

### Array Types

汎用の多次元配列型（NumPy ベース）：

詳細：[reference/array.md](reference/array.md)

### Series Types

時系列データ型：

詳細：[reference/series.md](reference/series.md)

### Field Types

物理フィールド型（GW信号など）：

詳細：[reference/field.md](reference/field.md)

## Implementation Steps

### 1. Survey & Plan

基本クラスの選定、メタデータスロット、スライス動作を定義

詳細：各type reference ファイルの Step 1

### 2. Core Class Implementation

`__new__`, `__array_finalize__`, メタデータ保持インデックス操作

詳細：各type reference ファイルの Step 2

### 3. Collections

List/Dict コレクションクラス（バッチ処理対応）

詳細：各type reference ファイルの Step 3

### 4. Integration & Documentation

`__init__.py` へのエクスポート、ドキュメント作成

詳細：各type reference ファイルの Step 4

### 5. Testing

ユニットテスト、メタデータ保持性の検証

詳細：各type reference ファイルの Step 5

## Key Principles

- **一貫性**: 既存クラス階層との整合性を保つ
- **メタデータ保持**: スライス・演算時にメタデータを維持
- **両言語対応**: 英日両方のドキュメント作成
- **テスト完全性**: 新型の全機能をカバーする
