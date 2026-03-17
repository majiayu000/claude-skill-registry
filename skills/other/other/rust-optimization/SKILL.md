---
name: rust-optimization
description: 当用户要求Rust性能优化、缓存策略、并行计算、内存优化或线性规划加速时使用。
---

# Rust Optimization Skill

## 适用范围
- Rust 性能与内存优化
- 缓存/并行计算策略
- 线性规划与数值计算加速

## 关键规则（Critical Rules）
- 高频静态数据优先缓存，使用 `moka`
- CPU 密集任务使用 `rayon` 或 `tokio::task::spawn_blocking`
- 避免无意义 clone，优先借用切片与引用
- 异步上下文中避免阻塞调用

## 快速模板
### Moka 缓存
```rust
use moka::future::Cache;
use std::time::Duration;

pub struct MaterialCache {
    cache: Cache<String, crate::material::material::Material>,
}

impl MaterialCache {
    pub fn new() -> Self {
        Self {
            cache: Cache::builder()
                .max_capacity(1000)
                .time_to_live(Duration::from_secs(3600))
                .build(),
        }
    }
}
```

### Rayon 并行
```rust
use rayon::prelude::*;

let totals: Vec<f64> = materials
    .par_iter()
    .map(|m| m.price)
    .collect();
```

### 阻塞计算下沉
```rust
let result = tokio::task::spawn_blocking(move || heavy_calc(input))
    .await?;
```

## 优化要点
- 大量查询前先裁剪数据范围
- 频繁计算值可缓存，避免重复计算
- 共享只读配置使用 `Arc`，可变状态用 `tokio::sync`

## 检查清单
- [ ] 是否存在重复计算可缓存
- [ ] CPU 密集任务是否并行化
- [ ] 异步路径无阻塞调用
- [ ] clone 明确且必要
