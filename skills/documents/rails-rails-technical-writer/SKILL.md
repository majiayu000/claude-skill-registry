---
name: rails-technical-writer
description: Technical documentation specialist for Rails projects. Use when writing README files, API documentation, setup guides, architectural decisions, code comments, or user-facing documentation. Focuses on clarity, completeness, and maintainability.
---

# Rails Technical Writer

Create clear, comprehensive documentation for Rails applications.

## When to Use This Skill

- Writing or updating README.md
- Documenting API endpoints
- Creating setup/installation guides
- Writing architectural decision records (ADRs)
- Documenting complex features or workflows
- Adding inline code documentation
- Creating migration guides
- Documenting deployment processes

## Quick Templates

### README.md

```markdown
# Project Name

Brief description of what the application does.

## Features

- User authentication with email confirmation
- Role-based authorization (admin, user)
- Real-time notifications with Turbo Streams

## Tech Stack

- **Framework**: Ruby on Rails 7.1
- **Database**: PostgreSQL 15
- **Frontend**: ViewComponent, Hotwire, Tailwind CSS
- **Background Jobs**: Solid Queue
- **Testing**: RSpec, FactoryBot, Capybara

## Prerequisites

- Ruby 3.3.0
- PostgreSQL 15+
- Node.js 20+

## Setup

```bash
# Install dependencies
bundle install
yarn install

# Database setup
bundle exec rails db:create db:migrate

# Start server
bin/dev
```

## Testing

```bash
bundle exec rspec
```

## License

[MIT License](LICENSE)
```

### API Endpoint Documentation

```ruby
# @api public
# @endpoint GET /api/v1/users
# @description List all users with pagination
#
# @param [Integer] page Page number (default: 1)
# @param [Integer] per_page Items per page (default: 25)
#
# @response 200 [Array<User>] List of users
# @response_example
#   {
#     "users": [
#       { "id": 1, "name": "John", "email": "john@example.com" }
#     ],
#     "meta": { "current_page": 1, "total_pages": 10 }
#   }
#
# @error 401 Unauthorized
# @error 422 Invalid parameters
def index
  @users = policy_scope(User).page(params[:page])
  render json: UsersSerializer.new(@users)
end
```

### Architecture Decision Record (ADR)

```markdown
# ADR 001: Use ActiveInteraction for Business Logic

## Status
Accepted

## Context
We need a pattern for encapsulating business logic with:
- Clear input/output contracts
- Built-in validation
- Composability
- Testability

## Decision
Use ActiveInteraction for all business logic operations.

## Consequences

### Positive
- Built-in type checking and validation
- Self-documenting interface
- Composable via `compose` method
- Consistent error handling

### Negative
- Additional gem dependency
- Team needs to learn new pattern

## Implementation
- Add `gem "active_interaction"` to Gemfile
- Create interactions in `app/interactions/`
- Follow naming: `Namespace::Verb` (e.g., `Users::Create`)

## Examples
See `app/interactions/users/create.rb`
```

### Code Documentation

```ruby
# Processes a payment and updates order status.
#
# Steps:
# 1. Validates payment method is active
# 2. Charges the payment gateway
# 3. Updates order status to "paid"
# 4. Sends confirmation email
#
# @param order [Order] The order to process
# @param payment_method [PaymentMethod] Payment method to charge
# @return [Boolean] true if successful
# @raise [PaymentGatewayError] if gateway unavailable
#
# @example
#   processor.process_payment(order, payment_method)
#
def process_payment(order, payment_method)
  return false unless payment_method.active?

  result = gateway.charge(
    amount: order.total,
    source: payment_method.token
  )

  if result.success?
    order.update!(status: :paid)
    OrderMailer.payment_confirmation(order).deliver_later
    true
  else
    order.errors.add(:base, result.error_message)
    false
  end
end
```

## Documentation Best Practices

### Writing Style

**✅ Do:**
- Use active voice: "The system validates..."
- Be concise: "Creates a user" not "This method creates a user record"
- Include examples with code snippets
- Structure with clear headings
- Keep documentation updated

**❌ Avoid:**
- Passive voice
- Outdated information
- Obvious comments: `i++ // increment i`
- Commented-out code (use git instead)

### When to Add Comments

**Comment:**
- ✓ Why, not what (explain reasoning)
- ✓ Complex algorithms or business logic
- ✓ Workarounds for bugs
- ✓ Performance optimizations
- ✓ Security considerations
- ✓ Public API methods

**Don't comment:**
- ✗ Obvious code
- ✗ Redundant information
- ✗ Changelog info (use git)

## README Structure

**Essential sections (in order):**

1. **Project name + description**
2. **Features** - What it does
3. **Tech stack** - Technologies used
4. **Prerequisites** - Requirements
5. **Setup** - Installation steps
6. **Usage** - How to run
7. **Testing** - How to test
8. **Deployment** - How to deploy
9. **Contributing** - Guidelines
10. **License** - Legal info

## Feature Documentation

```markdown
# Feature Name

## Overview
Brief description of the feature.

## Implementation

### Key Components
- `Model` - Handles data
- `Interaction` - Business logic
- `Controller` - HTTP interface

### How It Works

1. User performs action
2. Controller calls interaction
3. Interaction validates and processes
4. Result returned to user

## Usage

```ruby
# Example code
result = Features::DoSomething.run(params)
```

## Testing

```ruby
RSpec.describe Features::DoSomething do
  it "works correctly" do
    # test code
  end
end
```

## Gotchas

- Important consideration #1
- Important consideration #2
```

## Documentation Checklist

When making changes, update:

- [ ] README.md (if features/setup changed)
- [ ] API docs (if API endpoints changed)
- [ ] Inline comments (for complex logic)
- [ ] ADR (for architectural decisions)
- [ ] CHANGELOG (for all user-facing changes)
- [ ] Migration guide (for breaking changes)

## OpenAPI/Swagger Format

```yaml
# swagger/v1/swagger.yaml
openapi: 3.0.0
info:
  title: MyApp API
  version: 1.0.0

paths:
  /api/v1/users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        '200':
          description: Successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
```

## Markdown Conventions

Use consistent formatting:
- `# H1` for main title
- `## H2` for sections
- `### H3` for subsections
- ` ```ruby ` for code blocks with syntax
- `**bold**` for emphasis
- `- bullet` for unordered lists
- `1. number` for ordered lists
- `[link text](url)` for links

## YARD Documentation (Ruby)

```ruby
# @!group User Management

# Creates a new user account
# @param [Hash] attributes User attributes
# @option attributes [String] :email User email
# @option attributes [String] :password User password
# @return [User, nil] Created user or nil
# @raise [ValidationError] if invalid
def create_user(attributes)
  # implementation
end

# @!endgroup
```

## Good vs Bad Examples

### Good Documentation

```markdown
## Email Verification Flow

When a user registers:

1. User submits registration form
2. System creates user with `confirmed_at: nil`
3. System generates unique confirmation token
4. System sends confirmation email with link
5. User clicks link in email
6. System verifies token and sets `confirmed_at`

**Security notes:**
- Tokens expire after 24 hours
- Tokens are single-use only
- Rate limiting applied
```

### Bad Documentation

```markdown
## Email stuff

User gets email. Click link. Done.
```

---

## Reference Documentation

For comprehensive templates and detailed examples:
- Full documentation guide: `technical-writing-reference.md` (complete templates, setup guides, all platforms)

---

**Remember**: Good documentation is:
- **Clear** - Easy to understand
- **Complete** - All necessary information
- **Current** - Reflects actual code
- **Concise** - No unnecessary detail
- **Consistent** - Follows same structure
