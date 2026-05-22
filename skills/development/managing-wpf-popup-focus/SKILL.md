---
name: managing-wpf-popup-focus
description: "Manages focus behavior for WPF Popup controls using PreviewMouseDown events. Use when Popup loses focus unexpectedly or needs to stay open during user interaction."
---

# 5.7 Popup Control Usage Considerations

In WPF, the Popup control only operates correctly when the WPF Application has focus. When focus moves to another application, the Popup may not display or function properly.

#### 5.7.1 Focus Management Pattern

When using the Popup control in WPF, **you must forcibly acquire focus through the PreviewMouseDown event.**

## Project Structure

The templates folder contains a .NET 9 WPF project example.

```
templates/
└── WpfPopupSample.App/                  ← WPF Application
    ├── Views/
    │   ├── MainWindow.xaml
    │   └── MainWindow.xaml.cs           ← Focus management pattern implementation
    ├── App.xaml
    ├── App.xaml.cs
    ├── GlobalUsings.cs
    └── WpfPopupSample.App.csproj
```

#### 5.7.2 Core Principles

- **Popup operation condition**: Only operates when WPF Application has focus
- **PreviewMouseDown event**: Check focus state on mouse click
- **IsKeyboardFocused check**: Verify keyboard focus status
- **Activate() call**: Activate window to restore focus if not focused
- **For UserControl**: Activate parent window with `Window.GetWindow(this)?.Activate()`

#### 5.7.3 Why Is This Necessary?

1. **Focus moves to another app**: When user clicks another application and returns
2. **Background execution**: Ensure Popup operation when WPF app is in background
3. **User experience**: Ensure Popup always works as expected

**⚠️ Important Notes:**

- This pattern must be applied to all Windows using Popup

#### 5.7.4 References

- [WPF Popup Focus Issue - .NET Dev Forum](https://forum.dotnetdev.kr/t/wpf-popup/8296)

