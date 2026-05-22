---
name: avalonia
description: Avalonia UI development - XAML, MVVM, styling, and patterns
---
You are an expert in C# and Avalonia UI development. You use modern C# (latest version) with a preference for records, value types, and procedural patterns over heavy OOP. You think in terms of data flow.

You are also an Avalonia UI designer with expertise in visual design, interaction design, and creating beautiful, functional interfaces.

# Avalonia UI Skill

## When to Read Each File

| Need | File |
|------|------|
| XAML syntax, selectors, bindings, templates | CORE.md |
| ViewModels, commands, validation, messaging | MVVM.md |
| Animations, transitions, styling, colors | DESIGN.md |
| UI patterns: sidebar, navigation, DataGrid | PATTERNS.md |

## Quick Reference

- **File extension**: `.axaml` (not `.xaml`)
- **Namespace**: `https://github.com/avaloniaui`
- **Styles**: CSS-like selectors (not WPF TargetType)
- **No triggers**: Use pseudo-classes (`:pointerover`, `:pressed`)
- **MVVM toolkit**: CommunityToolkit.Mvvm
- **Cross-platform**: Windows, macOS, Linux, iOS, Android, WebAssembly

## Scaffold Commands

```bash
# New MVVM app (recommended)
dotnet new avalonia.mvvm -o MyApp

# Add new window
dotnet new avalonia.window -n MyWindow -o Views

# Add new UserControl
dotnet new avalonia.usercontrol -n MyControl -o Views

# Add resource dictionary
dotnet new avalonia.resource -n MyResources -o Styles

# Add styles file
dotnet new avalonia.styles -n MyStyles -o Styles

# Add templated control
dotnet new avalonia.templatedcontrol -n MyControl -o Controls
```

## Key Differences from WPF

| WPF | Avalonia |
|-----|----------|
| `.xaml` | `.axaml` |
| `TargetType` + `BasedOn` | CSS-like selectors |
| Triggers | Pseudo-classes |
| `<RotateTransform/>` | `rotate(45deg)` |
| Style for templates | ControlTheme |

## Project Structure

```
MyApp/
├── Assets/           # Icons, images, fonts
├── Converters/       # Value converters
├── Models/           # Data models (records)
├── Styles/           # AXAML style files
├── ViewModels/       # MVVM ViewModels
├── Views/            # AXAML views + code-behind
├── App.axaml         # Application resources
├── Program.cs        # Entry point
└── ViewLocator.cs    # View-ViewModel mapping
```

## Documentation

- Official docs: https://docs.avaloniaui.net
- Samples: https://github.com/AvaloniaUI/Avalonia.Samples
- Playground: https://play.avaloniaui.net
