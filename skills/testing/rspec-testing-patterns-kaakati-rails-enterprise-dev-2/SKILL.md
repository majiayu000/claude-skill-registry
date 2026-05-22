---
name: "RSpec Testing Patterns"
description: "Complete guide to testing Ruby on Rails applications with RSpec. Use this skill when writing unit tests, integration tests, system tests, or when setting up test infrastructure including factories, shared examples, and mocking strategies."
---

# RSpec Testing Patterns Skill

This skill provides comprehensive guidance for testing Rails applications with RSpec.

## When to Use This Skill

- Writing new specs (unit, integration, system)
- Setting up test factories
- Creating shared examples
- Mocking external services
- Testing ViewComponents
- Testing background jobs

## Directory Structure

```
spec/
├── rails_helper.rb
├── spec_helper.rb
├── support/
│   ├── factory_bot.rb
│   ├── database_cleaner.rb
│   ├── shared_contexts/
│   └── shared_examples/
├── factories/
│   ├── tasks.rb
│   ├── users.rb
│   └── ...
├── models/
├── services/
├── controllers/
├── requests/
├── system/
├── components/
└── jobs/
```

## Basic Spec Structure

```ruby
# spec/models/task_spec.rb
require 'rails_helper'

RSpec.describe Task, type: :model do
  describe 'associations' do
    it { is_expected.to belong_to(:account) }
    it { is_expected.to belong_to(:merchant) }
    it { is_expected.to have_many(:timelines) }
  end

  describe 'validations' do
    it { is_expected.to validate_presence_of(:status) }
    it { is_expected.to validate_inclusion_of(:status).in_array(Task::STATUSES) }
  end

  describe 'scopes' do
    describe '.active' do
      let!(:pending_task) { create(:task, status: 'pending') }
      let!(:completed_task) { create(:task, status: 'completed') }

      it 'returns only non-completed tasks' do
        expect(Task.active).to include(pending_task)
        expect(Task.active).not_to include(completed_task)
      end
    end
  end

  describe '#completable?' do
    context 'when task is pending' do
      let(:task) { build(:task, status: 'pending') }

      it 'returns true' do
        expect(task.completable?).to be true
      end
    end

    context 'when task is completed' do
      let(:task) { build(:task, status: 'completed') }

      it 'returns false' do
        expect(task.completable?).to be false
      end
    end
  end
end
```

## Factories (FactoryBot)

### Basic Factory

```ruby
# spec/factories/tasks.rb
FactoryBot.define do
  factory :task do
    account
    merchant
    recipient

    sequence(:tracking_number) { |n| "TRK#{n.to_s.rjust(8, '0')}" }
    status { 'pending' }
    description { Faker::Lorem.sentence }
    amount { Faker::Number.decimal(l_digits: 2, r_digits: 2) }

    # Traits
    trait :completed do
      status { 'completed' }
      completed_at { Time.current }
      carrier
    end

    trait :with_carrier do
      carrier
    end

    trait :express do
      task_type { 'express' }
    end

    trait :next_day do
      task_type { 'next_day' }
    end

    trait :with_photos do
      after(:create) do |task|
        create_list(:photo, 2, task: task)
      end
    end

    # Callbacks
    after(:create) do |task|
      task.timelines.create!(status: task.status, created_at: task.created_at)
    end
  end
end
```

### Factory with Associations

```ruby
# spec/factories/accounts.rb
FactoryBot.define do
  factory :account do
    sequence(:name) { |n| "Account #{n}" }
    subdomain { name.parameterize }
    active { true }
  end
end

# spec/factories/merchants.rb
FactoryBot.define do
  factory :merchant do
    account
    sequence(:name) { |n| "Merchant #{n}" }
    email { Faker::Internet.email }

    trait :with_branches do
      after(:create) do |merchant|
        create_list(:branch, 2, merchant: merchant)
      end
    end
  end
end
```

### Transient Attributes

```ruby
FactoryBot.define do
  factory :bundle do
    account
    carrier

    transient do
      task_count { 5 }
    end

    after(:create) do |bundle, evaluator|
      create_list(:task, evaluator.task_count, bundle: bundle, account: bundle.account)
    end
  end
end

# Usage
create(:bundle, task_count: 10)
```

## Service Specs

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
      amount: 100.00,
      address: "123 Test St"
    }
  end

  describe '.call' do
    subject(:service_call) do
      described_class.call(
        account: account,
        merchant: merchant,
        params: valid_params
      )
    end

    context 'with valid params' do
      it 'creates a task' do
        expect { service_call }.to change(Task, :count).by(1)
      end

      it 'returns the created task' do
        expect(service_call).to be_a(Task)
        expect(service_call).to be_persisted
      end

      it 'associates with correct account' do
        expect(service_call.account).to eq(account)
      end

      it 'schedules notification job' do
        expect { service_call }
          .to have_enqueued_job(TaskNotificationJob)
                .with(kind_of(Integer))
      end
    end

    context 'with invalid params' do
      context 'when recipient is missing' do
        let(:valid_params) { super().except(:recipient_id) }

        it 'raises ArgumentError' do
          expect { service_call }.to raise_error(ArgumentError, /Recipient required/)
        end
      end

      context 'when address is missing' do
        let(:valid_params) { super().except(:address) }

        it 'raises ArgumentError' do
          expect { service_call }.to raise_error(ArgumentError, /Address required/)
        end
      end
    end

    context 'with service result pattern' do
      # For services returning ServiceResult
      subject(:result) { described_class.call(...) }

      context 'on success' do
        it 'returns success result' do
          expect(result).to be_success
        end

        it 'includes the task in data' do
          expect(result.data).to be_a(Task)
        end
      end

      context 'on failure' do
        it 'returns failure result' do
          expect(result).to be_failure
        end

        it 'includes error message' do
          expect(result.error).to eq("Expected error message")
        end
      end
    end
  end
end
```

## Request Specs

```ruby
# spec/requests/api/v1/tasks_spec.rb
require 'rails_helper'

RSpec.describe "Api::V1::Tasks", type: :request do
  let(:account) { create(:account) }
  let(:user) { create(:user, account: account) }
  let(:headers) { auth_headers(user) }

  describe "GET /api/v1/tasks" do
    let!(:tasks) { create_list(:task, 3, account: account) }
    let!(:other_task) { create(:task) }  # Different account

    before { get api_v1_tasks_path, headers: headers }

    it "returns success" do
      expect(response).to have_http_status(:ok)
    end

    it "returns tasks for current account only" do
      expect(json_response['data'].size).to eq(3)
    end

    it "does not include other account tasks" do
      ids = json_response['data'].pluck('id')
      expect(ids).not_to include(other_task.id)
    end
  end

  describe "POST /api/v1/tasks" do
    let(:merchant) { create(:merchant, account: account) }
    let(:recipient) { create(:recipient, account: account) }

    let(:valid_params) do
      {
        task: {
          merchant_id: merchant.id,
          recipient_id: recipient.id,
          description: "New task",
          amount: 50.00
        }
      }
    end

    context "with valid params" do
      it "creates a task" do
        expect {
          post api_v1_tasks_path, params: valid_params, headers: headers
        }.to change(Task, :count).by(1)
      end

      it "returns created status" do
        post api_v1_tasks_path, params: valid_params, headers: headers
        expect(response).to have_http_status(:created)
      end
    end

    context "with invalid params" do
      let(:invalid_params) { { task: { description: "" } } }

      it "returns unprocessable entity" do
        post api_v1_tasks_path, params: invalid_params, headers: headers
        expect(response).to have_http_status(:unprocessable_entity)
      end

      it "returns errors" do
        post api_v1_tasks_path, params: invalid_params, headers: headers
        expect(json_response['errors']).to be_present
      end
    end
  end

  # Helper for JSON response
  def json_response
    JSON.parse(response.body)
  end
end
```

## ViewComponent Specs

```ruby
# spec/components/metrics/kpi_card_component_spec.rb
require 'rails_helper'

RSpec.describe Metrics::KpiCardComponent, type: :component do
  let(:title) { "Total Orders" }
  let(:value) { 1234 }

  subject(:component) do
    described_class.new(title: title, value: value)
  end

  describe "#render" do
    before { render_inline(component) }

    it "renders the title" do
      expect(page).to have_css("h3", text: title)
    end

    it "renders the value" do
      expect(page).to have_text("1,234")
    end
  end

  describe "#formatted_value" do
    it "formats large numbers with delimiter" do
      component = described_class.new(title: "Test", value: 1234567)
      expect(component.formatted_value).to eq("1,234,567")
    end
  end

  context "with trend" do
    let(:component) do
      described_class.new(title: title, value: value, trend: :up)
    end

    before { render_inline(component) }

    it "shows trend indicator" do
      expect(page).to have_css(".text-green-500")
    end
  end

  context "with content block" do
    before do
      render_inline(component) do
        "Additional content"
      end
    end

    it "renders the block content" do
      expect(page).to have_text("Additional content")
    end
  end
end
```

## System Specs (Capybara)

```ruby
# spec/system/tasks_spec.rb
require 'rails_helper'

RSpec.describe "Tasks", type: :system do
  let(:account) { create(:account) }
  let(:user) { create(:user, account: account) }

  before do
    sign_in(user)
  end

  describe "viewing tasks" do
    let!(:tasks) { create_list(:task, 5, account: account) }

    it "displays all tasks" do
      visit tasks_path

      tasks.each do |task|
        expect(page).to have_content(task.tracking_number)
      end
    end
  end

  describe "creating a task" do
    let!(:merchant) { create(:merchant, account: account) }
    let!(:recipient) { create(:recipient, account: account) }

    it "creates a new task" do
      visit new_task_path

      select merchant.name, from: "Merchant"
      select recipient.name, from: "Recipient"
      fill_in "Description", with: "Test delivery"
      fill_in "Amount", with: "100.00"

      click_button "Create Task"

      expect(page).to have_content("Task created successfully")
      expect(page).to have_content("Test delivery")
    end
  end

  describe "with Turbo" do
    it "updates task status via Turbo Stream" do
      task = create(:task, account: account, status: 'pending')

      visit tasks_path

      within("#task_#{task.id}") do
        click_button "Start"
      end

      # Wait for Turbo Stream update
      expect(page).to have_css("#task_#{task.id} .status", text: "In Progress")
    end
  end
end
```

## Job Specs

```ruby
# spec/jobs/task_notification_job_spec.rb
require 'rails_helper'

RSpec.describe TaskNotificationJob, type: :job do
  let(:task) { create(:task) }

  describe "#perform" do
    it "sends SMS notification" do
      expect(SmsService).to receive(:send).with(
        to: task.recipient.phone,
        message: include(task.tracking_number)
      )

      described_class.perform_now(task.id)
    end

    context "when task doesn't exist" do
      it "handles gracefully" do
        expect { described_class.perform_now(0) }.not_to raise_error
      end
    end
  end

  describe "enqueuing" do
    it "enqueues in correct queue" do
      expect {
        described_class.perform_later(task.id)
      }.to have_enqueued_job.on_queue("notifications")
    end
  end
end
```

## Shared Examples

```ruby
# spec/support/shared_examples/tenant_scoped.rb
RSpec.shared_examples "tenant scoped" do
  describe "tenant scoping" do
    let(:account) { create(:account) }
    let(:other_account) { create(:account) }

    let!(:scoped_record) { create(described_class.model_name.singular, account: account) }
    let!(:other_record) { create(described_class.model_name.singular, account: other_account) }

    it "scopes to current account" do
      Current.account = account
      expect(described_class.all).to include(scoped_record)
      expect(described_class.all).not_to include(other_record)
    end
  end
end

# Usage
RSpec.describe Task do
  it_behaves_like "tenant scoped"
end
```

```ruby
# spec/support/shared_examples/api_authentication.rb
RSpec.shared_examples "requires authentication" do
  context "without authentication" do
    let(:headers) { {} }

    it "returns unauthorized" do
      make_request
      expect(response).to have_http_status(:unauthorized)
    end
  end
end

# Usage
RSpec.describe "Api::V1::Tasks" do
  describe "GET /api/v1/tasks" do
    it_behaves_like "requires authentication" do
      let(:make_request) { get api_v1_tasks_path, headers: headers }
    end
  end
end
```

## Shared Contexts

```ruby
# spec/support/shared_contexts/authenticated_user.rb
RSpec.shared_context "authenticated user" do
  let(:account) { create(:account) }
  let(:user) { create(:user, account: account) }

  before do
    sign_in(user)
    Current.account = account
  end
end

# Usage
RSpec.describe TasksController do
  include_context "authenticated user"

  # tests with authenticated user...
end
```

## Mocking External Services

```ruby
# spec/support/webmock_helpers.rb
module WebmockHelpers
  def stub_shipping_api_success
    stub_request(:post, "https://shipping.example.com/api/labels")
      .to_return(
        status: 200,
        body: { tracking_number: "SHIP123", label_url: "https://..." }.to_json,
        headers: { 'Content-Type' => 'application/json' }
      )
  end

  def stub_shipping_api_failure
    stub_request(:post, "https://shipping.example.com/api/labels")
      .to_return(status: 500, body: { error: "Server error" }.to_json)
  end
end

RSpec.configure do |config|
  config.include WebmockHelpers
end

# Usage in spec
describe "creating shipping label" do
  before { stub_shipping_api_success }

  it "creates label successfully" do
    # test...
  end
end
```

## Test Helpers

```ruby
# spec/support/helpers/auth_helpers.rb
module AuthHelpers
  def auth_headers(user)
    token = user.generate_jwt_token
    { 'Authorization' => "Bearer #{token}" }
  end

  def sign_in(user)
    login_as(user, scope: :user)
  end
end

RSpec.configure do |config|
  config.include AuthHelpers, type: :request
  config.include AuthHelpers, type: :system
end
```

## API Testing Comprehensive Patterns

### Request Specs for REST APIs

```ruby
# spec/requests/api/v1/posts_spec.rb
require 'rails_helper'

RSpec.describe 'API V1 Posts', type: :request do
  let(:user) { create(:user) }
  let(:token) { JsonWebTokenService.encode(user_id: user.id) }
  let(:auth_headers) { { 'Authorization' => "Bearer #{token}", 'Content-Type' => 'application/json' } }

  describe 'GET /api/v1/posts' do
    context 'with valid authentication' do
      before do
        create_list(:post, 3, :published)
        create(:post, :draft)
      end

      it 'returns published posts' do
        get '/api/v1/posts', headers: auth_headers

        expect(response).to have_http_status(:ok)
        expect(json_response['posts'].size).to eq(3)
      end

      it 'includes pagination metadata' do
        create_list(:post, 30, :published)

        get '/api/v1/posts', params: { page: 2, per_page: 10 }, headers: auth_headers

        expect(json_response['meta']).to include(
          'current_page' => 2,
          'total_pages' => 3,
          'total_count' => 30,
          'per_page' => 10
        )
      end

      it 'filters by status' do
        create_list(:post, 2, status: 'published')
        create_list(:post, 3, status: 'draft')

        get '/api/v1/posts', params: { status: 'draft' }, headers: auth_headers

        expect(json_response['posts'].size).to eq(3)
      end
    end

    context 'without authentication' do
      it 'returns 401 unauthorized' do
        get '/api/v1/posts'

        expect(response).to have_http_status(:unauthorized)
        expect(json_response['error']).to eq('Unauthorized')
      end
    end

    context 'with invalid token' do
      it 'returns 401 unauthorized' do
        get '/api/v1/posts', headers: { 'Authorization' => 'Bearer invalid' }

        expect(response).to have_http_status(:unauthorized)
      end
    end
  end

  describe 'POST /api/v1/posts' do
    let(:valid_params) do
      {
        post: {
          title: 'Test Post',
          body: 'Test body content',
          published_at: Time.current
        }
      }
    end

    context 'with valid parameters' do
      it 'creates a post' do
        expect {
          post '/api/v1/posts', params: valid_params.to_json, headers: auth_headers
        }.to change(Post, :count).by(1)

        expect(response).to have_http_status(:created)
        expect(json_response['title']).to eq('Test Post')
        expect(response.headers['Location']).to be_present
      end

      it 'returns serialized post' do
        post '/api/v1/posts', params: valid_params.to_json, headers: auth_headers

        expect(json_response).to include(
          'id',
          'title',
          'body',
          'published_at'
        )
        expect(json_response).not_to include('password', 'internal_notes')
      end
    end

    context 'with invalid parameters' do
      let(:invalid_params) { { post: { title: '' } } }

      it 'returns validation errors' do
        post '/api/v1/posts', params: invalid_params.to_json, headers: auth_headers

        expect(response).to have_http_status(:unprocessable_entity)
        expect(json_response['error']['errors']).to have_key('title')
        expect(json_response['error']['errors']['title']).to include("can't be blank")
      end

      it 'does not create post' do
        expect {
          post '/api/v1/posts', params: invalid_params.to_json, headers: auth_headers
        }.not_to change(Post, :count)
      end
    end
  end

  describe 'PATCH /api/v1/posts/:id' do
    let(:post_record) { create(:post, author: user) }
    let(:update_params) { { post: { title: 'Updated Title' } } }

    context 'when user is post author' do
      it 'updates the post' do
        patch "/api/v1/posts/#{post_record.id}",
              params: update_params.to_json,
              headers: auth_headers

        expect(response).to have_http_status(:ok)
        expect(post_record.reload.title).to eq('Updated Title')
      end
    end

    context 'when user is not post author' do
      let(:other_post) { create(:post) }

      it 'returns 403 forbidden' do
        patch "/api/v1/posts/#{other_post.id}",
              params: update_params.to_json,
              headers: auth_headers

        expect(response).to have_http_status(:forbidden)
        expect(json_response['error']).to eq('Forbidden')
      end
    end

    context 'when post does not exist' do
      it 'returns 404 not found' do
        patch '/api/v1/posts/99999',
              params: update_params.to_json,
              headers: auth_headers

        expect(response).to have_http_status(:not_found)
      end
    end
  end

  describe 'DELETE /api/v1/posts/:id' do
    let(:post_record) { create(:post, author: user) }

    it 'deletes the post' do
      delete "/api/v1/posts/#{post_record.id}", headers: auth_headers

      expect(response).to have_http_status(:no_content)
      expect(response.body).to be_empty
      expect(Post.exists?(post_record.id)).to be false
    end
  end

  # Helper method for parsing JSON responses
  def json_response
    JSON.parse(response.body)
  end
end
```

### Testing Rate Limiting

```ruby
# spec/requests/api/rate_limiting_spec.rb
require 'rails_helper'

RSpec.describe 'API Rate Limiting', type: :request do
  let(:user) { create(:user) }
  let(:token) { JsonWebTokenService.encode(user_id: user.id) }
  let(:auth_headers) { { 'Authorization' => "Bearer #{token}" } }

  before do
    # Use Rack::Attack test mode
    Rack::Attack.cache.store = ActiveSupport::Cache::MemoryStore.new
    Rack::Attack.enabled = true
  end

  after do
    Rack::Attack.cache.store.clear
  end

  it 'allows requests within limit' do
    5.times do
      get '/api/v1/posts', headers: auth_headers
      expect(response).to have_http_status(:ok)
    end
  end

  it 'throttles requests exceeding limit' do
    # Assuming limit is 10 requests per minute
    11.times do |i|
      get '/api/v1/posts', headers: auth_headers
    end

    expect(response).to have_http_status(:too_many_requests)
    expect(response.headers['Retry-After']).to be_present
  end
end
```

### Testing API Versioning

```ruby
# spec/requests/api/versioning_spec.rb
require 'rails_helper'

RSpec.describe 'API Versioning', type: :request do
  let(:user) { create(:user) }
  let(:token) { JsonWebTokenService.encode(user_id: user.id) }

  describe 'v1 endpoint' do
    it 'returns v1 response format' do
      get '/api/v1/posts', headers: { 'Authorization' => "Bearer #{token}" }

      expect(json_response).to have_key('posts')
      expect(json_response).to have_key('meta')
    end
  end

  describe 'v2 endpoint' do
    it 'returns v2 response format' do
      get '/api/v2/posts', headers: { 'Authorization' => "Bearer #{token}" }

      # v2 might have different structure
      expect(json_response).to have_key('data')
      expect(json_response).to have_key('pagination')
    end
  end

  describe 'header-based versioning' do
    it 'uses v2 with accept header' do
      get '/api/posts',
          headers: {
            'Authorization' => "Bearer #{token}",
            'Accept' => 'application/vnd.myapp.v2+json'
          }

      expect(response).to have_http_status(:ok)
    end
  end
end
```

### Shared Examples for API Responses

```ruby
# spec/support/shared_examples/api_responses.rb
RSpec.shared_examples 'requires authentication' do |method, path|
  it 'returns 401 without token' do
    send(method, path)
    expect(response).to have_http_status(:unauthorized)
  end

  it 'returns 401 with invalid token' do
    send(method, path, headers: { 'Authorization' => 'Bearer invalid' })
    expect(response).to have_http_status(:unauthorized)
  end
end

RSpec.shared_examples 'paginates results' do
  it 'includes pagination metadata' do
    make_request

    expect(json_response['meta']).to include(
      'current_page',
      'total_pages',
      'total_count',
      'per_page'
    )
  end

  it 'respects per_page parameter' do
    make_request(per_page: 5)

    expect(json_response['meta']['per_page']).to eq(5)
    expect(json_response[collection_key].size).to be <= 5
  end
end

RSpec.shared_examples 'returns JSON API format' do
  it 'sets correct content type' do
    make_request
    expect(response.content_type).to include('application/json')
  end

  it 'returns valid JSON' do
    make_request
    expect { JSON.parse(response.body) }.not_to raise_error
  end
end

# Usage
describe 'GET /api/v1/posts' do
  def make_request(params = {})
    get '/api/v1/posts', params: params, headers: auth_headers
  end

  let(:collection_key) { 'posts' }

  it_behaves_like 'requires authentication', :get, '/api/v1/posts'
  it_behaves_like 'paginates results'
  it_behaves_like 'returns JSON API format'
end
```

## Hotwire Testing Patterns

### System Tests for Turbo

```ruby
# spec/system/turbo_posts_spec.rb
require 'rails_helper'

RSpec.describe 'Turbo Posts', type: :system do
  before do
    driven_by(:selenium_chrome_headless)
  end

  describe 'creating a post with Turbo' do
    it 'creates post without full page reload' do
      visit posts_path

      within '#new_post' do
        fill_in 'Title', with: 'My Turbo Post'
        fill_in 'Body', with: 'Content here'
        click_button 'Create Post'
      end

      # Post appears without page reload
      expect(page).to have_content('My Turbo Post')
      expect(page).to have_current_path(posts_path) # No redirect

      # Form is reset
      expect(find_field('Title').value).to be_blank
    end

    it 'displays validation errors inline' do
      visit posts_path

      within '#new_post' do
        fill_in 'Title', with: ''
        click_button 'Create Post'
      end

      # Error displayed without reload
      within '#new_post' do
        expect(page).to have_content("can't be blank")
      end
    end
  end

  describe 'updating post with Turbo Frame' do
    let!(:post) { create(:post, title: 'Original Title') }

    it 'updates post inline' do
      visit posts_path

      within "##{dom_id(post)}" do
        click_link 'Edit'

        # Edit form loads in frame
        fill_in 'Title', with: 'Updated Title'
        click_button 'Update'

        # Updated content shows in place
        expect(page).to have_content('Updated Title')
        expect(page).not_to have_field('Title') # No longer editing
      end

      # Rest of page unchanged
      expect(page).to have_current_path(posts_path)
    end
  end

  describe 'deleting post with Turbo Stream' do
    let!(:post) { create(:post, title: 'To Delete') }

    it 'removes post from list' do
      visit posts_path

      within "##{dom_id(post)}" do
        accept_confirm do
          click_button 'Delete'
        end
      end

      # Post removed without page reload
      expect(page).not_to have_content('To Delete')
      expect(page).to have_current_path(posts_path)
    end
  end

  describe 'real-time updates with Turbo Streams' do
    it 'shows new posts from other users', :js do
      visit posts_path

      # Simulate another user creating a post
      perform_enqueued_jobs do
        create(:post, title: 'Real-time Post')
      end

      # New post appears automatically
      expect(page).to have_content('Real-time Post')
    end
  end
end
```

### Testing Turbo Frames

```ruby
# spec/system/turbo_frames_spec.rb
require 'rails_helper'

RSpec.describe 'Turbo Frames', type: :system do
  before do
    driven_by(:selenium_chrome_headless)
  end

  describe 'lazy loading frames' do
    let!(:post) { create(:post) }

    it 'loads frame content when visible' do
      visit post_path(post)

      # Frame starts with loading message
      within 'turbo-frame#comments' do
        expect(page).to have_content('Loading comments...')
      end

      # Wait for lazy load
      sleep 0.5

      # Comments loaded
      within 'turbo-frame#comments' do
        expect(page).not_to have_content('Loading comments...')
        expect(page).to have_selector('.comment', count: post.comments.count)
      end
    end
  end

  describe 'frame navigation' do
    let!(:post) { create(:post) }

    it 'navigates within frame boundary' do
      visit posts_path

      # Click link that targets frame
      within 'turbo-frame#sidebar' do
        click_link 'Categories'

        # Only frame content changes
        expect(page).to have_content('All Categories')
      end

      # Main content unchanged
      expect(page).to have_current_path(posts_path)
    end

    it 'breaks out of frame with data-turbo-frame="_top"' do
      visit posts_path

      within 'turbo-frame#sidebar' do
        click_link 'View All Posts', data: { turbo_frame: '_top' }
      end

      # Full page navigation occurred
      expect(page).to have_current_path(posts_path)
    end
  end
end
```

### Testing Stimulus Controllers

```ruby
# spec/javascript/controllers/search_controller_spec.js
import { Application } from "@hotwired/stimulus"
import SearchController from "controllers/search_controller"

describe("SearchController", () => {
  let application
  let controller

  beforeEach(() => {
    document.body.innerHTML = `
      <div data-controller="search">
        <input data-search-target="input" type="text">
        <div data-search-target="results"></div>
        <span data-search-target="count"></span>
      </div>
    `

    application = Application.start()
    application.register("search", SearchController)
    controller = application.getControllerForElementAndIdentifier(
      document.querySelector('[data-controller="search"]'),
      "search"
    )
  })

  afterEach(() => {
    application.stop()
  })

  describe("#connect", () => {
    it("initializes with empty results", () => {
      expect(controller.resultsTarget.innerHTML).toBe("")
    })
  })

  describe("#search", () => {
    it("performs search with query", async () => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          text: () => Promise.resolve("<div class='result'>Result 1</div>")
        })
      )

      controller.inputTarget.value = "test query"
      await controller.search()

      expect(global.fetch).toHaveBeenCalledWith("/search?q=test query")
      expect(controller.resultsTarget.innerHTML).toContain("Result 1")
    })

    it("updates count", async () => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          text: () => Promise.resolve("<div>1</div><div>2</div>")
        })
      )

      controller.inputTarget.value = "test"
      await controller.search()

      expect(controller.countTarget.textContent).toBe("2")
    })
  })

  describe("#clear", () => {
    it("clears input and results", () => {
      controller.inputTarget.value = "test"
      controller.resultsTarget.innerHTML = "<div>Results</div>"

      controller.clear()

      expect(controller.inputTarget.value).toBe("")
      expect(controller.resultsTarget.innerHTML).toBe("")
    })
  })
})
```

### Testing Turbo Streams in Request Specs

```ruby
# spec/requests/turbo_streams_spec.rb
require 'rails_helper'

RSpec.describe 'Turbo Streams', type: :request do
  let(:user) { create(:user) }

  before { sign_in user }

  describe 'POST /posts' do
    let(:valid_params) { { post: { title: 'Test', body: 'Content' } } }

    it 'returns turbo stream response' do
      post posts_path, params: valid_params, as: :turbo_stream

      expect(response.media_type).to eq('text/vnd.turbo-stream.html')
      expect(response.body).to include('turbo-stream')
    end

    it 'prepends new post' do
      post posts_path, params: valid_params, as: :turbo_stream

      expect(response.body).to include('action="prepend"')
      expect(response.body).to include('target="posts"')
      expect(response.body).to include('Test')
    end

    it 'resets form' do
      post posts_path, params: valid_params, as: :turbo_stream

      # Check for form reset stream
      expect(response.body).to include('action="replace"')
      expect(response.body).to include('target="post_form"')
    end

    context 'with validation errors' do
      let(:invalid_params) { { post: { title: '' } } }

      it 'returns unprocessable entity status' do
        post posts_path, params: invalid_params, as: :turbo_stream

        expect(response).to have_http_status(:unprocessable_entity)
      end

      it 'replaces form with errors' do
        post posts_path, params: invalid_params, as: :turbo_stream

        expect(response.body).to include('action="replace"')
        expect(response.body).to include("can't be blank")
      end
    end
  end

  describe 'DELETE /posts/:id' do
    let!(:post) { create(:post, author: user) }

    it 'removes post via turbo stream' do
      delete post_path(post), as: :turbo_stream

      expect(response.body).to include('action="remove"')
      expect(response.body).to include(dom_id(post))
    end
  end
end
```

### Integration with Capybara Helpers

```ruby
# spec/support/turbo_helpers.rb
module TurboHelpers
  def expect_turbo_stream(action:, target:)
    expect(page).to have_selector(
      "turbo-stream[action='#{action}'][target='#{target}']",
      visible: false
    )
  end

  def wait_for_turbo_frame(id, timeout: 5)
    expect(page).to have_selector("turbo-frame##{id}[complete]", wait: timeout)
  end

  def within_turbo_frame(id, &block)
    within("turbo-frame##{id}", &block)
  end
end

RSpec.configure do |config|
  config.include TurboHelpers, type: :system
end

# Usage
it 'loads comments in frame' do
  visit post_path(post)

  wait_for_turbo_frame('comments')

  within_turbo_frame('comments') do
    expect(page).to have_selector('.comment', count: 5)
  end
end
```

## Configuration

```ruby
# spec/rails_helper.rb
require 'spec_helper'
ENV['RAILS_ENV'] ||= 'test'
require_relative '../config/environment'

abort("Running in production!") if Rails.env.production?

require 'rspec/rails'

Dir[Rails.root.join('spec/support/**/*.rb')].sort.each { |f| require f }

RSpec.configure do |config|
  config.fixture_path = Rails.root.join('spec/fixtures')
  config.use_transactional_fixtures = true
  config.infer_spec_type_from_file_location!
  config.filter_rails_from_backtrace!

  # FactoryBot
  config.include FactoryBot::Syntax::Methods

  # Shoulda matchers
  Shoulda::Matchers.configure do |shoulda_config|
    shoulda_config.integrate do |with|
      with.test_framework :rspec
      with.library :rails
    end
  end
end
```
