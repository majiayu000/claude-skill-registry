---
name: feature-development
description: 完整的功能開發流程，從規劃到部署，編排多個 Skills 協同工作。
---

---
name: feature-development
description: Complete feature development workflow orchestrating multiple skills from planning to deployment. Triggers: FD, 新功能, 開發功能, feature, implement, 實作, 實現, 建立功能, create feature, develop, 開發新, add feature, 加功能, 功能開發.
version: 1.0.0
category: workflow
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
orchestrates:
  - ddd-architect
  - test-generator
  - code-reviewer
  - memory-updater
  - git-precommit
allowed-tools:
  - read_file
  - write_file
  - create_file
  - create_directory
  - list_dir
  - grep_search
  - semantic_search
  - run_in_terminal
  - get_changed_files
---

# 功能開發工作流

## 描述

完整的功能開發流程，從規劃到部署，編排多個 Skills 協同工作。

## 觸發條件

- 「新功能開發」「implement feature」「建立新功能」
- 「FD: [功能名稱]」

---

## 📋 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│              Feature Development Workflow                    │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: 📐 規劃 (Planning)                                 │
│  ├─ 需求分析與確認                                           │
│  ├─ 識別影響範圍                                             │
│  └─ 更新 Memory Bank (activeContext)                        │
├─────────────────────────────────────────────────────────────┤
│  Phase 2: 🏗️ 架構 (Architecture)                            │
│  ├─ [ddd-architect] 生成 DDD 結構                           │
│  ├─ 建立介面定義                                             │
│  └─ 更新架構文檔                                             │
├─────────────────────────────────────────────────────────────┤
│  Phase 3: 🧪 測試先行 (TDD)                                  │
│  ├─ [test-generator] 生成測試框架                            │
│  ├─ 撰寫失敗的測試案例                                       │
│  └─ 定義驗收標準                                             │
├─────────────────────────────────────────────────────────────┤
│  Phase 4: 💻 實作 (Implementation)                          │
│  ├─ 實作 Domain 層                                          │
│  ├─ 實作 Application 層                                     │
│  ├─ 實作 Infrastructure 層                                  │
│  └─ 實作 Presentation 層                                    │
├─────────────────────────────────────────────────────────────┤
│  Phase 5: ✅ 驗證 (Verification)                            │
│  ├─ 執行測試套件                                             │
│  ├─ [code-reviewer] 程式碼審查                              │
│  ├─ [security-reviewer] 安全檢查                            │
│  └─ 靜態分析 (mypy, ruff, vulture)                          │
├─────────────────────────────────────────────────────────────┤
│  Phase 6: 📦 提交 (Commit)                                  │
│  ├─ [memory-updater] 更新 Memory Bank                       │
│  ├─ [git-precommit] 執行提交前檢查                          │
│  └─ 提交變更                                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 使用範例

### 基本用法

```
「新功能：用戶認證模組」

AI 執行：
1. 📐 確認需求：登入、註冊、密碼重設
2. 🏗️ 生成 DDD 結構 (Domain/Application/Infrastructure)
3. 🧪 生成測試框架
4. 💻 引導逐步實作
5. ✅ 執行驗證
6. 📦 準備提交
```

### 帶參數用法

```
「FD: Order 管理 --frontend React --backend Python」

AI 執行：
1. 生成後端 Python DDD 結構
2. 生成前端 React DDD 結構
3. 建立 API 契約
4. 生成前後端測試
```

---

## 📊 輸出格式

```markdown
## 🚀 功能開發報告

### 功能: 用戶認證模組

#### Phase 1: 規劃 ✅
- 需求: 登入、註冊、密碼重設
- 影響範圍: 5 個新檔案

#### Phase 2: 架構 ✅
- 建立 Domain/Entities/User.py
- 建立 Application/UseCases/AuthenticateUser.py
- 建立 Infrastructure/Repositories/UserRepository.py

#### Phase 3: 測試 ✅
- 單元測試: 12 個
- 整合測試: 5 個

#### Phase 4: 實作 🚧
- [x] Domain 層
- [x] Application 層
- [ ] Infrastructure 層
- [ ] Presentation 層

#### Phase 5: 驗證 ⏳
- 等待實作完成

#### Phase 6: 提交 ⏳
- 等待驗證通過

### 下一步
實作 Infrastructure 層的 UserRepository
```

---

## ⚙️ 配置選項

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--frontend` | 前端框架 (React/Vue/none) | none |
| `--backend` | 後端語言 (Python/Go/Rust) | Python |
| `--skip-tests` | 跳過測試生成 | false |
| `--quick` | 快速模式（跳過審查） | false |
