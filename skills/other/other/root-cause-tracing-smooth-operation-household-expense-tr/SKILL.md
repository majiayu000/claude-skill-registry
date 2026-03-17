---
name: root-cause-tracing
description: "Use when symptoms don't reveal the cause. Trace backward through call chains to find where problems originate. Follow: Observe symptom → Find immediate cause → Identify caller → Keep tracing → Locate trigger."
---

# Root Cause Tracing

## Core Principle

Symptoms appear downstream. Root causes live upstream. Trace backward through the call chain until you find the original trigger.

## When to Use This Skill

- Bug appears far from its source
- Symptoms don't reveal the cause
- Test failures that make no sense
- Data corruption or invalid state
- "How did this value get here?"
- Intermittent failures with no clear pattern
- Test pollution (one test affects another)

## The Iron Law

**NEVER STOP AT THE SYMPTOM. Trace backward until you find the ORIGINAL TRIGGER.**

Fixing symptoms is temporary. Fixing root causes is permanent.

## Why Root Cause Tracing?

**Benefits:**
✅ Finds actual cause, not just symptoms
✅ Prevents problem from recurring
✅ Reveals systemic issues
✅ Builds system understanding
✅ Fixes multiple symptoms at once

**Without root cause tracing:**
❌ Fix one symptom, three more appear
❌ Same bug keeps coming back
❌ Waste time on wrong solutions
❌ Never understand the real problem
❌ Accumulate technical debt

## The Backward Tracing Process

### Step 1: Observe the Symptom

```
🔍 OBSERVE Phase

Symptom: User profile page shows wrong user data

Specific observation:
- User A logs in
- Views profile page (/profile)
- Sees User B's name and email
- But sees own profile picture

Initial symptom recorded ✅
```

**What to capture:**
- Exact behavior observed
- Expected vs actual
- When it occurs
- Under what conditions
- Any error messages

### Step 2: Find Immediate Cause

```
🎯 IMMEDIATE CAUSE Phase

Symptom: Profile page shows wrong user data

Where does profile data come from?

Checking ProfileController:
```php
public function show()
{
    $user = User::find(1);  // ⚠️ HARDCODED ID!
    return view('profile', ['user' => $user]);
}
```

Immediate cause found: Hardcoded user ID (1)
But this isn't the root cause - WHY is it hardcoded?
```

**Investigation techniques:**
- Check the code where symptom appears
- Add logging to see data flow
- Use debugger to inspect state
- Check what calls this code

### Step 3: Identify the Caller

```
📞 CALLER Phase

Immediate cause: Hardcoded user ID in ProfileController

Who calls this controller? Trace backward:

Route: /profile → ProfileController@show

Who defined this route?
routes/web.php:
```php
Route::get('/profile', [ProfileController::class, 'show']);
```

Wait - no authentication middleware!
Route is missing ->middleware('auth')

But this still might not be the root cause.
When was this route added? Check git history:
```bash
git log -p routes/web.php
```

Found: Added in commit abc123 "Quick fix for profile page"
Commit message says "temporary fix"

Tracing deeper...
```

**Tracing techniques:**
- Check call stack
- Search codebase for callers
- Review git history
- Check when/why code was added
- Look for comments like "TODO" or "FIXME"

### Step 4: Keep Tracing Upstream

```
⬆️ UPSTREAM TRACING Phase

Current understanding:
- Symptom: Wrong user data displayed
- Immediate: Hardcoded user ID
- Caller: Route without auth middleware
- Origin: "Quick fix" commit

Why was quick fix needed? Check related commits:

Previous commit: "Refactor authentication system"
- Removed old auth middleware
- Added new AuthService
- Updated MOST routes (but not /profile)

ROOT CAUSE FOUND:
During authentication refactor, /profile route was
accidentally left without middleware. Developer added
"quick fix" to make it work temporarily but hardcoded
user ID instead of fixing properly.

Original trigger: Incomplete refactoring
```

**Keep asking:**
- Why does this code exist?
- What was the original requirement?
- When was this pattern established?
- Who made this decision and why?
- What changed to expose this issue?

### Step 5: Verify the Root Cause

```
✅ VERIFY ROOT CAUSE Phase

Hypothesized root cause:
Incomplete refactor left route without auth middleware

Verification:
1. Check if auth middleware works on other routes
   Result: ✅ Yes, /dashboard and /settings work correctly

2. Check if adding auth middleware fixes the issue
   ```php
   Route::get('/profile', [ProfileController::class, 'show'])
       ->middleware('auth');
   ```

   And remove hardcoded ID:
   ```php
   public function show()
   {
       $user = Auth::user();
       return view('profile', ['user' => $user]);
   }
   ```

3. Test the fix
   Result: ✅ Profile page now shows correct user data

4. Check for other routes with same issue
   Result: Found 2 more routes also missing middleware

Root cause verified ✅
Systematic fix: Add middleware to all user-specific routes
```

## Advanced Tracing: Test Pollution

### The find-polluter.sh Pattern

```bash
# When one test affects another (test pollution)

🔍 Problem: TestUserLogin passes alone, fails in suite

Symptom: Test expects clean database, finds existing user

Backward trace:
1. Which test leaves data behind?
2. Use binary search to find polluter

Script concept:
```bash
#!/bin/bash
# find-polluter.sh

FAILING_TEST="TestUserLogin"
ALL_TESTS=($(./find-all-tests.sh))

test_passes_with_subset() {
    tests=$1
    run_tests "$tests" && run_test "$FAILING_TEST"
}

# Binary search
low=0
high=${#ALL_TESTS[@]}

while [ $low -lt $high ]; do
    mid=$(( (low + high) / 2 ))
    subset="${ALL_TESTS[@]:0:$mid}"

    if test_passes_with_subset "$subset"; then
        low=$((mid + 1))
    else
        high=$mid
    fi
done

echo "Polluter found: ${ALL_TESTS[$low]}"
```

Result: TestUserRegistration doesn't clean up test data

Root cause: Missing database rollback in tearDown()

Fix:
```php
protected function tearDown(): void
{
    DB::rollback();
    parent::tearDown();
}
```
```

## Real-World Root Cause Tracing Examples

### Example 1: Performance Degradation

```
Symptom: Dashboard loads in 15 seconds (was 2 seconds)

Immediate: Database query takes 14 seconds
```sql
SELECT * FROM orders WHERE user_id = 123;
-- Takes 14 seconds
```

Trace backward:
- When did it get slow? Last week
- What changed? Added 1 million orders to database
- Why is query slow? Missing index on user_id

But keep tracing...

- Why was index missing? Schema migration doesn't include it
- Why not? Developer forgot to add it
- Why did developer forget? No code review checklist for migrations
- Why no checklist? No process documentation

ROOT CAUSE: Missing process for migration reviews

FIXES:
1. Immediate: Add index
2. Systematic: Create migration review checklist
3. Preventive: Add performance testing to CI

```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
-- Now takes 0.1 seconds ✅
```
```

### Example 2: Data Corruption

```
Symptom: User balance shows negative value (-$50)

Immediate: Balance calculated incorrectly
```php
$balance = $income - $expenses;  // Results in -50
```

Trace backward:
- Why negative? Expenses > income
- Why expenses so high? Duplicate transaction
- Why duplicate? Transaction processed twice
- Why processed twice? Race condition in payment handler

Keep tracing:
- When was payment handler added? 3 months ago
- Why didn't we catch this? No transaction uniqueness check
- Why no check? Assumed external payment API would prevent duplicates
- Why that assumption? Misread API documentation

ROOT CAUSE: Misunderstood payment API behavior + missing safeguards

FIXES:
1. Immediate: Deduplicate transactions
2. Systematic: Add idempotency key to transactions
3. Preventive: Add unique constraint on transaction_id

```php
// Add idempotency
public function processPayment($paymentId, $idempotencyKey)
{
    if (Transaction::where('idempotency_key', $idempotencyKey)->exists()) {
        return ['status' => 'already_processed'];
    }

    // Process payment...

    Transaction::create([
        'payment_id' => $paymentId,
        'idempotency_key' => $idempotencyKey,
        // ...
    ]);
}
```
```

### Example 3: Intermittent Test Failures

```
Symptom: Test fails randomly (1 in 20 runs)

Immediate: Assertion fails on expected value
```php
public function test_order_total_calculation()
{
    $order = Order::factory()->create();
    $order->addItem(['price' => 10.00, 'qty' => 2]);

    $this->assertEquals(20.00, $order->total());
    // Sometimes fails: Expected 20.00, got 0.00
}
```

Trace backward:
- Why sometimes 0.00? total() calculated before items saved?
- Check timing:
```php
public function addItem($item)
{
    // Async save?
    dispatch(new SaveOrderItemJob($this->id, $item));
}

public function total()
{
    return $this->items->sum('price');
    // Might run before job completes!
}
```

Keep tracing:
- Why async save? "For performance"
- When was this added? Last month's optimization
- Why not caught sooner? Tests usually run on fast machine
- Why intermittent? Job queue processing time varies

ROOT CAUSE: Premature optimization introduced race condition

FIXES:
1. Immediate: Use synchronous save in tests
2. Systematic: Add proper job synchronization
3. Preventive: Add test for race conditions

```php
public function addItem($item)
{
    if (app()->environment('testing')) {
        // Synchronous in tests
        $this->items()->create($item);
    } else {
        // Async in production
        dispatch(new SaveOrderItemJob($this->id, $item));
    }
}
```
```

## Root Cause Tracing Patterns

### Pattern 1: The Five Whys

```
Problem: User logout fails

Why? → Token not invalidated
Why? → Logout method doesn't call revokeTokens()
Why? → Developer didn't know about revokeTokens()
Why? → No documentation on authentication system
Why? → No process for documenting architectural decisions

Root cause: Missing architectural decision records (ADRs)

Fix: Implement ADR process for all major decisions
```

### Pattern 2: The Timeline Analysis

```
Problem: Search feature broken

Timeline:
- Jan 1: Feature works ✅
- Jan 15: No issues reported
- Jan 30: Feature broken ❌

What changed between Jan 15-30?
```bash
git log --since="Jan 15" --until="Jan 30" --oneline
```

Found:
- Jan 25: "Upgrade Elasticsearch from v7 to v8"

Check breaking changes in Elasticsearch v8:
- Query DSL syntax changed

Root cause: Breaking changes in dependency upgrade

Fix: Update query syntax for v8 compatibility
```

### Pattern 3: The Dependency Chain

```
Problem: Email sending fails

Dependency chain:
EmailController → EmailService → QueueManager → RedisConnection → Redis Server

Trace backward:
1. EmailController calls EmailService ✅
2. EmailService queues job ✅
3. QueueManager connects to Redis ❌ FAILS HERE
4. Redis connection timeout

Why Redis timeout?
- Check Redis server: Running ✅
- Check connection config: Uses wrong port ❌
- Why wrong port? .env.example not updated after Redis upgrade
- Why .env.example not updated? Not part of upgrade checklist

Root cause: Incomplete upgrade process

Fix: Add .env.example updates to upgrade checklist
```

## Tracing Tools and Techniques

### Tool 1: Git Bisect (Find Breaking Commit)

```bash
# Feature worked last week, broken now

git bisect start
git bisect bad HEAD          # Current (broken)
git bisect good v1.2.0       # Last known good

# Git checks out middle commit
# Test if bug exists
./run-test.sh

git bisect bad  # if broken
# or
git bisect good # if works

# Repeat until found
# Git identifies exact breaking commit

git bisect reset

# Now trace backward from that commit
```

### Tool 2: Call Stack Analysis

```php
// Add to debug code
Log::debug('Call stack', [
    'trace' => debug_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS)
]);

// Shows exact call chain:
// ProfileController@show
// ← Route::dispatch
// ← Kernel@handle
// ← index.php

// Reveals: ProfileController called without auth middleware
```

### Tool 3: Database Query Logging

```php
// Enable query log
DB::enableQueryLog();

// Run problematic code
$user->orders()->get();

// Check queries
$queries = DB::getQueryLog();
Log::debug('Queries executed', $queries);

// Reveals:
// SELECT * FROM orders (no WHERE clause!)
// Missing user_id filter

// Trace backward to find why WHERE clause missing
```

### Tool 4: Binary Search for Test Pollution

```bash
# Test passes alone, fails in suite

# Run first half of tests + failing test
./run-tests.sh "tests/Unit/Test*.php tests/Feature/FailingTest.php"
# Passes? Polluter in second half
# Fails? Polluter in first half

# Repeat, narrowing down to single polluter
```

## Integration with Skills

**Use with:**
- `systematic-debugging` - After isolating problem location
- `test-driven-development` - Write test that exposes root cause
- `code-review` - Review fixes for root causes, not symptoms
- `git-workflow` - Use git history to trace origins

**Leads to:**
- `writing-plans` - Plan systematic fix for root cause
- `executing-plans` - Implement comprehensive solution
- `verification-before-completion` - Verify root cause fixed

## Common Mistakes

### Mistake 1: Stopping at Symptoms

```
❌ BAD:
Symptom: Query slow
Fix: Add LIMIT 100 to query

✅ GOOD:
Symptom: Query slow
Trace: Why slow? → Missing index
Trace: Why missing index? → Not in migration
Trace: Why not in migration? → No review checklist
Fix: Add index + create migration review checklist
```

### Mistake 2: Not Tracing Far Enough

```
❌ BAD:
Problem: User sees 500 error
Fix: Add try/catch to suppress error

✅ GOOD:
Problem: User sees 500 error
Trace: What causes error? → Null pointer
Trace: Why null? → Database query returns nothing
Trace: Why no results? → Wrong table name in query
Trace: Why wrong table? → Copy/paste error
Trace: How to prevent? → Add test coverage
Fix: Correct table name + add test
```

### Mistake 3: Accepting First Explanation

```
❌ BAD:
"This fails because of X" → Fix X

✅ GOOD:
"This fails because of X"
- Why X?
- What caused X?
- How did X get into this state?
- When was X introduced?
- Why didn't we catch X sooner?
→ Fix root cause of X
```

## Red Flags

- ❌ "I fixed the symptom, good enough"
- ❌ "This is too hard to trace, I'll just work around it"
- ❌ "It's working now, don't know why"
- ❌ "Let's just rewrite this part"
- ❌ "We'll fix the real problem later"

## Root Cause Tracing Checklist

For each bug:
- [ ] Symptom clearly documented
- [ ] Immediate cause identified
- [ ] Traced backward through call chain
- [ ] Asked "Why?" at least 5 times
- [ ] Found original trigger
- [ ] Verified root cause hypothesis
- [ ] Fixed root cause (not symptom)
- [ ] Added tests to prevent recurrence
- [ ] Documented findings

## Authority

**This skill is based on:**
- Five Whys technique (Taiichi Ohno, Toyota Production System)
- Root Cause Analysis (RCA) from systems engineering
- Causal chain analysis from incident investigation
- Professional debugging practices from industry leaders

**Research**: Studies show fixing root causes prevents 5-10 related bugs from occurring.

**Social Proof**: All mature engineering organizations require root cause analysis for critical bugs.

## Your Commitment

When investigating bugs:
- [ ] I will trace backward through the call chain
- [ ] I will not stop at the immediate cause
- [ ] I will ask "Why?" at least 5 times
- [ ] I will find the original trigger
- [ ] I will fix the root cause, not symptoms
- [ ] I will add safeguards to prevent recurrence
- [ ] I will document my findings

---

**Bottom Line**: Symptoms lie downstream. Root causes live upstream. Trace backward until you find the original trigger. Fix the cause, not the symptom, or the bug will return.
