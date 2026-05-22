---
name: rails-hotwire
description: Use when hotwire (Turbo and Stimulus) for building modern reactive Rails applications without complex JavaScript frameworks.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Rails Hotwire

Master Hotwire for building modern, reactive Rails applications using Turbo
and Stimulus without requiring heavy JavaScript frameworks.

## Overview

Hotwire (HTML Over The Wire) is a modern approach to building web applications
that sends HTML instead of JSON over the wire. It consists of Turbo (for
delivering server-rendered HTML) and Stimulus (for JavaScript sprinkles).

## Installation and Setup

### Installing Hotwire

```bash
# Add to Gemfile
bundle add turbo-rails stimulus-rails

# Install Turbo
rails turbo:install

# Install Stimulus
rails stimulus:install

# Install Redis for ActionCable (Turbo Streams)
bundle add redis

# Configure ActionCable
rails generate channel turbo_stream
```

### Configuration

```ruby
# config/cable.yml
development:
  adapter: redis
  url: redis://localhost:6379/1

production:
  adapter: redis
  url: <%= ENV.fetch("REDIS_URL") { "redis://localhost:6379/1" } %>
  channel_prefix: myapp_production

# config/routes.rb
Rails.application.routes.draw do
  mount ActionCable.server => '/cable'
end
```

## Core Patterns

### 1. Turbo Drive (Page Acceleration)

```ruby
# Turbo Drive is automatic, but you can customize behavior

# app/views/layouts/application.html.erb
<!DOCTYPE html>
<html>
  <head>
    <%= csrf_meta_tags %>
    <%= csp_meta_tag %>
    <%= turbo_refreshes_with method: :morph, scroll: :preserve %>
  </head>
  <body>
    <%= yield %>
  </body>
</html>

# Disable Turbo for specific links
<%= link_to "Legacy Page", legacy_path, data: { turbo: false } %>

# Disable Turbo for forms
<%= form_with url: upload_path, data: { turbo: false } do |f| %>
  <%= f.file_field :document %>
<% end %>

# Custom progress bar
<style>
  .turbo-progress-bar {
    background: linear-gradient(to right, #4ade80, #3b82f6);
  }
</style>
```

### 2. Turbo Frames (Lazy Loading & Decomposition)

```ruby
# app/views/posts/index.html.erb
<div id="posts">
  <% @posts.each do |post| %>
    <%= turbo_frame_tag dom_id(post) do %>
      <%= render post %>
    <% end %>
  <% end %>
</div>

# app/views/posts/_post.html.erb
<article>
  <h2><%= post.title %></h2>
  <p><%= post.body %></p>

  <%= link_to "Edit", edit_post_path(post) %>
  <%= link_to "Delete", post_path(post),
              data: { turbo_method: :delete,
                      turbo_confirm: "Are you sure?" } %>
</article>

# app/views/posts/edit.html.erb
<%= turbo_frame_tag dom_id(@post) do %>
  <%= form_with model: @post do |f| %>
    <%= f.text_field :title %>
    <%= f.text_area :body %>
    <%= f.submit %>
  <% end %>
<% end %>

# Lazy loading frames
<%= turbo_frame_tag "analytics", src: analytics_path, loading: :lazy do %>
  <p>Loading analytics...</p>
<% end %>

# Target different frames
<%= link_to "Show Post", post_path(post),
            data: { turbo_frame: "modal" } %>

# Break out of frame
<%= link_to "New Page", new_post_path,
            data: { turbo_frame: "_top" } %>
```

### 3. Turbo Streams (Real-time Updates)

```ruby
# app/controllers/posts_controller.rb
class PostsController < ApplicationController
  def create
    @post = Post.new(post_params)

    respond_to do |format|
      if @post.save
        format.turbo_stream
        format.html { redirect_to @post }
      else
        format.html { render :new, status: :unprocessable_entity }
      end
    end
  end

  def destroy
    @post = Post.find(params[:id])
    @post.destroy

    respond_to do |format|
      format.turbo_stream { render turbo_stream: turbo_stream.remove(@post) }
      format.html { redirect_to posts_path }
    end
  end
end

# app/views/posts/create.turbo_stream.erb
<%= turbo_stream.prepend "posts", partial: "posts/post",
                         locals: { post: @post } %>
<%= turbo_stream.update "new_post", "" %>
<%= turbo_stream.replace "flash",
    partial: "shared/flash",
    locals: { message: "Post created!" } %>

# Multiple Turbo Stream actions
<%= turbo_stream.append "notifications" do %>
  <div class="notification">New post created!</div>
<% end %>

<%= turbo_stream.update "post_count",
    Post.count %>

<%= turbo_stream.remove "loading_spinner" %>

<%= turbo_stream.replace dom_id(@post),
    partial: "posts/post",
    locals: { post: @post } %>
```

### 4. Broadcasting Updates

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  broadcasts_to ->(post) { [post.user, "posts"] }, inserts_by: :prepend

  # Or more explicit
  after_create_commit -> {
    broadcast_prepend_to "posts",
      partial: "posts/post",
      locals: { post: self },
      target: "posts"
  }

  after_update_commit -> {
    broadcast_replace_to "posts",
      partial: "posts/post",
      locals: { post: self },
      target: dom_id(self)
  }

  after_destroy_commit -> {
    broadcast_remove_to "posts", target: dom_id(self)
  }
end

# app/views/posts/index.html.erb
<%= turbo_stream_from "posts" %>

<div id="posts">
  <%= render @posts %>
</div>

# Broadcast to specific users
class Comment < ApplicationRecord
  belongs_to :post

  after_create_commit -> {
    broadcast_prepend_to [post.user, :comments],
      partial: "comments/comment",
      locals: { comment: self },
      target: "comments"
  }
end

# app/views/posts/show.html.erb
<%= turbo_stream_from current_user, :comments %>
```

### 5. Stimulus Controllers

```javascript
// app/javascript/controllers/clipboard_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["source", "button"]
  static values = {
    successMessage: String,
    errorMessage: String
  }

  copy(event) {
    event.preventDefault()

    navigator.clipboard.writeText(this.sourceTarget.value).then(
      () => this.showSuccess(),
      () => this.showError()
    )
  }

  showSuccess() {
    this.buttonTarget.textContent = this.successMessageValue || "Copied!"
    setTimeout(() => {
      this.buttonTarget.textContent = "Copy"
    }, 2000)
  }

  showError() {
    this.buttonTarget.textContent = this.errorMessageValue || "Failed!"
  }
}
```

```erb
<!-- app/views/posts/show.html.erb -->
<div data-controller="clipboard"
     data-clipboard-success-message-value="Copied to clipboard!">
  <input type="text"
         value="<%= @post.share_url %>"
         data-clipboard-target="source"
         readonly>
  <button data-clipboard-target="button"
          data-action="click->clipboard#copy">
    Copy
  </button>
</div>
```

### 6. Form Validation with Stimulus

```javascript
// app/javascript/controllers/form_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["email", "password", "submit"]
  static classes = ["error"]

  connect() {
    this.validateForm()
  }

  validateField(event) {
    const field = event.target
    const isValid = field.checkValidity()

    if (isValid) {
      field.classList.remove(this.errorClass)
    } else {
      field.classList.add(this.errorClass)
    }

    this.validateForm()
  }

  validateForm() {
    const isValid = this.element.checkValidity()
    this.submitTarget.disabled = !isValid
  }

  async submit(event) {
    event.preventDefault()

    if (!this.element.checkValidity()) {
      return
    }

    const formData = new FormData(this.element)
    const response = await fetch(this.element.action, {
      method: this.element.method,
      body: formData,
      headers: {
        "Accept": "text/vnd.turbo-stream.html"
      }
    })

    if (response.ok) {
      const html = await response.text()
      Turbo.renderStreamMessage(html)
    }
  }
}
```

```erb
<%= form_with model: @user,
    data: { controller: "form",
            form_error_class: "border-red-500" } do |f| %>

  <%= f.email_field :email,
      required: true,
      data: { form_target: "email",
              action: "blur->form#validateField" } %>

  <%= f.password_field :password,
      required: true,
      minlength: 8,
      data: { form_target: "password",
              action: "blur->form#validateField" } %>

  <%= f.submit "Sign Up",
      data: { form_target: "submit",
              action: "click->form#submit" } %>
<% end %>
```

### 7. Infinite Scroll

```javascript
// app/javascript/controllers/infinite_scroll_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["entries", "pagination"]
  static values = {
    url: String,
    page: Number
  }

  initialize() {
    this.scroll = this.scroll.bind(this)
  }

  connect() {
    this.createObserver()
  }

  disconnect() {
    this.observer.disconnect()
  }

  createObserver() {
    this.observer = new IntersectionObserver(
      entries => this.handleIntersect(entries),
      { threshold: 1.0 }
    )
    this.observer.observe(this.paginationTarget)
  }

  handleIntersect(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        this.loadMore()
      }
    })
  }

  async loadMore() {
    const url = this.paginationTarget.querySelector("a[rel='next']")?.href

    if (!url) return

    this.pageValue++

    const response = await fetch(url, {
      headers: {
        Accept: "text/vnd.turbo-stream.html"
      }
    })

    if (response.ok) {
      const html = await response.text()
      Turbo.renderStreamMessage(html)
    }
  }
}
```

```erb
<!-- app/views/posts/index.html.erb -->
<div data-controller="infinite-scroll">
  <div id="posts" data-infinite-scroll-target="entries">
    <%= render @posts %>
  </div>

  <div data-infinite-scroll-target="pagination">
    <%= paginate @posts %>
  </div>
</div>

<!-- app/views/posts/index.turbo_stream.erb -->
<%= turbo_stream.append "posts" do %>
  <%= render @posts %>
<% end %>

<%= turbo_stream.replace "pagination" do %>
  <%= paginate @posts %>
<% end %>
```

### 8. Modal Dialogs

```javascript
// app/javascript/controllers/modal_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["container", "backdrop"]

  connect() {
    document.body.classList.add("overflow-hidden")
  }

  disconnect() {
    document.body.classList.remove("overflow-hidden")
  }

  close(event) {
    if (event.target === this.backdropTarget ||
        event.currentTarget.dataset.closeModal === "true") {
      this.element.remove()
    }
  }

  closeWithKeyboard(event) {
    if (event.key === "Escape") {
      this.element.remove()
    }
  }
}
```

```erb
<!-- app/views/posts/_modal.html.erb -->
<div data-controller="modal"
     data-action="keyup@window->modal#closeWithKeyboard"
     class="fixed inset-0 z-50">

  <div data-modal-target="backdrop"
       data-action="click->modal#close"
       class="fixed inset-0 bg-black bg-opacity-50"></div>

  <div data-modal-target="container"
       class="fixed inset-0 flex items-center justify-center">
    <div class="bg-white rounded-lg p-6 max-w-lg">
      <%= turbo_frame_tag "modal_content" do %>
        <%= yield %>
      <% end %>

      <button data-close-modal="true"
              data-action="click->modal#close">
        Close
      </button>
    </div>
  </div>
</div>

<!-- Trigger modal -->
<%= link_to "Edit Post",
    edit_post_path(@post),
    data: { turbo_frame: "modal" } %>
```

### 9. Autosave with Stimulus

```javascript
// app/javascript/controllers/autosave_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["status"]
  static values = {
    delay: { type: Number, default: 1000 },
    url: String
  }

  connect() {
    this.timeout = null
    this.saving = false
  }

  save() {
    clearTimeout(this.timeout)

    this.timeout = setTimeout(() => {
      this.persist()
    }, this.delayValue)
  }

  async persist() {
    if (this.saving) return

    this.saving = true
    this.showStatus("Saving...")

    const formData = new FormData(this.element)

    try {
      const response = await fetch(this.urlValue, {
        method: "PATCH",
        body: formData,
        headers: {
          "X-CSRF-Token": document.querySelector("[name='csrf-token']").content,
          "Accept": "application/json"
        }
      })

      if (response.ok) {
        this.showStatus("Saved", "success")
      } else {
        this.showStatus("Error saving", "error")
      }
    } catch (error) {
      this.showStatus("Error saving", "error")
    } finally {
      this.saving = false
    }
  }

  showStatus(message, type = "info") {
    this.statusTarget.textContent = message
    this.statusTarget.className = `status-${type}`

    setTimeout(() => {
      this.statusTarget.textContent = ""
    }, 2000)
  }
}
```

```erb
<%= form_with model: @post,
    data: { controller: "autosave",
            autosave_url_value: post_path(@post),
            action: "input->autosave#save" } do |f| %>

  <div data-autosave-target="status"></div>

  <%= f.text_field :title %>
  <%= f.text_area :body %>
<% end %>
```

### 10. Search with Debouncing

```javascript
// app/javascript/controllers/search_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "results"]
  static values = {
    url: String,
    delay: { type: Number, default: 300 }
  }

  connect() {
    this.timeout = null
  }

  search() {
    clearTimeout(this.timeout)

    this.timeout = setTimeout(() => {
      this.performSearch()
    }, this.delayValue)
  }

  async performSearch() {
    const query = this.inputTarget.value

    if (query.length < 2) {
      this.resultsTarget.innerHTML = ""
      return
    }

    const url = new URL(this.urlValue)
    url.searchParams.set("q", query)

    const response = await fetch(url, {
      headers: {
        Accept: "text/vnd.turbo-stream.html"
      }
    })

    if (response.ok) {
      const html = await response.text()
      Turbo.renderStreamMessage(html)
    }
  }

  clear() {
    this.inputTarget.value = ""
    this.resultsTarget.innerHTML = ""
  }
}
```

```erb
<div data-controller="search"
     data-search-url-value="<%= search_posts_path %>">

  <input type="text"
         data-search-target="input"
         data-action="input->search#search"
         placeholder="Search posts...">

  <button data-action="click->search#clear">Clear</button>

  <div id="search-results" data-search-target="results"></div>
</div>
```

## Best Practices

1. **Use Turbo Frames for isolation** - Scope updates to specific parts
2. **Broadcast model changes** - Keep all clients synchronized
3. **Progressive enhancement** - Ensure functionality without JavaScript
4. **Lazy load frames** - Improve initial page load performance
5. **Use Stimulus for sprinkles** - Keep JavaScript minimal and focused
6. **Leverage Turbo Streams** - Update multiple parts of the page
7. **Handle errors gracefully** - Provide fallbacks for network issues
8. **Cache appropriately** - Use HTTP caching with Turbo
9. **Test real-time features** - Verify broadcasts work correctly
10. **Optimize database queries** - Prevent N+1 with includes/preload

## Common Pitfalls

1. **Over-using Turbo Frames** - Not everything needs to be a frame
2. **Missing CSRF tokens** - Forgetting tokens in AJAX requests
3. **Race conditions** - Not handling concurrent broadcasts
4. **Memory leaks** - Not disconnecting ActionCable subscriptions
5. **Flash message issues** - Flash persisting across Turbo requests
6. **Breaking browser history** - Improper Turbo navigation
7. **SEO concerns** - Not considering search engine crawlers
8. **Form state loss** - Losing unsaved data on navigation
9. **Accessibility issues** - Not managing focus and ARIA attributes
10. **Over-engineering** - Using Hotwire when simple HTML suffices

## When to Use

- Building modern Rails applications
- Creating real-time collaborative features
- Implementing live updates without polling
- Building single-page-like experiences
- Reducing JavaScript complexity
- Progressive enhancement scenarios
- Mobile-friendly responsive interfaces
- Admin dashboards with live data
- Chat and messaging applications
- Live notifications and feeds

## Resources

- [Hotwire Documentation](https://hotwired.dev/)
- [Turbo Handbook](https://turbo.hotwired.dev/handbook/introduction)
- [Stimulus Handbook](https://stimulus.hotwired.dev/handbook/introduction)
- [Turbo Rails Gem](https://github.com/hotwired/turbo-rails)
- [Stimulus Components](https://www.stimulus-components.com/)
- [GoRails Hotwire Tutorials](https://gorails.com/series/hotwire-rails)
