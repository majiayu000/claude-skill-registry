---
name: koan-quickstart
description: Zero to first Koan app in under 10 minutes (S0 + S1 patterns)
---

# Koan Quickstart

## Core Principle

**Get productive in under 10 minutes.** Create entities, save data, expose APIs with minimal code.

## 10-Minute First App

### Step 1: Create Project (1 min)

```bash
dotnet new web -n MyKoanApp
cd MyKoanApp
dotnet add package Koan.Core --version 0.6.3
dotnet add package Koan.Data.Core --version 0.6.3
dotnet add package Koan.Data.Connector.Json --version 0.6.3
dotnet add package Koan.Web --version 0.6.3
```

### Step 2: Minimal Program.cs (1 min)

```csharp
using Koan.Core;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddKoan();
var app = builder.Build();
app.Run();
```

### Step 3: Create Entity (2 min)

```csharp
// Models/Todo.cs
using Koan.Data.Core;

public class Todo : Entity<Todo>
{
    public string Title { get; set; } = "";
    public bool Completed { get; set; }
}
```

### Step 4: Create Controller (2 min)

```csharp
// Controllers/TodosController.cs
using Koan.Web;
using Microsoft.AspNetCore.Mvc;

[Route("api/[controller]")]
public class TodosController : EntityController<Todo>
{
    // Full CRUD API auto-generated!
}
```

### Step 5: Run and Test (4 min)

```bash
dotnet run

# Test endpoints:
curl http://localhost:5000/api/todos
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"First task","completed":false}'
```

**Done!** You now have a working CRUD API with:
- ✅ Auto GUID v7 IDs
- ✅ GET/POST/PUT/DELETE/PATCH endpoints
- ✅ JSON file storage
- ✅ Zero configuration

## Next Steps

### Add Relationships (5 min)

```csharp
public class User : Entity<User>
{
    public string Name { get; set; } = "";
}

public class Todo : Entity<Todo>
{
    public string Title { get; set; } = "";
    public string UserId { get; set; } = "";

    public Task<User?> GetUser(CancellationToken ct = default) =>
        User.Get(UserId, ct);
}
```

### Switch to Real Database (2 min)

```bash
# Add PostgreSQL
dotnet add package Koan.Data.Connector.Postgres

# Update appsettings.json
{
  "Koan": {
    "Data": {
      "Sources": {
        "Default": {
          "Adapter": "postgres",
          "ConnectionString": "Host=localhost;Database=myapp;Username=koan;Password=dev"
        }
      }
    }
  }
}

# Entity code unchanged! Provider transparency.
```

## When This Skill Applies

- ✅ Starting new projects
- ✅ Learning Koan basics
- ✅ Quick prototypes
- ✅ Proof of concepts

## Reference Documentation

- **Sample:** `samples/S0.ConsoleJsonRepo/` (Minimal 20-line example)
- **Sample:** `samples/S1.Web/` (Full web app with relationships)
- **Getting Started:** `docs/getting-started/overview.md`
