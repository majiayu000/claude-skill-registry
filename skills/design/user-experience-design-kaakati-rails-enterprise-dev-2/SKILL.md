---
name: "User Experience Design"
description: "Comprehensive UX design patterns for Rails applications including responsive design, animations/transitions, dark mode, loading states, form UX, and performance optimization. Use this skill when implementing user-facing features requiring polished interactions and responsive layouts. Trigger keywords: UX, responsive, mobile-first, animation, transition, dark mode, loading, skeleton, progress, toast, form validation, performance, Core Web Vitals, user flow"
---

# User Experience Design Patterns

This skill provides production-ready UX patterns for Rails applications, covering responsive design, animations, dark mode, loading states, and performance optimization.

---

## When to Use This Skill

Invoke this skill when:

- Implementing **responsive layouts** with mobile-first approach
- Adding **animations and transitions** for micro-interactions
- Implementing **dark mode** support with TailAdmin
- Creating **loading states** (skeletons, progress indicators)
- Designing **form UX** (validation, multi-step, auto-save)
- Optimizing **performance** for Core Web Vitals
- Building **toast notifications** and feedback systems

---

## 1. Mobile-First Responsive Design

### 1.1 Breakpoint Strategy

Use Tailwind CSS breakpoints consistently:

```css
/* Tailwind Breakpoints (mobile-first) */
sm: 640px   /* Small devices (landscape phones) */
md: 768px   /* Medium devices (tablets) */
lg: 1024px  /* Large devices (laptops) */
xl: 1280px  /* Extra large devices (desktops) */
2xl: 1536px /* 2X large devices (large monitors) */
```

**Mobile-First Pattern**:

```erb
<%# Base styles = mobile, then layer up %>
<div class="
  p-4           <%# Mobile: 1rem padding %>
  sm:p-6        <%# Small: 1.5rem padding %>
  md:p-8        <%# Medium: 2rem padding %>
  lg:p-10       <%# Large: 2.5rem padding %>

  grid
  grid-cols-1   <%# Mobile: single column %>
  sm:grid-cols-2 <%# Small: two columns %>
  lg:grid-cols-3 <%# Large: three columns %>
  xl:grid-cols-4 <%# Extra large: four columns %>

  gap-4
  sm:gap-6
  lg:gap-8
">
  <%= yield %>
</div>
```

### 1.2 Touch Targets

Minimum touch target sizes for mobile accessibility:

```erb
<%# Minimum 44x44px touch targets (WCAG 2.2) %>
<button class="
  min-h-[44px]
  min-w-[44px]
  p-3
  touch-manipulation  <%# Disable double-tap zoom %>
">
  <%= content %>
</button>

<%# Icon buttons need explicit sizing %>
<button class="
  h-11 w-11          <%# 44px %>
  flex items-center justify-center
  rounded-lg
  hover:bg-gray-100
  dark:hover:bg-gray-700
  touch-manipulation
"
  aria-label="<%= action_label %>"
>
  <%= icon %>
</button>
```

### 1.3 Responsive Typography

```erb
<%# Fluid typography with clamp %>
<h1 class="
  text-2xl           <%# Mobile: 1.5rem %>
  sm:text-3xl        <%# Small: 1.875rem %>
  md:text-4xl        <%# Medium: 2.25rem %>
  lg:text-5xl        <%# Large: 3rem %>
  font-bold
  leading-tight
  tracking-tight
">
  <%= @page.title %>
</h1>

<%# Body text %>
<p class="
  text-base          <%# 1rem %>
  md:text-lg         <%# 1.125rem on larger screens %>
  leading-relaxed
  text-gray-700
  dark:text-gray-300
">
  <%= @page.description %>
</p>
```

### 1.4 Responsive Navigation Pattern

```erb
<%# Mobile: hamburger menu, Desktop: horizontal nav %>
<nav class="relative">
  <%# Desktop navigation %>
  <div class="hidden md:flex items-center space-x-6">
    <% navigation_items.each do |item| %>
      <%= link_to item.label, item.path, class: "
        px-3 py-2
        text-gray-700 dark:text-gray-300
        hover:text-primary-600 dark:hover:text-primary-400
        transition-colors
      " %>
    <% end %>
  </div>

  <%# Mobile hamburger %>
  <button
    class="md:hidden p-2"
    data-controller="mobile-nav"
    data-action="click->mobile-nav#toggle"
    aria-expanded="false"
    aria-controls="mobile-menu"
  >
    <span class="sr-only">Open menu</span>
    <%= render_icon :menu, class: "h-6 w-6" %>
  </button>

  <%# Mobile menu (hidden by default) %>
  <div
    id="mobile-menu"
    class="
      md:hidden
      absolute top-full left-0 right-0
      bg-white dark:bg-gray-800
      shadow-lg
      hidden
    "
    data-mobile-nav-target="menu"
  >
    <% navigation_items.each do |item| %>
      <%= link_to item.label, item.path, class: "
        block px-4 py-3
        border-b border-gray-100 dark:border-gray-700
        hover:bg-gray-50 dark:hover:bg-gray-700
      " %>
    <% end %>
  </div>
</nav>
```

### 1.5 Responsive Tables

```erb
<%# Card layout on mobile, table on desktop %>
<div class="overflow-x-auto">
  <%# Desktop table (hidden on mobile) %>
  <table class="hidden md:table w-full">
    <thead class="bg-gray-50 dark:bg-gray-700">
      <tr>
        <th class="px-4 py-3 text-left text-sm font-semibold">Name</th>
        <th class="px-4 py-3 text-left text-sm font-semibold">Email</th>
        <th class="px-4 py-3 text-left text-sm font-semibold">Status</th>
        <th class="px-4 py-3 text-right text-sm font-semibold">Actions</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
      <% @users.each do |user| %>
        <tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50">
          <td class="px-4 py-3"><%= user.name %></td>
          <td class="px-4 py-3"><%= user.email %></td>
          <td class="px-4 py-3"><%= render_status_badge(user.status) %></td>
          <td class="px-4 py-3 text-right"><%= render_actions(user) %></td>
        </tr>
      <% end %>
    </tbody>
  </table>

  <%# Mobile card layout %>
  <div class="md:hidden space-y-4">
    <% @users.each do |user| %>
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
        <div class="flex items-center justify-between mb-2">
          <h3 class="font-semibold"><%= user.name %></h3>
          <%= render_status_badge(user.status) %>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
          <%= user.email %>
        </p>
        <div class="flex justify-end space-x-2">
          <%= render_actions(user) %>
        </div>
      </div>
    <% end %>
  </div>
</div>
```

---

## 2. Animation & Transition Patterns

### 2.1 Transition Timing Functions

```css
/* Recommended easing functions */
.ease-smooth {
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); /* Default Tailwind */
}

.ease-bounce {
  transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.ease-elastic {
  transition-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

### 2.2 Micro-Interactions

```erb
<%# Button hover/active states %>
<button class="
  px-4 py-2
  bg-primary-600
  text-white
  rounded-lg

  <%# Smooth transitions %>
  transition-all
  duration-200
  ease-out

  <%# Hover: slight lift %>
  hover:bg-primary-700
  hover:shadow-md
  hover:-translate-y-0.5

  <%# Active: press down %>
  active:translate-y-0
  active:shadow-sm

  <%# Focus: ring %>
  focus:outline-none
  focus:ring-2
  focus:ring-primary-500
  focus:ring-offset-2
">
  <%= content %>
</button>

<%# Card hover effect %>
<div class="
  bg-white dark:bg-gray-800
  rounded-xl
  shadow-sm
  p-6

  transition-all
  duration-300
  ease-out

  hover:shadow-lg
  hover:-translate-y-1

  cursor-pointer
">
  <%= yield %>
</div>
```

### 2.3 Page Transitions with Turbo

```javascript
// app/javascript/controllers/page_transition_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["content"]

  connect() {
    document.addEventListener("turbo:before-visit", this.fadeOut.bind(this))
    document.addEventListener("turbo:load", this.fadeIn.bind(this))
  }

  fadeOut() {
    this.contentTarget.classList.add("opacity-0", "translate-y-2")
  }

  fadeIn() {
    requestAnimationFrame(() => {
      this.contentTarget.classList.remove("opacity-0", "translate-y-2")
    })
  }
}
```

```erb
<%# In layout %>
<main
  class="transition-all duration-300 ease-out"
  data-controller="page-transition"
  data-page-transition-target="content"
>
  <%= yield %>
</main>
```

### 2.4 Modal/Drawer Animations

```javascript
// app/javascript/controllers/modal_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["backdrop", "panel"]
  static values = { open: Boolean }

  connect() {
    if (this.openValue) this.open()
  }

  open() {
    // Prevent body scroll
    document.body.classList.add("overflow-hidden")

    // Show modal
    this.element.classList.remove("hidden")

    // Animate in (next frame for transition)
    requestAnimationFrame(() => {
      this.backdropTarget.classList.remove("opacity-0")
      this.panelTarget.classList.remove("opacity-0", "scale-95", "translate-y-4")
    })
  }

  close() {
    // Animate out
    this.backdropTarget.classList.add("opacity-0")
    this.panelTarget.classList.add("opacity-0", "scale-95", "translate-y-4")

    // Hide after animation
    setTimeout(() => {
      this.element.classList.add("hidden")
      document.body.classList.remove("overflow-hidden")
    }, 300)
  }

  backdropClick(event) {
    if (event.target === this.backdropTarget) {
      this.close()
    }
  }
}
```

```erb
<div
  class="fixed inset-0 z-50 hidden"
  data-controller="modal"
  data-modal-open-value="false"
  data-action="keydown.esc->modal#close"
>
  <%# Backdrop %>
  <div
    class="
      fixed inset-0
      bg-black/50
      transition-opacity duration-300
      opacity-0
    "
    data-modal-target="backdrop"
    data-action="click->modal#backdropClick"
  ></div>

  <%# Panel %>
  <div class="fixed inset-0 flex items-center justify-center p-4">
    <div
      class="
        bg-white dark:bg-gray-800
        rounded-xl
        shadow-2xl
        max-w-lg w-full
        max-h-[90vh]
        overflow-y-auto

        transition-all duration-300 ease-out
        opacity-0 scale-95 translate-y-4
      "
      data-modal-target="panel"
      role="dialog"
      aria-modal="true"
    >
      <%= yield %>
    </div>
  </div>
</div>
```

### 2.5 Respecting Reduced Motion

```css
/* Always include reduced motion support */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```erb
<%# Tailwind classes with motion-safe %>
<div class="
  motion-safe:transition-all
  motion-safe:duration-300
  motion-safe:hover:-translate-y-1
  motion-reduce:transition-none
">
  <%= content %>
</div>
```

```javascript
// Check in JavaScript
const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
).matches

if (!prefersReducedMotion) {
  // Apply animations
}
```

### 2.6 Loading Animations

```erb
<%# Spinner %>
<div class="
  h-8 w-8
  border-4
  border-primary-200
  border-t-primary-600
  rounded-full
  animate-spin
" role="status">
  <span class="sr-only">Loading...</span>
</div>

<%# Pulse dots %>
<div class="flex space-x-1" role="status">
  <span class="sr-only">Loading...</span>
  <div class="h-2 w-2 bg-primary-600 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
  <div class="h-2 w-2 bg-primary-600 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
  <div class="h-2 w-2 bg-primary-600 rounded-full animate-bounce"></div>
</div>

<%# Progress bar %>
<div class="h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
  <div
    class="h-full bg-primary-600 transition-all duration-500 ease-out"
    style="width: <%= @progress %>%"
    role="progressbar"
    aria-valuenow="<%= @progress %>"
    aria-valuemin="0"
    aria-valuemax="100"
  ></div>
</div>
```

---

## 3. Dark Mode Implementation

### 3.1 TailAdmin Dark Mode System

TailAdmin uses class-based dark mode. Toggle the `dark` class on `<html>`:

```javascript
// app/javascript/controllers/dark_mode_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["toggle"]
  static values = { mode: String }

  connect() {
    this.modeValue = this.loadPreference()
    this.apply()
  }

  toggle() {
    this.modeValue = this.modeValue === "dark" ? "light" : "dark"
    this.apply()
    this.savePreference()
  }

  apply() {
    if (this.modeValue === "dark") {
      document.documentElement.classList.add("dark")
    } else {
      document.documentElement.classList.remove("dark")
    }
  }

  loadPreference() {
    const stored = localStorage.getItem("theme")
    if (stored) return stored

    // Fall back to system preference
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark"
    }
    return "light"
  }

  savePreference() {
    localStorage.setItem("theme", this.modeValue)
  }
}
```

### 3.2 Dark Mode Color Patterns

```erb
<%# Always pair light and dark classes %>
<div class="
  bg-white           dark:bg-gray-800
  text-gray-900      dark:text-gray-100
  border-gray-200    dark:border-gray-700
">
  <h2 class="
    text-gray-900    dark:text-white
    font-semibold
  ">
    <%= @title %>
  </h2>

  <p class="
    text-gray-600    dark:text-gray-400
  ">
    <%= @description %>
  </p>

  <%# Muted/secondary text %>
  <span class="
    text-gray-500    dark:text-gray-500
  ">
    <%= @metadata %>
  </span>
</div>
```

### 3.3 Dark Mode Toggle Component

```erb
<%# Dark mode toggle button %>
<button
  type="button"
  class="
    relative
    p-2
    rounded-lg
    text-gray-500 dark:text-gray-400
    hover:bg-gray-100 dark:hover:bg-gray-700
    focus:outline-none
    focus:ring-2
    focus:ring-primary-500
  "
  data-controller="dark-mode"
  data-action="click->dark-mode#toggle"
  aria-label="Toggle dark mode"
>
  <%# Sun icon (shown in dark mode) %>
  <svg class="h-5 w-5 hidden dark:block" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd" />
  </svg>

  <%# Moon icon (shown in light mode) %>
  <svg class="h-5 w-5 block dark:hidden" fill="currentColor" viewBox="0 0 20 20">
    <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
  </svg>
</button>
```

### 3.4 Prevent Flash on Load

```erb
<%# In <head> before any CSS loads %>
<script>
  // Immediately apply theme to prevent flash
  (function() {
    const theme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (theme === 'dark' || (!theme && prefersDark)) {
      document.documentElement.classList.add('dark');
    }
  })();
</script>
```

---

## 4. Loading States & Feedback

### 4.1 Skeleton Loaders

```erb
<%# Card skeleton %>
<div class="animate-pulse">
  <div class="bg-gray-200 dark:bg-gray-700 rounded-lg h-48 mb-4"></div>
  <div class="space-y-3">
    <div class="bg-gray-200 dark:bg-gray-700 rounded h-4 w-3/4"></div>
    <div class="bg-gray-200 dark:bg-gray-700 rounded h-4 w-1/2"></div>
  </div>
</div>

<%# Table row skeleton %>
<tr class="animate-pulse">
  <td class="px-4 py-3">
    <div class="bg-gray-200 dark:bg-gray-700 rounded h-4 w-32"></div>
  </td>
  <td class="px-4 py-3">
    <div class="bg-gray-200 dark:bg-gray-700 rounded h-4 w-48"></div>
  </td>
  <td class="px-4 py-3">
    <div class="bg-gray-200 dark:bg-gray-700 rounded-full h-6 w-16"></div>
  </td>
</tr>

<%# Avatar skeleton %>
<div class="flex items-center space-x-3 animate-pulse">
  <div class="bg-gray-200 dark:bg-gray-700 rounded-full h-10 w-10"></div>
  <div class="space-y-2">
    <div class="bg-gray-200 dark:bg-gray-700 rounded h-4 w-24"></div>
    <div class="bg-gray-200 dark:bg-gray-700 rounded h-3 w-32"></div>
  </div>
</div>
```

### 4.2 Skeleton ViewComponent

```ruby
# app/components/skeleton_component.rb
class SkeletonComponent < ViewComponent::Base
  VARIANTS = {
    text: "h-4 rounded",
    title: "h-6 rounded",
    avatar: "h-10 w-10 rounded-full",
    button: "h-10 w-24 rounded-lg",
    card: "h-48 rounded-lg",
    image: "aspect-video rounded-lg"
  }.freeze

  def initialize(variant: :text, width: nil, count: 1)
    @variant = variant
    @width = width
    @count = count
  end

  def call
    content_tag :div, class: "animate-pulse #{'space-y-3' if @count > 1}" do
      safe_join(
        @count.times.map { skeleton_element },
        "\n"
      )
    end
  end

  private

  def skeleton_element
    content_tag :div, nil, class: [
      "bg-gray-200 dark:bg-gray-700",
      VARIANTS[@variant],
      width_class
    ].compact.join(" ")
  end

  def width_class
    return @width if @width.is_a?(String)

    case @width
    when :full then "w-full"
    when :half then "w-1/2"
    when :third then "w-1/3"
    when :quarter then "w-1/4"
    when :three_quarter then "w-3/4"
    end
  end
end
```

### 4.3 Turbo Frame Loading States

```erb
<%# Frame with loading indicator %>
<turbo-frame
  id="users-list"
  src="<%= users_path %>"
  loading="lazy"
  data-controller="loading-frame"
>
  <%# Loading state (shown while loading) %>
  <div data-loading-frame-target="loading" class="py-8 text-center">
    <div class="inline-flex items-center space-x-2 text-gray-500">
      <%= render SkeletonComponent.new(variant: :avatar) %>
      <span>Loading users...</span>
    </div>
  </div>
</turbo-frame>
```

### 4.4 Button Loading States

```erb
<%# Submit button with loading state %>
<button
  type="submit"
  class="
    relative
    px-4 py-2
    bg-primary-600
    text-white
    rounded-lg
    disabled:opacity-50
    disabled:cursor-not-allowed
  "
  data-controller="submit-button"
  data-action="click->submit-button#loading"
>
  <%# Normal state %>
  <span data-submit-button-target="label">
    Save Changes
  </span>

  <%# Loading state (hidden by default) %>
  <span
    data-submit-button-target="loading"
    class="absolute inset-0 flex items-center justify-center hidden"
  >
    <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
    </svg>
  </span>
</button>
```

```javascript
// app/javascript/controllers/submit_button_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["label", "loading"]

  loading() {
    this.element.disabled = true
    this.labelTarget.classList.add("invisible")
    this.loadingTarget.classList.remove("hidden")
  }

  reset() {
    this.element.disabled = false
    this.labelTarget.classList.remove("invisible")
    this.loadingTarget.classList.add("hidden")
  }
}
```

### 4.5 Optimistic UI Updates

```javascript
// app/javascript/controllers/optimistic_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["item"]
  static values = { url: String }

  async toggle(event) {
    const checkbox = event.currentTarget
    const originalState = !checkbox.checked

    // Optimistic update - UI changes immediately
    this.updateUI(checkbox.checked)

    try {
      const response = await fetch(this.urlValue, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": document.querySelector("[name='csrf-token']").content
        },
        body: JSON.stringify({ completed: checkbox.checked })
      })

      if (!response.ok) throw new Error("Failed to update")

    } catch (error) {
      // Rollback on failure
      checkbox.checked = originalState
      this.updateUI(originalState)
      this.showError("Failed to update. Please try again.")
    }
  }

  updateUI(completed) {
    if (completed) {
      this.itemTarget.classList.add("opacity-50", "line-through")
    } else {
      this.itemTarget.classList.remove("opacity-50", "line-through")
    }
  }
}
```

---

## 5. Error & Success Messaging

### 5.1 Toast Notifications

```ruby
# app/components/toast_component.rb
class ToastComponent < ViewComponent::Base
  VARIANTS = {
    success: {
      bg: "bg-green-50 dark:bg-green-900/50",
      border: "border-green-500",
      text: "text-green-800 dark:text-green-200",
      icon: "check-circle"
    },
    error: {
      bg: "bg-red-50 dark:bg-red-900/50",
      border: "border-red-500",
      text: "text-red-800 dark:text-red-200",
      icon: "x-circle"
    },
    warning: {
      bg: "bg-yellow-50 dark:bg-yellow-900/50",
      border: "border-yellow-500",
      text: "text-yellow-800 dark:text-yellow-200",
      icon: "exclamation-triangle"
    },
    info: {
      bg: "bg-blue-50 dark:bg-blue-900/50",
      border: "border-blue-500",
      text: "text-blue-800 dark:text-blue-200",
      icon: "information-circle"
    }
  }.freeze

  def initialize(variant: :info, message:, dismissable: true, auto_dismiss: 5000)
    @variant = variant
    @message = message
    @dismissable = dismissable
    @auto_dismiss = auto_dismiss
  end

  def styles
    VARIANTS[@variant]
  end
end
```

```erb
<%# app/components/toast_component.html.erb %>
<div
  class="
    flex items-start gap-3
    p-4
    rounded-lg
    border-l-4
    <%= styles[:bg] %>
    <%= styles[:border] %>
    <%= styles[:text] %>
    shadow-lg
  "
  data-controller="toast"
  data-toast-auto-dismiss-value="<%= @auto_dismiss %>"
  role="alert"
>
  <%= render_icon styles[:icon], class: "h-5 w-5 flex-shrink-0 mt-0.5" %>

  <p class="flex-1 text-sm font-medium">
    <%= @message %>
  </p>

  <% if @dismissable %>
    <button
      type="button"
      class="flex-shrink-0 p-1 rounded hover:bg-black/10"
      data-action="click->toast#dismiss"
      aria-label="Dismiss"
    >
      <%= render_icon :x, class: "h-4 w-4" %>
    </button>
  <% end %>
</div>
```

### 5.2 Toast Container with Turbo Streams

```erb
<%# app/views/layouts/_toast_container.html.erb %>
<div
  id="toast-container"
  class="
    fixed bottom-4 right-4
    z-50
    flex flex-col gap-3
    max-w-sm w-full
    pointer-events-none
  "
  aria-live="polite"
  aria-atomic="true"
>
  <%# Toasts will be inserted here via Turbo Streams %>
</div>
```

```ruby
# app/controllers/concerns/toastable.rb
module Toastable
  extend ActiveSupport::Concern

  def toast(message, variant: :info)
    respond_to do |format|
      format.turbo_stream do
        render turbo_stream: turbo_stream.append(
          "toast-container",
          ToastComponent.new(variant: variant, message: message)
        )
      end
    end
  end
end
```

### 5.3 Inline Form Validation

```erb
<%# Form field with inline error %>
<div data-controller="form-field">
  <label
    for="email"
    class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
  >
    Email Address
  </label>

  <input
    type="email"
    id="email"
    name="user[email]"
    value="<%= @user.email %>"
    class="
      w-full
      px-3 py-2
      border rounded-lg
      transition-colors

      <%= if @user.errors[:email].any? %>
        border-red-500
        focus:border-red-500
        focus:ring-red-500
      <% else %>
        border-gray-300 dark:border-gray-600
        focus:border-primary-500
        focus:ring-primary-500
      <% end %>
    "
    aria-invalid="<%= @user.errors[:email].any? %>"
    aria-describedby="<%= 'email-error' if @user.errors[:email].any? %>"
    data-action="blur->form-field#validate"
  />

  <% if @user.errors[:email].any? %>
    <p id="email-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
      <%= @user.errors[:email].first %>
    </p>
  <% end %>
</div>
```

### 5.4 Success States

```erb
<%# Success checkmark animation %>
<div class="flex flex-col items-center py-8">
  <div class="
    h-16 w-16
    rounded-full
    bg-green-100 dark:bg-green-900/50
    flex items-center justify-center
    mb-4
  ">
    <svg
      class="h-8 w-8 text-green-600 dark:text-green-400"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M5 13l4 4L19 7"
        class="animate-[draw_0.5s_ease-out_forwards]"
        style="stroke-dasharray: 20; stroke-dashoffset: 20;"
      />
    </svg>
  </div>

  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
    Successfully Saved!
  </h3>
  <p class="text-gray-600 dark:text-gray-400">
    Your changes have been saved.
  </p>
</div>

<style>
  @keyframes draw {
    to { stroke-dashoffset: 0; }
  }
</style>
```

---

## 6. Form UX Patterns

### 6.1 Multi-Step Form Wizard

```erb
<%# Step indicator %>
<nav aria-label="Progress" class="mb-8">
  <ol class="flex items-center justify-center space-x-4">
    <% steps.each_with_index do |step, index| %>
      <li class="flex items-center">
        <% if index < current_step %>
          <%# Completed step %>
          <span class="
            flex items-center justify-center
            h-10 w-10
            rounded-full
            bg-primary-600
            text-white
          ">
            <%= render_icon :check, class: "h-5 w-5" %>
          </span>
        <% elsif index == current_step %>
          <%# Current step %>
          <span class="
            flex items-center justify-center
            h-10 w-10
            rounded-full
            border-2 border-primary-600
            bg-white dark:bg-gray-800
            text-primary-600
            font-semibold
          ">
            <%= index + 1 %>
          </span>
        <% else %>
          <%# Future step %>
          <span class="
            flex items-center justify-center
            h-10 w-10
            rounded-full
            border-2 border-gray-300 dark:border-gray-600
            text-gray-500
          ">
            <%= index + 1 %>
          </span>
        <% end %>

        <% unless index == steps.length - 1 %>
          <div class="
            ml-4 h-0.5 w-16
            <%= index < current_step ? 'bg-primary-600' : 'bg-gray-300 dark:bg-gray-600' %>
          "></div>
        <% end %>
      </li>
    <% end %>
  </ol>
</nav>
```

### 6.2 Auto-Save Draft

```javascript
// app/javascript/controllers/autosave_controller.js
import { Controller } from "@hotwired/stimulus"
import { debounce } from "lodash-es"

export default class extends Controller {
  static targets = ["form", "status"]
  static values = { url: String, delay: { type: Number, default: 2000 } }

  connect() {
    this.save = debounce(this.save.bind(this), this.delayValue)
  }

  changed() {
    this.statusTarget.textContent = "Unsaved changes..."
    this.statusTarget.classList.remove("text-green-600")
    this.statusTarget.classList.add("text-yellow-600")
    this.save()
  }

  async save() {
    const formData = new FormData(this.formTarget)

    try {
      this.statusTarget.textContent = "Saving..."

      const response = await fetch(this.urlValue, {
        method: "PATCH",
        body: formData,
        headers: {
          "X-CSRF-Token": document.querySelector("[name='csrf-token']").content,
          "Accept": "application/json"
        }
      })

      if (response.ok) {
        this.statusTarget.textContent = "Saved"
        this.statusTarget.classList.remove("text-yellow-600")
        this.statusTarget.classList.add("text-green-600")
      }
    } catch (error) {
      this.statusTarget.textContent = "Failed to save"
      this.statusTarget.classList.add("text-red-600")
    }
  }
}
```

```erb
<div data-controller="autosave" data-autosave-url-value="<%= draft_path(@draft) %>">
  <div class="flex items-center justify-between mb-4">
    <h2>Edit Draft</h2>
    <span
      data-autosave-target="status"
      class="text-sm text-gray-500"
    >
      All changes saved
    </span>
  </div>

  <%= form_with model: @draft, data: { autosave_target: "form" } do |f| %>
    <%= f.text_field :title,
      data: { action: "input->autosave#changed" },
      class: "..."
    %>

    <%= f.text_area :content,
      data: { action: "input->autosave#changed" },
      class: "..."
    %>
  <% end %>
</div>
```

### 6.3 Character Counter

```erb
<div data-controller="character-counter" data-character-counter-max-value="280">
  <label for="bio" class="block text-sm font-medium mb-1">
    Bio
  </label>

  <textarea
    id="bio"
    name="user[bio]"
    rows="4"
    class="w-full px-3 py-2 border rounded-lg"
    data-character-counter-target="input"
    data-action="input->character-counter#count"
    maxlength="280"
  ><%= @user.bio %></textarea>

  <div class="flex justify-end mt-1">
    <span
      data-character-counter-target="count"
      class="text-sm text-gray-500"
    >
      <%= @user.bio&.length || 0 %>/280
    </span>
  </div>
</div>
```

---

## 7. Performance Optimization

### 7.1 Lazy Loading Images

```erb
<%# Native lazy loading %>
<%= image_tag @product.image,
  loading: "lazy",
  decoding: "async",
  class: "w-full h-auto rounded-lg",
  alt: @product.name
%>

<%# With blur-up placeholder %>
<div class="relative overflow-hidden rounded-lg bg-gray-200">
  <%# Tiny placeholder (inline base64) %>
  <img
    src="<%= @product.placeholder_url %>"
    class="absolute inset-0 w-full h-full object-cover blur-lg scale-110"
    aria-hidden="true"
  />

  <%# Full image %>
  <img
    src="<%= @product.image_url %>"
    loading="lazy"
    class="relative w-full h-auto"
    alt="<%= @product.name %>"
    onload="this.previousElementSibling.remove()"
  />
</div>
```

### 7.2 Intersection Observer for Lazy Loading

```javascript
// app/javascript/controllers/lazy_load_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["content"]
  static values = { url: String }

  connect() {
    this.observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.load()
            this.observer.disconnect()
          }
        })
      },
      { rootMargin: "100px" }
    )

    this.observer.observe(this.element)
  }

  async load() {
    const response = await fetch(this.urlValue, {
      headers: { "Accept": "text/html" }
    })

    if (response.ok) {
      const html = await response.text()
      this.contentTarget.innerHTML = html
    }
  }

  disconnect() {
    this.observer?.disconnect()
  }
}
```

### 7.3 Core Web Vitals Optimization

```erb
<%# Preload critical resources %>
<link rel="preload" href="<%= asset_path('fonts/inter.woff2') %>" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="<%= image_path('hero.webp') %>" as="image">

<%# Preconnect to external resources %>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://analytics.example.com">

<%# Above-the-fold critical CSS (inline) %>
<style>
  /* Critical CSS for LCP element */
  .hero { /* ... */ }
</style>

<%# Defer non-critical CSS %>
<link rel="stylesheet" href="<%= stylesheet_path('application') %>" media="print" onload="this.media='all'">
```

### 7.4 Prevent Layout Shift (CLS)

```erb
<%# Always set dimensions on images %>
<img
  src="<%= @image.url %>"
  width="800"
  height="600"
  class="w-full h-auto"
  alt="<%= @image.alt %>"
/>

<%# Reserve space for dynamic content %>
<div
  style="min-height: 400px;"
  data-controller="lazy-load"
  data-lazy-load-url-value="<%= comments_path %>"
>
  <%# Skeleton placeholder %>
  <%= render SkeletonComponent.new(variant: :card, count: 3) %>
</div>

<%# Aspect ratio containers %>
<div class="aspect-video bg-gray-200 rounded-lg overflow-hidden">
  <iframe
    src="<%= @video.embed_url %>"
    loading="lazy"
    class="w-full h-full"
    allowfullscreen
  ></iframe>
</div>
```

---

## Quick Reference Checklist

### Responsive Design
- [ ] Mobile-first approach (base styles = mobile)
- [ ] Touch targets minimum 44x44px
- [ ] Tables convert to cards on mobile
- [ ] Navigation collapses to hamburger
- [ ] Typography scales appropriately

### Animations
- [ ] Transitions use easing (not linear)
- [ ] Duration 200-300ms for micro-interactions
- [ ] `prefers-reduced-motion` respected
- [ ] No animations on initial load

### Dark Mode
- [ ] All colors have dark: variants
- [ ] Toggle saved to localStorage
- [ ] System preference detected
- [ ] No flash on page load

### Loading States
- [ ] Skeleton loaders match content
- [ ] Buttons show loading spinner
- [ ] Forms disable during submit
- [ ] Optimistic UI where appropriate

### Performance
- [ ] Images lazy loaded
- [ ] Critical CSS inlined
- [ ] Fonts preloaded
- [ ] Layout shift prevented

---

## Related Skills

- **accessibility-patterns** - WCAG 2.2 compliance
- **hotwire-patterns** - Turbo and Stimulus integration
- **viewcomponents-specialist** - Component architecture
- **tailadmin-patterns** - TailAdmin-specific patterns
