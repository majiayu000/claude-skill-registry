---
name: Implementation Safety
description: |
  Production-ready safety checklists for Rails implementation. Covers nil safety,
  ActiveRecord patterns, security vulnerabilities, error handling, and performance.
  Use before marking any file complete during implementation phases.
version: 1.0.0
tags: [safety, rails, checklists, quality]
---

# Implementation Safety Skill

Comprehensive safety checklists to prevent common Rails bugs and vulnerabilities during implementation.

## Quick Reference

Use these checklists **before marking any file complete** during Phase 4 (Implementation).

---

## 1. Nil Safety Checklist

Prevent `NoMethodError: undefined method for nil` errors.

```ruby
# BAD - Crashes if user is nil
user.email.downcase

# GOOD - Safe navigation
user&.email&.downcase

# BAD - Crashes if find_by returns nil
User.find_by(email: email).name

# GOOD - Handle nil explicitly
User.find_by(email: email)&.name || "Unknown"
```

**Checklist:**
- [ ] Use safe navigation (`&.`) for potentially nil objects
- [ ] Add presence validations for required attributes
- [ ] Handle nil cases explicitly in conditionals
- [ ] Use `find_by!` or handle `find_by` returning nil
- [ ] Check for nil before calling methods
- [ ] Filter nil values from collections: `hash.compact.each`

---

## 2. ActiveRecord Safety Checklist

Prevent N+1 queries, validation failures, and data integrity issues.

```ruby
# BAD - N+1 queries
Post.all.each { |p| puts p.author.name }

# GOOD - Eager loading
Post.includes(:author).each { |p| puts p.author.name }

# BAD - Silent validation failure
user.save

# GOOD - Handle validation explicitly
if user.save
  redirect_to user
else
  render :edit, status: :unprocessable_entity
end
```

**Checklist:**
- [ ] Use `includes`/`joins` to prevent N+1 queries
- [ ] Add validations for all user inputs
- [ ] Handle validation failures explicitly
- [ ] Add indexes on foreign keys
- [ ] Use scopes instead of class methods for queries
- [ ] Add counter caches for frequently accessed counts

---

## 3. Security Checklist

Prevent SQL injection, XSS, mass assignment, and other vulnerabilities.

```ruby
# BAD - SQL injection
User.where("email = '#{params[:email]}'")

# GOOD - Parameterized query
User.where(email: params[:email])
User.where("email = ?", params[:email])

# BAD - Mass assignment vulnerability
User.create(params[:user])

# GOOD - Strong parameters
User.create(user_params)

private
def user_params
  params.require(:user).permit(:name, :email)
end
```

**Checklist:**
- [ ] Strong parameters for all user inputs
- [ ] No string interpolation in SQL queries
- [ ] Sanitize HTML output (`sanitize` or `strip_tags`)
- [ ] No mass assignment without whitelisting
- [ ] Use `has_secure_password` for authentication
- [ ] No sensitive data in logs or error messages

---

## 4. Error Handling Checklist

Prevent crashes, ensure proper logging, and return meaningful errors.

```ruby
# BAD - Catches everything, hides bugs
rescue => e
  render json: { error: e.message }

# GOOD - Specific exception handling
rescue ActiveRecord::RecordNotFound => e
  render json: { error: "Resource not found" }, status: :not_found
rescue ActiveRecord::RecordInvalid => e
  render json: { errors: e.record.errors.full_messages }, status: :unprocessable_entity
```

**Checklist:**
- [ ] Rescue specific exceptions, not `StandardError`
- [ ] Log errors with context: `Rails.logger.error("Context: #{e.message}")`
- [ ] Return meaningful error messages (not raw exceptions)
- [ ] Handle edge cases (empty arrays, nil values, zero amounts)
- [ ] Use Result pattern for service objects

---

## 5. Performance Checklist

Prevent slow queries, memory bloat, and inefficient operations.

```ruby
# BAD - Loads all records into memory
User.all.map(&:email)

# GOOD - Only fetches emails
User.pluck(:email)

# BAD - Counts by loading records
User.all.any?

# GOOD - Uses SQL EXISTS
User.exists?

# BAD - Loads all records at once
User.all.each { |u| process(u) }

# GOOD - Batches of 1000
User.find_each { |u| process(u) }
```

**Checklist:**
- [ ] Use `pluck`/`select` for specific columns
- [ ] Use `exists?` instead of `any?` or `count > 0`
- [ ] Use `find_each` for large collections
- [ ] Add database indexes for frequently queried columns
- [ ] Use counter caches instead of repeated count queries

---

## 6. Migration Safety Checklist

Prevent data loss and ensure reversible migrations.

```ruby
# GOOD - Complete migration with all safety measures
class CreateOrders < ActiveRecord::Migration[7.1]
  def change
    create_table :orders do |t|
      t.references :user, null: false, foreign_key: true, index: true
      t.string :status, null: false, default: 'pending'
      t.decimal :total, precision: 10, scale: 2, null: false

      t.timestamps
    end

    add_index :orders, :status
    add_index :orders, [:user_id, :status]
  end
end
```

**Checklist:**
- [ ] Add indexes on all foreign keys
- [ ] Include `null: false` for required columns
- [ ] Add unique indexes for uniqueness constraints
- [ ] Make migrations reversible (provide `down` method if needed)
- [ ] Add default values where appropriate
- [ ] Use precision/scale for decimal columns

---

## 7. Specific Error Prevention

### NoMethodError Prevention

```ruby
# Pattern: Safe navigation chain
result = object&.method1&.method2&.method3

# Pattern: Filter nil from collections
hash.compact.each do |key, value|
  # key and value are guaranteed non-nil
end

# Pattern: Explicit nil checks
if value.nil?
  handle_missing_value
else
  process(value)
end
```

### N+1 Query Prevention

```ruby
# Pattern: Preload in controller
def index
  @posts = Post.includes(:author, :comments, :tags)
end

# Pattern: Counter cache in model
class Post < ApplicationRecord
  belongs_to :author, counter_cache: true
end

# Pattern: Test with Bullet gem
# config/environments/development.rb
Bullet.enable = true
Bullet.rails_logger = true
```

### Security Vulnerability Prevention

```ruby
# Pattern: Define strong parameters for every action
class PostsController < ApplicationController
  private

  def post_params
    params.require(:post).permit(:title, :body, :published_at)
  end

  def filter_params
    params.permit(:status, :author_id, :created_after)
  end
end

# Pattern: Parameterized queries only
User.where("email LIKE ?", "%#{sanitized_input}%")
User.where(status: params[:status])
```

---

## 8. Integration with Rails Error Prevention Skill

This skill provides quick checklists. For detailed patterns, examples, and edge cases, reference the **rails-error-prevention** skill:

```bash
# Discover full error prevention patterns
cat .claude/skills/rails-error-prevention/SKILL.md
```

**Cross-reference:**
- Nil Safety → `rails-error-prevention` Section 2
- ActiveRecord Safety → `rails-error-prevention` Section 3
- Security → `rails-error-prevention` Section 4
- Error Handling → `rails-error-prevention` Section 5

---

## Usage in Implementation Phase

During Phase 4 (Implementation), before marking each file complete:

1. **Read this skill** for quick checklist reference
2. **Review the file** against each applicable checklist
3. **Fix any violations** before proceeding
4. **Mark file complete** only after all checks pass

```bash
# Implementation workflow
# 1. Generate code for file
# 2. Run implementation-safety checklist
# 3. Fix any issues found
# 4. Run tests
# 5. Mark file complete
```
