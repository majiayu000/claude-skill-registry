---
name: "Action Cable & WebSocket Patterns"
description: "Real-time WebSocket features with Action Cable in Rails. Use when: (1) Building real-time chat, (2) Live notifications/presence, (3) Broadcasting model updates, (4) WebSocket authorization. Trigger keywords: Action Cable, WebSocket, real-time, channels, broadcasting, stream, subscriptions, presence, cable"
version: 1.1.0
---

# Action Cable Patterns

Real-time WebSocket features for Rails applications.

## Real-Time Feature Decision Tree

```
What real-time feature?
│
├─ User notifications
│   └─ Personal stream: stream_from "notifications_#{current_user.id}"
│
├─ Chat room messages
│   └─ Group stream: stream_from "chat_room_#{room.id}"
│
├─ Model updates (live editing)
│   └─ Model stream: stream_for @post (with broadcast_to)
│
├─ Presence tracking (who's online)
│   └─ Presence stream + Redis: stream_from "presence_room_#{room.id}"
│
└─ Dashboard/analytics
    └─ Scoped stream: stream_from "dashboard_#{account.id}"
```

---

## Core Principles (CRITICAL)

### 1. Authorization First

```ruby
# WRONG - Security vulnerability!
def subscribed
  stream_from "private_data"  # Anyone can subscribe!
end

# RIGHT - Explicit authorization
def subscribed
  reject unless current_user
  reject unless current_user.can_access?(params[:resource_id])
  stream_from "private_#{params[:resource_id]}"
end
```

### 2. Persist First, Broadcast Second

```ruby
# WRONG - Data lost if client offline
def speak(data)
  ActionCable.server.broadcast("chat", message: data['text'])
end

# RIGHT - Persist then broadcast
def speak(data)
  message = Message.create!(user: current_user, text: data['text'])
  ActionCable.server.broadcast("chat", message: message)
end
```

### 3. Use stream_for for Models

```ruby
# WRONG - Manual naming (error-prone)
stream_from "posts:#{params[:id]}"
ActionCable.server.broadcast("posts:#{@post.id}", data)

# RIGHT - Type-safe model broadcasting
stream_for @post
PostChannel.broadcast_to(@post, data)
```

---

## NEVER Do This

**NEVER** skip authorization:
```ruby
# Every channel MUST have: reject unless current_user
# Plus resource-specific authorization
```

**NEVER** broadcast before commit:
```ruby
# WRONG
post.save
ActionCable.server.broadcast(...)  # Transaction may rollback!

# RIGHT - Use after_commit callback
after_create_commit { broadcast_creation }
```

**NEVER** broadcast full objects:
```ruby
# WRONG - Leaks data, slow
ActionCable.server.broadcast("posts", post: @post)

# RIGHT - Only needed fields
ActionCable.server.broadcast("posts", post: @post.as_json(only: [:id, :title]))
```

**NEVER** create subscriptions without cleanup (JavaScript):
```javascript
// WRONG - Memory leak
consumer.subscriptions.create("ChatChannel", { ... })

// RIGHT - Cleanup on unmount
useEffect(() => {
  const sub = consumer.subscriptions.create(...)
  return () => sub.unsubscribe()
}, [])
```

---

## Channel Template

```ruby
class NotificationsChannel < ApplicationCable::Channel
  def subscribed
    # 1. Authorization (REQUIRED)
    reject unless current_user

    # 2. Subscribe to stream
    stream_from "notifications_#{current_user.id}"
  end

  def unsubscribed
    # Cleanup (optional)
  end

  # Client action: channel.perform('mark_as_read', {id: 123})
  def mark_as_read(data)
    notification = current_user.notifications.find(data['id'])
    notification.mark_as_read!

    ActionCable.server.broadcast(
      "notifications_#{current_user.id}",
      action: 'count_updated',
      unread_count: current_user.notifications.unread.count
    )
  end
end
```

---

## Stream Patterns Quick Reference

| Pattern | Use Case | Code |
|---------|----------|------|
| Personal | Notifications | `stream_from "user_#{current_user.id}"` |
| Model | Live updates | `stream_for @post` → `PostChannel.broadcast_to(@post, data)` |
| Group | Chat rooms | `stream_from "room_#{room.id}"` |
| Presence | Who's online | `stream_from "presence_#{room.id}"` + Redis |

---

## Broadcasting Patterns

### From Model (Recommended)
```ruby
class Post < ApplicationRecord
  after_create_commit { broadcast_creation }
  after_update_commit { broadcast_update }

  private

  def broadcast_creation
    PostChannel.broadcast_to(self, action: 'created', post: as_json(only: [:id, :title]))
  end
end
```

### From Controller
```ruby
def create
  @comment = @post.comments.create!(comment_params)
  CommentsChannel.broadcast_to(@post, action: 'created', comment: @comment.as_json)
end
```

### From Background Job
```ruby
class BroadcastJob < ApplicationJob
  def perform(channel_name, data)
    ActionCable.server.broadcast(channel_name, data)
  end
end
```

---

## Connection Authentication

```ruby
# app/channels/application_cable/connection.rb
module ApplicationCable
  class Connection < ActionCable::Connection::Base
    identified_by :current_user

    def connect
      self.current_user = find_verified_user
    end

    private

    def find_verified_user
      # Cookie auth (default Rails)
      if user = User.find_by(id: cookies.encrypted[:user_id])
        user
      # Token auth (API clients)
      elsif user = find_user_from_token
        user
      else
        reject_unauthorized_connection
      end
    end

    def find_user_from_token
      token = request.params[:token]
      return nil unless token
      payload = JWT.decode(token, Rails.application.secret_key_base).first
      User.find_by(id: payload['user_id'])
    rescue JWT::DecodeError
      nil
    end
  end
end
```

---

## Testing Quick Reference

```ruby
# spec/channels/notifications_channel_spec.rb
RSpec.describe NotificationsChannel, type: :channel do
  let(:user) { create(:user) }

  before { stub_connection(current_user: user) }

  it 'subscribes to user stream' do
    subscribe
    expect(subscription).to be_confirmed
    expect(subscription).to have_stream_from("notifications_#{user.id}")
  end

  it 'rejects unauthenticated users' do
    stub_connection(current_user: nil)
    subscribe
    expect(subscription).to be_rejected
  end

  it 'broadcasts on action' do
    subscribe
    expect {
      perform :mark_as_read, id: notification.id
    }.to have_broadcasted_to("notifications_#{user.id}")
  end
end
```

---

## Production Config

```yaml
# config/cable.yml
production:
  adapter: redis
  url: <%= ENV['REDIS_URL'] %>
  channel_prefix: myapp_production
```

```ruby
# config/environments/production.rb
config.action_cable.url = ENV['ACTION_CABLE_URL']
config.action_cable.allowed_request_origins = ['https://example.com']
```

---

## References

Detailed examples in `references/`:
- `javascript-consumers.md` - Client-side subscription patterns
- `presence-tracking.md` - Complete presence implementation with Redis
- `deployment.md` - Nginx, scaling, production configuration
