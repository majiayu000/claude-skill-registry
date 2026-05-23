---
name: views
description: Customizing Plutonium views - pages, forms, displays, tables, and layouts using Phlex
---

# Plutonium Views

Plutonium uses [Phlex](https://www.phlex.fun/) for all view components. This provides a Ruby-first approach to building HTML with full IDE support and type safety.

## Architecture Overview

```
Definition
├── IndexPage    → renders Table
├── ShowPage     → renders Display
├── NewPage      → renders Form
├── EditPage     → renders Form
└── InteractiveActionPage → renders Form
```

Each definition has nested classes you can override:

```ruby
class PostDefinition < ResourceDefinition
  class IndexPage < IndexPage; end
  class ShowPage < ShowPage; end
  class NewPage < NewPage; end
  class EditPage < EditPage; end
  class Form < Form; end
  class Table < Table; end
  class Display < Display; end
end
```

## Page Customization

### Page Configuration

Set page titles and descriptions in definitions:

```ruby
class PostDefinition < ResourceDefinition
  # Static titles
  index_page_title "Blog Posts"
  index_page_description "Manage all published articles"

  show_page_title "Article Details"
  new_page_title "Write New Article"
  edit_page_title "Edit Article"

  # Control breadcrumbs
  breadcrumbs true          # Global default
  index_page_breadcrumbs false  # Per-page override
  show_page_breadcrumbs true
end
```

### Custom Page Class

Override page rendering by subclassing:

```ruby
class PostDefinition < ResourceDefinition
  class ShowPage < ShowPage
    private

    # Custom title logic
    def page_title
      "#{object.title} - #{object.author.name}"
    end

    # Add content before the main area
    def render_before_content
      div(class: "alert alert-info") {
        "This post has #{object.comments.count} comments"
      }
    end

    # Add content after
    def render_after_content
      render RelatedPostsComponent.new(post: object)
    end

    # Override the toolbar
    def render_toolbar
      div(class: "flex gap-2") {
        button(class: "btn") { "Preview" }
        button(class: "btn btn-primary") { "Publish" }
      }
    end
  end
end
```

### Page Hooks

All pages inherit these customization hooks:

| Hook | Purpose |
|------|---------|
| `render_before_header` | Before entire header section |
| `render_after_header` | After entire header section |
| `render_before_breadcrumbs` | Before breadcrumbs |
| `render_after_breadcrumbs` | After breadcrumbs |
| `render_before_page_header` | Before title/actions |
| `render_after_page_header` | After title/actions |
| `render_before_toolbar` | Before toolbar |
| `render_after_toolbar` | After toolbar |
| `render_before_content` | Before main content |
| `render_after_content` | After main content |
| `render_before_footer` | Before footer |
| `render_after_footer` | After footer |

### Custom View Files

For complete control, create custom ERB view files that replace the default entirely.

**File locations:**

```
# Main app (for a PostsController)
app/views/posts/index.html.erb
app/views/posts/show.html.erb
app/views/posts/new.html.erb
app/views/posts/edit.html.erb

# Portal-specific
packages/admin_portal/app/views/admin_portal/posts/show.html.erb
```

**Default view structure:**

The default views simply render the page class:

```erb
<%# app/views/resource/show.html.erb %>
<%= render current_definition.show_page_class.new %>
```

**Custom view example:**

```erb
<%# app/views/posts/show.html.erb %>
<div class="max-w-4xl mx-auto">
  <article class="prose lg:prose-xl">
    <h1><%= resource_record!.title %></h1>
    <div class="meta text-gray-500">
      By <%= resource_record!.author.name %> on <%= resource_record!.created_at.strftime("%B %d, %Y") %>
    </div>
    <%= raw resource_record!.content %>
  </article>

  <div class="mt-8">
    <%= link_to "Edit", resource_url_for(resource_record!, action: :edit), class: "btn" %>
    <%= link_to "Back", resource_url_for(Post), class: "btn" %>
  </div>
</div>
```

**Mixing approaches:**

Render the default page with additions:

```erb
<%# app/views/posts/show.html.erb %>
<div class="announcement-banner">
  Special announcement here
</div>

<%= render current_definition.show_page_class.new %>

<div class="related-posts">
  <%= render partial: "related_posts", locals: { post: resource_record! } %>
</div>
```

## Form Customization

### Custom Form Template

Override how fields are rendered:

```ruby
class PostDefinition < ResourceDefinition
  class Form < Form
    def form_template
      # Custom layout with sections
      div(class: "grid grid-cols-2 gap-6") {
        div {
          h3(class: "text-lg font-medium") { "Basic Info" }
          render_resource_field :title
          render_resource_field :slug
        }

        div {
          h3(class: "text-lg font-medium") { "Content" }
          render_resource_field :content
        }
      }

      div(class: "mt-6") {
        h3(class: "text-lg font-medium") { "Publishing" }
        render_resource_field :published_at
        render_resource_field :category
      }

      render_actions
    end
  end
end
```

### Form Methods

| Method | Purpose |
|--------|---------|
| `render_fields` | Render all permitted fields |
| `render_resource_field(name)` | Render a single field |
| `render_actions` | Render submit buttons |
| `record` | The form object (alias: `object`) |
| `resource_fields` | List of permitted field names |
| `resource_definition` | The definition instance |

## Display Customization

### Custom Display Template

Override the show page detail rendering:

```ruby
class PostDefinition < ResourceDefinition
  class Display < Display
    def display_template
      # Hero section
      div(class: "bg-gradient-to-r from-blue-500 to-purple-600 p-8 rounded-lg text-white mb-6") {
        h1(class: "text-3xl font-bold") { object.title }
        p(class: "mt-2 opacity-90") { object.excerpt }
      }

      # Main content
      Block do
        fields_wrapper do
          render_resource_field :author
          render_resource_field :published_at
          render_resource_field :category
        end
      end

      # Full-width content
      Block do
        div(class: "prose max-w-none") {
          raw object.content
        }
      end

      # Associations (tabs)
      render_associations if present_associations?
    end
  end
end
```

### Display Methods

| Method | Purpose |
|--------|---------|
| `render_fields` | Render all permitted fields in a block |
| `render_resource_field(name)` | Render single field |
| `render_associations` | Render association tabs |
| `object` | The record being displayed |
| `resource_fields` | List of permitted field names |
| `resource_associations` | List of permitted associations |

## Table Customization

### Custom Table Rendering

Override list page table:

```ruby
class PostDefinition < ResourceDefinition
  class Table < Table
    def view_template
      render_search_bar
      render_scopes_bar

      if collection.empty?
        render_empty_card
      else
        # Custom card grid instead of table
        div(class: "grid grid-cols-3 gap-4") {
          collection.each do |post|
            render PostCardComponent.new(post:)
          end
        }
      end

      render_footer
    end
  end
end
```

### Table Methods

| Method | Purpose |
|--------|---------|
| `render_search_bar` | Search input |
| `render_scopes_bar` | Scope tabs |
| `render_table` | Default table |
| `render_empty_card` | Empty state |
| `render_footer` | Pagination |
| `collection` | The paginated records |
| `resource_fields` | Column field names |

## Component Kit

Plutonium provides shorthand methods for common components:

```ruby
class MyPage < Plutonium::UI::Page::Base
  def render_content
    # These are automatically rendered
    PageHeader(title: "Dashboard")

    Panel(class: "mt-4") {
      p { "Content here" }
    }

    Block {
      TabList(items: tabs)
    }

    EmptyCard("No items found")

    ActionButton(action, url: "/posts/new")
  end
end
```

Available kit methods:
- `Breadcrumbs()`
- `PageHeader(title:, description:, actions:)`
- `Panel(**attrs)`
- `Block(**attrs)`
- `TabList(items:)`
- `EmptyCard(message)`
- `ActionButton(action, url:)`
- `DynaFrameHost()` / `DynaFrameContent()`
- `TableSearchBar()`
- `TableScopesBar()`
- `TableInfo(pagy)`
- `TablePagination(pagy)`

## Custom Components

### Creating a Phlex Component

```ruby
# app/components/post_card_component.rb
class PostCardComponent < Plutonium::UI::Component::Base
  def initialize(post:)
    @post = post
  end

  def view_template
    div(class: "bg-white rounded-lg shadow p-4") {
      h3(class: "font-bold") { @post.title }
      p(class: "text-gray-600 mt-2") { @post.excerpt }

      div(class: "mt-4 flex justify-between items-center") {
        span(class: "text-sm text-gray-500") { @post.published_at&.strftime("%B %d, %Y") }
        a(href: resource_url_for(@post), class: "text-blue-600") { "Read more" }
      }
    }
  end
end
```

### Using in Definitions

Reference components in field definitions:

```ruby
class PostDefinition < ResourceDefinition
  # Custom display component
  display :status, as: StatusBadgeComponent

  # Custom input component
  input :color, as: ColorPickerComponent

  # Block with component
  display :metrics do |field|
    MetricsChartComponent.new(data: field.value)
  end
end
```

## Layout Customization

### Eject Layout

Copy the layout template to your project:

```bash
rails generate pu:eject:layout
```

This copies `layouts/resource.html.erb` to your portal.

### Custom Layout Class

Override the Phlex layout:

```ruby
# packages/admin_portal/app/views/layouts/admin_portal/resource_layout.rb
module AdminPortal
  class ResourceLayout < Plutonium::UI::Layout::ResourceLayout
    private

    # Custom body classes
    def body_attributes
      {class: "antialiased bg-slate-100 dark:bg-slate-900"}
    end

    # Add custom header content
    def render_before_main
      super
      render AnnouncementBanner.new if Announcement.active.any?
    end

    # Custom scripts
    def render_body_scripts
      super
      script(src: "/custom-analytics.js")
    end
  end
end
```

### Layout Hooks

| Hook | Purpose |
|------|---------|
| `render_before_main` | Before main content area |
| `render_after_main` | After main (modals, etc.) |
| `render_before_content` | Inside main, before content |
| `render_after_content` | Inside main, after content |
| `render_flash` | Flash messages |
| `render_head` | HTML head section |
| `render_title` | Page title tag |
| `render_metatags` | Meta tags |
| `render_assets` | CSS/JS assets |
| `render_body_scripts` | Scripts at end of body |

## Available Context

Both ERB views and Phlex components have access to the same context.

### Resource Methods

| Method | Description |
|--------|-------------|
| `resource_class` | The model class (e.g., `Post`) |
| `resource_record!` | Current record (raises if not found) |
| `resource_record?` | Current record (nil if not found) |
| `current_parent` | Parent record for nested routes |
| `current_scoped_entity` | Entity for multi-tenant portals |

### Definition & Policy

| Method | Description |
|--------|-------------|
| `current_definition` | Definition instance for current resource |
| `current_policy` | Policy instance for current record |
| `current_authorized_scope` | Scoped collection user can access |

### Authentication

| Method | Description |
|--------|-------------|
| `current_user` | Authenticated user (if using Rodauth) |

### URL Helpers

| Method | Description |
|--------|-------------|
| `resource_url_for(record)` | URL for a record |
| `resource_url_for(record, action: :edit)` | Action URL for record |
| `resource_url_for(Model)` | Index URL for model |
| `resource_url_for(Model, action: :new)` | New URL for model |
| `resource_url_for(record, parent: parent)` | Nested resource URL |

### Display Helpers

| Method | Description |
|--------|-------------|
| `display_name_of(record)` | Human-readable name for record |
| `resource_name(klass)` | Singular model name |
| `resource_name_plural(klass)` | Plural model name |

### In Phlex Components

```ruby
class MyComponent < Plutonium::UI::Component::Base
  def view_template
    # All the above methods work directly
    current_user
    resource_record!
    resource_url_for(@post)

    # Rails helpers via helpers proxy
    helpers.link_to(...)
    helpers.image_tag(...)
    helpers.number_to_currency(...)
  end
end
```

### In ERB Views

```erb
<%# All methods available directly %>
<%= resource_record!.title %>
<%= current_user.name %>
<%= link_to "Edit", resource_url_for(resource_record!, action: :edit) %>

<%# Render Phlex components %>
<%= render current_definition.show_page_class.new %>
<%= render MyCustomComponent.new(post: resource_record!) %>
```

## Portal-Specific Views

Each portal can have its own view overrides:

```ruby
# Base definition
class PostDefinition < ResourceDefinition
  class ShowPage < ShowPage
    # Default behavior
  end
end

# Admin portal override
class AdminPortal::PostDefinition < ::PostDefinition
  class ShowPage < ShowPage  # Inherits from ::PostDefinition::ShowPage
    def render_after_content
      super
      render AdminOnlySection.new(post: object)
    end
  end
end
```

## Related Skills

- `forms` - Custom form templates and field builders
- `assets` - TailwindCSS and component theming
- `definition-fields` - Field/input/display configuration
- `definition-actions` - Action buttons and interactions
- `controller` - Presentation hooks (`present_parent?`, etc.)
- `portal` - Portal-specific customization
