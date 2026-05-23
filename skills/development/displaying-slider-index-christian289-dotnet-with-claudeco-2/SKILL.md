---
name: displaying-slider-index
description: "Displays 0-based collection indices as 1-based numbers in WPF Slider controls. Use when showing user-friendly slice/page numbers while maintaining 0-based internal indexing."
---

# WPF Slider 0-based Index Display Pattern

## Problem Scenario

When displaying collection indices with a slider, **internally using 0-based index** but **displaying as 1-based to users** is a common requirement.

### Symptoms
- 120 images exist but displayed as "0 / 120" ~ "119 / 120"
- Users expect "1 / 120" ~ "120 / 120"
- Dragging slider to the end doesn't reach the last item

### Cause
- If slider's `Maximum` is set to `TotalCount`, it exceeds the valid range
- Displaying 0-based index directly confuses users

---

## Solution

### Add Display Properties to ViewModel

```csharp
public partial class ViewerViewModel : ObservableObject
{
    // Internal index (0-based)
    [NotifyPropertyChangedFor(nameof(SliceDisplayNumber))]
    [ObservableProperty] private int _currentSliceIndex;

    // Total count
    [NotifyPropertyChangedFor(nameof(MaxSliceIndex))]
    [ObservableProperty] private int _totalSliceCount;

    /// <summary>
    /// Slider Maximum value (0-based index maximum)
    /// </summary>
    public int MaxSliceIndex => Math.Max(0, TotalSliceCount - 1);

    /// <summary>
    /// User display number (1-based)
    /// </summary>
    public int SliceDisplayNumber => CurrentSliceIndex + 1;
}
```

### XAML Binding

```xml
<Grid>
    <Grid.ColumnDefinitions>
        <ColumnDefinition Width="Auto" />
        <ColumnDefinition Width="*" />
        <ColumnDefinition Width="Auto" />
    </Grid.ColumnDefinitions>

    <!-- Current number (1-based display) -->
    <TextBlock Grid.Column="0"
               Text="{Binding SliceDisplayNumber}" />

    <!-- Slider (0-based index, Maximum is Count-1) -->
    <Slider Grid.Column="1"
            Minimum="0"
            Maximum="{Binding MaxSliceIndex}"
            Value="{Binding CurrentSliceIndex}" />

    <!-- Total count -->
    <TextBlock Grid.Column="2"
               Text="{Binding TotalSliceCount}" />
</Grid>
```

---

## Key Points

| Property | Value Range | Purpose |
|----------|-------------|---------|
| `CurrentSliceIndex` | 0 ~ (Count-1) | Internal logic, Slider Value |
| `MaxSliceIndex` | Count-1 | Slider Maximum |
| `SliceDisplayNumber` | 1 ~ Count | User display |
| `TotalSliceCount` | Count | Total count display |

---

## Using NotifyPropertyChangedFor

The `[NotifyPropertyChangedFor]` attribute automatically raises `PropertyChanged` for computed properties when the source property changes.

```csharp
// When CurrentSliceIndex changes, SliceDisplayNumber also raises PropertyChanged
[NotifyPropertyChangedFor(nameof(SliceDisplayNumber))]
[ObservableProperty] private int _currentSliceIndex;

// When TotalSliceCount changes, MaxSliceIndex also raises PropertyChanged
[NotifyPropertyChangedFor(nameof(MaxSliceIndex))]
[ObservableProperty] private int _totalSliceCount;
```

---

## Application Examples

- Image viewer slice navigation (CT/MRI)
- Pagination (document viewer)
- Media player track list
- Gallery image index
