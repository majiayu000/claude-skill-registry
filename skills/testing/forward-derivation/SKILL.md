---
name: forward-derivation
description: |
  從已批准的 SDD 規格推演 BDD 場景、TDD 測試骨架和 ATDD 驗收測試。
  使用時機：規格已批准、開始 BDD/TDD 實作、生成測試結構。
  關鍵字：forward derivation, spec to test, BDD generation, TDD skeleton, test derivation, 正向推演, 規格轉測試, 測試生成。
source: ../../../../../skills/claude-code/forward-derivation/SKILL.md
source_version: 1.0.0
translation_version: 1.0.0
last_synced: 2026-01-19
status: current
---

# 正向推演指南

> **語言**: [English](../../../../../skills/claude-code/forward-derivation/SKILL.md) | 繁體中文

**版本**: 1.0.0
**最後更新**: 2026-01-19
**適用範圍**: Claude Code Skills

> **核心規範**：此技能實作[正向推演標準](../../../core/forward-derivation-standards.md)。任何 AI 工具皆可參考核心規範取得完整方法論文件。

---

## 目的

此技能引導您從已批准的 SDD 規格推演 BDD 場景、TDD 測試骨架和 ATDD 驗收測試，並嚴格遵循反幻覺標準。

正向推演是[反向工程](../reverse-engineer/SKILL.md)的對稱對應：
- **反向工程**：程式碼 → 規格
- **正向推演**：規格 → 測試

## 快速參考

### 正向推演工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                      正向推演工作流程                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  SPEC 解析（AI 自動化）                                    │
│      ├─ 讀取已批准的規格                                        │
│      ├─ 提取驗收條件（GWT 或條列式）                            │
│      └─ 驗證 SPEC 結構和完整性                                  │
│                                                                 │
│  2️⃣  推演（AI 自動化）                                         │
│      ├─ AC → BDD Gherkin 場景                                  │
│      ├─ AC → TDD 測試骨架（帶 TODO）                           │
│      └─ AC → ATDD 驗收測試表格                                 │
│                                                                 │
│  3️⃣  人類審查（必要）                                          │
│      ├─ 驗證生成的場景符合 AC 意圖                              │
│      ├─ 填寫 [TODO] 區塊                                       │
│      └─ 如需要精煉步驟定義                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 命令概覽

| 命令 | 輸入 | 輸出 | 目的 |
|------|------|------|------|
| `/derive-bdd` | SPEC-XXX.md | .feature | AC → Gherkin 場景 |
| `/derive-tdd` | SPEC-XXX.md | .test.ts | AC → 測試骨架 |
| `/derive-atdd` | SPEC-XXX.md | acceptance.md | AC → 驗收測試表格 |
| `/derive-all` | SPEC-XXX.md | 以上全部 | 完整推演管道 |

## 核心原則

### 1. 規格限定生成

**關鍵**：只推演規格中存在的內容。不添加 AC 未明確定義的場景、測試或功能。

```
# 反幻覺規則
輸入：SPEC 有 N 個驗收條件
輸出：恰好 N 個場景（BDD）
      恰好 N 個測試群組（TDD）
      恰好 N 個驗收測試（ATDD）

若任何輸出數量 ≠ 輸入數量 → 違規
```

### 2. 來源標註

每個生成項目必須包含可追溯性：

```gherkin
# Generated from: specs/SPEC-001.md
# AC: AC-1

@SPEC-001 @AC-1
Scenario: 使用者以有效憑證登入
```

### 3. 確定性標籤

| 標籤 | 使用時機 | 範例 |
|------|----------|------|
| `[來源]` | 直接來自 SPEC 的內容 | 功能標題、AC 文字 |
| `[推演]` | 從 SPEC 內容轉換 | 從條列 AC 推演的 GWT |
| `[生成]` | AI 生成的結構 | 測試骨架 |
| `[TODO]` | 需要人類實作 | 斷言、步驟定義 |

## 工作流程階段

### 階段 1：SPEC 解析

**輸入**：已批准的規格檔案
**輸出**：結構化的驗收條件列表

**動作**：
1. 讀取規格檔案
2. 識別驗收條件區塊
3. 解析 AC 格式（Given-When-Then 或條列式）
4. 驗證 AC 完整性

**驗證清單**：
- [ ] SPEC 狀態為「已批准」或「就緒」
- [ ] 驗收條件區塊存在
- [ ] 每個 AC 有唯一識別碼（AC-1、AC-2 等）
- [ ] AC 格式可解析（GWT 或條列式）

### 階段 2：BDD 推演

**輸入**：已解析的驗收條件
**輸出**：Gherkin .feature 檔案

**轉換規則**：

| AC 格式 | 轉換 |
|---------|------|
| Given-When-Then | 直接對應到 Gherkin |
| 條列式 | 使用 GWT 模式匹配轉換 |
| 勾選清單 | 條件 → Given、動作 → When、結果 → Then |

### 階段 3：TDD 推演

**輸入**：已解析的驗收條件
**輸出**：測試骨架檔案

**參數**：
| 參數 | 選項 | 預設值 |
|------|------|--------|
| `--lang` | typescript, javascript, python, java, go | typescript |
| `--framework` | vitest, jest, pytest, junit, go-test | vitest |

### 階段 4：ATDD 推演

**輸入**：已解析的驗收條件
**輸出**：驗收測試表格文件

### 階段 5：人類審查

**輸入**：生成的檔案
**輸出**：審查和精煉的檔案

**審查清單**：
- [ ] 生成的場景符合 AC 意圖
- [ ] 沒有超出 AC 數量的額外場景
- [ ] 來源標註正確
- [ ] [TODO] 區塊已識別供實作
- [ ] 步驟語言為業務層級（非技術層級）

## 輸出格式

### BDD Feature 檔案

```gherkin
# Generated from: specs/SPEC-001.md
# Generator: /derive-bdd v1.0.0
# Generated at: 2026-01-19T10:00:00Z

@SPEC-001
Feature: 使用者認證
  [來源] 來自 SPEC-001 摘要

  @AC-1 @happy-path
  Scenario: 使用者以有效憑證登入
    # [來源] 來自 SPEC-001 AC-1
    Given 已註冊的使用者有有效憑證
    When 使用者提交登入表單
    Then 使用者被導向儀表板

  @AC-2 @error-handling
  Scenario: 無效憑證登入失敗
    # [來源] 來自 SPEC-001 AC-2
    Given 使用者有無效憑證
    When 使用者提交登入表單
    Then 顯示錯誤訊息
```

### TDD 測試骨架

```typescript
/**
 * Tests for SPEC-001: 使用者認證
 * Generated from: specs/SPEC-001.md
 * Generated at: 2026-01-19T10:00:00Z
 * AC Coverage: AC-1, AC-2
 */

describe('SPEC-001: 使用者認證', () => {
  describe('AC-1: 使用者以有效憑證登入', () => {
    it('should redirect to dashboard on successful login', async () => {
      // Arrange
      // [TODO] 設定已註冊使用者和有效憑證

      // Act
      // [TODO] 提交登入表單

      // Assert
      // [TODO] 驗證導向儀表板
      expect(true).toBe(true); // Placeholder
    });
  });
});
```

### ATDD 驗收測試表格

```markdown
# SPEC-001 驗收測試

**規格**: SPEC-001
**生成時間**: 2026-01-19
**狀態**: 待審查

## AT-001: 使用者以有效憑證登入
**來源**: AC-1

| 步驟 | 動作 | 預期結果 | 通過/失敗 |
|------|------|----------|-----------|
| 1 | 導航到登入頁面 | 顯示登入表單 | [ ] |
| 2 | 輸入有效憑證 | 欄位接受輸入 | [ ] |
| 3 | 點擊登入 | 表單已提交 | [ ] |
| 4 | 驗證導向 | 顯示儀表板 | [ ] |

**測試人員**: _______________
**日期**: _______________
**結果**: [ ] 通過 / [ ] 失敗
```

## 與其他技能的整合

### 與 /spec（規格驅動開發）

1. 使用 `/spec` 工作流程完成 SPEC
2. 透過審查獲得 SPEC 批准
3. 執行 `/derive-all` 生成測試結構
4. 在 BDD/TDD 工作流程中使用生成的輸出

### 與 /bdd（行為驅動開發）

1. 使用 `/derive-bdd` 生成 BDD 場景
2. 與利害關係人審查和精煉場景
3. 使用 `/bdd` 繼續 BDD 制定
4. 實作步驟定義

### 與 /tdd（測試驅動開發）

1. 使用 `/derive-tdd` 生成 TDD 骨架
2. 填寫 [TODO] 區塊的實際斷言
3. 以生成的測試結構進入 TDD 紅燈階段
4. 實作程式碼使測試通過

### 與整合流程

正向推演適合整合流程方法論：

```
spec-review (已批准) → forward-derivation → discovery (BDD)
                              │
                              ├─→ .feature 檔案供 BDD
                              ├─→ .test.ts 骨架供 TDD
                              └─→ acceptance.md 供 ATDD
```

## 完整推演管道

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         完整正向推演管道                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   已批准 SPEC                                                            │
│        │                                                                │
│        ▼                                                                │
│   /derive-all specs/SPEC-XXX.md                                        │
│        │                                                                │
│        ├─→ /derive-bdd                                                  │
│        │    └─→ features/SPEC-XXX.feature                              │
│        │                                                                │
│        ├─→ /derive-tdd                                                  │
│        │    └─→ tests/SPEC-XXX.test.ts                                 │
│        │                                                                │
│        └─→ /derive-atdd                                                 │
│             └─→ acceptance/SPEC-XXX-acceptance.md                      │
│                                                                         │
│   人類審查                                                               │
│        │                                                                │
│        ├─→ 驗證 1:1 AC 對應                                             │
│        ├─→ 填寫 [TODO] 區塊                                             │
│        └─→ 精煉步驟定義                                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 使用範例

```bash
# 生成 BDD 場景
/derive-bdd specs/SPEC-001.md

# 使用 Python/pytest 生成 TDD 骨架
/derive-tdd specs/SPEC-001.md --lang python --framework pytest

# 生成所有測試結構
/derive-all specs/SPEC-001.md

# 預覽不建立檔案
/derive-all specs/SPEC-001.md --dry-run

# 指定輸出目錄
/derive-all specs/SPEC-001.md --output-dir ./generated
```

## 應避免的反模式

### ❌ 不要這樣做

1. **添加額外場景**
   - 錯誤：SPEC 有 3 個 AC，生成 5 個場景
   - 正確：SPEC 有 3 個 AC，恰好生成 3 個場景

2. **從草稿 SPEC 推演**
   - 錯誤：對未批准的規格執行 `/derive-all`
   - 正確：只從已批准的規格推演

3. **跳過來源標註**
   - 錯誤：沒有 @SPEC-XXX 標籤的場景
   - 正確：每個場景標記來源 SPEC 和 AC

4. **過度指定技術細節**
   - 錯誤：`Given 使用 PostgreSQL 驅動程式建立資料庫連線`
   - 正確：`Given 系統中存在使用者資料`

5. **將骨架視為完整**
   - 錯誤：不填寫 [TODO] 就使用生成的測試
   - 正確：執行測試前填寫所有 [TODO] 區塊

## 最佳實踐

### 應該做的

- ✅ 只從已批准的規格推演
- ✅ 維持嚴格的 1:1 AC 到輸出對應
- ✅ 在所有輸出中包含來源標註
- ✅ 使用 [TODO] 標記實作區塊
- ✅ 與利害關係人審查生成的輸出
- ✅ 保持步驟語言在業務層級

### 不應該做的

- ❌ 添加 AC 未定義的場景
- ❌ 從草稿或未批准的規格推演
- ❌ 跳過對生成輸出的人類審查
- ❌ 將生成的骨架視為完整測試
- ❌ 移除來源標註註解
- ❌ 過度指定實作細節

---

## 設定偵測

此技能會自動偵測專案設定：

1. 檢查現有的 `specs/` 目錄結構
2. 從 package.json/pyproject.toml 偵測測試框架
3. 識別偏好的輸出目錄
4. 設定語言特定範本

---

## 相關規範

- [正向推演標準](../../../core/forward-derivation-standards.md) - **核心方法論規範（主要參考）**
- [反向工程標準](../../../core/reverse-engineering-standards.md) - 對稱對應
- [規格驅動開發](../../../core/spec-driven-development.md) - 輸入規格格式
- [行為驅動開發](../../../core/behavior-driven-development.md) - BDD 輸出格式
- [測試驅動開發](../../../core/test-driven-development.md) - TDD 輸出用法
- [反幻覺指南](../../../core/anti-hallucination.md) - 生成合規

---

## 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 1.0.0 | 2026-01-19 | 初始發布 |

---

## 授權

此技能採用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
