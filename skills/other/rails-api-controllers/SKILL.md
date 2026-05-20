---
name: rails-api-controllers
description: "RESTful API controller patterns for Ruby on Rails. Use when: (1) Building JSON APIs, (2) API versioning, (3) Error handling and status codes, (4) Authentication with tokens/JWT, (5) Rate limiting, (6) CORS configuration, (7) Pagination and filtering, (8) API documentation, (9) Testing API endpoints"
---

# Rails API Controllers

Build production-ready RESTful JSON APIs with Rails. This skill covers API controller patterns, versioning, authentication, error handling, and best practices for modern API development.

<when-to-use>
- Building JSON APIs for mobile apps, SPAs, or third-party integrations
- Creating microservices or API-first applications
- Versioning APIs for backward compatibility
- Implementing token-based authentication (JWT, API keys)
- Adding rate limiting and throttling
- Configuring CORS for cross-origin requests
- Implementing pagination, filtering, and sorting
- Testing API endpoints with RSpec
</when-to-use>

<benefits>
- **RESTful Design** - Follow REST conventions for predictable, maintainable APIs
- **Proper Status Codes** - Use correct HTTP status codes for all responses
- **Error Handling** - Consistent error responses with meaningful messages
- **Versioning** - Support multiple API versions simultaneously
- **Authentication** - Token-based auth without sessions or cookies
- **Performance** - Efficient JSON rendering and database queries
- **Documentation** - Auto-generated API docs with tools like Rswag
</benefits>

<verification-checklist>
Before completing API controller work:
- ✅ Proper HTTP status codes used (200, 201, 204, 400, 401, 403, 404, 422, 500)
- ✅ Consistent JSON response structure
- ✅ Authentication/authorization implemented
- ✅ Error handling covers all edge cases
- ✅ API tests passing (request specs)
- ✅ CORS configured if needed
- ✅ Rate limiting configured for production
- ✅ API documentation generated/updated
</verification-checklist>

<standards>
- Use `ApplicationController` parent with `ActionController::API` for API-only apps
- Return proper HTTP status codes for all responses
- Use consistent JSON structure across all endpoints
- Implement authentication via tokens (JWT, API keys), NOT sessions
- Version APIs via URL path (`/api/v1/`) or Accept header
- Handle errors consistently with JSON error responses
- Use strong parameters for input validation
- Test with request specs, not controller specs
- Document APIs with OpenAPI/Swagger
- Implement rate limiting to prevent abuse
</standards>

---

## API-Only Rails Setup

<pattern name="api-only-application">
<description>Create new API-only Rails application</description>

**Generate API-Only App:**

```bash
# New API-only Rails app (skips views, helpers, assets)
rails new my_api --api

# Or add to existing app
# config/application.rb
module MyApi
  class Application < Rails::Application
    config.api_only = true
  end
end
```

**Base API Controller:**

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::API
  include ActionController::HttpAuthentication::Token::ControllerMethods

  # Global error handling
  rescue_from ActiveRecord::RecordNotFound, with: :not_found
  rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity
  rescue_from ActionController::ParameterMissing, with: :bad_request

  before_action :authenticate

  private

  def authenticate
    authenticate_token || render_unauthorized
  end

  def authenticate_token
    authenticate_with_http_token do |token, options|
      @current_user = User.find_by(api_token: token)
    end
  end

  def render_unauthorized
    render json: { error: 'Unauthorized' }, status: :unauthorized
  end

  def not_found(exception)
    render json: { error: exception.message }, status: :not_found
  end

  def unprocessable_entity(exception)
    render json: {
      error: 'Validation failed',
      details: exception.record.errors.full_messages
    }, status: :unprocessable_entity
  end

  def bad_request(exception)
    render json: { error: exception.message }, status: :bad_request
  end
end
```

**Why:** API-only mode removes unnecessary middleware and optimizes for JSON responses. Centralized error handling ensures consistent responses.
</pattern>

---

## RESTful API Design

<pattern name="restful-resource-controller">
<description>Standard RESTful API controller with all CRUD actions</description>

```ruby
# app/controllers/api/v1/articles_controller.rb
module Api
  module V1
    class ArticlesController < ApplicationController
      before_action :set_article, only: [:show, :update, :destroy]

      # GET /api/v1/articles
      def index
        @articles = Article.published
                          .includes(:author)
                          .page(params[:page])
                          .per(params[:per_page] || 20)

        render json: @articles, status: :ok
      end

      # GET /api/v1/articles/:id
      def show
        render json: @article, status: :ok
      end

      # POST /api/v1/articles
      def create
        @article = Article.new(article_params)
        @article.author = current_user

        if @article.save
          render json: @article, status: :created, location: api_v1_article_url(@article)
        else
          render json: {
            error: 'Failed to create article',
            details: @article.errors.full_messages
          }, status: :unprocessable_entity
        end
      end

      # PATCH/PUT /api/v1/articles/:id
      def update
        if @article.update(article_params)
          render json: @article, status: :ok
        else
          render json: {
            error: 'Failed to update article',
            details: @article.errors.full_messages
          }, status: :unprocessable_entity
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
    end
  end
end
```

**Routes:**

```ruby
# config/routes.rb
Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :articles
    end
  end
end
```

**Why:** Follows REST conventions with proper status codes (200 OK, 201 Created, 204 No Content, 422 Unprocessable Entity). Namespace by version for future API changes.
</pattern>

<pattern name="http-status-codes">
<description>Use correct HTTP status codes for API responses</description>

**Common Status Codes:**

| Code | Symbol | Usage |
|------|--------|-------|
| 200 | `:ok` | Successful GET, PATCH, PUT |
| 201 | `:created` | Successful POST (resource created) |
| 204 | `:no_content` | Successful DELETE (no response body) |
| 400 | `:bad_request` | Invalid request syntax, missing parameters |
| 401 | `:unauthorized` | Missing or invalid authentication |
| 403 | `:forbidden` | Authenticated but lacks permission |
| 404 | `:not_found` | Resource doesn't exist |
| 422 | `:unprocessable_entity` | Validation errors |
| 429 | `:too_many_requests` | Rate limit exceeded |
| 500 | `:internal_server_error` | Server error |

**Examples:**

```ruby
# Success responses
render json: @article, status: :ok                    # 200
render json: @article, status: :created               # 201
head :no_content                                       # 204

# Error responses
render json: { error: 'Bad request' }, status: :bad_request              # 400
render json: { error: 'Unauthorized' }, status: :unauthorized            # 401
render json: { error: 'Forbidden' }, status: :forbidden                  # 403
render json: { error: 'Not found' }, status: :not_found                  # 404
render json: { error: 'Validation failed' }, status: :unprocessable_entity  # 422
```

**Why:** Correct status codes help API clients handle responses appropriately and provide clear semantics about what happened.
</pattern>

---

## API Versioning

<pattern name="url-versioning">
<description>Version APIs via URL namespace for backward compatibility</description>

**Directory Structure:**

```
app/controllers/
└── api/
    ├── v1/
    │   ├── articles_controller.rb
    │   └── users_controller.rb
    └── v2/
        ├── articles_controller.rb
        └── users_controller.rb
```

**V1 Controller:**

```ruby
# app/controllers/api/v1/articles_controller.rb
module Api
  module V1
    class ArticlesController < ApplicationController
      def index
        @articles = Article.all
        render json: @articles
      end
    end
  end
end
```

**V2 Controller (Breaking Changes):**

```ruby
# app/controllers/api/v2/articles_controller.rb
module Api
  module V2
    class ArticlesController < ApplicationController
      def index
        # V2 adds pagination and filtering
        @articles = Article
                    .where(status: params[:status]) if params[:status].present?
                    .page(params[:page])

        render json: {
          data: @articles,
          meta: {
            current_page: @articles.current_page,
            total_pages: @articles.total_pages,
            total_count: @articles.total_count
          }
        }
      end
    end
  end
end
```

**Routes:**

```ruby
# config/routes.rb
Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :articles
    end

    namespace :v2 do
      resources :articles
    end
  end
end
```

**Why:** URL versioning is explicit, easy to test, and allows multiple versions to coexist. Clients can migrate at their own pace.
</pattern>

<antipattern>
<description>Breaking API changes without versioning</description>
<bad-example>

```ruby
# ❌ WRONG - Breaking existing clients
class Api::ArticlesController < ApplicationController
  def index
    # Changed response structure without versioning
    render json: {
      articles: @articles,           # Was just array, now nested
      total: @articles.count          # New field
    }
  end
end
```

</bad-example>
<good-example>

```ruby
# ✅ CORRECT - New version for breaking changes
module Api
  module V1
    class ArticlesController < ApplicationController
      def index
        render json: @articles  # Keep V1 unchanged
      end
    end
  end

  module V2
    class ArticlesController < ApplicationController
      def index
        render json: {
          articles: @articles,
          total: @articles.count
        }
      end
    end
  end
end
```

</good-example>

**Why bad:** Breaking changes without versioning break existing API clients. Always version when changing response structure or behavior.
</antipattern>

---

## Authentication & Authorization

<pattern name="token-authentication">
<description>Token-based authentication for stateless APIs</description>

**User Model:**

```ruby
# app/models/user.rb
class User < ApplicationRecord
  has_secure_password
  has_secure_token :api_token

  # Regenerate token on password change
  after_update :regenerate_api_token, if: :saved_change_to_password_digest?

  private

  def regenerate_api_token
    regenerate_api_token
  end
end
```

**Authentication Controller:**

```ruby
# app/controllers/api/v1/authentication_controller.rb
module Api
  module V1
    class AuthenticationController < ApplicationController
      skip_before_action :authenticate, only: [:create]

      # POST /api/v1/auth
      def create
        user = User.find_by(email: params[:email])

        if user&.authenticate(params[:password])
          render json: {
            token: user.api_token,
            user: {
              id: user.id,
              email: user.email,
              name: user.name
            }
          }, status: :ok
        else
          render json: { error: 'Invalid email or password' }, status: :unauthorized
        end
      end

      # DELETE /api/v1/auth
      def destroy
        current_user.regenerate_api_token
        head :no_content
      end
    end
  end
end
```

**Using Token in Requests:**

```bash
# Client sends token in Authorization header
curl -H "Authorization: Token YOUR_API_TOKEN" \
     https://api.example.com/api/v1/articles
```

**Why:** Token authentication is stateless (no sessions), works across domains, and is suitable for mobile/SPA clients.
</pattern>

<pattern name="jwt-authentication">
<description>JWT (JSON Web Token) authentication for APIs</description>

**Setup:**

```ruby
# Gemfile
gem 'jwt'

# lib/json_web_token.rb
class JsonWebToken
  SECRET_KEY = Rails.application.credentials.secret_key_base

  def self.encode(payload, exp = 24.hours.from_now)
    payload[:exp] = exp.to_i
    JWT.encode(payload, SECRET_KEY)
  end

  def self.decode(token)
    body = JWT.decode(token, SECRET_KEY)[0]
    HashWithIndifferentAccess.new(body)
  rescue JWT::DecodeError, JWT::ExpiredSignature
    nil
  end
end
```

**Application Controller:**

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::API
  before_action :authenticate_request

  private

  def authenticate_request
    header = request.headers['Authorization']
    token = header.split(' ').last if header
    decoded = JsonWebToken.decode(token)

    if decoded
      @current_user = User.find(decoded[:user_id])
    else
      render json: { error: 'Unauthorized' }, status: :unauthorized
    end
  rescue ActiveRecord::RecordNotFound
    render json: { error: 'Unauthorized' }, status: :unauthorized
  end

  attr_reader :current_user
end
```

**Authentication Endpoint:**

```ruby
# app/controllers/api/v1/authentication_controller.rb
module Api
  module V1
    class AuthenticationController < ApplicationController
      skip_before_action :authenticate_request, only: [:create]

      def create
        user = User.find_by(email: params[:email])

        if user&.authenticate(params[:password])
          token = JsonWebToken.encode(user_id: user.id)
          render json: { token: token, user: user }, status: :ok
        else
          render json: { error: 'Invalid credentials' }, status: :unauthorized
        end
      end
    end
  end
end
```

**Why:** JWT is self-contained, stateless, and can include claims (user_id, roles, expiration). Widely supported by API clients.
</pattern>

---

## Pagination, Filtering & Sorting

<pattern name="pagination">
<description>Paginate API responses with Kaminari or Pagy</description>

**With Kaminari:**

```ruby
# Gemfile
gem 'kaminari'

# app/controllers/api/v1/articles_controller.rb
def index
  page = params[:page] || 1
  per_page = params[:per_page] || 20

  @articles = Article.page(page).per(per_page)

  render json: {
    data: @articles,
    meta: {
      current_page: @articles.current_page,
      next_page: @articles.next_page,
      prev_page: @articles.prev_page,
      total_pages: @articles.total_pages,
      total_count: @articles.total_count
    }
  }
end
```

**With Pagy (Faster):**

```ruby
# Gemfile
gem 'pagy'

# app/controllers/application_controller.rb
include Pagy::Backend

# app/controllers/api/v1/articles_controller.rb
def index
  pagy, articles = pagy(Article.all, items: params[:per_page] || 20)

  render json: {
    data: articles,
    meta: {
      current_page: pagy.page,
      total_pages: pagy.pages,
      total_count: pagy.count,
      per_page: pagy.items
    }
  }
end
```

**Why:** Pagination prevents loading large datasets into memory. Include metadata so clients know how to fetch more pages.
</pattern>

<pattern name="filtering-and-sorting">
<description>Allow clients to filter and sort resources</description>

```ruby
# app/controllers/api/v1/articles_controller.rb
def index
  @articles = Article.all

  # Filtering
  @articles = @articles.where(status: params[:status]) if params[:status].present?
  @articles = @articles.where(category: params[:category]) if params[:category].present?
  @articles = @articles.where('created_at >= ?', params[:from_date]) if params[:from_date].present?

  # Searching
  @articles = @articles.where('title ILIKE ?', "%#{params[:q]}%") if params[:q].present?

  # Sorting
  sort_column = params[:sort_by] || 'created_at'
  sort_direction = params[:order] || 'desc'
  @articles = @articles.order("#{sort_column} #{sort_direction}")

  # Pagination
  @articles = @articles.page(params[:page]).per(params[:per_page] || 20)

  render json: {
    data: @articles,
    meta: pagination_meta(@articles)
  }
end

private

def pagination_meta(collection)
  {
    current_page: collection.current_page,
    total_pages: collection.total_pages,
    total_count: collection.total_count
  }
end
```

**Example Requests:**

```bash
# Filter by status
GET /api/v1/articles?status=published

# Search by title
GET /api/v1/articles?q=rails

# Sort by created_at descending
GET /api/v1/articles?sort_by=created_at&order=desc

# Combine filters, search, sort, and pagination
GET /api/v1/articles?status=published&q=rails&sort_by=title&order=asc&page=2&per_page=50
```

**Why:** Flexible filtering and sorting let clients fetch exactly what they need without loading unnecessary data.
</pattern>

---

## CORS Configuration

<pattern name="cors-setup">
<description>Configure CORS to allow cross-origin API requests</description>

**Setup:**

```ruby
# Gemfile
gem 'rack-cors'

# config/initializers/cors.rb
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins 'example.com', 'localhost:3000'  # Whitelist specific origins

    resource '/api/*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options, :head],
      credentials: true,
      max_age: 86400  # Cache preflight for 24 hours
  end
end
```

**Development (Allow All Origins):**

```ruby
# config/initializers/cors.rb
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    if Rails.env.development?
      origins '*'  # Allow all in development
    else
      origins ENV['ALLOWED_ORIGINS']&.split(',') || 'example.com'
    end

    resource '/api/*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options, :head]
  end
end
```

**Why:** CORS is required when frontend (SPA, mobile app) and API are on different domains. Whitelist specific origins in production for security.
</pattern>

---

## Rate Limiting

<pattern name="rate-limiting">
<description>Implement rate limiting to prevent API abuse</description>

**With Rack::Attack:**

```ruby
# Gemfile
gem 'rack-attack'

# config/initializers/rack_attack.rb
class Rack::Attack
  # Throttle all requests by IP (60 requests per minute)
  throttle('req/ip', limit: 60, period: 1.minute) do |req|
    req.ip if req.path.start_with?('/api/')
  end

  # Throttle POST requests by IP (10 per minute)
  throttle('req/ip/post', limit: 10, period: 1.minute) do |req|
    req.ip if req.path.start_with?('/api/') && req.post?
  end

  # Throttle authenticated requests by user token
  throttle('req/token', limit: 100, period: 1.minute) do |req|
    if req.path.start_with?('/api/')
      token = req.env['HTTP_AUTHORIZATION']&.split(' ')&.last
      User.find_by(api_token: token)&.id if token
    end
  end

  # Custom response for throttled requests
  self.throttled_responder = lambda do |env|
    [
      429,
      { 'Content-Type' => 'application/json' },
      [{ error: 'Rate limit exceeded. Try again later.' }.to_json]
    ]
  end
end

# config/application.rb
config.middleware.use Rack::Attack
```

**Why:** Rate limiting prevents abuse, protects server resources, and ensures fair usage across all API clients.
</pattern>

---

## Error Handling

<pattern name="consistent-error-responses">
<description>Standardized error response format</description>

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::API
  rescue_from StandardError, with: :internal_server_error
  rescue_from ActiveRecord::RecordNotFound, with: :not_found
  rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity
  rescue_from ActionController::ParameterMissing, with: :bad_request
  rescue_from Pundit::NotAuthorizedError, with: :forbidden

  private

  def not_found(exception)
    render json: error_response(
      'Resource not found',
      exception.message
    ), status: :not_found
  end

  def unprocessable_entity(exception)
    render json: error_response(
      'Validation failed',
      exception.record.errors.full_messages
    ), status: :unprocessable_entity
  end

  def bad_request(exception)
    render json: error_response(
      'Bad request',
      exception.message
    ), status: :bad_request
  end

  def forbidden(exception)
    render json: error_response(
      'Forbidden',
      'You are not authorized to perform this action'
    ), status: :forbidden
  end

  def internal_server_error(exception)
    # Log error for debugging
    Rails.logger.error(exception.message)
    Rails.logger.error(exception.backtrace.join("\n"))

    render json: error_response(
      'Internal server error',
      Rails.env.production? ? 'Something went wrong' : exception.message
    ), status: :internal_server_error
  end

  def error_response(message, details = nil)
    response = { error: message }
    response[:details] = details if details.present?
    response
  end
end
```

**Example Error Responses:**

```json
// 404 Not Found
{
  "error": "Resource not found",
  "details": "Couldn't find Article with 'id'=999"
}

// 422 Unprocessable Entity
{
  "error": "Validation failed",
  "details": [
    "Title can't be blank",
    "Body is too short (minimum is 10 characters)"
  ]
}

// 400 Bad Request
{
  "error": "Bad request",
  "details": "param is missing or the value is empty: article"
}
```

**Why:** Consistent error format makes it easy for clients to parse and display errors. Include details for debugging without exposing sensitive info.
</pattern>

---

## Testing API Endpoints

<pattern name="request-specs">
<description>Test API endpoints with RSpec request specs</description>

```ruby
# spec/requests/api/v1/articles_spec.rb
require 'rails_helper'

RSpec.describe 'Api::V1::Articles', type: :request do
  let(:user) { create(:user) }
  let(:headers) { { 'Authorization' => "Token #{user.api_token}" } }

  describe 'GET /api/v1/articles' do
    let!(:articles) { create_list(:article, 3, :published) }

    it 'returns all published articles' do
      get '/api/v1/articles', headers: headers

      expect(response).to have_http_status(:ok)
      expect(json_response['data'].size).to eq(3)
    end

    it 'filters by status' do
      draft = create(:article, status: :draft)

      get '/api/v1/articles', params: { status: 'draft' }, headers: headers

      expect(response).to have_http_status(:ok)
      expect(json_response['data'].size).to eq(1)
      expect(json_response['data'].first['id']).to eq(draft.id)
    end

    it 'paginates results' do
      create_list(:article, 25)

      get '/api/v1/articles', params: { page: 2, per_page: 10 }, headers: headers

      expect(response).to have_http_status(:ok)
      expect(json_response['data'].size).to eq(10)
      expect(json_response['meta']['current_page']).to eq(2)
    end
  end

  describe 'POST /api/v1/articles' do
    let(:valid_attributes) { { article: { title: 'Test', body: 'Content' } } }

    it 'creates a new article' do
      expect {
        post '/api/v1/articles', params: valid_attributes, headers: headers
      }.to change(Article, :count).by(1)

      expect(response).to have_http_status(:created)
      expect(json_response['title']).to eq('Test')
      expect(response.location).to be_present
    end

    it 'returns errors for invalid data' do
      post '/api/v1/articles', params: { article: { title: '' } }, headers: headers

      expect(response).to have_http_status(:unprocessable_entity)
      expect(json_response['error']).to eq('Failed to create article')
      expect(json_response['details']).to include("Title can't be blank")
    end
  end

  describe 'DELETE /api/v1/articles/:id' do
    let!(:article) { create(:article) }

    it 'deletes the article' do
      expect {
        delete "/api/v1/articles/#{article.id}", headers: headers
      }.to change(Article, :count).by(-1)

      expect(response).to have_http_status(:no_content)
      expect(response.body).to be_empty
    end
  end

  describe 'authentication' do
    it 'returns 401 without token' do
      get '/api/v1/articles'

      expect(response).to have_http_status(:unauthorized)
      expect(json_response['error']).to eq('Unauthorized')
    end

    it 'returns 401 with invalid token' do
      get '/api/v1/articles', headers: { 'Authorization' => 'Token invalid' }

      expect(response).to have_http_status(:unauthorized)
    end
  end

  private

  def json_response
    JSON.parse(response.body)
  end
end
```

**Why:** Request specs test the full HTTP request/response cycle including routing, authentication, and JSON parsing. More realistic than controller specs.
</pattern>

---

<testing>

```ruby
# spec/support/request_helpers.rb
module RequestHelpers
  def json_response
    JSON.parse(response.body)
  end

  def auth_headers(user)
    { 'Authorization' => "Token #{user.api_token}" }
  end
end

RSpec.configure do |config|
  config.include RequestHelpers, type: :request
end

# spec/requests/api/v1/authentication_spec.rb
RSpec.describe 'Api::V1::Authentication', type: :request do
  describe 'POST /api/v1/auth' do
    let(:user) { create(:user, email: 'test@example.com', password: 'password') }

    it 'returns token with valid credentials' do
      post '/api/v1/auth', params: { email: 'test@example.com', password: 'password' }

      expect(response).to have_http_status(:ok)
      expect(json_response['token']).to be_present
      expect(json_response['user']['email']).to eq('test@example.com')
    end

    it 'returns error with invalid credentials' do
      post '/api/v1/auth', params: { email: 'test@example.com', password: 'wrong' }

      expect(response).to have_http_status(:unauthorized)
      expect(json_response['error']).to eq('Invalid email or password')
    end
  end
end
```

</testing>

---

<related-skills>
- rails-ai:models - Model patterns for API resources
- rails-ai:serializers - JSON serialization (ActiveModelSerializers, Blueprinter)
- rails-ai:testing - Testing patterns for API endpoints
- rails-ai:auth-with-devise - Token-based authentication with Devise
- rails-ai:jobs - Background processing for async API operations
</related-skills>

<resources>

**Official Documentation:**
- [Rails Guides - API-Only Applications](https://guides.rubyonrails.org/api_app.html)
- [Rails API Documentation](https://api.rubyonrails.org/)

**Gems & Libraries:**
- [jwt](https://github.com/jwt/ruby-jwt) - JSON Web Token implementation
- [rack-cors](https://github.com/cyu/rack-cors) - CORS middleware
- [rack-attack](https://github.com/rack/rack-attack) - Rate limiting and throttling
- [kaminari](https://github.com/kaminari/kaminari) - Pagination
- [pagy](https://github.com/ddnexus/pagy) - Fast pagination
- [pundit](https://github.com/varvet/pundit) - Authorization

**API Documentation:**
- [rswag](https://github.com/rswag/rswag) - OpenAPI/Swagger docs for Rails APIs
- [apipie-rails](https://github.com/Apipie/apipie-rails) - API documentation tool

**Best Practices:**
- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)

</resources>
