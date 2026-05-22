---
name: rails-auth-with-devise
description: "Complete authentication setup for Ruby on Rails applications using Devise. Use when: (1) Setting up user authentication in a Rails app, (2) Adding sign in/sign up/sign out functionality, (3) Implementing email confirmation, password recovery, or account locking, (4) Configuring OmniAuth social login, (5) Adding multiple user models (User/Admin), (6) Customizing Devise views or controllers, (7) Testing authentication with RSpec/Minitest, (8) API authentication setup"
---

# Rails Authentication with Devise

Devise is the most popular authentication solution for Rails, providing a complete MVC solution with 10 modular components.

## Quick Setup

```bash
# Add to Gemfile
bundle add devise

# Install Devise
rails generate devise:install

# Generate User model with authentication
rails generate devise User

# Run migrations
rails db:migrate
```

## Essential Configuration

After `devise:install`, configure in `config/environments/development.rb`:
```ruby
config.action_mailer.default_url_options = { host: 'localhost', port: 3000 }
```

Set root route in `config/routes.rb`:
```ruby
root to: 'home#index'
```

## Devise Modules Reference

Enable modules in the model (e.g., `app/models/user.rb`):

| Module | Purpose | Migration Columns |
|--------|---------|-------------------|
| `:database_authenticatable` | Password hashing/storage | `email`, `encrypted_password` |
| `:registerable` | Sign up, edit, destroy account | - |
| `:recoverable` | Password reset via email | `reset_password_token`, `reset_password_sent_at` |
| `:rememberable` | "Remember me" cookie | `remember_created_at` |
| `:trackable` | Sign in stats | `sign_in_count`, `current_sign_in_at`, `last_sign_in_at`, `current_sign_in_ip`, `last_sign_in_ip` |
| `:validatable` | Email/password validations | - |
| `:confirmable` | Email confirmation | `confirmation_token`, `confirmed_at`, `confirmation_sent_at`, `unconfirmed_email` |
| `:lockable` | Lock after failed attempts | `failed_attempts`, `unlock_token`, `locked_at` |
| `:timeoutable` | Session expiration | - |
| `:omniauthable` | OAuth provider support | - |

## Controller Helpers

```ruby
# Require authentication
before_action :authenticate_user!

# Check if signed in
user_signed_in?

# Get current user
current_user

# Access session
user_session
```

For other models (e.g., Admin):
```ruby
before_action :authenticate_admin!
admin_signed_in?
current_admin
admin_session
```

## Common Tasks

### Add Custom Fields (e.g., username)

1. Generate migration:
```bash
rails g migration AddUsernameToUsers username:string:uniq
rails db:migrate
```

2. Permit in `ApplicationController`:
```ruby
class ApplicationController < ActionController::Base
  before_action :configure_permitted_parameters, if: :devise_controller?

  protected

  def configure_permitted_parameters
    devise_parameter_sanitizer.permit(:sign_up, keys: [:username])
    devise_parameter_sanitizer.permit(:account_update, keys: [:username])
  end
end
```

### Customize Views

```bash
# Generate all views
rails generate devise:views

# Scoped views for specific model
rails generate devise:views users

# Specific modules only
rails generate devise:views -v registrations confirmations
```

### Customize Controllers

```bash
# Generate controllers
rails generate devise:controllers users

# Or specific controller
rails generate devise:controllers users -c sessions registrations
```

Update routes:
```ruby
devise_for :users, controllers: {
  sessions: 'users/sessions',
  registrations: 'users/registrations'
}
```

### Custom Redirect After Sign In

In `ApplicationController`:
```ruby
def after_sign_in_path_for(resource)
  stored_location_for(resource) || dashboard_path
end

def after_sign_out_path_for(resource_or_scope)
  root_path
end
```

## Hotwire/Turbo Configuration (Rails 7+)

In `config/initializers/devise.rb`:
```ruby
Devise.setup do |config|
  config.responder.error_status = :unprocessable_entity
  config.responder.redirect_status = :see_other
end
```

Ensure `responders` gem version >= 3.1.0.

## Testing

### RSpec Setup

In `spec/support/devise.rb`:
```ruby
RSpec.configure do |config|
  config.include Devise::Test::ControllerHelpers, type: :controller
  config.include Devise::Test::ControllerHelpers, type: :view
  config.include Devise::Test::IntegrationHelpers, type: :feature
  config.include Devise::Test::IntegrationHelpers, type: :request
end
```

Usage:
```ruby
sign_in user
sign_out user
```

### Minitest Setup

```ruby
class ActionDispatch::IntegrationTest
  include Devise::Test::IntegrationHelpers
end
```

## Additional Guides

- **OmniAuth setup**: See [references/omniauth.md](references/omniauth.md)
- **API authentication**: See [references/api-auth.md](references/api-auth.md)
- **Advanced patterns**: See [references/advanced.md](references/advanced.md)
