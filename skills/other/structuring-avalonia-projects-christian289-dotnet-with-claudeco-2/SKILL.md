---
name: structuring-avalonia-projects
description: "Guides the design of AvaloniaUI solution and project structures. Use when creating new AvaloniaUI solutions or organizing projects following naming conventions and layer separation."
---

# 6.2 AvaloniaUI Solution and Project Structure

#### 6.2.1 Project Naming Conventions

```
SolutionName/
├── SolutionName.Abstractions      // .NET Class Library (Interface, abstract class, and other abstract types)
├── SolutionName.Core              // .NET Class Library (Business logic, pure C#)
├── SolutionName.Core.Tests        // xUnit Test Project
├── SolutionName.ViewModels        // .NET Class Library (MVVM ViewModel)
├── SolutionName.AvaloniaServices  // Avalonia Class Library (Avalonia-related services)
├── SolutionName.AvaloniaLib       // Avalonia Class Library (Reusable components)
├── SolutionName.AvaloniaApp       // Avalonia Application Project (Entry point)
├── SolutionName.UI                // Avalonia Custom Control Library (Custom controls)
└── [Solution Folders]
    ├── SolutionName/              // Main project group
    └── Common/                    // Common project group
```

**Naming by Project Type:**
- `.Abstractions`: .NET Class Library - Defines abstract types like Interface, abstract class (Inversion of Control)
- `.Core`: .NET Class Library - Business logic, data models, services (UI framework independent)
- `.Core.Tests`: xUnit/NUnit/MSTest Test Project
- `.ViewModels`: .NET Class Library - MVVM ViewModel (UI framework independent)
- `.AvaloniaServices`: Avalonia Class Library - Avalonia-related services (DialogService, NavigationService, etc.)
- `.AvaloniaLib`: Avalonia Class Library - Reusable UserControl, Window, Converter, Behavior, AttachedProperty
- `.AvaloniaApp`: Avalonia Application Project - Entry point, App.axaml
- `.UI`: Avalonia Custom Control Library - ControlTheme-based custom controls

**Project Dependency Hierarchy:**
```
SolutionName.AvaloniaApp
    ↓ references
SolutionName.Abstractions (Top layer - does not depend on other projects)
    ↓ references
SolutionName.Core
```

**Role of the Abstractions Layer:**
- Houses all Interfaces and abstract classes
- Dependency inversion through abstract types instead of direct references to concrete types (Dependency Inversion Principle)
- Actual implementations injected via DI container at runtime
- Can be replaced with Mock objects during testing

