---
name: hanami
description: |
  Hanami 2+ framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Hanami projects, or when the user mentions Hanami.
  Provides clean architecture, dry-rb integration, ROM, and modular design guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: ruby
  extensions: ".rb"
---

# Hanami Guide

> Applies to: Hanami 2.x, Ruby 3.1+, Web Applications, APIs, Domain-Driven Design, Clean Architecture

## Core Principles

1. **Clean Architecture**: Strict separation between delivery (actions/views) and domain (operations/repos)
2. **Slices as Bounded Contexts**: Each slice is an isolated module with its own dependencies
3. **Dependency Injection**: Auto-injection via `include Deps[...]` -- no globals, no singletons
4. **dry-rb Ecosystem**: Leverage dry-types, dry-monads, dry-validation for type safety and result handling
5. **ROM Persistence**: Relations for queries, repositories for data access, entities for domain objects
6. **Convention Over Configuration**: Predictable file layout, auto-registration of components

## Guardrails

### Architecture

- Use slices for bounded contexts (e.g., `slices/api/`, `slices/admin/`)
- Keep actions thin -- delegate to operations for business logic
- Operations return `Dry::Monads::Result` (Success/Failure), never raise for domain errors
- Repositories wrap ROM relations -- never call relations directly from actions
- Entities are value objects (ROM::Struct) -- keep behavior minimal
- Use providers for external service registration (`config/providers/`)

### Actions

- One action per route handler (no fat controllers)
- Validate params with `params do ... end` block inside the action
- Always check `request.params.valid?` before processing
- Use `halt` for early returns (401, 403, 404)
- Handle exceptions with `handle_exception` class method
- Web actions render views; API actions set `response.body` with JSON

### Views & Templates

- Views expose data to templates via `expose` declarations
- Keep logic in view classes, not in ERB templates
- Use layouts for shared page structure (`config.layout = "app"`)
- Templates use ERB by default; keep them presentation-only

### Persistence (ROM)

- Relations define schema, associations, and reusable query scopes
- Use `infer: true` in relation schema to auto-detect columns
- Repositories define commands (`:create`, `update: :by_pk`, `delete: :by_pk`)
- Wrap multi-step writes in `transaction` blocks
- Use `combine` for eager loading associations (avoids N+1)
- Paginate with `.limit().offset()` -- never load unbounded datasets

### Security

- Validate all inputs at the action params layer
- Use parameterized queries via ROM (never string interpolation)
- Hash passwords with bcrypt; verify with constant-time comparison
- Store secrets in settings (`config/settings.rb`), loaded from environment
- API auth: verify JWT tokens in a base action `before` hook or `authenticate!` method
- Set CSP headers via `config.actions.content_security_policy`

### Testing

- Use RSpec with `rack-test` for request specs
- Use `database_cleaner-sequel` with transaction strategy
- Test operations in isolation (unit tests) -- they are pure business logic
- Test actions as request specs (integration) -- verify HTTP status and body
- Use `factory_bot` for test data setup
- Coverage target: >80% for operations and repositories

## Project Structure

```
myapp/
├── app/                      # Main application slice
│   ├── action.rb             # Base action class
│   ├── view.rb               # Base view class
│   ├── actions/              # Route handlers (one class per endpoint)
│   │   └── users/
│   │       ├── index.rb
│   │       ├── show.rb
│   │       └── create.rb
│   ├── views/                # View classes (expose data to templates)
│   │   └── users/
│   │       ├── index.rb
│   │       └── show.rb
│   └── templates/            # ERB templates
│       ├── layouts/
│       │   └── app.html.erb
│       └── users/
│           ├── index.html.erb
│           └── show.html.erb
├── slices/                   # Additional slices (bounded contexts)
│   └── api/
│       ├── action.rb         # API base action (format :json)
│       └── actions/
│           └── v1/
│               └── users/
├── config/
│   ├── app.rb                # Application configuration
│   ├── routes.rb             # Route definitions
│   ├── settings.rb           # Settings schema (env vars)
│   └── providers/            # Service providers
├── db/
│   ├── migrate/              # ROM migrations
│   └── seeds.rb
├── lib/
│   └── myapp/
│       ├── entities/          # ROM structs (value objects)
│       ├── repositories/      # Data access (ROM repositories)
│       ├── operations/        # Business logic (dry-monads)
│       ├── services/          # Infrastructure services
│       └── types.rb           # Custom dry-types
├── spec/
│   ├── spec_helper.rb
│   ├── support/
│   ├── actions/
│   ├── operations/
│   └── repositories/
├── Gemfile
└── config.ru
```

### Layer Responsibilities

| Layer | Knows About | Never References |
|-------|-------------|-----------------|
| Actions | Operations, views, params | Repositories, ROM directly |
| Views | Exposed data, template helpers | Actions, operations |
| Operations | Repositories, services, monads | Actions, views, request/response |
| Repositories | ROM relations, entities | Operations, actions |
| Services | External APIs, libraries | Actions, views |

## Quick Reference Commands

```bash
# Create new app
gem install hanami
hanami new myapp && cd myapp

# Development
bundle exec hanami server            # Start dev server
bundle exec hanami console           # Interactive console

# Generate components
bundle exec hanami generate slice api
bundle exec hanami generate action web.users.index
bundle exec hanami generate relation users

# Database
bundle exec hanami db create
bundle exec hanami db migrate
bundle exec hanami db seed

# Testing
bundle exec rspec
bundle exec rspec --format documentation
```

## Configuration

### Application (config/app.rb)

```ruby
# config/app.rb
require "hanami"

module MyApp
  class App < Hanami::App
    config.actions.default_response_format = :html
    config.actions.content_security_policy[:default_src] = "'self'"

    config.sessions = :cookie, {
      key: "_myapp_session",
      secret: settings.session_secret,
      expire_after: 60 * 60 * 24 * 7
    }
  end
end
```

### Settings (config/settings.rb)

```ruby
module MyApp
  class Settings < Hanami::Settings
    setting :database_url, constructor: Types::String
    setting :session_secret, constructor: Types::String
    setting :redis_url, constructor: Types::String.optional
    setting :log_level, default: "info",
      constructor: Types::String.enum("debug", "info", "warn", "error")
  end
end
```

### Routes (config/routes.rb)

```ruby
module MyApp
  class Routes < Hanami::Routes
    root to: "home.index"

    scope "users" do
      get "/", to: "users.index"
      get "/new", to: "users.new"
      post "/", to: "users.create"
      get "/:id", to: "users.show"
      patch "/:id", to: "users.update"
      delete "/:id", to: "users.destroy"
    end

    # Mount a slice at a path prefix
    slice :api, at: "/api" do
      scope "v1" do
        get "/users", to: "v1.users.index"
        post "/users", to: "v1.users.create"
        get "/users/:id", to: "v1.users.show"
      end
    end
  end
end
```

## Actions

### Web Action

```ruby
# app/actions/users/create.rb
module MyApp
  module Actions
    module Users
      class Create < MyApp::Action
        include Deps["operations.users.create"]

        params do
          required(:user).hash do
            required(:email).filled(:string)
            required(:name).filled(:string)
            required(:password).filled(:string, min_size?: 8)
          end
        end

        def handle(request, response)
          unless request.params.valid?
            response.render(view, errors: request.params.errors)
            return
          end

          result = create.call(request.params[:user])

          if result.success?
            response.flash[:success] = "User created"
            response.redirect_to routes.path(:users_show, id: result.value!.id)
          else
            response.render(view, errors: result.failure)
          end
        end
      end
    end
  end
end
```

### API Base Action (Slice)

```ruby
# slices/api/action.rb -- JSON-only base with JWT auth and error handlers
module API
  class Action < Hanami::Action
    format :json

    handle_exception ROM::TupleCountMismatchError => :handle_not_found
    handle_exception StandardError => :handle_error

    private

    def authenticate!
      token = request.get_header("HTTP_AUTHORIZATION")&.sub("Bearer ", "")
      halt 401, { error: "Missing token" }.to_json unless token
      payload = JWT.decode(token, ENV["JWT_SECRET"], true, algorithm: "HS256").first
      @current_user = user_repo.find(payload["user_id"])
      halt 401, { error: "Invalid token" }.to_json unless @current_user
    rescue JWT::DecodeError
      halt 401, { error: "Invalid token" }.to_json
    end

    def handle_not_found(_req, res, _ex) = (res.status = 404; res.body = { error: "Not found" }.to_json)
    def handle_error(_req, res, ex)       = (Hanami.logger.error(ex); res.status = 500; res.body = { error: "Internal server error" }.to_json)
  end
end
```

### API Endpoint

```ruby
# slices/api/actions/v1/users/index.rb
module API
  module Actions
    module V1
      module Users
        class Index < API::Action
          include Deps["repositories.user_repo"]

          params do
            optional(:page).filled(:integer, gt?: 0)
            optional(:per_page).filled(:integer, gt?: 0, lteq?: 100)
          end

          def handle(request, response)
            page = request.params[:page] || 1
            per_page = request.params[:per_page] || 20
            users = user_repo.all_paginated(page: page, per_page: per_page)

            response.body = {
              users: users.map { |u| { id: u.id, email: u.email, name: u.name } },
              meta: { page: page, per_page: per_page, total: user_repo.count }
            }.to_json
          end
        end
      end
    end
  end
end
```

## Persistence (ROM)

### Relation

```ruby
# lib/myapp/persistence/relations/users.rb
module MyApp
  module Persistence
    module Relations
      class Users < ROM::Relation[:sql]
        schema(:users, infer: true) do
          associations do
            has_many :posts
          end
        end

        def by_id(id)    = where(id: id)
        def by_email(e)  = where(email: e.downcase)
        def active        = where(active: true)
        def with_posts    = combine(:posts)
      end
    end
  end
end
```

### Repository

```ruby
# lib/myapp/repositories/user_repo.rb
module MyApp
  module Repositories
    class UserRepo < ROM::Repository[:users]
      include Deps[container: "persistence.rom"]

      commands :create, update: :by_pk, delete: :by_pk

      def find(id)              = users.by_id(id).one
      def find_by_email(email)  = users.by_email(email).one
      def all_active             = users.active.to_a
      def count                  = users.count

      def all_paginated(page:, per_page:)
        users.active
          .order { created_at.desc }
          .limit(per_page)
          .offset((page - 1) * per_page)
          .to_a
      end
    end
  end
end
```

### Migration

```ruby
# db/migrate/20240115000001_create_users.rb
ROM::SQL.migration do
  change do
    create_table :users do
      primary_key :id
      column :email, String, null: false, unique: true
      column :name, String, null: false
      column :password_digest, String, null: false
      column :role, String, default: "user"
      column :active, TrueClass, default: true
      column :created_at, DateTime, null: false
      column :updated_at, DateTime, null: false
    end

    add_index :users, :email, unique: true
  end
end
```

## Operations (Business Logic)

```ruby
# lib/myapp/operations/users/create.rb
require "dry/monads"

module MyApp
  module Operations
    module Users
      class Create
        include Dry::Monads[:result]
        include Deps["repositories.user_repo", "services.password_hasher"]

        def call(params)
          return Failure(email: ["already taken"]) if user_repo.find_by_email(params[:email])

          user = user_repo.create(
            email: params[:email].downcase.strip,
            name: params[:name].strip,
            password_digest: password_hasher.hash(params[:password]),
            created_at: Time.now,
            updated_at: Time.now
          )

          Success(user)
        rescue => e
          Hanami.logger.error(e)
          Failure(base: ["An unexpected error occurred"])
        end
      end
    end
  end
end
```

## Views & Providers

```ruby
# app/view.rb -- Base view: set layout, expose shared data
module MyApp
  class View < Hanami::View
    config.paths = [File.join(__dir__, "templates")]
    config.layout = "app"
    expose :current_user
    expose :flash
  end
end

# app/views/users/show.rb -- Expose user, add helper methods for templates
module MyApp
  module Views
    module Users
      class Show < MyApp::View
        expose :user
        private
        def user_posts(user) = user.posts.select(&:published?)
      end
    end
  end
end

# config/providers/services.rb -- Register services in the DI container
Hanami.app.register_provider :services do
  start do
    register "services.password_hasher", MyApp::Services::PasswordHasher.new
    register "services.jwt_encoder", MyApp::Services::JWTEncoder.new
  end
end
```

## Dependencies

| Gem | Purpose |
|-----|---------|
| `hanami` (~> 2.1), `-router`, `-controller`, `-view` | Framework core |
| `puma` (~> 6.0) | Application server |
| `rom` (~> 5.3), `rom-sql` (~> 3.6), `pg` | Persistence (ROM + PostgreSQL) |
| `dry-types`, `dry-monads`, `dry-validation` | Type system, results, validation |
| `bcrypt` (~> 3.1), `jwt` (~> 2.7) | Auth (password hashing, tokens) |
| `rspec`, `rack-test`, `database_cleaner-sequel`, `factory_bot` | Testing |

## Advanced Topics

For detailed patterns, validation contracts, interactors, testing strategies, assets, and deployment, see:

- [references/patterns.md](references/patterns.md) -- ROM advanced queries, dry-validation contracts, interactor pipelines, testing patterns, asset management, deployment

## External References

- [Hanami Guides](https://guides.hanamirb.org/)
- [Hanami API Docs](https://hanamirb.org/api/)
- [Hanami GitHub](https://github.com/hanami/hanami)
- [ROM Documentation](https://rom-rb.org/)
- [Dry-rb Libraries](https://dry-rb.org/)
