---
name: rust-async
description: "高级异步模式专家。处理 Stream, backpressure, select, join, cancellation, Future trait 等问题。触发词：async, Stream, backpressure, select, Future, tokio, async-std, 异步, 流, 取消"
globs: ["**/*.rs"]
---

# 高级异步模式

## 核心问题

**如何在异步代码中正确处理流、控制和资源？**

异步不是并行，但异步代码有独特的复杂性。

---

## Stream 处理

```rust
use tokio_stream::{self as Stream, StreamExt};

async fn process_stream(stream: impl Stream<Item = Data>) {
    stream
        .chunks(100)           // 批量处理
        .for_each(|batch| async {
            process_batch(batch).await;
        })
        .await;
}
```

### 背压 (Backpressure)

```rust
use tokio::sync::Semaphore;

let semaphore = Semaphore::new(10);  // 最多 10 个并发

let stream = tokio_stream::iter(0..1000)
    .map(|i| {
        let permit = semaphore.clone().acquire_owned();
        async move {
            let _permit = permit.await;
            process(i).await
        }
    })
    .buffer_unordered(100);  // 最多 100 并发
```

---

## select! 多路复用

```rust
use tokio::select;
use tokio::time::{sleep, timeout};

async fn multiplex() {
    loop {
        select! {
            msg = receiver.recv() => {
                if let Ok(msg) = msg {
                    handle(msg).await;
                }
            }
            _ = sleep(Duration::from_secs(5)) => {
                // 超时处理
            }
            else => break,  // 所有分支都完成
        }
    }
}
```

---

## 任务取消

```rust
use tokio::time::timeout;

async fn with_timeout() -> Result<Value, TimeoutError> {
    timeout(Duration::from_secs(5), long_operation()).await
}

// 协作式取消
let mut task = tokio::spawn(async move {
    loop {
        // 检查取消
        if task.is_cancelled() {
            return;
        }
        // 继续工作
    }
});

// 取消任务
task.abort();
```

---

## join! vs try_join!

```rust
// 并行执行，不等待完成
let (a, b) = tokio::join!(async_a(), async_b());

// 全部成功才成功
let (a, b) = tokio::try_join!(async_a(), async_b())?;

// 错误传播
fn combined() -> impl Future<Output = Result<(A, B), E>> {
    async {
        let (a, b) = try_join!(op_a(), op_b())?;
        Ok((a, b))
    }
}
```

---

## 常见错误

| 错误 | 原因 | 解决 |
|-----|-----|-----|
| 忘记 `.await` | future 不执行 | 检查 await |
| 任务取消未处理 | 协作式取消缺失 | 检查 is_cancelled |
| 背压缺失 | 无限制并发 | Semaphore/buffer |
| 死锁 | 锁在 await 时持有 | 缩小锁范围 |
| async Drop 未实现 | 资源泄漏 | 用 tokio::spawn 清理 |

---

## 性能提示

- `select!` 比多个 `tokio::spawn` 更轻量
- `buffer_unordered` 比 `for_each_concurrent` 更灵活
- 大批量用 `.chunks()` 减少开销
- 避免在锁内 await

