---
name: Refactoring Workflow
description: |
  Complete refactoring workflow with tracking, validation, and cross-layer impact
  checklists. Integrates with beads for progress tracking and ensures no
  references to old names remain after refactoring.
version: 1.0.0
tags: [refactoring, tracking, validation, workflow]
---

# Refactoring Workflow Skill

Systematic refactoring with tracking, validation, and completeness verification.

## Quick Start

```bash
# 1. Record what you're refactoring
record_refactoring "Payment" "Transaction" "class_rename"

# 2. Update files, track progress
update_refactoring_progress "Payment" "app/models/transaction.rb"

# 3. Validate no old references remain
validate_refactoring "Payment" "Transaction"
```

---

## 1. Refactoring Log Functions

### record_refactoring()

Start refactoring by recording what's being changed:

```bash
record_refactoring() {
  local old_name=$1
  local new_name=$2
  local refactor_type=$3  # class_rename, attribute_rename, method_rename, table_rename

  if [ -n "$TASK_ID" ] && command -v bd &> /dev/null; then
    bd comment $TASK_ID "🔄 Refactoring Log: $old_name → $new_name

**Type**: $refactor_type
**Started**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Status**: ⏳ In Progress

### Changes Planned

1. **$(echo $refactor_type | sed 's/_/ /g')**: \`$old_name\` → \`$new_name\`

### Affected Files (Auto-detected)

\`\`\`bash
# Ruby files referencing old name
$(rg --files-with-matches \"\\b$old_name\\b\" --type ruby 2>/dev/null | head -20 || echo "None detected")
\`\`\`

### Validation Checklist

- [ ] No references to \`$old_name\` in Ruby files
- [ ] No references in view templates
- [ ] No references in routes
- [ ] No references in specs
- [ ] No references in factories
- [ ] Migration files checked (if applicable)"
  fi
}

# Examples:
# record_refactoring "Payment" "Transaction" "class_rename"
# record_refactoring "user_id" "account_id" "attribute_rename"
# record_refactoring "payments" "transactions" "table_rename"
```

### update_refactoring_progress()

Track progress as files are updated:

```bash
update_refactoring_progress() {
  local old_name=$1
  local file_updated=$2

  if [ -n "$TASK_ID" ] && command -v bd &> /dev/null; then
    bd comment $TASK_ID "✅ Refactoring Progress: Updated \`$file_updated\`

Old references to \`$old_name\` in this file have been updated.

Remaining files: $(rg --files-with-matches \"\\b$old_name\\b\" --type ruby 2>/dev/null | wc -l || echo "?")"
  fi
}
```

### validate_refactoring()

Validate all references have been updated:

```bash
validate_refactoring() {
  local old_name=$1
  local new_name=$2

  echo "🔍 Validating refactoring: $old_name → $new_name"

  # Check for remaining references
  local remaining=$(rg --count "\\b$old_name\\b" --type ruby --type erb 2>/dev/null | wc -l)

  if [ "$remaining" -gt 0 ]; then
    echo "❌ Refactoring validation failed"
    echo "Found $remaining files still referencing '$old_name':"
    rg --files-with-matches "\\b$old_name\\b" --type ruby --type erb 2>/dev/null

    if [ -n "$TASK_ID" ] && command -v bd &> /dev/null; then
      bd update $TASK_ID --status blocked
    fi

    return 1
  else
    echo "✅ Refactoring validation passed"
    echo "All references to '$old_name' successfully updated."
    return 0
  fi
}
```

---

## 2. Complete Refactoring Workflow

### Workflow Steps

1. **Start**: Record refactoring with `record_refactoring()`
2. **Update**: Update files incrementally, track with `update_refactoring_progress()`
3. **Validate**: Before phase completion, run `validate_refactoring()`
4. **Fix**: If validation fails, update remaining references
5. **Re-validate**: Run validation again until it passes
6. **Complete**: Only close task after validation passes

### Example: Class Rename Workflow

```bash
# Phase starts: Renaming Payment to Transaction

# Step 1: Record refactoring
record_refactoring "Payment" "Transaction" "class_rename"

# Step 2: Update model file
mv app/models/payment.rb app/models/transaction.rb
# Update class name in file
sed -i 's/class Payment/class Transaction/g' app/models/transaction.rb
update_refactoring_progress "Payment" "app/models/transaction.rb"

# Step 3: Update associations in other models
# ... update files ...
update_refactoring_progress "Payment" "app/models/account.rb"

# Step 4: Update controller
mv app/controllers/payments_controller.rb app/controllers/transactions_controller.rb
# ... update class name and references ...
update_refactoring_progress "Payment" "app/controllers/transactions_controller.rb"

# Step 5: Update views, specs, factories, routes
# ... update all remaining files ...

# Step 6: Validate completeness
validate_refactoring "Payment" "Transaction"

if [ $? -eq 0 ]; then
  echo "✅ Refactoring complete"
else
  echo "❌ Refactoring incomplete, fix remaining references"
fi
```

---

## 3. Cross-Layer Impact Checklists

### Class Rename Checklist

When renaming `Payment` → `Transaction`:

**Ruby Layer:**
- [ ] Model class definition
- [ ] Associations in other models (`has_many :payments`)
- [ ] Controller class name
- [ ] Controller instance variables (`@payment`)
- [ ] Service class references
- [ ] Job class references
- [ ] Serializer references
- [ ] String references (polymorphic: `"Payment"`)

**View Layer:**
- [ ] View template paths (`app/views/payments/`)
- [ ] View helpers and form objects
- [ ] Partials and layouts

**Routes:**
- [ ] Route resources (`resources :payments`)
- [ ] Named routes and path helpers

**Tests:**
- [ ] Spec describe blocks
- [ ] Factory definitions (`:payment`, `:payments`)
- [ ] Fixtures (if used)

**JavaScript/Frontend:**
- [ ] Stimulus controllers (`payment_controller.js`)
- [ ] Stimulus class names (`PaymentController`)
- [ ] data-controller attributes (`data-controller="payment"`)
- [ ] data-action attributes (`data-action="payment#submit"`)
- [ ] JavaScript imports and references
- [ ] Event names (`payment:updated`)
- [ ] Turbo frame IDs (`#payment-form`)
- [ ] Importmap pins

**I18n:**
- [ ] Locale keys (`activerecord.models.payment`)

**Configuration:**
- [ ] Initializer references
- [ ] Environment configs

### Attribute Rename Checklist

When renaming `user_id` → `account_id`:

**Database:**
- [ ] Migration (column rename)
- [ ] Run migration: `rails db:migrate`
- [ ] Verify in schema.rb

**Model:**
- [ ] Attribute references
- [ ] Validations
- [ ] Associations (`:foreign_key` option)
- [ ] Scopes and queries

**Controller:**
- [ ] Strong params

**Views:**
- [ ] Form fields
- [ ] Display references

**Tests:**
- [ ] Spec let statements
- [ ] Factory attributes

**API:**
- [ ] Serializer attributes
- [ ] API documentation

**JavaScript:**
- [ ] data-{controller}-{attr}-value attributes
- [ ] Stimulus value definitions

**I18n:**
- [ ] Attribute keys (`activerecord.attributes.model.user_id`)

### Table Rename Checklist

When renaming `payments` → `transactions`:

- [ ] Migration (table rename)
- [ ] Run migration: `rails db:migrate`
- [ ] Verify in schema.rb
- [ ] Model `table_name` declaration (if explicit)
- [ ] Foreign key constraints
- [ ] Indexes
- [ ] Raw SQL queries
- [ ] Database views (if any)

### JavaScript/Stimulus Refactoring Checklist

When renaming `payment` → `transaction` in frontend:

- [ ] Controller file rename (`payment_controller.js` → `transaction_controller.js`)
- [ ] Controller class name (`PaymentController` → `TransactionController`)
- [ ] data-controller attributes in views
- [ ] data-{controller}-target attributes
- [ ] data-action attributes
- [ ] JavaScript imports
- [ ] Event names and dispatching
- [ ] CSS class names that reference the controller
- [ ] Turbo frame IDs
- [ ] Importmap pins

### Namespace/Module Move Checklist

When moving `Services::Payment` → `Billing::Transaction`:

- [ ] File path (`app/services/payment.rb` → `app/billing/transaction.rb`)
- [ ] Module/namespace declaration
- [ ] All references to the old namespace
- [ ] Autoload paths (if custom)
- [ ] Spec file path
- [ ] Factory namespace
- [ ] Route namespace (if applicable)

---

## 4. Intentional Legacy References

Create `.refactorignore` to exclude files from validation:

```gitignore
# .refactorignore - Files to exclude from refactoring validation

# Legacy compatibility layer
lib/legacy_api_adapter.rb

# Historical documentation
CHANGELOG.md
docs/migration_guide.md

# Rename migrations (reference old names by design)
db/migrate/*_rename_*.rb

# External API contracts (can't change)
app/serializers/api/v1/*_serializer.rb
```

---

## 5. Integration with Beads

Refactoring workflow integrates with beads for:

1. **Task Tracking**: Creates comments for start, progress, completion
2. **Status Updates**: Sets task to `blocked` if validation fails
3. **Audit Trail**: Full history of what was changed and when

```bash
# Set TASK_ID before starting refactoring
export TASK_ID="PROJ-123"

# All functions will automatically log to beads
record_refactoring "Payment" "Transaction" "class_rename"
update_refactoring_progress "Payment" "app/models/transaction.rb"
validate_refactoring "Payment" "Transaction"
```

---

## 6. Quick Reference

| Function | Purpose | Example |
|----------|---------|---------|
| `record_refactoring` | Start tracking | `record_refactoring "Old" "New" "class_rename"` |
| `update_refactoring_progress` | Track file update | `update_refactoring_progress "Old" "path/file.rb"` |
| `validate_refactoring` | Check completeness | `validate_refactoring "Old" "New"` |

| Refactor Type | Key Layers to Check |
|---------------|---------------------|
| `class_rename` | Model, Controller, Views, Routes, Specs, JS |
| `attribute_rename` | Model, Controller params, Views, Specs, JS values |
| `table_rename` | Migration, Schema, Raw SQL |
| `method_rename` | All call sites, Specs |
| `namespace_move` | File paths, Autoloading, All references |
