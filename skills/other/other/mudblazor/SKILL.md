---
name: mudblazor
description: |
  Creates Material Design UI components and touch-optimized interfaces for Blazor WebAssembly.
  Use when: building dashboard pages, forms, data tables, dialogs, or any UI component in VanDaemon's frontend.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# MudBlazor Skill

MudBlazor provides Material Design components for Blazor. VanDaemon uses MudBlazor 6.x for touch-optimized interfaces designed for mobile devices in camper van environments. Key patterns include real-time data binding with SignalR, responsive layouts, and dark/light theme support.

## Quick Start

### Basic Page Layout

```razor
@page "/dashboard"
@inject HttpClient Http

<MudContainer MaxWidth="MaxWidth.Large" Class="mt-4">
    <MudPaper Class="pa-4">
        <MudText Typo="Typo.h4">Tank Levels</MudText>
        <MudGrid>
            @foreach (var tank in tanks)
            {
                <MudItem xs="12" sm="6" md="4">
                    <MudCard>
                        <MudCardContent>
                            <MudText>@tank.Name</MudText>
                            <MudProgressLinear Value="@tank.CurrentLevel" Color="Color.Primary" />
                        </MudCardContent>
                    </MudCard>
                </MudItem>
            }
        </MudGrid>
    </MudPaper>
</MudContainer>
```

### Touch-Optimized Control

```razor
<MudSwitch @bind-Value="@control.IsOn"
           Color="Color.Success"
           Size="Size.Large"
           Label="@control.Name"
           @onclick="() => ToggleControl(control.Id)" />

<MudSlider @bind-Value="@dimmerValue"
           Min="0" Max="255"
           Step="1"
           Color="Color.Primary"
           Size="Size.Large"
           ValueLabel="true"
           @onchange="() => UpdateDimmer()" />
```

## Key Concepts

| Component | Use Case | Size Prop |
|-----------|----------|-----------|
| `MudSwitch` | Toggle controls (lights, pump) | `Size.Large` for touch |
| `MudSlider` | Dimmer controls (0-255) | `Size.Large` for touch |
| `MudProgressLinear` | Tank level display | N/A |
| `MudCard` | Content containers | N/A |
| `MudGrid/MudItem` | Responsive layout | `xs`, `sm`, `md` breakpoints |
| `MudDialog` | Confirmations, settings | N/A |

## Common Patterns

### Real-Time Data Binding

**When:** Displaying SignalR-updated values

```razor
@code {
    private double tankLevel;

    protected override async Task OnInitializedAsync()
    {
        hubConnection.On<Guid, double, string>("TankLevelUpdated", (id, level, name) =>
        {
            tankLevel = level;
            InvokeAsync(StateHasChanged);  // Required for SignalR callbacks
        });
    }
}
```

### Responsive Grid

**When:** Building dashboard layouts

```razor
<MudGrid Spacing="3">
    <MudItem xs="12" sm="6" md="4" lg="3">
        <!-- Full width on mobile, half on tablet, quarter on desktop -->
    </MudItem>
</MudGrid>
```

## See Also

- [patterns](references/patterns.md) - Component patterns and anti-patterns
- [workflows](references/workflows.md) - Form handling, theming, dialogs

## Related Skills

- See the **blazor** skill for component lifecycle and SignalR integration
- See the **signalr** skill for real-time data updates
- See the **frontend-design** skill for responsive design patterns