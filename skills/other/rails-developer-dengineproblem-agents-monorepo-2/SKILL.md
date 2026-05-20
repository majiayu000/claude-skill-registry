---
name: rails-developer
description: Эксперт Ruby on Rails. Используй для Rails приложений, ActiveRecord, Hotwire и Rails best practices.
---

# Ruby on Rails Developer

Expert in Ruby on Rails development with focus on Rails 8, Hotwire, and the Solid Trifecta stack.

## Core Principles

```yaml
stack_philosophy:
  framework: "Rails 8"
  database: "SQLite3 (production-ready)"
  background_jobs: "SolidQueue"
  websockets: "SolidCable"
  caching: "SolidCache"
  frontend: "Hotwire (Turbo + Stimulus)"
  styling: "Tailwind CSS"

code_conventions:
  naming:
    files: "snake_case"
    methods: "snake_case"
    classes: "CamelCase"
    constants: "SCREAMING_SNAKE_CASE"

  structure:
    - "Follow Rails conventions"
    - "RESTful routing"
    - "Thin controllers, fat models"
    - "Service objects for complex logic"
```

## Rails 8 Features

### Authentication

```ruby
# Generate built-in authentication
# rails g authentication

# app/models/user.rb
class User < ApplicationRecord
  has_secure_password

  normalizes :email, with: ->(email) { email.strip.downcase }

  validates :email, presence: true,
                    uniqueness: true,
                    format: { with: URI::MailTo::EMAIL_REGEXP }
end

# app/controllers/sessions_controller.rb
class SessionsController < ApplicationController
  def create
    user = User.find_by(email: params[:email])

    if user&.authenticate(params[:password])
      session[:user_id] = user.id
      redirect_to root_path, notice: "Logged in!"
    else
      flash.now[:alert] = "Invalid email or password"
      render :new, status: :unprocessable_entity
    end
  end

  def destroy
    session[:user_id] = nil
    redirect_to root_path, notice: "Logged out!"
  end
end
```

### Solid Trifecta

```ruby
# config/queue.yml - SolidQueue configuration
production:
  workers:
    - queues: "*"
      threads: 5
      polling_interval: 0.1
  dispatchers:
    - polling_interval: 1
      batch_size: 500

# app/jobs/process_order_job.rb
class ProcessOrderJob < ApplicationJob
  queue_as :default
  retry_on StandardError, wait: :polynomially_longer, attempts: 5

  def perform(order_id)
    order = Order.find(order_id)
    OrderProcessor.new(order).process!
  end
end

# Using SolidCable for ActionCable
# config/cable.yml
production:
  adapter: solid_cable
  polling_interval: 0.1

# Using SolidCache
# config/cache.yml
production:
  store: solid_cache
  size: 256.megabytes
```

## ActiveRecord Patterns

### Models & Validations

```ruby
# app/models/product.rb
class Product < ApplicationRecord
  belongs_to :category
  has_many :order_items, dependent: :restrict_with_error
  has_many :orders, through: :order_items
  has_one_attached :image
  has_rich_text :description

  enum :status, { draft: 0, published: 1, archived: 2 }

  validates :name, presence: true, length: { maximum: 255 }
  validates :price, presence: true, numericality: { greater_than: 0 }
  validates :sku, presence: true, uniqueness: true

  scope :available, -> { published.where("stock > 0") }
  scope :featured, -> { where(featured: true).order(created_at: :desc) }

  before_validation :generate_sku, on: :create
  after_commit :update_search_index, on: [:create, :update]

  private

  def generate_sku
    self.sku ||= "SKU-#{SecureRandom.hex(4).upcase}"
  end

  def update_search_index
    SearchIndexJob.perform_later(self)
  end
end
```

### Query Interface

```ruby
# Efficient queries
class ProductQuery
  def initialize(relation = Product.all)
    @relation = relation
  end

  def search(term)
    return self if term.blank?
    @relation = @relation.where("name ILIKE :term OR description ILIKE :term",
                                 term: "%#{term}%")
    self
  end

  def by_category(category_id)
    return self if category_id.blank?
    @relation = @relation.where(category_id: category_id)
    self
  end

  def price_range(min:, max:)
    @relation = @relation.where(price: min..max) if min && max
    self
  end

  def results
    @relation
  end
end

# Usage
products = ProductQuery.new
  .search(params[:q])
  .by_category(params[:category_id])
  .price_range(min: 10, max: 100)
  .results
  .includes(:category, image_attachment: :blob)
  .page(params[:page])
```

### Migrations

```ruby
# db/migrate/20241201000000_create_orders.rb
class CreateOrders < ActiveRecord::Migration[8.0]
  def change
    create_table :orders do |t|
      t.references :user, null: false, foreign_key: true
      t.string :number, null: false, index: { unique: true }
      t.integer :status, null: false, default: 0
      t.decimal :total, precision: 10, scale: 2, null: false, default: 0
      t.jsonb :metadata, null: false, default: {}
      t.datetime :completed_at

      t.timestamps
    end

    add_index :orders, :status
    add_index :orders, :completed_at
    add_index :orders, [:user_id, :status]
  end
end
```

## Hotwire

### Turbo Frames

```erb
<!-- app/views/products/index.html.erb -->
<%= turbo_frame_tag "products" do %>
  <div class="grid grid-cols-3 gap-4">
    <% @products.each do |product| %>
      <%= render product %>
    <% end %>
  </div>

  <%= paginate @products %>
<% end %>

<!-- app/views/products/_product.html.erb -->
<%= turbo_frame_tag dom_id(product) do %>
  <div class="card" data-controller="product">
    <h3><%= product.name %></h3>
    <p><%= number_to_currency product.price %></p>

    <%= link_to "Edit", edit_product_path(product),
                data: { turbo_frame: "modal" } %>
  </div>
<% end %>
```

### Turbo Streams

```ruby
# app/controllers/comments_controller.rb
class CommentsController < ApplicationController
  def create
    @comment = @post.comments.build(comment_params)
    @comment.user = current_user

    if @comment.save
      respond_to do |format|
        format.turbo_stream
        format.html { redirect_to @post }
      end
    else
      render :new, status: :unprocessable_entity
    end
  end
end

# app/views/comments/create.turbo_stream.erb
<%= turbo_stream.prepend "comments", @comment %>
<%= turbo_stream.update "new_comment" do %>
  <%= render "form", comment: Comment.new %>
<% end %>
<%= turbo_stream.update "comments_count", @post.comments.count %>
```

### Stimulus Controllers

```javascript
// app/javascript/controllers/form_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "submit", "output"]
  static values = {
    url: String,
    debounce: { type: Number, default: 300 }
  }

  connect() {
    this.timeout = null
  }

  search() {
    clearTimeout(this.timeout)
    this.timeout = setTimeout(() => {
      this.performSearch()
    }, this.debounceValue)
  }

  async performSearch() {
    const query = this.inputTarget.value
    if (query.length < 2) return

    this.submitTarget.disabled = true

    try {
      const response = await fetch(`${this.urlValue}?q=${encodeURIComponent(query)}`)
      const html = await response.text()
      this.outputTarget.innerHTML = html
    } finally {
      this.submitTarget.disabled = false
    }
  }
}
```

## Testing with RSpec

```ruby
# spec/models/product_spec.rb
RSpec.describe Product, type: :model do
  describe "validations" do
    subject { build(:product) }

    it { should validate_presence_of(:name) }
    it { should validate_presence_of(:price) }
    it { should validate_uniqueness_of(:sku) }
    it { should validate_numericality_of(:price).is_greater_than(0) }
  end

  describe "associations" do
    it { should belong_to(:category) }
    it { should have_many(:order_items) }
  end

  describe "scopes" do
    describe ".available" do
      let!(:available) { create(:product, status: :published, stock: 10) }
      let!(:out_of_stock) { create(:product, status: :published, stock: 0) }
      let!(:draft) { create(:product, status: :draft, stock: 10) }

      it "returns only published products with stock" do
        expect(Product.available).to contain_exactly(available)
      end
    end
  end
end

# spec/requests/products_spec.rb
RSpec.describe "Products", type: :request do
  describe "GET /products" do
    it "returns successful response" do
      get products_path
      expect(response).to have_http_status(:success)
    end
  end

  describe "POST /products" do
    let(:valid_params) { { product: attributes_for(:product) } }

    context "with valid params" do
      it "creates a new product" do
        expect {
          post products_path, params: valid_params
        }.to change(Product, :count).by(1)
      end
    end
  end
end

# spec/system/products_spec.rb
RSpec.describe "Product management", type: :system do
  before { driven_by(:selenium_chrome_headless) }

  it "allows creating a new product" do
    visit new_product_path

    fill_in "Name", with: "Test Product"
    fill_in "Price", with: "99.99"
    click_button "Create Product"

    expect(page).to have_content("Product was successfully created")
    expect(page).to have_content("Test Product")
  end
end
```

## Performance Optimization

### Caching

```ruby
# Fragment caching with Russian Doll strategy
# app/views/products/_product.html.erb
<% cache product do %>
  <div class="product">
    <% cache [product, "details"] do %>
      <h3><%= product.name %></h3>
      <p><%= product.description %></p>
    <% end %>

    <% cache [product.category, "category"] do %>
      <span class="category"><%= product.category.name %></span>
    <% end %>
  </div>
<% end %>

# Low-level caching
class Product < ApplicationRecord
  def expensive_calculation
    Rails.cache.fetch([cache_key_with_version, "calculation"], expires_in: 1.hour) do
      # Complex computation
      perform_expensive_operation
    end
  end
end

# Counter caching
class Comment < ApplicationRecord
  belongs_to :post, counter_cache: true
end
```

### N+1 Prevention

```ruby
# app/controllers/posts_controller.rb
class PostsController < ApplicationController
  def index
    @posts = Post
      .includes(:author, :comments, :tags)
      .with_attached_image
      .order(created_at: :desc)
      .page(params[:page])
  end
end

# Using strict loading in development
# config/environments/development.rb
config.active_record.strict_loading_by_default = true
```

### Database Optimization

```ruby
# Add proper indexes
class AddIndexesToProducts < ActiveRecord::Migration[8.0]
  def change
    add_index :products, :category_id
    add_index :products, [:status, :created_at]
    add_index :products, :price

    # Partial index
    add_index :products, :featured, where: "featured = true"

    # GIN index for JSONB
    add_index :products, :metadata, using: :gin
  end
end

# Bulk operations
Product.insert_all([
  { name: "Product 1", price: 10 },
  { name: "Product 2", price: 20 }
])

Product.where(status: :draft).update_all(status: :archived)
```

## Security

```ruby
# Strong parameters
class ProductsController < ApplicationController
  private

  def product_params
    params.require(:product).permit(:name, :price, :description,
                                     :category_id, :image, tags: [])
  end
end

# Authorization
class ApplicationController < ActionController::Base
  before_action :authenticate_user!

  private

  def authorize_admin!
    redirect_to root_path, alert: "Not authorized" unless current_user.admin?
  end
end

# Content Security Policy
# config/initializers/content_security_policy.rb
Rails.application.configure do
  config.content_security_policy do |policy|
    policy.default_src :self, :https
    policy.font_src    :self, :https, :data
    policy.img_src     :self, :https, :data
    policy.object_src  :none
    policy.script_src  :self, :https
    policy.style_src   :self, :https, :unsafe_inline
  end
end
```

## API Mode

```ruby
# app/controllers/api/v1/base_controller.rb
module Api
  module V1
    class BaseController < ActionController::API
      include ActionController::HttpAuthentication::Token::ControllerMethods

      before_action :authenticate_api_user!

      private

      def authenticate_api_user!
        authenticate_or_request_with_http_token do |token, options|
          @current_api_user = User.find_by(api_token: token)
        end
      end

      def current_api_user
        @current_api_user
      end
    end
  end
end

# app/controllers/api/v1/products_controller.rb
module Api
  module V1
    class ProductsController < BaseController
      def index
        products = Product.available.page(params[:page]).per(25)

        render json: {
          products: products.as_json(only: [:id, :name, :price]),
          meta: {
            current_page: products.current_page,
            total_pages: products.total_pages,
            total_count: products.total_count
          }
        }
      end

      def show
        product = Product.find(params[:id])
        render json: ProductSerializer.new(product).as_json
      end
    end
  end
end
```

## Лучшие практики

1. **Convention over Configuration** — следуй Rails conventions
2. **Fat Model, Skinny Controller** — логика в моделях и сервисах
3. **Hotwire first** — минимум JavaScript, максимум Turbo
4. **Test everything** — RSpec для моделей, запросов и системных тестов
5. **Cache strategically** — Russian Doll caching для производительности
6. **Secure by default** — strong parameters, CSP, аутентификация
