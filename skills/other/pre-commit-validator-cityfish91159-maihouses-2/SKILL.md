---
name: pre-commit-validator
description: Git commit 前的完整驗證檢查。當用戶提到「commit」、「提交」、「push」或完成重要修改時自動執行。
allowed-tools: Bash, Grep, Read
---

# Pre-Commit Validator Skill

在 Git commit 前執行完整的代碼品質驗證，確保所有修改符合最高規格標準。

## 🎯 執行時機

- 用戶提到要「commit」或「提交代碼」
- 用戶提到要「push」到遠端
- 完成重要功能開發後
- 用戶明確要求「檢查」或「驗證」在提交前

## 📋 完整檢查清單

### 1. Git 狀態檢查

```bash
git status
```

確認：

- ✅ 有未提交的修改
- ✅ 在正確的分支上
- ✅ 沒有未追蹤的重要檔案被遺漏

### 2. TypeScript 類型檢查

```bash
npm run typecheck
```

**必須通過，無任何錯誤**

如果有錯誤：

1. 使用 `type-checker` skill 修復
2. 重新執行驗證
3. 不可跳過或忽略

### 3. ESLint 代碼風格檢查

```bash
npm run lint
```

**必須通過，無任何警告或錯誤**

如果有錯誤：

1. 優先使用自動修復: `npm run lint -- --fix`
2. 手動修復無法自動處理的問題
3. 重新執行驗證

### 4. 單元測試（如果有）

```bash
npm test
```

所有測試必須通過。

### 5. Build 構建檢查

```bash
npm run build
```

**必須成功構建，無任何錯誤**

這確保：

- 所有 import/export 正確
- 所有依賴可解析
- 生產環境代碼可用

### 6. 禁止模式搜尋

使用 Grep 搜尋絕對禁止出現的模式：

```bash
# 搜尋 console.log (僅在新修改的檔案中)
git diff --name-only | xargs grep -n "console\.log"

# 搜尋 debugger 語句
git diff --name-only | xargs grep -n "debugger"

# 搜尋 TODO/FIXME 標記
git diff --name-only | xargs grep -n "TODO\|FIXME"
```

如果發現：

- `console.log` → 必須移除或改用 logger
- `debugger` → 必須移除
- `TODO`/`FIXME` → 確認是否需要在此 commit 完成

### 7. 敏感資訊檢查

```bash
# 檢查是否包含 API keys, tokens, passwords
git diff --cached | grep -iE "(api[_-]?key|secret|password|token|credential)"
```

如果發現敏感資訊：

- 🚨 **立即停止 commit**
- 移除敏感資訊
- 使用環境變數或配置檔案

### 8. 檔案大小檢查

```bash
# 檢查是否有大檔案（>1MB）
git diff --cached --name-only | xargs ls -lh | awk '$5 ~ /M/ {print}'
```

大檔案應該：

- 圖片/媒體 → 使用 CDN 或壓縮
- 資料檔案 → 不應提交到 git

### 9. 相依性檢查

```bash
# 檢查 package.json 是否有變更
git diff --name-only | grep "package.json"
```

如果 `package.json` 有變更：

- 確認 `package-lock.json` 也有變更
- 執行 `npm install` 確保依賴正確

## 📝 驗證報告格式

```markdown
## Pre-Commit 驗證報告

### Git 狀態

- 分支: `feature/xxx`
- 修改檔案: 5 個
- 新增檔案: 2 個

### 驗證結果

✅ TypeScript 類型檢查通過
✅ ESLint 代碼風格檢查通過
✅ 單元測試通過 (12/12)
✅ Build 構建成功
✅ 無禁止模式
✅ 無敏感資訊
✅ 無異常大檔案
✅ 相依性正確

### 可以安全提交 ✅

建議 commit message:
```

feat: 實作用戶認證功能

- 新增 Login 組件
- 實作 JWT 驗證
- 加入錯誤處理

```

```

## 🚨 如果驗證失敗

```markdown
## Pre-Commit 驗證報告

### 驗證結果

❌ TypeScript 類型檢查失敗

- src/components/Login.tsx:42 - TS7006
- src/api/auth.ts:15 - TS2345

✅ ESLint 代碼風格檢查通過
⚠️ 發現 3 個 console.log

- src/utils/debug.ts:12
- src/components/Form.tsx:45
- src/hooks/useAuth.ts:88

### ⛔ 不可提交！

必須先修復以上問題。
```

**處理步驟：**

1. 使用相應的 skill 修復問題（如 `type-checker`）
2. 重新執行完整驗證
3. 直到所有檢查通過

## ⚠️ 絕對禁止

```bash
# ❌ 永遠不要這樣做
git commit --no-verify
git push --force
git commit -m "wip" # 沒有描述性的 message
```

## ✅ 最佳實踐

### Commit Message 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 類型：**

- `feat`: 新功能
- `fix`: 修復 bug
- `refactor`: 重構
- `docs`: 文檔
- `style`: 格式（不影響代碼運行）
- `test`: 測試
- `chore`: 構建過程或輔助工具變動

**範例：**

```
feat(auth): 實作 JWT 認證

- 新增 login API endpoint
- 實作 token 驗證 middleware
- 加入 refresh token 機制

Closes #123
```

## 🔄 完整 Commit 流程

```bash
# 1. 執行 pre-commit 驗證（使用此 skill）
# 2. 所有檢查通過後
git add .

# 3. 提交（使用描述性 message）
git commit -m "feat: 實作功能"

# 4. Push 前再次確認
git log -1 --stat

# 5. Push
git push origin branch-name
```

## 📊 檢查統計

完成驗證後，提供統計資訊：

```markdown
### 修改統計

- 修改: 8 檔案
- 新增: 245 行
- 刪除: 102 行
- 測試覆蓋率: 87%

### 品質指標

- TypeScript 錯誤: 0
- ESLint 警告: 0
- 測試通過率: 100%
- Build 時間: 12.3s
```

## 🎯 驗證標準

所有檢查必須 100% 通過，沒有例外。

**記住：寧可多花時間確保品質，也不要提交有問題的代碼。**
