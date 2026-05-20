---
name: rails-pagination-kaminari
description: "Pagination for Ruby on Rails applications using Kaminari. Use when: (1) Implementing pagination for database records, (2) Building paginated API endpoints, (3) Customizing pagination UI with themes, (4) Handling large datasets efficiently, (5) Creating infinite scroll, (6) Paginating arrays or custom collections, (7) Adding SEO-friendly pagination URLs, (8) Internationalizing pagination labels"
---

# Rails Pagination with Kaminari

Kaminari is a scope and engine-based pagination library that provides a clean, powerful, customizable paginator for Rails applications. It's non-intrusive, chainable with ActiveRecord, and highly customizable.

## Quick Setup

```bash
# Add to Gemfile
bundle add kaminari

# Generate configuration file (optional)
rails g kaminari:config

# Generate view templates for customization (optional)
rails g kaminari:views default
```

## Basic Usage

### Controller Pagination

```ruby
# app/controllers/posts_controller.rb
class PostsController < ApplicationController
  def index
    @posts = Post.order(:created_at).page(params[:page])
    # Returns 25 items per page by default
  end
end
```

### View Helper

```erb
<!-- app/views/posts/index.html.erb -->
<%= paginate @posts %>
```

That's it! Kaminari automatically adds pagination links.

## Core Methods

### Page Scope

```ruby
# Basic pagination
User.page(1)                    # First page, 25 items
User.page(params[:page])        # Dynamic page from params

# Custom per-page
User.page(1).per(50)            # 50 items per page

# Chaining with scopes
User.active.order(:name).page(params[:page]).per(20)

# With associations
User.includes(:posts).page(params[:page])
```

### Pagination Metadata

```ruby
users = User.page(2).per(20)

users.current_page      #=> 2
users.total_pages       #=> 10
users.total_count       #=> 200
users.limit_value       #=> 20
users.first_page?       #=> false
users.last_page?        #=> false
users.next_page         #=> 3
users.prev_page         #=> 1
users.out_of_range?     #=> false
```

## Configuration

### Global Configuration

```ruby
# config/initializers/kaminari_config.rb
Kaminari.configure do |config|
  config.default_per_page = 25        # Default items per page
  config.max_per_page = 100           # Maximum allowed per page
  config.max_pages = nil              # Maximum pages (nil = unlimited)
  config.window = 4                   # Inner window size
  config.outer_window = 0             # Outer window size
  config.left = 0                     # Left outer window
  config.right = 0                    # Right outer window
  config.page_method_name = :page     # Method name (change if conflicts)
  config.param_name = :page           # URL parameter name
end
```

### Per-Model Configuration

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  paginates_per 50              # This model shows 50 per page
  max_paginates_per 100         # User can't request more than 100
  max_pages 100                 # Limit to 100 pages total
end
```

## View Helpers

### Basic Pagination

```erb
<!-- Simple pagination links -->
<%= paginate @posts %>

<!-- With options -->
<%= paginate @posts, window: 2 %>
<%= paginate @posts, outer_window: 1 %>
<%= paginate @posts, left: 1, right: 1 %>

<!-- Custom parameter name -->
<%= paginate @posts, param_name: :pagina %>

<!-- For AJAX/Turbo -->
<%= paginate @posts, remote: true %>
```

### Navigation Links

```erb
<!-- Previous/Next links -->
<%= link_to_prev_page @posts, 'Previous', class: 'btn' %>
<%= link_to_next_page @posts, 'Next', class: 'btn' %>

<!-- With custom content -->
<%= link_to_prev_page @posts do %>
  <span aria-hidden="true">&larr;</span> Older
<% end %>

<%= link_to_next_page @posts do %>
  Newer <span aria-hidden="true">&rarr;</span>
<% end %>
```

### Page Info

```erb
<!-- Shows: "Displaying posts 1 - 25 of 100 in total" -->
<%= page_entries_info @posts %>

<!-- Custom format -->
<%= page_entries_info @posts, entry_name: 'item' %>
```

### SEO Helpers

```erb
<!-- Add rel="next" and rel="prev" link tags to <head> -->
<%= rel_next_prev_link_tags @posts %>
```

### URL Helpers

```ruby
# Get URLs for navigation
path_to_next_page(@posts)  #=> "/posts?page=3"
path_to_prev_page(@posts)  #=> "/posts?page=1"
```

## Customization

### Generating Custom Views

```bash
# Generate default theme
rails g kaminari:views default

# Generate with namespace
rails g kaminari:views default --views-prefix admin

# Generate specific theme
rails g kaminari:views bootstrap4
```

This creates templates in `app/views/kaminari/`:
- `_first_page.html.erb`
- `_prev_page.html.erb`
- `_page.html.erb`
- `_next_page.html.erb`
- `_last_page.html.erb`
- `_gap.html.erb`
- `_paginator.html.erb`

### Using Themes

```erb
<!-- Default theme -->
<%= paginate @posts %>

<!-- Custom theme -->
<%= paginate @posts, theme: 'my_theme' %>

<!-- Bootstrap theme -->
<%= paginate @posts, theme: 'twitter-bootstrap-4' %>
```

### Custom Pagination Template

```erb
<!-- app/views/kaminari/_paginator.html.erb -->
<nav class="pagination" role="navigation" aria-label="Pagination">
  <ul class="pagination-list">
    <%= first_page_tag %>
    <%= prev_page_tag %>

    <% each_page do |page| %>
      <% if page.left_outer? || page.right_outer? || page.inside_window? %>
        <%= page_tag page %>
      <% elsif !page.was_truncated? %>
        <%= gap_tag %>
      <% end %>
    <% end %>

    <%= next_page_tag %>
    <%= last_page_tag %>
  </ul>
</nav>
```

## API Pagination

### JSON Response

```ruby
# app/controllers/api/v1/posts_controller.rb
module Api
  module V1
    class PostsController < ApplicationController
      def index
        @posts = Post.page(params[:page]).per(params[:per_page] || 20)

        render json: {
          posts: @posts.map { |p| PostSerializer.new(p) },
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
          total_count: collection.total_count
        }
      end
    end
  end
end
```

### API Response Helper

```ruby
# app/controllers/concerns/paginatable.rb
module Paginatable
  extend ActiveSupport::Concern

  def paginate(collection)
    collection
      .page(params[:page] || 1)
      .per(params[:per_page] || default_per_page)
  end

  def pagination_links(collection)
    {
      self: request.original_url,
      first: url_for(page: 1),
      prev: collection.prev_page ? url_for(page: collection.prev_page) : nil,
      next: collection.next_page ? url_for(page: collection.next_page) : nil,
      last: url_for(page: collection.total_pages)
    }
  end

  def pagination_meta(collection)
    {
      current_page: collection.current_page,
      total_pages: collection.total_pages,
      total_count: collection.total_count,
      per_page: collection.limit_value
    }
  end

  private

  def default_per_page
    20
  end
end
```

## Performance Optimization

### Without Count Query

For very large datasets, skip expensive COUNT queries:

```ruby
# Controller
def index
  @posts = Post.order(:created_at).page(params[:page]).without_count
end

# View - use simple navigation only
<%= link_to_prev_page @posts, 'Previous' %>
<%= link_to_next_page @posts, 'Next' %>
```

**Note**: `total_pages`, `total_count`, and numbered page links won't work with `without_count`.

### Eager Loading

```ruby
# Prevent N+1 queries
@posts = Post.includes(:user, :comments)
             .order(:created_at)
             .page(params[:page])
```

### Caching

```ruby
# Fragment caching
<% cache ["posts-page", @posts.current_page] do %>
  <%= render @posts %>
  <%= paginate @posts %>
<% end %>
```

## Advanced Features

### Paginating Arrays

```ruby
# Controller
@items = expensive_operation_returning_array
@paginated_items = Kaminari.paginate_array(@items, total_count: @items.count)
                           .page(params[:page])
                           .per(10)

# Or with known total
@paginated_items = Kaminari.paginate_array(
  @items,
  total_count: 145,
  limit: 10,
  offset: (params[:page].to_i - 1) * 10
).page(params[:page]).per(10)
```

### SEO-Friendly URLs

```ruby
# config/routes.rb
resources :posts do
  get 'page/:page', action: :index, on: :collection
end

# Creates URLs like: /posts/page/2 instead of /posts?page=2

# Or using concerns
concern :paginatable do
  get '(page/:page)', action: :index, on: :collection, as: ''
end

resources :posts, concerns: :paginatable
resources :articles, concerns: :paginatable
```

### Infinite Scroll

```ruby
# app/controllers/posts_controller.rb
def index
  @posts = Post.order(:created_at).page(params[:page])

  respond_to do |format|
    format.html
    format.js   # For infinite scroll
  end
end
```

```javascript
// app/views/posts/index.js.erb
$('#posts').append('<%= j render @posts %>');

<% if @posts.next_page %>
  $('.pagination').replaceWith('<%= j paginate @posts %>');
<% else %>
  $('.pagination').remove();
<% end %>
```

### Custom Scopes with Pagination

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  scope :published, -> { where(published: true) }
  scope :by_author, ->(author_id) { where(author_id: author_id) }
  scope :recent_first, -> { order(created_at: :desc) }

  # Chainable with pagination
  # Post.published.recent_first.page(1)
end
```

## Internationalization

```yaml
# config/locales/en.yml
en:
  views:
    pagination:
      first: "&laquo; First"
      last: "Last &raquo;"
      previous: "&lsaquo; Prev"
      next: "Next &rsaquo;"
      truncate: "&hellip;"
  helpers:
    page_entries_info:
      one_page:
        display_entries:
          zero: "No %{entry_name} found"
          one: "Displaying <b>1</b> %{entry_name}"
          other: "Displaying <b>all %{count}</b> %{entry_name}"
      more_pages:
        display_entries: "Displaying %{entry_name} <b>%{first}&nbsp;-&nbsp;%{last}</b> of <b>%{total}</b> in total"
```

## Common Patterns

### Search with Pagination

```ruby
# app/controllers/posts_controller.rb
def index
  @posts = Post.all
  @posts = @posts.where('title LIKE ?', "%#{params[:q]}%") if params[:q].present?
  @posts = @posts.order(:created_at).page(params[:page])
end
```

```erb
<!-- app/views/posts/index.html.erb -->
<%= form_with url: posts_path, method: :get do |f| %>
  <%= f.text_field :q, value: params[:q], placeholder: 'Search...' %>
  <%= f.submit 'Search' %>
<% end %>

<%= render @posts %>
<%= paginate @posts, params: { q: params[:q] } %>
```

### Filtered Pagination

```ruby
# app/controllers/posts_controller.rb
def index
  @posts = Post.all
  @posts = @posts.where(category_id: params[:category_id]) if params[:category_id]
  @posts = @posts.where(status: params[:status]) if params[:status]
  @posts = @posts.order(:created_at).page(params[:page])
end
```

```erb
<%= paginate @posts, params: { category_id: params[:category_id], status: params[:status] } %>
```

### Admin Pagination

```ruby
# app/controllers/admin/users_controller.rb
module Admin
  class UsersController < AdminController
    def index
      @users = User.order(:email).page(params[:page]).per(50)
    end
  end
end
```

## Testing

### RSpec

```ruby
# spec/models/post_spec.rb
RSpec.describe Post, type: :model do
  describe '.page' do
    let!(:posts) { create_list(:post, 30) }

    it 'returns first page with default per_page' do
      page = Post.page(1)
      expect(page.count).to eq(25)
      expect(page.current_page).to eq(1)
    end

    it 'returns correct page' do
      page = Post.page(2).per(10)
      expect(page.count).to eq(10)
      expect(page.current_page).to eq(2)
      expect(page.total_pages).to eq(3)
    end
  end
end

# spec/requests/posts_spec.rb
RSpec.describe 'Posts', type: :request do
  describe 'GET /posts' do
    let!(:posts) { create_list(:post, 30) }

    it 'paginates posts' do
      get posts_path, params: { page: 2 }
      expect(response).to have_http_status(:ok)
      expect(assigns(:posts).current_page).to eq(2)
    end

    it 'handles out of range pages' do
      get posts_path, params: { page: 999 }
      expect(response).to have_http_status(:ok)
      expect(assigns(:posts)).to be_empty
      expect(assigns(:posts).out_of_range?).to be true
    end
  end
end
```

### Controller Tests

```ruby
# spec/controllers/posts_controller_spec.rb
RSpec.describe PostsController, type: :controller do
  describe 'GET #index' do
    let!(:posts) { create_list(:post, 30) }

    it 'assigns paginated posts' do
      get :index, params: { page: 1 }
      expect(assigns(:posts).count).to eq(25)
      expect(assigns(:posts).total_count).to eq(30)
    end

    it 'respects per_page parameter' do
      get :index, params: { page: 1, per_page: 10 }
      expect(assigns(:posts).count).to eq(10)
    end
  end
end
```

## Troubleshooting

### Page Parameter Not Working

```ruby
# If using custom routes, ensure page param is permitted
params.permit(:page, :per_page)
```

### Total Count Performance

```ruby
# For large tables, use counter cache or without_count
class Post < ApplicationRecord
  # Option 1: Counter cache
  belongs_to :category, counter_cache: true

  # Option 2: Skip count query
  # Use .without_count in controller
end
```

### Styling Issues

```bash
# Ensure you've generated views
rails g kaminari:views default

# Or use a theme
rails g kaminari:views bootstrap4
```

## Best Practices

1. **Always order before paginating**: Ensures consistent results across pages
2. **Use `per` wisely**: Set reasonable limits with `max_paginates_per`
3. **Eager load associations**: Prevent N+1 queries with `includes`
4. **Cache pagination**: Use fragment caching for expensive queries
5. **Handle out of range**: Check `out_of_range?` and redirect if needed
6. **API pagination**: Always include metadata in JSON responses
7. **SEO**: Use `rel_next_prev_link_tags` for better search indexing
8. **Test edge cases**: Empty results, last page, out of range pages
9. **Use `without_count` for large datasets**: Skip COUNT queries when possible
10. **Preserve filters**: Pass filter params to `paginate` helper

## Additional Resources

For more advanced patterns, see:
- **API Pagination**: [references/api-pagination.md](references/api-pagination.md)
- **Custom Themes**: [references/custom-themes.md](references/custom-themes.md)
- **Performance Optimization**: [references/performance.md](references/performance.md)

## Resources

- [Kaminari GitHub](https://github.com/kaminari/kaminari)
- [Kaminari Wiki](https://github.com/kaminari/kaminari/wiki)
