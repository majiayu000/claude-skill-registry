---
name: code-reviewer
description: 自動化代碼審查，檢查程式碼品質、架構合規性、編碼標準，並與規格定義進行比對。
---

# Code Reviewer Skill

## 觸發時機

- Pull Request 創建或更新
- 開發人員請求代碼審查
- CI/CD Pipeline 品質門檻
- 與 `multi-model-reviewer` 協作時

## 核心任務

1. **架構合規性檢查**：驗證 Clean Architecture 分層
2. **編碼標準檢查**：語言特定的編碼規範
3. **規格對照**：程式實作是否符合規格定義
4. **測試覆蓋**：確認關鍵路徑有測試

---

## 審查維度

### 1. Clean Architecture 合規性

```yaml
architecture_checks:
  layer_dependency:
    name: "依賴方向"
    rule: "外層只能依賴內層，內層不得依賴外層"
    layers:
      - adapter (外) → usecase → entity (內)
    violations:
      - "Entity 不得 import UseCase"
      - "UseCase 不得 import Adapter"
  
  package_structure:
    name: "套件結構"
    rule: "符合 {aggregate}/{layer}/{component} 結構"
    expected:
      - "{aggregate}/adapter/in/web/"
      - "{aggregate}/adapter/out/persistence/"
      - "{aggregate}/entity/"
      - "{aggregate}/usecase/port/"
      - "{aggregate}/usecase/service/"
```

### 2. DDD 模式檢查

```yaml
ddd_checks:
  aggregate_root:
    name: "Aggregate Root 識別"
    rule: "Aggregate Root 必須控制子實體的生命週期"
    markers:
      - "@AggregateRoot annotation"
      - "private constructor for child entities"
  
  value_object:
    name: "Value Object 不變性"
    rule: "Value Object 必須 immutable"
    checks:
      - "record class 或 final fields"
      - "no setters"
      - "equals/hashCode based on all fields"
  
  domain_event:
    name: "Domain Event 標準"
    rule: "符合 domain-event-standard.yaml"
    checks:
      - "sealed interface DomainEvent"
      - "includes standard metadata"
      - "occurredOn timestamp"
```

### 3. 語言特定標準

參考對應的編碼標準：

| 語言 | 參考文件 |
|------|----------|
| Java | `coding-standards/references/JAVA_CLEAN_ARCH.md` |
| TypeScript | `coding-standards/references/TYPESCRIPT.md` |
| Go | `coding-standards/references/GOLANG.md` |
| Rust | `coding-standards/references/RUST.md` |

---

## 審查檢查清單

### Use Case Service

```yaml
usecase_checks:
  - id: UC1
    name: "單一職責"
    rule: "一個 Service 只處理一個 Use Case"
    
  - id: UC2
    name: "Port 依賴"
    rule: "透過 Port interface 依賴外部資源"
    
  - id: UC3
    name: "輸入驗證"
    rule: "Input DTO 在 UseCase 層驗證"
    
  - id: UC4
    name: "Domain Event 發布"
    rule: "狀態變更後發布對應 Domain Event"
    
  - id: UC5
    name: "交易邊界"
    rule: "Aggregate 操作在單一交易內完成"
```

### Aggregate Entity

```yaml
aggregate_checks:
  - id: AG1
    name: "Invariant 保護"
    rule: "所有 public 方法必須維護 invariants"
    
  - id: AG2
    name: "私有建構子"
    rule: "Child Entity 使用 private/package constructor"
    
  - id: AG3
    name: "狀態封裝"
    rule: "不直接暴露可變集合"
    
  - id: AG4
    name: "Factory Method"
    rule: "複雜物件使用 Factory 創建"
```

### Repository/Adapter

```yaml
adapter_checks:
  - id: AD1
    name: "Port 實作"
    rule: "Adapter 必須實作對應的 Port interface"
    
  - id: AD2
    name: "依賴注入"
    rule: "透過 Constructor Injection"
    
  - id: AD3
    name: "錯誤轉換"
    rule: "Infrastructure 錯誤轉換為 Domain 錯誤"
```

---

## 輸出格式

### 審查報告

```
╔═══════════════════════════════════════════════════════════════════╗
║                      CODE REVIEW REPORT                            ║
╠═══════════════════════════════════════════════════════════════════╣
║ File: CreateWorkflowService.java                                   ║
║ Aggregate: Workflow                                                ║
║ Layer: usecase/service                                             ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║ ✅ UC1: Single Responsibility                    PASS              ║
║ ✅ UC2: Port Dependency                          PASS              ║
║ ✅ UC3: Input Validation                         PASS              ║
║ ⚠️ UC4: Domain Event Publication                 WARNING           ║
║    └─ Event 'WorkflowCreated' missing 'metadata' field            ║
║ ✅ UC5: Transaction Boundary                     PASS              ║
║                                                                    ║
╠═══════════════════════════════════════════════════════════════════╣
║ TOTAL: 4/5 PASS, 1 WARNING                                         ║
╚═══════════════════════════════════════════════════════════════════╝
```

### 問題詳情

```yaml
review_issues:
  - id: CR-001
    file: "CreateWorkflowService.java"
    line: 45
    severity: warning
    check: UC4
    message: "Domain Event 'WorkflowCreated' missing 'metadata' field"
    
    current_code: |
      return new WorkflowCreated(
          workflow.getId(),
          workflow.getBoardId(),
          workflow.getName()
      );
    
    suggested_fix: |
      return new WorkflowCreated(
          workflow.getId(),
          workflow.getBoardId(),
          workflow.getName(),
          EventMetadata.now()  // Add metadata
      );
    
    spec_reference: "aggregate.yaml#domain_events.WorkflowCreated"
```

---

## 與其他 Skills 協作

```
                    ┌─────────────────────┐
                    │   code-reviewer     │ ◄── 本 Skill
                    │   (代碼審查)         │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   arch-guard    │ │coding-standards │ │ multi-model-    │
│ (架構守護)       │ │ (編碼標準)       │ │ reviewer        │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## 命令行工具

```bash
# 審查單一檔案
python ~/.claude/skills/code-reviewer/scripts/review.py \
    --file src/workflow/usecase/service/CreateWorkflowService.java

# 審查目錄
python ~/.claude/skills/code-reviewer/scripts/review.py \
    --dir src/workflow/

# 比對規格
python ~/.claude/skills/code-reviewer/scripts/review.py \
    --file src/workflow/usecase/service/CreateWorkflowService.java \
    --spec docs/specs/create-workflow/

# PR 審查模式
python ~/.claude/skills/code-reviewer/scripts/review.py \
    --git-diff origin/main..HEAD
```

---

## 配置檔案

### .code-review.yaml

```yaml
language: java
architecture: clean-architecture

checks:
  architecture:
    enabled: true
    strict: true
    
  coding_standards:
    enabled: true
    config: ".coding-standards.yaml"
    
  spec_compliance:
    enabled: true
    spec_dir: "docs/specs/"

ignore:
  files:
    - "**/test/**"
    - "**/generated/**"
  rules:
    - UC5  # Skip transaction check for specific cases

severity_thresholds:
  error: 0    # Block if any errors
  warning: 5  # Block if > 5 warnings
```
