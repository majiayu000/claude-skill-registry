---
name: credo-checks
description: Use when understanding and fixing common Credo check issues for Elixir code quality and consistency.
allowed-tools: []
---

# Credo Checks

Understanding and fixing common Credo issues.

## Check Categories

### Consistency Checks

Ensure consistent code style across the project.

### Design Checks

Identify design issues and anti-patterns.

### Readability Checks

Improve code readability and maintainability.

### Refactoring Checks

Highlight refactoring opportunities.

### Warning Checks

Catch potential bugs and issues.

## Common Issues

### Module Documentation

```elixir
# Issue: Missing module documentation
defmodule MyModule do
end

# Fixed
@moduledoc """
This module handles user authentication.
"""
defmodule MyModule do
end
```

### Function Complexity

```elixir
# Issue: High cyclomatic complexity
def complex_function(x) do
  if x > 10 do
    if x < 20 do
      if rem(x, 2) == 0 do
        :even_mid
      else
        :odd_mid
      end
    else
      :high
    end
  else
    :low
  end
end

# Fixed: Extract to separate functions
def classify_number(x) do
  case {x > 10, x < 20, rem(x, 2) == 0} do
    {false, _, _} -> :low
    {true, false, _} -> :high
    {true, true, true} -> :even_mid
    {true, true, false} -> :odd_mid
  end
end
```

### Pipe Chain

```elixir
# Issue: Single pipe
list |> Enum.map(&(&1 * 2))

# Fixed
Enum.map(list, &(&1 * 2))
```

### Unused Variables

```elixir
# Issue
def process({:ok, result}, _context) do
  result
end

# Fixed: Prefix with underscore
def process({:ok, result}, _context) do
  result
end
```
