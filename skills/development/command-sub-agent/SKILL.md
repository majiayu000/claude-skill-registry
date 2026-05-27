---
name: command-sub-agent
description: 專責處理 CBF (Commanded Behavior Frame) 類型的需求。讀取規格目錄結構，生成/審查 Command Side 設計與實作。支援 Java、TypeScript、Go 多語言。
---

# Command Sub-agent Skill

## 觸發時機

- analyze-frame 判定 frame_type=CommandedBehaviorFrame 時
- 需要建立/修改 Command Side (寫模型) 的用例、聚合、事件時
- saga-orchestrator 分派 Command 類型任務時

## 核心任務

1. 讀取規格目錄結構（frame.yaml, machine/, controlled-domain/）
2. 設計/驗證 CQRS Command Side 的用例、聚合與事件流
3. 產出程式碼骨架或審查既有實作
4. 確保 Frame Concerns 都有對應的實作

---

## 規格目錄讀取

本 Skill 讀取以下規格檔案：

```
docs/specs/{feature-name}/
├── frame.yaml                 # 讀取 frame_concerns, cross_context_dependencies
├── requirements/              # 讀取業務規則
│   └── req-{n}-{feature}.yaml
├── machine/                   # 讀取 Application 層規格
│   ├── controller.yaml
│   └── use-case.yaml
├── controlled-domain/         # 讀取 Domain 層規格
│   └── aggregate.yaml
└── cross-context/             # 讀取跨 BC 依賴
    └── {context}.yaml
```

---

## Claude Code Sub-agent 整合

本 Skill 可作為 `runSubagent` 的任務目標：

```
saga-orchestrator → runSubagent → command-sub-agent
                                    ├── 讀取規格目錄
                                    ├── 套用 coding-standards
                                    ├── 套用 enforce-contract  
                                    └── 輸出 Command Side 代碼
```

### 被分派時的輸入格式

```yaml
task:
  type: "command"
  spec_dir: "docs/specs/create-workflow/"
  language: "typescript"  # | java | go
  output_paths:
    application: "src/application/use-cases/"
    domain: "src/domain/"
```

---

## 工作流程

### 1. 解析規格

```yaml
# 從 frame.yaml 讀取
problem_frame: "CreateWorkflow"
frame_type: CommandedBehaviorFrame

# 識別 Frame Concerns 需要滿足
frame_concerns:
  - FC1: Structure Integrity → 對應 aggregate.yaml#invariants
  - FC2: Concurrency → 對應 use-case.yaml#transaction_boundary

# 識別跨 BC 依賴
cross_context_dependencies:
  - XC1: Authorization → 需整合 ACL
```

### 2. 生成 Use Case

從 `machine/use-case.yaml` 生成 Application 層代碼：

- 讀取 Input/Output 定義
- 讀取 contracts (pre/post-conditions)
- 讀取 transaction_boundary, idempotency 設定
- 讀取 publishes_events 列表

### 3. 生成 Aggregate

從 `controlled-domain/aggregate.yaml` 生成 Domain 層代碼：

- 讀取 identity, properties
- 讀取 entities, value_objects
- 讀取 invariants（在 constructor 和 mutating methods 中強制執行）
- 讀取 domain_events

### 4. 整合 Cross-Context

從 `cross-context/{context}.yaml` 整合 ACL：

- 在 Use Case 中注入 ACL 介面
- 在執行前進行授權檢查

---

## TypeScript 生成範例

### Use Case (從 machine/use-case.yaml 生成)

```typescript
// src/application/use-cases/CreateWorkflowUseCase.ts
// Generated from: docs/specs/create-workflow/machine/use-case.yaml

import { AuthorizationService } from '@/domain/services/AuthorizationService';
import { WorkflowRepository } from '@/domain/repositories/WorkflowRepository';
import { EventPublisher } from '@/domain/events/EventPublisher';
import { Workflow } from '@/domain/aggregates/Workflow';
import { WorkflowCreatedEvent } from '@/domain/events/WorkflowCreatedEvent';

// ===== Input/Output (from use-case.yaml#input/output) =====

export interface CreateWorkflowInput {
  readonly boardId: string;
  readonly name: string;
  readonly operatorId: string;
}

export interface CreateWorkflowOutput {
  readonly workflowId: string;
  readonly status: WorkflowStatus;
  readonly createdAt: Date;
}

// ===== Use Case =====

export class CreateWorkflowUseCase {
  constructor(
    // XC1: Authorization dependency (from cross-context/authorization.yaml)
    private readonly authorizationService: AuthorizationService,
    private readonly workflowRepository: WorkflowRepository,
    private readonly eventPublisher: EventPublisher,
  ) {}

  async execute(input: CreateWorkflowInput): Promise<CreateWorkflowOutput> {
    // ===== Pre-conditions (from use-case.yaml#contracts.pre_conditions) =====
    if (!input.boardId) {
      throw new ValidationError('boardId is required');
    }
    if (!input.name) {
      throw new ValidationError('name is required');
    }
    if (!input.operatorId) {
      throw new ValidationError('operatorId is required');
    }

    // ===== XC1: Authorization Check (from cross-context/authorization.yaml) =====
    const authResult = await this.authorizationService.canExecute(
      input.operatorId,
      'create',
      'Workflow',
      input.boardId,
    );
    if (!authResult.authorized) {
      throw new UnauthorizedError(`Not authorized: ${authResult.reason}`);
    }

    // ===== Domain Logic (from controlled-domain/aggregate.yaml) =====
    const workflow = Workflow.create({
      boardId: new BoardId(input.boardId),
      name: new WorkflowName(input.name),
      createdBy: new UserId(input.operatorId),
    });

    // ===== Persist =====
    await this.workflowRepository.save(workflow);

    // ===== Publish Domain Event (from use-case.yaml#publishes_events) =====
    await this.eventPublisher.publish(new WorkflowCreatedEvent({
      workflowId: workflow.id.value,
      boardId: workflow.boardId.value,
      name: workflow.name.value,
      createdBy: workflow.createdBy.value,
      createdAt: workflow.createdAt,
    }));

    // ===== Post-conditions (from use-case.yaml#contracts.post_conditions) =====
    // POST1: result.workflowId is not null - enforced by return type
    return {
      workflowId: workflow.id.value,
      status: workflow.status,
      createdAt: workflow.createdAt,
    };
  }
}
```

### Aggregate (從 controlled-domain/aggregate.yaml 生成)

```typescript
// src/domain/aggregates/Workflow.ts
// Generated from: docs/specs/create-workflow/controlled-domain/aggregate.yaml

import { WorkflowId } from '../value-objects/WorkflowId';
import { WorkflowName } from '../value-objects/WorkflowName';
import { BoardId } from '../value-objects/BoardId';
import { Stage } from '../entities/Stage';

export class Workflow {
  // ===== Identity (from aggregate.yaml#identity) =====
  readonly id: WorkflowId;
  
  // ===== Properties (from aggregate.yaml#properties) =====
  readonly boardId: BoardId;
  private _name: WorkflowName;
  private _stages: Stage[] = [];
  readonly createdBy: UserId;
  readonly createdAt: Date;

  private constructor(props: WorkflowProps) {
    this.id = props.id;
    this.boardId = props.boardId;
    this._name = props.name;
    this.createdBy = props.createdBy;
    this.createdAt = props.createdAt;

    // ===== INV1: Enforce invariants in constructor (from aggregate.yaml#invariants) =====
    this.validateInvariants();
  }

  static create(props: CreateWorkflowProps): Workflow {
    return new Workflow({
      id: WorkflowId.generate(),
      boardId: props.boardId,
      name: props.name,
      createdBy: props.createdBy,
      createdAt: new Date(),
    });
  }

  // ===== Mutating Methods =====

  addStage(stage: Stage): void {
    // ===== FC1: Structure Integrity - Lane Hierarchy (from frame_concerns) =====
    // Stage may be root or nested, validated in Stage entity
    this._stages.push(stage);
    
    // Re-validate invariants after mutation
    this.validateInvariants();
  }

  // ===== Invariants Validation (from aggregate.yaml#invariants.shared) =====

  private validateInvariants(): void {
    // INV1: Structure Integrity
    for (const stage of this._stages) {
      for (const lane of stage.swimLanes) {
        // SwimLane cannot exist at root; it must be under a Stage
        if (!lane.parentStage) {
          throw new InvariantViolationError(
            'SwimLane must be under a Stage'
          );
        }
      }
    }
  }

  // ===== Getters =====

  get name(): WorkflowName {
    return this._name;
  }

  get stages(): readonly Stage[] {
    return [...this._stages];
  }

  get status(): WorkflowStatus {
    return this._stages.length > 0 
      ? WorkflowStatus.Active 
      : WorkflowStatus.Empty;
  }
}
```

---

## Go 生成範例

### Use Case

```go
// src/application/usecase/create_workflow.go
// Generated from: docs/specs/create-workflow/machine/use-case.yaml

package usecase

import (
    "context"
    "time"

    "myapp/domain/aggregates"
    "myapp/domain/events"
    "myapp/domain/services"
    "myapp/domain/valueobjects"
)

// ===== Input/Output (from use-case.yaml) =====

type CreateWorkflowInput struct {
    BoardID    string `json:"board_id" validate:"required,uuid"`
    Name       string `json:"name" validate:"required,min=1,max=100"`
    OperatorID string `json:"operator_id" validate:"required,uuid"`
}

type CreateWorkflowOutput struct {
    WorkflowID string    `json:"workflow_id"`
    Status     string    `json:"status"`
    CreatedAt  time.Time `json:"created_at"`
}

// ===== Use Case =====

type CreateWorkflowUseCase struct {
    authService   services.AuthorizationService  // XC1
    workflowRepo  aggregates.WorkflowRepository
    eventPub      events.EventPublisher
}

func NewCreateWorkflowUseCase(
    authService services.AuthorizationService,
    workflowRepo aggregates.WorkflowRepository,
    eventPub events.EventPublisher,
) *CreateWorkflowUseCase {
    return &CreateWorkflowUseCase{
        authService:   authService,
        workflowRepo:  workflowRepo,
        eventPub:      eventPub,
    }
}

func (uc *CreateWorkflowUseCase) Execute(
    ctx context.Context,
    input CreateWorkflowInput,
) (*CreateWorkflowOutput, error) {
    // ===== Pre-conditions (from use-case.yaml#contracts.pre_conditions) =====
    if err := ValidateInput(input); err != nil {
        return nil, err
    }

    // ===== XC1: Authorization Check =====
    authResult, err := uc.authService.CanExecute(
        ctx,
        input.OperatorID,
        services.ActionCreate,
        services.ResourceWorkflow,
        input.BoardID,
    )
    if err != nil {
        return nil, err
    }
    if !authResult.Authorized {
        return nil, domain.NewUnauthorizedError(authResult.Reason)
    }

    // ===== Domain Logic =====
    workflow, err := aggregates.NewWorkflow(
        valueobjects.NewBoardID(input.BoardID),
        valueobjects.NewWorkflowName(input.Name),
        valueobjects.NewUserID(input.OperatorID),
    )
    if err != nil {
        return nil, err
    }

    // ===== Persist =====
    if err := uc.workflowRepo.Save(ctx, workflow); err != nil {
        return nil, err
    }

    // ===== Publish Domain Event =====
    if err := uc.eventPub.Publish(ctx, events.NewWorkflowCreatedEvent(workflow)); err != nil {
        return nil, err
    }

    return &CreateWorkflowOutput{
        WorkflowID: workflow.ID().String(),
        Status:     string(workflow.Status()),
        CreatedAt:  workflow.CreatedAt(),
    }, nil
}
```

### Aggregate

```go
// src/domain/aggregates/workflow.go
// Generated from: docs/specs/create-workflow/controlled-domain/aggregate.yaml

package aggregates

import (
    "time"

    "myapp/domain/entities"
    "myapp/domain/valueobjects"
)

type Workflow struct {
    id        valueobjects.WorkflowID
    boardID   valueobjects.BoardID
    name      valueobjects.WorkflowName
    stages    []*entities.Stage
    createdBy valueobjects.UserID
    createdAt time.Time
}

func NewWorkflow(
    boardID valueobjects.BoardID,
    name valueobjects.WorkflowName,
    createdBy valueobjects.UserID,
) (*Workflow, error) {
    w := &Workflow{
        id:        valueobjects.GenerateWorkflowID(),
        boardID:   boardID,
        name:      name,
        stages:    make([]*entities.Stage, 0),
        createdBy: createdBy,
        createdAt: time.Now(),
    }

    // ===== INV1: Validate invariants in constructor =====
    if err := w.validateInvariants(); err != nil {
        return nil, err
    }

    return w, nil
}

func (w *Workflow) AddStage(stage *entities.Stage) error {
    // ===== FC1: Structure Integrity =====
    w.stages = append(w.stages, stage)
    
    // Re-validate after mutation
    return w.validateInvariants()
}

// ===== Invariants (from aggregate.yaml#invariants.shared) =====

func (w *Workflow) validateInvariants() error {
    // INV1: Structure Integrity - Lane hierarchy
    for _, stage := range w.stages {
        for _, lane := range stage.SwimLanes() {
            if lane.ParentStage() == nil {
                return domain.NewInvariantViolationError(
                    "SwimLane must be under a Stage",
                )
            }
        }
    }
    return nil
}

// ===== Getters =====

func (w *Workflow) ID() valueobjects.WorkflowID { return w.id }
func (w *Workflow) BoardID() valueobjects.BoardID { return w.boardID }
func (w *Workflow) Name() valueobjects.WorkflowName { return w.name }
func (w *Workflow) Stages() []*entities.Stage { return w.stages }
func (w *Workflow) CreatedBy() valueobjects.UserID { return w.createdBy }
func (w *Workflow) CreatedAt() time.Time { return w.createdAt }

func (w *Workflow) Status() WorkflowStatus {
    if len(w.stages) > 0 {
        return WorkflowStatusActive
    }
    return WorkflowStatusEmpty
}
```

---

## Frame Concerns 對應表

生成代碼時，確保每個 Frame Concern 都有對應的實作：

| Frame Concern | 規格位置 | 實作位置 |
|---------------|----------|----------|
| FC1: Structure Integrity | aggregate.yaml#invariants.shared | Aggregate.validateInvariants() |
| FC2: Concurrency | use-case.yaml#transaction_boundary | Use Case transaction handling |
| XC1: Authorization | cross-context/authorization.yaml | Use Case authorization check |

---

## 品質檢查清單

- [ ] 是否讀取完整的規格目錄結構？
- [ ] 是否使用 Input/Output 模式並保持不可變？
- [ ] 每個 Frame Concern 是否都有對應實作？
- [ ] 跨 BC 依賴是否透過 ACL 整合？
- [ ] pre-conditions 是否完整覆蓋？
- [ ] Aggregate invariants 是否在 constructor 和 mutating methods 中強制執行？
- [ ] Domain Events 是否正確發布？
- [ ] Repository 介面是否位於 Domain，實作位於 Infrastructure？

---

## 常見錯誤防範

- ❌ 忽略 Frame Concerns，生成「剛好能跑」但不滿足業務規則的代碼
- ❌ 在 Domain/UseCase 中使用框架註解
- ❌ 跳過 ACL，直接呼叫外部 BC
- ❌ 在 Use Case 中混入查詢邏輯（應留給 query-sub-agent）
- ❌ 使用可變的 Input/Output 物件
- ❌ 忘記在 mutating methods 後驗證 invariants
