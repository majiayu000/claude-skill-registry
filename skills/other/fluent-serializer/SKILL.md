---
name: fluent-serializer
description: >
  Guidance for fluent API serialization configuration patterns in .NET.
  USE FOR: building configurable serialization pipelines, wrapping System.Text.Json or Newtonsoft.Json
  with fluent APIs, custom serialization profiles, convention-based JSON configuration,
  reusable serialization presets across multiple services.
  DO NOT USE FOR: binary serialization (use protobuf-net or Bond), schema-first serialization,
  high-throughput hot-path serialization where configuration overhead matters.
license: MIT
metadata:
  displayName: "Fluent Serializer"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "System.Text.Json Documentation"
    url: "https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/overview"
  - title: "JSON Serialization in .NET"
    url: "https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/how-to"
---

# Fluent Serializer

## Overview

The Fluent Serializer pattern provides a builder-style API for configuring JSON serialization behavior in .NET. Rather than scattering `JsonSerializerOptions` configuration across multiple files, a fluent serializer centralizes serialization settings into composable, readable chains. This pattern works on top of `System.Text.Json` or `Newtonsoft.Json`, enabling reusable serialization profiles that can be shared across microservices, tested in isolation, and swapped at runtime. It is especially valuable in projects with multiple serialization contexts (API responses, event payloads, file storage) that each need different settings.

## Basic Fluent Serializer

Build a fluent wrapper around `System.Text.Json` that chains configuration methods.

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

public class FluentJsonSerializer
{
    private readonly JsonSerializerOptions _options = new();

    public FluentJsonSerializer CamelCase()
    {
        _options.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
        return this;
    }

    public FluentJsonSerializer SnakeCase()
    {
        _options.PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower;
        return this;
    }

    public FluentJsonSerializer Indented()
    {
        _options.WriteIndented = true;
        return this;
    }

    public FluentJsonSerializer IgnoreNulls()
    {
        _options.DefaultIgnoreCondition =
            JsonIgnoreCondition.WhenWritingNull;
        return this;
    }

    public FluentJsonSerializer WithEnumStrings()
    {
        _options.Converters.Add(new JsonStringEnumConverter());
        return this;
    }

    public FluentJsonSerializer CaseInsensitiveRead()
    {
        _options.PropertyNameCaseInsensitive = true;
        return this;
    }

    public string Serialize<T>(T obj) =>
        JsonSerializer.Serialize(obj, _options);

    public T? Deserialize<T>(string json) =>
        JsonSerializer.Deserialize<T>(json, _options);

    public JsonSerializerOptions Build() =>
        new(_options); // return a copy
}

// Usage
string json = new FluentJsonSerializer()
    .CamelCase()
    .IgnoreNulls()
    .Indented()
    .WithEnumStrings()
    .Serialize(myObject);
```

## Generic Fluent Serializer with Type Customization

Add per-type configuration with property inclusion/exclusion.

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Text.Json.Serialization.Metadata;

public class FluentSerializer<T>
{
    private readonly JsonSerializerOptions _options = new();
    private readonly List<Action<JsonTypeInfo<T>>> _typeModifiers = new();

    public FluentSerializer<T> CamelCase()
    {
        _options.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
        return this;
    }

    public FluentSerializer<T> IgnoreNulls()
    {
        _options.DefaultIgnoreCondition =
            JsonIgnoreCondition.WhenWritingNull;
        return this;
    }

    public FluentSerializer<T> IgnoreProperty(string propertyName)
    {
        _typeModifiers.Add(typeInfo =>
        {
            var prop = typeInfo.Properties
                .FirstOrDefault(p => p.Name.Equals(
                    propertyName, StringComparison.OrdinalIgnoreCase));
            if (prop is not null)
                prop.ShouldSerialize = (_, _) => false;
        });
        return this;
    }

    public string Serialize(T obj)
    {
        _options.TypeInfoResolver = new DefaultJsonTypeInfoResolver
        {
            Modifiers =
            {
                typeInfo =>
                {
                    if (typeInfo.Type == typeof(T) &&
                        typeInfo is JsonTypeInfo<T> typed)
                    {
                        foreach (var modifier in _typeModifiers)
                            modifier(typed);
                    }
                }
            }
        };
        return JsonSerializer.Serialize(obj, _options);
    }
}

// Usage: serialize User but exclude Password property
string json = new FluentSerializer<User>()
    .CamelCase()
    .IgnoreNulls()
    .IgnoreProperty("Password")
    .Serialize(user);
```

## Serialization Profile Registry

Create named profiles for different serialization contexts.

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

public sealed class SerializationProfile
{
    public string Name { get; }
    public JsonSerializerOptions Options { get; }

    private SerializationProfile(string name, JsonSerializerOptions options)
    {
        Name = name;
        Options = options;
    }

    public static SerializationProfile Create(
        string name, Action<FluentJsonSerializer> configure)
    {
        var builder = new FluentJsonSerializer();
        configure(builder);
        return new SerializationProfile(name, builder.Build());
    }
}

public sealed class SerializationProfileRegistry
{
    private readonly Dictionary<string, SerializationProfile> _profiles = new();

    public SerializationProfileRegistry Register(
        string name, Action<FluentJsonSerializer> configure)
    {
        _profiles[name] = SerializationProfile.Create(name, configure);
        return this;
    }

    public JsonSerializerOptions GetOptions(string profileName)
    {
        if (!_profiles.TryGetValue(profileName, out var profile))
            throw new KeyNotFoundException(
                $"Serialization profile '{profileName}' not found.");
        return profile.Options;
    }

    public string Serialize<T>(string profileName, T obj) =>
        JsonSerializer.Serialize(obj, GetOptions(profileName));

    public T? Deserialize<T>(string profileName, string json) =>
        JsonSerializer.Deserialize<T>(json, GetOptions(profileName));
}

// Registration and usage
var registry = new SerializationProfileRegistry()
    .Register("api", cfg => cfg.CamelCase().IgnoreNulls().WithEnumStrings())
    .Register("storage", cfg => cfg.SnakeCase().Indented())
    .Register("events", cfg => cfg.CamelCase().IgnoreNulls());

string apiJson = registry.Serialize("api", order);
string storageJson = registry.Serialize("storage", order);
```

## Dependency Injection Integration

Register fluent serializer profiles with the ASP.NET Core DI container.

```csharp
using System.Text.Json;
using Microsoft.Extensions.DependencyInjection;

public static class FluentSerializerExtensions
{
    public static IServiceCollection AddFluentSerialization(
        this IServiceCollection services,
        Action<SerializationProfileRegistry> configure)
    {
        var registry = new SerializationProfileRegistry();
        configure(registry);
        services.AddSingleton(registry);
        return services;
    }
}

// Program.cs
builder.Services.AddFluentSerialization(registry =>
{
    registry
        .Register("api", cfg => cfg
            .CamelCase()
            .IgnoreNulls()
            .WithEnumStrings()
            .CaseInsensitiveRead())
        .Register("storage", cfg => cfg
            .SnakeCase()
            .Indented())
        .Register("messaging", cfg => cfg
            .CamelCase()
            .IgnoreNulls());
});

// Configure ASP.NET Core to use the API profile
builder.Services.Configure<Microsoft.AspNetCore.Http.Json.JsonOptions>(
    options =>
    {
        var registry = builder.Services
            .BuildServiceProvider()
            .GetRequiredService<SerializationProfileRegistry>();
        var apiOptions = registry.GetOptions("api");
        options.SerializerOptions.PropertyNamingPolicy =
            apiOptions.PropertyNamingPolicy;
        options.SerializerOptions.DefaultIgnoreCondition =
            apiOptions.DefaultIgnoreCondition;
    });
```

## Newtonsoft.Json Fluent Adapter

Wrap Newtonsoft.Json with the same fluent pattern for legacy codebases.

```csharp
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using Newtonsoft.Json.Serialization;

public class FluentNewtonsoftSerializer
{
    private readonly JsonSerializerSettings _settings = new();

    public FluentNewtonsoftSerializer CamelCase()
    {
        _settings.ContractResolver = new CamelCasePropertyNamesContractResolver();
        return this;
    }

    public FluentNewtonsoftSerializer IgnoreNulls()
    {
        _settings.NullValueHandling = NullValueHandling.Ignore;
        return this;
    }

    public FluentNewtonsoftSerializer Indented()
    {
        _settings.Formatting = Formatting.Indented;
        return this;
    }

    public FluentNewtonsoftSerializer WithEnumStrings()
    {
        _settings.Converters.Add(new StringEnumConverter());
        return this;
    }

    public FluentNewtonsoftSerializer WithDateFormat(string format)
    {
        _settings.DateFormatString = format;
        return this;
    }

    public string Serialize(object obj) =>
        JsonConvert.SerializeObject(obj, _settings);

    public T? Deserialize<T>(string json) =>
        JsonConvert.DeserializeObject<T>(json, _settings);
}
```

## Serializer Configuration Comparison

| Feature | System.Text.Json Fluent | Newtonsoft.Json Fluent | Raw JsonSerializerOptions |
|---------|------------------------|----------------------|--------------------------|
| Configuration style | Chained methods | Chained methods | Property assignment |
| Reusability | Profile registry | Profile registry | Manual sharing |
| Type customization | TypeInfoResolver | ContractResolver | Attributes |
| Performance | Native STJ speed | Slower (reflection) | Native STJ speed |
| Readability | High | High | Medium |
| Testability | Easy (isolated profiles) | Easy | Harder (global state) |

## Best Practices

1. **Return `this` from every configuration method**: every fluent method must return the builder instance to enable method chaining; break the chain only with terminal methods like `Serialize` or `Build`.
2. **Make `Build()` return a copy of the options**: return `new JsonSerializerOptions(options)` to prevent callers from mutating the shared configuration after building.
3. **Create named profiles for distinct serialization contexts**: use separate profiles for API responses, event payloads, and file storage rather than a single global `JsonSerializerOptions`.
4. **Register the profile registry as a singleton**: serialization profiles are immutable after registration and safe to share across all requests.
5. **Default to camelCase and null-ignoring for API profiles**: most REST API consumers expect camelCase property names and no null fields in JSON responses.
6. **Add `WithEnumStrings()` for APIs and `WithEnumNumbers()` for storage**: string enums improve API readability while numeric enums are more compact for database or event storage.
7. **Validate that profiles exist at startup**: call `GetOptions(name)` for each expected profile during application startup to fail fast instead of at runtime.
8. **Use `JsonSerializerOptions.Default` as the base**: start from the framework defaults and override only what you need, rather than building options from scratch.
9. **Avoid mutating options after first use**: `System.Text.Json` locks `JsonSerializerOptions` after first serialization; the fluent builder must complete configuration before the first `Serialize` call.
10. **Write unit tests for each profile**: verify that each named profile produces the expected JSON output (casing, null handling, date format) using snapshot testing or string assertions.
