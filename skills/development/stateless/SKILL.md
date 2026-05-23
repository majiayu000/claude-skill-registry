---
name: stateless
description: >
  Guidance for Stateless state machine library for .NET.
  USE FOR: modeling state transitions with guards and actions, workflow engines, order processing pipelines, device lifecycle management, protocol implementations, approval workflows.
  DO NOT USE FOR: distributed state machines (use Durable Functions or Temporal), event sourcing (use Marten), full BPMN workflow engines (use Elsa), simple boolean flags.
license: MIT
metadata:
  displayName: Stateless
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Stateless GitHub Repository"
    url: "https://github.com/dotnet-state-machine/stateless"
  - title: "Stateless NuGet Package"
    url: "https://www.nuget.org/packages/Stateless"
---

# Stateless

## Overview

Stateless is a lightweight library for creating state machines in .NET. It uses a fluent configuration API to define states, triggers, guard conditions, entry/exit actions, and sub-states. State machines built with Stateless are in-memory and synchronous by default, with support for async triggers.

Stateless is ideal for modeling domain workflows where an entity transitions through a defined set of states in response to events (triggers). Examples include order processing, device lifecycle, approval workflows, and protocol implementations.

Install via NuGet:
```
dotnet add package Stateless
```

## Basic State Machine

Define states and triggers as enums, then configure valid transitions.

```csharp
using Stateless;

public enum OrderState
{
    Draft,
    Submitted,
    Approved,
    Rejected,
    Shipped,
    Delivered,
    Cancelled
}

public enum OrderTrigger
{
    Submit,
    Approve,
    Reject,
    Ship,
    Deliver,
    Cancel
}

var machine = new StateMachine<OrderState, OrderTrigger>(OrderState.Draft);

machine.Configure(OrderState.Draft)
    .Permit(OrderTrigger.Submit, OrderState.Submitted)
    .Permit(OrderTrigger.Cancel, OrderState.Cancelled);

machine.Configure(OrderState.Submitted)
    .Permit(OrderTrigger.Approve, OrderState.Approved)
    .Permit(OrderTrigger.Reject, OrderState.Rejected)
    .Permit(OrderTrigger.Cancel, OrderState.Cancelled);

machine.Configure(OrderState.Approved)
    .Permit(OrderTrigger.Ship, OrderState.Shipped)
    .Permit(OrderTrigger.Cancel, OrderState.Cancelled);

machine.Configure(OrderState.Shipped)
    .Permit(OrderTrigger.Deliver, OrderState.Delivered);

// Fire triggers
Console.WriteLine($"State: {machine.State}"); // Draft
machine.Fire(OrderTrigger.Submit);
Console.WriteLine($"State: {machine.State}"); // Submitted
machine.Fire(OrderTrigger.Approve);
Console.WriteLine($"State: {machine.State}"); // Approved
```

## Guard Conditions

Use guards to allow transitions only when specific conditions are met.

```csharp
using Stateless;

public class OrderProcessor
{
    private readonly StateMachine<OrderState, OrderTrigger> _machine;
    private decimal _orderTotal;
    private string? _approverName;

    public OrderProcessor(decimal orderTotal)
    {
        _orderTotal = orderTotal;
        _machine = new StateMachine<OrderState, OrderTrigger>(OrderState.Draft);

        _machine.Configure(OrderState.Draft)
            .PermitIf(OrderTrigger.Submit, OrderState.Submitted,
                () => _orderTotal > 0, "Order total must be positive");

        _machine.Configure(OrderState.Submitted)
            .PermitIf(OrderTrigger.Approve, OrderState.Approved,
                () => _approverName is not null, "Approver must be set")
            .PermitIf(OrderTrigger.Approve, OrderState.Approved,
                () => _orderTotal <= 10000, "Orders over $10,000 require VP approval")
            .Permit(OrderTrigger.Reject, OrderState.Rejected);

        _machine.Configure(OrderState.Approved)
            .Permit(OrderTrigger.Ship, OrderState.Shipped);
    }

    public OrderState State => _machine.State;

    public void SetApprover(string name) => _approverName = name;

    public bool CanFire(OrderTrigger trigger) => _machine.CanFire(trigger);

    public void Fire(OrderTrigger trigger) => _machine.Fire(trigger);
}
```

## Entry and Exit Actions

Execute logic when entering or exiting a state.

```csharp
using System;
using Stateless;
using Microsoft.Extensions.Logging;

public class DocumentWorkflow
{
    private readonly StateMachine<DocState, DocTrigger> _machine;
    private readonly ILogger _logger;

    public enum DocState { Draft, Review, Approved, Published, Archived }
    public enum DocTrigger { SubmitForReview, Approve, Reject, Publish, Archive }

    public DocumentWorkflow(ILogger<DocumentWorkflow> logger)
    {
        _logger = logger;
        _machine = new StateMachine<DocState, DocTrigger>(DocState.Draft);

        _machine.Configure(DocState.Draft)
            .Permit(DocTrigger.SubmitForReview, DocState.Review)
            .OnExit(() => _logger.LogInformation("Document left draft state"));

        _machine.Configure(DocState.Review)
            .Permit(DocTrigger.Approve, DocState.Approved)
            .Permit(DocTrigger.Reject, DocState.Draft)
            .OnEntry(() =>
            {
                _logger.LogInformation("Document entered review at {Time}", DateTime.UtcNow);
                NotifyReviewers();
            })
            .OnExit(transition =>
                _logger.LogInformation("Leaving review via {Trigger}", transition.Trigger));

        _machine.Configure(DocState.Approved)
            .Permit(DocTrigger.Publish, DocState.Published)
            .OnEntry(() => _logger.LogInformation("Document approved"));

        _machine.Configure(DocState.Published)
            .Permit(DocTrigger.Archive, DocState.Archived)
            .OnEntry(() =>
            {
                _logger.LogInformation("Document published");
                UpdateSearchIndex();
            });
    }

    public DocState State => _machine.State;
    public void Fire(DocTrigger trigger) => _machine.Fire(trigger);

    private void NotifyReviewers() { /* send emails */ }
    private void UpdateSearchIndex() { /* update search */ }
}
```

## Parameterized Triggers

Pass data with triggers using parameterized trigger types.

```csharp
using Stateless;

public class TicketMachine
{
    public enum State { Open, Assigned, InProgress, Resolved, Closed }
    public enum Trigger { Assign, StartWork, Resolve, Close, Reopen }

    private readonly StateMachine<State, Trigger> _machine;
    private readonly StateMachine<State, Trigger>.TriggerWithParameters<string> _assignTrigger;
    private readonly StateMachine<State, Trigger>.TriggerWithParameters<string> _resolveTrigger;

    private string? _assignee;
    private string? _resolution;

    public TicketMachine()
    {
        _machine = new StateMachine<State, Trigger>(State.Open);
        _assignTrigger = _machine.SetTriggerParameters<string>(Trigger.Assign);
        _resolveTrigger = _machine.SetTriggerParameters<string>(Trigger.Resolve);

        _machine.Configure(State.Open)
            .Permit(Trigger.Assign, State.Assigned);

        _machine.Configure(State.Assigned)
            .OnEntryFrom(_assignTrigger, assignee =>
            {
                _assignee = assignee;
                Console.WriteLine($"Ticket assigned to {assignee}");
            })
            .Permit(Trigger.StartWork, State.InProgress)
            .Permit(Trigger.Close, State.Closed);

        _machine.Configure(State.InProgress)
            .Permit(Trigger.Resolve, State.Resolved);

        _machine.Configure(State.Resolved)
            .OnEntryFrom(_resolveTrigger, resolution =>
            {
                _resolution = resolution;
                Console.WriteLine($"Resolved: {resolution}");
            })
            .Permit(Trigger.Close, State.Closed)
            .Permit(Trigger.Reopen, State.Open);

        _machine.Configure(State.Closed)
            .Permit(Trigger.Reopen, State.Open);
    }

    public void Assign(string assignee) => _machine.Fire(_assignTrigger, assignee);
    public void Resolve(string resolution) => _machine.Fire(_resolveTrigger, resolution);
    public void Fire(Trigger trigger) => _machine.Fire(trigger);
    public State CurrentState => _machine.State;
}
```

## Async State Machine

Use async entry/exit actions and async trigger firing.

```csharp
using System.Threading.Tasks;
using Stateless;

public class AsyncPaymentProcessor
{
    public enum State { Pending, Processing, Succeeded, Failed, Refunded }
    public enum Trigger { Process, Succeed, Fail, Refund }

    private readonly StateMachine<State, Trigger> _machine;

    public AsyncPaymentProcessor()
    {
        _machine = new StateMachine<State, Trigger>(State.Pending);

        _machine.Configure(State.Pending)
            .Permit(Trigger.Process, State.Processing);

        _machine.Configure(State.Processing)
            .OnEntryAsync(async () =>
            {
                await CallPaymentGatewayAsync();
            })
            .Permit(Trigger.Succeed, State.Succeeded)
            .Permit(Trigger.Fail, State.Failed);

        _machine.Configure(State.Succeeded)
            .OnEntryAsync(async () =>
            {
                await SendConfirmationEmailAsync();
            })
            .Permit(Trigger.Refund, State.Refunded);

        _machine.Configure(State.Failed)
            .Permit(Trigger.Process, State.Processing); // retry
    }

    public async Task ProcessAsync()
    {
        await _machine.FireAsync(Trigger.Process);
    }

    public State CurrentState => _machine.State;

    private async Task CallPaymentGatewayAsync() => await Task.Delay(100);
    private async Task SendConfirmationEmailAsync() => await Task.Delay(50);
}
```

## Generating State Machine Diagrams

Stateless can export its configuration to DOT format for visualization.

```csharp
using Stateless;
using Stateless.Graph;

var machine = new StateMachine<OrderState, OrderTrigger>(OrderState.Draft);
// ... configure machine ...

// Generate DOT graph
string dotGraph = UmlDotGraph.Format(machine.GetInfo());
Console.WriteLine(dotGraph);
// Output can be rendered with Graphviz or online tools

// Query permitted triggers
var permitted = machine.GetPermittedTriggers();
Console.WriteLine($"Permitted triggers: {string.Join(", ", permitted)}");
```

## Best Practices

1. **Define states and triggers as enums** rather than strings to get compile-time safety and prevent typos in state/trigger names.
2. **Use guard conditions (`PermitIf`)** to enforce business rules at the transition level rather than checking preconditions in calling code.
3. **Provide human-readable guard descriptions** as the last parameter to `PermitIf` so that `GetPermittedTriggers` and diagram exports show why a transition is blocked.
4. **Use `OnEntry`/`OnExit` actions for side effects** (logging, notifications, database updates) rather than placing them in the code that calls `Fire`.
5. **Call `CanFire` before `Fire`** in UI-driven scenarios to enable/disable buttons based on valid transitions, preventing `InvalidOperationException`.
6. **Use parameterized triggers** to pass context data (assignee, reason, amount) into entry actions rather than setting instance fields before firing.
7. **Use `FireAsync` and `OnEntryAsync`** when entry/exit actions involve I/O operations (database, HTTP calls) to avoid blocking threads.
8. **Externalize state storage** by using the `StateMachine<TState, TTrigger>(stateAccessor, stateMutator)` constructor overload to persist state in a database or cache.
9. **Export DOT diagrams** with `UmlDotGraph.Format` during development to visually verify that the state machine matches the intended workflow design.
10. **Handle `InvalidOperationException`** from invalid transitions gracefully by logging the current state and attempted trigger rather than letting the exception propagate unhandled.
