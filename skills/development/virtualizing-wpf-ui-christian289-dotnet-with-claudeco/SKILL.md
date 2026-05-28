---
name: virtualizing-wpf-ui
description: Implements WPF UI virtualization for large data sets using VirtualizingStackPanel. Use when displaying 1000+ items in ItemsControl, ListView, or DataGrid to prevent memory and performance issues.
---

# WPF UI Virtualization

## Quick Setup
```xml
<ListBox ItemsSource="{Binding LargeCollection}"
         VirtualizingPanel.IsVirtualizing="True"
         VirtualizingPanel.VirtualizationMode="Recycling"
         VirtualizingPanel.ScrollUnit="Pixel"
         VirtualizingPanel.CacheLength="2,2"
         VirtualizingPanel.CacheLengthUnit="Page"/>
```

## Key Properties

| Property | Recommended | Purpose |
|----------|-------------|---------|
| `IsVirtualizing` | True | Enable virtualization |
| `VirtualizationMode` | Recycling | Reuse containers |
| `ScrollUnit` | Pixel | Smooth scrolling |
| `CacheLength` | "1,1" to "2,2" | Buffer pages |

## Virtualization Breakers

**These disable virtualization:**
```xml
<!-- ❌ ScrollViewer wrapper -->
<ScrollViewer>
    <ListBox/>
</ScrollViewer>

<!-- ❌ CanContentScroll disabled -->
<ListBox ScrollViewer.CanContentScroll="False"/>

<!-- ❌ Grouping without flag -->
<ListBox>
    <ListBox.GroupStyle>...</ListBox.GroupStyle>
</ListBox>
```

**Fixes:**
```xml
<!-- ✅ No wrapper needed - ListBox has built-in ScrollViewer -->
<ListBox ItemsSource="{Binding Items}"/>

<!-- ✅ Grouping with virtualization -->
<ListBox VirtualizingPanel.IsVirtualizingWhenGrouping="True">
    <ListBox.GroupStyle>...</ListBox.GroupStyle>
</ListBox>
```

## Recycling Mode Considerations
```csharp
// When using Recycling mode, clean up in PrepareContainerForItemOverride
protected override void PrepareContainerForItemOverride(
    DependencyObject element, object item)
{
    base.PrepareContainerForItemOverride(element, item);

    var container = (ListBoxItem)element;
    // Reset any manually attached handlers or state
}
```

## Performance Tips

### Deferred Scrolling
```xml
<!-- Faster scrollbar dragging -->
<ListBox ScrollViewer.IsDeferredScrollingEnabled="True"/>
```

### Diagnostic Check
```csharp
public static bool IsVirtualizing(ItemsControl control)
{
    var panel = FindVisualChild<VirtualizingStackPanel>(control);
    return panel != null && VirtualizingPanel.GetIsVirtualizing(control);
}

public static int GetRealizedCount(ItemsControl control)
{
    var generator = control.ItemContainerGenerator;
    return Enumerable.Range(0, control.Items.Count)
        .Count(i => generator.ContainerFromIndex(i) != null);
}
```

## DataGrid Virtualization
```xml
<DataGrid ItemsSource="{Binding Items}"
          EnableRowVirtualization="True"
          EnableColumnVirtualization="True"
          VirtualizingPanel.IsVirtualizing="True"
          VirtualizingPanel.VirtualizationMode="Recycling"/>
```