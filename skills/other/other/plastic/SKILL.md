---
name: plastic
description: |
  USE FOR: Implementing business workflows as command pipelines using the Plastic library's command pattern. Use when orchestrating multi-step operations with validation, execution, and rollback semantics.
  DO NOT USE FOR: Simple input validation (use FluentValidation), individual guard clauses (use CommunityToolkit Guard), or full event-sourcing/CQRS frameworks (use MediatR, Wolverine, or MassTransit).
license: MIT
metadata:
  displayName: Plastic
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Plastic GitHub Repository"
    url: "https://github.com/sang-hyeon/Plastic"
---

# Plastic

## Overview

Plastic is a lightweight .NET library that implements the command pattern for building validation and execution pipelines. Commands encapsulate a unit of work with validation logic and execution logic. Commands can be composed into pipelines where each command executes sequentially, with built-in support for validation before execution and rollback on failure. Plastic is useful for orchestrating multi-step business workflows where each step may have preconditions and side effects that need to be undone if a later step fails.

## Basic Command Implementation

Create commands by implementing validation and execution logic.

```csharp
namespace MyApp.Commands;

public interface ICommand
{
    bool IsValid { get; }
    string? ErrorMessage { get; }
    void Validate();
    void Execute();
}

public interface ICommand<T> : ICommand
{
    T Result { get; }
}

public abstract class CommandBase : ICommand
{
    public bool IsValid { get; private set; } = true;
    public string? ErrorMessage { get; private set; }

    protected void Invalidate(string message)
    {
        IsValid = false;
        ErrorMessage = message;
    }

    public abstract void Validate();
    public abstract void Execute();
}

public abstract class CommandBase<T> : CommandBase, ICommand<T>
{
    public T Result { get; protected set; } = default!;
}
```

## Concrete Command with Validation

Implement commands that validate preconditions before executing business logic.

```csharp
namespace MyApp.Commands;

public class CreateOrderCommand : CommandBase<Order>
{
    private readonly IOrderRepository _orderRepo;
    private readonly IInventoryService _inventoryService;
    private readonly ICustomerRepository _customerRepo;
    private readonly CreateOrderRequest _request;

    public CreateOrderCommand(
        IOrderRepository orderRepo,
        IInventoryService inventoryService,
        ICustomerRepository customerRepo,
        CreateOrderRequest request)
    {
        _orderRepo = orderRepo;
        _inventoryService = inventoryService;
        _customerRepo = customerRepo;
        _request = request;
    }

    public override void Validate()
    {
        if (_request.Items.Count == 0)
        {
            Invalidate("Order must contain at least one item.");
            return;
        }

        if (_request.Items.Any(i => i.Quantity <= 0))
        {
            Invalidate("All item quantities must be greater than zero.");
            return;
        }

        var customer = _customerRepo.GetById(_request.CustomerId);
        if (customer is null)
        {
            Invalidate($"Customer {_request.CustomerId} not found.");
            return;
        }

        if (!customer.IsActive)
        {
            Invalidate($"Customer '{customer.Name}' is not active.");
            return;
        }

        foreach (var item in _request.Items)
        {
            var stock = _inventoryService.GetStock(item.ProductId);
            if (stock < item.Quantity)
            {
                Invalidate($"Insufficient stock for {item.ProductId}. " +
                           $"Available: {stock}, Requested: {item.Quantity}.");
                return;
            }
        }
    }

    public override void Execute()
    {
        var order = new Order
        {
            CustomerId = _request.CustomerId,
            Items = _request.Items.Select(i => new OrderItem
            {
                ProductId = i.ProductId,
                Quantity = i.Quantity,
                UnitPrice = i.UnitPrice
            }).ToList(),
            CreatedAt = DateTime.UtcNow,
            Status = OrderStatus.Pending
        };

        order.Total = order.Items.Sum(i => i.Quantity * i.UnitPrice);
        _orderRepo.Insert(order);

        foreach (var item in order.Items)
        {
            _inventoryService.DecrementStock(item.ProductId, item.Quantity);
        }

        Result = order;
    }
}
```

## Command Pipeline

Compose commands into a pipeline that executes them sequentially with validation.

```csharp
namespace MyApp.Pipelines;

public class CommandPipeline
{
    private readonly List<ICommand> _commands = new();
    private readonly List<ICommand> _executedCommands = new();

    public CommandPipeline Add(ICommand command)
    {
        _commands.Add(command);
        return this;
    }

    public PipelineResult Execute()
    {
        // Validate all commands first
        foreach (var command in _commands)
        {
            command.Validate();
            if (!command.IsValid)
            {
                return PipelineResult.Failed(command.ErrorMessage!);
            }
        }

        // Execute all commands
        try
        {
            foreach (var command in _commands)
            {
                command.Execute();
                _executedCommands.Add(command);
            }

            return PipelineResult.Succeeded();
        }
        catch (Exception ex)
        {
            // Rollback executed commands in reverse order
            Rollback();
            return PipelineResult.Failed($"Pipeline failed: {ex.Message}");
        }
    }

    private void Rollback()
    {
        for (int i = _executedCommands.Count - 1; i >= 0; i--)
        {
            if (_executedCommands[i] is IRollbackable rollbackable)
            {
                rollbackable.Rollback();
            }
        }
    }
}

public interface IRollbackable
{
    void Rollback();
}

public class PipelineResult
{
    public bool Success { get; private set; }
    public string? Error { get; private set; }

    public static PipelineResult Succeeded() => new() { Success = true };
    public static PipelineResult Failed(string error) => new() { Success = false, Error = error };
}
```

## Rollbackable Command

Implement commands that can undo their effects on failure.

```csharp
namespace MyApp.Commands;

public class ReserveInventoryCommand : CommandBase, IRollbackable
{
    private readonly IInventoryService _inventoryService;
    private readonly List<OrderItem> _items;
    private readonly List<(string ProductId, int Quantity)> _reservations = new();

    public ReserveInventoryCommand(
        IInventoryService inventoryService,
        List<OrderItem> items)
    {
        _inventoryService = inventoryService;
        _items = items;
    }

    public override void Validate()
    {
        foreach (var item in _items)
        {
            var stock = _inventoryService.GetStock(item.ProductId);
            if (stock < item.Quantity)
            {
                Invalidate($"Cannot reserve {item.Quantity} of {item.ProductId}. Only {stock} available.");
                return;
            }
        }
    }

    public override void Execute()
    {
        foreach (var item in _items)
        {
            _inventoryService.DecrementStock(item.ProductId, item.Quantity);
            _reservations.Add((item.ProductId, item.Quantity));
        }
    }

    public void Rollback()
    {
        foreach (var (productId, quantity) in _reservations)
        {
            _inventoryService.IncrementStock(productId, quantity);
        }
        _reservations.Clear();
    }
}

public class ChargePaymentCommand : CommandBase<string>, IRollbackable
{
    private readonly IPaymentGateway _paymentGateway;
    private readonly decimal _amount;
    private readonly string _paymentMethodId;
    private string? _transactionId;

    public ChargePaymentCommand(
        IPaymentGateway paymentGateway,
        decimal amount,
        string paymentMethodId)
    {
        _paymentGateway = paymentGateway;
        _amount = amount;
        _paymentMethodId = paymentMethodId;
    }

    public override void Validate()
    {
        if (_amount <= 0)
            Invalidate("Payment amount must be positive.");

        if (string.IsNullOrWhiteSpace(_paymentMethodId))
            Invalidate("Payment method is required.");
    }

    public override void Execute()
    {
        _transactionId = _paymentGateway.Charge(_paymentMethodId, _amount);
        Result = _transactionId;
    }

    public void Rollback()
    {
        if (_transactionId is not null)
        {
            _paymentGateway.Refund(_transactionId);
            _transactionId = null;
        }
    }
}
```

## Plastic vs Other Command/Validation Patterns

| Feature | Plastic (Command) | Peasy (Rules) | MediatR (Pipeline) | Saga Pattern |
|---|---|---|---|---|
| Unit of work | Command | Rule | Request Handler | Step |
| Validation | Per-command | Per-rule | Pipeline behavior | Per-step |
| Execution | Sequential pipeline | Rule chain | Handler + behaviors | Orchestrator |
| Rollback | IRollbackable | Not built-in | Not built-in | Compensating actions |
| Async | Optional | Built-in | Built-in | Built-in |
| Composition | Pipeline.Add() | IfValidThenValidate | DI pipeline | State machine |

## Best Practices

1. **Implement `Validate()` to check all preconditions before any side effects** and `Execute()` to perform the actual work, never mixing validation logic into `Execute()`; this separation ensures that calling `Validate()` alone is safe and idempotent for preview or dry-run scenarios.

2. **Implement `IRollbackable` on every command that produces side effects** (database writes, payment charges, inventory decrements, external API calls) and track the state needed to undo those effects, so the pipeline can restore consistency when a later command fails.

3. **Store undo state in the command instance** (e.g., `_reservations`, `_transactionId`) during `Execute()` so that `Rollback()` has the information it needs; do not rely on re-querying the database for rollback data because the state may have changed between execution and rollback.

4. **Order commands in the pipeline from least-side-effectful to most-side-effectful** (validate-only commands first, then database writes, then external API calls like payment charges last), minimizing the number of commands that need rollback when a late-stage command fails.

5. **Return `PipelineResult` objects from the pipeline rather than throwing exceptions** for business-rule failures, because pipeline failures are expected outcomes that should be communicated as structured responses; reserve exceptions for unexpected infrastructure errors.

6. **Create separate command classes for each discrete side effect** (e.g., `ReserveInventoryCommand`, `ChargePaymentCommand`, `SendConfirmationEmailCommand`) rather than combining multiple operations in a single command, so that each command's rollback logic is clear and self-contained.

7. **Unit test each command's `Validate()` and `Execute()` independently** by mocking dependencies and asserting on `IsValid`, `ErrorMessage`, and `Result`, then test the pipeline composition with integration tests that verify the full sequence including rollback.

8. **Do not reuse command instances across multiple pipeline executions** because commands store internal state (validation results, execution state, rollback data) from the previous run; create fresh command instances for each pipeline execution to avoid stale state leaking between runs.

9. **Log the start and completion of each command in the pipeline** with the command class name and duration, so that pipeline failures can be diagnosed by examining which command succeeded and which failed, without stepping through the entire pipeline in a debugger.

10. **Use the pipeline pattern for multi-step workflows (order fulfillment, user registration, batch processing)** that involve multiple repositories or external services, but do not use it for single-step operations where a simple service method with Guard clauses is sufficient.
