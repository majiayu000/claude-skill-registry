---
name: implement-feature
description: Implement a feature using SDD (Spec Driven Development). Guides you through: explore → write failing specs → implement → verify.
disable-model-invocation: true
argument-hint: "[feature description or issue number]"
---

# Implement Feature with SDD

**Feature**: $ARGUMENTS

Follow the Spec Driven Development workflow strictly. Do NOT skip any step.

---

## Step 1: Explore (Read Before Writing)

Understand the codebase before writing anything:

1. Read the relevant issue if a number was provided: `gh issue view $ARGUMENTS`
2. Read related models in `app/models/`
3. Read existing specs for similar features in `spec/`
4. Check `config/routes.rb` for existing routes
5. Check `spec/factories/` for available factories

Summarize what you found: what exists, what needs to be added.

---

## Step 2: Write Failing Specs First

**Before writing any implementation code**, write RSpec specs:

### Model specs (if adding model logic)
- File: `spec/models/<model>_spec.rb`
- Test validations, associations, scopes, and methods

### Request specs (if adding controller actions)
- File: `spec/requests/<resource>_spec.rb`
- Test HTTP status, authentication, authorization

### System specs (if adding user-facing features)
- File: `spec/system/<feature>_spec.rb`
- Test user flow with Capybara

Run specs to **confirm they fail**:
```bash
bundle exec rspec <spec-file> --format documentation
```

Show the failing output. If specs pass without implementation, they're testing the wrong thing.

---

## Step 3: Implement

Write minimal code to pass the specs:

1. Generate model/migration if needed: `bin/rails generate model ...`
2. Run migrations: `bin/rails db:migrate`
3. Add model logic (validations, associations, methods)
4. Add controller actions with proper authentication/authorization
5. Add views using ERB + Turbo Frames/Streams
6. Add Stimulus controller if JavaScript behavior is needed

Follow existing patterns — read similar code first.

---

## Step 4: Verify

Run specs after implementation:

```bash
# Run the new specs
bundle exec rspec <spec-file> --format documentation

# Run full test suite
bundle exec rspec

# Auto-fix linting
bin/rubocop -a

# Security scan
bin/brakeman --no-pager
```

All steps must pass before creating a PR.

---

## Step 5: Report

Summarize:
- What specs were written (file paths)
- What was implemented (files changed)
- Test results (pass/fail counts)
- Any rubocop or brakeman findings
