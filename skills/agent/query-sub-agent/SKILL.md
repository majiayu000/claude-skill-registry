---
name: query-sub-agent
description: 專責處理 IDF (Information Display Frame) 類型的需求。讀取規格目錄結構，生成/審查 Query Side 設計與實作。支援 Java、TypeScript、Go 多語言。
---

# Query Sub-agent Skill

## 觸發時機

- analyze-frame 判定 frame_type=InformationDisplayFrame 時
- 需要建立/修改 Query Side (讀模型) 的查詢、投影時
- saga-orchestrator 分派 Query 類型任務時

## 核心任務

1. 讀取規格目錄結構（frame.yaml, machine/）
2. 設計/驗證 CQRS Query Side 的查詢處理器與讀模型
3. 產出程式碼骨架或審查既有實作
4. 確保查詢效能與快取策略

---

## 規格目錄讀取

本 Skill 讀取以下規格檔案：

```
docs/specs/{feature-name}/
├── frame.yaml                 # 讀取 frame_concerns
├── requirements/              # 讀取查詢需求
│   └── req-{n}-{feature}.yaml
├── machine/                   # 讀取 Query 規格
│   ├── query.yaml             # Query Handler 規格
│   └── read-model.yaml        # Read Model 規格
└── cross-context/             # 若需跨 BC 查詢
    └── {context}.yaml
```

---

## machine/query.yaml 格式

```yaml
# docs/specs/{feature-name}/machine/query.yaml
query:
  name: "{FeatureName}Query"
  type: "single"  # | list | paginated | aggregated
  
  # Input 定義
  input:
    name: "{FeatureName}QueryInput"
    fields:
      - name: "id"
        type: "string"
        required: true
      # 分頁參數 (若 type=paginated)
      - name: "page"
        type: "number"
        default: 1
      - name: "pageSize"
        type: "number"
        default: 20
  
  # Output 定義
  output:
    name: "{FeatureName}QueryOutput"
    type: "single"  # | list | paginated
    fields:
      - name: "id"
        type: "string"
      - name: "name"
        type: "string"
    # 分頁輸出 (若 type=paginated)
    pagination:
      total: "number"
      page: "number"
      pageSize: "number"
      hasNext: "boolean"
  
  # 快取策略
  caching:
    enabled: true
    ttl: "5m"
    key_pattern: "{feature}:{id}"
    invalidation:
      - on_event: "{AggregateUpdatedEvent}"
  
  # 效能約束
  performance:
    max_response_time: "100ms"
    max_items_per_page: 100
```

---

## Claude Code Sub-agent 整合

```
saga-orchestrator → runSubagent → query-sub-agent
                                    ├── 讀取規格目錄
                                    ├── 套用 coding-standards
                                    └── 輸出 Query Side 代碼
```

### 被分派時的輸入格式

```yaml
task:
  type: "query"
  spec_dir: "docs/specs/get-workflow/"
  language: "typescript"
  output_paths:
    queries: "src/application/queries/"
    read_models: "src/infrastructure/read-models/"
```

---

## TypeScript 範例

### Query Handler

```typescript
// src/application/queries/GetWorkflowByIdQuery.ts
// Generated from: docs/specs/get-workflow/machine/query.yaml

import { WorkflowReadModel } from '@/infrastructure/read-models/WorkflowReadModel';
import { CacheService } from '@/infrastructure/cache/CacheService';

// ===== Input/Output (from query.yaml) =====

export interface GetWorkflowByIdInput {
  readonly workflowId: string;
}

export interface GetWorkflowByIdOutput {
  readonly id: string;
  readonly boardId: string;
  readonly name: string;
  readonly stages: readonly StageView[];
  readonly status: string;
  readonly createdAt: Date;
}

// ===== Query Handler =====

export class GetWorkflowByIdQuery {
  constructor(
    private readonly readModel: WorkflowReadModel,
    private readonly cache: CacheService,
  ) {}

  async execute(input: GetWorkflowByIdInput): Promise<GetWorkflowByIdOutput | null> {
    // ===== Pre-conditions =====
    if (!input.workflowId) {
      throw new ValidationError('workflowId is required');
    }

    // ===== Caching (from query.yaml#caching) =====
    const cacheKey = `workflow:${input.workflowId}`;
    const cached = await this.cache.get<GetWorkflowByIdOutput>(cacheKey);
    if (cached) {
      return cached;
    }

    // ===== Query Read Model =====
    const result = await this.readModel.findById(input.workflowId);
    
    if (result) {
      // Cache for 5 minutes (from query.yaml#caching.ttl)
      await this.cache.set(cacheKey, result, { ttl: 300 });
    }

    return result;
  }
}
```

### Paginated Query

```typescript
// src/application/queries/ListWorkflowsQuery.ts

export interface ListWorkflowsInput {
  readonly boardId: string;
  readonly page?: number;
  readonly pageSize?: number;
}

export interface ListWorkflowsOutput {
  readonly items: readonly WorkflowSummary[];
  readonly pagination: {
    readonly total: number;
    readonly page: number;
    readonly pageSize: number;
    readonly hasNext: boolean;
  };
}

export class ListWorkflowsQuery {
  constructor(
    private readonly readModel: WorkflowReadModel,
  ) {}

  async execute(input: ListWorkflowsInput): Promise<ListWorkflowsOutput> {
    const page = input.page ?? 1;
    const pageSize = Math.min(input.pageSize ?? 20, 100); // Max 100 items
    const offset = (page - 1) * pageSize;

    const [items, total] = await Promise.all([
      this.readModel.findByBoardId(input.boardId, { offset, limit: pageSize }),
      this.readModel.countByBoardId(input.boardId),
    ]);

    return {
      items,
      pagination: {
        total,
        page,
        pageSize,
        hasNext: offset + items.length < total,
      },
    };
  }
}
```

### Read Model

```typescript
// src/infrastructure/read-models/WorkflowReadModel.ts

export interface WorkflowReadModel {
  findById(id: string): Promise<WorkflowView | null>;
  findByBoardId(boardId: string, options: PaginationOptions): Promise<WorkflowSummary[]>;
  countByBoardId(boardId: string): Promise<number>;
}

// Implementation with optimized queries
export class PostgresWorkflowReadModel implements WorkflowReadModel {
  constructor(private readonly db: Database) {}

  async findById(id: string): Promise<WorkflowView | null> {
    // Optimized query with joins for stages
    const result = await this.db.query(`
      SELECT w.*, 
             json_agg(s.*) as stages
      FROM workflows w
      LEFT JOIN stages s ON s.workflow_id = w.id
      WHERE w.id = $1
      GROUP BY w.id
    `, [id]);

    return result.rows[0] ?? null;
  }

  async findByBoardId(
    boardId: string, 
    options: PaginationOptions
  ): Promise<WorkflowSummary[]> {
    // Summary query without heavy joins
    const result = await this.db.query(`
      SELECT id, name, status, created_at,
             (SELECT COUNT(*) FROM stages WHERE workflow_id = w.id) as stage_count
      FROM workflows w
      WHERE board_id = $1
      ORDER BY created_at DESC
      LIMIT $2 OFFSET $3
    `, [boardId, options.limit, options.offset]);

    return result.rows;
  }
}
```

---

## Go 範例

### Query Handler

```go
// src/application/query/get_workflow_by_id.go

package query

import (
    "context"
    "time"

    "myapp/infrastructure/cache"
    "myapp/infrastructure/readmodel"
)

type GetWorkflowByIdInput struct {
    WorkflowID string `json:"workflow_id" validate:"required,uuid"`
}

type GetWorkflowByIdOutput struct {
    ID        string      `json:"id"`
    BoardID   string      `json:"board_id"`
    Name      string      `json:"name"`
    Stages    []StageView `json:"stages"`
    Status    string      `json:"status"`
    CreatedAt time.Time   `json:"created_at"`
}

type GetWorkflowByIdQuery struct {
    readModel readmodel.WorkflowReadModel
    cache     cache.CacheService
}

func NewGetWorkflowByIdQuery(
    rm readmodel.WorkflowReadModel,
    c cache.CacheService,
) *GetWorkflowByIdQuery {
    return &GetWorkflowByIdQuery{readModel: rm, cache: c}
}

func (q *GetWorkflowByIdQuery) Execute(
    ctx context.Context,
    input GetWorkflowByIdInput,
) (*GetWorkflowByIdOutput, error) {
    // ===== Pre-conditions =====
    if err := validate.Struct(input); err != nil {
        return nil, err
    }

    // ===== Caching =====
    cacheKey := fmt.Sprintf("workflow:%s", input.WorkflowID)
    if cached, err := q.cache.Get(ctx, cacheKey); err == nil && cached != nil {
        return cached.(*GetWorkflowByIdOutput), nil
    }

    // ===== Query Read Model =====
    result, err := q.readModel.FindByID(ctx, input.WorkflowID)
    if err != nil {
        return nil, err
    }

    if result != nil {
        // Cache for 5 minutes
        _ = q.cache.Set(ctx, cacheKey, result, 5*time.Minute)
    }

    return result, nil
}
```

---

## 快取失效策略

當 Domain Event 發生時，自動失效相關快取：

```typescript
// src/infrastructure/cache/WorkflowCacheInvalidator.ts

export class WorkflowCacheInvalidator {
  constructor(private readonly cache: CacheService) {}

  @OnEvent('WorkflowCreatedEvent')
  @OnEvent('WorkflowUpdatedEvent')
  async invalidate(event: WorkflowEvent): void {
    // Invalidate single item cache
    await this.cache.delete(`workflow:${event.workflowId}`);
    
    // Invalidate list cache for the board
    await this.cache.deletePattern(`workflows:board:${event.boardId}:*`);
  }
}
```

---

## 品質檢查清單

- [ ] 查詢是否只讀取資料，不修改狀態？
- [ ] 是否使用 Read Model 而非直接查詢 Aggregate？
- [ ] 分頁查詢是否有最大筆數限制？
- [ ] 快取策略是否合理？TTL 和失效條件？
- [ ] 是否有效能約束的監控？
- [ ] N+1 查詢問題是否已解決？

---

## 常見錯誤防範

- ❌ 在 Query Handler 中修改資料
- ❌ 直接查詢 Aggregate Repository（應使用專用 Read Model）
- ❌ 忽略分頁限制，可能一次返回過多資料
- ❌ 沒有快取失效策略，導致資料不一致
- ❌ N+1 查詢問題
