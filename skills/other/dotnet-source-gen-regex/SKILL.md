---
name: dotnet-source-gen-regex
description: Converts Regex instances to use the compile-time source generator. Use when the user wants to optimize regex performance or enable AOT compatibility.
license: MIT
metadata:
  author: Im5tu
  version: "1.0"
  repositoryUrl: https://github.com/im5tu/dotnet-skills
allowed-tools: Bash(dotnet:*) Read Glob Grep AskUserQuestion
---

# .NET Regex Source Generator

The regex source generator creates compile-time generated regex implementations that are:
- **AOT-compatible**: Works with Native AOT and trimming
- **Debuggable**: Step through the generated matching code
- **Performant**: No runtime compilation overhead

## When to Use

This skill applies when the user:
- Wants to optimize regex performance
- Needs AOT-compatible regex patterns
- Asks about `[GeneratedRegex]` attribute
- Mentions converting `new Regex(...)` to source-generated
- Discusses regex compilation or startup performance

## Workflow

1. **Find regex usages** in the codebase:
   - `new Regex(...)` constructor calls
   - `Regex.IsMatch()`, `Regex.Match()`, `Regex.Replace()` static method calls
   - Other static `Regex.*` methods with inline patterns

2. **For each regex with a compile-time known pattern**:
   - Ensure the containing class is `partial`
   - Create a partial method with `[GeneratedRegex]` attribute:
     ```csharp
     [GeneratedRegex("pattern", RegexOptions.IgnoreCase)]
     private static partial Regex MyRegex();
     ```
   - Name the method descriptively based on what the pattern matches

3. **Replace usages** to call the generated method:
   ```csharp
   // Before
   var regex = new Regex(@"\d+", RegexOptions.Compiled);
   if (regex.IsMatch(input)) { ... }

   // After
   if (MyNumberRegex().IsMatch(input)) { ... }

   [GeneratedRegex(@"\d+")]
   private static partial Regex MyNumberRegex();
   ```

4. **Verify** with `dotnet build`

5. **If build fails**, check:
   - Class is marked `partial`
   - Pattern is a compile-time constant
   - .NET version is 7 or higher

## Key Notes

| Note | Detail |
|------|--------|
| `RegexOptions.Compiled` | Ignored by source gen - remove it |
| .NET Version | Requires .NET 7+ |
| Caching | Generated method caches singleton internally |
| Timeout | Use `[GeneratedRegex("pattern", RegexOptions.None, 1000)]` for timeout (milliseconds) |

## Pattern Conversion Examples

**Instance with options:**
```csharp
// Before
private readonly Regex _emailRegex = new(@"^[\w-\.]+@[\w-]+\.\w+$", RegexOptions.Compiled | RegexOptions.IgnoreCase);

// After
[GeneratedRegex(@"^[\w-\.]+@[\w-]+\.\w+$", RegexOptions.IgnoreCase)]
private static partial Regex EmailRegex();
```

**Static method call:**
```csharp
// Before
if (Regex.IsMatch(input, @"^\d{3}-\d{4}$"))

// After
if (PhoneNumberRegex().IsMatch(input))

[GeneratedRegex(@"^\d{3}-\d{4}$")]
private static partial Regex PhoneNumberRegex();
```

## Error Handling

- **If pattern is not constant**: Cannot use source gen - leave as runtime regex
- **If class is not partial**: Add `partial` modifier to the class declaration
- **If build fails after conversion**: Check error messages for unsupported pattern features
