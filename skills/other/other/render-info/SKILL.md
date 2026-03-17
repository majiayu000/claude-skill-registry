---
name: render-info
description: Using the RendererInfo class in Blazor to detect rendering context and interactivity.
---

# Using RendererInfo in Blazor

The `RendererInfo` class in Blazor provides runtime information about the renderer that is executing the component. It is particularly useful for detecting whether a component is running interactively or statically, and for identifying the specific rendering platform (e.g., Server, WebAssembly, WebView).

## Key Properties

### `IsInteractive`
- **Type:** `bool`
- **Description:** Indicates whether the component is currently running in an interactive render mode.
- **Usage:** Use this to conditionally render UI elements that require interactivity, such as disabling buttons or showing loading indicators during static server-side rendering (SSR) or prerendering.

```csharp
@if (!RendererInfo.IsInteractive)
{
    <p>Connecting...</p>
}
else
{
    <button @onclick="HandleClick">Click Me</button>
}
```

### `Name`
- **Type:** `string`
- **Description:** Returns the name of the renderer.
- **Common Values:**
  - `"Static"`: Running in static server-side rendering (SSR).
  - `"Server"`: Running in Interactive Server mode (SignalR).
  - `"WebAssembly"`: Running in Interactive WebAssembly mode.
  - `"WebView"`: Running in a Blazor Hybrid application (MAUI, WPF, WinForms).

```csharp
<p>Current Render Mode: @RendererInfo.Name</p>
```

## Common Scenarios

### 1. Disabling Inputs During Prerendering
When a component is prerendered on the server, event handlers (like `@onclick`) are not active. You can use `RendererInfo.IsInteractive` to disable inputs until the interactive runtime takes over.

```razor
<button @onclick="Submit" disabled="@(!RendererInfo.IsInteractive)">
    Submit
</button>
```

### 2. Rendering Different Content for Static vs. Interactive
You might want to show a simple HTML form for static SSR and a rich, interactive component for interactive modes.

```razor
@if (RendererInfo.Name == "Static")
{
    <form action="/search" method="get">
        <input name="q" />
        <button type="submit">Search</button>
    </form>
}
else
{
    <SearchComponent />
}
```

## Related Concepts
- **`AssignedRenderMode`**: A property on `ComponentBase` that tells you which render mode was assigned to the component (e.g., `InteractiveServer`, `InteractiveWebAssembly`, `InteractiveAuto`). Note that `AssignedRenderMode` might be `null` during static rendering.

## Important Notes
- `RendererInfo` is available in .NET 8.0 and later.
- It is a static class, so you can access it directly in your Razor markup or C# code without injection.
