---
name: credo-custom-checks
description: Use when creating custom Credo checks for project-specific code quality rules and standards in Elixir.
allowed-tools: []
---

# Credo Custom Checks

Creating custom Credo checks for project-specific rules.

## Creating a Custom Check

```elixir
defmodule MyApp.Credo.Check.NoHardcodedSecrets do
  use Credo.Check,
    category: :warning,
    base_priority: :high,
    explanations: [
      check: """
      Detects hardcoded secrets in code.
      """
    ]

  @impl true
  def run(%SourceFile{} = source_file, params) do
    issue_meta = IssueMeta.for(source_file, params)

    Credo.Code.prewalk(source_file, &traverse(&1, &2, issue_meta))
  end

  defp traverse(
         {:@, _, [{:secret_key, _, [value]}]} = ast,
         issues,
         issue_meta
       )
       when is_binary(value) do
    new_issue = issue_for(issue_meta, value)
    {ast, [new_issue | issues]}
  end

  defp traverse(ast, issues, _issue_meta) do
    {ast, issues}
  end

  defp issue_for(issue_meta, value) do
    format_issue(
      issue_meta,
      message: "Hardcoded secret found: #{String.slice(value, 0..5)}...",
      trigger: value
    )
  end
end
```

## Using Custom Checks

```elixir
# .credo.exs
%{
  configs: [
    %{
      name: "default",
      requires: ["./lib/my_app/credo/check/*.ex"],
      checks: %{
        enabled: [
          {MyApp.Credo.Check.NoHardcodedSecrets, []}
        ]
      }
    }
  ]
}
```
