---
name: cross-context
description: 處理跨 Bounded Context 的依賴關係。當需求涉及多個限界上下文（如權限管理、付款、通知）時觸發，設計 Anti-Corruption Layer 和 Context Mapping。
---

# Cross-Context Skill

## 觸發時機

- analyze-frame 識別出 `cross_context_dependencies` 時
- 需求涉及多個 Bounded Context 的協作
- 設計 Anti-Corruption Layer (ACL) 時
- 定義 Context Mapping 策略時

## 核心任務

1. 識別跨 BC 依賴的類型與方向
2. 設計適當的整合模式 (ACL, Open Host, Shared Kernel, etc.)
3. 定義跨 BC 的契約規格
4. 確保當前 BC 不被外部 BC 污染

---

## Context Mapping 模式

### 上游/下游關係

| 模式 | 說明 | 適用場景 |
|------|------|----------|
| **Customer-Supplier** | 下游需求驅動上游開發 | 緊密合作的團隊 |
| **Conformist** | 下游完全遵循上游模型 | 無法影響上游時 |
| **Anti-Corruption Layer** | 下游建立隔離層 | 保護自身模型 |
| **Open Host Service** | 上游提供標準化 API | 多下游消費者 |
| **Published Language** | 共享交換格式 | 跨組織整合 |

### 對等關係

| 模式 | 說明 | 適用場景 |
|------|------|----------|
| **Shared Kernel** | 共享部分模型 | 高度協作 |
| **Partnership** | 雙方共同演進 | 緊密合作 |
| **Separate Ways** | 完全獨立 | 無需整合 |

---

## cross-context/{context-name}.yaml 格式

```yaml
# docs/specs/{feature-name}/cross-context/{context-name}.yaml
cross_context:
  id: XC1
  name: "Authorization"
  
  # ---------------------------------------------------------------------------
  # Context 關係
  # ---------------------------------------------------------------------------
  
  relationship:
    source_context: "AccessControl"     # 提供服務的 BC
    target_context: "WorkflowManagement" # 當前 BC
    direction: "upstream-downstream"     # | symmetric | separate
    pattern: "AntiCorruptionLayer"       # | Conformist | OpenHostService | SharedKernel
  
  # ---------------------------------------------------------------------------
  # 介面契約（需求層：只描述「需要什麼」）
  # ---------------------------------------------------------------------------
  
  required_capability:
    name: "AuthorizationCheck"
    description: |
      Check if the operator has permission to perform the action on the resource.
    
    # 這是「需求」，不是「實作」
    operations:
      - name: "canExecute"
        input:
          - name: "operatorId"
            type: "string"
            description: "The ID of the operator"
          - name: "action"
            type: "string"
            description: "The action to perform (e.g., 'create', 'update', 'delete')"
          - name: "resourceType"
            type: "string"
            description: "The type of resource (e.g., 'Workflow', 'Board')"
          - name: "resourceId"
            type: "string"
            description: "The ID of the resource"
        output:
          type: "boolean"
          description: "true if authorized, false otherwise"
        
        # Design by Contract
        pre_conditions:
          - "operatorId must not be empty"
          - "action must be a valid action type"
        post_conditions:
          - "returns true or false, never throws for authorization check"
        
        # 異常情況
        errors:
          - name: "OperatorNotFoundError"
            when: "operatorId does not exist"
  
  # ---------------------------------------------------------------------------
  # ACL 設計（實作層）
  # ---------------------------------------------------------------------------
  
  acl_design:
    adapter_interface:
      name: "AuthorizationService"
      location: "src/domain/services/"
      
    adapter_implementation:
      name: "AccessControlAuthorizationAdapter"
      location: "src/infrastructure/acl/"
      
    # 模型轉換
    translation:
      - source_model: "AccessControl.Permission"
        target_model: "WorkflowManagement.AuthorizationResult"
        mapping: |
          Permission.isGranted → AuthorizationResult.authorized
          Permission.denialReason → AuthorizationResult.reason
  
  # ---------------------------------------------------------------------------
  # 容錯策略
  # ---------------------------------------------------------------------------
  
  fault_tolerance:
    timeout: "3s"
    retry:
      max_attempts: 3
      backoff: "exponential"
    fallback:
      strategy: "deny-by-default"  # | allow-by-default | cached
      description: "If authorization service is unavailable, deny the request"
    circuit_breaker:
      enabled: true
      failure_threshold: 5
      reset_timeout: "30s"
  
  # ---------------------------------------------------------------------------
  # 可追溯性
  # ---------------------------------------------------------------------------
  
  satisfied_by:
    - machine/controller.yaml#authorization_check
    - "src/infrastructure/acl/AccessControlAuthorizationAdapter.ts"
  
  validates_concerns:
    - FC1  # 若有 Frame Concern 與權限相關
```

---

## TypeScript 範例

### Domain Service Interface (在 Domain 層)

```typescript
// src/domain/services/AuthorizationService.ts

/**
 * Authorization Service Interface
 * 
 * 這是 Domain 層的介面，不依賴任何外部實作
 * Anti-Corruption Layer 的入口點
 */
export interface AuthorizationService {
  /**
   * Check if the operator can execute the action
   * 
   * @pre operatorId must not be empty
   * @pre action must be a valid action type
   * @post returns AuthorizationResult, never throws for check
   */
  canExecute(
    operatorId: string,
    action: ActionType,
    resourceType: ResourceType,
    resourceId: string
  ): Promise<AuthorizationResult>;
}

export interface AuthorizationResult {
  readonly authorized: boolean;
  readonly reason?: string;
}

export type ActionType = 'create' | 'read' | 'update' | 'delete';
export type ResourceType = 'Workflow' | 'Board' | 'Stage' | 'SwimLane';
```

### ACL Adapter (在 Infrastructure 層)

```typescript
// src/infrastructure/acl/AccessControlAuthorizationAdapter.ts

import { AuthorizationService, AuthorizationResult, ActionType, ResourceType } 
  from '../../domain/services/AuthorizationService';
import { AccessControlClient } from '../clients/AccessControlClient';
import { CircuitBreaker } from '../resilience/CircuitBreaker';

/**
 * Anti-Corruption Layer Adapter
 * 
 * 將 AccessControl BC 的模型轉換為當前 BC 的模型
 * 包含容錯策略：timeout, retry, circuit breaker
 */
export class AccessControlAuthorizationAdapter implements AuthorizationService {
  constructor(
    private readonly client: AccessControlClient,
    private readonly circuitBreaker: CircuitBreaker,
  ) {}

  async canExecute(
    operatorId: string,
    action: ActionType,
    resourceType: ResourceType,
    resourceId: string
  ): Promise<AuthorizationResult> {
    // ===== Pre-conditions =====
    if (!operatorId) {
      throw new Error('operatorId must not be empty');
    }

    try {
      // 透過 Circuit Breaker 呼叫外部服務
      const permission = await this.circuitBreaker.execute(
        () => this.client.checkPermission({
          userId: operatorId,
          action: this.mapAction(action),
          resource: `${resourceType}:${resourceId}`,
        }),
        {
          timeout: 3000,
          fallback: () => ({ isGranted: false, denialReason: 'Service unavailable' }),
        }
      );

      // ===== Model Translation (ACL 核心) =====
      return this.translateToAuthorizationResult(permission);

    } catch (error) {
      // Fallback: deny by default
      return {
        authorized: false,
        reason: 'Authorization service unavailable',
      };
    }
  }

  /**
   * 模型轉換：將外部 BC 的 Permission 轉換為當前 BC 的 AuthorizationResult
   */
  private translateToAuthorizationResult(
    permission: ExternalPermission
  ): AuthorizationResult {
    return {
      authorized: permission.isGranted,
      reason: permission.denialReason,
    };
  }

  private mapAction(action: ActionType): string {
    // 若外部 BC 使用不同的 action 命名，在此轉換
    const mapping: Record<ActionType, string> = {
      create: 'CREATE',
      read: 'READ',
      update: 'UPDATE',
      delete: 'DELETE',
    };
    return mapping[action];
  }
}
```

---

## Go 範例

### Domain Service Interface

```go
// domain/services/authorization.go
package services

type ActionType string
type ResourceType string

const (
    ActionCreate ActionType = "create"
    ActionRead   ActionType = "read"
    ActionUpdate ActionType = "update"
    ActionDelete ActionType = "delete"
)

type AuthorizationResult struct {
    Authorized bool
    Reason     string
}

// AuthorizationService - Domain layer interface
// This is the Anti-Corruption Layer entry point
type AuthorizationService interface {
    // CanExecute checks if the operator can perform the action
    // @pre operatorId must not be empty
    // @post returns AuthorizationResult, never returns error for check
    CanExecute(
        ctx context.Context,
        operatorID string,
        action ActionType,
        resourceType ResourceType,
        resourceID string,
    ) (*AuthorizationResult, error)
}
```

### ACL Adapter

```go
// infrastructure/acl/access_control_adapter.go
package acl

import (
    "context"
    "time"
    
    "myapp/domain/services"
    "myapp/infrastructure/clients"
    "myapp/infrastructure/resilience"
)

type AccessControlAuthorizationAdapter struct {
    client         *clients.AccessControlClient
    circuitBreaker *resilience.CircuitBreaker
    timeout        time.Duration
}

func NewAccessControlAuthorizationAdapter(
    client *clients.AccessControlClient,
    cb *resilience.CircuitBreaker,
) *AccessControlAuthorizationAdapter {
    return &AccessControlAuthorizationAdapter{
        client:         client,
        circuitBreaker: cb,
        timeout:        3 * time.Second,
    }
}

func (a *AccessControlAuthorizationAdapter) CanExecute(
    ctx context.Context,
    operatorID string,
    action services.ActionType,
    resourceType services.ResourceType,
    resourceID string,
) (*services.AuthorizationResult, error) {
    // ===== Pre-conditions =====
    if operatorID == "" {
        return nil, errors.New("operatorId must not be empty")
    }

    // Context with timeout
    ctx, cancel := context.WithTimeout(ctx, a.timeout)
    defer cancel()

    // Execute through circuit breaker
    result, err := a.circuitBreaker.Execute(ctx, func() (interface{}, error) {
        return a.client.CheckPermission(ctx, &clients.PermissionRequest{
            UserID:   operatorID,
            Action:   a.mapAction(action),
            Resource: fmt.Sprintf("%s:%s", resourceType, resourceID),
        })
    })

    if err != nil {
        // Fallback: deny by default
        return &services.AuthorizationResult{
            Authorized: false,
            Reason:     "Authorization service unavailable",
        }, nil
    }

    // ===== Model Translation (ACL 核心) =====
    permission := result.(*clients.Permission)
    return a.translateToAuthorizationResult(permission), nil
}

func (a *AccessControlAuthorizationAdapter) translateToAuthorizationResult(
    permission *clients.Permission,
) *services.AuthorizationResult {
    return &services.AuthorizationResult{
        Authorized: permission.IsGranted,
        Reason:     permission.DenialReason,
    }
}

func (a *AccessControlAuthorizationAdapter) mapAction(action services.ActionType) string {
    mapping := map[services.ActionType]string{
        services.ActionCreate: "CREATE",
        services.ActionRead:   "READ",
        services.ActionUpdate: "UPDATE",
        services.ActionDelete: "DELETE",
    }
    return mapping[action]
}
```

---

## Use Case 整合範例

```typescript
// 在 Use Case 中使用 AuthorizationService

export class CreateWorkflowUseCase {
  constructor(
    private readonly authorizationService: AuthorizationService,
    private readonly workflowRepository: WorkflowRepository,
    private readonly eventPublisher: EventPublisher,
  ) {}

  async execute(input: CreateWorkflowInput): Promise<CreateWorkflowOutput> {
    // ===== Cross-Context: Authorization Check =====
    const authResult = await this.authorizationService.canExecute(
      input.operatorId,
      'create',
      'Workflow',
      input.boardId,
    );

    if (!authResult.authorized) {
      throw new UnauthorizedError(
        `Not authorized to create workflow: ${authResult.reason}`
      );
    }

    // ===== Domain Logic =====
    const workflow = Workflow.create({
      boardId: new BoardId(input.boardId),
      name: input.name,
      createdBy: new UserId(input.operatorId),
    });

    await this.workflowRepository.save(workflow);
    await this.eventPublisher.publish(new WorkflowCreatedEvent(workflow));

    return {
      workflowId: workflow.id.value,
      status: workflow.status,
      createdAt: workflow.createdAt,
    };
  }
}
```

---

## 常見的跨 BC 場景

| 場景 | Source BC | Pattern | 說明 |
|------|-----------|---------|------|
| 權限檢查 | AccessControl | ACL | 檢查操作權限 |
| 用戶資訊 | UserManagement | ACL | 取得用戶詳情 |
| 付款處理 | Payment | ACL + Saga | 處理付款流程 |
| 通知發送 | Notification | Open Host | 發送通知 |
| 審計日誌 | Audit | Published Language | 記錄操作 |

---

## 品質檢查清單

- [ ] 是否明確識別上下游關係？
- [ ] ACL 是否在 Infrastructure 層，介面在 Domain 層？
- [ ] 模型轉換是否完整，不洩漏外部 BC 概念？
- [ ] 是否有適當的容錯策略（timeout, retry, circuit breaker）？
- [ ] Fallback 策略是否符合業務需求？
- [ ] 是否有明確的 pre/post-conditions？
- [ ] 是否可追溯到 Frame Concerns？

---

## 與其他 Skills 的協作

```
analyze-frame
    │
    ├── 識別 cross_context_dependencies
    │
    └── cross-context (本 Skill)
        │
        ├── 設計 ACL 規格
        │
        ├── 連結到 arch-guard (確保層次正確)
        │
        └── 連結到 command-sub-agent / query-sub-agent
            └── 在 Use Case 中整合 ACL
```
