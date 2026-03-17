---
name: pre-commit-check
description: 提交前檢查程式碼品質。此 Skill 由 /commit-session 和 /commit-all 自動引用。
---

# Pre-Commit 檢查規範

此文件定義 commit 前的檢查標準，由 `/commit-session` 和 `/commit-all` 指令自動引用。

---

## 檢查項目

### 1. Console 與 Alert 檢查

- [ ] 最少化 `console.xx` 系列指令
- [ ] 不應該有 `alert()` 指令

```typescript
// 可接受（開發除錯用）
if (import.meta.env.DEV) {
  console.log('debug info')
}

// 應避免
console.log('debug info')  // 正式環境不應出現
alert('message')           // 禁用
```

### 2. 註解檢查

#### 必須移除的註解類型：
- [ ] AI 更改說明（如「Claude 修改」）
- [ ] 更改後的差異說明
- [ ] 臨時開發註解（如「TODO」、「FIXME」、「測試用」）

#### 應保留的註解類型：
- [ ] 功能說明註解（解釋複雜邏輯）
- [ ] 重要警告註解

### 3. Import 檢查

- [ ] 所有 Vue API 明確導入
- [ ] 型別使用 `import type` 導入

### 4. ESLint 檢查（可選）

```bash
npm run lint
```

---

## Commit 訊息格式

```
<type>(<scope>): <主題>

- 要點 1
- 要點 2
```

### Type 選項

| Type | 說明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 錯誤修復 |
| `refactor` | 重構 |
| `docs` | 文件更新 |
| `style` | 樣式調整 |
| `chore` | 建置/工具 |

### 範例

```
feat(segment): 新增文字編輯功能

- 實作即時編輯 UI
- 新增儲存/取消按鈕
```

```
fix(search): 修復搜尋結果高亮問題

- 修正正則表達式匹配
```

---

## 注意事項

- 過程中**不執行** `npm run build`
- 僅執行 `npm run lint` 檢查
- 保持 commit 訊息簡潔，3-5 個要點為佳
