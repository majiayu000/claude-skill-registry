# Rust Agent Specialist Workflow

Apply Rust-native patterns to ccswarm codebase development.

## Overview

This skill provides guidance for implementing Rust-idiomatic patterns in the ccswarm multi-agent orchestration system.

## Core Patterns

### Type-State Pattern

Compile-time state validation with zero runtime cost.

```rust
// State types
pub struct Uninitialized;
pub struct Initialized;
pub struct Running;

pub struct Agent<State> {
    inner: AgentInner,
    _state: PhantomData<State>,
}

impl Agent<Uninitialized> {
    pub fn new() -> Self { /* ... */ }
    pub fn initialize(self) -> Agent<Initialized> { /* ... */ }
}

impl Agent<Initialized> {
    pub fn start(self) -> Agent<Running> { /* ... */ }
}

impl Agent<Running> {
    pub fn execute(&self, task: Task) -> Result<Output> { /* ... */ }
}
```

### Channel-Based Orchestration

Replace Arc<Mutex> with message-passing.

```rust
use tokio::sync::mpsc;

pub struct Orchestrator {
    task_tx: mpsc::Sender<Task>,
}

pub struct Worker {
    task_rx: mpsc::Receiver<Task>,
    result_tx: mpsc::Sender<Result<Output>>,
}

// No shared mutable state
async fn run_worker(mut worker: Worker) {
    while let Some(task) = worker.task_rx.recv().await {
        let result = process_task(task).await;
        let _ = worker.result_tx.send(result).await;
    }
}
```

### Actor Model

Each agent as an independent actor.

```rust
pub struct AgentActor {
    mailbox: mpsc::Receiver<Message>,
    state: AgentState,
}

impl AgentActor {
    pub async fn run(mut self) {
        while let Some(msg) = self.mailbox.recv().await {
            match msg {
                Message::Task(task) => self.handle_task(task).await,
                Message::Query(q) => self.handle_query(q).await,
                Message::Shutdown => break,
            }
        }
    }
}
```

## Workflow

### 1. Analyze Current Code

```bash
# Find shared state patterns
grep -r "Arc<Mutex" crates/ccswarm/src --include="*.rs"

# Find potential type-state candidates
grep -r "enum.*State\|State::" crates/ccswarm/src --include="*.rs"
```

### 2. Identify Refactoring Targets

- Functions with state validation at runtime
- Shared mutable state across threads
- Large match statements for state handling

### 3. Apply Patterns

1. Convert runtime state checks to type-state
2. Replace Arc<Mutex> with channels where possible
3. Implement actor pattern for agents

### 4. Verify

```bash
cargo fmt && cargo clippy -- -D warnings && cargo test
```

## Guidelines

### DO
- Use type-state for state machines
- Prefer channels over shared memory
- Keep actors independent
- Use oneshot for request-response

### DON'T
- Use Arc<Mutex> for simple coordination
- Share mutable state between agents
- Hold locks across await points
- Over-abstract simple patterns

## Reference Implementation

See `crates/ccswarm/src/agent/` for agent implementations.
See `crates/ccswarm/src/orchestrator/` for orchestration patterns.
