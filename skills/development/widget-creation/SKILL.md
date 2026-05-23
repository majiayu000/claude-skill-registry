---
name: widget-creation
description: Create new desktop widgets for the 3SC WPF widget host. Use when adding a new widget type or instance, including its domain model, persistence, viewmodel, view, and registration in the shell/launcher flow.
---

# Widget Creation

## Overview

Define, implement, and register widgets consistently across domain, data, UI, and tests.

## Constraints

- .NET 8 WPF
- MVVM with CommunityToolkit.Mvvm
- Use shared styles/resources; avoid widget-specific hardcoded colors
- Persist widget instances in SQLite via repositories

## Definition of done (DoD)

- Widget follows `_WidgetTemplate.cs` pattern for DB operations
- ViewModel has no WPF dependencies (testable in isolation)
- Widget registered in WidgetPickerViewModel and IWidgetWindowService
- Position/size persistence via repository works correctly
- Remove widget flow deletes from DB and notifies shell
- At least one ViewModel test exists for the widget
- Widget has resize handles implementation with "Resize Handles" menu item
- Widget is responsive (font sizes scale with widget dimensions)
- Widget uses theme brushes (Brushes.WidgetSurface, Brushes.WidgetOutline, etc.)
- Context menu includes: Settings (if applicable), Lock Widget, Resize Handles, Remove Widget
- Widget supports locked state (prevents dragging and resizing)
- Widget name is NOT displayed on the widget UI itself (Window Title can have name for system purposes)
- Widget position constrained to screen bounds (uses ScreenBoundsHelper in constructor)

## Workflow

1. Add domain artifacts:
   - Ensure a `Widget` entry exists for the type.
   - Add or update `WidgetInstance` usage for placements.
2. Add application logic:
   - Add a viewmodel for the widget.
   - Add any commands or validation.
3. Add UI artifacts:
   - Create a view under `3SC/Views` or `3SC/Widgets/<WidgetName>/`.
   - Bind to viewmodel properties; no code-behind logic except resize handlers.
   - **Do NOT display widget name on the widget** - show only content/functionality
   - **Must include**: Resize handles (Top, Bottom, Left, Right thumbs with Collapsed visibility)
   - **Must include**: ResizeOutline rectangle for visual feedback
   - **Must include**: Grid with Margin="6" wrapper for consistent shadow spacing
   - **Must set**: ResizeMode="NoResize" on Window (manual resize only)
4. Add resize and responsive logic:
   - Add resize handle drag delta handlers (ResizeLeft/Right/Top/Bottom_DragDelta)
   - Add UpdateFontSizes() method to scale text based on widget dimensions
   - Define min/max size constraints (MinWidgetWidth, MinWidgetHeight)
   - Add ResizeToggle_Click and LockWidget_Click handlers
   - Add IsResizeThumbSource() helper to prevent drag-move on thumbs
5. Use consistent theme:
   - Background: `{DynamicResource Brushes.WidgetSurface}`
   - Border: `{DynamicResource Brushes.WidgetBorder}`
   - Outline: `{DynamicResource Brushes.WidgetOutline}`
   - Text: `{DynamicResource Brushes.TextPrimary/Secondary}`
   - Accent: `{DynamicResource Brushes.Accent}`
   - Corner radius: 12-16 (match existing widgets)
6. Register the widget:
   - Add to the widget picker viewmodel list.
   - Create or update any factory/service to instantiate widgets.
7. Persist widget state:
   - Use repositories and unit of work for saves.
   - Save position, size, and locked state.
8. Add tests:
   - Domain invariants
   - Viewmodel tests
   - Repository integration tests when persistence is touched

## Naming and layout

- Widget key: `clock`, `weather`, `notes`
- ViewModel: `<WidgetName>WidgetViewModel`
- View: `<WidgetName>WidgetView` or `<WidgetName>Widget`
- Placement: `WidgetInstance` with `WidgetPosition` and `WidgetSize`

## Required XAML structure

```xaml
<Window ResizeMode="NoResize" WindowStyle="None" AllowsTransparency="True" Background="Transparent">
  <Grid Margin="6">
    <Border x:Name="RootBorder" 
            Background="{DynamicResource Brushes.WidgetSurface}"
            CornerRadius="12-16"
            SnapsToDevicePixels="True">
      <Border.ContextMenu>
        <ContextMenu>
          <MenuItem Header="Lock Widget" IsCheckable="True" Click="LockWidget_Click"/>
          <MenuItem Header="Resize Handles" IsCheckable="True" Click="ResizeToggle_Click"/>
          <Separator/>
          <MenuItem Header="Remove Widget" Click="RemoveWidget_Click"/>
        </ContextMenu>
      </Border.ContextMenu>
      
      <Grid>
        <!-- Resize outline and handles -->
        <Rectangle x:Name="ResizeOutline" Visibility="Collapsed"/>
        <Thumb x:Name="ResizeTop/Bottom/Left/Right" Visibility="Collapsed" DragDelta="..."/>
        
        <!-- Widget content -->
      </Grid>
    </Border>
  </Grid>
</Window>
```

## Required code-behind fields

```csharp
private bool _isLocked = false;
private bool _resizeHandlesVisible = false;
private const double MinWidgetWidth = 200;
private const double MinWidgetHeight = 100;
```

## Required methods

- `LockWidget_Click`: Toggle _isLocked and persist state
- `ResizeToggle_Click`: Toggle resize handles visibility
- `SetResizeHandlesVisibility(bool)`: Show/hide thumbs and outline
- `ResizeLeft/Right/Top/Bottom_DragDelta`: Handle resize with min constraints
- `UpdateFontSizes()`: Scale text based on widget size (responsive)
- `IsResizeThumbSource(DependencyObject?)`: Prevent drag on thumb clicks
- `SavePositionAndState()`: Persist to repository

## References

- `references/widget-checklist.md` for creation checklist.
- `references/registration.md` for picker/registration guidance.
