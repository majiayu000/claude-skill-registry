---
name: peasy
description: |
  USE FOR: Implementing business rules as composable, testable rule objects using the Peasy framework. Use when building middle-tier validation pipelines for commands and services that require rule chaining, async validation, and conditional execution.
  DO NOT USE FOR: Simple argument null checks (use CommunityToolkit Guard), form-level input validation (use FluentValidation or DataAnnotations), or full CQRS/event-sourcing frameworks (use MediatR or Wolverine).
license: MIT
metadata:
  displayName: Peasy
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Peasy.NET GitHub Repository"
    url: "https://github.com/peasy/Peasy.NET"
  - title: "Peasy.NET Wiki"
    url: "https://github.com/peasy/Peasy.NET/wiki"
  - title: "Peasy NuGet Package"
    url: "https://www.nuget.org/packages/Peasy"
---

# Peasy

## Overview

Peasy is a lightweight .NET middle-tier framework that provides patterns for implementing business logic through composable rules, commands, and services. The core abstraction is `RuleBase`, a base class for business rules that can be validated individually or chained together. Rules encapsulate a single business invariant and produce an `ErrorMessage` when violated. Peasy supports async rule validation, rule chaining with `IfValidThenValidate`, and integration with service layers via the `ServiceBase<T>` class that orchestrates rules before executing data operations.

## Basic Business Rules

Create rules by inheriting from `RuleBase` and overriding `OnValidateAsync`.

```csharp
using Peasy;

namespace MyApp.Rules;

public class OrderMinimumAmountRule : RuleBase
{
    private readonly decimal _orderTotal;
    private readonly decimal _minimumAmount;

    public OrderMinimumAmountRule(decimal orderTotal, decimal minimumAmount = 10.00m)
    {
        _orderTotal = orderTotal;
        _minimumAmount = minimumAmount;
    }

    protected override Task OnValidateAsync()
    {
        if (_orderTotal < _minimumAmount)
        {
            Invalidate($"Order total must be at least {_minimumAmount:C2}. Current total: {_orderTotal:C2}.");
        }

        return Task.CompletedTask;
    }
}

public class CustomerIsActiveRule : RuleBase
{
    private readonly ICustomerRepository _customerRepo;
    private readonly int _customerId;

    public CustomerIsActiveRule(ICustomerRepository customerRepo, int customerId)
    {
        _customerRepo = customerRepo;
        _customerId = customerId;
    }

    protected override async Task OnValidateAsync()
    {
        var customer = await _customerRepo.GetByIdAsync(_customerId);

        if (customer is null)
        {
            Invalidate($"Customer with ID {_customerId} was not found.");
            return;
        }

        if (!customer.IsActive)
        {
            Invalidate($"Customer '{customer.Name}' is deactivated and cannot place orders.");
        }
    }
}

public class InventoryAvailableRule : RuleBase
{
    private readonly IInventoryRepository _inventoryRepo;
    private readonly string _productId;
    private readonly int _requestedQuantity;

    public InventoryAvailableRule(
        IInventoryRepository inventoryRepo,
        string productId,
        int requestedQuantity)
    {
        _inventoryRepo = inventoryRepo;
        _productId = productId;
        _requestedQuantity = requestedQuantity;
    }

    protected override async Task OnValidateAsync()
    {
        var stock = await _inventoryRepo.GetStockAsync(_productId);

        if (stock < _requestedQuantity)
        {
            Invalidate(
                $"Insufficient inventory for product {_productId}. " +
                $"Requested: {_requestedQuantity}, Available: {stock}.");
        }
    }
}
```

## Rule Chaining with IfValidThenValidate

Chain rules so that dependent rules only execute if prerequisite rules pass.

```csharp
using Peasy;

namespace MyApp.Rules;

public class CanPlaceOrderRuleSet
{
    private readonly ICustomerRepository _customerRepo;
    private readonly IInventoryRepository _inventoryRepo;

    public CanPlaceOrderRuleSet(
        ICustomerRepository customerRepo,
        IInventoryRepository inventoryRepo)
    {
        _customerRepo = customerRepo;
        _inventoryRepo = inventoryRepo;
    }

    public IEnumerable<IRule> GetRules(Order order)
    {
        // First validate customer is active, then check order rules
        var customerActiveRule = new CustomerIsActiveRule(
            _customerRepo, order.CustomerId);

        // These rules only run if the customer is active
        var minimumAmountRule = new OrderMinimumAmountRule(order.Total);
        var inventoryRules = order.Items.Select(item =>
            new InventoryAvailableRule(
                _inventoryRepo, item.ProductId, item.Quantity));

        // Chain: customer must be active before checking inventory
        customerActiveRule
            .IfValidThenValidate(minimumAmountRule)
            .IfValidThenValidate(inventoryRules.ToArray());

        yield return customerActiveRule;
    }
}
```

## Service Layer with Rule Orchestration

Use Peasy's service pattern to orchestrate rule execution before data operations.

```csharp
using Peasy;

namespace MyApp.Services;

public class OrderService
{
    private readonly IOrderRepository _orderRepo;
    private readonly ICustomerRepository _customerRepo;
    private readonly IInventoryRepository _inventoryRepo;

    public OrderService(
        IOrderRepository orderRepo,
        ICustomerRepository customerRepo,
        IInventoryRepository inventoryRepo)
    {
        _orderRepo = orderRepo;
        _customerRepo = customerRepo;
        _inventoryRepo = inventoryRepo;
    }

    public async Task<ExecutionResult<Order>> CreateOrderAsync(Order order)
    {
        var ruleSet = new CanPlaceOrderRuleSet(_customerRepo, _inventoryRepo);
        var rules = ruleSet.GetRules(order);

        // Validate all rules
        var errors = new List<string>();
        foreach (var rule in rules)
        {
            var result = await rule.ValidateAsync();
            if (!result.IsValid)
            {
                errors.Add(result.ErrorMessage);
            }
        }

        if (errors.Count > 0)
        {
            return new ExecutionResult<Order>
            {
                Success = false,
                Errors = errors
            };
        }

        // All rules passed, execute the operation
        var created = await _orderRepo.InsertAsync(order);
        await _inventoryRepo.DecrementStockAsync(order.Items);

        return new ExecutionResult<Order>
        {
            Success = true,
            Value = created
        };
    }
}

public class ExecutionResult<T>
{
    public bool Success { get; set; }
    public T? Value { get; set; }
    public List<string> Errors { get; set; } = new();
}
```

## Integration with ASP.NET Core Endpoints

Map rule execution results to HTTP responses.

```csharp
app.MapPost("/api/orders", async (
    CreateOrderDto dto,
    OrderService orderService) =>
{
    var order = new Order
    {
        CustomerId = dto.CustomerId,
        Items = dto.Items.Select(i => new OrderItem
        {
            ProductId = i.ProductId,
            Quantity = i.Quantity,
            UnitPrice = i.UnitPrice
        }).ToList(),
        Total = dto.Items.Sum(i => i.Quantity * i.UnitPrice)
    };

    var result = await orderService.CreateOrderAsync(order);

    if (!result.Success)
    {
        return Results.BadRequest(new { result.Errors });
    }

    return Results.Created($"/api/orders/{result.Value!.Id}", result.Value);
});
```

## Peasy vs Other Validation/Rules Approaches

| Feature | Peasy | FluentValidation | MediatR Behaviors | Plastic |
|---|---|---|---|---|
| Focus | Business rules + services | Input validation | Pipeline cross-cuts | Command pipelines |
| Rule object | `RuleBase` | `AbstractValidator<T>` | `IPipelineBehavior` | `ICommand` |
| Chaining | `IfValidThenValidate` | RuleSet groups | Middleware chain | Pipeline |
| Async | Yes | Yes | Yes | No |
| Service integration | `ServiceBase<T>` | Manual | Handler pattern | Manual |
| Error type | `ErrorMessage` string | `ValidationFailure` | Exception-based | Exception-based |

## Best Practices

1. **Encode exactly one business invariant per rule class** (e.g., "customer must be active", "inventory must be available") so that each rule has a single reason to change, can be independently unit tested, and produces a clear, specific error message when violated.

2. **Use `IfValidThenValidate` to chain dependent rules** so that downstream rules only execute when prerequisite rules pass; for example, skip inventory checks if the customer is not active, avoiding unnecessary database queries and misleading compound error messages.

3. **Inject repository or service dependencies through the rule's constructor** rather than accessing static services or `ServiceLocator`, so that rules can be unit tested with mock repositories that return controlled data without hitting a database.

4. **Return `ExecutionResult<T>` from service methods instead of throwing exceptions on business rule failures**, because rule violations are expected outcomes (not programming errors) and should be communicated to the caller as structured error lists that map to HTTP 400 responses.

5. **Collect all rule errors before returning to the caller** by iterating through the full rule set rather than short-circuiting on the first failure, so that API consumers receive all violations in a single response and can fix them in one attempt.

6. **Create a `RuleSet` class (e.g., `CanPlaceOrderRuleSet`) that encapsulates related rules for a use case** rather than scattering rule instantiation across service methods, keeping rule composition testable and reusable across multiple entry points (API, message handler, scheduled job).

7. **Name rule classes as assertions starting with the condition** (e.g., `CustomerIsActiveRule`, `InventoryAvailableRule`, `OrderMinimumAmountRule`) rather than action verbs, because the name should describe the invariant being checked, not the action being performed.

8. **Write unit tests for each rule in isolation** by mocking the repository to return specific data and asserting on `rule.ValidateAsync().IsValid` and `.ErrorMessage`, independent of the service layer or HTTP pipeline; test the rule set composition separately.

9. **Use Peasy rules for cross-aggregate business invariants** (e.g., "customer credit limit not exceeded across all open orders") that span multiple repositories, and use simple Guard clauses or value objects for single-entity invariants (e.g., "email format is valid").

10. **Map `ExecutionResult.Errors` to HTTP `400 BadRequest` with a structured JSON body** containing an `errors` array and use HTTP `422 UnprocessableEntity` when the request is syntactically valid but violates business rules, distinguishing between input format errors and domain logic rejections.
