---
name: test-data-builder-pattern
description: 使用 Test Data Builder Pattern 建構可維護、可讀、流暢的測試資料。當需要建立測試物件、管理複雜測試資料、或改善測試可讀性時使用此技能。適用於單元測試與整合測試的測試資料準備階段。
license: MIT
---

# Test Data Builder Pattern 測試資料建構器模式

## 概述

Test Data Builder Pattern 是一種專為測試設計的建構者模式（Builder Pattern）變體，用於建立清晰、可維護且表意明確的測試資料。此模式特別適合處理具有多個屬性的複雜物件，讓測試程式碼更易讀且降低維護成本。

## 核心概念

### 什麼是 Test Data Builder Pattern？

Test Data Builder Pattern 是 Object Mother Pattern 的改良版，主要解決以下問題：

1. **固定測試資料的問題**：Object Mother 提供固定的測試物件，難以針對特定測試情境調整
2. **測試意圖不明確**：直接建立物件時，測試的關注點容易被大量屬性設定所掩蓋
3. **重複程式碼**：相似的物件建立邏輯在多個測試中重複出現

### 為何需要 Builder Pattern？

**傳統測試資料建立的問題：**

```csharp
// ❌ 問題：過多參數設定，測試意圖不明確
var user = new User
{
    Name = "John Doe",
    Email = "john@example.com",
    Age = 30,
    Roles = new[] { "User" },
    Settings = new UserSettings { Theme = "Dark", Language = "zh-TW" },
    IsActive = true,
    CreatedAt = DateTime.Now,
    ModifiedAt = DateTime.Now
};
```

**使用 Builder Pattern 的改善：**

```csharp
// ✅ 改善：意圖明確，只設定測試關注的屬性
var user = UserBuilder
    .AUser()
    .WithName("John Doe")
    .WithValidEmail()
    .Build();
```

## 實作指南

### 基本 Builder 結構

一個標準的 Test Data Builder 應包含：

1. **預設值**：為所有必要屬性提供合理的預設值
2. **流暢介面**：使用 `With*` 方法鏈來設定屬性
3. **語意化方法**：提供有意義的預設建立者（如 `AnAdminUser()`、`ARegularUser()`）
4. **Build 方法**：最終建立並回傳目標物件

### 完整 Builder 範例

```csharp
public class UserBuilder
{
    // 預設值：提供所有屬性的合理預設值
    private string _name = "Default User";
    private string _email = "default@example.com";
    private int _age = 25;
    private List<string> _roles = new();
    private UserSettings _settings = new() 
    { 
        Theme = "Light", 
        Language = "en-US" 
    };
    private bool _isActive = true;
    private DateTime _createdAt = DateTime.UtcNow;
    
    // With* 方法：流暢介面設定個別屬性
    public UserBuilder WithName(string name)
    {
        _name = name;
        return this;
    }
    
    public UserBuilder WithEmail(string email)
    {
        _email = email;
        return this;
    }
    
    public UserBuilder WithAge(int age)
    {
        _age = age;
        return this;
    }
    
    public UserBuilder WithRole(string role)
    {
        _roles.Add(role);
        return this;
    }
    
    public UserBuilder WithRoles(params string[] roles)
    {
        _roles.AddRange(roles);
        return this;
    }
    
    public UserBuilder WithSettings(UserSettings settings)
    {
        _settings = settings;
        return this;
    }
    
    public UserBuilder IsInactive()
    {
        _isActive = false;
        return this;
    }
    
    public UserBuilder CreatedOn(DateTime createdAt)
    {
        _createdAt = createdAt;
        return this;
    }
    
    // 語意化預設建立者：提供常見情境的快速建立方法
    public static UserBuilder AUser() => new();
    
    public static UserBuilder AnAdminUser() => new UserBuilder()
        .WithRoles("Admin", "User");
    
    public static UserBuilder ARegularUser() => new UserBuilder()
        .WithRole("User");
    
    public static UserBuilder AnInactiveUser() => new UserBuilder()
        .IsInactive();
    
    // 語意化組合方法
    public UserBuilder WithValidEmail()
    {
        _email = $"{_name.Replace(" ", ".").ToLower()}@example.com";
        return this;
    }
    
    public UserBuilder WithAdminRights()
    {
        return WithRoles("Admin", "User");
    }
    
    // Build 方法：建立最終物件
    public User Build()
    {
        return new User
        {
            Name = _name,
            Email = _email,
            Age = _age,
            Roles = _roles.ToArray(),
            Settings = _settings,
            IsActive = _isActive,
            CreatedAt = _createdAt,
            ModifiedAt = _createdAt
        };
    }
}
```

## 在測試中使用 Builder

### 單一測試情境

```csharp
[Fact]
public void CreateUser_有效管理員使用者_應成功建立()
{
    // Arrange - 使用 Builder 建立測試資料
    var adminUser = UserBuilder
        .AnAdminUser()
        .WithName("John Admin")
        .WithEmail("john.admin@company.com")
        .WithAge(35)
        .Build();
        
    var userService = new UserService();
    
    // Act
    var result = userService.CreateUser(adminUser);
    
    // Assert
    Assert.NotNull(result);
    Assert.Equal("John Admin", result.Name);
    Assert.Contains("Admin", result.Roles);
}
```

### 配合 Theory 使用

```csharp
public class UserValidationTests
{
    [Theory]
    [MemberData(nameof(GetUserScenarios))]
    public void ValidateUser_不同使用者情境_應回傳正確驗證結果(User user, bool expected)
    {
        // Arrange
        var validator = new UserValidator();
        
        // Act
        var result = validator.IsValid(user);
        
        // Assert
        Assert.Equal(expected, result);
    }
    
    public static IEnumerable<object[]> GetUserScenarios()
    {
        // ✅ 有效使用者情境
        yield return new object[]
        {
            UserBuilder.AUser()
                .WithName("Valid User")
                .WithEmail("valid@example.com")
                .WithAge(25)
                .Build(),
            true
        };
        
        // ❌ 無效使用者情境 - 空名稱
        yield return new object[]
        {
            UserBuilder.AUser()
                .WithName("")
                .Build(),
            false
        };
        
        // ❌ 無效使用者情境 - 年齡過小
        yield return new object[]
        {
            UserBuilder.AUser()
                .WithAge(10)
                .Build(),
            false
        };
        
        // ❌ 無效使用者情境 - 無效 Email
        yield return new object[]
        {
            UserBuilder.AUser()
                .WithEmail("invalid-email")
                .Build(),
            false
        };
    }
}
```

## 最佳實踐

### 1. 提供合理的預設值

**✅ 良好實踐：預設值讓物件處於有效狀態**

```csharp
public class ProductBuilder
{
    private string _name = "Default Product";
    private decimal _price = 100m;
    private int _stock = 10;
    private bool _isAvailable = true;
    
    // 預設值確保建立的物件是有效的
    public Product Build() => new()
    {
        Name = _name,
        Price = _price,
        Stock = _stock,
        IsAvailable = _isAvailable
    };
}
```

### 2. 使用語意化的命名

**✅ 良好實踐：方法名稱表達測試意圖**

```csharp
public static class UserScenarios
{
    public static UserBuilder ANewUser() => UserBuilder.AUser()
        .CreatedOn(DateTime.UtcNow);
    
    public static UserBuilder AnExpiredUser() => UserBuilder.AUser()
        .CreatedOn(DateTime.UtcNow.AddYears(-5))
        .IsInactive();
    
    public static UserBuilder APremiumUser() => UserBuilder.AUser()
        .WithRoles("Premium", "User")
        .WithSettings(new UserSettings { FeatureFlags = new[] { "AdvancedSearch" } });
}
```

### 3. Builder 之間的組合

**✅ 良好實踐：Builder 可以組合使用**

```csharp
public class OrderBuilder
{
    private User _customer = UserBuilder.AUser().Build();
    private List<Product> _products = new();
    private decimal _totalAmount = 0m;
    
    public OrderBuilder ForCustomer(User customer)
    {
        _customer = customer;
        return this;
    }
    
    public OrderBuilder WithProduct(Product product)
    {
        _products.Add(product);
        _totalAmount += product.Price;
        return this;
    }
    
    public OrderBuilder WithProducts(params Product[] products)
    {
        _products.AddRange(products);
        _totalAmount = _products.Sum(p => p.Price);
        return this;
    }
    
    public Order Build() => new()
    {
        Customer = _customer,
        Products = _products,
        TotalAmount = _totalAmount,
        OrderDate = DateTime.UtcNow
    };
}

// 使用組合的 Builder
var order = new OrderBuilder()
    .ForCustomer(UserBuilder.APremiumUser().Build())
    .WithProducts(
        ProductBuilder.AProduct().WithPrice(100m).Build(),
        ProductBuilder.AProduct().WithPrice(200m).Build()
    )
    .Build();
```

### 4. 避免過度複雜化

**❌ 不良實踐：Builder 過於複雜**

```csharp
// 避免在 Builder 中加入複雜的業務邏輯
public UserBuilder WithComplexValidation()
{
    // ❌ 不要在 Builder 中進行複雜驗證
    if (_email.Contains("@"))
    {
        var parts = _email.Split('@');
        if (parts[1].Length > 10)
        {
            _email = parts[0] + "@short.com";
        }
    }
    return this;
}
```

**✅ 良好實踐：保持 Builder 簡單**

```csharp
// Builder 只負責建立物件，不包含業務邏輯
public UserBuilder WithShortDomainEmail()
{
    _email = "user@short.com";
    return this;
}
```

### 5. 統一管理測試資料

**✅ 良好實踐：建立共享的測試資料類別**

```csharp
public static class TestData
{
    public static class Users
    {
        public static User John => UserBuilder.AUser()
            .WithName("John Doe")
            .WithEmail("john@example.com")
            .Build();
        
        public static User AdminUser => UserBuilder.AnAdminUser()
            .WithName("Admin User")
            .WithEmail("admin@company.com")
            .Build();
    }
    
    public static class Products
    {
        public static Product Laptop => ProductBuilder.AProduct()
            .WithName("Laptop")
            .WithPrice(1000m)
            .Build();
    }
}

// 在測試中使用
[Fact]
public void ProcessOrder_有效訂單_應成功處理()
{
    var order = new OrderBuilder()
        .ForCustomer(TestData.Users.John)
        .WithProduct(TestData.Products.Laptop)
        .Build();
    // ...
}
```

## 與其他模式的比較

### Test Data Builder vs. Object Mother

| 特性     | Test Data Builder           | Object Mother         |
| -------- | --------------------------- | --------------------- |
| 彈性     | ✅ 高度彈性，可針對測試調整 | ❌ 固定的測試資料     |
| 可讀性   | ✅ 流暢介面，意圖明確       | ⚠️ 需要查看方法實作 |
| 維護性   | ✅ 集中管理，易於修改       | ❌ 變更影響所有測試   |
| 使用場景 | 單元測試、情境測試          | 簡單的整合測試        |

### Test Data Builder vs. AutoFixture

| 特性       | Test Data Builder       | AutoFixture               |
| ---------- | ----------------------- | ------------------------- |
| 控制度     | ✅ 完全控制物件建立     | ⚠️ 自動產生，控制度較低 |
| 設定複雜度 | ⚠️ 需手動建立 Builder | ✅ 幾乎零設定             |
| 測試意圖   | ✅ 非常明確             | ⚠️ 需額外說明           |
| 適用時機   | 需要精確控制的測試      | 大量資料產生、匿名測試    |

> **建議**：Test Data Builder 和 AutoFixture 可以相輔相成。簡單情境使用 AutoFixture，複雜情境或需明確意圖時使用 Builder Pattern。

## 實戰範例

請參考 `templates/` 目錄下的完整實作範例：

- `user-builder-example.cs` - 基本 User Builder 實作
- `advanced-builder-scenarios.cs` - 進階 Builder 組合與使用情境
- `builder-with-theory.cs` - Builder 配合 xUnit Theory 的實務範例

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 03 - 測試資料的準備方式：Test Data Builder Pattern**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10374064
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day03

### 延伸閱讀

- **Test Data Builder 原始文章**：[Test Data Builders: an alternative to the Object Mother pattern](http://www.natpryce.com/articles/000714.html) by Nat Pryce
- **Builder Pattern vs Object Mother**：[Test Data Builders and Object Mother: another look](https://www.javacodegeeks.com/2014/06/test-data-builders-and-object-mother-another-look.html)

### 相關技能

- `autofixture-basics` - 使用 AutoFixture 自動產生測試資料
- `xunit-project-setup` - xUnit 測試專案的基礎設定
- `test-naming-conventions` - 測試命名規範

## 總結

Test Data Builder Pattern 是撰寫可維護測試的重要技巧：

✅ **使用時機**：

- 測試物件有多個屬性需要設定
- 需要在多個測試中重複使用相似的測試資料
- 希望測試程式碼表達清晰的意圖

✅ **核心優勢**：

- 提升測試可讀性
- 降低測試維護成本
- 增強測試表達力

⚠️ **注意事項**：

- 保持 Builder 簡單，避免加入業務邏輯
- 提供合理的預設值
- 使用語意化的方法名稱
