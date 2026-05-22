---
name: blazor
description: |
  Blazor framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Blazor projects, or when the user mentions Blazor.
  Provides WebAssembly/Server patterns, component lifecycle, SignalR, and state management guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: csharp
  extensions: ".razor,.cs"
---

# Blazor Guide

> Applies to: Blazor (.NET 8+), C# 12+, WebAssembly, Server, Blazor United, Interactive Web Apps

## Core Principles

1. **Component-Based**: Build encapsulated `.razor` components that own their state and rendering
2. **Hosting Flexibility**: Choose WebAssembly, Server, or Blazor United (hybrid) per-component
3. **C# Everywhere**: Share models, validation, and logic between client and server
4. **Type Safety**: Leverage nullable reference types and strong parameter typing
5. **Lifecycle Awareness**: Understand component lifecycle to avoid leaks and race conditions

## Hosting Models

| Model | Runs In | Best For |
|-------|---------|----------|
| **WebAssembly** | Browser (WASM) | Offline-capable apps, PWAs, reduced server load |
| **Server** | Server (SignalR) | Low-latency, SEO, thin clients |
| **United (.NET 8)** | Hybrid SSR + interactive | Per-component render mode selection |

## Guardrails

### Component Rules

- Keep components under 200 lines (split with child components)
- Use `[Parameter, EditorRequired]` for required parameters
- Never mutate `[Parameter]` properties directly -- use local state instead
- Use `EventCallback<T>` for parent-child communication (not `Action<T>`)
- Implement `IDisposable` when subscribing to events, timers, or state changes
- Use `@key` directive on list-rendered items for DOM diffing performance
- Wrap component trees in `<ErrorBoundary>` for graceful error handling
- Use `RenderFragment` and `RenderFragment<T>` for templated components

### Lifecycle Rules

- Do NOT call JS interop in `OnInitialized`/`OnInitializedAsync` -- use `OnAfterRender`
- Use `OnParametersSet` for reacting to parameter changes (not property setters)
- Call `StateHasChanged()` only when necessary (avoid triggering excessive re-renders)
- Use `ShouldRender()` override to prevent unnecessary renders on hot paths
- Always use `CancellationToken` with async lifecycle methods to handle disposal

### Data Binding

- Use `@bind-Value` for two-way binding with input components
- Use `@bind:event` to control when binding updates (e.g., `oninput` vs `onchange`)
- Use `EditForm` with `DataAnnotationsValidator` for form validation
- Never use `@bind` and `@onchange` on the same element (they conflict)

### Security

- Use `[Authorize]` attribute on pages requiring authentication
- Use `<AuthorizeView>` for conditional UI based on auth state
- Validate all inputs server-side (client validation is for UX, not security)
- Never trust Blazor WASM for authorization decisions -- enforce on API
- Use antiforgery tokens for form submissions in SSR mode

### Performance

- Use `<Virtualize>` for large lists instead of `@foreach`
- Use `@rendermode` appropriately (static SSR by default, interactive only when needed)
- Use `[StreamRendering]` for pages with async data loading
- Minimize JS interop calls (batch operations when possible)
- Use `IMemoryCache` or `Blazored.LocalStorage` for client-side caching
- Lazy-load assemblies for large WASM apps with `LazyAssemblyLoader`

## Project Structure

```
MyApp/
├── MyApp.Client/                    # Blazor WebAssembly / interactive
│   ├── Pages/                       # Routable components (@page)
│   │   ├── Home.razor
│   │   └── Users/
│   │       ├── UserList.razor
│   │       ├── UserDetail.razor
│   │       └── UserForm.razor
│   ├── Components/                  # Reusable components
│   │   ├── Layout/
│   │   │   ├── MainLayout.razor
│   │   │   └── NavMenu.razor
│   │   ├── Common/
│   │   │   ├── LoadingSpinner.razor
│   │   │   ├── ErrorBoundary.razor
│   │   │   └── Modal.razor
│   │   └── Users/
│   │       └── UserCard.razor
│   ├── Services/                    # Client-side services
│   │   ├── IUserService.cs
│   │   └── UserService.cs
│   ├── State/                       # State management
│   │   └── AppState.cs
│   ├── wwwroot/                     # Static assets
│   ├── _Imports.razor               # Global using directives
│   ├── App.razor                    # Root component
│   └── Program.cs                   # DI and startup
├── MyApp.Server/                    # API / server host
│   ├── Controllers/
│   └── Program.cs
├── MyApp.Shared/                    # Shared models and DTOs
│   ├── Models/
│   └── DTOs/
├── tests/
│   ├── MyApp.Client.Tests/          # bUnit component tests
│   └── MyApp.Server.Tests/          # API integration tests
└── MyApp.sln
```

### Layer Responsibilities

| Layer | Purpose | Depends On |
|-------|---------|------------|
| Client | UI components, pages, client services | Shared |
| Server | API endpoints, server logic, auth | Shared |
| Shared | Models, DTOs, validation attributes | Nothing |
| Tests | bUnit component tests, API tests | Client, Server |

## Component Patterns

### Page Component with Data Loading

```razor
@page "/users"
@attribute [Authorize]
@inject IUserService UserService

<PageTitle>Users</PageTitle>

@if (loading)
{
    <LoadingSpinner />
}
else if (error is not null)
{
    <div class="alert alert-danger">
        <p>@error</p>
        <button class="btn btn-outline-danger" @onclick="LoadUsers">Retry</button>
    </div>
}
else if (users is null || users.Count == 0)
{
    <div class="alert alert-info">No users found.</div>
}
else
{
    @foreach (var user in users)
    {
        <UserCard @key="user.Id" User="user" OnEdit="() => Edit(user.Id)" />
    }
}

@code {
    private List<UserResponse>? users;
    private bool loading = true;
    private string? error;

    protected override async Task OnInitializedAsync()
    {
        await LoadUsers();
    }

    private async Task LoadUsers()
    {
        loading = true;
        error = null;
        try
        {
            users = await UserService.GetUsersAsync();
        }
        catch (Exception ex)
        {
            error = ex.Message;
        }
        finally
        {
            loading = false;
        }
    }

    private void Edit(long id) => Navigation.NavigateTo($"/users/{id}/edit");
}
```

### Reusable Component with Parameters

```razor
<div class="card h-100">
    <div class="card-body">
        <h5 class="card-title">@User.FirstName @User.LastName</h5>
        <small class="text-muted">@User.Email</small>
        <span class="badge @(User.Active ? "bg-success" : "bg-secondary")">
            @(User.Active ? "Active" : "Inactive")
        </span>
    </div>
    <div class="card-footer">
        <button class="btn btn-sm btn-outline-primary" @onclick="OnEdit">Edit</button>
        <button class="btn btn-sm btn-outline-danger" @onclick="OnDelete">Delete</button>
    </div>
</div>

@code {
    [Parameter, EditorRequired]
    public UserResponse User { get; set; } = default!;

    [Parameter]
    public EventCallback OnEdit { get; set; }

    [Parameter]
    public EventCallback OnDelete { get; set; }
}
```

### Templated Component (RenderFragment)

```razor
@code {
    [Parameter] public string Title { get; set; } = "Modal";
    [Parameter] public RenderFragment? BodyContent { get; set; }
    [Parameter] public RenderFragment? FooterContent { get; set; }
    [Parameter] public EventCallback OnClose { get; set; }
}
```

Use `RenderFragment` for content slots, `RenderFragment<T>` for typed template parameters.

## Data Binding & Forms

### EditForm with Validation

```razor
<EditForm Model="model" OnValidSubmit="HandleSubmit">
    <DataAnnotationsValidator />
    <ValidationSummary class="alert alert-danger" />

    <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <InputText id="email" class="form-control" @bind-Value="model.Email" />
        <ValidationMessage For="@(() => model.Email)" class="text-danger" />
    </div>

    <button type="submit" class="btn btn-primary" disabled="@submitting">
        @(submitting ? "Saving..." : "Save")
    </button>
</EditForm>
```

## Routing

### Route Parameters and Constraints

```razor
@page "/users/{Id:long}"
@page "/users/{Id:long}/edit"

@code {
    [Parameter]
    public long Id { get; set; }
}
```

### Navigation

```csharp
@inject NavigationManager Navigation

Navigation.NavigateTo("/users");                    // Client-side navigation
Navigation.NavigateTo("/users/1", forceLoad: true); // Full page reload
```

Use `<NavLink>` with `Match="NavLinkMatch.Prefix"` or `NavLinkMatch.All` for active CSS state.

## State Management

### Observable State Service

```csharp
public class AppState
{
    private UserResponse? _currentUser;

    public UserResponse? CurrentUser
    {
        get => _currentUser;
        set { _currentUser = value; NotifyStateChanged(); }
    }

    public event Action? OnChange;
    private void NotifyStateChanged() => OnChange?.Invoke();
}
```

### Consuming State in Components

```razor
@inject AppState State
@implements IDisposable

<span>@State.CurrentUser?.FirstName</span>

@code {
    protected override void OnInitialized()
    {
        State.OnChange += StateHasChanged;
    }

    public void Dispose()
    {
        State.OnChange -= StateHasChanged;
    }
}
```

### CascadingValue for Shared Data

Use `<CascadingValue Value="@theme">` in layouts. Consume with `[CascadingParameter]` in children. Good for theme, auth state, and locale. Avoid for frequently changing data (triggers full subtree re-render).

## JavaScript Interop

### Calling JS from C#

```csharp
@inject IJSRuntime JS

@code {
    // Only call in OnAfterRenderAsync, not OnInitializedAsync
    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            var width = await JS.InvokeAsync<int>("blazorInterop.getWindowWidth");
        }
    }
}
```

Encapsulate JS interop behind service classes registered in DI. Use `InvokeVoidAsync` for calls without return values, `InvokeAsync<T>` for typed returns.

## .NET 8 Blazor United

### Interactive Render Modes

```razor
@* Static SSR (default -- no interactivity) *@
<StaticComponent />

@* Interactive Server (SignalR) *@
<InteractiveComponent @rendermode="InteractiveServer" />

@* Interactive WebAssembly *@
<InteractiveComponent @rendermode="InteractiveWebAssembly" />

@* Interactive Auto (starts Server, switches to WASM when downloaded) *@
<InteractiveComponent @rendermode="InteractiveAuto" />
```

### Streaming Rendering

Add `@attribute [StreamRendering]` to pages with async data loading. The page renders immediately with placeholder content, then streams updates as `OnInitializedAsync` completes. Ideal for SSR pages loading slow data.

## Testing Overview

### Standards

- Use **bUnit** for component unit tests
- Use **xUnit** as the test runner
- Use **Moq** or **NSubstitute** for service mocking
- Use **FluentAssertions** for readable assertions
- Test rendered markup, parameter behavior, and event callbacks
- Coverage target: >80% for business logic components

### Basic Component Test

```csharp
using Bunit;
using FluentAssertions;

public class UserCardTests : TestContext
{
    [Fact]
    public void UserCard_DisplaysUserInfo()
    {
        var user = new UserResponse(1, "test@example.com", "John", "Doe",
            "User", true, DateTime.UtcNow);

        var cut = RenderComponent<UserCard>(p => p.Add(x => x.User, user));

        cut.Find(".card-title").TextContent.Should().Contain("John Doe");
        cut.Find("small.text-muted").TextContent.Should().Contain("test@example.com");
    }

    [Fact]
    public void UserCard_EditButton_InvokesCallback()
    {
        var user = new UserResponse(1, "t@e.com", "J", "D", "User", true, DateTime.UtcNow);
        var clicked = false;

        var cut = RenderComponent<UserCard>(p => p
            .Add(x => x.User, user)
            .Add(x => x.OnEdit, EventCallback.Factory.Create(this, () => clicked = true)));

        cut.Find("button.btn-outline-primary").Click();
        clicked.Should().BeTrue();
    }
}
```

## Tooling

### Essential Commands

```bash
dotnet new blazorwasm -o MyApp.Client     # New Blazor WASM app
dotnet new blazorserver -o MyApp.Server   # New Blazor Server app
dotnet new blazor -o MyApp                # New Blazor Web App (.NET 8 United)
dotnet watch run --project MyApp.Client   # Dev server with hot reload
dotnet build                              # Build
dotnet publish -c Release                 # Publish
dotnet test                               # Run tests
dotnet add package bunit                  # Add bUnit testing
```

### Key Dependencies

| Package | Purpose |
|---------|---------|
| `Microsoft.AspNetCore.Components.WebAssembly` | WASM hosting |
| `Microsoft.AspNetCore.Components.WebAssembly.Authentication` | WASM auth |
| `Blazored.LocalStorage` | Browser local storage |
| `Blazored.Toast` | Toast notifications |
| `bunit` | Component testing |
| `Fluxor.Blazor.Web` | Redux-style state management |

## Best Practices Summary

### DO

- Use `@key` on list items for efficient DOM diffing
- Use `EventCallback` over `Action` for component events
- Implement `IDisposable` for event handler and timer cleanup
- Use `<Virtualize>` for rendering large collections
- Use typed `HttpClient` for API calls
- Use `CascadingValue` for widely shared state (theme, auth)
- Use `@rendermode` per-component in .NET 8 United

### DO NOT

- Call JS interop in `OnInitialized` (use `OnAfterRender`)
- Mutate `[Parameter]` properties directly
- Use synchronous HTTP calls
- Ignore component lifecycle (leaks events and timers)
- Overuse JS interop (prefer C# solutions)
- Skip loading/error state handling in data-fetching components

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Forms, SignalR, authentication, testing, performance, error handling patterns

## External References

- [Blazor Documentation](https://learn.microsoft.com/aspnet/core/blazor)
- [Blazor University](https://blazor-university.com/)
- [bUnit Testing](https://bunit.dev/)
- [Blazored Libraries](https://github.com/Blazored)
- [Awesome Blazor](https://github.com/AdrienTorris/awesome-blazor)
