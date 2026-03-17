---
name: tailwindcss
description: TailwindCSS utility-first styling for Rails
version: 1.0.0
rails_version: ">= 7.0"
tags:
  - css
  - tailwind
  - styling
  - frontend
---

# TailwindCSS in Rails

## Quick Reference

| Category | Classes |
|----------|---------|
| **Layout** | `flex`, `grid`, `container`, `mx-auto` |
| **Spacing** | `p-4`, `m-2`, `px-6`, `py-3`, `space-x-4` |
| **Typography** | `text-lg`, `font-bold`, `text-center`, `text-gray-700` |
| **Colors** | `bg-blue-500`, `text-white`, `border-gray-300` |
| **Sizing** | `w-full`, `h-64`, `max-w-md`, `min-h-screen` |
| **Flexbox** | `flex`, `items-center`, `justify-between` |
| **Grid** | `grid`, `grid-cols-3`, `gap-4` |
| **Responsive** | `md:flex`, `lg:grid-cols-4`, `sm:text-sm` |

## Installation

```bash
# Rails 7+ with Tailwind
./bin/bundle add tailwindcss-rails
./bin/rails tailwindcss:install
```

## Common Patterns

### Container & Layout

```erb
<%# Max-width container %>
<div class="container mx-auto px-4">
  Content
</div>

<%# Full-width section with max-width content %>
<section class="w-full bg-gray-100">
  <div class="max-w-7xl mx-auto px-4 py-8">
    Content
  </div>
</section>
```

### Flexbox Layouts

```erb
<%# Horizontal flex %>
<div class="flex items-center space-x-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<%# Space between %>
<div class="flex justify-between items-center">
  <div>Left</div>
  <div>Right</div>
</div>

<%# Centered content %>
<div class="flex items-center justify-center min-h-screen">
  <div>Centered</div>
</div>

<%# Vertical flex %>
<div class="flex flex-col space-y-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Grid Layouts

```erb
<%# Basic grid %>
<div class="grid grid-cols-3 gap-4">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>

<%# Responsive grid %>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <% @posts.each do |post| %>
    <%= render post %>
  <% end %>
</div>

<%# Grid with different column spans %>
<div class="grid grid-cols-12 gap-4">
  <div class="col-span-8">Main content</div>
  <div class="col-span-4">Sidebar</div>
</div>
```

### Cards

```erb
<div class="bg-white rounded-lg shadow-md p-6">
  <h3 class="text-xl font-bold mb-2"><%= @post.title %></h3>
  <p class="text-gray-600"><%= @post.excerpt %></p>
  <div class="mt-4">
    <%= link_to "Read More", @post, class: "text-blue-500 hover:text-blue-700" %>
  </div>
</div>

<%# Card with hover effect %>
<div class="bg-white rounded-lg shadow hover:shadow-xl transition-shadow duration-300 p-6">
  Content
</div>
```

### Buttons

```erb
<%# Primary button %>
<%= link_to "Submit", path, class: "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" %>

<%# Secondary button %>
<%= link_to "Cancel", path, class: "bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded" %>

<%# Outline button %>
<%= link_to "Edit", path, class: "border border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white font-bold py-2 px-4 rounded" %>

<%# Icon button %>
<button class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded-full">
  <svg class="w-6 h-6">...</svg>
</button>
```

### Forms

```erb
<%= form_with model: @post, class: "space-y-6" do |f| %>
  <div>
    <%= f.label :title, class: "block text-sm font-medium text-gray-700 mb-1" %>
    <%= f.text_field :title, class: "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" %>
  </div>

  <div>
    <%= f.label :body, class: "block text-sm font-medium text-gray-700 mb-1" %>
    <%= f.text_area :body, rows: 6, class: "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" %>
  </div>

  <div class="flex items-center">
    <%= f.check_box :published, class: "h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" %>
    <%= f.label :published, class: "ml-2 block text-sm text-gray-900" %>
  </div>

  <div class="flex space-x-4">
    <%= f.submit "Save", class: "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded" %>
    <%= link_to "Cancel", posts_path, class: "bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-6 rounded" %>
  </div>
<% end %>
```

### Navigation

```erb
<nav class="bg-white shadow-lg">
  <div class="max-w-7xl mx-auto px-4">
    <div class="flex justify-between items-center h-16">
      <%= link_to "Logo", root_path, class: "text-xl font-bold text-gray-800" %>
      
      <div class="hidden md:flex space-x-8">
        <%= link_to "Home", root_path, class: "text-gray-700 hover:text-blue-500" %>
        <%= link_to "Posts", posts_path, class: "text-gray-700 hover:text-blue-500" %>
        <%= link_to "About", about_path, class: "text-gray-700 hover:text-blue-500" %>
      </div>
      
      <button class="md:hidden">
        <svg class="w-6 h-6">...</svg>
      </button>
    </div>
  </div>
</nav>
```

### Tables

```erb
<div class="overflow-x-auto">
  <table class="min-w-full bg-white border">
    <thead class="bg-gray-100">
      <tr>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Title
        </th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Author
        </th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Actions
        </th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-200">
      <% @posts.each do |post| %>
        <tr class="hover:bg-gray-50">
          <td class="px-6 py-4 whitespace-nowrap">
            <%= post.title %>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <%= post.author.name %>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm">
            <%= link_to "Edit", edit_post_path(post), class: "text-blue-500 hover:text-blue-700 mr-4" %>
            <%= link_to "Delete", post, method: :delete, class: "text-red-500 hover:text-red-700" %>
          </td>
        </tr>
      <% end %>
    </tbody>
  </table>
</div>
```

### Alerts/Flash Messages

```erb
<% flash.each do |type, message| %>
  <div class="<%= alert_class(type) %> p-4 rounded-md mb-4">
    <div class="flex">
      <div class="flex-shrink-0">
        <%# Icon %>
      </div>
      <div class="ml-3">
        <p class="text-sm font-medium">
          <%= message %>
        </p>
      </div>
    </div>
  </div>
<% end %>

<%# Helper method %>
def alert_class(type)
  case type.to_sym
  when :notice, :success
    "bg-green-100 border border-green-400 text-green-700"
  when :alert, :error
    "bg-red-100 border border-red-400 text-red-700"
  when :warning
    "bg-yellow-100 border border-yellow-400 text-yellow-700"
  else
    "bg-blue-100 border border-blue-400 text-blue-700"
  end
end
```

### Modal

```erb
<div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" id="my-modal">
  <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
    <div class="mt-3">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Modal Title</h3>
      <div class="mt-2">
        <p class="text-sm text-gray-500">Modal content goes here.</p>
      </div>
      <div class="mt-4 flex justify-end space-x-3">
        <button class="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400">
          Cancel
        </button>
        <button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
          Confirm
        </button>
      </div>
    </div>
  </div>
</div>
```

### Badges

```erb
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
  New
</span>

<span class="inline-flex items-center px-3 py-1 rounded-md text-sm font-medium bg-green-100 text-green-800">
  Published
</span>
```

### Responsive Design

```erb
<%# Hide on mobile, show on desktop %>
<div class="hidden md:block">
  Desktop only
</div>

<%# Show on mobile, hide on desktop %>
<div class="block md:hidden">
  Mobile only
</div>

<%# Responsive text sizes %>
<h1 class="text-2xl md:text-4xl lg:text-6xl font-bold">
  Title
</h1>

<%# Responsive padding %>
<div class="p-4 md:p-8 lg:p-12">
  Content
</div>
```

## Customization

```javascript
// config/tailwind.config.js
module.exports = {
  content: [
    './app/views/**/*.html.erb',
    './app/helpers/**/*.rb',
    './app/assets/stylesheets/**/*.css',
    './app/javascript/**/*.js'
  ],
  theme: {
    extend: {
      colors: {
        'brand': {
          light: '#3fbaeb',
          DEFAULT: '#0fa9e6',
          dark: '#0c87b8',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

## Best Practices

1. **Use @apply sparingly** - Prefer utility classes in templates
2. **Create components** for repeated patterns
3. **Use responsive prefixes** - mobile-first approach
4. **Leverage Tailwind plugins** - forms, typography, etc.
5. **Keep custom CSS minimal** - use Tailwind's configuration
6. **Use consistent spacing scale** - stick to theme spacing
7. **Optimize for production** - PurgeCSS removes unused styles automatically

## Common Pitfalls

- **Too many utilities** - Extract to components or use @apply
- **Not purging** - Make sure content paths are configured correctly
- **Fighting the framework** - Use Tailwind's patterns, don't fight them
- **Forgetting responsive** - Always test mobile-first

## References

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind CSS Rails](https://github.com/rails/tailwindcss-rails)
- [Tailwind UI Components](https://tailwindui.com/)
