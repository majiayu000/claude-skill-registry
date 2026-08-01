---
name: doc-flow
description: 五重文件管理系統 - 專案文件運作的核心控制中心
---

# Doc-Flow SKILL

五重文件管理系統 - 專案文件運作的核心控制中心

## 核心理念

**每個文件有單一職責，工程師只需讀對應文件就能理解全部**

---

## 重要規範：禁用 Emoji

**所有五重文件系統中的文件禁止使用 emoji**

原因：
1. 交接文件需要專業、正式
2. emoji 在某些環境可能顯示不正確
3. Claude Code CLI 處理 markdown 表格中的 emoji 可能導致 Rust panic

適用範圍：
- CHANGELOG.md
- todolist.md
- worklog (docs/work-logs/)
- ticket (docs/work-logs/v*/tickets/)
- error-patterns (docs/error-patterns/)

---

## 五重文件系統

### 職責定義

| 文件 | 核心問題 | 職責定位 | 更新時機 |
|------|---------|---------|---------|
| **CHANGELOG** | "這個版本做了什麼改變？" | 版本推進變化（給工程師看） | 版本發布時 |
| **todo.md** | "還有哪些問題需要處理？" | 已知待處理問題（尚未排程） | 持續更新 |
| **worklog** | "這個版本要達成什麼目標？" | 版本企劃（大方向 + 策略） | 版本開始/結束 |
| **ticket** | "這個任務的執行細節是什麼？" | 任務執行歷程（細節記錄） | 執行過程中 |
| **error-patterns** | "之前遇過類似問題嗎？" | 經驗學習（查詢/更新） | 執行前後 |

### 關係圖

```
                    ┌─────────────────┐
                    │   CHANGELOG     │  ← 版本發布時自動更新
                    │  (版本間差異)    │
                    └────────┬────────┘
                             │ 提取
                    ┌────────┴────────┐
                    │    worklog      │  ← 版本企劃 + 目標
                    │   (大方向)       │
                    └────────┬────────┘
                             │ 索引
            ┌────────────────┼────────────────┐
            │                │                │
     ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐
     │   ticket    │  │   todo.md   │  │error-patterns│
     │ (執行細節)   │  │ (待處理問題) │  │ (經驗學習)   │
     └─────────────┘  └─────────────┘  └─────────────┘
```

---

## 職責詳解

### 1. CHANGELOG.md

**核心問題**：這個版本做了什麼改變？

**內容範圍**：
- 新增功能
- 架構變更
- Bug 修復
- 重大決策

**寫作風格**：
- 給其他工程師閱讀
- 簡潔、技術導向
- 按版本倒序排列

**更新時機**：版本發布時（由 `/version-release` 觸發）

**禁止內容**：
- 過度詳細的實作細節
- 開發過程中的嘗試錯誤
- 用戶不關心的內部變更

### 2. todo.md

**核心問題**：還有哪些問題需要處理？

**內容範圍**：
- 已知但尚未排程的問題
- 技術債務清單
- 未來版本的規劃項目

**寫作風格**：
- 清單形式
- 簡短描述
- 標記優先級或目標版本

**更新時機**：
- 發現新問題時新增
- 問題解決時**移除**（不是標記完成）
- 排入版本計畫時移至 worklog

**關鍵規則**：
- 已解決的問題必須移除
- 已排入執行的任務應在 worklog 中追蹤

### 3. worklog（版本企劃）

**核心問題**：這個版本要達成什麼目標？怎麼規劃？

**內容範圍**：
- 版本目標（一句話描述）
- 前情提要（為什麼需要這個版本）
- 執行策略（Step-by-Step）
- Ticket 總覽（連結到細節）
- Context 還原指引

**寫作風格**：
- 大方向、高層次
- 任何工程師不需其他 context 就能理解
- 執行細節**下沉到 ticket**

**更新時機**：
- 版本開始時建立
- 版本完成時更新狀態

**禁止內容**：
- 具體的程式碼變更
- 詳細的執行日誌
- 問題的完整分析過程（這些屬於 ticket）

### 4. ticket（任務執行細節）

**核心問題**：這個任務的完整執行歷程是什麼？

**內容範圍**：
- 任務來源和目標
- 5W1H 設計
- 問題分析
- 解決方案
- 測試結果
- 執行進度

**寫作風格**：
- 詳細、完整
- 記錄所有決策和變更
- 直到任務完成

**更新時機**：
- 任務建立時（/ticket-create）
- 執行過程中持續更新
- 完成時標記狀態

**格式**：Markdown + YAML Frontmatter

### 5. error-patterns（經驗學習）

**核心問題**：之前遇過類似問題嗎？

**內容範圍**：
- 錯誤症狀
- 根因分析
- 解決方案
- 預防措施
- 相關 Ticket

**寫作風格**：
- 模式化、可查詢
- 按類型分類
- 提供具體範例

**更新時機**：
- 執行 ticket 前查詢
- 發現新模式時新增
- 修復後補充預防措施

---

## 可用指令

### 狀態查詢

```bash
/doc-flow status                    # 查看五重文件系統整體狀態
/doc-flow check                     # 檢查文件一致性
```

### Worklog 管理

```bash
/doc-flow worklog init <version>    # 初始化新版本 worklog
/doc-flow worklog read <version>    # 讀取指定版本 worklog 摘要
/doc-flow worklog update            # 更新當前版本 worklog 狀態
```

### Todo 管理

```bash
/doc-flow todo list                 # 列出所有待處理問題
/doc-flow todo add <description>    # 新增待處理問題
/doc-flow todo resolve <id>         # 標記問題已解決（移除）
/doc-flow todo defer <id> <version> # 延遲到指定版本
```

### Changelog 管理

```bash
/doc-flow changelog preview         # 預覽即將發布的變更
/doc-flow changelog update          # 版本發布時更新
```

### Error Pattern 整合

```bash
/doc-flow learn                     # 觸發錯誤模式學習流程
```

---

## 工作流程整合

### 開始新版本

```
1. /doc-flow worklog init v0.26.0
   - 建立版本企劃
   - 定義目標和策略

2. /ticket-create
   - 建立具體任務 tickets
   - worklog 自動索引 tickets

3. 執行開發
   - 更新 ticket 進度
   - 查詢/新增 error-patterns
```

### 執行任務前

```
1. /doc-flow check
   - 確認文件同步狀態

2. /error-pattern query <關鍵字>
   - 查詢既有經驗

3. /ticket-track claim <ticket-id>
   - 開始執行任務
```

### 完成版本

```
1. /doc-flow worklog update
   - 更新版本狀態為完成

2. /doc-flow changelog preview
   - 預覽 CHANGELOG 更新

3. /version-release
   - 發布版本
   - 自動更新 CHANGELOG
```

---

## 與現有 SKILL 整合

| 現有 SKILL | 整合方式 |
|-----------|---------|
| `/ticket-create` | worklog 自動索引新建的 tickets |
| `/ticket-track` | 追蹤 ticket 狀態同步到 worklog |
| `/tech-debt-capture` | 捕獲的 TD 同步到 todo.md |
| `/version-release` | 發布時更新 CHANGELOG 和 worklog |
| `/error-pattern` | 經驗學習系統整合 |

---

## 檔案位置

```
docs/
├── CHANGELOG.md                     # 版本變更記錄
├── todolist.md                      # 待處理問題清單
├── error-patterns/                  # 錯誤模式知識庫
│   ├── README.md
│   └── categories/
└── work-logs/
    └── v{VERSION}/
        ├── v{VERSION}-main.md       # 版本企劃（大方向）
        └── tickets/                 # 執行細節
            ├── {version}-W1-001.md
            └── ...
```

---

## 設計原則

### 1. 職責單一化

每個文件回答一個核心問題，不重疊、不混淆。

### 2. 自給自足原則

讀 worklog 就能理解版本全貌，不需要額外 context。

### 3. 細節下沉原則

執行細節 → Ticket
大方向 → Worklog

### 4. 經驗累積原則

每次修復都查詢/更新 error-patterns，持續改善工作模式。

---

## 相關文件

- 方法論：`.claude/methodologies/five-document-system-methodology.md`
- 原有規範：`.claude/document-responsibilities.md`
- Worklog 模板：`.claude/skills/doc-flow/templates/worklog.md.template`
