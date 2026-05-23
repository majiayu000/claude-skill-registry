---
name: plutonium-package
description: Plutonium packages - modular Rails engines for organizing features and portals
---

# Plutonium Packages

Packages are specialized Rails engines for organizing code. There are two types:

| Type | Purpose | Generator |
|------|---------|-----------|
| **Feature** | Business logic (models, policies, interactions) | `rails g pu:pkg:package NAME` |
| **Portal** | Web interface (controllers, views, auth) | `rails g pu:pkg:portal NAME` |

## Feature Packages

Contain domain logic without web interface:

```bash
rails g pu:pkg:package blogging
```

### Structure

```
packages/blogging/
├── app/
│   ├── models/blogging/
│   │   ├── post.rb
│   │   └── comment.rb
│   ├── definitions/blogging/
│   │   ├── post_definition.rb
│   │   └── comment_definition.rb
│   ├── policies/blogging/
│   │   ├── post_policy.rb
│   │   └── comment_policy.rb
│   └── interactions/blogging/
│       └── publish_post_interaction.rb
├── db/migrate/
└── lib/
    └── engine.rb
```

### Engine

```ruby
module Blogging
  class Engine < Rails::Engine
    include Plutonium::Package::Engine
  end
end
```

### Namespacing

All classes are auto-namespaced:
- `app/models/blogging/post.rb` → `Blogging::Post`
- `app/policies/blogging/post_policy.rb` → `Blogging::PostPolicy`

## Portal Packages

Provide web interfaces for specific user types:

```bash
rails g pu:pkg:portal admin
rails g pu:pkg:portal dashboard
```

### Structure

```
packages/admin_portal/
├── app/
│   ├── controllers/admin_portal/
│   │   ├── concerns/controller.rb
│   │   ├── dashboard_controller.rb
│   │   ├── plutonium_controller.rb
│   │   └── resource_controller.rb
│   ├── definitions/admin_portal/     # Portal-specific overrides
│   ├── policies/admin_portal/        # Portal-specific overrides
│   └── views/
│       └── layouts/admin_portal.html.erb
├── config/
│   └── routes.rb
└── lib/
    └── engine.rb
```

### Engine

```ruby
module AdminPortal
  class Engine < Rails::Engine
    include Plutonium::Portal::Engine

    config.after_initialize do
      # Optional: multi-tenancy
      scope_to_entity Organization, strategy: :path
    end
  end
end
```

See `plutonium-portal` skill for portal-specific features.

## Package Loading

Packages are loaded via `config/packages.rb`:

```ruby
# config/packages.rb (generated during install)
Dir.glob(File.expand_path("../packages/**/lib/engine.rb", __dir__)) do |package|
  load package
end
```

This is required in `config/application.rb`.

## Creating Resources in Packages

```bash
# In main app
rails g pu:res:scaffold Post title:string --dest=main_app

# In feature package
rails g pu:res:scaffold Blogging::Post title:string --dest=blogging
```

## Connecting Resources to Portals

Resources must be connected to portals to be accessible:

```bash
rails g pu:res:conn Post --dest=admin_portal
rails g pu:res:conn Blogging::Post --dest=admin_portal
```

This creates:
- Portal-specific controller
- Portal-specific policy (optional)
- Portal-specific definition (optional)
- Route registration

## When to Use Each Type

### Feature Packages

Use for:
- Domain-specific models and logic
- Reusable business functionality
- Shared code across portals

Examples: `blogging`, `billing`, `inventory`, `user_management`

### Portal Packages

Use for:
- User-facing interfaces
- Role-specific access (admin, customer, public)
- Different authentication requirements

Examples: `admin_portal`, `dashboard_portal`, `public_portal`, `api_portal`

## Typical Architecture

```
packages/
├── blogging/              # Feature: blog functionality
│   └── models, definitions, policies
├── billing/               # Feature: payment/invoicing
│   └── models, definitions, policies
├── admin_portal/          # Portal: admin interface
│   └── controllers, views, routes
└── dashboard_portal/      # Portal: user dashboard
    └── controllers, views, routes
```

## Migration Integration

Package migrations are automatically integrated:

```bash
rails db:migrate  # Runs migrations from all packages
```

## Related Skills

- `plutonium-portal` - Portal-specific features (auth, entity scoping, routes)
- `plutonium-resource` - Resource architecture overview
- `plutonium-connect-resource` - Connecting resources to portals
- `plutonium-create-resource` - Creating resources
