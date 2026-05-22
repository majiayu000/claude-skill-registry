---
name: rust-actor
description: "Actor 模型专家。处理 Actor 死锁, 消息传递, 状态管理, supervision, 容错, Actix, Erlang 风格并发"
globs: ["**/*.rs"]
---

# Actor 模型

## 核心问题

**如何在并发系统中避免死锁并实现可靠的进程间通信？**

Actor 模型通过消息传递和状态隔离来简化并发。

---

## Actor vs 线程模型

| 特性 | 线程模型 | Actor 模型 |
|-----|---------|-----------|
| 状态共享 | 共享内存 + 锁 | 无共享，消息传递 |
| 死锁风险 | 高（锁顺序） | 低（消息队列） |
| 扩展性 | 受限于线程数 | 可扩展到百万级 |
| 故障处理 | 手动 | Supervision 树 |
| 调试难度 | 难（竞态条件） | 相对容易（消息序列） |

---

## Actor 核心结构

```rust
// Actor 基础 trait
trait Actor: Send + 'static {
    type Message: Send + 'static;
    type Error: std::error::Error;
    
    fn receive(&mut self, ctx: &mut Context<Self::Message>, msg: Self::Message);
}

// Actor 上下文
struct Context<A: Actor> {
    mailbox: Receiver<A::Message>,
    sender: Sender<A::Message>,
    state: ActorState,
    supervisor: Option<SupervisorAddr>,
}

enum ActorState {
    Starting,
    Running,
    Restarting,
    Stopping,
    Stopped,
}
```

---

## 消息传递

```rust
// 同步消息
fn sync_request<A: Actor, R>(
    actor: &Addr<A>,
    msg: A::Message,
    timeout: Duration,
) -> Result<R, A::Error> {
    let (tx, rx) = channel();
    let request = Request {
        payload: msg,
        response: tx,
    };
    
    actor.send(request)?;
    
    rx.recv_timeout(timeout)?
}

// 异步消息
fn async_send<A: Actor>(actor: &Addr<A>, msg: A::Message) {
    actor.send(msg);
}

// 消息信封
enum Envelope<A: Actor> {
    Async(A::Message),
    Request {
        payload: A::Message,
        response: Sender<Result<A::Response, A::Error>>,
    },
    Signal(ActorSignal),
}
```

---

## 死锁预防

```rust
// 1. 避免循环等待：使用唯一消息顺序
enum GlobalMessage {
    // 按固定顺序排列
    UserMsg(UserMessage),
    SystemMsg(SystemMessage),
    InternalMsg(InternalMessage),
}

// 2. 超时机制
fn send_with_timeout<A: Actor, M: Send + 'static>(
    addr: &Addr<A>,
    msg: M,
    timeout: Duration,
) -> Result<(), SendError<M>> {
    let (tx, rx) = channel();
    
    addr.send(AsyncWrapper { msg, reply_to: tx });
    
    rx.recv_timeout(timeout)
        .map(|_| ())
        .map_err(|_| SendError::Timeout)
}

// 3. 限制邮箱大小（背压）
struct BoundedMailbox<A: Actor> {
    receiver: Receiver<A::Message>,
    sender: Sender<A::Message>,
    capacity: usize,
}

impl<A: Actor> Mailbox for BoundedMailbox<A> {
    fn capacity(&self) -> usize {
        self.capacity
    }
}
```

---

## Supervision 树

```rust
// Supervision 策略
enum SupervisionStrategy {
    OneForOne,    // 只重启出错的子 actor
    AllForOne,    // 一个出错，全部重启
    RestForOne,   // 出错的和之后的重启
}

struct Supervisor {
    children: HashMap<ChildId, Child>,
    strategy: SupervisionStrategy,
    max_restarts: u32,
    window: Duration,
}

impl Supervisor {
    fn handle_child_error(&mut self, child_id: ChildId, error: &dyn std::error::Error) {
        let child = self.children.get_mut(&child_id).unwrap();
        child.restart_count += 1;
        
        if self.should_restart(child_id) {
            self.restart_child(child_id);
        } else {
            self.stop_child(child_id);
        }
    }
    
    fn should_restart(&self, child_id: ChildId) -> bool {
        let child = &self.children[&child_id];
        child.restart_count <= self.max_restarts
    }
}
```

---

## 状态管理

```rust
// Actor 内部状态
struct UserActor {
    id: UserId,
    session: Option<Session>,
    message_history: Vec<Message>,
    followers: HashSet<UserId>,
}

impl Actor for UserActor {
    type Message = UserMessage;
    
    fn receive(&mut self, ctx: &mut Context<Self::Message>, msg: Self::Message) {
        match msg {
            UserMessage::Login(session) => {
                self.session = Some(session);
            }
            UserMessage::Post(content) => {
                if let Some(session) = &self.session {
                    self.message_history.push(Message {
                        content,
                        timestamp: Utc::now(),
                        user: session.user_id,
                    });
                }
            }
            UserMessage::Follow(target_id) => {
                self.followers.insert(target_id);
            }
        }
    }
}

// 状态快照
impl UserActor {
    fn snapshot(&self) -> UserSnapshot {
        UserSnapshot {
            id: self.id,
            message_count: self.message_history.len(),
            followers_count: self.followers.len(),
            is_online: self.session.is_some(),
        }
    }
}
```

---

## Actor 生命周期

```rust
// 生命周期事件
enum LifecycleEvent {
    PreStart,
    PostStart,
    PreRestart,
    PostRestart,
    PostStop,
}

trait LifecycleHandler: Actor {
    fn pre_start(&mut self, ctx: &mut Context<Self::Message>) {
        // 初始化资源
    }
    
    fn post_start(&mut self, ctx: &mut Context<Self::Message>) {
        // 启动定时器、连接等
    }
    
    fn pre_restart(&mut self, ctx: &mut Context<Self::Message>, error: &dyn std::error::Error) {
        // 清理资源
    }
    
    fn post_stop(&mut self) {
        // 保存状态、关闭连接
    }
}
```

---

## Actix 示例

```rust
// Actix Web Actor
use actix::{Actor, Handler, Message, Context};

struct MyActor {
    counter: usize,
}

impl Actor for MyActor {
    type Context = Context<Self>;
    
    fn started(&mut self, _ctx: &mut Self::Context) {
        println!("Actor started");
    }
}

#[derive(Message)]
#[rtype(result = "usize")]
struct Increment;

impl Handler<Increment> for MyActor {
    type Result = usize;
    
    fn handle(&mut self, msg: Increment, _ctx: &mut Self::Context) -> Self::Result {
        self.counter += 1;
        self.counter
    }
}

// 使用
let actor = MyActor { counter: 0 }.start();
let result = actor.send(Increment).await?;
```

---

## 常见问题

| 问题 | 原因 | 解决 |
|-----|------|-----|
| 死锁 | 循环消息等待 | 超时、避免循环依赖 |
| 消息积压 | 消费者慢 | 背压、限流 |
| 内存泄漏 | Actor 未停止 | 生命周期管理 |
| 状态不一致 | 并发消息 | 顺序处理、单线程 |

---

## 与其他技能关联

```
rust-actor
    │
    ├─► rust-concurrency → 并发模型
    ├─► rust-async → 异步消息
    └─► rust-error → 错误传播
```

