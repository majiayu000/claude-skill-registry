---
name: multi-model-reviewer
description: 協調多個 AI 模型（ChatGPT、Gemini、Codex、QWEN、Claude）進行三角驗證，確保「Specification == Program == Test」一致性。過濾假警報後輸出報告，大幅減少人工介入時間。
---

# Multi-Model Reviewer Skill

## 觸發時機

- 規格變更後需要驗證一致性
- Pull Request 審查階段
- CI/CD Pipeline 中的品質門檻
- 開發人員請求全面審查時

## 核心任務

透過多模型交叉驗證，確保：
1. **Specification ↔ Program**：規格有的，程式必須實作
2. **Program ↔ Test**：程式有的，測試必須涵蓋
3. **Test ↔ Specification**：測試驗證的，規格必須定義

---

## 驗證三角形

```
        ┌─────────────────┐
        │  Specification  │
        │   (YAML Specs)  │
        └────────┬────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌───────┐   ┌───────┐   ┌───────┐
│ Spec  │   │ Spec  │   │ Test  │
│  ==   │   │  ==   │   │  ==   │
│Program│   │ Test  │   │Program│
└───────┘   └───────┘   └───────┘
```

---

## 多模型架構

### 參與的 AI Agents

| # | Model | 呼叫方式 | 專長 |
|---|-------|----------|------|
| 1 | ChatGPT 5.2 | API (OpenAI) | 語意理解、邏輯推理 |
| 2 | Gemini | CLI (本地) | 多模態、長上下文 |
| 3 | Codex | CLI (本地) | 代碼生成、理解 |
| 4 | QWEN 32B | Local LLM | 中文理解、快速推理 |
| 5 | Claude | CLI (本地) | 規格分析、假警報過濾 |

### 審查流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Model Review Pipeline                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                     │
│  │   Spec   │   │  Program │   │   Test   │                     │
│  │  (YAML)  │   │  (Code)  │   │  (BDD)   │                     │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘                     │
│       │              │              │                            │
│       └──────────────┼──────────────┘                            │
│                      ▼                                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Parallel Review                          │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────┐ │  │
│  │  │ChatGPT  │ │ Gemini  │ │  Codex  │ │  QWEN   │ │Claude│ │  │
│  │  │  5.2    │ │   CLI   │ │   CLI   │ │  32B    │ │ CLI  │ │  │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └──┬───┘ │  │
│  │       │           │           │           │         │      │  │
│  │       └───────────┴───────────┴───────────┴─────────┘      │  │
│  │                           │                                 │  │
│  └───────────────────────────┼─────────────────────────────────┘  │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Claude: False Positive Filter                 │  │
│  │                                                            │  │
│  │  • 交叉比對各模型發現                                       │  │
│  │  • 過濾假警報 (≥3 models agree = real issue)              │  │
│  │  • 分類嚴重程度                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Final Report                            │  │
│  │                                                            │  │
│  │  ✅ PASS / ⚠️ WARNINGS / ❌ ERRORS                         │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 驗證項目

### 1. Specification → Program (規格 → 實作)

檢查規格定義的內容是否都有對應實作：

```yaml
checks:
  - id: SP1
    name: "Domain Events 實作完整性"
    rule: "frame.yaml 定義的 domain_events 必須在程式中有對應實作"
    example: "WorkflowCreated event defined but not published in CreateWorkflowUseCase"
  
  - id: SP2
    name: "Use Case 實作完整性"
    rule: "use-case.yaml 定義的 input/output 必須與實際 Service 一致"
  
  - id: SP3
    name: "Invariants 實作"
    rule: "aggregate.yaml 的 invariants 必須在 Aggregate 中有 enforced_in 對應的驗證"
  
  - id: SP4
    name: "Pre/Post Conditions"
    rule: "contracts 定義的 pre_conditions 必須在程式中有檢查"
```

### 2. Program → Test (實作 → 測試)

檢查實作的功能是否都有測試涵蓋：

```yaml
checks:
  - id: PT1
    name: "Use Case 測試覆蓋"
    rule: "每個 Service class 必須有對應的測試 class"
  
  - id: PT2
    name: "Domain Event 測試"
    rule: "程式發布的 Domain Events 必須在測試中驗證"
  
  - id: PT3
    name: "Error Path 測試"
    rule: "程式拋出的每種 Exception 必須有對應的測試案例"
  
  - id: PT4
    name: "Invariant 測試"
    rule: "Aggregate 的每個 invariant 必須有違反時的測試"
```

### 3. Test → Specification (測試 → 規格)

檢查測試驗證的內容是否都有規格定義：

```yaml
checks:
  - id: TS1
    name: "測試追溯性"
    rule: "每個測試案例必須能追溯到 acceptance.yaml 的 AC"
  
  - id: TS2
    name: "Frame Concerns 覆蓋"
    rule: "所有 frame_concerns 必須被測試涵蓋"
  
  - id: TS3
    name: "隱式行為"
    rule: "測試驗證的行為如果規格沒有定義，標記為潛在遺漏"
```

---

## 輸出格式

### 審查摘要報告

```
╔═══════════════════════════════════════════════════════════════════╗
║            DOMAIN EVENT STANDARD UPDATE SUMMARY                    ║
╠═══════════════════════════════════════════════════════════════════╣
║ #  │ Use Case              │ Event                │ Status        ║
╠════╪═══════════════════════╪══════════════════════╪═══════════════╣
║ 1  │ create-workflow       │ WorkflowCreated      │ ✅ DONE       ║
║ 2  │ create-stage          │ StageCreated         │ ✅ DONE       ║
║ 3  │ create-swimlane       │ SwimLaneCreated      │ ✅ DONE       ║
║ 4  │ copy-lane             │ LaneCopied           │ ✅ DONE       ║
║ 5  │ move-lane             │ LaneMoved            │ ✅ DONE       ║
║ 6  │ delete-lane           │ LaneDeleted          │ ✅ DONE       ║
║ 7  │ rename-lane           │ LaneRenamed          │ ✅ DONE       ║
║ 8  │ rename-workflow       │ WorkflowRenamed      │ ✅ DONE       ║
║ 9  │ delete-workflow       │ WorkflowDeleted      │ ✅ DONE       ║
║ 10 │ move-workflow         │ WorkflowMoved        │ ✅ DONE       ║
║ 11 │ set-wip-limit         │ WipLimitSet          │ ✅ DONE       ║
║ 12 │ change-workflow-note  │ WorkflowNoteChanged  │ ✅ DONE       ║
╠════╧═══════════════════════╧══════════════════════╧═══════════════╣
║ TOTAL: 12/12 (100%) ✅                                             ║
╚═══════════════════════════════════════════════════════════════════╝

變更摘要：
每個 aggregate.yaml 的 domain_events 區塊現在統一：
1. 新增 includes_standard: true
2. 新增 standard_ref: "../../../../shared/domain-event-standard.yaml"
3. 移除重複的 id 和 occurredOn 屬性
4. 新增 metadata 屬性的註解說明
5. 調整 workflowId 為第一個屬性（一致的排序）

共用標準檔案：
- /.dev/problem-frames/ezkanban/board-management/shared/domain-event-standard.yaml

這樣就解決了 multi-model review 發現的 metadata spec mismatch 問題，
所有 12 個 Workflow aggregate 的 domain events 現在都符合標準。
```

### 問題報告格式

```yaml
review_report:
  timestamp: "2025-12-31T10:30:00Z"
  spec_dir: "docs/specs/create-workflow/"
  
  summary:
    total_checks: 24
    passed: 22
    warnings: 1
    errors: 1
    
  issues:
    - id: ISSUE-001
      severity: error
      type: "spec_program_mismatch"
      description: "Domain event 'WorkflowCreated' missing 'metadata' property in spec"
      detected_by: ["chatgpt", "gemini", "claude"]  # 3/5 models
      confidence: high
      
      spec_location: "aggregate.yaml#domain_events.WorkflowCreated"
      program_location: "WorkflowEvents.java#WorkflowCreated"
      
      spec_definition: |
        properties:
          - workflowId
          - boardId
          - name
          
      program_implementation: |
        record WorkflowCreated(
            WorkflowId workflowId,
            BoardId boardId,
            String name,
            EventMetadata metadata  // ← Missing in spec
        )
      
      suggested_fix: |
        Add 'metadata' property to aggregate.yaml:
        ```yaml
        domain_events:
          - name: WorkflowCreated
            includes_standard: true
            standard_ref: "../shared/domain-event-standard.yaml"
        ```
    
    - id: ISSUE-002
      severity: warning
      type: "test_coverage_gap"
      description: "No test for 'WorkflowCreated' event publication"
      detected_by: ["codex", "qwen"]  # 2/5 models - warning level
      confidence: medium
      
      test_location: "CreateWorkflowAcceptanceTest.java"
      suggestion: "Add assertion for event publication in ThenSuccess block"
```

---

## 假警報過濾規則

### 共識閾值

```yaml
consensus_rules:
  error:
    threshold: 3  # ≥3 models agree = confirmed error
    action: "report as error"
  
  warning:
    threshold: 2  # 2 models agree = warning
    action: "report as warning"
  
  ignored:
    threshold: 1  # only 1 model = likely false positive
    action: "log but don't report"
```

### Claude 最終裁決

Claude 作為最終審查者，負責：

1. **語意分析**：理解各模型的發現是否指向同一問題
2. **上下文判斷**：考慮專案特定的慣例
3. **嚴重程度分類**：根據影響範圍分級
4. **建議生成**：提供可執行的修復建議

---

## 工具腳本 (scripts/)

### multi_model_review.py

```bash
# 執行多模型審查
python ~/.claude/skills/multi-model-reviewer/scripts/multi_model_review.py \
    --spec-dir docs/specs/create-workflow/ \
    --program-dir src/application/workflow/ \
    --test-dir tests/acceptance/workflow/ \
    --output review-report.yaml

# 只驗證規格與程式
python ~/.claude/skills/multi-model-reviewer/scripts/multi_model_review.py \
    --spec-dir docs/specs/create-workflow/ \
    --program-dir src/application/workflow/ \
    --check spec-program

# 使用特定模型子集
python ~/.claude/skills/multi-model-reviewer/scripts/multi_model_review.py \
    --spec-dir docs/specs/create-workflow/ \
    --models chatgpt,claude,gemini
```

---

## 與其他 Skills 的協作

```
spec-compliance-validator
    │
    ├── 驗證單一規格完整性
    │
    └── 提供規格資料給 →
                        │
                        ▼
            multi-model-reviewer (本 Skill)
                        │
                        ├── 協調 5 個 AI Agents
                        ├── 交叉驗證 Spec == Program == Test
                        ├── Claude 過濾假警報
                        │
                        └── 輸出報告給 →
                                        │
                                        ▼
                              code-reviewer
                                        │
                                        └── 開發人員確認 → AI 修訂
```

---

## 配置檔案

### .multi-model-review.yaml

```yaml
# 專案根目錄配置
models:
  chatgpt:
    enabled: true
    api_key_env: "OPENAI_API_KEY"
    model: "gpt-5.2"
    
  gemini:
    enabled: true
    cli_command: "gemini"
    
  codex:
    enabled: true
    cli_command: "codex"
    
  qwen:
    enabled: true
    endpoint: "http://localhost:11434/api/generate"
    model: "qwen2.5:32b"
    
  claude:
    enabled: true
    cli_command: "claude"
    role: "final_arbiter"  # 最終裁決者

paths:
  specs: "docs/specs/"
  source: "src/"
  tests: "tests/"

shared_standards:
  domain_events: "shared/domain-event-standard.yaml"
  
consensus:
  error_threshold: 3
  warning_threshold: 2
```

---

## 開發人員工作流程

```
1. 開發完成
       │
       ▼
2. 執行 multi-model-review
       │
       ▼
3. 收到報告
   ├── ✅ PASS → 提交 PR
   │
   └── ❌ ISSUES FOUND
           │
           ▼
4. 開發人員確認
   ├── 真問題 → 請 AI 修訂
   │              │
   │              ▼
   │         5. AI 自動修復
   │              │
   │              ▼
   │         6. 重新驗證 → 回到步驟 2
   │
   └── 假警報 → 標記忽略規則
```

### 效益

- **減少人工審查時間**：只需確認 AI 發現的問題
- **提高一致性**：多模型交叉驗證降低漏檢率
- **自動修復**：確認問題後 AI 自動生成修復方案
- **標準化**：建立共用標準檔案，統一規格格式
