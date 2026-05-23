---
name: rust-performance
description: "性能优化专家。处理 benchmark, profiling, allocation, SIMD, cache, 优化, 基准测试等问题。触发词：performance, optimization, benchmark, profiling, allocation, SIMD, cache, make it faster, 性能优化, 基准测试, 内存分配"
globs: ["**/*.rs"]
---

# 性能优化

## 核心问题

**瓶颈在哪里？优化值得吗？**

先测量，再优化。不要猜测。

---

## 优化优先级

```
1. 算法选择     (10x - 1000x)   ← 最大收益
2. 数据结构     (2x - 10x)
3. 减少分配     (2x - 5x)
4. 缓存优化     (1.5x - 3x)
5. SIMD/并行    (2x - 8x)
```

**警告**：过早优化是万恶之源。先让代码跑起来，再优化热点。

---

## 测量工具

### Benchmark

```bash
# cargo bench
cargo bench
# criterion 统计基准测试
```

### Profiling

| 工具 | 用途 |
|-----|------|
| `perf` / `flamegraph` | CPU 火焰图 |
| `heaptrack` | 分配追踪 |
| `valgrind --tool=cachegrind` | 缓存分析 |
| `dhat` | 堆分配分析 |

---

## 常见优化技术

### 1. 预分配

```rust
// ❌ 每次增长都分配
let mut vec = Vec::new();
for i in 0..1000 {
    vec.push(i);
}

// ✅ 预分配已知大小
let mut vec = Vec::with_capacity(1000);
for i in 0..1000 {
    vec.push(i);
}
```

### 2. 避免 clone

```rust
// ❌ 不必要的 clone
fn process(item: &Item) {
    let data = item.data.clone();
    // ...
}

// ✅ 使用引用
fn process(item: &Item) {
    let data = &item.data;
    // ...
}
```

### 3. 批量操作

```rust
// ❌ 多次数据库调用
for user_id in user_ids {
    db.update(user_id, status)?;
}

// ✅ 批量更新
db.update_all(user_ids, status)?;
```

### 4. 小对象优化

```rust
// 常用小集合用 SmallVec
use smallvec::SmallVec;
let mut vec: SmallVec<[u8; 16]> = SmallVec::new();
// 16 个以内不分配堆内存
```

### 5. 并行处理

```rust
use rayon::prelude::*;
let sum: i32 = data
    .par_iter()
    .map(|x| expensive(x))
    .sum();
```

---

## 反模式

| 反模式 | 为什么不好 | 正确做法 |
|-------|-----------|---------|
| clone 躲避生命周期 | 性能开销 | 正确所有权设计 |
| 什么都 Box | 间接成本 | 优先栈分配 |
| HashMap 小数据集 | 开销过大 | Vec + 线性搜索 |
| 循环中字符串拼接 | O(n²) | `with_capacity` 或 `format!` |
| LinkedList | 缓存不友好 | `Vec` 或 `VecDeque` |

---

## 常见问题排查

| 症状 | 可能原因 | 排查方法 |
|-----|---------|---------|
| 内存持续增长 | 泄漏、累积 | heaptrack |
| CPU 占用高 | 算法问题 | flamegraph |
| 响应不稳定 | 分配波动 | dhat |
| 吞吐量低 | 串行处理 | rayon 并行 |

---

## 优化检查清单

- [ ] 测了吗？不要猜测
- [ ] 瓶颈确认了吗？
- [ ] 算法最优吗？
- [ ] 数据结构合适吗？
- [ ] 减少不必要的分配了吗？
- [ ] 能并行吗？
- [ ] 释放内存了吗？（RAII）

---

# 高级性能优化

> 以下内容针对多线程、高并发场景

## 为什么多线程代码反而更慢？

性能问题往往藏在看不见的地方。

---

## False Sharing (伪共享)

### 症状

```rust
// 问题代码：多个 AtomicU64 挤在一个 struct 里
struct ShardCounters {
    inflight: AtomicU64,
    completed: AtomicU64,
}
```

- CPU 一个核心长期 90%+
- perf 显示大量 LLC miss
- 原子 RMW 操作异常多
- 增加线程数反而变慢

### 诊断

```bash
# perf 分析
perf stat -d
# 看 LLC-load-misses 和 locked-instrs

# 火焰图
cargo flamegraph
# 找 atomic fetch_add 热点
```

### 解决：Cache Line Padding

```rust
// 每个字段独立一个 cache line
#[repr(align(64))]
struct PaddedAtomicU64(AtomicU64);

struct ShardCounters {
    inflight: PaddedAtomicU64,
    completed: PaddedAtomicU64,
}
```

### 验证

```rust
// Benchmark 对比
fn bench_naive() { /* 多个 AtomicU64 */ }
fn bench_padded() { /* 独立 cache line */ }
```

---

## 锁竞争优化

### 症状

```rust
// 全局共享 HashMap，所有线程竞争同一把锁
let shared: Arc<Mutex<HashMap<String, usize>>> = Arc::new(Mutex::new(HashMap::new()));
```

- 大量时间在 mutex lock/unlock
- 增加线程数性能不升反降
- 系统时间占比高

### 解决：分片本地计数

```rust
// 每个线程本地 HashMap，最后合并
pub fn parallel_count(data: &[String], num_threads: usize) -> HashMap<String, usize> {
    let mut handles = Vec::new();
    
    for chunk in data.chunks(/*...*/) {
        handles.push(thread::spawn(move || {
            let mut local = HashMap::new();
            for key in chunk {
                *local.entry(key).or_insert(0) += 1;
            }
            local  // 返回本地计数
        }));
    }
    
    // 合并所有本地结果
    let mut result = HashMap::new();
    for handle in handles {
        for (k, v) in handle.join().unwrap() {
            *result.entry(k).or_insert(0) += v;
        }
    }
    result
}
```

---

## NUMA 感知

### 问题场景

```rust
// 多 socket 服务器，内存分配在远端 NUMA node
let pool = ArenaPool::new(num_threads);
// Rayon work-stealing 让任务在任意线程执行
// 跨 NUMA 访问导致严重的内存迁移延迟
```

### 解决

```rust
// 1. NUMA 节点绑定
let numa_node = detect_numa_node();
let pool = NumaAwarePool::new(numa_node);

// 2. 统一 allocator（jemalloc）
#[global_allocator]
static ALLOC: jemallocator::Jemalloc = jemallocator::Jemalloc;

// 3. 避免跨 NUMA 的对象 clone
// 直接借用，不做数据拷贝
```

### 工具

```bash
# 检查 NUMA 拓扑
numactl --hardware

# 绑定 NUMA node
numactl --cpunodebind=0 --membind=0 ./my_program
```

---

## 数据结构优化

### HashMap vs 分片

| 场景 | 方案 | 原因 |
|-----|------|-----|
| 高并发写入 | DashMap 或分片 | 减少锁竞争 |
| 读多写少 | RwLock<HashMap> | 读锁不阻塞 |
| 小数据集 | Vec + 线性搜索 | HashMap 开销更大 |
| 固定 key | Enum + 数组 | 完全无哈希开销 |

### 示例：读多写少

```rust
// 大量读取，少量更新
struct Config {
    map: RwLock<HashMap<String, ConfigValue>>,
}

impl Config {
    pub fn get(&self, key: &str) -> Option<ConfigValue> {
        self.map.read().get(key).cloned()
    }
    
    pub fn update(&self, key: String, value: ConfigValue) {
        self.map.write().insert(key, value);
    }
}
```

---

## 常见陷阱速查

| 陷阱 | 症状 | 解决 |
|-----|------|-----|
| 相邻原子变量 | 伪共享 | `#[repr(align(64))]` |
| 全局 Mutex | 锁竞争 | 本地计数 + 合并 |
| 跨 NUMA 分配 | 内存迁移 | NUMA 感知分配 |
| 频繁小分配 | allocator 压力 | 对象池 |
| 动态字符串 key | 额外分配 | 用整数 ID 代替 |

---

## 性能诊断工具

| 工具 | 用途 |
|-----|------|
| `perf stat -d` | CPU 周期、缓存命中率 |
| `perf record -g` | 采样火焰图 |
| `valgrind --tool=cachegrind` | 缓存分析 |
| `jemalloc profiling` | 内存分配分析 |
| `numactl` | NUMA 拓扑 |

