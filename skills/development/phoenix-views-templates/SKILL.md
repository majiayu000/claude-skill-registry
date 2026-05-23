---
name: phoenix-views-templates
description: Render views and templates in Phoenix using HEEx templates, function components, slots, and assigns
allowed-tools: [Bash, Read]
---

# Phoenix Views and Templates

Phoenix uses HEEx (HTML+EEx) templates for rendering dynamic HTML content. HEEx provides compile-time validation, security through automatic escaping, and a component-based architecture. Views in Phoenix are modules that organize template rendering logic and house reusable function components.

## View Module Structure

Phoenix view modules use the `embed_templates` macro to load HEEx templates from a directory:

```elixir
defmodule HelloWeb.HelloHTML do
  use HelloWeb, :html

  embed_templates "hello_html/*"
end
```

This automatically creates functions for each `.html.heex` file in the `hello_html/` directory.

## HEEx Templates

### Basic Template Structure

HEEx templates combine HTML with embedded Elixir expressions:

```heex
<section>
  <h2>Hello World, from Phoenix!</h2>
</section>
```

### Interpolating Dynamic Content

Use `<%= ... %>` to interpolate Elixir expressions into HTML:

```heex
<section>
  <h2>Hello World, from <%= @messenger %>!</h2>
</section>
```

The `@` symbol accesses assigns passed from the controller.

### Multi-line Expressions

For expressions without output, omit the `=`:

```heex
<% # This is a comment %>
<% user_name = String.upcase(@user.name) %>
<p>Welcome, <%= user_name %>!</p>
```

## Working with Assigns

Assigns are key-value pairs passed from controllers to templates:

```elixir
# Controller
def show(conn, %{"messenger" => messenger}) do
  render(conn, :show, messenger: messenger, receiver: "Dweezil")
end
```

```heex
<!-- Template -->
<section>
  <h2>Hello <%= @receiver %>, from <%= @messenger %>!</h2>
</section>
```

All assigns are accessed with the `@` prefix in templates.

## Conditional Rendering

### Using if/else

HEEx supports conditional rendering with `if/else` blocks:

```heex
<%= if some_condition? do %>
  <p>Some condition is true for user: <%= @username %></p>
<% else %>
  <p>Some condition is false for user: <%= @username %></p>
<% end %>
```

### Using unless

For negative conditions:

```heex
<%= unless @user.premium do %>
  <div class="upgrade-banner">
    Upgrade to premium for more features!
  </div>
<% end %>
```

### Pattern Matching with case

For multiple conditions:

```heex
<%= case @status do %>
  <% :pending -> %>
    <span class="badge badge-warning">Pending</span>
  <% :approved -> %>
    <span class="badge badge-success">Approved</span>
  <% :rejected -> %>
    <span class="badge badge-danger">Rejected</span>
<% end %>
```

## Looping and Iteration

### For Comprehensions

Generate dynamic lists using `for`:

```heex
<table>
  <tr>
    <th>Number</th>
    <th>Power</th>
  </tr>
  <%= for number <- 1..10 do %>
    <tr>
      <td><%= number %></td>
      <td><%= number * number %></td>
    </tr>
  <% end %>
</table>
```

### Iterating Over Collections

Loop through lists or maps:

```heex
<ul>
  <%= for post <- @posts do %>
    <li>
      <h3><%= post.title %></h3>
      <p><%= post.excerpt %></p>
    </li>
  <% end %>
</ul>
```

### Shorthand :for Attribute

HEEx provides cleaner syntax for simple iterations:

```heex
<ul>
  <li :for={item <- @items}><%= item.name %></li>
</ul>
```

### Accessing Index

Get the iteration index with `Enum.with_index/2`:

```heex
<%= for {item, index} <- Enum.with_index(@items) do %>
  <div class="item-<%= index %>">
    <%= item.name %>
  </div>
<% end %>
```

## Function Components

Function components are reusable UI elements defined as Elixir functions that return HEEx templates.

### Defining Function Components

Use the `attr` macro to declare attributes and the `~H` sigil for the template:

```elixir
defmodule HelloWeb.HelloHTML do
  use HelloWeb, :html

  embed_templates "hello_html/*"

  attr :messenger, :string, required: true

  def greet(assigns) do
    ~H"""
    <h2>Hello World, from <%= @messenger %>!</h2>
    """
  end
end
```

### Using Function Components

Invoke components with the `<.component_name />` syntax:

```heex
<section>
  <.greet messenger={@messenger} />
</section>
```

### Optional Attributes with Defaults

Define optional attributes with default values:

```elixir
attr :messenger, :string, default: nil
attr :class, :string, default: "greeting"

def greet(assigns) do
  ~H"""
  <h2 class={@class}>
    Hello World<%= if @messenger, do: ", from #{@messenger}" %>!
  </h2>
  """
end
```

### Multiple Attribute Types

Components can accept various attribute types:

```elixir
attr :title, :string, required: true
attr :count, :integer, default: 0
attr :active, :boolean, default: false
attr :user, :map, required: true
attr :items, :list, default: []

def card(assigns) do
  ~H"""
  <div class={"card" <> if @active, do: " active", else: ""}>
    <h3><%= @title %></h3>
    <p>Count: <%= @count %></p>
    <p>User: <%= @user.name %></p>
    <ul>
      <li :for={item <- @items}><%= item %></li>
    </ul>
  </div>
  """
end
```

### Components with Computed Values

Use `assign/2` to compute values within components:

```elixir
attr :x, :integer, required: true
attr :y, :integer, required: true
attr :title, :string, required: true

def sum_component(assigns) do
  assigns = assign(assigns, sum: assigns.x + assigns.y)

  ~H"""
  <h1><%= @title %></h1>
  <p>Sum: <%= @sum %></p>
  """
end
```

## Slots

Slots allow components to accept blocks of content, enabling powerful composition patterns.

### Defining and Using Slots

Define a slot and render it:

```elixir
slot :inner_block, required: true

def card(assigns) do
  ~H"""
  <div class="card">
    <%= render_slot(@inner_block) %>
  </div>
  """
end
```

Use the component with content:

```heex
<.card>
  <h2>Card Title</h2>
  <p>Card content goes here</p>
</.card>
```

### Named Slots

Components can have multiple named slots:

```elixir
slot :header, required: true
slot :body, required: true
slot :footer

def panel(assigns) do
  ~H"""
  <div class="panel">
    <div class="panel-header">
      <%= render_slot(@header) %>
    </div>
    <div class="panel-body">
      <%= render_slot(@body) %>
    </div>
    <%= if @footer != [] do %>
      <div class="panel-footer">
        <%= render_slot(@footer) %>
      </div>
    <% end %>
  </div>
  """
end
```

Usage:

```heex
<.panel>
  <:header>
    <h2>Panel Title</h2>
  </:header>
  <:body>
    <p>Panel content</p>
  </:body>
  <:footer>
    <button>Close</button>
  </:footer>
</.panel>
```

### Slots with Attributes

Slots can accept attributes for more dynamic rendering:

```elixir
slot :item, required: true do
  attr :title, :string, required: true
  attr :highlighted, :boolean, default: false
end

def list(assigns) do
  ~H"""
  <ul>
    <%= for item <- @item do %>
      <li class={if item.highlighted, do: "highlight"}>
        <%= item.title %>: <%= render_slot(item) %>
      </li>
    <% end %>
  </ul>
  """
end
```

## Rendering Child Templates

### Rendering Other Templates

Include child templates within a parent:

```heex
<%= render("child_template.html", assigns) %>
```

### Rendering Components from Other Modules

Call components from different modules:

```heex
<MyApp.Components.button text="Click me" />
```

Or with aliasing:

```elixir
alias MyApp.Components

# In template:
<Components.button text="Click me" />
```

## Layout Templates

### Using Layouts

Layouts wrap rendered templates. Configure the layout in the controller:

```elixir
def controller do
  quote do
    use Phoenix.Controller,
      formats: [:html, :json],
      layouts: [html: HelloWeb.Layouts]
    ...
  end
end
```

### Root Layout

The root layout includes the `@inner_content` placeholder:

```heex
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>My App</title>
  </head>
  <body>
    <%= @inner_content %>
  </body>
</html>
```

### App Layout Component

Nest layouts using components:

```heex
<Layouts.app flash={@flash}>
  <section>
    <h2>Hello World, from <%= @messenger %>!</h2>
  </section>
</Layouts.app>
```

### Disabling Layouts

Render without a layout:

```elixir
def home(conn, _params) do
  render(conn, :home, layout: false)
end
```

## LiveView Integration

### Delegating to Phoenix Views

LiveView can delegate rendering to existing view modules:

```elixir
defmodule AppWeb.ThermostatLive do
  use Phoenix.LiveView

  def render(assigns) do
    Phoenix.View.render(AppWeb.PageView, "page.html", assigns)
  end
end
```

### Embedding LiveView in Templates

Render LiveView components within static templates:

```heex
<h1>Temperature Control</h1>
<%= live_render(@conn, AppWeb.ThermostatLive) %>
```

### Function Components in LiveView

Define and use function components in LiveView:

```elixir
def weather_greeting(assigns) do
  ~H"""
  <div title="My div" class={@class}>
    <p>Hello <%= @name %></p>
    <MyApp.Weather.city name="Kraków"/>
  </div>
  """
end
```

## Testing Views

### Testing View Rendering

Test views directly using `render_to_string/4`:

```elixir
defmodule HelloWeb.ErrorHTMLTest do
  use HelloWeb.ConnCase, async: true

  import Phoenix.Template

  test "renders 404.html" do
    assert render_to_string(HelloWeb.ErrorHTML, "404", "html", []) == "Not Found"
  end

  test "renders 500.html" do
    assert render_to_string(HelloWeb.ErrorHTML, "500", "html", []) == "Internal Server Error"
  end
end
```

### Testing Function Components

Test components in isolation:

```elixir
import Phoenix.LiveViewTest

test "renders greet component" do
  assigns = %{messenger: "Phoenix"}
  html = rendered_to_string(~H"""
  <HelloWeb.HelloHTML.greet messenger={@messenger} />
  """)
  assert html =~ "Hello World, from Phoenix!"
end
```

## When to Use This Skill

Use this skill when you need to:

1. Create dynamic HTML templates for Phoenix applications
2. Build reusable function components for consistent UI elements
3. Implement conditional rendering based on application state
4. Render lists and tables with dynamic data
5. Create complex layouts with nested components and slots
6. Integrate LiveView components with static templates
7. Test view rendering logic and component behavior
8. Build accessible and semantic HTML structures
9. Implement responsive designs with dynamic classes
10. Create forms with validation feedback
11. Display flash messages and user notifications
12. Render navigation menus and breadcrumbs
13. Build card-based layouts and dashboards
14. Implement pagination controls

## Best Practices

1. **Use function components** - Encapsulate reusable UI patterns in components
2. **Declare attributes explicitly** - Use `attr` macro for all component attributes
3. **Provide default values** - Make components flexible with sensible defaults
4. **Use semantic HTML** - Choose appropriate HTML elements for accessibility
5. **Leverage slots** - Use slots for flexible component composition
6. **Keep templates simple** - Move complex logic to controller or context
7. **Use :for shorthand** - Prefer `:for` attribute for simple iterations
8. **Avoid inline styles** - Use CSS classes for styling
9. **Test components** - Write tests for complex component logic
10. **Document components** - Add docstrings to explain component usage
11. **Use verified routes** - Always use `~p` sigil in templates
12. **Escape user content** - Let HEEx handle escaping automatically
13. **Optimize renders** - Minimize computation in template code
14. **Use descriptive names** - Name components and attributes clearly
15. **Follow conventions** - Stick to Phoenix naming patterns

## Common Pitfalls

1. **Putting logic in templates** - Complex business logic belongs in contexts, not views
2. **Not escaping HTML** - Using `raw/1` without sanitizing user input
3. **Deeply nested templates** - Creating hard-to-maintain template hierarchies
4. **Missing attribute declarations** - Not using `attr` macro for component attributes
5. **Overusing inline conditionals** - Making templates hard to read
6. **Not using components** - Repeating markup instead of extracting components
7. **Forgetting slot checks** - Not checking if optional slots are provided
8. **Mixing concerns** - Combining data fetching with presentation logic
9. **Large template files** - Creating monolithic templates instead of components
10. **Inconsistent formatting** - Not following HEEx formatting conventions
11. **Using EEx instead of HEEx** - Missing compile-time validation benefits
12. **Ignoring accessibility** - Not adding ARIA labels and semantic markup
13. **Hardcoding values** - Not using assigns for configurable content
14. **Not testing edge cases** - Missing nil checks and empty state handling
15. **Excessive nesting** - Creating deeply nested component trees

## Resources

- [Phoenix Components Guide](https://hexdocs.pm/phoenix/components.html)
- [Phoenix.Component Documentation](https://hexdocs.pm/phoenix_live_view/Phoenix.Component.html)
- [HEEx Template Engine](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.HTMLEngine.html)
- [Phoenix Templates Guide](https://hexdocs.pm/phoenix/templates.html)
- [Phoenix Views Documentation](https://hexdocs.pm/phoenix/views.html)
- [Phoenix LiveView Documentation](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html)
