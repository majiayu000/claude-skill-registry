---
name: rails-conventions
description: Rails code patterns and conventions following rubocop-rails-omakase style.
---

# Rails Conventions

Opinionated Rails patterns for clean, maintainable code.

## Core Philosophy

1. **Duplication > Complexity**: Simple duplicated code beats complex DRY abstractions
   - "I'd rather have four simple controllers than three complex ones"

2. **Testability = Quality**: If it's hard to test, structure needs refactoring

3. **Adding controllers is never bad. Making controllers complex IS bad.**

## Turbo Streams

Simple turbo streams MUST be inline in controllers:

```ruby
# FAIL: Separate .turbo_stream.erb files for simple operations
render "posts/update"

# PASS: Inline array
render turbo_stream: [
  turbo_stream.replace("post_#{@post.id}", partial: "posts/post", locals: { post: @post }),
  turbo_stream.remove("flash")
]
```

## Controller & Concerns

Business logic belongs in models or concerns, not controllers.

```ruby
# Concern structure
module Dispatchable
  extend ActiveSupport::Concern

  included do
    scope :available, -> { where(status: "pending") }
  end

  class_methods do
    def claim!(batch_size)
      # class-level behavior
    end
  end
end
```

## Service Extraction

Extract when you see MULTIPLE of:
- Complex business rules (not just "it's long")
- Multiple models orchestrated
- External API interactions
- Reusable cross-controller logic

Service structure:
- Single public method
- Namespace by responsibility (`Extraction::RegexExtractor`)
- Constructor takes dependencies
- Return data structures, not domain objects

## Modern Ruby Style

```ruby
# Hash shorthand
{ id:, slug:, doc_type: kind }

# Safe navigation
created_at&.iso8601
@setting ||= SlugSetting.active.find_by!(slug:)

# Keyword arguments
def extract(document_type:, subject:, filename:)
def process!(strategy: nil)
```

## Enum Patterns

```ruby
# Frozen arrays with validation
STATUSES = %w[processed needs_review].freeze
enum :status, STATUSES.index_by(&:itself), validate: true
```

## Scope Patterns

```ruby
# Guard with .present?, chainable design
scope :by_slug, ->(slug) { where(slug:) if slug.present? }
scope :from_date, ->(date) { where(created_at: Date.parse(date).beginning_of_day..) if date.present? }

def self.filtered(params)
  all.by_slug(params[:slug]).by_kind(params[:kind])
rescue ArgumentError
  all
end
```

## Error Handling

```ruby
# Domain-specific errors
class InactiveSlug < StandardError; end

# Log with context, re-raise for upstream
def handle_exception!(error:)
  log_error("Exception #{error.class}: #{error.message}", error:)
  mark_failed!(error.message)
  raise
end
```

## Testing (Minitest + Fixtures)

```ruby
test "describes expected behavior" do
  email = emails(:two)
  email.process
  email.reload
  assert_equal "finished", email.processing_status
end
```

Principles:
- **Behavior-driven**: Test what, not how
- **Fixture-based**: Use `emails(:two)` for setup
- **Mock externals**: Stub S3, APIs, PDFs
- **State verification**: `.reload` after operations
- **Helper methods**: `build_valid_email`, `with_stubbed_download`

## Naming (5-Second Rule)

If you can't understand in 5 seconds:

```ruby
# FAIL
show_in_frame
process_stuff

# PASS
fact_check_modal
_fact_frame
```

## Performance

- Consider scale impact
- No premature caching
- KISS - Keep It Simple
- Indexes slow writes - add only when needed
