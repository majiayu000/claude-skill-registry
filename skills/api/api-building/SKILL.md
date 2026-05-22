---
name: koan-api-building
description: EntityController<T>, custom routes, payload transformers, auth policies
---

# Koan API Building

## Core Principle

**EntityController<T> provides full CRUD APIs automatically.** Extend with custom routes for business operations. No manual endpoint implementation needed.

## Quick Reference

### Basic CRUD API

```csharp
[Route("api/[controller]")]
public class TodosController : EntityController<Todo>
{
    // Full CRUD auto-generated:
    // GET    /api/todos
    // GET    /api/todos/{id}
    // POST   /api/todos
    // PUT    /api/todos/{id}
    // DELETE /api/todos/{id}
    // PATCH  /api/todos/{id}
}
```

### Custom Routes

```csharp
[Route("api/[controller]")]
public class ProductsController : EntityController<Product>
{
    [HttpPost("{id}/discount")]
    public async Task<IActionResult> ApplyDiscount(
        string id,
        [FromBody] DiscountRequest request,
        CancellationToken ct)
    {
        var product = await Product.Get(id, ct);
        if (product is null) return NotFound();

        await product.ApplyDiscount(request.Amount);
        return Ok(product);
    }

    [HttpGet("overstock")]
    public async Task<IActionResult> GetOverstock(CancellationToken ct)
    {
        var products = await Product.Query(p => p.Stock > 1000, ct);
        return Ok(products);
    }
}
```

### Auth Policies

```csharp
[Route("api/[controller]")]
[Authorize] // Require authentication for all endpoints
public class OrdersController : EntityController<Order>
{
    [HttpGet]
    public Task<List<Order>> GetMyOrders(CancellationToken ct)
    {
        var userEmail = User.FindFirst(ClaimTypes.Email)?.Value;
        return Order.Query(o => o.CustomerEmail == userEmail, ct);
    }

    [HttpPost]
    [Authorize(Policy = "CanCreateOrders")] // Require specific policy
    public override async Task<IActionResult> Post([FromBody] Order entity)
    {
        entity.CustomerEmail = User.FindFirst(ClaimTypes.Email)?.Value ?? "";
        return await base.Post(entity);
    }
}
```

### Payload Transformers

```csharp
public class TodoTransformer : IPayloadTransformer<Todo>
{
    public Task<object> TransformAsync(Todo entity)
    {
        return Task.FromResult<object>(new
        {
            entity.Id,
            entity.Title,
            entity.Completed,
            _links = new
            {
                self = $"/api/todos/{entity.Id}",
                user = $"/api/users/{entity.UserId}"
            }
        });
    }
}

// Register in KoanAutoRegistrar
services.AddScoped<IPayloadTransformer<Todo>, TodoTransformer>();
```

## When This Skill Applies

- ✅ Building REST APIs
- ✅ Custom endpoints
- ✅ Authentication/authorization
- ✅ Response formatting
- ✅ Error handling
- ✅ API versioning

## Reference Documentation

- **Full Guide:** `docs/guides/building-apis.md`
- **API Conventions:** `docs/api/web-http-api.md`
- **Sample:** `samples/S1.Web/Controllers/`
