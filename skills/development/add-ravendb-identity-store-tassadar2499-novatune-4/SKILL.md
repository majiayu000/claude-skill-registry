---
description: Implement ASP.NET Identity user and refresh token stores backed by RavenDB
---
# Add RavenDB Identity Store Skill

Implement ASP.NET Identity stores backed by RavenDB for NovaTune.

## Project Context

- Identity models: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/Identity/`
- Identity stores: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Identity/`
- RavenDB config: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/RavenDb/`

## Steps

### 1. Create Identity Models

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/Identity/`

```csharp
// ApplicationUser.cs
public class ApplicationUser
{
    public string Id { get; set; } = null!;           // RavenDB internal ID: "Users/{guid}"
    public string UserId { get; set; } = null!;        // ULID external identifier
    public string Email { get; set; } = null!;
    public string NormalizedEmail { get; set; } = null!;
    public string DisplayName { get; set; } = null!;
    public string PasswordHash { get; set; } = null!;
    public UserStatus Status { get; set; } = UserStatus.Active;
    public List<string> Roles { get; set; } = ["Listener"];
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? LastLoginAt { get; set; }
}

// UserStatus.cs
public enum UserStatus
{
    Active,
    Disabled,
    PendingDeletion
}

// RefreshToken.cs
public class RefreshToken
{
    public string Id { get; set; } = null!;           // RavenDB: "RefreshTokens/{guid}"
    public string UserId { get; set; } = null!;        // References ApplicationUser.UserId
    public string TokenHash { get; set; } = null!;     // SHA-256 hash
    public string? DeviceIdentifier { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime ExpiresAt { get; set; }
    public bool IsRevoked { get; set; }
}
```

### 2. Create User Store

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Identity/RavenDbUserStore.cs`

```csharp
public class RavenDbUserStore :
    IUserStore<ApplicationUser>,
    IUserPasswordStore<ApplicationUser>,
    IUserRoleStore<ApplicationUser>,
    IUserEmailStore<ApplicationUser>
{
    private readonly IAsyncDocumentSession _session;

    public RavenDbUserStore(IAsyncDocumentSession session)
    {
        _session = session;
    }

    // IUserStore
    public async Task<IdentityResult> CreateAsync(
        ApplicationUser user, CancellationToken ct)
    {
        user.UserId = Ulid.NewUlid().ToString();
        await _session.StoreAsync(user, ct);
        await _session.SaveChangesAsync(ct);
        return IdentityResult.Success;
    }

    public async Task<ApplicationUser?> FindByIdAsync(
        string userId, CancellationToken ct)
    {
        return await _session.Query<ApplicationUser>()
            .FirstOrDefaultAsync(u => u.UserId == userId, ct);
    }

    public async Task<ApplicationUser?> FindByNameAsync(
        string normalizedUserName, CancellationToken ct)
    {
        return await _session.Query<ApplicationUser>()
            .FirstOrDefaultAsync(u => u.NormalizedEmail == normalizedUserName, ct);
    }

    public async Task<IdentityResult> UpdateAsync(
        ApplicationUser user, CancellationToken ct)
    {
        await _session.SaveChangesAsync(ct);
        return IdentityResult.Success;
    }

    public async Task<IdentityResult> DeleteAsync(
        ApplicationUser user, CancellationToken ct)
    {
        _session.Delete(user);
        await _session.SaveChangesAsync(ct);
        return IdentityResult.Success;
    }

    public Task<string> GetUserIdAsync(
        ApplicationUser user, CancellationToken ct) =>
        Task.FromResult(user.UserId);

    public Task<string?> GetUserNameAsync(
        ApplicationUser user, CancellationToken ct) =>
        Task.FromResult<string?>(user.Email);

    public Task SetUserNameAsync(
        ApplicationUser user, string? userName, CancellationToken ct)
    {
        user.Email = userName!;
        return Task.CompletedTask;
    }

    public Task<string?> GetNormalizedUserNameAsync(
        ApplicationUser user, CancellationToken ct) =>
        Task.FromResult<string?>(user.NormalizedEmail);

    public Task SetNormalizedUserNameAsync(
        ApplicationUser user, string? normalizedName, CancellationToken ct)
    {
        user.NormalizedEmail = normalizedName!;
        return Task.CompletedTask;
    }

    // IUserPasswordStore
    public Task SetPasswordHashAsync(
        ApplicationUser user, string? passwordHash, CancellationToken ct)
    {
        user.PasswordHash = passwordHash!;
        return Task.CompletedTask;
    }

    public Task<string?> GetPasswordHashAsync(
        ApplicationUser user, CancellationToken ct) =>
        Task.FromResult<string?>(user.PasswordHash);

    public Task<bool> HasPasswordAsync(
        ApplicationUser user, CancellationToken ct) =>
        Task.FromResult(!string.IsNullOrEmpty(user.PasswordHash));

    // IUserRoleStore
    public Task AddToRoleAsync(
        ApplicationUser user, string roleName, CancellationToken ct)
    {
        if (!user.Roles.Contains(roleName, StringComparer.OrdinalIgnoreCase))
            user.Roles.Add(roleName);
        return Task.CompletedTask;
    }

    public Task RemoveFromRoleAsync(
        ApplicationUser user, string roleName, CancellationToken ct)
    {
        user.Roles.RemoveAll(r =>
            r.Equals(roleName, StringComparison.OrdinalIgnoreCase));
        return Task.CompletedTask;
    }

    public Task<IList<string>> GetRolesAsync(
        ApplicationUser user, CancellationToken ct) =>
        Task.FromResult<IList<string>>(user.Roles);

    public Task<bool> IsInRoleAsync(
        ApplicationUser user, string roleName, CancellationToken ct) =>
        Task.FromResult(user.Roles.Contains(roleName, StringComparer.OrdinalIgnoreCase));

    public async Task<IList<ApplicationUser>> GetUsersInRoleAsync(
        string roleName, CancellationToken ct)
    {
        return await _session.Query<ApplicationUser>()
            .Where(u => u.Roles.Contains(roleName))
            .ToListAsync(ct);
    }

    // IUserEmailStore
    public Task SetEmailAsync(
        ApplicationUser user, string? email, CancellationToken ct)
    {
        user.Email = email!;
        return Task.CompletedTask;
    }

    public Task<string?> GetEmailAsync(
        ApplicationUser user, CancellationToken ct) =>
        Task.FromResult<string?>(user.Email);

    public Task<bool> GetEmailConfirmedAsync(
        ApplicationUser user, CancellationToken ct) =>
        Task.FromResult(true); // Email confirmation not required for MVP

    public Task SetEmailConfirmedAsync(
        ApplicationUser user, bool confirmed, CancellationToken ct) =>
        Task.CompletedTask;

    public async Task<ApplicationUser?> FindByEmailAsync(
        string normalizedEmail, CancellationToken ct)
    {
        return await _session.Query<ApplicationUser>()
            .FirstOrDefaultAsync(u => u.NormalizedEmail == normalizedEmail, ct);
    }

    public Task<string?> GetNormalizedEmailAsync(
        ApplicationUser user, CancellationToken ct) =>
        Task.FromResult<string?>(user.NormalizedEmail);

    public Task SetNormalizedEmailAsync(
        ApplicationUser user, string? normalizedEmail, CancellationToken ct)
    {
        user.NormalizedEmail = normalizedEmail!;
        return Task.CompletedTask;
    }

    public void Dispose() { }
}
```

### 3. Create Refresh Token Repository

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Identity/RefreshTokenRepository.cs`

```csharp
public interface IRefreshTokenRepository
{
    Task<RefreshToken> CreateAsync(string userId, string tokenHash, DateTime expiresAt,
        string? deviceId, CancellationToken ct);
    Task<RefreshToken?> FindByHashAsync(string tokenHash, CancellationToken ct);
    Task RevokeAsync(string tokenId, CancellationToken ct);
    Task RevokeAllForUserAsync(string userId, CancellationToken ct);
    Task<int> GetActiveCountForUserAsync(string userId, CancellationToken ct);
    Task RevokeOldestForUserAsync(string userId, CancellationToken ct);
}

public class RefreshTokenRepository : IRefreshTokenRepository
{
    private readonly IAsyncDocumentSession _session;

    public RefreshTokenRepository(IAsyncDocumentSession session)
    {
        _session = session;
    }

    public async Task<RefreshToken> CreateAsync(
        string userId, string tokenHash, DateTime expiresAt,
        string? deviceId, CancellationToken ct)
    {
        var token = new RefreshToken
        {
            UserId = userId,
            TokenHash = tokenHash,
            ExpiresAt = expiresAt,
            DeviceIdentifier = deviceId
        };

        await _session.StoreAsync(token, ct);
        await _session.SaveChangesAsync(ct);
        return token;
    }

    public async Task<RefreshToken?> FindByHashAsync(
        string tokenHash, CancellationToken ct)
    {
        return await _session.Query<RefreshToken>()
            .FirstOrDefaultAsync(t =>
                t.TokenHash == tokenHash &&
                !t.IsRevoked &&
                t.ExpiresAt > DateTime.UtcNow, ct);
    }

    public async Task RevokeAsync(string tokenId, CancellationToken ct)
    {
        var token = await _session.LoadAsync<RefreshToken>(tokenId, ct);
        if (token != null)
        {
            token.IsRevoked = true;
            await _session.SaveChangesAsync(ct);
        }
    }

    public async Task RevokeAllForUserAsync(string userId, CancellationToken ct)
    {
        var tokens = await _session.Query<RefreshToken>()
            .Where(t => t.UserId == userId && !t.IsRevoked)
            .ToListAsync(ct);

        foreach (var token in tokens)
            token.IsRevoked = true;

        await _session.SaveChangesAsync(ct);
    }

    public async Task<int> GetActiveCountForUserAsync(
        string userId, CancellationToken ct)
    {
        return await _session.Query<RefreshToken>()
            .CountAsync(t =>
                t.UserId == userId &&
                !t.IsRevoked &&
                t.ExpiresAt > DateTime.UtcNow, ct);
    }

    public async Task RevokeOldestForUserAsync(string userId, CancellationToken ct)
    {
        var oldest = await _session.Query<RefreshToken>()
            .Where(t => t.UserId == userId && !t.IsRevoked)
            .OrderBy(t => t.CreatedAt)
            .FirstOrDefaultAsync(ct);

        if (oldest != null)
        {
            oldest.IsRevoked = true;
            await _session.SaveChangesAsync(ct);
        }
    }
}
```

### 4. Register Identity Services in Program.cs

```csharp
// Register RavenDB session (per request)
builder.Services.AddScoped(sp =>
{
    var store = sp.GetRequiredService<IDocumentStore>();
    return store.OpenAsyncSession();
});

// Register identity stores
builder.Services.AddScoped<IUserStore<ApplicationUser>, RavenDbUserStore>();
builder.Services.AddScoped<IRefreshTokenRepository, RefreshTokenRepository>();

// Configure Identity (without Entity Framework)
builder.Services.AddIdentityCore<ApplicationUser>(options =>
{
    options.Password.RequireDigit = false;
    options.Password.RequireLowercase = false;
    options.Password.RequireUppercase = false;
    options.Password.RequireNonAlphanumeric = false;
    options.Password.RequiredLength = 1;  // Non-empty per requirements
    options.User.RequireUniqueEmail = true;
})
.AddRoles<IdentityRole>()
.AddUserStore<RavenDbUserStore>()
.AddDefaultTokenProviders();
```

### 5. Create RavenDB Indexes

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/RavenDb/Indexes/`

```csharp
// Users_ByEmail.cs
public class Users_ByEmail : AbstractIndexCreationTask<ApplicationUser>
{
    public Users_ByEmail()
    {
        Map = users => from user in users
                       select new { user.NormalizedEmail };
    }
}

// RefreshTokens_ByUserAndHash.cs
public class RefreshTokens_ByUserAndHash : AbstractIndexCreationTask<RefreshToken>
{
    public RefreshTokens_ByUserAndHash()
    {
        Map = tokens => from token in tokens
                        select new
                        {
                            token.UserId,
                            token.TokenHash,
                            token.IsRevoked,
                            token.ExpiresAt
                        };
    }
}
```

## Required NuGet Packages

```bash
dotnet add package Microsoft.AspNetCore.Identity
dotnet add package Microsoft.Extensions.Identity.Core
dotnet add package Ulid
```

## RavenDB Collections

| Collection | Document Type | Purpose |
|------------|---------------|---------|
| `Users` | `ApplicationUser` | User accounts and credentials |
| `RefreshTokens` | `RefreshToken` | Hashed refresh tokens |

## Testing

```csharp
[Fact]
public async Task CreateAsync_GeneratesUlid()
{
    var user = new ApplicationUser { Email = "test@example.com" };

    var result = await _userStore.CreateAsync(user, CancellationToken.None);

    result.Succeeded.Should().BeTrue();
    user.UserId.Should().NotBeNullOrEmpty();
    Ulid.TryParse(user.UserId, out _).Should().BeTrue();
}

[Fact]
public async Task FindByEmailAsync_ReturnsUser_WhenExists()
{
    var user = await _userStore.FindByEmailAsync("TEST@EXAMPLE.COM", CancellationToken.None);

    user.Should().NotBeNull();
    user!.Email.Should().Be("test@example.com");
}
```