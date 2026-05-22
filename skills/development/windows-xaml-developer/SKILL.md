---
name: windows-xaml-developer
description: Expert guidance on building modern Windows apps with WinUI 3, WPF, and the MVVM pattern.
---

# Windows XAML Developer

## Overview
This skill provides best practices, architectural patterns, and library recommendations for building high-quality Windows desktop applications using XAML-based frameworks (WinUI 3 and WPF). It emphasizes the Model-View-ViewModel (MVVM) pattern, Dependency Injection (DI), and modern C# features.

## When to Use
- When generating code for Windows desktop applications (WinUI 3, WPF, UWP).
- When structuring a new Windows XAML project.
- When implementing the MVVM pattern.
- When troubleshooting XAML binding or UI responsiveness issues.

## Core Principles

1.  **MVVM First**: Always separate UI logic (View) from business logic (ViewModel). Avoid code-behind (`.xaml.cs`) except for pure UI concerns (e.g., window manipulation).
2.  **Dependency Injection**: Use DI to manage services and ViewModels. Avoid static singletons for testability.
3.  **Responsive UI**: Never block the UI thread. Use `async/await` for I/O and heavy computations.
4.  **Modern Tooling**: Leverage Roslyn source generators (e.g., `CommunityToolkit.Mvvm`) to reduce boilerplate.

## Recommended Tech Stack

### Frameworks
* **Primary**: **WinUI 3 (Windows App SDK)** - The modern, native UI stack for Windows. Best for new applications.
* **Secondary**: **WPF (.NET 8/9)** - Mature, stable ecosystem. Best for complex enterprise apps or when specific third-party controls are needed.

### Essential Libraries
| Category | Library | Usage |
| :--- | :--- | :--- |
| **MVVM** | `CommunityToolkit.Mvvm` | Standard implementation for `ObservableObject`, `RelayCommand`, and Messenger. |
| **Dependency Injection** | `Microsoft.Extensions.DependencyInjection` | Industry-standard DI container. |
| **Hosting/Lifecycle** | `Microsoft.Extensions.Hosting` | Application bootstrap, logging, and configuration. |
| **WPF UI Library** | `MaterialDesignInXamlToolkit` or `MahApps.Metro` | (WPF Only) Modern styling and controls. |
| **WinUI Helpers** | `CommunityToolkit.WinUI` | Additional controls, helpers, and extensions for WinUI 3. |

## Project Structure
Organize the solution to enforce strict separation of concerns:

```text
MyWindowsApp/
├── App.xaml                 # Application entry & DI composition root
├── Views/                   # XAML Windows, Pages, and UserControls
├── ViewModels/              # C# ViewModels (one per View)
├── Models/                  # Domain entities and data structures
├── Services/                # Business logic and data access interfaces/implementations
├── Converters/              # IValueConverter implementations
└── Assets/                  # Images, fonts, and resources