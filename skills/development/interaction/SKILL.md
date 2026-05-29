---
name: plutonium-interaction
description: Plutonium interactions - encapsulated business logic for custom actions
---

# Plutonium Interactions

Interactions encapsulate business logic into reusable, testable units. They handle input validation, execution, and outcomes.

## Basic Structure

```ruby
# app/interactions/resource_interaction.rb (generated during install)
class ResourceInteraction < Plutonium::Resource::Interaction
end

# app/interactions/publish_post_interaction.rb
class PublishPostInteraction < ResourceInteraction
  # Presentation
  presents label: "Publish",
           icon: Phlex::TablerIcons::Send,
           description: "Make this post public"

  # Attributes (inputs)
  attribute :resource  # The record being acted upon
  attribute :publish_date, :datetime, default: -> { Time.current }

  # Form inputs (what user sees)
  input :publish_date, as: :datetime

  # Validations
  validates :publish_date, presence: true

  private

  def execute
    resource.update!(published_at: publish_date)
    succeed(resource).with_message("Post published!")
  rescue ActiveRecord::RecordInvalid => e
    failed(e.record.errors)
  end
end
```

## Attributes

Define inputs using ActiveModel attributes:

```ruby
attribute :resource                              # Record (for record actions)
attribute :resources                             # Collection (for bulk actions)
attribute :email, :string                        # String input
attribute :count, :integer, default: 1           # With default
attribute :active, :boolean, default: -> { true } # Callable default
attribute :tags, :array                          # Array
attribute :metadata, :hash                       # Hash
attribute :date, :datetime                       # DateTime
```

## Form Inputs

Define form fields with the `input` method (same as definitions):

```ruby
input :email
input :role, as: :select, choices: %w[admin user]
input :content, as: :text
input :date, as: :date
```

See `plutonium-definition-fields` skill for all input types and options.

## Presentation

Configure how the action appears in the UI:

```ruby
presents label: "Archive Record",
         icon: Phlex::TablerIcons::Archive,
         description: "Move to archive for later reference"
```

Access presentation:
```ruby
MyInteraction.label       # => "Archive Record"
MyInteraction.icon        # => Phlex::TablerIcons::Archive
MyInteraction.description # => "Move to archive..."
```

## Execution and Outcomes

### The execute Method

```ruby
private

def execute
  # Your business logic here
  # Must return succeed() or failed()
end
```

### Success Outcomes

```ruby
# Basic success (redirects automatically to resource)
succeed(resource)

# With message
succeed(resource).with_message("Done!")
succeed(resource).with_message("Warning!", :alert)

# With custom redirect (only if different from default)
succeed(resource).with_redirect_response(custom_path)

# With file download
succeed(resource).with_file_response(file_path, filename: "report.pdf")
```

**Note:** Redirect is automatic on success - the controller redirects to the resource by default. Only use `with_redirect_response` if you need a different destination.

### Failure Outcomes

```ruby
# Basic failure
failed("Something went wrong")

# With ActiveModel errors
failed(resource.errors)

# With hash of errors
failed(email: "is invalid", name: "is required")
```

### Chaining Interactions

```ruby
def execute
  CreateUserInteraction.call(view_context:, **user_params)
    .and_then { |result| SendWelcomeEmail.call(view_context:, user: result.value) }
    .and_then { |result| LogActivity.call(view_context:, user: result.value) }
    .with_message("User created and welcomed!")
end
```

On failure, the chain short-circuits and returns the failure immediately.

## Validations

Use standard ActiveModel validations:

```ruby
validates :email, presence: true
validates :email, format: { with: URI::MailTo::EMAIL_REGEXP }
validates :role, inclusion: { in: %w[admin user guest] }

validate :custom_validation

private

def custom_validation
  if resource.archived?
    errors.add(:resource, "cannot be modified when archived")
  end
end
```

Validations run automatically before `execute`. If invalid, returns `failed()` with errors.

## Interaction Types

### Record Actions

Act on a single record:

```ruby
class ArchiveInteraction < Plutonium::Resource::Interaction
  attribute :resource  # Single record

  def execute
    resource.update!(archived: true)
    succeed(resource)
  rescue ActiveRecord::RecordInvalid => e
    failed(e.record.errors)
  end
end
```

**Note:** `ActiveRecord::RecordInvalid` is NOT rescued automatically. Always rescue it when using bang methods (`create!`, `update!`, `save!`).

### Resource Actions

Act at the collection/class level (no specific record):

```ruby
class ImportInteraction < Plutonium::Resource::Interaction
  # No :resource attribute
  attribute :file

  input :file, as: :file

  def execute
    records = CSV.parse(file)
    Post.import(records)
    succeed(records)
  end
end
```

### Bulk Actions (Multiple Records)

Act on multiple selected records. When registered, the table shows checkboxes and a toolbar appears when records are selected.

```ruby
class BulkArchiveInteraction < Plutonium::Resource::Interaction
  attribute :resources  # Collection of records (note: plural)

  def execute
    resources.update_all(archived: true)
    succeed(resources).with_message("Archived #{resources.count} records")
  end
end
```

**Authorization:** Bulk actions use per-record authorization. The policy method is checked for each selected record - if any fails, the entire request is rejected. The UI only shows actions that all selected records support.

## Connecting to Definitions

Register interactions as actions:

```ruby
class PostDefinition < ResourceDefinition
  # Record action (shows on individual records)
  action :publish, interaction: PublishPostInteraction

  # Resource action (shows at collection level)
  action :import, interaction: ImportInteraction

  # With options
  action :archive,
    interaction: ArchiveInteraction,
    confirmation: "Are you sure?",
    category: :danger,
    position: 100
end
```

### Action Options

| Option | Description |
|--------|-------------|
| `interaction:` | The interaction class |
| `confirmation:` | Confirmation message before execution |
| `category:` | `:primary`, `:secondary`, `:danger` |
| `position:` | Display order (lower = first) |
| `turbo_frame:` | Turbo frame target (default: `remote_modal`) |
| `icon:` | Override interaction icon |
| `label:` | Override interaction label |

## Policy Integration

Control access with policy methods:

```ruby
class PostPolicy < ResourcePolicy
  def publish?
    update? && record.draft?
  end

  def archive?
    destroy? && !record.archived?
  end

  def import?
    create?  # Resource-level action
  end
end
```

The policy method name matches the action name with `?`.

## Accessing Context

Inside interactions:

```ruby
def execute
  # Access current user via view_context
  current_user = view_context.controller.helpers.current_user

  # Access the resource
  resource.update!(updated_by: current_user)

  succeed(resource)
end
```

## Immediate vs Form Actions

Plutonium automatically determines if an action needs a form:

- **Has inputs defined** → Shows form first (GET), then executes (POST)
- **No inputs** → Executes immediately (POST with confirmation)

```ruby
# Shows form (has inputs)
class InviteUserInteraction < Plutonium::Resource::Interaction
  attribute :resource
  attribute :email
  input :email  # This triggers form display
end

# Immediate execution (no inputs)
class ArchiveInteraction < Plutonium::Resource::Interaction
  attribute :resource
  # No inputs = immediate with confirmation
end
```

## Complete Example

```ruby
class Company::InviteUserInteraction < Plutonium::Resource::Interaction
  presents label: "Invite User",
           icon: Phlex::TablerIcons::UserPlus,
           description: "Send an invitation email"

  attribute :resource  # The company
  attribute :email, :string
  attribute :role, :string

  input :email
  input :role, as: :select, choices: -> { UserInvite.roles.keys }

  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :role, presence: true, inclusion: { in: UserInvite.roles.keys }
  validate :not_already_invited

  private

  def execute
    invite = UserInvite.create!(
      company: resource,
      email: email,
      role: role,
      invited_by: current_user
    )
    UserInviteMailer.invitation(invite).deliver_later

    succeed(resource).with_message("Invitation sent to #{email}")
  rescue ActiveRecord::RecordInvalid => e
    failed(e.record.errors)
  end

  def not_already_invited
    return unless email.present?

    if UserInvite.exists?(company: resource, email: email, state: :pending)
      errors.add(:email, "already has a pending invitation")
    end
  end

  def current_user
    view_context.controller.helpers.current_user
  end
end
```

## Best Practices

1. **Keep interactions focused** - One action per interaction
2. **Use validations** - Validate all inputs before execution
3. **Handle errors gracefully** - Rescue exceptions and return `failed()`
4. **Return meaningful messages** - Help users understand what happened
5. **Use `and_then` for chains** - Compose complex workflows from simple interactions
6. **Test independently** - Interactions are easy to unit test

## Related Skills

- `plutonium-definition-actions` - Declaring actions in definitions
- `plutonium-forms` - Custom interaction form templates
- `plutonium-policy` - Controlling access to actions
- `plutonium-resource` - How interactions fit in the architecture
