---
name: rails-debugging
description: Use when debugging Rails issues - provides Rails-specific debugging tools (logs, console, byebug, SQL logging) integrated with systematic debugging process
---

# Rails Debugging Tools & Techniques

<superpowers-integration>
**REQUIRED BACKGROUND:** Use superpowers:systematic-debugging for investigation process
  - That skill defines 4-phase framework (Root Cause → Pattern → Hypothesis → Implementation)
  - This skill provides Rails-specific debugging tools for each phase
</superpowers-integration>

<when-to-use>
- Rails application behaving unexpectedly
- Tests failing with unclear errors
- Performance issues or N+1 queries
- Production errors need investigation
</when-to-use>

<verification-checklist>
Before completing debugging work:
- ✅ Root cause identified (not just symptoms)
- ✅ Regression test added (prevents recurrence)
- ✅ Fix verified in development and test environments
- ✅ All tests passing (bin/ci passes)
- ✅ Logs reviewed for related issues
- ✅ Performance impact verified (if applicable)
</verification-checklist>

<phase1-root-cause-investigation>

<tool name="rails-logs">
<description>Check Rails logs for errors and request traces</description>

```bash
# Development logs
tail -f log/development.log

# Production logs (Kamal)
kamal app logs --tail

# Filter by severity
grep ERROR log/production.log

# Filter by request
grep "Started GET" log/development.log

```
</tool>

<tool name="rails-console">
<description>Interactive Rails console for testing models/queries</description>

```ruby
# Start console
rails console

# Or production console (Kamal)
kamal app exec 'bin/rails console'

# Test models
user = User.find(1)
user.valid?  # Check validations
user.errors.full_messages  # See errors

# Test queries
User.where(email: "test@example.com").to_sql  # See SQL
User.includes(:posts).where(posts: { published: true })  # Avoid N+1

```
</tool>

<tool name="byebug">
<description>Breakpoint debugger for stepping through code</description>

```ruby
# Add to any Rails file
def some_method
  byebug  # Execution stops here
  # ... rest of method
end

# Byebug commands:
# n  - next line
# s  - step into method
# c  - continue execution
# pp variable  - pretty print
# var local  - show local variables
# exit  - quit debugger

```
</tool>

<tool name="sql-logging">
<description>Enable verbose SQL logging to see queries</description>

```ruby
# In rails console or code
ActiveRecord::Base.logger = Logger.new(STDOUT)

# Now all SQL queries print to console
User.all
# => SELECT "users".* FROM "users"

```
</tool>

</phase1-root-cause-investigation>

<phase2-pattern-analysis>

<tool name="rails-routes">
<description>Check route definitions and paths</description>

```bash
# List all routes
rails routes

# Filter routes
rails routes | grep users

# Show routes for controller
rails routes -c users

```
</tool>

<tool name="rails-db-status">
<description>Check migration status and schema</description>

```bash
# Migration status
rails db:migrate:status

# Show schema version
rails db:version

# Check pending migrations
rails db:abort_if_pending_migrations

```
</tool>

</phase2-pattern-analysis>

<phase3-hypothesis-testing>

<tool name="rails-runner">
<description>Run Ruby code in Rails environment</description>

```bash
# Run one-liner
rails runner "puts User.count"

# Run script
rails runner scripts/investigate_users.rb

# Production environment
RAILS_ENV=production rails runner "User.pluck(:email)"

```
</tool>

</phase3-hypothesis-testing>

<phase4-implementation>

<tool name="rails-test-verbose">
<description>Run tests with detailed output</description>

```bash
# Run single test with backtrace
rails test test/models/user_test.rb --verbose

# Run with warnings enabled
RUBYOPT=-W rails test

# Run with seed for reproducibility
rails test --seed 12345

```
</tool>

</phase4-implementation>

<common-issues>

<issue name="n-plus-one-queries">
<detection>
Check logs for many similar queries:

```

User Load (0.1ms)  SELECT * FROM users WHERE id = 1
Post Load (0.1ms)  SELECT * FROM posts WHERE user_id = 1
Post Load (0.1ms)  SELECT * FROM posts WHERE user_id = 2
Post Load (0.1ms)  SELECT * FROM posts WHERE user_id = 3

```
</detection>
<solution>
Use includes/preload:

```ruby
# Bad
users.each { |user| user.posts.count }

# Good
users.includes(:posts).each { |user| user.posts.count }

```
</solution>
</issue>

<issue name="missing-migration">
<detection>
Error: "ActiveRecord::StatementInvalid: no such column"
</detection>
<solution>

```bash
# Check migration status
rails db:migrate:status

# Run pending migrations
rails db:migrate

# Or rollback and retry
rails db:rollback
rails db:migrate

```
</solution>
</issue>

</common-issues>

<related-skills>
- superpowers:systematic-debugging (4-phase framework)
- rails-ai:models (Query optimization, N+1 debugging)
- rails-ai:controllers (Request debugging, parameter inspection)
- rails-ai:testing (Test debugging, failure investigation)
</related-skills>

<resources>

**Official Documentation:**
- [Rails Guides - Debugging Rails Applications](https://guides.rubyonrails.org/debugging_rails_applications.html)
- [Rails API - ActiveSupport::Logger](https://api.rubyonrails.org/classes/ActiveSupport/Logger.html)
- [Ruby Debugging Guide](https://ruby-doc.org/stdlib-3.0.0/libdoc/debug/rdoc/index.html)

**Gems & Libraries:**
- [byebug](https://github.com/deivid-rodriguez/byebug) - Ruby debugger
- [bullet](https://github.com/flyerhzm/bullet) - N+1 query detection

**Tools:**
- [Rack Mini Profiler](https://github.com/MiniProfiler/rack-mini-profiler) - Performance profiling

</resources>
