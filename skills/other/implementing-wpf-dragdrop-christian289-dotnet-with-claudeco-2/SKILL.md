---
name: implementing-wpf-dragdrop
description: Implements WPF drag and drop functionality using DragDrop.DoDragDrop, DataObject, and drag/drop events. Use when building file drop zones, list reordering, or inter-application data transfer.
---

# WPF Drag and Drop Patterns

Implementing drag and drop functionality for data transfer within and between applications.

**Advanced Patterns:** See [ADVANCED.md](ADVANCED.md) for visual feedback, list reordering, and custom data formats.

## 1. Drag and Drop Overview

```
Drag Source                           Drop Target
    │                                      │
    ├─ MouseDown                           │
    ├─ MouseMove (drag threshold)          │
    ├─ DragDrop.DoDragDrop()───────────────┤
    │                                      ├─ DragEnter
    │                                      ├─ DragOver
    │                                      ├─ DragLeave
    │                                      └─ Drop
    └─ GiveFeedback (cursor change)
```

---

## 2. Basic Drag Source

### 2.1 Simple Text Drag

```csharp
namespace MyApp.Views;

using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

public partial class DragSourceView : UserControl
{
    private Point _startPoint;

    private void TextBlock_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        _startPoint = e.GetPosition(null);
    }

    private void TextBlock_MouseMove(object sender, MouseEventArgs e)
    {
        if (e.LeftButton != MouseButtonState.Pressed)
            return;

        var currentPoint = e.GetPosition(null);
        var diff = _startPoint - currentPoint;

        // Check if drag threshold is exceeded
        if (Math.Abs(diff.X) > SystemParameters.MinimumHorizontalDragDistance ||
            Math.Abs(diff.Y) > SystemParameters.MinimumVerticalDragDistance)
        {
            if (sender is TextBlock textBlock)
            {
                // Create data object and start drag
                var data = new DataObject(DataFormats.Text, textBlock.Text);
                DragDrop.DoDragDrop(textBlock, data, DragDropEffects.Copy);
            }
        }
    }
}
```

### 2.2 Multiple Data Formats

```csharp
private void StartDragWithMultipleFormats(FrameworkElement source, object item)
{
    var data = new DataObject();

    // Add multiple formats for compatibility
    if (item is MyDataItem dataItem)
    {
        data.SetData(typeof(MyDataItem), dataItem);
        data.SetData(DataFormats.Text, dataItem.ToString());
        data.SetData(DataFormats.Serializable, dataItem);
    }

    DragDrop.DoDragDrop(source, data, DragDropEffects.Copy | DragDropEffects.Move);
}
```

---

## 3. Drop Target

### 3.1 Basic Drop Target

```xml
<Border x:Name="DropZone"
        AllowDrop="True"
        DragEnter="DropZone_DragEnter"
        DragOver="DropZone_DragOver"
        DragLeave="DropZone_DragLeave"
        Drop="DropZone_Drop"
        Background="LightGray"
        BorderBrush="Gray"
        BorderThickness="2">
    <TextBlock Text="Drop files here"
               HorizontalAlignment="Center"
               VerticalAlignment="Center"/>
</Border>
```

```csharp
private void DropZone_DragEnter(object sender, DragEventArgs e)
{
    // Check if data format is acceptable
    if (!e.Data.GetDataPresent(DataFormats.FileDrop) &&
        !e.Data.GetDataPresent(DataFormats.Text))
    {
        e.Effects = DragDropEffects.None;
    }
    else
    {
        e.Effects = DragDropEffects.Copy;
        HighlightDropZone(true);
    }
    e.Handled = true;
}

private void DropZone_DragOver(object sender, DragEventArgs e)
{
    // Continuously update effects based on position or modifier keys
    if (e.Data.GetDataPresent(DataFormats.FileDrop))
    {
        e.Effects = (e.KeyStates & DragDropKeyStates.ControlKey) != 0
            ? DragDropEffects.Copy
            : DragDropEffects.Move;
    }
    e.Handled = true;
}

private void DropZone_DragLeave(object sender, DragEventArgs e)
{
    HighlightDropZone(false);
}

private void DropZone_Drop(object sender, DragEventArgs e)
{
    HighlightDropZone(false);

    if (e.Data.GetDataPresent(DataFormats.FileDrop))
    {
        var files = (string[])e.Data.GetData(DataFormats.FileDrop);
        ProcessDroppedFiles(files);
    }
    else if (e.Data.GetDataPresent(DataFormats.Text))
    {
        var text = (string)e.Data.GetData(DataFormats.Text);
        ProcessDroppedText(text);
    }

    e.Handled = true;
}
```

---

## 4. File Drop Zone Control

```csharp
namespace MyApp.Controls;

using System.Collections.Generic;
using System.IO;
using System.Windows;
using System.Windows.Controls;

public sealed partial class FileDropZone : UserControl
{
    public static readonly DependencyProperty AcceptedExtensionsProperty =
        DependencyProperty.Register(
            nameof(AcceptedExtensions),
            typeof(string[]),
            typeof(FileDropZone),
            new PropertyMetadata(new[] { "*" }));

    public string[] AcceptedExtensions
    {
        get => (string[])GetValue(AcceptedExtensionsProperty);
        set => SetValue(AcceptedExtensionsProperty, value);
    }

    public event EventHandler<IReadOnlyList<string>>? FilesDropped;

    public FileDropZone()
    {
        InitializeComponent();
        AllowDrop = true;
    }

    protected override void OnDragEnter(DragEventArgs e)
    {
        ValidateAndSetEffects(e);
    }

    protected override void OnDragOver(DragEventArgs e)
    {
        ValidateAndSetEffects(e);
    }

    protected override void OnDrop(DragEventArgs e)
    {
        if (!e.Data.GetDataPresent(DataFormats.FileDrop))
            return;

        var files = (string[])e.Data.GetData(DataFormats.FileDrop);
        var validFiles = FilterValidFiles(files);

        if (validFiles.Count > 0)
        {
            FilesDropped?.Invoke(this, validFiles);
        }
    }

    private void ValidateAndSetEffects(DragEventArgs e)
    {
        e.Effects = DragDropEffects.None;

        if (!e.Data.GetDataPresent(DataFormats.FileDrop))
        {
            e.Handled = true;
            return;
        }

        var files = (string[])e.Data.GetData(DataFormats.FileDrop);

        if (FilterValidFiles(files).Count > 0)
        {
            e.Effects = DragDropEffects.Copy;
        }

        e.Handled = true;
    }

    private List<string> FilterValidFiles(string[] files)
    {
        var result = new List<string>();

        foreach (var file in files)
        {
            if (!File.Exists(file))
                continue;

            var extension = Path.GetExtension(file).ToLowerInvariant();

            if (AcceptedExtensions.Contains("*") ||
                AcceptedExtensions.Contains(extension))
            {
                result.Add(file);
            }
        }

        return result;
    }
}
```

### Usage

```xml
<local:FileDropZone AcceptedExtensions=".jpg,.png,.gif"
                    FilesDropped="OnImagesDropped"
                    Width="300" Height="200">
    <TextBlock Text="Drop images here (.jpg, .png, .gif)"
               HorizontalAlignment="Center"
               VerticalAlignment="Center"/>
</local:FileDropZone>
```

---

## 5. DragDropEffects

| Effect | Description | Cursor |
|--------|-------------|--------|
| **None** | Drop not allowed | No-drop cursor |
| **Copy** | Copy data | Copy cursor (+) |
| **Move** | Move data | Move cursor |
| **Link** | Create link | Link cursor |
| **Scroll** | Scrolling occurring | Scroll cursor |
| **All** | Copy, Move, Scroll combined | - |

```csharp
private void DropZone_DragOver(object sender, DragEventArgs e)
{
    // Set effect based on modifier keys
    if ((e.KeyStates & DragDropKeyStates.ControlKey) != 0)
    {
        e.Effects = DragDropEffects.Copy;
    }
    else if ((e.KeyStates & DragDropKeyStates.ShiftKey) != 0)
    {
        e.Effects = DragDropEffects.Move;
    }
    else if ((e.KeyStates & DragDropKeyStates.AltKey) != 0)
    {
        e.Effects = DragDropEffects.Link;
    }
    else
    {
        e.Effects = DragDropEffects.Move; // Default
    }
}
```

---

## 6. References

- [Drag and Drop Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/drag-and-drop-overview)
- [DataObject Class - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.dataobject)
- [DragDrop Class - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.dragdrop)
