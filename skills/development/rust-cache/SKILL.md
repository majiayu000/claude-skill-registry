---
name: rust-cache
description: "Redis 缓存管理、连接池、TTL策略、模式匹配删除、性能优化"
category: infrastructure
triggers: ["cache", "redis", "ttl", "connection", "性能优化", "缓存"]
related_skills:
  - rust-concurrency
  - rust-async
  - rust-performance
  - rust-error
---

# Rust Cache - 缓存管理技能

> 本技能提供 Redis 缓存的系统化解决方案，包括连接管理、缓存策略、性能优化等。

## 核心概念

### 1. 缓存架构设计

```
缓存层设计模式
├── 缓存管理器 (CacheManager)
│   ├── 连接管理 (ConnectionManager)
│   ├── 序列化/反序列化
│   ├── TTL 控制
│   └── 统计信息
├── 缓存键生成器 (CacheKeyBuilder)
│   ├── 命名空间前缀
│   └── 业务标识
└── 缓存策略
    ├── Cache-Aside (旁路缓存)
    ├── Write-Through (写穿透)
    └── Write-Behind (写回)
```

### 2. 性能提升数据

| 场景 | 无缓存 | 有缓存 | 提升 |
|-----|-------|-------|------|
| 复杂查询 | ~100ms | <5ms | **95%+** |
| 频繁访问 | ~50ms | <2ms | **96%** |

---

## 核心模式

### 1. 缓存管理器实现

```rust
//! 缓存管理器实现
//!
//! 提供分布式 Redis 缓存的通用模式

use redis::{aio::ConnectionManager, AsyncCommands};
use serde::{de::DeserializeOwned, Serialize};
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::RwLock;

/// 缓存管理器
pub struct CacheManager {
    /// 配置
    config: CacheConfig,
    /// Redis 连接管理器
    redis: Option<ConnectionManager>,
    /// 统计信息
    stats: Arc<RwLock<CacheStats>>,
}

impl CacheManager {
    /// 创建新的缓存管理器（带超时控制）
    pub async fn new(config: CacheConfig) -> Result<Self, CacheError> {
        let redis = if config.enabled && config.redis.enabled {
            // 创建 Redis 客户端
            let client = redis::Client::open(config.redis.url.as_str())
                .map_err(|e| CacheError::Connection(format!("Redis 连接失败: {}", e)))?;

            // 超时控制（适应远程 Redis）
            let timeout = Duration::from_secs(30);
            
            match tokio::time::timeout(timeout, ConnectionManager::new(client)).await {
                Ok(Ok(conn)) => Some(conn),
                Ok(Err(e)) => return Err(CacheError::Connection(format!("Redis 连接失败: {}", e))),
                Err(_) => return Err(CacheError::Timeout(format!("Redis 连接超时（{}秒）", timeout.as_secs()))),
            }
        } else {
            None
        };

        Ok(Self {
            config,
            redis,
            stats: Arc::new(RwLock::new(CacheStats::new())),
        })
    }

    /// 获取缓存
    pub async fn get<T: DeserializeOwned>(&self, key: &str) -> Result<Option<T>, CacheError> {
        if !self.config.enabled {
            return Ok(None);
        }

        // 增加请求计数
        {
            let mut stats = self.stats.write().await;
            stats.total_requests += 1;
        }

        if let Some(mut redis) = self.redis.clone() {
            match redis.get::<&str, Vec<u8>>(key).await {
                Ok(bytes) if !bytes.is_empty() => {
                    // 更新统计
                    {
                        let mut stats = self.stats.write().await;
                        stats.redis_hits += 1;
                    }
                    self.deserialize(&bytes)
                }
                Ok(_) => {
                    let mut stats = self.stats.write().await;
                    stats.redis_misses += 1;
                    Ok(None)
                }
                Err(e) => {
                    log::warn!("Redis 读取失败: key={}, error={}", key, e);
                    let mut stats = self.stats.write().await;
                    stats.redis_misses += 1;
                    Ok(None)  // 缓存失败不应影响业务
                }
            }
        } else {
            Ok(None)
        }
    }

    /// 设置缓存（带 TTL）
    pub async fn set<T: Serialize>(
        &self,
        key: &str,
        value: &T,
        ttl: Option<u64>,
    ) -> Result<(), CacheError> {
        if !self.config.enabled {
            return Ok(());
        }

        let bytes = self.serialize(value)?;

        if let Some(mut redis) = self.redis.clone() {
            let ttl_seconds = ttl.unwrap_or(self.config.default_ttl);
            match redis.set_ex::<&str, Vec<u8>, ()>(key, bytes, ttl_seconds).await {
                Ok(_) => log::debug!("Redis 写入: key={}, ttl={}s", key, ttl_seconds),
                Err(e) => log::warn!("Redis 写入失败: key={}, error={}", key, e),
            }
        }

        Ok(())
    }

    /// 删除缓存
    pub async fn delete(&self, key: &str) -> Result<(), CacheError> {
        if let Some(mut redis) = self.redis.clone() {
            match redis.del::<&str, ()>(key).await {
                Ok(_) => log::debug!("Redis 删除: {}", key),
                Err(e) => log::warn!("Redis 删除失败: key={}, error={}", key, e),
            }
        }
        Ok(())
    }

    /// 序列化
    fn serialize<T: Serialize>(&self, value: &T) -> Result<Vec<u8>, CacheError> {
        serde_json::to_vec(value).map_err(|e| {
            CacheError::Serialization(format!("序列化失败: {}", e))
        })
    }

    /// 反序列化
    fn deserialize<T: DeserializeOwned>(&self, bytes: &[u8]) -> Result<Option<T>, CacheError> {
        if bytes.is_empty() {
            return Ok(None);
        }
        
        match serde_json::from_slice(bytes) {
            Ok(value) => Ok(Some(value)),
            Err(e) => {
                log::warn!("反序列化失败: {}", e);
                Ok(None)  // 损坏数据应跳过，不返回错误
            }
        }
    }
}

/// 缓存统计信息
#[derive(Debug, Clone, Default)]
pub struct CacheStats {
    pub total_requests: u64,
    pub redis_hits: u64,
    pub redis_misses: u64,
}

impl CacheStats {
    pub fn new() -> Self {
        Self::default()
    }

    /// 命中率
    pub fn hit_rate(&self) -> f64 {
        if self.total_requests == 0 {
            0.0
        } else {
            self.redis_hits as f64 / self.total_requests as f64 * 100.0
        }
    }
}

/// 缓存错误类型
#[derive(Debug, thiserror::Error)]
pub enum CacheError {
    #[error("连接错误: {0}")]
    Connection(String),
    #[error("超时错误: {0}")]
    Timeout(String),
    #[error("序列化错误: {0}")]
    Serialization(String),
    #[error("Redis 错误: {0}")]
    Redis(#[from] redis::RedisError),
}
```

### 2. 缓存键设计模式

```rust
/// 缓存键生成器
///
/// 设计原则：
/// 1. 使用命名空间前缀避免 key 冲突
/// 2. 包含业务标识便于问题排查
/// 3. 支持版本控制便于缓存更新
pub struct CacheKeyBuilder;

impl CacheKeyBuilder {
    /// 构建带命名空间的键
    /// 格式: {namespace}:{entity}:{id}
    pub fn build(namespace: &str, entity: &str, id: impl std::fmt::Display) -> String {
        format!("{}:{}:{}", namespace, entity, id)
    }

    /// 构建列表缓存键
    /// 格式: {namespace}:{entity}:list:{query_hash}
    pub fn list_key(namespace: &str, entity: &str, query: &str) -> String {
        use sha2::{Digest, Sha256};
        let mut hasher = Sha256::new();
        hasher.update(query.as_bytes());
        let hash = format!("{:x}", hasher.finalize());
        format!("{}:{}:list:{}", namespace, entity, &hash[..8])
    }

    /// 构建模式匹配键
    /// 格式: {namespace}:{entity}:*
    pub fn pattern(namespace: &str, entity: &str) -> String {
        format!("{}:{}:*", namespace, entity)
    }

    /// 构建版本化键
    /// 格式: {namespace}:{entity}:{id}:v{version}
    pub fn versioned(namespace: &str, entity: &str, id: impl std::fmt::Display, version: u64) -> String {
        format!("{}:{}:{}:v{}", namespace, entity, id, version)
    }
}
```

### 3. 批量缓存删除模式

```rust
impl CacheManager {
    /// 批量删除缓存（支持模式匹配）
    ///
    /// 使用 SCAN 命令遍历删除，避免 DEL 阻塞
    pub async fn delete_pattern(&self, pattern: &str) -> Result<usize, CacheError> {
        let mut deleted_count = 0;
        
        if let Some(redis) = &self.redis {
            let mut cursor: u64 = 0;
            
            loop {
                let result: std::result::Result<(u64, Vec<String>), redis::RedisError> = 
                    redis::cmd("SCAN")
                        .arg(cursor)
                        .arg("MATCH")
                        .arg(pattern)
                        .arg("COUNT")
                        .arg(100)
                        .query_async(&mut redis.clone())
                        .await;
                
                match result {
                    Ok((new_cursor, keys)) => {
                        if !keys.is_empty() {
                            let del_result: std::result::Result<(), redis::RedisError> = 
                                redis::cmd("DEL").arg(&keys).query_async(&mut redis.clone()).await;
                            
                            if del_result.is_ok() {
                                deleted_count += keys.len();
                            }
                        }
                        cursor = new_cursor;
                        if cursor == 0 {
                            break;
                        }
                    }
                    Err(e) => {
                        log::warn!("Redis SCAN 失败: {}", e);
                        break;
                    }
                }
            }
            
            log::info!("批量删除完成: pattern={}, deleted={}", pattern, deleted_count);
        }

        Ok(deleted_count)
    }
}
```

---

## 配置管理

### 1. 缓存配置

```rust
/// 缓存配置
#[derive(Debug, Clone)]
pub struct CacheConfig {
    pub enabled: bool,
    pub redis: RedisConfig,
    pub default_ttl: u64,  // 默认 TTL（秒）
}

#[derive(Debug, Clone)]
pub struct RedisConfig {
    pub enabled: bool,
    pub url: String,
    pub pool_size: u32,
    pub max_retries: u32,
}

impl Default for CacheConfig {
    fn default() -> Self {
        Self {
            enabled: true,
            redis: RedisConfig {
                enabled: true,
                url: "redis://localhost:6379".to_string(),
                pool_size: 10,
                max_retries: 3,
            },
            default_ttl: 3600,  // 默认 1 小时
        }
    }
}
```

---

## 最佳实践

### 1. 缓存策略选择

| 策略 | 适用场景 | 优点 | 缺点 |
|-----|---------|------|------|
| **Cache-Aside** | 读多写少 | 简单、可靠 | 缓存不一致风险 |
| **Write-Through** | 数据一致性要求高 | 强一致性 | 写入延迟增加 |
| **Write-Behind** | 高写入吞吐量 | 写入性能高 | 数据丢失风险 |

### 2. TTL 分层设计

```rust
/// TTL 分层设计
pub struct CacheTTL {
    pub short: u64 = 300,     // 5 分钟 - 热数据
    pub medium: u64 = 3600,   // 1 小时 - 中频数据
    pub long: u64 = 86400,    // 24 小时 - 低频数据
    pub static_data: u64 = 604800,  // 7 天 - 静态数据
}

/// 使用示例
impl CacheManager {
    /// 存储高频访问数据 - 5 分钟
    pub async fn set_hot_data<T: Serialize>(&self, key: &str, data: &T) -> Result<()> {
        self.set(key, data, Some(300)).await
    }

    /// 存储中频数据 - 1 小时
    pub async fn set_medium_data<T: Serialize>(&self, key: &str, data: &T) -> Result<()> {
        self.set(key, data, Some(3600)).await
    }

    /// 存储低频数据 - 24 小时
    pub async fn set_cold_data<T: Serialize>(&self, key: &str, data: &T) -> Result<()> {
        self.set(key, data, Some(86400)).await
    }
}
```

### 3. 缓存穿透防护

```rust
/// 缓存穿透防护
pub struct CacheBreaker<K, T> {
    manager: Arc<CacheManager>,
    _phantom: std::marker::PhantomData<(K, T)>,
}

impl<K, T> CacheBreaker<K, T>
where
    K: std::fmt::Display + Clone + Send + Sync,
    T: DeserializeOwned + Serialize + Clone,
{
    pub fn new(manager: Arc<CacheManager>) -> Self {
        Self { manager, _phantom: std::marker::PhantomData }
    }

    /// 获取数据（带缓存保护）
    pub async fn get_or_load<F, Fut>(&self, key: &str, loader: F) -> Result<Option<T>>
    where
        F: FnOnce() -> Fut,
        Fut: std::future::Future<Output = Result<Option<T>>>,
    {
        // 1. 尝试从缓存获取
        if let Some(cached) = self.manager.get::<T>(key).await? {
            return Ok(Some(cached));
        }

        // 2. 缓存未命中，从数据源加载
        let result = loader().await?;

        // 3. 将结果写入缓存
        if let Some(ref value) = result {
            self.manager.set(key, value, None).await?;
        }

        Ok(result)
    }
}
```

### 4. 缓存雪崩防护

```rust
/// 缓存雪崩防护：随机 TTL 抖动
fn calculate_jitter_ttl(base_ttl: u64) -> u64 {
    let jitter = (base_ttl as f64 * 0.1)..(base_ttl as f64 * 0.2);
    let jitter_seconds = rand::thread_rng().gen_range(jitter);
    (base_ttl as f64 + jitter_seconds) as u64
}

/// 使用示例
pub async fn set_with_jitter(
    cache: &CacheManager,
    key: &str,
    value: &impl Serialize,
    base_ttl: u64,
) -> Result<()> {
    let ttl = calculate_jitter_ttl(base_ttl);
    cache.set(key, value, Some(ttl)).await
}
```

---

## 监控与指标

```rust
use prometheus::{Counter, Histogram, Gauge};

/// 缓存指标
#[derive(Debug)]
pub struct CacheMetrics {
    pub hits: Counter,
    pub misses: Counter,
    pub operations: Histogram,
    pub latency: Histogram,
    pub size: Gauge,
}

impl CacheMetrics {
    pub fn new() -> Self {
        Self {
            hits: Counter::new("cache_hits_total", "Cache hits total"),
            misses: Counter::new("cache_misses_total", "Cache misses total"),
            operations: Histogram::new(
                "cache_operation_duration_seconds",
                "Cache operation duration",
                vec![0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0],
            ),
            latency: Histogram::new(
                "cache_latency_seconds",
                "Cache latency",
                vec![0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05],
            ),
            size: Gauge::new("cache_size", "Cache size"),
        }
    }

    pub fn record_hit(&self) {
        self.hits.inc();
    }

    pub fn record_miss(&self) {
        self.misses.inc();
    }

    pub fn hit_rate(&self) -> f64 {
        let hits = self.hits.get() as f64;
        let total = hits + self.misses.get() as f64;
        if total > 0.0 { hits / total * 100.0 } else { 0.0 }
    }
}
```

---

## 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|-----|---------|---------|
| 缓存命中率低 | TTL 设置不当 | 调整 TTL，区分热冷数据 |
| Redis 连接超时 | 网络延迟或连接池耗尽 | 增加超时，扩大连接池 |
| 缓存与数据库不一致 | 并发写入未加锁 | 使用分布式锁 |
| 内存使用过高 | 缓存数据过大 | 启用压缩，设置容量上限 |
| 批量删除阻塞 | 使用 DEL 而非 SCAN | 改用 SCAN 模式删除 |

---

## 关联技能

- `rust-concurrency` - 并发访问控制
- `rust-async` - 异步操作模式
- `rust-performance` - 性能优化
- `rust-error` - 错误处理
