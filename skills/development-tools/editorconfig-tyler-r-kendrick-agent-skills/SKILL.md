---
name: editorconfig
description: >
  USE FOR: Configuring consistent C# coding styles, naming conventions, formatting rules,
  and Roslyn analyzer severity levels across editors and IDEs using .editorconfig files.
  DO NOT USE FOR: Runtime code behavior, NuGet package configuration, or MSBuild property settings
  that belong in Directory.Build.props.
license: MIT
metadata:
  displayName: EditorConfig for .NET
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "EditorConfig Official Website"
    url: "https://editorconfig.org/"
  - title: "EditorConfig Specification"
    url: "https://spec.editorconfig.org/"
  - title: "Code Style Rule Options in .NET"
    url: "https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/code-style-rule-options"
---

# EditorConfig for .NET

## Overview

EditorConfig is a file-format specification that defines coding styles and formatting rules enforced by editors, IDEs, and build tooling. In .NET projects the `.editorconfig` file controls whitespace, indentation, naming conventions, code-style preferences, and Roslyn diagnostic severity levels. When `EnforceCodeStyleInBuild` is enabled in `Directory.Build.props`, violations reported by `.editorconfig` rules are promoted to build-time warnings or errors, making the file a first-class part of the project system.

A root `.editorconfig` placed at the repository top with `root = true` prevents editors from inheriting settings from parent directories. Nested `.editorconfig` files in subdirectories can override specific rules for tests, generated code, or legacy projects.

## File Structure and Sections

Every `.editorconfig` begins with global settings, then adds per-glob overrides. Sections are declared with bracket-enclosed glob patterns.

```ini
# .editorconfig
root = true

# Global defaults for all files
[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true
max_line_length = 120

# C# source files
[*.{cs,csx}]
indent_size = 4

# XML project files
[*.{csproj,props,targets}]
indent_size = 2

# JSON and YAML configuration
[*.{json,yml,yaml}]
indent_size = 2

# Markdown allows trailing whitespace for line breaks
[*.md]
trim_trailing_whitespace = false

# Generated files - relaxed rules
[**/obj/**.cs]
generated_code = true
dotnet_analyzer_diagnostic.severity = none
```

## C# Code Style Rules

The `.editorconfig` controls expression-level preferences, pattern-matching style, null-checking, and `using` directive placement.

```ini
[*.cs]
# 'var' preferences
csharp_style_var_for_built_in_types = true:suggestion
csharp_style_var_when_type_is_apparent = true:suggestion
csharp_style_var_elsewhere = true:suggestion

# Expression-bodied members
csharp_style_expression_bodied_methods = when_on_single_line:suggestion
csharp_style_expression_bodied_constructors = false:suggestion
csharp_style_expression_bodied_properties = true:suggestion
csharp_style_expression_bodied_accessors = true:suggestion
csharp_style_expression_bodied_lambdas = true:silent
csharp_style_expression_bodied_local_functions = false:silent

# Pattern matching
csharp_style_pattern_matching_over_is_with_cast_check = true:warning
csharp_style_pattern_matching_over_as_with_null_check = true:warning
csharp_style_prefer_switch_expression = true:suggestion
csharp_style_prefer_pattern_matching = true:suggestion
csharp_style_prefer_not_pattern = true:suggestion
csharp_style_prefer_extended_property_pattern = true:suggestion

# Null checking
csharp_style_throw_expression = true:suggestion
csharp_style_conditional_delegate_call = true:suggestion
dotnet_style_coalesce_expression = true:warning
dotnet_style_null_propagation = true:warning
csharp_style_prefer_null_check_over_type_check = true:suggestion

# Using directives
csharp_using_directive_placement = outside_namespace:warning
dotnet_sort_system_directives_first = true
dotnet_separate_import_directive_groups = false

# Namespace declarations
csharp_style_namespace_declarations = file_scoped:warning

# Primary constructors
csharp_style_prefer_primary_constructors = true:suggestion
```

## C# Formatting Rules

Formatting rules control brace placement, spacing, and wrapping.

```ini
[*.cs]
# New-line preferences
csharp_new_line_before_open_brace = all
csharp_new_line_before_else = true
csharp_new_line_before_catch = true
csharp_new_line_before_finally = true
csharp_new_line_before_members_in_object_initializers = true
csharp_new_line_before_members_in_anonymous_types = true
csharp_new_line_between_query_expression_clauses = true

# Indentation
csharp_indent_case_contents = true
csharp_indent_switch_labels = true
csharp_indent_labels = flush_left
csharp_indent_block_contents = true
csharp_indent_braces = false

# Spacing
csharp_space_after_cast = false
csharp_space_after_keywords_in_control_flow_statements = true
csharp_space_between_parentheses = false
csharp_space_before_colon_in_inheritance_clause = true
csharp_space_after_colon_in_inheritance_clause = true
csharp_space_around_binary_operators = before_and_after

# Wrapping
csharp_preserve_single_line_statements = false
csharp_preserve_single_line_blocks = true
```

## Naming Conventions

Naming rules enforce PascalCase for public members, camelCase with underscore prefix for private fields, and interface prefix rules.

```ini
[*.cs]
# Symbol specifications
dotnet_naming_symbols.public_members.applicable_kinds = property, method, event, delegate
dotnet_naming_symbols.public_members.applicable_accessibilities = public, internal, protected, protected_internal

dotnet_naming_symbols.private_fields.applicable_kinds = field
dotnet_naming_symbols.private_fields.applicable_accessibilities = private, private_protected

dotnet_naming_symbols.interfaces.applicable_kinds = interface
dotnet_naming_symbols.interfaces.applicable_accessibilities = *

dotnet_naming_symbols.type_parameters.applicable_kinds = type_parameter
dotnet_naming_symbols.type_parameters.applicable_accessibilities = *

dotnet_naming_symbols.const_fields.applicable_kinds = field
dotnet_naming_symbols.const_fields.required_modifiers = const

dotnet_naming_symbols.async_methods.applicable_kinds = method
dotnet_naming_symbols.async_methods.required_modifiers = async

# Naming styles
dotnet_naming_style.pascal_case.capitalization = pascal_case
dotnet_naming_style.camel_case_underscore.capitalization = camel_case
dotnet_naming_style.camel_case_underscore.required_prefix = _
dotnet_naming_style.interface_prefix.capitalization = pascal_case
dotnet_naming_style.interface_prefix.required_prefix = I
dotnet_naming_style.type_parameter_prefix.capitalization = pascal_case
dotnet_naming_style.type_parameter_prefix.required_prefix = T
dotnet_naming_style.async_suffix.capitalization = pascal_case
dotnet_naming_style.async_suffix.required_suffix = Async

# Naming rules (ordered by priority)
dotnet_naming_rule.interfaces_must_begin_with_i.symbols = interfaces
dotnet_naming_rule.interfaces_must_begin_with_i.style = interface_prefix
dotnet_naming_rule.interfaces_must_begin_with_i.severity = error

dotnet_naming_rule.type_parameters_must_begin_with_t.symbols = type_parameters
dotnet_naming_rule.type_parameters_must_begin_with_t.style = type_parameter_prefix
dotnet_naming_rule.type_parameters_must_begin_with_t.severity = error

dotnet_naming_rule.private_fields_camel_case.symbols = private_fields
dotnet_naming_rule.private_fields_camel_case.style = camel_case_underscore
dotnet_naming_rule.private_fields_camel_case.severity = warning

dotnet_naming_rule.const_fields_pascal_case.symbols = const_fields
dotnet_naming_rule.const_fields_pascal_case.style = pascal_case
dotnet_naming_rule.const_fields_pascal_case.severity = warning

dotnet_naming_rule.async_methods_must_end_with_async.symbols = async_methods
dotnet_naming_rule.async_methods_must_end_with_async.style = async_suffix
dotnet_naming_rule.async_methods_must_end_with_async.severity = suggestion

dotnet_naming_rule.public_members_pascal_case.symbols = public_members
dotnet_naming_rule.public_members_pascal_case.style = pascal_case
dotnet_naming_rule.public_members_pascal_case.severity = warning
```

## Analyzer Severity Configuration

Control Roslyn analyzer diagnostic severity directly in `.editorconfig` instead of using `#pragma` directives or `.globalconfig`.

```ini
[*.cs]
# .NET analyzer defaults
dotnet_analyzer_diagnostic.category-Style.severity = warning
dotnet_analyzer_diagnostic.category-Design.severity = warning
dotnet_analyzer_diagnostic.category-Performance.severity = warning
dotnet_analyzer_diagnostic.category-Reliability.severity = warning
dotnet_analyzer_diagnostic.category-Security.severity = error

# Specific rule overrides
dotnet_diagnostic.CA1062.severity = warning      # Validate arguments of public methods
dotnet_diagnostic.CA1822.severity = suggestion    # Mark members as static
dotnet_diagnostic.CA2007.severity = none          # Do not directly await a Task (library-only)
dotnet_diagnostic.IDE0005.severity = warning      # Remove unnecessary usings
dotnet_diagnostic.IDE0055.severity = warning      # Fix formatting
dotnet_diagnostic.IDE0060.severity = warning      # Remove unused parameter
dotnet_diagnostic.IDE0090.severity = suggestion   # Simplify new expression
dotnet_diagnostic.CS8618.severity = warning       # Non-nullable field uninitialized

# Test projects - relax certain rules
[*Tests/**/*.cs]
dotnet_diagnostic.CA1707.severity = none          # Allow underscores in test method names
dotnet_diagnostic.CA1062.severity = none          # Test parameters do not need validation
dotnet_diagnostic.CA2007.severity = none
```

## Severity Levels Reference

| Severity     | Build Behavior                              | Editor Behavior                  |
|--------------|---------------------------------------------|----------------------------------|
| `error`      | Fails the build                             | Red squiggly underline           |
| `warning`    | Build warning (error with TreatWarningsAsErrors) | Green squiggly underline     |
| `suggestion` | Build info message                          | Gray dots under first two chars  |
| `silent`     | No build output                             | Refactoring available on demand  |
| `none`       | Rule completely disabled                    | No analysis performed            |

## Best Practices

1. **Place the root `.editorconfig` at the repository root with `root = true`** to prevent accidental inheritance from user-profile or machine-level `.editorconfig` files that exist outside your repository.

2. **Set `EnforceCodeStyleInBuild` to `true` in `Directory.Build.props`** so that code-style rules defined in `.editorconfig` are enforced during `dotnet build`, not only inside the IDE.

3. **Use severity level `warning` rather than `error` for style rules during initial adoption** to avoid blocking builds while the team adjusts; escalate to `error` once the codebase is clean.

4. **Create a separate `[*Tests/**/*.cs]` section that relaxes rules like CA1707 and CA1062** because test methods conventionally use underscores in names and test parameters do not require null-guards.

5. **Define naming rules in priority order with explicit severity levels** because `.editorconfig` naming rules are evaluated top-to-bottom and the first matching rule wins; place more specific rules (interfaces, type parameters) before general rules (public members).

6. **Pin `csharp_style_namespace_declarations = file_scoped:warning`** to enforce file-scoped namespaces across the codebase and eliminate unnecessary indentation in every source file.

7. **Add `generated_code = true` and `dotnet_analyzer_diagnostic.severity = none` for `obj` and auto-generated file globs** to prevent analyzers from reporting false positives on machine-generated code.

8. **Commit the `.editorconfig` to version control and review changes to it through pull requests** to ensure the entire team agrees on style changes before they are enforced.

9. **Use `dotnet_sort_system_directives_first = true` with `csharp_using_directive_placement = outside_namespace:warning`** for a consistent, predictable ordering of `using` directives across all files.

10. **Run `dotnet format` in CI as a verification step** after configuring `.editorconfig` to catch formatting drift and ensure every committed file conforms to the declared style rules.
