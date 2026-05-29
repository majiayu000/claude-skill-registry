---
name: plutonium-resource
description: Overview of Plutonium resources - what they are and how the pieces fit together
---

# Plutonium Resources

A **resource** in Plutonium is the combination of four layers that work together to provide full CRUD functionality with minimal code.

## The Four Layers

| Layer | File | Purpose |
|-------|------|---------|
| **Model** | `app/models/post.rb` | Data, validations, associations, business rules |
| **Definition** | `app/definitions/post_definition.rb` | UI configuration - how fields render, actions, filters |
| **Policy** | `app/policies/post_policy.rb` | Authorization - who can do what |
| **Controller** | `app/controllers/posts_controller.rb` | Request handling - usually empty, inherits CRUD |

```
┌─────────────────────────────────────────────────────────────────┐
│                           Resource                               │
├─────────────────────────────────────────────────────────────────┤
│  Model          │  Definition      │  Policy        │ Controller │
│  (WHAT it is)   │  (HOW it looks)  │  (WHO can act) │ (HOW it    │
│                 │                  │                │  responds)  │
├─────────────────────────────────────────────────────────────────┤
│  - attributes   │  - field types   │  - permissions │ - CRUD     │
│  - associations │  - inputs/forms  │  - scoping     │ - redirects│
│  - validations  │  - displays      │  - attributes  │ - params   │
│  - scopes       │  - actions       │                │            │
│  - callbacks    │  - filters       │                │            │
└─────────────────────────────────────────────────────────────────┘
```

## Creating Resources

### New Resources (from scratch)

Use the scaffold generator to create all four layers at once:

```bash
rails g pu:res:scaffold Post title:string content:text:required published:boolean
```

This generates:
- `app/models/post.rb` - Model with validations
- `app/definitions/post_definition.rb` - Definition (empty, uses auto-detection)
- `app/policies/post_policy.rb` - Policy with sensible defaults
- `app/controllers/posts_controller.rb` - Controller (empty, inherits CRUD)
- Migration file

See `plutonium-create-resource` skill for full generator options.

### From Existing Models

For existing Rails projects, you can convert models to Plutonium resources:

1. **Include the module** in your model:

```ruby
class Post < ApplicationRecord
  include Plutonium::Resource::Record
  # Your existing code...
end
```

Or inherit from a base class that includes it:

```ruby
class Post < ResourceRecord
  # Your existing code...
end
```

2. **Generate the supporting files** (definition, policy, controller):

```bash
rails g pu:res:scaffold Post --no-migration
```

This creates definition, policy, and controller without touching your existing model.

3. **Connect to a portal**:

```bash
rails g pu:res:conn Post --dest=admin_portal
```

## Connecting to Portals

Resources must be connected to a portal to be accessible:

```bash
rails g pu:res:conn Post --dest=admin_portal
```

This:
- Registers the resource in portal routes
- Creates portal-specific controller
- Creates portal-specific policy with attribute permissions

See `plutonium-connect-resource` skill for details.

## Layer Responsibilities

### Model (Data Layer)

```ruby
class Post < ResourceRecord
  belongs_to :author, class_name: "User"
  has_many :comments

  validates :title, presence: true

  scope :published, -> { where(published: true) }
end
```

The model handles:
- Database schema and associations
- Data validation
- Business logic scopes
- Callbacks

**Skills:** `plutonium-model`, `plutonium-model-features`

### Definition (UI Layer)

```ruby
class PostDefinition < ResourceDefinition
  # Override auto-detected field types
  input :content, as: :markdown

  # Add filters and scopes
  filter :published, with: Plutonium::Query::Filters::Boolean
  scope :published

  # Add actions
  action :publish, interaction: PublishPostInteraction
end
```

The definition handles:
- Field type overrides (auto-detection handles most cases)
- Form input customization
- Display formatting
- Search, filters, scopes, sorting
- Actions (interactive operations)

**Skills:** `plutonium-definition`, `plutonium-definition-fields`, `plutonium-definition-actions`, `plutonium-definition-query`

### Policy (Authorization Layer)

```ruby
class PostPolicy < ResourcePolicy
  # Who can perform actions
  def create?
    user.present?
  end

  def read?
    true
  end

  def publish?
    user.admin? || record.author == user
  end

  # What records are visible
  relation_scope do |relation|
    return relation if user.admin?
    relation.where(author: user)
  end

  # What attributes are readable/writable
  def permitted_attributes_for_read
    %i[title content published author created_at]
  end

  def permitted_attributes_for_create
    %i[title content]
  end
end
```

The policy handles:
- Action authorization (create?, update?, destroy?, custom actions)
- Resource scoping (what records user can see)
- Attribute permissions (read/write access per field)

**Skill:** `plutonium-policy`

### Controller (Request Layer)

```ruby
class PostsController < ::ResourceController
  # Empty - all CRUD actions inherited automatically
end
```

Controllers are usually empty because they inherit full CRUD functionality. Customize only when needed:

```ruby
class PostsController < ::ResourceController
  private

  def preferred_action_after_submit
    "index"  # Redirect to list instead of show
  end
end
```

The controller handles:
- Request/response cycle
- Redirect logic
- Custom parameter processing
- Non-standard authorization flows

**Skill:** `plutonium-controller`

## Auto-Detection

Plutonium automatically detects from your model:
- All database columns with appropriate field types
- Associations (belongs_to, has_one, has_many)
- Attachments (Active Storage)
- Enums

**You only need to declare when overriding defaults.**

## Portal-Specific Customization

Each portal can have its own definition that overrides the base:

```ruby
# Base definition
class PostDefinition < ResourceDefinition
  scope :published
end

# Admin portal sees more
class AdminPortal::PostDefinition < ::PostDefinition
  scope :draft
  scope :pending_review
  action :feature, interaction: FeaturePostInteraction
end

# Public portal is restricted
class PublicPortal::PostDefinition < ::PostDefinition
  # Only published scope, no actions
end
```

## Workflow Summary

1. **Generate** - `rails g pu:res:scaffold Model attributes... --dest=main_app`
2. **Connect** - `rails g pu:res:conn Model --dest=portal_name`
3. **Customize** - Edit definition/policy as needed (model rarely needs changes)
4. **Override per portal** - Create portal-specific definitions when needed

## Related Skills

- `plutonium-model` - Model structure and organization
- `plutonium-model-features` - has_cents, associations, scopes, routes
- `plutonium-definition` - Definition overview and structure
- `plutonium-definition-fields` - Fields, inputs, displays, columns
- `plutonium-definition-actions` - Actions and interactions
- `plutonium-interaction` - Writing interaction classes
- `plutonium-definition-query` - Search, filters, scopes, sorting
- `plutonium-policy` - Authorization and permissions
- `plutonium-controller` - Controller customization
- `plutonium-views` - Custom pages, displays, tables using Phlex
- `plutonium-forms` - Custom form templates and field builders
- `plutonium-assets` - TailwindCSS and component theming
- `plutonium-package` - Feature and portal packages
- `plutonium-portal` - Portal configuration and entity scoping
- `plutonium-nested-resources` - Parent/child routes and scoping
- `plutonium-installation` - Setting up Plutonium
- `plutonium-rodauth` - Authentication setup
- `plutonium-create-resource` - Scaffold generator details
- `plutonium-connect-resource` - Portal connection details
