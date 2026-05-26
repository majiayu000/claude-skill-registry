---
name: analyze-frame
description: 當接收到新需求或 Event Storming 產出後觸發。分析問題類別（CBF/IDF/RIF），生成完整的規格目錄結構。實現「需求與實作分離」、「規格即文檔、文檔即規格」。
---

# Analyze Frame Skill

## 觸發時機

- 接收到新需求描述時
- Event Storming 工作坊產出後
- 使用者要求分析問題框架時

## 核心任務

將需求分析為 Problem Frames 的五種基本類別，並輸出結構化的規格目錄。

---

## Problem Frame 類別定義

### CBF (Commanded Behavior Frame) - 命令行為框架
- **特徵**：Operator 發出命令，Machine 控制 Controlled Domain 執行狀態變更
- **對應 Sub-agent**：`command-sub-agent`
- **典型場景**：建立訂單、更新資料、執行交易
- **CQRS 角色**：Command Side

### IDF (Information Display Frame) - 資訊顯示框架
- **特徵**：使用者查詢資訊，系統回傳資料（無狀態變更）
- **對應 Sub-agent**：`query-sub-agent`
- **典型場景**：查詢報表、搜尋資料、讀取詳情
- **CQRS 角色**：Query Side

### RIF (Required Behavior Frame) - 反應式框架
- **特徵**：系統對事件做出反應，通常是非同步處理
- **對應 Sub-agent**：`reactor-sub-agent`
- **典型場景**：事件監聽、訊息處理、系統整合

### WPF (Workpieces Frame) - 工作件框架
- **特徵**：對工作產物（文件、報告）進行編輯與管理
- **典型場景**：文件編輯、報表生成

### TF (Transformation Frame) - 轉換框架
- **特徵**：輸入資料經過轉換產生輸出
- **典型場景**：資料轉換、格式轉換、ETL

---

## 輸出：規格目錄結構

在 `docs/specs/{feature-name}/` 目錄下生成完整規格：

```
docs/specs/{feature-name}/
├── frame.yaml                 # 問題框架定義 (核心)
├── acceptance.yaml            # 驗收測試規格 (在根目錄)
│
├── requirements/              # 需求層 (What) - 純業務語言
│   └── cbf-req-1-{feature}.yaml
│
├── machine/                   # 機器層 (How) - Application 層
│   ├── machine.yaml           # Machine 定義
│   ├── controller.yaml        # API 入口規格
│   └── use-case.yaml          # Use Case 規格
│
├── controlled-domain/         # 領域層 - Domain 層
│   └── aggregate.yaml         # Aggregate + Entities + Value Objects
│
├── cross-context/             # 跨 Bounded Context 依賴 (若有)
│   └── {context-name}.yaml    # ACL 定義
│
└── runbook/                   # 執行指南 (選用)
    └── execute.md
```

### 命名規範

- **requirements/**: `{frame-type}-req-{n}-{feature}.yaml`
  - 範例：`cbf-req-1-create-workflow.yaml`
  - Frame Type: `cbf` | `idf` | `rif` | `wpf` | `tf`
- **acceptance.yaml**: 放在規格根目錄，不是子目錄

---

## frame.yaml 規格格式

```yaml
# docs/specs/{feature-name}/frame.yaml
problem_frame: "{FeatureName}"
frame_type: CommandedBehaviorFrame  # | InformationDisplayFrame | RequiredBehaviorFrame

intent: |
  {一句話描述問題意圖}
  {使用 "When ... the Machine shall ..." 格式}

# ---------------------------------------------------------------------------
# Problem Frame Components
# ---------------------------------------------------------------------------

operator:
  name: "{Actor}"
  description: "{Actor 描述}"

machine:
  name: "{FeatureName}Machine"
  machine_spec: machine/machine.yaml

controlled_domain:
  domain: "{DomainName}"
  entity: "{AggregateRoot} (Aggregate Root)"
  aggregate_spec: controlled-domain/aggregate.yaml

# ---------------------------------------------------------------------------
# Frame Concerns（問題框架關注點）
# ---------------------------------------------------------------------------

frame_concerns:
  - id: FC1
    name: "{Concern Name}"
    description: |
      {描述這個關注點的業務規則或技術約束}
    satisfied_by:
      - controlled-domain/aggregate.yaml#invariants.{name}
      - tests#{test-id}

  - id: FC2
    name: "Interference / Concurrency"
    description: |
      {描述並發或干擾問題}
    satisfied_by:
      - machine/use-case.yaml#transaction_boundary
      - machine/use-case.yaml#idempotency

# ---------------------------------------------------------------------------
# Cross-Context Dependencies（跨限界上下文依賴）
# ---------------------------------------------------------------------------

cross_context_dependencies:
  - id: XC1
    name: "{DependencyName}"
    source_context: "{SourceBC}"
    target_context: "{CurrentBC}"
    interface_type: "AntiCorruption Layer"
    contract_spec: cross-context/{context-name}.yaml

# ---------------------------------------------------------------------------
# Generation Metadata（生成元數據）
# ---------------------------------------------------------------------------

generation:
  version: "1.0.0"
  created_at: "{ISO-8601}"
  last_generated: null
  
  history: []
  
  output_paths:
    application: "src/application/use-cases/"
    domain: "src/domain/"
    infrastructure: "src/infrastructure/"
```

---

## requirements/req-{n}-{feature}.yaml 格式

```yaml
# 需求層：純業務語言，不含任何實作細節
requirement:
  id: REQ-{NNN}
  title: "{Feature Title}"
  type: functional  # | non-functional | constraint
  priority: high    # | medium | low
  
  # User Story 格式
  description: |
    As a {Actor}
    I want to {Action}
    So that {Benefit}
  
  # 業務規則（仍在需求層，無實作）
  business_rules:
    - id: BR1
      rule: "{Business Rule 1}"
    - id: BR2
      rule: "{Business Rule 2}"
  
  # 連結到 Frame Concerns
  addresses_concerns:
    - FC1
    - FC2
  
  # 驗收條件（高層次）
  acceptance_conditions:
    - "AC1: {Condition 1}"
    - "AC2: {Condition 2}"
```

---

## machine/use-case.yaml 格式

```yaml
# Machine 層：Application 層規格
use_case:
  name: "{FeatureName}UseCase"
  type: command  # | query
  
  # Input/Output 定義
  input:
    name: "{FeatureName}Input"
    fields:
      - name: "{fieldName}"
        type: "{Type}"
        required: true
        validation: "{validation rule}"
  
  output:
    name: "{FeatureName}Output"
    fields:
      - name: "{fieldName}"
        type: "{Type}"

  # Design by Contract
  contracts:
    pre_conditions:
      - id: PRE1
        condition: "{condition}"
        error: "{ErrorType}"
    
    post_conditions:
      - id: POST1
        condition: "{condition}"
  
  # 技術約束
  transaction_boundary:
    type: "RequiresNew"
    isolation: "ReadCommitted"
  
  idempotency:
    enabled: true
    key: "{idempotencyKeyField}"
  
  # 發布的 Domain Events
  publishes_events:
    - "{FeatureName}CreatedEvent"
```

---

## controlled-domain/aggregate.yaml 格式

```yaml
# Domain 層：Aggregate 規格
aggregate:
  name: "{AggregateName}"
  root: true
  
  # 身份識別
  identity:
    name: "{AggregateName}Id"
    type: "UUID"
  
  # 屬性
  properties:
    - name: "{propertyName}"
      type: "{Type}"
      mutable: false
  
  # 內部 Entities
  entities:
    - name: "{EntityName}"
      identity: "{EntityName}Id"
  
  # Value Objects
  value_objects:
    - name: "{ValueObjectName}"
      properties:
        - name: "{prop}"
          type: "{Type}"
  
  # Invariants（不變量）
  invariants:
    shared:
      - id: INV1
        name: "{InvariantName}"
        rule: "{Rule description}"
        enforced_in: 
          - "constructor"
          - "method:{methodName}"
  
  # Domain Events
  domain_events:
    - name: "{AggregateName}CreatedEvent"
      properties:
        - name: "{prop}"
          type: "{Type}"
```

---

## 分析流程

1. **識別 Operator**：誰發起這個需求？
2. **識別 Machine**：需要什麼機器來處理？
3. **識別 Controlled Domain**：控制什麼領域實體？
4. **識別 Frame Concerns**：有哪些關注點需要滿足？
5. **識別 Cross-Context**：是否依賴其他 Bounded Context？
6. **分類 Frame**：根據上述判斷屬於五種 Frame 之一
7. **生成規格目錄**：輸出完整目錄結構

---

## 實作優先順序策略

### 原則

1. **先核心 Aggregate，後支援 Aggregate**
2. **先 Command，後 Query**（或並行）
3. **依相依性順序**：被依賴的先做
4. **完整生命週期**：一個 Aggregate 完成 CRUD 後再換下一個

### 優先順序規劃範例

當有多個 Aggregate 和 Use Case 時，建議按以下方式排序：

```
Phase 1: 核心 Aggregate 建立 (Create)
├── create-product.json      ✅ 已完成
├── create-pbi.json          ✅ 已完成
└── create-sprint.json       ✅ 已完成

Phase 2: 完成第一個 Aggregate 生命週期
├── start-sprint             → Command | Medium
├── complete-sprint          → Command | Medium
├── cancel-sprint            → Command | Low
├── get-sprint               → Query   | Low
├── get-sprints-by-product   → Query   | Low
└── delete-sprint            → Command | Medium

Phase 3: 擴展其他 Aggregate
├── Product Aggregate (6 use cases)
├── PBI Aggregate (15 use cases) - 最大 backlog
└── Scrum Team Aggregate (5 use cases) - 新 aggregate
```

### 複雜度評估

| 複雜度 | 標準 | 估計時間 |
|--------|------|----------|
| Low | 單一 Aggregate，無跨 BC | 1-2 小時 |
| Medium | 有驗證邏輯或狀態轉換 | 2-4 小時 |
| High | 跨多個 Aggregate 或 BC | 4-8 小時 |

---

## 品質檢查清單

- [ ] Frame 類別判斷是否正確？
- [ ] 需求層是否只有業務語言，無實作細節？
- [ ] Frame Concerns 是否有明確的 satisfied_by 連結？
- [ ] 是否識別出所有跨 BC 依賴？
- [ ] Aggregate Invariants 是否完整？
- [ ] Acceptance Criteria 是否可測試？
- [ ] 是否涵蓋主要的異常場景？

---

## 與其他 Skills 的協作

```
analyze-frame (本 Skill)
    │
    ├── 輸出 → frame.yaml + 目錄結構
    │
    ├── spec-template → 生成各層 YAML 模板
    │
    ├── cross-context → 處理跨 BC 依賴
    │
    └── 觸發 Sub-agents
        ├── command-sub-agent (CBF)
        ├── query-sub-agent (IDF)
        └── reactor-sub-agent (RIF)
```

---

## 工具腳本 (scripts/)

本 Skill 提供驗證工具，位於 `scripts/` 目錄：

### validate_spec.py - 規格驗證器

用於驗證規格目錄的完整性與正確性。

**使用方式：**

```bash
# 驗證單一功能規格
python ~/.claude/skills/analyze-frame/scripts/validate_spec.py docs/specs/create-workflow/

# 驗證多個規格
python ~/.claude/skills/analyze-frame/scripts/validate_spec.py docs/specs/create-workflow/ docs/specs/query-dashboard/

# 在 CI/CD 中使用
python ~/.claude/skills/analyze-frame/scripts/validate_spec.py docs/specs/*/ || exit 1
```

**驗證項目：**

| 檢查項目 | 類型 | 說明 |
|---------|------|------|
| 目錄結構 | ERROR | 必要目錄是否存在 |
| frame.yaml | ERROR | 問題框架定義是否存在且有效 |
| YAML 語法 | ERROR | 所有 YAML 檔案語法正確性 |
| Frame Concerns | WARNING | 是否有 satisfied_by 連結 |
| Cross-Context | INFO | ACL 規格是否存在 |
| Acceptance | WARNING | 測試覆蓋率檢查 |

**Exit Codes：**
- `0`: 驗證通過
- `1`: 有 ERROR 級別錯誤
- `2`: 參數錯誤

---

## 規格範本 (templates/)

本 Skill 提供完整的 YAML 規格範本，位於 `templates/` 目錄：

```
templates/
├── frame.yaml                      # 問題框架範本
├── requirements/
│   └── req-template.yaml           # 需求規格範本 (純業務語言)
├── machine/
│   └── use-case.yaml               # Use Case 規格範本
├── controlled-domain/
│   └── aggregate.yaml              # Aggregate 規格範本
├── acceptance/
│   └── acceptance.yaml             # 驗收測試範本
├── cross-context/
│   └── authorization.yaml          # ACL 規格範本
└── runbook/
    └── execute.md                  # 執行指南範本
```

### 範本使用方式

1. **初始化新功能規格**：
   ```bash
   # 建立目錄結構
   mkdir -p docs/specs/{feature-name}/{requirements,machine,controlled-domain,cross-context,acceptance,runbook}
   
   # 複製範本
   cp ~/.claude/skills/analyze-frame/templates/frame.yaml docs/specs/{feature-name}/
   ```

2. **在 Claude 中使用**：
   ```
   請根據 ~/.claude/skills/analyze-frame/templates/ 的範本
   為「建立工作流程」功能生成規格目錄
   ```

### 範本特點

| 範本 | 用途 | 特點 |
|------|------|------|
| `frame.yaml` | 問題框架定義 | 包含 frame_concerns + satisfied_by |
| `req-template.yaml` | 需求規格 | 純業務語言，禁止實作細節 |
| `use-case.yaml` | Application 層 | Design by Contract、冪等性 |
| `aggregate.yaml` | Domain 層 | Invariants 含 enforced_in |
| `acceptance.yaml` | 測試規格 | BDD 格式，ezSpec 相容 |
| `authorization.yaml` | ACL 規格 | 容錯、重試、Circuit Breaker |
| `execute.md` | 執行指南 | 生成步驟、品質驗證 |

---

## 完整工作流程

```
1. 需求輸入
       ↓
2. 分析問題框架 (analyze-frame)
       ↓
3. 生成規格目錄 (使用 templates/)
       ↓
4. 驗證規格完整性 (scripts/validate_spec.py)
       ↓
5. 分派至 Sub-agent
   ├── command-sub-agent (CBF)
   ├── query-sub-agent (IDF)
   └── reactor-sub-agent (RIF)
       ↓
6. 生成程式碼
       ↓
7. 生成驗收測試 (generate-acceptance-test)
       ↓
8. 品質檢查 (arch-guard, enforce-contract)
       ↓
9. 執行測試驗證
```
