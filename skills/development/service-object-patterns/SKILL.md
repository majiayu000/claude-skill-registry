---
name: "Service Object Patterns"
description: "Complete guide to implementing Service Objects in Ruby on Rails applications. Use this skill when creating business logic services, organizing service namespaces, handling service results, and designing service interfaces for complex operations."
---

# Service Object Patterns Skill

This skill provides comprehensive guidance for implementing Service Objects in Rails applications following consistent patterns and conventions.

## When to Use This Skill

- Creating new service objects for business logic
- Refactoring fat models or controllers
- Designing service interfaces
- Implementing result objects for service responses
- Organizing services into namespaces

## When to Use Service Objects

### Use Service Objects When:
- Business logic spans multiple models
- Operation has multiple steps/side effects
- Logic doesn't naturally belong to one model
- Need to orchestrate external services
- Complex validation or business rules
- Operation needs transaction management

### Don't Use Service Objects When:
- Simple CRUD operations
- Logic clearly belongs to one model
- Single-line delegation
- No side effects beyond model updates

## Directory Structure

```
app/services/
├── application_service.rb          # Base class
├── tasks_manager/
│   ├── create_task.rb
│   ├── assign_carrier.rb
│   ├── complete_task.rb
│   └── bundling/
│       ├── bundle_tasks.rb
│       └── optimize_routes.rb
├── billing_manager/
│   ├── generate_invoice.rb
│   ├── process_payment.rb
│   └── calculate_fees.rb
├── notifications_manager/
│   ├── send_sms.rb
│   └── send_push_notification.rb
└── integrations/
    ├── salla/
    │   └── sync_orders.rb
    └── shipping/
        └── create_label.rb
```

## Naming Convention

```ruby
# Pattern: {Domain}Manager::{Action} or {Domain}Manager::{SubDomain}::{Action}

# Examples:
TasksManager::CreateTask
TasksManager::Bundling::BundleTasks
BillingManager::GenerateInvoice
IntegrationsManager::Salla::SyncOrders
```

## Base Service Class

```ruby
# app/services/application_service.rb
class ApplicationService
  def self.call(...)
    new(...).call
  end

  private

  attr_reader :params

  def initialize(**params)
    @params = params
  end
end
```

## Basic Service Pattern

```ruby
# app/services/tasks_manager/create_task.rb
module TasksManager
  class CreateTask < ApplicationService
    def initialize(account:, merchant:, params:)
      @account = account
      @merchant = merchant
      @params = params
    end

    def call
      validate_params!
      
      ActiveRecord::Base.transaction do
        task = build_task
        assign_zone(task)
        task.save!
        schedule_notifications(task)
        task
      end
    end

    private

    attr_reader :account, :merchant, :params

    def validate_params!
      raise ArgumentError, "Recipient required" unless params[:recipient_id]
      raise ArgumentError, "Address required" unless params[:address]
    end

    def build_task
      account.tasks.build(
        merchant: merchant,
        recipient_id: params[:recipient_id],
        description: params[:description],
        amount: params[:amount],
        status: 'pending'
      )
    end

    def assign_zone(task)
      zone = ZoneFinder.new(account, params[:address]).find
      task.zone = zone
    end

    def schedule_notifications(task)
      TaskNotificationJob.perform_later(task.id)
    end
  end
end

# Usage:
task = TasksManager::CreateTask.call(
  account: current_account,
  merchant: merchant,
  params: task_params
)
```

## Result Object Pattern

For services that need structured success/failure responses:

```ruby
# app/services/service_result.rb
class ServiceResult
  attr_reader :data, :error, :errors

  def initialize(success:, data: nil, error: nil, errors: [])
    @success = success
    @data = data
    @error = error
    @errors = errors
  end

  def success?
    @success
  end

  def failure?
    !@success
  end

  def self.success(data = nil)
    new(success: true, data: data)
  end

  def self.failure(error = nil, errors: [])
    new(success: false, error: error, errors: errors)
  end
end
```

```ruby
# app/services/tasks_manager/assign_carrier.rb
module TasksManager
  class AssignCarrier < ApplicationService
    def initialize(task:, carrier:)
      @task = task
      @carrier = carrier
    end

    def call
      return ServiceResult.failure("Task already assigned") if task.carrier.present?
      return ServiceResult.failure("Carrier not available") unless carrier_available?
      return ServiceResult.failure("Carrier not in zone") unless carrier_in_zone?

      ActiveRecord::Base.transaction do
        task.update!(carrier: carrier, assigned_at: Time.current)
        notify_carrier
        notify_recipient
      end

      ServiceResult.success(task.reload)
    rescue ActiveRecord::RecordInvalid => e
      ServiceResult.failure(e.message, errors: task.errors.full_messages)
    end

    private

    attr_reader :task, :carrier

    def carrier_available?
      carrier.active? && carrier.available?
    end

    def carrier_in_zone?
      return true unless task.zone
      carrier.zones.include?(task.zone)
    end

    def notify_carrier
      CarrierNotificationJob.perform_later(carrier.id, task.id)
    end

    def notify_recipient
      RecipientNotificationJob.perform_later(task.id, :carrier_assigned)
    end
  end
end

# Usage in controller:
result = TasksManager::AssignCarrier.call(task: @task, carrier: @carrier)

if result.success?
  render json: result.data, status: :ok
else
  render json: { error: result.error, errors: result.errors }, status: :unprocessable_entity
end
```

## Dry-Monads Pattern (Alternative)

If using the `dry-monads` gem:

```ruby
# Gemfile
gem 'dry-monads'

# app/services/tasks_manager/complete_task.rb
module TasksManager
  class CompleteTask
    include Dry::Monads[:result, :do]

    def initialize(task:, otp:, photos: [])
      @task = task
      @otp = otp
      @photos = photos
    end

    def call
      yield validate_otp
      yield validate_photos
      yield complete_task
      yield process_payment
      yield notify_parties

      Success(task.reload)
    end

    private

    attr_reader :task, :otp, :photos

    def validate_otp
      return Failure(:invalid_otp) unless task.otp == otp
      Success()
    end

    def validate_photos
      return Failure(:photos_required) if task.requires_photos? && photos.empty?
      Success()
    end

    def complete_task
      task.update!(
        status: 'completed',
        completed_at: Time.current
      )
      Success()
    rescue ActiveRecord::RecordInvalid => e
      Failure(e.message)
    end

    def process_payment
      # Payment processing logic
      Success()
    end

    def notify_parties
      TaskCompletionNotificationJob.perform_later(task.id)
      Success()
    end
  end
end

# Usage:
result = TasksManager::CompleteTask.new(task: @task, otp: params[:otp]).call

case result
in Success(task)
  render json: task
in Failure(:invalid_otp)
  render json: { error: "Invalid OTP" }, status: :unprocessable_entity
in Failure(error)
  render json: { error: error }, status: :unprocessable_entity
end
```

## Service Composition

For complex operations that coordinate multiple services:

```ruby
# app/services/tasks_manager/process_delivery.rb
module TasksManager
  class ProcessDelivery < ApplicationService
    def initialize(task:, carrier:, params:)
      @task = task
      @carrier = carrier
      @params = params
    end

    def call
      ActiveRecord::Base.transaction do
        validate_delivery!
        complete_task!
        process_cod! if task.cod?
        generate_invoice!
        notify_all_parties!
      end

      ServiceResult.success(task.reload)
    rescue StandardError => e
      ServiceResult.failure(e.message)
    end

    private

    attr_reader :task, :carrier, :params

    def validate_delivery!
      result = DeliveryValidator.call(task: task, params: params)
      raise result.error unless result.success?
    end

    def complete_task!
      result = CompleteTask.call(
        task: task,
        otp: params[:otp],
        photos: params[:photos]
      )
      raise result.error unless result.success?
    end

    def process_cod!
      result = BillingManager::ProcessCod.call(
        task: task,
        carrier: carrier,
        amount: task.cod_amount
      )
      raise result.error unless result.success?
    end

    def generate_invoice!
      BillingManager::GenerateInvoice.call(task: task)
    end

    def notify_all_parties!
      NotificationsManager::DeliveryComplete.call(task: task)
    end
  end
end
```

## Service with External API

```ruby
# app/services/integrations/shipping/create_label.rb
module Integrations
  module Shipping
    class CreateLabel < ApplicationService
      TIMEOUT = 30.seconds

      def initialize(task:, shipping_company:)
        @task = task
        @shipping_company = shipping_company
      end

      def call
        response = make_api_request
        
        if response.success?
          label = create_label_record(response.body)
          ServiceResult.success(label)
        else
          handle_error(response)
        end
      rescue Faraday::TimeoutError
        ServiceResult.failure("Shipping API timeout")
      rescue Faraday::ConnectionFailed
        ServiceResult.failure("Unable to connect to shipping API")
      end

      private

      attr_reader :task, :shipping_company

      def make_api_request
        client.post('/labels', label_payload)
      end

      def client
        @client ||= Faraday.new(url: shipping_company.api_url) do |f|
          f.request :json
          f.response :json
          f.options.timeout = TIMEOUT
          f.headers['Authorization'] = "Bearer #{shipping_company.api_key}"
        end
      end

      def label_payload
        {
          sender: sender_details,
          recipient: recipient_details,
          package: package_details
        }
      end

      def create_label_record(response_body)
        task.create_shipping_label!(
          tracking_number: response_body['tracking_number'],
          label_url: response_body['label_url'],
          shipping_company: shipping_company
        )
      end

      def handle_error(response)
        error_message = response.body['error'] || "API Error: #{response.status}"
        Rails.logger.error("Shipping API Error: #{error_message}")
        ServiceResult.failure(error_message)
      end
    end
  end
end
```

## Service with Background Jobs

```ruby
# app/services/tasks_manager/bulk_import.rb
module TasksManager
  class BulkImport < ApplicationService
    def initialize(account:, file:, user:)
      @account = account
      @file = file
      @user = user
    end

    def call
      import = create_import_record
      schedule_processing(import)
      ServiceResult.success(import)
    end

    private

    attr_reader :account, :file, :user

    def create_import_record
      account.task_imports.create!(
        file: file,
        user: user,
        status: 'pending',
        total_rows: count_rows
      )
    end

    def schedule_processing(import)
      BulkImportJob.perform_later(import.id)
    end

    def count_rows
      # Count rows in uploaded file
      CSV.read(file.path).count - 1  # Minus header
    end
  end
end
```

## Testing Services

```ruby
# spec/services/tasks_manager/create_task_spec.rb
require 'rails_helper'

RSpec.describe TasksManager::CreateTask do
  let(:account) { create(:account) }
  let(:merchant) { create(:merchant, account: account) }
  let(:recipient) { create(:recipient, account: account) }
  
  let(:valid_params) do
    {
      recipient_id: recipient.id,
      description: "Test delivery",
      amount: 100,
      address: "123 Test St"
    }
  end

  describe '.call' do
    context 'with valid params' do
      it 'creates a task' do
        expect {
          described_class.call(
            account: account,
            merchant: merchant,
            params: valid_params
          )
        }.to change(Task, :count).by(1)
      end

      it 'assigns the zone' do
        task = described_class.call(
          account: account,
          merchant: merchant,
          params: valid_params
        )
        
        expect(task.zone).to be_present
      end

      it 'schedules notification' do
        expect {
          described_class.call(
            account: account,
            merchant: merchant,
            params: valid_params
          )
        }.to have_enqueued_job(TaskNotificationJob)
      end
    end

    context 'with invalid params' do
      it 'raises error without recipient' do
        invalid_params = valid_params.except(:recipient_id)
        
        expect {
          described_class.call(
            account: account,
            merchant: merchant,
            params: invalid_params
          )
        }.to raise_error(ArgumentError, "Recipient required")
      end
    end
  end
end
```

## Service Interface Guidelines

### Method Visibility

```ruby
class MyService
  # PUBLIC: Only .call is public (entry point)
  def self.call(...)
    new(...).call
  end

  def call
    # Main logic
  end

  private

  # PRIVATE: All other methods are private
  attr_reader :params

  def validate!
    # validation
  end

  def process
    # processing
  end
end
```

### Input Validation

```ruby
def initialize(user:, params:)
  @user = user
  @params = params
  validate_input!
end

private

def validate_input!
  raise ArgumentError, "User required" unless @user
  raise ArgumentError, "Params required" unless @params
end
```

### Transaction Management

```ruby
def call
  ActiveRecord::Base.transaction do
    step_one
    step_two
    step_three
  end
rescue ActiveRecord::RecordInvalid => e
  # Handle validation errors
  ServiceResult.failure(e.message)
rescue StandardError => e
  # Handle other errors
  Rails.logger.error("Service error: #{e.message}")
  ServiceResult.failure("An error occurred")
end
```

## Comprehensive Error Handling

### Custom Error Classes
```ruby
# app/services/errors.rb
module Services
  module Errors
    class ServiceError < StandardError
      attr_reader :context

      def initialize(message = nil, context: {})
        @context = context
        super(message)
      end
    end

    class ValidationError < ServiceError; end
    class AuthorizationError < ServiceError; end
    class ExternalServiceError < ServiceError; end
    class TimeoutError < ServiceError; end
    class RateLimitError < ServiceError; end
    class ResourceNotFoundError < ServiceError; end
  end
end

# Usage in service
module TasksManager
  class CreateTask < ApplicationService
    def call
      validate_authorization!
      validate_params!

      task = build_and_save_task
      ServiceResult.success(task)
    rescue Services::Errors::ValidationError => e
      ServiceResult.failure(e.message, errors: e.context[:errors])
    rescue Services::Errors::AuthorizationError => e
      ServiceResult.failure("Not authorized", context: e.context)
    end

    private

    def validate_authorization!
      unless @user.can?(:create_task, @account)
        raise Services::Errors::AuthorizationError.new(
          "User not authorized to create tasks",
          context: { user_id: @user.id, account_id: @account.id }
        )
      end
    end

    def validate_params!
      errors = []
      errors << "Recipient required" unless @params[:recipient_id]
      errors << "Address required" unless @params[:address]

      if errors.any?
        raise Services::Errors::ValidationError.new(
          "Validation failed",
          context: { errors: errors }
        )
      end
    end
  end
end
```

### Error Handler Concern
```ruby
# app/services/concerns/error_handling.rb
module Services
  module Concerns
    module ErrorHandling
      extend ActiveSupport::Concern

      included do
        rescue_from StandardError, with: :handle_standard_error
        rescue_from ActiveRecord::RecordInvalid, with: :handle_record_invalid
        rescue_from Services::Errors::ServiceError, with: :handle_service_error
      end

      private

      def handle_standard_error(exception)
        log_error(exception)
        track_error(exception)
        ServiceResult.failure("An unexpected error occurred")
      end

      def handle_record_invalid(exception)
        log_error(exception)
        ServiceResult.failure(
          "Validation failed",
          errors: exception.record.errors.full_messages
        )
      end

      def handle_service_error(exception)
        log_error(exception, context: exception.context)
        ServiceResult.failure(exception.message, context: exception.context)
      end

      def log_error(exception, context: {})
        Rails.logger.error({
          error_class: exception.class.name,
          error_message: exception.message,
          backtrace: exception.backtrace.first(5),
          context: context,
          service: self.class.name
        }.to_json)
      end

      def track_error(exception)
        # Integrate with error tracking service (Sentry, Rollbar, etc.)
        if defined?(Sentry)
          Sentry.capture_exception(exception, extra: {
            service: self.class.name,
            params: sanitized_params
          })
        end
      end

      def sanitized_params
        # Remove sensitive data before logging
        @params.except(:password, :token, :api_key)
      end
    end
  end
end

# Usage
module TasksManager
  class CreateTask < ApplicationService
    include Services::Concerns::ErrorHandling

    def call
      # Implementation
    end
  end
end
```

### Retry Mechanisms
```ruby
# app/services/concerns/retriable.rb
module Services
  module Concerns
    module Retriable
      extend ActiveSupport::Concern

      RETRYABLE_ERRORS = [
        Faraday::TimeoutError,
        Faraday::ConnectionFailed,
        Services::Errors::TimeoutError,
        ActiveRecord::Deadlocked
      ].freeze

      def with_retry(max_attempts: 3, backoff: 2, &block)
        attempt = 1

        begin
          yield
        rescue *RETRYABLE_ERRORS => e
          if attempt < max_attempts
            sleep_duration = backoff**attempt
            Rails.logger.warn(
              "Retrying after error (attempt #{attempt}/#{max_attempts}): #{e.message}. " \
              "Sleeping #{sleep_duration}s"
            )
            sleep(sleep_duration)
            attempt += 1
            retry
          else
            Rails.logger.error("Max retry attempts (#{max_attempts}) exceeded: #{e.message}")
            raise
          end
        end
      end
    end
  end
end

# Usage
module Integrations
  module Shipping
    class CreateLabel < ApplicationService
      include Services::Concerns::Retriable

      def call
        with_retry(max_attempts: 3, backoff: 2) do
          response = make_api_request
          process_response(response)
        end
      rescue Faraday::TimeoutError => e
        ServiceResult.failure("Shipping API timeout after retries")
      end
    end
  end
end
```

### Circuit Breaker Pattern
```ruby
# app/services/concerns/circuit_breaker.rb
module Services
  module Concerns
    module CircuitBreaker
      extend ActiveSupport::Concern

      class_methods do
        def circuit_breaker(service_name, failure_threshold: 5, timeout: 60)
          @circuit_state ||= {}
          @circuit_state[service_name] ||= {
            failures: 0,
            last_failure_time: nil,
            state: :closed  # :closed, :open, :half_open
          }
        end

        def circuit_open?(service_name)
          circuit = @circuit_state[service_name]
          return false unless circuit

          if circuit[:state] == :open
            # Check if timeout period has passed
            if Time.current - circuit[:last_failure_time] > circuit[:timeout]
              circuit[:state] = :half_open
              false
            else
              true
            end
          else
            false
          end
        end

        def record_success(service_name)
          circuit = @circuit_state[service_name]
          return unless circuit

          circuit[:failures] = 0
          circuit[:state] = :closed
        end

        def record_failure(service_name)
          circuit = @circuit_state[service_name]
          return unless circuit

          circuit[:failures] += 1
          circuit[:last_failure_time] = Time.current

          if circuit[:failures] >= circuit[:failure_threshold]
            circuit[:state] = :open
            Rails.logger.warn("Circuit breaker opened for #{service_name}")
          end
        end
      end

      def with_circuit_breaker(service_name, &block)
        if self.class.circuit_open?(service_name)
          raise Services::Errors::ExternalServiceError.new(
            "Circuit breaker open for #{service_name}",
            context: { service: service_name }
          )
        end

        result = yield
        self.class.record_success(service_name)
        result
      rescue StandardError => e
        self.class.record_failure(service_name)
        raise
      end
    end
  end
end

# Usage
module Integrations
  module Shipping
    class CreateLabel < ApplicationService
      include Services::Concerns::CircuitBreaker

      circuit_breaker :shipping_api, failure_threshold: 5, timeout: 60

      def call
        with_circuit_breaker(:shipping_api) do
          response = make_api_request
          process_response(response)
        end
      rescue Services::Errors::ExternalServiceError => e
        ServiceResult.failure(e.message)
      end
    end
  end
end
```

## Instrumentation & Monitoring

### Performance Instrumentation
```ruby
# app/services/concerns/instrumentation.rb
module Services
  module Concerns
    module Instrumentation
      extend ActiveSupport::Concern

      included do
        around_action :instrument_service_call, only: :call
      end

      private

      def instrument_service_call
        start_time = Time.current
        service_name = self.class.name.underscore.tr('/', '.')

        ActiveSupport::Notifications.instrument(
          "service.call",
          service: service_name,
          params: sanitized_params
        ) do
          result = yield

          duration = (Time.current - start_time) * 1000  # Convert to ms

          log_performance(service_name, duration, result)
          track_metrics(service_name, duration, result)

          result
        end
      end

      def log_performance(service_name, duration, result)
        Rails.logger.info({
          service: service_name,
          duration_ms: duration.round(2),
          success: result.success?,
          timestamp: Time.current.iso8601
        }.to_json)
      end

      def track_metrics(service_name, duration, result)
        # StatsD integration
        if defined?(StatsD)
          StatsD.increment("service.calls", tags: [
            "service:#{service_name}",
            "status:#{result.success? ? 'success' : 'failure'}"
          ])

          StatsD.timing("service.duration", duration, tags: [
            "service:#{service_name}"
          ])
        end

        # Prometheus integration
        if defined?(PrometheusExporter)
          PrometheusExporter::Client.default.send_json(
            type: "service_call",
            service: service_name,
            duration: duration,
            success: result.success?
          )
        end
      end
    end
  end
end
```

### Structured Logging
```ruby
# app/services/concerns/loggable.rb
module Services
  module Concerns
    module Loggable
      extend ActiveSupport::Concern

      private

      def log_info(message, context = {})
        log(:info, message, context)
      end

      def log_warn(message, context = {})
        log(:warn, message, context)
      end

      def log_error(message, context = {})
        log(:error, message, context)
      end

      def log_debug(message, context = {})
        log(:debug, message, context)
      end

      def log(level, message, context = {})
        Rails.logger.public_send(level, {
          service: self.class.name,
          message: message,
          timestamp: Time.current.iso8601,
          **context
        }.to_json)
      end

      def log_service_start(context = {})
        log_info("Service started", {
          params: sanitized_params,
          **context
        })
      end

      def log_service_complete(result, context = {})
        log_info("Service completed", {
          success: result.success?,
          duration_ms: context[:duration_ms],
          **context
        })
      end

      def log_external_api_call(api_name, endpoint, context = {})
        log_info("External API call", {
          api: api_name,
          endpoint: endpoint,
          **context
        })
      end
    end
  end
end

# Usage
module Integrations
  module Shipping
    class CreateLabel < ApplicationService
      include Services::Concerns::Loggable

      def call
        log_service_start(task_id: @task.id)
        start_time = Time.current

        log_external_api_call("Shipping API", "/labels", {
          task_id: @task.id,
          shipping_company: @shipping_company.name
        })

        response = make_api_request
        result = process_response(response)

        duration = (Time.current - start_time) * 1000
        log_service_complete(result, duration_ms: duration)

        result
      end
    end
  end
end
```

### Metrics Collection
```ruby
# app/services/concerns/metrics.rb
module Services
  module Concerns
    module Metrics
      extend ActiveSupport::Concern

      def track_counter(metric_name, value = 1, tags: {})
        if defined?(StatsD)
          StatsD.increment(
            "service.#{metric_name}",
            value,
            tags: format_tags(tags)
          )
        end
      end

      def track_gauge(metric_name, value, tags: {})
        if defined?(StatsD)
          StatsD.gauge(
            "service.#{metric_name}",
            value,
            tags: format_tags(tags)
          )
        end
      end

      def track_timing(metric_name, duration_ms, tags: {})
        if defined?(StatsD)
          StatsD.timing(
            "service.#{metric_name}",
            duration_ms,
            tags: format_tags(tags)
          )
        end
      end

      def track_histogram(metric_name, value, tags: {})
        if defined?(StatsD)
          StatsD.histogram(
            "service.#{metric_name}",
            value,
            tags: format_tags(tags)
          )
        end
      end

      private

      def format_tags(tags)
        default_tags.merge(tags).map { |k, v| "#{k}:#{v}" }
      end

      def default_tags
        {
          service: self.class.name.underscore.tr('/', '.'),
          environment: Rails.env
        }
      end
    end
  end
end

# Usage
module TasksManager
  class CreateTask < ApplicationService
    include Services::Concerns::Metrics

    def call
      start_time = Time.current

      task = build_and_save_task
      track_counter("task.created", tags: { merchant_id: @merchant.id })

      duration = (Time.current - start_time) * 1000
      track_timing("task.creation_time", duration)

      ServiceResult.success(task)
    end
  end
end
```

### ActiveSupport Notifications
```ruby
# app/services/tasks_manager/create_task.rb
module TasksManager
  class CreateTask < ApplicationService
    def call
      ActiveSupport::Notifications.instrument(
        "task.create",
        account_id: @account.id,
        merchant_id: @merchant.id
      ) do |payload|
        task = build_and_save_task

        payload[:task_id] = task.id
        payload[:zone_id] = task.zone_id

        ServiceResult.success(task)
      end
    end
  end
end

# config/initializers/service_notifications.rb
ActiveSupport::Notifications.subscribe("task.create") do |name, start, finish, id, payload|
  duration = (finish - start) * 1000

  Rails.logger.info({
    event: name,
    duration_ms: duration.round(2),
    account_id: payload[:account_id],
    task_id: payload[:task_id]
  }.to_json)

  # Send metrics
  StatsD.increment("task.created", tags: [
    "account:#{payload[:account_id]}",
    "merchant:#{payload[:merchant_id]}"
  ]) if defined?(StatsD)

  StatsD.timing("task.creation_duration", duration, tags: [
    "account:#{payload[:account_id]}"
  ]) if defined?(StatsD)
end
```

### Error Tracking Integration
```ruby
# app/services/concerns/error_tracking.rb
module Services
  module Concerns
    module ErrorTracking
      extend ActiveSupport::Concern

      private

      def capture_exception(exception, context: {})
        # Sentry integration
        if defined?(Sentry)
          Sentry.capture_exception(exception, extra: {
            service: self.class.name,
            context: context,
            params: sanitized_params
          })
        end

        # Rollbar integration
        if defined?(Rollbar)
          Rollbar.error(exception, {
            service: self.class.name,
            context: context,
            params: sanitized_params
          })
        end

        # Airbrake integration
        if defined?(Airbrake)
          Airbrake.notify(exception, {
            service: self.class.name,
            context: context,
            params: sanitized_params
          })
        end
      end

      def capture_message(message, level: :info, context: {})
        if defined?(Sentry)
          Sentry.capture_message(message, level: level, extra: {
            service: self.class.name,
            context: context
          })
        end
      end
    end
  end
end

# Usage
module TasksManager
  class CreateTask < ApplicationService
    include Services::Concerns::ErrorTracking

    def call
      task = build_and_save_task
      ServiceResult.success(task)
    rescue StandardError => e
      capture_exception(e, context: {
        account_id: @account.id,
        merchant_id: @merchant.id,
        params: @params
      })
      ServiceResult.failure("Failed to create task")
    end
  end
end
```

### Comprehensive Service Template
```ruby
# app/services/tasks_manager/create_task.rb
module TasksManager
  class CreateTask < ApplicationService
    include Services::Concerns::ErrorHandling
    include Services::Concerns::Retriable
    include Services::Concerns::Instrumentation
    include Services::Concerns::Loggable
    include Services::Concerns::Metrics
    include Services::Concerns::ErrorTracking

    def initialize(account:, merchant:, params:, user:)
      @account = account
      @merchant = merchant
      @params = params
      @user = user
    end

    def call
      log_service_start(account_id: @account.id, merchant_id: @merchant.id)
      start_time = Time.current

      validate_authorization!
      validate_params!

      task = with_retry(max_attempts: 3) do
        build_and_save_task
      end

      track_counter("task.created", tags: { merchant_id: @merchant.id })
      duration = (Time.current - start_time) * 1000
      track_timing("task.creation_time", duration)

      log_service_complete(ServiceResult.success(task), duration_ms: duration)

      ServiceResult.success(task)
    rescue Services::Errors::ServiceError => e
      capture_exception(e, context: { account_id: @account.id })
      ServiceResult.failure(e.message, context: e.context)
    rescue StandardError => e
      log_error("Unexpected error", error: e.message, backtrace: e.backtrace.first(5))
      capture_exception(e, context: { account_id: @account.id })
      ServiceResult.failure("An unexpected error occurred")
    end

    private

    attr_reader :account, :merchant, :params, :user

    def validate_authorization!
      unless user.can?(:create_task, account)
        raise Services::Errors::AuthorizationError.new(
          "User not authorized",
          context: { user_id: user.id, account_id: account.id }
        )
      end
    end

    def validate_params!
      errors = []
      errors << "Recipient required" unless params[:recipient_id]
      errors << "Address required" unless params[:address]

      if errors.any?
        raise Services::Errors::ValidationError.new(
          "Validation failed",
          context: { errors: errors }
        )
      end
    end

    def build_and_save_task
      ActiveRecord::Base.transaction do
        task = account.tasks.build(
          merchant: merchant,
          recipient_id: params[:recipient_id],
          description: params[:description],
          amount: params[:amount],
          status: 'pending'
        )

        assign_zone(task)
        task.save!

        log_info("Task created", task_id: task.id)
        schedule_notifications(task)

        task
      end
    end

    def assign_zone(task)
      zone = ZoneFinder.new(account, params[:address]).find
      task.zone = zone
      log_debug("Zone assigned", zone_id: zone&.id)
    end

    def schedule_notifications(task)
      TaskNotificationJob.perform_later(task.id)
      log_debug("Notifications scheduled", task_id: task.id)
    end
  end
end
```

## Pre-Creation Checklist

Before creating a service:

```bash
# 1. Check existing service structure
ls app/services/
ls app/services/*/ 2>/dev/null

# 2. Review existing service patterns
head -50 $(find app/services -name '*.rb' | head -1)

# 3. Check naming conventions
grep -r 'class.*Manager' app/services/ --include='*.rb' | head -10

# 4. Verify namespace exists
ls app/services/{namespace}/ 2>/dev/null

# 5. Check for existing concerns
ls app/services/concerns/ 2>/dev/null

# 6. Review error handling patterns
grep -r 'ServiceError' app/services/ --include='*.rb' | head -5
```
