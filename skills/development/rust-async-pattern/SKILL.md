---
name: rust-async-pattern
description: "高级异步模式专家。处理 Stream 实现, 零拷贝, tokio::spawn 生命周期, 插件系统调度, tonic 流式响应等问题。触发词：async, Stream, tokio::spawn, 零拷贝, 插件系统, tonic, 流式, BorrowedMessage, 异步调度"
globs: ["**/*.rs"]
---

# 高级异步模式

## 核心问题

**异步代码的生命周期怎么这么难管？**

async 让生命周期问题更复杂。

---

## Stream + 自引用缓冲区

### 问题代码

```rust
// ❌ Stream 实现中返回借用内部缓冲区的 slice
pub struct SessionStream<'buf> {
    buf: Vec<u8>,
    cache: Vec<CachedResponse<'buf>>,
}

impl Stream for SessionStream<'buf> {
    type Item = Result<CachedResponse<'buf>, Status>;
    
    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        // ❌ 返回的 CachedResponse<'buf> 生命周期依赖于 self.buf
        // 但 Stream trait 的 Item 必须能在任意时刻被使用
    }
}
```

### 错误信息

```
error[E0700]: hidden type for `impl futures_core::Stream` captures lifetime that does not appear in bounds
error[E0310]: the parameter type may not live long enough
```

### 原因

- Stream 的 Item 可以被任意持有
- `'buf` 和 `self` 绑定在一起
- 返回的 Item 逃逸了 self 的生命周期

### 解决：Worker + Channel 模式

```rust
// ✅ 内部 worker 持有缓冲区，对外只发 owned snapshot
pub struct SessionWorker {
    rx_events: Receiver<Bytes>,
    tx_snapshots: Sender<SnapshotResponse>,
    buf: Vec<u8>,
}

impl SessionWorker {
    pub async fn run(&mut self) {
        while let Some(event) = self.rx_events.recv().await {
            let snapshot = self.process_event(event);
            self.tx_snapshots.send(snapshot).await;
        }
    }
    
    fn process_event(&mut self, event: Bytes) -> SnapshotResponse {
        // 内部可以借用 self.buf
        let start = self.buf.len();
        self.buf.extend_from_slice(&event);
        
        // 但对外发的是 owned SnapshotResponse
        SnapshotResponse {
            id: self.next_id,
            payload: Bytes::copy_from_slice(&self.buf[start..]),
        }
    }
}

// ✅ Stream 只读 channel，发的都是 owned
pub struct SessionStream {
    rx_snapshots: Receiver<SnapshotResponse>,
}

impl Stream for SessionStream {
    type Item = Result<SnapshotResponse, Status>;
    
    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        // 这里发的都是 SnapshotResponse (owned)，没问题
    }
}
```

---

## tokio::spawn + 非 'static 生命周期

### 问题代码

```rust
// ❌ tokio::spawn 要求 'static，但 BorrowedMessage<'a> 不是
pub struct BorrowedMessage<'a> {
    pub raw: &'a [u8],
    pub meta: MessageMeta,
}

pub trait Plugin: Send + Sync {
    fn handle<'a>(&'a self, msg: BorrowedMessage<'a>)
        -> Pin<Box<dyn Future<Output = Result<(), HandlerError>> + Send + 'a>>;
}

fn dispatch_to_plugins(msg: BorrowedMessage<'a>) {
    for p in &plugins {
        let fut = p.handle(msg);
        tokio::spawn(fut);  // ❌ fut 不是 'static
    }
}
```

### 原因

- tokio::spawn 不知道任务何时完成
- 如果任务持有 `'a` 引用，`'a` 可能已过期

### 解决：事件循环 + Actor 模式

```rust
// ✅ 不 spawn，每个插件是一个长期存在的 actor
struct PluginActor<M: MessageHandler> {
    plugin: M,
    queue: Receiver<PluginMsg>,
    arena: MessageArena,
}

impl<M: MessageHandler> PluginActor<M> {
    pub async fn run(&mut self) {
        while let Some(msg) = self.queue.recv().await {
            // 在 arena 域内处理消息
            self.arena.with_message(msg, |msg_ref| {
                self.plugin.handle(msg_ref);
            });
        }
    }
}

// ✅ 用索引代替直接借用
pub struct MessageRef {
    index: usize,
    generation: u64,
}

struct MessageArena {
    buffers: Vec<Arc<Buffer>>,
}

impl MessageArena {
    pub fn get(&self, ref: MessageRef) -> Option<&[u8]> {
        // 通过索引安全获取
        self.buffers.get(ref.index)?.get(ref.generation)
    }
}
```

---

## 插件系统调度模式

### 约束

1. 零拷贝缓冲区复用
2. 插件热插拔
3. 异步 handler
4. 可重试/延后 ack

### 最终架构

```
┌─────────────────────────────────────┐
│          Decode Layer               │  持有缓冲区
├─────────────────────────────────────┤
│           MessageArena              │  缓冲区管理
├─────────────────────────────────────┤
│           Event Loop                │  协作式调度
├─────────────────────────────────────┤
│           Plugin Actor              │  每个插件一个
└─────────────────────────────────────┘
│
↓  API 层只看到 owned 数据
┌─────────────────────────────────────┐
│         GraphQL / gRPC              │  'static 要求
└─────────────────────────────────────┘
```

### 关键设计

```rust
// 1. 缓冲区管理域
struct MessageArena {
    buffers: Vec<Arc<Buffer>>,
    free_list: Vec<usize>,
}

impl MessageArena {
    // 分配时返回索引，不是引用
    fn alloc(&mut self, data: &[u8]) -> MessageRef {
        let idx = self.buffers.len();
        self.buffers.push(Arc::new(data.to_vec()));
        MessageRef { index: idx, generation: 0 }
    }
}

// 2. API 层只暴露 owned
pub trait Plugin: Send + Sync {
    async fn handle(&self, msg: OwnedMessage);  // owned
}
```

---

## 常见问题速查

| 问题 | 原因 | 解决 |
|-----|------|-----|
| Stream 返回借用 | Item 生命周期逃逸 | Worker + Channel |
| tokio::spawn 非 'static | 任务可能持有临时引用 | 事件循环模式 |
| 插件 handler 生命周期 | 插件持有消息 | Actor + 索引 |
| async-graphql + GAT | 'static 要求 | owned DTO |
| tonic Stream 自引用 | 缓冲区复用冲突 | Snapshot 模式 |

---

## 何时用 spawn，何时用 actor

| 场景 | 方案 |
|-----|-----|
| 独立任务，可并行 | tokio::spawn |
| 需要协作调度 | Event Loop |
| 插件系统 | Actor 模式 |
| 长期运行的状态ful | Actor |
| 短命任务 | spawn |
| 需要背压控制 | Channel + actor |

