---
name: "Turbo & Hotwire Patterns"
description: "Complete guide to Hotwire implementation including Turbo Drive, Turbo Frames, Turbo Streams, and Stimulus controllers in Rails applications. Use this skill when implementing real-time updates, partial page rendering, or JavaScript behaviors in Rails views."
---

# Turbo & Hotwire Patterns Skill

This skill provides comprehensive guidance for implementing Hotwire (Turbo + Stimulus) in Ruby on Rails applications.

## When to Use This Skill

- Implementing partial page updates
- Adding real-time features
- Creating Turbo Frames and Streams
- Writing Stimulus controllers
- Debugging Turbo-related issues

## External References

- **Turbo**: https://turbo.hotwired.dev/
- **Stimulus**: https://stimulus.hotwired.dev/

## Hotwire Stack Overview

```
Hotwire
├── Turbo
│   ├── Turbo Drive      — Full page navigation without reload
│   ├── Turbo Frames     — Partial page updates
│   └── Turbo Streams    — Real-time updates over WebSocket/HTTP
│
└── Stimulus             — Lightweight JavaScript controllers
```

## Turbo Drive

Automatically converts all link clicks and form submissions into AJAX requests.

### Disabling for Specific Links
```erb
<%# Skip Turbo Drive for this link %>
<%= link_to "External", "https://example.com", data: { turbo: false } %>

<%# Skip for form %>
<%= form_with model: @user, data: { turbo: false } do |f| %>
```

### Progress Bar
```css
/* Customize Turbo progress bar */
.turbo-progress-bar {
  background-color: #4f46e5;
  height: 3px;
}
```

## Turbo Frames

Partial page updates within a frame boundary.

### Basic Frame

```erb
<%# app/views/tasks/index.html.erb %>
<%= turbo_frame_tag "tasks_list" do %>
  <% @tasks.each do |task| %>
    <%= render task %>
  <% end %>
  
  <%= link_to "Load more", tasks_path(page: @next_page) %>
<% end %>
```

### Frame Navigation

```erb
<%# Links within frame navigate inside frame %>
<%= turbo_frame_tag dom_id(@task) do %>
  <h3><%= @task.title %></h3>
  <%= link_to "Edit", edit_task_path(@task) %>
<% end %>

<%# Edit form replaces frame content %>
<%# app/views/tasks/edit.html.erb %>
<%= turbo_frame_tag dom_id(@task) do %>
  <%= render "form", task: @task %>
<% end %>
```

### Breaking Out of Frame

```erb
<%# Target another frame %>
<%= link_to "Details", task_path(@task), data: { turbo_frame: "task_detail" } %>

<%# Target the whole page %>
<%= link_to "Full Page", task_path(@task), data: { turbo_frame: "_top" } %>
```

### Lazy Loading Frames

```erb
<%# Load content when frame becomes visible %>
<%= turbo_frame_tag "comments", 
                    src: task_comments_path(@task), 
                    loading: :lazy do %>
  <p>Loading comments...</p>
<% end %>
```

### Frame with Different Source

```erb
<%# Frame that loads from different URL %>
<%= turbo_frame_tag "sidebar",
                    src: sidebar_path,
                    target: "_top" do %>
  <p>Loading sidebar...</p>
<% end %>
```

## Turbo Streams

Real-time DOM updates via WebSocket or HTTP responses.

### Stream Actions

```erb
<%# Append to container %>
<%= turbo_stream.append "tasks" do %>
  <%= render @task %>
<% end %>

<%# Prepend to container %>
<%= turbo_stream.prepend "tasks" do %>
  <%= render @task %>
<% end %>

<%# Replace specific element %>
<%= turbo_stream.replace dom_id(@task) do %>
  <%= render @task %>
<% end %>

<%# Update contents (not replace element) %>
<%= turbo_stream.update "task_count" do %>
  <%= @tasks.count %>
<% end %>

<%# Remove element %>
<%= turbo_stream.remove dom_id(@task) %>

<%# Before/After %>
<%= turbo_stream.before dom_id(@task) do %>
  <div class="alert">Task updated!</div>
<% end %>

<%= turbo_stream.after dom_id(@task) do %>
  <div class="related">Related tasks...</div>
<% end %>
```

### Stream Response from Controller

```ruby
# app/controllers/tasks_controller.rb
class TasksController < ApplicationController
  def create
    @task = current_account.tasks.build(task_params)
    
    respond_to do |format|
      if @task.save
        format.turbo_stream  # Renders create.turbo_stream.erb
        format.html { redirect_to @task }
      else
        format.turbo_stream do
          render turbo_stream: turbo_stream.replace(
            "task_form",
            partial: "form",
            locals: { task: @task }
          )
        end
        format.html { render :new }
      end
    end
  end
  
  def destroy
    @task = current_account.tasks.find(params[:id])
    @task.destroy
    
    respond_to do |format|
      format.turbo_stream { render turbo_stream: turbo_stream.remove(dom_id(@task)) }
      format.html { redirect_to tasks_path }
    end
  end
end
```

```erb
<%# app/views/tasks/create.turbo_stream.erb %>
<%= turbo_stream.prepend "tasks" do %>
  <%= render @task %>
<% end %>

<%= turbo_stream.replace "task_form" do %>
  <%= render "form", task: Task.new %>
<% end %>

<%= turbo_stream.update "tasks_count" do %>
  <%= current_account.tasks.count %>
<% end %>
```

### Broadcast Streams (Real-time)

```ruby
# app/models/task.rb
class Task < ApplicationRecord
  after_create_commit -> { broadcast_prepend_to "tasks" }
  after_update_commit -> { broadcast_replace_to "tasks" }
  after_destroy_commit -> { broadcast_remove_to "tasks" }
  
  # Or with custom stream name
  after_create_commit -> { 
    broadcast_prepend_to [account, "tasks"],
                         target: "tasks_list",
                         partial: "tasks/task"
  }
end
```

```erb
<%# Subscribe to stream in view %>
<%= turbo_stream_from @account, "tasks" %>

<div id="tasks_list">
  <%= render @tasks %>
</div>
```

## Stimulus Controllers

Lightweight JavaScript behaviors.

### Basic Controller

```javascript
// app/javascript/controllers/hello_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  connect() {
    console.log("Hello controller connected!")
  }
  
  greet() {
    alert("Hello, Stimulus!")
  }
}
```

```erb
<div data-controller="hello">
  <button data-action="click->hello#greet">Greet</button>
</div>
```

### Targets

```javascript
// app/javascript/controllers/search_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "results", "count"]
  
  search() {
    const query = this.inputTarget.value
    
    fetch(`/search?q=${query}`)
      .then(response => response.text())
      .then(html => {
        this.resultsTarget.innerHTML = html
      })
  }
  
  clear() {
    this.inputTarget.value = ""
    this.resultsTarget.innerHTML = ""
  }
  
  // Check if target exists
  updateCount() {
    if (this.hasCountTarget) {
      this.countTarget.textContent = this.resultsTarget.children.length
    }
  }
}
```

```erb
<div data-controller="search">
  <input data-search-target="input" 
         data-action="input->search#search">
  
  <button data-action="click->search#clear">Clear</button>
  
  <span data-search-target="count"></span>
  
  <div data-search-target="results"></div>
</div>
```

### Values

```javascript
// app/javascript/controllers/countdown_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = {
    seconds: { type: Number, default: 60 },
    url: String,
    autoStart: { type: Boolean, default: false }
  }
  
  connect() {
    if (this.autoStartValue) {
      this.start()
    }
  }
  
  start() {
    this.remaining = this.secondsValue
    this.timer = setInterval(() => this.tick(), 1000)
  }
  
  tick() {
    if (this.remaining > 0) {
      this.remaining--
      this.element.textContent = this.remaining
    } else {
      this.finish()
    }
  }
  
  finish() {
    clearInterval(this.timer)
    if (this.hasUrlValue) {
      window.location.href = this.urlValue
    }
  }
  
  // Called when value changes
  secondsValueChanged() {
    this.remaining = this.secondsValue
  }
  
  disconnect() {
    clearInterval(this.timer)
  }
}
```

```erb
<div data-controller="countdown"
     data-countdown-seconds-value="30"
     data-countdown-url-value="/timeout"
     data-countdown-auto-start-value="true">
  30
</div>
```

### Actions

```javascript
// app/javascript/controllers/form_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["submit"]
  
  // Default action (no method specified)
  submit(event) {
    event.preventDefault()
    this.submitTarget.disabled = true
    // ... form submission logic
  }
  
  // With event options
  // data-action="keydown.enter->form#submit"
  // data-action="click->form#submit:prevent"
}
```

```erb
<form data-controller="form"
      data-action="submit->form#submit">
  
  <input data-action="keydown.enter->form#submit:prevent">
  
  <button data-form-target="submit"
          data-action="click->form#validate">
    Submit
  </button>
</form>
```

### Classes

```javascript
// app/javascript/controllers/dropdown_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static classes = ["open", "closed"]
  static targets = ["menu"]
  
  toggle() {
    if (this.menuTarget.classList.contains(this.openClass)) {
      this.close()
    } else {
      this.open()
    }
  }
  
  open() {
    this.menuTarget.classList.remove(this.closedClass)
    this.menuTarget.classList.add(this.openClass)
  }
  
  close() {
    this.menuTarget.classList.remove(this.openClass)
    this.menuTarget.classList.add(this.closedClass)
  }
}
```

```erb
<div data-controller="dropdown"
     data-dropdown-open-class="block"
     data-dropdown-closed-class="hidden">
  
  <button data-action="click->dropdown#toggle">Menu</button>
  
  <div data-dropdown-target="menu" class="hidden">
    Menu content
  </div>
</div>
```

### Outlets (Controller Communication)

```javascript
// app/javascript/controllers/modal_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static outlets = ["form"]
  
  open() {
    this.element.classList.add("open")
    
    // Call method on connected form controller
    if (this.hasFormOutlet) {
      this.formOutlet.reset()
    }
  }
  
  close() {
    this.element.classList.remove("open")
  }
}
```

```erb
<div data-controller="modal"
     data-modal-form-outlet="#task-form">
  
  <div id="task-form" data-controller="form">
    <!-- form content -->
  </div>
</div>
```

## Common Patterns

### Infinite Scroll

```erb
<%# View %>
<div data-controller="infinite-scroll"
     data-infinite-scroll-url-value="<%= tasks_path %>"
     data-infinite-scroll-page-value="1">
  
  <div id="tasks" data-infinite-scroll-target="container">
    <%= render @tasks %>
  </div>
  
  <div data-infinite-scroll-target="loading" class="hidden">
    Loading...
  </div>
</div>
```

```javascript
// app/javascript/controllers/infinite_scroll_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["container", "loading"]
  static values = { url: String, page: Number }
  
  connect() {
    this.observer = new IntersectionObserver(
      entries => this.handleIntersect(entries),
      { threshold: 0.1 }
    )
    this.observer.observe(this.loadingTarget)
  }
  
  handleIntersect(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        this.loadMore()
      }
    })
  }
  
  async loadMore() {
    this.loadingTarget.classList.remove("hidden")
    
    const response = await fetch(
      `${this.urlValue}?page=${this.pageValue + 1}`,
      { headers: { "Accept": "text/vnd.turbo-stream.html" } }
    )
    
    if (response.ok) {
      this.pageValue++
      const html = await response.text()
      Turbo.renderStreamMessage(html)
    }
    
    this.loadingTarget.classList.add("hidden")
  }
  
  disconnect() {
    this.observer.disconnect()
  }
}
```

### Auto-Submit Form

```erb
<%= form_with url: search_path, 
              method: :get,
              data: { 
                controller: "auto-submit",
                turbo_frame: "results"
              } do |f| %>
  
  <%= f.text_field :q, 
                   data: { 
                     action: "input->auto-submit#submit",
                     auto_submit_target: "input"
                   } %>
<% end %>

<%= turbo_frame_tag "results" do %>
  <%= render @results %>
<% end %>
```

```javascript
// app/javascript/controllers/auto_submit_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input"]
  
  submit() {
    clearTimeout(this.timeout)
    this.timeout = setTimeout(() => {
      this.element.requestSubmit()
    }, 300)
  }
}
```

### Flash Messages with Turbo

```erb
<%# app/views/layouts/_flash.html.erb %>
<div id="flash">
  <% flash.each do |type, message| %>
    <div class="flash flash-<%= type %>"
         data-controller="flash"
         data-flash-timeout-value="5000">
      <%= message %>
      <button data-action="click->flash#dismiss">×</button>
    </div>
  <% end %>
</div>
```

```javascript
// app/javascript/controllers/flash_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { timeout: { type: Number, default: 5000 } }
  
  connect() {
    this.timer = setTimeout(() => this.dismiss(), this.timeoutValue)
  }
  
  dismiss() {
    this.element.remove()
  }
  
  disconnect() {
    clearTimeout(this.timer)
  }
}
```

## Turbo 8 Modern Features

### Page Refresh (Turbo 8+)

**Morphing** - Update page without full reload, preserving scroll and focus:

```html
<!-- Enable morphing globally -->
<meta name="turbo-refresh-method" content="morph">

<!-- Or per-page -->
<meta name="turbo-refresh-method" content="replace">
```

```ruby
# Controller - trigger page refresh
class TasksController < ApplicationController
  def update
    @task.update(task_params)

    # Send refresh signal to clients
    respond_to do |format|
      format.html { redirect_to tasks_path }
      format.turbo_stream {
        render turbo_stream: turbo_stream.action(:refresh)
      }
    end
  end
end
```

### Morph Refresh

**Preserve elements during morph:**

```html
<!-- Element persists across morphs -->
<div id="video-player" data-turbo-permanent>
  <video src="movie.mp4" controls></video>
</div>

<!-- Input state persists -->
<input type="text" data-turbo-permanent>
```

### View Transitions API Integration

```css
/* Smooth transitions during Turbo navigation */
@view-transition {
  navigation: auto;
}

::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}

/* Custom transition for specific elements */
.task-card {
  view-transition-name: task-card;
}
```

## Turbo Native (Mobile Apps)

### Basic Setup

```swift
// iOS - SceneDelegate.swift
import Turbo

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?
    var navigationController = UINavigationController()

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = (scene as? UIWindowScene) else { return }

        window = UIWindow(windowScene: windowScene)
        window?.rootViewController = navigationController
        window?.makeKeyAndVisible()

        visit(url: URL(string: "https://example.com")!)
    }

    func visit(url: URL) {
        let viewController = VisitableViewController(url: url)
        navigationController.pushViewController(viewController, animated: true)
    }
}
```

```kotlin
// Android - MainActivity.kt
import dev.hotwire.turbo.session.Session
import dev.hotwire.turbo.visit.TurboVisitOptions

class MainActivity : AppCompatActivity(), TurboActivity {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        TurboSessionNavHostFragment.visit(
            url = "https://example.com",
            options = TurboVisitOptions(action = TurboVisitAction.ADVANCE)
        )
    }
}
```

### Native Bridge Patterns

```erb
<!-- app/views/tasks/show.html.erb -->
<% if turbo_native_app? %>
  <%= link_to "Share", "#", data: {
    turbo_frame: "_top",
    controller: "bridge",
    action: "click->bridge#share"
  } %>
<% end %>
```

```javascript
// app/javascript/controllers/bridge_controller.js
import { BridgeComponent } from "@hotwired/turbo-ios"

export default class extends BridgeComponent {
  share() {
    this.send("share", {
      title: "Task Title",
      url: window.location.href
    })
  }
}
```

## Form Validation with Turbo

### Client-Side Validation

```erb
<%= form_with model: @task,
              data: {
                controller: "form-validation",
                action: "turbo:submit-end->form-validation#handleResponse"
              } do |f| %>

  <%= f.text_field :title,
                   required: true,
                   minlength: 5,
                   data: {
                     form_validation_target: "field",
                     action: "blur->form-validation#validateField"
                   } %>
  <span data-form-validation-target="error" class="hidden text-red-500"></span>

  <%= f.submit "Save",
               data: { form_validation_target: "submit" } %>
<% end %>
```

```javascript
// app/javascript/controllers/form_validation_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["field", "error", "submit"]

  validateField(event) {
    const field = event.target
    const error = field.parentElement.querySelector('[data-form-validation-target="error"]')

    if (!field.validity.valid) {
      error.textContent = field.validationMessage
      error.classList.remove("hidden")
      field.classList.add("border-red-500")
    } else {
      error.classList.add("hidden")
      field.classList.remove("border-red-500")
    }
  }

  handleResponse(event) {
    const { success, fetchResponse } = event.detail

    if (!success && fetchResponse.response.status === 422) {
      // Server returned validation errors
      this.disableSubmit(false)
    }
  }

  disableSubmit(disabled) {
    this.submitTarget.disabled = disabled
  }
}
```

### Server-Side Validation with Turbo

```ruby
# app/controllers/tasks_controller.rb
def create
  @task = Task.new(task_params)

  respond_to do |format|
    if @task.save
      format.turbo_stream {
        render turbo_stream: [
          turbo_stream.prepend("tasks", partial: "tasks/task", locals: { task: @task }),
          turbo_stream.replace("task_form", partial: "tasks/form", locals: { task: Task.new })
        ]
      }
    else
      format.turbo_stream {
        render turbo_stream: turbo_stream.replace(
          "task_form",
          partial: "tasks/form",
          locals: { task: @task }
        ), status: :unprocessable_entity
      }
    end
  end
end
```

```erb
<!-- app/views/tasks/_form.html.erb -->
<%= turbo_frame_tag "task_form" do %>
  <%= form_with model: task do |f| %>
    <div class="field">
      <%= f.label :title %>
      <%= f.text_field :title, class: task.errors[:title].any? ? 'error' : '' %>
      <% if task.errors[:title].any? %>
        <span class="error-message"><%= task.errors[:title].first %></span>
      <% end %>
    </div>

    <%= f.submit %>
  <% end %>
<% end %>
```

## Error Handling Patterns

### Turbo Stream Error Responses

```ruby
# app/controllers/concerns/turbo_streamable_errors.rb
module TurboStreamableErrors
  extend ActiveSupport::Concern

  included do
    rescue_from ActiveRecord::RecordNotFound, with: :handle_not_found
    rescue_from StandardError, with: :handle_error
  end

  private

  def handle_not_found(exception)
    respond_to do |format|
      format.turbo_stream {
        render turbo_stream: turbo_stream.replace(
          "flash",
          partial: "shared/flash",
          locals: { message: "Record not found", type: "error" }
        ), status: :not_found
      }
      format.html { redirect_to root_path, alert: "Record not found" }
    end
  end

  def handle_error(exception)
    Rails.logger.error(exception.message)

    respond_to do |format|
      format.turbo_stream {
        render turbo_stream: turbo_stream.replace(
          "flash",
          partial: "shared/flash",
          locals: { message: "An error occurred", type: "error" }
        ), status: :internal_server_error
      }
      format.html { redirect_to root_path, alert: "An error occurred" }
    end
  end
end
```

### Handling Network Errors

```javascript
// app/javascript/application.js
document.addEventListener("turbo:fetch-request-error", (event) => {
  const { detail: { fetchResponse } } = event

  if (!fetchResponse || fetchResponse.response.status >= 500) {
    // Show offline/error UI
    document.getElementById("error-banner").classList.remove("hidden")
  }
})

document.addEventListener("turbo:frame-missing", (event) => {
  // Handle missing frame gracefully
  const frame = event.target
  frame.innerHTML = `
    <div class="alert alert-warning">
      Content could not be loaded. <a href="${frame.src}">Try again</a>
    </div>
  `
  event.preventDefault()
})
```

## Progressive Enhancement

### No-JS Fallbacks

```erb
<!-- Works without JavaScript -->
<%= form_with model: @task do |f| %>
  <!-- Form works with or without Turbo -->
  <%= f.text_field :title %>
  <%= f.submit %>
<% end %>

<!-- Link works without Turbo -->
<%= link_to "View", task_path(@task) %>

<!-- Progressive Turbo Frame -->
<turbo-frame id="comments" src="<%= task_comments_path(@task) %>">
  <!-- Fallback content shown during load and without JS -->
  <a href="<%= task_comments_path(@task) %>">View comments</a>
</turbo-frame>
```

### Feature Detection

```javascript
// app/javascript/controllers/progressive_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  connect() {
    // Check for required features
    if ('IntersectionObserver' in window) {
      this.enableLazyLoading()
    }

    if ('fetch' in window) {
      this.enableAjaxFeatures()
    }
  }

  enableLazyLoading() {
    // Use IntersectionObserver for lazy loading
  }

  enableAjaxFeatures() {
    // Enable AJAX-dependent features
  }
}
```

## Accessibility with Turbo/Stimulus

### ARIA Live Regions

```erb
<!-- Announce dynamic updates to screen readers -->
<div id="tasks" aria-live="polite" aria-atomic="false">
  <%= render @tasks %>
</div>

<div id="flash"
     role="status"
     aria-live="assertive"
     aria-atomic="true">
  <!-- Flash messages announced immediately -->
</div>
```

### Keyboard Navigation

```javascript
// app/javascript/controllers/keyboard_nav_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["item"]

  connect() {
    this.currentIndex = 0
    this.itemTargets[this.currentIndex]?.focus()
  }

  next(event) {
    if (event.key === "ArrowDown") {
      event.preventDefault()
      this.currentIndex = Math.min(this.currentIndex + 1, this.itemTargets.length - 1)
      this.itemTargets[this.currentIndex].focus()
    }
  }

  previous(event) {
    if (event.key === "ArrowUp") {
      event.preventDefault()
      this.currentIndex = Math.max(this.currentIndex - 1, 0)
      this.itemTargets[this.currentIndex].focus()
    }
  }

  select(event) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault()
      event.target.click()
    }
  }
}
```

```erb
<div data-controller="keyboard-nav"
     tabindex="0"
     data-action="keydown->keyboard-nav#next keydown->keyboard-nav#previous">

  <% @items.each do |item| %>
    <div data-keyboard-nav-target="item"
         tabindex="0"
         role="button"
         aria-label="<%= item.title %>"
         data-action="keydown->keyboard-nav#select">
      <%= item.title %>
    </div>
  <% end %>
</div>
```

### Focus Management

```javascript
// app/javascript/controllers/modal_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["dialog", "closeButton"]

  open() {
    this.previousFocus = document.activeElement
    this.dialogTarget.showModal()
    this.closeButtonTarget.focus()

    // Trap focus within modal
    this.dialogTarget.addEventListener("keydown", this.trapFocus.bind(this))
  }

  close() {
    this.dialogTarget.close()
    this.previousFocus?.focus()
  }

  trapFocus(event) {
    if (event.key === "Tab") {
      const focusableElements = this.dialogTarget.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
      const firstElement = focusableElements[0]
      const lastElement = focusableElements[focusableElements.length - 1]

      if (event.shiftKey && document.activeElement === firstElement) {
        lastElement.focus()
        event.preventDefault()
      } else if (!event.shiftKey && document.activeElement === lastElement) {
        firstElement.focus()
        event.preventDefault()
      }
    }
  }
}
```

## Testing Turbo and Stimulus

### System Tests for Turbo

```ruby
# spec/system/tasks_spec.rb
require 'rails_helper'

RSpec.describe "Tasks", type: :system do
  before do
    driven_by(:selenium_chrome_headless)
  end

  it "creates a task with Turbo" do
    visit tasks_path

    within "#task_form" do
      fill_in "Title", with: "New Task"
      click_button "Create"
    end

    # Verify Turbo update without page reload
    expect(page).to have_content("New Task")
    expect(page).to have_current_path(tasks_path) # No redirect
    expect(page).to have_selector("#task_form input[value='']") # Form reset
  end

  it "updates task via Turbo Stream" do
    task = create(:task, title: "Old Title")
    visit tasks_path

    within "##{dom_id(task)}" do
      click_link "Edit"
      fill_in "Title", with: "New Title"
      click_button "Update"
    end

    # Frame updated in place
    within "##{dom_id(task)}" do
      expect(page).to have_content("New Title")
      expect(page).not_to have_field("Title")
    end
  end

  it "handles validation errors with Turbo" do
    visit tasks_path

    within "#task_form" do
      fill_in "Title", with: "" # Invalid
      click_button "Create"
    end

    expect(page).to have_content("can't be blank")
    expect(page).to have_selector("#task_form") # Form still visible
  end
end
```

### Testing Stimulus Controllers

```javascript
// spec/javascript/controllers/search_controller.test.js
import { Application } from "@hotwired/stimulus"
import SearchController from "controllers/search_controller"

describe("SearchController", () => {
  let application
  let controller

  beforeEach(() => {
    document.body.innerHTML = `
      <div data-controller="search">
        <input data-search-target="input" type="text">
        <div data-search-target="results"></div>
      </div>
    `

    application = Application.start()
    application.register("search", SearchController)
    controller = application.getControllerForElementAndIdentifier(
      document.querySelector('[data-controller="search"]'),
      "search"
    )
  })

  afterEach(() => {
    application.stop()
  })

  it("clears input and results", () => {
    controller.inputTarget.value = "test query"
    controller.resultsTarget.innerHTML = "<div>Results</div>"

    controller.clear()

    expect(controller.inputTarget.value).toBe("")
    expect(controller.resultsTarget.innerHTML).toBe("")
  })

  it("searches when input changes", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve("<div>Search results</div>")
      })
    )

    controller.inputTarget.value = "rails"
    await controller.search()

    expect(global.fetch).toHaveBeenCalledWith("/search?q=rails")
    expect(controller.resultsTarget.innerHTML).toContain("Search results")
  })
})
```

## Debouncing and Throttling

### Debounce Pattern

```javascript
// app/javascript/controllers/debounced_search_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { delay: { type: Number, default: 300 } }
  static targets = ["input", "results"]

  search() {
    clearTimeout(this.timeout)

    this.timeout = setTimeout(() => {
      this.performSearch()
    }, this.delayValue)
  }

  async performSearch() {
    const query = this.inputTarget.value

    if (query.length < 2) return

    const response = await fetch(`/search?q=${encodeURIComponent(query)}`)
    const html = await response.text()
    this.resultsTarget.innerHTML = html
  }

  disconnect() {
    clearTimeout(this.timeout)
  }
}
```

### Throttle Pattern

```javascript
// app/javascript/controllers/scroll_tracking_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { interval: { type: Number, default: 200 } }

  connect() {
    this.lastRun = 0
    this.element.addEventListener("scroll", this.handleScroll.bind(this))
  }

  handleScroll() {
    const now = Date.now()

    if (now - this.lastRun >= this.intervalValue) {
      this.track()
      this.lastRun = now
    }
  }

  track() {
    const scrollPercentage = (this.element.scrollTop / this.element.scrollHeight) * 100
    console.log(`Scrolled ${scrollPercentage}%`)

    // Send analytics, etc.
  }
}
```

## Stimulus Components Integration

```javascript
// Using stimulus-components library
import { Application } from "@hotwired/stimulus"
import Dropdown from "@stimulus-components/dropdown"
import Notification from "@stimulus-components/notification"
import Popover from "@stimulus-components/popover"

const application = Application.start()
application.register("dropdown", Dropdown)
application.register("notification", Notification)
application.register("popover", Popover)
```

```erb
<!-- Dropdown component -->
<div data-controller="dropdown">
  <button data-action="dropdown#toggle">Menu</button>
  <div data-dropdown-target="menu">
    <a href="/profile">Profile</a>
    <a href="/settings">Settings</a>
  </div>
</div>

<!-- Notification component -->
<div data-controller="notification"
     data-notification-delay-value="5000"
     data-notification-remove-after-value="true">
  <p>Your task was created successfully!</p>
  <button data-action="notification#hide">×</button>
</div>

<!-- Popover component -->
<div data-controller="popover"
     data-popover-translate-x="-50%"
     data-popover-translate-y="8">
  <button data-action="popover#toggle">Show Info</button>
  <div data-popover-target="card" class="hidden">
    Popover content
  </div>
</div>
```

## Debugging

### Turbo Events

```javascript
// Listen to Turbo events for debugging
document.addEventListener("turbo:before-fetch-request", (event) => {
  console.log("Turbo request:", event.detail.url)
})

document.addEventListener("turbo:frame-missing", (event) => {
  console.log("Frame missing:", event.target.id)
})

// Log all Turbo events
[
  "turbo:click",
  "turbo:before-visit",
  "turbo:visit",
  "turbo:before-fetch-request",
  "turbo:before-fetch-response",
  "turbo:submit-start",
  "turbo:submit-end",
  "turbo:before-stream-render",
  "turbo:before-frame-render",
  "turbo:frame-render",
  "turbo:frame-load",
  "turbo:load"
].forEach(event => {
  document.addEventListener(event, (e) => console.log(event, e.detail))
})
```

### Common Issues

1. **Frame not updating**: Check frame IDs match between source and target
2. **Streams not working**: Verify `turbo_stream_from` subscription
3. **Actions not firing**: Check data-action syntax and controller registration
4. **Morphing issues**: Use `data-turbo-permanent` for persistent elements
5. **Focus loss**: Implement focus management in Stimulus controllers
6. **Screen reader issues**: Add proper ARIA attributes and live regions
