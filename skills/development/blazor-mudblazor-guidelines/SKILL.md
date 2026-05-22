---
name: blazor-mudblazor-guidelines
description: Blazor component best practices and MudBlazor usage for ISLAMU Event. Covers Server + WebAssembly hybrid, MudBlazor components, lifecycle, state management, and render modes.
type: domain
enforcement: suggest
priority: high
---

# Blazor + MudBlazor Guidelines

## 🎯 Purpose

Provides best practices for building UI components with **Blazor** (Server + WebAssembly hybrid) and **MudBlazor** in the ISLAMU Event project.

## ⚡ When This Skill Activates

**Triggered by**:
- Keywords: "blazor", "component", "razor", "mudblazor", "ui", "page", "dialog", "render", "parameter"
- File patterns: `**/*.razor`, `**/*.razor.cs`, `**/*.Client/**/*.cs`
- Content patterns: `@page`, `@inject`, `<Mud`, `Parameter`, `EventCallback`

## 🏗️ ISLAMU Event Blazor Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Blazor Hybrid Architecture                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Explore.Blazor (Server)                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  • Server-side Blazor (BFF pattern)                │    │
│  │  • OIDC Authentication with Keycloak               │    │
│  │  • Cookie-based auth                               │    │
│  │  • HttpContext access                              │    │
│  │  • Components/Pages/*.razor                        │    │
│  │  • @rendermode="InteractiveAuto"                   │    │
│  └────────────────────────────────────────────────────┘    │
│                          ↓                                  │
│  Explore.Blazor.Client (WebAssembly)                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │  • Client-side Blazor (WASM)                       │    │
│  │  • Runs in browser                                 │    │
│  │  • No server access                                │    │
│  │  • Shared components                               │    │
│  │  • Layout/MainLayout.razor                         │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  Render Mode: InteractiveAuto                               │
│  ├─ Starts with Server (fast initial load)                 │
│  ├─ Downloads WASM in background                           │
│  └─ Switches to client-side after download                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📚 Resources

| Resource | Description |
|----------|-------------|
| [component-structure.md](resources/component-structure.md) | Blazor lifecycle, @code blocks, parameters |
| [mudblazor-components.md](resources/mudblazor-components.md) | MudGrid, MudButton, MudDialog, MudTable |
| [state-management.md](resources/state-management.md) | CascadingValue, EventCallback, services |
| [render-modes.md](resources/render-modes.md) | InteractiveAuto, Server, WebAssembly |
| [common-patterns.md](resources/common-patterns.md) | Forms, dialogs, tables, navigation |

## ⚡ Quick Reference

### Basic Component Structure

```razor
@page "/events"
@using MudBlazor
@inject HttpClient Http
@inject NavigationManager NavigationManager

<PageTitle>Events</PageTitle>

<MudContainer MaxWidth="MaxWidth.Large">
    <MudText Typo="Typo.h4" Class="mb-4">Events</MudText>

    @if (_events == null)
    {
        <MudProgressCircular Indeterminate="true" />
    }
    else
    {
        <MudGrid>
            @foreach (var evt in _events)
            {
                <MudItem xs="12" md="6" lg="4">
                    <MudCard>
                        <MudCardContent>
                            <MudText Typo="Typo.h5">@evt.Title</MudText>
                            <MudText Typo="Typo.body2">@evt.Description</MudText>
                        </MudCardContent>
                        <MudCardActions>
                            <MudButton Variant="Variant.Text" Color="Color.Primary"
                                       OnClick="@(() => NavigateToDetails(evt.Id))">
                                View Details
                            </MudButton>
                        </MudCardActions>
                    </MudCard>
                </MudItem>
            }
        </MudGrid>
    }
</MudContainer>

@code {
    private List<EventListDto>? _events;

    protected override async Task OnInitializedAsync()
    {
        _events = await Http.GetFromJsonAsync<List<EventListDto>>("api/v1/events");
    }

    private void NavigateToDetails(Guid id)
    {
        NavigationManager.NavigateTo($"/events/{id}");
    }
}
```

### MudBlazor Grid System

```razor
<MudGrid>
    <MudItem xs="12" sm="6" md="4" lg="3">
        <!-- Full width on mobile, half on tablet, 1/3 on desktop, 1/4 on large -->
    </MudItem>
</MudGrid>
```

**Breakpoints**:
- `xs` - Extra small (mobile)
- `sm` - Small (tablet portrait)
- `md` - Medium (tablet landscape)
- `lg` - Large (desktop)
- `xl` - Extra large

### Component Parameters

```razor
@* Parent Component *@
<EventCard Event="@selectedEvent" OnDelete="HandleDelete" />

@* Child Component: EventCard.razor *@
<MudCard>
    <MudCardContent>
        <MudText>@Event.Title</MudText>
    </MudCardContent>
    <MudCardActions>
        <MudButton OnClick="DeleteClicked" Color="Color.Error">Delete</MudButton>
    </MudCardActions>
</MudCard>

@code {
    [Parameter]
    public EventDto Event { get; set; } = null!;

    [Parameter]
    public EventCallback<Guid> OnDelete { get; set; }

    private async Task DeleteClicked()
    {
        await OnDelete.InvokeAsync(Event.Id);
    }
}
```

### Dependency Injection

```razor
@inject IMediator Mediator
@inject ISnackbar Snackbar
@inject NavigationManager NavigationManager
@inject AuthenticationStateProvider AuthStateProvider
@inject IDialogService DialogService

@code {
    protected override async Task OnInitializedAsync()
    {
        // Use injected services
        var authState = await AuthStateProvider.GetAuthenticationStateAsync();
        var user = authState.User;
    }
}
```

### Render Modes

```razor
@* Interactive Auto (project default) *@
@rendermode InteractiveAuto

@* Interactive Server only *@
@rendermode InteractiveServer

@* Interactive WebAssembly only *@
@rendermode InteractiveWebAssembly

@* Static Server Rendering (no interactivity) *@
@* No @rendermode directive *@
```

## ✅ Do's

- ✅ **DO** use `@rendermode="InteractiveAuto"` (project default)
- ✅ **DO** use MudBlazor components over custom HTML
- ✅ **DO** use `[Parameter]` for component inputs
- ✅ **DO** use `EventCallback<T>` for child → parent communication
- ✅ **DO** use `@inject` for dependency injection
- ✅ **DO** use `OnInitializedAsync` for async initialization
- ✅ **DO** use `MudGrid`/`MudItem` for responsive layouts
- ✅ **DO** use `ISnackbar` for notifications (not JavaScript alert)
- ✅ **DO** use `StateHasChanged()` when updating from non-UI events
- ✅ **DO** implement `IDisposable` for event cleanup

## ❌ Don'ts

- ❌ **DON'T** use raw HTML when MudBlazor component exists
- ❌ **DON'T** use JavaScript interop for what MudBlazor provides
- ❌ **DON'T** forget `@rendermode` on interactive components
- ❌ **DON'T** use `[Parameter]` properties without `{ get; set; }`
- ❌ **DON'T** call `StateHasChanged()` unnecessarily (impacts performance)
- ❌ **DON'T** access HttpContext in WASM components (server only)
- ❌ **DON'T** use `OnAfterRender` for data fetching (use `OnInitializedAsync`)

## 🎨 Common MudBlazor Components

### MudButton
```razor
<MudButton Variant="Variant.Filled" Color="Color.Primary" OnClick="HandleClick">
    Click Me
</MudButton>
```

### MudTextField
```razor
<MudTextField @bind-Value="title" Label="Event Title" Required="true" />
```

### MudSelect
```razor
<MudSelect @bind-Value="selectedStatus" Label="Status">
    @foreach (var status in statuses)
    {
        <MudSelectItem Value="@status">@status.Name</MudSelectItem>
    }
</MudSelect>
```

### MudDialog
```razor
<MudDialog>
    <DialogContent>
        <MudText>Are you sure you want to delete this event?</MudText>
    </DialogContent>
    <DialogActions>
        <MudButton OnClick="Cancel">Cancel</MudButton>
        <MudButton Color="Color.Error" Variant="Variant.Filled" OnClick="Confirm">Delete</MudButton>
    </DialogActions>
</MudDialog>

@code {
    [CascadingParameter]
    MudDialogInstance MudDialog { get; set; } = null!;

    void Cancel() => MudDialog.Cancel();
    void Confirm() => MudDialog.Close(DialogResult.Ok(true));
}
```

### MudTable
```razor
<MudTable Items="@events" Hover="true" Breakpoint="Breakpoint.Sm">
    <HeaderContent>
        <MudTh>Title</MudTh>
        <MudTh>Date</MudTh>
        <MudTh>Actions</MudTh>
    </HeaderContent>
    <RowTemplate>
        <MudTd DataLabel="Title">@context.Title</MudTd>
        <MudTd DataLabel="Date">@context.StartDate.ToShortDateString()</MudTd>
        <MudTd DataLabel="Actions">
            <MudIconButton Icon="@Icons.Material.Filled.Edit" OnClick="@(() => Edit(context.Id))" />
        </MudTd>
    </RowTemplate>
</MudTable>
```

## 🔄 Component Lifecycle

```
Constructor
     ↓
SetParametersAsync
     ↓
OnInitialized / OnInitializedAsync    ← Data fetching here
     ↓
OnParametersSet / OnParametersSetAsync
     ↓
BuildRenderTree (first render)
     ↓
OnAfterRender / OnAfterRenderAsync(firstRender: true)  ← JS interop here
     ↓
[Parameters changed? → OnParametersSet again]
     ↓
[StateHasChanged called? → Re-render]
     ↓
OnAfterRender / OnAfterRenderAsync(firstRender: false)
     ↓
Dispose (if IDisposable)
```

## 🎓 ISLAMU Event Specific Patterns

### Theme Management (Dark/Light)

```razor
@* App.razor pattern *@
@inject IHttpContextAccessor HttpContextAccessor

@code {
    var theme = HttpContextAccessor.HttpContext?.Request.Cookies["theme"];
    var isDark = theme == "dark";
}

<CascadingValue Value="isDark" Name="InitialTheme">
    <Routes @rendermode="InteractiveAuto" />
</CascadingValue>
```

### Authentication State

```razor
<CascadingAuthenticationState>
    <AuthorizeView>
        <Authorized>
            <MudText>Welcome, @context.User.Identity?.Name!</MudText>
        </Authorized>
        <NotAuthorized>
            <MudButton Href="/login">Login</MudButton>
        </NotAuthorized>
    </AuthorizeView>
</CascadingAuthenticationState>
```

### Global Imports (_Imports.razor)

```razor
@using MudBlazor
@using MudBlazor.Services
@using Explore.Blazor
@using Explore.Blazor.Client
@using Microsoft.AspNetCore.Components.Authorization
```

## 📖 Deep Dive

For comprehensive guidance:
- **Component Structure**: [component-structure.md](resources/component-structure.md)
- **MudBlazor Components**: [mudblazor-components.md](resources/mudblazor-components.md)
- **State Management**: [state-management.md](resources/state-management.md)
- **Render Modes**: [render-modes.md](resources/render-modes.md)
- **Common Patterns**: [common-patterns.md](resources/common-patterns.md)

---

**Related Skills**:
- `clean-architecture-rules` - Ensures components are in correct layer
- `cqrs-mediatr-guidelines` - MediatR usage from Blazor
- `backend-dev-guidelines` - API integration

**Enforcement Level**: 💡 SUGGEST (Provides guidance, doesn't block)
