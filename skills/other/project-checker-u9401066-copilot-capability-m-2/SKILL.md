```markdown
---
name: project-checker
description: |
  Comprehensive project health check for documentation, architecture, and code quality.
  LOAD THIS SKILL WHEN: User says "檢查專案", "project check", "專案狀態" | before releases | reviewing project health | onboarding new contributors.
  CHECKS: File completeness (README, CHANGELOG, LICENSE), Memory Bank status, DDD compliance, test coverage, Git status.
---

# 專案檢查技能

## 描述
全面檢查專案狀態，包含文件完整性、架構合規性、測試覆蓋等。

## 觸發條件
- 「檢查專案」
- 「專案狀態」
- 「project check」
- Workflow 中的檢查步驟

## 檢查項目

### 1. 文件完整性
- [ ] README.md 存在且完整
- [ ] CHANGELOG.md 更新
- [ ] LICENSE 存在
- [ ] .gitignore 設定正確
- [ ] pyproject.toml / package.json 存在

### 2. Memory Bank 狀態
- [ ] activeContext.md 更新
- [ ] progress.md 反映當前狀態
- [ ] decisionLog.md 記錄完整

### 3. 架構合規性
- [ ] 遵循 DDD 原則
- [ ] DAL 獨立
- [ ] 依賴方向正確

### 4. 程式碼品質
- [ ] 無明顯語法錯誤
- [ ] Lint 檢查通過
- [ ] 測試存在且通過

### 5. Git 狀態
- [ ] 無未追蹤重要檔案
- [ ] 無未提交變更
- [ ] 分支狀態正確

## 輸出格式
```
🔍 專案檢查報告

📁 專案：[專案名稱]
📅 檢查時間：[時間]

═══════════════════════════════════════

📋 文件完整性         [8/10] ⚠️
   ✅ README.md
   ✅ CHANGELOG.md
   ❌ API.md 缺失
   ⚠️ README 缺少安裝說明

🏗️ 架構合規性         [10/10] ✅
   ✅ DDD 結構正確
   ✅ DAL 獨立
   ✅ 依賴方向正確

🧪 測試覆蓋           [6/10] ⚠️
   ⚠️ 覆蓋率 60%
   ❌ 缺少 E2E 測試

📝 Memory Bank        [10/10] ✅
   ✅ 全部更新

🔧 Git 狀態           [8/10] ⚠️
   ⚠️ 3 個未提交變更
   ✅ 分支狀態正常

═══════════════════════════════════════

📊 整體評分：42/50 (84%) - 良好

🔧 建議修正：
1. 新增 API.md 文檔
2. 補充 README 安裝說明
3. 提高測試覆蓋率
4. 提交待處理變更
```

## 使用範例
```
「檢查專案狀態」
「project check」
「快速檢查」 -- 只檢查必要項目
```

```
