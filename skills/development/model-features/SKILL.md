---
name: model-features
description: Plutonium model features - has_cents, associations, scopes, and routing
---

# Plutonium Model Features

Advanced features available in Plutonium resource models.

## Monetary Handling (has_cents)

Store monetary values as integers (cents) while exposing decimal interfaces.

### Basic Usage

```ruby
class Product < ResourceRecord
  has_cents :price_cents                    # Creates price getter/setter
  has_cents :cost_cents, name: :wholesale   # Custom accessor name
  has_cents :tax_cents, rate: 1000          # 3 decimal places
  has_cents :quantity_cents, rate: 1        # Whole numbers only
end

product = Product.new
product.price = 19.99
product.price_cents  # => 1999
product.price        # => 19.99

# Truncates (doesn't round)
product.price = 10.999
product.price_cents  # => 1099
```

### Options

```ruby
has_cents :field_cents,
  name: :custom_name,    # Accessor name (default: field without _cents)
  rate: 100,             # Conversion rate (default: 100)
  suffix: "amount"       # Suffix for generated name (default: "amount")
```

### Validation

```ruby
class Product < ResourceRecord
  has_cents :price_cents

  # Validate the cents field
  validates :price_cents, numericality: {greater_than: 0}
end

product = Product.new(price: -10)
product.valid?  # => false
product.errors[:price_cents]  # => ["must be greater than 0"]
product.errors[:price]        # => ["is invalid"] (propagated)
```

### Introspection

```ruby
Product.has_cents_attributes
# => {price_cents: {name: :price, rate: 100}, ...}

Product.has_cents_attribute?(:price_cents)  # => true
```

## Association SGID Support

All associations get Signed Global ID (SGID) methods for secure serialization.

### Singular Associations (belongs_to, has_one)

```ruby
class Post < ResourceRecord
  belongs_to :user
  has_one :featured_image
end

post = Post.first

# Get SGID
post.user_sgid           # => "BAh7CEkiCG..."
post.featured_image_sgid # => "BAh7CEkiCG..."

# Set by SGID (finds and assigns)
post.user_sgid = "BAh7CEkiCG..."
post.featured_image_sgid = "BAh7CEkiCG..."
```

### Collection Associations (has_many, has_and_belongs_to_many)

```ruby
class User < ResourceRecord
  has_many :posts
  has_and_belongs_to_many :roles
end

user = User.first

# Get SGIDs
user.post_sgids  # => ["BAh7CEkiCG...", "BAh7CEkiCG..."]
user.role_sgids  # => ["BAh7CEkiCG...", "BAh7CEkiCG..."]

# Bulk assignment
user.post_sgids = ["BAh7CEkiCG...", ...]

# Individual manipulation
user.add_post_sgid("BAh7CEkiCG...")     # Add to collection
user.remove_post_sgid("BAh7CEkiCG...")  # Remove from collection
```

### Use Cases

- Secure form submissions without exposing internal IDs
- API responses with portable references
- Caching and serialization

## Entity Scoping (associated_with)

Query records associated with another record. Essential for multi-tenant apps.

### Basic Usage

```ruby
class Comment < ResourceRecord
  belongs_to :post
end

# Find comments for a post
Comment.associated_with(post)
# => Comment.where(post: post)
```

### Association Detection

Works with:
- `belongs_to` - Uses WHERE clause (most efficient)
- `has_one` - Uses JOIN + WHERE
- `has_many` - Uses JOIN + WHERE

```ruby
# Direct association (preferred)
Comment.associated_with(post)  # WHERE post_id = ?

# Reverse association (less efficient, logs warning)
Post.associated_with(comment)  # JOIN comments WHERE comments.id = ?
```

### Custom Scopes

For optimal performance, define custom scopes:

```ruby
class Comment < ResourceRecord
  # Custom scope naming: associated_with_{model_name}
  scope :associated_with_user, ->(user) do
    joins(:post).where(posts: {user_id: user.id})
  end
end

# Automatically uses custom scope
Comment.associated_with(user)
```

### Error Handling

```ruby
# When no association exists
UnrelatedModel.associated_with(user)
# Raises: Could not resolve the association between 'UnrelatedModel' and 'User'
#
# Define:
#  1. the associations between the models
#  2. a named scope on UnrelatedModel e.g.
#
# scope :associated_with_user, ->(user) { do_something_here }
```

## URL Routing

### Default Behavior

```ruby
user = User.find(1)
user.to_param  # => "1"
```

### Custom Path Parameters

Use a stable, unique field instead of ID:

```ruby
class User < ResourceRecord
  private

  def path_parameter(param_name)
    :username  # Must be unique
  end
end

user = User.create(username: "john_doe")
user.to_param  # => "john_doe"
# URLs: /users/john_doe
```

### Dynamic Path Parameters (SEO-friendly)

Include ID prefix for uniqueness with human-readable suffix:

```ruby
class Article < ResourceRecord
  private

  def dynamic_path_parameter(param_name)
    :title
  end
end

article = Article.create(id: 1, title: "My Great Article")
article.to_param  # => "1-my-great-article"
# URLs: /articles/1-my-great-article
```

### Path Parameter Lookup

```ruby
# Scope for finding by path parameter
User.from_path_param("john_doe")
Article.from_path_param("1-my-great-article")  # Extracts ID
```

## Association Route Discovery

```ruby
class User < ResourceRecord
  has_many :posts
  has_many :comments
  accepts_nested_attributes_for :posts
end

# Get has_many association names
User.has_many_association_routes
# => ["posts", "comments"]

# Get nested attributes config
User.all_nested_attributes_options
# => {posts: {allow_destroy: false, update_only: false, macro: :has_many, class: Post}}
```

## Performance Tips

### Field Introspection

```ruby
# Cached in production, fresh in development
User.resource_field_names  # First call queries, subsequent cached
```

### Association Queries

```ruby
# Efficient: Direct belongs_to
Comment.associated_with(post)  # Simple WHERE

# Less efficient: Reverse has_many (logs warning)
Post.associated_with(comment)  # JOIN required

# Optimal: Custom scope when direct isn't possible
scope :associated_with_user, ->(user) { where(user_id: user.id) }
```

### SGID Operations

```ruby
# Efficient: Batch assignment
user.post_sgids = sgid_array  # Single operation

# Inefficient: Individual adds
sgid_array.each { |sgid| user.add_post_sgid(sgid) }
```

## Related Skills

- `model` - Model overview and structure
- `create-resource` - Scaffold generator
