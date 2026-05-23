---
name: saga-orchestrator
description: 處理跨 Frame 的複雜業務流程，協調多個 Sub-agent (command/query/reactor) 完成 Saga/Choreography 模式的分散式交易。當需求涉及多個狀態變更、事件反應與查詢的組合時使用。
---

# Saga Orchestrator Skill

## 觸發時機

- 業務流程橫跨多個 Frame 類型（CBF + RIF + IDF）
- 需要 Saga 或 Choreography 模式的分散式交易
- 需要協調多個 Sub-agent 完成複雜任務
- 使用 Claude Code 的 `runSubagent` 進行任務分解

## 核心任務

1. 分解複雜業務流程為多個 Frame
2. 設計 Saga 步驟與補償邏輯
3. 協調 Sub-agent 執行順序
4. 確保最終一致性與錯誤恢復

## 跨 Frame 流程分析

### 識別複合流程

一個完整的業務流程可能包含：

```
使用者下單 (CBF)
    ↓
庫存扣減 (CBF)
    ↓
發布 OrderCreated 事件 (RIF)
    ↓
通知倉儲系統 (RIF)
    ↓
更新訂單報表 (IDF)
```

### 流程拆解範本

```yaml
# docs/specs/{saga-name}.yaml
metadata:
  name: "{saga-name}"
  type: "saga"
  version: "1.0.0"

saga_steps:
  - step: 1
    name: "create-order"
    frame_type: "CBF"
    sub_agent: "command-sub-agent"
    action: "建立訂單"
    compensation: "取消訂單"
    output_event: "OrderCreated"
    
  - step: 2
    name: "reserve-inventory"
    frame_type: "CBF"
    sub_agent: "command-sub-agent"
    action: "扣減庫存"
    compensation: "恢復庫存"
    trigger_event: "OrderCreated"
    output_event: "InventoryReserved"
    
  - step: 3
    name: "process-payment"
    frame_type: "RIF"
    sub_agent: "reactor-sub-agent"
    action: "處理付款"
    compensation: "退款"
    trigger_event: "InventoryReserved"
    output_event: "PaymentProcessed"
    
  - step: 4
    name: "update-analytics"
    frame_type: "IDF"
    sub_agent: "query-sub-agent"
    action: "更新報表快取"
    trigger_event: "PaymentProcessed"
    # 無補償，查詢面向最終一致

error_handling:
  strategy: "backward-compensation"
  max_retries: 3
  timeout_per_step: "30s"
```

## Claude Code Sub-agent 整合

### 使用 runSubagent 分派任務

在 Claude Code 中，可透過 `runSubagent` 將任務分派給專責的子代理：

```
當處理複雜的跨 Frame 流程時，我會：

1. 先用 analyze-frame 判斷每個步驟的 Frame 類型
2. 使用 runSubagent 分派任務給對應的 sub-agent
3. 收集結果並協調下一步驟
```

### Sub-agent 分派策略

| 任務類型 | 分派給 | 說明 |
|---------|-------|------|
| 狀態變更 | `command-sub-agent` | 處理 Command、Aggregate、Domain Event |
| 資料查詢 | `query-sub-agent` | 處理 Query、Read Model、快取 |
| 事件反應 | `reactor-sub-agent` | 處理 Event Handler、整合、重試 |

### 任務分派範例

對於「使用者下單」流程，Orchestrator 會這樣分派：

**Step 1: 分派給 command-sub-agent**
```
請根據 create-order.yaml 規格，生成 CreateOrderUseCase：
- 輸入：customerId, items, shippingAddress
- 輸出：orderId, status
- 需發布 OrderCreated 事件
```

**Step 2: 分派給 reactor-sub-agent**
```
請設計 OrderCreatedHandler 處理 OrderCreated 事件：
- 觸發庫存扣減
- 設計冪等策略
- 設計重試與死信機制
```

**Step 3: 分派給 query-sub-agent**
```
請更新 OrderDashboardQuery：
- 當 PaymentProcessed 事件發生時更新快取
- 設計投影更新策略
```

## Saga 模式實作

### TypeScript 範例

```typescript
// saga/OrderSaga.ts
import { SagaStep, SagaOrchestrator } from './saga-framework';

interface OrderSagaContext {
  orderId?: string;
  customerId: string;
  items: OrderItem[];
  inventoryReservationId?: string;
  paymentId?: string;
}

export class OrderSaga extends SagaOrchestrator<OrderSagaContext> {
  
  protected defineSteps(): SagaStep<OrderSagaContext>[] {
    return [
      {
        name: 'createOrder',
        execute: async (ctx) => {
          const result = await this.commandBus.execute(
            new CreateOrderCommand(ctx.customerId, ctx.items)
          );
          ctx.orderId = result.orderId;
        },
        compensate: async (ctx) => {
          await this.commandBus.execute(
            new CancelOrderCommand(ctx.orderId!)
          );
        },
      },
      {
        name: 'reserveInventory',
        execute: async (ctx) => {
          const result = await this.commandBus.execute(
            new ReserveInventoryCommand(ctx.orderId!, ctx.items)
          );
          ctx.inventoryReservationId = result.reservationId;
        },
        compensate: async (ctx) => {
          await this.commandBus.execute(
            new ReleaseInventoryCommand(ctx.inventoryReservationId!)
          );
        },
      },
      {
        name: 'processPayment',
        execute: async (ctx) => {
          const result = await this.commandBus.execute(
            new ProcessPaymentCommand(ctx.orderId!)
          );
          ctx.paymentId = result.paymentId;
        },
        compensate: async (ctx) => {
          await this.commandBus.execute(
            new RefundPaymentCommand(ctx.paymentId!)
          );
        },
      },
    ];
  }
}
```

### Go 範例

```go
// saga/order_saga.go
package saga

import (
    "context"
    "fmt"
)

type OrderSagaContext struct {
    OrderID              string
    CustomerID           string
    Items                []OrderItem
    InventoryReservation string
    PaymentID            string
}

type OrderSaga struct {
    commandBus CommandBus
    steps      []SagaStep[*OrderSagaContext]
}

func NewOrderSaga(commandBus CommandBus) *OrderSaga {
    saga := &OrderSaga{commandBus: commandBus}
    saga.steps = []SagaStep[*OrderSagaContext]{
        {
            Name: "createOrder",
            Execute: func(ctx context.Context, sagaCtx *OrderSagaContext) error {
                result, err := saga.commandBus.Execute(ctx, &CreateOrderCommand{
                    CustomerID: sagaCtx.CustomerID,
                    Items:      sagaCtx.Items,
                })
                if err != nil {
                    return err
                }
                sagaCtx.OrderID = result.OrderID
                return nil
            },
            Compensate: func(ctx context.Context, sagaCtx *OrderSagaContext) error {
                _, err := saga.commandBus.Execute(ctx, &CancelOrderCommand{
                    OrderID: sagaCtx.OrderID,
                })
                return err
            },
        },
        {
            Name: "reserveInventory",
            Execute: func(ctx context.Context, sagaCtx *OrderSagaContext) error {
                result, err := saga.commandBus.Execute(ctx, &ReserveInventoryCommand{
                    OrderID: sagaCtx.OrderID,
                    Items:   sagaCtx.Items,
                })
                if err != nil {
                    return err
                }
                sagaCtx.InventoryReservation = result.ReservationID
                return nil
            },
            Compensate: func(ctx context.Context, sagaCtx *OrderSagaContext) error {
                _, err := saga.commandBus.Execute(ctx, &ReleaseInventoryCommand{
                    ReservationID: sagaCtx.InventoryReservation,
                })
                return err
            },
        },
    }
    return saga
}

func (s *OrderSaga) Run(ctx context.Context, sagaCtx *OrderSagaContext) error {
    completedSteps := []int{}
    
    for i, step := range s.steps {
        if err := step.Execute(ctx, sagaCtx); err != nil {
            // 執行補償
            for j := len(completedSteps) - 1; j >= 0; j-- {
                stepIdx := completedSteps[j]
                if compErr := s.steps[stepIdx].Compensate(ctx, sagaCtx); compErr != nil {
                    return fmt.Errorf("compensation failed at step %d: %w", stepIdx, compErr)
                }
            }
            return fmt.Errorf("saga failed at step %s: %w", step.Name, err)
        }
        completedSteps = append(completedSteps, i)
    }
    return nil
}
```

## Choreography 模式（事件驅動）

適用於較鬆耦合的場景：

```yaml
choreography:
  events:
    - event: "OrderCreated"
      handlers:
        - service: "inventory"
          action: "ReserveInventory"
          publishes: "InventoryReserved"
        - service: "notification"
          action: "SendOrderConfirmation"
          
    - event: "InventoryReserved"
      handlers:
        - service: "payment"
          action: "ProcessPayment"
          publishes: "PaymentProcessed"
          
    - event: "PaymentProcessed"
      handlers:
        - service: "shipping"
          action: "ScheduleShipment"
        - service: "analytics"
          action: "UpdateDashboard"
```

## 檢查清單

### 設計階段

- [ ] 是否識別出所有涉及的 Frame 類型？
- [ ] 每個步驟是否有明確的補償邏輯？
- [ ] 是否定義失敗重試策略？
- [ ] 是否考慮部分成功的處理？

### 實作階段

- [ ] 每個步驟是否冪等？
- [ ] 是否正確使用對應的 Sub-agent？
- [ ] 是否有完整的錯誤處理與日誌？
- [ ] 是否有監控與告警機制？

### 測試階段

- [ ] 是否測試完整成功路徑？
- [ ] 是否測試每個步驟的失敗與補償？
- [ ] 是否測試併發執行的情況？
- [ ] 是否測試網路分區/超時情況？

## 常見錯誤防範

- ❌ 未設計補償邏輯導致資料不一致
- ❌ 補償操作不冪等導致重複執行問題
- ❌ 未考慮併發執行的競爭條件
- ❌ 過度使用 Saga 造成系統複雜度過高（簡單場景用單一 Transaction 即可）

