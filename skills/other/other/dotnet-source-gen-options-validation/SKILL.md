---
name: dotnet-source-gen-options-validation
description: Converts options validation to use the compile-time source generator. Use when the user wants AOT-compatible, reflection-free options validation.
license: MIT
metadata:
  author: Im5tu
  version: "1.0"
  repositoryUrl: https://github.com/im5tu/dotnet-skills
allowed-tools: Bash(dotnet:*) Read Glob Grep AskUserQuestion
---

Convert options validation to use the compile-time source generator, enabling AOT-compatible, reflection-free validation at startup.

## When to Use

- Preparing application for Native AOT compilation
- Eliminating reflection-based validation overhead
- Ensuring validation errors surface at compile time rather than runtime
- Migrating from `ValidateDataAnnotations()` to source-generated validation

## Steps

1. **Find options classes** with data annotations:
   - Search for classes using `[Required]`, `[Range]`, `[RegularExpression]`, `[MaxLength]`, `[MinLength]`, `[Length]`
   - These are typically in files matching `*Options.cs` or `*Settings.cs`

2. **Check existing validation setup**:
   - If class already has a corresponding `[OptionsValidator]` partial class, skip it
   - Note any existing `ValidateDataAnnotations()` calls for removal later

3. **For each options class**, create a partial validator class:
   ```csharp
   [OptionsValidator]
   public partial class Validate{OptionsClassName} : IValidateOptions<{OptionsClassName}>
   {
   }
   ```
   - Place the validator in the same namespace as the options class
   - The source generator will implement the validation logic at compile time

4. **Register the validator in DI**:
   ```csharp
   services.AddSingleton<IValidateOptions<MyOptions>, ValidateMyOptions>();
   ```
   - Replace any existing `ValidateDataAnnotations()` calls
   - Ensure `Microsoft.Extensions.Options` using directive is present

5. **Verify with build**:
   ```bash
   dotnet build
   ```

6. **If build fails**, check for:
   - Missing `partial` keyword on validator class
   - Unsupported validation attributes
   - Missing package reference to `Microsoft.Extensions.Options`

7. **Report results**:
   - List all validator classes created
   - List all DI registrations added
   - Confirm build status

## Supported Validation Attributes

- `[Required]` - Property must have a value
- `[Range]` - Numeric value within specified range
- `[RegularExpression]` - String matches regex pattern
- `[MaxLength]` - Maximum length for strings/collections
- `[MinLength]` - Minimum length for strings/collections
- `[Length]` - Exact or range length constraint

## Notes

- Requires .NET 8.0 or higher
- Requires `Microsoft.Extensions.Options` version 8.0 or higher
- `ValidateDataAnnotations()` is NOT needed and should be removed
- The `[OptionsValidator]` attribute triggers source generation
- Validation runs at startup when options are first resolved
- Unsupported attributes will produce compiler warnings
