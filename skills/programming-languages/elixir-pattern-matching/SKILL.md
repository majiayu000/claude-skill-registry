---
name: elixir-pattern-matching
description: Use when Elixir pattern matching including function clauses, case statements, with statements, and destructuring. Use for elegant control flow.
allowed-tools:
  - Bash
  - Read
---

# Elixir Pattern Matching

Master pattern matching in Elixir to write elegant, declarative code.
This skill covers function patterns, case statements, guards, and
destructuring across various data structures.

## Basic Pattern Matching

```elixir
# Simple assignment is pattern matching
x = 1
1 = x  # This works because x matches 1

# Pattern matching with tuples
{:ok, value} = {:ok, "success"}
value  # => "success"

# Will raise MatchError if patterns don't match
# {:error, _} = {:ok, "success"}  # MatchError

# Pin operator to use existing value
x = 1
^x = 1  # Works
# ^x = 2  # MatchError

# Ignore values with underscore
{:ok, _} = {:ok, "any value"}
{_, _, third} = {1, 2, 3}
third  # => 3
```

## Function Pattern Matching

```elixir
defmodule Calculator do
  def add(a, b), do: a + b

  def factorial(0), do: 1
  def factorial(n) when n > 0, do: n * factorial(n - 1)

  def describe_tuple({:ok, value}) do
    "Success: #{value}"
  end

  def describe_tuple({:error, reason}) do
    "Error: #{reason}"
  end

  def describe_tuple(_) do
    "Unknown tuple format"
  end
end

# Usage
Calculator.factorial(5)  # => 120
Calculator.describe_tuple({:ok, "done"})  # => "Success: done"
```

## Guards in Pattern Matching

```elixir
defmodule NumberChecker do
  def check(x) when is_integer(x) and x > 0 do
    "Positive integer"
  end

  def check(x) when is_integer(x) and x < 0 do
    "Negative integer"
  end

  def check(0), do: "Zero"

  def check(x) when is_float(x), do: "Float"

  def check(_), do: "Not a number"
end

defmodule Validator do
  def valid_email?(email) when is_binary(email) do
    String.contains?(email, "@")
  end

  def valid_email?(_), do: false

  def in_range?(num, min, max)
      when is_number(num) and num >= min and num <= max do
    true
  end

  def in_range?(_, _, _), do: false
end
```

## Case Statements

```elixir
defmodule ResponseHandler do
  def handle(response) do
    case response do
      {:ok, data} ->
        {:success, data}

      {:error, :not_found} ->
        {:failure, "Resource not found"}

      {:error, :timeout} ->
        {:failure, "Request timed out"}

      {:error, reason} ->
        {:failure, "Error: #{inspect(reason)}"}

      _ ->
        {:failure, "Unknown response"}
    end
  end

  def parse_number(str) do
    case Integer.parse(str) do
      {num, ""} -> {:ok, num}
      {num, _remainder} -> {:ok, num}
      :error -> {:error, "Not a valid number"}
    end
  end
end
```

## With Statement for Pipeline Pattern Matching

```elixir
defmodule UserService do
  def create_user(params) do
    with {:ok, email} <- validate_email(params["email"]),
         {:ok, password} <- validate_password(params["password"]),
         {:ok, user} <- insert_user(email, password),
         {:ok, _} <- send_welcome_email(user) do
      {:ok, user}
    else
      {:error, reason} -> {:error, reason}
      _ -> {:error, "Unknown error"}
    end
  end

  defp validate_email(email) when is_binary(email) do
    if String.contains?(email, "@") do
      {:ok, email}
    else
      {:error, "Invalid email"}
    end
  end

  defp validate_email(_), do: {:error, "Email required"}

  defp validate_password(pass) when is_binary(pass) do
    if String.length(pass) >= 8 do
      {:ok, pass}
    else
      {:error, "Password too short"}
    end
  end

  defp validate_password(_), do: {:error, "Password required"}

  defp insert_user(email, password) do
    {:ok, %{id: 1, email: email}}
  end

  defp send_welcome_email(_user) do
    {:ok, "sent"}
  end
end
```

## List Pattern Matching

```elixir
defmodule ListOps do
  def sum([]), do: 0
  def sum([head | tail]), do: head + sum(tail)

  def first([head | _tail]), do: head
  def first([]), do: nil

  def second([_, second | _]), do: second
  def second(_), do: nil

  def take_first_three([a, b, c | _rest]) do
    [a, b, c]
  end

  def take_first_three(list), do: list

  def split_at_middle(list) do
    middle = div(length(list), 2)
    {Enum.take(list, middle), Enum.drop(list, middle)}
  end
end
```

## Map Pattern Matching

```elixir
defmodule UserHandler do
  def greet(%{name: name, age: age}) do
    "Hello #{name}, you are #{age} years old"
  end

  def greet(%{name: name}) do
    "Hello #{name}"
  end

  def admin?(%{role: "admin"}), do: true
  def admin?(_), do: false

  def process_user(%{id: id, name: name} = user) do
    # Can use both the whole user and destructured parts
    IO.puts("Processing user #{id}: #{name}")
    user
  end

  def update_status(%{status: old_status} = user, new_status) do
    %{user | status: new_status}
  end
end

defmodule ConfigParser do
  def get_database_url(config) do
    case config do
      %{database: %{host: host, port: port, name: db}} ->
        "postgresql://#{host}:#{port}/#{db}"

      %{database: %{url: url}} ->
        url

      _ ->
        "postgresql://localhost:5432/default"
    end
  end
end
```

## Struct Pattern Matching

```elixir
defmodule User do
  defstruct [:id, :name, :email, role: "user"]
end

defmodule StructMatcher do
  def display_user(%User{name: name, email: email}) do
    "#{name} <#{email}>"
  end

  def is_admin?(%User{role: "admin"}), do: true
  def is_admin?(%User{}), do: false

  def update_email(%User{} = user, new_email) do
    %User{user | email: new_email}
  end
end

# Usage
user = %User{id: 1, name: "Alice", email: "alice@example.com"}
StructMatcher.display_user(user)
```

## Binary Pattern Matching

```elixir
defmodule BinaryParser do
  def parse_header(<<
        magic::binary-size(4),
        version::16,
        flags::8,
        rest::binary
      >>) do
    %{
      magic: magic,
      version: version,
      flags: flags,
      payload: rest
    }
  end

  def parse_ipv4(<<a, b, c, d>>) do
    "#{a}.#{b}.#{c}.#{d}"
  end

  def parse_utf8(<<codepoint::utf8, rest::binary>>) do
    {codepoint, rest}
  end

  def extract_first_byte(<<first::8, _::binary>>) do
    first
  end
end
```

## Cond for Multiple Conditions

```elixir
defmodule GradeCalculator do
  def letter_grade(score) do
    cond do
      score >= 90 -> "A"
      score >= 80 -> "B"
      score >= 70 -> "C"
      score >= 60 -> "D"
      true -> "F"
    end
  end

  def describe_number(n) do
    cond do
      n < 0 -> "negative"
      n == 0 -> "zero"
      n > 0 and n < 10 -> "small positive"
      n >= 10 and n < 100 -> "medium positive"
      true -> "large positive"
    end
  end
end
```

## Advanced Pattern Matching

```elixir
defmodule AdvancedMatcher do
  # Pattern matching in function arguments with multiple clauses
  def process([]), do: :empty
  def process([_]), do: :single
  def process([_, _]), do: :pair
  def process([h | t]) when length(t) > 1, do: :multiple

  # Pattern matching with maps and guards
  def format_response(%{status: status, body: body})
      when status >= 200 and status < 300 do
    {:ok, body}
  end

  def format_response(%{status: status, body: body})
      when status >= 400 do
    {:error, body}
  end

  # Nested pattern matching
  def extract_user_city(%{
        user: %{address: %{city: city}}
      }) do
    {:ok, city}
  end

  def extract_user_city(_), do: {:error, :no_city}

  # Pattern matching in for comprehensions
  def extract_ok_values(results) do
    for {:ok, value} <- results, do: value
  end
end
```

## When to Use This Skill

Use elixir-pattern-matching when you need to:

- Write expressive, declarative control flow
- Handle different data shapes with function clauses
- Extract values from complex data structures
- Validate data formats at function boundaries
- Implement clean error handling with tagged tuples
- Parse binary data or protocols
- Build robust, maintainable Elixir applications
- Leverage Elixir's functional programming strengths
- Create clear, self-documenting code

## Best Practices

- Use pattern matching instead of if/else when possible
- Order function clauses from most specific to most general
- Use guards to add constraints to patterns
- Leverage the pin operator when you need existing values
- Use underscore for values you don't care about
- Prefer pattern matching over accessor functions
- Use with statements for complex validation pipelines
- Keep patterns readable and not overly complex
- Document complex pattern matching logic
- Use tagged tuples {:ok, val} and {:error, reason} consistently

## Common Pitfalls

- Forgetting that = is pattern matching, not assignment
- Not ordering function clauses correctly (specific to general)
- Overusing guards when simpler patterns would work
- Not handling all possible pattern cases
- Creating MatchErrors by not handling edge cases
- Forgetting to use pin operator when needed
- Making patterns too complex and hard to read
- Not using with statement for multi-step validations
- Ignoring compiler warnings about unused variables
- Not leveraging pattern matching for cleaner code

## Resources

- [Elixir Pattern Matching Guide](https://elixir-lang.org/getting-started/pattern-matching.html)
- [Function Clauses Documentation](https://hexdocs.pm/elixir/patterns-and-guards.html)
- [Guards Reference](https://hexdocs.pm/elixir/patterns-and-guards.html#guards)
- [With Statement Guide](https://hexdocs.pm/elixir/Kernel.SpecialForms.html#with/1)
- [Binary Pattern Matching](https://elixir-lang.org/getting-started/binaries-strings-and-char-lists.html)
