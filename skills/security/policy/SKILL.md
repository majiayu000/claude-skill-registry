---
name: plutonium-policy
description: Plutonium resource policies - authorization, attribute permissions, and scoping
---

# Plutonium Policies

Policies control WHO can do WHAT with resources. Built on [ActionPolicy](https://actionpolicy.evilmartians.io/).

Plutonium extends ActionPolicy with:
- Attribute permissions (`permitted_attributes_for_*`)
- Association permissions (`permitted_associations`)
- Automatic entity scoping for multi-tenancy
- Derived action methods (e.g., `update?` inherits from `create?`)

## Base Class

```ruby
# app/policies/resource_policy.rb (generated during install)
class ResourcePolicy < Plutonium::Resource::Policy
  # App-wide authorization defaults
end

# app/policies/post_policy.rb (per resource)
class PostPolicy < ResourcePolicy
  def create?
    user.present?
  end

  def read?
    true
  end

  def permitted_attributes_for_create
    %i[title content]
  end

  def permitted_attributes_for_read
    %i[title content author created_at]
  end
end
```

## Action Permissions

### Core Actions (Must Override)

```ruby
def create?  # Default: false - MUST override
  user.present?
end

def read?    # Default: false - MUST override
  true
end
```

### Derived Actions (Inherit by Default)

| Method | Inherits From | Override When |
|--------|---------------|---------------|
| `update?` | `create?` | Different update rules |
| `destroy?` | `create?` | Different delete rules |
| `index?` | `read?` | Custom listing rules |
| `show?` | `read?` | Record-specific read rules |
| `new?` | `create?` | Rarely needed |
| `edit?` | `update?` | Rarely needed |
| `search?` | `index?` | Search-specific rules |

### Custom Actions

Define methods matching your action names:

```ruby
def publish?
  update? && record.draft?
end

def archive?
  create? && !record.archived?
end

def invite_user?
  user.admin?
end
```

Actions are secure by default - undefined methods return `false`.

### Bulk Action Authorization

Bulk actions (operating on multiple selected records) support **per-record authorization**:

```ruby
def bulk_archive?
  create? && !record.locked?  # Per-record check
end

def bulk_publish?
  user.admin? || record.author == user
end
```

**How bulk authorization works:**
1. Policy method (e.g., `bulk_archive?`) is checked **per record** in the selection
2. **Backend:** If any selected record fails authorization, the entire request is rejected
3. **UI:** Only actions that **all** selected records support are shown (intersection)
4. Records are fetched via `current_authorized_scope` - only accessible records can be selected

This provides full per-record authorization while keeping the UI clean - users only see actions they can actually perform on their entire selection.

## Attribute Permissions

### Core Methods (Must Override for Production)

```ruby
# What users can see (index, show)
def permitted_attributes_for_read
  %i[title content author published_at created_at]
end

# What users can set (create, update)
def permitted_attributes_for_create
  %i[title content]
end
```

### Derived Methods (Inherit by Default)

| Method | Inherits From |
|--------|---------------|
| `permitted_attributes_for_update` | `permitted_attributes_for_create` |
| `permitted_attributes_for_index` | `permitted_attributes_for_read` |
| `permitted_attributes_for_show` | `permitted_attributes_for_read` |
| `permitted_attributes_for_new` | `permitted_attributes_for_create` |
| `permitted_attributes_for_edit` | `permitted_attributes_for_update` |

### Per-Action Attributes

Show different fields for different views:

```ruby
def permitted_attributes_for_index
  %i[title author created_at]  # Minimal for list
end

def permitted_attributes_for_read
  %i[title content author tags created_at updated_at]  # Full for detail
end
```

### Auto-Detection (Development Only)

In development, undefined attribute methods auto-detect from the model. This raises errors in production - always define explicitly.

## Association Permissions

Control which associations can be rendered:

```ruby
def permitted_associations
  %i[comments tags author]
end
```

Used for:
- Nested forms
- Related data displays
- Association fields in tables

## Collection Scoping

Filter which records users can see:

```ruby
relation_scope do |relation|
  if user.admin?
    relation
  else
    relation.where(author: user)
  end
end
```

### With Entity Scoping

Call `super` to preserve automatic entity scoping:

```ruby
relation_scope do |relation|
  relation = super(relation)  # Apply entity scope first

  if user.admin?
    relation
  else
    relation.where(published: true)
  end
end
```

## Portal-Specific Policies

Override policies per portal:

```ruby
# Base policy
class PostPolicy < ResourcePolicy
  def create?
    user.present?
  end
end

# Admin portal - more permissive
class AdminPortal::PostPolicy < ::PostPolicy
  include AdminPortal::ResourcePolicy

  def destroy?
    true  # Admins can always delete
  end

  def permitted_attributes_for_create
    %i[title content featured internal_notes]  # More fields
  end
end

# Public portal - restricted
class PublicPortal::PostPolicy < ::PostPolicy
  include PublicPortal::ResourcePolicy

  def create?
    false  # No public creation
  end
end
```

## Common Patterns

### Check Model Capabilities

```ruby
def archive?
  return false unless record.respond_to?(:archived!)
  return false if record.archived?

  user.admin?
end
```

### Prevent Actions on Archived Records

```ruby
def update?
  return false if record.try(:archived?)
  super
end

def destroy?
  return false if record.try(:archived?)
  super
end
```

### Owner-Based Permissions

```ruby
def update?
  record.author == user || user.admin?
end

def destroy?
  update?  # Same rules as update
end
```

### Role-Based Permissions

```ruby
def create?
  user.admin? || user.editor?
end

def read?
  true  # Everyone can read
end

def update?
  return true if user.admin?
  return true if user.editor? && record.author == user
  false
end
```

### Conditional Attribute Access

```ruby
def permitted_attributes_for_create
  attrs = %i[title content]
  attrs << :featured if user.admin?
  attrs << :author_id if user.admin?  # Only admins can set author
  attrs
end
```

## Authorization Context

Policies have access to:

```ruby
user         # Current user (required)
record       # The resource being authorized
entity_scope # Current scoped entity (for multi-tenancy)
```

### Custom Context

Add custom context in controllers:

```ruby
# In policy
class PostPolicy < ResourcePolicy
  authorize :department, allow_nil: true

  def create?
    department&.allows_posting?
  end
end

# In controller
class PostsController < ResourceController
  authorize :department, through: :current_department

  private

  def current_department
    current_user.department
  end
end
```

## Controller Integration

Built-in CRUD actions automatically:
- Call `authorize_current!` at the start of each action
- Apply `relation_scope` for index/listings
- Filter params through `permitted_attributes`

After-action callbacks verify authorization was performed - if you add custom actions, you must call `authorize_current!` yourself or skip verification.

### Skip Verification (When Needed)

```ruby
class PostsController < ResourceController
  skip_verify_authorize_current only: [:custom_action]

  def custom_action
    # Handle authorization manually
  end
end
```

## Best Practices

1. **Always override `create?` and `read?`** - They default to `false`
2. **Define attributes explicitly** - Auto-detection only works in development
3. **Call `super` in `relation_scope`** - Preserves entity scoping
4. **Use derived methods** - Let `update?` inherit from `create?` when appropriate
5. **Keep policies focused** - Authorization logic only, no business logic
6. **Test edge cases** - Archived records, nil associations, role combinations

## Related Skills

- `plutonium-resource` - How policies fit in the resource architecture
- `plutonium-definition-actions` - Actions that need policy methods
- `plutonium-controller` - How controllers use policies
