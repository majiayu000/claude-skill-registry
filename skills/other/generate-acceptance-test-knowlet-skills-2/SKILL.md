---
name: generate-acceptance-test
description: 從規格目錄的 acceptance.yaml 生成/維護 BDD/ezSpec 測試。使用類似 Gherkin 語法，AI 自動產生 step definition（開發人員不需要手寫），驗收測試規格即為 Executable Specification。
---

# Generate Acceptance Test Skill

## 觸發時機

- analyze-frame 產生規格目錄後
- acceptance.yaml 更新時
- 需求異動需同步更新驗收測試時
- 代碼生成前，希望先鎖定可執行的驗收測試

## 核心任務

1. 解析 acceptance.yaml 的測試規格
2. **自動生成 ezSpec step definition（開發人員不需要手寫）**
3. 維護規格與測試的一致性
4. 建立與 Frame Concerns 的可追溯連結

---

## 工具腳本 (scripts/)

### generate_tests.py - 測試生成器

從 acceptance.yaml 生成各語言的 BDD 測試骨架。支援新格式 (`acceptance_criteria`) 和舊格式 (`scenarios`)。

**使用方式：**

```bash
# 生成 Gherkin .feature 檔案
python ~/.claude/skills/generate-acceptance-test/scripts/generate_tests.py \
    docs/specs/create-workflow/ --lang gherkin

# 生成 TypeScript Cucumber.js step definitions
python ~/.claude/skills/generate-acceptance-test/scripts/generate_tests.py \
    docs/specs/create-workflow/ --lang typescript --output tests/acceptance/

# 生成 Go Ginkgo 測試
python ~/.claude/skills/generate-acceptance-test/scripts/generate_tests.py \
    docs/specs/create-workflow/ --lang go --output tests/acceptance/

# 生成 Rust cucumber-rs 測試
python ~/.claude/skills/generate-acceptance-test/scripts/generate_tests.py \
    docs/specs/create-workflow/ --lang rust --output tests/acceptance/
```

**支援語言：**

| Language | Flag | Output |
|----------|------|--------|
| Gherkin | `--lang gherkin` | `{feature}.feature` |
| TypeScript | `--lang typescript` | `{feature}.steps.ts` |
| Go | `--lang go` | `{feature}_test.go` |
| Rust | `--lang rust` | `{feature}.rs` |

**格式相容性：**

腳本自動偵測並支援兩種格式：

```yaml
# 新格式 (推薦)
acceptance_criteria:
  - id: AC1
    trace:
      requirement: [CBF-REQ-1]
      frame_concerns: [FC1]
    given: ["..."]
    when: ["..."]
    then: ["..."]

# 舊格式 (向下相容)
acceptance:
  scenarios:
    - id: AT1
      given:
        - condition: "..."
      when:
        - action: "..."
      then:
        - expectation: "..."
```

---

## 關鍵概念

### Executable Specification

- 驗收測試規格 = 可執行的規格
- 使用類似 Gherkin 的 `given/when/then` 語法
- AI 自動生成 step definition，開發人員不需要手寫
- 規格變更時，測試自動同步

### 目錄結構

```
docs/specs/{feature-name}/
├── frame.yaml
├── acceptance.yaml            # 測試規格 (輸入) - 在根目錄
├── requirements/
│   └── cbf-req-1-{feature}.yaml
├── machine/
│   ├── controller.yaml
│   ├── machine.yaml
│   └── use-case.yaml
├── controlled-domain/
│   └── aggregate.yaml
└── ...
```

---

## acceptance.yaml 格式

```yaml
# docs/specs/{feature-name}/acceptance.yaml
# 注意：放在規格根目錄，不是 acceptance/ 子目錄

acceptance_criteria:

  # ---------------------------------------------------------------------------
  # Happy Path - 成功場景
  # ---------------------------------------------------------------------------
  
  - id: AC1
    type: business          # business | technical | edge-case
    test_tier: usecase      # usecase | integration | e2e
    name: "Create a valid workflow (board existence is not synchronously validated)"
    
    # 追溯連結
    trace:
      requirement:
        - CBF-REQ-1
      frame_concerns:
        - WF-FC-AUTH        # Authorization
        - FC2               # Observability & Auditability
    
    # 連結到生成的測試
    tests_anchor:
      - tests#success
      - tests#event-published
    
    # Given-When-Then 規格
    given:
      - "A boardId <boardId> is provided (existence is NOT synchronously validated in this bounded context)"
      - "A user <userId> is authorized to create workflows for that boardId"
    
    when:
      - "The user requests to create a workflow with boardId <boardId> and name <workflowName>"
    
    then:
      - "The request succeeds"
      - "A Workflow is created and belongs to Board <boardId>"
      - "The Workflow has name <workflowName>"
      - "The Workflow is active (not deleted)"
      - "The Workflow starts in an empty structure state (no stages/lanes configured yet)"
    
    and:
      - "A WorkflowCreated domain event is published for downstream consumers"
    
    # 測試資料範例
    examples:
      - boardId: "board-001"
        userId: "user-123"
        workflowName: "First workflow"

  # ---------------------------------------------------------------------------
  # Error Cases
  # ---------------------------------------------------------------------------
  
  - id: AC2
    type: business
    test_tier: usecase
    name: "Reject workflow creation when not authorized"
    
    trace:
      requirement:
        - CBF-REQ-1
      frame_concerns:
        - WF-FC-AUTH
    
    tests_anchor:
      - tests#unauthorized
    
    given:
      - "A boardId <boardId> is provided"
      - "A user <userId> is NOT authorized to create workflows for that boardId"
    
    when:
      - "The user requests to create a workflow with boardId <boardId>"
    
    then:
      - "The request fails with AuthorizationError"
      - "No Workflow is created"
      - "No domain event is published"
    
    examples:
      - boardId: "board-001"
        userId: "unauthorized-user"
```

---

## ezSpec Java 生成（Fluent API）

AI 自動生成的 ezSpec 測試，開發人員**不需要手寫 step definition**：

```java
// tests/acceptance/CreateWorkflowAcceptanceTest.java
// Auto-generated from acceptance.yaml

/**
 * AC1: Create a valid workflow successfully
 * Validates:
 * - then: workflow is created with correct boardId
 * - then: workflow is not deleted (isDeleted = false)
 * - then: workflow has no lanes/stages initially
 * - then: WorkflowCreated event is published
 */
@EzScenario(rule = SUCCESSFUL_CREATION_RULE)
public void should_create_workflow_successfully() {
    feature.newScenario()
        .Given("a user wants to create a workflow for a board", ScenarioEnvironment env -> {
            String workflowId = UUID.randomUUID().toString();
            String boardId = UUID.randomUUID().toString();
            String userId = "test-user";

            env.put("workflowId", workflowId)
               .put("boardId", boardId)
               .put("userId", userId)
               .put("name", "Development Workflow");
        })
        .When("the workflow is created", ScenarioEnvironment env -> {...})
        .ThenSuccess(ScenarioEnvironment env -> {...})
        .And("the workflow should be persisted with correct boardId", ScenarioEnvironment env -> {...})
        .And("the workflow should not be deleted", ScenarioEnvironment env -> {...})
        .And("the workflow should have no root stages initially", ScenarioEnvironment env -> {...})
        .And("a WorkflowCreated event should be published", ScenarioEnvironment env -> {
            await().atMost(timeout: 5, TimeUnit.SECONDS).untilAsserted(() -> {
                assertThat(notifyFakeHandleAllEventsService.getHandledEventsSize()).isEqualTo(expected: 1);
                assertThat(notifyFakeHandleAllEventsService.handledEventTimes(WorkflowEvents.WorkflowCreated.class)).isEqualTo(1);
            });

            WorkflowEvents.WorkflowCreated event = (WorkflowEvents.WorkflowCreated) notifyFakeHandleAllEventsService.getEvent(0);
            var input = env.get("input", CreateWorkflowInput.class);
            assertThat(event.workflowId().value()).isEqualTo(input.workflowId);
            assertThat(event.boardId().value()).isEqualTo(input.boardId);
            assertThat(event.name()).isEqualTo(input.name);
        })
        .Execute();
}
```

### ezSpec 生成規則

1. **方法命名**：`should_{action}_{outcome}` 格式
2. **JavaDoc 註解**：包含 AC ID 和 Validates 項目
3. **Fluent API**：`.Given()` → `.When()` → `.ThenSuccess()` / `.ThenFailure()` → `.And()` → `.Execute()`
4. **Lambda 環境**：使用 `ScenarioEnvironment` 傳遞狀態
5. **事件驗證**：使用 `await().atMost()` 處理非同步事件
        boardId: "board-123"
        name: "Sprint 1"
        operatorId: "user-456"
    
    - name: "invalidWorkflowInput"
      type: "CreateWorkflowInput"
      value:
        boardId: ""
        name: ""
        operatorId: "user-456"
```

---

## Error Case ezSpec 範例

```java
/**
 * AC2: Reject workflow creation when not authorized
 * Validates:
 * - frame_concerns: WF-FC-AUTH
 */
@EzScenario(rule = AUTHORIZATION_RULE)
public void should_reject_when_not_authorized() {
    feature.newScenario()
        .Given("a user is not authorized to create workflows", ScenarioEnvironment env -> {
            String boardId = UUID.randomUUID().toString();
            String userId = "unauthorized-user";
            
            // Mock authorization service to deny
            when(authorizationService.hasCapability(userId, "create_workflow", boardId))
                .thenReturn(false);
            
            env.put("boardId", boardId)
               .put("userId", userId);
        })
        .When("the user attempts to create a workflow", ScenarioEnvironment env -> {
            var input = CreateWorkflowInput.builder()
                .boardId(env.get("boardId", String.class))
                .name("Test Workflow")
                .operatorId(env.get("userId", String.class))
                .build();
            env.put("input", input);
            
            try {
                useCase.execute(input);
                env.put("error", null);
            } catch (Exception e) {
                env.put("error", e);
            }
        })
        .ThenFailure(AuthorizationException.class, ScenarioEnvironment env -> {
            var error = env.get("error", Exception.class);
            assertThat(error).isInstanceOf(AuthorizationException.class);
        })
        .And("no workflow should be created", ScenarioEnvironment env -> {
            var input = env.get("input", CreateWorkflowInput.class);
            var workflow = workflowRepository.findById(WorkflowId.of(input.workflowId));
            assertThat(workflow).isEmpty();
        })
        .And("no domain event should be published", ScenarioEnvironment env -> {
            assertThat(notifyFakeHandleAllEventsService.getHandledEventsSize()).isEqualTo(0);
        })
        .Execute();
}
```

---

## 生成的 Gherkin .feature 檔案

```gherkin
# docs/specs/create-workflow/generated/create-workflow.feature
# Auto-generated from acceptance.yaml - DO NOT EDIT DIRECTLY
# Last generated: {ISO-8601}
# Validates: WF-FC-AUTH, FC2

@feature-create-workflow
Feature: Create Workflow
  As a board member
  I want to create a workflow for my board
  So that I can organize my work into stages and lanes

  # ===== Happy Path =====
  
  @smoke @api @AC1
  Scenario Outline: Create a valid workflow successfully
    # Trace: CBF-REQ-1
    # Frame Concerns: WF-FC-AUTH, FC2
    Given A boardId <boardId> is provided (existence is NOT synchronously validated in this bounded context)
    And A user <userId> is authorized to create workflows for that boardId
    When The user requests to create a workflow with boardId <boardId> and name <workflowName>
    Then The request succeeds
    And A Workflow is created and belongs to Board <boardId>
    And The Workflow has name <workflowName>
    And The Workflow is active (not deleted)
    And The Workflow starts in an empty structure state (no stages/lanes configured yet)
    And A WorkflowCreated domain event is published for downstream consumers

    Examples:
      | boardId   | userId   | workflowName   |
      | board-001 | user-123 | First workflow |

  # ===== Error Cases =====
  
  @security @AC2
  Scenario Outline: Reject workflow creation when not authorized
    # Trace: CBF-REQ-1
    # Frame Concerns: WF-FC-AUTH
    Given A boardId <boardId> is provided
    And A user <userId> is NOT authorized to create workflows for that boardId
    When The user requests to create a workflow with boardId <boardId>
    Then The request fails with AuthorizationError
    And No Workflow is created
    And No domain event is published

    Examples:
      | boardId   | userId            |
      | board-001 | unauthorized-user |
```

---

## TypeScript 測試骨架生成

```typescript
// tests/acceptance/CreateWorkflow.spec.ts
// Auto-generated from acceptance.yaml

import { describe, it, beforeEach, expect } from 'vitest';
import { CreateWorkflowUseCase } from '@/application/use-cases/CreateWorkflowUseCase';
import { InMemoryWorkflowRepository } from '@/infrastructure/repositories/InMemoryWorkflowRepository';
import { MockEventPublisher } from '@/tests/mocks/MockEventPublisher';
import { AuthFixture, BoardFixture } from '@/tests/fixtures';

describe('Feature: Create Workflow', () => {
  let useCase: CreateWorkflowUseCase;
  let workflowRepository: InMemoryWorkflowRepository;
  let eventPublisher: MockEventPublisher;

  beforeEach(() => {
    workflowRepository = new InMemoryWorkflowRepository();
    eventPublisher = new MockEventPublisher();
    useCase = new CreateWorkflowUseCase(
      /* dependencies injected */
    );
  });

  // ===== AT1: Successfully create workflow =====
  // Validates: POST1, INV1
  // Tags: @smoke @api
  describe('Scenario: Successfully create workflow', () => {
    it('should create workflow with generated ID', async () => {
      // Given
      const user = AuthFixture.authenticatedUser();
      const board = await BoardFixture.exists('board-123');
      await BoardFixture.memberOf(user.id, board.id);

      // When
      const input = {
        boardId: 'board-123',
        name: 'Sprint 1',
        operatorId: user.id,
      };
      const result = await useCase.execute(input);

      // Then
      expect(result.workflowId).toBeDefined();
      expect(result.workflowId).not.toBeNull();
    });

    it('should publish WorkflowCreated event', async () => {
      // Given
      const user = AuthFixture.authenticatedUser();
      await BoardFixture.memberOf(user.id, 'board-123');

      // When
      await useCase.execute({
        boardId: 'board-123',
        name: 'Sprint 1',
        operatorId: user.id,
      });

      // Then
      expect(eventPublisher.published).toContainEqual(
        expect.objectContaining({ type: 'WorkflowCreatedEvent' })
      );
    });
  });

  // ===== AT2: Fail when user is not authorized =====
  // Validates: XC1 (Authorization)
  // Tags: @security
  describe('Scenario: Fail when user is not authorized', () => {
    it('should throw UnauthorizedError', async () => {
      // Given
      const user = AuthFixture.authenticatedUser();
      // User is NOT a board member

      // When & Then
      await expect(
        useCase.execute({
          boardId: 'board-123',
          name: 'Sprint 1',
          operatorId: user.id,
        })
      ).rejects.toThrow(UnauthorizedError);
    });

    it('should not create any workflow', async () => {
      // Given
      const user = AuthFixture.authenticatedUser();
      const initialCount = await workflowRepository.count();

      // When
      try {
        await useCase.execute({
          boardId: 'board-123',
          name: 'Sprint 1',
          operatorId: user.id,
        });
      } catch (e) {
        // Expected
      }

      // Then
      expect(await workflowRepository.count()).toBe(initialCount);
    });
  });

  // ===== AT3: Handle concurrent workflow creation =====
  // Validates: FC2 (Concurrency)
  // Tags: @concurrency
  describe('Scenario: Handle concurrent workflow creation', () => {
    it('should only create one workflow', async () => {
      // Given
      const user1 = AuthFixture.authenticatedUser('user-1');
      const user2 = AuthFixture.authenticatedUser('user-2');
      await BoardFixture.memberOf(user1.id, 'board-123');
      await BoardFixture.memberOf(user2.id, 'board-123');

      // When: Concurrent execution
      const [result1, result2] = await Promise.allSettled([
        useCase.execute({ boardId: 'board-123', name: 'Sprint 1', operatorId: user1.id }),
        useCase.execute({ boardId: 'board-123', name: 'Sprint 1', operatorId: user2.id }),
      ]);

      // Then
      const fulfilled = [result1, result2].filter(r => r.status === 'fulfilled');
      const rejected = [result1, result2].filter(r => r.status === 'rejected');
      
      expect(fulfilled.length).toBe(1);
      expect(rejected.length).toBe(1);
      expect(rejected[0].reason).toBeInstanceOf(ConflictError);
    });
  });
});
```

---

## Go 測試骨架生成

```go
// tests/acceptance/create_workflow_test.go
// Auto-generated from acceptance.yaml

package acceptance

import (
    "context"
    "testing"
    "sync"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    
    "myapp/application/usecase"
    "myapp/tests/fixtures"
    "myapp/tests/mocks"
)

func TestCreateWorkflow(t *testing.T) {
    // ===== AT1: Successfully create workflow =====
    t.Run("Scenario: Successfully create workflow", func(t *testing.T) {
        t.Run("should create workflow with generated ID", func(t *testing.T) {
            // Given
            user := fixtures.AuthenticatedUser(t)
            board := fixtures.BoardExists(t, "board-123")
            fixtures.MemberOf(t, user.ID, board.ID)
            
            repo := mocks.NewInMemoryWorkflowRepository()
            eventPub := mocks.NewMockEventPublisher()
            uc := usecase.NewCreateWorkflowUseCase(repo, eventPub)

            // When
            input := usecase.CreateWorkflowInput{
                BoardID:    "board-123",
                Name:       "Sprint 1",
                OperatorID: user.ID,
            }
            result, err := uc.Execute(context.Background(), input)

            // Then
            require.NoError(t, err)
            assert.NotEmpty(t, result.WorkflowID)
        })

        t.Run("should publish WorkflowCreated event", func(t *testing.T) {
            // Given
            user := fixtures.AuthenticatedUser(t)
            fixtures.MemberOf(t, user.ID, "board-123")
            
            repo := mocks.NewInMemoryWorkflowRepository()
            eventPub := mocks.NewMockEventPublisher()
            uc := usecase.NewCreateWorkflowUseCase(repo, eventPub)

            // When
            _, err := uc.Execute(context.Background(), usecase.CreateWorkflowInput{
                BoardID:    "board-123",
                Name:       "Sprint 1",
                OperatorID: user.ID,
            })

            // Then
            require.NoError(t, err)
            assert.Contains(t, eventPub.Published(), "WorkflowCreatedEvent")
        })
    })

    // ===== AT2: Fail when user is not authorized =====
    t.Run("Scenario: Fail when user is not authorized", func(t *testing.T) {
        t.Run("should return UnauthorizedError", func(t *testing.T) {
            // Given
            user := fixtures.AuthenticatedUser(t)
            // User is NOT a board member

            repo := mocks.NewInMemoryWorkflowRepository()
            eventPub := mocks.NewMockEventPublisher()
            authSvc := mocks.NewDenyAllAuthorizationService()
            uc := usecase.NewCreateWorkflowUseCase(repo, eventPub, authSvc)

            // When
            _, err := uc.Execute(context.Background(), usecase.CreateWorkflowInput{
                BoardID:    "board-123",
                Name:       "Sprint 1",
                OperatorID: user.ID,
            })

            // Then
            assert.ErrorIs(t, err, domain.ErrUnauthorized)
        })
    })

    // ===== AT3: Handle concurrent workflow creation =====
    t.Run("Scenario: Handle concurrent workflow creation", func(t *testing.T) {
        t.Run("should only create one workflow", func(t *testing.T) {
            // Given
            user1 := fixtures.AuthenticatedUser(t)
            user2 := fixtures.AuthenticatedUser(t)
            fixtures.MemberOf(t, user1.ID, "board-123")
            fixtures.MemberOf(t, user2.ID, "board-123")

            repo := mocks.NewInMemoryWorkflowRepository()
            eventPub := mocks.NewMockEventPublisher()
            uc := usecase.NewCreateWorkflowUseCase(repo, eventPub)

            // When: Concurrent execution
            var wg sync.WaitGroup
            results := make(chan error, 2)

            for _, userID := range []string{user1.ID, user2.ID} {
                wg.Add(1)
                go func(uid string) {
                    defer wg.Done()
                    _, err := uc.Execute(context.Background(), usecase.CreateWorkflowInput{
                        BoardID:    "board-123",
                        Name:       "Sprint 1",
                        OperatorID: uid,
                    })
                    results <- err
                }(userID)
            }
            wg.Wait()
            close(results)

            // Then
            var successCount, conflictCount int
            for err := range results {
                if err == nil {
                    successCount++
                } else if errors.Is(err, domain.ErrConflict) {
                    conflictCount++
                }
            }
            
            assert.Equal(t, 1, successCount)
            assert.Equal(t, 1, conflictCount)
        })
    })
}
```

---

## 同步檢查機制

當規格更新時，Skill 會：

1. **偵測變更**：比對 acceptance.yaml 的變更
2. **標記過時測試**：在 .feature 檔案中標記需更新的場景
3. **生成差異報告**：列出需要同步的項目

```yaml
# 同步狀態報告
sync_report:
  generated_at: "2024-12-25T10:00:00Z"
  
  in_sync:
    - AT1
    - AT2
  
  out_of_sync:
    - id: AT3
      reason: "acceptance.yaml updated, feature file not regenerated"
      diff: "then clause changed"
  
  missing:
    - id: AT4
      reason: "New scenario added to acceptance.yaml"
```

---

## 品質檢查清單

- [ ] 每個 scenario 是否都有可執行的 Given/When/Then？
- [ ] 是否涵蓋 happy-path、error-case、edge-case？
- [ ] 是否與 Frame Concerns 建立 validates_concerns 連結？
- [ ] 是否與 contracts 建立 validates_contracts 連結？
- [ ] 測試名稱、檔名是否對應 feature-name？
- [ ] 併發場景是否有測試 (若 FC 包含 Concurrency)？

---

## BDD 框架支援

本 Skill 支援以下語言與 BDD 框架：

| 語言 | 框架 | 特點 |
|------|------|------|
| Java | ezSpec | Fluent API, 無需 step definition |
| Go | Ginkgo + Gomega | BDD 風格, 表格驅動測試 |
| TypeScript | Cucumber.js / Jest-Cucumber | Gherkin 原生支援 |
| Rust | cucumber-rs | Async 支援, 宏輔助 |

---

## Go: Ginkgo + Gomega 生成

```go
// tests/acceptance/create_workflow_test.go
// Auto-generated from acceptance.yaml
// Framework: Ginkgo v2 + Gomega

package acceptance_test

import (
    "context"
    "testing"

    . "github.com/onsi/ginkgo/v2"
    . "github.com/onsi/gomega"

    "myapp/application/usecase"
    "myapp/domain"
    "myapp/tests/fixtures"
    "myapp/tests/mocks"
)

func TestCreateWorkflow(t *testing.T) {
    RegisterFailHandler(Fail)
    RunSpecs(t, "Create Workflow Suite")
}

var _ = Describe("Feature: Create Workflow", func() {
    var (
        repo     *mocks.InMemoryWorkflowRepository
        eventPub *mocks.MockEventPublisher
        authSvc  *mocks.MockAuthorizationService
        uc       *usecase.CreateWorkflowUseCase
    )

    BeforeEach(func() {
        repo = mocks.NewInMemoryWorkflowRepository()
        eventPub = mocks.NewMockEventPublisher()
        authSvc = mocks.NewMockAuthorizationService()
        uc = usecase.NewCreateWorkflowUseCase(repo, eventPub, authSvc)
    })

    // ===== AC1: Create a valid workflow successfully =====
    // Trace: CBF-REQ-1
    // Frame Concerns: WF-FC-AUTH, FC2
    Describe("Scenario: Create a valid workflow successfully", Label("smoke", "api", "AC1"), func() {
        var (
            ctx    context.Context
            input  usecase.CreateWorkflowInput
            result *usecase.CreateWorkflowOutput
            err    error
        )

        BeforeEach(func() {
            ctx = context.Background()
        })

        When("a user is authorized and requests to create a workflow", func() {
            BeforeEach(func() {
                // Given
                user := fixtures.AuthenticatedUser()
                authSvc.AllowCapability(user.ID, "create_workflow", "board-001")

                // When
                input = usecase.CreateWorkflowInput{
                    BoardID:    "board-001",
                    Name:       "First workflow",
                    OperatorID: user.ID,
                }
                result, err = uc.Execute(ctx, input)
            })

            It("should succeed", func() {
                Expect(err).NotTo(HaveOccurred())
            })

            It("should create a workflow with the correct boardId", func() {
                Expect(result.WorkflowID).NotTo(BeEmpty())
                
                workflow, err := repo.FindByID(ctx, result.WorkflowID)
                Expect(err).NotTo(HaveOccurred())
                Expect(workflow.BoardID).To(Equal("board-001"))
            })

            It("should have the correct name", func() {
                workflow, _ := repo.FindByID(ctx, result.WorkflowID)
                Expect(workflow.Name).To(Equal("First workflow"))
            })

            It("should be active (not deleted)", func() {
                workflow, _ := repo.FindByID(ctx, result.WorkflowID)
                Expect(workflow.IsDeleted).To(BeFalse())
            })

            It("should start with empty structure", func() {
                workflow, _ := repo.FindByID(ctx, result.WorkflowID)
                Expect(workflow.Stages).To(BeEmpty())
                Expect(workflow.Lanes).To(BeEmpty())
            })

            It("should publish WorkflowCreated event", func() {
                Eventually(func() int {
                    return eventPub.EventCount()
                }).Should(Equal(1))

                event := eventPub.LastEvent()
                Expect(event).To(BeAssignableToTypeOf(&domain.WorkflowCreatedEvent{}))
            })
        })
    })

    // ===== AC2: Reject when not authorized =====
    // Frame Concerns: WF-FC-AUTH
    Describe("Scenario: Reject workflow creation when not authorized", Label("security", "AC2"), func() {
        When("a user is NOT authorized", func() {
            var err error

            BeforeEach(func() {
                // Given: user is not authorized
                authSvc.DenyAll()

                // When
                input := usecase.CreateWorkflowInput{
                    BoardID:    "board-001",
                    Name:       "Test Workflow",
                    OperatorID: "unauthorized-user",
                }
                _, err = uc.Execute(context.Background(), input)
            })

            It("should return AuthorizationError", func() {
                Expect(err).To(MatchError(domain.ErrUnauthorized))
            })

            It("should not create any workflow", func() {
                count, _ := repo.Count(context.Background())
                Expect(count).To(Equal(0))
            })

            It("should not publish any event", func() {
                Expect(eventPub.EventCount()).To(Equal(0))
            })
        })
    })

    // ===== Table-Driven Tests =====
    DescribeTable("Scenario: Validation errors",
        func(boardID, name, expectedError string) {
            authSvc.AllowAll()

            input := usecase.CreateWorkflowInput{
                BoardID:    boardID,
                Name:       name,
                OperatorID: "user-123",
            }
            _, err := uc.Execute(context.Background(), input)

            Expect(err).To(HaveOccurred())
            Expect(err.Error()).To(ContainSubstring(expectedError))
        },
        Entry("empty boardId", "", "Workflow", "boardId is required"),
        Entry("empty name", "board-001", "", "name is required"),
        Entry("name too long", "board-001", string(make([]byte, 256)), "name exceeds max length"),
    )
})
```

---

## TypeScript: Cucumber.js 生成

```typescript
// tests/acceptance/features/create-workflow.feature
// Auto-generated from acceptance.yaml

Feature: Create Workflow
  As a board member
  I want to create a workflow for my board
  So that I can organize my work

  @smoke @api @AC1
  Scenario: Create a valid workflow successfully
    Given a boardId "board-001" is provided
    And a user "user-123" is authorized to create workflows for that boardId
    When the user requests to create a workflow with name "First workflow"
    Then the request should succeed
    And a Workflow should be created with name "First workflow"
    And the Workflow should belong to Board "board-001"
    And the Workflow should be active
    And a WorkflowCreated event should be published

  @security @AC2  
  Scenario: Reject workflow creation when not authorized
    Given a boardId "board-001" is provided
    And a user "unauthorized-user" is NOT authorized to create workflows
    When the user attempts to create a workflow
    Then the request should fail with "AuthorizationError"
    And no Workflow should be created
```

```typescript
// tests/acceptance/steps/create-workflow.steps.ts
// Auto-generated step definitions for Cucumber.js

import { Given, When, Then, Before, After } from '@cucumber/cucumber';
import { expect } from 'chai';
import { CreateWorkflowUseCase } from '@/application/use-cases/CreateWorkflowUseCase';
import { InMemoryWorkflowRepository } from '@/infrastructure/repositories/InMemoryWorkflowRepository';
import { MockEventPublisher } from '@/tests/mocks/MockEventPublisher';
import { MockAuthorizationService } from '@/tests/mocks/MockAuthorizationService';

interface World {
  repository: InMemoryWorkflowRepository;
  eventPublisher: MockEventPublisher;
  authService: MockAuthorizationService;
  useCase: CreateWorkflowUseCase;
  input: { boardId: string; name: string; operatorId: string };
  result: { workflowId: string } | null;
  error: Error | null;
}

Before(function (this: World) {
  this.repository = new InMemoryWorkflowRepository();
  this.eventPublisher = new MockEventPublisher();
  this.authService = new MockAuthorizationService();
  this.useCase = new CreateWorkflowUseCase(
    this.repository,
    this.eventPublisher,
    this.authService
  );
  this.result = null;
  this.error = null;
});

// ===== Given Steps =====

Given('a boardId {string} is provided', function (this: World, boardId: string) {
  this.input = { ...this.input, boardId };
});

Given(
  'a user {string} is authorized to create workflows for that boardId',
  function (this: World, userId: string) {
    this.input = { ...this.input, operatorId: userId };
    this.authService.allowCapability(userId, 'create_workflow', this.input.boardId);
  }
);

Given(
  'a user {string} is NOT authorized to create workflows',
  function (this: World, userId: string) {
    this.input = { ...this.input, operatorId: userId };
    this.authService.denyAll();
  }
);

// ===== When Steps =====

When(
  'the user requests to create a workflow with name {string}',
  async function (this: World, name: string) {
    this.input = { ...this.input, name };
    try {
      this.result = await this.useCase.execute(this.input);
    } catch (e) {
      this.error = e as Error;
    }
  }
);

When('the user attempts to create a workflow', async function (this: World) {
  this.input = { ...this.input, name: 'Test Workflow' };
  try {
    this.result = await this.useCase.execute(this.input);
  } catch (e) {
    this.error = e as Error;
  }
});

// ===== Then Steps =====

Then('the request should succeed', function (this: World) {
  expect(this.error).to.be.null;
  expect(this.result).to.not.be.null;
});

Then('the request should fail with {string}', function (this: World, errorType: string) {
  expect(this.error).to.not.be.null;
  expect(this.error!.name).to.equal(errorType);
});

Then(
  'a Workflow should be created with name {string}',
  async function (this: World, name: string) {
    const workflow = await this.repository.findById(this.result!.workflowId);
    expect(workflow).to.not.be.null;
    expect(workflow!.name).to.equal(name);
  }
);

Then(
  'the Workflow should belong to Board {string}',
  async function (this: World, boardId: string) {
    const workflow = await this.repository.findById(this.result!.workflowId);
    expect(workflow!.boardId).to.equal(boardId);
  }
);

Then('the Workflow should be active', async function (this: World) {
  const workflow = await this.repository.findById(this.result!.workflowId);
  expect(workflow!.isDeleted).to.be.false;
});

Then('a WorkflowCreated event should be published', function (this: World) {
  expect(this.eventPublisher.events).to.have.lengthOf(1);
  expect(this.eventPublisher.events[0].type).to.equal('WorkflowCreated');
});

Then('no Workflow should be created', async function (this: World) {
  const count = await this.repository.count();
  expect(count).to.equal(0);
});
```

### TypeScript: Jest-Cucumber 替代方案

```typescript
// tests/acceptance/create-workflow.spec.ts
// Using jest-cucumber for tighter Jest integration

import { defineFeature, loadFeature } from 'jest-cucumber';
import { CreateWorkflowUseCase } from '@/application/use-cases/CreateWorkflowUseCase';
import { InMemoryWorkflowRepository } from '@/infrastructure/repositories/InMemoryWorkflowRepository';
import { MockEventPublisher } from '@/tests/mocks/MockEventPublisher';
import { MockAuthorizationService } from '@/tests/mocks/MockAuthorizationService';

const feature = loadFeature('./features/create-workflow.feature');

defineFeature(feature, (test) => {
  let repository: InMemoryWorkflowRepository;
  let eventPublisher: MockEventPublisher;
  let authService: MockAuthorizationService;
  let useCase: CreateWorkflowUseCase;
  let input: { boardId: string; name: string; operatorId: string };
  let result: { workflowId: string } | null;
  let error: Error | null;

  beforeEach(() => {
    repository = new InMemoryWorkflowRepository();
    eventPublisher = new MockEventPublisher();
    authService = new MockAuthorizationService();
    useCase = new CreateWorkflowUseCase(repository, eventPublisher, authService);
    result = null;
    error = null;
  });

  test('Create a valid workflow successfully', ({ given, and, when, then }) => {
    given(/^a boardId "(.*)" is provided$/, (boardId: string) => {
      input = { ...input, boardId };
    });

    and(/^a user "(.*)" is authorized to create workflows for that boardId$/, (userId: string) => {
      input = { ...input, operatorId: userId };
      authService.allowCapability(userId, 'create_workflow', input.boardId);
    });

    when(/^the user requests to create a workflow with name "(.*)"$/, async (name: string) => {
      input = { ...input, name };
      try {
        result = await useCase.execute(input);
      } catch (e) {
        error = e as Error;
      }
    });

    then('the request should succeed', () => {
      expect(error).toBeNull();
      expect(result).not.toBeNull();
    });

    and(/^a Workflow should be created with name "(.*)"$/, async (name: string) => {
      const workflow = await repository.findById(result!.workflowId);
      expect(workflow?.name).toBe(name);
    });

    and('a WorkflowCreated event should be published', () => {
      expect(eventPublisher.events).toHaveLength(1);
      expect(eventPublisher.events[0].type).toBe('WorkflowCreated');
    });
  });
});
```

---

## Rust: cucumber-rs 生成

```rust
// tests/acceptance/create_workflow.rs
// Auto-generated from acceptance.yaml
// Framework: cucumber-rs

use cucumber::{given, when, then, World};
use async_trait::async_trait;
use std::sync::Arc;
use tokio::sync::Mutex;

use myapp::application::use_cases::{CreateWorkflowUseCase, CreateWorkflowInput, CreateWorkflowOutput};
use myapp::domain::{WorkflowRepository, EventPublisher, AuthorizationService};
use myapp::domain::errors::DomainError;
use myapp::infrastructure::repositories::InMemoryWorkflowRepository;
use myapp::tests::mocks::{MockEventPublisher, MockAuthorizationService};

// ===== World Definition =====

#[derive(Debug, World)]
#[world(init = Self::new)]
pub struct CreateWorkflowWorld {
    repository: Arc<Mutex<InMemoryWorkflowRepository>>,
    event_publisher: Arc<Mutex<MockEventPublisher>>,
    auth_service: Arc<Mutex<MockAuthorizationService>>,
    input: Option<CreateWorkflowInput>,
    result: Option<Result<CreateWorkflowOutput, DomainError>>,
}

impl CreateWorkflowWorld {
    fn new() -> Self {
        Self {
            repository: Arc::new(Mutex::new(InMemoryWorkflowRepository::new())),
            event_publisher: Arc::new(Mutex::new(MockEventPublisher::new())),
            auth_service: Arc::new(Mutex::new(MockAuthorizationService::new())),
            input: None,
            result: None,
        }
    }
}

// ===== AC1: Create a valid workflow successfully =====
// Trace: CBF-REQ-1
// Frame Concerns: WF-FC-AUTH, FC2

#[given(expr = "a boardId {string} is provided")]
async fn given_board_id(world: &mut CreateWorkflowWorld, board_id: String) {
    world.input = Some(CreateWorkflowInput {
        board_id,
        name: String::new(),
        operator_id: String::new(),
    });
}

#[given(expr = "a user {string} is authorized to create workflows for that boardId")]
async fn given_user_authorized(world: &mut CreateWorkflowWorld, user_id: String) {
    let mut input = world.input.take().unwrap();
    input.operator_id = user_id.clone();
    world.input = Some(input);

    let mut auth = world.auth_service.lock().await;
    auth.allow_capability(&user_id, "create_workflow", &world.input.as_ref().unwrap().board_id);
}

#[given(expr = "a user {string} is NOT authorized to create workflows")]
async fn given_user_not_authorized(world: &mut CreateWorkflowWorld, user_id: String) {
    let mut input = world.input.take().unwrap();
    input.operator_id = user_id;
    world.input = Some(input);

    let mut auth = world.auth_service.lock().await;
    auth.deny_all();
}

#[when(expr = "the user requests to create a workflow with name {string}")]
async fn when_create_workflow(world: &mut CreateWorkflowWorld, name: String) {
    let mut input = world.input.take().unwrap();
    input.name = name;
    world.input = Some(input.clone());

    let use_case = CreateWorkflowUseCase::new(
        world.repository.clone(),
        world.event_publisher.clone(),
        world.auth_service.clone(),
    );

    world.result = Some(use_case.execute(input).await);
}

#[when("the user attempts to create a workflow")]
async fn when_attempt_create(world: &mut CreateWorkflowWorld) {
    let mut input = world.input.take().unwrap();
    input.name = "Test Workflow".to_string();
    world.input = Some(input.clone());

    let use_case = CreateWorkflowUseCase::new(
        world.repository.clone(),
        world.event_publisher.clone(),
        world.auth_service.clone(),
    );

    world.result = Some(use_case.execute(input).await);
}

#[then("the request should succeed")]
async fn then_success(world: &mut CreateWorkflowWorld) {
    assert!(world.result.as_ref().unwrap().is_ok(), "Expected success but got error");
}

#[then(expr = "the request should fail with {string}")]
async fn then_fail_with(world: &mut CreateWorkflowWorld, error_type: String) {
    let result = world.result.as_ref().unwrap();
    assert!(result.is_err(), "Expected error but got success");
    
    let err = result.as_ref().unwrap_err();
    match error_type.as_str() {
        "AuthorizationError" => assert!(matches!(err, DomainError::Unauthorized(_))),
        "ValidationError" => assert!(matches!(err, DomainError::Validation(_))),
        _ => panic!("Unknown error type: {}", error_type),
    }
}

#[then(expr = "a Workflow should be created with name {string}")]
async fn then_workflow_created(world: &mut CreateWorkflowWorld, name: String) {
    let result = world.result.as_ref().unwrap().as_ref().unwrap();
    let repo = world.repository.lock().await;
    let workflow = repo.find_by_id(&result.workflow_id).await.unwrap().unwrap();
    
    assert_eq!(workflow.name, name);
}

#[then(expr = "the Workflow should belong to Board {string}")]
async fn then_workflow_belongs_to_board(world: &mut CreateWorkflowWorld, board_id: String) {
    let result = world.result.as_ref().unwrap().as_ref().unwrap();
    let repo = world.repository.lock().await;
    let workflow = repo.find_by_id(&result.workflow_id).await.unwrap().unwrap();
    
    assert_eq!(workflow.board_id, board_id);
}

#[then("the Workflow should be active")]
async fn then_workflow_active(world: &mut CreateWorkflowWorld) {
    let result = world.result.as_ref().unwrap().as_ref().unwrap();
    let repo = world.repository.lock().await;
    let workflow = repo.find_by_id(&result.workflow_id).await.unwrap().unwrap();
    
    assert!(!workflow.is_deleted);
}

#[then("a WorkflowCreated event should be published")]
async fn then_event_published(world: &mut CreateWorkflowWorld) {
    let publisher = world.event_publisher.lock().await;
    assert_eq!(publisher.event_count(), 1);
    assert!(publisher.has_event_type("WorkflowCreated"));
}

#[then("no Workflow should be created")]
async fn then_no_workflow(world: &mut CreateWorkflowWorld) {
    let repo = world.repository.lock().await;
    assert_eq!(repo.count().await, 0);
}

// ===== Test Runner =====

#[tokio::main]
async fn main() {
    CreateWorkflowWorld::run("tests/features/create-workflow.feature").await;
}
```

### Rust: Cargo.toml 依賴

```toml
[dev-dependencies]
cucumber = { version = "0.20", features = ["macros"] }
async-trait = "0.1"
tokio = { version = "1", features = ["full", "test-util"] }
```

---

## 框架選擇指南

| 考量 | Java | Go | TypeScript | Rust |
|------|------|-----|------------|------|
| **推薦框架** | ezSpec | Ginkgo | Cucumber.js | cucumber-rs |
| **備選** | Cucumber-JVM | godog | jest-cucumber | - |
| **Step Definition** | 自動 (ezSpec) | 內建 | 手寫 | 宏輔助 |
| **非同步支援** | ✅ | ✅ | ✅ | ✅ (async/await) |
| **表格測試** | Examples | DescribeTable | Scenario Outline | Examples |
| **IDE 支援** | IntelliJ | GoLand | VS Code | rust-analyzer |

---

## 與其他 Skills 的協作

```
analyze-frame
    │
    └── 生成 acceptance.yaml
            │
            └── generate-acceptance-test (本 Skill)
                    │
                    ├── 生成 .feature (Gherkin)
                    ├── 生成 Java ezSpec (Fluent API)
                    ├── 生成 Go Ginkgo tests
                    ├── 生成 TypeScript Cucumber steps
                    ├── 生成 Rust cucumber-rs tests
                    │
                    ├── 連結 → enforce-contract (驗證 contracts)
                    └── 連結 → cross-context (驗證 ACL)
```
