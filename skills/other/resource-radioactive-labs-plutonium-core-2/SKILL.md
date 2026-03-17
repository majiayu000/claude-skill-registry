---
name: plutonium-nested-resources
description: Plutonium nested resources - parent/child routes, scoping, and URL generation
---

# Nested Resources

Plutonium automatically creates nested routes for `has_many` and `has_one` associations, scopes queries to the parent, and handles URL generation.

## How It Works

When you register resources with parent-child relationships:

```ruby
# In portal routes
register_resource ::Company
register_resource ::Property  # has belongs_to :company
register_resource ::CompanyProfile  # has belongs_to :company (has_one on Company)
```

Plutonium automatically creates nested routes with a `nested_` prefix:
- `/companies/:company_id/nested_properties` - Properties scoped to company (has_many)
- `/companies/:company_id/nested_properties/new` - New property for company
- `/companies/:company_id/nested_properties/:id` - Property in company context
- `/companies/:company_id/nested_company_profile` - Singular profile (has_one)
- `/companies/:company_id/nested_company_profile/new` - New profile for company

The `nested_` prefix prevents route conflicts when the same resource is registered both as a top-level and nested resource.

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

Collections are automatically scoped to the parent via policies. The policy receives `parent` and `parent_association` context:

```ruby
class PropertyPolicy < ResourcePolicy
  # parent: the parent record (e.g., Company instance)
  # parent_association: the association name (e.g., :properties)

  relation_scope do |relation|
    relation = super(relation)  # Applies parent scoping automatically
    relation
  end
end
```

### How Parent Scoping Works

For **has_many** associations, scoping uses the association directly:
```ruby
# parent.properties => Company#properties
parent.send(parent_association)
```

For **has_one** associations, scoping uses a where clause:
```ruby
# Property.where(company_id: company.id) with limit
relation.where(foreign_key => parent.id)
```

### Parent vs Entity Scope

When a parent is present, parent scoping takes precedence over entity scoping:

```ruby
# With parent: scopes via parent association
# Without parent: falls back to entity_scope (multi-tenancy)
```

This prevents double-scoping - the parent was already authorized and entity-scoped during its own authorization.

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
# Child collection (has_many)
resource_url_for(Property, parent: company)
# => /companies/123/nested_properties

# Child record
resource_url_for(property, parent: company)
# => /companies/123/nested_properties/456

# New child form
resource_url_for(Property, action: :new, parent: company)
# => /companies/123/nested_properties/new

# Edit child
resource_url_for(property, action: :edit, parent: company)
# => /companies/123/nested_properties/456/edit

# Singular resource (has_one)
resource_url_for(company_profile, parent: company)
# => /companies/123/nested_company_profile

resource_url_for(CompanyProfile, action: :new, parent: company)
# => /companies/123/nested_company_profile/new
```

### Cross-Package URL Generation

Generate URLs for resources in a different package:

```ruby
# From AdminPortal, generate URL to CustomerPortal resource
resource_url_for(property, parent: company, package: CustomerPortal)
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

## has_one Associations

Plutonium supports both `has_many` and `has_one` associations:

```ruby
class Company < ResourceRecord
  has_many :properties           # Plural routes
  has_one :company_profile       # Singular routes
end
```

Routes generated:
- `has_many`: `/companies/:id/nested_properties` (plural, with `:id` param)
- `has_one`: `/companies/:id/nested_company_profile` (singular, no `:id` param)

For has_one associations:
- Index redirects to show (or new if no record exists)
- Only one record can exist per parent
- Forms don't show parent field (determined by URL)

## Nesting Limitations

Plutonium supports **one level of nesting**:

- ✅ `/companies/:company_id/nested_properties` (parent → child)
- ❌ `/companies/:company_id/nested_properties/:property_id/nested_units` (grandparent → parent → child)

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
    get :analytics, as: :analytics
    post :archive, as: :archive
  end
end
```

**Important:** Always use the `as:` option to name custom routes. This ensures `resource_url_for` can generate correct URLs for nested resources. Without named routes, URL generation will fail.

Generates nested routes:
- `/companies/:company_id/nested_properties/:id/analytics`
- `/companies/:company_id/nested_properties/:id/archive`

## Related Skills

- `plutonium-portal` - Route registration
- `plutonium-policy` - Authorization and scoping
- `plutonium-controller` - Presentation hooks
- `plutonium-model-features` - associated_with scope
