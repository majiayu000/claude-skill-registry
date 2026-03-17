---
name: rails-controllers
description: Controller actions, routing, REST conventions, filters, and response handling
version: 1.0.0
rails_version: ">= 7.0"
tags:
  - controllers
  - routing
  - actions
  - rest
---

# Rails Controllers

## Quick Reference

| Pattern | Example |
|---------|---------|
| **Generate** | `rails g controller Posts index show` |
| **Route** | `resources :posts` |
| **Action** | `def show; @post = Post.find(params[:id]); end` |
| **Render** | `render :edit` |
| **Redirect** | `redirect_to posts_path` |
| **Filter** | `before_action :authenticate_user!` |
| **Strong Params** | `params.require(:post).permit(:title, :body)` |

## Controller Structure

```ruby
class PostsController < ApplicationController
  before_action :set_post, only: [:show, :edit, :update, :destroy]
  before_action :authenticate_user!, except: [:index, :show]
  
  # GET /posts
  def index
    @posts = Post.all.order(created_at: :desc)
  end
  
  # GET /posts/:id
  def show
    # @post set by before_action
  end
  
  # GET /posts/new
  def new
    @post = Post.new
  end
  
  # POST /posts
  def create
    @post = Post.new(post_params)
    
    if @post.save
      redirect_to @post, notice: 'Post created successfully.'
    else
      render :new, status: :unprocessable_entity
    end
  end
  
  # GET /posts/:id/edit
  def edit
    # @post set by before_action
  end
  
  # PATCH/PUT /posts/:id
  def update
    if @post.update(post_params)
      redirect_to @post, notice: 'Post updated successfully.'
    else
      render :edit, status: :unprocessable_entity
    end
  end
  
  # DELETE /posts/:id
  def destroy
    @post.destroy
    redirect_to posts_path, notice: 'Post deleted successfully.'
  end
  
  private
  
  def set_post
    @post = Post.find(params[:id])
  end
  
  def post_params
    params.require(:post).permit(:title, :body, :published)
  end
end
```

## Routing

### RESTful Routes

```ruby
# config/routes.rb
Rails.application.routes.draw do
  # Creates 7 standard routes (index, show, new, create, edit, update, destroy)
  resources :posts
  
  # Limit actions
  resources :posts, only: [:index, :show]
  resources :posts, except: [:destroy]
  
  # Nested resources
  resources :authors do
    resources :posts
  end
  # URLs: /authors/:author_id/posts
  
  # Shallow nesting (recommended for deep nesting)
  resources :authors do
    resources :posts, shallow: true
  end
  # URLs: /authors/:author_id/posts (collection)
  #       /posts/:id (member)
  
  # Custom member and collection routes
  resources :posts do
    member do
      post :publish
      post :unpublish
    end
    
    collection do
      get :archived
    end
  end
  # URLs: POST /posts/:id/publish
  #       GET /posts/archived
  
  # Singular resource
  resource :profile, only: [:show, :edit, :update]
  # URLs: /profile (no :id needed)
end
```

### Custom Routes

```ruby
# Named routes
get 'about', to: 'pages#about', as: :about
# Usage: about_path

# Root route
root 'posts#index'

# Redirect
get '/old-path', to: redirect('/new-path')

# Constraints
get 'posts/:id', to: 'posts#show', constraints: { id: /\d+/ }

# Namespace
namespace :admin do
  resources :posts
end
# URLs: /admin/posts
# Controller: Admin::PostsController

# Scope
scope module: 'admin' do
  resources :posts
end
# URLs: /posts
# Controller: Admin::PostsController

# Concern for reusable routes
concern :commentable do
  resources :comments
end

resources :posts, concerns: :commentable
resources :photos, concerns: :commentable
```

## Filters (Callbacks)

```ruby
class ApplicationController < ActionController::Base
  before_action :authenticate_user!
  before_action :set_locale
  around_action :log_request
  after_action :track_analytics
  
  private
  
  def set_locale
    I18n.locale = params[:locale] || I18n.default_locale
  end
  
  def log_request
    start_time = Time.current
    yield
    duration = Time.current - start_time
    Rails.logger.info "Request took #{duration}s"
  end
end

class PostsController < ApplicationController
  skip_before_action :authenticate_user!, only: [:index, :show]
  before_action :set_post, only: [:show, :edit, :update, :destroy]
  before_action :authorize_post, only: [:edit, :update, :destroy]
  
  private
  
  def authorize_post
    unless @post.author == current_user
      redirect_to root_path, alert: 'Not authorized'
    end
  end
end
```

## Strong Parameters

```ruby
class PostsController < ApplicationController
  private
  
  # Basic
  def post_params
    params.require(:post).permit(:title, :body, :published)
  end
  
  # Arrays
  def post_params
    params.require(:post).permit(:title, :body, tag_ids: [])
  end
  
  # Nested attributes
  def post_params
    params.require(:post).permit(
      :title,
      :body,
      comments_attributes: [:id, :content, :_destroy]
    )
  end
  
  # Conditional
  def post_params
    permitted = [:title, :body]
    permitted << :published if current_user.admin?
    params.require(:post).permit(permitted)
  end
end
```

## Rendering and Redirecting

```ruby
class PostsController < ApplicationController
  def show
    @post = Post.find(params[:id])
    
    # Implicit render: renders views/posts/show.html.erb
    
    # Explicit template
    # render :show
    
    # Different template
    # render :custom_template
    
    # Partial
    # render partial: 'post', locals: { post: @post }
    
    # JSON
    # render json: @post
    
    # Plain text
    # render plain: "Hello"
    
    # Status codes
    # render :show, status: :ok
    # render :new, status: :unprocessable_entity
    # render json: { error: 'Not found' }, status: :not_found
  end
  
  def create
    @post = Post.new(post_params)
    
    if @post.save
      # Redirect to show page
      redirect_to @post
      
      # With flash message
      # redirect_to @post, notice: 'Created!'
      
      # With custom path
      # redirect_to posts_path
      
      # Back to previous page
      # redirect_back(fallback_location: root_path)
    else
      render :new, status: :unprocessable_entity
    end
  end
end
```

## Flash Messages

```ruby
class PostsController < ApplicationController
  def create
    @post = Post.new(post_params)
    
    if @post.save
      # Set flash for next request
      flash[:notice] = 'Post created!'
      # Or shorter:
      redirect_to @post, notice: 'Post created!'
      
      # Different flash types
      # flash[:success] = 'Success!'
      # flash[:error] = 'Error!'
      # flash[:alert] = 'Alert!'
      # flash[:warning] = 'Warning!'
    else
      # flash.now for current request
      flash.now[:alert] = 'Could not create post'
      render :new
    end
  end
  
  def update
    # Keep flash for next request
    flash.keep
    redirect_to @post
  end
end
```

## Response Formats

```ruby
class PostsController < ApplicationController
  def show
    @post = Post.find(params[:id])
    
    respond_to do |format|
      format.html # renders show.html.erb
      format.json { render json: @post }
      format.xml { render xml: @post }
      format.pdf { render pdf: generate_pdf(@post) }
    end
  end
  
  def create
    @post = Post.new(post_params)
    
    respond_to do |format|
      if @post.save
        format.html { redirect_to @post, notice: 'Created!' }
        format.json { render json: @post, status: :created }
      else
        format.html { render :new, status: :unprocessable_entity }
        format.json { render json: @post.errors, status: :unprocessable_entity }
      end
    end
  end
end
```

## Controller Concerns

```ruby
# app/controllers/concerns/authenticatable.rb
module Authenticatable
  extend ActiveSupport::Concern
  
  included do
    before_action :authenticate_user!
    helper_method :current_user, :logged_in?
  end
  
  def current_user
    @current_user ||= User.find_by(id: session[:user_id])
  end
  
  def logged_in?
    current_user.present?
  end
  
  def authenticate_user!
    unless logged_in?
      redirect_to login_path, alert: 'Please log in'
    end
  end
end

# Usage
class PostsController < ApplicationController
  include Authenticatable
end
```

## Error Handling

```ruby
class ApplicationController < ActionController::Base
  rescue_from ActiveRecord::RecordNotFound, with: :record_not_found
  rescue_from ActionController::ParameterMissing, with: :parameter_missing
  
  private
  
  def record_not_found
    render file: "#{Rails.root}/public/404.html", status: :not_found
  end
  
  def parameter_missing
    render json: { error: 'Missing parameter' }, status: :bad_request
  end
end

class PostsController < ApplicationController
  def show
    @post = Post.find(params[:id])
  rescue ActiveRecord::RecordNotFound
    redirect_to posts_path, alert: 'Post not found'
  end
end
```

## Session and Cookies

```ruby
class SessionsController < ApplicationController
  def create
    user = User.find_by(email: params[:email])
    
    if user&.authenticate(params[:password])
      # Set session
      session[:user_id] = user.id
      
      # Set cookie
      cookies[:user_name] = user.name
      
      # Signed cookie (tamper-proof)
      cookies.signed[:user_id] = user.id
      
      # Encrypted cookie
      cookies.encrypted[:user_data] = { id: user.id, role: user.role }
      
      # Permanent cookie (20 years)
      cookies.permanent[:remember_token] = user.remember_token
      
      redirect_to root_path
    else
      flash.now[:alert] = 'Invalid credentials'
      render :new
    end
  end
  
  def destroy
    session.delete(:user_id)
    cookies.delete(:user_name)
    redirect_to root_path
  end
end
```

## Best Practices

1. **Keep controllers thin** - Move business logic to models or service objects
2. **Use before_action** for common setup code
3. **Always use strong parameters** for security
4. **Return proper HTTP status codes**
5. **Use concerns** for shared controller behavior
6. **Follow REST conventions** when possible
7. **Handle errors gracefully** with rescue_from
8. **Use flash messages** for user feedback
9. **Set instance variables** only for view rendering
10. **Avoid complex queries** in controllers - use scopes or query objects

## Common Patterns

### Service Objects for Complex Actions

```ruby
class PostsController < ApplicationController
  def create
    result = Posts::CreateService.call(
      params: post_params,
      user: current_user
    )
    
    if result.success?
      redirect_to result.post, notice: 'Created!'
    else
      @post = result.post
      flash.now[:alert] = result.error
      render :new
    end
  end
end
```

### Query Objects for Complex Queries

```ruby
class PostsController < ApplicationController
  def index
    @posts = PostsQuery.new(params).call
  end
end
```

## References

- [Rails Guides - Controllers](https://guides.rubyonrails.org/action_controller_overview.html)
- [Rails Guides - Routing](https://guides.rubyonrails.org/routing.html)
- [Rails API - ActionController](https://api.rubyonrails.org/classes/ActionController/Base.html)
