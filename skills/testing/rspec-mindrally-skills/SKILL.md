---
name: rspec
description: RSpec testing best practices for Ruby and Rails applications, covering test organization, data management, and isolation patterns.
---

# RSpec Testing Best Practices

You are an expert in Ruby, Rails, and RSpec testing.

## Key Principles

### Comprehensive Coverage
Tests must cover both typical cases and edge cases, including invalid inputs and error conditions.

### Readability and Clarity
- Employ descriptive names for `describe`, `context`, and `it` blocks
- Use the `expect` syntax for improved assertion readability
- Keep test code concise without unnecessary complexity
- Include comments explaining complex logic

### Test Organization
- Use `describe` for classes/modules and `context` for different scenarios
- Use the `subject` helper to prevent repetition when defining objects under test
- Mirror your source file structure within the spec directory

### Test Data Management
- Leverage `let` and `let!` for minimal, necessary setup
- Prefer FactoryBot factories over fixtures for generating test data
- Create only the data necessary for each test

### Test Isolation
- Each test must be independent without shared state between tests
- Mock external services (APIs, databases) and stub methods appropriately
- Avoid over-mocking: test real behavior when feasible

### Reduce Duplication
- Share common behaviors across contexts using `shared_examples`
- Extract repetitive patterns into helpers or custom matchers
- Use `shared_context` for common setup across multiple specs

## Example Structure

```ruby
RSpec.describe User, type: :model do
  subject { build(:user) }

  describe 'validations' do
    it { is_expected.to validate_presence_of(:email) }
    it { is_expected.to validate_uniqueness_of(:email) }
  end

  describe '#full_name' do
    context 'when both first and last name are present' do
      let(:user) { build(:user, first_name: 'John', last_name: 'Doe') }

      it 'returns the combined name' do
        expect(user.full_name).to eq('John Doe')
      end
    end

    context 'when last name is missing' do
      let(:user) { build(:user, first_name: 'John', last_name: nil) }

      it 'returns only the first name' do
        expect(user.full_name).to eq('John')
      end
    end
  end
end
```
