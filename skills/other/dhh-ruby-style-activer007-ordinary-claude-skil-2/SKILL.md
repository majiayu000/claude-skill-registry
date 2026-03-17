---
name: dhh-ruby-style
description: Write Ruby and Rails code in DHH's distinctive 37signals style. Use this skill when writing Ruby code, Rails applications, creating models, controllers, or any Ruby file. Triggers on Ruby/Rails code generation, refactoring requests, code review, or when the user mentions DHH, 37signals, Basecamp, HEY, or Campfire style. Embodies REST purity, fat models, thin controllers, Current attributes, Hotwire patterns, and the "clarity over cleverness" philosophy.
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

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Setter methods | `set_` prefix | `set_message`, `set_room` |
| Parameter methods | `{model}_params` | `message_params` |
| Association names | Semantic, not generic | `creator` not `user` |
| Scopes | Chainable, descriptive | `with_creator`, `page_before` |
| Predicates | End with `?` | `direct?`, `can_administer?` |

### Hotwire/Turbo Patterns
Broadcasting is model responsibility:

```ruby
# In model
def broadcast_create
  broadcast_append_to room, :messages, target: "messages"
end

# In controller
@message.broadcast_replace_to @room, :messages,
  target: [ @message, :presentation ],
  partial: "messages/presentation",
  attributes: { maintain_scroll: true }
```

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

## Detailed References

For comprehensive patterns and examples, see:
- `references/patterns.md` - Complete code patterns with explanations
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
9. **Pragmatic testing**: System tests over unit tests, real integrations
