---
name: rigorous_testing
description: |
  嚴格測試協議。強制執行「如果沒測試，就不算完成」原則。

  觸發時機：
  - 修復 bug 時（必須新增回歸測試）
  - 實作新功能時（必須有對應測試）
  - 修改現有代碼時（確保測試仍通過）
  - 用戶提到「測試」、「test」、「驗證功能」

allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
---

# Rigorous Testing Protocol

## 1. 黃金法則

**「如果沒測試，就不算完成。」**

- 永遠不要假設修改有效而不跑測試
- 如果現有測試失敗，修復代碼而非修改測試（除非測試本身過時）
- 每個 bug 修復必須有回歸測試

---

## 2. 測試時機

### 修改前（建立基準）

```bash
# 跑相關測試檔案，確認當前狀態
npm run test <相關檔案>
```

### 開發中（TDD 循環）

```
RED    → 先寫失敗的測試
GREEN  → 寫最少代碼讓測試通過
REFACTOR → 優化代碼，保持測試通過
```

### 修改後（確保無回歸）

```bash
# 跑完整測試套件
npm test
```

---

## 3. MaiHouses 測試堆疊

### 單元測試 (Vitest)

- **用途**: 工具函數、hooks、獨立組件
- **Mock**: 使用 `vi.mock` 模擬 API
- **路徑**: `src/**/__tests__/*.test.ts`

```typescript
// 範例
import { describe, it, expect, vi } from 'vitest';

describe('功能名稱', () => {
  it('應該正確處理某情況', () => {
    // Arrange
    const input = 'test';

    // Act
    const result = myFunction(input);

    // Assert
    expect(result).toBe('expected');
  });
});
```

### 整合測試 (API)

- **用途**: Backend 邏輯 (`api/` 目錄)
- **Mock**: 使用 `node-mocks-http` 模擬 Request/Response
- **路徑**: `api/**/__tests__/*.test.ts`

### E2E 測試 (Playwright)

- **用途**: 關鍵用戶流程（登入、發文等）
- **路徑**: `tests/e2e/*.spec.ts`

---

## 4. 必做檢查清單

### 每次修改後

- [ ] 跑過相關測試檔案？
- [ ] 所有測試通過？
- [ ] 如果修復 bug，有新增回歸測試？
- [ ] TypeScript 類型檢查通過？ (`npm run typecheck`)

### 提交前

- [ ] 完整測試套件通過？ (`npm test`)
- [ ] 無跳過的測試？
- [ ] 測試覆蓋新增的代碼？

---

## 5. 測試命名規範

```typescript
describe('模組/組件名稱', () => {
  describe('功能分類', () => {
    it('應該 [預期行為] 當 [條件]', () => {
      // ...
    });
  });
});

// 範例
describe('useComments', () => {
  describe('toggleLike', () => {
    it('應該正確切換按讚狀態當用戶點擊', () => {
      // ...
    });

    it('應該回滾狀態當 API 失敗', () => {
      // ...
    });
  });
});
```

---

## 6. 常見測試模式

### Mock API 呼叫

```typescript
vi.mock('../lib/supabase', () => ({
  supabase: {
    from: vi.fn(() => ({
      select: vi.fn(() => ({
        eq: vi.fn(() => Promise.resolve({ data: [], error: null })),
      })),
    })),
  },
}));
```

### Mock Hook

```typescript
vi.mock('../hooks/useAuth', () => ({
  useAuth: () => ({
    user: { id: 'test-user' },
    isLoggedIn: true,
  }),
}));
```

### 測試異步操作

```typescript
it('應該處理異步操作', async () => {
  const { result } = renderHook(() => useMyHook());

  await act(async () => {
    await result.current.asyncAction();
  });

  expect(result.current.state).toBe('expected');
});
```

### 測試錯誤情況

```typescript
it('應該正確處理錯誤', async () => {
  // Mock API 返回錯誤
  vi.mocked(fetch).mockRejectedValueOnce(new Error('Network error'));

  const { result } = renderHook(() => useMyHook());

  await act(async () => {
    await result.current.action();
  });

  expect(result.current.error).toBe('Network error');
});
```

---

## 7. 故障排除

### 測試掛起

- 檢查未關閉的 handles 或 DB 連線
- 確認所有 Promise 都有 await

### 測試不穩定 (Flaky)

- 檢查 async/await 問題
- 檢查共享狀態
- 使用 `waitFor` 等待異步更新

### Mock 不生效

- 確認 mock 在 import 之前
- 檢查 mock 路徑是否正確
- 使用 `vi.clearAllMocks()` 在 `beforeEach`

---

## 8. 測試指令速查

```bash
# 執行所有測試
npm test

# 執行單一檔案
npx vitest run src/path/to/file.test.ts

# 監視模式
npm run test:watch

# 查看覆蓋率
npx vitest run --coverage

# 只跑符合名稱的測試
npx vitest run -t "測試名稱關鍵字"
```

---

## 9. 與其他 Skills 整合

| 階段     | 整合 Skill              | 說明             |
| -------- | ----------------------- | ---------------- |
| 測試前   | `/read-before-edit`     | 先讀懂現有測試   |
| 寫測試   | `/code-validator`       | 確保測試代碼品質 |
| 測試失敗 | `/type-checker`         | 修復類型問題     |
| 提交前   | `/pre-commit-validator` | 確保所有測試通過 |

---

## 10. 記住

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   🧪 沒有測試的代碼 = 不存在的代碼                              │
│                                                                 │
│   ✅ 測試通過 ≠ 代碼正確（但至少有基本保障）                    │
│                                                                 │
│   🔄 測試失敗 → 修復代碼，不是刪除測試                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
