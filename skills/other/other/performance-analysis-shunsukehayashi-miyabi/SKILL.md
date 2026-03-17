---
name: Performance Analysis and Optimization
description: CPU profiling, benchmarking, and memory analysis for Rust applications. Use when code is slow, memory usage is high, or optimization is needed.
allowed-tools: Bash, Read, Grep, Glob
---

# ⚡ Performance Analysis and Optimization

**Version**: 2.0.0
**Last Updated**: 2025-11-22
**Priority**: ⭐⭐⭐ (P2 Level)
**Purpose**: Rustアプリケーションのパフォーマンス分析と最適化

---

## 📋 概要

CPUプロファイリング、ベンチマーク、メモリ分析を通じた
パフォーマンス問題の特定と最適化を提供します。

---

## 🎯 P0: 呼び出しトリガー

| トリガー | 例 |
|---------|-----|
| 遅い | "this is slow" |
| メモリ使用 | "why is memory usage so high?" |
| 最適化 | "optimize this function" |
| プロファイリング | "profile this code" |
| ベンチマーク | "benchmark performance" |

---

## 🔧 P1: 分析ツール一覧

### ツール優先順位

| ツール | 用途 | 対象 | コマンド |
|--------|------|------|---------|
| `criterion` | ベンチマーク | 関数 | `cargo bench` |
| `flamegraph` | CPUプロファイル | プロセス | `cargo flamegraph` |
| `perf` | 詳細プロファイル | Linux | `perf record` |
| `valgrind` | メモリ | ヒープ | `valgrind --tool=massif` |
| `heaptrack` | ヒープ追跡 | 割り当て | `heaptrack ./binary` |
| `cargo-bloat` | バイナリサイズ | サイズ | `cargo bloat` |
| `tokio-console` | 非同期 | タスク | `tokio-console` |

---

## 🚀 P2: 分析パターン

### Pattern 1: ベンチマーク（criterion）

```rust
// benches/my_benchmark.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn bench_function(c: &mut Criterion) {
    c.bench_function("my_function", |b| {
        b.iter(|| my_function(black_box(input)))
    });
}

criterion_group!(benches, bench_function);
criterion_main!(benches);
```

```bash
cargo bench
```

### Pattern 2: Flamegraph

```bash
# フレームグラフ生成
cargo flamegraph --bin miyabi -- --issue 270

# 出力: flamegraph.svg
```

### Pattern 3: メモリプロファイル

```bash
# valgrind massif
valgrind --tool=massif ./target/release/miyabi
ms_print massif.out.*

# heaptrack（推奨）
heaptrack ./target/release/miyabi
heaptrack_gui heaptrack.miyabi.*
```

### Pattern 4: バイナリサイズ分析

```bash
# サイズ分析
cargo bloat --release --crates

# シンボル別
cargo bloat --release -n 20
```

---

## ⚡ P3: 最適化戦略

### 最適化優先順位

| 優先度 | 戦略 | 効果 | 難易度 |
|--------|------|------|--------|
| 1 | アルゴリズム改善 | 高 | 中 |
| 2 | データ構造変更 | 高 | 中 |
| 3 | メモリ割り当て削減 | 中 | 低 |
| 4 | 並列化 | 中 | 高 |
| 5 | キャッシュ活用 | 中 | 中 |
| 6 | SIMD/低レベル | 低 | 高 |

### よくある最適化

```rust
// ❌ 毎回allocate
for item in items {
    let s = item.to_string();
    // ...
}

// ✅ 事前allocate
let mut buf = String::with_capacity(1024);
for item in items {
    buf.clear();
    write!(&mut buf, "{}", item).unwrap();
    // ...
}
```

```rust
// ❌ Clone多用
fn process(data: Vec<T>) -> Vec<T> {
    data.clone()
}

// ✅ 参照で渡す
fn process(data: &[T]) -> Vec<T> {
    // ...
}
```

---

## 📊 パフォーマンス目標

| メトリクス | 目標 | 測定方法 |
|-----------|------|---------|
| ビルド時間 | <5分 | CI計測 |
| テスト時間 | <2分 | `cargo test` |
| バイナリサイズ | <50MB | `cargo bloat` |
| メモリ使用量 | <500MB | runtime計測 |

---

## 🛡️ 注意事項

### リリースビルドで測定

```bash
# ❌ デバッグビルド（遅い）
cargo run

# ✅ リリースビルド
cargo run --release
```

### PGO（Profile-Guided Optimization）

```bash
# Step 1: インストルメント
RUSTFLAGS="-Cprofile-generate=/tmp/pgo" cargo build --release

# Step 2: プロファイル収集
./target/release/miyabi [typical workload]

# Step 3: 最適化ビルド
llvm-profdata merge -o /tmp/pgo/merged.profdata /tmp/pgo
RUSTFLAGS="-Cprofile-use=/tmp/pgo/merged.profdata" cargo build --release
```

---

## ✅ 成功基準

| チェック項目 | 基準 |
|-------------|------|
| ボトルネック特定 | 上位3箇所 |
| ベンチマーク | 改善前後比較 |
| メモリリーク | なし |
| 回帰テスト | パフォーマンス維持 |

---

## 🔗 関連Skills

- **Rust Development**: ビルド最適化
- **Debugging**: 問題箇所特定
- **Security Audit**: セキュリティとのトレードオフ
