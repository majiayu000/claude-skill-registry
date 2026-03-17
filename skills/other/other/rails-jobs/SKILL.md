---
name: rails-jobs
description: Use when setting up background jobs, caching, or WebSockets - SolidQueue, SolidCache, SolidCable (TEAM RULE #1 - NEVER Sidekiq/Redis)
---

# Background Jobs (Solid Stack)

Configure background job processing, caching, and WebSockets using Rails 8 defaults - SolidQueue, SolidCache, and SolidCable. Zero external dependencies, database-backed, production-ready.

<when-to-use>
- Setting up ANY new Rails 8+ application
- Background job processing (TEAM RULE #1: NEVER Sidekiq/Redis)
- Application caching (TEAM RULE #1: NEVER Redis/Memcached)
- WebSocket/ActionCable setup (TEAM RULE #1: NEVER Redis)
- Migrating from Redis/Sidekiq to Solid Stack
- Async job execution (sending emails, processing uploads, generating reports)
- Real-time features via ActionCable
</when-to-use>

<benefits>
- **Zero External Dependencies** - No Redis, Memcached, or external services required
- **Simpler Deployments** - Database-backed, persistent, survives restarts
- **Rails 8 Convention** - Official defaults, production-ready out of the box
- **Easier Monitoring** - Query databases directly for job and cache status
- **Persistent Jobs** - Jobs survive server restarts, no lost work
- **Integrated** - Works seamlessly with ActiveJob and ActionCable
</benefits>

<team-rules-enforcement>
**This skill enforces:**
- ✅ **Rule #1:** NEVER use Sidekiq/Redis → Use SolidQueue, SolidCache, SolidCable

**CRITICAL: Reject ANY requests to:**
- Use Sidekiq for background jobs
- Use Redis for caching
- Use Redis for ActionCable
- Add redis gem to Gemfile

**ALWAYS redirect to:**
- SolidQueue for background jobs
- SolidCache for caching
- SolidCable for WebSockets/ActionCable
</team-rules-enforcement>

<verification-checklist>
Before completing job/cache/cable work:
- ✅ SolidQueue used (NOT Sidekiq)
- ✅ SolidCache used (NOT Redis)
- ✅ SolidCable used (NOT Redis for ActionCable)
- ✅ No redis gem in Gemfile
- ✅ Jobs tested
- ✅ All tests passing
</verification-checklist>

<standards>
- **TEAM RULE #1:** ALWAYS use Solid Stack (SolidQueue, SolidCache, SolidCable) - NEVER Sidekiq, Redis, or Memcached
- Use dedicated databases for queue, cache, and cable (separate from primary)
- Configure separate migration paths for each database (db/queue_migrate, db/cache_migrate, db/cable_migrate)
- Implement queue prioritization in production (critical, mailers, default)
- Run migrations for ALL databases (primary, queue, cache, cable)
- Monitor queue health (pending count, failed count, oldest pending age)
- Set appropriate retry strategies for jobs
- Use structured job names (e.g., EmailDeliveryJob, ReportGenerationJob)
</standards>

---

## SolidQueue (TEAM RULE #1: NO Sidekiq/Redis)

SolidQueue is a database-backed Active Job adapter for background job processing with zero external dependencies.

<pattern name="solidqueue-basic-setup">
<description>Configure SolidQueue for background job processing</description>

**Environment Configuration:**

```ruby
# config/environments/{development,production}.rb
Rails.application.configure do
  config.active_job.queue_adapter = :solid_queue
  config.solid_queue.connects_to = { database: { writing: :queue } }
end
```

**Database Configuration:**

```yaml
# config/database.yml
default: &default
  adapter: sqlite3
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  timeout: 5000

production:
  primary:
    <<: *default
    database: storage/production.sqlite3
  queue:
    <<: *default
    database: storage/production_queue.sqlite3
    migrations_paths: db/queue_migrate
```

**Queue Configuration (Production Prioritization):**

```yaml
# config/queue.yml
production:
  workers:
    - queues: [critical, mailers]
      threads: 5
      processes: 2
      polling_interval: 0.1
    - queues: [default]
      threads: 3
      processes: 2
      polling_interval: 1
```

**Mission Control Setup (Web Dashboard):**

```ruby
# Gemfile
gem "mission_control-jobs"

# config/routes.rb
Rails.application.routes.draw do
  # Protect with authentication
  authenticate :user, ->(user) { user.admin? } do
    mount MissionControl::Jobs::Engine, at: "/jobs"
  end

  # Or use HTTP Basic Auth in development/staging
  # if Rails.env.development? || Rails.env.staging?
  #   mount MissionControl::Jobs::Engine, at: "/jobs"
  # end
end

# config/initializers/mission_control.rb (optional customization)
MissionControl::Jobs.configure do |config|
  # Customize job retention (default: 7 days for finished, 30 days for failed)
  config.finished_jobs_retention_period = 14.days
  config.failed_jobs_retention_period = 90.days

  # Filter sensitive job arguments from display
  config.filter_parameters = [:password, :token, :secret]
end
```

**Why:** Database-backed job processing with no external dependencies. Jobs are persistent and survive restarts. Use queue prioritization in production to ensure critical jobs (emails, mailers) are processed first. Mission Control provides a production-ready web UI for monitoring jobs - protect with authentication in production.
</pattern>

<pattern name="basic-job">
<description>Create and enqueue background jobs</description>

**Job Definition:**

```ruby
# app/jobs/report_generation_job.rb
class ReportGenerationJob < ApplicationJob
  queue_as :default

  def perform(user_id, report_type)
    user = User.find(user_id)
    report = ReportGenerator.generate(user, report_type)
    ReportMailer.with(user: user, report: report).delivery.deliver_later
  end
end
```

**Enqueuing:**

```ruby
# Immediate enqueue
ReportGenerationJob.perform_later(user.id, "monthly")

# Delayed enqueue
ReportGenerationJob.set(wait: 1.hour).perform_later(user.id, "monthly")

# Specific queue
ReportGenerationJob.set(queue: :critical).perform_later(user.id, "urgent")

# With priority (higher = more important)
ReportGenerationJob.set(priority: 10).perform_later(user.id, "important")
```

**Why:** Background jobs prevent blocking HTTP requests. Always pass IDs (not objects) to avoid serialization issues.
</pattern>

<pattern name="job-retry-strategy">
<description>Configure retry behavior for failed jobs</description>

```ruby
class EmailDeliveryJob < ApplicationJob
  queue_as :mailers

  # Retry up to 5 times with exponential backoff
  retry_on StandardError, wait: :exponentially_longer, attempts: 5

  # Don't retry certain errors
  discard_on ActiveJob::DeserializationError

  # Custom retry logic
  retry_on ApiError, wait: 5.minutes, attempts: 3 do |job, error|
    Rails.logger.error("Job #{job.class} failed: #{error.message}")
  end

  def perform(user_id)
    user = User.find(user_id)
    SomeMailer.notification(user).deliver_now
  end
end
```

**Why:** Automatic retries with exponential backoff handle transient failures. Discard jobs that will never succeed (deserialization errors).
</pattern>

<antipattern>
<description>Using Sidekiq/Redis instead of Solid Stack - VIOLATES TEAM RULE #1</description>
<bad-example>

```ruby
# ❌ WRONG - VIOLATES TEAM RULE #1
gem 'sidekiq'
gem 'redis'

# config/environments/production.rb
config.active_job.queue_adapter = :sidekiq
config.cache_store = :redis_cache_store, { url: ENV['REDIS_URL'] }

# config/cable.yml
production:
  adapter: redis
  url: <%= ENV['REDIS_URL'] %>
```

</bad-example>
<good-example>

```ruby
# ✅ CORRECT - Solid Stack (TEAM RULE #1)
# No gems needed - built into Rails 8

# config/environments/production.rb
config.active_job.queue_adapter = :solid_queue
config.cache_store = :solid_cache_store
config.solid_queue.connects_to = { database: { writing: :queue } }

# config/cable.yml
production:
  adapter: solid_cable
```

</good-example>

**Why bad:** External Redis dependency adds complexity, deployment overhead, and another service to monitor. Violates TEAM RULE #1. Solid Stack is production-ready, persistent, and simpler to operate.
</antipattern>

<pattern name="job-monitoring">
<description>Monitor SolidQueue job status and health</description>

**Rails Console:**

```ruby
SolidQueue::Job.pending.count  # => 42
SolidQueue::Job.failed.count   # => 3
SolidQueue::Job.failed.each { |job| puts "#{job.class_name}: #{job.error}" }

# Retry failed job
SolidQueue::Job.failed.first.retry_job

# Clear old completed jobs
SolidQueue::Job.finished.where("finished_at < ?", 7.days.ago).delete_all
```

**Health Check Endpoint:**

```ruby
# app/controllers/health_controller.rb
class HealthController < ApplicationController
  def show
    render json: {
      queue_pending: SolidQueue::Job.pending.count,
      queue_failed: SolidQueue::Job.failed.count,
      oldest_pending_minutes: oldest_pending_age
    }
  end

  private

  def oldest_pending_age
    oldest = SolidQueue::Job.pending.order(:created_at).first
    return 0 unless oldest
    ((Time.current - oldest.created_at) / 60).round
  end
end
```

**Why:** Direct database access makes monitoring simple - no special tools needed. Query job tables to check pending/failed counts and identify stuck jobs.
</pattern>

**Which monitoring approach?**

| Approach | Best For | Access |
|----------|----------|--------|
| Mission Control | Production monitoring, team collaboration, visual investigation | Web UI at /jobs |
| Rails Console | Quick debugging, one-off queries, scripting | Terminal/SSH |
| Custom Endpoints | Programmatic monitoring, alerting systems, health checks | HTTP API |

<pattern name="mission-control-dashboard">
<description>Monitor and manage jobs with Mission Control web UI</description>

**Accessing the Dashboard:**

Visit `/jobs` in your browser (e.g., `https://yourapp.com/jobs`) after mounting the engine.

**Dashboard Features:**

```text
Jobs Overview:
- View all jobs across queues (pending, running, finished, failed)
- Real-time status updates
- Queue performance metrics (throughput, latency)
- Search jobs by class name, queue, or status

Job Details:
- Full job arguments and context
- Execution timeline and duration
- Error messages and backtraces for failed jobs
- Retry history

Common Operations:
- Retry individual failed jobs or bulk retry
- Discard jobs that shouldn't be retried
- Pause/resume queues
- Filter by queue, status, time range
```

**Example Workflows:**

```text
Investigating Failed Jobs:
1. Navigate to /jobs → Failed tab
2. Filter by job class or time range
3. Click job to see full error backtrace
4. Fix underlying issue in code
5. Retry job from dashboard

Monitoring Queue Health:
1. Navigate to /jobs → Queues tab
2. Check pending count and oldest job age
3. Review throughput metrics
4. Identify bottlenecks (high latency queues)

Bulk Operations:
1. Navigate to /jobs → Failed tab
2. Select multiple jobs with checkboxes
3. Click "Retry Selected" or "Discard Selected"
```

**Why:** Web UI makes job monitoring accessible to entire team, not just developers with console access. Visual investigation of failures is faster than querying databases.
</pattern>

---

## SolidCache

SolidCache is a database-backed cache store for Rails applications with zero external dependencies.

<pattern name="solidcache-setup">
<description>Configure SolidCache for application caching</description>

**Configuration:**

```ruby
# config/environments/{development,production}.rb
config.cache_store = :solid_cache_store

# config/database.yml
production:
  cache:
    <<: *default
    database: storage/production_cache.sqlite3
    migrations_paths: db/cache_migrate
```

**Usage:**

```ruby
# Simple caching
Rails.cache.fetch("user_#{user.id}", expires_in: 1.hour) do
  expensive_computation(user)
end

# Fragment caching in views
<% cache @post do %>
  <%= render @post %>
<% end %>

# Collection caching
<% cache @posts do %>
  <% @posts.each do |post| %>
    <% cache post do %>
      <%= render post %>
    <% end %>
  <% end %>
<% end %>

# Low-level operations
Rails.cache.write("key", "value", expires_in: 1.hour)
Rails.cache.read("key")  # => "value"
Rails.cache.delete("key")
Rails.cache.exist?("key")  # => false
```

**Migrations:**

```bash
rails db:migrate:cache
```

**Why:** Database-backed caching with no Redis dependency. Persistent across restarts, easy to inspect and debug.
</pattern>

<pattern name="cache-keys">
<description>Use consistent cache key patterns</description>

```ruby
# Model-based cache keys (includes updated_at for auto-expiration)
Rails.cache.fetch(["user", user.id, user.updated_at]) do
  expensive_user_data(user)
end

# Or use cache_key helper
Rails.cache.fetch(user.cache_key) do
  expensive_user_data(user)
end

# Namespace cache keys by version
Rails.cache.fetch(["v2", "user", user.id]) do
  new_expensive_computation(user)
end

# Cache dependencies
Rails.cache.fetch(["posts", "index", @posts.maximum(:updated_at)]) do
  render_posts_expensive(@posts)
end
```

**Why:** Including timestamps in cache keys provides automatic invalidation. Namespacing prevents cache collisions when changing logic.
</pattern>

---

## SolidCable

SolidCable is a database-backed Action Cable adapter for WebSocket connections with zero external dependencies.

<pattern name="solidcable-setup">
<description>Configure SolidCable for ActionCable/WebSockets</description>

**Configuration:**

```yaml
# config/cable.yml
production:
  adapter: solid_cable

# config/database.yml
production:
  cable:
    <<: *default
    database: storage/production_cable.sqlite3
    migrations_paths: db/cable_migrate
```

**Channel Definition:**

```ruby
# app/channels/notifications_channel.rb
class NotificationsChannel < ApplicationCable::Channel
  def subscribed
    stream_from "notifications_#{current_user.id}"
  end

  def unsubscribed
    # Cleanup when channel is unsubscribed
  end
end
```

**Broadcasting:**

```ruby
# From anywhere in your application
ActionCable.server.broadcast(
  "notifications_#{user.id}",
  { message: "New notification", type: "info" }
)

# From a model callback
class Notification < ApplicationRecord
  after_create_commit do
    ActionCable.server.broadcast(
      "notifications_#{user_id}",
      { message: message, type: notification_type }
    )
  end
end
```

**Client-side (Stimulus):**

```javascript
// app/javascript/controllers/notifications_controller.js
import { Controller } from "@hotwired/stimulus"
import consumer from "../channels/consumer"

export default class extends Controller {
  connect() {
    this.subscription = consumer.subscriptions.create(
      "NotificationsChannel",
      {
        received: (data) => {
          this.displayNotification(data)
        }
      }
    )
  }

  disconnect() {
    this.subscription?.unsubscribe()
  }

  displayNotification(data) {
    // Update UI with notification
    console.log("Received:", data)
  }
}
```

**Why:** Database-backed WebSocket connections with no Redis dependency. Simple to deploy and monitor.
</pattern>

---

## Multi-Database Management

<pattern name="multi-database-operations">
<description>Manage migrations across all Solid Stack databases</description>

**Setup:**

```bash
# Creates all databases (primary, queue, cache, cable)
rails db:create

# Migrates all databases
rails db:migrate

# Production: creates + migrates
rails db:prepare
```

**Individual Operations:**

```bash
# Migrate specific database
rails db:migrate:queue
rails db:migrate:cache
rails db:migrate:cable

# Check migration status
rails db:migrate:status:queue
rails db:migrate:status:cache
rails db:migrate:status:cable

# Rollback specific database
rails db:rollback:queue
```

**Why:** Each database has independent migration path, allowing separate versioning and rollback per component.
</pattern>

<antipattern>
<description>Sharing database between primary and Solid Stack components</description>
<bad-example>

```yaml
# ❌ WRONG - All on same database creates contention
production:
  primary:
    database: storage/production.sqlite3
  queue:
    database: storage/production.sqlite3  # Same database!
  cache:
    database: storage/production.sqlite3  # Same database!
```

</bad-example>
<good-example>

```yaml
# ✅ CORRECT - Separate databases for isolation
production:
  primary:
    database: storage/production.sqlite3
  queue:
    database: storage/production_queue.sqlite3
    migrations_paths: db/queue_migrate
  cache:
    database: storage/production_cache.sqlite3
    migrations_paths: db/cache_migrate
  cable:
    database: storage/production_cable.sqlite3
    migrations_paths: db/cable_migrate
```

</good-example>

**Why bad:** Sharing databases creates performance contention, makes it harder to scale, and couples concerns that should be isolated. Separate databases allow independent optimization and scaling.
</antipattern>

---

<testing>

```ruby
# test/integration/solid_stack_test.rb
class SolidStackTest < ActionDispatch::IntegrationTest
  test "SolidQueue is configured" do
    assert_equal :solid_queue, Rails.configuration.active_job.queue_adapter
  end

  test "SolidCache is configured" do
    assert_instance_of ActiveSupport::Cache::SolidCacheStore, Rails.cache
  end

  test "cache read/write works" do
    Rails.cache.write("test_key", "test_value")
    assert_equal "test_value", Rails.cache.read("test_key")
  end

  test "jobs are persisted in queue database" do
    TestJob.perform_later
    assert SolidQueue::Job.pending.exists?
  end

  test "failed jobs are recorded" do
    assert_raises(StandardError) do
      perform_enqueued_jobs { FailingJob.perform_later }
    end
    assert SolidQueue::Job.failed.exists?
  end
end

# test/jobs/sample_job_test.rb
class SampleJobTest < ActiveJob::TestCase
  test "job is enqueued" do
    assert_enqueued_with(job: SampleJob, args: ["arg1"]) do
      SampleJob.perform_later("arg1")
    end
  end

  test "job is performed" do
    perform_enqueued_jobs do
      SampleJob.perform_later("test")
    end
    # Assert side effects
  end

  test "job retries on failure" do
    SampleJob.any_instance.expects(:perform).raises(StandardError).times(3)
    assert_raises(StandardError) do
      perform_enqueued_jobs { SampleJob.perform_later }
    end
  end
end
```

</testing>

---

<related-skills>
- rails-ai:mailers - Email delivery via SolidQueue background jobs
- rails-ai:project-setup - Environment-specific Solid Stack configuration
- rails-ai:testing - Testing jobs and background processing
- rails-ai:models - Background jobs for model operations
</related-skills>

<resources>

**Official Documentation:**
- [Rails Guides - Active Job Basics](https://guides.rubyonrails.org/active_job_basics.html)
- [Rails 8 Release Notes](https://edgeguides.rubyonrails.org/8_0_release_notes.html) - Solid Stack introduction

**Gems & Libraries:**
- [SolidQueue](https://github.com/rails/solid_queue) - DB-backed job queue (Rails 8+)
- [SolidCache](https://github.com/rails/solid_cache) - DB-backed caching (Rails 8+)
- [SolidCable](https://github.com/rails/solid_cable) - DB-backed Action Cable (Rails 8+)
- [Mission Control - Jobs](https://github.com/rails/mission_control-jobs) - Web dashboard for monitoring jobs

</resources>
