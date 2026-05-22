# NSubstitute Mocking Skill

---
name: nsubstitute-mocking
description: 協助使用 NSubstitute 建立測試替身（Test Double），包含 Mock、Stub、Spy。當使用者需要隔離外部相依、模擬介面行為、驗證方法呼叫、測試相依注入，或需要建立假物件時，請使用此技能。
license: MIT
---

## 技能說明

此技能專注於使用 NSubstitute 建立和管理測試替身，涵蓋 Test Double 五大類型、依賴隔離策略、行為設定與驗證的最佳實踐。

## 為什麼需要測試替身？

真實世界的程式碼通常依賴外部資源，這些依賴會讓測試變得：

1. **緩慢** - 需要實際操作資料庫、檔案系統、網路
2. **不穩定** - 外部服務異常導致測試失敗
3. **難以重複** - 時間、隨機數導致結果不一致
4. **環境依賴** - 需要特定的外部環境設定
5. **開發阻塞** - 必須等待外部系統準備就緒

測試替身（Test Double）讓我們能夠隔離這些依賴，專注測試業務邏輯。

## 前置需求

### 套件安裝

```xml
<PackageReference Include="NSubstitute" Version="5.3.0" />
<PackageReference Include="xunit" Version="2.9.3" />
<PackageReference Include="Microsoft.Extensions.Logging" Version="9.0.0" />
<PackageReference Include="AwesomeAssertions" Version="9.1.0" />
```

### 基本 using 指令

```csharp
using NSubstitute;
using NSubstitute.ExceptionExtensions;
using Xunit;
using AwesomeAssertions;
using Microsoft.Extensions.Logging;
```

## Test Double 五大類型

根據 Gerard Meszaros 在《xUnit Test Patterns》中的定義：

### 1. Dummy - 填充物件

僅用於滿足方法簽章，不會被實際使用。

```csharp
public interface IEmailService
{
    void SendEmail(string to, string subject, string body, ILogger logger);
}

[Fact]
public void ProcessOrder_不使用Logger_應成功處理訂單()
{
    // Dummy：只是為了滿足參數要求
    var dummyLogger = Substitute.For<ILogger>();
    
    var service = new OrderService();
    var result = service.ProcessOrder(order, dummyLogger);
    
    result.Success.Should().BeTrue();
    // 不關心 logger 是否被調用
}
```

### 2. Stub - 預設回傳值

提供預先定義的回傳值，用於測試特定情境。

```csharp
[Fact]
public void GetUser_有效的使用者ID_應回傳使用者資料()
{
    // Arrange - Stub：預設回傳值
    var stubRepository = Substitute.For<IUserRepository>();
    stubRepository.GetById(123).Returns(new User { Id = 123, Name = "John" });
    
    var service = new UserService(stubRepository);
    
    // Act
    var actual = service.GetUser(123);
    
    // Assert
    actual.Name.Should().Be("John");
    // 不關心 GetById 被呼叫了幾次
}
```

### 3. Fake - 簡化實作

有實際功能但簡化的實作，通常用於整合測試。

```csharp
public class FakeUserRepository : IUserRepository
{
    private readonly Dictionary<int, User> _users = new();
    
    public User GetById(int id) => _users.TryGetValue(id, out var user) ? user : null;
    public void Save(User user) => _users[user.Id] = user;
    public void Delete(int id) => _users.Remove(id);
}

[Fact]
public void CreateUser_建立使用者_應儲存並可查詢()
{
    // Fake：有真實邏輯的簡化實作
    var fakeRepository = new FakeUserRepository();
    var service = new UserService(fakeRepository);
    
    service.CreateUser(new User { Id = 1, Name = "John" });
    var actual = service.GetUser(1);
    
    actual.Name.Should().Be("John");
}
```

### 4. Spy - 記錄呼叫

記錄被如何呼叫，可以事後驗證。

```csharp
[Fact]
public void CreateUser_建立使用者_應記錄建立資訊()
{
    // Arrange
    var spyLogger = Substitute.For<ILogger<UserService>>();
    var repository = Substitute.For<IUserRepository>();
    var service = new UserService(repository, spyLogger);
    
    // Act
    service.CreateUser(new User { Name = "John" });
    
    // Assert - Spy：驗證呼叫記錄
    spyLogger.Received(1).LogInformation("User created: {Name}", "John");
}
```

### 5. Mock - 行為驗證

預設期望的互動行為，測試失敗如果期望沒有滿足。

```csharp
[Fact]
public void RegisterUser_註冊使用者_應發送歡迎郵件()
{
    // Arrange
    var mockEmailService = Substitute.For<IEmailService>();
    var repository = Substitute.For<IUserRepository>();
    var service = new UserService(repository, mockEmailService);
    
    // Act
    service.RegisterUser("john@example.com", "John");
    
    // Assert - Mock：驗證特定的互動行為
    mockEmailService.Received(1).SendWelcomeEmail("john@example.com", "John");
}
```

## NSubstitute 核心功能

### 基本替代語法

```csharp
// 建立介面替代
var substitute = Substitute.For<IUserRepository>();

// 建立類別替代（需要虛擬成員）
var classSubstitute = Substitute.For<BaseService>();

// 建立多重介面替代
var multiSubstitute = Substitute.For<IService, IDisposable>();
```

### 回傳值設定

#### 基本回傳值

```csharp
// 精確參數匹配
_repository.GetById(1).Returns(new User { Id = 1, Name = "John" });

// 任意參數匹配
_service.Process(Arg.Any<string>()).Returns("processed");

// 回傳序列值
_generator.GetNext().Returns(1, 2, 3, 4, 5);
```

#### 條件回傳值

```csharp
// 使用委派計算回傳值
_calculator.Add(Arg.Any<int>(), Arg.Any<int>())
           .Returns(x => (int)x[0] + (int)x[1]);

// 條件匹配
_service.Process(Arg.Is<string>(x => x.StartsWith("test")))
        .Returns("test-result");
```

#### 拋出例外

```csharp
// 同步方法拋出例外
_service.RiskyOperation()
        .Throws(new InvalidOperationException("Something went wrong"));

// 非同步方法拋出例外
_service.RiskyOperationAsync()
        .Throws(new InvalidOperationException("Async operation failed"));
```

### 引數匹配器

```csharp
// 任意值
_service.Process(Arg.Any<string>()).Returns("result");

// 特定條件
_service.Process(Arg.Is<string>(x => x.Length > 5)).Returns("long-result");

// 引數擷取
string capturedArg = null;
_service.Process(Arg.Do<string>(x => capturedArg = x)).Returns("result");
_service.Process("test");
capturedArg.Should().Be("test");

// 引數檢查
_service.Process(Arg.Is<string>(x =>
{
    x.Should().StartWith("prefix");
    return true;
})).Returns("result");
```

### 呼叫驗證

```csharp
// 驗證被呼叫（至少一次）
_service.Received().Process("test");

// 驗證呼叫次數
_service.Received(2).Process(Arg.Any<string>());

// 驗證未被呼叫
_service.DidNotReceive().Delete(Arg.Any<int>());

// 驗證任意參數呼叫
_service.ReceivedWithAnyArgs().Process(default);

// 驗證呼叫順序
Received.InOrder(() =>
{
    _service.Start();
    _service.Process();
    _service.Stop();
});
```

## 實戰模式

### 模式 1：依賴注入與測試設定

#### 被測試類別

```csharp
public class FileBackupService
{
    private readonly IFileSystem _fileSystem;
    private readonly IDateTimeProvider _dateTimeProvider;
    private readonly IBackupRepository _backupRepository;
    private readonly ILogger<FileBackupService> _logger;
    
    public FileBackupService(
        IFileSystem fileSystem,
        IDateTimeProvider dateTimeProvider,
        IBackupRepository backupRepository,
        ILogger<FileBackupService> logger)
    {
        _fileSystem = fileSystem;
        _dateTimeProvider = dateTimeProvider;
        _backupRepository = backupRepository;
        _logger = logger;
    }
    
    public async Task<BackupResult> BackupFileAsync(string sourcePath, string destinationPath)
    {
        if (!_fileSystem.FileExists(sourcePath))
        {
            _logger.LogWarning("Source file not found: {Path}", sourcePath);
            return new BackupResult { Success = false, Message = "Source file not found" };
        }
        
        var fileInfo = _fileSystem.GetFileInfo(sourcePath);
        if (fileInfo.Length > 100 * 1024 * 1024)
        {
            return new BackupResult { Success = false, Message = "File too large" };
        }
        
        var timestamp = _dateTimeProvider.Now.ToString("yyyyMMdd_HHmmss");
        var backupFileName = $"{Path.GetFileNameWithoutExtension(sourcePath)}_{timestamp}{Path.GetExtension(sourcePath)}";
        var fullBackupPath = Path.Combine(destinationPath, backupFileName);
        
        _fileSystem.CopyFile(sourcePath, fullBackupPath);
        await _backupRepository.SaveBackupHistory(sourcePath, fullBackupPath, _dateTimeProvider.Now);
        
        _logger.LogInformation("Backup completed: {Path}", fullBackupPath);
        
        return new BackupResult { Success = true, BackupPath = fullBackupPath };
    }
}
```

#### 測試類別設定

```csharp
public class FileBackupServiceTests
{
    private readonly IFileSystem _fileSystem;
    private readonly IDateTimeProvider _dateTimeProvider;
    private readonly IBackupRepository _backupRepository;
    private readonly ILogger<FileBackupService> _logger;
    private readonly FileBackupService _sut; // System Under Test
    
    public FileBackupServiceTests()
    {
        _fileSystem = Substitute.For<IFileSystem>();
        _dateTimeProvider = Substitute.For<IDateTimeProvider>();
        _backupRepository = Substitute.For<IBackupRepository>();
        _logger = Substitute.For<ILogger<FileBackupService>>();
        
        _sut = new FileBackupService(_fileSystem, _dateTimeProvider, _backupRepository, _logger);
    }
    
    [Fact]
    public async Task BackupFileAsync_檔案存在且大小合理_應成功備份()
    {
        // Arrange
        var sourcePath = @"C:\source\test.txt";
        var destinationPath = @"C:\backup";
        var testTime = new DateTime(2024, 1, 1, 12, 0, 0);
        
        _fileSystem.FileExists(sourcePath).Returns(true);
        _fileSystem.GetFileInfo(sourcePath).Returns(new FileInfo { Length = 1024 });
        _dateTimeProvider.Now.Returns(testTime);
        
        // Act
        var result = await _sut.BackupFileAsync(sourcePath, destinationPath);
        
        // Assert
        result.Success.Should().BeTrue();
        result.BackupPath.Should().Be(@"C:\backup\test_20240101_120000.txt");
        
        _fileSystem.Received(1).CopyFile(sourcePath, result.BackupPath);
        await _backupRepository.Received(1).SaveBackupHistory(
            sourcePath, result.BackupPath, testTime);
    }
}
```

### 模式 2：Mock vs Stub 的實戰差異

#### Stub：關注狀態

```csharp
[Fact]
public void CalculateDiscount_高級會員_應回傳20折扣()
{
    // Stub：只關心回傳值，用於設定測試情境
    var stubCustomerService = Substitute.For<ICustomerService>();
    stubCustomerService.GetCustomerType(123).Returns(CustomerType.Premium);
    
    var service = new PricingService(stubCustomerService);
    
    // Act
    var discount = service.CalculateDiscount(123, 1000);
    
    // Assert - 只驗證結果狀態
    discount.Should().Be(200); // 20% of 1000
}
```

#### Mock：關注行為

```csharp
[Fact]
public void ProcessPayment_成功付款_應記錄交易資訊()
{
    // Mock：關心是否正確互動
    var mockLogger = Substitute.For<ILogger<PaymentService>>();
    var stubPaymentGateway = Substitute.For<IPaymentGateway>();
    stubPaymentGateway.ProcessPayment(Arg.Any<decimal>()).Returns(PaymentResult.Success);
    
    var service = new PaymentService(stubPaymentGateway, mockLogger);
    
    // Act
    service.ProcessPayment(100);
    
    // Assert - 驗證互動行為
    mockLogger.Received(1).LogInformation(
        "Payment processed: {Amount} - Result: {Result}", 
        100, 
        PaymentResult.Success);
}
```

### 模式 3：非同步方法測試

```csharp
[Fact]
public async Task GetUserAsync_使用者存在_應回傳使用者資料()
{
    // Arrange
    var repository = Substitute.For<IUserRepository>();
    repository.GetByIdAsync(123).Returns(Task.FromResult(
        new User { Id = 123, Name = "John" }));
    
    var service = new UserService(repository);
    
    // Act
    var result = await service.GetUserAsync(123);
    
    // Assert
    result.Name.Should().Be("John");
    await repository.Received(1).GetByIdAsync(123);
}

[Fact]
public async Task SaveUserAsync_資料庫錯誤_應拋出例外()
{
    // Arrange
    var repository = Substitute.For<IUserRepository>();
    repository.SaveAsync(Arg.Any<User>())
              .Throws(new InvalidOperationException("Database error"));
    
    var service = new UserService(repository);
    
    // Act & Assert
    await service.SaveUserAsync(new User { Name = "John" })
                .Should().ThrowAsync<InvalidOperationException>()
                .WithMessage("Database error");
}
```

### 模式 4：ILogger 驗證

由於 ILogger 的擴展方法特性，需要驗證底層的 Log 方法：

```csharp
[Fact]
public async Task BackupFileAsync_檔案不存在_應記錄警告()
{
    // Arrange
    var sourcePath = @"C:\nonexistent\test.txt";
    _fileSystem.FileExists(sourcePath).Returns(false);
    
    // Act
    var result = await _sut.BackupFileAsync(sourcePath, @"C:\backup");
    
    // Assert
    result.Success.Should().BeFalse();
    
    // 驗證 ILogger.Log 方法被正確呼叫
    _logger.Received(1).Log(
        LogLevel.Warning,
        Arg.Any<EventId>(),
        Arg.Is<object>(v => v.ToString().Contains("Source file not found")),
        null,
        Arg.Any<Func<object, Exception, string>>());
}
```

### 模式 5：複雜設定管理

使用基底測試類別管理共用設定：

```csharp
public class OrderServiceTestsBase
{
    protected readonly IOrderRepository Repository;
    protected readonly IEmailService EmailService;
    protected readonly ILogger<OrderService> Logger;
    protected readonly OrderService Sut;
    
    protected OrderServiceTestsBase()
    {
        Repository = Substitute.For<IOrderRepository>();
        EmailService = Substitute.For<IEmailService>();
        Logger = Substitute.For<ILogger<OrderService>>();
        Sut = new OrderService(Repository, EmailService, Logger);
    }
    
    protected void SetupValidOrder(int orderId = 1)
    {
        Repository.GetById(orderId).Returns(
            new Order { Id = orderId, Status = OrderStatus.Pending });
    }
    
    protected void SetupEmailServiceSuccess()
    {
        EmailService.SendConfirmation(Arg.Any<string>()).Returns(true);
    }
}

public class OrderServiceTests : OrderServiceTestsBase
{
    [Fact]
    public void ProcessOrder_有效訂單_應成功處理()
    {
        // Arrange
        SetupValidOrder();
        SetupEmailServiceSuccess();
        
        // Act
        var result = Sut.ProcessOrder(1);
        
        // Assert
        result.Success.Should().BeTrue();
    }
}
```

## 引數匹配進階技巧

### 複雜物件匹配

```csharp
[Fact]
public void CreateOrder_建立訂單_應儲存正確的訂單資料()
{
    var repository = Substitute.For<IOrderRepository>();
    var service = new OrderService(repository);
    
    service.CreateOrder("Product A", 5, 100);
    
    // 驗證物件屬性
    repository.Received(1).Save(Arg.Is<Order>(o =>
        o.ProductName == "Product A" &&
        o.Quantity == 5 &&
        o.Price == 100));
}
```

### 引數擷取與驗證

```csharp
[Fact]
public void RegisterUser_註冊使用者_應產生正確的雜湊密碼()
{
    var repository = Substitute.For<IUserRepository>();
    var service = new UserService(repository);
    
    User capturedUser = null;
    repository.Save(Arg.Do<User>(u => capturedUser = u));
    
    service.RegisterUser("john@example.com", "password123");
    
    capturedUser.Should().NotBeNull();
    capturedUser.Email.Should().Be("john@example.com");
    capturedUser.PasswordHash.Should().NotBe("password123"); // 應該被雜湊
    capturedUser.PasswordHash.Length.Should().BeGreaterThan(20);
}
```

## 常見陷阱與最佳實踐

### ✅ 推薦做法

1. **針對介面而非實作建立 Substitute**

    ```csharp
    // ✅ 正確：針對介面
    var repository = Substitute.For<IUserRepository>();

    // ❌ 錯誤：針對具體類別（除非有虛擬成員）
    var repository = Substitute.For<UserRepository>();
    ```

2. **使用有意義的測試資料**

    ```csharp
    // ✅ 正確：清楚表達意圖
    var user = new User { Id = 123, Name = "John Doe", Email = "john@example.com" };

    // ❌ 錯誤：無意義的資料
    var user = new User { Id = 1, Name = "test", Email = "a@b.c" };
    ```

3. **避免過度驗證**

    ```csharp
    // ✅ 正確：只驗證重要的行為
    _emailService.Received(1).SendWelcomeEmail(Arg.Any<string>());

    // ❌ 錯誤：驗證所有內部實作細節
    _repository.Received(1).GetById(123);
    _repository.Received(1).Update(Arg.Any<User>());
    _validator.Received(1).Validate(Arg.Any<User>());
    ```

4. **Mock 與 Stub 的明確區分**

    ```csharp
    // ✅ 正確：Stub 用於設定情境，Mock 用於驗證行為
    var stubRepository = Substitute.For<IUserRepository>(); // Stub
    var mockLogger = Substitute.For<ILogger>(); // Mock

    stubRepository.GetById(123).Returns(user);
    service.ProcessUser(123);
    mockLogger.Received(1).LogInformation(Arg.Any<string>());
    ```

### ❌ 避免做法

1. **避免模擬值類型**

    ```csharp
    // ❌ 錯誤：DateTime 是值類型
    var badDate = Substitute.For<DateTime>();

    // ✅ 正確：抽象時間提供者
    var dateTimeProvider = Substitute.For<IDateTimeProvider>();
    dateTimeProvider.Now.Returns(new DateTime(2024, 1, 1));
    ```

2. **避免測試與實作強耦合**

    ```csharp
    // ❌ 錯誤：測試實作細節
    _repository.Received(1).Query(Arg.Any<string>());
    _repository.Received(1).Filter(Arg.Any<Expression<Func<User, bool>>>());

    // ✅ 正確：測試行為結果
    var users = service.GetActiveUsers();
    users.Should().HaveCount(2);
    ```

3. **避免設定過於複雜**

    ```csharp
    // ❌ 錯誤：過多的 Substitute（可能違反 SRP）
    var sub1 = Substitute.For<IService1>();
    var sub2 = Substitute.For<IService2>();
    var sub3 = Substitute.For<IService3>();
    var sub4 = Substitute.For<IService4>();

    // ✅ 正確：重新思考類別職責
    // 考慮是否違反單一職責原則，需要重構
    ```

## 識別需要替代的相依性

### 應該替代的

- ✅ 外部 API 呼叫（IHttpClient、IApiClient）
- ✅ 資料庫操作（IRepository、IDbContext）
- ✅ 檔案系統操作（IFileSystem）
- ✅ 網路通訊（IEmailService、IMessageQueue）
- ✅ 時間依賴（IDateTimeProvider、TimeProvider）
- ✅ 隨機數產生（IRandom）
- ✅ 昂貴的計算（IComplexCalculator）
- ✅ 記錄服務（ILogger<T>）

### 不應該替代的

- ❌ 值物件（DateTime、string、int）
- ❌ 簡單的資料傳輸物件（DTO）
- ❌ 純函數工具（如 AutoMapper 的 IMapper，考慮使用真實實例）
- ❌ 框架核心類別（除非有明確需求）

## 疑難排解

### Q1: 如何測試沒有介面的類別？

**A:** 確保要模擬的成員是 virtual：

```csharp
public class BaseService
{
    public virtual string GetData() => "real data";
}

var substitute = Substitute.For<BaseService>();
substitute.GetData().Returns("test data");
```

### Q2: 如何驗證方法被呼叫的順序？

**A:** 使用 Received.InOrder()：

```csharp
Received.InOrder(() =>
{
    _service.Start();
    _service.Process();
    _service.Stop();
});
```

### Q3: 如何處理 out 參數？

**A:** 使用 Returns() 配合委派：

```csharp
_service.TryGetValue("key", out Arg.Any<string>())
        .Returns(x =>
        {
            x[1] = "value";
            return true;
        });
```

### Q4: NSubstitute 與 Moq 該如何選擇？

**A:** NSubstitute 優勢：

- 語法更簡潔直觀
- 學習曲線平緩
- 沒有隱私爭議
- 對多數測試場景足夠

選擇 NSubstitute，除非：

- 專案已使用 Moq
- 需要 Moq 特有的進階功能
- 團隊已熟悉 Moq 語法

## 與其他技能整合

此技能可與以下技能組合使用：

- **unit-test-fundamentals**: 單元測試基礎與 3A 模式
- **dependency-injection-testing**: 依賴注入測試策略
- **test-naming-conventions**: 測試命名規範
- **test-output-logging**: ITestOutputHelper 與 ILogger 整合
- **datetime-testing-timeprovider**: TimeProvider 抽象化時間依賴
- **filesystem-testing-abstractions**: 檔案系統依賴抽象化

## 範本檔案參考

本技能提供以下範本檔案：

- `templates/mock-patterns.cs`: 完整的 Mock/Stub/Spy 模式範例
- `templates/verification-examples.cs`: 行為驗證與引數匹配範例

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 07 - 依賴替代入門：使用 NSubstitute**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10374508
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day07

### NSubstitute 官方

- [NSubstitute 官方網站](https://nsubstitute.github.io/)
- [NSubstitute GitHub](https://github.com/nsubstitute/NSubstitute)
- [NSubstitute NuGet](https://www.nuget.org/packages/NSubstitute/)

### Test Double 理論

- [XUnit Test Patterns](http://xunitpatterns.com/Test%20Double.html)
- [Martin Fowler - Test Double](https://martinfowler.com/bliki/TestDouble.html)
