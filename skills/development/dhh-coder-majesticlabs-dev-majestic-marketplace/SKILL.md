---
name: dhh-coder
description: Write Ruby and Rails code in DHH's distinctive 37signals style. Use this skill when writing Ruby code, Rails applications, creating models, controllers, or any Ruby file. Triggers on Ruby/Rails code generation, refactoring requests, or when the user mentions DHH, 37signals, Basecamp, HEY, Fizzy, or Campfire style.
---

# DHH Ruby/Rails Style Guide

Write Ruby and Rails code following DHH's philosophy: **clarity over cleverness**, **convention over configuration**, **developer happiness** above all.

## Quick Reference

### Controller Actions
- **Only 7 REST actions**: `index`, `show`, `new`, `create`, `edit`, `update`, `destroy`
- **New behavior?** Create a new controller, not a custom action
- **Action length**: 1-5 lines maximum
- **Empty actions are fine**: Let Rails convention handle rendering

```ruby
class MessagesController < ApplicationController
  before_action :set_message, only: %i[ show edit update destroy ]

  def index
    @messages = @room.messages.with_creator.last_page
    fresh_when @messages
  end

  def show
  end

  def create
    @message = @room.messages.create_with_attachment!(message_params)
    @message.broadcast_create
  end

  private
    def set_message
      @message = @room.messages.find(params[:id])
    end

    def message_params
      params.require(:message).permit(:body, :attachment)
    end
end
```

### Private Method Indentation
Indent private methods one level under `private` keyword:

```ruby
  private
    def set_message
      @message = Message.find(params[:id])
    end

    def message_params
      params.require(:message).permit(:body)
    end
```

### Model Design (Fat Models)
Models own business logic, authorization, and broadcasting:

```ruby
class Message < ApplicationRecord
  belongs_to :room
  belongs_to :creator, class_name: "User"
  has_many :mentions

  scope :with_creator, -> { includes(:creator) }
  scope :page_before, ->(cursor) { where("id < ?", cursor.id).order(id: :desc).limit(50) }

  def broadcast_create
    broadcast_append_to room, :messages, target: "messages"
  end

  def mentionees
    mentions.includes(:user).map(&:user)
  end
end

class User < ApplicationRecord
  def can_administer?(message)
    message.creator == self || admin?
  end
end
```

### Current Attributes
Use `Current` for request context, never pass `current_user` everywhere:

```ruby
class Current < ActiveSupport::CurrentAttributes
  attribute :user, :session
end

# Usage anywhere in app
Current.user.can_administer?(@message)
```

### Ruby Syntax Preferences

```ruby
# Symbol arrays with spaces inside brackets
before_action :set_message, only: %i[ show edit update destroy ]

# Modern hash syntax exclusively
params.require(:message).permit(:body, :attachment)

# Single-line blocks with braces
users.each { |user| user.notify }

# Ternaries for simple conditionals
@room.direct? ? @room.users : @message.mentionees

# Bang methods for fail-fast
@message = Message.create!(params)
@message.update!(message_params)

# Predicate methods with question marks
@room.direct?
user.can_administer?(@message)
@messages.any?

# Expression-less case for cleaner conditionals
case
when params[:before].present?
  @room.messages.page_before(params[:before])
when params[:after].present?
  @room.messages.page_after(params[:after])
else
  @room.messages.last_page
end
```

### Query Optimization

```ruby
# WRONG: Load all records then extract attribute
users.map(&:name)

# CORRECT: Pluck directly from database
users.pluck(:name)

# WRONG: Count via Ruby
messages.to_a.count

# CORRECT: Count via SQL
messages.count
```

### StringInquirer for Predicates

Use `.inquiry` on string enums for readable conditionals:

```ruby
class Event < ApplicationRecord
  def action
    super.inquiry
  end
end

# Clean predicate methods
event.action.completed?
event.action.pending?
event.action.failed?
```

### Controller Response Patterns

```ruby
# Return 204 No Content for successful updates without body
def update
  @message.update!(message_params)
  head :no_content
end

# Return 201 Created for successful creates
def create
  @message = Message.create!(message_params)
  head :created
end
```

### My:: Namespace for Current User Resources

Use `My::` namespace for resources scoped to `Current.user`:

```ruby
# routes.rb
namespace :my do
  resource :profile, only: %i[ show edit update ]
  resources :notifications, only: %i[ index destroy ]
end

# app/controllers/my/profiles_controller.rb
class My::ProfilesController < ApplicationController
  def show
    @profile = Current.user
  end
end
```

No `index` or `show` with ID needed—resource is implicit from `Current.user`.

### Compute at Write Time

Perform data manipulation during saves, not during presentation:

```ruby
# WRONG: Compute on read
def display_name
  "#{first_name} #{last_name}".titleize
end

# CORRECT: Compute on write
before_save :set_display_name

private
  def set_display_name
    self.display_name = "#{first_name} #{last_name}".titleize
  end
```

Benefits: enables pagination, caching, and reduces view complexity.

### Delegate for Lazy Loading

Use `delegate` to enable lazy loading through associations:

```ruby
class Message < ApplicationRecord
  belongs_to :session
  delegate :user, to: :session
end

# Lazy loads user through session
message.user
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Setter methods | `set_` prefix | `set_message`, `set_room` |
| Parameter methods | `{model}_params` | `message_params` |
| Association names | Semantic, not generic | `creator` not `user` |
| Scopes | Chainable, descriptive | `with_creator`, `page_before` |
| Predicates | End with `?` | `direct?`, `can_administer?` |
| Current user resources | `My::` namespace | `My::ProfilesController` |

### Hotwire/Turbo Patterns
Broadcasting is model responsibility:

```ruby
# In model
def broadcast_create
  broadcast_append_to room, :messages, target: "messages"
end
```

**For detailed Hotwire patterns, use `hotwire-coder` skill.**

### Error Handling
Rescue specific exceptions, fail fast with bang methods:

```ruby
def create
  @message = @room.messages.create_with_attachment!(message_params)
  @message.broadcast_create
rescue ActiveRecord::RecordNotFound
  render action: :room_not_found
end
```

### State as Records (Not Booleans)

Track state via database records rather than boolean columns:

```ruby
# WRONG: Boolean columns for state
class Card < ApplicationRecord
  # closed: boolean, gilded: boolean columns
end
card.update!(closed: true)
card.closed?  # Loses who/when/why

# CORRECT: State as separate records
class Card < ApplicationRecord
  has_one :closure
  has_one :gilding

  def close(by:)
    create_closure!(closed_by: by)
  end

  def closed?
    closure.present?
  end
end
card.close(by: Current.user)
card.closure.closed_by  # Full audit trail
```

### REST URL Transformations

Map custom actions to nested resource controllers:

| Custom Action | REST Resource |
|---------------|---------------|
| `POST /cards/:id/close` | `POST /cards/:id/closure` |
| `DELETE /cards/:id/close` | `DELETE /cards/:id/closure` |
| `POST /cards/:id/gild` | `POST /cards/:id/gilding` |
| `POST /posts/:id/publish` | `POST /posts/:id/publication` |
| `DELETE /posts/:id/publish` | `DELETE /posts/:id/publication` |

```ruby
# routes.rb
resources :cards do
  resource :closure, only: %i[ create destroy ]
  resource :gilding, only: %i[ create destroy ]
end

# app/controllers/cards/closures_controller.rb
class Cards::ClosuresController < ApplicationController
  def create
    @card = Card.find(params[:card_id])
    @card.close(by: Current.user)
  end

  def destroy
    @card = Card.find(params[:card_id])
    @card.closure.destroy!
  end
end
```

### Architecture Preferences

| Traditional | DHH Way |
|-------------|---------|
| PostgreSQL | SQLite (for single-tenant) |
| Redis + Sidekiq | Solid Queue |
| Redis cache | Solid Cache |
| Kubernetes | Single Docker container |
| Service objects | Fat models |
| Policy objects (Pundit) | Authorization on User model |
| FactoryBot | Fixtures |
| Boolean state columns | State as records |

## Detailed References

For comprehensive patterns and examples, see:

### Core Patterns
- `references/patterns.md` - Complete code patterns with explanations
- `references/palkan-patterns.md` - Namespaced model classes, counter caches, model organization order, PostgreSQL enums
- `references/concerns-organization.md` - Model-specific vs common concerns, facade pattern
- `references/delegated-types.md` - Polymorphism without STI problems
- `references/recording-pattern.md` - Unifying abstraction for diverse content types
- `references/filter-objects.md` - PORO filter objects, URL-based state, testable query building
- `references/database-patterns.md` - UUIDv7, hard deletes, state as records, counter caches, indexing

### Rails Components
- `references/activerecord-tips.md` - ActiveRecord query patterns, validations, associations
- `references/controllers-tips.md` - Controller patterns, routing, rate limiting, form objects
- `references/activestorage-tips.md` - File uploads, attachments, blob handling

### Hotwire
- `references/hotwire-tips.md` - Turbo Frames, Turbo Streams, ViewComponents
- `references/turbo-morphing.md` - Turbo 8 page refresh with morphing patterns
- `references/stimulus-catalog.md` - Copy-paste-ready Stimulus controllers (clipboard, dialog, hotkey, etc.)
- **Also see:** `hotwire-coder`, `stimulus-coder`, `viewcomponent-coder` skills for detailed patterns

### Frontend
- `references/css-architecture.md` - Native CSS patterns (layers, OKLCH, nesting, dark mode)

### Authentication & Multi-Tenancy
- `references/passwordless-auth.md` - Magic link authentication, sessions, identity model
- `references/multi-tenancy.md` - Path-based tenancy, cookie scoping, tenant-aware jobs

### Infrastructure & Integrations
- `references/webhooks.md` - Secure webhook delivery, SSRF protection, retry strategies
- `references/caching-strategies.md` - Russian Doll caching, Solid Cache, cache analysis
- `references/config-tips.md` - Configuration, logging, deployment patterns
- `references/structured-events.md` - Rails 8.1 `Rails.event` API for structured observability
- `references/resources.md` - Links to source material and further reading

## Philosophy Summary

1. **REST purity**: 7 actions only; new controllers for variations
2. **Fat models**: Authorization, broadcasting, business logic in models
3. **Thin controllers**: 1-5 line actions; extract complexity
4. **Convention over configuration**: Empty methods, implicit rendering
5. **Minimal abstractions**: No service objects for simple cases
6. **Current attributes**: Thread-local request context everywhere
7. **Hotwire-first**: Model-level broadcasting, Turbo Streams, Stimulus
8. **Readable code**: Semantic naming, small methods, no comments needed

## Success Indicators

Code aligns with DHH style when:

- [ ] Controllers map CRUD verbs to resources (no custom actions)
- [ ] Models use concerns for horizontal behavior sharing
- [ ] State uses records instead of boolean columns
- [ ] Abstractions remain minimal (no unnecessary service objects)
- [ ] Database backs solutions (Solid Queue/Cache, not Redis)
- [ ] Turbo/Stimulus handle all interactivity
- [ ] Authorization lives on User model (`can_*?` methods)
- [ ] Current attributes provide request context
- [ ] Scopes follow naming conventions (`chronologically`, `with_*`, etc.)
- [ ] Uses `pluck` over `map` for attribute extraction
- [ ] Current user resources use `My::` namespace
- [ ] Data computed at write time, not presentation
