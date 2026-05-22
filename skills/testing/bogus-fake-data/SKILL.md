---
name: bogus-fake-data
description: 協助使用 Bogus 假資料產生函式庫在 .NET 測試中產生真實感的測試資料。當使用者需要產生擬真的姓名、地址、電話、公司資訊等測試資料，或需要多語言支援的測試資料時，請使用此技能。
author: Kevin Tsen
license: MIT
version: 1.0.0
tags: [bogus, fake-data, test-data, realistic-data, faker, xunit, testing]
related_skills:
  - autofixture-basics
  - autofixture-bogus-integration
  - test-data-builder-pattern
---

# Bogus 假資料產生器

## 技能概述

Bogus 是一個 .NET 平台的假資料產生函式庫，移植自著名的 JavaScript 函式庫 faker.js。它專門用於產生真實感強烈的假資料，如姓名、地址、電話號碼、電子郵件等，特別適合需要模擬真實世界資料的測試場景。

### 適用情境

當被要求執行以下任務時，請使用此技能：

- 產生具有真實感的測試資料（姓名、地址、公司名稱等）
- 需要多語言或多地區格式的測試資料
- 整合測試或 UI 原型需要擬真資料
- 效能測試需要大量真實格式的資料
- 資料庫種子（Seed）需要初始化開發或測試環境

### 核心價值

- **真實感資料產生**：提供有意義的假資料，如真實的姓名、地址、公司名稱
- **多語言支援**：支援超過 40 種語言和地區格式（包含繁體中文 `zh_TW`）
- **可重現性**：透過 seed 控制，確保測試資料的一致性
- **豐富的資料類型**：內建多種 DataSet，涵蓋各種真實世界的資料類型
- **簡潔的 Fluent API**：直觀易用的設定語法

---

## 套件安裝與設定

### 安裝 Bogus

```bash
dotnet add package Bogus
```

### NuGet 套件資訊

| 套件名稱 | 用途             | NuGet 連結                                         |
| -------- | ---------------- | -------------------------------------------------- |
| `Bogus`  | 假資料產生函式庫 | [nuget.org](https://www.nuget.org/packages/Bogus/) |

**GitHub 儲存庫**：[bchavez/Bogus](https://github.com/bchavez/Bogus)

---

## 核心概念

### 基本語法結構

Bogus 的核心是 `Faker<T>` 類別，使用 `RuleFor` 方法定義屬性的產生規則：

```csharp
using Bogus;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string Description { get; set; } = string.Empty;
    public DateTime CreatedDate { get; set; }
}

// 建立產品資料的 Faker
var productFaker = new Faker<Product>()
    .RuleFor(p => p.Id, f => f.IndexFaker)
    .RuleFor(p => p.Name, f => f.Commerce.ProductName())
    .RuleFor(p => p.Price, f => f.Random.Decimal(10, 1000))
    .RuleFor(p => p.Description, f => f.Lorem.Sentence())
    .RuleFor(p => p.CreatedDate, f => f.Date.Past());

// 產生單筆資料
var product = productFaker.Generate();

// 產生多筆資料
var products = productFaker.Generate(10);
```

### 內建 DataSet 概覽

Bogus 提供豐富的內建 DataSet，每個都專注於特定領域的資料產生：

#### 個人資訊 (Person DataSet)

```csharp
var faker = new Faker();

var fullName = faker.Person.FullName;        // 完整姓名
var firstName = faker.Person.FirstName;      // 名字
var lastName = faker.Person.LastName;        // 姓氏
var email = faker.Person.Email;              // 電子郵件
var gender = faker.Person.Gender;            // 性別
var dateOfBirth = faker.Person.DateOfBirth;  // 生日
```

#### 地址資訊 (Address DataSet)

```csharp
var fullAddress = faker.Address.FullAddress();    // 完整地址
var streetAddress = faker.Address.StreetAddress(); // 街道地址
var city = faker.Address.City();                   // 城市
var state = faker.Address.State();                 // 州/省
var zipCode = faker.Address.ZipCode();             // 郵遞區號
var country = faker.Address.Country();             // 國家
var latitude = faker.Address.Latitude();           // 緯度
var longitude = faker.Address.Longitude();         // 經度
```

#### 商業資訊 (Company & Commerce DataSet)

```csharp
var companyName = faker.Company.CompanyName();     // 公司名稱
var catchPhrase = faker.Company.CatchPhrase();     // 標語
var department = faker.Commerce.Department();      // 部門
var productName = faker.Commerce.ProductName();    // 產品名稱
var price = faker.Commerce.Price(1, 1000, 2);      // 價格（字串格式）
var ean13 = faker.Commerce.Ean13();                // EAN-13 條碼
```

#### 網路資訊 (Internet DataSet)

```csharp
var url = faker.Internet.Url();               // URL
var domainName = faker.Internet.DomainName(); // 網域名稱
var ipAddress = faker.Internet.Ip();          // IPv4 地址
var ipv6 = faker.Internet.Ipv6();             // IPv6 地址
var userName = faker.Internet.UserName();     // 使用者名稱
var password = faker.Internet.Password();     // 密碼
var email = faker.Internet.Email();           // 電子郵件
```

#### 金融資訊 (Finance DataSet)

```csharp
var creditCardNumber = faker.Finance.CreditCardNumber();  // 信用卡號
var creditCardCvv = faker.Finance.CreditCardCvv();        // CVV
var account = faker.Finance.Account();                     // 帳戶號碼
var amount = faker.Finance.Amount(100, 10000, 2);          // 金額
var currency = faker.Finance.Currency();                   // 貨幣
var iban = faker.Finance.Iban();                          // IBAN
var bic = faker.Finance.Bic();                            // BIC/SWIFT
```

#### 時間資訊 (Date DataSet)

```csharp
var pastDate = faker.Date.Past();                        // 過去日期
var futureDate = faker.Date.Future();                    // 未來日期
var recentDate = faker.Date.Recent();                    // 最近日期
var soonDate = faker.Date.Soon();                        // 即將到來的日期
var between = faker.Date.Between(start, end);            // 範圍內日期
var weekday = faker.Date.Weekday();                      // 星期幾
```

#### 隨機資料 (Random DataSet)

```csharp
var randomInt = faker.Random.Int(1, 100);                  // 整數
var randomDecimal = faker.Random.Decimal(0, 1000);         // 小數
var randomBool = faker.Random.Bool();                      // 布林
var randomGuid = faker.Random.Guid();                      // GUID
var randomEnum = faker.Random.Enum<DayOfWeek>();           // 隨機列舉
var randomElement = faker.Random.ArrayElement(array);      // 陣列隨機元素
var shuffled = faker.Random.Shuffle(collection);           // 洗牌
```

#### 文字內容 (Lorem DataSet)

```csharp
var word = faker.Lorem.Word();             // 單字
var words = faker.Lorem.Words(5);          // 多個單字
var sentence = faker.Lorem.Sentence();     // 句子
var paragraph = faker.Lorem.Paragraph();   // 段落
var text = faker.Lorem.Text();             // 文字區塊
```

---

## 多語言支援

Bogus 的一大特色是支援多種語言和文化，讓產生的資料更符合當地習慣：

```csharp
// 繁體中文
var chineseFaker = new Faker<Person>("zh_TW")
    .RuleFor(p => p.Name, f => f.Person.FullName)
    .RuleFor(p => p.Address, f => f.Address.FullAddress());

// 日文
var japaneseFaker = new Faker<Person>("ja")
    .RuleFor(p => p.Name, f => f.Person.FullName)
    .RuleFor(p => p.Phone, f => f.Phone.PhoneNumber());

// 法文
var frenchFaker = new Faker<Person>("fr")
    .RuleFor(p => p.Name, f => f.Person.FullName)
    .RuleFor(p => p.Company, f => f.Company.CompanyName());
```

### 支援的語言代碼

| 語言         | 代碼    | 語言     | 代碼    |
| ------------ | ------- | -------- | ------- |
| 英文（美國） | `en_US` | 簡體中文 | `zh_CN` |
| 繁體中文     | `zh_TW` | 日文     | `ja`    |
| 韓文         | `ko`    | 法文     | `fr`    |
| 德文         | `de`    | 西班牙文 | `es`    |
| 俄文         | `ru`    | 葡萄牙文 | `pt_BR` |

---

## 進階功能

### 可重現性控制（Seed）

透過設定 seed，確保每次產生相同的資料序列：

```csharp
// 設定全域 seed
Randomizer.Seed = new Random(12345);

var productFaker = new Faker<Product>()
    .RuleFor(p => p.Name, f => f.Commerce.ProductName());

// 每次執行都會產生相同的產品名稱序列
var products1 = productFaker.Generate(5);

// 重置 seed 後重新產生
Randomizer.Seed = new Random(12345);
var products2 = productFaker.Generate(5); // 相同的資料

// 重置為隨機
Randomizer.Seed = new Random();
```

### 條件式產生與機率控制

```csharp
var userFaker = new Faker<User>()
    .RuleFor(u => u.Name, f => f.Person.FullName)
    // 80% 機率有 Premium 會員
    .RuleFor(u => u.IsPremium, f => f.Random.Bool(0.8f))
    // OrNull：50% 機率為 null
    .RuleFor(u => u.MiddleName, f => f.Name.FirstName().OrNull(f, 0.5f))
    // 隨機選擇陣列元素
    .RuleFor(u => u.Department, f => f.PickRandom("IT", "HR", "Finance", "Marketing"))
    // 權重式隨機選擇
    .RuleFor(u => u.Role, f => f.PickRandomWeighted(
        new[] { "User", "Admin", "SuperAdmin" },
        new[] { 0.7f, 0.25f, 0.05f }));
```

### 關聯資料與巢狀物件

```csharp
// 產生具有關聯性的訂單資料
var orderFaker = new Faker<Order>()
    .RuleFor(o => o.Id, f => f.IndexFaker)
    .RuleFor(o => o.CustomerName, f => f.Person.FullName)
    .RuleFor(o => o.OrderDate, f => f.Date.Past())
    // 產生 1-5 個訂單明細
    .RuleFor(o => o.Items, f => 
    {
        var itemFaker = new Faker<OrderItem>()
            .RuleFor(i => i.ProductName, f => f.Commerce.ProductName())
            .RuleFor(i => i.Quantity, f => f.Random.Int(1, 10))
            .RuleFor(i => i.UnitPrice, f => decimal.Parse(f.Commerce.Price(10, 100)));
        
        return itemFaker.Generate(f.Random.Int(1, 5));
    })
    // 計算總金額（參考其他屬性）
    .RuleFor(o => o.TotalAmount, (f, o) => 
        o.Items.Sum(item => item.Quantity * item.UnitPrice));
```

### 複雜業務邏輯約束

```csharp
// 具有複雜業務邏輯的員工資料產生
var employeeFaker = new Faker<Employee>()
    .RuleFor(e => e.Id, f => f.Random.Guid())
    .RuleFor(e => e.FirstName, f => f.Person.FirstName)
    .RuleFor(e => e.LastName, f => f.Person.LastName)
    // 根據姓名產生 Email
    .RuleFor(e => e.Email, (f, e) => 
        f.Internet.Email(e.FirstName, e.LastName, "company.com"))
    // 年齡範圍限制
    .RuleFor(e => e.Age, f => f.Random.Int(22, 65))
    // 根據年齡決定職級
    .RuleFor(e => e.Level, (f, e) => e.Age switch
    {
        < 25 => "Junior",
        < 35 => "Senior",
        < 45 => "Lead",
        _ => "Principal"
    })
    // 根據職級決定薪資範圍
    .RuleFor(e => e.Salary, (f, e) => e.Level switch
    {
        "Junior" => f.Random.Decimal(35000, 50000),
        "Senior" => f.Random.Decimal(50000, 80000),
        "Lead" => f.Random.Decimal(80000, 120000),
        "Principal" => f.Random.Decimal(120000, 200000),
        _ => f.Random.Decimal(35000, 50000)
    });
```

### 自訂 DataSet 擴充

```csharp
// 建立自訂的台灣資料產生器
public static class TaiwanDataSetExtensions
{
    private static readonly string[] TaiwanCities = 
    {
        "台北市", "新北市", "桃園市", "台中市", "台南市", "高雄市",
        "基隆市", "新竹市", "嘉義市", "宜蘭縣", "新竹縣", "苗栗縣"
    };
    
    private static readonly string[] TaiwanCompanies = 
    {
        "台積電", "鴻海", "聯發科", "中華電信", "台塑", "統一"
    };
    
    public static string TaiwanCity(this Faker faker)
        => faker.PickRandom(TaiwanCities);
    
    public static string TaiwanCompany(this Faker faker)
        => faker.PickRandom(TaiwanCompanies);
    
    public static string TaiwanMobilePhone(this Faker faker)
    {
        var prefix = "09";
        var middle = faker.Random.Int(0, 9);
        var suffix = faker.Random.String2(7, "0123456789");
        return $"{prefix}{middle}{suffix}";
    }
    
    public static string TaiwanIdCard(this Faker faker)
    {
        var firstChar = faker.PickRandom("ABCDEFGHJKLMNPQRSTUVXYWZIO");
        var genderDigit = faker.Random.Int(1, 2);
        var digits = faker.Random.String2(8, "0123456789");
        return $"{firstChar}{genderDigit}{digits}";
    }
}

// 使用自訂擴充
var taiwanPersonFaker = new Faker<TaiwanPerson>()
    .RuleFor(p => p.City, f => f.TaiwanCity())
    .RuleFor(p => p.Company, f => f.TaiwanCompany())
    .RuleFor(p => p.Mobile, f => f.TaiwanMobilePhone())
    .RuleFor(p => p.IdCard, f => f.TaiwanIdCard());
```

---

## Bogus vs AutoFixture 比較

### 設計理念差異

| 項目         | AutoFixture               | Bogus                           |
| ------------ | ------------------------- | ------------------------------- |
| **核心理念** | 匿名測試 (Anonymous Test) | 真實模擬 (Realistic Simulation) |
| **資料品質** | 隨機填充，專注測試邏輯    | 有意義資料，模擬真實情境        |
| **學習成本** | 自動推斷，零配置          | 明確定義，需要學習 DataSet      |
| **可讀性**   | 抽象化，減少資料噪音      | 具體化，資料有意義              |

### 適用場景分析

| 場景           | 建議工具    | 原因                           |
| -------------- | ----------- | ------------------------------ |
| **單元測試**   | AutoFixture | 專注於邏輯驗證，不關心資料內容 |
| **整合測試**   | Bogus       | 需要真實感的資料進行端到端測試 |
| **UI 原型**    | Bogus       | 展示用的擬真資料               |
| **效能測試**   | Bogus       | 大量真實格式的資料             |
| **資料庫種子** | Bogus       | 初始化開發/測試環境            |
| **複雜相依性** | AutoFixture | 自動處理循環參考和巢狀物件     |

### 程式碼比較

```csharp
// AutoFixture：簡單直接，自動推斷
var fixture = new Fixture();
var user = fixture.Create<User>(); // 一行搞定，但資料無意義

// Bogus：需要設定，但資料有意義
var userFaker = new Faker<User>()
    .RuleFor(u => u.Name, f => f.Person.FullName)    // 真實的姓名格式
    .RuleFor(u => u.Email, f => f.Internet.Email()); // 真實的郵件格式
var user = userFaker.Generate();
```

---

## 效能最佳化

### 重用 Faker 實例

```csharp
public class OptimizedDataGenerator
{
    // 預編譯 Faker 以提升效能（靜態欄位，只初始化一次）
    private static readonly Faker<User> _userFaker = new Faker<User>()
        .RuleFor(u => u.Id, f => f.Random.Guid())
        .RuleFor(u => u.Name, f => f.Person.FullName)
        .RuleFor(u => u.Email, f => f.Internet.Email());
    
    public static List<User> GenerateUsers(int count) 
        => _userFaker.Generate(count);
}
```

### 批次產生

```csharp
// 批次產生以減少記憶體分配
public static IEnumerable<User> GenerateUsersBatch(int totalCount, int batchSize = 1000)
{
    var generated = 0;
    while (generated < totalCount)
    {
        var currentBatchSize = Math.Min(batchSize, totalCount - generated);
        var batch = _userFaker.Generate(currentBatchSize);
        
        foreach (var user in batch)
        {
            yield return user;
        }
        
        generated += currentBatchSize;
    }
}
```

### Lazy 初始化

```csharp
// 使用 Lazy 延遲初始化複雜的 Faker
private static readonly Lazy<Faker<ComplexEntity>> _complexFaker = 
    new(() => new Faker<ComplexEntity>()
        .RuleFor(e => e.Id, f => f.Random.Guid())
        .RuleFor(e => e.Data, f => GenerateComplexData(f)));

public static ComplexEntity Generate() => _complexFaker.Value.Generate();
```

---

## 測試實作範例

### 郵件服務測試

```csharp
[Fact]
public void EmailService_SendWelcomeEmail_ShouldFormatCorrectly()
{
    // Arrange - 需要真實的使用者資料來測試郵件格式
    var userFaker = new Faker<User>()
        .RuleFor(u => u.Name, f => f.Person.FullName)
        .RuleFor(u => u.Email, f => f.Internet.Email());
    
    var user = userFaker.Generate();
    var emailService = new EmailService();
    
    // Act
    var emailContent = emailService.GenerateWelcomeEmail(user);
    
    // Assert
    emailContent.Should().Contain(user.Name);
    emailContent.Should().Contain(user.Email);
}
```

### 資料庫種子

```csharp
public static class DatabaseSeeder
{
    public static void SeedDatabase(AppDbContext context)
    {
        // 設定 seed 確保可重現
        Randomizer.Seed = new Random(42);
        
        var customerFaker = new Faker<Customer>("zh_TW")
            .RuleFor(c => c.Name, f => f.Person.FullName)
            .RuleFor(c => c.Email, f => f.Internet.Email())
            .RuleFor(c => c.Phone, f => f.Phone.PhoneNumber())
            .RuleFor(c => c.Address, f => f.Address.FullAddress());
        
        var customers = customerFaker.Generate(100);
        context.Customers.AddRange(customers);
        context.SaveChanges();
    }
}
```

---

## 最佳實踐

### 命名與組織

1. **Faker 命名慣例**：使用 `{EntityName}Faker` 格式命名
2. **集中管理**：將 Faker 定義集中在 `TestDataGenerators` 或 `Fakers` 資料夾
3. **重用靜態實例**：避免重複建立 Faker 實例

### 程式碼組織

```text
MyProject.Tests/
├── Fakers/
│   ├── CustomerFaker.cs
│   ├── OrderFaker.cs
│   └── TaiwanDataSetExtensions.cs
├── Services/
│   └── CustomerServiceTests.cs
└── ...
```

### 常見陷阱

1. **避免過度配置**：只設定測試需要的屬性
2. **注意隨機性**：使用 seed 確保測試可重現
3. **效能考量**：大量資料時使用批次產生

---

## 相關技能

| 技能名稱                        | 關聯說明                                     |
| ------------------------------- | -------------------------------------------- |
| `autofixture-basics`            | AutoFixture 基礎使用，適合單元測試的匿名資料 |
| `autofixture-bogus-integration` | AutoFixture 與 Bogus 混合使用策略            |
| `test-data-builder-pattern`     | 手動 Builder Pattern，適合簡單場景           |

---

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 14 - 使用 Bogus 產生假資料**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10375208
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day14

### 官方文件

- [Bogus NuGet Package](https://www.nuget.org/packages/Bogus/)
- [Bogus GitHub Repository](https://github.com/bchavez/Bogus)
- [Bogus 官方文件](https://github.com/bchavez/Bogus#readme)

### 延伸閱讀

- [Bogus 與 AutoFixture 在測試中的應用 | mrkt的程式學習筆記](https://www.dotblogs.com.tw/mrkt/2024/09/29/191300)

---

## 範例檔案

請參考同目錄下的範例程式碼：

- [basic-usage.cs](templates/basic-usage.cs) - 基本使用範例
- [datasets-examples.cs](templates/datasets-examples.cs) - DataSet 使用範例
- [advanced-patterns.cs](templates/advanced-patterns.cs) - 進階模式與自訂擴充
