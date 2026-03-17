---
name: using-wpf-clipboard
description: Uses WPF Clipboard for copy/paste operations with text, images, and custom data formats. Use when implementing copy/paste functionality or inter-application data transfer.
---

# WPF Clipboard Patterns

Implementing copy/paste functionality using the Windows clipboard.

**Advanced Patterns:** See [ADVANCED.md](ADVANCED.md) for clipboard monitoring and error handling.

## 1. Clipboard Overview

```
Clipboard Operations
├── Text Operations
│   ├── SetText / GetText
│   └── Unicode, RTF, HTML support
├── Image Operations
│   ├── SetImage / GetImage
│   └── BitmapSource support
├── File Operations
│   ├── SetFileDropList / GetFileDropList
│   └── File path collection
└── Custom Data
    ├── SetData / GetData
    └── DataObject with multiple formats
```

---

## 2. Text Operations

### 2.1 Basic Text Copy/Paste

```csharp
using System.Windows;

// Copy text to clipboard
Clipboard.SetText("Hello, World!");

// Paste text from clipboard
if (Clipboard.ContainsText())
{
    var text = Clipboard.GetText();
    // Use text
}
```

### 2.2 Text Formats

```csharp
// Set text with specific format
Clipboard.SetText("Hello", TextDataFormat.UnicodeText);
Clipboard.SetText("<b>Hello</b>", TextDataFormat.Html);
Clipboard.SetText(@"{\rtf1 Hello}", TextDataFormat.Rtf);

// Get text with specific format
if (Clipboard.ContainsText(TextDataFormat.Html))
{
    var html = Clipboard.GetText(TextDataFormat.Html);
}
```

**TextDataFormat Options:**
| Value | Description |
|-------|-------------|
| **Text** | ANSI text |
| **UnicodeText** | Unicode text (default) |
| **Rtf** | Rich Text Format |
| **Html** | HTML format |
| **CommaSeparatedValue** | CSV format |

---

## 3. Image Operations

### 3.1 Copy/Paste Images

```csharp
using System.Windows;
using System.Windows.Media.Imaging;

// Copy image to clipboard
var bitmap = new BitmapImage(new Uri("pack://application:,,,/Images/logo.png"));
Clipboard.SetImage(bitmap);

// Paste image from clipboard
if (Clipboard.ContainsImage())
{
    var image = Clipboard.GetImage();
    MyImage.Source = image;
}
```

### 3.2 Copy UI Element as Image

```csharp
using System.Windows.Media;
using System.Windows.Media.Imaging;

public static void CopyElementAsImage(FrameworkElement element)
{
    var width = (int)element.ActualWidth;
    var height = (int)element.ActualHeight;

    var renderBitmap = new RenderTargetBitmap(
        width, height, 96, 96, PixelFormats.Pbgra32);

    renderBitmap.Render(element);
    Clipboard.SetImage(renderBitmap);
}
```

---

## 4. File Operations

### 4.1 Copy/Paste File Paths

```csharp
using System.Collections.Specialized;
using System.Windows;

// Copy files to clipboard
var files = new StringCollection
{
    @"C:\Documents\file1.txt",
    @"C:\Documents\file2.txt"
};
Clipboard.SetFileDropList(files);

// Paste files from clipboard
if (Clipboard.ContainsFileDropList())
{
    var fileList = Clipboard.GetFileDropList();

    foreach (var file in fileList)
    {
        ProcessFile(file);
    }
}
```

---

## 5. DataObject (Multiple Formats)

### 5.1 Setting Multiple Formats

```csharp
public static void CopyWithMultipleFormats(MyDataItem item)
{
    var dataObject = new DataObject();

    // Add multiple formats for compatibility
    dataObject.SetData(DataFormats.Text, item.ToString());
    dataObject.SetData(DataFormats.Html, item.ToHtml());
    dataObject.SetData(typeof(MyDataItem), item);

    Clipboard.SetDataObject(dataObject);
}
```

### 5.2 Getting Data by Format

```csharp
public static void PasteData()
{
    var dataObject = Clipboard.GetDataObject();

    if (dataObject == null)
        return;

    // Check available formats
    var formats = dataObject.GetFormats();

    // Try custom format first
    if (dataObject.GetDataPresent(typeof(MyDataItem)))
    {
        var item = dataObject.GetData(typeof(MyDataItem)) as MyDataItem;
        ProcessItem(item);
        return;
    }

    // Fall back to text
    if (dataObject.GetDataPresent(DataFormats.Text))
    {
        var text = dataObject.GetData(DataFormats.Text) as string;
        ProcessText(text);
    }
}
```

### 5.3 Keeping Data After App Close

```csharp
// Data persists after application closes
Clipboard.SetDataObject(dataObject, copy: true);

// Data is removed when application closes (default)
Clipboard.SetDataObject(dataObject, copy: false);
```

---

## 6. Custom Data Formats

### 6.1 Registering Custom Format

```csharp
public static class CustomClipboardFormats
{
    public static readonly string MyAppItemFormat =
        DataFormats.GetDataFormat("MyApp.CustomItem").Name;
}
```

### 6.2 Using Custom Format

```csharp
// Copy with custom format
var dataObject = new DataObject();
dataObject.SetData(CustomClipboardFormats.MyAppItemFormat, myItem);
Clipboard.SetDataObject(dataObject);

// Paste with custom format
var data = Clipboard.GetDataObject();

if (data?.GetDataPresent(CustomClipboardFormats.MyAppItemFormat) == true)
{
    var item = data.GetData(CustomClipboardFormats.MyAppItemFormat) as MyItem;
}
```

---

## 7. Clipboard with Commands

### 7.1 Built-in Commands

```xml
<TextBox x:Name="MyTextBox"/>

<!-- Built-in clipboard commands work automatically -->
<Button Command="ApplicationCommands.Cut"
        CommandTarget="{Binding ElementName=MyTextBox}"
        Content="Cut"/>
<Button Command="ApplicationCommands.Copy"
        CommandTarget="{Binding ElementName=MyTextBox}"
        Content="Copy"/>
<Button Command="ApplicationCommands.Paste"
        CommandTarget="{Binding ElementName=MyTextBox}"
        Content="Paste"/>
```

### 7.2 Custom Clipboard Commands

```csharp
namespace MyApp.ViewModels;

using System.Windows;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public partial class MainViewModel : ObservableObject
{
    [ObservableProperty] private MyItem? _selectedItem;

    [RelayCommand(CanExecute = nameof(CanCopy))]
    private void Copy()
    {
        if (SelectedItem == null)
            return;

        var dataObject = new DataObject();
        dataObject.SetData(typeof(MyItem), SelectedItem);
        dataObject.SetData(DataFormats.Text, SelectedItem.ToString());

        Clipboard.SetDataObject(dataObject, copy: true);
    }

    private bool CanCopy() => SelectedItem != null;

    [RelayCommand(CanExecute = nameof(CanPaste))]
    private void Paste()
    {
        var data = Clipboard.GetDataObject();

        if (data?.GetDataPresent(typeof(MyItem)) == true)
        {
            var item = data.GetData(typeof(MyItem)) as MyItem;

            if (item != null)
            {
                Items.Add(item.Clone());
            }
        }
    }

    private bool CanPaste() => Clipboard.ContainsData(typeof(MyItem).FullName!);
}
```

---

## 8. References

- [Clipboard Class - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.clipboard)
- [DataObject Class - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.dataobject)
- [How to: Use the Clipboard - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/how-to-use-the-clipboard)
