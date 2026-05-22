---
name: rails-background-jobs
description: Specialized skill for Rails background jobs with Solid Queue. Use when creating jobs, scheduling tasks, implementing recurring jobs, testing jobs, or monitoring job queues. Includes best practices for reliable background processing.
---

# Rails Background Jobs

Modern background processing with Solid Queue and Mission Control.

## When to Use This Skill

- Creating background jobs
- Scheduling delayed tasks
- Setting up recurring jobs (cron-like)
- Testing jobs with RSpec
- Monitoring jobs with Mission Control
- Implementing retry strategies
- Handling job failures
- Processing bulk operations

## Tech Stack

```ruby
# Gemfile
gem "solid_queue"           # Background jobs
gem "mission_control-jobs"  # Web UI for monitoring
```

## Setup

```bash
# Install Solid Queue
$ bin/rails solid_queue:install

# This creates:
# - db/queue_schema.rb
# - config/queue.yml
# - config/recurring.yml
```

```ruby
# config/application.rb
config.active_job.queue_adapter = :solid_queue
```

## Basic Job

```ruby
# app/jobs/send_welcome_email_job.rb
class SendWelcomeEmailJob < ApplicationJob
  queue_as :default

  def perform(user_id)
    user = User.find(user_id)
    UserMailer.welcome(user).deliver_now
  end
end
```

## Queue Configuration

### Queue Names

```ruby
class SendWelcomeEmailJob < ApplicationJob
  queue_as :mailers  # Specific queue

  # Or dynamic queue
  queue_as do
    user.premium? ? :high_priority : :default
  end

  def perform(user)
    # ...
  end
end
```

### Retry Configuration

```ruby
class ProcessPaymentJob < ApplicationJob
  queue_as :payments

  # Retry up to 5 times with exponential backoff
  retry_on PaymentGatewayError, wait: :exponentially_longer, attempts: 5

  # Don't retry certain errors
  discard_on InvalidCardError

  # Custom retry logic
  retry_on ActiveRecord::Deadlocked, wait: 5.seconds, attempts: 3

  def perform(order_id)
    order = Order.find(order_id)
    PaymentGateway.charge(order)
  end
end
```

### Job Callbacks

```ruby
class ReportGenerationJob < ApplicationJob
  before_perform :log_start
  after_perform :log_completion
  around_perform :measure_time

  def perform(report_id)
    report = Report.find(report_id)
    report.generate!
  end

  private

  def log_start
    Rails.logger.info "Starting report generation"
  end

  def log_completion
    Rails.logger.info "Completed report generation"
  end

  def measure_time
    start = Time.current
    yield
    duration = Time.current - start
    Rails.logger.info "Report took #{duration}s"
  end
end
```

## Scheduling Jobs

### Immediate Execution

```ruby
# Enqueue now
SendWelcomeEmailJob.perform_later(user.id)

# With options
SendWelcomeEmailJob.set(queue: :high_priority, priority: 10)
  .perform_later(user.id)
```

### Delayed Execution

```ruby
# Run in 1 hour
SendReminderJob.set(wait: 1.hour).perform_later(user.id)

# Run at specific time
SendNewsletterJob.set(wait_until: Date.tomorrow.noon).perform_later

# Run in 2 days
ExportDataJob.set(wait: 2.days).perform_later(user.id)
```

### Bulk Enqueuing

```ruby
# Better: Use perform_all_later (Rails 7.1+)
jobs = User.pluck(:id).map do |user_id|
  SendWelcomeEmailJob.new(user_id)
end

ActiveJob.perform_all_later(jobs)
```

## Recurring Jobs

### Configuration

```yaml
# config/recurring.yml
production:
  cleanup_old_records:
    class: CleanupJob
    schedule: every day at 2am

  send_daily_digest:
    class: DailyDigestJob
    schedule: every day at 8am
    args: ["digest"]

  process_payments:
    class: ProcessPaymentsJob
    schedule: every 15 minutes

  generate_reports:
    class: GenerateReportsJob
    schedule: every monday at 9am
    args: ["weekly"]
```

### Recurring Job Class

```ruby
# app/jobs/cleanup_job.rb
class CleanupJob < ApplicationJob
  queue_as :maintenance

  def perform
    # Clean old records
    OldRecord.where("created_at < ?", 90.days.ago).delete_all

    # Clean expired sessions
    ActiveRecord::SessionStore::Session
      .where("updated_at < ?", 30.days.ago)
      .delete_all

    Rails.logger.info "Cleanup completed"
  end
end
```

### Schedule Syntax

```yaml
# Every X minutes/hours/days
schedule: every 5 minutes
schedule: every 2 hours
schedule: every day

# Specific times
schedule: every day at 3pm
schedule: every monday at 9am
schedule: every 1st of month at 8am

# Multiple times
schedule: every day at 9am, 3pm, 9pm
```

## Testing Jobs

### Basic Job Test

```ruby
# spec/jobs/send_welcome_email_job_spec.rb
RSpec.describe SendWelcomeEmailJob, type: :job do
  let(:user) { create(:user) }

  describe "#perform" do
    it "sends welcome email" do
      expect {
        described_class.perform_now(user.id)
      }.to change { ActionMailer::Base.deliveries.count }.by(1)
    end

    it "sends email to correct user" do
      described_class.perform_now(user.id)

      mail = ActionMailer::Base.deliveries.last
      expect(mail.to).to include(user.email)
    end
  end

  describe "enqueuing" do
    it "enqueues job" do
      expect {
        described_class.perform_later(user.id)
      }.to have_enqueued_job(described_class).with(user.id)
    end

    it "enqueues on correct queue" do
      expect {
        described_class.perform_later(user.id)
      }.to have_enqueued_job.on_queue("mailers")
    end

    it "schedules delayed job" do
      expect {
        described_class.set(wait: 1.hour).perform_later(user.id)
      }.to have_enqueued_job.at(1.hour.from_now)
    end
  end
end
```

### Testing with perform_enqueued_jobs

```ruby
RSpec.describe "User registration", type: :request do
  include ActiveJob::TestHelper

  it "sends welcome email" do
    perform_enqueued_jobs do
      post users_path, params: {
        user: { email: "user@example.com", name: "John" }
      }
    end

    expect(ActionMailer::Base.deliveries.count).to eq(1)
  end
end
```

## Monitoring

### Mission Control

```ruby
# config/routes.rb
Rails.application.routes.draw do
  mount MissionControl::Jobs::Engine, at: "/jobs"
end
```

Access at: `http://localhost:3000/jobs`

**Features**:
- View queued, running, and failed jobs
- Retry failed jobs
- Pause/resume queues
- View job history
- Monitor performance

### Running Workers

```bash
# Development
$ bin/jobs

# Production
$ bundle exec rake solid_queue:start
```

## Best Practices

### 1. Keep Jobs Idempotent

Jobs should be safe to run multiple times:

```ruby
# GOOD - Idempotent
class UpdateUserStatusJob < ApplicationJob
  def perform(user_id)
    user = User.find(user_id)
    user.update(status: "active") unless user.active?
  end
end

# BAD - Not idempotent
class IncrementCounterJob < ApplicationJob
  def perform(user_id)
    user = User.find(user_id)
    user.increment!(:login_count)  # Dangerous if runs twice
  end
end
```

### 2. Pass IDs, Not Objects

```ruby
# GOOD - Pass ID
SendEmailJob.perform_later(user.id)

class SendEmailJob < ApplicationJob
  def perform(user_id)
    user = User.find(user_id)  # Fetch fresh data
    UserMailer.welcome(user).deliver_now
  end
end

# BAD - Pass object (stale data risk)
SendEmailJob.perform_later(user)
```

### 3. Break Large Jobs into Smaller Ones

```ruby
# GOOD - Parent job enqueues smaller jobs
class ProcessBatchJob < ApplicationJob
  def perform(batch_id)
    batch = Batch.find(batch_id)

    batch.items.find_each do |item|
      ProcessItemJob.perform_later(item.id)
    end
  end
end

# BAD - One huge job
class ProcessAllItemsJob < ApplicationJob
  def perform
    Item.find_each do |item|  # Could timeout
      item.process!
    end
  end
end
```

### 4. Handle Failures Gracefully

```ruby
class SendNewsletterJob < ApplicationJob
  retry_on MailerError, wait: :exponentially_longer, attempts: 5

  discard_on ActiveRecord::RecordNotFound do |job, error|
    Rails.logger.error "User not found: #{job.arguments.first}"
  end

  def perform(user_id)
    user = User.find(user_id)
    NewsletterMailer.send_to(user).deliver_now
  rescue => e
    ErrorTracker.notify(e, user_id: user_id)
    raise
  end
end
```

### 5. Set Appropriate Timeouts

```ruby
class LongRunningJob < ApplicationJob
  def perform
    Timeout.timeout(5.minutes) do
      # Long-running task
    end
  rescue Timeout::Error
    Rails.logger.error "Job timed out"
    raise  # Will trigger retry
  end
end
```

## Common Patterns

### Conditional Enqueuing

```ruby
class User < ApplicationRecord
  after_create :send_welcome_email

  private

  def send_welcome_email
    SendWelcomeEmailJob.perform_later(id) if confirmed?
  end
end
```

### Error Tracking

```ruby
class ApplicationJob < ActiveJob::Base
  rescue_from StandardError do |exception|
    ErrorTracker.notify(exception, job: self.class.name)
    raise exception  # Re-raise to trigger retry
  end
end
```

## Reference Documentation

For comprehensive job patterns:
- Background jobs guide: `background-jobs.md` (detailed examples and advanced patterns)
