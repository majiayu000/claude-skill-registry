---
name: "Rails Error Prevention"
description: "Comprehensive checklist and prevention strategies for common Ruby on Rails errors. Use this skill BEFORE writing any Rails code to prevent ViewComponent template errors, ActiveRecord query mistakes, method exposure issues, N+1 queries, and other common Rails pitfalls."
---

# Rails Error Prevention Skill

This skill provides preventative checklists and error patterns for common Rails mistakes. **Review relevant sections BEFORE writing code.**

## When to Use This Skill

- Before creating ViewComponents
- Before writing ActiveRecord queries with GROUP BY or joins
- Before writing view code that calls component methods
- Before creating controller actions
- When debugging undefined method errors
- When debugging template not found errors
- When debugging ActiveRecord grouping errors

## Critical Rule: Method Exposure Verification

**This is the #1 cause of runtime errors in Rails applications.**

```
WRONG ASSUMPTION: Service has method → View can call it through component
CORRECT RULE:     Service has method + Component exposes it = View can call it
```

### Verification Process

```bash
# Step 1: List all methods view will call on component
grep -oE '@[a-z_]+\.[a-z_]+' app/views/{path}/*.erb | sort -u

# Step 2: List all public methods in component
grep -E '^\s+def [a-z_]+' app/components/{component}_component.rb

# Step 3: Compare - any view call without component method = BUG
# Missing methods MUST be added to component BEFORE writing view code
```

### Patterns to Fix Missing Methods

```ruby
# Pattern 1: Delegation
class Metrics::DashboardComponent < ViewComponent::Base
  delegate :calculate_lifetime_tasks,
           :calculate_lifetime_success_rate,
           to: :@service
  
  def initialize(service:)
    @service = service
  end
end

# Pattern 2: Wrapper methods (preferred for transformation)
class Metrics::DashboardComponent < ViewComponent::Base
  def initialize(service:)
    @service = service
  end
  
  def lifetime_tasks
    @service.calculate_lifetime_tasks
  end
  
  def lifetime_success_rate
    @service.calculate_lifetime_success_rate
  end
end

# Pattern 3: Expose service directly (use sparingly)
class Metrics::DashboardComponent < ViewComponent::Base
  attr_reader :service
  
  def initialize(service:)
    @service = service
  end
end
# View then calls: dashboard.service.calculate_lifetime_tasks
```

---

## ViewComponent Errors

### Template Not Found

**Error Pattern:**
```
Couldn't find a template file or inline render method for {Component}
```

**Root Causes:**
- Missing template file (component.html.erb)
- Template in wrong location
- Class name doesn't match file path
- Using render without inline template defined

**Prevention Checklist:**
```bash
# Before creating component:
ls app/components/                              # Check structure
head -50 app/components/*_component.rb | head -1 # Review existing pattern
# Verify naming: ComponentName -> component_name/
```

**Required Files:**
```
app/components/{namespace}/{component_name}_component.rb
app/components/{namespace}/{component_name}_component.html.erb
```

**Correct Patterns:**

```ruby
# Option A: Separate template file
# app/components/metrics/kpi_card_component.rb
class Metrics::KpiCardComponent < ViewComponent::Base
  def initialize(title:, value:)
    @title = title
    @value = value
  end
end

# app/components/metrics/kpi_card_component.html.erb
# <div class="kpi-card">
#   <h3><%= @title %></h3>
#   <span><%= @value %></span>
# </div>

# Option B: Inline template (call method)
class Metrics::KpiCardComponent < ViewComponent::Base
  def initialize(title:, value:)
    @title = title
    @value = value
  end

  def call
    content_tag :div, class: "kpi-card" do
      safe_join([
        content_tag(:h3, @title),
        content_tag(:span, @value)
      ])
    end
  end
end
```

### Helper Method Errors

**Error Pattern:**
```
undefined local variable or method '{method}' for an instance of {Component}
Did you mean `helpers.{method}`?
```

**Root Cause:** Calling view helper directly without `helpers.` prefix

**Prevention Rules:**
- ViewComponents do NOT have direct access to view helpers
- Must use `helpers.method_name` for any Rails helper

**Helpers Requiring Prefix:**
```ruby
# WRONG                          # CORRECT
link_to(...)                     helpers.link_to(...)
image_tag(...)                   helpers.image_tag(...)
url_for(...)                     helpers.url_for(...)
form_with(...)                   helpers.form_with(...)
number_to_currency(...)          helpers.number_to_currency(...)
time_ago_in_words(...)           helpers.time_ago_in_words(...)
truncate(...)                    helpers.truncate(...)
pluralize(...)                   helpers.pluralize(...)
content_tag(...)                 helpers.content_tag(...)
tag(...)                         helpers.tag(...)
content_for(...)                 helpers.content_for(...)
```

**Alternative - Delegate Helpers:**
```ruby
class Metrics::KpiCardComponent < ViewComponent::Base
  delegate :number_to_currency, :link_to, to: :helpers

  def formatted_value
    number_to_currency(@value)  # Now works without prefix
  end
end
```

### Content Block Errors

**Error Pattern:**
```
content is not defined
```

**Prevention:** Always check `content?` before using `content`

```erb
<% if content? %>
  <%= content %>
<% end %>
```

---

## ActiveRecord Errors

### Grouping Error (PostgreSQL)

**Error Pattern:**
```
PG::GroupingError: ERROR: column "{table}.{column}" must appear in the GROUP BY clause
```

**Root Causes:**
- SELECT includes columns not in GROUP BY or aggregate functions
- Using `.select` with `.group` but including non-grouped columns
- Eager loading (`includes`/`preload`) with GROUP BY
- Using `.pluck` or `.select` with associations and GROUP BY

**Prevention Rules:**
1. Every non-aggregated column in SELECT must be in GROUP BY
2. **NEVER** combine `includes`/`preload`/`eager_load` with GROUP BY
3. Use `.select` only for grouped columns and aggregates
4. If you need associated data with grouped results, query separately

**Examples:**

```ruby
# WRONG - selecting all columns with group
Task.includes(:user).group(:task_type).count
# This tries to select tasks.* which fails

# WRONG - selecting id with group
Task.select(:task_type, :id).group(:task_type).count
# id is not grouped or aggregated

# CORRECT - only select grouped columns and aggregates
Task.group(:task_type).count
# => { "type_a" => 5, "type_b" => 3 }

# CORRECT - explicit select with only valid columns
Task.select(:task_type, 'COUNT(*) as count').group(:task_type)

# CORRECT - if you need associated data, query separately
type_counts = Task.group(:task_type).count
tasks_by_type = type_counts.keys.each_with_object({}) do |type, hash|
  hash[type] = Task.where(task_type: type).includes(:user).limit(5)
end

# CORRECT - using pluck for simple aggregations
Task.group(:task_type).pluck(:task_type, 'COUNT(*)')
# => [["type_a", 5], ["type_b", 3]]
```

**Before Writing GROUP BY Query:**
```bash
# Detection command
grep -r '\.group(' app/ --include='*.rb' -A3 -B3
grep -r '\.includes.*\.group\|.group.*\.includes' app/ --include='*.rb'
```

### N+1 Queries

**Detection:** Multiple queries for same association in logs

**Prevention:**
```ruby
# WRONG - N+1
tasks.each { |t| puts t.user.name }

# CORRECT
tasks.includes(:user).each { |t| puts t.user.name }
```

### Ambiguous Column

**Error Pattern:**
```
PG::AmbiguousColumn: ERROR: column reference "{column}" is ambiguous
```

**Prevention:** Always qualify columns when joining

```ruby
# WRONG
User.joins(:tasks).where(status: 'active')  # Both have status?

# CORRECT
User.joins(:tasks).where(users: { status: 'active' })
# OR
User.joins(:tasks).where('users.status = ?', 'active')
```

### Missing Attribute

**Error Pattern:**
```
ActiveModel::MissingAttributeError: missing attribute: {attribute}
```

**Prevention:** Include all attributes needed downstream

```ruby
# WRONG - later code needs 'email'
users = User.select(:id, :name)
users.each { |u| puts u.email }  # ERROR!

# CORRECT
users = User.select(:id, :name, :email)
```

---

## Controller Errors

### Missing Template

**Error Pattern:**
```
ActionView::MissingTemplate
```

**Prevention:**
- Every non-redirect action needs a view OR explicit render
- View path must match controller namespace

```bash
# Before creating controller action:
ls app/views/{controller}/
```

### Unknown Action

**Error Pattern:**
```
AbstractController::ActionNotFound
```

**Root Causes:**
- Route points to non-existent action
- Action is private/protected (must be public)

```bash
# Verification
rails routes | grep {controller}
grep -n 'def ' app/controllers/{controller}_controller.rb
```

---

## Nil Errors

**Error Pattern:**
```
undefined method '{method}' for nil:NilClass
```

**Prevention Patterns:**

```ruby
# Safe navigation
user&.profile&.settings&.theme

# Guard clause
return unless user&.profile

# With default
user&.profile&.settings&.theme || 'default'

# Early return
def process_user(user)
  return if user.nil?
  # ... rest of method
end
```

---

## Argument Errors

**Error Pattern:**
```
ArgumentError: wrong number of arguments (given X, expected Y)
```

**Prevention:**
```bash
# Before modifying method signature
grep -r 'method_name' app/ --include='*.rb'
# Update all call sites
```

**Rules:**
- Prefer keyword arguments for methods with 2+ params
- Use default values for optional params

---

## Prevention Checklists

### Before Creating ViewComponent

```
[ ] Check app/components/ structure
[ ] Review existing component for template pattern (inline vs file)
[ ] Verify naming: Namespace::ComponentNameComponent
[ ] Create both .rb AND .html.erb files (unless using inline)
[ ] List ALL methods view will need
[ ] Implement ALL needed methods in component
[ ] Prefix ALL Rails helpers with 'helpers.' or delegate them
```

### Before Writing View Code

```
[ ] List ALL methods view will call on component
[ ] For EACH method, verify it exists in component class
[ ] If method missing, ADD to component BEFORE view code
[ ] Verify underlying service/model has implementation
```

### Before Writing ActiveRecord Query with GROUP BY

```
[ ] List ALL columns in SELECT
[ ] Verify each is in GROUP BY or aggregate function
[ ] Remove includes/preload/eager_load
[ ] Test query in rails console first
```

### Before Writing ActiveRecord Query with Joins

```
[ ] Qualify ambiguous columns with table name
[ ] Consider if includes is better for the use case
```

### Before Creating Controller Action

```
[ ] View exists for non-redirect actions?
[ ] Routes point to public methods?
[ ] All @variables view needs are set?
```

### Before Any Code

```
[ ] Inspect existing similar implementations
[ ] Check naming conventions in codebase
[ ] Verify all dependencies exist (gems, files, routes)
[ ] Verify method exposure across all layers (view→component→service)
```

---

## Quick Debugging Commands

```bash
# Find where method is called
grep -r 'method_name' app/ --include='*.rb'

# Find method definition
grep -rn 'def method_name' app/ --include='*.rb'

# Check method visibility
grep -B5 'def method_name' app/path/to/file.rb

# List component methods
grep -E '^\s+def [a-z_]+' app/components/path_component.rb

# List service methods  
grep -E '^\s+def [a-z_]+' app/services/path.rb

# Compare view calls vs component methods
grep -oE '@\w+\.\w+' app/views/path/*.erb | sort -u
```
