---
name: API Development Patterns
description: "Comprehensive guide to building production-ready REST APIs in Rails with serialization, authentication, versioning, rate limiting, and testing. Trigger keywords: REST API, JSON, serialization, versioning, authentication, JWT, rate limiting, API controllers, request specs, API testing, endpoints, responses"
version: 1.0.0
---

# API Development Patterns

Complete patterns and best practices for building production-grade REST APIs in Rails 7.x/8.x.

## RESTful API Conventions

### Resource-Oriented Design

**Core Principles:**
- Resources are nouns (not verbs): `/users`, `/posts`, not `/get_user`
- Use HTTP methods for actions: GET (read), POST (create), PATCH/PUT (update), DELETE (destroy)
- Nest resources for relationships, but limit nesting to 1-2 levels
- Use plural resource names: `/users` not `/user`

**Standard Resource Routes:**

```ruby
# config/routes.rb
Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :posts do
        resources :comments, only: [:index, :create] # Nested but limited
        member do
          post :publish
          post :archive
        end
        collection do
          get :trending
        end
      end

      # Flat route for comments by ID (better than deep nesting)
      resources :comments, only: [:show, :update, :destroy]
    end
  end
end
```

### HTTP Methods & Status Codes

**Standard API Actions:**

| Method | Action | Success Status | Body |
|--------|--------|----------------|------|
| GET | Index/List | 200 OK | Resource array + pagination |
| GET | Show | 200 OK | Single resource |
| POST | Create | 201 Created | Created resource |
| PATCH/PUT | Update | 200 OK | Updated resource |
| DELETE | Destroy | 204 No Content | Empty |

**Error Status Codes:**

| Code | Meaning | When to Use |
|------|---------|-------------|
| 400 | Bad Request | Invalid JSON, malformed request |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Maintenance mode, overloaded |

**Controller Example:**

```ruby
# app/controllers/api/v1/posts_controller.rb
module Api
  module V1
    class PostsController < Api::BaseController
      before_action :authenticate_api_user!
      before_action :set_post, only: [:show, :update, :destroy]

      def index
        @posts = Post.published
                     .page(params[:page])
                     .per(params[:per_page] || 25)

        render json: PostBlueprint.render(@posts, root: :posts), status: :ok
      end

      def show
        render json: PostBlueprint.render(@post), status: :ok
      end

      def create
        @post = Current.user.posts.build(post_params)

        if @post.save
          render json: PostBlueprint.render(@post), status: :created, location: api_v1_post_url(@post)
        else
          render json: { errors: @post.errors }, status: :unprocessable_entity
        end
      end

      def update
        if @post.update(post_params)
          render json: PostBlueprint.render(@post), status: :ok
        else
          render json: { errors: @post.errors }, status: :unprocessable_entity
        end
      end

      def destroy
        @post.destroy
        head :no_content
      end

      private

      def set_post
        @post = Post.find(params[:id])
      rescue ActiveRecord::RecordNotFound
        render json: { error: "Post not found" }, status: :not_found
      end

      def post_params
        params.require(:post).permit(:title, :body, :published_at, tag_ids: [])
      end
    end
  end
end
```

---

## Serialization Patterns

### Blueprinter (Recommended)

**Installation:**

```ruby
# Gemfile
gem 'blueprinter'
gem 'oj' # Fast JSON parser
```

**Basic Blueprint:**

```ruby
# app/blueprints/post_blueprint.rb
class PostBlueprint < Blueprinter::Base
  identifier :id

  fields :title, :body, :published_at, :created_at

  field :slug do |post|
    post.title.parameterize
  end

  association :author, blueprint: UserBlueprint, view: :compact

  association :comments, blueprint: CommentBlueprint do |post, options|
    post.comments.limit(options[:comment_limit] || 10)
  end

  view :compact do
    fields :id, :title, :slug
  end

  view :extended do
    include_view :default
    fields :view_count, :like_count
    association :tags, blueprint: TagBlueprint
  end
end
```

**Using Views:**

```ruby
# Compact view for lists
PostBlueprint.render(@posts, view: :compact, root: :posts)

# Extended view for show
PostBlueprint.render(@post, view: :extended)

# Pass options to associations
PostBlueprint.render(@post, comment_limit: 5)
```

### JSONAPI::Serializer (Alternative)

**For JSON:API Specification Compliance:**

```ruby
# Gemfile
gem 'jsonapi-serializer'

# app/serializers/post_serializer.rb
class PostSerializer
  include JSONAPI::Serializer

  attributes :title, :body, :published_at

  belongs_to :author, serializer: UserSerializer
  has_many :comments, serializer: CommentSerializer

  attribute :slug do |post|
    post.title.parameterize
  end

  link :self do |post|
    Rails.application.routes.url_helpers.api_v1_post_url(post)
  end
end

# Usage
PostSerializer.new(@posts, include: [:author, :comments]).serializable_hash
```

### Alba (Lightweight Alternative)

```ruby
# Gemfile
gem 'alba'

# app/serializers/post_serializer.rb
class PostSerializer
  include Alba::Resource

  attributes :id, :title, :body, :published_at

  one :author, resource: UserSerializer
  many :comments, resource: CommentSerializer

  attribute :slug do |post|
    post.title.parameterize
  end
end

# Usage
PostSerializer.new(@posts).serialize
```

---

## Authentication

### JWT (JSON Web Tokens)

**Installation:**

```ruby
# Gemfile
gem 'jwt'
gem 'bcrypt' # For password hashing
```

**JWT Service:**

```ruby
# app/services/json_web_token_service.rb
class JsonWebTokenService
  SECRET_KEY = Rails.application.credentials.secret_key_base
  ALGORITHM = 'HS256'

  def self.encode(payload, expiration = 24.hours.from_now)
    payload[:exp] = expiration.to_i
    JWT.encode(payload, SECRET_KEY, ALGORITHM)
  end

  def self.decode(token)
    decoded = JWT.decode(token, SECRET_KEY, true, algorithm: ALGORITHM)[0]
    HashWithIndifferentAccess.new(decoded)
  rescue JWT::DecodeError, JWT::ExpiredSignature => e
    nil
  end
end
```

**Authentication Controller:**

```ruby
# app/controllers/api/v1/authentication_controller.rb
module Api
  module V1
    class AuthenticationController < Api::BaseController
      skip_before_action :authenticate_api_user!, only: [:create]

      def create
        user = User.find_by(email: params[:email])

        if user&.authenticate(params[:password])
          token = JsonWebTokenService.encode(user_id: user.id)
          render json: {
            token: token,
            user: UserBlueprint.render_as_hash(user)
          }, status: :ok
        else
          render json: { error: 'Invalid credentials' }, status: :unauthorized
        end
      end

      def destroy
        # Implement token revocation (requires Redis/database storage)
        head :no_content
      end
    end
  end
end
```

**Base Controller with JWT Authentication:**

```ruby
# app/controllers/api/base_controller.rb
module Api
  class BaseController < ActionController::API
    before_action :authenticate_api_user!

    rescue_from ActiveRecord::RecordNotFound, with: :not_found
    rescue_from ActionController::ParameterMissing, with: :bad_request

    private

    def authenticate_api_user!
      token = request.headers['Authorization']&.split(' ')&.last
      return render_unauthorized unless token

      decoded_token = JsonWebTokenService.decode(token)
      return render_unauthorized unless decoded_token

      @current_user = User.find_by(id: decoded_token[:user_id])
      return render_unauthorized unless @current_user

      # Store in Current for easy access
      Current.user = @current_user
    rescue
      render_unauthorized
    end

    def current_user
      @current_user
    end

    def render_unauthorized
      render json: { error: 'Unauthorized' }, status: :unauthorized
    end

    def not_found
      render json: { error: 'Resource not found' }, status: :not_found
    end

    def bad_request
      render json: { error: 'Bad request' }, status: :bad_request
    end
  end
end
```

### API Keys (Alternative)

**For Service-to-Service Authentication:**

```ruby
# Migration
create_table :api_keys do |t|
  t.references :user, null: false, foreign_key: true
  t.string :key, null: false, index: { unique: true }
  t.string :name # e.g., "Production Server", "Mobile App"
  t.datetime :last_used_at
  t.datetime :expires_at
  t.timestamps
end

# app/models/api_key.rb
class ApiKey < ApplicationRecord
  belongs_to :user

  before_create :generate_key

  scope :active, -> { where('expires_at IS NULL OR expires_at > ?', Time.current) }

  def self.authenticate(key)
    active.find_by(key: key)&.tap do |api_key|
      api_key.update_column(:last_used_at, Time.current)
    end
  end

  private

  def generate_key
    self.key = SecureRandom.base58(32)
  end
end

# Authentication in controller
def authenticate_api_key!
  key = request.headers['X-API-Key'] || params[:api_key]
  return render_unauthorized unless key

  @api_key = ApiKey.authenticate(key)
  return render_unauthorized unless @api_key

  @current_user = @api_key.user
  Current.user = @current_user
end
```

---

## Authorization

### Pundit for APIs

```ruby
# Gemfile
gem 'pundit'

# app/controllers/api/base_controller.rb
module Api
  class BaseController < ActionController::API
    include Pundit::Authorization

    rescue_from Pundit::NotAuthorizedError, with: :forbidden

    private

    def forbidden
      render json: { error: 'Forbidden' }, status: :forbidden
    end
  end
end

# app/policies/post_policy.rb
class PostPolicy < ApplicationPolicy
  def index?
    true
  end

  def show?
    record.published? || record.author == user
  end

  def create?
    user.present?
  end

  def update?
    record.author == user
  end

  def destroy?
    record.author == user || user.admin?
  end
end

# In controller
def show
  @post = Post.find(params[:id])
  authorize @post
  render json: PostBlueprint.render(@post)
end
```

---

## Versioning Strategies

### URL Versioning (Recommended)

**Routes:**

```ruby
# config/routes.rb
Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :posts
    end

    namespace :v2 do
      resources :posts
    end
  end
end
```

**Pros:** Simple, clear, cache-friendly
**Cons:** URLs change between versions

### Header Versioning

```ruby
# config/routes.rb
namespace :api, defaults: { format: :json } do
  scope module: :v1, constraints: ApiVersion.new('v1', default: true) do
    resources :posts
  end

  scope module: :v2, constraints: ApiVersion.new('v2') do
    resources :posts
  end
end

# lib/api_version.rb
class ApiVersion
  def initialize(version, default = false)
    @version = version
    @default = default
  end

  def matches?(request)
    @default || check_headers(request.headers)
  end

  private

  def check_headers(headers)
    accept = headers['Accept']
    accept&.include?("application/vnd.myapp.#{@version}+json")
  end
end
```

**Usage:**
```
Accept: application/vnd.myapp.v2+json
```

---

## Pagination

### Kaminari

```ruby
# Gemfile
gem 'kaminari'

# Controller
def index
  @posts = Post.published
               .page(params[:page])
               .per(params[:per_page] || 25)

  render json: {
    posts: PostBlueprint.render_as_hash(@posts, view: :compact),
    meta: pagination_meta(@posts)
  }
end

private

def pagination_meta(collection)
  {
    current_page: collection.current_page,
    next_page: collection.next_page,
    prev_page: collection.prev_page,
    total_pages: collection.total_pages,
    total_count: collection.total_count,
    per_page: collection.limit_value
  }
end
```

### pagy (Faster Alternative)

```ruby
# Gemfile
gem 'pagy'

# app/controllers/api/base_controller.rb
include Pagy::Backend

def index
  @pagy, @posts = pagy(Post.published, items: params[:per_page] || 25)

  render json: {
    posts: PostBlueprint.render_as_hash(@posts),
    meta: pagy_metadata(@pagy)
  }
end

private

def pagy_metadata(pagy_object)
  {
    current_page: pagy_object.page,
    next_page: pagy_object.next,
    prev_page: pagy_object.prev,
    total_pages: pagy_object.pages,
    total_count: pagy_object.count,
    per_page: pagy_object.items
  }
end
```

---

## Rate Limiting

### Rack::Attack

```ruby
# Gemfile
gem 'rack-attack'

# config/initializers/rack_attack.rb
class Rack::Attack
  # Throttle all requests by IP
  throttle('req/ip', limit: 300, period: 5.minutes) do |req|
    req.ip if req.path.start_with?('/api/')
  end

  # Throttle API requests by authentication token
  throttle('api/token', limit: 1000, period: 1.hour) do |req|
    req.env['HTTP_AUTHORIZATION']&.split(' ')&.last if req.path.start_with?('/api/')
  end

  # Throttle login attempts
  throttle('logins/email', limit: 5, period: 20.minutes) do |req|
    if req.path == '/api/v1/login' && req.post?
      req.params['email'].to_s.downcase.gsub(/\s+/, "")
    end
  end

  # Block specific IPs
  blocklist('block bad IPs') do |req|
    # Read from Redis or database
    Redis.current.sismember('blocked_ips', req.ip)
  end

  # Custom response for throttled requests
  self.throttled_responder = lambda do |env|
    retry_after = env['rack.attack.match_data'][:period]
    [
      429,
      {
        'Content-Type' => 'application/json',
        'Retry-After' => retry_after.to_s
      },
      [{ error: 'Rate limit exceeded', retry_after: retry_after }.to_json]
    ]
  end
end

# config/application.rb
config.middleware.use Rack::Attack
```

---

## Error Handling

### Standardized Error Format

```ruby
# app/controllers/api/base_controller.rb
module Api
  class BaseController < ActionController::API
    rescue_from StandardError, with: :internal_server_error
    rescue_from ActiveRecord::RecordNotFound, with: :not_found
    rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity
    rescue_from ActionController::ParameterMissing, with: :bad_request
    rescue_from Pundit::NotAuthorizedError, with: :forbidden

    private

    def render_error(message, status, details = {})
      render json: {
        error: {
          message: message,
          status: status,
          **details
        }
      }, status: status
    end

    def bad_request(exception)
      render_error('Bad request', :bad_request, details: exception.message)
    end

    def unauthorized
      render_error('Unauthorized', :unauthorized)
    end

    def forbidden(exception)
      render_error('Forbidden', :forbidden, details: exception.message)
    end

    def not_found(exception)
      render_error('Resource not found', :not_found, resource: exception.model)
    end

    def unprocessable_entity(exception)
      render json: {
        error: {
          message: 'Validation failed',
          status: 422,
          errors: exception.record.errors.as_json
        }
      }, status: :unprocessable_entity
    end

    def internal_server_error(exception)
      Rails.logger.error(exception.message)
      Rails.logger.error(exception.backtrace.join("\n"))

      # Report to error tracking service (Sentry, Rollbar, etc.)
      ErrorTrackingService.report(exception) if defined?(ErrorTrackingService)

      render_error('Internal server error', :internal_server_error)
    end
  end
end
```

### Validation Errors Format

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  validates :title, presence: true, length: { minimum: 5, maximum: 100 }
  validates :body, presence: true
end

# Response for validation errors (422):
{
  "error": {
    "message": "Validation failed",
    "status": 422,
    "errors": {
      "title": ["can't be blank", "is too short (minimum is 5 characters)"],
      "body": ["can't be blank"]
    }
  }
}
```

---

## CORS Configuration

```ruby
# Gemfile
gem 'rack-cors'

# config/initializers/cors.rb
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins 'https://example.com', 'https://app.example.com'

    resource '/api/*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options, :head],
      credentials: true,
      max_age: 86400
  end

  # Development
  if Rails.env.development?
    allow do
      origins 'http://localhost:3000', 'http://localhost:3001'
      resource '*', headers: :any, methods: :any
    end
  end
end
```

---

## API Documentation

### rswag (OpenAPI/Swagger)

**Installation:**

```ruby
# Gemfile
gem 'rswag'

# Run installer
rails g rswag:install
```

**Request Spec:**

```ruby
# spec/requests/api/v1/posts_spec.rb
require 'swagger_helper'

RSpec.describe 'API V1 Posts', type: :request do
  path '/api/v1/posts' do
    get 'Retrieves posts' do
      tags 'Posts'
      produces 'application/json'
      parameter name: :page, in: :query, type: :integer, required: false
      parameter name: :per_page, in: :query, type: :integer, required: false

      response '200', 'posts found' do
        schema type: :object,
          properties: {
            posts: {
              type: :array,
              items: {
                type: :object,
                properties: {
                  id: { type: :integer },
                  title: { type: :string },
                  body: { type: :string },
                  published_at: { type: :string, format: 'date-time' }
                },
                required: ['id', 'title']
              }
            },
            meta: {
              type: :object,
              properties: {
                current_page: { type: :integer },
                total_pages: { type: :integer },
                total_count: { type: :integer }
              }
            }
          }

        run_test!
      end
    end

    post 'Creates a post' do
      tags 'Posts'
      consumes 'application/json'
      produces 'application/json'
      parameter name: :post, in: :body, schema: {
        type: :object,
        properties: {
          title: { type: :string },
          body: { type: :string }
        },
        required: ['title', 'body']
      }

      response '201', 'post created' do
        let(:post) { { title: 'Test Post', body: 'Test body' } }
        run_test!
      end

      response '422', 'invalid request' do
        let(:post) { { title: '' } }
        run_test!
      end
    end
  end
end
```

**Generate Swagger Docs:**

```bash
rake rswag:specs:swaggerize
```

**Access at:** `http://localhost:3000/api-docs`

---

## Performance Optimization

### Caching

```ruby
# Controller with caching
def index
  @posts = Rails.cache.fetch(['posts', 'index', params[:page]], expires_in: 5.minutes) do
    Post.published
        .includes(:author, :tags)
        .page(params[:page])
        .per(25)
        .to_a
  end

  render json: PostBlueprint.render(@posts)
end

# ETags for conditional requests
def show
  @post = Post.find(params[:id])

  if stale?(@post)
    render json: PostBlueprint.render(@post)
  end
end
```

### N+1 Query Prevention

```ruby
# Always use includes/eager_load for associations
def index
  @posts = Post.published
               .includes(:author, :tags, comments: :user)
               .page(params[:page])

  render json: PostBlueprint.render(@posts)
end
```

### Bullet Gem (Development)

```ruby
# Gemfile
group :development do
  gem 'bullet'
end

# config/environments/development.rb
config.after_initialize do
  Bullet.enable = true
  Bullet.alert = true
  Bullet.bullet_logger = true
  Bullet.console = true
  Bullet.rails_logger = true
  Bullet.add_footer = false # API doesn't need HTML footer
end
```

---

## Testing

### Request Specs

```ruby
# spec/requests/api/v1/posts_spec.rb
require 'rails_helper'

RSpec.describe 'API V1 Posts', type: :request do
  let(:user) { create(:user) }
  let(:token) { JsonWebTokenService.encode(user_id: user.id) }
  let(:auth_headers) { { 'Authorization' => "Bearer #{token}" } }

  describe 'GET /api/v1/posts' do
    before do
      create_list(:post, 3, :published)
      create(:post, :draft) # Should not be included
    end

    it 'returns published posts' do
      get '/api/v1/posts', headers: auth_headers

      expect(response).to have_http_status(:ok)
      json = JSON.parse(response.body)
      expect(json['posts'].size).to eq(3)
    end

    it 'paginates results' do
      create_list(:post, 30, :published)

      get '/api/v1/posts', params: { page: 2, per_page: 10 }, headers: auth_headers

      json = JSON.parse(response.body)
      expect(json['posts'].size).to eq(10)
      expect(json['meta']['current_page']).to eq(2)
    end

    it 'returns 401 without authentication' do
      get '/api/v1/posts'
      expect(response).to have_http_status(:unauthorized)
    end
  end

  describe 'POST /api/v1/posts' do
    let(:valid_params) do
      { post: { title: 'Test Post', body: 'Test body' } }
    end

    it 'creates a post' do
      expect {
        post '/api/v1/posts', params: valid_params, headers: auth_headers
      }.to change(Post, :count).by(1)

      expect(response).to have_http_status(:created)
      json = JSON.parse(response.body)
      expect(json['title']).to eq('Test Post')
      expect(response.headers['Location']).to be_present
    end

    it 'returns validation errors' do
      post '/api/v1/posts', params: { post: { title: '' } }, headers: auth_headers

      expect(response).to have_http_status(:unprocessable_entity)
      json = JSON.parse(response.body)
      expect(json['error']['errors']).to have_key('title')
    end
  end

  describe 'PATCH /api/v1/posts/:id' do
    let(:post_record) { create(:post, author: user) }

    it 'updates the post' do
      patch "/api/v1/posts/#{post_record.id}",
        params: { post: { title: 'Updated' } },
        headers: auth_headers

      expect(response).to have_http_status(:ok)
      expect(post_record.reload.title).to eq('Updated')
    end

    it 'returns 403 for unauthorized update' do
      other_post = create(:post)

      patch "/api/v1/posts/#{other_post.id}",
        params: { post: { title: 'Hacked' } },
        headers: auth_headers

      expect(response).to have_http_status(:forbidden)
    end
  end
end
```

### Factory for API Testing

```ruby
# spec/factories/users.rb
FactoryBot.define do
  factory :user do
    email { Faker::Internet.email }
    password { 'password123' }
    password_confirmation { 'password123' }
  end
end

# spec/factories/posts.rb
FactoryBot.define do
  factory :post do
    title { Faker::Lorem.sentence }
    body { Faker::Lorem.paragraphs(number: 3).join("\n") }
    association :author, factory: :user

    trait :published do
      published_at { 1.day.ago }
    end

    trait :draft do
      published_at { nil }
    end
  end
end
```

### Shared Examples for API Responses

```ruby
# spec/support/shared_examples/api_responses.rb
RSpec.shared_examples 'requires authentication' do
  it 'returns 401 without token' do
    make_request(headers: {})
    expect(response).to have_http_status(:unauthorized)
  end

  it 'returns 401 with invalid token' do
    make_request(headers: { 'Authorization' => 'Bearer invalid' })
    expect(response).to have_http_status(:unauthorized)
  end
end

RSpec.shared_examples 'paginates results' do
  it 'includes pagination metadata' do
    make_request

    json = JSON.parse(response.body)
    expect(json['meta']).to include(
      'current_page',
      'total_pages',
      'total_count'
    )
  end
end

# Usage in specs
describe 'GET /api/v1/posts' do
  def make_request(headers: auth_headers)
    get '/api/v1/posts', headers: headers
  end

  it_behaves_like 'requires authentication'
  it_behaves_like 'paginates results'
end
```

---

## Security Best Practices

### Input Sanitization

```ruby
# Always use strong parameters
def post_params
  params.require(:post).permit(:title, :body, :published_at, tag_ids: [])
end
```

### SQL Injection Prevention

```ruby
# BAD - vulnerable to SQL injection
Post.where("title = '#{params[:title]}'")

# GOOD - use parameterized queries
Post.where("title = ?", params[:title])
Post.where(title: params[:title])
```

### Mass Assignment Protection

```ruby
# Models automatically protected with strong parameters
# Never use:
Post.new(params[:post]) # BAD
Post.create(params[:post]) # BAD

# Always use:
Post.new(post_params) # GOOD
Post.create(post_params) # GOOD
```

### Sensitive Data Filtering

```ruby
# config/initializers/filter_parameter_logging.rb
Rails.application.config.filter_parameters += [
  :password,
  :password_confirmation,
  :token,
  :api_key,
  :secret,
  :credit_card
]
```

---

## Anti-Patterns to Avoid

### ❌ Don't Return ActiveRecord Objects Directly

```ruby
# BAD
def index
  render json: Post.all # Exposes all attributes
end

# GOOD
def index
  render json: PostBlueprint.render(Post.all)
end
```

### ❌ Don't Use Sessions/Cookies in APIs

```ruby
# APIs should be stateless
# Use JWT or API keys, not session-based authentication
```

### ❌ Don't Skip Authorization

```ruby
# BAD
def destroy
  @post = Post.find(params[:id])
  @post.destroy
end

# GOOD
def destroy
  @post = Post.find(params[:id])
  authorize @post # Pundit
  @post.destroy
end
```

### ❌ Don't Ignore Rate Limiting

```ruby
# Always implement rate limiting for public APIs
# Use Rack::Attack or similar
```

### ❌ Don't Return 200 for All Responses

```ruby
# Use appropriate status codes
# 200 OK, 201 Created, 204 No Content, 400 Bad Request, etc.
```

---

## Summary Checklist

When building a new API endpoint:

- [ ] Use RESTful resource naming and HTTP methods
- [ ] Implement proper authentication (JWT/API keys)
- [ ] Add authorization checks (Pundit)
- [ ] Use serializers (Blueprinter) - never expose raw models
- [ ] Return appropriate HTTP status codes
- [ ] Implement pagination for list endpoints
- [ ] Add rate limiting (Rack::Attack)
- [ ] Configure CORS properly
- [ ] Handle errors consistently
- [ ] Write comprehensive request specs
- [ ] Document with rswag/OpenAPI
- [ ] Optimize queries (includes, caching)
- [ ] Version your API (URL or header)
- [ ] Filter sensitive parameters in logs
- [ ] Use strong parameters for mass assignment protection

This skill provides the foundation for building production-ready REST APIs in Rails!
