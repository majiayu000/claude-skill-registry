---
name: receiving-code-review
description: "Use when processing code review feedback. Technical evaluation of feedback, verify before implementing. No performative agreement or gratitude."
---

# Receiving Code Review

## Core Principle

**Verify before implementing. Ask before assuming. Technical correctness over social comfort.**

## Overview

Code review feedback requires technical evaluation, not performative agreement. This skill teaches how to receive, evaluate, and implement feedback professionally.

## The Iron Laws

### Law 1: Technical Evaluation Required

**Never blindly accept feedback.** Verify it's technically correct first.

### Law 2: No Performative Agreement

**Forbidden phrases:**
- ❌ "You're absolutely right!"
- ❌ "Great point!"
- ❌ "Good catch!"
- ❌ "Thanks for the feedback!"
- ❌ "I should have thought of that!"

**Why forbidden:** These are social lubricants, not technical responses. They signal submission rather than evaluation.

### Law 3: Verify Against Codebase

**Check actual code before responding.** Reviewer may be wrong or looking at old version.

## Response Pattern (The Six Steps)

### Step 1: READ

Read feedback completely without reacting.

```
Reviewer feedback received:
"This function does too much. Split into smaller functions."

[Read completely, don't respond yet]
```

### Step 2: UNDERSTAND

Restate the requirement to confirm understanding.

```
Understanding check:
Reviewer suggests: Break down AuthController->login() into smaller methods

My understanding:
- Current login() method is ~80 lines
- Reviewer wants it split into multiple single-purpose methods
- Likely: validateCredentials(), generateToken(), logAuthEvent()

Is my understanding correct?
```

### Step 3: VERIFY

Check against actual codebase reality.

```
Verification:

Checking AuthController->login():
- Line count: 82 lines ✅ (confirms "too long")
- Complexity: 3 nested conditions
- Responsibilities: Validation, auth, token generation, logging, response

Verification: Reviewer's observation is accurate.
```

### Step 4: EVALUATE

Is the feedback technically sound?

```
Technical evaluation:

Pros of splitting:
- Single Responsibility Principle
- Easier to test individual parts
- More readable

Cons of splitting:
- More indirection
- Might be premature abstraction

Decision: Feedback is technically sound. Benefits outweigh costs.
```

### Step 5: RESPOND

Technical acknowledgment or reasoned pushback.

**If agreeing:**
```
Technical acknowledgment:

The login() method is indeed 82 lines with multiple responsibilities.

I'll refactor into:
1. validateCredentials() - credential checking
2. generateToken() - token creation
3. logAuthEvent() - logging
4. Main login() - orchestration

This improves testability and readability.

Implementing now.
```

**If disagreeing:**
```
Technical analysis:

I've reviewed the suggestion to split the login() method.

However, I believe it should remain as-is because:

1. The 82 lines are mostly validation rules (50 lines), which are a cohesive unit
2. Splitting would create artificial boundaries in what is inherently sequential logic
3. The current structure follows Laravel controller convention
4. Tests already cover this method comprehensively (12 test cases)

Alternative: I can extract the 50 lines of validation into a FormRequest class, reducing controller to 32 lines. This follows Laravel patterns better.

What do you think of this approach?
```

### Step 6: IMPLEMENT

Implement ONE item at a time, test each.

```
Implementing feedback:

Item 1: Extract validateCredentials() method
[Implement]
[Test]
✅ Tests pass

Item 2: Extract generateToken() method
[Implement]
[Test]
✅ Tests pass

Item 3: Extract logAuthEvent() method
[Implement]
[Test]
✅ Tests pass

All feedback items implemented ✅
Running full test suite...
✅ All 127 tests pass
```

## Example Responses

### Example 1: Security Issue

**Reviewer:**
"This endpoint is vulnerable to SQL injection."

**Bad Response:**
```
❌ "You're right! I'll fix it immediately."
```

**Good Response:**
```
✅ Technical evaluation:

Checking the endpoint code:
```php
$users = DB::select("SELECT * FROM users WHERE email = '{$email}'");
```

Verification: This IS vulnerable to SQL injection.
The email parameter is concatenated directly into SQL.

Fix: Use parameter binding:
```php
$users = DB::select("SELECT * FROM users WHERE email = ?", [$email]);
```

Or better, use Eloquent:
```php
$users = User::where('email', $email)->get();
```

Implementing Eloquent approach (safer and more maintainable).
```

### Example 2: Performance Issue

**Reviewer:**
"This has an N+1 query problem."

**Bad Response:**
```
❌ "Great catch! Fixing now."
```

**Good Response:**
```
✅ Verification:

Checking the code:
```php
$users = User::all();
foreach ($users as $user) {
    echo $user->posts->count(); // Query in loop
}
```

Confirmed: N+1 problem.
- 1 query for users
- N queries for posts (one per user)
- With 100 users: 101 queries

Fix: Eager loading
```php
$users = User::withCount('posts')->get();
foreach ($users as $user) {
    echo $user->posts_count; // No additional query
}
```

Result: 101 queries → 1 query

Implementing now.
```

### Example 3: Disagreeing with Feedback

**Reviewer:**
"Use a singleton pattern for the UserService."

**Bad Response:**
```
❌ "I disagree. Singletons are an anti-pattern."
[Dismissive, no technical reasoning]
```

**Good Response:**
```
✅ Technical analysis:

I've evaluated the singleton suggestion for UserService.

My assessment:

**Against singleton:**
1. Laravel's service container already provides singleton-like behavior via bind/singleton
2. Singletons make testing harder (global state)
3. Current implementation uses dependency injection, which is more testable
4. No performance benefit (Laravel caching handles this)

**Current approach:**
```php
// Registered in ServiceProvider
$this->app->singleton(UserService::class);

// Injected where needed
public function __construct(UserService $userService) {
    $this->userService = $userService;
}
```

This achieves the same goal (single instance) while maintaining testability.

**Question:** Is there a specific problem the singleton would solve that the current approach doesn't?

I'm happy to reconsider if there's a technical reason I'm missing.
```

### Example 4: Unclear Feedback

**Reviewer:**
"This could be better."

**Bad Response:**
```
❌ "Okay, I'll improve it."
[What does "better" mean?]
```

**Good Response:**
```
✅ Clarification request:

I'd like to understand the concern more specifically.

Current code:
```php
public function process($data) {
    // Processing logic
}
```

Questions:
1. What aspect could be better? (naming, logic, performance, structure?)
2. What specific improvement are you suggesting?
3. Is there a particular issue you're seeing?

Once I understand the specific concern, I can evaluate and address it.
```

## Handling Different Feedback Types

### Type 1: Security Feedback
**Response:** Always implement. Security > all other concerns.

### Type 2: Performance Feedback
**Response:** Verify the problem exists, measure improvement.

### Type 3: Style/Naming Feedback
**Response:** Follow project conventions. If no convention, reasonable disagreement OK.

### Type 4: Architecture Feedback
**Response:** Discuss trade-offs. Large changes need agreement.

### Type 5: Test Coverage Feedback
**Response:** Add tests if gaps identified. Defend if coverage is adequate.

## Red Flags in Your Response

- ❌ Immediate agreement without verification
- ❌ Gratitude expressions ("Thanks!", "Great catch!")
- ❌ Superlatives ("You're absolutely right!")
- ❌ Defensive reactions ("That's how it's supposed to work!")
- ❌ Dismissive responses ("That's not important")
- ❌ Implementation without understanding

## Green Flags in Your Response

- ✅ Technical evaluation performed
- ✅ Verification against codebase
- ✅ Clear reasoning provided
- ✅ Questions when unclear
- ✅ One implementation at a time
- ✅ Tests after each change

## Common Mistakes

### Mistake 1: Blind Acceptance

```
❌ Reviewer: "Add caching here"
You: "Good idea! Added caching."

Problem: Didn't evaluate if caching is appropriate, what to cache, how long, etc.
```

### Mistake 2: Performative Agreement

```
❌ "You're absolutely right! This is a critical issue!"

Problem: Social performance, not technical evaluation.
```

### Mistake 3: No Verification

```
❌ Reviewer: "This function is never called"
You: "I'll remove it"

Problem: Didn't verify. Function might be called via reflection, routes, etc.
```

### Mistake 4: Batch Implementation

```
❌ Implementing all 10 feedback items at once

Problem: If something breaks, unclear which change caused it.
```

## Integration with Other Skills

**Use with:**
- `code-review` - Your self-review before implementing feedback
- `systematic-debugging` - If implementing feedback breaks something
- `test-driven-development` - Add tests for changes

**After receiving feedback:**
- `verification-before-completion` - Verify all changes work
- `requesting-code-review` - Request re-review after changes

## Response Checklist

For each feedback item:
- [ ] Read completely without reacting
- [ ] Restate to confirm understanding
- [ ] Verify against actual code
- [ ] Evaluate technical merit
- [ ] Respond with reasoning
- [ ] Implement ONE item at a time
- [ ] Test after EACH implementation
- [ ] Verify all tests still pass

## Authority

**This skill is based on:**
- Professional code review practices
- Technical evaluation over social performance
- Emphasis on verification before implementation
- Inspired by obra/superpowers receiving-code-review skill

**Social Proof**: Technical teams value reasoned responses over blind agreement.

## Your Commitment

When receiving feedback:
- [ ] I will verify before agreeing
- [ ] I will ask when unclear
- [ ] I will provide technical reasoning
- [ ] I will implement one change at a time
- [ ] I will test after each change
- [ ] I will avoid performative agreement

---

**Bottom Line**: Code review is technical evaluation, not social agreement. Verify feedback against reality, provide reasoned responses, implement systematically. Technical correctness over social comfort.
