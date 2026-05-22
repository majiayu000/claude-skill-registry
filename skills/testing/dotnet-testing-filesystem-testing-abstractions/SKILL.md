---
name: dotnet-testing-filesystem-testing-abstractions
description: |
  使用 System.IO.Abstractions 測試檔案系統操作的專門技能。當需要測試 File、Directory、Path 等操作、模擬檔案系統時使用。涵蓋 IFileSystem、MockFileSystem、檔案讀寫測試、目錄操作測試等。
  Keywords: file testing, filesystem, 檔案測試, 檔案系統測試, IFileSystem, MockFileSystem, System.IO.Abstractions, File.ReadAllText, File.WriteAllText, Directory.CreateDirectory, Path.Combine, mock file system, 檔案抽象化
license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: ".NET, testing, IFileSystem, MockFileSystem, file testing"
---

# 檔案系統測試：使用 System.IO.Abstractions 模擬檔案操作

## 適用情境

當被要求執行以下任務時，請使用此技能：

- 重構直接使用 `System.IO.File`、`System.IO.Directory` 等靜態類別的程式碼
- 為涉及檔案讀寫、目錄操作的程式碼撰寫單元測試
- 使用 MockFileSystem 模擬各種檔案系統狀態
- 測試檔案權限不足、檔案不存在等異常情境
- 設計可測試的檔案處理服務架構

## 核心原則

### 1. 檔案系統相依性的根本問題

傳統直接使用 `System.IO` 靜態類別的程式碼難以測試，原因包括：

- **速度問題**：實際磁碟 IO 比記憶體操作慢 10-100 倍
- **環境相依**：測試結果受檔案系統狀態、權限、路徑影響
- **副作用**：測試會在磁碟上留下痕跡，影響其他測試
- **並行問題**：多個測試同時操作同一檔案會產生競爭條件
- **錯誤模擬困難**：難以模擬權限不足、磁碟空間不足等異常

### 2. System.IO.Abstractions 解決方案

這是一個將 System.IO 靜態類別包裝成介面的套件，支援依賴注入和測試替身。

**核心介面架構**：

```csharp
public interface IFileSystem
{
    IFile File { get; }
    IDirectory Directory { get; }
    IFileInfo FileInfo { get; }
    IDirectoryInfo DirectoryInfo { get; }
    IPath Path { get; }
    IDriveInfo DriveInfo { get; }
}
```

**必要 NuGet 套件**：

```xml
<!-- 正式環境 -->
<PackageReference Include="System.IO.Abstractions" Version="21.*" />

<!-- 測試專案 -->
<PackageReference Include="System.IO.Abstractions.TestingHelpers" Version="21.*" />
```

### 3. 重構步驟

**步驟一**：將直接使用靜態類別的程式碼改為依賴 `IFileSystem`

```csharp
// ❌ 重構前（不可測試）
public class ConfigService
{
    public string LoadConfig(string path)
    {
        return File.ReadAllText(path);
    }
}

// ✅ 重構後（可測試）
public class ConfigService
{
    private readonly IFileSystem _fileSystem;
    
    public ConfigService(IFileSystem fileSystem)
    {
        _fileSystem = fileSystem;
    }
    
    public string LoadConfig(string path)
    {
        return _fileSystem.File.ReadAllText(path);
    }
}
```

**步驟二**：在 DI 容器中註冊真實實作

```csharp
// Program.cs
services.AddSingleton<IFileSystem, FileSystem>();
services.AddScoped<ConfigService>();
```

**步驟三**：在測試中使用 MockFileSystem

```csharp
var mockFs = new MockFileSystem(new Dictionary<string, MockFileData>
{
    ["config.json"] = new MockFileData("{ \"key\": \"value\" }")
});
var service = new ConfigService(mockFs);
```

## MockFileSystem 測試模式

### 模式一：預設檔案狀態

```csharp
[Fact]
public async Task LoadConfig_檔案存在_應回傳內容()
{
    // Arrange - 建立預設的檔案系統狀態
    var mockFileSystem = new MockFileSystem(new Dictionary<string, MockFileData>
    {
        ["config.json"] = new MockFileData("{ \"key\": \"value\" }"),
        [@"C:\data\users.csv"] = new MockFileData("Name,Age\nJohn,25"),
        [@"C:\logs\"] = new MockDirectoryData()  // 空目錄
    });
    
    var service = new ConfigService(mockFileSystem);
    
    // Act
    var result = await service.LoadConfigAsync("config.json");
    
    // Assert
    result.Should().Contain("key");
}
```

### 模式二：驗證寫入結果

```csharp
[Fact]
public async Task SaveConfig_指定內容_應正確寫入()
{
    // Arrange
    var mockFileSystem = new MockFileSystem();
    var service = new ConfigService(mockFileSystem);
    
    // Act
    await service.SaveConfigAsync("output.json", "{ \"saved\": true }");
    
    // Assert - 驗證檔案系統的最終狀態
    mockFileSystem.File.Exists("output.json").Should().BeTrue();
    var content = await mockFileSystem.File.ReadAllTextAsync("output.json");
    content.Should().Contain("saved");
}
```

### 模式三：測試目錄操作

```csharp
[Fact]
public void CopyFile_目標目錄不存在_應自動建立()
{
    // Arrange
    var mockFileSystem = new MockFileSystem(new Dictionary<string, MockFileData>
    {
        [@"C:\source\file.txt"] = new MockFileData("content")
    });
    var service = new FileManagerService(mockFileSystem);
    
    // Act
    service.CopyFileToDirectory(@"C:\source\file.txt", @"C:\target\subfolder");
    
    // Assert
    mockFileSystem.Directory.Exists(@"C:\target\subfolder").Should().BeTrue();
    mockFileSystem.File.Exists(@"C:\target\subfolder\file.txt").Should().BeTrue();
}
```

### 模式四：使用 NSubstitute 模擬錯誤

當需要模擬特定異常時，MockFileSystem 支援有限，可使用 NSubstitute：

```csharp
[Fact]
public void TryReadFile_權限不足_應回傳False()
{
    // Arrange
    var mockFileSystem = Substitute.For<IFileSystem>();
    var mockFile = Substitute.For<IFile>();
    
    mockFileSystem.File.Returns(mockFile);
    mockFile.Exists("protected.txt").Returns(true);
    mockFile.ReadAllText("protected.txt")
            .Throws(new UnauthorizedAccessException("存取被拒"));
    
    var service = new FilePermissionService(mockFileSystem);
    
    // Act
    var result = service.TryReadFile("protected.txt", out var content);
    
    // Assert
    result.Should().BeFalse();
    content.Should().BeNull();
}
```

## 進階測試技巧

### 串流操作測試

```csharp
[Fact]
public async Task CountLines_多行檔案_應回傳正確行數()
{
    // Arrange
    var content = "Line 1\nLine 2\nLine 3\nLine 4";
    var mockFileSystem = new MockFileSystem(new Dictionary<string, MockFileData>
    {
        ["data.txt"] = new MockFileData(content)
    });
    
    var processor = new StreamProcessorService(mockFileSystem);
    
    // Act
    var result = await processor.CountLinesAsync("data.txt");
    
    // Assert
    result.Should().Be(4);
}
```

### 檔案資訊測試

```csharp
[Fact]
public void GetFileInfo_檔案存在_應回傳正確資訊()
{
    // Arrange
    var content = "Hello, World!";
    var mockFileSystem = new MockFileSystem(new Dictionary<string, MockFileData>
    {
        [@"C:\test.txt"] = new MockFileData(content)
    });
    
    var service = new FileManagerService(mockFileSystem);
    
    // Act
    var info = service.GetFileInfo(@"C:\test.txt");
    
    // Assert
    info.Should().NotBeNull();
    info!.Name.Should().Be("test.txt");
    info.Size.Should().Be(content.Length);
}
```

### 備份檔案測試

```csharp
[Fact]
public void BackupFile_檔案存在_應建立時間戳記備份()
{
    // Arrange
    var mockFileSystem = new MockFileSystem(new Dictionary<string, MockFileData>
    {
        [@"C:\data\important.txt"] = new MockFileData("重要資料")
    });
    
    var service = new FileManagerService(mockFileSystem);
    
    // Act
    var backupPath = service.BackupFile(@"C:\data\important.txt");
    
    // Assert
    backupPath.Should().StartWith(@"C:\data\important_");
    backupPath.Should().EndWith(".txt");
    mockFileSystem.File.Exists(backupPath).Should().BeTrue();
}
```

## 最佳實踐

### ✅ 應該這樣做

1. **使用 Path.Combine 處理路徑**：

   ```csharp
   var path = _fileSystem.Path.Combine("configs", "app.json");
   ```

2. **防禦性檢查檔案存在性**：

   ```csharp
   if (!_fileSystem.File.Exists(filePath))
   {
       return defaultValue;
   }
   ```

3. **自動建立必要目錄**：

   ```csharp
   var dir = _fileSystem.Path.GetDirectoryName(filePath);
   if (!string.IsNullOrEmpty(dir) && !_fileSystem.Directory.Exists(dir))
   {
       _fileSystem.Directory.CreateDirectory(dir);
   }
   ```

4. **妥善處理各種 IO 異常**：

   ```csharp
   try
   {
       return await _fileSystem.File.ReadAllTextAsync(path);
   }
   catch (UnauthorizedAccessException) { /* 權限不足 */ }
   catch (IOException) { /* 檔案被鎖定 */ }
   catch (DirectoryNotFoundException) { /* 目錄不存在 */ }
   ```

5. **每個測試使用獨立的 MockFileSystem**：

   ```csharp
   public class ServiceTests
   {
       [Fact]
       public void Test1()
       {
           var mockFs = new MockFileSystem(); // 獨立實例
       }
       
       [Fact]
       public void Test2()
       {
           var mockFs = new MockFileSystem(); // 獨立實例
       }
   }
   ```

### ❌ 應該避免

1. **硬編碼路徑分隔符號**：

   ```csharp
   // ❌ 不要這樣做
   var path = "configs\\app.json";  // Windows only
   var path = "configs/app.json";   // Unix only
   
   // ✅ 應該這樣做
   var path = _fileSystem.Path.Combine("configs", "app.json");
   ```

2. **在單元測試中使用真實檔案系統**：

   ```csharp
   // ❌ 這不是單元測試
   var realFs = new FileSystem();
   
   // ✅ 單元測試應使用 MockFileSystem
   var mockFs = new MockFileSystem();
   ```

3. **忽略例外處理**：

   ```csharp
   // ❌ 不要假設檔案一定存在
   var content = _fileSystem.File.ReadAllText(path);
   
   // ✅ 加入存在性檢查和例外處理
   if (_fileSystem.File.Exists(path))
   {
       try { return _fileSystem.File.ReadAllText(path); }
       catch (IOException) { return defaultValue; }
   }
   ```

## 效能考量

### MockFileSystem 優勢

- **速度**：比真實檔案操作快 10-100 倍
- **可靠性**：不受磁碟狀態影響
- **隔離性**：測試之間完全隔離
- **錯誤模擬**：可精確模擬各種異常情境

### 記憶體使用建議

- 只建立測試必需的檔案
- 避免在測試中模擬超大檔案
- 對於大檔案處理邏輯，使用適度大小的測試資料：

```csharp
// ✅ 適度大小的測試資料
var testContent = string.Join("\n", 
    Enumerable.Range(1, 1000).Select(i => $"Line {i}"));
mockFileSystem.AddFile("test.txt", new MockFileData(testContent));
```

## 實務整合範例

### 設定檔管理服務

請參考 `templates/configmanager-service.cs` 中的完整實作，包含：

- 設定檔載入與儲存
- JSON 序列化與反序列化
- 自動建立目錄
- 設定檔備份功能

### 檔案管理服務

請參考 `templates/filemanager-service.cs` 中的實作，包含：

- 檔案複製與備份
- 目錄操作
- 檔案資訊查詢
- 錯誤處理模式

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 17 - 檔案與 IO 測試：使用 System.IO.Abstractions 模擬檔案系統**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10375981
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day17

### 官方文件

- [System.IO.Abstractions GitHub](https://github.com/TestableIO/System.IO.Abstractions)
- [System.IO.Abstractions NuGet](https://www.nuget.org/packages/System.IO.Abstractions/)
- [TestingHelpers NuGet](https://www.nuget.org/packages/System.IO.Abstractions.TestingHelpers/)

### 相關技能

- `nsubstitute-mocking` - 測試替身與模擬
- `unit-test-fundamentals` - 單元測試基礎
