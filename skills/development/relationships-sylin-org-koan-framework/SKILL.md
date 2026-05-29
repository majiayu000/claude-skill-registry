---
name: koan-relationships
description: Entity navigation, batch loading, relationship best practices
---

# Koan Relationships

## Core Principle

**Relationships use foreign keys + navigation helpers.** Batch load to prevent N+1 queries. No ORM mapping configuration needed.

## Relationship Patterns

### One-to-Many

```csharp
public class User : Entity<User>
{
    public string Name { get; set; } = "";

    public Task<List<Todo>> GetTodos(CancellationToken ct = default) =>
        Todo.Query(t => t.UserId == Id, ct);
}

public class Todo : Entity<Todo>
{
    public string UserId { get; set; } = "";

    public Task<User?> GetUser(CancellationToken ct = default) =>
        User.Get(UserId, ct);
}
```

### Preventing N+1 Queries

```csharp
// ❌ WRONG: N+1 query problem
foreach (var todo in todos)
{
    var user = await todo.GetUser(); // N queries!
}

// ✅ CORRECT: Batch load
var userIds = todos.Select(t => t.UserId).Distinct().ToArray();
var users = await User.Get(userIds);
var userDict = users.Where(u => u != null).ToDictionary(u => u!.Id);

foreach (var todo in todos)
{
    var user = userDict[todo.UserId];
}
```

### Optional Relationships

```csharp
public class Todo : Entity<Todo>
{
    public string? CategoryId { get; set; }

    public Task<Category?> GetCategory(CancellationToken ct = default) =>
        string.IsNullOrEmpty(CategoryId) ? Task.FromResult<Category?>(null)
            : Category.Get(CategoryId, ct);
}
```

### Hierarchical (Parent-Child)

```csharp
public class TodoItem : Entity<TodoItem>
{
    public string TodoId { get; set; } = "";
    public int SortOrder { get; set; }

    public Task<Todo?> GetParentTodo(CancellationToken ct = default) =>
        Todo.Get(TodoId, ct);
}

public class Todo : Entity<Todo>
{
    public Task<List<TodoItem>> GetItems(CancellationToken ct = default) =>
        TodoItem.Query(i => i.TodoId == Id, ct)
            .ContinueWith(t => t.Result.OrderBy(i => i.SortOrder).ToList());
}
```

## When This Skill Applies

- ✅ Complex data relationships
- ✅ Navigation patterns
- ✅ Performance optimization (N+1)
- ✅ Hierarchical data
- ✅ Optional relationships

## Reference Documentation

- **Example Code:** `.claude/skills/entity-first/examples/entity-relationships.cs`
- **Sample:** `samples/S1.Web/README.md` (Relationship demo)
