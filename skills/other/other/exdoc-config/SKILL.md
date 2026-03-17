---
name: exdoc-config
description: Configures ExDoc for Elixir projects including mix.exs setup, extras, groups, cheatsheets, and livebooks. Use when setting up or modifying ExDoc documentation generation.
---

# ExDoc Configuration

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Markdown, cheatsheets (.cheatmd), livebooks (.livemd) | [references/extras-formats.md](references/extras-formats.md) |
| Custom head/body tags, syntax highlighting, nesting, annotations | [references/advanced-config.md](references/advanced-config.md) |

## Dependency Setup

Add ExDoc to `mix.exs` deps:

```elixir
defp deps do
  [
    {:ex_doc, "~> 0.34", only: :dev, runtime: false}
  ]
end
```

## Project Configuration

Configure your `project/0` function in `mix.exs`:

```elixir
def project do
  [
    app: :weather_station,
    version: "0.1.0",
    elixir: "~> 1.17",
    start_permanent: Mix.env() == :prod,
    deps: deps(),

    # ExDoc
    name: "WeatherStation",
    source_url: "https://github.com/acme/weather_station",
    homepage_url: "https://acme.github.io/weather_station",
    docs: docs()
  ]
end
```

## The docs/0 Function

Define a private `docs/0` function to keep project config clean:

```elixir
defp docs do
  [
    main: "readme",
    logo: "priv/static/images/logo.png",
    output: "doc",
    formatters: ["html", "epub"],
    source_ref: "v#{@version}",
    extras: extras(),
    groups_for_modules: groups_for_modules(),
    groups_for_extras: groups_for_extras()
  ]
end
```

### Key Options

| Option | Default | Description |
|--------|---------|-------------|
| `main` | `"api-reference"` | Landing page module name or extra filename (without extension) |
| `logo` | `nil` | Path to logo image displayed in sidebar |
| `output` | `"doc"` | Output directory for generated docs |
| `formatters` | `["html"]` | List of output formats (`"html"`, `"epub"`) |
| `source_ref` | `"main"` | Git ref used for "View Source" links |
| `assets` | `nil` | Map of source directory to target directory for static assets |
| `deps` | `[]` | Links to dependency documentation |

### Setting the Landing Page

The `main` option controls what users see first:

```elixir
# Use the README as the landing page (most common)
docs: [main: "readme"]

# Use a specific module as the landing page
docs: [main: "WeatherStation"]

# Use a custom guide
docs: [main: "getting-started"]
```

The value matches the extra filename without its extension, or a module name.

## Extras

Extras are additional pages beyond the API reference. Add them as a list of file paths:

```elixir
defp extras do
  [
    "README.md",
    "CHANGELOG.md",
    "LICENSE.md",
    "guides/getting-started.md",
    "guides/configuration.md",
    "guides/deployment.md",
    "cheatsheets/query-syntax.cheatmd",
    "notebooks/data-pipeline.livemd"
  ]
end
```

### Controlling Extra Titles

By default, ExDoc uses the first `h1` heading as the title. Override with a keyword tuple:

```elixir
defp extras do
  [
    {"README.md", [title: "Overview"]},
    {"CHANGELOG.md", [title: "Changelog"]},
    "guides/getting-started.md"
  ]
end
```

### Ordering

Extras appear in the sidebar in the order listed. Put the most important pages first:

```elixir
defp extras do
  [
    "README.md",
    "guides/getting-started.md",
    "guides/architecture.md",
    "guides/deployment.md",
    "CHANGELOG.md"
  ]
end
```

## Grouping

### Grouping Modules

Organize modules into logical sections in the sidebar:

```elixir
defp groups_for_modules do
  [
    "Sensors": [
      WeatherStation.Sensor,
      WeatherStation.Sensor.Temperature,
      WeatherStation.Sensor.Humidity,
      WeatherStation.Sensor.Pressure
    ],
    "Data Processing": [
      WeatherStation.Pipeline,
      WeatherStation.Pipeline.Transform,
      WeatherStation.Pipeline.Aggregate
    ],
    "Storage": [
      WeatherStation.Repo,
      WeatherStation.Schema.Reading,
      WeatherStation.Schema.Station
    ]
  ]
end
```

Use regex to group by pattern:

```elixir
defp groups_for_modules do
  [
    "Sensors": [~r/Sensor/],
    "Schemas": [~r/Schema/],
    "Pipeline": [~r/Pipeline/]
  ]
end
```

Modules not matching any group appear under a default "Modules" heading.

### Grouping Functions

Group functions within a module using `groups_for_docs`:

```elixir
defp docs do
  [
    groups_for_docs: [
      "Lifecycle": &(&1[:section] == :lifecycle),
      "Queries": &(&1[:section] == :queries),
      "Mutations": &(&1[:section] == :mutations)
    ]
  ]
end
```

Tag functions in your module with `@doc` metadata:

```elixir
@doc section: :lifecycle
def start_link(opts), do: GenServer.start_link(__MODULE__, opts)

@doc section: :queries
def get_reading(station_id), do: Repo.get(Reading, station_id)
```

### Grouping Extras

Organize guides, cheatsheets, and notebooks in the sidebar:

```elixir
defp groups_for_extras do
  [
    "Guides": [
      "guides/getting-started.md",
      "guides/configuration.md",
      "guides/deployment.md"
    ],
    "Cheatsheets": [
      "cheatsheets/query-syntax.cheatmd",
      "cheatsheets/ecto-types.cheatmd"
    ],
    "Tutorials": [
      "notebooks/data-pipeline.livemd",
      "notebooks/sensor-setup.livemd"
    ]
  ]
end
```

Use glob patterns for convenience:

```elixir
defp groups_for_extras do
  [
    "Guides": ~r/guides\/.*/,
    "Cheatsheets": ~r/cheatsheets\/.*/,
    "Tutorials": ~r/notebooks\/.*/
  ]
end
```

## Dependency Doc Links

Link to documentation for your dependencies so ExDoc cross-references resolve:

```elixir
defp docs do
  [
    deps: [
      ecto: "https://hexdocs.pm/ecto",
      phoenix: "https://hexdocs.pm/phoenix",
      plug: "https://hexdocs.pm/plug"
    ]
  ]
end
```

This enables references like `t:Ecto.Schema.t/0` to link directly to the dependency docs.

## Generating Docs

```bash
# Generate HTML docs
mix docs

# Open in browser
open doc/index.html
```

## Complete mix.exs Example

```elixir
defmodule WeatherStation.MixProject do
  use Mix.Project

  @version "1.3.0"
  @source_url "https://github.com/acme/weather_station"

  def project do
    [
      app: :weather_station,
      version: @version,
      elixir: "~> 1.17",
      start_permanent: Mix.env() == :prod,
      deps: deps(),
      name: "WeatherStation",
      source_url: @source_url,
      homepage_url: "https://acme.github.io/weather_station",
      docs: docs()
    ]
  end

  defp docs do
    [
      main: "readme",
      logo: "priv/static/images/logo.png",
      source_ref: "v#{@version}",
      formatters: ["html"],
      extras: extras(),
      groups_for_modules: groups_for_modules(),
      groups_for_extras: groups_for_extras(),
      deps: [
        ecto: "https://hexdocs.pm/ecto",
        phoenix: "https://hexdocs.pm/phoenix"
      ]
    ]
  end

  defp extras do
    [
      "README.md",
      "CHANGELOG.md",
      "guides/getting-started.md",
      "guides/configuration.md",
      "guides/deployment.md",
      "cheatsheets/query-syntax.cheatmd",
      "notebooks/data-pipeline.livemd"
    ]
  end

  defp groups_for_modules do
    [
      "Sensors": [~r/Sensor/],
      "Data Processing": [~r/Pipeline/],
      "Storage": [~r/Schema|Repo/]
    ]
  end

  defp groups_for_extras do
    [
      "Guides": ~r/guides\/.*/,
      "Cheatsheets": ~r/cheatsheets\/.*/,
      "Tutorials": ~r/notebooks\/.*/
    ]
  end

  defp deps do
    [
      {:phoenix, "~> 1.7"},
      {:ecto_sql, "~> 3.12"},
      {:ex_doc, "~> 0.34", only: :dev, runtime: false}
    ]
  end
end
```

## When to Load References

- Setting up cheatsheets or livebooks as extras -> extras-formats.md
- Injecting custom CSS/JS, configuring syntax highlighting, or tuning module nesting -> advanced-config.md
