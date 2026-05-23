---
name: plutonium-installation
description: Installing Plutonium in a Rails application - setup, generators, and configuration
---

# Plutonium Installation

## New Rails App (Recommended)

Use the Rails template for a fully configured setup:

```bash
rails new myapp -a propshaft -j esbuild -c tailwind \
  -m https://radioactive-labs.github.io/plutonium-core/templates/plutonium.rb
```

This sets up Rails with Propshaft, esbuild, TailwindCSS, and Plutonium in one command.

## Existing Rails App

### Option 1: Rails Template

```bash
bin/rails app:template \
  LOCATION=https://radioactive-labs.github.io/plutonium-core/templates/base.rb
```

### Option 2: Manual Installation

```bash
# Add to Gemfile
gem "plutonium"

# Install
bundle install
rails generate pu:core:install
```

## What Gets Generated

After `pu:core:install`:

```
app/
├── controllers/
│   ├── plutonium_controller.rb    # Base controller
│   └── resource_controller.rb     # Resource CRUD base
├── definitions/
│   └── resource_definition.rb     # Definition base class
├── interactions/
│   └── resource_interaction.rb    # Interaction base class
├── models/
│   └── resource_record.rb         # Abstract model base
├── policies/
│   └── resource_policy.rb         # Policy base class
└── views/
    └── layouts/
        └── resource.html.erb      # Base layout

config/
├── initializers/
│   └── plutonium.rb               # Configuration
└── packages.rb                    # Package loader

packages/
└── .keep
```

## Base Classes

### ResourceController

```ruby
class ResourceController < PlutoniumController
  include Plutonium::Resource::Controller
  # Provides: index, show, new, create, edit, update, destroy
  # Plus: interactive actions, authorization, query handling
end
```

### ResourcePolicy

```ruby
class ResourcePolicy < Plutonium::Resource::Policy
  def create?
    true  # Override with your logic
  end

  def read?
    true
  end
end
```

### ResourceDefinition

```ruby
class ResourceDefinition < Plutonium::Resource::Definition
  # Add app-wide definition defaults here
end
```

### ResourceRecord

```ruby
class ResourceRecord < ApplicationRecord
  self.abstract_class = true
  # Models inherit from this for Plutonium features
end
```

## Authentication Setup

### Install Rodauth

```bash
rails generate pu:rodauth:install
```

### Create Account Types

```bash
# Basic user account
rails generate pu:rodauth:account user

# Admin with 2FA, lockout, audit logging
rails generate pu:rodauth:admin

# Customer with entity association
rails generate pu:rodauth:customer customer
```

### Account Options

| Option | Description |
|--------|-------------|
| `--defaults` | Enable common features (login, logout, remember, reset_password) |
| `--kitchen_sink` | Enable all available features |
| `--no-allow_signup` | Disable public signup |
| `--entity=Organization` | Create associated entity model |

### Connect Auth to Controllers

```ruby
# app/controllers/resource_controller.rb
class ResourceController < PlutoniumController
  include Plutonium::Resource::Controller
  include Plutonium::Auth::Rodauth(:user)  # Add this
end
```

## Creating Your First Resource

```bash
rails generate pu:res:scaffold Post user:belongs_to title:string content:text
rails db:migrate
```

## Creating a Portal

```bash
rails generate pu:pkg:portal admin
```

Select authentication when prompted:
- **Rodauth account** - Use existing auth
- **Public access** - No authentication
- **Bring your own** - Custom implementation

### Mount the Portal

```ruby
# config/routes.rb
Rails.application.routes.draw do
  mount AdminPortal::Engine, at: "/admin"
end
```

### Connect Resources to Portal

```bash
rails generate pu:res:conn Post --dest=admin_portal
```

## Configuration

```ruby
# config/initializers/plutonium.rb
Plutonium.configure do |config|
  config.load_defaults 1.0

  # Custom assets (optional)
  # config.assets.stylesheet = "custom_stylesheet"
  # config.assets.script = "custom_script"
  # config.assets.logo = "custom_logo.png"
end
```

## Package System

Packages are loaded from `config/packages.rb`:

```ruby
Dir.glob(File.expand_path("../packages/**/lib/engine.rb", __dir__)) { |package| load package }
```

Create packages in `packages/` directory:
- **Feature packages** - Business logic (`rails g pu:pkg:package blogging`)
- **Portal packages** - Web interfaces (`rails g pu:pkg:portal admin`)

## Post-Installation Checklist

1. **Install core**
   ```bash
   rails generate pu:core:install
   ```

2. **Setup authentication** (if needed)
   ```bash
   rails generate pu:rodauth:install
   rails generate pu:rodauth:account user
   ```

3. **Create a portal**
   ```bash
   rails generate pu:pkg:portal admin
   ```

4. **Create resources**
   ```bash
   rails generate pu:res:scaffold Post title:string content:text
   ```

5. **Connect resources to portal**
   ```bash
   rails generate pu:res:conn Post --dest=admin_portal
   ```

6. **Run migrations**
   ```bash
   rails db:migrate
   ```

7. **Mount portal** (add to `config/routes.rb`)
   ```ruby
   mount AdminPortal::Engine, at: "/admin"
   ```

8. **Start server**
   ```bash
   rails server
   ```

## Converting Existing Models

For models that already exist in your app:

1. Include the module:
   ```ruby
   class Post < ApplicationRecord
     include Plutonium::Resource::Record
   end
   ```

2. Generate supporting files (skips model/migration):
   ```bash
   rails g pu:res:scaffold Post
   ```

3. Connect to portal:
   ```bash
   rails g pu:res:conn Post --dest=admin_portal
   ```

## Generator Reference

| Generator | Purpose |
|-----------|---------|
| `pu:core:install` | Initial Plutonium setup |
| `pu:rodauth:install` | Setup Rodauth authentication |
| `pu:rodauth:account NAME` | Create user account type |
| `pu:rodauth:admin` | Create admin account with 2FA |
| `pu:rodauth:customer NAME` | Create customer with entity |
| `pu:pkg:package NAME` | Create feature package |
| `pu:pkg:portal NAME` | Create portal package |
| `pu:res:scaffold NAME` | Create resource (model, policy, definition, controller) |
| `pu:res:conn NAME` | Connect resource to portal |
| `pu:eject:layout` | Eject layout files for customization |
| `pu:skills:sync` | Sync Claude Code skills to project |

## Related Skills

- `plutonium-resource` - Resource architecture overview
- `plutonium-rodauth` - Authentication setup and configuration
- `plutonium-package` - Feature and portal packages
- `plutonium-portal` - Portal configuration
- `plutonium-views` - Custom pages, layouts, and Phlex components
- `plutonium-assets` - TailwindCSS and custom styling
- `plutonium-create-resource` - Resource scaffold options
- `plutonium-connect-resource` - Portal connection
