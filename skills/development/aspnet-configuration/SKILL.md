---
name: aspnet-configuration
description: Guide for ASP.NET Core configuration with appsettings.json, environment-specific settings, and the options pattern
type: domain
enforcement: suggest
priority: medium
---

# ASP.NET Core Configuration

This skill provides guidance for **configuration management** in ASP.NET Core applications using appsettings.json, environment-specific settings, user secrets, and the options pattern.

## Table of Contents
1. [Configuration Files](#configuration-files)
2. [Environment-Specific Configuration](#environment-specific-configuration)
3. [Accessing Configuration](#accessing-configuration)
4. [Options Pattern](#options-pattern)
5. [User Secrets](#user-secrets)
6. [Best Practices](#best-practices)
7. [Quick Reference](#quick-reference)

---

## Configuration Files

### appsettings.json

Both projects have appsettings.json:
- `src/ClaudeStack.Web/appsettings.json`
- `src/ClaudeStack.API/appsettings.json`

**Standard structure:**
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

### Configuration Hierarchy

ASP.NET Core loads configuration in this order (later sources override earlier):
1. appsettings.json
2. appsettings.{Environment}.json
3. User Secrets (Development only)
4. Environment variables
5. Command-line arguments

---

## Environment-Specific Configuration

### appsettings.Development.json

Overrides appsettings.json in Development environment:
- `src/ClaudeStack.Web/appsettings.Development.json`
- `src/ClaudeStack.API/appsettings.Development.json`

**Example:**
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Information"
    }
  }
}
```

### Determining Environment

**Set via environment variable:**
```bash
# Windows
$env:ASPNETCORE_ENVIRONMENT="Development"

# Linux/macOS
export ASPNETCORE_ENVIRONMENT=Development
```

**Check in code:**
```csharp
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();  // Only in development
}
```

### Creating Environment-Specific Files

```bash
# Create production settings
# src/ClaudeStack.Web/appsettings.Production.json
```

Automatically loaded when `ASPNETCORE_ENVIRONMENT=Production`.

---

## Accessing Configuration

### IConfiguration Interface

**In Program.cs (Minimal API):**
```csharp
var builder = WebApplication.CreateBuilder(args);

// Access configuration from builder
var connectionString = builder.Configuration["ConnectionStrings:DefaultConnection"];

var app = builder.Build();

// Access configuration in endpoint
app.MapGet("/config", (IConfiguration config) =>
{
    var value = config["MySettings:MyValue"];
    return value;
});
```

**In MVC Controller:**
```csharp
public class HomeController : Controller
{
    private readonly IConfiguration _configuration;

    public HomeController(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public IActionResult Index()
    {
        var value = _configuration["MySettings:MyValue"];
        return View();
    }
}
```

### Nested Configuration

**appsettings.json:**
```json
{
  "Database": {
    "ConnectionString": "Server=localhost;Database=MyDb",
    "Timeout": 30
  }
}
```

**Access:**
```csharp
var connectionString = config["Database:ConnectionString"];
var timeout = config.GetValue<int>("Database:Timeout");
```

---

## Options Pattern

### Strongly-Typed Configuration

**1. Define options class:**
```csharp
public class DatabaseOptions
{
    public string ConnectionString { get; set; }
    public int Timeout { get; set; }
}
```

**2. Bind configuration:**
```csharp
// In Program.cs
builder.Services.Configure<DatabaseOptions>(
    builder.Configuration.GetSection("Database"));
```

**3. Use in services/controllers:**
```csharp
public class UserService
{
    private readonly DatabaseOptions _options;

    public UserService(IOptions<DatabaseOptions> options)
    {
        _options = options.Value;
    }

    public void Connect()
    {
        var conn = _options.ConnectionString;
    }
}
```

### IOptions vs IOptionsSnapshot vs IOptionsMonitor

```csharp
IOptions<T>          // Singleton, never reloads
IOptionsSnapshot<T>  // Scoped, reloads per request
IOptionsMonitor<T>   // Singleton, reloads on change
```

**Use IOptions** for most cases.
**Use IOptionsSnapshot** if configuration changes between requests.
**Use IOptionsMonitor** to react to configuration changes in real-time.

---

## User Secrets

### Overview

User Secrets stores sensitive configuration **outside** the project directory. Used in Development only.

**For:**
- API keys
- Connection strings
- Passwords

**Not for:**
- Production secrets (use Azure Key Vault, etc.)
- Non-sensitive settings

### Initialize User Secrets

```bash
cd src/ClaudeStack.Web
dotnet user-secrets init
```

Adds `<UserSecretsId>` to .csproj:
```xml
<PropertyGroup>
  <UserSecretsId>guid-here</UserSecretsId>
</PropertyGroup>
```

### Set Secrets

```bash
# Set individual secret
dotnet user-secrets set "ApiKey" "secret-value-123"

# Set nested secret
dotnet user-secrets set "Database:ConnectionString" "Server=..."

# List all secrets
dotnet user-secrets list

# Remove secret
dotnet user-secrets remove "ApiKey"

# Clear all secrets
dotnet user-secrets clear
```

### Access Secrets

Same as regular configuration:
```csharp
var apiKey = builder.Configuration["ApiKey"];
```

**Location:**
- Windows: `%APPDATA%\Microsoft\UserSecrets\<user_secrets_id>\secrets.json`
- Linux/macOS: `~/.microsoft/usersecrets/<user_secrets_id>/secrets.json`

---

## Best Practices

### 1. Never Commit Secrets

```bash
# .gitignore already includes:
appsettings.Development.json  # Sometimes
**/secrets.json
```

Use User Secrets for local development secrets.

### 2. Use Options Pattern

**Prefer:**
```csharp
builder.Services.Configure<MyOptions>(
    builder.Configuration.GetSection("MySettings"));
```

**Over:**
```csharp
var value = builder.Configuration["MySettings:Value"];  // Weakly-typed
```

### 3. Validate Options

```csharp
builder.Services.AddOptions<DatabaseOptions>()
    .Bind(builder.Configuration.GetSection("Database"))
    .ValidateDataAnnotations()
    .ValidateOnStart();

public class DatabaseOptions
{
    [Required]
    public string ConnectionString { get; set; }

    [Range(1, 300)]
    public int Timeout { get; set; }
}
```

### 4. Environment-Specific Settings

```json
// appsettings.json - defaults
{
  "Database": {
    "ConnectionString": "Server=localhost"
  }
}

// appsettings.Production.json - production overrides
{
  "Database": {
    "ConnectionString": "Server=prod-server"
  }
}
```

### 5. Connection Strings

Special section:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyDb"
  }
}
```

Access:
```csharp
var connStr = builder.Configuration.GetConnectionString("DefaultConnection");
```

---

## Quick Reference

### Configuration Access

```csharp
// Simple value
config["MyKey"]

// Nested value
config["Section:SubSection:Key"]

// Typed value
config.GetValue<int>("Section:IntKey")

// Connection string
config.GetConnectionString("DefaultConnection")

// Entire section
var section = config.GetSection("MySection")
```

### Options Pattern

```csharp
// Register
builder.Services.Configure<MyOptions>(
    builder.Configuration.GetSection("MySection"));

// Use (constructor injection)
public MyService(IOptions<MyOptions> options)
{
    var value = options.Value.Property;
}
```

### User Secrets Commands

```bash
dotnet user-secrets init
dotnet user-secrets set "Key" "Value"
dotnet user-secrets list
dotnet user-secrets remove "Key"
dotnet user-secrets clear
```

### Environment Setup

```bash
# Set environment
$env:ASPNETCORE_ENVIRONMENT="Development"

# Check in code
if (app.Environment.IsDevelopment()) { }
if (app.Environment.IsProduction()) { }
```

---

## Related Skills

- **dotnet-minimal-apis**: Using configuration in minimal APIs
- **dotnet-cli-essentials**: Running applications with different environments

---

## Additional Resources

- [Configuration in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/configuration/)
- [Options Pattern](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/configuration/options)
- [User Secrets](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets)
- [Environment Variables](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/environments)

---

## Version Information

- **ASP.NET Core**: 10.0 RC 2
- **.NET SDK**: 10.0.100-rc.2.25502.107

Configuration system is stable across .NET versions. This project uses .NET 10 RC 2 patterns.
