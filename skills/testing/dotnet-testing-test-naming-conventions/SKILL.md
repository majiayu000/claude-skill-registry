---
name: dotnet-testing-test-naming-conventions
description: |
  測試命名規範與最佳實踐的專門技能。當需要為測試方法命名、改進測試可讀性、建立命名標準時使用。涵蓋三段式命名法、中文命名建議、測試類別命名等。
  Keywords: test naming, 測試命名, naming conventions, 命名規範, 三段式命名, three-part naming, method_scenario_expected, 方法_情境_預期, 如何命名測試, 測試可讀性, test readability, 命名最佳實踐, 測試報告, test documentation
license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: ".NET, testing, naming conventions, test naming, readability"
---

# .NET 測試命名規範指南

## 適用情境

當被要求執行以下任務時，請使用此技能：

- 為測試方法或測試類別命名
- 檢視並改進現有測試的命名
- 確保測試報告的可讀性
- 建立團隊一致的測試命名標準

## 測試方法命名規範

### 標準格式

使用底線分隔的三段式命名法：

```text
[被測試方法名稱]_[測試情境/輸入條件]_[預期行為/結果]
```

### 各段說明

| 區段                  | 說明                     | 範例                                       |
| --------------------- | ------------------------ | ------------------------------------------ |
| **被測試方法名稱**    | 正在測試的方法名稱       | `Add`、`ProcessOrder`、`IsValidEmail`      |
| **測試情境/輸入條件** | 描述測試的前置條件或輸入 | `輸入1和2`、`輸入null`、`輸入有效訂單`     |
| **預期行為/結果**     | 描述預期的輸出或行為     | `應回傳3`、`應拋出Exception`、`應回傳True` |

## 命名範例對照表

### ✅ 好的命名 vs ❌ 不好的命名

| ❌ 不好的命名 | ✅ 好的命名                                         | 原因                       |
| ------------- | --------------------------------------------------- | -------------------------- |
| `TestAdd`     | `Add_輸入1和2_應回傳3`                              | 清楚說明測試情境與預期結果 |
| `Test1`       | `Add_輸入負數和正數_應回傳正確結果`                 | 有意義的描述               |
| `EmailTest`   | `IsValidEmail_輸入有效Email_應回傳True`             | 完整的三段式命名           |
| `OrderTest`   | `ProcessOrder_輸入null_應拋出ArgumentNullException` | 明確的例外情境             |

## 實際範例

### 基本運算測試

```csharp
// ✅ 正常路徑測試
[Fact]
public void Add_輸入1和2_應回傳3()

// ✅ 邊界條件測試
[Fact]
public void Add_輸入0和0_應回傳0()

// ✅ 負數測試
[Fact]
public void Add_輸入負數和正數_應回傳正確結果()
```

### 驗證邏輯測試

```csharp
// ✅ 有效輸入測試
[Fact]
public void IsValidEmail_輸入有效Email_應回傳True()

// ✅ 無效輸入 - null
[Fact]
public void IsValidEmail_輸入null值_應回傳False()

// ✅ 無效輸入 - 空字串
[Fact]
public void IsValidEmail_輸入空字串_應回傳False()

// ✅ 無效輸入 - 格式錯誤
[Fact]
public void IsValidEmail_輸入無效Email格式_應回傳False()
```

### 業務邏輯測試

```csharp
// ✅ 處理流程測試
[Fact]
public void ProcessOrder_輸入有效訂單_應回傳處理後訂單()

// ✅ 例外處理測試
[Fact]
public void ProcessOrder_輸入null_應拋出ArgumentNullException()

// ✅ 格式化測試
[Fact]
public void GetOrderNumber_輸入有效訂單_應回傳格式化訂單號碼()
```

### 計算邏輯測試

```csharp
// ✅ 正常計算
[Fact]
public void Calculate_輸入100元和10Percent折扣_應回傳90元()

// ✅ 無效輸入 - 負數
[Fact]
public void Calculate_輸入負數價格_應拋出ArgumentException()

// ✅ 邊界值測試
[Fact]
public void Calculate_輸入0元價格_應正常處理()

// ✅ 含稅計算
[Fact]
public void CalculateWithTax_輸入100元和5Percent稅率_應回傳105元()
```

### 狀態變化測試

```csharp
// ✅ 初始狀態測試
[Fact]
public void Increment_從0開始_應回傳1()

// ✅ 連續操作測試
[Fact]
public void Increment_從0開始連續兩次_應回傳2()

// ✅ 重設測試
[Fact]
public void Reset_從任意值_應回傳0()
```

## 測試類別命名規範

### 標準格式

```text
[被測試類別名稱]Tests
```

### 範例

| 被測試類別        | 測試類別名稱           |
| ----------------- | ---------------------- |
| `Calculator`      | `CalculatorTests`      |
| `OrderService`    | `OrderServiceTests`    |
| `EmailHelper`     | `EmailHelperTests`     |
| `PriceCalculator` | `PriceCalculatorTests` |

### 類別結構範本

```csharp
namespace MyProject.Tests;

/// <summary>
/// class CalculatorTests - Calculator 測試類別
/// </summary>
public class CalculatorTests
{
    private readonly Calculator _calculator;

    public CalculatorTests()
    {
        _calculator = new Calculator();
    }

    //---------------------------------------------------------------------------------------------
    // Add 方法測試

    [Fact]
    public void Add_輸入1和2_應回傳3()
    {
        // ...
    }

    //---------------------------------------------------------------------------------------------
    // Divide 方法測試

    [Fact]
    public void Divide_輸入10和2_應回傳5()
    {
        // ...
    }
}
```

## 參數化測試命名

使用 `[Theory]` 時的命名規範：

```csharp
// ✅ 使用「各種」表示多組測試資料
[Theory]
[InlineData(1, 2, 3)]
[InlineData(-1, 1, 0)]
[InlineData(0, 0, 0)]
public void Add_輸入各種數值組合_應回傳正確結果(int a, int b, int expected)

// ✅ 使用「有效」表示正向測試
[Theory]
[InlineData("test@example.com")]
[InlineData("user.name@domain.org")]
public void IsValidEmail_輸入有效Email格式_應回傳True(string validEmail)

// ✅ 使用「無效」表示負向測試
[Theory]
[InlineData("invalid-email")]
[InlineData("@example.com")]
public void IsValidEmail_輸入無效Email格式_應回傳False(string invalidEmail)
```

## 常用情境詞彙

### 輸入條件詞彙

| 詞彙        | 使用情境             |
| ----------- | -------------------- |
| `輸入`      | 一般輸入參數         |
| `給定`      | Given-When-Then 風格 |
| `當`        | 事件觸發             |
| `從...開始` | 初始狀態描述         |

### 預期結果詞彙

| 詞彙         | 使用情境 |
| ------------ | -------- |
| `應回傳`     | 有回傳值 |
| `應拋出`     | 預期例外 |
| `應為`       | 狀態驗證 |
| `應包含`     | 集合驗證 |
| `應正常處理` | 邊界條件 |

## 命名檢查清單

為測試方法命名時，請確認：

- [ ] 使用三段式命名 `方法_情境_預期`
- [ ] 情境描述清楚明確
- [ ] 預期結果具體可驗證
- [ ] 使用中文增加可讀性
- [ ] 避免模糊詞彙如 `Test1`、`TestMethod`
- [ ] 參數化測試使用「各種」、「有效」、「無效」等詞彙

## 測試報告可讀性

好的命名會讓測試報告更易讀：

```text
✅ CalculatorTests
   ✅ Add_輸入1和2_應回傳3
   ✅ Add_輸入負數和正數_應回傳正確結果
   ❌ Divide_輸入10和0_應拋出DivideByZeroException
   
✅ EmailHelperTests
   ✅ IsValidEmail_輸入有效Email_應回傳True
   ✅ IsValidEmail_輸入null值_應回傳False
```

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 01 - 老派工程師的測試啟蒙**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10373888
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day01
