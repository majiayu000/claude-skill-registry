---
name: rust-distributed
description: "分布式系统专家。处理 Raft, 2PC, 共识算法, 分布式事务, 分布式一致性, 分布式协调"
globs: ["**/*.rs"]
---

# 分布式系统

## 核心问题

**如何在分布式环境中实现数据一致性和高可用？**

分布式系统需要在CAP理论中做出权衡。

---

## Raft 共识算法

### Raft 核心概念

```
┌─────────────────────────────────────────────────────┐
│                   Raft 集群                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐      │
│   │ Leader  │ ◄──►│ Follower│ ◄──►│ Follower│      │
│   │  节点   │     │  节点   │     │  节点   │      │
│   └────┬────┘     └─────────┘     └─────────┘      │
│        │                                           │
│   - 处理客户端请求                                  │
│   - 复制日志到 Follower                            │
│   - 管理心跳和选举                                  │
└─────────────────────────────────────────────────────┘
```

### 状态机

```rust
// Raft 节点状态
enum RaftState {
    Follower,
    Candidate,
    Leader,
}

struct RaftNode {
    state: RaftState,
    current_term: u64,
    voted_for: Option<u64>,
    log: Vec<LogEntry>,
    commit_index: usize,
    last_applied: usize,
    
    // 选举相关
    election_timeout: Duration,
    last_heartbeat: Instant,
    
    // 集群配置
    node_id: u64,
    peers: Vec<u64>,
}
```

### 日志复制

```rust
struct LogEntry {
    term: u64,
    index: usize,
    command: Vec<u8>,
}

impl RaftNode {
    // Leader 复制日志到 Follower
    fn replicate_log(&mut self, peer: u64) {
        let prev_log_index = self.get_last_log_index_for(peer);
        let prev_log_term = self.get_last_log_term_for(peer);
        
        let entries: Vec<LogEntry> = self.log
            [(prev_log_index + 1)..]
            .to_vec();
        
        let rpc = AppendEntriesRequest {
            term: self.current_term,
            leader_id: self.node_id,
            prev_log_index,
            prev_log_term,
            entries,
            leader_commit: self.commit_index,
        };
        
        self.send_append_entries(peer, rpc);
    }
}
```

### 选举机制

```rust
impl RaftNode {
    fn start_election(&mut self) {
        self.state = RaftState::Candidate;
        self.current_term += 1;
        self.voted_for = Some(self.node_id);
        
        let mut votes = 1;
        
        // 向所有节点请求投票
        for peer in &self.peers {
            let request = RequestVoteRequest {
                term: self.current_term,
                candidate_id: self.node_id,
                last_log_index: self.log.len(),
                last_log_term: self.get_last_log_term(),
            };
            
            if let Some(response) = self.send_request_vote(peer, request) {
                if response.vote_granted {
                    votes += 1;
                    if votes > self.peers.len() / 2 {
                        self.become_leader();
                        return;
                    }
                }
            }
        }
        
        // 选举失败，回到 Follower
        self.state = RaftState::Follower;
    }
}
```

---

## 两阶段提交 (2PC)

### 协调者

```rust
struct TwoPhaseCommitCoordinator {
    transaction_id: u128,
    participants: Vec<Participant>,
    state: TwoPCState,
}

enum TwoPCState {
    Init,
    WaitingPrepare,
    WaitingCommit,
    Committed,
    Aborted,
}

impl TwoPhaseCommitCoordinator {
    pub fn start_transaction(&mut self) {
        self.state = TwoPCState::WaitingPrepare;
        
        // 第一阶段：发送 prepare
        for participant in &self.participants {
            participant.send(PrepareMessage {
                transaction_id: self.transaction_id,
            });
        }
    }
    
    pub fn handle_prepare_response(&mut self, response: PrepareResponse) {
        if response.vote == Vote::Abort {
            self.abort();
        } else if self.all_prepared() {
            self.state = TwoPCState::WaitingCommit;
            
            // 第二阶段：发送 commit
            for participant in &self.participants {
                participant.send(CommitMessage {
                    transaction_id: self.transaction_id,
                });
            }
        }
    }
}
```

### 参与者

```rust
struct Participant {
    transaction_manager: TransactionManager,
    state: ParticipantState,
}

enum ParticipantState {
    Init,
    Prepared,
    Committed,
    Aborted,
}

impl Participant {
    pub fn handle_prepare(&mut self, msg: PrepareMessage) {
        // 执行本地事务操作
        let result = self.transaction_manager.execute();
        
        match result {
            Ok(_) => {
                self.state = ParticipantState::Prepared;
                self.send(PrepareResponse {
                    vote: Vote::Commit,
                    ..msg
                });
            }
            Err(_) => {
                self.send(PrepareResponse {
                    vote: Vote::Abort,
                    ..msg
                });
            }
        }
    }
}
```

### 2PC 问题与解决方案

| 问题 | 原因 | 解决方案 |
|-----|------|---------|
| 阻塞 | 协调者故障 | 超时机制、备份协调者 |
| 单点故障 | 依赖协调者 | 分布式协调者 (etcd/ZooKeeper) |
| 性能 | 多次网络往返 | 批量提交、优化超时 |

---

## 分布式一致性模型

```rust
// 最终一致性
trait EventuallyConsistent {
    fn put(&self, key: &str, value: &str);
    fn get(&self, key: &str) -> Option<String>;
}

// 强一致性（线性化）
trait Linearizable {
    fn put(&self, key: &str, value: &str) -> Result<()>;
    fn get(&self, key: &str) -> Result<String>;
}

// 顺序一致性
trait SequentialConsistent {
    fn put(&self, key: &str, value: &str);
    fn get(&self, key: &str) -> Vec<String>; // 返回历史版本
}
```

---

## 分布式 ID 生成

```rust
// Snowflake 算法
struct SnowflakeGenerator {
    worker_id: u64,
    datacenter_id: u64,
    sequence: u64,
    last_timestamp: u64,
}

impl SnowflakeGenerator {
    pub fn generate(&mut self) -> u64 {
        let timestamp = current_timestamp();
        
        if timestamp == self.last_timestamp {
            self.sequence = (self.sequence + 1) & 0xFFF; // 12位
            if self.sequence == 0 {
                // 等待下一毫秒
                while current_timestamp() == timestamp {}
            }
        } else {
            self.sequence = 0;
        }
        
        self.last_timestamp = timestamp;
        
        (timestamp << 22)       // 41位时间戳
        | (self.datacenter_id << 17)  // 5位数据中心
        | (self.worker_id << 12)      // 5位工作节点
        | self.sequence               // 12位序列号
    }
}
```

---

## 分布式锁

```rust
use std::sync::{Arc, atomic::{AtomicU64, Ordering}};
use std::time::Duration;

struct DistributedLock {
    key: String,
    ttl: Duration,
    owner: u64,
}

impl DistributedLock {
    // 基于 etcd 的分布式锁
    pub async fn try_lock(&self, owner: u64, ttl: Duration) -> Result<bool, LockError> {
        let response = etcd_client.put(
            format!("/lock/{}", self.key),
            owner.to_string(),
            Some(PutOptions::new().with_ttl(ttl))
        ).await?;
        
        // 如果是第一个设置者，获得锁
        Ok(response.prev_key().is_none())
    }
    
    pub async fn unlock(&self, owner: u64) -> Result<(), LockError> {
        // 只能由锁的持有者释放
        let response = etcd_client.get(format!("/lock/{}", self.key)).await?;
        
        if response.value() == owner.to_string() {
            etcd_client.delete(format!("/lock/{}", self.key)).await?;
        }
        
        Ok(())
    }
}
```

---

## 分布式事件溯源

```rust
// 事件溯源模式
trait EventSourced {
    type Event;
    
    fn apply(&mut self, event: Self::Event);
    fn snapshot(&self) -> Self;
}

struct Aggregate {
    version: u64,
    events: Vec<Event>,
    state: AggregateState,
}

impl Aggregate {
    pub fn new() -> Self {
        Self {
            version: 0,
            events: Vec::new(),
            state: AggregateState::Init,
        }
    }
    
    pub fn apply_event(&mut self, event: Event) {
        self.state.transition(&event);
        self.events.push(event);
        self.version += 1;
    }
    
    pub fn snapshot(&self) -> EventSourcedSnapshot {
        EventSourcedSnapshot {
            version: self.version,
            state: self.state.clone(),
        }
    }
}
```

---

## 常见问题

| 问题 | 原因 | 解决 |
|-----|------|-----|
| 脑裂 | 网络分区 | 法定人数、任期机制 |
| 活锁 | 选举超时冲突 | 随机化超时 |
| 数据不一致 | 并发写入 | 冲突解决策略 |
| 性能瓶颈 | 单点写入 | 分片、复制 |

---

## 与其他技能关联

```
rust-distributed
    │
    ├─► rust-concurrency → 并发控制
    ├─► rust-performance → 性能优化
    └─► rust-async → 异步通信
```

