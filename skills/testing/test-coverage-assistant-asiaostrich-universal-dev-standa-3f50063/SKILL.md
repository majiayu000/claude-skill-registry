---
name: coverage
description: |
  使用 8 維度框架評估測試完整性。
  使用時機：撰寫測試、審查測試覆蓋率、確保測試品質。
  關鍵字：test coverage, completeness, dimensions, 8 dimensions, test quality, 測試覆蓋, 測試完整性, 八維度。
source: ../../../../skills/test-coverage-assistant/SKILL.md
source_version: 1.1.0
translation_version: 1.1.0
last_synced: 2026-01-25
status: current
---

# 測試覆蓋助手

> **語言**: [English](../../../../skills/test-coverage-assistant/SKILL.md) | 繁體中文

**版本**: 1.1.0
**最後更新**: 2026-01-25
**適用範圍**: Claude Code Skills

---

## 目的

此技能使用 8 維度框架幫助評估和改善測試完整性，確保每個功能都有全面的測試覆蓋。

## 快速參考

### 8 個維度

```
┌─────────────────────────────────────────────────────────────┐
│              測試完整性 = 8 個維度                            │
├─────────────────────────────────────────────────────────────┤
│  1. 正常路徑        正常預期行為                              │
│  2. 邊界條件        最小/最大值、限制                         │
│  3. 錯誤處理        無效輸入、例外狀況                        │
│  4. 授權驗證        角色存取控制                              │
│  5. 狀態變更        前後狀態驗證                              │
│  6. 驗證邏輯        格式、商業規則                            │
│  7. 整合測試        真實查詢驗證                              │
│  8. AI 生成品質     AI 生成測試的品質 (新增)                │
└─────────────────────────────────────────────────────────────┘
```

### 維度摘要表

| # | 維度 | 測試內容 | 關鍵問題 |
|---|------|----------|----------|
| 1 | **正常路徑** | 有效輸入 → 預期輸出 | 正常流程是否運作？ |
| 2 | **邊界條件** | 最小/最大值、限制 | 邊界情況會發生什麼？ |
| 3 | **錯誤處理** | 無效輸入、找不到資料 | 錯誤如何處理？ |
| 4 | **授權驗證** | 角色權限 | 誰可以做什麼？ |
| 5 | **狀態變更** | 前後狀態驗證 | 狀態是否正確變更？ |
| 6 | **驗證邏輯** | 格式、商業規則 | 輸入是否有驗證？ |
| 7 | **整合測試** | 真實 DB/API 呼叫 | 查詢真的有效嗎？ |
| 8 | **AI 生成品質** | AI 生成測試的品質 | AI 測試是否有意義？ |

### 各功能類型需要的維度

| 功能類型 | 需要的維度 |
|----------|------------|
| CRUD API | 1, 2, 3, 4, 6, 7, 8* |
| 查詢/搜尋 | 1, 2, 3, 4, 7, 8* |
| 狀態機 | 1, 3, 4, 5, 6, 8* |
| 驗證邏輯 | 1, 2, 3, 6, 8* |
| 背景作業 | 1, 3, 5, 8* |
| 外部整合 | 1, 3, 7, 8* |

*維度 8 (AI 生成品質) 適用於 AI 生成的測試

## 測試設計檢查清單

為每個功能使用此檢查清單：

```
功能：___________________

□ 正常路徑
  □ 有效輸入產生預期成功
  □ 正確的資料被回傳/建立
  □ 預期的副作用發生

□ 邊界條件
  □ 最小有效值
  □ 最大有效值
  □ 空集合
  □ 單一項目集合
  □ 大型集合（如適用）

□ 錯誤處理
  □ 無效輸入格式
  □ 缺少必要欄位
  □ 重複/衝突情況
  □ 找不到資料情況
  □ 外部服務失敗（如適用）

□ 授權驗證
  □ 每個允許的角色已測試
  □ 每個拒絕的角色已測試
  □ 未認證存取已測試
  □ 跨邊界存取已測試

□ 狀態變更
  □ 初始狀態已驗證
  □ 最終狀態已驗證
  □ 所有有效的狀態轉換已測試

□ 驗證邏輯
  □ 格式驗證（電子郵件、電話等）
  □ 商業規則驗證
  □ 跨欄位驗證

□ 整合測試（如 UT 使用萬用字元）
  □ 查詢述詞已驗證
  □ 實體關聯已驗證
  □ 分頁已驗證
  □ 排序/過濾已驗證
```

## 詳細指南

完整標準請參考：
- [測試完整性維度](../../core/test-completeness-dimensions.md)
- [測試標準](../../core/testing-standards.md)

### AI 優化格式（節省 Token）

AI 助手可使用 YAML 格式檔案以減少 Token 使用量：
- 基礎標準：`ai/standards/test-completeness-dimensions.ai.yaml`

## 範例

### 1. 正常路徑

```csharp
[Fact]
public async Task CreateUser_WithValidData_ReturnsSuccess()
{
    // Arrange
    var request = new CreateUserRequest
    {
        Username = "newuser",
        Email = "user@example.com"
    };

    // Act
    var result = await _service.CreateUserAsync(request);

    // Assert
    result.Success.Should().BeTrue();
    result.Data.Username.Should().Be("newuser");
}
```

### 2. 邊界條件

```csharp
[Theory]
[InlineData(0, false)]      // 低於最小值
[InlineData(1, true)]       // 最小有效值
[InlineData(100, true)]     // 最大有效值
[InlineData(101, false)]    // 高於最大值
public void ValidateQuantity_BoundaryValues_ReturnsExpected(
    int quantity, bool expected)
{
    var result = _validator.IsValidQuantity(quantity);
    result.Should().Be(expected);
}
```

### 4. 授權驗證

```csharp
[Fact]
public async Task DeleteUser_AsAdmin_Succeeds()
{
    var adminContext = CreateContext(role: "Admin");
    var result = await _service.DeleteUserAsync(userId, adminContext);
    result.Success.Should().BeTrue();
}

[Fact]
public async Task DeleteUser_AsMember_ReturnsForbidden()
{
    var memberContext = CreateContext(role: "Member");
    var result = await _service.DeleteUserAsync(userId, memberContext);
    result.ErrorCode.Should().Be("FORBIDDEN");
}
```

### 5. 狀態變更

```csharp
[Fact]
public async Task DisableUser_UpdatesStateCorrectly()
{
    // Arrange
    var user = await CreateEnabledUser();
    user.IsEnabled.Should().BeTrue();  // 驗證初始狀態

    // Act
    await _service.DisableUserAsync(user.Id);

    // Assert
    var updatedUser = await _repository.GetByIdAsync(user.Id);
    updatedUser.IsEnabled.Should().BeFalse();  // 驗證最終狀態
}
```

## 授權矩陣範本

為每個功能建立矩陣：

| 操作 | 管理員 | 經理 | 成員 | 訪客 |
|------|--------|------|------|------|
| 建立 | ✅ | ✅ | ❌ | ❌ |
| 讀取全部 | ✅ | ⚠️ 範圍限制 | ❌ | ❌ |
| 更新 | ✅ | ⚠️ 僅自己部門 | ❌ | ❌ |
| 刪除 | ✅ | ❌ | ❌ | ❌ |

每個格子都應該有對應的測試案例。

## 要避免的反模式

- ❌ 只測試正常路徑
- ❌ 多角色系統缺少授權測試
- ❌ 沒有驗證狀態變更
- ❌ 單元測試使用萬用字元但沒有對應的整合測試
- ❌ 測試資料中 ID 和業務識別碼使用相同值
- ❌ 測試實作細節而非行為

---

## 設定偵測

此技能支援專案特定設定。

### 偵測順序

1. 檢查 `CONTRIBUTING.md` 中的「測試標準」區段
2. 檢查程式碼庫中現有的測試模式
3. 若無找到，**預設使用全部 7 個維度**

### 首次設定

若未找到設定：

1. 建議：「此專案尚未設定測試完整性要求。您要自訂需要哪些維度嗎？」
2. 建議在 `CONTRIBUTING.md` 中記錄：

```markdown
## 測試完整性

我們使用 7 維度框架來確保測試覆蓋。

### 各功能類型需要的維度
- API 端點：全部 7 個維度
- 工具函式：維度 1, 2, 3, 6
- 背景作業：維度 1, 3, 5
```

---

## 相關標準

- [測試完整性維度](../../core/test-completeness-dimensions.md)
- [測試標準](../../core/testing-standards.md)
- [測試指南](../testing-guide/SKILL.md)

---

## 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 1.0.0 | 2025-12-30 | 初始發布 |

---

## 授權

此技能採用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
