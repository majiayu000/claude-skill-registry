---
name: plutonium-connect-resource
description: Connect existing resources to portals for web access
---

# Connect Resource Skill

Use the `pu:res:conn` generator to connect resources to portals. This is required to expose resources through a portal's web interface.

## Command Syntax

```bash
rails g pu:res:conn RESOURCE [RESOURCE...] --dest=PORTAL_NAME
```

**Always specify resources directly** - this avoids interactive prompts. The `--src` option is only needed for interactive mode and can be ignored.

## Usage Patterns

### Main App Resources (not in a package)

```bash
rails g pu:res:conn PropertyAmenity --dest=admin_portal
rails g pu:res:conn Post Comment Tag --dest=dashboard_portal
```

### Namespaced Resources (from a feature package)

Use the full class name:

```bash
rails g pu:res:conn Blogging::Post --dest=admin_portal
rails g pu:res:conn Blogging::Post Blogging::Comment --dest=admin_portal
```

### Multiple Resources at Once

```bash
rails g pu:res:conn Property PropertyAmenity Unit Tenant --dest=admin_portal
```

## What Gets Generated

For a resource `Post` connected to `admin_portal`:

```
packages/admin_portal/
├── app/
│   ├── controllers/admin_portal/
│   │   └── posts_controller.rb      # Portal controller
│   ├── policies/admin_portal/
│   │   └── post_policy.rb           # Portal policy (if needed)
│   └── definitions/admin_portal/
│       └── post_definition.rb       # Portal definition (if needed)
└── config/
    └── routes.rb                    # Updated with register_resource
```

### Generated Controller

```ruby
class AdminPortal::PostsController < ::PostsController
  include AdminPortal::Concerns::Controller
end
```

### Generated Policy

```ruby
class AdminPortal::PostPolicy < ::PostPolicy
  include AdminPortal::ResourcePolicy

  def permitted_attributes_for_create
    [:title, :content, :user_id]
  end

  def permitted_attributes_for_read
    [:title, :content, :user_id, :created_at, :updated_at]
  end

  def permitted_associations
    %i[]
  end
end
```

### Route Registration

```ruby
# In packages/admin_portal/config/routes.rb
register_resource ::Post
```

## Typical Workflow

```bash
# 1. Create resources (always specify --dest)
rails g pu:res:scaffold Post user:belongs_to title:string 'content:text?' --dest=main_app

# 2. Run migrations
rails db:migrate

# 3. Connect resources to portal (always specify --dest)
rails g pu:res:conn Post --dest=admin_portal
```

## Important Notes

1. **Always specify resources directly** - avoids prompts, no `--src` needed
2. **Always use the generator** - never manually connect resources
3. **Run after migrations** - the generator reads model columns for policy attributes
4. **Portal-specific customization** - customize the generated policy/definition per-portal
