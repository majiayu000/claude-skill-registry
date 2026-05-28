---
name: Rails Context Verification
description: Systematic verification of codebase context before code generation to prevent assumption bugs
version: 1.1.0
category: implementation
---

# Rails Context Verification Skill

## Purpose

Prevent "assumption bugs" by **verifying codebase context** before generating code. Never assume helper methods, authentication patterns, or namespace conventions exist - always verify first.

## The Assumption Bug Pattern

**Common Mistake:**
```ruby
# ❌ Agent assumes current_admin exists
# Agent copies pattern from client → admin without verification
# Result: undefined method 'current_admin' error

# In admin header view
<%= current_admin.email %>  # BREAKS - current_admin doesn't exist
```

**Correct Approach:**
```ruby
# ✅ Agent verifies authentication helper FIRST
# 1. Search: rg "def current_" app/controllers/
# 2. Find: current_administrator (actual helper name)
# 3. Use verified helper

# In admin header view
<%= current_administrator.email %>  # WORKS - verified from codebase
```

## Critical Rule

**NEVER assume - ALWAYS verify:**
- Helper method names (current_user, current_admin, signed_in?, etc.)
- Authentication patterns (Devise scope names)
- Namespace conventions (admin vs client patterns)
- Controller methods availability
- View helper existence
- Model method names

## Pre-Implementation Verification Protocol

### Step 1: Identify Context

Before generating ANY code, identify:

**1. Namespace Context:**
```bash
# What namespace am I working in?
- Admin namespace (app/controllers/admins/, app/views/admins/)
- Client namespace (app/controllers/clients/, app/views/clients/)
- API namespace (app/controllers/api/)
- Public namespace (app/controllers/)
```

**2. Authentication Context:**
```bash
# What authentication system is used here?
# Search for Devise configuration:
rg "devise_for" config/routes.rb

# Example output:
# devise_for :users, path: 'clients'
# devise_for :admins, path: 'admins'
# devise_for :administrators

# This tells you:
# - User model → current_user, user_signed_in?
# - Admin model → current_admin, admin_signed_in?
# - Administrator model → current_administrator, administrator_signed_in?
```

**3. Controller Inheritance:**
```bash
# What base controller is used?
# Admin controllers:
rg "class.*Controller.*ApplicationController" app/controllers/admins/

# May show:
# class Admins::BaseController < ApplicationController
# class Admins::DashboardController < Admins::BaseController
```

### Step 2: Verify Helper Methods

**Before using ANY helper in views/controllers, verify it exists:**

#### Authentication Helpers

```bash
# Search for current_* helpers
rg "def current_" app/controllers/ app/helpers/

# Common patterns:
# - current_user (Devise for :users)
# - current_admin (Devise for :admins)
# - current_administrator (Devise for :administrators)
# - current_account (custom helper)
# - current_organization (custom helper)
```

**Example Verification:**

```bash
# Task: Add user dropdown to admin header
# Question: What is the authentication helper name?

# Step 1: Search for authentication helper
$ rg "def current_" app/controllers/admins/ app/controllers/application_controller.rb

# Output:
app/controllers/application_controller.rb:
  def current_administrator
    @current_administrator ||= Administrator.find_by(id: session[:admin_id])
  end

# Step 2: Use verified helper name
# ✅ Use: current_administrator
# ❌ Don't use: current_admin (assumption)
```

#### View Helpers

```bash
# Search for custom view helpers
rg "def helper_name" app/helpers/

# Example:
$ rg "def format_currency" app/helpers/

# If found → safe to use
# If not found → DON'T use (will cause NoMethodError)
```

#### Controller Methods

```bash
# Check if controller method exists before calling from view
rg "def method_name" app/controllers/namespace/

# Example: Verify @current_account is set
$ rg "@current_account\s*=" app/controllers/clients/

# If found in before_action → safe to use in views
# If not found → will be nil in views
```

### Step 3: Extract Existing Patterns

**Don't invent patterns - discover them:**

#### Authentication Pattern Discovery

```bash
# Find existing authentication usage in target namespace
rg "signed_in\?" app/views/admins/ --type erb

# Example output:
app/views/admins/dashboard/_header.html.erb:
  <% if administrator_signed_in? %>

# Pattern discovered: administrator_signed_in? (not admin_signed_in?)
# Use this pattern, not an assumed one
```

#### Authorization Pattern Discovery

```bash
# Find existing authorization patterns
rg "authorize\|policy\|can\?" app/controllers/admins/

# Example output:
app/controllers/admins/users_controller.rb:
  before_action :require_super_admin

# Pattern discovered: require_super_admin (not authorize :admin)
# Use this pattern
```

#### Routing Pattern Discovery

```bash
# Find existing route helper usage
rg "path\|url" app/views/admins/ --type erb | head -20

# Example output:
admins_dashboard_path
destroy_admins_session_path
new_admins_administrator_path

# Pattern discovered: admins_ prefix for admin routes
# Use: admins_users_path (not admin_users_path)
```

### Step 4: Namespace-Specific Patterns

Different namespaces have different conventions:

#### Admin Namespace Patterns

```ruby
# Authentication
current_administrator  # (not current_admin)
administrator_signed_in?

# Routes
admins_dashboard_path
destroy_admins_session_path

# Controllers
class Admins::UsersController < Admins::BaseController
  before_action :authenticate_administrator!
end

# Models
Administrator (not Admin)
```

#### Client Namespace Patterns

```ruby
# Authentication
current_user
user_signed_in?
current_account  # If multi-tenancy

# Routes
clients_dashboard_path
destroy_clients_session_path

# Controllers
class Clients::DashboardController < Clients::BaseController
  before_action :authenticate_user!
  before_action :set_account
end
```

## Verification Checklist (Before Code Generation)

### For Views

- [ ] Verify authentication helper name (`rg "def current_"`)
- [ ] Verify signed_in? helper name (`rg "signed_in\?"`)
- [ ] Verify all instance variables are set in controller (`rg "@variable_name\s*=" controller_file`)
- [ ] Verify all view helpers exist (`rg "def helper_name" app/helpers/`)
- [ ] Check route helper names (`rails routes | grep namespace`)
- [ ] Verify model methods exist (`rg "def method_name" app/models/`)

### For Controllers

- [ ] Verify authentication method (`authenticate_user!` vs `authenticate_admin!`)
- [ ] Verify authorization method (Pundit, CanCanCan, custom)
- [ ] Verify before_action callbacks exist
- [ ] Verify model finder methods (find_by vs find)
- [ ] Verify service object existence (`rg "class ServiceName"`)

### For Services

- [ ] Verify model associations (`rg "has_many :association" model_file`)
- [ ] Verify model methods exist before calling
- [ ] Verify background job classes exist (`rg "class JobName"`)
- [ ] Verify mailer methods exist (`rg "def mailer_method" app/mailers/`)

### For Tests

- [ ] Verify factory exists (`rg "factory :model_name" spec/factories/`)
- [ ] Verify test helper methods (`rg "def helper" spec/support/`)
- [ ] Verify shared examples exist (`rg "shared_examples" spec/support/`)

## Common Assumption Bugs & Prevention

### Bug 1: Undefined Authentication Helper

**Assumption:**
```erb
<%# Agent assumes current_admin exists %>
<%= current_admin.email %>
```

**Prevention:**
```bash
# Verify first
$ rg "def current_" app/controllers/

# Find actual helper name, then use it
<%= current_administrator.email %>
```

### Bug 2: Wrong Devise Scope Name

**Assumption:**
```ruby
# Agent assumes admin_signed_in? exists
before_action :authenticate_admin!
```

**Prevention:**
```bash
# Check routes.rb for devise_for declaration
$ rg "devise_for" config/routes.rb

# Output: devise_for :administrators
# Correct helper: authenticate_administrator!
```

### Bug 3: Namespace Route Mismatch

**Assumption:**
```erb
<%# Agent assumes admin_users_path exists %>
<%= link_to "Users", admin_users_path %>
```

**Prevention:**
```bash
# Check existing route helper patterns
$ rg "_path" app/views/admins/ --type erb | head -5

# Output: admins_users_path (note the 's' in admins)
# Correct: admins_users_path
```

### Bug 4: Undefined Instance Variable

**Assumption:**
```erb
<%# Agent assumes @current_account is set %>
<%= @current_account.name %>
```

**Prevention:**
```bash
# Check controller sets this variable
$ rg "@current_account\s*=" app/controllers/namespace/controller.rb

# If not found → DON'T use in view
# Add to controller first, or use different pattern
```

### Bug 5: Undefined View Helper

**Assumption:**
```erb
<%# Agent assumes format_currency helper exists %>
<%= format_currency(@amount) %>
```

**Prevention:**
```bash
# Verify helper exists
$ rg "def format_currency" app/helpers/

# If not found → define helper first, or use number_to_currency (Rails built-in)
```

### Bug 6: Copying Patterns Across Namespaces

**Assumption:**
```ruby
# Agent copies client pattern to admin without verification
# Client controller uses:
before_action :set_account

# Agent assumes admin also has set_account
# In admin controller:
before_action :set_account  # BREAKS - admin doesn't have accounts
```

**Prevention:**
```bash
# Check what before_actions exist in target namespace
$ rg "before_action" app/controllers/admins/base_controller.rb

# Output shows actual available callbacks
# Use only verified callbacks, don't copy blindly
```

## Pattern Discovery Examples

### Example 1: Adding User Dropdown to Admin Header

**Task:** Add admin user dropdown with logout link

**Wrong Approach (Assumption):**
```erb
<%# Assume current_admin and destroy_admin_session_path %>
<% if admin_signed_in? %>
  <%= current_admin.email %>
  <%= link_to "Logout", destroy_admin_session_path %>
<% end %>
```

**Correct Approach (Verification):**

```bash
# Step 1: Verify authentication helper
$ rg "def current_" app/controllers/
# Found: def current_administrator

# Step 2: Verify signed_in? helper
$ rg "signed_in\?" app/views/admins/
# Found: administrator_signed_in?

# Step 3: Verify logout route
$ rails routes | grep destroy.*session | grep admin
# Found: destroy_admins_session_path

# Step 4: Use verified helpers
```

```erb
<% if administrator_signed_in? %>
  <%= current_administrator.email %>
  <%= link_to "Logout", destroy_admins_session_path, method: :delete %>
<% end %>
```

### Example 2: Adding Authorization Check

**Task:** Restrict action to super admins

**Wrong Approach (Assumption):**
```ruby
# Assume authorize method exists
before_action :authorize_admin!
```

**Correct Approach (Verification):**

```bash
# Step 1: Check existing authorization patterns
$ rg "before_action.*authorize\|admin\|permission" app/controllers/admins/

# Found pattern:
before_action :require_super_admin

# Step 2: Verify method exists
$ rg "def require_super_admin" app/controllers/

# Found in: app/controllers/admins/base_controller.rb

# Step 3: Use verified pattern
```

```ruby
before_action :require_super_admin
```

### Example 3: Adding Account-Scoped Query

**Task:** Show records for current account

**Wrong Approach (Assumption):**
```ruby
# Assume current_account exists
@records = current_account.records
```

**Correct Approach (Verification):**

```bash
# Step 1: Check if multi-tenancy is used
$ rg "current_account" app/controllers/clients/

# Step 2: Check how it's set
$ rg "def current_account\|@current_account\s*=" app/controllers/

# Step 3: If found, verify it's available in this controller
# Step 4: If not found, check what scoping is used

# If current_account exists:
@records = current_account.records

# If not, check for other patterns:
@records = current_user.records  # Or:
@records = Record.all  # If no scoping
```

## Integration with Implementation Workflow

### Before Delegating to Specialist

**In implementation-executor.md Step 2.6 (Context Verification):**

```markdown
## Step 2.6: Context Verification

Before delegating to specialist, VERIFY context:

1. **Identify Namespace:**
   - Admin? Client? API? Public?
   - Check file paths: app/controllers/[namespace]/
   - Check view paths: app/views/[namespace]/

2. **Search for Existing Patterns:**
   ```bash
   # Authentication helpers
   rg "def current_" app/controllers/

   # signed_in? helpers
   rg "signed_in\?" app/views/[namespace]/

   # Route patterns
   rails routes | grep [namespace]

   # before_actions
   rg "before_action" app/controllers/[namespace]/base_controller.rb
   ```

3. **Extract Verified Names:**
   - Authentication helper: [verified from search]
   - Routes prefix: [verified from search]
   - Authorization method: [verified from search]

4. **Pass to Specialist:**
   Include verified names in delegation message (see below)
```

### Delegation Message Format

**Add Context Verification Section:**

```markdown
**Context Verification:**
Namespace: [admin/clients/api/public]
Authentication helper: `current_administrator` (verified: app/controllers/application_controller.rb:42)
Signed-in helper: `administrator_signed_in?` (verified: app/views/admins/dashboard/_header.html.erb:12)
Route prefix: `admins_` (verified: rails routes | grep admins)
Authorization: `require_super_admin` (verified: app/controllers/admins/base_controller.rb:8)
Available instance variables: `@current_administrator` (set in before_action)

**CRITICAL:**
- DO NOT assume helper names - use ONLY the verified helpers above
- DO NOT copy patterns from other namespaces without verification
- DO NOT use helpers that aren't listed above (they don't exist)
- If you need a helper not listed, ask for it to be added first
```

## Per-Feature Context Tracking

**New in v1.1.0:** Context verification results are now persisted per-feature in beads comments.

After completing verification for a feature, the implementation-executor records the verified context in the beads feature issue comment:

```yaml
verified_context:
  namespace: admin
  auth_helper: current_administrator
  signed_in_helper: administrator_signed_in?
  route_prefix: admins_
  authorization_methods:
    - require_super_admin
    - authenticate_administrator!
  instance_variables:
    - @current_administrator
  verified_at: 2025-01-15T10:30:00Z
```

**Benefits:**
1. **Single verification** for entire feature (not per-phase)
2. **All specialists** reference same verified context
3. **Audit trail** of what was verified and when
4. **Quality assurance** - reviewers can verify correct usage

**Usage:**
When implementing any phase, check the feature beads comment for verified context and use only those exact helper/route names.

## Common Violation Patterns to Avoid

### Violation 1: Generic Name Assumption

```ruby
# ❌ WRONG - Assuming generic "current_user"
if current_user.admin?
  # code
end

# ✅ CORRECT - Use verified helper
# Verified: current_administrator (from rg search)
if current_administrator.super_admin?
  # code
end
```

### Violation 2: Cross-Namespace Pattern Copying

```ruby
# ❌ WRONG - Copying client pattern to admin
# In app/controllers/clients/dashboard_controller.rb:
before_action :set_account

# In app/controllers/admins/dashboard_controller.rb:
before_action :set_account  # FAILS - admins don't have accounts!

# ✅ CORRECT - Verify admin patterns separately
# Search: rg "before_action" app/controllers/admins/base_controller.rb
# Found: before_action :authenticate_administrator!
before_action :authenticate_administrator!
```

### Violation 3: Route Helper Plurality Mismatch

```ruby
# ❌ WRONG - Assuming singular prefix
link_to "Dashboard", admin_dashboard_path

# ✅ CORRECT - Verify actual route prefix
# Verified: rails routes | grep admin → shows "admins_" (plural)
link_to "Dashboard", admins_dashboard_path
```

### Violation 4: Devise Scope Name Mismatch

```ruby
# ❌ WRONG - Assuming scope matches model name
# Model: Administrator
# Assumption: admin_signed_in?

before_action :authenticate_admin!  # FAILS!

# ✅ CORRECT - Check devise_for scope in routes.rb
# Found: devise_for :administrators
# Correct helpers: current_administrator, administrator_signed_in?

before_action :authenticate_administrator!  # WORKS!
```

### Violation 5: Undefined Instance Variable Usage

```erb
<%# ❌ WRONG - Using @current_account without verification %>
<%= @current_account.name %>  # NIL ERROR if not set!

<%# ✅ CORRECT - Verify controller sets it first %>
<%# Search: rg "@current_account\s*=" app/controllers/admins/ %>
<%# Result: Not found in admin namespace %>
<%# Action: Use different pattern or add to controller first %>

<%= current_administrator.account&.name %>
```

## Enforcement Mechanisms

### PreToolUse Hook (verify-assumptions.sh)

The `verify-assumptions.sh` hook runs **before any code generation** to enforce verification:

**Checks:**
1. Context verification exists in beads feature comment
2. Generated code uses only verified helpers
3. No cross-namespace assumptions
4. All route helpers match verified prefix

**Blocks if:**
- Context not verified (Step 2.6 not complete)
- Code uses unverified helpers (e.g., `current_admin` when `current_administrator` verified)
- Cross-namespace copying detected

**Logs:**
Violations are logged to `.claude/assumption-violations.log` for review and learning.

### Quality Gate Integration

The Chief Reviewer validates:
- All helpers used match verified context
- No assumption patterns in generated code
- Beads comment has verified context section
- Context verification timestamp exists

## Remember

1. **Never assume - always verify** helper names, routes, methods
2. **Search first, code second** - discover patterns before applying them
3. **Namespace matters** - admin ≠ client ≠ api (different patterns)
4. **Inheritance matters** - check base controller for available methods
5. **Devise scope matters** - :users ≠ :admins ≠ :administrators (different helpers)
6. **Verification is enforced** - hooks will block unverified code generation
7. **Context is tracked** - verified context persists in beads for entire feature

## Quick Reference

**Before using in code, verify:**

| What | How to Verify | Command |
|------|---------------|---------|
| current_* helper | Search controllers | `rg "def current_" app/controllers/` |
| signed_in? helper | Search views | `rg "signed_in\?" app/views/namespace/` |
| Route helper | Check routes | `rails routes \| grep namespace` |
| View helper | Search helpers | `rg "def helper_name" app/helpers/` |
| Instance variable | Check controller | `rg "@variable\s*=" controller_file` |
| before_action | Check base controller | `rg "before_action" base_controller.rb` |
| Model method | Search model | `rg "def method_name" app/models/model.rb` |
| Factory | Search factories | `rg "factory :name" spec/factories/` |

**Verification is not optional - it's mandatory.**

Assumption bugs cause production errors. Take 2 minutes to verify, save hours of debugging.
