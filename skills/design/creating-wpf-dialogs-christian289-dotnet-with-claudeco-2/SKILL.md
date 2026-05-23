---
name: creating-wpf-dialogs
description: Creates WPF dialog windows including modal dialogs, MessageBox, and common dialogs. Use when implementing confirmation prompts, settings windows, or file/folder pickers.
---

# WPF Dialog Patterns

Creating and managing dialog windows for user interaction.

**Advanced Patterns:** See [ADVANCED.md](ADVANCED.md) for MVVM dialog service, modeless dialogs, and input dialogs.

## 1. Dialog Types Overview

```
Dialog Types
├── Modal Dialogs (ShowDialog)
│   ├── Custom Window dialogs
│   └── MessageBox
├── Modeless Dialogs (Show)
│   └── Tool windows, floating panels
└── Common Dialogs
    ├── OpenFileDialog
    ├── SaveFileDialog
    └── FolderBrowserDialog
```

---

## 2. MessageBox

### 2.1 Basic Usage

```csharp
// Simple message
MessageBox.Show("Operation completed successfully.");

// With title
MessageBox.Show("File saved.", "Success");

// With buttons
var result = MessageBox.Show(
    "Do you want to save changes?",
    "Confirm",
    MessageBoxButton.YesNoCancel);

// With icon
MessageBox.Show(
    "An error occurred.",
    "Error",
    MessageBoxButton.OK,
    MessageBoxImage.Error);
```

### 2.2 MessageBox Options

**Buttons:**
| Value | Buttons |
|-------|---------|
| OK | OK |
| OKCancel | OK, Cancel |
| YesNo | Yes, No |
| YesNoCancel | Yes, No, Cancel |

**Icons:**
| Value | Icon |
|-------|------|
| None | No icon |
| Information | Info circle |
| Warning | Warning triangle |
| Error | Red X |

### 2.3 Processing Results

```csharp
var result = MessageBox.Show(
    "Are you sure you want to delete this item?",
    "Confirm Delete",
    MessageBoxButton.YesNo,
    MessageBoxImage.Warning,
    MessageBoxResult.No);  // Default button

switch (result)
{
    case MessageBoxResult.Yes:
        DeleteItem();
        break;
    case MessageBoxResult.No:
        // Cancelled
        break;
}
```

---

## 3. Custom Modal Dialog

### 3.1 Dialog Window XAML

```xml
<Window x:Class="MyApp.Dialogs.SettingsDialog"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Settings"
        Width="400" Height="300"
        WindowStartupLocation="CenterOwner"
        ResizeMode="NoResize"
        ShowInTaskbar="False">
    <Grid Margin="20">
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>

        <!-- Content -->
        <StackPanel Grid.Row="0">
            <Label Content="User Name:"/>
            <TextBox x:Name="UserNameTextBox" Margin="0,5,0,15"/>
            <CheckBox x:Name="EnableNotificationsCheckBox"
                      Content="Enable notifications"/>
        </StackPanel>

        <!-- Dialog buttons -->
        <StackPanel Grid.Row="1" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="OK" Width="80" Margin="0,0,10,0"
                    Click="OkButton_Click" IsDefault="True"/>
            <Button Content="Cancel" Width="80"
                    Click="CancelButton_Click" IsCancel="True"/>
        </StackPanel>
    </Grid>
</Window>
```

### 3.2 Dialog Code-Behind

```csharp
namespace MyApp.Dialogs;

using System.Windows;

public partial class SettingsDialog : Window
{
    public string UserName { get; private set; } = string.Empty;
    public bool EnableNotifications { get; private set; }

    public SettingsDialog()
    {
        InitializeComponent();
    }

    private void OkButton_Click(object sender, RoutedEventArgs e)
    {
        // Validate input
        if (string.IsNullOrWhiteSpace(UserNameTextBox.Text))
        {
            MessageBox.Show("Please enter a user name.", "Validation Error",
                MessageBoxButton.OK, MessageBoxImage.Warning);
            UserNameTextBox.Focus();
            return;
        }

        // Set results
        UserName = UserNameTextBox.Text;
        EnableNotifications = EnableNotificationsCheckBox.IsChecked ?? false;

        // Close with success
        DialogResult = true;
    }

    private void CancelButton_Click(object sender, RoutedEventArgs e)
    {
        DialogResult = false;
    }
}
```

### 3.3 Using the Dialog

```csharp
private void OpenSettings_Click(object sender, RoutedEventArgs e)
{
    var dialog = new SettingsDialog
    {
        Owner = this  // Set owner for centering
    };

    if (dialog.ShowDialog() == true)
    {
        // User clicked OK
        _currentUserName = dialog.UserName;
        _enableNotifications = dialog.EnableNotifications;
        ApplySettings();
    }
}
```

---

## 4. Common Dialogs

### 4.1 OpenFileDialog

```csharp
using Microsoft.Win32;

private void OpenFile_Click(object sender, RoutedEventArgs e)
{
    var dialog = new OpenFileDialog
    {
        Title = "Open File",
        Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*",
        FilterIndex = 1,
        InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
        Multiselect = false,
        CheckFileExists = true
    };

    if (dialog.ShowDialog() == true)
    {
        var filePath = dialog.FileName;
        LoadFile(filePath);
    }
}

// Multiple file selection
private void OpenMultipleFiles_Click(object sender, RoutedEventArgs e)
{
    var dialog = new OpenFileDialog
    {
        Multiselect = true,
        Filter = "Image files (*.png;*.jpg)|*.png;*.jpg"
    };

    if (dialog.ShowDialog() == true)
    {
        foreach (var file in dialog.FileNames)
        {
            ProcessFile(file);
        }
    }
}
```

### 4.2 SaveFileDialog

```csharp
using Microsoft.Win32;

private void SaveFile_Click(object sender, RoutedEventArgs e)
{
    var dialog = new SaveFileDialog
    {
        Title = "Save File",
        Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*",
        FileName = "document.txt",
        DefaultExt = ".txt",
        AddExtension = true,
        OverwritePrompt = true
    };

    if (dialog.ShowDialog() == true)
    {
        var filePath = dialog.FileName;
        SaveFile(filePath);
    }
}
```

### 4.3 .NET 8+ Folder Picker

```csharp
// .NET 8+ includes OpenFolderDialog
private void SelectFolder_Click(object sender, RoutedEventArgs e)
{
    var dialog = new OpenFolderDialog
    {
        Title = "Select Output Folder",
        InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments)
    };

    if (dialog.ShowDialog() == true)
    {
        var folderPath = dialog.FolderName;
        ProcessFolder(folderPath);
    }
}
```

---

## 5. References

- [Dialog Boxes Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/windows/dialog-boxes-overview)
- [MessageBox Class - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.messagebox)
- [OpenFileDialog Class - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/microsoft.win32.openfiledialog)
