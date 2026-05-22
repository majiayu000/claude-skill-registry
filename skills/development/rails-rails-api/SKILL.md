---
name: rails-api
description: REST API specialist for Rails applications. Use when building API endpoints, implementing serialization, API versioning, JWT authentication, or creating API documentation. Focuses on RESTful design, performance, and consistency.
---

# Rails REST API Specialist

Build clean, performant REST APIs with Rails.

## When to Use This Skill

- Creating REST API endpoints
- Implementing API serialization (ActiveModel::Serializers, Blueprinter)
- API versioning strategies
- Token-based authentication (JWT, API keys)
- API documentation (OpenAPI/Swagger)
- Rate limiting and throttling
- API error handling
- Performance optimization for APIs

## Core Principles

**RESTful Design:**
- Use standard HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Resource-based URLs (`/api/v1/articles`, not `/api/v1/get_articles`)
- Proper status codes (200, 201, 404, 422, 500)
- Consistent response format
- Stateless requests

## 🚨 API Versioning is MANDATORY

**NEVER create an API without versioning. This is non-negotiable.**

**Why versioning is required:**
- Protects existing clients from breaking changes
- Allows independent evolution of API versions
- Enables deprecation strategies (v1 → v2 → v3)
- Follows industry best practices
- Makes your API maintainable long-term

**Always start with `/api/v1/` from day one, even for internal APIs.**

### Correct vs Wrong Approaches

```ruby
# ❌ WRONG - No versioning (will cause pain later)
namespace :api do
  resources :articles  # Results in: /api/articles
  resources :users     # Impossible to change structure later
end

# ✅ CORRECT - Versioned from start
namespace :api do
  namespace :v1 do
    resources :articles  # Results in: /api/v1/articles
    resources :users     # Can add v2 with breaking changes later
  end
end
```

## Base API Controller

```ruby
# app/controllers/api/base_controller.rb
class Api::BaseController < ActionController::API
  before_action :authenticate

  rescue_from ActiveRecord::RecordNotFound, with: :not_found
  rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity
  rescue_from Pundit::NotAuthorizedError, with: :forbidden

  private

  def not_found(exception)
    render json: { error: exception.message }, status: :not_found
  end

  def unprocessable_entity(exception)
    render json: {
      error: "Validation failed",
      errors: exception.record.errors.full_messages
    }, status: :unprocessable_entity
  end

  def forbidden
    render json: { error: "Access denied" }, status: :forbidden
  end
end
```

## RESTful Controller Pattern

```ruby
# app/controllers/api/v1/articles_controller.rb
class Api::V1::ArticlesController < Api::BaseController
  before_action :set_article, only: [:show, :update, :destroy]

  # GET /api/v1/articles
  def index
    @articles = Article.published
      .page(params[:page])
      .per(params[:per_page] || 20)

    render json: @articles,
      meta: pagination_meta(@articles),
      each_serializer: ArticleSerializer
  end

  # GET /api/v1/articles/:id
  def show
    render json: @article, serializer: ArticleDetailSerializer
  end

  # POST /api/v1/articles
  def create
    @article = current_user.articles.build(article_params)

    if @article.save
      render json: @article,
        status: :created,
        location: api_v1_article_url(@article)
    else
      render json: { errors: @article.errors },
        status: :unprocessable_entity
    end
  end

  # PATCH/PUT /api/v1/articles/:id
  def update
    if @article.update(article_params)
      render json: @article
    else
      render json: { errors: @article.errors },
        status: :unprocessable_entity
    end
  end

  # DELETE /api/v1/articles/:id
  def destroy
    @article.destroy
    head :no_content
  end

  private

  def set_article
    @article = Article.find(params[:id])
  end

  def article_params
    params.require(:article).permit(:title, :body, :published)
  end

  def pagination_meta(collection)
    {
      current_page: collection.current_page,
      total_pages: collection.total_pages,
      total_count: collection.total_count,
      per_page: collection.limit_value
    }
  end
end
```

## Serialization

```ruby
# app/serializers/article_serializer.rb
class ArticleSerializer < ActiveModel::Serializer
  attributes :id, :title, :excerpt, :published_at, :created_at

  belongs_to :author, serializer: UserSerializer
  has_many :tags

  def excerpt
    object.body.truncate(200)
  end
end
```

### Response Format

**Success:**
```json
{
  "data": {
    "id": 123,
    "type": "articles",
    "attributes": {
      "title": "Article Title",
      "excerpt": "Article excerpt..."
    },
    "relationships": {
      "author": { "data": { "id": 1, "type": "users" } }
    }
  },
  "meta": {
    "current_page": 1,
    "total_pages": 10
  }
}
```

**Error:**
```json
{
  "error": "Validation failed",
  "errors": [
    "Title can't be blank",
    "Body is too short"
  ]
}
```

## Authentication

### JWT Authentication

```ruby
# Gemfile
gem 'jwt'

# app/controllers/api/v1/auth_controller.rb
class Api::V1::AuthController < Api::BaseController
  skip_before_action :authenticate, only: [:login]

  def login
    user = User.find_by(email: params[:email])

    if user&.authenticate(params[:password])
      token = encode_token(user_id: user.id)
      render json: {
        token: token,
        user: UserSerializer.new(user),
        expires_at: 24.hours.from_now
      }
    else
      render json: { error: 'Invalid credentials' },
        status: :unauthorized
    end
  end

  private

  def encode_token(payload)
    payload[:exp] = 24.hours.from_now.to_i
    JWT.encode(payload, Rails.application.credentials.secret_key_base)
  end
end

# Update authenticate method in base controller
def authenticate
  token = request.headers['Authorization']&.split(' ')&.last
  return render json: { error: 'No token' }, status: :unauthorized unless token

  begin
    decoded = JWT.decode(token, Rails.application.credentials.secret_key_base)[0]
    @current_user = User.find(decoded['user_id'])
  rescue JWT::ExpiredSignature
    render json: { error: 'Token expired' }, status: :unauthorized
  rescue JWT::DecodeError
    render json: { error: 'Invalid token' }, status: :unauthorized
  end
end
```

### API Key Authentication

```ruby
# app/models/user.rb
class User < ApplicationRecord
  before_create :generate_api_token

  private

  def generate_api_token
    self.api_token = SecureRandom.hex(32)
  end
end

# app/controllers/api/base_controller.rb
def authenticate
  authenticate_or_request_with_http_token do |token, options|
    @current_user = User.find_by(api_token: token)
  end
end
```

## Rate Limiting

```ruby
# Gemfile
gem 'rack-attack'

# config/initializers/rack_attack.rb
class Rack::Attack
  # Throttle all API requests by IP
  throttle('req/ip', limit: 300, period: 5.minutes) do |req|
    req.ip if req.path.start_with?('/api/')
  end

  # Throttle login attempts
  throttle('logins/email', limit: 5, period: 20.seconds) do |req|
    if req.path == '/api/v1/auth/login' && req.post?
      req.params['email'].presence
    end
  end
end

# config/application.rb
config.middleware.use Rack::Attack
```

## Filtering and Pagination

```ruby
def index
  @articles = Article.all
  @articles = apply_filters(@articles)
  @articles = @articles.page(params[:page]).per(params[:per_page] || 20)

  render json: @articles, meta: pagination_meta(@articles)
end

private

def apply_filters(scope)
  scope = scope.where(status: params[:status]) if params[:status].present?
  scope = scope.where(author_id: params[:author_id]) if params[:author_id].present?
  scope = scope.where('created_at >= ?', params[:from_date]) if params[:from_date].present?
  scope
end
```

## Performance

### Avoid N+1 Queries

```ruby
def index
  @articles = Article.includes(:author, :tags)
    .page(params[:page])
    .per(params[:per_page])

  render json: @articles
end
```

### HTTP Caching

```ruby
def show
  @article = Article.find(params[:id])

  if stale?(last_modified: @article.updated_at, etag: @article)
    render json: @article
  end
end
```

## Testing APIs

```ruby
# spec/requests/api/v1/articles_spec.rb
RSpec.describe 'Articles API', type: :request do
  let(:user) { create(:user) }
  let(:token) { JWT.encode({ user_id: user.id }, Rails.application.credentials.secret_key_base) }
  let(:headers) { { 'Authorization' => "Bearer #{token}" } }

  describe 'GET /api/v1/articles' do
    it 'returns articles' do
      create_list(:article, 3, :published)

      get '/api/v1/articles', headers: headers

      expect(response).to have_http_status(:ok)
      expect(JSON.parse(response.body)['data'].size).to eq(3)
    end
  end

  describe 'POST /api/v1/articles' do
    let(:valid_params) do
      { article: { title: 'New Article', body: 'Content' } }
    end

    it 'creates article' do
      expect {
        post '/api/v1/articles', params: valid_params, headers: headers
      }.to change(Article, :count).by(1)

      expect(response).to have_http_status(:created)
    end

    it 'returns errors for invalid params' do
      post '/api/v1/articles', params: { article: { title: '' } }, headers: headers

      expect(response).to have_http_status(:unprocessable_entity)
      expect(JSON.parse(response.body)['errors']).to be_present
    end
  end
end
```

## Best Practices

### ✅ Do

- **ALWAYS version your API (v1, v2, v3)** - MANDATORY, not optional
- Use proper HTTP status codes (200, 201, 404, 422, 500)
- Implement authentication and authorization
- Add rate limiting to prevent abuse
- Document your API (OpenAPI/Swagger)
- Use serializers for consistent responses
- Implement pagination for collections
- Handle errors gracefully with consistent format
- Use ETags for caching
- Test all endpoints with request specs

### ❌ Don't

- **NEVER create API without versioning** - This will cause pain later
- Create routes like `/api/articles` instead of `/api/v1/articles`
- Expose internal IDs without consideration
- Return sensitive data (passwords, tokens, internal fields)
- Use GET for state-changing operations
- Return inconsistent response formats
- Skip authentication on "internal" endpoints
- Expose database errors to clients
- Make breaking changes to existing API versions

---

## Reference Documentation

For comprehensive examples and advanced patterns:
- Full API guide: `api-reference.md` (detailed auth, documentation, testing, all patterns)

---

**Remember**: A good API is **versioned from day one**, consistent, well-documented, secure, and performant. API versioning is not optional—it's a fundamental requirement.
