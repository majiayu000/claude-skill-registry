---
name: action-cable-realtime
description: This skill should be used when the user asks about Action Cable, WebSockets,
  real-time features, channels, broadcasting, subscriptions, chat applications, live
  notifications, presence indicators, coll
---

---
name: action-cable-realtime
description: This skill should be used when the user asks about Action Cable, WebSockets, real-time features, channels, broadcasting, subscriptions, chat applications, live notifications, presence indicators, collaborative editing, server push, pub/sub patterns, Solid Cable, or streaming updates. Also use when discussing real-time architecture, WebSocket deployment, or alternatives like polling and Server-Sent Events. Examples:

<example>
Context: User wants to build a chat feature
user: "How do I build a real-time chat with Rails?"
assistant: "I'll show you how to use Action Cable channels for chat functionality."
<commentary>
This is a classic Action Cable use case involving channels and broadcasting.
</commentary>
</example>

<example>
Context: User wants live notifications
user: "How can I push notifications to users without them refreshing?"
assistant: "Action Cable broadcasts are perfect for this. Let me explain channels and subscriptions."
<commentary>
This relates to Action Cable broadcasting and real-time updates.
</commentary>
</example>

<example>
Context: User asks about deployment
user: "Do I need Redis for Action Cable in production?"
assistant: "Rails 8 includes Solid Cable which uses your database instead of Redis."
<commentary>
This involves Action Cable configuration and the Solid Cable adapter.
</commentary>
</example>
---

# Action Cable & Real-Time: WebSockets in Rails

## Overview

Action Cable integrates WebSockets with Rails, enabling real-time features like chat, notifications, and live updates. It provides both server-side Ruby and client-side JavaScript frameworks that work together seamlessly.

**Action Cable enables:**
- Real-time chat and messaging
- Live notifications
- Presence indicators (who's online)
- Collaborative editing
- Live dashboard updates
- Real-time feeds

Rails 8 introduces **Solid Cable**, which replaces Redis with database-backed pub/sub, simplifying deployment.

## Core Concepts

### WebSockets vs HTTP

**HTTP (Request-Response):**
```
Client → Request → Server
Client ← Response ← Server
[Connection closes]
```

**WebSocket (Persistent Connection):**
```
Client ↔ Persistent Connection ↔ Server
[Messages flow both directions]
[Connection stays open]
```

Benefits:
- Bi-directional communication
- Low latency (no connection overhead)
- Server can push to clients
- Efficient for real-time features

### Action Cable Architecture

```
Browser (Consumer) → WebSocket → Connection → Channels → Broadcasters
```

**Connection**: WebSocket connection (one per browser tab)
**Channel**: Logical grouping (like a controller)
**Subscription**: Consumer subscribed to a channel
**Broadcasting**: Message sent to all channel subscribers

## Channels

Channels are like controllers for WebSockets.

### Creating a Channel

```bash
rails generate channel Chat
```

Generates:

```ruby
# app/channels/chat_channel.rb
class ChatChannel < ApplicationCable::Channel
  def subscribed
    # Called when consumer subscribes
    stream_from "chat_#{params[:room_id]}"
  end

  def unsubscribed
    # Called when consumer unsubscribes (cleanup)
  end

  def speak(data)
    # Called when consumer sends message
    Message.create!(
      content: data['message'],
      user: current_user,
      room_id: params[:room_id]
    )
  end
end
```

```javascript
// app/javascript/channels/chat_channel.js
import consumer from "./consumer"

consumer.subscriptions.create(
  { channel: "ChatChannel", room_id: 123 },
  {
    connected() {
      console.log("Connected to chat")
    },

    disconnected() {
      console.log("Disconnected from chat")
    },

    received(data) {
      // Handle broadcasted message
      const messagesContainer = document.getElementById("messages")
      messagesContainer.insertAdjacentHTML("beforeend", data.html)
    },

    speak(message) {
      this.perform("speak", { message: message })
    }
  }
)
```

### Streaming

Subscribe to broadcasts:

```ruby
class ChatChannel < ApplicationCable::Channel
  def subscribed
    # Stream from named channel
    stream_from "chat_room_#{params[:room_id]}"

    # Stream for current user only
    stream_for current_user

    # Stop streaming
    stop_all_streams
  end
end
```

### Channel Callbacks

Channels support lifecycle callbacks and exception handling:

```ruby
class ChatChannel < ApplicationCable::Channel
  before_subscribe :verify_access
  after_subscribe :log_subscription

  rescue_from UnauthorizedError, with: :handle_unauthorized

  def subscribed
    stream_from "chat_#{params[:room_id]}"
  end

  private

  def verify_access
    reject unless current_user.can_access?(params[:room_id])
  end

  def log_subscription
    Rails.logger.info "User #{current_user.id} subscribed to chat"
  end

  def handle_unauthorized(exception)
    # Handle error, optionally broadcast error message
    transmit(error: "Unauthorized access")
  end
end
```

Available callbacks: `before_subscribe`, `after_subscribe`, `before_unsubscribe`, `after_unsubscribe`.

## Broadcasting

Send messages to channel subscribers:

### From Models

```ruby
class Message < ApplicationRecord
  belongs_to :room
  belongs_to :user

  after_create_commit :broadcast_message

  private

  def broadcast_message
    ActionCable.server.broadcast(
      "chat_room_#{room_id}",
      {
        html: ApplicationController.render(
          partial: 'messages/message',
          locals: { message: self }
        ),
        user: user.name
      }
    )
  end
end
```

### From Controllers

```ruby
class MessagesController < ApplicationController
  def create
    @message = Message.new(message_params)

    if @message.save
      # Broadcast happens in model callback
      head :ok
    else
      render json: { errors: @message.errors }, status: :unprocessable_entity
    end
  end
end
```

### From Jobs

```ruby
class NotificationBroadcastJob < ApplicationJob
  queue_as :default

  def perform(notification)
    ActionCable.server.broadcast(
      "notifications_#{notification.user_id}",
      { html: render_notification(notification) }
    )
  end

  private

  def render_notification(notification)
    ApplicationController.render(
      partial: 'notifications/notification',
      locals: { notification: notification }
    )
  end
end
```

## Authentication

Authenticate WebSocket connections:

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
      if verified_user = User.find_by(id: cookies.encrypted[:user_id])
        verified_user
      else
        reject_unauthorized_connection
      end
    end
  end
end
```

Now `current_user` is available in all channels.

## Rails 8: Solid Cable

Solid Cable replaces Redis with database-backed pub/sub.

### Configuration

```yaml
# config/cable.yml
production:
  adapter: solid_cable
  polling_interval: 0.1  # 100ms
  message_retention: 1.day
```

```ruby
# No Redis needed!
# Solid Cable stores messages in database
# Polls for new messages every 100ms
```

### Migration

```bash
rails solid_cable:install
rails db:migrate
```

Creates `solid_cable_messages` table.

### Trade-offs

**Solid Cable:**
- Simpler deployment (no Redis)
- One database to manage
- ~100-150ms latency
- Sufficient for chat, notifications, updates

**Redis:**
- Lower latency (<50ms)
- Higher throughput
- Better for millions of connections

For most apps, Solid Cable is simpler and sufficient.

See `references/solid-cable.md` for details.

## Common Patterns

### Chat Application

```ruby
# Channel
class ChatChannel < ApplicationCable::Channel
  def subscribed
    stream_from "chat_#{params[:room_id]}"
  end

  def speak(data)
    Message.create!(
      room_id: params[:room_id],
      user: current_user,
      content: data['message']
    )
  end
end

# Model
class Message < ApplicationRecord
  after_create_commit -> {
    broadcast_append_to "chat_#{room_id}",
      target: "messages",
      partial: "messages/message",
      locals: { message: self }
  }
end
```

### Live Notifications

```ruby
class NotificationChannel < ApplicationCable::Channel
  def subscribed
    stream_for current_user
  end
end

# Broadcast to specific user
NotificationChannel.broadcast_to(user, {
  html: render_notification(notification)
})
```

### Presence (Who's Online)

```ruby
class AppearanceChannel < ApplicationCable::Channel
  def subscribed
    stream_from "appearances"
    broadcast_appearance("online")
  end

  def unsubscribed
    broadcast_appearance("offline")
  end

  def appear
    broadcast_appearance("online")
  end

  def away
    broadcast_appearance("away")
  end

  private

  def broadcast_appearance(status)
    ActionCable.server.broadcast("appearances", {
      user_id: current_user.id,
      username: current_user.name,
      status: status
    })
  end
end
```

See `references/action-cable-patterns.md` for more examples.

## Testing

### Channel Tests

```ruby
require "test_helper"

class ChatChannelTest < ActionCable::Channel::TestCase
  test "subscribes to stream" do
    subscribe room_id: 42

    assert subscription.confirmed?
    assert_has_stream "chat_42"
  end

  test "receives broadcasts" do
    subscribe room_id: 42

    perform :speak, message: "Hello!"

    assert_broadcast_on("chat_42", message: "Hello!")
  end
end
```

### Integration Tests

```ruby
test "broadcasts message to chat" do
  room = rooms(:general)

  assert_broadcasts("chat_#{room.id}", 1) do
    Message.create!(room: room, user: users(:alice), content: "Hello!")
  end
end
```

## Deployment Considerations

### Standalone Server

For high-traffic apps, run Action Cable on separate servers:

```ruby
# config/cable.yml
production:
  adapter: solid_cable
  url: wss://cable.example.com
```

### Scaling

Action Cable scales horizontally:
- Multiple app servers
- Shared pub/sub (Solid Cable database or Redis)
- Load balancer with WebSocket support

### Monitoring

Track connection count, message throughput, latency, and errors.

## Alternatives to Action Cable

### Server-Sent Events (SSE)

One-way server → client:

```ruby
def stream
  response.headers['Content-Type'] = 'text/event-stream'
  response.headers['Cache-Control'] = 'no-cache'

  sse = SSE.new(response.stream)
  sse.write({ message: "Hello" })
ensure
  sse.close
end
```

**Use when:** Only server → client needed (notifications, live feeds)

### Polling

Regular HTTP requests:

```javascript
setInterval(() => {
  fetch('/api/notifications/latest')
    .then(r => r.json())
    .then(data => updateUI(data))
}, 5000)
```

**Use when:** Simple updates, low frequency, broad browser support needed

## Further Reading

For deeper exploration:

- **`references/action-cable-patterns.md`**: Chat, notifications, presence patterns
- **`references/solid-cable.md`**: Database-backed pub/sub in Rails 8

For code examples (in `examples/`):

- **`chat-channel.rb`**: Real-time chat with typing indicators
- **`notifications-channel.rb`**: User-specific push notifications
- **`presence-channel.rb`**: Online status tracking
- **`dashboard-channel.rb`**: Admin dashboard with live stats
- **`multi-room-chat.rb`**: Multiple rooms with private messages
- **`collaborative-editing.rb`**: Document editing with cursors
- **`live-feed.rb`**: Real-time feed updates

## Summary

Action Cable provides:
- **WebSocket integration** with Rails
- **Channels** for logical grouping
- **Broadcasting** to connected clients
- **Authentication** via connection identification
- **Solid Cable** for database-backed pub/sub (Rails 8)
- **Turbo Streams** integration for HTML updates

Master Action Cable and you'll build real-time features that feel magical.
