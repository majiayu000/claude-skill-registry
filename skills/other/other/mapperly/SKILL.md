---
name: mapperly
description: >
  Guidance for Mapperly compile-time source-generated object mapper.
  USE FOR: high-performance object mapping via source generation, compile-time mapping validation, zero-reflection mapping, AOT-compatible mapping, enum mapping, collection mapping.
  DO NOT USE FOR: runtime convention-based mapping with ProjectTo (use automapper), mapping configurations that change at runtime, mapping that requires DI-injected services.
license: MIT
metadata:
  displayName: "Mapperly"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Mapperly Documentation"
    url: "https://mapperly.riok.app/"
  - title: "Mapperly GitHub Repository"
    url: "https://github.com/riok/mapperly"
  - title: "Riok.Mapperly NuGet Package"
    url: "https://www.nuget.org/packages/Riok.Mapperly"
---

# Mapperly

## Overview

Mapperly (`Riok.Mapperly`) is a compile-time object mapper for .NET that uses C# source generators to produce mapping code at build time. The generated code is equivalent to hand-written property assignments, with no runtime reflection, no expression tree compilation, and no hidden allocations. This makes Mapperly suitable for performance-critical paths, AOT (ahead-of-time) compilation scenarios, and applications where compile-time validation of mappings is important.

Mapperly is configured entirely through attributes on partial classes and methods. The source generator analyzes the source and destination types at compile time and emits the mapping implementation. If a property cannot be mapped (missing or incompatible types), the compiler produces a warning or error, catching mistakes during the build rather than at runtime.

## Basic Mapper Definition

Define a partial class with the `[Mapper]` attribute. Declare partial methods for each mapping, and Mapperly generates the implementations.

```csharp
using Riok.Mapperly.Abstractions;

namespace MyApp.Mapping;

[Mapper]
public partial class OrderMapper
{
    public partial OrderDto MapToDto(Order order);
    public partial Order MapToEntity(CreateOrderRequest request);
    public partial IEnumerable<OrderDto> MapToDtos(
        IEnumerable<Order> orders);
}

public record Order(
    Guid Id, string CustomerName, decimal Total,
    DateTime CreatedAt, List<OrderItem> Items);
public record OrderItem(
    string ProductName, int Quantity, decimal Price);
public record OrderDto(
    Guid Id, string CustomerName, decimal Total,
    DateTime CreatedAt, List<OrderItemDto> Items);
public record OrderItemDto(
    string ProductName, int Quantity, decimal Price);
public record CreateOrderRequest(
    string CustomerName, decimal Total,
    List<OrderItemDto> Items);
```

## Custom Property Mapping

Use `[MapProperty]` to map between properties with different names.

```csharp
using Riok.Mapperly.Abstractions;

namespace MyApp.Mapping;

[Mapper]
public partial class CustomerMapper
{
    [MapProperty(nameof(Customer.FullName), nameof(CustomerDto.Name))]
    [MapProperty(
        nameof(Customer.EmailAddress),
        nameof(CustomerDto.Email))]
    public partial CustomerDto MapToDto(Customer customer);

    [MapperIgnoreSource(nameof(Customer.PasswordHash))]
    [MapperIgnoreTarget(nameof(CustomerDto.DisplayBadge))]
    public partial CustomerDto MapToPublicDto(Customer customer);
}

public record Customer(
    Guid Id, string FullName, string EmailAddress,
    string PasswordHash, DateTime CreatedAt);
public record CustomerDto(
    Guid Id, string Name, string Email,
    DateTime CreatedAt, string? DisplayBadge);
```

## Custom Mapping Methods

Implement specific member mappings by providing a non-partial method. Mapperly will use it for matching types.

```csharp
using Riok.Mapperly.Abstractions;

namespace MyApp.Mapping;

[Mapper]
public partial class ProductMapper
{
    public partial ProductDto MapToDto(Product product);

    // Custom mapping for Money -> string
    private string MapMoney(Money money)
        => $"{money.Amount:F2} {money.Currency}";

    // Custom mapping for DateTimeOffset -> string
    private string MapDate(DateTimeOffset date)
        => date.ToString("yyyy-MM-dd");

    // Enum mapping with explicit values
    [MapEnum(EnumMappingStrategy.ByName)]
    private partial ProductCategoryDto MapCategory(
        ProductCategory category);
}

public record Product(
    Guid Id, string Name, Money Price,
    DateTimeOffset ListedAt, ProductCategory Category);
public record Money(decimal Amount, string Currency);
public record ProductDto(
    Guid Id, string Name, string Price,
    string ListedAt, ProductCategoryDto Category);
public enum ProductCategory { Electronics, Clothing, Food }
public enum ProductCategoryDto { Electronics, Clothing, Food }
```

## Enum Mapping

Mapperly supports different strategies for mapping enums: by value (default), by name, or with explicit mappings.

```csharp
using Riok.Mapperly.Abstractions;

namespace MyApp.Mapping;

[Mapper]
public partial class StatusMapper
{
    // Map by name (string comparison)
    [MapEnum(EnumMappingStrategy.ByName)]
    public partial ExternalStatus MapStatus(InternalStatus status);

    // Explicit enum value mapping
    [MapEnumValue(InternalStatus.InProgress, ExternalStatus.Active)]
    [MapEnumValue(InternalStatus.Done, ExternalStatus.Completed)]
    public partial ExternalStatus MapStatusExplicit(
        InternalStatus status);
}

public enum InternalStatus { Draft, InProgress, Done, Cancelled }
public enum ExternalStatus { Draft, Active, Completed, Cancelled }
```

## Nullable and Collection Handling

Mapperly handles nullable types, collections, and dictionaries automatically.

```csharp
using Riok.Mapperly.Abstractions;

namespace MyApp.Mapping;

[Mapper]
public partial class InventoryMapper
{
    // Nullable source to nullable destination
    public partial WarehouseDto? MapWarehouse(Warehouse? warehouse);

    // List mapping (generates a loop)
    public partial List<ItemDto> MapItems(List<Item> items);

    // Dictionary mapping
    public partial Dictionary<string, ItemDto> MapInventory(
        Dictionary<string, Item> inventory);

    // Array mapping
    public partial ItemDto[] MapItemArray(Item[] items);
}

public record Warehouse(string Name, string Location);
public record WarehouseDto(string Name, string Location);
public record Item(string Sku, string Name, int Quantity);
public record ItemDto(string Sku, string Name, int Quantity);
```

## DI Registration and Usage

Mapperly mappers are plain classes with no runtime dependencies, making registration straightforward.

```csharp
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.DependencyInjection;

var builder = WebApplication.CreateBuilder(args);

// Register as singleton since mappers are stateless
builder.Services.AddSingleton<MyApp.Mapping.OrderMapper>();
builder.Services.AddSingleton<MyApp.Mapping.CustomerMapper>();

var app = builder.Build();

app.MapGet("/orders/{id:guid}",
    async (Guid id, OrderMapper mapper, IOrderRepository repo) =>
    {
        var order = await repo.GetByIdAsync(id);
        return order is null
            ? Results.NotFound()
            : Results.Ok(mapper.MapToDto(order));
    });

app.Run();
```

## Mapper Configuration

Global mapper settings are configured via the `[Mapper]` attribute.

```csharp
using Riok.Mapperly.Abstractions;

namespace MyApp.Mapping;

[Mapper(
    EnumMappingStrategy = EnumMappingStrategy.ByName,
    EnumMappingIgnoreCase = true,
    ThrowOnMappingNullMismatch = true,
    ThrowOnPropertyMappingNullMismatch = false,
    UseDeepCloning = false)]
public partial class StrictMapper
{
    public partial OrderDto MapOrder(Order order);
}
```

## Mapperly vs AutoMapper

| Feature | Mapperly | AutoMapper |
|---|---|---|
| Mapping generation | Compile-time source gen | Runtime reflection |
| Performance | Near hand-written | Moderate (cached expressions) |
| AOT compatible | Yes | No |
| Configuration | Attributes on partial classes | Fluent API in Profile classes |
| Compile-time errors | Yes (missing properties) | No (runtime validation) |
| IQueryable ProjectTo | Not supported | Built-in |
| DI-injected resolvers | Not supported | Yes (IValueResolver) |
| Custom logic | Non-partial methods in mapper | Value resolvers, type converters |
| Learning curve | Low (attributes + partial methods) | Moderate (Profiles, resolvers) |

## Best Practices

1. **Prefer Mapperly over AutoMapper** for new projects and performance-sensitive paths because source-generated code has zero runtime overhead and catches mapping errors at compile time.
2. **Define one mapper class per aggregate or feature area** (e.g., `OrderMapper`, `CustomerMapper`) to keep mapping logic organized and discoverable.
3. **Register mappers as singletons** in the DI container since they are stateless and thread-safe, with no per-request state to manage.
4. **Use `[MapProperty]` for name mismatches** instead of renaming domain or DTO properties, preserving the natural naming of each layer.
5. **Provide custom non-partial methods** for complex value transformations (e.g., `Money` to `string`, `DateTimeOffset` to formatted string) and Mapperly will automatically use them for matching types.
6. **Use `[MapperIgnoreSource]` and `[MapperIgnoreTarget]`** to explicitly suppress warnings for properties that should not be mapped, such as `PasswordHash` or computed fields.
7. **Review the generated source code** (visible in the IDE or in `obj/`) to verify that Mapperly produces the expected assignments, especially for nested objects and collections.
8. **Use `[MapEnum(EnumMappingStrategy.ByName)]`** when source and destination enums have the same member names but different underlying values to avoid silent data corruption.
9. **Enable `ThrowOnMappingNullMismatch`** in the `[Mapper]` attribute during development to surface null-safety issues, then decide on production behavior based on your error-handling strategy.
10. **Combine with AutoMapper only when you need `ProjectTo`** for EF Core queries; use Mapperly for in-memory object mapping and AutoMapper exclusively for IQueryable projection.
