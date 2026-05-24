---
name: rust-coroutine
description: "协程与绿色线程专家。处理 generator, suspend/resume, stackful coroutine, stackless coroutine, context switch, 协程, 绿色线程, 上下文切换, 生成器"
globs: ["**/*.rs"]
---

# 协程与绿色线程

## 核心问题

**如何实现高效的轻量级并发？**

协程提供用户态的上下文切换，避免内核线程的开销。

---

## 协程 vs 线程

| 特性 | OS 线程 | 协程 |
|-----|--------|------|
| 调度 | 内核 | 用户态 |
| 切换开销 | ~1μs | ~100ns |
| 数量限制 | 数千 | 数十万 |
| 栈大小 | 1-8MB | 几 KB |
| 抢占 | 抢占式 | 协作式 |

---

## Rust 原生 Generator

```rust
// Rust Nightly 的 generator
#![feature(generators)]
#![feature(generator_trait)]

use std::ops::Generator;

fn simple_generator() -> impl Generator<Yield = i32, Return = ()> {
    || {
        yield 1;
        yield 2;
        yield 3;
        // Generator 完成
    }
}

fn main() {
    let mut gen = simple_generator();
    loop {
        match unsafe { Pin::new_unchecked(&mut gen).resume() } {
            GeneratorState::Yielded(v) => println!("Yielded: {}", v),
            GeneratorState::Complete(()) => {
                println!("Done!");
                break;
            }
        }
    }
}
```

---

## 栈式协程 (Stackful Coroutine)

```rust
// 使用 stackful 协程库
use corosensei::{Coroutine, Pin, Unpin};

fn runner<'a>(start: bool, coroutine: &'a Coroutine<'_, ()>) {
    if start {
        println!("Starting coroutine");
        coroutine.run();
    }
}

fn main() {
    let coroutine = Coroutine::new(|_| {
        println!("  In coroutine - 1");
        corosensei::yield!();
        println!("  In coroutine - 2");
        corosensei::yield!();
        println!("  In coroutine - 3");
    });

    let mut pin = Pin::new(&coroutine);
    unsafe { pin.as_mut().set_running(true) };

    println!("Main: first resume");
    unsafe { pin.resume(false) }; // false = 不是第一次

    println!("Main: second resume");
    unsafe { pin.resume(false) };

    println!("Main: third resume");
    unsafe { pin.resume(false) };

    println!("Main: done");
}
```

---

## 栈式协程设计模式

### 1. 协程状态机

```rust
enum CoroutineState {
    Init,
    Processing,
    Waiting,
    Done,
}

struct StatefulCoroutine {
    state: CoroutineState,
    data: Vec<u8>,
}

impl StatefulCoroutine {
    fn new() -> Self {
        Self {
            state: CoroutineState::Init,
            data: Vec::new(),
        }
    }

    fn step(&mut self) {
        match self.state {
            CoroutineState::Init => {
                println!("Initialize");
                self.state = CoroutineState::Processing;
            }
            CoroutineState::Processing => {
                println!("Processing data");
                self.state = CoroutineState::Waiting;
            }
            CoroutineState::Waiting => {
                println!("Waiting for I/O");
                self.state = CoroutineState::Done;
            }
            CoroutineState::Done => {
                println!("Already done");
            }
        }
    }
}
```

### 2. 协程池

```rust
use std::sync::Arc;
use std::thread;
use std::sync::mpsc;

struct CoroutinePool {
    workers: Vec<thread::JoinHandle<()>>,
    sender: mpsc::Sender<Job>,
}

struct Job {
    data: Vec<u8>,
    result_tx: mpsc::Sender<Result<Vec<u8>, ()>>,
}

impl CoroutinePool {
    pub fn new(size: usize) -> Self {
        let (sender, receiver) = mpsc::channel();
        let receiver = Arc::new(receiver);
        
        let workers = (0..size)
            .map(|_| {
                let receiver = Arc::clone(&receiver);
                thread::spawn(move || {
                    while let Ok(job) = receiver.recv() {
                        // 处理 job
                        let result = process_job(&job);
                        let _ = job.result_tx.send(result);
                    }
                })
            })
            .collect();

        Self { workers, sender }
    }

    pub fn submit(&self, data: Vec<u8>) -> mpsc::Receiver<Result<Vec<u8>, ()>> {
        let (result_tx, result_rx) = mpsc::channel();
        let job = Job { data, result_tx };
        self.sender.send(job).unwrap();
        result_rx
    }
}

fn process_job(job: &Job) -> Result<Vec<u8>, ()> {
    Ok(job.data.clone())
}
```

---

## 栈无关协程 (Stackless Coroutine)

```rust
// 使用 async/await 实现栈无关协程
async fn async_task(id: u32) -> u32 {
    println!("Task {} started", id);
    
    // 模拟 I/O 操作
    tokio::time::sleep(std::time::Duration::from_millis(100)).await;
    
    println!("Task {} resumed", id);
    id * 2
}

async fn main() {
    // 并发执行多个协程
    let results = futures::future::join_all(
        (0..10).map(|i| async_task(i))
    ).await;
    
    println!("Results: {:?}", results);
}
```

---

## 上下文切换机制

```rust
// 手动上下文切换
use std::arch::asm;

struct Context {
    rsp: u64,
    r15: u64,
    r14: u64,
    r13: u64,
    r12: u64,
    rbp: u64,
    rbx: u64,
}

impl Context {
    unsafe fn new(stack: &mut [u8]) -> Self {
        let stack_top = stack.as_mut_ptr().add(stack.len());
        let rsp = (stack_top as *mut u64).wrapping_sub(1) as u64;
        
        Self {
            rsp,
            r15: 0,
            r14: 0,
            r13: 0,
            r12: 0,
            rbp: 0,
            rbx: 0,
        }
    }
    
    unsafe fn switch(&mut self, next: &mut Context) {
        asm!(
            "push rbx",
            "push rbp",
            "push r12",
            "push r13",
            "push r14",
            "push r15",
            "mov [rdi], rsp",     // 保存当前栈指针
            "mov rsp, [rsi]",     // 切换到新栈
            "pop r15",
            "pop r14",
            "pop r13",
            "pop r12",
            "pop rbp",
            "pop rbx",
            in("rdi") self as *mut Context,
            in("rsi") next as *mut Context,
        );
    }
}
```

---

## 协程调度器

```rust
// 简单协程调度器
enum Task {
    Coroutine(fn(&mut Scheduler)),
    Finished,
}

struct Scheduler {
    ready: Vec<Task>,
    current: Option<Task>,
}

impl Scheduler {
    pub fn new() -> Self {
        Self {
            ready: Vec::new(),
            current: None,
        }
    }

    pub fn spawn(&mut self, task: Task) {
        self.ready.push(task);
    }

    pub fn run(&mut self) {
        while let Some(task) = self.ready.pop() {
            self.current = Some(task);
            match std::mem::replace(&mut self.ready, vec![]) {
                Task::Coroutine(f) => f(self),
                Task::Finished => continue,
            }
        }
    }
}
```

---

## 常见问题

| 问题 | 原因 | 解决 |
|-----|------|-----|
| 协程不执行 | 缺少调度器 | 实现或使用调度器 |
| 栈溢出 | 递归太深 | 使用堆分配栈 |
| 内存泄漏 | 任务未完成 | 正确清理协程 |
| 死锁 | 循环等待 | 避免循环依赖 |

---

## 与其他技能关联

```
rust-coroutine
    │
    ├─► rust-async → async/await 实现
    ├─► rust-concurrency → 并发模型
    └─► rust-performance → 性能优化
```

