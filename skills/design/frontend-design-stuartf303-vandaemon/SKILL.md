---
name: frontend-design
description: |
  Applies UI design with Material Design components and SVG diagrams for the VanDaemon Blazor WebAssembly frontend.
  Use when: Creating new pages, styling components, designing dashboard overlays, implementing touch-friendly interfaces, or working with van diagram SVGs.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Frontend Design Skill

VanDaemon uses MudBlazor for Material Design components with a touch-optimized, offline-first IoT dashboard. The design emphasizes real-time data visualization through SVG van diagrams with draggable overlays, high-contrast readability for use in varying lighting conditions, and immediate visual feedback for control operations.

## Quick Start

### MudBlazor Component Styling

```razor
@* Touch-optimized control card *@
<MudCard Class="pa-4 my-2" Elevation="2">
    <MudCardContent>
        <MudText Typo="Typo.h6">@Control.Name</MudText>
        <MudSwitch T="bool" 
                   @bind-Value="isOn"
                   Color="Color.Primary"
                   Class="mud-switch-large" />
    </MudCardContent>
</MudCard>
```

### SVG Diagram Overlay

```razor
<div class="van-diagram-container" style="position: relative;">
    <img src="diagrams/@settings.VanDiagram" alt="Van Diagram" class="van-image" />
    @foreach (var overlay in overlayPositions)
    {
        <div class="overlay-item" 
             style="left: @(overlay.X)%; top: @(overlay.Y)%; position: absolute;">
            <MudChip Color="@GetStatusColor(overlay)" Size="Size.Small">
                @overlay.Label: @overlay.Value%
            </MudChip>
        </div>
    }
</div>
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Touch targets | Minimum 48px for IoT controls | `Class="mud-switch-large"` |
| Status colors | Semantic feedback for tank/control states | `Color.Success`, `Color.Warning`, `Color.Error` |
| Elevation | Visual hierarchy in dashboard cards | `Elevation="2"` for cards, `Elevation="4"` for dialogs |
| Dense mode | Compact displays for small screens | `Dense="true"` on tables and lists |

## Common Patterns

### Real-Time Status Display

**When:** Displaying tank levels, control states, or sensor readings.

```razor
<MudProgressLinear Color="@GetTankColor(tank.CurrentLevel)" 
                   Value="@tank.CurrentLevel"
                   Class="my-2"
                   Rounded="true"
                   Size="Size.Large">
    <MudText Typo="Typo.body2">@tank.Name: @tank.CurrentLevel.ToString("F0")%</MudText>
</MudProgressLinear>

@code {
    private Color GetTankColor(double level) => level switch
    {
        < 15 => Color.Error,
        < 30 => Color.Warning,
        _ => Color.Success
    };
}
```

### Connection Status Indicator

**When:** Showing SignalR connection state in the app bar.

```razor
<MudBadge Color="@(isConnected ? Color.Success : Color.Error)" 
          Dot="true" 
          Overlap="true"
          Class="mx-2">
    <MudIcon Icon="@Icons.Material.Filled.Wifi" />
</MudBadge>
```

## See Also

- [aesthetics](references/aesthetics.md) - Color system and typography
- [components](references/components.md) - MudBlazor component patterns
- [layouts](references/layouts.md) - Page structure and responsive design
- [motion](references/motion.md) - Transitions and loading states
- [patterns](references/patterns.md) - Design anti-patterns to avoid

## Related Skills

- See the **mudblazor** skill for component API details
- See the **blazor** skill for Blazor WASM patterns and state management
- See the **signalr** skill for real-time update integration