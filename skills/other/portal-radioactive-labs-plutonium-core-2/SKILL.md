---
name: plutonium-portal
description: Plutonium portals - web interfaces with authentication, entity scoping, and routes
---

# Plutonium Portals

Portals are Rails engines that provide web interfaces for specific user types.

## Creating a Portal

```bash
rails g pu:pkg:portal dashboard
```

### Generator Options

| Option | Description |
|--------|-------------|
| `--auth=NAME` | Rodauth account to authenticate with (e.g., `--auth=user`) |
| `--public` | Grant public access (no authentication) |
| `--byo` | Bring your own authentication |
| `--scope=CLASS` | Entity class to scope to for multi-tenancy (e.g., `--scope=Organization`) |

```bash
# Non-interactive examples
rails g pu:pkg:portal admin --auth=admin
rails g pu:pkg:portal api --public
rails g pu:pkg:portal custom --byo

# With entity scoping (multi-tenancy)
rails g pu:pkg:portal admin --auth=admin --scope=Organization
```

Without flags, the generator prompts interactively:
- **Rodauth account** - Use existing Rodauth authentication
- **Public access** - No authentication required
- **Bring your own** - Implement custom `current_user`

## Portal Engine

```ruby
# packages/dashboard_portal/lib/engine.rb
module DashboardPortal
  class Engine < Rails::Engine
    include Plutonium::Portal::Engine

    config.after_initialize do
      # Optional: multi-tenancy
      scope_to_entity Organization, strategy: :path
    end
  end
end
```

## Authentication

### Rodauth Integration

```ruby
# packages/dashboard_portal/app/controllers/dashboard_portal/concerns/controller.rb
module DashboardPortal
  module Concerns
    module Controller
      extend ActiveSupport::Concern
      include Plutonium::Portal::Controller
      include Plutonium::Auth::Rodauth(:user)  # Use :user account
    end
  end
end
```

### Public Access

```ruby
module DashboardPortal
  module Concerns
    module Controller
      extend ActiveSupport::Concern
      include Plutonium::Portal::Controller
      include Plutonium::Auth::Public
    end
  end
end
```

### Custom Authentication

```ruby
module DashboardPortal
  module Concerns
    module Controller
      extend ActiveSupport::Concern
      include Plutonium::Portal::Controller
      include Plutonium::Auth::Public

      def current_user
        @current_user ||= User.find_by(api_key: request.headers["X-API-Key"])
      end
    end
  end
end
```

## Entity Scoping (Multi-tenancy)

Automatically scope all data to a parent entity.

### Path Strategy

Entity ID in URL path:

```ruby
module AdminPortal
  class Engine < Rails::Engine
    include Plutonium::Portal::Engine

    config.after_initialize do
      scope_to_entity Organization, strategy: :path
    end
  end
end
```

Routes become: `/organizations/:organization_id/posts`

### Custom Strategy

Implement your own lookup method:

```ruby
module AdminPortal
  class Engine < Rails::Engine
    include Plutonium::Portal::Engine

    config.after_initialize do
      scope_to_entity Organization, strategy: :current_organization
    end
  end
end

# In controller concern
module AdminPortal
  module Concerns
    module Controller
      extend ActiveSupport::Concern
      include Plutonium::Portal::Controller

      private

      # Method name must match strategy
      def current_organization
        @current_organization ||= Organization.find_by!(subdomain: request.subdomain)
      end
    end
  end
end
```

### Accessing the Scoped Entity

```ruby
current_scoped_entity  # The current Organization/Account/etc.
scoped_to_entity?      # true if scoping is active
```

### Model Requirements

Models must have an association path to the scoped entity:

```ruby
# Direct association (preferred)
class Post < ResourceRecord
  belongs_to :organization
end

# Through association
class Comment < ResourceRecord
  belongs_to :post
  has_one :organization, through: :post
end

# Complex (define custom scope)
class AuditLog < ResourceRecord
  scope :associated_with_organization, ->(org) {
    joins(:user).where(users: { organization_id: org.id })
  }
end
```

## Routes

### Portal Routes

```ruby
# packages/dashboard_portal/config/routes.rb
DashboardPortal::Engine.routes.draw do
  root to: "dashboard#index"

  # Register resources
  register_resource ::Post
  register_resource Blogging::Comment

  # Custom routes
  get "settings", to: "settings#index"
end
```

### Custom Routes on Resources

Add member or collection routes with a block:

```ruby
register_resource ::Post do
  member do
    get :preview
    get :analytics
    post :publish
  end
  collection do
    get :archived
    post :bulk_publish
  end
end
```

This generates:
- `GET /posts/:id/preview`
- `GET /posts/:id/analytics`
- `POST /posts/:id/publish`
- `GET /posts/archived`
- `POST /posts/bulk_publish`

### Mounting in Main App

```ruby
# config/routes.rb
Rails.application.routes.draw do
  # With authentication constraint
  constraints Rodauth::Rails.authenticate(:user) do
    mount DashboardPortal::Engine, at: "/dashboard"
  end

  # Or without
  mount PublicPortal::Engine, at: "/public"
end
```

## Controller Hierarchy

Portal controllers inherit from the feature package's controller if one exists (and include the portal's `Concerns::Controller`). If no feature package controller exists, they inherit from the portal's `ResourceController`.

```ruby
# With feature package controller:
class DashboardPortal::PostsController < ::PostsController
  include DashboardPortal::Concerns::Controller
end

# Without feature package controller:
class DashboardPortal::PostsController < DashboardPortal::ResourceController
end
```

### Portal ResourceController

The portal's `ResourceController` serves as the base class for resource controllers when no feature package controller exists. It includes the portal's `Concerns::Controller` so individual resource controllers don't need to.

```ruby
# packages/dashboard_portal/app/controllers/dashboard_portal/resource_controller.rb
module DashboardPortal
  class ResourceController < ::ResourceController
    include DashboardPortal::Concerns::Controller
  end
end
```

### Non-Resource Controllers

For portal pages not tied to a resource (dashboard, settings, etc.), inherit from `PlutoniumController`:

```ruby
# packages/dashboard_portal/app/controllers/dashboard_portal/dashboard_controller.rb
module DashboardPortal
  class DashboardController < PlutoniumController
    def index
      # Dashboard home page
    end
  end
end
```

## Portal-Specific Overrides

### Override Definition

```ruby
# packages/dashboard_portal/app/definitions/dashboard_portal/post_definition.rb
class DashboardPortal::PostDefinition < ::PostDefinition
  # Hide certain actions from this portal
  # Add portal-specific scopes
  scope :my_posts, -> { where(user: current_user) }
end
```

### Override Policy

```ruby
# packages/dashboard_portal/app/policies/dashboard_portal/post_policy.rb
class DashboardPortal::PostPolicy < ::PostPolicy
  include DashboardPortal::ResourcePolicy

  def destroy?
    false  # No deletion in user portal
  end

  def permitted_attributes_for_create
    %i[title content]  # Fewer fields than admin
  end
end
```

### Override Controller

```ruby
# packages/dashboard_portal/app/controllers/dashboard_portal/posts_controller.rb
module DashboardPortal
  class PostsController < ResourceController
    private

    def preferred_action_after_submit
      "index"
    end
  end
end
```

## Layout and Views

### Portal Layout

```erb
<!-- packages/dashboard_portal/app/views/layouts/dashboard_portal.html.erb -->
<!DOCTYPE html>
<html>
<head>
  <title>Dashboard</title>
  <%= csrf_meta_tags %>
  <%= stylesheet_link_tag "application" %>
</head>
<body>
  <nav><!-- Portal navigation --></nav>
  <main><%= yield %></main>
</body>
</html>
```

### Dashboard Controller

```ruby
# packages/dashboard_portal/app/controllers/dashboard_portal/dashboard_controller.rb
module DashboardPortal
  class DashboardController < PlutoniumController
    def index
      # Dashboard home page
    end
  end
end
```

## Multiple Portals Example

```ruby
# Admin portal - full access
module AdminPortal
  class Engine < Rails::Engine
    include Plutonium::Portal::Engine

    config.after_initialize do
      scope_to_entity Organization, strategy: :path
    end
  end
end

# User dashboard - limited access
module DashboardPortal
  class Engine < Rails::Engine
    include Plutonium::Portal::Engine

    config.after_initialize do
      scope_to_entity Organization, strategy: :path
    end
  end
end

# Public portal - read-only, no auth
module PublicPortal
  class Engine < Rails::Engine
    include Plutonium::Portal::Engine
  end
end
```

Each portal can:
- Have different authentication
- Show different fields
- Allow different actions
- Use different layouts

## Related Skills

- `plutonium-package` - Package overview (features vs portals)
- `plutonium-rodauth` - Authentication setup and configuration
- `plutonium-connect-resource` - Connecting resources to portals
- `plutonium-policy` - Portal-specific policies
- `plutonium-definition` - Portal-specific definitions
- `plutonium-controller` - Portal-specific controllers
