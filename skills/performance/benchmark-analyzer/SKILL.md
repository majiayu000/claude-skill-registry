---
name: benchmark-analyzer
description: >-
  ユーザーが「ベンチマーク実行」「パフォーマンス測定」「性能分析」「速度を測って」「ベンチマークして」等と要求した時に発動。
  Go benchmarkを実行し、結果を分析してボトルネックを特定し、改善提案を行う。
  既存のベンチマークがない場合は、まず作成する。
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

### 手順
1. **ベンチマーク対象の特定**:
   - ユーザー指定がある場合: その関数
   - 指定がない場合: パフォーマンスが重要な関数を検出
2. **既存ベンチマークの確認**:
   - `*_test.go` 内の `Benchmark` 関数を検索
   - 存在しない場合は、ベンチマーク関数を生成
3. **ベンチマーク実行**:
   - `go test -bench=. -benchmem -benchtime=3s` を実行
   - 複数回実行して安定した結果を取得
4. **結果の分析**:
   - ns/op (1操作あたりのナノ秒)
   - B/op (1操作あたりのバイトアロケーション)
   - allocs/op (1操作あたりのアロケーション回数)
5. **ボトルネック特定**:
   - CPU プロファイリング（必要に応じて）
   - メモリプロファイリング（アロケーションが多い場合）
   - `go test -bench=. -cpuprofile=cpu.prof`
6. **改善提案**:
   - 具体的な最適化案を提示
   - トレードオフ（可読性 vs パフォーマンス）を明記
7. **レポート生成**: 結果と提案をマークダウン形式で出力

### ベンチマーク関数の生成例

```go
func BenchmarkSum(b *testing.B) {
    nums := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        Sum(nums)
    }
}

func BenchmarkSumLarge(b *testing.B) {
    nums := make([]int, 10000)
    for i := range nums {
        nums[i] = i
    }
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        Sum(nums)
    }
}
```

### 分析レポートフォーマット

```markdown
# Benchmark Analysis Report

## Summary
Function: `Sum()`
Date: 2025-10-23

## Benchmark Results

### Small Input (10 elements)
```
BenchmarkSum-8    50000000    25.3 ns/op    0 B/op    0 allocs/op
```

### Large Input (10,000 elements)
```
BenchmarkSumLarge-8    100000    11234 ns/op    0 B/op    0 allocs/op
```

## Analysis

### Performance Characteristics
- ✅ **Good**: Zero allocations - operates on input slice without copying
- ✅ **Good**: Linear time complexity O(n) as expected
- ⚠️ **Note**: Performance scales linearly with input size

### Bottlenecks
None detected. Implementation is optimal for this use case.

## Optimization Opportunities

### 1. SIMD Optimization (Advanced)
For very large slices (>100k elements), could consider SIMD instructions.
**Trade-off**: Significant complexity increase for marginal gains.
**Recommendation**: Not worth it for this use case.

### 2. Parallel Processing
For slices >10M elements, could use goroutines.
```go
func SumParallel(nums []int) int {
    // Split into chunks, sum in parallel, combine
}
```
**Trade-off**: Overhead makes it slower for typical use cases.
**Recommendation**: Only if consistently processing huge datasets.

## Comparison with Standard Library

| Implementation | Time (ns/op) | Allocs |
|----------------|--------------|--------|
| Current Sum()  | 25.3         | 0      |
| Naive approach | 28.1         | 0      |

Current implementation is 10% faster than naive approach.

## Recommendations

1. ✅ **Keep current implementation** - Already optimized
2. ✅ **Add benchmark to CI** - Detect performance regressions
3. ❌ **Don't optimize further** - Diminishing returns

## Action Items
- [ ] Add benchmarks to test suite
- [ ] Document performance characteristics in GoDoc
```

### パフォーマンス最適化の観点

#### メモリアロケーション削減
- 不要な `append` を避ける
- スライス容量を事前確保（`make([]T, 0, capacity)`）
- `sync.Pool` でオブジェクト再利用
- ポインタ vs 値のトレードオフ

#### CPU最適化
- ループアンローリング（コンパイラが通常やる）
- 分岐予測を意識（ホットパスを最適化）
- インライン化（小さな関数）
- 不要な型変換を避ける

#### プロファイリングコマンド
```bash
# CPU プロファイル
go test -bench=. -cpuprofile=cpu.prof
go tool pprof cpu.prof

# メモリプロファイル
go test -bench=. -memprofile=mem.prof
go tool pprof mem.prof

# トレース
go test -bench=. -trace=trace.out
go tool trace trace.out
```

### ベンチマークのベストプラクティス
- `b.ResetTimer()` で初期化コストを除外
- 複数の入力サイズでテスト（small, medium, large）
- `-benchtime=3s` で安定した結果を取得
- `-count=5` で統計的信頼性を確保
- ベンチマーク専用のデータを使う（本番データは避ける）

### 警告: 早すぎる最適化
- まず正確性、次に可読性、最後にパフォーマンス
- 計測してから最適化（推測しない）
- ボトルネックを特定してから対処
- パフォーマンス改善は具体的な数値で示す
