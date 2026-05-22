---
name: dotnet-testing-fluentvalidation-testing
description: |
  測試 FluentValidation 驗證器的專門技能。當需要為 Validator 類別建立測試、驗證業務規則、測試錯誤訊息時使用。涵蓋 FluentValidation.TestHelper 完整使用、ShouldHaveValidationErrorFor、非同步驗證、跨欄位邏輯等。
  Keywords: validator, 驗證器, fluentvalidation, validation testing, UserValidator, CreateOrderValidator, TestHelper, ShouldHaveValidationErrorFor, ShouldNotHaveValidationErrorFor, TestValidate, TestValidateAsync, 測試驗證器, 驗證業務規則
license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: ".NET, testing, FluentValidation, validator, validation"
---

# FluentValidation Testing Skill

## 技能說明

此技能專注於使用 FluentValidation.TestHelper 測試資料驗證邏輯，涵蓋基本驗證、複雜業務規則、非同步驗證和測試最佳實踐。

## 為什麼要測試驗證器？

驗證器是應用程式的第一道防線，測試驗證器能：

1. **確保資料完整性** - 防止無效資料進入系統
2. **業務規則文件化** - 測試即活文件，清楚展示業務規則
3. **安全性保障** - 防止惡意或不當資料輸入
4. **重構安全網** - 業務規則變更時提供保障
5. **跨欄位邏輯驗證** - 確保複雜邏輯正確運作

## 前置需求

### 套件安裝

```xml
<PackageReference Include="FluentValidation" Version="11.11.0" />
<PackageReference Include="FluentValidation.TestHelper" Version="11.11.0" />
<PackageReference Include="xunit" Version="2.9.3" />
<PackageReference Include="Microsoft.Extensions.Time.Testing" Version="9.0.0" />
<PackageReference Include="NSubstitute" Version="5.3.0" />
<PackageReference Include="AwesomeAssertions" Version="9.1.0" />
```

### 基本 using 指令

```csharp
using FluentValidation;
using FluentValidation.TestHelper;
using Microsoft.Extensions.Time.Testing;
using NSubstitute;
using Xunit;
using AwesomeAssertions;
```

## 核心測試模式

### 模式 1：基本欄位驗證

#### 驗證器範例

```csharp
public class UserValidator : AbstractValidator<UserRegistrationRequest>
{
    public UserValidator()
    {
        RuleFor(x => x.Username)
            .NotEmpty().WithMessage("使用者名稱不可為 null 或空白")
            .Length(3, 20).WithMessage("使用者名稱長度必須在 3 到 20 個字元之間")
            .Matches(@"^[a-zA-Z0-9_]+$").WithMessage("使用者名稱只能包含字母、數字和底線");

        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("電子郵件不可為 null 或空白")
            .EmailAddress().WithMessage("電子郵件格式不正確")
            .MaximumLength(100).WithMessage("電子郵件長度不能超過 100 個字元");

        RuleFor(x => x.Age)
            .GreaterThanOrEqualTo(18).WithMessage("年齡必須大於或等於 18 歲")
            .LessThanOrEqualTo(120).WithMessage("年齡必須小於或等於 120 歲");
    }
}
```

#### 測試範例

```csharp
public class UserValidatorTests
{
    private readonly UserValidator _validator;

    public UserValidatorTests()
    {
        _validator = new UserValidator();
    }

    [Fact]
    public void Validate_有效使用者名稱_應該通過驗證()
    {
        // Arrange
        var request = new UserRegistrationRequest { Username = "valid_user123" };

        // Act
        var result = _validator.TestValidate(request);

        // Assert
        result.ShouldNotHaveValidationErrorFor(x => x.Username);
    }

    [Fact]
    public void Validate_空白使用者名稱_應該驗證失敗()
    {
        // Arrange
        var request = new UserRegistrationRequest { Username = "" };

        // Act
        var result = _validator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Username)
              .WithErrorMessage("使用者名稱不可為 null 或空白");
    }
}
```

### 模式 2：參數化測試

```csharp
[Theory]
[InlineData("", "使用者名稱不可為 null 或空白")]
[InlineData("ab", "使用者名稱長度必須在 3 到 20 個字元之間")]
[InlineData("a_very_long_username_exceeds_limit", "使用者名稱長度必須在 3 到 20 個字元之間")]
[InlineData("user@name", "使用者名稱只能包含字母、數字和底線")]
public void Validate_無效使用者名稱_應該回傳對應錯誤(string username, string expectedError)
{
    // Arrange
    var request = new UserRegistrationRequest { Username = username };

    // Act
    var result = _validator.TestValidate(request);

    // Assert
    result.ShouldHaveValidationErrorFor(x => x.Username)
          .WithErrorMessage(expectedError);
}

[Theory]
[InlineData("user123")]
[InlineData("valid_user")]
[InlineData("TEST_User_99")]
public void Validate_有效使用者名稱_應該通過驗證(string username)
{
    // Arrange
    var request = new UserRegistrationRequest { Username = username };

    // Act
    var result = _validator.TestValidate(request);

    // Assert
    result.ShouldNotHaveValidationErrorFor(x => x.Username);
}
```

### 模式 3：跨欄位驗證

#### 密碼與確認密碼

```csharp
public class UserValidator : AbstractValidator<UserRegistrationRequest>
{
    public UserValidator()
    {
        RuleFor(x => x.Password)
            .NotEmpty().WithMessage("密碼不可為 null 或空白")
            .Length(8, 50).WithMessage("密碼長度必須在 8 到 50 個字元之間")
            .Must(BeComplexPassword).WithMessage("密碼必須包含大小寫字母和數字");

        RuleFor(x => x.ConfirmPassword)
            .Equal(x => x.Password).WithMessage("確認密碼必須與密碼相同");
    }

    private bool BeComplexPassword(string password)
    {
        return !string.IsNullOrEmpty(password) && 
               Regex.IsMatch(password, @"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$");
    }
}
```

#### 測試範例

```csharp
[Fact]
public void Validate_密碼與確認密碼不一致_應該驗證失敗()
{
    // Arrange
    var request = new UserRegistrationRequest
    {
        Password = "Password123",
        ConfirmPassword = "DifferentPass456"
    };

    // Act
    var result = _validator.TestValidate(request);

    // Assert
    result.ShouldHaveValidationErrorFor(x => x.ConfirmPassword)
          .WithErrorMessage("確認密碼必須與密碼相同");
}

[Theory]
[InlineData("weak", "密碼長度必須在 8 到 50 個字元之間")]
[InlineData("weakpass", "密碼必須包含大小寫字母和數字")]
[InlineData("WEAKPASS123", "密碼必須包含大小寫字母和數字")]
public void Validate_弱密碼_應該驗證失敗(string password, string expectedError)
{
    // Arrange
    var request = new UserRegistrationRequest
    {
        Password = password,
        ConfirmPassword = password
    };

    // Act
    var result = _validator.TestValidate(request);

    // Assert
    result.ShouldHaveValidationErrorFor(x => x.Password)
          .WithErrorMessage(expectedError);
}
```

### 模式 4：時間相依驗證

#### 年齡與生日一致性驗證

```csharp
public class UserValidator : AbstractValidator<UserRegistrationRequest>
{
    private readonly TimeProvider _timeProvider;

    public UserValidator(TimeProvider timeProvider)
    {
        _timeProvider = timeProvider;

        RuleFor(x => x.BirthDate)
            .Must((request, birthDate) => IsAgeConsistentWithBirthDate(birthDate, request.Age))
            .WithMessage("生日與年齡不一致");
    }

    private bool IsAgeConsistentWithBirthDate(DateTime birthDate, int age)
    {
        var currentDate = _timeProvider.GetLocalNow().Date;
        var calculatedAge = currentDate.Year - birthDate.Year;

        if (birthDate.Date > currentDate.AddYears(-calculatedAge))
        {
            calculatedAge--;
        }

        return calculatedAge == age;
    }
}
```

#### 測試範例

```csharp
public class UserValidatorTests
{
    private readonly FakeTimeProvider _fakeTimeProvider;
    private readonly UserValidator _validator;

    public UserValidatorTests()
    {
        _fakeTimeProvider = new FakeTimeProvider();
        _fakeTimeProvider.SetUtcNow(new DateTime(2024, 1, 1));
        _validator = new UserValidator(_fakeTimeProvider);
    }

    [Fact]
    public void Validate_年齡與生日一致_應該通過驗證()
    {
        // Arrange
        var request = new UserRegistrationRequest
        {
            BirthDate = new DateTime(1990, 1, 1),
            Age = 34 // 2024 - 1990 = 34
        };

        // Act
        var result = _validator.TestValidate(request);

        // Assert
        result.ShouldNotHaveValidationErrorFor(x => x.BirthDate);
    }

    [Fact]
    public void Validate_年齡與生日不一致_應該驗證失敗()
    {
        // Arrange
        var request = new UserRegistrationRequest
        {
            BirthDate = new DateTime(1990, 1, 1),
            Age = 25 // 錯誤的年齡
        };

        // Act
        var result = _validator.TestValidate(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.BirthDate)
              .WithErrorMessage("生日與年齡不一致");
    }

    [Fact]
    public void Validate_生日尚未到達_年齡計算應該正確()
    {
        // Arrange
        _fakeTimeProvider.SetUtcNow(new DateTime(2024, 2, 1));
        var validator = new UserValidator(_fakeTimeProvider);

        var request = new UserRegistrationRequest
        {
            BirthDate = new DateTime(1990, 6, 15), // 生日在今年尚未到達
            Age = 33 // 2024 - 1990 - 1 = 33
        };

        // Act
        var result = validator.TestValidate(request);

        // Assert
        result.ShouldNotHaveValidationErrorFor(x => x.BirthDate);
    }
}
```

### 模式 5：條件式驗證

#### 驗證器定義

```csharp
public class UserValidator : AbstractValidator<UserRegistrationRequest>
{
    public UserValidator()
    {
        // 電話號碼為可選，但如果有填就必須是有效格式
        RuleFor(x => x.PhoneNumber)
            .Matches(@"^09\d{8}$").WithMessage("電話號碼格式不正確")
            .When(x => !string.IsNullOrWhiteSpace(x.PhoneNumber));
    }
}
```

#### 測試範例

```csharp
[Fact]
public void Validate_電話號碼為空_應該跳過驗證()
{
    // Arrange
    var request = new UserRegistrationRequest { PhoneNumber = null };

    // Act
    var result = _validator.TestValidate(request);

    // Assert
    result.ShouldNotHaveValidationErrorFor(x => x.PhoneNumber);
}

[Fact]
public void Validate_電話號碼格式錯誤_應該驗證失敗()
{
    // Arrange
    var request = new UserRegistrationRequest { PhoneNumber = "123456789" };

    // Act
    var result = _validator.TestValidate(request);

    // Assert
    result.ShouldHaveValidationErrorFor(x => x.PhoneNumber)
          .WithErrorMessage("電話號碼格式不正確");
}

[Theory]
[InlineData("0912345678")]
[InlineData("0987654321")]
public void Validate_有效電話號碼_應該通過驗證(string phoneNumber)
{
    // Arrange
    var request = new UserRegistrationRequest { PhoneNumber = phoneNumber };

    // Act
    var result = _validator.TestValidate(request);

    // Assert
    result.ShouldNotHaveValidationErrorFor(x => x.PhoneNumber);
}
```

### 模式 6：非同步驗證

#### 驗證器定義

```csharp
public interface IUserService
{
    Task<bool> IsUsernameAvailableAsync(string username);
    Task<bool> IsEmailRegisteredAsync(string email);
}

public class UserAsyncValidator : AbstractValidator<UserRegistrationRequest>
{
    private readonly IUserService _userService;

    public UserAsyncValidator(IUserService userService)
    {
        _userService = userService;

        RuleFor(x => x.Username)
            .MustAsync(async (username, cancellation) =>
                await _userService.IsUsernameAvailableAsync(username))
            .WithMessage("使用者名稱已被使用");

        RuleFor(x => x.Email)
            .MustAsync(async (email, cancellation) =>
                !await _userService.IsEmailRegisteredAsync(email))
            .WithMessage("此電子郵件已被註冊");
    }
}
```

#### 測試範例

```csharp
public class UserAsyncValidatorTests
{
    private readonly IUserService _mockUserService;
    private readonly UserAsyncValidator _validator;

    public UserAsyncValidatorTests()
    {
        _mockUserService = Substitute.For<IUserService>();
        _validator = new UserAsyncValidator(_mockUserService);
    }

    [Fact]
    public async Task ValidateAsync_使用者名稱可用_應該通過驗證()
    {
        // Arrange
        var request = new UserRegistrationRequest { Username = "newuser123" };

        _mockUserService.IsUsernameAvailableAsync("newuser123")
                       .Returns(Task.FromResult(true));

        // Act
        var result = await _validator.TestValidateAsync(request);

        // Assert
        result.ShouldNotHaveValidationErrorFor(x => x.Username);
        await _mockUserService.Received(1).IsUsernameAvailableAsync("newuser123");
    }

    [Fact]
    public async Task ValidateAsync_使用者名稱已被使用_應該驗證失敗()
    {
        // Arrange
        var request = new UserRegistrationRequest { Username = "existinguser" };

        _mockUserService.IsUsernameAvailableAsync("existinguser")
                       .Returns(Task.FromResult(false));

        // Act
        var result = await _validator.TestValidateAsync(request);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Username)
              .WithErrorMessage("使用者名稱已被使用");
        await _mockUserService.Received(1).IsUsernameAvailableAsync("existinguser");
    }

    [Fact]
    public async Task ValidateAsync_外部服務拋出例外_應該正確處理()
    {
        // Arrange
        var request = new UserRegistrationRequest { Username = "testuser" };

        _mockUserService.IsUsernameAvailableAsync("testuser")
                       .Returns(Task.FromException<bool>(new TimeoutException("服務逾時")));

        // Act & Assert
        await _validator.TestValidateAsync(request)
                       .Should().ThrowAsync<TimeoutException>();
    }
}
```

### 模式 7：集合驗證

```csharp
public class UserValidator : AbstractValidator<UserRegistrationRequest>
{
    public UserValidator()
    {
        RuleFor(x => x.Roles)
            .NotEmpty().WithMessage("角色清單不可為 null 或空陣列")
            .Must(roles => roles == null || roles.All(role => IsValidRole(role)))
            .WithMessage("包含無效的角色");
    }

    private bool IsValidRole(string role)
    {
        var validRoles = new[] { "User", "Admin", "Manager", "Support" };
        return validRoles.Contains(role);
    }
}
```

#### 測試範例

```csharp
[Fact]
public void Validate_空的角色清單_應該驗證失敗()
{
    // Arrange
    var request = new UserRegistrationRequest { Roles = new List<string>() };

    // Act
    var result = _validator.TestValidate(request);

    // Assert
    result.ShouldHaveValidationErrorFor(x => x.Roles)
          .WithErrorMessage("角色清單不可為 null 或空陣列");
}

[Theory]
[InlineData("InvalidRole")]
[InlineData("SuperUser")]
public void Validate_無效角色_應該驗證失敗(string invalidRole)
{
    // Arrange
    var request = new UserRegistrationRequest
    {
        Roles = new List<string> { "User", invalidRole }
    };

    // Act
    var result = _validator.TestValidate(request);

    // Assert
    result.ShouldHaveValidationErrorFor(x => x.Roles)
          .WithErrorMessage("包含無效的角色");
}

[Theory]
[InlineData(new[] { "User" })]
[InlineData(new[] { "Admin" })]
[InlineData(new[] { "User", "Manager" })]
public void Validate_有效角色_應該通過驗證(string[] roles)
{
    // Arrange
    var request = new UserRegistrationRequest { Roles = roles.ToList() };

    // Act
    var result = _validator.TestValidate(request);

    // Assert
    result.ShouldNotHaveValidationErrorFor(x => x.Roles);
}
```

## FluentValidation.TestHelper 核心 API

### 測試方法

| 方法                       | 用途           | 範例                                          |
| -------------------------- | -------------- | --------------------------------------------- |
| `TestValidate(model)`      | 執行同步驗證   | `_validator.TestValidate(request)`            |
| `TestValidateAsync(model)` | 執行非同步驗證 | `await _validator.TestValidateAsync(request)` |

### 斷言方法

| 方法                                               | 用途                     | 範例                                                   |
| -------------------------------------------------- | ------------------------ | ------------------------------------------------------ |
| `ShouldHaveValidationErrorFor(x => x.Property)`    | 斷言該屬性應該有錯誤     | `result.ShouldHaveValidationErrorFor(x => x.Username)` |
| `ShouldNotHaveValidationErrorFor(x => x.Property)` | 斷言該屬性不應該有錯誤   | `result.ShouldNotHaveValidationErrorFor(x => x.Email)` |
| `ShouldNotHaveAnyValidationErrors()`               | 斷言整個物件沒有任何錯誤 | `result.ShouldNotHaveAnyValidationErrors()`            |

### 錯誤訊息驗證

| 方法                       | 用途             | 範例                                      |
| -------------------------- | ---------------- | ----------------------------------------- |
| `WithErrorMessage(string)` | 驗證錯誤訊息內容 | `.WithErrorMessage("使用者名稱不可為空")` |
| `WithErrorCode(string)`    | 驗證錯誤代碼     | `.WithErrorCode("NOT_EMPTY")`             |

## 測試最佳實踐

### ✅ 推薦做法

1. **使用參數化測試** - 用 Theory 測試多種輸入組合
2. **測試邊界值** - 特別注意邊界條件
3. **控制時間** - 使用 FakeTimeProvider 處理時間相依
4. **Mock 外部依賴** - 使用 NSubstitute 隔離外部服務
5. **建立輔助方法** - 統一管理測試資料
6. **清楚的測試命名** - 使用 `方法_情境_預期結果` 格式
7. **測試錯誤訊息** - 確保使用者看到正確的錯誤訊息

### ❌ 避免做法

1. **避免使用 DateTime.Now** - 會導致測試不穩定
2. **避免測試過度耦合** - 每個測試只驗證一個規則
3. **避免硬編碼測試資料** - 使用輔助方法建立
4. **避免忽略邊界條件** - 邊界值是最容易出錯的地方
5. **避免跳過錯誤訊息驗證** - 錯誤訊息是使用者體驗的一部分

## 常見測試場景

### 場景 1：Email 格式驗證

```csharp
[Theory]
[InlineData("", "電子郵件不可為 null 或空白")]
[InlineData("invalid", "電子郵件格式不正確")]
[InlineData("@example.com", "電子郵件格式不正確")]
public void Validate_無效Email_應該驗證失敗(string email, string expectedError)
{
    var request = new UserRegistrationRequest { Email = email };
    var result = _validator.TestValidate(request);
    result.ShouldHaveValidationErrorFor(x => x.Email).WithErrorMessage(expectedError);
}
```

### 場景 2：年齡範圍驗證

```csharp
[Theory]
[InlineData(17, "年齡必須大於或等於 18 歲")]
[InlineData(121, "年齡必須小於或等於 120 歲")]
public void Validate_無效年齡_應該驗證失敗(int age, string expectedError)
{
    var request = new UserRegistrationRequest { Age = age };
    var result = _validator.TestValidate(request);
    result.ShouldHaveValidationErrorFor(x => x.Age).WithErrorMessage(expectedError);
}
```

### 場景 3：必填欄位驗證

```csharp
[Fact]
public void Validate_未同意條款_應該驗證失敗()
{
    var request = new UserRegistrationRequest { AgreeToTerms = false };
    var result = _validator.TestValidate(request);
    result.ShouldHaveValidationErrorFor(x => x.AgreeToTerms)
          .WithErrorMessage("必須同意使用條款");
}
```

## 測試輔助工具

### 測試資料建構器

```csharp
public static class TestDataBuilder
{
    public static UserRegistrationRequest CreateValidRequest()
    {
        return new UserRegistrationRequest
        {
            Username = "testuser123",
            Email = "test@example.com",
            Password = "TestPass123",
            ConfirmPassword = "TestPass123",
            BirthDate = new DateTime(1990, 1, 1),
            Age = 34,
            PhoneNumber = "0912345678",
            Roles = new List<string> { "User" },
            AgreeToTerms = true
        };
    }

    public static UserRegistrationRequest WithUsername(this UserRegistrationRequest request, string username)
    {
        request.Username = username;
        return request;
    }

    public static UserRegistrationRequest WithEmail(this UserRegistrationRequest request, string email)
    {
        request.Email = email;
        return request;
    }
}

// 使用範例
var request = TestDataBuilder.CreateValidRequest()
                            .WithUsername("newuser")
                            .WithEmail("new@example.com");
```

## 與其他技能整合

此技能可與以下技能組合使用：

- **unit-test-fundamentals**: 單元測試基礎與 3A 模式
- **test-naming-conventions**: 測試命名規範
- **nsubstitute-mocking**: Mock 外部服務依賴
- **test-data-builder-pattern**: 建構複雜測試資料
- **datetime-testing-timeprovider**: 時間相依測試

## 疑難排解

### Q1: 如何測試需要資料庫查詢的驗證？

**A:** 使用 Mock 隔離資料庫依賴：

```csharp
_mockUserService.IsUsernameAvailableAsync("username")
                .Returns(Task.FromResult(false));
```

### Q2: 如何處理時間相關的驗證？

**A:** 使用 FakeTimeProvider 控制時間：

```csharp
_fakeTimeProvider.SetUtcNow(new DateTime(2024, 1, 1));
```

### Q3: 如何測試複雜的跨欄位驗證？

**A:** 分別測試每個條件，確保完整覆蓋：

```csharp
// 測試生日已過的情況
// 測試生日未到的情況
// 測試邊界日期
```

### Q4: 應該測試到什麼程度？

**A:** 重點測試：

- 每個驗證規則至少一個測試
- 邊界值和特殊情況
- 錯誤訊息正確性
- 跨欄位邏輯的所有組合

## 範本檔案參考

本技能提供以下範本檔案：

- `templates/validator-test-template.cs`: 完整的驗證器測試範例
- `templates/async-validator-examples.cs`: 非同步驗證範例

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 18 - 驗證測試：FluentValidation Test Extensions**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10376147
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day18

### 官方文件

- [FluentValidation Documentation](https://docs.fluentvalidation.net/)
- [FluentValidation.TestHelper](https://docs.fluentvalidation.net/en/latest/testing.html)
- [FluentValidation GitHub](https://github.com/FluentValidation/FluentValidation)

### 相關技能

- `unit-test-fundamentals` - 單元測試基礎
- `nsubstitute-mocking` - 測試替身與模擬
