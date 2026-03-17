---
name: resources-localization
description: >
  Guidance for .NET resource files (.resx) and IStringLocalizer-based localization.
  USE FOR: .resx resource file management, IStringLocalizer and IStringLocalizerFactory usage, strongly-typed resource access, satellite assembly localization.
  DO NOT USE FOR: culture-aware number/date formatting (use globalization-localization), ICU plural/gender patterns (use messageformat-net), full i18n architecture (use i18n).
license: MIT
metadata:
  displayName: "Resources and Localization"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: ".NET Localization Documentation"
    url: "https://learn.microsoft.com/en-us/dotnet/core/extensions/localization"
  - title: "Globalization and Localization in ASP.NET Core"
    url: "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/localization"
  - title: "Globalize and Localize .NET Applications"
    url: "https://learn.microsoft.com/en-us/dotnet/core/extensions/globalization-and-localization"
---

# Resources and Localization

## Overview

.NET resource files (`.resx`) are the standard mechanism for storing localizable strings, images, and other assets. At compile time, `.resx` files are embedded into satellite assemblies organized by culture. At runtime, `ResourceManager` or the higher-level `IStringLocalizer<T>` abstraction resolves the correct resource based on the current UI culture. This system supports culture fallback chains (e.g., `fr-CA` falls back to `fr`, then to the neutral/default resource).

ASP.NET Core wraps this infrastructure with `IStringLocalizer<T>`, `IStringLocalizerFactory`, and `IHtmlLocalizer<T>`, integrating resource lookup with dependency injection and the request localization middleware.

## Basic Resource File Setup

Create `.resx` files following the naming convention `{TypeName}.{culture}.resx`. The neutral resource (no culture suffix) serves as the fallback.

```
Resources/
  Services/
    GreetingService.resx          # Default (en-US)
    GreetingService.fr-FR.resx    # French
    GreetingService.de-DE.resx    # German
    GreetingService.ja-JP.resx    # Japanese
```

Register localization services pointing to the resource directory:

```csharp
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddLocalization(options =>
    options.ResourcesPath = "Resources");

var app = builder.Build();
app.UseRequestLocalization();
app.Run();
```

## IStringLocalizer Usage

`IStringLocalizer<T>` provides strongly-typed resource lookup tied to a specific class. The type parameter determines which `.resx` file is searched.

```csharp
using Microsoft.Extensions.Localization;

namespace MyApp.Services;

public sealed class GreetingService
{
    private readonly IStringLocalizer<GreetingService> _localizer;

    public GreetingService(IStringLocalizer<GreetingService> localizer)
    {
        _localizer = localizer;
    }

    public string GetWelcome()
    {
        // Looks up "WelcomeMessage" in
        // Resources/Services/GreetingService.{culture}.resx
        return _localizer["WelcomeMessage"];
    }

    public string GetItemCount(int count)
    {
        // Parameterized: "You have {0} items in your cart."
        return _localizer["ItemCount", count];
    }

    public IEnumerable<LocalizedString> GetAllStrings()
    {
        return _localizer.GetAllStrings(includeParentCultures: true);
    }
}
```

## Strongly-Typed Resource Access

The classic `ResourceManager` pattern generates a strongly-typed class from the `.resx` file at compile time, providing compile-time safety for resource keys.

```csharp
using System.Globalization;
using System.Resources;

namespace MyApp.Resources;

// Auto-generated from Messages.resx by ResXFileCodeGenerator
// Access via: Messages.WelcomeTitle
public static class Messages
{
    private static readonly ResourceManager _resourceManager =
        new ResourceManager(
            "MyApp.Resources.Messages",
            typeof(Messages).Assembly);

    public static string WelcomeTitle =>
        _resourceManager.GetString(
            nameof(WelcomeTitle),
            CultureInfo.CurrentUICulture) ?? nameof(WelcomeTitle);

    public static string ErrorNotFound =>
        _resourceManager.GetString(
            nameof(ErrorNotFound),
            CultureInfo.CurrentUICulture) ?? nameof(ErrorNotFound);

    public static string FormatGreeting(string name) =>
        string.Format(
            CultureInfo.CurrentUICulture,
            _resourceManager.GetString(
                "Greeting",
                CultureInfo.CurrentUICulture) ?? "Hello, {0}!",
            name);
}
```

## IStringLocalizerFactory for Dynamic Types

When you need to resolve resources for a type determined at runtime, use `IStringLocalizerFactory`.

```csharp
using Microsoft.Extensions.Localization;
using System;

namespace MyApp.Services;

public class DynamicLocalizationService
{
    private readonly IStringLocalizerFactory _factory;

    public DynamicLocalizationService(
        IStringLocalizerFactory factory)
    {
        _factory = factory;
    }

    public string Localize(string key, string resourceSource)
    {
        var type = Type.GetType(resourceSource)
            ?? throw new ArgumentException(
                $"Type '{resourceSource}' not found.");
        var localizer = _factory.Create(type);
        return localizer[key];
    }

    public string LocalizeByBaseName(
        string key, string baseName, string location)
    {
        var localizer = _factory.Create(baseName, location);
        return localizer[key];
    }
}
```

## Missing Resource Detection

In development, detect missing translation keys to report them to the localization team.

```csharp
using Microsoft.Extensions.Localization;
using Microsoft.Extensions.Logging;

namespace MyApp.Services;

public sealed class SafeLocalizer<T>
{
    private readonly IStringLocalizer<T> _localizer;
    private readonly ILogger<SafeLocalizer<T>> _logger;

    public SafeLocalizer(
        IStringLocalizer<T> localizer,
        ILogger<SafeLocalizer<T>> logger)
    {
        _localizer = localizer;
        _logger = logger;
    }

    public string this[string key, params object[] arguments]
    {
        get
        {
            var result = _localizer[key, arguments];
            if (result.ResourceNotFound)
            {
                _logger.LogWarning(
                    "Missing resource key '{Key}' for type '{Type}'",
                    key, typeof(T).FullName);
            }
            return result.Value;
        }
    }
}
```

## Resource Lookup Resolution Order

| Step | Resource Searched | Example for `fr-CA` |
|---|---|---|
| 1 | Exact culture | `GreetingService.fr-CA.resx` |
| 2 | Parent culture | `GreetingService.fr.resx` |
| 3 | Neutral / default | `GreetingService.resx` |
| 4 | Key returned as-is | `"WelcomeMessage"` (the key string) |

## IStringLocalizer vs ResourceManager

| Feature | `IStringLocalizer<T>` | `ResourceManager` |
|---|---|---|
| DI integration | Built-in | Manual |
| Parameterized strings | `_localizer["Key", arg]` | `string.Format(rm.GetString("Key"), arg)` |
| Missing key behavior | Returns key as value | Returns `null` |
| HTML-safe variant | `IHtmlLocalizer<T>` | Not available |
| Compile-time safety | No (string keys) | Yes (generated properties) |
| ASP.NET Core integration | First-class | Requires manual wiring |

## Best Practices

1. **Keep resource keys stable and descriptive** (e.g., `OrderConfirmation_Subject`) because renaming keys invalidates existing translations and breaks satellite assemblies.
2. **Use `IStringLocalizer<T>` over raw `ResourceManager`** in ASP.NET Core applications to benefit from DI, culture-aware middleware, and the `IHtmlLocalizer` variant.
3. **Always provide a neutral fallback `.resx`** (without a culture suffix) for every resource file to ensure the application never displays raw resource keys to users.
4. **Organize resources to mirror the namespace structure** (e.g., `Resources/Services/OrderService.resx`) so that `IStringLocalizer<T>` can resolve them automatically.
5. **Use parameterized resource values** (`"Welcome, {0}!"`) instead of concatenating localized fragments, because word order varies across languages.
6. **Set the `ResourcesPath` option** in `AddLocalization()` to a single `Resources` folder to keep translation files separate from code files.
7. **Log missing resource keys in development** by checking `LocalizedString.ResourceNotFound` to catch untranslated strings before they reach production.
8. **Avoid embedding formatting logic** (dates, numbers) in resource values; keep the raw parameterized string in the `.resx` and format values in code using `CultureInfo`.
9. **Use the shared resource pattern** (a marker class like `SharedResource`) for cross-cutting strings (button labels, common errors) to avoid duplicating keys.
10. **Validate all resource files at build time** by enabling `MissingManifestResourceException` detection in tests or CI to catch `.resx` files that were not embedded correctly.
