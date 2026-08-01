---
name: project-tester
description: 執行專案測試，分析測試結果和覆蓋率。
---

```markdown
---
name: project-tester
description: |
  Execute project tests and analyze coverage.
  LOAD THIS SKILL WHEN: User says "測試", "run tests", "執行測試", "跑測試" | before commits | checking code quality | CI failures.
  CAPABILITIES: Unit/Integration/E2E tests, coverage reports, failure analysis, Python pytest, Node.js npm test.
---

# 專案測試技能

## 描述
執行專案測試，分析測試結果和覆蓋率。

## 觸發條件
- 「執行測試」
- 「測試專案」
- 「run tests」
- Workflow 中的測試步驟

## 測試類型

### 1. 單元測試 (Unit Tests)
```bash
# Python
pytest tests/unit/ -v

# Node.js
npm run test:unit
```

### 2. 整合測試 (Integration Tests)
```bash
# Python
pytest tests/integration/ -v

# Node.js
npm run test:integration
```

### 3. 端對端測試 (E2E Tests)
```bash
# Python
pytest tests/e2e/ -v

# Node.js
npm run test:e2e
```

## 輸出格式
```
🧪 測試執行報告

═══════════════════════════════════════

📊 測試結果摘要

單元測試：    ✅ 45/45 通過 (100%)
整合測試：    ✅ 12/12 通過 (100%)
端對端測試：  ⚠️ 8/10 通過 (80%)

═══════════════════════════════════════

❌ 失敗的測試：

1. test_user_login_timeout
   位置：tests/e2e/test_auth.py:45
   錯誤：TimeoutError: Login exceeded 30s

2. test_api_rate_limit
   位置：tests/e2e/test_api.py:78
   錯誤：AssertionError: Expected 429, got 200

═══════════════════════════════════════

📈 覆蓋率報告

整體覆蓋率：78%

| 模組 | 行數 | 覆蓋率 |
|------|------|--------|
| auth | 245 | 92% ✅ |
| api  | 512 | 85% ✅ |
| core | 189 | 45% ⚠️ |

═══════════════════════════════════════

🔧 建議：
1. 修復 2 個失敗的 E2E 測試
2. 增加 core 模組的測試覆蓋
```

## 使用範例
```
「執行所有測試」
「只跑單元測試」
「測試並顯示覆蓋率」
```

```
