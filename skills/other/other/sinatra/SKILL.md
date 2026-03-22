---
name: sinatra
description: |
  Sinatra framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Sinatra projects, or when the user mentions Sinatra.
  Provides lightweight Ruby web patterns, routing DSL, middleware, and REST API guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: ruby
  extensions: ".rb"
---

# Sinatra Framework Guide

> Applies to: Sinatra 3.x, Ruby 3.0+, REST APIs, Microservices, Prototypes
> Language Guide: @.claude/skills/ruby-guide/SKILL.md

## Overview

Sinatra is a lightweight DSL for building web applications and APIs in Ruby. It maps HTTP verbs directly to Ruby blocks, providing minimal ceremony and maximum flexibility.

**Use Sinatra when:**
- Building microservices or small-to-medium APIs
- Rapid prototyping or proof-of-concept work
- Lightweight webhooks, proxies, or internal tools
- You want minimal framework overhead

**Consider alternatives when:**
- You need a full MVC framework (use Rails)
- You need built-in admin, ORM, and auth out of the box (use Rails)
- Application complexity exceeds 10+ route modules (use Rails or Hanami)

## Guardrails

### Sinatra-Specific Guidelines

- Use modular style (`Sinatra::Base`) for production applications
- Classic style is acceptable for scripts and prototypes only
- Use `sinatra-contrib` for JSON, namespaces, and reloader support
- Use Puma as the production application server
- Use Bundler for dependency management with a Gemfile
- Separate routes into modules via `register` and `Sinatra::Namespace`
- Extract helpers into dedicated modules under `app/helpers/`
- Use service objects for business logic (keep routes thin)

### Security Guidelines

- Never hardcode secrets; use environment variables via `dotenv`
- Set `session_secret` from `ENV` (not random fallback in production)
- Validate all user input before processing
- Use parameterized queries via ActiveRecord or Sequel ORM
- Implement authentication checks with `before` filters
- Use HTTPS in production with proper HSTS headers
- Implement rate limiting via Rack middleware
- Configure CORS restrictively (never `*` in production)

### Testing Guidelines

- Use RSpec with `rack-test` for HTTP integration tests
- Use `database_cleaner` to reset state between tests
- Test both success and error paths for every endpoint
- Mock external services (never call real APIs in tests)
- Use factory_bot for test data setup
- Coverage target: >80% for business logic

## Project Structure

### Simple Application (Prototypes Only)

```
myapp/
├── app.rb              # All routes and config
├── config.ru           # Rack configuration
├── Gemfile
├── public/             # Static assets
├── views/              # ERB/Haml templates
│   ├── layout.erb
│   └── index.erb
└── spec/
    └── app_spec.rb
```

### Modular Application (Production)

```
myapp/
├── config.ru                  # Rack entry point
├── Gemfile
├── Rakefile                   # Database tasks
├── app/
│   ├── main.rb                # Sinatra::Base application class
│   ├── routes/                # Route modules (one per resource)
│   │   ├── auth.rb
│   │   ├── users.rb
│   │   └── posts.rb
│   ├── models/                # ActiveRecord/Sequel models
│   │   ├── user.rb
│   │   └── post.rb
│   ├── services/              # Business logic (no Sinatra imports)
│   │   └── user_service.rb
│   └── helpers/               # Reusable helper modules
│       ├── auth_helper.rb
│       └── response_helper.rb
├── config/
│   ├── database.yml
│   └── environment.rb         # Boot: dotenv, bundler, DB setup
├── db/
│   └── migrations/
├── public/
├── views/
└── spec/
    ├── spec_helper.rb
    ├── routes/
    └── models/
```

Key conventions:
- `app/main.rb` contains the `Sinatra::Base` subclass and wires everything together
- `app/routes/` holds one module per resource, registered via `register`
- `app/services/` holds business logic with no framework coupling
- `app/helpers/` holds modules included via `helpers` DSL
- `config/environment.rb` boots dotenv, bundler, and database connection

## Routing DSL

Sinatra maps HTTP verbs directly to Ruby blocks. Parameters are captured via `:name` symbols.

```ruby
# Basic CRUD routes
get    '/users'     { json users: User.all.map(&:to_h) }
get    '/users/:id' { json user: find_user!.to_h }
post   '/users'     { create_user }
put    '/users/:id' { update_user }
delete '/users/:id' { delete_user }
```

### Route Parameters

```ruby
# Named parameters (available in params hash)
get '/users/:id' do
  user = User.find(params[:id])
  json user: user.to_h
end

# Splat (wildcard) parameters
get '/files/*.*' do
  # params['splat'] => ['path/to/file', 'ext']
end

# Query parameters
get '/search' do
  # params[:q], params[:page]
end

# Regular expression routes
get %r{/posts/(\d+)} do |id|
  Post.find(id)
end
```

### Namespaced Routes

Use `sinatra/namespace` to group routes with shared prefixes.

```ruby
require 'sinatra/namespace'

class App < Sinatra::Base
  register Sinatra::Namespace

  namespace '/api/v1' do
    namespace '/users' do
      get  { json users: User.all.map(&:to_h) }
      post { create_user }

      get '/:id' do
        json user: User.find(params[:id]).to_h
      end
    end
  end
end
```

## Request & Response

### Reading Request Data

```ruby
# JSON body (use a helper for safety)
def json_params
  @json_params ||= begin
    body = request.body.read
    body.empty? ? {} : JSON.parse(body, symbolize_names: true)
  end
rescue JSON::ParserError
  halt 400, json(error: 'Invalid JSON')
end

# Form data
params[:field_name]

# Headers
request.env['HTTP_AUTHORIZATION']
request.content_type
request.accept?('application/json')
```

### Response Patterns

```ruby
# JSON response (via sinatra/json)
get '/health' do
  json status: 'ok', timestamp: Time.now.iso8601
end

# Status codes
post '/users' do
  user = User.create!(json_params)
  status 201
  json user: user.to_h
end

# Halt with error (stops execution immediately)
halt 404, json(error: 'Not found')
halt 401, json(error: 'Unauthorized')
halt 422, json(errors: user.errors.full_messages)

# Redirect
redirect '/login'
redirect '/users', 303  # See Other

# Headers
headers 'X-Custom-Header' => 'value'
content_type :json
```

## Helpers

Define reusable methods available in routes and views.

```ruby
# In modular style, define helper modules
module AuthHelper
  def current_user
    @current_user ||= User.find_by(id: session[:user_id]) if session[:user_id]
  end

  def require_login!
    halt 401, json(error: 'Unauthorized') unless current_user
  end

  def require_admin!
    require_login!
    halt 403, json(error: 'Forbidden') unless current_user.admin?
  end
end

module ResponseHelper
  def paginate(collection, per_page: 20)
    page = (params[:page] || 1).to_i
    per  = (params[:per_page] || per_page).to_i
    total = collection.count
    items = collection.offset((page - 1) * per).limit(per)

    { items: items, meta: { page: page, per_page: per, total: total } }
  end
end

# Register in the app
class App < Sinatra::Base
  helpers AuthHelper
  helpers ResponseHelper
end
```

## Views & Templates

Sinatra supports ERB, Haml, Slim, and other Tilt-compatible template engines. For JSON APIs, skip views entirely and use the `json` helper.

```ruby
# Render a template (looks in views/ directory)
get '/' do
  @title = 'Home'
  erb :index            # renders views/index.erb
end

# Custom layout
get '/admin' do
  erb :dashboard, layout: :admin_layout
end
```

Use template inheritance via `<%= yield %>` in `views/layout.erb`. Keep logic out of templates; use helpers and instance variables set in routes.

## Error Handling

### Error Handlers

```ruby
class App < Sinatra::Base
  # Named error handlers
  not_found do
    json error: 'Not found'
  end

  error do
    json error: 'Internal server error'
  end

  # Catch specific exceptions
  error ActiveRecord::RecordNotFound do
    status 404
    json error: 'Resource not found'
  end

  error ActiveRecord::RecordInvalid do |e|
    status 422
    json errors: e.record.errors.full_messages
  end

  error JSON::ParserError do
    status 400
    json error: 'Invalid JSON'
  end
end
```

### Environment-Specific Error Display

```ruby
configure :development do
  enable :show_exceptions
  enable :logging
end

configure :production do
  disable :show_exceptions
  enable :raise_errors
end
```

## Filters

Use `before` and `after` filters for cross-cutting concerns.

```ruby
class App < Sinatra::Base
  # Run before every request
  before do
    content_type :json if request.accept?('application/json')
  end

  # Scoped to path prefix
  before '/api/*' do
    content_type :json
    authenticate_token!
  end

  # Run after every request
  after do
    response.headers['X-Request-Id'] = SecureRandom.uuid
  end
end
```

## Modular Application Pattern

### Application Class (app/main.rb)

```ruby
require 'sinatra/base'
require 'sinatra/json'
require 'sinatra/namespace'

class App < Sinatra::Base
  register Sinatra::Namespace

  configure do
    set :server, :puma
    set :root, File.dirname(__FILE__)
    set :views, proc { File.join(root, '..', 'views') }
    enable :sessions
    set :session_secret, ENV.fetch('SESSION_SECRET')
  end

  configure :development do
    require 'sinatra/reloader'
    register Sinatra::Reloader
    enable :logging
  end

  Dir[File.join(__dir__, 'helpers', '*.rb')].each { |f| require f }
  helpers AuthHelper, ResponseHelper

  Dir[File.join(__dir__, 'routes', '*.rb')].each { |f| require f }
  register Routes::Users
  register Routes::Auth

  get('/health') { json status: 'ok' }
  not_found { json error: 'Not found' }
  error     { json error: 'Internal server error' }
end
```

### Route Module (app/routes/users.rb)

```ruby
module Routes
  module Users
    def self.registered(app)
      app.namespace '/api/v1/users' do
        get    { json users: User.all.map(&:to_h) }
        get('/:id') { json user: User.find(params[:id]).to_h }

        post do
          user = User.create!(json_params)
          status 201
          json user: user.to_h
        rescue ActiveRecord::RecordInvalid => e
          status 422
          json errors: e.record.errors.full_messages
        end
      end
    end
  end
end
```

### Rack Configuration (config.ru)

```ruby
require 'bundler/setup'
Bundler.require(:default, ENV.fetch('RACK_ENV', 'development'))
require_relative 'config/environment'
require_relative 'app/main'
run App
```

## Commands Reference

```bash
# Install dependencies
bundle install

# Run development server (with auto-reload)
bundle exec ruby app.rb
# Or with rackup
bundle exec rackup -p 4567

# Run tests
bundle exec rspec
bundle exec rspec --format documentation

# Run with coverage
bundle exec rspec --format progress --require simplecov

# Database tasks
bundle exec rake db:create
bundle exec rake db:migrate
bundle exec rake db:rollback

# Production server
bundle exec puma -C config/puma.rb

# Console (interactive)
bundle exec pry -r ./config/environment

# Docker
docker build -t myapp .
docker run -p 4567:4567 myapp
```

## Dependencies

| Gem | Purpose |
|-----|---------|
| `sinatra` | Web framework DSL |
| `sinatra-contrib` | Extensions: JSON, namespace, reloader |
| `puma` | Production application server |
| `rake` | Task runner for migrations |
| `dotenv` | Environment variable loading |
| `activerecord` / `sequel` | ORM for database access |
| `pg` | PostgreSQL adapter |
| `bcrypt` | Password hashing (`has_secure_password`) |
| `jwt` | JSON Web Token authentication |
| `rspec` | Test framework |
| `rack-test` | HTTP request helpers for Rack apps |
| `database_cleaner-active_record` | DB cleanup between tests |
| `factory_bot` | Test data factories |

## Advanced Topics

For detailed code examples and advanced patterns, see:

- [references/patterns.md](references/patterns.md) -- Database integration, authentication (sessions and JWT), Rack middleware, testing patterns, deployment, and Sequel ORM alternative

## External References

- [Sinatra Documentation](http://sinatrarb.com/documentation.html)
- [Sinatra Recipes](http://recipes.sinatrarb.com/)
- [Sinatra GitHub](https://github.com/sinatra/sinatra)
- [Sinatra Contrib](https://github.com/sinatra/sinatra/tree/main/sinatra-contrib)
- [Rack Documentation](https://github.com/rack/rack)
