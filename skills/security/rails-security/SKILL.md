---
name: rails-security
description: Specialized skill for Rails security, authorization, and data protection. Use when implementing Pundit policies, Lockbox encryption, Blind Index searches, authentication, secure configuration, or fixing security vulnerabilities. Includes security best practices and common pitfall prevention.
---

# Rails Security & Data Protection

Comprehensive security implementation with Lockbox, Blind Index, and Pundit.

## When to Use This Skill

- Implementing authorization with Pundit policies
- Encrypting sensitive data with Lockbox
- Adding searchable encryption with Blind Index
- Configuring authentication (Devise)
- Setting up secure credentials and secrets
- Implementing two-factor authentication
- Fixing security vulnerabilities
- Setting up HTTPS, CORS, CSP
- Preventing common attacks (XSS, CSRF, SQL injection)

## Core Security Stack

```ruby
# Gemfile
gem "lockbox"           # Encryption at rest
gem "blind_index"       # Searchable encryption
gem "pundit"            # Authorization
gem "devise"            # Authentication (optional)
gem "brakeman"          # Security scanner
gem "bundler-audit"     # Dependency vulnerabilities
```

## Encryption at Rest (Lockbox)

### Setup

```ruby
# Install
$ rails lockbox:install

# Creates config/master.key (DO NOT COMMIT!)
```

### Encrypting Model Fields

```ruby
# app/models/user.rb
class User < ApplicationRecord
  # Encrypt sensitive fields
  has_encrypted :email, :ssn, :phone, :credit_card_number

  # Lockbox creates:
  # - email_ciphertext (stored in DB)
  # - email (virtual, decrypted)
end
```

### Migration

```ruby
class AddEncryptedFieldsToUsers < ActiveRecord::Migration[7.1]
  def change
    add_column :users, :email_ciphertext, :text
    add_column :users, :ssn_ciphertext, :text
    add_column :users, :phone_ciphertext, :text
  end
end
```

### Usage

```ruby
# Writing
user = User.create!(email: "user@example.com")  # Auto-encrypted

# Reading
user.email  # => "user@example.com" (auto-decrypted)

# Database stores encrypted
user.email_ciphertext  # => "encrypted_string..."
```

## Searchable Encryption (Blind Index)

### Setup

```ruby
# app/models/user.rb
class User < ApplicationRecord
  has_encrypted :email, :phone

  # Add blind indexes for searchable fields
  blind_index :email
  blind_index :phone
end
```

### Migration

```ruby
class AddBlindIndexesToUsers < ActiveRecord::Migration[7.1]
  def change
    add_column :users, :email_bidx, :string
    add_column :users, :phone_bidx, :string

    add_index :users, :email_bidx, unique: true
    add_index :users, :phone_bidx
  end
end
```

### Searching Encrypted Fields

```ruby
# Find by encrypted field (works!)
user = User.find_by(email: "user@example.com")

# Where clause
users = User.where(email: "user@example.com")

# Limitations
User.where("email LIKE ?", "%partial%")  # Won't work
User.where("email > ?", "a@a.com")       # Won't work (no range queries)
```

## Authorization (Pundit)

### Setup

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  include Pundit::Authorization

  rescue_from Pundit::NotAuthorizedError, with: :user_not_authorized

  private

  def user_not_authorized
    flash[:alert] = "You are not authorized to perform this action."
    redirect_to(request.referrer || root_path)
  end
end
```

### Policy Example

```ruby
# app/policies/article_policy.rb
class ArticlePolicy < ApplicationPolicy
  def index?
    true  # Anyone can view list
  end

  def show?
    record.published? || user_is_author?
  end

  def create?
    user.present?
  end

  def update?
    user_is_author? || user&.admin?
  end

  def destroy?
    user_is_author? || user&.admin?
  end

  class Scope < Scope
    def resolve
      if user&.admin?
        scope.all
      elsif user
        scope.where(published: true).or(scope.where(user: user))
      else
        scope.where(published: true)
      end
    end
  end

  private

  def user_is_author?
    user && record.user == user
  end
end
```

### Using in Controllers

```ruby
class ArticlesController < ApplicationController
  def index
    @articles = policy_scope(Article)
  end

  def show
    @article = Article.find(params[:id])
    authorize @article
  end

  def update
    @article = Article.find(params[:id])
    authorize @article

    if @article.update(article_params)
      redirect_to @article
    else
      render :edit
    end
  end
end
```

### Using in Views

```erb
<% if policy(@article).update? %>
  <%= link_to "Edit", edit_article_path(@article) %>
<% end %>

<% if policy(@article).destroy? %>
  <%= button_to "Delete", article_path(@article), method: :delete %>
<% end %>
```

## Authentication (Devise)

### Strong Configuration

```ruby
# config/initializers/devise.rb
Devise.setup do |config|
  # Strong passwords
  config.password_length = 12..128

  # Paranoid mode (don't reveal if email exists)
  config.paranoid = true

  # Account lockout
  config.lock_strategy = :failed_attempts
  config.maximum_attempts = 5
  config.unlock_strategy = :time
  config.unlock_in = 1.hour

  # Session timeout
  config.timeout_in = 30.minutes
end
```

## Secure Configuration

### Never Commit Secrets

```bash
# .gitignore
/.env
/config/master.key
/config/credentials/*.key
```

### Use Rails Credentials

```bash
# Edit credentials
$ EDITOR=vim rails credentials:edit

# In file:
aws:
  access_key_id: YOUR_KEY
  secret_access_key: YOUR_SECRET
```

```ruby
# Access in code
Rails.application.credentials.aws[:access_key_id]
```

### HTTPS Enforcement

```ruby
# config/environments/production.rb
config.force_ssl = true
```

## Common Security Pitfalls

### 1. Mass Assignment

```ruby
# VULNERABLE
def create
  User.create(params[:user])  # Allows ANY attribute!
end

# SAFE
def create
  User.create(user_params)
end

private

def user_params
  params.require(:user).permit(:name, :email, :password)
end
```

### 2. SQL Injection

```ruby
# VULNERABLE
User.where("name = '#{params[:name]}'")

# SAFE
User.where("name = ?", params[:name])
User.where(name: params[:name])
```

### 3. XSS (Cross-Site Scripting)

```erb
<%# VULNERABLE %>
<%= raw @article.body %>
<%= @article.body.html_safe %>

<%# SAFE - Escape by default %>
<%= @article.body %>

<%# Or sanitize allowed HTML %>
<%= sanitize @article.body, tags: %w[p br strong em] %>
```

### 4. Insecure Direct Object References

```ruby
# VULNERABLE - No authorization
def show
  @article = Article.find(params[:id])
end

# SAFE - Authorize first
def show
  @article = Article.find(params[:id])
  authorize @article
end

# Or scope to current user
def show
  @article = current_user.articles.find(params[:id])
end
```

### 5. Timing Attacks

```ruby
# VULNERABLE
def valid_api_key?(provided_key)
  provided_key == stored_key  # Timing reveals info
end

# SAFE
def valid_api_key?(provided_key)
  ActiveSupport::SecurityUtils.secure_compare(provided_key, stored_key)
end
```

## Security Checklist

Before deploying:

- ✓ All secrets in credentials, not code
- ✓ SSL/HTTPS enforced in production
- ✓ Strong password requirements
- ✓ CSRF protection enabled
- ✓ Mass assignment protected (strong params)
- ✓ Authorization checks on all actions
- ✓ Sensitive data encrypted (Lockbox)
- ✓ Brakeman scan passes
- ✓ bundler-audit passes
- ✓ Input validation on all user data
- ✓ Output escaping by default

## Running Security Scans

```bash
# Security scan
bundle exec brakeman --no-pager

# Dependency audit
bundle exec bundle-audit check --update

# Both should pass before merge
```

## Reference Documentation

For comprehensive security patterns:
- Security guide: `security.md` (detailed examples and advanced patterns)
