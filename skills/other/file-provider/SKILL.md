---
name: file-provider
description: >
  Guidance for Microsoft.Extensions.FileProviders abstraction layer.
  USE FOR: abstracting file access over physical files, embedded resources, and composite sources, watching for file changes, serving static content, testable file access, configuration file providers.
  DO NOT USE FOR: high-throughput binary I/O (use System.IO directly), file upload handling (use ASP.NET form files), database-backed storage, cloud blob storage (use Azure SDK).
license: MIT
metadata:
  displayName: File Providers
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "File Providers in ASP.NET Core Documentation on Microsoft Learn"
    url: "https://learn.microsoft.com/aspnet/core/fundamentals/file-providers"
  - title: "Microsoft.Extensions.FileProviders.Physical NuGet Package"
    url: "https://www.nuget.org/packages/Microsoft.Extensions.FileProviders.Physical"
  - title: "Microsoft.Extensions.FileProviders.Abstractions NuGet Package"
    url: "https://www.nuget.org/packages/Microsoft.Extensions.FileProviders.Abstractions"
---

# Microsoft.Extensions.FileProviders

## Overview

`Microsoft.Extensions.FileProviders` provides a unified abstraction for reading files from different sources including the physical file system, embedded resources in assemblies, and composite providers that merge multiple sources. The core interface `IFileProvider` exposes methods for getting file info, listing directory contents, and watching for changes.

File providers integrate deeply with ASP.NET Core for static file serving, configuration reloading, and Razor view discovery. They are also useful in non-web applications for abstracting file access behind an interface that can be swapped for testing or to support embedded resources.

Install via NuGet:
```
dotnet add package Microsoft.Extensions.FileProviders.Abstractions
dotnet add package Microsoft.Extensions.FileProviders.Physical
dotnet add package Microsoft.Extensions.FileProviders.Embedded
dotnet add package Microsoft.Extensions.FileProviders.Composite
```

## PhysicalFileProvider

`PhysicalFileProvider` reads files from a directory on disk. It supports glob-based file watching via `IChangeToken`.

```csharp
using System.IO;
using Microsoft.Extensions.FileProviders;

// Create a provider rooted at a directory
var contentRoot = Path.Combine(Directory.GetCurrentDirectory(), "content");
using var provider = new PhysicalFileProvider(contentRoot);

// Get a single file
IFileInfo fileInfo = provider.GetFileInfo("templates/welcome.html");
if (fileInfo.Exists)
{
    using var stream = fileInfo.CreateReadStream();
    using var reader = new StreamReader(stream);
    string content = await reader.ReadToEndAsync();
    Console.WriteLine($"File: {fileInfo.Name}, Length: {fileInfo.Length}");
}

// List directory contents
IDirectoryContents directory = provider.GetDirectoryContents("templates");
foreach (var file in directory)
{
    Console.WriteLine($"  {file.Name} ({file.Length} bytes, Dir={file.IsDirectory})");
}
```

## EmbeddedFileProvider (ManifestEmbeddedFileProvider)

`ManifestEmbeddedFileProvider` reads files embedded in an assembly. Files must be included as embedded resources in the `.csproj`.

```xml
<!-- In your .csproj file -->
<ItemGroup>
  <EmbeddedResource Include="Resources/**/*" />
</ItemGroup>

<PropertyGroup>
  <GenerateEmbeddedFilesManifest>true</GenerateEmbeddedFilesManifest>
</PropertyGroup>

<ItemGroup>
  <PackageReference Include="Microsoft.Extensions.FileProviders.Embedded" Version="8.0.0" />
</ItemGroup>
```

```csharp
using System.Reflection;
using Microsoft.Extensions.FileProviders;

// Access embedded resources with directory structure preserved
var assembly = Assembly.GetExecutingAssembly();
var embedded = new ManifestEmbeddedFileProvider(assembly, "Resources");

IFileInfo template = embedded.GetFileInfo("email/welcome.html");
if (template.Exists)
{
    using var stream = template.CreateReadStream();
    using var reader = new StreamReader(stream);
    var html = await reader.ReadToEndAsync();
}

// List embedded files
var files = embedded.GetDirectoryContents("email");
foreach (var file in files)
{
    Console.WriteLine($"Embedded: {file.Name}");
}
```

## CompositeFileProvider

`CompositeFileProvider` merges multiple providers so files can be resolved from any source in priority order. The first provider to contain a matching file wins.

```csharp
using Microsoft.Extensions.FileProviders;

// Overlay: user overrides first, then embedded defaults
var userOverrides = new PhysicalFileProvider("/app/custom-templates");
var defaults = new ManifestEmbeddedFileProvider(typeof(Program).Assembly, "Resources");
var composite = new CompositeFileProvider(userOverrides, defaults);

// Resolves from userOverrides if present, otherwise from defaults
IFileInfo file = composite.GetFileInfo("email/welcome.html");
```

## Watching for File Changes

`IFileProvider.Watch` returns an `IChangeToken` that triggers when files matching a glob pattern are created, modified, or deleted. Use `ChangeToken.OnChange` for convenient callback registration.

```csharp
using Microsoft.Extensions.FileProviders;
using Microsoft.Extensions.Primitives;

using var provider = new PhysicalFileProvider("/app/config");

// Watch for changes to any JSON file in the config directory
ChangeToken.OnChange(
    () => provider.Watch("**/*.json"),
    () =>
    {
        Console.WriteLine("Configuration files changed, reloading...");
        ReloadConfiguration(provider);
    });

// Watch a specific file
ChangeToken.OnChange(
    () => provider.Watch("appsettings.json"),
    () => Console.WriteLine("appsettings.json was modified"));

void ReloadConfiguration(IFileProvider fileProvider)
{
    var settingsFile = fileProvider.GetFileInfo("appsettings.json");
    if (settingsFile.Exists)
    {
        using var stream = settingsFile.CreateReadStream();
        // Parse and apply new settings
    }
}
```

## Integrating with Dependency Injection

Register file providers in the DI container and inject `IFileProvider` where needed.

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.FileProviders;
using Microsoft.Extensions.Hosting;

var builder = Host.CreateApplicationBuilder(args);

// Register a named file provider
builder.Services.AddSingleton<IFileProvider>(sp =>
{
    var env = sp.GetRequiredService<IHostEnvironment>();
    var physical = new PhysicalFileProvider(
        Path.Combine(env.ContentRootPath, "templates"));
    var embedded = new ManifestEmbeddedFileProvider(
        typeof(Program).Assembly, "Resources");
    return new CompositeFileProvider(physical, embedded);
});

builder.Services.AddTransient<TemplateService>();

using var host = builder.Build();
```

```csharp
using System.IO;
using System.Threading.Tasks;
using Microsoft.Extensions.FileProviders;

public class TemplateService
{
    private readonly IFileProvider _fileProvider;

    public TemplateService(IFileProvider fileProvider)
    {
        _fileProvider = fileProvider;
    }

    public async Task<string> LoadTemplateAsync(string templateName)
    {
        var fileInfo = _fileProvider.GetFileInfo($"email/{templateName}.html");
        if (!fileInfo.Exists)
            throw new FileNotFoundException($"Template not found: {templateName}");

        using var stream = fileInfo.CreateReadStream();
        using var reader = new StreamReader(stream);
        return await reader.ReadToEndAsync();
    }
}
```

## Provider Comparison

| Provider | Source | Change Watching | Use Case |
|----------|--------|-----------------|----------|
| `PhysicalFileProvider` | Disk | Yes (polling) | Config files, user uploads, templates |
| `ManifestEmbeddedFileProvider` | Assembly | No | Default templates, bundled assets |
| `CompositeFileProvider` | Multiple | Delegates to children | Overlay user files over defaults |
| `NullFileProvider` | None | No | Testing, placeholder |

## Best Practices

1. **Use `CompositeFileProvider` for override patterns** where user-customizable files take priority over embedded defaults, eliminating conditional file-exists logic.
2. **Inject `IFileProvider` through DI** rather than creating providers inline so the file source can be swapped for testing with `NullFileProvider` or an in-memory implementation.
3. **Dispose `PhysicalFileProvider` when the application shuts down** because it holds a `FileSystemWatcher` internally that leaks if not disposed.
4. **Use `ManifestEmbeddedFileProvider` with `GenerateEmbeddedFilesManifest`** in the `.csproj` to preserve directory structure; without the manifest, directory listings are not supported.
5. **Prefer `ChangeToken.OnChange` over manual `IChangeToken` polling** because it handles re-registration automatically when a token is consumed.
6. **Scope `PhysicalFileProvider` to a specific directory** rather than the filesystem root to limit access and prevent path traversal.
7. **Check `IFileInfo.Exists` before calling `CreateReadStream()`** because non-existent files return a `NotFoundFileInfo` that throws on stream creation.
8. **Use glob patterns in `Watch()`** like `**/*.json` for recursive watching or `config/*.yaml` for directory-scoped watching instead of watching individual files one at a time.
9. **Cache file contents in memory** for frequently accessed templates rather than reading from the provider on every request, using `IChangeToken` to invalidate the cache.
10. **Avoid using `PhysicalFileProvider` in unit tests** -- create a test implementation of `IFileProvider` or use `NullFileProvider` to keep tests fast and deterministic.
