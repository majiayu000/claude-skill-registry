---
name: worker-orchestration
description: Manage concurrent background workers with scheduling, dependencies, health monitoring, and automatic disabling of failing workers.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: workers
  time: 4h
  source: drift-masterguide
---

# Worker Orchestration

Coordinate multiple background workers.

## When to Use This Skill

- Multiple background jobs need coordination
- Jobs have dependencies on each other
- Need to prevent conflicting concurrent execution
- Want automatic disabling of failing workers

## Core Concepts

1. **Scheduling** - Run workers on intervals
2. **Dependencies** - Worker A must complete before B starts
3. **Blocking** - Workers that can't run concurrently
4. **Auto-disable** - Stop workers after consecutive failures

## TypeScript Implementation

### Types

```typescript
// types.ts
export enum WorkerExecutionMode {
  SCHEDULED = 'scheduled',
  TRIGGERED = 'triggered',
  CONTINUOUS = 'continuous',
}

export enum JobPriority {
  LOW = 0,
  NORMAL = 1,
  HIGH = 2,
  CRITICAL = 3,
}

export interface WorkerConfig {
  name: string;
  executionMode: WorkerExecutionMode;
  intervalSeconds: number;
  timeoutSeconds: number;
  maxRetries: number;
  priority: JobPriority;
  maxConsecutiveFailures: number;
  dependsOn: string[];
  blocks: string[];
  
  // Runtime state
  isEnabled: boolean;
  isRunning: boolean;
  consecutiveFailures: number;
  lastRun?: Date;
  lastSuccess?: Date;
  lastError?: string;
}

export type WorkerFn = (config: WorkerConfig) => Promise<void>;
```

### Orchestrator

```typescript
// orchestrator.ts
import { WorkerConfig, WorkerFn, WorkerExecutionMode, JobPriority } from './types';

interface OrchestratorConfig {
  tickIntervalMs: number;
  maxConcurrentWorkers: number;
}

export class WorkerOrchestrator {
  private workers = new Map<string, WorkerConfig>();
  private workerFns = new Map<string, WorkerFn>();
  private running = new Set<string>();
  private tickInterval: NodeJS.Timeout | null = null;
  private state: 'stopped' | 'running' | 'stopping' = 'stopped';

  constructor(private config: OrchestratorConfig) {}

  registerWorker(
    name: string,
    fn: WorkerFn,
    options: Partial<WorkerConfig> = {}
  ): void {
    this.workers.set(name, {
      name,
      executionMode: options.executionMode || WorkerExecutionMode.SCHEDULED,
      intervalSeconds: options.intervalSeconds || 300,
      timeoutSeconds: options.timeoutSeconds || 60,
      maxRetries: options.maxRetries || 3,
      priority: options.priority || JobPriority.NORMAL,
      maxConsecutiveFailures: options.maxConsecutiveFailures || 5,
      dependsOn: options.dependsOn || [],
      blocks: options.blocks || [],
      isEnabled: true,
      isRunning: false,
      consecutiveFailures: 0,
    });
    this.workerFns.set(name, fn);
  }

  async start(): Promise<void> {
    if (this.state !== 'stopped') return;
    
    this.state = 'running';
    this.tickInterval = setInterval(
      () => this.tick(),
      this.config.tickIntervalMs
    );
    console.log(`[Orchestrator] Started with ${this.workers.size} workers`);
  }

  async stop(): Promise<void> {
    if (this.state === 'stopped') return;
    
    this.state = 'stopping';
    if (this.tickInterval) clearInterval(this.tickInterval);

    // Wait for running workers
    const maxWait = 30000;
    const start = Date.now();
    while (this.running.size > 0 && Date.now() - start < maxWait) {
      await this.sleep(100);
    }

    this.state = 'stopped';
    console.log('[Orchestrator] Stopped');
  }

  private async tick(): Promise<void> {
    if (this.state !== 'running') return;

    // Sort by priority (higher first)
    const sortedWorkers = Array.from(this.workers.entries())
      .sort((a, b) => b[1].priority - a[1].priority);

    for (const [name, config] of sortedWorkers) {
      if (!config.isEnabled || config.isRunning) continue;
      if (this.running.size >= this.config.maxConcurrentWorkers) break;

      if (this.shouldRun(config)) {
        this.executeWorker(name, config);
      }
    }
  }

  private shouldRun(config: WorkerConfig): boolean {
    // Check dependencies - must not be running
    for (const dep of config.dependsOn) {
      if (this.workers.get(dep)?.isRunning) return false;
    }

    // Check blockers - must not be running
    for (const blocker of config.blocks) {
      if (this.workers.get(blocker)?.isRunning) return false;
    }

    // Check schedule
    if (!config.lastRun) return true;
    const elapsed = (Date.now() - config.lastRun.getTime()) / 1000;
    return elapsed >= config.intervalSeconds;
  }

  private async executeWorker(name: string, config: WorkerConfig): Promise<void> {
    const fn = this.workerFns.get(name);
    if (!fn) return;

    config.isRunning = true;
    this.running.add(name);
    console.log(`[Orchestrator] Starting ${name}`);

    try {
      // Execute with timeout
      await Promise.race([
        fn(config),
        this.sleep(config.timeoutSeconds * 1000).then(() => {
          throw new Error('Worker timeout');
        }),
      ]);
      
      config.lastRun = new Date();
      config.lastSuccess = new Date();
      config.consecutiveFailures = 0;
      console.log(`[Orchestrator] Completed ${name}`);
      
    } catch (error) {
      config.lastRun = new Date();
      config.lastError = error instanceof Error ? error.message : String(error);
      config.consecutiveFailures++;
      console.error(`[Orchestrator] Failed ${name}:`, config.lastError);

      // Auto-disable after too many failures
      if (config.consecutiveFailures >= config.maxConsecutiveFailures) {
        config.isEnabled = false;
        console.log(`[Orchestrator] Disabled ${name} after ${config.consecutiveFailures} failures`);
      }
    } finally {
      config.isRunning = false;
      this.running.delete(name);
    }
  }

  async triggerWorker(name: string): Promise<boolean> {
    const config = this.workers.get(name);
    if (!config || config.isRunning) return false;
    
    await this.executeWorker(name, config);
    return true;
  }

  enableWorker(name: string): void {
    const config = this.workers.get(name);
    if (config) {
      config.isEnabled = true;
      config.consecutiveFailures = 0;
    }
  }

  disableWorker(name: string): void {
    const config = this.workers.get(name);
    if (config) {
      config.isEnabled = false;
    }
  }

  getStatus() {
    return {
      state: this.state,
      workers: this.workers.size,
      running: this.running.size,
      workerStates: Object.fromEntries(
        Array.from(this.workers.entries()).map(([name, config]) => [
          name,
          {
            enabled: config.isEnabled,
            running: config.isRunning,
            failures: config.consecutiveFailures,
            lastRun: config.lastRun,
            lastError: config.lastError,
          },
        ])
      ),
    };
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

## Python Implementation

```python
# orchestrator.py
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Set, Callable, Awaitable, Optional, List

class JobPriority(int, Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class WorkerConfig:
    name: str
    interval_seconds: int = 300
    timeout_seconds: int = 60
    max_consecutive_failures: int = 5
    priority: JobPriority = JobPriority.NORMAL
    depends_on: List[str] = field(default_factory=list)
    blocks: List[str] = field(default_factory=list)
    
    # Runtime state
    is_enabled: bool = True
    is_running: bool = False
    consecutive_failures: int = 0
    last_run: Optional[datetime] = None
    last_error: Optional[str] = None

WorkerFn = Callable[[WorkerConfig], Awaitable[None]]

class WorkerOrchestrator:
    def __init__(self, tick_interval: float = 5.0, max_concurrent: int = 5):
        self._tick_interval = tick_interval
        self._max_concurrent = max_concurrent
        self._workers: Dict[str, WorkerConfig] = {}
        self._worker_fns: Dict[str, WorkerFn] = {}
        self._running: Set[str] = set()
        self._state = "stopped"
        self._task: Optional[asyncio.Task] = None

    def register_worker(
        self,
        name: str,
        fn: WorkerFn,
        **options
    ):
        self._workers[name] = WorkerConfig(name=name, **options)
        self._worker_fns[name] = fn

    async def start(self):
        if self._state != "stopped":
            return
        
        self._state = "running"
        self._task = asyncio.create_task(self._tick_loop())
        print(f"[Orchestrator] Started with {len(self._workers)} workers")

    async def stop(self):
        if self._state == "stopped":
            return
        
        self._state = "stopping"
        if self._task:
            self._task.cancel()
        
        # Wait for running workers
        timeout = 30.0
        start = datetime.now()
        while self._running and (datetime.now() - start).total_seconds() < timeout:
            await asyncio.sleep(0.1)
        
        self._state = "stopped"
        print("[Orchestrator] Stopped")

    async def _tick_loop(self):
        while self._state == "running":
            await self._tick()
            await asyncio.sleep(self._tick_interval)

    async def _tick(self):
        # Sort by priority
        sorted_workers = sorted(
            self._workers.items(),
            key=lambda x: x[1].priority,
            reverse=True
        )

        for name, config in sorted_workers:
            if not config.is_enabled or config.is_running:
                continue
            if len(self._running) >= self._max_concurrent:
                break

            if self._should_run(config):
                asyncio.create_task(self._execute_worker(name, config))

    def _should_run(self, config: WorkerConfig) -> bool:
        # Check dependencies
        for dep in config.depends_on:
            if self._workers.get(dep, WorkerConfig(name="")).is_running:
                return False

        # Check blockers
        for blocker in config.blocks:
            if self._workers.get(blocker, WorkerConfig(name="")).is_running:
                return False

        # Check schedule
        if not config.last_run:
            return True
        elapsed = (datetime.now() - config.last_run).total_seconds()
        return elapsed >= config.interval_seconds

    async def _execute_worker(self, name: str, config: WorkerConfig):
        fn = self._worker_fns.get(name)
        if not fn:
            return

        config.is_running = True
        self._running.add(name)

        try:
            await asyncio.wait_for(
                fn(config),
                timeout=config.timeout_seconds
            )
            config.last_run = datetime.now()
            config.consecutive_failures = 0
        except Exception as e:
            config.last_run = datetime.now()
            config.last_error = str(e)
            config.consecutive_failures += 1

            if config.consecutive_failures >= config.max_consecutive_failures:
                config.is_enabled = False
                print(f"[Orchestrator] Disabled {name}")
        finally:
            config.is_running = False
            self._running.discard(name)

    def get_status(self) -> Dict:
        return {
            "state": self._state,
            "workers": len(self._workers),
            "running": len(self._running),
            "worker_states": {
                name: {
                    "enabled": c.is_enabled,
                    "running": c.is_running,
                    "failures": c.consecutive_failures,
                }
                for name, c in self._workers.items()
            },
        }
```

## Usage Examples

```typescript
const orchestrator = new WorkerOrchestrator({
  tickIntervalMs: 5000,
  maxConcurrentWorkers: 5,
});

// High-priority data fetcher
orchestrator.registerWorker('fetch-data', fetchDataWorker, {
  intervalSeconds: 60,
  timeoutSeconds: 30,
  priority: JobPriority.HIGH,
});

// Depends on fetch-data completing first
orchestrator.registerWorker('process-data', processDataWorker, {
  intervalSeconds: 120,
  dependsOn: ['fetch-data'],
});

// Can't run while process-data is running
orchestrator.registerWorker('cleanup', cleanupWorker, {
  intervalSeconds: 3600,
  priority: JobPriority.LOW,
  blocks: ['process-data'],
});

// Start
await orchestrator.start();

// Graceful shutdown
process.on('SIGTERM', () => orchestrator.stop());
```

## Best Practices

1. **Use dependencies** - For sequential workflows
2. **Use blocks** - For mutually exclusive jobs
3. **Set timeouts** - Prevent hung workers
4. **Auto-disable** - Stop failing workers automatically
5. **Monitor status** - Expose metrics endpoint

## Common Mistakes

- No timeout on workers (hung forever)
- Missing dependencies (race conditions)
- Too many concurrent workers (resource exhaustion)
- Not handling graceful shutdown
- No visibility into worker state

## Related Skills

- [Background Jobs](../background-jobs/)
- [Graceful Shutdown](../graceful-shutdown/)
- [Leader Election](../leader-election/)
