---
name: blazor
description: |
  Develops Blazor WebAssembly single-page applications with component-based UI.
  Use when: Creating/modifying .razor components, managing component state, handling SignalR subscriptions, or working with MudBlazor UI components.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Blazor Skill

Blazor WebAssembly frontend for VanDaemon running on .NET 10. Components live in `src/Frontend/VanDaemon.Web/Pages/`. Uses MudBlazor for Material Design UI and SignalR for real-time updates from the API.

## Quick Start

### Basic Page Component

```razor
@page "/tanks"
@inject HttpClient Http
@inject ILogger<Tanks> Logger

<PageTitle>Tanks</PageTitle>

<MudText Typo="Typo.h4">Tank Levels</MudText>

@if (_tanks is null)
{
    <MudProgressCircular Indeterminate="true" />
}
else
{
    @foreach (var tank in _tanks)
    {
        <MudCard Class="mb-4">
            <MudCardContent>
                <MudText>@tank.Name: @tank.CurrentLevel%</MudText>
            </MudCardContent>
        </MudCard>
    }
}

@code {
    private List<Tank>? _tanks;

    protected override async Task OnInitializedAsync()
    {
        _tanks = await Http.GetFromJsonAsync<List<Tank>>("api/tanks");
    }
}
```

### SignalR Real-Time Subscription

```razor
@inject HubConnection HubConnection
@implements IAsyncDisposable

@code {
    protected override async Task OnInitializedAsync()
    {
        HubConnection.On<Guid, double, string>("TankLevelUpdated", 
            (id, level, name) =>
            {
                var tank = _tanks?.FirstOrDefault(t => t.Id == id);
                if (tank is not null)
                {
                    tank.CurrentLevel = level;
                    InvokeAsync(StateHasChanged);
                }
            });

        await HubConnection.InvokeAsync("SubscribeToTanks");
    }

    public async ValueTask DisposeAsync()
    {
        HubConnection.Remove("TankLevelUpdated");
    }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Page routing | `@page "/path"` directive | `@page "/settings"` |
| DI injection | `@inject` directive | `@inject HttpClient Http` |
| State updates | Call `StateHasChanged()` | After SignalR callback |
| Event binding | `@onclick`, `@onchange` | `@onclick="HandleClick"` |
| Two-way binding | `@bind` directive | `@bind-Value="_searchText"` |

## Common Patterns

### Conditional Rendering with Loading State

**When:** Fetching data on component initialization

```razor
@if (_isLoading)
{
    <MudProgressCircular Indeterminate="true" />
}
else if (_error is not null)
{
    <MudAlert Severity="Severity.Error">@_error</MudAlert>
}
else
{
    <!-- Render data -->
}
```

### Component Parameters

**When:** Creating reusable components

```razor
<!-- TankCard.razor -->
@code {
    [Parameter, EditorRequired]
    public Tank Tank { get; set; } = default!;

    [Parameter]
    public EventCallback<Tank> OnTankSelected { get; set; }
}
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **mudblazor** skill for UI component patterns
- See the **signalr** skill for real-time communication
- See the **csharp** skill for language patterns in `@code` blocks
- See the **aspnet-core** skill for API integration