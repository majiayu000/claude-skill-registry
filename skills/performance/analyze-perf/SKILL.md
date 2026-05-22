---
name: analyze-perf
description: Go プロジェクトのパフォーマンスを計測・分析する。「パフォーマンス計測」「ベンチマーク」「perf」「性能測定」「プロファイリング」「最適化提案」「パフォーマンス分析」などで起動。ベンチマーク実行、プロファイリング、改善案の提示をサポート。
allowed-tools: [Read, Bash, Glob, Grep]
context: fork
agent: shiiman-go:performance-optimizer
---

# Analyze-Perf

Go プロジェクトのパフォーマンスを計測・分析し、改善案を提示します。

## 引数

- `[パッケージパス]`: 対象パッケージ（例: ./internal/handler）
- `--bench`: ベンチマークのみ実行
- `--profile`: プロファイリングを実行
- `--help`: ヘルプを表示

## 実行フロー

```
1. 対象コードの特定
   ↓
2. ベースライン測定
   ↓
3. ボトルネック分析
   ↓
4. 改善案提示
   ↓
5. ユーザーと方針決定
   ↓
6. 修正実装
   ↓
7. 効果測定
```

## 実行手順

### 1. ベンチマーク実行

```bash
# 基本的なベンチマーク
go test -bench=. -benchmem ./...

# 特定パッケージのベンチマーク
go test -bench=. -benchmem ./internal/handler

# 複数回実行して安定した結果を取得
go test -bench=. -benchmem -count=3 ./... | tee baseline.txt
```

### 2. プロファイリング

```bash
# CPU プロファイル
go test -bench=. -cpuprofile=cpu.prof ./...
go tool pprof cpu.prof

# メモリプロファイル
go test -bench=. -memprofile=mem.prof ./...
go tool pprof mem.prof

# pprof コマンド
# top    - 実行時間が最も長い関数を表示
# list   - 特定関数のソースコード行ごとの分析
# web    - グラフ形式で可視化
```

### 3. 結果レポート

```
## パフォーマンス分析結果

### ベンチマーク結果
- BenchmarkXxx: {N} ns/op
- メモリアロケーション: {M} B/op
- アロケーション回数: {K} allocs/op

### 特定されたボトルネック
1. {関数名}: {問題の説明}
2. {関数名}: {問題の説明}

### 改善案
| 提案 | 内容 | 期待される改善 |
|------|------|---------------|
| 1 | {改善内容} | {効果} |
| 2 | {改善内容} | {効果} |

どの改善案を適用しますか？
```

## 改善案の観点

| 観点 | 改善例 |
|------|--------|
| データ構造 | slice、map の適切な選択 |
| アルゴリズム | 計算量の削減、キャッシング |
| 並行処理 | goroutine、channel、ワーカープール |
| メモリ管理 | sync.Pool、スライスの事前確保 |
| 文字列操作 | strings.Builder の使用 |
| PGO | Profile-Guided Optimization（Go 1.22+） |

## 期待される改善率の目安

| 最適化内容 | 期待される改善率 |
|-----------|----------------|
| スライスの事前確保 | メモリ 30-50% 削減 |
| ポインタレシーバ | CPU 20-40% 高速化 |
| strings.Builder | 文字列操作 2-5x 高速化 |
| sync.Pool | アロケーション 50-80% 削減 |
| 並行処理最適化 | スループット 2-10x 向上 |
| PGO | 全体 2-14% 高速化 |

## benchstat による比較

```bash
# 最適化前
go test -bench=. -benchmem -count=3 ./... | tee before.txt

# 最適化後
go test -bench=. -benchmem -count=3 ./... | tee after.txt

# 比較
benchstat before.txt after.txt
```

## 重要な注意事項

- ✅ 最適化前に必ずベンチマークで現状を測定
- ✅ 修正前後のベンチマーク結果を比較して効果を確認
- ✅ 実際にボトルネックとなっている箇所に集中
- ❌ パフォーマンス向上のために可読性を大きく損なわない
- ❌ 早すぎる最適化を避ける
