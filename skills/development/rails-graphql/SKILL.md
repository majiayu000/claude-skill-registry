---
name: rails-graphql
description: GraphQL specialist for Rails applications. Use when building GraphQL schemas, resolvers, mutations, subscriptions, or implementing DataLoader for N+1 prevention. Alternative to REST APIs with flexible querying capabilities.
---

# Rails GraphQL Specialist

Build flexible, efficient GraphQL APIs with Rails.

## When to Use This Skill

- Creating GraphQL schemas and types
- Implementing query resolvers
- Building mutations (create, update, delete)
- Setting up subscriptions (real-time updates)
- Preventing N+1 queries with DataLoader
- GraphQL authentication and authorization
- Query complexity analysis
- Testing GraphQL endpoints

## Setup

```ruby
# Gemfile
gem 'graphql'
gem 'graphiql-rails', group: :development  # GraphQL IDE

# Install
bundle install
rails generate graphql:install

# This creates:
# app/graphql/
#   types/
#   mutations/
#   my_app_schema.rb
# app/controllers/graphql_controller.rb
```

## Schema Design

### Type Definitions

```ruby
# app/graphql/types/user_type.rb
module Types
  class UserType < Types::BaseObject
    description "A user in the system"

    field :id, ID, null: false
    field :email, String, null: false
    field :name, String, null: true
    field :avatar_url, String, null: true
    field :created_at, GraphQL::Types::ISO8601DateTime, null: false

    # Associations
    field :posts, [Types::PostType], null: true
    field :comments, [Types::CommentType], null: true

    # Computed fields
    field :posts_count, Integer, null: false

    def posts_count
      object.posts.count
    end

    def avatar_url
      object.avatar.attached? ? Rails.application.routes.url_helpers.url_for(object.avatar) : nil
    end
  end
end
```

### Query Type

```ruby
# app/graphql/types/query_type.rb
module Types
  class QueryType < Types::BaseObject
    # Single resource
    field :user, Types::UserType, null: true do
      description "Find a user by ID"
      argument :id, ID, required: true
    end

    def user(id:)
      User.find_by(id: id)
    end

    # Collection with pagination
    field :users, [Types::UserType], null: false do
      description "List all users"
      argument :limit, Integer, required: false, default_value: 20
      argument :offset, Integer, required: false, default_value: 0
      argument :search, String, required: false
    end

    def users(limit:, offset:, search: nil)
      scope = User.all
      scope = scope.where("name ILIKE ?", "%#{search}%") if search.present?
      scope.limit(limit).offset(offset)
    end

    # Current user
    field :me, Types::UserType, null: true do
      description "Get currently authenticated user"
    end

    def me
      context[:current_user]
    end
  end
end
```

## Mutations

### Base Mutation

```ruby
# app/graphql/mutations/base_mutation.rb
module Mutations
  class BaseMutation < GraphQL::Schema::RelayClassicMutation
    argument_class Types::BaseArgument
    field_class Types::BaseField
    input_object_class Types::BaseInputObject
    object_class Types::BaseObject

    def current_user
      context[:current_user]
    end

    def authenticate!
      raise GraphQL::ExecutionError, "Authentication required" unless current_user
    end

    def authorize!(record, action)
      policy = Pundit.policy!(current_user, record)
      raise GraphQL::ExecutionError, "Not authorized" unless policy.public_send("#{action}?")
    end
  end
end
```

### Create Mutation

```ruby
# app/graphql/mutations/create_post.rb
module Mutations
  class CreatePost < BaseMutation
    description "Create a new post"

    argument :title, String, required: true
    argument :body, String, required: true
    argument :published, Boolean, required: false, default_value: false

    field :post, Types::PostType, null: true
    field :errors, [String], null: false

    def resolve(title:, body:, published:)
      authenticate!

      post = current_user.posts.build(
        title: title,
        body: body,
        published: published
      )

      if post.save
        # Trigger subscription
        MyAppSchema.subscriptions.trigger('postCreated', {}, post)

        { post: post, errors: [] }
      else
        { post: nil, errors: post.errors.full_messages }
      end
    end
  end
end
```

### Update Mutation

```ruby
# app/graphql/mutations/update_post.rb
module Mutations
  class UpdatePost < BaseMutation
    argument :id, ID, required: true
    argument :title, String, required: false
    argument :body, String, required: false
    argument :published, Boolean, required: false

    field :post, Types::PostType, null: true
    field :errors, [String], null: false

    def resolve(id:, **attributes)
      authenticate!

      post = Post.find(id)
      authorize!(post, :update)

      if post.update(attributes.compact)
        { post: post, errors: [] }
      else
        { post: nil, errors: post.errors.full_messages }
      end
    rescue ActiveRecord::RecordNotFound
      { post: nil, errors: ["Post not found"] }
    end
  end
end
```

### Delete Mutation

```ruby
# app/graphql/mutations/delete_post.rb
module Mutations
  class DeletePost < BaseMutation
    argument :id, ID, required: true

    field :success, Boolean, null: false
    field :errors, [String], null: false

    def resolve(id:)
      authenticate!

      post = Post.find(id)
      authorize!(post, :destroy)

      if post.destroy
        { success: true, errors: [] }
      else
        { success: false, errors: post.errors.full_messages }
      end
    rescue ActiveRecord::RecordNotFound
      { success: false, errors: ["Post not found"] }
    end
  end
end
```

## DataLoader (N+1 Prevention)

### Record Loader

```ruby
# app/graphql/loaders/record_loader.rb
module Loaders
  class RecordLoader < GraphQL::Dataloader::Source
    def initialize(model, column: model.primary_key, where: nil)
      @model = model
      @column = column.to_s
      @column_type = model.type_for_attribute(@column)
      @where = where
    end

    def fetch(keys)
      records = @model.where(@column => keys)
      records = records.merge(@where) if @where

      key_to_record = records.index_by { |record| @column_type.cast(record.public_send(@column)) }
      keys.map { |key| key_to_record[@column_type.cast(key)] }
    end
  end
end
```

### Association Loader

```ruby
# app/graphql/loaders/association_loader.rb
module Loaders
  class AssociationLoader < GraphQL::Dataloader::Source
    def initialize(model, association_name)
      @model = model
      @association_name = association_name
    end

    def fetch(records)
      ActiveRecord::Associations::Preloader.new(
        records: records,
        associations: @association_name
      ).call

      records.map { |record| record.public_send(@association_name) }
    end
  end
end
```

### Usage in Types

```ruby
module Types
  class PostType < Types::BaseObject
    field :author, Types::UserType, null: false

    def author
      # Instead of: object.author (causes N+1)
      dataloader.with(Loaders::RecordLoader, User).load(object.user_id)
    end

    field :comments, [Types::CommentType], null: false

    def comments
      # Instead of: object.comments (causes N+1)
      dataloader.with(Loaders::AssociationLoader, Post, :comments).load(object)
    end
  end
end
```

## Subscriptions

### Subscription Type

```ruby
# app/graphql/types/subscription_type.rb
module Types
  class SubscriptionType < Types::BaseObject
    field :post_created, Types::PostType, null: false do
      description "Subscribe to new posts"
      argument :author_id, ID, required: false
    end

    def post_created(author_id: nil)
      return object unless author_id
      object if object.user_id.to_s == author_id
    end

    field :comment_added, Types::CommentType, null: false do
      argument :post_id, ID, required: true
    end

    def comment_added(post_id:)
      object if object.post_id.to_s == post_id
    end
  end
end
```

### Triggering Subscriptions

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  after_create_commit :notify_subscribers

  private

  def notify_subscribers
    MyAppSchema.subscriptions.trigger('postCreated', {}, self)
  end
end

# Or manually in mutations
MyAppSchema.subscriptions.trigger(
  'commentAdded',
  { post_id: comment.post_id },
  comment
)
```

## Authentication & Authorization

### Controller Setup

```ruby
# app/controllers/graphql_controller.rb
class GraphqlController < ApplicationController
  skip_before_action :verify_authenticity_token

  def execute
    result = MyAppSchema.execute(
      params[:query],
      variables: ensure_hash(params[:variables]),
      context: {
        current_user: current_user,
        current_ability: current_ability,
        request: request
      },
      operation_name: params[:operationName]
    )

    render json: result
  rescue StandardError => e
    raise e unless Rails.env.development?
    handle_error_in_development(e)
  end

  private

  def current_user
    return nil unless request.headers['Authorization'].present?

    token = request.headers['Authorization'].split(' ').last
    decoded = JWT.decode(token, Rails.application.credentials.secret_key_base)[0]
    User.find(decoded['user_id'])
  rescue JWT::DecodeError, ActiveRecord::RecordNotFound
    nil
  end

  def ensure_hash(ambiguous_param)
    case ambiguous_param
    when String
      ambiguous_param.present? ? JSON.parse(ambiguous_param) : {}
    when Hash, ActionController::Parameters
      ambiguous_param
    when nil
      {}
    else
      raise ArgumentError, "Unexpected parameter: #{ambiguous_param}"
    end
  end
end
```

### Field-Level Authorization

```ruby
module Types
  class UserType < Types::BaseObject
    field :email, String, null: false do
      description "User email (only visible to self or admins)"
    end

    def email
      if context[:current_user] == object || context[:current_user]&.admin?
        object.email
      else
        raise GraphQL::ExecutionError, "Not authorized to view email"
      end
    end

    field :private_notes, String, null: true

    def private_notes
      return nil unless context[:current_user] == object
      object.private_notes
    end
  end
end
```

## Query Complexity & Rate Limiting

```ruby
# app/graphql/my_app_schema.rb
class MyAppSchema < GraphQL::Schema
  mutation(Types::MutationType)
  query(Types::QueryType)
  subscription(Types::SubscriptionType)

  # Limit query complexity
  max_complexity 300
  max_depth 15

  # Validate queries before execution
  validate_max_errors 50

  # Custom complexity analysis
  def self.max_complexity_count_for(query_or_multiplex)
    if query_or_multiplex.context[:current_user]&.admin?
      500  # Higher limit for admins
    else
      300
    end
  end

  # Rate limiting per user
  def self.max_query_count_per_minute_for(query_or_multiplex)
    user = query_or_multiplex.context[:current_user]
    user&.premium? ? 1000 : 100
  end
end
```

## Testing

```ruby
# spec/graphql/mutations/create_post_spec.rb
RSpec.describe Mutations::CreatePost, type: :graphql do
  let(:user) { create(:user) }
  let(:context) { { current_user: user } }

  let(:mutation) do
    <<~GQL
      mutation($title: String!, $body: String!) {
        createPost(input: { title: $title, body: $body }) {
          post {
            id
            title
            body
          }
          errors
        }
      }
    GQL
  end

  it 'creates a post' do
    variables = { title: "Test Post", body: "Post content" }

    expect {
      result = MyAppSchema.execute(mutation, variables: variables, context: context)
      expect(result.dig('data', 'createPost', 'errors')).to be_empty
    }.to change(Post, :count).by(1)
  end

  it 'returns errors for invalid data' do
    variables = { title: "", body: "" }

    result = MyAppSchema.execute(mutation, variables: variables, context: context)
    errors = result.dig('data', 'createPost', 'errors')

    expect(errors).to be_present
    expect(errors).to include("Title can't be blank")
  end

  it 'requires authentication' do
    result = MyAppSchema.execute(mutation, variables: {}, context: {})
    expect(result['errors']).to be_present
  end
end
```

## Best Practices

### ✅ Do

- Use DataLoader to prevent N+1 queries
- Implement query complexity limits
- Add field-level authorization
- Use descriptive field names and descriptions
- Version your schema with deprecations
- Test resolvers and mutations
- Monitor query performance
- Document your schema

### ❌ Don't

- Expose internal database structure directly
- Allow unlimited query depth/complexity
- Skip authorization checks
- Return raw database errors
- Create overly nested types
- Forget to handle null cases
- Expose sensitive data without checks

---

**Remember**: GraphQL gives clients flexibility but requires careful attention to performance, security, and schema design. Always use DataLoader and implement proper authorization.

For detailed examples and advanced patterns, see `graphql-reference.md`.
