---
name: "Sidekiq & Async Patterns"
description: "Complete guide to background job processing with Sidekiq in Ruby on Rails. Use this skill when: (1) Creating background jobs, (2) Configuring queues and workers, (3) Implementing retry logic and error handling, (4) Designing idempotent jobs, (5) Setting up scheduled/recurring jobs, (6) Optimizing job performance."
---

# Sidekiq & Async Patterns Skill

This skill provides comprehensive guidance for implementing background jobs with Sidekiq in Rails applications.

## When to Use This Skill

- Creating new background jobs
- Configuring Sidekiq queues
- Implementing retry strategies
- Designing idempotent operations
- Setting up scheduled jobs
- Handling job failures
- Optimizing async processing

## External Documentation

**Official Wiki**: https://github.com/sidekiq/sidekiq/wiki

```bash
# Always check the official wiki for latest patterns
# Key wiki pages:
# - Best Practices: https://github.com/sidekiq/sidekiq/wiki/Best-Practices
# - Error Handling: https://github.com/sidekiq/sidekiq/wiki/Error-Handling
# - Scheduled Jobs: https://github.com/sidekiq/sidekiq/wiki/Scheduled-Jobs
```

## Pre-Work Inspection

```bash
# Check existing jobs
ls app/jobs/ app/sidekiq/ app/workers/ 2>/dev/null

# Check job naming conventions
head -30 $(find app/jobs -name '*.rb' | head -1) 2>/dev/null

# Check Sidekiq configuration
cat config/sidekiq.yml 2>/dev/null
cat config/initializers/sidekiq.rb 2>/dev/null

# Check queue configuration
grep -r 'queue_as\|sidekiq_options' app/jobs/ --include='*.rb' | head -10

# Check scheduled jobs
cat config/schedule.yml 2>/dev/null
cat config/recurring.yml 2>/dev/null
```

## Core Principles

### 1. Idempotency (CRITICAL)

**Jobs MUST be idempotent** - running the same job multiple times produces the same result.

```ruby
# WRONG - Not idempotent (sends duplicate emails)
class SendWelcomeEmailJob < ApplicationJob
  def perform(user_id)
    user = User.find(user_id)
    UserMailer.welcome(user).deliver_now
  end
end

# CORRECT - Idempotent (checks before sending)
class SendWelcomeEmailJob < ApplicationJob
  def perform(user_id)
    user = User.find(user_id)
    return if user.welcome_email_sent_at.present?
    
    UserMailer.welcome(user).deliver_now
    user.update!(welcome_email_sent_at: Time.current)
  end
end
```

### 2. Small Payloads

**Pass IDs, not objects** - objects serialize and can become stale.

```ruby
# WRONG - Object serialization
NotificationJob.perform_later(@user)  # Serializes entire user object

# CORRECT - Pass ID
NotificationJob.perform_later(@user.id)
```

### 3. Fail Fast

**Find records early** - fail immediately if data doesn't exist.

```ruby
class ProcessTaskJob < ApplicationJob
  def perform(task_id)
    task = Task.find(task_id)  # Raises if not found
    # ... process task
  end
end
```

## Job Structure Template

```ruby
# app/jobs/task_notification_job.rb
class TaskNotificationJob < ApplicationJob
  queue_as :notifications
  
  # Retry configuration
  retry_on ActiveRecord::RecordNotFound, wait: 5.seconds, attempts: 3
  retry_on Net::OpenTimeout, wait: :polynomially_longer, attempts: 5
  discard_on ActiveJob::DeserializationError

  def perform(task_id, notification_type = :created)
    task = Task.find(task_id)
    
    case notification_type.to_sym
    when :created
      send_creation_notification(task)
    when :completed
      send_completion_notification(task)
    end
  end

  private

  def send_creation_notification(task)
    return unless task.recipient.phone.present?
    return if task.notification_sent_at.present?  # Idempotency check
    
    SmsService.send(
      to: task.recipient.phone,
      message: I18n.t('sms.task_created', tracking: task.tracking_number)
    )
    
    task.update!(notification_sent_at: Time.current)
  end

  def send_completion_notification(task)
    # Implementation
  end
end
```

## Sidekiq Configuration

### config/sidekiq.yml

```yaml
---
:concurrency: <%= ENV.fetch('SIDEKIQ_CONCURRENCY', 10) %>
:timeout: 25
:max_retries: 5

:queues:
  - [critical, 6]      # Highest priority
  - [default, 5]
  - [notifications, 4]
  - [integrations, 3]  # External API calls
  - [bulk, 2]          # Batch processing
  - [scheduled, 1]
  - [low, 1]           # Lowest priority

production:
  :concurrency: 20

development:
  :concurrency: 5
```

### config/initializers/sidekiq.rb

```ruby
Sidekiq.configure_server do |config|
  config.redis = {
    url: ENV.fetch('REDIS_URL', 'redis://localhost:6379/0'),
    network_timeout: 5,
    pool_timeout: 5
  }

  # Death handler - job exhausted all retries
  config.death_handlers << ->(job, ex) do
    Rails.logger.error("Job #{job['class']} died: #{ex.message}")
    Sentry.capture_exception(ex, extra: { job: job })
  end
end

Sidekiq.configure_client do |config|
  config.redis = {
    url: ENV.fetch('REDIS_URL', 'redis://localhost:6379/0'),
    network_timeout: 5,
    pool_timeout: 5
  }
end

# Recommended: strict argument mode
Sidekiq.strict_args!
```

## Queue Strategy

### Priority Guidelines

| Queue | Priority | Use For |
|-------|----------|---------|
| `critical` | 6 | Payment processing, time-sensitive operations |
| `default` | 5 | Standard operations |
| `notifications` | 4 | User notifications (SMS, email, push) |
| `integrations` | 3 | External API calls (may be slow) |
| `bulk` | 2 | Batch processing, imports |
| `scheduled` | 1 | Scheduled/recurring tasks |
| `low` | 1 | Non-urgent, can wait |

### Setting Queue in Jobs

```ruby
class PaymentProcessingJob < ApplicationJob
  queue_as :critical
  
  def perform(payment_id)
    # Critical payment processing
  end
end

class SendNewsletterJob < ApplicationJob
  queue_as :low
  
  def perform(user_ids)
    # Low priority newsletter
  end
end

# Dynamic queue selection
class FlexibleJob < ApplicationJob
  queue_as do
    if self.arguments.first.priority == 'high'
      :critical
    else
      :default
    end
  end
end
```

## Retry Strategies

### Built-in Retry Configuration

```ruby
class ExternalApiJob < ApplicationJob
  # Retry specific exceptions
  retry_on Net::OpenTimeout, wait: 5.seconds, attempts: 3
  retry_on Faraday::TimeoutError, wait: :polynomially_longer, attempts: 5
  
  # Exponential backoff: 3s, 18s, 83s, 258s, 627s
  retry_on ApiRateLimitError, wait: :polynomially_longer, attempts: 5
  
  # Custom wait calculation
  retry_on CustomError, wait: ->(executions) { executions * 10.seconds }
  
  # Don't retry these - discard instead
  discard_on ActiveJob::DeserializationError
  discard_on UnrecoverableError
  
  def perform(task_id)
    # Implementation
  end
end
```

### Manual Retry Control

```ruby
class ManualRetryJob < ApplicationJob
  def perform(task_id)
    task = Task.find(task_id)
    
    begin
      external_service.process(task)
    rescue RateLimitError => e
      # Re-enqueue with delay
      self.class.set(wait: 1.minute).perform_later(task_id)
    rescue PermanentError => e
      # Don't retry, log and notify
      Rails.logger.error("Permanent failure: #{e.message}")
      Sentry.capture_exception(e)
    end
  end
end
```

## Common Job Patterns

### Batch Processing

```ruby
class BulkUpdateJob < ApplicationJob
  queue_as :bulk

  def perform(record_ids, attributes)
    Model.where(id: record_ids).find_each(batch_size: 100) do |record|
      record.update!(attributes)
    rescue ActiveRecord::RecordInvalid => e
      Rails.logger.error("Failed to update #{record.id}: #{e.message}")
      # Continue with next record
    end
  end
end
```

### Progress Tracking

```ruby
class ImportJob < ApplicationJob
  queue_as :bulk

  def perform(import_id)
    import = Import.find(import_id)
    import.update!(status: 'processing', started_at: Time.current)

    total = import.rows.count
    processed = 0
    errors = []

    import.rows.each do |row|
      begin
        process_row(row, import)
        processed += 1
      rescue StandardError => e
        errors << { row: row[:number], error: e.message }
      end

      # Update progress every 10 rows
      if processed % 10 == 0
        import.update!(
          progress: (processed.to_f / total * 100).round(1),
          processed_count: processed
        )
      end
    end

    import.update!(
      status: errors.empty? ? 'completed' : 'completed_with_errors',
      completed_at: Time.current,
      error_details: errors
    )
  end
end
```

### External API Calls

```ruby
class SyncExternalDataJob < ApplicationJob
  queue_as :integrations

  retry_on Faraday::TimeoutError, wait: 1.minute, attempts: 3
  retry_on Faraday::ConnectionFailed, wait: 5.minutes, attempts: 3
  discard_on ExternalApi::ClientError  # 4xx errors - don't retry

  def perform(resource_id)
    resource = Resource.find(resource_id)
    
    data = ExternalApi.fetch(resource.external_id)
    
    resource.update!(
      external_data: data,
      synced_at: Time.current
    )
  end
end
```

### Scheduled Jobs (with sidekiq-scheduler)

```yaml
# config/recurring.yml
daily_cleanup:
  cron: '0 2 * * *'  # 2 AM daily
  class: DailyCleanupJob
  queue: scheduled

hourly_sync:
  cron: '0 * * * *'  # Every hour
  class: HourlySyncJob
  queue: integrations

weekly_report:
  cron: '0 9 * * 1'  # Monday 9 AM
  class: WeeklyReportJob
  queue: low
```

### Unique Jobs (with sidekiq-unique-jobs)

```ruby
class UniqueProcessingJob < ApplicationJob
  queue_as :default

  # Prevent duplicate jobs for same arguments
  sidekiq_options lock: :until_executed,
                  lock_args_method: :lock_args

  def self.lock_args(args)
    [args[0]]  # Lock on first argument only
  end

  def perform(resource_id, options = {})
    # Only one job per resource_id at a time
  end
end
```

## Error Handling

### Comprehensive Error Wrapper

```ruby
# app/jobs/concerns/error_handling.rb
module ErrorHandling
  extend ActiveSupport::Concern

  included do
    around_perform :with_error_handling
  end

  private

  def with_error_handling
    yield
  rescue ActiveRecord::RecordNotFound => e
    # Log but don't re-raise (job completes)
    Rails.logger.warn("#{self.class.name}: Record not found - #{e.message}")
  rescue StandardError => e
    # Log, notify, and re-raise (triggers retry)
    Rails.logger.error("#{self.class.name} failed: #{e.message}")
    Sentry.capture_exception(e, extra: { job_args: arguments })
    raise
  end
end

# Usage
class MyJob < ApplicationJob
  include ErrorHandling
  
  def perform(task_id)
    # Implementation
  end
end
```

## Testing Jobs

```ruby
# spec/jobs/task_notification_job_spec.rb
require 'rails_helper'

RSpec.describe TaskNotificationJob, type: :job do
  include ActiveJob::TestHelper

  let(:task) { create(:task) }

  describe '#perform' do
    it 'sends notification' do
      expect(SmsService).to receive(:send).with(
        to: task.recipient.phone,
        message: include(task.tracking_number)
      )

      described_class.perform_now(task.id)
    end

    it 'is idempotent' do
      allow(SmsService).to receive(:send)
      
      # First call
      described_class.perform_now(task.id)
      
      # Second call should not send again
      expect(SmsService).not_to receive(:send)
      described_class.perform_now(task.id)
    end

    context 'when task not found' do
      it 'raises error' do
        expect {
          described_class.perform_now(0)
        }.to raise_error(ActiveRecord::RecordNotFound)
      end
    end
  end

  describe 'queueing' do
    it 'queues on correct queue' do
      expect {
        described_class.perform_later(task.id)
      }.to have_enqueued_job.on_queue('notifications')
    end
  end
end
```

## Monitoring & Debugging

### Sidekiq Web UI

```ruby
# config/routes.rb
require 'sidekiq/web'

Rails.application.routes.draw do
  # Protect with authentication
  authenticate :user, ->(u) { u.admin? } do
    mount Sidekiq::Web => '/sidekiq'
  end
end
```

### Useful Commands

```bash
# Check queue sizes
redis-cli LLEN queue:default
redis-cli LLEN queue:critical

# Monitor Sidekiq processes
bundle exec sidekiq -q critical -q default

# Clear all queues (DANGEROUS)
redis-cli FLUSHDB

# Check scheduled jobs
redis-cli ZRANGE schedule 0 -1
```

## Anti-Patterns to Avoid

### ❌ Non-Idempotent Jobs

```ruby
# WRONG
def perform(user_id)
  User.find(user_id).increment!(:login_count)
end
```

### ❌ Large Payloads

```ruby
# WRONG
def perform(user_data)  # Passing full hash
  User.create!(user_data)
end

# CORRECT
def perform(user_id)
  user = User.find(user_id)
  # Process user
end
```

### ❌ Long-Running Jobs

```ruby
# WRONG - Job runs for hours
def perform
  User.all.each { |u| process(u) }
end

# CORRECT - Batch into smaller jobs
def perform(user_ids)
  User.where(id: user_ids).find_each { |u| process(u) }
end
```

### ❌ No Error Handling

```ruby
# WRONG
def perform(task_id)
  external_api.call(task_id)  # May fail silently
end

# CORRECT
def perform(task_id)
  result = external_api.call(task_id)
  raise "API failed: #{result.error}" unless result.success?
end
```

## Sidekiq 7.x Modern Features

### Capsules (Sidekiq 7.2+)
```ruby
# config/initializers/sidekiq.rb
Sidekiq.configure_server do |config|
  # Define separate thread pools for different workloads
  config.capsule("default") do |cap|
    cap.concurrency = 5
    cap.queues = %w[default low]
  end

  config.capsule("critical") do |cap|
    cap.concurrency = 10
    cap.queues = %w[critical high_priority]
  end

  config.capsule("bulk") do |cap|
    cap.concurrency = 20
    cap.queues = %w[bulk imports exports]
  end
end

# Jobs automatically use appropriate capsule based on queue
class CriticalJob < ApplicationJob
  queue_as :critical  # Uses "critical" capsule
end
```

### Embedded Mode (Sidekiq 7.0+)
```ruby
# config/puma.rb
# Run Sidekiq in-process with Puma
on_worker_boot do
  @sidekiq_pid = fork do
    require 'sidekiq/cli'
    Sidekiq::CLI.instance.run([
      '-c', '5',
      '-q', 'critical,5',
      '-q', 'default,3'
    ])
  end
end

on_worker_shutdown do
  Process.kill('TERM', @sidekiq_pid) if @sidekiq_pid
  Process.wait(@sidekiq_pid) if @sidekiq_pid
rescue Errno::ESRCH, Errno::ECHILD
  # Process already gone
end
```

### Strict Arguments (Sidekiq 7.0+)
```ruby
# config/initializers/sidekiq.rb
# Enforce strict argument checking
Sidekiq.strict_args!

# Only JSON-native types allowed
class GoodJob < ApplicationJob
  def perform(user_id, options = {})
    # ✅ Works: primitives, arrays, hashes
  end
end

class BadJob < ApplicationJob
  def perform(user)
    # ❌ Fails: ActiveRecord objects
  end
end
```

### Job Iteration (for Long-Running Jobs)
```ruby
# Gemfile
gem 'job-iteration'

# app/jobs/bulk_update_job.rb
class BulkUpdateJob < ApplicationJob
  include JobIteration::Iteration

  def build_enumerator(cursor:)
    active_record_records_enumerator(
      User.where(active: true),
      cursor: cursor,
      batch_size: 100
    )
  end

  def each_iteration(user, cursor:)
    user.update!(last_seen_at: Time.current)
  end
end

# Graceful interruption support
# Job can be paused and resumed without data loss
```

## Sidekiq Pro Features (Paid)

### Batches
```ruby
# Track completion of multiple related jobs
class BulkProcessingJob < ApplicationJob
  def perform
    batch = Sidekiq::Batch.new
    batch.description = "Process 1000 users"

    batch.on(:success, BulkProcessingCallback)
    batch.on(:complete, BulkProcessingCallback)

    batch.jobs do
      User.find_in_batches(batch_size: 100) do |users|
        users.each do |user|
          ProcessUserJob.perform_async(user.id)
        end
      end
    end
  end
end

class BulkProcessingCallback
  def on_success(status, options)
    # All jobs succeeded
    AdminMailer.bulk_processing_complete.deliver_now
  end

  def on_complete(status, options)
    # All jobs finished (some may have failed)
    if status.failures > 0
      AdminMailer.bulk_processing_with_errors(status.failures).deliver_now
    end
  end
end
```

### Super Fetch (Performance Boost)
```ruby
# config/initializers/sidekiq.rb
Sidekiq::Pro.configure_server do |config|
  # Fetch jobs in bulk (25 at a time)
  config.super_fetch!

  # Reduce Redis round-trips by ~95%
  # Significantly improves throughput
end
```

### Reliability Features
```ruby
# config/initializers/sidekiq.rb
Sidekiq::Pro.configure_server do |config|
  # Persistent storage - jobs survive Redis restarts
  config.reliable_fetch!

  # If process dies, jobs return to queue within 30 minutes
  config.reliability_heartbeat_interval = 30.minutes
end
```

### Rate Limiting (Pro)
```ruby
class ApiCallJob < ApplicationJob
  include Sidekiq::Limiter::Mixin

  sidekiq_options queue: :integrations

  # Limit to 10 concurrent jobs
  sidekiq_options limit: {
    concurrency: 10,
    timeout: 60  # Wait up to 60s for slot
  }

  # Limit by custom key (e.g., per API key)
  def perform(api_key, params)
    # Rate limit per API key
    limiter = Sidekiq::Limiter.concurrent(api_key, 5)

    limiter.within_limit do
      ExternalApi.call(api_key, params)
    end
  end
end
```

## Sidekiq Enterprise Features (Paid)

### Unique Jobs (Built-in)
```ruby
class UniqueProcessingJob < ApplicationJob
  sidekiq_options lock: :until_executed,
                  lock_timeout: 3600

  def perform(resource_id)
    # Only one job per resource_id can execute at a time
    resource = Resource.find(resource_id)
    resource.process!
  end
end

# Lock strategies:
# :until_executing - Unlock when job starts
# :until_executed  - Unlock when job finishes
# :until_expired   - Unlock after lock_timeout
```

### Periodic Jobs (Replacement for sidekiq-scheduler)
```ruby
# config/initializers/sidekiq.rb
Sidekiq::Enterprise.configure_server do |config|
  config.periodic do |p|
    # Run every day at 2 AM
    p.cron "DailyCleanup", "0 2 * * *", class: "DailyCleanupJob"

    # Run every hour
    p.every "HourlySync", "1h", class: "HourlySyncJob"

    # Run every 30 minutes
    p.every "FrequentTask", "30m", class: "FrequentTaskJob"

    # With custom queue
    p.every "LowPriorityTask", "6h", class: "LowPriorityJob", queue: "low"
  end
end
```

### Rate Limiting (Enterprise)
```ruby
# Global rate limiting across all workers
class ThrottledJob < ApplicationJob
  include Sidekiq::RateLimiter::Mixin

  # Limit to 100 jobs per minute
  sidekiq_throttle threshold: { limit: 100, period: 60 }

  def perform(user_id)
    # Only 100 of these will execute per minute
  end
end

# Per-argument rate limiting
class PerUserJob < ApplicationJob
  include Sidekiq::RateLimiter::Mixin

  sidekiq_throttle threshold: {
    limit: 10,
    period: 3600,
    key: -> (user_id) { "user:#{user_id}" }
  }

  def perform(user_id)
    # Max 10 jobs per user per hour
  end
end
```

### Rolling Restarts (Zero Downtime)
```ruby
# Terminal 1: Start new version
bundle exec sidekiq -C config/sidekiq.yml

# Terminal 2: Gracefully stop old version
bundle exec sidekiqctl quiet /tmp/sidekiq.pid
# Workers stop accepting new jobs, finish current ones
# Then:
bundle exec sidekiqctl stop /tmp/sidekiq.pid
```

## Advanced Patterns

### Transactional Outbox Pattern
```ruby
# Ensure jobs are enqueued only if database transaction succeeds
class CreateUserService
  def call(params)
    user = nil

    ApplicationRecord.transaction do
      user = User.create!(params)

      # Job enqueued only if transaction commits
      SendWelcomeEmailJob.perform_later(user.id)

      # For immediate execution on commit
      # after_commit { SendWelcomeEmailJob.perform_later(user.id) }
    end

    user
  end
end

# Better: Use after_commit callback
class User < ApplicationRecord
  after_commit :send_welcome_email, on: :create

  private

  def send_welcome_email
    SendWelcomeEmailJob.perform_later(id)
  end
end
```

### Debouncing Jobs
```ruby
# app/jobs/search_index_job.rb
class SearchIndexJob < ApplicationJob
  sidekiq_options lock: :until_executed

  def perform(model_class, model_id)
    # Wait 5 seconds to batch multiple updates
    sleep 5

    model = model_class.constantize.find(model_id)
    model.reindex
  end
end

# In model:
after_commit :schedule_reindex

def schedule_reindex
  SearchIndexJob.set(wait: 5.seconds).perform_later(
    self.class.name,
    id
  )
end
```

### Job Chaining
```ruby
class StepOneJob < ApplicationJob
  def perform(data_id)
    data = Data.find(data_id)
    result = process_step_one(data)

    # Chain to next job
    StepTwoJob.perform_later(data_id, result) if result.success?
  end
end

class StepTwoJob < ApplicationJob
  def perform(data_id, step_one_result)
    data = Data.find(data_id)
    result = process_step_two(data, step_one_result)

    # Chain to final job
    StepThreeJob.perform_later(data_id, result) if result.success?
  end
end
```

### Parent-Child Job Pattern
```ruby
class ParentJob < ApplicationJob
  def perform(batch_id)
    batch = Batch.find(batch_id)

    batch.items.find_each do |item|
      ChildJob.perform_later(item.id, batch_id)
    end

    # Track completion
    batch.update!(child_jobs_count: batch.items.count)
  end
end

class ChildJob < ApplicationJob
  def perform(item_id, batch_id)
    item = Item.find(item_id)
    item.process!

    # Decrement counter
    batch = Batch.find(batch_id)
    batch.decrement!(:child_jobs_count)

    # Check if all children complete
    CompleteParentJob.perform_later(batch_id) if batch.child_jobs_count.zero?
  end
end
```

## Performance Optimization

### Connection Pooling
```ruby
# config/initializers/sidekiq.rb
Sidekiq.configure_server do |config|
  # Match concurrency + 5
  config.redis = {
    url: ENV['REDIS_URL'],
    pool_size: (ENV['SIDEKIQ_CONCURRENCY']&.to_i || 10) + 5
  }
end

# config/database.yml
production:
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  # Sidekiq needs pool >= concurrency
```

### Bulk Enqueuing
```ruby
# Instead of this (N Redis calls):
users.each do |user|
  SendEmailJob.perform_later(user.id)
end

# Do this (1 Redis call):
args = users.map { |user| [user.id] }
Sidekiq::Client.push_bulk(
  'class' => SendEmailJob,
  'queue' => 'notifications',
  'args' => args
)
```

### Job Compression (for Large Payloads)
```ruby
# app/jobs/large_data_job.rb
class LargeDataJob < ApplicationJob
  before_perform do |job|
    # Decompress arguments
    if job.arguments.first.is_a?(String) && job.arguments.first.start_with?('COMPRESSED:')
      compressed = job.arguments.first.sub('COMPRESSED:', '')
      decompressed = Zlib::Inflate.inflate(Base64.decode64(compressed))
      job.arguments[0] = JSON.parse(decompressed)
    end
  end

  def perform(large_data)
    # Process data
  end

  def self.perform_later_compressed(data)
    json = data.to_json
    compressed = Base64.encode64(Zlib::Deflate.deflate(json))
    perform_later("COMPRESSED:#{compressed}")
  end
end
```

### Database Query Optimization
```ruby
# WRONG: N+1 queries in job
class ProcessUsersJob < ApplicationJob
  def perform(user_ids)
    User.where(id: user_ids).each do |user|
      user.orders.each do |order|  # N+1!
        process_order(order)
      end
    end
  end
end

# CORRECT: Eager loading
class ProcessUsersJob < ApplicationJob
  def perform(user_ids)
    User.includes(:orders).where(id: user_ids).each do |user|
      user.orders.each do |order|
        process_order(order)
      end
    end
  end
end
```

## Monitoring & Observability

### Custom Metrics
```ruby
# app/jobs/concerns/metrics.rb
module JobMetrics
  extend ActiveSupport::Concern

  included do
    around_perform :track_job_metrics
  end

  private

  def track_job_metrics
    start_time = Time.current

    yield

    duration = (Time.current - start_time) * 1000

    StatsD.increment("jobs.#{self.class.name.underscore}.success")
    StatsD.timing("jobs.#{self.class.name.underscore}.duration", duration)
  rescue StandardError => e
    StatsD.increment("jobs.#{self.class.name.underscore}.failure")
    raise
  end
end

# Usage
class MyJob < ApplicationJob
  include JobMetrics
end
```

### Logging Best Practices
```ruby
class WellLoggedJob < ApplicationJob
  def perform(resource_id)
    logger.info({
      job: self.class.name,
      resource_id: resource_id,
      jid: jid,
      event: 'started'
    }.to_json)

    resource = Resource.find(resource_id)
    result = process(resource)

    logger.info({
      job: self.class.name,
      resource_id: resource_id,
      jid: jid,
      event: 'completed',
      result: result
    }.to_json)
  rescue StandardError => e
    logger.error({
      job: self.class.name,
      resource_id: resource_id,
      jid: jid,
      event: 'failed',
      error: e.class.name,
      message: e.message
    }.to_json)
    raise
  end
end
```

### Dead Job Alerts
```ruby
# config/initializers/sidekiq.rb
Sidekiq.configure_server do |config|
  config.death_handlers << ->(job, exception) do
    # Job exhausted all retries
    Rails.logger.error({
      event: 'job_died',
      job_class: job['class'],
      args: job['args'],
      error: exception.message,
      retry_count: job['retry_count']
    }.to_json)

    # Alert team
    if defined?(Sentry)
      Sentry.capture_message("Job died: #{job['class']}", extra: {
        job: job,
        exception: exception
      })
    end

    # Slack notification for critical jobs
    if job['queue'] == 'critical'
      SlackNotifier.notify(
        "🚨 Critical job failed: #{job['class']}",
        exception.message
      )
    end
  end
end
```

## Checklist Before Creating Jobs

```
[ ] Job is idempotent (safe to run multiple times)
[ ] Passes IDs, not objects
[ ] Has appropriate retry configuration
[ ] Handles expected errors gracefully
[ ] Logs failures for debugging
[ ] Has correct queue assignment
[ ] Has tests covering happy path and failures
[ ] Considers Sidekiq 7.x features (capsules, strict args)
[ ] Uses job iteration for long-running tasks
[ ] Implements proper monitoring and metrics
[ ] Documents expected runtime and dependencies
```
