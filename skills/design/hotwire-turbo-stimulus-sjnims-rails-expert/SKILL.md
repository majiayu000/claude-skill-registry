---
name: hotwire-turbo-stimulus
description: This skill should be used when the user asks about Hotwire, Turbo Drive,
  Turbo Frames, Turbo Streams, Stimulus controllers, frontend interactivity, server-rendered
  HTML updates, websocket updates, pro
---

---
name: hotwire-turbo-stimulus
description: This skill should be used when the user asks about Hotwire, Turbo Drive, Turbo Frames, Turbo Streams, Stimulus controllers, frontend interactivity, server-rendered HTML updates, websocket updates, progressive enhancement, data attributes, importing JavaScript modules, or building interactive UIs without React/Vue. Also use when discussing the "HTML over the wire" approach or NO BUILD philosophy. Examples:

<example>
Context: User wants to update part of a page without full reload
user: "How can I update just the product list without refreshing the entire page?"
assistant: "I'll show you Turbo Frames for partial page updates."
<commentary>
This relates to Turbo Frames for scoped page updates.
</commentary>
</example>

<example>
Context: User needs real-time updates
user: "How do I push updates to users when new comments are added?"
assistant: "Turbo Streams over WebSockets is perfect for this. Let me explain."
<commentary>
This involves Turbo Streams with Action Cable for real-time broadcasts.
</commentary>
</example>

<example>
Context: User wants JavaScript interactivity
user: "I need a dropdown menu that opens on click"
assistant: "This is a perfect use case for a Stimulus controller. Let me show you."
<commentary>
This relates to Stimulus for lightweight JavaScript interactions.
</commentary>
</example>
---

# Hotwire/Turbo/Stimulus: Modern Rails Frontend

## Overview

Hotwire (HTML Over The Wire) is Rails' answer to frontend complexity. Instead of shipping JSON to a heavy JavaScript framework, Hotwire delivers HTML directly from the server.

**Hotwire consists of:**
- **Turbo Drive**: Fast navigation without full page reloads
- **Turbo Frames**: Update specific page sections
- **Turbo Streams**: Real-time HTML updates via WebSockets or HTTP
- **Stimulus**: Lightweight JavaScript controllers for sprinkles of interactivity

Together, they provide rich, reactive UIs with minimal JavaScript and no build step.

## Philosophy

Hotwire reflects Rails 8's core principles:
- **NO BUILD**: No webpack, no complex toolchains
- **Server-rendered**: HTML comes from Rails, not JavaScript
- **Progressive enhancement**: Start with HTML, add JavaScript as needed
- **Minimal JavaScript**: Write only what browsers can't do
- **Integrated**: Works seamlessly with Rails conventions

Most applications need less JavaScript than you think. Hotwire proves it.

## Turbo Drive

### What It Does

Turbo Drive intercepts link clicks and form submissions, replacing full page loads with AJAX requests that update the page content.

**Without Turbo Drive:**
```
Click link → Browser requests page → Full page reload → JavaScript re-initializes
```

**With Turbo Drive:**
```
Click link → AJAX request → Replace <body> → Fast transition
```

Benefits:
- Instant navigation
- Preserved scroll position
- CSS/JS stay loaded
- Smooth transitions

### How It Works

Automatically enabled when you include Turbo:

```javascript
// app/javascript/application.js
import "@hotwired/turbo-rails"
```

Now all links and forms use Turbo Drive automatically:

```erb
<%= link_to "Products", products_path %>
<!-- Navigates via Turbo Drive -->

<%= form_with model: @product do |f| %>
  <!-- Submits via Turbo Drive -->
<% end %>
```

### Disabling Turbo Drive

For specific links/forms:

```erb
<%= link_to "External", "https://example.com", data: { turbo: false } %>

<%= form_with model: @product, data: { turbo: false } do |f| %>
  <!-- Regular form submission -->
<% end %>
```

### Turbo Drive Progress Bar

Built-in progress indicator for navigation:

```css
/* Customize progress bar */
.turbo-progress-bar {
  height: 5px;
  background-color: #0076ff;
}
```

## Turbo Frames

### What They Do

Turbo Frames let you update specific page sections without affecting the rest of the page.

**Traditional approach:**
```
Update product → Full page reload → Entire page re-renders
```

**With Turbo Frames:**
```
Update product → Only product frame updates → Rest of page untouched
```

### Basic Usage

```erb
<!-- app/views/products/index.html.erb -->
<h1>Products</h1>

<%= turbo_frame_tag "new_product" do %>
  <%= link_to "New Product", new_product_path %>
<% end %>

<div id="products">
  <%= render @products %>
</div>

<!-- app/views/products/new.html.erb -->
<%= turbo_frame_tag "new_product" do %>
  <h2>New Product</h2>
  <%= form_with model: @product do |f| %>
    <%= f.text_field :name %>
    <%= f.submit %>
  <% end %>
<% end %>
```

When clicking "New Product", only the `new_product` frame updates—the rest of the page stays.

### dom_id Helper

Rails provides `dom_id` for consistent frame IDs:

```erb
<%= turbo_frame_tag dom_id(@product) do %>
  <%= render @product %>
<% end %>
<!-- Generates: <turbo-frame id="product_123">...</turbo-frame> -->
```

### Frame Navigation

```erb
<!-- Clicking links inside frame navigates the frame -->
<%= turbo_frame_tag "products" do %>
  <% @products.each do |product| %>
    <%= link_to product.name, product_path(product) %>
    <!-- Navigates the frame, not the page -->
  <% end %>
<% end %>
```

### Breaking Out of Frames

Navigate the full page from within a frame:

```erb
<%= link_to "View All", products_path, data: { turbo_frame: "_top" } %>
<!-- data-turbo-frame="_top" navigates the whole page -->
```

### Lazy Loading Frames

Load content on demand:

```erb
<%= turbo_frame_tag "lazy_content", src: lazy_products_path do %>
  Loading...
<% end %>
<!-- Automatically loads when frame appears in viewport -->
```

See `references/turbo-frames.md` for advanced patterns.

## Turbo Streams

### What They Do

Turbo Streams deliver targeted HTML updates after form submissions or via WebSockets.

**Seven Stream Actions:**
- **append**: Add to bottom of target
- **prepend**: Add to top of target
- **replace**: Replace entire target
- **update**: Replace target's content (keeps the target element)
- **remove**: Delete target
- **before**: Insert before target
- **after**: Insert after target

### After Form Submission

```ruby
# app/controllers/products_controller.rb
def create
  @product = Product.new(product_params)

  respond_to do |format|
    if @product.save
      format.turbo_stream { render turbo_stream: turbo_stream.prepend("products", @product) }
      format.html { redirect_to @product }
    else
      format.turbo_stream { render turbo_stream: turbo_stream.replace(dom_id(@product), partial: "form", locals: { product: @product }) }
      format.html { render :new, status: :unprocessable_entity }
    end
  end
end
```

```erb
<!-- app/views/products/index.html.erb -->
<div id="products">
  <%= render @products %>
</div>

<%= turbo_frame_tag "new_product" do %>
  <%= render "form", product: @product %>
<% end %>
```

When form submits, new product prepends to #products list without page reload.

### Broadcast Updates (Real-Time)

Stream changes to all connected users:

```ruby
# app/models/product.rb
class Product < ApplicationRecord
  after_create_commit -> { broadcast_prepend_to "products", target: "products" }
  after_update_commit -> { broadcast_replace_to "products" }
  after_destroy_commit -> { broadcast_remove_to "products" }
end
```

```erb
<!-- app/views/products/index.html.erb -->
<%= turbo_stream_from "products" %>

<div id="products">
  <%= render @products %>
</div>
```

Now when any user creates/updates/deletes a product, all connected users see the change instantly.

### Multiple Stream Actions

```ruby
# app/views/products/create.turbo_stream.erb
<%= turbo_stream.prepend "products", @product %>
<%= turbo_stream.update "counter", Product.count %>
<%= turbo_stream.replace "flash", partial: "shared/flash" %>
```

See `references/turbo-streams.md` for broadcasting patterns.

## Stimulus

### What It Does

Stimulus is a modest JavaScript framework for adding behavior to HTML.

**Philosophy:**
- HTML is the source of truth
- Controllers connect to HTML via data attributes
- Small, focused controllers
- Progressive enhancement

### Basic Structure

```javascript
// app/javascript/controllers/dropdown_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["menu"]

  toggle() {
    this.menuTarget.classList.toggle("hidden")
  }
}
```

```erb
<!-- app/views/shared/_header.html.erb -->
<div data-controller="dropdown">
  <button data-action="click->dropdown#toggle">Menu</button>

  <nav data-dropdown-target="menu" class="hidden">
    <a href="/products">Products</a>
    <a href="/about">About</a>
  </nav>
</div>
```

### Data Attributes

Stimulus uses three data attributes:

1. **data-controller**: Connects element to Stimulus controller
2. **data-{controller}-target**: Marks element as a target
3. **data-action**: Connects event to controller method

### Targets

Reference elements in controllers:

```javascript
export default class extends Controller {
  static targets = ["input", "output", "button"]

  connect() {
    console.log(this.inputTarget)  // First matching element
    console.log(this.inputTargets) // All matching elements
    console.log(this.hasInputTarget) // Boolean check
  }
}
```

```erb
<div data-controller="example">
  <input data-example-target="input">
  <input data-example-target="input">
  <div data-example-target="output"></div>
  <button data-example-target="button">Click</button>
</div>
```

### Actions

Connect events to methods:

```erb
<!-- Default event (click for buttons/links, input for form fields) -->
<button data-action="dropdown#toggle">Toggle</button>

<!-- Explicit event -->
<input data-action="keyup->search#query">

<!-- Multiple actions -->
<form data-action="submit->form#submit ajax:success->form#success">

<!-- Action options -->
<button data-action="click->menu#open:prevent">
  <!-- :prevent calls preventDefault() -->
</button>
```

### Values

Pass data to controllers:

```javascript
export default class extends Controller {
  static values = {
    url: String,
    count: Number,
    active: Boolean
  }

  connect() {
    console.log(this.urlValue)
    console.log(this.countValue)
    console.log(this.activeValue)
  }

  urlValueChanged(value, previousValue) {
    // Called when value changes
  }
}
```

```erb
<div data-controller="example"
     data-example-url-value="<%= products_path %>"
     data-example-count-value="5"
     data-example-active-value="true">
</div>
```

See `references/stimulus-controllers.md` for controller patterns.

## Integration Patterns

### Turbo Frames + Stimulus

```erb
<div data-controller="auto-refresh" data-auto-refresh-interval-value="5000">
  <%= turbo_frame_tag "stats", src: stats_path do %>
    Loading...
  <% end %>
</div>
```

```javascript
// auto_refresh_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { interval: Number }
  static targets = ["frame"]

  connect() {
    this.startRefreshing()
  }

  disconnect() {
    this.stopRefreshing()
  }

  startRefreshing() {
    this.refreshTimer = setInterval(() => {
      this.element.querySelector('turbo-frame').reload()
    }, this.intervalValue)
  }

  stopRefreshing() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer)
    }
  }
}
```

### Inline Editing

```erb
<%= turbo_frame_tag dom_id(product) do %>
  <div data-controller="inline-edit">
    <span data-inline-edit-target="display">
      <%= product.name %>
    </span>
    <button data-action="inline-edit#edit">Edit</button>
  </div>
<% end %>
```

## Common Patterns

### Modal with Turbo Frame

```erb
<%= turbo_frame_tag "modal" %>

<%= link_to "New Product", new_product_path, data: { turbo_frame: "modal" } %>
```

Form renders inside modal frame.

### Infinite Scroll

```erb
<div data-controller="infinite-scroll" data-action="scroll->infinite-scroll#loadMore">
  <%= turbo_frame_tag "products", src: products_path(page: 1) %>
</div>
```

### Live Search

```erb
<%= form_with url: search_products_path, method: :get, data: { turbo_frame: "results", turbo_action: "advance" } do |f| %>
  <%= f.search_field :q, data: { action: "input->debounce#search" } %>
<% end %>

<%= turbo_frame_tag "results" do %>
  <!-- Search results render here -->
<% end %>
```

## Further Reading

For deeper exploration:

- **`references/turbo-frames.md`**: Complete Turbo Frames guide with patterns
- **`references/turbo-streams.md`**: Broadcasting and real-time updates
- **`references/stimulus-controllers.md`**: Building Stimulus controllers

For code examples (in `examples/`):

- **`autosave_controller.js`**: Auto-save form data
- **`character_counter_controller.js`**: Live character counting
- **`clipboard_controller.js`**: Copy to clipboard functionality
- **`confirm_controller.js`**: Confirmation dialogs
- **`dropdown_controller.js`**: Interactive dropdown menus
- **`form_controller.js`**: Form handling and validation
- **`infinite_scroll_controller.js`**: Infinite scroll pagination
- **`modal_controller.js`**: Modal dialogs with Stimulus
- **`nested_form_controller.js`**: Dynamic nested form fields
- **`remote_form_controller.js`**: AJAX form submissions
- **`search_controller.js`**: Real-time search filtering
- **`slideshow_controller.js`**: Image carousel/slideshow
- **`tabs_controller.js`**: Tab navigation
- **`toggle_controller.js`**: Toggle visibility patterns

## Summary

Hotwire provides:
- **Turbo Drive**: Fast navigation without full reloads
- **Turbo Frames**: Scoped page updates
- **Turbo Streams**: Real-time HTML over WebSockets
- **Stimulus**: Lightweight JavaScript controllers
- **NO BUILD**: No webpack, no complex tooling
- **Server-rendered**: HTML from Rails, not JSON APIs

Master Hotwire and build rich, interactive applications with minimal JavaScript.
