---
name: plutonium-definition-actions
description: Add custom actions and interactions to Plutonium resources
---

# Definition Actions

Actions define custom operations that can be performed on resources. They can be simple (navigation) or interactive (with business logic via Interactions).

## Action Types

| Type | Shows In | Use Case |
|------|----------|----------|
| `resource_action` | Index page | Import, Export, Create |
| `record_action` | Show page | Edit, Delete, Archive |
| `collection_record_action` | Table rows | Quick actions per row |
| `bulk_action` | Selected records | Bulk operations |

## Simple Actions (Navigation)

Simple actions link to existing routes. **The target route must already exist** - these don't create new functionality, just navigation links.

```ruby
class PostDefinition < ResourceDefinition
  # Link to external URL
  action :documentation,
    label: "Documentation",
    route_options: {url: "https://docs.example.com"},
    icon: Phlex::TablerIcons::Book,
    resource_action: true

  # Link to custom controller action (you must add the action + route yourself)
  action :reports,
    route_options: {action: :reports},
    icon: Phlex::TablerIcons::ChartBar,
    resource_action: true
end
```

**Important:** When adding custom routes for actions, always use the `as:` option to name them:

```ruby
# In your portal routes or config/routes.rb
resources :posts do
  collection do
    get :reports, as: :reports  # Named route required!
  end
end
```

This ensures `resource_url_for` can generate correct URLs, especially for nested resources.

**Note:** For custom operations with business logic, use **Interactive Actions** with an Interaction class instead. That's the recommended approach for most custom actions.

## Interactive Actions (with Interaction)

```ruby
class PostDefinition < ResourceDefinition
  action :publish,
    interaction: PublishInteraction,
    icon: Phlex::TablerIcons::Send

  action :archive,
    interaction: ArchiveInteraction,
    color: :danger,
    category: :danger,
    position: 1000,
    confirmation: "Are you sure?"
end
```

## Action Options

```ruby
action :name,
  # Display
  label: "Custom Label",           # Button text (default: name.titleize)
  description: "What it does",     # Tooltip/description
  icon: Phlex::TablerIcons::Star,  # Icon component
  color: :danger,                  # :primary, :secondary, :danger

  # Visibility
  resource_action: true,           # Show on index page
  record_action: true,             # Show on show page
  collection_record_action: true,  # Show in table rows
  bulk_action: true,               # For selected records

  # Grouping
  category: :primary,              # :primary, :secondary, :danger
  position: 50,                    # Order (lower = first)

  # Behavior
  confirmation: "Are you sure?",   # Confirmation dialog
  turbo_frame: "_top",             # Turbo frame target
  route_options: {action: :foo}    # Route configuration
```

## Creating an Interaction

### Basic Structure

```ruby
# app/interactions/resource_interaction.rb (generated during install)
class ResourceInteraction < Plutonium::Resource::Interaction
end

# app/interactions/archive_interaction.rb
class ArchiveInteraction < ResourceInteraction
  presents label: "Archive",
           icon: Phlex::TablerIcons::Archive,
           description: "Archive this record"

  attribute :resource  # The record being acted on

  def execute
    resource.archived!
    succeed(resource).with_message("Record archived successfully.")
  rescue ActiveRecord::RecordInvalid => e
    failed(e.record.errors)
  rescue => error
    failed("Archive failed. Please try again.")
  end
end
```

### With Additional Inputs

```ruby
# app/interactions/company/invite_user_interaction.rb
class Company::InviteUserInteraction < Plutonium::Resource::Interaction
  presents label: "Invite User", icon: Phlex::TablerIcons::Mail

  attribute :resource  # The company
  attribute :email
  attribute :role

  # Configure form inputs
  input :email, as: :email, hint: "User's email address"
  input :role, as: :select, choices: %w[admin member viewer]

  # Validations
  validates :email, presence: true, format: {with: URI::MailTo::EMAIL_REGEXP}
  validates :role, presence: true, inclusion: {in: %w[admin member viewer]}

  def execute
    UserInvite.create!(
      company: resource,
      email: email,
      role: role,
      invited_by: current_user
    )
    succeed(resource).with_message("Invitation sent to #{email}.")
  rescue ActiveRecord::RecordInvalid => e
    failed(e.record.errors)
  end
end
```

### Bulk Action (Multiple Records)

Bulk actions operate on multiple selected records at once. When a definition has bulk actions, the resource table automatically shows:
- **Selection checkboxes** in each row
- **Bulk actions toolbar** that appears when records are selected

```ruby
# 1. Create the interaction (note: plural `resources` attribute)
class BulkArchiveInteraction < Plutonium::Resource::Interaction
  presents label: "Archive Selected", icon: Phlex::TablerIcons::Archive

  attribute :resources  # Array of records (note: plural)

  def execute
    count = 0
    resources.each do |record|
      record.archived!
      count += 1
    end
    succeed(resources).with_message("#{count} records archived.")
  rescue => error
    failed("Bulk archive failed: #{error.message}")
  end
end

# 2. Register the action in the definition
class PostDefinition < ResourceDefinition
  action :bulk_archive, interaction: BulkArchiveInteraction
  # bulk_action: true is automatically inferred from `resources` attribute
end

# 3. Add policy method
class PostPolicy < ResourcePolicy
  def bulk_archive?
    create?  # Or whatever permission level is appropriate
  end
end
```

**Authorization for bulk actions:**
- Policy method (e.g., `bulk_archive?`) is checked **per record** - the backend fails the entire request if any selected record is not authorized
- Records are fetched via `current_authorized_scope` - only records the user can access are included
- The UI only shows action buttons that **all** selected records support (intersection of allowed actions)

### Resource Action (No Record)

```ruby
class ImportInteraction < Plutonium::Resource::Interaction
  presents label: "Import CSV", icon: Phlex::TablerIcons::Upload

  # No :resource or :resources attribute = resource action
  attribute :file

  input :file, as: :file

  validates :file, presence: true

  def execute
    # Import logic...
    succeed(nil).with_message("Import completed.")
  end
end
```

## Interaction Responses

```ruby
def execute
  # Success with message (redirects to resource automatically)
  succeed(resource).with_message("Done!")

  # Success with custom redirect (only if different from default)
  succeed(resource)
    .with_redirect_response(custom_dashboard_path)
    .with_message("Redirecting...")

  # Failure with field errors
  failed(resource.errors)

  # Failure with custom message
  failed("Something went wrong")

  # Failure with specific field
  failed("Invalid value", :email)
end
```

**Note:** Redirect is automatic on success. Only use `with_redirect_response` for a different destination.

## Interaction Context

Inside an interaction:
- `current_user` - The authenticated user
- `view_context` - Access to helpers and view methods

```ruby
def execute
  resource.update!(
    archived_by: current_user,
    archived_at: Time.current
  )
  succeed(resource)
end
```

## Defining in Definition

### Basic

```ruby
class PostDefinition < ResourceDefinition
  action :publish, interaction: PublishInteraction
  action :archive, interaction: ArchiveInteraction
end
```

### With Overrides

```ruby
class PostDefinition < ResourceDefinition
  action :archive,
    interaction: ArchiveInteraction,
    collection_record_action: false,  # Don't show in table
    color: :danger,
    position: 1000                    # Show last
end
```

### Inherited Actions

Actions defined in `ResourceDefinition` (created during install) are inherited by all definitions:

```ruby
# app/definitions/resource_definition.rb (created during install)
class ResourceDefinition < Plutonium::Resource::Definition
  action :archive, interaction: ArchiveInteraction, color: :danger, position: 1000
end

# All definitions inherit the archive action automatically
class PostDefinition < ResourceDefinition
end
```

### Portal-Specific Actions

Override actions for a specific portal:

```ruby
# packages/admin_portal/app/definitions/admin_portal/post_definition.rb
class AdminPortal::PostDefinition < ::PostDefinition
  # Add admin-only actions
  action :feature, interaction: FeaturePostInteraction
  action :bulk_publish, interaction: BulkPublishInteraction
end
```

## Default CRUD Actions

Plutonium provides these by default:

```ruby
action :new,     resource_action: true,           position: 10
action :show,    collection_record_action: true,  position: 10
action :edit,    record_action: true,             position: 20
action :destroy, record_action: true,             position: 100, category: :danger
```

## Authorization

Actions are authorized via policies:

```ruby
# app/policies/post_policy.rb
class PostPolicy < ResourcePolicy
  def publish?
    user.admin? || record.author == user
  end

  def archive?
    user.admin?
  end
end
```

The action only appears if the policy method returns `true`.

## Immediate vs Form Actions

**Immediate** - Executes without showing a form (when interaction has no extra inputs):

```ruby
class ArchiveInteraction < Plutonium::Resource::Interaction
  attribute :resource  # Only resource, no other inputs
  # No input declarations

  def execute
    resource.archived!
    succeed(resource)
  end
end
```

**Form** - Shows a form first (when interaction has additional inputs):

```ruby
class InviteUserInteraction < Plutonium::Resource::Interaction
  attribute :resource
  attribute :email
  attribute :role

  input :email
  input :role, as: :select, choices: %w[admin member]
  # Has inputs = shows form first
end
```

## Common Patterns

### Archive/Restore

```ruby
class ArchiveInteraction < Plutonium::Resource::Interaction
  presents label: "Archive", icon: Phlex::TablerIcons::Archive
  attribute :resource

  def execute
    resource.archived!
    succeed(resource).with_message("Archived.")
  end
end

class RestoreInteraction < Plutonium::Resource::Interaction
  presents label: "Restore", icon: Phlex::TablerIcons::Refresh
  attribute :resource

  def execute
    resource.active!
    succeed(resource).with_message("Restored.")
  end
end
```

### Send Notification

```ruby
class SendReminderInteraction < Plutonium::Resource::Interaction
  presents label: "Send Reminder", icon: Phlex::TablerIcons::Bell
  attribute :resource
  attribute :message

  input :message, as: :text, hint: "Custom message (optional)"

  def execute
    ReminderMailer.with(record: resource, message: message).deliver_later
    succeed(resource).with_message("Reminder sent.")
  end
end
```

## Related Skills

- `plutonium-definition` - Overview and structure
- `plutonium-definition-fields` - Fields, inputs, displays
- `plutonium-definition-query` - Search, filters, scopes
- `plutonium-interaction` - Writing interaction classes
- `plutonium-policy` - Controlling action access
