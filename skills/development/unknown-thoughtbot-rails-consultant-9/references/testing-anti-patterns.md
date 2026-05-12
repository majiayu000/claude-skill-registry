# Testing Anti-Patterns

Four categories of test smells that undermine confidence in a test suite. When adding mocks, test utilities, or shared setup, check your work against these.

## 1. Obscure Tests

Tests where it is difficult to understand what is being tested. Setup code lives far from the test, making intent unclear.

The core problem is the **Mystery Guest** — objects defined outside the test case whose attributes and meaning aren't visible where they're used.

<Bad>

```ruby
describe Post do
  let(:user) { build_stubbed(:user) }
  let(:title) { "Example Post" }
  subject(:post) { build_stubbed(:post, user: user, title: title) }

  describe "#slug" do
    it "generates a slug from the title" do
      expect(post.slug).to eq("example-post")
    end
  end
end
```

Where does `post` come from? What title does it have? You have to scroll up and mentally assemble the object.

</Bad>

<Good>

```ruby
describe "#slug" do
  it "generates a slug from the title" do
    post = build_stubbed(:post, title: "Example Post")

    expect(post.slug).to eq("example-post")
  end
end
```

Everything you need to understand the test is in the test.

</Good>

**Rule:** Each test should read top-to-bottom without jumping elsewhere to understand setup.

## 2. Fragile Tests

Tests that break when seemingly unrelated changes are made to shared setup.

When test objects are created far from the test case, modifications to shared `let` blocks or `before` hooks can unexpectedly break unrelated tests.

<Bad>

```ruby
describe Post do
  let(:user) { build_stubbed(:user) }
  let(:title) { "Example Post" }
  subject(:post) { build_stubbed(:post, user: user, title: title) }

  context "with an author" do
    let(:user) { build_stubbed(:user, name: "Willy") }

    it "returns the author's name" do
      expect(post.author_name).to eq("Willy")
    end
  end
end
```

Overrides `user` locally but relies on `subject` to pick up the override. Change the `subject` definition and this test breaks for no obvious reason.

</Bad>

<Good>

```ruby
context "with an author" do
  it "returns the author's name" do
    author = build_stubbed(:user)
    post = build_stubbed(:post, user: author)

    expect(post.author_name).to eq(author.name)
  end
end
```

The test owns its setup. No implicit dependencies on shared state.

</Good>

**Rule:** Tests should break only when the behavior they describe changes — never because of unrelated setup modifications.

## 3. Erratic Tests

Tests that fail intermittently without code changes. These destroy confidence in the suite.

### Interacting Tests

Tests with side effects that leak into subsequent tests. Common sources:

- **Database records** left between test runs
- **Class-level memoization:** `@recent ||= order(created_at: :desc).limit(10)` — cached across tests
- **Mailer queues** retaining emails between tests
- **Caching enabled:** `config.action_controller.perform_caching = true` in test environment

**Diagnosis:** Run specs with `--order rand`. If failures reproduce only with a specific seed, you have interacting tests.

### JavaScript Feature Specs

Async timing issues. These methods introduce erratic behavior because they don't wait for Capybara's synchronization:

```ruby
# Fragile — race conditions
first(".active").click
all(".active").each(&:click)
execute_script("$('.active').focus()")
expect(find_field("Username").value).to eq("Joe")
expect(find(".user")["data-name"]).to eq("Joe")
expect(has_css?(".active")).to eq(false)
```

**Fix:** Use Capybara matchers that synchronize automatically — `have_css`, `have_content`, `have_field`. Let Capybara wait for the DOM rather than querying it directly.

### Date and Time

Assertions against specific dates or times break depending on when the suite runs.

**Fix:** Use `travel_to` (Rails) or Timecop to freeze time in tests that depend on it.

## 4. Test Hooks

Methods in production code that only execute during testing. This creates divergence between what you test and what runs in production.

<Bad>

```ruby
class ApplicationController < ActionController::Base
  unless Rails.env.test?
    before_filter :require_login
  end
end
```

In production, login is required. In tests, it's skipped entirely. If the login flow breaks, no test will catch it.

</Bad>

<Good>

Use test-level utilities that don't pollute production code. For authentication, use a back door that injects middleware in test mode only:

```ruby
# In feature specs — Clearance's back door
visit root_path(as: user)
```

The production code stays clean. The test infrastructure handles the shortcut.

</Good>

**Rule:** Production code should never ask "am I in a test?" If you see `Rails.env.test?` in application code, extract the test concern into test infrastructure.

## Summary

| Anti-Pattern  | Signal                                                 | Fix                                            |
| ------------- | ------------------------------------------------------ | ---------------------------------------------- |
| Obscure Tests | Can't understand the test without reading shared setup | Inline setup — everything visible in the test  |
| Fragile Tests | Unrelated setup changes break tests                    | Tests own their data, no implicit dependencies |
| Erratic Tests | Tests fail intermittently or in certain orders         | Isolate side effects, use sync matchers        |
| Test Hooks    | `Rails.env.test?` in production code                   | Move test concerns to test infrastructure      |
