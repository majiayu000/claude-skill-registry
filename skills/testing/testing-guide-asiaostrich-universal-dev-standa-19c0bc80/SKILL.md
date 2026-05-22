---
source: skills/testing-guide/SKILL.md
source_version: 1.1.0
translation_version: 1.1.0
last_synced: 2025-12-29
status: current
name: testing
description: |
  Testing pyramid and test writing standards for UT/IT/ST/E2E.
  Supports ISTQB and Industry Pyramid frameworks.
  Use when: writing tests, discussing test coverage, test strategy, or test naming.
  Keywords: test, unit, integration, e2e, coverage, mock, ISTQB, SIT, 測試, 單元, 整合, 端對端.
---

# 測試指南

> **語言**: [English](../../../../skills/testing-guide/SKILL.md) | 繁體中文

**版本**: 1.1.0
**最後更新**: 2025-12-29
**適用範圍**: Claude Code Skills

---

## 目的

本 Skill 提供測試金字塔標準和系統化測試的最佳實踐，支援 ISTQB 和業界通行金字塔框架。

## 框架選擇

| 框架 | 層級 | 適用場景 |
|-----------|--------|----------|
| **ISTQB** | UT → IT/SIT → ST → AT/UAT | 企業級、合規性、正式 QA |
| **業界通行金字塔** | UT (70%) → IT (20%) → E2E (10%) | 敏捷、DevOps、CI/CD |

**整合測試縮寫說明：**
- **IT** (Integration Testing)：敏捷/DevOps 社群常用
- **SIT** (System Integration Testing)：企業/ISTQB 環境常用
- 兩者指的是相同的測試層級

## 快速參考

### 測試金字塔（業界標準）

```
              ┌─────────┐
              │   E2E   │  ← 10%（較少、較慢）
             ─┴─────────┴─
            ┌─────────────┐
            │   IT/SIT    │  ← 20%（整合測試）
           ─┴─────────────┴─
          ┌─────────────────┐
          │       UT        │  ← 70%（單元測試）
          └─────────────────┘
```

### 測試層級概覽

| 層級 | 範圍 | 速度 | 相依性 |
|-------|-------|-------|-------------|
| **UT** | 單一函式/類別 | < 100ms | Mock |
| **IT/SIT** | 元件互動 | 1-10秒 | 真實資料庫（容器化） |
| **ST** | 完整系統（ISTQB） | 分鐘級 | 類生產環境 |
| **E2E** | 使用者旅程 | 30秒+ | 所有真實環境 |
| **AT/UAT** | 業務驗證（ISTQB） | 視情況 | 所有真實環境 |

### 覆蓋率目標

| 指標 | 最低要求 | 建議值 |
|--------|---------|-------------|
| 行覆蓋率 | 70% | 85% |
| 分支覆蓋率 | 60% | 80% |
| 函式覆蓋率 | 80% | 90% |

## 詳細指南

完整標準請參考：
- [測試金字塔](./testing-pyramid.md)

### AI 優化格式（Token 高效）

供 AI 助理使用，請採用 YAML 格式檔案以減少 Token 使用量：
- 基礎標準：`ai/standards/testing.ai.yaml`
- 框架選項：
  - ISTQB 框架：`ai/options/testing/istqb-framework.ai.yaml`
  - 業界通行金字塔：`ai/options/testing/industry-pyramid.ai.yaml`
- 測試層級選項：
  - 單元測試：`ai/options/testing/unit-testing.ai.yaml`
  - 整合測試：`ai/options/testing/integration-testing.ai.yaml`
  - 系統測試：`ai/options/testing/system-testing.ai.yaml`
  - E2E 測試：`ai/options/testing/e2e-testing.ai.yaml`

## 命名慣例

### 檔案命名

```
[ClassName]Tests.cs       # C#
[ClassName].test.ts       # TypeScript
[class_name]_test.py      # Python
[class_name]_test.go      # Go
```

### 方法命名

```
[MethodName]_[Scenario]_[ExpectedResult]()
should_[behavior]_when_[condition]()
test_[method]_[scenario]_[expected]()
```

## 測試替身

| 類型 | 用途 | 使用時機 |
|------|---------|-------------|
| **Stub** | 回傳預定義值 | 固定 API 回應 |
| **Mock** | 驗證互動 | 檢查方法是否被呼叫 |
| **Fake** | 簡化實作 | 記憶體資料庫 |
| **Spy** | 記錄呼叫、委派 | 部分 Mock |

### 何時使用

- **UT**: 對所有外部相依使用 mock/stub
- **IT**: 資料庫使用 fake，外部 API 使用 stub
- **ST**: 真實元件，僅對外部服務使用 fake
- **E2E**: 全部使用真實環境

## AAA 模式

```typescript
test('method_scenario_expected', () => {
    // Arrange - 設定測試資料
    const input = createTestInput();
    const sut = new SystemUnderTest();

    // Act - 執行行為
    const result = sut.execute(input);

    // Assert - 驗證結果
    expect(result).toBe(expected);
});
```

## FIRST 原則

- **F**ast（快速） - 測試執行快速
- **I**ndependent（獨立） - 測試之間不互相影響
- **R**epeatable（可重複） - 每次執行結果相同
- **S**elf-validating（自我驗證） - 明確的通過/失敗
- **T**imely（及時） - 與產品代碼一起撰寫

## 應避免的反模式

- ❌ 測試相依（測試必須按順序執行）
- ❌ 不穩定測試（有時通過、有時失敗）
- ❌ 測試實作細節
- ❌ 過度 Mock
- ❌ 缺少斷言
- ❌ 魔術數字/字串

---

## 設定偵測

本 Skill 支援專案特定設定。

### 偵測順序

1. 檢查 `CONTRIBUTING.md` 的「停用 Skills」區段
   - 如果列出此 Skill，則為該專案停用
2. 檢查 `CONTRIBUTING.md` 的「測試標準」區段
3. 若未找到，**預設使用標準覆蓋率目標**

### 首次設定

若未找到設定且上下文不清楚時：

1. 詢問使用者：「此專案尚未設定測試標準。您想要自訂覆蓋率目標嗎？」
2. 使用者選擇後，建議在 `CONTRIBUTING.md` 中記錄：

```markdown
## Testing Standards

### Coverage Targets
| Metric | Target |
|--------|--------|
| Line | 80% |
| Branch | 70% |
| Function | 85% |
```

### 設定範例

在專案的 `CONTRIBUTING.md` 中：

```markdown
## Testing Standards

### Coverage Targets
| Metric | Target |
|--------|--------|
| Line | 80% |
| Branch | 70% |
| Function | 85% |

### Testing Framework
- Unit Tests: Jest
- Integration Tests: Supertest
- E2E Tests: Playwright
```

---

## 相關標準

- [測試標準](../../core/testing-standards.md)
- [程式碼審查檢查清單](../../core/code-review-checklist.md)

---

## 版本歷史

| 版本 | 日期 | 變更內容 |
|---------|------|---------|
| 1.1.0 | 2025-12-29 | 新增：框架選擇（ISTQB/業界通行金字塔）、IT/SIT 縮寫說明 |
| 1.0.0 | 2025-12-24 | 新增：標準區段（目的、相關標準、版本歷史、授權） |

---

## 授權

本 Skill 以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權發布。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
