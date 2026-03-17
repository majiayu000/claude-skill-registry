---
name: plutonium-forms
description: Plutonium forms - custom templates, Phlex form components, field builders, and theming
---

# Plutonium Forms

Plutonium forms are built on [Phlexi::Form](https://github.com/radioactive-labs/phlexi-form), providing a Ruby-first approach to form building with Phlex components.

## Form Class Hierarchy

```
Phlexi::Form::Base
└── Plutonium::UI::Form::Base       # Base with Plutonium components
    ├── Plutonium::UI::Form::Resource   # Resource CRUD forms
    │   └── Plutonium::UI::Form::Interaction  # Interactive action forms
    └── Plutonium::UI::Form::Query      # Search/filter forms
```

## Customizing Resource Forms

### Override in Definition

```ruby
class PostDefinition < ResourceDefinition
  class Form < Form
    def form_template
      # Your custom form layout
      render_fields
      render_actions
    end
  end
end
```

### Form Template Methods

| Method | Description |
|--------|-------------|
| `form_template` | Main template method to override |
| `render_fields` | Render all permitted fields |
| `render_resource_field(name)` | Render a single field by name |
| `render_actions` | Render submit buttons |
| `fields_wrapper { }` | Wrapper div for field grid |
| `actions_wrapper { }` | Wrapper div for buttons |

### Form Attributes

| Attribute | Description |
|-----------|-------------|
| `object` / `record` | The form object being edited |
| `resource_fields` | Array of permitted field names |
| `resource_definition` | The definition instance |

## Custom Form Layout

### Sectioned Form

```ruby
class PostDefinition < ResourceDefinition
  class Form < Form
    def form_template
      section("Basic Information") {
        render_resource_field :title
        render_resource_field :slug
      }

      section("Content") {
        render_resource_field :content
        render_resource_field :excerpt
      }

      section("Publishing") {
        render_resource_field :published_at
        render_resource_field :category
      }

      render_actions
    end

    private

    def section(title, &)
      div(class: "mb-8") {
        h3(class: "text-lg font-semibold mb-4 text-gray-900 dark:text-white") { title }
        fields_wrapper(&)
      }
    end
  end
end
```

### Two-Column Layout

```ruby
class Form < Form
  def form_template
    div(class: "grid grid-cols-1 lg:grid-cols-3 gap-6") {
      # Main content - 2 columns
      div(class: "lg:col-span-2") {
        fields_wrapper {
          render_resource_field :title
          render_resource_field :content
        }
      }

      # Sidebar - 1 column
      div(class: "space-y-4") {
        Panel {
          h4(class: "font-medium mb-2") { "Settings" }
          render_resource_field :status
          render_resource_field :visibility
        }
      }
    }

    render_actions
  end
end
```

## Field Builder

When using `render_resource_field`, Plutonium uses the field builder. For custom rendering, use the `field` method directly.

### Basic Field Usage

```ruby
def form_template
  # Using field builder directly
  render field(:title).wrapped {|f| f.input_tag }
  render field(:content).wrapped {|f| f.easymde_tag }
  render field(:published).wrapped {|f| f.checkbox_tag }

  render_actions
end
```

### Field Builder Methods

The field builder (`f`) provides these tag methods:

| Method | Input Type |
|--------|------------|
| `f.input_tag` | Text input (auto-detects type) |
| `f.string_tag` | Text input |
| `f.text_tag` | Textarea |
| `f.number_tag` | Number input |
| `f.email_tag` | Email input |
| `f.password_tag` | Password input |
| `f.url_tag` | URL input |
| `f.tel_tag` | Telephone input |
| `f.hidden_tag` | Hidden input |
| `f.checkbox_tag` | Checkbox |
| `f.select_tag` | Select dropdown |
| `f.radio_button_tag` | Radio buttons |

### Plutonium-Enhanced Tags

| Method | Description |
|--------|-------------|
| `f.easymde_tag` / `f.markdown_tag` | Markdown editor (EasyMDE) |
| `f.slim_select_tag` | Enhanced select (Slim Select) |
| `f.flatpickr_tag` | Date/time picker (Flatpickr) |
| `f.phone_tag` / `f.int_tel_input_tag` | International phone input |
| `f.uppy_tag` / `f.file_tag` | File upload (Uppy) |
| `f.secure_association_tag` | Association with authorization |
| `f.belongs_to_tag` | Belongs-to association |
| `f.has_many_tag` | Has-many association |
| `f.has_one_tag` | Has-one association |
| `f.key_value_store_tag` | Key-value pairs |

### Field with Options

```ruby
# Select with choices
render field(:status).wrapped { |f|
  f.select_tag(choices: %w[draft published archived])
}

# Date picker with options
render field(:published_at).wrapped { |f|
  f.flatpickr_tag(min_date: Date.today, enable_time: true)
}

# File upload with restrictions
render field(:avatar).wrapped { |f|
  f.uppy_tag(
    allowed_file_types: %w[.jpg .png .gif],
    max_file_size: 5.megabytes
  )
}
```

### Wrapped vs Unwrapped

```ruby
# Wrapped - includes label, hint, errors
render field(:title).wrapped { |f| f.input_tag }

# Unwrapped - just the input element
render field(:title).input_tag

# Custom wrapper options
render field(:title).wrapped(class: "col-span-full") { |f|
  f.input_tag
}
```

## Input Configuration in Definitions

Define inputs in the definition, render them in the form:

```ruby
class PostDefinition < ResourceDefinition
  # Configure inputs
  input :title, hint: "Be descriptive", placeholder: "Enter title"
  input :content, as: :markdown
  input :status, as: :select, choices: %w[draft published]
  input :published_at, as: :flatpickr

  # Custom input with block
  input :category do |f|
    choices = Category.active.pluck(:name, :id)
    f.select_tag(choices: choices)
  end

  class Form < Form
    def form_template
      # render_resource_field uses the input configuration
      render_resource_field :title
      render_resource_field :content
      render_resource_field :status
      render_resource_field :published_at
      render_resource_field :category

      render_actions
    end
  end
end
```

## Dynamic Forms (pre_submit)

Fields with `pre_submit: true` trigger form re-rendering on change:

```ruby
class PostDefinition < ResourceDefinition
  input :post_type, as: :select,
    choices: %w[article video podcast],
    pre_submit: true

  input :video_url,
    condition: -> { object.post_type == "video" }

  input :podcast_url,
    condition: -> { object.post_type == "podcast" }
end
```

When `post_type` changes, the form re-renders via Turbo and shows/hides conditional fields.

## Nested Forms

For `has_many` / `has_one` associations with `accepts_nested_attributes_for`:

### Model Setup

```ruby
class Post < ResourceRecord
  has_many :comments
  accepts_nested_attributes_for :comments, allow_destroy: true
end
```

### Definition Setup

```ruby
class PostDefinition < ResourceDefinition
  nested_input :comments do |n|
    n.input :author_name
    n.input :body, as: :text
  end

  # Or reference another definition
  nested_input :comments, using: CommentDefinition, fields: %i[author_name body]
end
```

### Custom Nested Rendering

```ruby
class Form < Form
  def form_template
    render_resource_field :title
    render_resource_field :content

    # Nested fields are automatically handled
    render_resource_field :comments

    render_actions
  end
end
```

## Interaction Forms

Forms for interactive actions use `Plutonium::UI::Form::Interaction`:

```ruby
class PublishPostInteraction < ResourceInteraction
  attribute :publish_date, :date
  attribute :notify_subscribers, :boolean, default: true

  # Custom form
  class Form < Form
    def form_template
      div(class: "space-y-4") {
        render_resource_field :publish_date
        render_resource_field :notify_subscribers
      }
      render_actions
    end
  end
end
```

## Form Actions

### Default Actions

```ruby
def render_actions
  actions_wrapper {
    # "Create and add another" / "Update and continue editing" button
    # Primary submit button
    render submit_button
  }
end
```

### Custom Actions

```ruby
def render_actions
  actions_wrapper {
    # Cancel link
    a(href: resource_url_for(resource_class), class: "btn btn-secondary") {
      "Cancel"
    }

    # Save as draft
    button(type: :submit, name: "draft", value: "1", class: "btn") {
      "Save Draft"
    }

    # Primary submit
    render submit_button
  }
end
```

## Form Context

Inside form templates, you have access to:

```ruby
class Form < Form
  def form_template
    # Form object
    object              # The record
    record              # Alias for object
    object.new_record?  # Check if creating

    # Request context
    current_user
    current_parent
    current_scoped_entity
    request
    params

    # Definition
    resource_definition
    resource_fields     # Permitted fields

    # URL helpers
    resource_url_for(object)
    resource_url_for(Post, action: :new)

    # Rails helpers
    helpers.link_to(...)
  end
end
```

## Theming

Forms use a theme system for consistent styling:

```ruby
class PostDefinition < ResourceDefinition
  class Form < Form
    class Theme < Plutonium::UI::Form::Theme
      def self.theme
        super.merge({
          fields_wrapper: "grid grid-cols-2 gap-6",
          actions_wrapper: "flex justify-between mt-8",
          input: "w-full p-3 border-2 rounded-lg",
          label: "block mb-1 font-bold text-gray-700"
        })
      end
    end
  end
end
```

### Theme Keys

| Key | Description |
|-----|-------------|
| `base` | Form container |
| `fields_wrapper` | Grid wrapper for fields |
| `actions_wrapper` | Wrapper for buttons |
| `wrapper` | Individual field wrapper |
| `label` | Label styling |
| `input` | Input styling |
| `hint` | Hint text styling |
| `error` | Error message styling |
| `button` | Submit button styling |
| `checkbox` | Checkbox styling |
| `select` | Select styling |

## Related Skills

- `plutonium-definition-fields` - Input configuration (as:, hint:, condition:)
- `plutonium-views` - Custom page classes
- `plutonium-assets` - TailwindCSS and component theming
- `plutonium-interaction` - Interactive action forms
- `plutonium-nested-resources` - Parent/child forms
