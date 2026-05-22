---
name: testcontainers-nosql
description: 協助使用 Testcontainers 進行 MongoDB 與 Redis 的容器化整合測試。當使用者需要測試 NoSQL 資料庫操作、快取服務、文件查詢或五種 Redis 資料結構時使用此技能。
license: MIT
---

# Testcontainers NoSQL 整合測試指南

## 適用情境

當被要求執行以下任務時，請使用此技能：

- 使用 Testcontainers 測試 MongoDB 文件操作
- 使用 Testcontainers 測試 Redis 快取服務
- 建立 MongoDB Collection Fixture 共享容器
- 建立 Redis Collection Fixture 共享容器
- 測試 MongoDB BSON 序列化與複雜文件結構
- 測試 MongoDB 索引效能與唯一性約束
- 測試 Redis 五種資料結構（String、Hash、List、Set、Sorted Set）
- 實作 NoSQL 資料庫的資料隔離策略

## 核心概念

### NoSQL 測試的挑戰

NoSQL 資料庫測試與關聯式資料庫有顯著差異：

1. **文件模型複雜度**：MongoDB 支援巢狀物件、陣列、字典等複雜結構
2. **無固定 Schema**：需要透過測試驗證資料結構的一致性
3. **多樣化資料結構**：Redis 有五種主要資料結構，各有不同使用場景
4. **序列化處理**：BSON (MongoDB) 與 JSON (Redis) 序列化行為需要驗證

### Testcontainers 優勢

- **真實環境模擬**：使用實際的 MongoDB 7.0 和 Redis 7.2 容器
- **一致性測試**：測試結果直接反映正式環境行為
- **隔離性保證**：每個測試環境完全獨立
- **效能驗證**：可進行真實的索引效能測試

## 環境需求

### 必要套件

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <IsPackable>false</IsPackable>
  </PropertyGroup>

  <ItemGroup>
    <!-- MongoDB 相關套件 -->
    <PackageReference Include="MongoDB.Driver" Version="3.0.0" />
    <PackageReference Include="MongoDB.Bson" Version="3.0.0" />

    <!-- Redis 相關套件 -->
    <PackageReference Include="StackExchange.Redis" Version="2.8.16" />

    <!-- Testcontainers -->
    <PackageReference Include="Testcontainers" Version="4.0.0" />
    <PackageReference Include="Testcontainers.MongoDb" Version="4.0.0" />
    <PackageReference Include="Testcontainers.Redis" Version="4.0.0" />

    <!-- 測試框架 -->
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.12.0" />
    <PackageReference Include="xunit" Version="2.9.3" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
    <PackageReference Include="AwesomeAssertions" Version="9.1.0" />

    <!-- JSON 序列化與時間測試 -->
    <PackageReference Include="System.Text.Json" Version="9.0.0" />
    <PackageReference Include="Microsoft.Bcl.TimeProvider" Version="9.0.0" />
    <PackageReference Include="Microsoft.Extensions.TimeProvider.Testing" Version="9.0.0" />
  </ItemGroup>
</Project>
```

### 套件版本說明

| 套件                   | 版本   | 用途                               |
| ---------------------- | ------ | ---------------------------------- |
| MongoDB.Driver         | 3.0.0  | MongoDB 官方驅動程式，支援最新功能 |
| MongoDB.Bson           | 3.0.0  | BSON 序列化處理                    |
| StackExchange.Redis    | 2.8.16 | Redis 客戶端，支援 Redis 7.x       |
| Testcontainers.MongoDb | 4.0.0  | MongoDB 容器管理                   |
| Testcontainers.Redis   | 4.0.0  | Redis 容器管理                     |

---

## MongoDB 容器化測試

### MongoDB Container Fixture

使用 Collection Fixture 模式共享容器，節省 80% 以上的測試時間：

```csharp
using MongoDB.Driver;
using Testcontainers.MongoDb;

namespace YourProject.Integration.Tests.Fixtures;

/// <summary>
/// MongoDB 容器 Fixture - 實作 IAsyncLifetime 管理容器生命週期
/// </summary>
public class MongoDbContainerFixture : IAsyncLifetime
{
    private MongoDbContainer? _container;

    public IMongoDatabase Database { get; private set; } = null!;
    public string ConnectionString { get; private set; } = string.Empty;
    public string DatabaseName { get; } = "testdb";

    public async Task InitializeAsync()
    {
        // 使用 MongoDB 7.0 確保功能完整性
        _container = new MongoDbBuilder()
                     .WithImage("mongo:7.0")
                     .WithPortBinding(27017, true)
                     .Build();

        await _container.StartAsync();

        ConnectionString = _container.GetConnectionString();
        var client = new MongoClient(ConnectionString);
        Database = client.GetDatabase(DatabaseName);
    }

    public async Task DisposeAsync()
    {
        if (_container != null)
        {
            await _container.DisposeAsync();
        }
    }

    /// <summary>
    /// 清空資料庫中的所有集合 - 用於測試間隔離
    /// </summary>
    public async Task ClearDatabaseAsync()
    {
        var collections = await Database.ListCollectionNamesAsync();
        await collections.ForEachAsync(async collectionName =>
        {
            await Database.DropCollectionAsync(collectionName);
        });
    }
}

/// <summary>
/// 定義使用 MongoDB Fixture 的測試集合
/// </summary>
[CollectionDefinition("MongoDb Collection")]
public class MongoDbCollectionFixture : ICollectionFixture<MongoDbContainerFixture>
{
    // 此類別不需要實作，僅用於標記集合
}
```

### MongoDB 文件模型設計

建立包含巢狀物件、陣列、字典等複雜結構的文件模型：

```csharp
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace YourProject.Core.Models.Mongo;

/// <summary>
/// 使用者文件 - 展示 MongoDB 複雜文件結構
/// </summary>
public class UserDocument
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; } = string.Empty;

    [BsonElement("username")]
    [BsonRequired]
    public string Username { get; set; } = string.Empty;

    [BsonElement("email")]
    [BsonRequired]
    public string Email { get; set; } = string.Empty;

    [BsonElement("profile")]
    public UserProfile Profile { get; set; } = new();

    [BsonElement("addresses")]
    public List<Address> Addresses { get; set; } = new();

    [BsonElement("skills")]
    public List<Skill> Skills { get; set; } = new();

    [BsonElement("preferences")]
    public Dictionary<string, object> Preferences { get; set; } = new();

    [BsonElement("created_at")]
    [BsonDateTimeOptions(Kind = DateTimeKind.Utc)]
    public DateTime CreatedAt { get; set; }

    [BsonElement("updated_at")]
    [BsonDateTimeOptions(Kind = DateTimeKind.Utc)]
    public DateTime UpdatedAt { get; set; }

    [BsonElement("is_active")]
    public bool IsActive { get; set; } = true;

    [BsonElement("version")]
    public int Version { get; set; } = 1;

    /// <summary>
    /// 樂觀鎖定版本遞增
    /// </summary>
    public void IncrementVersion(DateTime updateTime)
    {
        Version++;
        UpdatedAt = updateTime;
    }
}

/// <summary>
/// 使用者檔案 - 巢狀文件範例
/// </summary>
public class UserProfile
{
    [BsonElement("first_name")]
    public string FirstName { get; set; } = string.Empty;

    [BsonElement("last_name")]
    public string LastName { get; set; } = string.Empty;

    [BsonElement("birth_date")]
    [BsonDateTimeOptions(Kind = DateTimeKind.Utc)]
    public DateTime? BirthDate { get; set; }

    [BsonElement("bio")]
    public string Bio { get; set; } = string.Empty;

    [BsonElement("social_links")]
    public Dictionary<string, string> SocialLinks { get; set; } = new();

    [BsonIgnore]
    public string FullName => $"{FirstName} {LastName}".Trim();
}

/// <summary>
/// 地址模型 - 用於地理空間查詢
/// </summary>
public class Address
{
    [BsonElement("type")]
    public string Type { get; set; } = string.Empty; // "home", "work", "other"

    [BsonElement("city")]
    public string City { get; set; } = string.Empty;

    [BsonElement("country")]
    public string Country { get; set; } = string.Empty;

    [BsonElement("location")]
    public GeoLocation? Location { get; set; }

    [BsonElement("is_primary")]
    public bool IsPrimary { get; set; }
}

/// <summary>
/// 地理位置 - GeoJSON 格式
/// </summary>
public class GeoLocation
{
    [BsonElement("type")]
    public string Type { get; set; } = "Point";

    [BsonElement("coordinates")]
    public double[] Coordinates { get; set; } = new double[2]; // [longitude, latitude]

    public static GeoLocation CreatePoint(double longitude, double latitude)
    {
        return new GeoLocation
        {
            Type = "Point",
            Coordinates = new[] { longitude, latitude }
        };
    }
}

/// <summary>
/// 技能模型 - 陣列查詢範例
/// </summary>
public class Skill
{
    [BsonElement("name")]
    public string Name { get; set; } = string.Empty;

    [BsonElement("level")]
    public SkillLevel Level { get; set; } = SkillLevel.Beginner;

    [BsonElement("years_experience")]
    public int YearsExperience { get; set; }

    [BsonElement("verified")]
    public bool Verified { get; set; }
}

/// <summary>
/// 技能等級列舉
/// </summary>
public enum SkillLevel
{
    [BsonRepresentation(BsonType.String)]
    Beginner,

    [BsonRepresentation(BsonType.String)]
    Intermediate,

    [BsonRepresentation(BsonType.String)]
    Advanced,

    [BsonRepresentation(BsonType.String)]
    Expert
}
```

### BSON 序列化測試

驗證 BSON 序列化行為：

```csharp
using MongoDB.Bson;
using AwesomeAssertions;

namespace YourProject.Integration.Tests.MongoDB;

public class MongoBsonTests
{
    [Fact]
    public void ObjectId產生_應產生有效的ObjectId()
    {
        // Arrange & Act
        var objectId = ObjectId.GenerateNewId();

        // Assert
        objectId.Should().NotBeNull();
        objectId.CreationTime.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(1));
        objectId.ToString().Should().HaveLength(24);
    }

    [Fact]
    public void BsonDocument建立_當傳入null值_應正確處理()
    {
        // Arrange
        var doc = new BsonDocument
        {
            ["name"] = "John",
            ["email"] = BsonNull.Value,
            ["age"] = 25
        };

        // Act
        var json = doc.ToJson();

        // Assert
        json.Should().Contain("\"email\" : null");
        doc["email"].IsBsonNull.Should().BeTrue();
    }

    [Fact]
    public void BsonArray操作_當使用複雜陣列_應正確處理()
    {
        // Arrange
        var skills = new BsonArray
        {
            new BsonDocument { ["name"] = "C#", ["level"] = 5 },
            new BsonDocument { ["name"] = "MongoDB", ["level"] = 3 }
        };

        var doc = new BsonDocument
        {
            ["userId"] = ObjectId.GenerateNewId(),
            ["skills"] = skills
        };

        // Act
        var skillsArray = doc["skills"].AsBsonArray;
        var firstSkill = skillsArray[0].AsBsonDocument;

        // Assert
        skillsArray.Should().HaveCount(2);
        firstSkill["name"].AsString.Should().Be("C#");
        firstSkill["level"].AsInt32.Should().Be(5);
    }
}
```

### MongoDB CRUD 測試

```csharp
using MongoDB.Driver;
using AwesomeAssertions;
using Microsoft.Extensions.Time.Testing;

namespace YourProject.Integration.Tests.MongoDB;

[Collection("MongoDb Collection")]
public class MongoUserServiceTests
{
    private readonly MongoUserService _mongoUserService;
    private readonly IMongoDatabase _database;
    private readonly FakeTimeProvider _fakeTimeProvider;

    public MongoUserServiceTests(MongoDbContainerFixture fixture)
    {
        _database = fixture.Database;
        _fakeTimeProvider = new FakeTimeProvider(DateTimeOffset.UtcNow);
        
        // 建立服務實例
        _mongoUserService = new MongoUserService(
            _database, 
            Options.Create(new MongoDbSettings { UsersCollectionName = "users" }),
            NullLogger<MongoUserService>.Instance,
            _fakeTimeProvider);
    }

    [Fact]
    public async Task CreateUserAsync_輸入有效使用者_應成功建立使用者()
    {
        // Arrange
        var user = new UserDocument
        {
            Username = $"testuser_{Guid.NewGuid():N}",
            Email = $"test_{Guid.NewGuid():N}@example.com",
            Profile = new UserProfile
            {
                FirstName = "Test",
                LastName = "User",
                Bio = "Test user bio"
            }
        };

        // Act
        var result = await _mongoUserService.CreateUserAsync(user);

        // Assert
        result.Should().NotBeNull();
        result.Username.Should().Be(user.Username);
        result.Email.Should().Be(user.Email);
        result.Id.Should().NotBeEmpty();
        result.CreatedAt.Should().Be(_fakeTimeProvider.GetUtcNow().DateTime);
    }

    [Fact]
    public async Task GetUserByIdAsync_輸入存在的ID_應回傳正確使用者()
    {
        // Arrange
        var user = new UserDocument
        {
            Username = $"gettest_{Guid.NewGuid():N}",
            Email = $"gettest_{Guid.NewGuid():N}@example.com",
            Profile = new UserProfile { FirstName = "Get", LastName = "Test" }
        };
        var createdUser = await _mongoUserService.CreateUserAsync(user);

        // Act
        var result = await _mongoUserService.GetUserByIdAsync(createdUser.Id);

        // Assert
        result.Should().NotBeNull();
        result!.Username.Should().Be(user.Username);
        result.Email.Should().Be(user.Email);
    }

    [Fact]
    public async Task UpdateUserAsync_使用樂觀鎖定_應成功更新版本號()
    {
        // Arrange
        var user = new UserDocument
        {
            Username = $"updatetest_{Guid.NewGuid():N}",
            Email = $"updatetest_{Guid.NewGuid():N}@example.com"
        };
        var createdUser = await _mongoUserService.CreateUserAsync(user);
        createdUser.Profile.Bio = "Updated bio";

        // Act
        var result = await _mongoUserService.UpdateUserAsync(createdUser);

        // Assert
        result.Should().NotBeNull();
        result!.Version.Should().Be(2);
        result.Profile.Bio.Should().Be("Updated bio");
    }

    [Fact]
    public async Task DeleteUserAsync_輸入存在的ID_應成功刪除使用者()
    {
        // Arrange
        var user = new UserDocument
        {
            Username = $"deletetest_{Guid.NewGuid():N}",
            Email = $"deletetest_{Guid.NewGuid():N}@example.com"
        };
        var createdUser = await _mongoUserService.CreateUserAsync(user);

        // Act
        var result = await _mongoUserService.DeleteUserAsync(createdUser.Id);

        // Assert
        result.Should().BeTrue();
        
        var deletedUser = await _mongoUserService.GetUserByIdAsync(createdUser.Id);
        deletedUser.Should().BeNull();
    }
}
```

### MongoDB 索引測試

```csharp
using MongoDB.Driver;
using AwesomeAssertions;
using System.Diagnostics;

namespace YourProject.Integration.Tests.MongoDB;

[Collection("MongoDb Collection")]
public class MongoIndexTests
{
    private readonly IMongoCollection<UserDocument> _users;
    private readonly ITestOutputHelper _output;

    public MongoIndexTests(MongoDbContainerFixture fixture, ITestOutputHelper output)
    {
        _users = fixture.Database.GetCollection<UserDocument>("index_test_users");
        _output = output;
    }

    [Fact]
    public async Task CreateUniqueIndex_電子郵件唯一索引_應防止重複插入()
    {
        // Arrange - 確保集合為空
        await _users.DeleteManyAsync(FilterDefinition<UserDocument>.Empty);

        // 建立唯一索引
        var indexKeysDefinition = Builders<UserDocument>.IndexKeys.Ascending(u => u.Email);
        var indexOptions = new CreateIndexOptions { Unique = true };
        await _users.Indexes.CreateOneAsync(
            new CreateIndexModel<UserDocument>(indexKeysDefinition, indexOptions));

        var uniqueEmail = $"unique_{Guid.NewGuid():N}@example.com";
        var user1 = new UserDocument { Username = "user1", Email = uniqueEmail };
        var user2 = new UserDocument { Username = "user2", Email = uniqueEmail };

        // Act & Assert
        await _users.InsertOneAsync(user1); // 第一次插入成功

        var exception = await Assert.ThrowsAsync<MongoWriteException>(
            () => _users.InsertOneAsync(user2));
        exception.WriteError.Category.Should().Be(ServerErrorCategory.DuplicateKey);

        _output.WriteLine("唯一索引測試通過 - 重複的 email 被正確阻擋");
    }

    [Fact]
    public async Task CompoundIndex_複合索引查詢效能_應提升查詢速度()
    {
        // Arrange - 確保集合為空
        await _users.DeleteManyAsync(FilterDefinition<UserDocument>.Empty);

        // 插入測試資料
        var testUsers = Enumerable.Range(0, 1000)
            .Select(i => new UserDocument
            {
                Username = $"user_{i:D4}",
                Email = $"user{i:D4}_{Guid.NewGuid():N}@example.com",
                IsActive = i % 2 == 0,
                CreatedAt = DateTime.UtcNow.AddDays(-i % 365)
            })
            .ToList();

        await _users.InsertManyAsync(testUsers);

        // 建立複合索引
        var compoundIndex = Builders<UserDocument>.IndexKeys
            .Ascending(u => u.IsActive)
            .Descending(u => u.CreatedAt);
        await _users.Indexes.CreateOneAsync(new CreateIndexModel<UserDocument>(compoundIndex));

        // 測試查詢效能
        var filter = Builders<UserDocument>.Filter.And(
            Builders<UserDocument>.Filter.Eq(u => u.IsActive, true),
            Builders<UserDocument>.Filter.Gte(u => u.CreatedAt, DateTime.UtcNow.AddDays(-100))
        );

        var stopwatch = Stopwatch.StartNew();
        var results = await _users.Find(filter).ToListAsync();
        stopwatch.Stop();

        _output.WriteLine($"查詢時間: {stopwatch.ElapsedMilliseconds}ms, 結果數量: {results.Count}");
        
        // Assert
        results.Should().NotBeEmpty();
    }
}
```

---

## Redis 容器化測試

### Redis Container Fixture

```csharp
using StackExchange.Redis;
using Testcontainers.Redis;

namespace YourProject.Integration.Tests.Fixtures;

/// <summary>
/// Redis 容器 Fixture - 管理 Redis 容器生命週期
/// </summary>
public class RedisContainerFixture : IAsyncLifetime
{
    private RedisContainer? _container;

    public IConnectionMultiplexer Connection { get; private set; } = null!;
    public IDatabase Database { get; private set; } = null!;
    public string ConnectionString { get; private set; } = string.Empty;

    public async Task InitializeAsync()
    {
        // 使用 Redis 7.2 版本
        _container = new RedisBuilder()
                     .WithImage("redis:7.2")
                     .WithPortBinding(6379, true)
                     .Build();

        await _container.StartAsync();

        ConnectionString = _container.GetConnectionString();
        Connection = await ConnectionMultiplexer.ConnectAsync(ConnectionString);
        Database = Connection.GetDatabase();
    }

    public async Task DisposeAsync()
    {
        if (Connection != null)
        {
            await Connection.DisposeAsync();
        }

        if (_container != null)
        {
            await _container.DisposeAsync();
        }
    }

    /// <summary>
    /// 清空資料庫 - 使用 KeyDelete 而非 FLUSHDB（避免權限問題）
    /// </summary>
    public async Task ClearDatabaseAsync()
    {
        var server = Connection.GetServer(Connection.GetEndPoints().First());
        var keys = server.Keys(Database.Database);
        if (keys.Any())
        {
            await Database.KeyDeleteAsync(keys.ToArray());
        }
    }
}

[CollectionDefinition("Redis Collection")]
public class RedisCollectionFixture : ICollectionFixture<RedisContainerFixture>
{
}
```

### Redis 快取模型

```csharp
using System.Text.Json.Serialization;

namespace YourProject.Core.Models.Redis;

/// <summary>
/// 通用快取包裝器 - 提供豐富的快取元資料
/// </summary>
public class CacheItem<T>
{
    [JsonPropertyName("data")]
    public T Data { get; set; } = default!;

    [JsonPropertyName("created_at")]
    public DateTime CreatedAt { get; set; }

    [JsonPropertyName("expires_at")]
    public DateTime? ExpiresAt { get; set; }

    [JsonPropertyName("key")]
    public string Key { get; set; } = string.Empty;

    [JsonPropertyName("tags")]
    public List<string> Tags { get; set; } = new();

    [JsonPropertyName("access_count")]
    public int AccessCount { get; set; }

    [JsonPropertyName("version")]
    public int Version { get; set; } = 1;

    [JsonIgnore]
    public bool IsExpired => ExpiresAt.HasValue && DateTime.UtcNow > ExpiresAt.Value;

    [JsonIgnore]
    public double TtlSeconds => ExpiresAt.HasValue
        ? Math.Max(0, ExpiresAt.Value.Subtract(DateTime.UtcNow).TotalSeconds)
        : -1;

    public static CacheItem<T> Create(string key, T data, TimeSpan? ttl = null, params string[] tags)
    {
        return new CacheItem<T>
        {
            Key = key,
            Data = data,
            CreatedAt = DateTime.UtcNow,
            ExpiresAt = ttl.HasValue ? DateTime.UtcNow.Add(ttl.Value) : null,
            Tags = tags.ToList()
        };
    }
}

/// <summary>
/// 使用者 Session - Hash 結構範例
/// </summary>
public class UserSession
{
    public string UserId { get; set; } = string.Empty;
    public string SessionId { get; set; } = string.Empty;
    public string IpAddress { get; set; } = string.Empty;
    public string UserAgent { get; set; } = string.Empty;
    public bool IsActive { get; set; }
}

/// <summary>
/// 最近瀏覽紀錄 - List 結構範例
/// </summary>
public class RecentView
{
    public string ItemId { get; set; } = string.Empty;
    public string ItemType { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
}

/// <summary>
/// 排行榜項目 - Sorted Set 結構範例
/// </summary>
public class LeaderboardEntry
{
    public string UserId { get; set; } = string.Empty;
    public string Username { get; set; } = string.Empty;
    public double Score { get; set; }
}
```

### Redis 五種資料結構測試

```csharp
using StackExchange.Redis;
using AwesomeAssertions;

namespace YourProject.Integration.Tests.Redis;

[Collection("Redis Collection")]
public class RedisCacheServiceTests
{
    private readonly RedisCacheService _redisCacheService;
    private readonly RedisContainerFixture _fixture;

    public RedisCacheServiceTests(RedisContainerFixture fixture)
    {
        _fixture = fixture;
        _redisCacheService = new RedisCacheService(
            fixture.Connection,
            Options.Create(new RedisSettings()),
            NullLogger<RedisCacheService>.Instance,
            TimeProvider.System);
    }

    #region String 測試

    [Fact]
    public async Task SetStringAsync_輸入字串值_應成功設定快取()
    {
        // Arrange
        var key = $"test_string_{Guid.NewGuid():N}";
        var value = "test_string_value";

        // Act
        var result = await _redisCacheService.SetStringAsync(key, value);

        // Assert
        result.Should().BeTrue();
        var retrieved = await _redisCacheService.GetStringAsync<string>(key);
        retrieved.Should().Be(value);
    }

    [Fact]
    public async Task SetObjectCacheAsync_輸入物件_應成功序列化並快取()
    {
        // Arrange
        var key = $"object_test_{Guid.NewGuid():N}";
        var user = new UserDocument
        {
            Username = "objecttest",
            Email = "object@test.com",
            Profile = new UserProfile { FirstName = "Object", LastName = "Test" }
        };

        // Act
        var result = await _redisCacheService.SetStringAsync(key, user, TimeSpan.FromMinutes(30));

        // Assert
        result.Should().BeTrue();
        var retrieved = await _redisCacheService.GetStringAsync<UserDocument>(key);
        retrieved.Should().NotBeNull();
        retrieved!.Username.Should().Be("objecttest");
    }

    [Fact]
    public async Task SetMultipleStringAsync_輸入多個鍵值對_應成功批次設定()
    {
        // Arrange
        var prefix = Guid.NewGuid().ToString("N")[..8];
        var keyValues = new Dictionary<string, string>
        {
            { $"multi1_{prefix}", "value1" },
            { $"multi2_{prefix}", "value2" },
            { $"multi3_{prefix}", "value3" }
        };

        // Act
        var result = await _redisCacheService.SetMultipleStringAsync(keyValues);

        // Assert
        result.Should().BeTrue();
        foreach (var kvp in keyValues)
        {
            var value = await _redisCacheService.GetStringAsync<string>(kvp.Key);
            value.Should().Be(kvp.Value);
        }
    }

    #endregion

    #region Hash 測試

    [Fact]
    public async Task SetHashAsync_輸入字串值_應設定Hash欄位()
    {
        // Arrange
        var key = $"hash_test_{Guid.NewGuid():N}";
        var field = "test_field";
        var value = "test_value";

        // Act
        var result = await _redisCacheService.SetHashAsync(key, field, value, TimeSpan.FromMinutes(30));

        // Assert
        result.Should().BeTrue();
        var retrieved = await _redisCacheService.GetHashAsync<string>(key, field);
        retrieved.Should().Be(value);
    }

    [Fact]
    public async Task SetHashAllAsync_輸入物件_應設定完整Hash()
    {
        // Arrange
        var key = $"hash_all_{Guid.NewGuid():N}";
        var session = new UserSession
        {
            UserId = "user123",
            SessionId = "session456",
            IpAddress = "192.168.1.1",
            UserAgent = "Test Browser",
            IsActive = true
        };

        // Act
        var result = await _redisCacheService.SetHashAllAsync(key, session, TimeSpan.FromHours(1));

        // Assert
        result.Should().BeTrue();
        var retrieved = await _redisCacheService.GetHashAllAsync<UserSession>(key);
        retrieved.Should().NotBeNull();
        retrieved!.UserId.Should().Be("user123");
        retrieved.SessionId.Should().Be("session456");
    }

    #endregion

    #region List 測試

    [Fact]
    public async Task ListLeftPushAsync_輸入值_應新增到List左側()
    {
        // Arrange
        var key = $"list_test_{Guid.NewGuid():N}";
        var view1 = new RecentView { ItemId = "item1", ItemType = "product", Title = "Product 1" };
        var view2 = new RecentView { ItemId = "item2", ItemType = "product", Title = "Product 2" };

        // Act
        var count1 = await _redisCacheService.ListLeftPushAsync(key, view1);
        var count2 = await _redisCacheService.ListLeftPushAsync(key, view2);

        // Assert
        count1.Should().Be(1);
        count2.Should().Be(2);

        var views = await _redisCacheService.ListRangeAsync<RecentView>(key);
        views.Should().HaveCount(2);
        views[0].ItemId.Should().Be("item2"); // 最後加入的在最前面
        views[1].ItemId.Should().Be("item1");
    }

    #endregion

    #region Set 測試

    [Fact]
    public async Task SetAddAsync_輸入值_應新增到Set()
    {
        // Arrange
        var key = $"set_test_{Guid.NewGuid():N}";
        var tag1 = "programming";
        var tag2 = "testing";
        var tag3 = "programming"; // 重複

        // Act
        var result1 = await _redisCacheService.SetAddAsync(key, tag1);
        var result2 = await _redisCacheService.SetAddAsync(key, tag2);
        var result3 = await _redisCacheService.SetAddAsync(key, tag3);

        // Assert
        result1.Should().BeTrue();
        result2.Should().BeTrue();
        result3.Should().BeFalse(); // 重複項目回傳 false

        var tags = await _redisCacheService.SetMembersAsync<string>(key);
        tags.Should().HaveCount(2);
        tags.Should().Contain("programming");
        tags.Should().Contain("testing");
    }

    #endregion

    #region Sorted Set 測試

    [Fact]
    public async Task SortedSetAddAsync_輸入分數和成員_應成功新增到排序集合()
    {
        // Arrange
        var key = $"sorted_set_{Guid.NewGuid():N}";
        var entry1 = new LeaderboardEntry { UserId = "user1", Username = "Player1", Score = 100 };
        var entry2 = new LeaderboardEntry { UserId = "user2", Username = "Player2", Score = 200 };

        // Act
        var result1 = await _redisCacheService.SortedSetAddAsync(key, entry1, entry1.Score);
        var result2 = await _redisCacheService.SortedSetAddAsync(key, entry2, entry2.Score);

        // Assert
        result1.Should().BeTrue();
        result2.Should().BeTrue();

        var rankings = await _redisCacheService.SortedSetRangeWithScoresAsync<LeaderboardEntry>(
            key, 0, -1, Order.Descending);
        rankings.Should().HaveCount(2);
        rankings[0].Member.Username.Should().Be("Player2"); // 分數高的在前面
        rankings[0].Score.Should().Be(200);
    }

    #endregion

    #region TTL 與過期測試

    [Fact]
    public async Task ExpireAsync_輸入過期時間_應正確設定TTL()
    {
        // Arrange
        var key = $"expire_test_{Guid.NewGuid():N}";
        await _redisCacheService.SetStringAsync(key, "expire_value");

        // Act
        var result = await _redisCacheService.ExpireAsync(key, TimeSpan.FromMinutes(5));

        // Assert
        result.Should().BeTrue();
        var ttl = await _redisCacheService.GetTtlAsync(key);
        ttl.Should().NotBeNull();
        ttl!.Value.TotalMinutes.Should().BeGreaterThan(4);
    }

    #endregion

    #region 資料隔離測試

    [Fact]
    public async Task 測試資料隔離_多個測試同時執行_應不互相影響()
    {
        // Arrange
        var testId = Guid.NewGuid().ToString("N")[..8];
        var key1 = $"isolation_test:{testId}:key1";
        var key2 = $"isolation_test:{testId}:key2";

        // Act
        await _redisCacheService.SetStringAsync(key1, "value1");
        await _redisCacheService.SetStringAsync(key2, "value2");

        // Assert
        var value1 = await _redisCacheService.GetStringAsync<string>(key1);
        var value2 = await _redisCacheService.GetStringAsync<string>(key2);

        value1.Should().Be("value1");
        value2.Should().Be("value2");

        // Cleanup
        await _redisCacheService.DeleteAsync(key1);
        await _redisCacheService.DeleteAsync(key2);
    }

    #endregion
}
```

---

## 最佳實踐

### 1. Collection Fixture 模式

使用 Collection Fixture 共享容器，避免每個測試重啟容器：

```csharp
// 定義集合
[CollectionDefinition("MongoDb Collection")]
public class MongoDbCollectionFixture : ICollectionFixture<MongoDbContainerFixture> { }

// 使用集合
[Collection("MongoDb Collection")]
public class MyMongoTests
{
    public MyMongoTests(MongoDbContainerFixture fixture)
    {
        // 使用共享的容器
    }
}
```

### 2. 資料隔離策略

確保測試間不互相干擾：

```csharp
// MongoDB：使用唯一的 Email/Username
var user = new UserDocument
{
    Username = $"testuser_{Guid.NewGuid():N}",
    Email = $"test_{Guid.NewGuid():N}@example.com"
};

// Redis：使用唯一的 Key 前綴
var testId = Guid.NewGuid().ToString("N")[..8];
var key = $"test:{testId}:mykey";
```

### 3. 清理策略

```csharp
// MongoDB：測試後清理
await fixture.ClearDatabaseAsync();

// Redis：使用 KeyDelete 而非 FLUSHDB（避免權限問題）
var keys = server.Keys(database.Database);
if (keys.Any())
{
    await database.KeyDeleteAsync(keys.ToArray());
}
```

### 4. 效能考量

| 策略               | 說明                                         |
| ------------------ | -------------------------------------------- |
| Collection Fixture | 容器只啟動一次，節省 80%+ 時間               |
| 資料隔離           | 使用唯一 Key/ID 而非清空資料庫               |
| 批次操作           | 使用 InsertManyAsync、SetMultipleStringAsync |
| 索引建立           | 在 Fixture 初始化時建立索引                  |

---

## 常見問題

### Redis FLUSHDB 權限問題

某些 Redis 容器映像檔預設不啟用 admin 模式：

```csharp
// ❌ 錯誤：可能失敗
await server.FlushDatabaseAsync();

// ✅ 正確：使用 KeyDelete
var keys = server.Keys(database.Database);
if (keys.Any())
{
    await database.KeyDeleteAsync(keys.ToArray());
}
```

### MongoDB 唯一索引重複插入

```csharp
// 測試時使用唯一的 Email 避免衝突
var uniqueEmail = $"test_{Guid.NewGuid():N}@example.com";
```

### 容器啟動超時

```csharp
// 增加等待時間
_container = new MongoDbBuilder()
    .WithImage("mongo:7.0")
    .WithWaitStrategy(Wait.ForUnixContainer()
        .UntilPortIsAvailable(27017))
    .Build();
```

---

## 相關技能

- [testcontainers-database](../testcontainers-database/SKILL.md) - PostgreSQL/MSSQL 容器化測試
- [aspnet-integration-testing](../aspnet-integration-testing/SKILL.md) - ASP.NET Core 整合測試
- [nsubstitute-mocking](../../dotnet-testing/nsubstitute-mocking/SKILL.md) - 測試替身與 Mock

---

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 22 - Testcontainers 整合測試：MongoDB 及 Redis 基礎到進階**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10376114
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day22

### 官方文件

- [Testcontainers 官方網站](https://testcontainers.com/)
- [.NET Testcontainers 文件](https://dotnet.testcontainers.org/)
- [MongoDB.Driver 官方文件](https://www.mongodb.com/docs/drivers/csharp/)
- [StackExchange.Redis 官方文件](https://stackexchange.github.io/StackExchange.Redis/)
- [xUnit Collection Fixtures](https://xunit.net/docs/shared-context#collection-fixture)
