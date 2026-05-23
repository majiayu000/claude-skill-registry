---
name: plutonium-nested-resources
description: Plutonium nested resources - parent/child routes, scoping, and URL generation
---

# Nested Resources

Plutonium automatically creates nested routes for `has_many` associations, scopes queries to the parent, and handles URL generation.

## How It Works

When you register resources with parent-child relationships:

```ruby
# In portal routes
register_resource ::Company
register_resource ::Property  # has belongs_to :company
```

Plutonium automatically creates nested routes:
- `/companies/:company_id/properties` - Properties scoped to company
- `/companies/:company_id/properties/new` - New property for company
- `/companies/:company_id/properties/:id` - Property in company context

## Automatic Behavior

When accessing nested routes, Plutonium automatically:

1. **Resolves the parent** via `current_parent`
2. **Scopes queries** to only show records belonging to parent
3. **Assigns parent** to new records on create
4. **Hides parent field** in forms (already determined by URL)
5. **Authorizes parent access** before proceeding

## Controller Methods

### current_parent

Returns the parent record from the URL:

```ruby
# URL: /companies/123/properties
current_parent  # => Company.find(123)
```

### parent_route_param

The URL parameter containing the parent ID:

```ruby
parent_route_param  # => :company_id
```

### parent_input_param

The association name on the child model:

```ruby
parent_input_param  # => :company
```

## Presentation Hooks

Control whether parent field appears in views/forms:

```ruby
class PropertiesController < ResourceController
  private

  # Show parent field in displays (default: false)
  def present_parent?
    true
  end

  # Allow changing parent in forms (default: same as present_parent?)
  def submit_parent?
    false  # Parent is set from URL, don't allow changing
  end
end
```

## Query Scoping

Collections are automatically scoped to the parent via policies:

```ruby
class PropertyPolicy < ResourcePolicy
  relation_scope do |relation|
    relation = super(relation)  # Applies associated_with(entity_scope)
    # entity_scope is the current_parent
    relation
  end
end
```

The `associated_with` scope finds records belonging to the parent:

```ruby
# Automatic detection via belongs_to
Property.associated_with(company)
# => Property.where(company: company)
```

### Custom Association Scope

For complex relationships, define a custom scope:

```ruby
class Property < ResourceRecord
  scope :associated_with_organization, ->(org) {
    joins(:company).where(companies: { organization_id: org.id })
  }
end
```

## URL Generation

Use `resource_url_for` with the `parent:` option:

```ruby
# Child collection
resource_url_for(Property, parent: company)
# => /companies/123/properties

# Child record
resource_url_for(property, parent: company)
# => /companies/123/properties/456

# New child form
resource_url_for(Property, action: :new, parent: company)
# => /companies/123/properties/new

# Edit child
resource_url_for(property, action: :edit, parent: company)
# => /companies/123/properties/456/edit
```

## Association Panels

On the parent's show page, child resources are displayed via association panels:

```ruby
class CompanyPolicy < ResourcePolicy
  def permitted_associations
    %i[properties contacts]  # Shows panels for these
  end
end
```

The panel loads children via the nested route automatically.

## Authorization

### Parent Authorization

The parent is authorized for `:read?` before `current_parent` returns:

```ruby
def current_parent
  # ... resolution logic ...
  authorize! parent, to: :read?
  parent
end
```

### Policy Context

The parent is passed to child policies as `entity_scope`:

```ruby
class PropertyPolicy < ResourcePolicy
  def create?
    # entity_scope is the parent company
    entity_scope.present? && user.member_of?(entity_scope)
  end

  def read?
    entity_scope.present? && record.company == entity_scope
  end
end
```

## Parameter Handling

Parent is automatically injected into resource params:

```ruby
# When creating a property under /companies/123/properties
resource_params
# => { name: "...", company: <Company:123>, company_id: 123 }
```

You don't need to include hidden fields for the parent in forms.

## Nesting Limitations

Plutonium supports **one level of nesting**:

- ✅ `/companies/:company_id/properties` (parent → child)
- ❌ `/companies/:company_id/properties/:property_id/units` (grandparent → parent → child)

## Common Patterns

### Scoped Uniqueness

Validate uniqueness within parent:

```ruby
class Property < ResourceRecord
  belongs_to :company
  validates :code, uniqueness: { scope: :company_id }
end
```

### Conditional Parent Display

Show parent only in certain contexts:

```ruby
class PropertiesController < ResourceController
  private

  def present_parent?
    # Show parent when accessed standalone, hide when nested
    current_parent.nil?
  end
end
```

### Custom Parent Resolution

Override parent lookup:

```ruby
class PropertiesController < ResourceController
  private

  def current_parent
    @current_parent ||= Company.friendly.find(params[:company_id])
  end
end
```

### Breadcrumbs

Breadcrumbs automatically include the parent:

```
Companies > Acme Corp > Properties > Property #123
```

## Route Registration with Custom Routes

Add custom member/collection routes to nested resources:

```ruby
register_resource ::Property do
  member do
    get :analytics
    post :archive
  end
end
```

Generates nested routes:
- `/companies/:company_id/properties/:id/analytics`
- `/companies/:company_id/properties/:id/archive`

## Related Skills

- `plutonium-portal` - Route registration
- `plutonium-policy` - Authorization and scoping
- `plutonium-controller` - Presentation hooks
- `plutonium-model-features` - associated_with scope
