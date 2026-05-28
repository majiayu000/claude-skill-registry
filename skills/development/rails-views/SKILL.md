---
name: rails-views
description: ERB templates, helpers, layouts, partials, and view patterns
version: 1.0.0
rails_version: ">= 7.0"
tags:
  - views
  - erb
  - templates
  - helpers
---

# Rails Views

## Quick Reference

| Pattern | Example |
|---------|---------|
| **Output** | `<%= @post.title %>` |
| **Code** | `<% @posts.each do |post| %>` |
| **Link** | `<%= link_to 'Home', root_path %>` |
| **Form** | `<%= form_with model: @post do |f| %>` |
| **Partial** | `<%= render 'shared/header' %>` |
| **Helper** | `<%= truncate @post.body, length: 100 %>` |
| **Asset** | `<%= image_tag 'logo.png' %>` |

## ERB Basics

```erb
<%# Comment - won't be rendered %>

<% # Ruby code - executed but not displayed %>
<% if user_signed_in? %>
  <p>Welcome back!</p>
<% end %>

<%= # Ruby code with output %>
<%= @post.title %>
<%= current_user.name %>

<%== # Output without HTML escaping (dangerous!) %>
<%== raw_html_content %>

<%- # Suppress whitespace before tag %>
<%- if condition -%>

<%= # Safe output (escapes HTML by default) %>
<%= user_input %> <%# Safe from XSS %>
```

## Layouts

```erb
<%# app/views/layouts/application.html.erb %>
<!DOCTYPE html>
<html>
  <head>
    <title><%= content_for?(:title) ? yield(:title) : "My App" %></title>
    <%= csrf_meta_tags %>
    <%= csp_meta_tag %>
    
    <%= stylesheet_link_tag "application", "data-turbo-track": "reload" %>
    <%= javascript_importmap_tags %>
    
    <%= yield :head %>
  </head>
  
  <body class="<%= controller_name %> <%= action_name %>">
    <%= render 'shared/header' %>
    
    <% flash.each do |type, message| %>
      <div class="alert alert-<%= type %>">
        <%= message %>
      </div>
    <% end %>
    
    <main>
      <%= yield %>
    </main>
    
    <%= render 'shared/footer' %>
  </body>
</html>
```

### Content For

```erb
<%# In view template %>
<% content_for :title do %>
  <%= @post.title %> - My Blog
<% end %>

<% content_for :head do %>
  <%= stylesheet_link_tag "posts" %>
  <meta name="description" content="<%= @post.excerpt %>">
<% end %>

<%# Content here will be yielded in layout %>
<article>
  <%= @post.body %>
</article>
```

## Partials

### Basic Partials

```erb
<%# Render partial %>
<%= render 'shared/header' %>
<%= render 'post' %>
<%= render partial: 'post' %>

<%# With local variables %>
<%= render 'post', post: @post %>
<%= render partial: 'post', locals: { post: @post, show_author: true } %>

<%# Partial file: app/views/shared/_header.html.erb %>
<header>
  <h1>My Blog</h1>
</header>

<%# Partial file: app/views/posts/_post.html.erb %>
<article>
  <h2><%= post.title %></h2>
  <p><%= post.body %></p>
  <% if local_assigns[:show_author] %>
    <p>By <%= post.author.name %></p>
  <% end %>
</article>
```

### Collection Partials

```erb
<%# Render for each item %>
<%= render partial: 'post', collection: @posts %>

<%# Shorthand %>
<%= render @posts %>

<%# With local variable name %>
<%= render partial: 'post', collection: @posts, as: :item %>

<%# With spacer template %>
<%= render partial: 'post', collection: @posts, spacer_template: 'post_divider' %>

<%# In partial, access current index %>
<article data-index="<%= post_counter %>">
  <%= post.title %>
</article>
```

## Forms

### Form Helpers

```erb
<%= form_with model: @post do |f| %>
  <% if @post.errors.any? %>
    <div class="errors">
      <h3><%= pluralize(@post.errors.count, "error") %> prohibited this post from being saved:</h3>
      <ul>
        <% @post.errors.full_messages.each do |message| %>
          <li><%= message %></li>
        <% end %>
      </ul>
    </div>
  <% end %>

  <div class="field">
    <%= f.label :title %>
    <%= f.text_field :title, class: 'form-control' %>
  </div>

  <div class="field">
    <%= f.label :body %>
    <%= f.text_area :body, rows: 10, class: 'form-control' %>
  </div>

  <div class="field">
    <%= f.label :published %>
    <%= f.check_box :published %>
  </div>

  <div class="field">
    <%= f.label :category_id %>
    <%= f.collection_select :category_id, Category.all, :id, :name, 
        { prompt: 'Select a category' }, { class: 'form-control' } %>
  </div>

  <div class="field">
    <%= f.label :tag_ids %>
    <%= f.collection_check_boxes :tag_ids, Tag.all, :id, :name %>
  </div>

  <div class="actions">
    <%= f.submit "Save Post", class: 'btn btn-primary' %>
  </div>
<% end %>
```

### Form Field Types

```erb
<%= f.text_field :name %>
<%= f.text_area :description %>
<%= f.password_field :password %>
<%= f.email_field :email %>
<%= f.url_field :website %>
<%= f.number_field :age %>
<%= f.date_field :birthday %>
<%= f.datetime_field :published_at %>
<%= f.time_field :starts_at %>
<%= f.hidden_field :user_id %>

<%= f.check_box :published %>
<%= f.radio_button :status, 'active' %>

<%= f.select :category_id, Category.pluck(:name, :id) %>
<%= f.collection_select :author_id, User.all, :id, :name %>
<%= f.collection_radio_buttons :status, Status.all, :id, :name %>
<%= f.collection_check_boxes :tag_ids, Tag.all, :id, :name %>

<%= f.file_field :avatar %>
```

### Non-Model Forms

```erb
<%= form_with url: search_path, method: :get do |f| %>
  <%= f.text_field :query, placeholder: 'Search...' %>
  <%= f.submit 'Search' %>
<% end %>
```

## Links and URLs

```erb
<%# Basic link %>
<%= link_to 'Home', root_path %>
<%= link_to 'Edit', edit_post_path(@post) %>
<%= link_to 'Delete', post_path(@post), data: { turbo_method: :delete, turbo_confirm: 'Are you sure?' } %>

<%# Link to object (uses polymorphic routing) %>
<%= link_to @post.title, @post %>
<%= link_to 'Edit', [:edit, @post] %>

<%# Link with block %>
<%= link_to post_path(@post) do %>
  <strong><%= @post.title %></strong>
  <p><%= @post.excerpt %></p>
<% end %>

<%# Link classes and data attributes %>
<%= link_to 'Click', path, class: 'btn btn-primary', data: { action: 'click->controller#method' } %>

<%# Button to (generates a form) %>
<%= button_to 'Delete', post_path(@post), method: :delete, class: 'btn btn-danger' %>

<%# Mail to %>
<%= mail_to 'user@example.com' %>
<%= mail_to 'user@example.com', 'Contact Us', subject: 'Hello' %>
```

## Asset Helpers

```erb
<%# Images %>
<%= image_tag 'logo.png' %>
<%= image_tag 'logo.png', alt: 'Logo', class: 'logo', size: '100x100' %>
<%= image_tag @post.cover_image_url %>

<%# Stylesheets %>
<%= stylesheet_link_tag 'application' %>
<%= stylesheet_link_tag 'posts', media: 'all' %>

<%# JavaScript %>
<%= javascript_include_tag 'application' %>
<%= javascript_importmap_tags %>

<%# Asset path %>
<%= asset_path 'image.png' %>
<%= asset_url 'image.png' %>
```

## View Helpers

### Text Helpers

```erb
<%= truncate @post.body, length: 100 %>
<%= truncate @post.body, length: 100, separator: ' ' %>

<%= simple_format @post.body %>

<%= pluralize @posts.count, 'post' %>

<%= number_to_currency 29.99 %>
<%= number_to_percentage 85.5 %>
<%= number_with_delimiter 1000000 %>
<%= number_to_human 1234567 %>

<%= time_ago_in_words @post.created_at %>
<%= distance_of_time_in_words Time.now, @post.created_at %>
```

### Content Helpers

```erb
<%= content_tag :div, "Hello", class: 'greeting' %>
<%# Output: <div class="greeting">Hello</div> %>

<%= content_tag :div, class: 'post' do %>
  <%= @post.title %>
<% end %>

<%= tag.div "Hello", class: 'greeting' %>
<%= tag.div class: 'post' do %>
  <%= @post.title %>
<% end %>
```

### Sanitization

```erb
<%# Strip all HTML tags %>
<%= strip_tags @post.html_content %>

<%# Allow specific tags %>
<%= sanitize @post.html_content, tags: %w[p br strong em] %>

<%# Escape HTML %>
<%= html_escape user_input %>
<%= h user_input %> <%# shorthand %>
```

## Custom Helpers

```ruby
# app/helpers/application_helper.rb
module ApplicationHelper
  def page_title(title)
    content_for(:title) { title }
    content_tag(:h1, title, class: 'page-title')
  end
  
  def active_link(text, path, **options)
    active = current_page?(path)
    classes = options[:class].to_s
    classes += ' active' if active
    link_to text, path, class: classes
  end
  
  def formatted_date(date)
    return 'N/A' unless date
    date.strftime('%B %d, %Y')
  end
  
  def user_avatar(user, size: 50)
    if user.avatar.attached?
      image_tag user.avatar.variant(resize_to_limit: [size, size])
    else
      image_tag "default-avatar.png", size: "#{size}x#{size}"
    end
  end
end
```

```erb
<%# Using custom helpers %>
<%= page_title "My Posts" %>
<%= active_link "Home", root_path, class: 'nav-link' %>
<%= formatted_date @post.created_at %>
<%= user_avatar current_user, size: 100 %>
```

## Turbo Frames

```erb
<%# Turbo Frame %>
<%= turbo_frame_tag "post_#{@post.id}" do %>
  <%= render @post %>
<% end %>

<%# Turbo Frame with lazy loading %>
<%= turbo_frame_tag "post_#{@post.id}", src: post_path(@post), loading: :lazy do %>
  Loading...
<% end %>

<%# Target a specific frame %>
<%= link_to "Edit", edit_post_path(@post), data: { turbo_frame: "post_#{@post.id}" } %>
```

## Turbo Streams

```erb
<%# app/views/posts/create.turbo_stream.erb %>
<%= turbo_stream.prepend "posts" do %>
  <%= render @post %>
<% end %>

<%= turbo_stream.update "flash" do %>
  <div class="notice">Post created!</div>
<% end %>

<%# Available actions: append, prepend, replace, update, remove, before, after %>
```

## Conditional Rendering

```erb
<% if user_signed_in? %>
  <p>Welcome, <%= current_user.name %>!</p>
  <%= link_to "Logout", logout_path, data: { turbo_method: :delete } %>
<% else %>
  <%= link_to "Login", login_path %>
<% end %>

<% unless @posts.empty? %>
  <%= render @posts %>
<% else %>
  <p>No posts yet.</p>
<% end %>

<%# Ternary operator %>
<%= @post.published? ? "Published" : "Draft" %>
```

## Loops and Iteration

```erb
<% @posts.each do |post| %>
  <%= render post %>
<% end %>

<% @posts.each_with_index do |post, index| %>
  <div class="post-<%= index + 1 %>">
    <%= render post %>
  </div>
<% end %>

<%# Check if collection is empty %>
<% if @posts.any? %>
  <% @posts.each do |post| %>
    <%= render post %>
  <% end %>
<% else %>
  <p>No posts found.</p>
<% end %>
```

## Best Practices

1. **Keep views simple** - Complex logic belongs in helpers or models
2. **Use partials** for reusable components
3. **Use helpers** for view-specific logic
4. **Escape user input** (Rails does this by default with `<%= %>`)
5. **Use semantic HTML** for accessibility
6. **Leverage Turbo** for reactive UIs without JavaScript
7. **Use content_for** for flexible layouts
8. **Keep CSS/JS out** of ERB files (use asset pipeline)
9. **Use I18n** for text content to support internationalization
10. **Test helpers** with unit tests

## Common Patterns

### Conditional Class Names

```erb
<div class="<%= 'active' if @post.published? %> post">
  ...
</div>

<%# Better with helper %>
<div class="<%= post_classes(@post) %>">
  ...
</div>

# In helper
def post_classes(post)
  classes = ['post']
  classes << 'published' if post.published?
  classes << 'featured' if post.featured?
  classes.join(' ')
end
```

### Empty State

```erb
<% if @posts.any? %>
  <%= render @posts %>
<% else %>
  <div class="empty-state">
    <p>No posts yet.</p>
    <%= link_to "Create your first post", new_post_path, class: 'btn' %>
  </div>
<% end %>
```

## References

- [Rails Guides - Layouts and Rendering](https://guides.rubyonrails.org/layouts_and_rendering.html)
- [Rails Guides - Form Helpers](https://guides.rubyonrails.org/form_helpers.html)
- [Rails Guides - Action View](https://guides.rubyonrails.org/action_view_overview.html)
- [Hotwire Turbo Handbook](https://turbo.hotwired.dev/handbook/introduction)
