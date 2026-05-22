---
source: ../../../../../skills/claude-code/tdd-assistant/SKILL.md
source_version: 1.0.0
translation_version: 1.0.0
last_synced: 2026-01-07
status: current
---

---
name: tdd-assistant
description: |
  Guide developers through Test-Driven Development workflow.
  Use when: writing tests first, practicing TDD, red-green-refactor cycle, BDD scenarios.
  Keywords: TDD, test first, red green refactor, FIRST, BDD, ATDD, 測試驅動開發, 紅綠重構.
---

# TDD 助手

> **語言**: [English](../../../../../skills/claude-code/tdd-assistant/SKILL.md) | 繁體中文

**版本**: 1.0.0
**最後更新**: 2026-01-07
**適用範圍**: Claude Code Skills

---

## 目的

此技能引導開發者完成測試驅動開發工作流程，協助他們：
- 撰寫有效的失敗測試（紅色階段）
- 實現最少程式碼讓測試通過（綠色階段）
- 在保持測試綠色的同時安全重構（重構階段）
- 識別並避免常見的 TDD 反模式
- 整合 TDD 與 BDD 和 ATDD 方法
- 根據情境適當地應用 TDD

---

## 快速參考

### TDD 循環檢查清單

```
┌─────────────────────────────────────────────────────────────────┐
│  🔴 紅色階段                                                     │
│  □ 測試描述預期行為，而非實作                                     │
│  □ 測試名稱清楚說明正在測試什麼                                   │
│  □ 測試遵循 AAA 模式（Arrange-Act-Assert）                       │
│  □ 測試因為「正確的原因」而失敗                                   │
│  □ 失敗訊息清楚且可操作                                          │
├─────────────────────────────────────────────────────────────────┤
│  🟢 綠色階段                                                     │
│  □ 撰寫「最少」程式碼讓測試通過                                   │
│  □ 「假裝」是可以接受的（如有需要可硬編碼）                        │
│  □ 不要優化或過度設計                                            │
│  □ 測試現在通過                                                  │
│  □ 所有其他測試仍然通過                                          │
├─────────────────────────────────────────────────────────────────┤
│  🔵 重構階段                                                     │
│  □ 消除重複（DRY）                                               │
│  □ 改善命名                                                      │
│  □ 如有需要提取方法                                              │
│  □ 「每次」變更後執行測試                                         │
│  □ 沒有新增功能                                                  │
│  □ 所有測試仍然通過                                              │
└─────────────────────────────────────────────────────────────────┘
```

### FIRST 原則快速參考

| 原則 | 檢查 | 常見違規 |
|------|------|---------|
| **F**ast（快速） | 每個單元測試 < 100ms | 資料庫呼叫、檔案 I/O、網路 |
| **I**ndependent（獨立） | 無共享狀態 | 靜態變數、執行順序依賴 |
| **R**epeatable（可重複） | 結果總是相同 | DateTime.Now、Random、外部服務 |
| **S**elf-validating（自我驗證） | 清楚的通過/失敗 | 手動檢查日誌、無斷言 |
| **T**imely（及時） | 程式碼之前測試 | 實現後才寫測試 |

### 反模式快速偵測

| 症狀 | 可能的反模式 | 快速修復 |
|------|-------------|---------|
| 重構時測試失敗 | 測試實作細節 | 只測試行為 |
| 測試通過但生產環境有 bug | 過度 mock | 新增整合測試 |
| 隨機測試失敗 | 測試相依性 | 隔離測試狀態 |
| 測試套件緩慢 | 整合測試太多 | 增加單元測試比例 |
| 團隊迴避寫測試 | 測試設置複雜 | 用建構器簡化 |

---

## TDD vs BDD vs ATDD 快速參考

| 面向 | TDD | BDD | ATDD |
|------|-----|-----|------|
| **誰撰寫** | 開發者 | 開發者 + BA + QA | 所有利益相關者 |
| **語言** | 程式碼 | Gherkin（Given-When-Then） | 業務語言 |
| **層級** | 單元/元件 | 功能/場景 | 驗收 |
| **時機** | 編碼期間 | 編碼之前 | Sprint 之前 |

### 何時使用哪個

```
是技術實作細節嗎？
├─ 是 → TDD
└─ 否 → 有業務利益相關者嗎？
         ├─ 是 → 利益相關者需要閱讀/驗證測試嗎？
         │        ├─ 是 → ATDD → BDD → TDD
         │        └─ 否 → BDD → TDD
         └─ 否 → TDD
```

---

## 工作流協助

### 紅色階段指導

撰寫失敗測試時，確保：

1. **清楚的意圖**
   ```typescript
   // ❌ 模糊
   test('it works', () => { ... });

   // ✅ 清楚
   test('should calculate discount when order total exceeds threshold', () => { ... });
   ```

2. **單一行為**
   ```typescript
   // ❌ 多個行為
   test('should validate and save user', () => { ... });

   // ✅ 單一行為
   test('should reject invalid email format', () => { ... });
   test('should save user with valid data', () => { ... });
   ```

3. **正確的斷言**
   ```typescript
   // ❌ 無斷言
   test('should process order', () => {
     orderService.process(order);
     // 缺少斷言！
   });

   // ✅ 清楚的斷言
   test('should mark order as processed', () => {
     const result = orderService.process(order);
     expect(result.status).toBe('processed');
   });
   ```

### 綠色階段指導

讓測試通過時，記住：

1. **最少實現**
   ```typescript
   // 測試：should return "FizzBuzz" for numbers divisible by both 3 and 5

   // ❌ 過度設計的第一次實現
   function fizzBuzz(n: number): string {
     const divisibleBy3 = n % 3 === 0;
     const divisibleBy5 = n % 5 === 0;
     if (divisibleBy3 && divisibleBy5) return 'FizzBuzz';
     if (divisibleBy3) return 'Fizz';
     if (divisibleBy5) return 'Buzz';
     return n.toString();
   }

   // ✅ 當前測試的最少實現（假裝！）
   function fizzBuzz(n: number): string {
     return 'FizzBuzz'; // 剛好足夠通過「這個」測試
   }
   ```

2. **漸進式泛化**
   - 第一個測試：硬編碼答案
   - 第二個測試：新增簡單條件
   - 第三個測試：泛化模式

### 重構階段指導

安全重構檢查清單：

```
之前：
□ 所有測試都是綠色
□ 理解程式碼在做什麼

期間（一次一個）：
□ 提取方法 → 執行測試
□ 重新命名 → 執行測試
□ 消除重複 → 執行測試
□ 簡化條件 → 執行測試

之後：
□ 所有測試仍然綠色
□ 程式碼更乾淨
□ 沒有新功能
```

---

## 與 SDD 整合

使用規格驅動開發時：

### Spec → 測試映射

| Spec 區段 | 測試類型 |
|----------|---------|
| 驗收標準 | 驗收測試（ATDD/BDD） |
| 業務規則 | 單元測試（TDD） |
| 邊界情況 | 單元測試（TDD） |
| 整合點 | 整合測試 |

### 工作流程

```
1. 閱讀 Spec (SPEC-XXX)
   ↓
2. 識別驗收標準
   ↓
3. 撰寫 BDD 場景（如適用）
   ↓
4. 對每個場景：
   ├─ TDD：紅 → 綠 → 重構
   └─ 標記 AC 為已實現
   ↓
5. 所有 AC 已實現？
   ├─ 是 → 標記 Spec 為完成
   └─ 否 → 返回步驟 4
```

### 測試文件參考

```typescript
/**
 * SPEC-001：使用者驗證 的測試
 *
 * 驗收標準：
 * - AC-1：使用者可以用有效憑證登入
 * - AC-2：無效密碼顯示錯誤
 * - AC-3：3 次失敗嘗試後帳號鎖定
 */
describe('使用者驗證 (SPEC-001)', () => {
  // 依 AC 組織測試
});
```

---

## 配置偵測

此技能支援專案特定配置。

### 偵測順序

1. 檢查 `CONTRIBUTING.md` 的「Disabled Skills」區段
   - 如果此技能在列表中，則對此專案停用
2. 檢查 `CONTRIBUTING.md` 的「TDD Standards」區段
3. 檢查程式碼庫中現有的測試模式
4. 如果未找到，**預設使用標準 TDD 實踐**

### 首次設置

如果未找到配置且情境不明確：

1. 詢問：「此專案尚未配置 TDD 偏好。您偏好哪種方法？」
   - 純 TDD（紅-綠-重構）
   - BDD 風格 TDD（Given-When-Then）
   - ATDD 搭配 BDD 和 TDD

2. 選擇後，建議在 `CONTRIBUTING.md` 中文件化：

```markdown
## TDD 標準

### 偏好方法
- 主要：TDD（紅-綠-重構）
- 對於有業務利益相關者的功能：BDD

### 測試命名慣例
- 模式：`should_[行為]_when_[條件]`
- 範例：`should_return_error_when_email_invalid`

### 覆蓋率目標
- 單元：80%
- 整合：60%
```

---

## 詳細指南

完整標準請參閱：
- [TDD 核心標準](../../../../../core/test-driven-development.md)
- [TDD 工作流程指南](./tdd-workflow.md)
- [語言範例](./language-examples.md)

相關測試標準：
- [測試標準](../../../../../core/testing-standards.md)
- [測試完整性維度](../../../../../core/test-completeness-dimensions.md)

---

## 相關標準

- [測試驅動開發](../../../../../core/test-driven-development.md) - TDD 核心標準
- [測試標準](../../../../../core/testing-standards.md) - 測試框架
- [測試完整性維度](../../../../../core/test-completeness-dimensions.md) - 7 維度
- [規格驅動開發](../../../../../core/spec-driven-development.md) - SDD 整合
- [測試指南技能](../testing-guide/SKILL.md) - 測試指南
- [測試覆蓋率助手](../test-coverage-assistant/SKILL.md) - 覆蓋率協助

---

## 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 1.0.0 | 2026-01-07 | 初始版本 |

---

## 授權

此技能依據 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權釋出。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
