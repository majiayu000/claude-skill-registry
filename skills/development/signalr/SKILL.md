---
name: signalr
description: |
  Implements real-time WebSocket communication and SignalR hub subscriptions.
  Use when: Adding real-time updates, broadcasting state changes, implementing client subscriptions, or configuring WebSocket connections in Blazor WASM.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# SignalR Skill

Real-time communication in VanDaemon uses SignalR for WebSocket-based updates between the .NET API and Blazor WASM frontend. The hub at `/hubs/telemetry` broadcasts tank levels, control states, and alerts to subscribed client groups. Background services poll hardware every 5 seconds and push changes via `IHubContext`.

## Quick Start

### Server Hub Definition

```csharp
// src/Backend/VanDaemon.Api/Hubs/TelemetryHub.cs
public class TelemetryHub : Hub
{
    public async Task SubscribeToTanks()
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, "tanks");
    }

    public async Task SubscribeToControls()
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, "controls");
    }

    public async Task SubscribeToAlerts()
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, "alerts");
    }
}
```

### Broadcasting from Background Service

```csharp
// Inject IHubContext<TelemetryHub> in background service
await _hubContext.Clients.Group("tanks").SendAsync(
    "TankLevelUpdated", tankId, currentLevel, tankName, cancellationToken);
```

### Blazor Client Connection

```csharp
// In Blazor component
_hubConnection = new HubConnectionBuilder()
    .WithUrl($"{_apiBaseUrl}/hubs/telemetry")
    .WithAutomaticReconnect()
    .Build();

_hubConnection.On<Guid, double, string>("TankLevelUpdated", (id, level, name) =>
{
    // Update UI state
    InvokeAsync(StateHasChanged);
});

await _hubConnection.StartAsync();
await _hubConnection.InvokeAsync("SubscribeToTanks");
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Hub | Server endpoint for connections | `TelemetryHub : Hub` |
| Groups | Broadcast to subset of clients | `Groups.AddToGroupAsync(connectionId, "tanks")` |
| IHubContext | Broadcast from services | `_hubContext.Clients.Group("tanks").SendAsync(...)` |
| On<T> | Client-side event handler | `_hubConnection.On<Guid, double>("TankLevelUpdated", ...)` |
| WithAutomaticReconnect | Resilient connections | `.WithAutomaticReconnect()` |

## Common Patterns

### Group-Based Subscriptions

**When:** Different clients need different update types.

```csharp
// Client subscribes only to what it needs
await _hubConnection.InvokeAsync("SubscribeToTanks");
await _hubConnection.InvokeAsync("SubscribeToControls");

// Server broadcasts to specific group
await _hubContext.Clients.Group("controls").SendAsync(
    "ControlStateChanged", controlId, newState, controlName);
```

### Connection State Handling

**When:** UI needs to reflect connection status.

```csharp
_hubConnection.Closed += async (error) =>
{
    _isConnected = false;
    await InvokeAsync(StateHasChanged);
};

_hubConnection.Reconnected += async (connectionId) =>
{
    _isConnected = true;
    await _hubConnection.InvokeAsync("SubscribeToTanks");
    await InvokeAsync(StateHasChanged);
};
```

## See Also

- [patterns](references/patterns.md) - Server and client implementation patterns
- [workflows](references/workflows.md) - Setup, testing, and deployment workflows

## Related Skills

- See the **aspnet-core** skill for API and DI configuration
- See the **blazor** skill for frontend integration patterns
- See the **docker** skill for nginx WebSocket proxy configuration