---
name: dotnet-json-polymorphic
description: Configures polymorphic JSON serialization with [JsonPolymorphic] and [JsonDerivedType] attributes
license: MIT
metadata:
  author: Im5tu
  version: "1.0"
  repositoryUrl: https://github.com/im5tu/dotnet-skills
allowed-tools: Bash(dotnet:*) Read Glob Grep AskUserQuestion
---

Configure polymorphic JSON serialization using `[JsonPolymorphic]` and `[JsonDerivedType]` attributes for type-safe inheritance hierarchies.

## When to Use

- Serializing inheritance hierarchies with System.Text.Json
- Adding type discriminators for polymorphic deserialization
- Preparing polymorphic types for AOT-compatible JSON source generation
- Replacing Newtonsoft.Json `TypeNameHandling` with modern attributes

## Requirements

- .NET 7 or higher

## Steps

1. **Ask scope**:
   - Ask user: "Apply to entire solution or specific project?"
   - If specific project, ask which project

2. **Search for existing `[JsonPolymorphic]` attributes**:
   - Detect existing project conventions
   - Note any `TypeDiscriminatorPropertyName` values found

3. **Extract discriminator conventions**:
   - Search for `TypeDiscriminatorPropertyName` in existing attributes
   - Record all unique discriminator property names found

4. **Find polymorphic candidates**:
   - Search for abstract classes with derived types
   - Search for interfaces with implementing classes used in serialization
   - Look for classes with virtual members that are inherited

5. **Ask about discriminator property name**:
   - If existing discriminators found, show them to user
   - Ask: "What discriminator property name? (Default: `$type`, Found: [list existing])"

6. **Check for consistency**:
   - If multiple different discriminators found in codebase
   - Ask: "Found multiple discriminators: [list]. Standardize to single value?"

7. **Apply attributes to base types**:
   ```csharp
   [JsonPolymorphic(TypeDiscriminatorPropertyName = "$type")]
   [JsonDerivedType(typeof(DerivedA), typeDiscriminator: "DerivedA")]
   [JsonDerivedType(typeof(DerivedB), typeDiscriminator: "DerivedB")]
   public abstract class BaseClass
   {
   }
   ```
   - Use full type name as discriminator value (e.g., `"WeatherForecastWithCity"`)

8. **Add using directive**:
   - Ensure `using System.Text.Json.Serialization;` is present

9. **Verify with build**:
   ```bash
   dotnet build
   ```

10. **Report results**:
    - List all base types configured
    - List all derived type mappings added
    - Confirm build status

## Example Conversion

**Before:**
```csharp
public abstract class Notification
{
    public string Message { get; set; }
}

public class EmailNotification : Notification
{
    public string EmailAddress { get; set; }
}

public class SmsNotification : Notification
{
    public string PhoneNumber { get; set; }
}
```

**After:**
```csharp
[JsonPolymorphic(TypeDiscriminatorPropertyName = "$type")]
[JsonDerivedType(typeof(EmailNotification), typeDiscriminator: "EmailNotification")]
[JsonDerivedType(typeof(SmsNotification), typeDiscriminator: "SmsNotification")]
public abstract class Notification
{
    public string Message { get; set; }
}

public class EmailNotification : Notification
{
    public string EmailAddress { get; set; }
}

public class SmsNotification : Notification
{
    public string PhoneNumber { get; set; }
}
```

**JSON Output:**
```json
{
  "$type": "EmailNotification",
  "message": "Hello",
  "emailAddress": "user@example.com"
}
```

## Notes

- **AOT Compatibility**: Metadata-based source generation is supported; fast-path source generation is NOT supported for polymorphic types
- **Serialization requirement**: Must serialize using the base type for polymorphism to work (e.g., `JsonSerializer.Serialize<Notification>(emailNotification)`)
- **Discriminator values**: String discriminators are recommended over integers for readability and forward compatibility
- **Nested hierarchies**: Each level in the hierarchy needs its own `[JsonPolymorphic]` attribute if it has derived types
- **Interface support**: Interfaces can also use `[JsonPolymorphic]` when they define the contract for serialization

## Documentation

- [System.Text.Json Polymorphism](https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/polymorphism)
