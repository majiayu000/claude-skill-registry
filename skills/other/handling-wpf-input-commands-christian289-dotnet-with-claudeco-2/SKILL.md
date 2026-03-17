---
name: handling-wpf-input-commands
description: Implements WPF input handling with RoutedCommand, ICommand, CommandBinding, and InputBinding patterns. Use when creating keyboard shortcuts, menu commands, or custom command implementations.
---

# WPF Input and Commands Patterns

Handling user input and implementing command patterns in WPF applications.

## 1. Command System Overview

```
ICommand (Interface)
├── RoutedCommand (WPF built-in)
│   ├── ApplicationCommands (Copy, Paste, Cut, etc.)
│   ├── NavigationCommands (BrowseBack, BrowseForward, etc.)
│   ├── MediaCommands (Play, Pause, Stop, etc.)
│   └── EditingCommands (ToggleBold, ToggleItalic, etc.)
└── RelayCommand / DelegateCommand (MVVM)
```

---

## 2. Built-in Commands

### 2.1 ApplicationCommands

```xml
<Window.CommandBindings>
    <CommandBinding Command="ApplicationCommands.Copy"
                    Executed="CopyCommand_Executed"
                    CanExecute="CopyCommand_CanExecute"/>
    <CommandBinding Command="ApplicationCommands.Paste"
                    Executed="PasteCommand_Executed"/>
</Window.CommandBindings>

<StackPanel>
    <Button Command="ApplicationCommands.Copy" Content="Copy (Ctrl+C)"/>
    <Button Command="ApplicationCommands.Paste" Content="Paste (Ctrl+V)"/>
    <Button Command="ApplicationCommands.Undo" Content="Undo (Ctrl+Z)"/>
    <Button Command="ApplicationCommands.Redo" Content="Redo (Ctrl+Y)"/>
</StackPanel>
```

```csharp
private void CopyCommand_Executed(object sender, ExecutedRoutedEventArgs e)
{
    // Copy logic
    Clipboard.SetText(SelectedText);
}

private void CopyCommand_CanExecute(object sender, CanExecuteRoutedEventArgs e)
{
    // Enable condition
    e.CanExecute = !string.IsNullOrEmpty(SelectedText);
}
```

### 2.2 Common Built-in Commands

| Category | Commands |
|----------|----------|
| **ApplicationCommands** | New, Open, Save, SaveAs, Close, Print, Copy, Cut, Paste, Undo, Redo, Find, Replace, SelectAll, Delete, Properties, Help |
| **NavigationCommands** | BrowseBack, BrowseForward, BrowseHome, BrowseStop, Refresh, Favorites, Search, GoToPage, NextPage, PreviousPage, FirstPage, LastPage |
| **MediaCommands** | Play, Pause, Stop, Record, NextTrack, PreviousTrack, FastForward, Rewind, ChannelUp, ChannelDown, TogglePlayPause, IncreaseVolume, DecreaseVolume, MuteVolume |
| **EditingCommands** | ToggleBold, ToggleItalic, ToggleUnderline, IncreaseFontSize, DecreaseFontSize, AlignLeft, AlignCenter, AlignRight, AlignJustify |

---

## 3. Custom RoutedCommand

### 3.1 Define Custom Command

```csharp
namespace MyApp.Commands;

using System.Windows.Input;

public static class CustomCommands
{
    // Define custom command
    public static readonly RoutedCommand RefreshData = new(
        nameof(RefreshData),
        typeof(CustomCommands),
        new InputGestureCollection
        {
            new KeyGesture(Key.F5),
            new KeyGesture(Key.R, ModifierKeys.Control)
        });

    public static readonly RoutedCommand ExportToPdf = new(
        nameof(ExportToPdf),
        typeof(CustomCommands),
        new InputGestureCollection
        {
            new KeyGesture(Key.E, ModifierKeys.Control | ModifierKeys.Shift)
        });

    public static readonly RoutedCommand ToggleFullScreen = new(
        nameof(ToggleFullScreen),
        typeof(CustomCommands),
        new InputGestureCollection
        {
            new KeyGesture(Key.F11)
        });
}
```

### 3.2 Use Custom Command in XAML

```xml
<Window xmlns:cmd="clr-namespace:MyApp.Commands">
    <Window.CommandBindings>
        <CommandBinding Command="{x:Static cmd:CustomCommands.RefreshData}"
                        Executed="RefreshData_Executed"
                        CanExecute="RefreshData_CanExecute"/>
        <CommandBinding Command="{x:Static cmd:CustomCommands.ExportToPdf}"
                        Executed="ExportToPdf_Executed"/>
    </Window.CommandBindings>

    <Menu>
        <MenuItem Header="_File">
            <MenuItem Header="_Refresh"
                      Command="{x:Static cmd:CustomCommands.RefreshData}"
                      InputGestureText="F5"/>
            <MenuItem Header="_Export to PDF"
                      Command="{x:Static cmd:CustomCommands.ExportToPdf}"
                      InputGestureText="Ctrl+Shift+E"/>
        </MenuItem>
    </Menu>
</Window>
```

---

## 4. InputBinding (Keyboard/Mouse Shortcuts)

### 4.1 KeyBinding

```xml
<Window.InputBindings>
    <!-- Keyboard shortcut -->
    <KeyBinding Key="N" Modifiers="Control" Command="ApplicationCommands.New"/>
    <KeyBinding Key="S" Modifiers="Control" Command="ApplicationCommands.Save"/>
    <KeyBinding Key="S" Modifiers="Control+Shift" Command="ApplicationCommands.SaveAs"/>
    <KeyBinding Key="F4" Modifiers="Alt" Command="ApplicationCommands.Close"/>

    <!-- Function keys -->
    <KeyBinding Key="F1" Command="ApplicationCommands.Help"/>
    <KeyBinding Key="F5" Command="{x:Static cmd:CustomCommands.RefreshData}"/>

    <!-- MVVM Command binding -->
    <KeyBinding Key="Delete" Command="{Binding DeleteCommand}"/>
</Window.InputBindings>
```

### 4.2 MouseBinding

```xml
<Border.InputBindings>
    <!-- Double-click -->
    <MouseBinding MouseAction="LeftDoubleClick"
                  Command="{Binding OpenDetailCommand}"/>

    <!-- Middle click -->
    <MouseBinding MouseAction="MiddleClick"
                  Command="{Binding CloseTabCommand}"/>

    <!-- Ctrl + Left click -->
    <MouseBinding MouseAction="LeftClick"
                  Modifiers="Control"
                  Command="{Binding MultiSelectCommand}"/>
</Border.InputBindings>
```

---

## 5. CommandParameter

### 5.1 Static Parameter

```xml
<Button Command="{Binding NavigateCommand}"
        CommandParameter="Home"
        Content="Go to Home"/>

<Button Command="{Binding SetZoomCommand}"
        CommandParameter="100"
        Content="Zoom 100%"/>
```

### 5.2 Binding Parameter

```xml
<ListBox x:Name="ItemList" ItemsSource="{Binding Items}"/>
<Button Command="{Binding DeleteCommand}"
        CommandParameter="{Binding SelectedItem, ElementName=ItemList}"
        Content="Delete Selected"/>

<!-- Self-reference -->
<Button Command="{Binding ProcessCommand}"
        CommandParameter="{Binding RelativeSource={RelativeSource Self}}"
        Content="Process This Button"/>
```

---

## 6. CommandTarget

### 6.1 Redirecting Command Target

```xml
<StackPanel>
    <TextBox x:Name="TargetTextBox"/>

    <!-- Commands target the TextBox even when button is focused -->
    <Button Command="ApplicationCommands.Copy"
            CommandTarget="{Binding ElementName=TargetTextBox}"
            Content="Copy from TextBox"/>

    <Button Command="ApplicationCommands.Paste"
            CommandTarget="{Binding ElementName=TargetTextBox}"
            Content="Paste to TextBox"/>
</StackPanel>
```

---

## 7. Handling Keyboard Input

### 7.1 Key Events

```csharp
namespace MyApp.Views;

using System.Windows;
using System.Windows.Input;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        // Preview events (Tunneling - captured before child elements)
        PreviewKeyDown += OnPreviewKeyDown;

        // Normal events (Bubbling - captured after child elements)
        KeyDown += OnKeyDown;
    }

    private void OnPreviewKeyDown(object sender, KeyEventArgs e)
    {
        // Global shortcut handling
        if (e.Key == Key.Escape)
        {
            // Close popup or cancel operation
            e.Handled = true;
        }

        // Modifier key combinations
        if (Keyboard.Modifiers == ModifierKeys.Control && e.Key == Key.G)
        {
            // Ctrl+G: Go to line
            ShowGoToLineDialog();
            e.Handled = true;
        }
    }

    private void OnKeyDown(object sender, KeyEventArgs e)
    {
        // Handle if not processed by child elements
    }
}
```

### 7.2 TextInput Event

```csharp
private void TextBox_PreviewTextInput(object sender, TextCompositionEventArgs e)
{
    // Allow only numeric input
    if (!char.IsDigit(e.Text, 0))
    {
        e.Handled = true;
    }
}
```

---

## 8. Handling Mouse Input

### 8.1 Mouse Events

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Input;

public partial class DrawingCanvas : FrameworkElement
{
    private Point _startPoint;
    private bool _isDragging;

    public DrawingCanvas()
    {
        MouseLeftButtonDown += OnMouseLeftButtonDown;
        MouseMove += OnMouseMove;
        MouseLeftButtonUp += OnMouseLeftButtonUp;
        MouseWheel += OnMouseWheel;
    }

    private void OnMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        _startPoint = e.GetPosition(this);
        _isDragging = true;

        // Capture mouse to receive events outside the element
        CaptureMouse();

        // Click count detection
        if (e.ClickCount == 2)
        {
            // Double click
        }
    }

    private void OnMouseMove(object sender, MouseEventArgs e)
    {
        if (!_isDragging) return;

        var currentPoint = e.GetPosition(this);
        var delta = currentPoint - _startPoint;

        // Draw or drag logic
    }

    private void OnMouseLeftButtonUp(object sender, MouseButtonEventArgs e)
    {
        if (_isDragging)
        {
            _isDragging = false;
            ReleaseMouseCapture();
        }
    }

    private void OnMouseWheel(object sender, MouseWheelEventArgs e)
    {
        // e.Delta: positive = scroll up, negative = scroll down
        var zoomFactor = e.Delta > 0 ? 1.1 : 0.9;
        ApplyZoom(zoomFactor);
    }
}
```

---

## 9. Focus Management

### 9.1 Programmatic Focus Control

```csharp
// Set focus
myTextBox.Focus();

// Set keyboard focus specifically
Keyboard.Focus(myTextBox);

// Check focus
if (myTextBox.IsFocused)
{
    // Has focus
}

if (myTextBox.IsKeyboardFocused)
{
    // Has keyboard focus
}
```

### 9.2 FocusManager

```xml
<!-- Set default focused element -->
<Window FocusManager.FocusedElement="{Binding ElementName=FirstTextBox}">
    <StackPanel>
        <TextBox x:Name="FirstTextBox"/>
        <TextBox x:Name="SecondTextBox"/>
    </StackPanel>
</Window>

<!-- Define focus scope -->
<ToolBar FocusManager.IsFocusScope="True">
    <Button Content="Button 1"/>
    <Button Content="Button 2"/>
</ToolBar>
```

---

## 10. References

- [Commanding Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/commanding-overview)
- [Input Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/input-overview)
- [Focus Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/focus-overview)
