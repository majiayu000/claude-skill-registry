---
name: plutonium-definition
description: Overview of Plutonium resource definitions - structure, inheritance, and best practices
---

# Definition Overview

Resource definitions configure **HOW** resources are rendered and interacted with. They are the central configuration point for UI behavior in Plutonium applications.

## Key Principle

**All model attributes are auto-detected** - you only declare when overriding defaults.

## File Location

- Main app: `app/definitions/model_name_definition.rb`
- Packages: `packages/pkg_name/app/definitions/pkg_name/model_name_definition.rb`

## Definition Structure

```ruby
class PostDefinition < Plutonium::Resource::Definition
  # Fields, inputs, displays, columns (see definition-fields skill)
  field :content, as: :markdown
  input :title, hint: "Be descriptive"
  display :content, as: :markdown
  column :title, align: :center

  # Search, filters, scopes, sorting (see definition-query skill)
  search { |scope, q| scope.where("title ILIKE ?", "%#{q}%") }
  filter :status, with: Plutonium::Query::Filters::Text, predicate: :eq
  scope :published
  sort :created_at

  # Actions (see definition-actions skill)
  action :publish, interaction: PublishInteraction
end
```

## Definition Hierarchy

Definitions exist at multiple levels:

### Main App (created by generators)

```ruby
# app/definitions/resource_definition.rb (base - created during install)
class ResourceDefinition < Plutonium::Resource::Definition
  action :archive, interaction: ArchiveInteraction, color: :danger, position: 1000
end

# app/definitions/post_definition.rb (resource-specific - created by scaffold)
class PostDefinition < ResourceDefinition
  scope :published
  input :content, as: :markdown
end
```

### Portal-Specific Overrides

After connecting a resource to a portal, you can create a portal-specific definition to override defaults for that portal only:

```ruby
# packages/admin_portal/app/definitions/admin_portal/post_definition.rb
class AdminPortal::PostDefinition < ::PostDefinition
  # Override or extend for admin portal only
  input :internal_notes, as: :text  # Only admins see this field
  scope :pending_review             # Admin-specific scope
end
```

This lets you:
- Show different fields per portal
- Add portal-specific actions
- Customize search/filters per context
- Keep main app definition clean

## Separation of Concerns

| Layer | Purpose | Example |
|-------|---------|---------|
| **Definition** | HOW fields render | `input :content, as: :markdown` |
| **Policy** | WHAT is visible/editable | `permitted_attributes_for_read` |
| **Interaction** | Business logic | `resource.update!(state: :archived)` |

## Auto-Detection

Plutonium automatically detects from your model:
- Database columns (string, text, integer, boolean, datetime, etc.)
- Associations (belongs_to, has_many, has_one)
- Active Storage/Active Shrine attachments (has_one_attached, has_many_attached)
- Enums
- Virtual attributes (with accessor methods)

**Only declare fields when you need to override the auto-detected behavior.**

## When to Declare

```ruby
class PostDefinition < ResourceDefinition
  # 1. Override auto-detected type
  field :content, as: :markdown      # text -> rich_text
  input :published_at, as: :date      # datetime -> date only

  # 2. Add custom options
  input :title, hint: "Be descriptive", placeholder: "Enter title"

  # 3. Configure select choices
  input :category, as: :select, choices: %w[Tech Business]

  # 4. Add conditional logic
  display :published_at, condition: -> { object.published? }

  # 5. Custom rendering
  display :status do |field|
    StatusBadgeComponent.new(value: field.value)
  end
end
```

## Minimal Definition Example

```ruby
class PostDefinition < ResourceDefinition
  # No field declarations needed - all auto-detected!

  # Only customize what you need:
  input :content, as: :markdown
  display :content, as: :markdown

  scope :published
  scope :draft
end
```

## Runtime Customization Hooks

Override these methods for dynamic behavior:

```ruby
class PostDefinition < ResourceDefinition
  def customize_fields
    field :debug_info if Rails.env.development?
  end

  def customize_inputs
    # Add/modify inputs at runtime
  end

  def customize_displays
    # Add/modify displays at runtime
  end

  def customize_filters
    # Add/modify filters at runtime
  end

  def customize_actions
    # Add/modify actions at runtime
  end
end
```

## Context Availability

| Context | current_user | object | current_parent |
|---------|-------------|--------|----------------|
| Definition file (class level) | No | No | No |
| `condition` procs | Yes | Yes | Yes |
| `input` blocks | Yes | Yes | Yes |
| Page title procs | Yes | Yes (current_record!) | Yes |

## Page Customization

```ruby
class PostDefinition < ResourceDefinition
  # Titles (static or dynamic)
  index_page_title "All Posts"
  show_page_title -> { "#{current_record!.title} - Details" }

  # Breadcrumbs
  breadcrumbs true
  show_page_breadcrumbs false

  # Custom page classes (inherit from parent's nested class)
  class IndexPage < IndexPage
    def view_template(&block)
      div(class: "custom-header") { h1 { "Custom" } }
      super(&block)
    end
  end

  class Form < Form
    def form_template
      div(class: "grid grid-cols-2") do
        render field(:title).input_tag
        render field(:content).easymde_tag
      end
      render_actions
    end
  end
end
```

## Best Practices

1. **Let auto-detection work** - Don't declare unless overriding
2. **Use portal-specific definitions** - Override per-portal when needed
3. **Keep definitions focused** - Configuration only, no business logic
4. **Use policies for authorization** - Not `condition` procs
5. **Group related declarations** - Use comments to organize sections

## Related Skills

- `plutonium-definition-fields` - Fields, inputs, displays, columns
- `plutonium-definition-actions` - Actions and interactions
- `plutonium-definition-query` - Search, filters, scopes, sorting
- `plutonium-views` - Custom page, form, display, and table classes
