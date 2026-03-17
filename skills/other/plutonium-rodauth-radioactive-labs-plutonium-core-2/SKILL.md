---
name: plutonium-rodauth
description: Plutonium Rodauth integration - authentication setup, account types, and configuration
---

# Plutonium Rodauth Authentication

Plutonium integrates with [Rodauth](http://rodauth.jeremyevans.net/) via [rodauth-rails](https://github.com/janko/rodauth-rails) for authentication. This provides a full-featured, secure authentication system.

## Installation

### Step 1: Install Rodauth Base

```bash
rails generate pu:rodauth:install
```

This installs:
- Required gems (`rodauth-rails`, `bcrypt`, `sequel-activerecord_connection`)
- `app/rodauth/rodauth_app.rb` - Main Roda app
- `app/rodauth/rodauth_plugin.rb` - Base plugin
- `app/controllers/rodauth_controller.rb` - Base controller
- `config/initializers/rodauth.rb` - Configuration
- `app/views/layouts/rodauth.html.erb` - Auth layout
- PostgreSQL extension migration (if using PostgreSQL)

### Step 2: Create Account Type

Choose the appropriate generator for your use case:

```bash
# Basic user account
rails generate pu:rodauth:account user

# Admin with 2FA and security features
rails generate pu:rodauth:admin admin

# SaaS user with entity/organization (multi-tenant)
rails generate pu:saas:setup --user Customer --entity Organization
```

## Account Generators

### Basic Account (`pu:rodauth:account`)

Creates a standard user account with configurable features:

```bash
rails generate pu:rodauth:account user [options]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--defaults` | Enable default features (login, logout, remember, password reset) |
| `--kitchen_sink` | Enable ALL available features |
| `--primary` | Mark as primary account (no URL prefix) |
| `--no-mails` | Skip mailer setup |
| `--argon2` | Use Argon2 instead of bcrypt for password hashing |
| `--api_only` | Configure for JSON API only (no sessions) |

**Feature Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--login` | ✓ | Login functionality |
| `--logout` | ✓ | Logout functionality |
| `--remember` | ✓ | "Remember me" cookies |
| `--create_account` | ✓ | User registration |
| `--verify_account` | ✓ | Email verification |
| `--reset_password` | ✓ | Password reset via email |
| `--change_password` | ✓ | Change password |
| `--change_login` | ✓ | Change email |
| `--verify_login_change` | ✓ | Verify email change |
| `--otp` | | TOTP two-factor auth |
| `--webauthn` | | WebAuthn/passkeys |
| `--recovery_codes` | | Recovery codes for 2FA |
| `--lockout` | | Account lockout after failed attempts |
| `--active_sessions` | | Track active sessions |
| `--audit_logging` | | Audit authentication events |
| `--close_account` | | Allow account deletion |
| `--email_auth` | | Passwordless login via email |
| `--sms_codes` | | SMS-based 2FA |
| `--jwt` | | JWT token authentication |
| `--jwt_refresh` | | JWT refresh tokens |

### Admin Account (`pu:rodauth:admin`)

Creates a secure admin account with:
- Multi-phase login (email first, then password)
- TOTP two-factor authentication (required)
- Recovery codes
- Account lockout
- Active sessions tracking
- Audit logging
- Role-based access control
- Invite interaction for adding new admins
- No public signup (accounts created via rake task or invite)

```bash
rails generate pu:rodauth:admin admin
rails generate pu:rodauth:admin admin --roles=super_admin,admin,viewer
rails generate pu:rodauth:admin admin --extra-attributes=name:string,department:string
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--roles` | super_admin,admin | Comma-separated roles for admin accounts |
| `--extra_attributes` | | Additional model attributes (e.g., name:string) |

**Generated role enum:**
```ruby
# app/models/admin.rb
enum :role, super_admin: 0, admin: 1
```

**Generated invite interaction:**
```ruby
# app/interactions/admin/invite_interaction.rb
class Admin::InviteInteraction < Plutonium::Interaction::Base
  attribute :email, :string
  attribute :role, default: :admin  # Second role is default

  def execute
    # Creates admin via internal request and sends invite email
  end
end
```

**Creates rake task:**
```bash
# Create admin account directly
rails rodauth_admin:create[admin@example.com,password123]
```

### SaaS Setup (`pu:saas:setup`)

Creates a complete multi-tenant SaaS setup with user account, entity, and membership:

```bash
rails generate pu:saas:setup --user Customer --entity Organization
rails generate pu:saas:setup --user Customer --entity Organization --roles=member,admin,owner
rails generate pu:saas:setup --user Customer --entity Organization --no-allow-signup
rails generate pu:saas:setup --user Customer --entity Organization --user-attributes=name:string --entity-attributes=slug:string
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--user=NAME` | (required) | User account model name (e.g., Customer) |
| `--entity=NAME` | (required) | Entity model name (e.g., Organization) |
| `--allow-signup` | true | Allow public registration |
| `--roles` | member,owner | Comma-separated membership roles |
| `--skip-entity` | false | Skip entity model generation |
| `--skip-membership` | false | Skip membership model generation |
| `--user-attributes` | | Additional user model attributes |
| `--entity-attributes` | | Additional entity model attributes (name is always included) |
| `--membership-attributes` | | Additional membership model attributes |

**Individual Generators:**

You can also run each component separately:

```bash
# Just the user account
rails g pu:saas:user Customer

# Just the entity model
rails g pu:saas:entity Organization

# Just the membership (requires user and entity to exist)
rails g pu:saas:membership --user Customer --entity Organization
```

**Generated Models:**

1. **User account** - The user model with Rodauth authentication
2. **Entity model** - The organization/company with unique name
3. **Membership model** - Join table `{entity}_{user}` (e.g., `OrganizationCustomer`)

```ruby
# app/models/customer.rb
class Customer < ApplicationRecord
  include Rodauth::Rails.model(:customer)

  has_many :organization_customers, dependent: :destroy
  has_many :organizations, through: :organization_customers
end

# app/models/organization.rb
class Organization < ApplicationRecord
  has_many :organization_customers, dependent: :destroy
  has_many :customers, through: :organization_customers
end

# app/models/organization_customer.rb
class OrganizationCustomer < ApplicationRecord
  belongs_to :organization
  belongs_to :customer

  enum :role, member: 0, owner: 1

  validates :customer, uniqueness: {
    scope: :organization_id,
    message: "is already a member of this organization"
  }
end
```

**Membership Roles:**

The membership model includes a role enum for access control within the entity:

```ruby
membership = OrganizationCustomer.find_by(organization: org, customer: current_user)
membership.member?  # Default role
membership.owner?   # Admin role for the entity
```

## Connecting Auth to Controllers

### Include in Resource Controller

```ruby
# app/controllers/resource_controller.rb
class ResourceController < PlutoniumController
  include Plutonium::Resource::Controller
  include Plutonium::Auth::Rodauth(:user)  # Use :user account
end
```

### Multiple Account Types

```ruby
# app/controllers/admin_controller.rb
class AdminController < PlutoniumController
  include Plutonium::Resource::Controller
  include Plutonium::Auth::Rodauth(:admin)
end

# app/controllers/customer_controller.rb
class CustomerController < PlutoniumController
  include Plutonium::Resource::Controller
  include Plutonium::Auth::Rodauth(:customer)
end
```

### What It Provides

Including `Plutonium::Auth::Rodauth(:name)` adds:

| Method | Description |
|--------|-------------|
| `current_user` | The authenticated account |
| `logout_url` | URL to logout |
| `plutonium-rodauth` | Access to Rodauth instance |

## Generated Files

### Account Structure

```
app/
├── controllers/
│   └── rodauth/
│       └── user_controller.rb      # Account-specific controller
├── mailers/
│   └── rodauth/
│       └── user_mailer.rb          # Account-specific mailer
├── models/
│   └── user.rb                     # Account model
├── rodauth/
│   ├── rodauth_app.rb              # Main Roda app
│   ├── rodauth_plugin.rb           # Base plugin
│   └── user_rodauth_plugin.rb      # Account-specific config
├── policies/
│   └── user_policy.rb              # Account policy
├── definitions/
│   └── user_definition.rb          # Account definition
└── views/
    ├── layouts/
    │   └── rodauth.html.erb        # Auth layout
    └── rodauth/
        └── user_mailer/            # Email templates
            ├── reset_password.text.erb
            ├── verify_account.text.erb
            └── ...
```

### Plugin Configuration

```ruby
# app/rodauth/user_rodauth_plugin.rb
class UserRodauthPlugin < RodauthPlugin
  configure do
    # Features enabled for this account
    enable :login, :logout, :remember, :create_account, ...

    # URL prefix (non-primary accounts)
    prefix "/users"

    # Password storage
    account_password_hash_column :password_hash

    # Controller for views
    rails_controller { Rodauth::UserController }

    # Model
    rails_account_model { User }

    # Redirects
    login_redirect "/"
    logout_redirect "/"

    # Session configuration
    session_key "_user_session"
    remember_cookie_key "_user_remember"
  end
end
```

## Customization

### Custom Login Redirect

```ruby
# app/rodauth/user_rodauth_plugin.rb
configure do
  login_redirect { "/dashboard" }

  # Or dynamically based on user
  login_redirect do
    if rails_account.admin?
      "/admin"
    else
      "/dashboard"
    end
  end
end
```

### Custom Validation

```ruby
configure do
  # Add custom field validation
  before_create_account do
    throw_error_status(422, "name", "must be present") if param("name").empty?
  end

  # After account creation
  after_create_account do
    Profile.create!(account_id: account_id, name: param("name"))
  end
end
```

### Password Requirements

```ruby
configure do
  # Minimum length
  password_minimum_length 12

  # Custom complexity
  password_meets_requirements? do |password|
    super(password) && password.match?(/\d/) && password.match?(/[^a-zA-Z\d]/)
  end
end
```

### Multi-Phase Login

```ruby
configure do
  # Ask for email first, then password
  use_multi_phase_login? true
end
```

### Prevent Public Signup

```ruby
configure do
  before_create_account_route do
    request.halt unless internal_request?
  end
end
```

## Email Configuration

Emails are sent via Action Mailer. Configure delivery in your environment:

```ruby
# config/environments/production.rb
config.action_mailer.delivery_method = :smtp
config.action_mailer.smtp_settings = {
  address: "smtp.example.com",
  port: 587,
  user_name: ENV["SMTP_USER"],
  password: ENV["SMTP_PASSWORD"]
}
```

### Custom Email Templates

Override templates in `app/views/rodauth/user_mailer/`:

```erb
<%# app/views/rodauth/user_mailer/reset_password.text.erb %>
Hi <%= @account.email %>,

Someone requested a password reset for your account.

Reset your password: <%= @reset_password_url %>

If you didn't request this, ignore this email.
```

## Portal Integration

### Selecting Auth for Portal

When generating a portal, select the Rodauth account:

```bash
rails generate pu:pkg:portal admin
# Select "Rodauth account" when prompted
# Choose "admin" account
```

### Manual Portal Auth Setup

```ruby
# packages/admin_portal/lib/engine.rb
module AdminPortal
  class Engine < Rails::Engine
    include Plutonium::Portal::Engine

    # Require authentication
    config.before_initialize do
      config.to_prepare do
        AdminPortal::ResourceController.class_eval do
          include Plutonium::Auth::Rodauth(:admin)

          before_action :require_authenticated

          private

          def require_authenticated
            redirect_to rodauth.login_path unless current_user
          end
        end
      end
    end
  end
end
```

## API Authentication

For JSON API authentication:

```bash
rails generate pu:rodauth:account api_user --api_only --jwt --jwt_refresh
```

This enables:
- JWT token authentication
- Refresh tokens
- No session/cookie handling

### Using JWT

```ruby
# Login
POST /api_users/login
Content-Type: application/json

{"login": "user@example.com", "password": "secret"}

# Response includes JWT
{"access_token": "...", "refresh_token": "..."}

# Authenticated requests
GET /api/posts
Authorization: Bearer <access_token>
```

## Internal Requests

Create accounts programmatically:

```ruby
# Using internal request
Rodauth::Rails.app(:user).rodauth(:user).create_account(
  login: "user@example.com",
  password: "secure_password"
)

# Or via model (if allowed)
User.create!(
  email: "user@example.com",
  password_hash: BCrypt::Password.create("secure_password"),
  status: 2  # verified
)
```

## Feature Reference

| Feature | Description |
|---------|-------------|
| `login` | Basic login/logout |
| `create_account` | User registration |
| `verify_account` | Email verification |
| `reset_password` | Password reset via email |
| `change_password` | Change password when logged in |
| `change_login` | Change email address |
| `verify_login_change` | Verify email change |
| `remember` | "Remember me" functionality |
| `otp` | TOTP two-factor authentication |
| `sms_codes` | SMS-based 2FA |
| `recovery_codes` | Backup codes for 2FA |
| `webauthn` | WebAuthn/passkey authentication |
| `lockout` | Lock account after failed attempts |
| `active_sessions` | Track/manage active sessions |
| `audit_logging` | Log authentication events |
| `email_auth` | Passwordless email login |
| `jwt` | JWT token authentication |
| `jwt_refresh` | JWT refresh tokens |
| `close_account` | Allow account deletion |
| `password_expiration` | Force password changes |
| `disallow_password_reuse` | Prevent password reuse |

## Related Skills

- `plutonium-installation` - Initial Plutonium setup
- `plutonium-portal` - Portal configuration
- `plutonium-policy` - Authorization after authentication
- `plutonium-invites` - User invitation system for multi-tenant apps
