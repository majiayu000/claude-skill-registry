---
name: performance-analyzer
description: Analyze code performance, detect bottlenecks, suggest optimizations for algorithms, queries, and resource usage. Use when improving application performance or investigating slow code.
---

# Performance Analyzer Skill

パフォーマンスボトルネックを特定し、最適化提案を行うスキルです。

## 概要

コードの実行時間、メモリ使用量、アルゴリズム複雑度を分析し、具体的な最適化提案を提供します。

## 主な機能

- **アルゴリズム複雑度分析**: Big O記法での評価
- **N+1クエリ検出**: データベースクエリの最適化
- **メモリリーク検出**: 未解放リソース、循環参照
- **キャッシング機会**: メモ化、CDN活用
- **非同期処理**: 並列化、Promise最適化
- **バンドルサイズ**: Tree shaking、Code splitting
- **レンダリング最適化**: 仮想化、遅延読み込み

## 使用方法

```
このコードのパフォーマンス分析：
[コード]

分析項目:
- アルゴリズム複雑度
- メモリ使用量
- 最適化提案
```

## 分析例

### N+1 クエリ問題

**問題のあるコード**:
```javascript
// O(n) のクエリを n 回実行 = O(n²)
const posts = await Post.findAll();
for (const post of posts) {
  post.author = await User.findById(post.authorId); // N+1問題
}
```

**最適化**:
```javascript
// O(n) + O(m) = O(n)
const posts = await Post.findAll();
const authorIds = posts.map(p => p.authorId);
const authors = await User.findByIds(authorIds); // 1回のクエリ
const authorMap = new Map(authors.map(a => [a.id, a]));
posts.forEach(post => post.author = authorMap.get(post.authorId));
```

**改善**: クエリ数 101回 → 2回、レスポンス時間 90% 削減

### アルゴリズム最適化

**非効率**:
```python
# O(n²) - 遅い
def has_duplicates(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False
```

**最適化**:
```python
# O(n) - 高速
def has_duplicates(arr):
    return len(arr) != len(set(arr))
```

### メモリ最適化

**問題**:
```javascript
// メモリリーク: イベントリスナーが解放されない
component.addEventListener('click', handler);
```

**修正**:
```javascript
// クリーンアップ
const controller = new AbortController();
component.addEventListener('click', handler, { signal: controller.signal });
// コンポーネント破棄時
controller.abort();
```

## 出力レポート

```markdown
# パフォーマンス分析レポート

## サマリー
- **Critical**: 2件（即時対応必須）
- **High**: 4件（短期対応）
- **Medium**: 6件（中期改善）

## Critical 問題

### [CRITICAL] N+1 クエリ問題
**場所**: api/posts.ts:45-52
**影響**: 100件のデータで101回のクエリ実行
**レスポンス時間**: 2.5秒 → 0.3秒（88%改善可能）

### [CRITICAL] O(n²) アルゴリズム
**場所**: utils/search.py:23
**影響**: 10,000件で100,000,000回の比較
**実行時間**: 45秒 → 0.5秒（98%改善可能）

## 最適化提案

1. **データベースクエリ**: Eager loading使用
2. **アルゴリズム**: ハッシュテーブル活用
3. **キャッシング**: Redis導入
4. **非同期処理**: Promise.all で並列化
```

## ベストプラクティス

1. **計測**: プロファイリングツール使用
2. **ボトルネック特定**: 最も影響の大きい部分から最適化
3. **トレードオフ**: 可読性とのバランス
4. **継続的監視**: APM ツール導入

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22
