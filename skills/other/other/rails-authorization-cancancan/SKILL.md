---
name: rails-authorization-cancancan
description: "Authorization and permissions management for Ruby on Rails applications using CanCanCan. Use when: (1) Implementing role-based access control (RBAC), (2) Defining user permissions and abilities, (3) Restricting resource access in controllers, (4) Filtering queries based on user permissions, (5) Hiding/showing UI elements based on authorization, (6) Testing authorization logic, (7) Managing admin vs user vs guest permissions, (8) Implementing attribute-based access control"
---

# Rails Authorization with CanCanCan

CanCanCan is a popular authorization library for Rails that restricts what resources a given user is allowed to access. It centralizes all permission logic in a single Ability class, keeping authorization rules DRY and maintainable.

## Quick Setup

```bash
# Add to Gemfile
bundle add cancancan

# Generate Ability class
rails generate cancan:ability
```

This creates `app/models/ability.rb` where all authorization rules are defined.

## Core Concepts

### Defining Abilities

The `Ability` class centralizes all permission logic:

```ruby
# app/models/ability.rb
class Ability
  include CanCan::Ability

  def initialize(user)
    # Guest users (not signed in)
    can :read, Post, published: true
    can :read, Comment

    # Signed-in users
    return unless user.present?

    can :read, Post
    can :create, Post
    can :update, Post, user_id: user.id
    can :destroy, Post, user_id: user.id

    can :create, Comment
    can :update, Comment, user_id: user.id
    can :destroy, Comment, user_id: user.id

    # Admin users
    return unless user.admin?

    can :manage, :all  # Can do anything
  end
end
```

**Best Practice**: Structure rules hierarchically (guest → user → admin) for clarity.

## Actions and Resources

### Standard CRUD Actions

```ruby
:read    # :index and :show
:create  # :new and :create
:update  # :edit and :update
:destroy # :destroy

:manage  # All actions (use carefully!)
```

### Custom Actions

```ruby
can :publish, Post
can :archive, Post
can :approve, Comment
```

### Multiple Resources

```ruby
can :read, [Post, Comment, Category]
can :manage, [User, Post], user_id: user.id
```

## Ability Conditions

### Hash Conditions

```ruby
# Simple equality
can :update, Post, user_id: user.id

# Multiple conditions (AND logic)
can :read, Post, published: true, category_id: user.accessible_category_ids

# SQL fragment (use sparingly)
can :read, Post, ["published_at <= ?", Time.zone.now]
```

### Block Conditions

```ruby
# Complex logic
can :update, Post do |post|
  post.user_id == user.id || user.admin?
end

# With associations
can :read, Post do |post|
  post.published? || post.user_id == user.id
end

# Accessing current user
can :destroy, Comment do |comment|
  comment.user_id == user.id && comment.created_at > 15.minutes.ago
end
```

**Important**: Block conditions cannot be used with `accessible_by` for database queries. Use hash conditions when you need to filter collections.

### Combining Conditions

```ruby
# Multiple can statements are OR'd together
can :read, Post, published: true          # Public posts
can :read, Post, user_id: user.id         # Own posts
# User can read posts that are EITHER published OR owned by them
```

## Controller Integration

### Manual Authorization

```ruby
class PostsController < ApplicationController
  def show
    @post = Post.find(params[:id])
    authorize! :read, @post  # Raises CanCan::AccessDenied if not authorized
  end

  def update
    @post = Post.find(params[:id])
    authorize! :update, @post

    if @post.update(post_params)
      redirect_to @post
    else
      render :edit
    end
  end
end
```

### Automatic Loading and Authorization

```ruby
class PostsController < ApplicationController
  load_and_authorize_resource

  def index
    # @posts automatically loaded with accessible_by
  end

  def show
    # @post automatically loaded and authorized
  end

  def create
    # @post initialized and authorized
    if @post.save
      redirect_to @post
    else
      render :new
    end
  end

  def update
    # @post loaded and authorized
    if @post.update(post_params)
      redirect_to @post
    else
      render :edit
    end
  end
end
```

**Benefits**: Eliminates repetitive authorization code across RESTful actions.

### Load and Authorize Options

```ruby
# Specific actions only
load_and_authorize_resource only: [:show, :edit, :update, :destroy]
load_and_authorize_resource except: [:index]

# Different resource name
load_and_authorize_resource :article

# Custom find method
load_and_authorize_resource find_by: :slug

# Nested resources
class CommentsController < ApplicationController
  load_and_authorize_resource :post
  load_and_authorize_resource :comment, through: :post
end

# Skip loading (only authorize)
authorize_resource

# Skip authorization for specific actions
skip_authorize_resource only: [:index]
```

## Fetching Authorized Records

### accessible_by

Retrieve only records the user can access:

```ruby
# In controller
def index
  @posts = Post.accessible_by(current_ability)
end

# With specific action
@posts = Post.accessible_by(current_ability, :read)
@editable_posts = Post.accessible_by(current_ability, :update)

# Chainable with ActiveRecord
@published_posts = Post.published.accessible_by(current_ability)
@posts = Post.accessible_by(current_ability).where(category_id: params[:category_id])
```

**Performance**: Uses SQL conditions from ability rules for efficient database queries.

## View Helpers

### Conditional UI Elements

```ruby
# Check single permission
<% if can? :update, @post %>
  <%= link_to 'Edit', edit_post_path(@post) %>
<% end %>

<% if can? :destroy, @post %>
  <%= link_to 'Delete', @post, method: :delete, data: { confirm: 'Are you sure?' } %>
<% end %>

# Negative check
<% if cannot? :update, @post %>
  <p>You cannot edit this post</p>
<% end %>

# Multiple permissions
<% if can?(:update, @post) || can?(:destroy, @post) %>
  <div class="post-actions">
    <%= link_to 'Edit', edit_post_path(@post) if can? :update, @post %>
    <%= link_to 'Delete', @post, method: :delete if can? :destroy, @post %>
  </div>
<% end %>

# Check on class (useful in index views)
<% if can? :create, Post %>
  <%= link_to 'New Post', new_post_path %>
<% end %>
```

### Navigation Menus

```ruby
<nav>
  <%= link_to 'Posts', posts_path if can? :read, Post %>
  <%= link_to 'New Post', new_post_path if can? :create, Post %>
  <%= link_to 'Admin', admin_path if can? :manage, :all %>
</nav>
```

## Handling Unauthorized Access

### Exception Rescue

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  rescue_from CanCan::AccessDenied do |exception|
    respond_to do |format|
      format.html { redirect_to root_path, alert: exception.message }
      format.json { render json: { error: exception.message }, status: :forbidden }
    end
  end
end
```

### Custom Error Messages

```ruby
# In Ability class
can :update, Post, user_id: user.id do |post|
  post.user_id == user.id
end

# In controller with custom message
authorize! :update, @post, message: "You can only edit your own posts"
```

### Flash Messages

```ruby
rescue_from CanCan::AccessDenied do |exception|
  redirect_to root_path, alert: "Access denied: #{exception.message}"
end
```

## Common Patterns

### Role-Based Authorization

```ruby
# app/models/user.rb
class User < ApplicationRecord
  ROLES = %w[guest user moderator admin].freeze

  enum role: { guest: 0, user: 1, moderator: 2, admin: 3 }

  def role?(check_role)
    role.to_sym == check_role.to_sym
  end
end

# app/models/ability.rb
class Ability
  include CanCan::Ability

  def initialize(user)
    user ||= User.new # Guest user

    if user.admin?
      can :manage, :all
    elsif user.moderator?
      can :manage, Post
      can :manage, Comment
      can :read, User
    elsif user.user?
      can :read, :all
      can :create, Post
      can :manage, Post, user_id: user.id
      can :manage, Comment, user_id: user.id
    else
      can :read, Post, published: true
    end
  end
end
```

### Organization/Tenant-Based Authorization

```ruby
class Ability
  include CanCan::Ability

  def initialize(user)
    return unless user.present?

    # User can manage resources in their organization
    can :manage, Post, organization_id: user.organization_id
    can :manage, Comment, post: { organization_id: user.organization_id }

    # Admin can manage organization settings
    can :manage, Organization, id: user.organization_id if user.admin?
  end
end
```

### Time-Based Authorization

```ruby
class Ability
  include CanCan::Ability

  def initialize(user)
    return unless user.present?

    # Can edit posts within 1 hour of creation
    can :update, Post do |post|
      post.user_id == user.id && post.created_at > 1.hour.ago
    end

    # Can read posts after publication date
    can :read, Post, ["published_at <= ?", Time.current]
  end
end
```

### Attribute-Based Authorization

```ruby
class Ability
  include CanCan::Ability

  def initialize(user)
    return unless user.present?

    # Users can update specific attributes of their own posts
    can [:update], Post, user_id: user.id

    # Only admins can change published status
    cannot :update, Post, :published unless user.admin?

    # Users can update their profile but not role
    can :update, User, id: user.id
    cannot :update, User, :role
  end
end
```

## Strong Parameters with CanCanCan

```ruby
# app/controllers/posts_controller.rb
def post_params
  params.require(:post).permit(:title, :body, :published)
end

# Restrict based on abilities
def post_params
  params.require(:post).permit(
    current_user.admin? ? [:title, :body, :published] : [:title, :body]
  )
end
```

## Testing

### RSpec Setup

```ruby
# spec/support/cancan.rb
RSpec.configure do |config|
  config.include CanCan::Ability
end
```

### Testing Abilities

```ruby
# spec/models/ability_spec.rb
require 'rails_helper'
require 'cancan/matchers'

RSpec.describe Ability, type: :model do
  subject(:ability) { Ability.new(user) }

  describe 'Guest user' do
    let(:user) { nil }

    it { is_expected.to be_able_to(:read, Post.new(published: true)) }
    it { is_expected.not_to be_able_to(:create, Post) }
    it { is_expected.not_to be_able_to(:update, Post) }
  end

  describe 'Regular user' do
    let(:user) { create(:user) }
    let(:own_post) { create(:post, user: user) }
    let(:other_post) { create(:post) }

    it { is_expected.to be_able_to(:read, Post) }
    it { is_expected.to be_able_to(:create, Post) }
    it { is_expected.to be_able_to(:update, own_post) }
    it { is_expected.not_to be_able_to(:update, other_post) }
    it { is_expected.to be_able_to(:destroy, own_post) }
    it { is_expected.not_to be_able_to(:destroy, other_post) }
  end

  describe 'Admin user' do
    let(:user) { create(:user, admin: true) }

    it { is_expected.to be_able_to(:manage, :all) }
  end
end
```

### Testing Controllers

```ruby
# spec/controllers/posts_controller_spec.rb
RSpec.describe PostsController, type: :controller do
  let(:user) { create(:user) }
  let(:other_user) { create(:user) }
  let(:post) { create(:post, user: user) }

  before { sign_in user }

  describe 'GET #edit' do
    context 'when editing own post' do
      it 'allows access' do
        get :edit, params: { id: post.id }
        expect(response).to have_http_status(:ok)
      end
    end

    context 'when editing other user post' do
      let(:other_post) { create(:post, user: other_user) }

      it 'denies access' do
        expect {
          get :edit, params: { id: other_post.id }
        }.to raise_error(CanCan::AccessDenied)
      end
    end
  end
end
```

### Testing accessible_by

```ruby
RSpec.describe 'Post access', type: :model do
  let(:user) { create(:user) }
  let(:admin) { create(:user, admin: true) }
  let!(:published_post) { create(:post, published: true) }
  let!(:draft_post) { create(:post, published: false, user: user) }
  let!(:other_draft) { create(:post, published: false) }

  it 'returns correct posts for user' do
    ability = Ability.new(user)
    accessible = Post.accessible_by(ability)

    expect(accessible).to include(published_post, draft_post)
    expect(accessible).not_to include(other_draft)
  end

  it 'returns all posts for admin' do
    ability = Ability.new(admin)
    accessible = Post.accessible_by(ability)

    expect(accessible).to include(published_post, draft_post, other_draft)
  end
end
```

## Performance Considerations

### Use Hash Conditions for Collections

```ruby
# Good - generates SQL query
can :read, Post, user_id: user.id
@posts = Post.accessible_by(current_ability)

# Bad - cannot generate SQL, will raise error
can :read, Post do |post|
  post.user_id == user.id
end
@posts = Post.accessible_by(current_ability)  # Error!
```

### Eager Loading

```ruby
# Prevent N+1 queries
@posts = Post.accessible_by(current_ability).includes(:user, :comments)
```

### Caching Abilities

```ruby
# Cache ability checks in instance variable
def current_ability
  @current_ability ||= Ability.new(current_user)
end
```

## Integration with Pundit

If migrating from Pundit or using both:

```ruby
# CanCanCan uses a single Ability class
# Pundit uses policy classes per model

# They can coexist, but choose one primary approach
# CanCanCan: Centralized, better for simple RBAC
# Pundit: Decentralized, better for complex domain logic
```

## Advanced Patterns

For more complex scenarios, see:
- **Multi-tenancy**: [references/multi-tenancy.md](references/multi-tenancy.md)
- **API authorization**: [references/api-authorization.md](references/api-authorization.md)
- **Complex permissions**: [references/complex-permissions.md](references/complex-permissions.md)

## Resources

- [CanCanCan GitHub](https://github.com/CanCanCommunity/cancancan)
- [CanCanCan Wiki](https://github.com/CanCanCommunity/cancancan/wiki)
