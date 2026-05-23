---
name: reactor-sub-agent
description: 專責處理 RIF (Required Behavior Frame) 類型的需求。讀取規格目錄結構，生成/審查 Event Handler 設計與實作。支援冪等性、重試、死信佇列。
---

# Reactor Sub-agent Skill

## 觸發時機

- analyze-frame 判定 frame_type=RequiredBehaviorFrame 時
- 需要建立/修改 Event Handler、訊息處理器時
- saga-orchestrator 分派 Reactor 類型任務時

## 核心任務

1. 讀取規格目錄結構（frame.yaml, machine/）
2. 設計/驗證 Event Handler 與反應式流程
3. 確保冪等性、重試策略、死信佇列處理
4. 產出程式碼骨架或審查既有實作

---

## 規格目錄結構

```
docs/specs/{feature-name}/
├── frame.yaml                 # 讀取 frame_concerns
├── requirements/              # 讀取反應需求
│   └── req-{n}-{feature}.yaml
├── machine/                   # 讀取 Reactor 規格
│   └── reactor.yaml           # Event Handler 規格
└── cross-context/             # 若需觸發其他 BC
    └── {context}.yaml
```

---

## machine/reactor.yaml 格式

```yaml
# docs/specs/{feature-name}/machine/reactor.yaml
reactor:
  name: "{EventName}Handler"
  
  # 監聽的事件
  subscribes_to:
    - event: "{DomainEvent}"
      source_context: "{SourceBC}"
      subscription_type: "durable"  # | ephemeral
  
  # 反應動作
  actions:
    - name: "{ActionName}"
      type: "command"  # | query | notification | integration
      target: "{TargetUseCase or Service}"
  
  # 冪等性設計
  idempotency:
    enabled: true
    key_source: "event.id"  # 用於判斷是否已處理
    storage: "database"     # | redis | in-memory
    ttl: "7d"
  
  # 重試策略
  retry:
    max_attempts: 3
    backoff:
      type: "exponential"  # | fixed | linear
      initial_delay: "1s"
      max_delay: "30s"
      multiplier: 2
    retryable_errors:
      - "NetworkError"
      - "TimeoutError"
    non_retryable_errors:
      - "ValidationError"
      - "UnauthorizedError"
  
  # 死信佇列
  dead_letter:
    enabled: true
    queue: "dlq.{feature-name}"
    alert_threshold: 10
  
  # 交易邊界
  transaction:
    type: "eventual"  # | immediate
    consistency: "at-least-once"  # | exactly-once | at-most-once
```

---

## Claude Code Sub-agent 整合

```
saga-orchestrator → runSubagent → reactor-sub-agent
                                    ├── 讀取規格目錄
                                    ├── 套用 coding-standards
                                    └── 輸出 Event Handler 代碼
```

### 被分派時的輸入格式

```yaml
task:
  type: "reactor"
  spec_dir: "docs/specs/on-workflow-created/"
  language: "typescript"
  output_paths:
    handlers: "src/application/event-handlers/"
```

---

## TypeScript 範例

### Event Handler with Full Features

```typescript
// src/application/event-handlers/WorkflowCreatedHandler.ts
// Generated from: docs/specs/on-workflow-created/machine/reactor.yaml

import { EventHandler, OnEvent } from '@/infrastructure/events/EventHandler';
import { IdempotencyService } from '@/infrastructure/idempotency/IdempotencyService';
import { RetryPolicy } from '@/infrastructure/retry/RetryPolicy';
import { DeadLetterQueue } from '@/infrastructure/dlq/DeadLetterQueue';
import { NotificationService } from '@/domain/services/NotificationService';

// ===== Event Type (from subscribes_to) =====

export interface WorkflowCreatedEvent {
  readonly id: string;           // Event ID for idempotency
  readonly workflowId: string;
  readonly boardId: string;
  readonly name: string;
  readonly createdBy: string;
  readonly createdAt: Date;
}

// ===== Handler Configuration (from reactor.yaml) =====

const RETRY_CONFIG = {
  maxAttempts: 3,
  backoff: {
    type: 'exponential' as const,
    initialDelay: 1000,
    maxDelay: 30000,
    multiplier: 2,
  },
  retryableErrors: ['NetworkError', 'TimeoutError'],
};

const IDEMPOTENCY_TTL = 7 * 24 * 60 * 60 * 1000; // 7 days

// ===== Event Handler =====

export class WorkflowCreatedHandler implements EventHandler<WorkflowCreatedEvent> {
  constructor(
    private readonly idempotencyService: IdempotencyService,
    private readonly retryPolicy: RetryPolicy,
    private readonly deadLetterQueue: DeadLetterQueue,
    private readonly notificationService: NotificationService,
    private readonly analyticsService: AnalyticsService,
  ) {}

  @OnEvent('WorkflowCreatedEvent')
  async handle(event: WorkflowCreatedEvent): Promise<void> {
    const idempotencyKey = `workflow-created:${event.id}`;

    try {
      // ===== Idempotency Check (from reactor.yaml#idempotency) =====
      const alreadyProcessed = await this.idempotencyService.check(idempotencyKey);
      if (alreadyProcessed) {
        console.log(`Event ${event.id} already processed, skipping`);
        return;
      }

      // ===== Execute with Retry (from reactor.yaml#retry) =====
      await this.retryPolicy.execute(
        async () => {
          await this.processEvent(event);
        },
        RETRY_CONFIG,
      );

      // ===== Mark as Processed =====
      await this.idempotencyService.markProcessed(idempotencyKey, IDEMPOTENCY_TTL);

    } catch (error) {
      // ===== Dead Letter Queue (from reactor.yaml#dead_letter) =====
      if (this.isNonRetryable(error)) {
        await this.deadLetterQueue.send({
          event,
          error: error.message,
          timestamp: new Date(),
          reason: 'non-retryable-error',
        });
        return;
      }

      // Re-throw for retry infrastructure
      throw error;
    }
  }

  private async processEvent(event: WorkflowCreatedEvent): Promise<void> {
    // ===== Actions (from reactor.yaml#actions) =====
    
    // Action 1: Send notification to board members
    await this.notificationService.notifyBoardMembers({
      boardId: event.boardId,
      message: `New workflow "${event.name}" created`,
      createdBy: event.createdBy,
    });

    // Action 2: Track analytics
    await this.analyticsService.track({
      event: 'workflow_created',
      properties: {
        workflowId: event.workflowId,
        boardId: event.boardId,
      },
    });
  }

  private isNonRetryable(error: Error): boolean {
    return ['ValidationError', 'UnauthorizedError'].some(
      type => error.name === type || error.constructor.name === type
    );
  }
}
```

### Idempotency Service

```typescript
// src/infrastructure/idempotency/IdempotencyService.ts

export interface IdempotencyService {
  check(key: string): Promise<boolean>;
  markProcessed(key: string, ttl: number): Promise<void>;
}

export class RedisIdempotencyService implements IdempotencyService {
  constructor(private readonly redis: Redis) {}

  async check(key: string): Promise<boolean> {
    const exists = await this.redis.exists(`idempotency:${key}`);
    return exists === 1;
  }

  async markProcessed(key: string, ttl: number): Promise<void> {
    await this.redis.set(
      `idempotency:${key}`,
      JSON.stringify({ processedAt: new Date() }),
      'PX',
      ttl,
    );
  }
}
```

### Retry Policy

```typescript
// src/infrastructure/retry/RetryPolicy.ts

export interface RetryConfig {
  maxAttempts: number;
  backoff: {
    type: 'exponential' | 'fixed' | 'linear';
    initialDelay: number;
    maxDelay: number;
    multiplier?: number;
  };
  retryableErrors?: string[];
}

export class RetryPolicy {
  async execute<T>(
    fn: () => Promise<T>,
    config: RetryConfig,
  ): Promise<T> {
    let lastError: Error;
    
    for (let attempt = 1; attempt <= config.maxAttempts; attempt++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error;
        
        // Check if retryable
        if (config.retryableErrors?.length) {
          const isRetryable = config.retryableErrors.some(
            type => error.name === type
          );
          if (!isRetryable) {
            throw error;
          }
        }

        // Last attempt, throw
        if (attempt === config.maxAttempts) {
          throw error;
        }

        // Calculate delay
        const delay = this.calculateDelay(attempt, config.backoff);
        await this.sleep(delay);
      }
    }
    
    throw lastError!;
  }

  private calculateDelay(attempt: number, backoff: RetryConfig['backoff']): number {
    let delay: number;
    
    switch (backoff.type) {
      case 'exponential':
        delay = backoff.initialDelay * Math.pow(backoff.multiplier ?? 2, attempt - 1);
        break;
      case 'linear':
        delay = backoff.initialDelay * attempt;
        break;
      case 'fixed':
      default:
        delay = backoff.initialDelay;
    }

    return Math.min(delay, backoff.maxDelay);
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

---

## Go 範例

### Event Handler

```go
// src/application/handlers/workflow_created_handler.go

package handlers

import (
    "context"
    "fmt"
    "time"

    "myapp/domain/events"
    "myapp/infrastructure/idempotency"
    "myapp/infrastructure/retry"
    "myapp/infrastructure/dlq"
)

const (
    idempotencyTTL = 7 * 24 * time.Hour
    maxRetryAttempts = 3
)

type WorkflowCreatedHandler struct {
    idempotency  idempotency.Service
    retryPolicy  *retry.Policy
    dlq          *dlq.DeadLetterQueue
    notification NotificationService
    analytics    AnalyticsService
}

func NewWorkflowCreatedHandler(
    idem idempotency.Service,
    rp *retry.Policy,
    dlq *dlq.DeadLetterQueue,
    notif NotificationService,
    analytics AnalyticsService,
) *WorkflowCreatedHandler {
    return &WorkflowCreatedHandler{
        idempotency:  idem,
        retryPolicy:  rp,
        dlq:          dlq,
        notification: notif,
        analytics:    analytics,
    }
}

func (h *WorkflowCreatedHandler) Handle(ctx context.Context, event events.WorkflowCreatedEvent) error {
    idempotencyKey := fmt.Sprintf("workflow-created:%s", event.ID)

    // ===== Idempotency Check =====
    processed, err := h.idempotency.Check(ctx, idempotencyKey)
    if err != nil {
        return err
    }
    if processed {
        return nil // Already processed
    }

    // ===== Execute with Retry =====
    err = h.retryPolicy.Execute(ctx, func() error {
        return h.processEvent(ctx, event)
    }, retry.Config{
        MaxAttempts:  maxRetryAttempts,
        InitialDelay: time.Second,
        MaxDelay:     30 * time.Second,
        BackoffType:  retry.Exponential,
    })

    if err != nil {
        // ===== Dead Letter Queue =====
        if isNonRetryable(err) {
            return h.dlq.Send(ctx, dlq.Message{
                Event:     event,
                Error:     err.Error(),
                Timestamp: time.Now(),
                Reason:    "non-retryable-error",
            })
        }
        return err
    }

    // ===== Mark as Processed =====
    return h.idempotency.MarkProcessed(ctx, idempotencyKey, idempotencyTTL)
}

func (h *WorkflowCreatedHandler) processEvent(ctx context.Context, event events.WorkflowCreatedEvent) error {
    // Action 1: Notify board members
    if err := h.notification.NotifyBoardMembers(ctx, NotifyRequest{
        BoardID:   event.BoardID,
        Message:   fmt.Sprintf("New workflow %q created", event.Name),
        CreatedBy: event.CreatedBy,
    }); err != nil {
        return err
    }

    // Action 2: Track analytics
    return h.analytics.Track(ctx, AnalyticsEvent{
        Name: "workflow_created",
        Properties: map[string]interface{}{
            "workflow_id": event.WorkflowID,
            "board_id":    event.BoardID,
        },
    })
}

func isNonRetryable(err error) bool {
    switch err.(type) {
    case *ValidationError, *UnauthorizedError:
        return true
    default:
        return false
    }
}
```

### Retry Policy

```go
// src/infrastructure/retry/policy.go

package retry

import (
    "context"
    "math"
    "time"
)

type BackoffType int

const (
    Fixed BackoffType = iota
    Linear
    Exponential
)

type Config struct {
    MaxAttempts  int
    InitialDelay time.Duration
    MaxDelay     time.Duration
    BackoffType  BackoffType
    Multiplier   float64
}

type Policy struct{}

func NewPolicy() *Policy {
    return &Policy{}
}

func (p *Policy) Execute(ctx context.Context, fn func() error, cfg Config) error {
    var lastErr error

    for attempt := 1; attempt <= cfg.MaxAttempts; attempt++ {
        if err := fn(); err == nil {
            return nil
        } else {
            lastErr = err
        }

        if attempt == cfg.MaxAttempts {
            break
        }

        delay := p.calculateDelay(attempt, cfg)
        select {
        case <-ctx.Done():
            return ctx.Err()
        case <-time.After(delay):
        }
    }

    return lastErr
}

func (p *Policy) calculateDelay(attempt int, cfg Config) time.Duration {
    multiplier := cfg.Multiplier
    if multiplier == 0 {
        multiplier = 2
    }

    var delay time.Duration
    switch cfg.BackoffType {
    case Exponential:
        delay = time.Duration(float64(cfg.InitialDelay) * math.Pow(multiplier, float64(attempt-1)))
    case Linear:
        delay = cfg.InitialDelay * time.Duration(attempt)
    default:
        delay = cfg.InitialDelay
    }

    if delay > cfg.MaxDelay {
        return cfg.MaxDelay
    }
    return delay
}
```

---

## 品質檢查清單

- [ ] 是否有冪等性機制？
- [ ] 重試策略是否區分 retryable 和 non-retryable 錯誤？
- [ ] 是否有死信佇列處理失敗的事件？
- [ ] 是否有監控和告警機制？
- [ ] 是否考慮事件順序問題？
- [ ] 是否有適當的日誌記錄？

---

## 常見錯誤防範

- ❌ 缺少冪等性檢查，導致重複處理
- ❌ 所有錯誤都重試，包括不可恢復的錯誤
- ❌ 沒有死信佇列，失敗的事件永遠丟失
- ❌ 在 Handler 中執行同步阻塞操作過久
- ❌ 沒有監控 DLQ 積壓情況
- ❌ 忽略事件版本和順序問題
