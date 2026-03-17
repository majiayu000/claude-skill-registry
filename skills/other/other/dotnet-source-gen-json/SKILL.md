---
name: dotnet-source-gen-json
description: Configures System.Text.Json source generation for AOT-compatible JSON serialization
license: MIT
metadata:
  author: Im5tu
  version: "1.0"
  repositoryUrl: https://github.com/im5tu/dotnet-skills
allowed-tools: Bash(dotnet:*) Read Glob Grep AskUserQuestion
---

Configure System.Text.Json source generation for AOT-compatible, reflection-free JSON serialization with compile-time type metadata.

## When to Use

- Preparing application for Native AOT compilation
- Eliminating reflection-based serialization overhead
- Improving startup performance by generating serialization code at compile time
- Ensuring JSON serialization errors surface at compile time

## Requirements

- .NET 8 or higher for full options support
- .NET 6+ for basic source generation

## Steps

1. **Invoke polymorphic skill first**:
   - Run `dotnet-json-polymorphic` skill to ensure polymorphic types are configured
   - This ensures `[JsonDerivedType]` attributes are in place before generating context

2. **Ask scope**:
   - Ask user: "Apply to entire solution or specific project?"
   - Filter to ASP.NET Core projects (those with web SDK or API endpoints)

3. **Scan for API endpoint types**:
   - Search for Minimal API patterns: `MapGet`, `MapPost`, `MapPut`, `MapDelete`, `MapPatch`
   - Extract request/response types from lambda parameters and return types

4. **Scan for controller types**:
   - Search for controller attributes: `[HttpGet]`, `[HttpPost]`, `[HttpPut]`, `[HttpDelete]`, `[HttpPatch]`
   - Extract parameter types and return types from action methods

5. **Find direct serialization calls**:
   - Search for `JsonSerializer.Serialize` and `JsonSerializer.Deserialize` calls
   - Extract type arguments from these calls

6. **Check for existing JsonSerializerContext**:
   - Search for classes inheriting from `JsonSerializerContext`
   - Note existing `[JsonSerializable]` types to avoid duplicates

7. **Ask about enum serialization**:
   - Ask user: "Enable enum-as-string converter? (Recommended: Yes)"

8. **Ask about property naming**:
   - Ask user: "Select property naming policy:"
     - CamelCase (Recommended)
     - SnakeCaseLower
     - SnakeCaseUpper
     - KebabCaseLower
     - KebabCaseUpper
     - None (preserve original casing)

9. **Ask about null value handling**:
   - Ask user: "Serialize null values? (Recommended: No)"
     - No - Omit null properties from output (smaller payloads)
     - Yes - Include null properties in output
   - If No: Add `DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull`

10. **Create JsonSerializerContext**:
    - File: `{ProjectName}JsonContext.cs` in project root (same level as Program.cs)
    - Class name: `{ProjectName}JsonContext`

11. **Add source generation options**:
    ```csharp
    [JsonSourceGenerationOptions(
        PropertyNamingPolicy = JsonKnownNamingPolicy.CamelCase,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull)]
    [JsonSerializable(typeof(WeatherForecast))]
    [JsonSerializable(typeof(List<WeatherForecast>))]
    public partial class MyApiJsonContext : JsonSerializerContext
    {
    }
    ```

12. **Include collection types**:
    - For each type `T`, also add `[JsonSerializable(typeof(List<T>))]`
    - Add `[JsonSerializable(typeof(T[]))]` if arrays are used

13. **Configure ASP.NET Core**:
    - Add to Program.cs:
    ```csharp
    builder.Services.ConfigureHttpJsonOptions(options =>
    {
        options.SerializerOptions.TypeInfoResolver = MyApiJsonContext.Default;
    });
    ```

14. **Verify with build**:
    ```bash
    dotnet build
    ```

15. **Report results**:
    - List the JsonSerializerContext file created
    - List all types added to [JsonSerializable]
    - Confirm ASP.NET Core integration added
    - Confirm build status

## Example Context

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

namespace MyApi;

[JsonSourceGenerationOptions(
    PropertyNamingPolicy = JsonKnownNamingPolicy.CamelCase,
    DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
    Converters = [typeof(JsonStringEnumConverter<Status>)])]
[JsonSerializable(typeof(WeatherForecast))]
[JsonSerializable(typeof(List<WeatherForecast>))]
[JsonSerializable(typeof(CreateOrderRequest))]
[JsonSerializable(typeof(OrderResponse))]
[JsonSerializable(typeof(List<OrderResponse>))]
[JsonSerializable(typeof(ErrorResponse))]
public partial class MyApiJsonContext : JsonSerializerContext
{
}
```

## ASP.NET Core Integration

**Program.cs:**
```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.TypeInfoResolver = MyApiJsonContext.Default;
});

var app = builder.Build();

app.MapGet("/weather", () => new WeatherForecast("Seattle", 72));
app.MapPost("/orders", (CreateOrderRequest request) => Results.Ok(new OrderResponse()));

app.Run();
```

## AOT Configuration

For full AOT compatibility, add to the `Directory.Build.props` file (preferred), or project file:

```xml
<PropertyGroup>
  <JsonSerializerIsReflectionEnabledByDefault>false</JsonSerializerIsReflectionEnabledByDefault>
</PropertyGroup>
```

This ensures compile-time errors if any type is missing from the context.

## Notes

- **Context naming**: Use `{ProjectName}JsonContext` for consistency
- **File location**: Place in project root alongside Program.cs
- **Collection types**: Always include `List<T>` and array types if used in APIs
- **Polymorphic types**: Run `dotnet-json-polymorphic` first; polymorphic types use metadata-based generation only
- **Enum handling**: `JsonStringEnumConverter<TEnum>` requires .NET 8+ for AOT support
- **Multiple contexts**: Can have multiple contexts; use `JsonTypeInfoResolver.Combine()` to merge them

## Documentation

- [System.Text.Json Source Generation](https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/source-generation)
