---
name: rails-testing
description: Specialized skill for Rails testing with RSpec, FactoryBot, and TDD workflows. Use when writing tests, setting up test coverage, creating factories, or implementing test-driven development. Covers unit tests, integration tests, system tests, and component tests.
---

# Rails Testing

Professional Rails testing guide following TDD best practices with RSpec.

## When to Use This Skill

- Writing RSpec tests (model, controller, request, system, component)
- Implementing test-driven development (TDD) workflow
- Creating FactoryBot factories and traits
- Setting up test coverage with SimpleCov
- Writing integration and system tests with Capybara
- Testing ViewComponents
- Testing background jobs
- Testing interactions and business logic

## Test-First Development (NON-NEGOTIABLE)

**Every feature MUST follow TDD cycle**:

```ruby
# 1. Write failing test FIRST
RSpec.describe User do
  it "validates presence of email" do
    user = User.new(email: nil)
    expect(user).not_to be_valid
  end
end

# 2. Run test - MUST fail (Red)
# 3. Implement minimal code to pass (Green)
# 4. Refactor while keeping tests green (Refactor)
```

**Strict Rules**:
- Tests written BEFORE implementation
- Never commit failing tests to main branch
- Never skip/disable tests to make builds pass
- Red-Green-Refactor cycle strictly enforced
- Tests serve as living documentation

## Test Coverage Expectations

| Layer | Coverage Target | What to Test |
|-------|----------------|--------------|
| Models | 100% | All validations, scopes, methods |
| Interactions | 100% | All business logic paths |
| Components | 90%+ | Rendering, conditional logic |
| Controllers | 80%+ | Success/failure paths, auth |
| System Tests | Key flows | Critical user journeys |

## Testing Tools

```ruby
# Gemfile
group :development, :test do
  gem "rspec-rails"        # Testing framework
  gem "factory_bot_rails"  # Test data factories
  gem "faker"              # Fake data generation
  gem "shoulda-matchers"   # One-liner matchers (optional)
end

group :test do
  gem "capybara"           # System test DSL
  gem "selenium-webdriver" # Browser automation
  gem "database_cleaner-active_record"  # Test DB cleanup
  gem "simplecov", require: false       # Coverage reporting
end
```

## Quick Reference

### Model Testing

```ruby
RSpec.describe Article, type: :model do
  describe "associations" do
    it { is_expected.to belong_to(:user) }
    it { is_expected.to have_many(:comments).dependent(:destroy) }
  end

  describe "validations" do
    it { is_expected.to validate_presence_of(:title) }
    it { is_expected.to validate_uniqueness_of(:slug) }
  end

  describe "scopes" do
    let!(:published) { create(:article, :published) }
    let!(:draft) { create(:article, :draft) }

    it "returns only published" do
      expect(Article.published).to contain_exactly(published)
    end
  end
end
```

### Interaction Testing

```ruby
RSpec.describe Users::Create, type: :interaction do
  let(:valid_params) { { email: "user@example.com", name: "John" } }

  context "with valid parameters" do
    it "creates user" do
      expect { described_class.run(valid_params) }
        .to change(User, :count).by(1)
    end

    it "returns valid outcome" do
      outcome = described_class.run(valid_params)
      expect(outcome).to be_valid
    end
  end
end
```

### System Testing

```ruby
RSpec.describe "Article Management", type: :system do
  let(:user) { create(:user) }

  before do
    driven_by(:selenium_chrome_headless)
    login_as(user)
  end

  it "allows creating article" do
    visit new_article_path

    fill_in "Title", with: "My Article"
    fill_in "Body", with: "Content"
    click_on "Create Article"

    expect(page).to have_content("Article was successfully created")
  end
end
```

### Factory Pattern

```ruby
FactoryBot.define do
  factory :user do
    sequence(:email) { |n| "user#{n}@example.com" }
    name { Faker::Name.name }

    trait :admin do
      role { "admin" }
    end

    trait :with_articles do
      after(:create) do |user|
        create_list(:article, 3, user: user)
      end
    end
  end
end
```

## Running Tests

```bash
# All tests
bundle exec rspec

# Specific file
bundle exec rspec spec/models/user_spec.rb

# Specific test by line number
bundle exec rspec spec/models/user_spec.rb:15

# With coverage
COVERAGE=true bundle exec rspec

# Watch mode (requires guard gem)
bundle exec guard
```

## Performance Testing

### N+1 Query Detection with Bullet

```ruby
# Gemfile
group :development, :test do
  gem 'bullet'
end

# config/environments/test.rb
config.after_initialize do
  Bullet.enable = true
  Bullet.bullet_logger = true
  Bullet.raise = true  # Raise error in tests
end

# RSpec test will fail if N+1 detected
RSpec.describe "Articles", type: :request do
  it "avoids N+1 queries" do
    create_list(:article, 5, :with_author)

    get articles_path

    # Bullet will raise if N+1 detected
    expect(response).to have_http_status(:ok)
  end
end
```

### Performance Profiling in Tests

```ruby
# spec/support/performance_helper.rb
RSpec.configure do |config|
  config.around(:each, :performance) do |example|
    start = Time.now
    example.run
    duration = Time.now - start

    puts "\n#{example.metadata[:full_description]}: #{duration.round(3)}s"
    expect(duration).to be < 0.5  # Fail if > 500ms
  end
end

# Usage in spec
RSpec.describe "Dashboard", :performance do
  it "loads quickly" do
    # Test code
  end
end
```

### Benchmarking

```ruby
# Gemfile
gem 'benchmark-ips'

# spec/benchmarks/query_benchmark.rb
require 'benchmark/ips'

Benchmark.ips do |x|
  x.report("without includes") { Article.all.map(&:author) }
  x.report("with includes") { Article.includes(:author).map(&:author) }
  x.compare!
end
```

## Reference Documentation

For comprehensive testing standards, refer to:
- Full testing guide: `testing.md` (detailed examples and advanced patterns)
