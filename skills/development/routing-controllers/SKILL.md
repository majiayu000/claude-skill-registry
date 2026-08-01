---
name: routing-controllers
description: This skill should be used when the user asks about Rails routing, URL
  patterns, RESTful routes, route helpers, controller actions, strong parameters,
  before_action callbacks, rendering, redirecting, t
---

---
name: routing-controllers
description: This skill should be used when the user asks about Rails routing, URL patterns, RESTful routes, route helpers, controller actions, strong parameters, before_action callbacks, rendering, redirecting, the params hash, nested resources, route constraints, controller concerns, or request/response handling. Also use when discussing how URLs map to code, route organization, or controller best practices. Examples:

<example>
Context: User is defining routes for a new resource
user: "How do I set up routes for my Blog posts?"
assistant: "I'll explain RESTful routing with the resources helper and controller conventions."
<commentary>
This relates to resource routing, the Rails default for URL patterns.
</commentary>
</example>

<example>
Context: User wants to restrict route parameters
user: "How can I make sure my :id parameter is only numeric?"
assistant: "Let me show you route constraints and parameter validation techniques."
<commentary>
This involves route constraints and controller parameter handling.
</commentary>
</example>

<example>
Context: User is organizing complex controller logic
user: "My controller is getting too fat with all this before logic"
assistant: "I'll demonstrate controller concerns, before_action organization, and keeping controllers thin."
<commentary>
This relates to controller best practices and the fat models, skinny controllers principle.
</commentary>
</example>
---

# Routing & Controllers: Rails Request/Response Cycle

## Overview

Routing and controllers form the entry point for all web requests in Rails. The router matches incoming HTTP requests to controller actions, and controllers coordinate the response. Understanding this layer is essential for building Rails applications.

Rails routing is designed around RESTful principles, using HTTP verbs (GET, POST, PATCH, DELETE) combined with URL paths to map to specific controller actions. This convention-based approach eliminates configuration while providing powerful flexibility when needed.

Controllers in Rails are thin coordinators. They parse requests, delegate to models, and render responses. They should NOT contain business logic—that belongs in models. Controllers handle HTTP concerns, nothing more.

## The Rails Router

### How Routing Works

When a request arrives, Rails asks the router to match it:

```
Request: GET /products/42
Router: Matches to ProductsController#show with params[:id] = "42"
Rails: Creates ProductsController instance, calls show method
Controller: Fetches product, renders view
```

The router is defined in `config/routes.rb` and uses a Ruby DSL to map URLs to controllers.

### RESTful Resource Routing

Rails defaults to RESTful routing via the `resources` helper:

```ruby
# config/routes.rb
Rails.application.routes.draw do
  resources :products
end
```

This single line creates 7 routes:

| Verb | Path | Controller#Action | Purpose |
|------|------|-------------------|---------|
| GET | /products | products#index | List all products |
| GET | /products/new | products#new | Form to create product |
| POST | /products | products#create | Create product |
| GET | /products/:id | products#show | Show specific product |
| GET | /products/:id/edit | products#edit | Form to edit product |
| PATCH/PUT | /products/:id | products#update | Update product |
| DELETE | /products/:id | products#destroy | Delete product |

Plus path helpers:
- `products_path` → `/products`
- `new_product_path` → `/products/new`
- `product_path(@product)` → `/products/42`
- `edit_product_path(@product)` → `/products/42/edit`

This is the Rails Way: conventional routes that cover standard CRUD operations.

### Singular Resources

For resources that exist once per user (like a profile or settings), use singular routing:

```ruby
resource :profile  # No :id needed
```

Creates these routes:

| Verb | Path | Controller#Action | Purpose |
|------|------|-------------------|---------|
| GET | /profile/new | profiles#new | Form to create profile |
| POST | /profile | profiles#create | Create profile |
| GET | /profile | profiles#show | Show profile |
| GET | /profile/edit | profiles#edit | Form to edit profile |
| PATCH/PUT | /profile | profiles#update | Update profile |
| DELETE | /profile | profiles#destroy | Delete profile |

Notice: no `index` action, no `:id` in URLs.

### Nested Resources

When resources have parent-child relationships, nest routes:

```ruby
resources :categories do
  resources :products
end
```

Creates URLs like:
- `/categories/1/products` → products in category 1
- `/categories/1/products/new` → new product in category 1
- `/categories/1/products/5` → product 5 in category 1

And path helpers:
- `category_products_path(@category)`
- `new_category_product_path(@category)`
- `category_product_path(@category, @product)`

**Best Practice:** Limit nesting to 1 level deep. Beyond that, use shallow nesting:

```ruby
resources :categories do
  resources :products, shallow: true
end
```

This creates:
- `/categories/1/products` (collection route, needs category)
- `/products/5` (member route, doesn't need category)

### Custom Routes

Beyond RESTful defaults, add custom actions:

```ruby
resources :products do
  member do
    post :duplicate    # /products/:id/duplicate
    get :preview       # /products/:id/preview
  end

  collection do
    get :search        # /products/search
    post :bulk_update  # /products/bulk_update
  end
end
```

**Member routes** act on a specific resource (require `:id`)
**Collection routes** act on the collection (no `:id`)

### Route Constraints

Constrain routes to match only certain patterns:

```ruby
# Only numeric IDs
resources :products, constraints: { id: /\d+/ }

# Only specific formats
resources :products, constraints: { format: /json|xml/ }

# Complex constraints
constraints(subdomain: 'api') do
  resources :products, defaults: { format: :json }
end
```

### Route Order Matters

Rails matches routes in order. More specific routes should come first:

```ruby
# WRONG ORDER
resources :photos
get 'photos/search', to: 'photos#search'  # Never matches!

# CORRECT ORDER
get 'photos/search', to: 'photos#search'  # Matches first
resources :photos
```

See `references/routing-patterns.md` for advanced routing techniques.

## Controllers

### Controller Basics

Controllers inherit from `ApplicationController` and define actions as public methods:

```ruby
class ProductsController < ApplicationController
  def index
    @products = Product.all
    # Rails automatically renders app/views/products/index.html.erb
  end

  def show
    @product = Product.find(params[:id])
    # Rails automatically renders app/views/products/show.html.erb
  end
end
```

Rails conventions:
- Controller name is plural: `ProductsController`
- Corresponds to `products` resource
- Actions match RESTful route names
- Instance variables (`@product`) available in views
- Views render automatically unless you specify otherwise

### The params Hash

The `params` hash contains all request data:

```ruby
# URL: /products?category=electronics&page=2
params[:category]  # => "electronics"
params[:page]      # => "2"

# Route: /products/:id
params[:id]        # => "42" (from URL)

# Form submission
params[:product]   # => { "name" => "Widget", "price" => "9.99" }
```

**Important:** `params` values are always strings. Convert as needed:

```ruby
page = params[:page].to_i
price = params[:price].to_f
published = params[:published] == "true"
```

### Strong Parameters (Rails 8)

Rails 8 introduces `params.expect` for safer parameter handling:

```ruby
def create
  # Old way (still works)
  @product = Product.new(product_params)

  # Rails 8 way
  @product = Product.new(params.expect(product: [:name, :price, :description]))

  if @product.save
    redirect_to @product
  else
    render :new
  end
end

private

# Traditional strong parameters
def product_params
  params.require(:product).permit(:name, :price, :description)
end
```

`expect` is clearer and more explicit than `require(...).permit(...)`.

**Nested parameters:**

```ruby
params.expect(product: [:name, :price, category: [:name, :description]])
```

**Arrays:**

```ruby
params.expect(product: [:name, tags: []])
```

See `references/strong-parameters.md` for comprehensive coverage.

### Before Actions (Callbacks)

Run code before actions execute:

```ruby
class ProductsController < ApplicationController
  before_action :set_product, only: [:show, :edit, :update, :destroy]
  before_action :require_login
  before_action :authorize_admin, only: [:edit, :update, :destroy]

  def show
    # @product already set by before_action
  end

  def edit
    # @product set, login required, admin authorized
  end

  private

  def set_product
    @product = Product.find(params[:id])
  end

  def require_login
    redirect_to login_path unless logged_in?
  end

  def authorize_admin
    redirect_to root_path unless current_user.admin?
  end
end
```

Other callbacks:
- `after_action` - runs after action completes
- `around_action` - wraps action execution
- `skip_before_action :callback_name` - skip inherited callbacks

### Rendering and Redirecting

**Implicit rendering:**

```ruby
def show
  @product = Product.find(params[:id])
  # Automatically renders app/views/products/show.html.erb
end
```

**Explicit rendering:**

```ruby
def show
  @product = Product.find(params[:id])
  render :show  # Same as implicit
  render 'products/show'  # Full path
  render template: 'products/show'
  render file: '/path/to/template'
end
```

**Rendering different formats:**

```ruby
def show
  @product = Product.find(params[:id])

  respond_to do |format|
    format.html  # Renders show.html.erb
    format.json { render json: @product }
    format.xml  { render xml: @product }
  end
end
```

**Redirecting:**

```ruby
redirect_to @product              # Uses product_path(@product)
redirect_to products_path         # List of products
redirect_to root_path             # Application root
redirect_to 'https://example.com' # External URL
redirect_to products_path, notice: 'Product created!'
redirect_to products_path, alert: 'Error occurred!'
```

**Important:** You can only render OR redirect once per action. Doing both causes an error.

### The Flash

Temporary messages for the next request:

```ruby
def create
  @product = Product.new(product_params)
  if @product.save
    flash[:notice] = "Product created successfully!"
    redirect_to @product
  else
    flash.now[:alert] = "Error creating product"
    render :new
  end
end
```

- `flash[:notice]` - persists to next request (for redirects)
- `flash.now[:alert]` - only current request (for renders)
- `flash[:success]`, `flash[:error]`, `flash[:warning]` - custom keys

Access in views:

```erb
<% if flash[:notice] %>
  <div class="notice"><%= flash[:notice] %></div>
<% end %>
```

Shorthand for redirect:

```ruby
redirect_to @product, notice: "Created!"
redirect_to @product, alert: "Error!"
```

### Sessions and Cookies

**Session:**

```ruby
# Store data across requests
session[:user_id] = @user.id
current_user_id = session[:user_id]
session.delete(:user_id)  # Logout
```

**Cookies:**

```ruby
# Persistent client-side storage
cookies[:theme] = 'dark'
cookies[:theme]  # => "dark"
cookies.delete(:theme)

# Signed cookies (tamper-proof)
cookies.signed[:user_id] = @user.id

# Encrypted cookies (secret)
cookies.encrypted[:api_token] = @user.api_token
```

### Controller Concerns

Extract shared behavior into concerns:

```ruby
# app/controllers/concerns/authenticable.rb
module Authenticable
  extend ActiveSupport::Concern

  included do
    before_action :require_login
  end

  private

  def require_login
    redirect_to login_path unless logged_in?
  end

  def logged_in?
    !!current_user
  end

  def current_user
    @current_user ||= User.find_by(id: session[:user_id])
  end
end

# app/controllers/products_controller.rb
class ProductsController < ApplicationController
  include Authenticable

  # now has require_login, logged_in?, current_user methods
end
```

## Controller Best Practices

### Keep Controllers Thin

Controllers should coordinate, not implement business logic:

**Bad (Fat Controller):**

```ruby
def create
  @order = Order.new(order_params)
  @order.user = current_user

  # Business logic in controller - BAD!
  total = 0
  @order.line_items.each do |item|
    total += item.quantity * item.product.price
  end
  @order.total = total

  if @order.total > 1000
    @order.discount = @order.total * 0.1
  end

  # More business logic...
  if @order.save
    # Email logic in controller - BAD!
    OrderMailer.confirmation(@order).deliver_later

    # Inventory logic in controller - BAD!
    @order.line_items.each do |item|
      item.product.decrement!(:inventory, item.quantity)
    end

    redirect_to @order
  else
    render :new
  end
end
```

**Good (Thin Controller, Fat Model):**

```ruby
def create
  @order = Order.new(order_params)
  @order.user = current_user

  if @order.place  # Business logic in model
    redirect_to @order, notice: "Order placed!"
  else
    render :new
  end
end

# app/models/order.rb
class Order < ApplicationRecord
  def place
    transaction do
      calculate_total
      apply_discount
      save!
      send_confirmation
      update_inventory
    end
  rescue ActiveRecord::RecordInvalid
    false
  end

  private

  def calculate_total
    self.total = line_items.sum { |item| item.quantity * item.product.price }
  end

  def apply_discount
    self.discount = total * 0.1 if total > 1000
  end

  def send_confirmation
    OrderMailer.confirmation(self).deliver_later
  end

  def update_inventory
    line_items.each { |item| item.product.decrement!(:inventory, item.quantity) }
  end
end
```

### Standard CRUD Actions

Follow the pattern:

```ruby
class ProductsController < ApplicationController
  before_action :set_product, only: [:show, :edit, :update, :destroy]

  def index
    @products = Product.all
  end

  def show
  end

  def new
    @product = Product.new
  end

  def create
    @product = Product.new(product_params)
    if @product.save
      redirect_to @product, notice: 'Created!'
    else
      render :new
    end
  end

  def edit
  end

  def update
    if @product.update(product_params)
      redirect_to @product, notice: 'Updated!'
    else
      render :edit
    end
  end

  def destroy
    @product.destroy
    redirect_to products_path, notice: 'Deleted!'
  end

  private

  def set_product
    @product = Product.find(params[:id])
  end

  def product_params
    params.expect(product: [:name, :price, :description])
  end
end
```

This pattern is conventional, predictable, and maintainable.

### Error Handling

Handle missing records gracefully:

```ruby
def set_product
  @product = Product.find(params[:id])
rescue ActiveRecord::RecordNotFound
  redirect_to products_path, alert: "Product not found"
end
```

Or use `find_by` to avoid exceptions:

```ruby
def set_product
  @product = Product.find_by(id: params[:id])
  redirect_to products_path, alert: "Product not found" unless @product
end
```

## Request and Response Objects

Access request details:

```ruby
request.remote_ip        # Client IP
request.format           # Requested format (:html, :json, etc.)
request.method           # HTTP verb (:get, :post, etc.)
request.headers          # HTTP headers
request.path             # URL path
request.fullpath         # Path with query string
request.protocol         # "http://" or "https://"
request.host             # "example.com"
request.port             # 80, 443, etc.
```

Modify response:

```ruby
response.headers['X-Custom-Header'] = 'value'
response.status = 404
response.content_type = 'application/json'
```

## Common Patterns

### Responders

Handle multiple formats cleanly:

```ruby
def show
  @product = Product.find(params[:id])

  respond_to do |format|
    format.html
    format.json { render json: @product }
    format.pdf { render pdf: @product }
  end
end
```

## Further Reading

For deeper exploration:

- **`references/routing-patterns.md`**: Advanced routing techniques (constraints, custom routes, route testing)
- **`references/strong-parameters.md`**: Complete guide to parameter handling and security

For code examples:

- **`examples/restful-controllers.rb`**: Complete CRUD controller examples

## Summary

Routing and controllers in Rails are about:
- **RESTful conventions** that map HTTP to CRUD operations
- **Resourceful routing** via `resources` helper
- **Thin controllers** that coordinate, not implement
- **Strong parameters** for security (`expect` in Rails 8)
- **Before actions** for DRY code
- **Concerns** for shared behavior
- **Fat models, skinny controllers** philosophy

Master routing and controllers, and you master how Rails applications respond to the world.
