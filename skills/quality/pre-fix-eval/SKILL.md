---
name: pre-fix-eval
description: "修復前強制評估系統. Use for: (1) 測試失敗自動評估, (2) 編譯錯誤分類處理, (3) 強制 Ticket 開設流程"
type: evaluation
category: quality-assurance
---

# 修復前強制評估 (Pre-Fix Evaluation) SKILL

**版本**: v1.0
**建立日期**: 2025-01-12
**狀態**: ✅ 實作完成，驗收通過

## 概述

修復前強制評估系統是一套完整的錯誤分析和修復流程，確保在修復任何問題前都進行充分的分析和規劃。該系統包含：

1. **自動錯誤偵測與分類** (PostToolUse Hook)
2. **六階段評估流程** (本 Skill)
3. **強制 Ticket 開設機制**
4. **專業代理人分派決策樹**

## 核心功能

### 自動錯誤分類

Hook 自動識別四種錯誤類型：

| 錯誤類型 | 識別模式 | 開 Ticket | 流程 | 代理人 |
|---------|---------|----------|------|--------|
| **SYNTAX_ERROR** | 括號、分號、拼字 | ❌ 不需 | 簡化流程 | mint-format-specialist |
| **COMPILATION_ERROR** | 類型、引用、導入 | ✅ 必須 | 完整評估 | parsley-flutter-developer |
| **TEST_FAILURE** | 斷言失敗、失敗計數 | ✅ 必須 | 完整評估 | parsley-flutter-developer |
| **ANALYZER_WARNING** | lint 警告、棄用 API | ✅ 必須 | 評估+延遲 | mint-format-specialist |

### 錯誤分類優先級

```
SYNTAX_ERROR > COMPILATION_ERROR > TEST_FAILURE > ANALYZER_WARNING
```

優先級高的錯誤會被優先分類，避免誤判。

## 強制評估流程

非語法錯誤必須進入完整的六階段評估流程：

```
Stage 1: 錯誤分類 (Hook 自動完成)
    ↓
Stage 2: BDD 意圖分析 (Skill 引導)
    ↓
Stage 3: 設計文件查詢 (用戶或 Skill 協助)
    ↓
Stage 4: 根因定位 (用戶分析)
    ↓
Stage 5: 開 Ticket 記錄 (強制, /ticket-create)
    ↓
Stage 6: 分派執行 (根據根因分派代理人)
```

## 六階段評估流程詳細說明

### 📋 Stage 1: 錯誤分類

**目標**: 準確識別錯誤類型和影響範圍

**檢查項目**:
- 錯誤訊息關鍵字分析
- 錯誤位置定位
- 相關檔案和模組識別
- 潛在影響面分析

**Hook 自動完成的項目**:
- ✅ 使用正則表達式分類錯誤類型
- ✅ 提供分類結果和建議流程
- ✅ 記錄評估結果到日誌

**輸出範例**:
```
Stage 1: 錯誤分類
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

錯誤類型: TEST_FAILURE
錯誤訊息: Expected: true, Actual: false
位置: test/unit/domains/import/services/import_service_test.dart:234
影響範圍: ImportService 相關功能
```

### 🎯 Stage 2: BDD 意圖分析（僅適用於非語法錯誤）

**目標**: 理解測試用例或程式邏輯的業務意圖

**分析項目**:
- **Given**: 初始狀態和前置條件
- **When**: 觸發的動作或條件變化
- **Then**: 預期的結果和行為

**關鍵問題**:
- 這個測試/程式在驗證什麼業務邏輯？
- 當前實作是否應該滿足這個需求？
- 業務需求是否發生變化？

**輸出範例**:
```
Stage 2: BDD 意圖分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Given: ImportService 載入了 Chrome 書籍列表
When: 執行 importBooks() 方法
Then: 應返回導入結果且不拋出異常

測試意圖: 驗證 Chrome 擴充套件書籍匯入功能
當前問題: importBooks() 方法拋出未預期的例外
```

### 📚 Stage 3: 設計文件查詢

**目標**: 檢查設計文件以確認需求和決策

**查詢檔案**:
- `docs/app-requirements-spec.md` - 應用需求規格
- `docs/app-use-cases.md` - 詳細用例說明
- `docs/ui_design_specification.md` - UI 設計
- `docs/work-logs/` - 相關的開發工作日誌
- `docs/app-error-handling-design.md` - 錯誤處理設計

**檢查項目**:
- 需求文件中是否定義了此功能？
- 是否有相關的設計決策記錄？
- 是否有已知的實作缺陷或待辦事項？
- 工作日誌中是否記錄了此問題？
- 是否有相關的設計變更記錄？

**輸出範例**:
```
Stage 3: 設計文件查詢
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

docs/app-use-cases.md:
  找到 Chrome 擴充套件匯入用例
  狀態: 已計畫，尚未實作完整

docs/app-requirements-spec.md:
  確認需要支援 Chrome 擴充套件書籍匯入
  必要欄位: title, author, ISBN, dateAdded

docs/work-logs/:
  找到相關記錄: v0.5.2-W1-003 (Chrome 書籍解析功能)
  狀態: 實作中
```

### 🔍 Stage 4: 根因定位

**目標**: 準確確定問題根本原因

**分析模式**:

| 問題現象 | 可能根因 | 判斷方法 |
|---------|--------|---------|
| 測試失敗 + 程式未實作 | 功能未完成 | 檢查程式碼是否有 TODO 或占位符 |
| 測試失敗 + 程式已實作 | 邏輯錯誤 | 檢查演算法和邊界條件 |
| 測試失敗 + 程式正確 | 測試過時 | 檢查設計文件是否有新的需求變更 |
| 編譯失敗 + 類型不匹配 | 設計變更 | 檢查介面定義是否已更新 |
| 語法錯誤 | 簡單拼寫 | 直接定位到括號/分號位置 |

**根因問題清單**:
1. 是否是未完成的實作？(TODO/占位符)
2. 是否是邏輯錯誤？(邊界條件、計算錯誤)
3. 是否是過度設計？(不需要的複雜性)
4. 是否是設計變更？(需求更新，文件未同步)
5. 是否是依賴問題？(版本衝突、缺少初始化)

**輸出範例**:
```
Stage 4: 根因定位
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

根因分析結果:
✓ 問題: importBooks() 方法拋出 null pointer 異常
✓ 根因: EventBus 在方法執行時尚未初始化
✓ 原因類別: 依賴問題 (初始化順序)

相關代碼位置:
  - lib/domains/import/services/import_service.dart:45
  - 調用: eventBus.post(BookImportedEvent(...))
  - 問題: eventBus 為 null
```

### 📋 Stage 5: 開 Ticket 記錄（強制）

**目標**: 將評估結果記錄為可追蹤的 Ticket

**強制要求**:
- ✅ **必須使用 `/ticket-create` 建立 Ticket**（除語法錯誤外）
- ✅ Ticket 必須包含前四階段的完整分析結果
- ✅ Ticket 必須明確指定修復策略
- ✅ Ticket 必須包含明確的驗收條件

**Ticket 建立提示模板**:

```markdown
# Fix {ErrorType}: {簡短描述}

## 🎯 錯誤分類
- 錯誤類型: {Stage 1 結果}
- 位置: {檔案路徑:行號}
- 影響範圍: {影響模組}

## 📊 BDD 分析
**Given**: {前置條件}
**When**: {觸發動作}
**Then**: {預期結果}

## 📚 文件查詢結果
- 需求規格: {查詢結果}
- 相關用例: {查詢結果}
- 工作日誌: {查詢結果}

## 🔍 根因分析
**根因**: {Stage 4 結果}
**根因類別**: {分類}

## 💡 修復策略
- **Action**: {修復動作: 補完/修正/更新}
- **Target**: {修復目標}
- **Approach**: {具體修復步驟}

## 📋 驗收條件
- [ ] {測試通過條件}
- [ ] {相關檢查}
- [ ] {文件同步}

## 5W1H 分析
- **Who**: {代理人} (執行者) | rosemary-project-manager (分派者)
- **What**: 修復 {錯誤類型}
- **When**: 評估完成後立即執行
- **Where**: {檔案路徑}
- **Why**: {根因分析}
- **How**: [Task Type: Implementation] {修復步驟}
```

**Ticket 建立檢查清單**:
- [ ] 標題清楚表達修復內容
- [ ] BDD 分析包含 Given-When-Then
- [ ] 文件查詢結果已記錄
- [ ] 根因分析明確
- [ ] 修復策略具體可行
- [ ] 驗收條件完整
- [ ] 5W1H 已填寫

### 🎯 Stage 6: 分派執行

**目標**: 將 Ticket 分派給專業代理人執行

**分派決策樹**:

```
修復 Ticket 已建立
    │
    ├─ 語法錯誤 (SYNTAX_ERROR)
    │   └─ 分派: mint-format-specialist
    │       └─ 說明: 直接精確修復括號/分號
    │
    ├─ 編譯錯誤 (COMPILATION_ERROR)
    │   ├─ 未完成實作?
    │   │   ├─ 是 → parsley-flutter-developer (補完實作)
    │   │   └─ 否 → parsley-flutter-developer (修正邏輯)
    │   │
    │   └─ 設計變更?
    │       ├─ 是 → PM 審核 → 再分派
    │       └─ 否 → parsley-flutter-developer
    │
    ├─ 測試失敗 (TEST_FAILURE)
    │   ├─ 邏輯錯誤?
    │   │   ├─ 是 → parsley-flutter-developer (修正邏輯)
    │   │   └─ 否 → pepper-test-implementer (更新測試)
    │   │
    │   └─ 根因明確後分派
    │
    └─ Analyzer 警告 (ANALYZER_WARNING)
        ├─ 棄用 API?
        │   └─ 是 → mint-format-specialist (更新 API 使用)
        │
        └─ 未使用符號?
            └─ 是 → mint-format-specialist (移除/修復)
```

**分派時檢查清單**:
- [ ] Ticket 已建立並有 ID
- [ ] Stage 1-4 分析完整
- [ ] 根因明確指導
- [ ] 修復策略清晰可行
- [ ] 代理人選擇符合任務類型
- [ ] 驗收條件完整

**分派指令格式**:
```python
Task(
    subagent_type="parsley-flutter-developer",
    description="修復測試失敗: ImportService",
    prompt="""
    修復 Ticket #{TICKET_ID}

    問題: {根因分析結果}

    修復策略:
    {詳細修復步驟}

    驗收條件:
    {完整的驗收檢查清單}

    禁止:
    - 不要修改測試邏輯
    - 不要進行大規模重寫
    - 執行後必須執行完整測試
    """
)
```

## 修復決策矩陣

根據以下矩陣決策修復方向：

| 情況 | 測試狀態 | 程式狀態 | Ticket | 修復行動 |
|------|---------|---------|--------|---------|
| **語法錯誤** | - | ❌ 語法錯誤 | ❌ 不需 | 直接精確修復 |
| **程式實作不完整** | ❌ 失敗 | ❌ 缺少實作 | ✅ 必須 | 評估 → 開 Ticket → 補完實作 |
| **程式邏輯錯誤** | ❌ 失敗 | ✅ 已實作 | ✅ 必須 | 評估 → 開 Ticket → 修正邏輯 |
| **測試過時** | ❌ 失敗 | ✅ 正確 | ✅ 必須 | 評估 → 開 Ticket → 驗證文件 → 更新測試 |
| **設計變更** | ❌ 失敗 | ❌ 無實作 | ✅ 必須 | 評估 → PM 審核 → 開 Ticket → 實作 → 測試 |
| **功能未實作** | ❌ 失敗 | ⚠️ 接口存在但未實作 | ✅ 必須 | 評估 → **查文件** → 開技術債 Ticket 或刪除測試 |

### 功能未實作的特殊處理規則

**此情況禁止以下行為**：
- ❌ 直接刪除測試而不查文件
- ❌ 直接標記測試為 `skip` 而不開 Ticket
- ❌ 假設功能不需要而跳過

**必須按以下順序處理**：
1. 查詢 `docs/app-requirements-spec.md` 確認功能定義
2. 查詢 `docs/usecase-flowcharts-review-report.md` 確認優先級
3. 根據優先級決定：
   - **高優先級** → 開實作 Ticket
   - **中/低優先級** → 開技術債 Ticket (TD-XXX)
   - **已放棄/被替代** → 刪除測試並記錄原因

## 常見情況處理指南

### 情況1: 語法錯誤

**識別**: 括號、分號、引號相關的錯誤

**流程**:
1. ✅ Hook 自動識別，提示簡化流程
2. ✅ 直接分派 mint-format-specialist
3. ✅ 無需開 Ticket

**範例**:
```
Error: Expected '}' but found 'void'

→ Hook 識別: SYNTAX_ERROR
→ 流程: 簡化 (直接修復)
→ 代理人: mint-format-specialist
→ Ticket: 不需要
```

### 情況2: 編譯錯誤 - 未完成實作

**識別**: Undefined name, missing implementation

**流程**:
1. ✅ 完成六階段評估
2. ✅ 開 Ticket: "實作缺失的方法"
3. ✅ 分派 parsley-flutter-developer

**例子**:
```
Error: Undefined name 'startBookScan'

Stage 4: 根因定位
→ 根因: startBookScan() 方法在 ScanService 中未實作
→ 原因類別: 功能未完成

→ Ticket: Implement ScanService.startBookScan()
→ Agent: parsley-flutter-developer
```

### 情況3: 測試失敗 - 邏輯錯誤

**識別**: Test assertion failed, expected X but got Y

**流程**:
1. ✅ 進行 BDD 分析確認測試意圖正確
2. ✅ 檢查程式邏輯是否正確實作
3. ✅ 開 Ticket: "修正邏輯錯誤"
4. ✅ 分派 parsley-flutter-developer

**例子**:
```
Test: test_import_returns_results_count()
Actual: 0 books imported
Expected: 3 books imported

Stage 2: BDD 分析
→ Given: ImportService 有 3 本書籍待匯入
→ When: importBooks() 執行
→ Then: 返回 3 本書籍

Stage 4: 根因定位
→ 根因: importBooks() 中的迴圈條件錯誤
→ 詳情: while (index < list.length) 應為 while (index <= list.length-1)

→ Ticket: Fix ImportService loop condition
→ Agent: parsley-flutter-developer
```

### 情況4: 測試失敗 - 過時測試

**識別**: Test passes in old code, passes in other modules, but fails for this module

**流程**:
1. ✅ 檢查設計文件是否有需求變更
2. ✅ 確認測試是否應該更新
3. ✅ 開 Ticket: "更新過時測試"
4. ✅ 分派 pepper-test-implementer

**例子**:
```
Test: test_widget_displays_rating()
Expected: Rating 顯示為 5 星
Actual: Widget 已移除評級功能

Stage 3: 文件查詢
→ 新需求: 移除評級功能
→ 設計更新: UI 規格已修改
→ 狀態: 測試未同步

→ Ticket: Update tests for removed rating feature
→ Agent: pepper-test-implementer
```

### 情況5: 測試失敗 - 功能未實作

**識別**: Test expects behavior that is not implemented (parameter accepted but not used, method exists but empty)

**流程**:
1. ✅ 進行 BDD 分析確認測試驗證的功能
2. ✅ **必須查詢設計文件確認功能需求狀態**
3. ✅ 根據文件查詢結果決定處理方式
4. ✅ 開 Ticket 或刪除測試（禁止直接跳過）

**文件查詢決策樹**:

```
測試驗證的功能在文件中的狀態？
    │
    ├─ 高優先級（必須實作）
    │   └─ 開實作 Ticket → 分派 parsley-flutter-developer
    │
    ├─ 中優先級（建議實作）
    │   └─ 開技術債 Ticket (TD-XXX) → 目標版本設為未來版本
    │
    ├─ 低優先級（可選實作）
    │   └─ 開技術債 Ticket → 標記為「延後」
    │
    └─ 已放棄/被替代
        └─ 刪除測試 → 記錄刪除原因到工作日誌
```

**禁止行為**:
- ❌ **禁止直接刪除測試而不查文件**
- ❌ **禁止直接標記測試為 `skip` 而不開 Ticket**
- ❌ **禁止假設功能不需要而跳過**

**必須執行的步驟**:
1. 查詢 `docs/app-requirements-spec.md` 確認功能定義
2. 查詢 `docs/app-use-cases.md` 確認用例狀態
3. 查詢 `docs/usecase-flowcharts-review-report.md` 確認優先級
4. 根據文件結果建立對應 Ticket 或刪除測試

**例子**:
```
Test: test_import_progress_tracking()
Expected: onProgress callback 被呼叫並報告進度
Actual: onProgress 參數接受但未實作

Stage 3: 文件查詢
→ docs/usecase-flowcharts-review-report.md:
  UC-01 進度回饋: 中優先級（建議調整）
  工作量: 2 小時

Stage 4: 根因定位
→ 根因: onProgress 回調功能尚未實作
→ 原因類別: 功能未完成（中優先級）

決策: 開技術債 Ticket
→ Ticket: 0.25.1-TD-001 - Implement onProgress callback
→ 目標版本: v0.26.x
→ 測試處理: 修改測試驗證基本功能，不依賴 onProgress
```

**後續行動檢查清單**:
- [ ] 文件查詢完成，優先級已確認
- [ ] 對應 Ticket 已建立（實作 Ticket 或技術債 Ticket）
- [ ] Ticket 已加入 todolist.md 技術債務追蹤表
- [ ] 測試已調整（驗證現有功能，不依賴未實作功能）
- [ ] 工作日誌已記錄處理決策

### 情況6: 編譯錯誤 - 設計變更

**識別**: Type mismatch, method signature changes

**流程**:
1. ✅ 檢查設計文件確認介面定義
2. ✅ PM 評估影響範圍
3. ✅ 開 Ticket: "同步設計變更"
4. ✅ 分派 parsley-flutter-developer

**例子**:
```
Error: The method 'create' expects 2 arguments, but 3 are provided

Stage 3: 文件查詢
→ 新設計: Book.create() 簽名已變更
→ 文件記錄: v0.6.0 API 更新

Stage 4: 根因定位
→ 根因: 呼叫方未同步新簽名
→ 位置: 5 個檔案受影響

→ Ticket: Sync method calls with new Book.create() signature
→ Agent: parsley-flutter-developer
```

## 禁止行為

❌ **絕對禁止**:

1. **還沒做完六階段評估就分派修復**
   - 任何非語法錯誤都必須完成 Stage 1-4
   - 不存在「簡化評估」的情況（除語法錯誤外）

2. **非語法錯誤跳過 Ticket 開設**
   - 所有編譯錯誤、測試失敗、Analyzer 警告都必須開 Ticket
   - Ticket 是唯一的追蹤方式

3. **看到測試失敗就直接改測試（沒文件支持的情況下）**
   - 必須先進行 BDD 分析和文件查詢
   - 確認是程式問題還是測試過時

4. **進行大規模代碼重寫**
   - 修復應該是最小化精確修改
   - 如果發現需要大幅重寫，說明根因分析不足

5. **分派修復後不追蹤驗收結果**
   - Ticket 開設後必須追蹤完成狀態
   - 修復完成後驗證所有驗收條件

## 自動化觸發機制

### PostToolUse Hook

Hook 在以下情況自動觸發：

**1. Bash 命令執行失敗**
```bash
flutter test          # 失敗自動評估
dart analyze          # 失敗自動評估
dart run              # 失敗自動評估
```

**2. MCP Dart 工具失敗**
```
mcp__dart__run_tests  # 失敗自動評估
```

### Hook 輸出識別

**語法錯誤 (簡化流程)**:
```
🔧 語法錯誤 - 簡化修復流程

錯誤數量: N
推薦代理人: mint-format-specialist

直接執行精確修復，無需開 Ticket。
```

**其他錯誤 (強制評估)**:
```
🚨 修復前強制評估 - {ERROR_TYPE}

⚠️ 此錯誤類型 **必須開 Ticket** 追蹤，禁止直接分派修復！

執行以下步驟：
1️⃣ 完成六階段評估 (使用 /pre-fix-eval 重新啟動此流程)
2️⃣ 使用 /ticket-create 建立修復 Ticket
3️⃣ Ticket 建立後分派給專業代理人執行
```

## 錯誤模式識別參考

### SYNTAX_ERROR 模式 (6 種)

```
1. Expected.*?['\"]([;})\]])['\"]     - 缺少括號或分號
2. Unexpected\s+(?:end of|token)\b   - 意外 token
3. unterminated string literal         - 字串未結束
4. unexpected end of.*file             - 檔案不完整
5. missing comma                       - 缺少逗號
6. invalid number format               - 無效數字格式
```

### COMPILATION_ERROR 模式 (7 種)

```
1. (?:type|variable).*?can't be assigned        - 類型不匹配
2. is not a subtype of                          - 子型檢查失敗
3. Undefined\s+(?:name|class|function)          - 未定義名稱
4. Target of URI.*?doesn't exist                - 導入檔案不存在
5. (?:Class|Function|Method).*?not found        - 引用不存在
6. cannot find symbol                           - 符號未定義
7. incompatible types                           - 類型不相容
```

### TEST_FAILURE 模式 (4 種)

```
1. Expected:.*?Actual:                  - 斷言失敗
2. (\d+)\s+tests?\s+failed             - 失敗計數
3. FAILED                               - 失敗標記
4. AssertionError                       - 斷言例外
```

### ANALYZER_WARNING 模式 (3 種)

```
1. info\s*-.*?unused               - 未使用的警告
2. warning\s*-                     - lint 警告
3. deprecated\s+(?:function|class|method)  - 已棄用 API
```

## 修復品質檢查清單

修復完成後驗證：

- [ ] 測試 100% 通過 (沒有新增失敗)
- [ ] 修改範圍最小化 (只改必要部分)
- [ ] 沒有引入新的問題
- [ ] 與設計文件一致
- [ ] 代碼風格符合規範
- [ ] Ticket 已更新為完成狀態
- [ ] 相關的工作日誌已更新
- [ ] 其他模組無受影響

## Reference

### 相關方法論
- 🎯 [Atomic Ticket 方法論]($CLAUDE_PROJECT_DIR/.claude/methodologies/atomic-ticket-methodology.md)
- 📋 [Ticket 設計派工方法論]($CLAUDE_PROJECT_DIR/.claude/methodologies/ticket-design-dispatch-methodology.md)
- ♻️ [Ticket 生命週期管理方法論]($CLAUDE_PROJECT_DIR/.claude/methodologies/ticket-lifecycle-management-methodology.md)
- 🚀 [敏捷重構方法論]($CLAUDE_PROJECT_DIR/.claude/methodologies/agile-refactor-methodology.md)

### 技術文件
- 📁 [Pre-Fix Evaluation Hook 實作說明]($CLAUDE_PROJECT_DIR/.claude/hook-specs/pre-fix-evaluation-implementation.md)
- ✅ [Pre-Fix Evaluation 驗收報告]($CLAUDE_PROJECT_DIR/.claude/hook-specs/pre-fix-evaluation-acceptance-report.md)
- 📖 [快速參考卡片]($CLAUDE_PROJECT_DIR/.claude/quick-ref-pre-fix-eval.md)

### Hook 配置
- 📝 [Hook 系統方法論]($CLAUDE_PROJECT_DIR/.claude/methodologies/hook-system-methodology.md)
- ⚙️ [settings.json 配置文件]($CLAUDE_PROJECT_DIR/.claude/settings.json)

### 日誌位置
- 📊 評估結果: `.claude/hook-logs/pre-fix-evaluation-*.json`
- 🔍 執行日誌: `.claude/hook-logs/pre-fix-evaluation-hook.log`

## 常見問題

### Q: 語法錯誤可以直接分派嗎？
**A**: 是的。語法錯誤 (括號、分號等) Hook 會識別為 SYNTAX_ERROR，可以直接分派給 mint-format-specialist，無需開 Ticket。

### Q: 什麼情況下必須開 Ticket？
**A**: 所有非語法錯誤都必須開 Ticket，包括：
- 編譯錯誤
- 測試失敗
- Analyzer 警告

### Q: BDD 分析是否適用於所有錯誤？
**A**: BDD 分析主要用於理解測試意圖，但也可以應用於程式邏輯的業務意圖分析。語法錯誤可以跳過此階段。

### Q: 根因分析如果無法確定怎麼辦？
**A**: 如果 Stage 1-3 之後根因仍不清楚，應該在 Ticket 中記錄「根因待定」，並在分派時要求代理人協助深入分析。

### Q: 如何確認測試是否過時？
**A**: 檢查 `docs/app-requirements-spec.md` 和 `docs/work-logs/` 中的相關記錄，確認是否有新的需求變更或設計決策。

### Q: 修復後如何驗收？
**A**: 按照 Ticket 中的驗收條件逐項驗證，確保測試 100% 通過且無新增失敗。

## 快速開始

### 第一次使用

1. **執行測試或編譯**: `flutter test` 或 `dart analyze`
2. **等待 Hook 自動評估**: Hook 會自動分類錯誤
3. **根據 Hook 輸出決策**:
   - 語法錯誤 → 直接分派 mint-format-specialist
   - 其他錯誤 → 執行 `/pre-fix-eval` 開始評估

### 評估流程

1. 執行 `/pre-fix-eval` 啟動此 Skill
2. 按照六階段流程逐步分析
3. 使用 `/ticket-create` 建立 Ticket
4. 根據決策樹分派代理人

### 日常使用

- 每次測試失敗或編譯錯誤，都遵循此流程
- Hook 自動提示是否需要開 Ticket
- Ticket 成為修復的唯一記錄
- Ticket 完成後更新工作日誌

## 最佳實踐

✅ **做這些事**:
- 完成所有六階段評估再開始修復
- 使用 Ticket 記錄修復計劃
- 根據錯誤類型分派正確的代理人
- 修復後執行完整測試套件
- 檢查無新增失敗

❌ **不要做這些事**:
- 跳過評估流程
- 忽視「必須開 Ticket」的提示
- 修改測試作為修復方案
- 進行大規模重寫（應最小化修改）
- 直接分派非語法錯誤修復
