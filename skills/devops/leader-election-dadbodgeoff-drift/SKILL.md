---
name: leader-election
description: Elect a single leader among multiple instances. Only one instance runs cron jobs or processes queues. Automatic failover when leader dies.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: resilience
  time: 4h
  source: drift-masterguide
---

# Leader Election

Single leader with automatic failover.

## When to Use This Skill

- Multiple instances, only one should run cron jobs
- Singleton queue consumers
- Coordinating distributed workers
- Need automatic failover when leader dies

## Core Concepts

1. **Heartbeat** - Leader sends periodic heartbeats
2. **Timeout** - If heartbeat stops, leader is dead
3. **Term** - Monotonic counter prevents split-brain
4. **Failover** - Followers compete to become new leader

## TypeScript Implementation

### Database Schema

```sql
-- migrations/leader_election.sql

CREATE TABLE leader_election (
    service_name VARCHAR(255) PRIMARY KEY,
    leader_id VARCHAR(255) NOT NULL,
    term INTEGER NOT NULL DEFAULT 1,
    last_heartbeat TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

-- Try to become leader (atomic)
CREATE OR REPLACE FUNCTION try_become_leader(
    p_service_name VARCHAR(255),
    p_candidate_id VARCHAR(255),
    p_timeout_seconds INTEGER DEFAULT 30
) RETURNS BOOLEAN AS $$
DECLARE
    v_now TIMESTAMPTZ := NOW();
    v_timeout TIMESTAMPTZ := v_now - (p_timeout_seconds || ' seconds')::INTERVAL;
    v_current RECORD;
BEGIN
    SELECT * INTO v_current
    FROM leader_election
    WHERE service_name = p_service_name
    FOR UPDATE;
    
    IF NOT FOUND THEN
        INSERT INTO leader_election (service_name, leader_id, term, last_heartbeat)
        VALUES (p_service_name, p_candidate_id, 1, v_now);
        RETURN TRUE;
    END IF;
    
    IF v_current.leader_id = p_candidate_id THEN
        UPDATE leader_election SET last_heartbeat = v_now
        WHERE service_name = p_service_name;
        RETURN TRUE;
    END IF;
    
    IF v_current.last_heartbeat < v_timeout THEN
        UPDATE leader_election
        SET leader_id = p_candidate_id, term = term + 1, last_heartbeat = v_now
        WHERE service_name = p_service_name;
        RETURN TRUE;
    END IF;
    
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- Send heartbeat
CREATE OR REPLACE FUNCTION leader_heartbeat(
    p_service_name VARCHAR(255),
    p_leader_id VARCHAR(255)
) RETURNS BOOLEAN AS $$
BEGIN
    UPDATE leader_election SET last_heartbeat = NOW()
    WHERE service_name = p_service_name AND leader_id = p_leader_id;
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;

-- Step down
CREATE OR REPLACE FUNCTION step_down(
    p_service_name VARCHAR(255),
    p_leader_id VARCHAR(255)
) RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM leader_election
    WHERE service_name = p_service_name AND leader_id = p_leader_id;
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;
```

### Leader Election Class

```typescript
// leader-election.ts
import { SupabaseClient } from '@supabase/supabase-js';

interface LeaderElectionConfig {
  serviceName: string;
  candidateId: string;
  heartbeatIntervalMs?: number;
  heartbeatTimeoutSeconds?: number;
  onBecomeLeader?: () => void | Promise<void>;
  onLoseLeadership?: () => void | Promise<void>;
}

export class LeaderElection {
  private config: Required<LeaderElectionConfig>;
  private supabase: SupabaseClient;
  private isLeader = false;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private running = false;

  constructor(supabase: SupabaseClient, config: LeaderElectionConfig) {
    this.supabase = supabase;
    this.config = {
      heartbeatIntervalMs: 10000,
      heartbeatTimeoutSeconds: 30,
      onBecomeLeader: () => {},
      onLoseLeadership: () => {},
      ...config,
    };
  }

  async start(): Promise<void> {
    if (this.running) return;
    this.running = true;

    await this.tryBecomeLeader();

    this.heartbeatInterval = setInterval(
      () => this.heartbeatLoop(),
      this.config.heartbeatIntervalMs
    );
  }

  async stop(): Promise<void> {
    this.running = false;

    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }

    if (this.isLeader) {
      await this.stepDown();
    }
  }

  isCurrentLeader(): boolean {
    return this.isLeader;
  }

  private async tryBecomeLeader(): Promise<boolean> {
    const { data, error } = await this.supabase.rpc('try_become_leader', {
      p_service_name: this.config.serviceName,
      p_candidate_id: this.config.candidateId,
      p_timeout_seconds: this.config.heartbeatTimeoutSeconds,
    });

    if (error) {
      console.error('[LeaderElection] Error:', error);
      return false;
    }

    const becameLeader = data === true;

    if (becameLeader && !this.isLeader) {
      this.isLeader = true;
      console.log(`[LeaderElection] ${this.config.candidateId} became leader`);
      await this.config.onBecomeLeader();
    }

    return becameLeader;
  }

  private async sendHeartbeat(): Promise<boolean> {
    const { data, error } = await this.supabase.rpc('leader_heartbeat', {
      p_service_name: this.config.serviceName,
      p_leader_id: this.config.candidateId,
    });

    return !error && data === true;
  }

  private async stepDown(): Promise<void> {
    if (!this.isLeader) return;

    await this.supabase.rpc('step_down', {
      p_service_name: this.config.serviceName,
      p_leader_id: this.config.candidateId,
    });

    this.isLeader = false;
    console.log(`[LeaderElection] ${this.config.candidateId} stepped down`);
    await this.config.onLoseLeadership();
  }

  private async heartbeatLoop(): Promise<void> {
    if (!this.running) return;

    if (this.isLeader) {
      const maintained = await this.sendHeartbeat();
      
      if (!maintained) {
        this.isLeader = false;
        console.log(`[LeaderElection] Lost leadership`);
        await this.config.onLoseLeadership();
      }
    } else {
      await this.tryBecomeLeader();
    }
  }
}
```

## Python Implementation

```python
# leader_election.py
import asyncio
from dataclasses import dataclass
from typing import Callable, Awaitable, Optional

@dataclass
class LeaderElectionConfig:
    service_name: str
    candidate_id: str
    heartbeat_interval: float = 10.0
    heartbeat_timeout: int = 30
    on_become_leader: Optional[Callable[[], Awaitable[None]]] = None
    on_lose_leadership: Optional[Callable[[], Awaitable[None]]] = None

class LeaderElection:
    def __init__(self, db, config: LeaderElectionConfig):
        self.db = db
        self.config = config
        self._is_leader = False
        self._running = False
        self._task: asyncio.Task | None = None

    async def start(self):
        if self._running:
            return
        self._running = True
        
        await self._try_become_leader()
        self._task = asyncio.create_task(self._heartbeat_loop())

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        if self._is_leader:
            await self._step_down()

    @property
    def is_leader(self) -> bool:
        return self._is_leader

    async def _try_become_leader(self) -> bool:
        result = await self.db.execute(
            "SELECT try_become_leader($1, $2, $3)",
            self.config.service_name,
            self.config.candidate_id,
            self.config.heartbeat_timeout,
        )
        
        became_leader = result[0][0]
        
        if became_leader and not self._is_leader:
            self._is_leader = True
            print(f"[LeaderElection] {self.config.candidate_id} became leader")
            if self.config.on_become_leader:
                await self.config.on_become_leader()
        
        return became_leader

    async def _send_heartbeat(self) -> bool:
        result = await self.db.execute(
            "SELECT leader_heartbeat($1, $2)",
            self.config.service_name,
            self.config.candidate_id,
        )
        return result[0][0]

    async def _step_down(self):
        await self.db.execute(
            "SELECT step_down($1, $2)",
            self.config.service_name,
            self.config.candidate_id,
        )
        self._is_leader = False
        if self.config.on_lose_leadership:
            await self.config.on_lose_leadership()

    async def _heartbeat_loop(self):
        while self._running:
            await asyncio.sleep(self.config.heartbeat_interval)
            
            if self._is_leader:
                if not await self._send_heartbeat():
                    self._is_leader = False
                    if self.config.on_lose_leadership:
                        await self.config.on_lose_leadership()
            else:
                await self._try_become_leader()
```

## Usage Examples

### Singleton Cron Job

```typescript
const election = new LeaderElection(supabase, {
  serviceName: 'daily-report-generator',
  candidateId: `worker-${process.env.HOSTNAME}`,
  
  onBecomeLeader: async () => {
    console.log('Starting cron jobs');
    startCronJobs();
  },
  
  onLoseLeadership: async () => {
    console.log('Stopping cron jobs');
    stopCronJobs();
  },
});

await election.start();

// Graceful shutdown
process.on('SIGTERM', async () => {
  await election.stop();
  process.exit(0);
});
```

### Queue Consumer

```typescript
const election = new LeaderElection(supabase, {
  serviceName: 'queue-consumer',
  candidateId: `consumer-${process.pid}`,
  
  onBecomeLeader: () => queueConsumer.start(),
  onLoseLeadership: () => queueConsumer.stop(),
});

await election.start();
```

### Conditional Execution

```typescript
async function runIfLeader<T>(
  election: LeaderElection,
  fn: () => Promise<T>
): Promise<T | null> {
  if (!election.isCurrentLeader()) {
    return null;
  }
  return fn();
}

// Usage
await runIfLeader(election, async () => {
  await sendDailyEmails();
});
```

## Configuration Guide

| Scenario | heartbeatIntervalMs | heartbeatTimeoutSeconds |
|----------|---------------------|-------------------------|
| Fast failover | 5000 | 15 |
| Normal | 10000 | 30 |
| Unreliable network | 30000 | 90 |

Rule: `heartbeatInterval < heartbeatTimeout / 3`

## Best Practices

1. **Unique candidate IDs** - Include hostname/PID
2. **Graceful shutdown** - Call stop() on SIGTERM
3. **Check before work** - Use isCurrentLeader()
4. **Monitor changes** - Alert on frequent leader changes
5. **Tune timeouts** - Match your network reliability

## Common Mistakes

- Same candidate ID across instances
- Not calling stop() on shutdown
- Starting work without checking leadership
- Heartbeat interval too close to timeout
- Not handling onLoseLeadership

## Related Skills

- [Distributed Lock](../distributed-lock/)
- [Background Jobs](../background-jobs/)
- [Graceful Shutdown](../graceful-shutdown/)
