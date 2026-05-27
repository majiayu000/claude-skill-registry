---
name: dialyzer-configuration
description: Use when configuring Dialyzer for Erlang/Elixir type checking and static analysis.
allowed-tools: []
---

# Dialyzer Configuration

Dialyzer is a static analysis tool for Erlang and Elixir that identifies software discrepancies such as type errors, unreachable code, and unnecessary tests.

## Configuration Files

### dialyzer.ignore-warnings

```
# Ignore specific warnings
lib/my_module.ex:42:pattern_match_cov
```

### .dialyzer_ignore.exs

```elixir
[
  {"lib/generated_code.ex", :no_return},
  {~r/lib\/legacy\/.*/, :unknown_function}
]
```

### mix.exs Configuration

```elixir
def project do
  [
    app: :my_app,
    dialyzer: [
      plt_add_apps: [:mix, :ex_unit],
      plt_core_path: "priv/plts",
      plt_file: {:no_warn, "priv/plts/dialyzer.plt"},
      flags: [:error_handling, :underspecs, :unmatched_returns],
      ignore_warnings: ".dialyzer_ignore.exs",
      list_unused_filters: true
    ]
  ]
end
```

## Common Configuration Options

### PLT Management

- `plt_add_apps`: Additional applications to include in PLT
- `plt_core_path`: Directory for core PLT files
- `plt_file`: Custom PLT file location
- `plt_add_deps`: Include dependencies (`:app_tree`, `:apps_direct`, `:transitive`)

### Analysis Flags

- `:error_handling` - Check error handling
- `:underspecs` - Warn on under-specified functions
- `:unmatched_returns` - Warn on unmatched return values
- `:unknown` - Warn on unknown functions/types
- `:overspecs` - Warn on over-specified functions

### Filter Options

- `ignore_warnings`: File with warning patterns to ignore
- `list_unused_filters`: Show unused ignore patterns

## Best Practices

1. **Incremental PLT Building**: Use project-specific PLTs to speed up analysis
2. **Gradual Adoption**: Start with subset of checks, expand over time
3. **CI Integration**: Run Dialyzer in continuous integration
4. **Type Specs**: Add comprehensive @spec annotations
5. **Warning Management**: Document intentional ignores

## Common Patterns

### Conditional Analysis

```elixir
if Mix.env() in [:dev, :test] do
  {:dialyxir, "~> 1.4", only: [:dev, :test], runtime: false}
end
```

### Custom Check Script

```bash
#!/bin/bash
mix dialyzer --format github
```

### GitHub Actions Integration

```yaml
- name: Run Dialyzer
  run: mix dialyzer --format github
```
