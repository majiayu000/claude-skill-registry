---
name: rails-viewcomponents
description: Specialized skill for building ViewComponents with Hotwire (Turbo & Stimulus). Use when creating reusable UI components, implementing frontend interactions, building Turbo Frames/Streams, or writing Stimulus controllers. Includes component testing with Lookbook.
---

# Rails ViewComponents & Frontend

Build modern, component-based UIs with ViewComponent, Turbo, and Stimulus.

## When to Use This Skill

- Creating ViewComponents
- Building Turbo Frames and Streams
- Writing Stimulus controllers
- Implementing custom confirmation modals
- Creating Lookbook previews
- Building form interactions
- Real-time updates with Turbo Streams
- Progressive enhancement with Stimulus

## Core Principle: Component-Based Architecture

**ALL UI components MUST be ViewComponents** - not partials.

### Why ViewComponents?

- ✓ Better encapsulation than partials
- ✓ Testable in isolation
- ✓ Object-oriented approach
- ✓ Type safety and contracts
- ✓ Performance benefits (compiled)
- ✓ IDE support

## Critical ViewComponent Rules

**1. Prefix Rails helpers with `helpers.`**

```erb
<%# CORRECT %>
<%= helpers.link_to "Home", root_path %>
<%= helpers.image_tag "logo.png" %>
<%= helpers.inline_svg_tag "icons/user.svg" %>

<%# WRONG %>
<%= link_to "Home", root_path %>
```

**Exception**: `t()` i18n helper does NOT need prefix:

```erb
<%# CORRECT %>
<%= t('.title') %>
```

**2. SVG Icons as Separate Files**

Store SVGs in `app/assets/images/icons/` and render with [`inline_svg`](https://github.com/jamesmartin/inline_svg) gem:

```erb
<%= helpers.inline_svg_tag "icons/user.svg", class: "w-5 h-5" %>
```

**NEVER inline SVG markup in Ruby code**.

## Quick Component Patterns

### Basic Component

```ruby
# app/components/button_component.rb
class ButtonComponent < ViewComponent::Base
  def initialize(text:, variant: :primary, **options)
    @text = text
    @variant = variant
    @options = options
  end
end
```

```erb
<%# app/components/button_component.html.erb %>
<button class="btn btn-<%= @variant %>" <%= html_attributes(@options) %>>
  <%= @text %>
</button>
```

### Component with Slots

```ruby
class CardComponent < ViewComponent::Base
  renders_one :header
  renders_one :footer
  renders_many :actions
end
```

```erb
<%= render CardComponent.new do |card| %>
  <% card.with_header do %>
    <h3>Title</h3>
  <% end %>

  <p>Body content</p>

  <% card.with_action do %>
    <%= helpers.link_to "Edit", edit_path %>
  <% end %>
<% end %>
```

### Component with Variants

```ruby
class BadgeComponent < ViewComponent::Base
  VARIANTS = {
    primary: "bg-blue-100 text-blue-800",
    success: "bg-green-100 text-green-800",
    danger: "bg-red-100 text-red-800"
  }.freeze

  def initialize(text:, variant: :primary)
    @text = text
    @variant = variant
  end

  def variant_classes
    VARIANTS[@variant]
  end
end
```

## Turbo Frames & Streams

### Turbo Frame (Edit in Place)

```erb
<%# index.html.erb %>
<%= turbo_frame_tag dom_id(article) do %>
  <h2><%= article.title %></h2>
  <%= link_to "Edit", edit_article_path(article) %>
<% end %>
```

```erb
<%# edit.html.erb %>
<%= turbo_frame_tag dom_id(@article) do %>
  <%= form_with model: @article do |f| %>
    <%= f.text_field :title %>
    <%= f.submit %>
  <% end %>
<% end %>
```

### Turbo Streams (Multiple Updates)

```ruby
# Controller
def create
  @article = Article.new(article_params)

  respond_to do |format|
    if @article.save
      format.turbo_stream do
        render turbo_stream: [
          turbo_stream.prepend("articles", partial: "article", locals: { article: @article }),
          turbo_stream.update("form", partial: "form", locals: { article: Article.new })
        ]
      end
    end
  end
end
```

## Stimulus Controllers

### Basic Controller

```javascript
// app/javascript/controllers/dropdown_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["menu"]
  static values = { open: Boolean }

  toggle() {
    this.openValue = !this.openValue
  }

  openValueChanged() {
    if (this.openValue) {
      this.menuTarget.classList.remove("hidden")
    } else {
      this.menuTarget.classList.add("hidden")
    }
  }
}
```

```erb
<div data-controller="dropdown">
  <button data-action="dropdown#toggle">Options</button>
  <div data-dropdown-target="menu" class="hidden">
    <a href="#">Edit</a>
  </div>
</div>
```

## Custom Confirmation Modals

**ALWAYS use custom modals instead of browser `confirm()`**

```javascript
// app/javascript/controllers/confirmation_modal_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["modal", "title", "message", "confirmButton"]

  show(options = {}) {
    this.titleTarget.textContent = options.title || "Confirm"
    this.messageTarget.textContent = options.message || "Are you sure?"
    this.modalTarget.classList.remove("hidden")
    this.onConfirm = options.onConfirm || (() => {})
  }

  confirm() {
    this.onConfirm()
    this.hide()
  }

  hide() {
    this.modalTarget.classList.add("hidden")
  }
}
```

## Lookbook Previews

Required for shared components:

```ruby
# spec/components/previews/button_component_preview.rb
class ButtonComponentPreview < ViewComponent::Preview
  def default
    render ButtonComponent.new(text: "Click me")
  end

  def primary
    render ButtonComponent.new(text: "Primary", variant: :primary)
  end

  def danger
    render ButtonComponent.new(text: "Delete", variant: :danger)
  end
end
```

Access at: `http://localhost:3000/lookbook`

## Testing Components

```ruby
RSpec.describe ButtonComponent, type: :component do
  it "renders button text" do
    render_inline(ButtonComponent.new(text: "Click me"))
    expect(page).to have_button("Click me")
  end

  it "applies variant classes" do
    render_inline(ButtonComponent.new(text: "Save", variant: :primary))
    expect(page).to have_css("button.btn-primary")
  end
end
```

## Tech Stack

- **ViewComponent** - Component framework
- **Lookbook** - Component documentation
- **Turbo** - SPA-like interactions
- **Stimulus** - JavaScript controllers
- **Tailwind CSS** - Styling (typical)
- **[inline_svg](https://github.com/jamesmartin/inline_svg)** - SVG rendering gem

## Reference Documentation

For comprehensive frontend patterns:
- Frontend guide: `frontend.md` (detailed examples and advanced patterns)
