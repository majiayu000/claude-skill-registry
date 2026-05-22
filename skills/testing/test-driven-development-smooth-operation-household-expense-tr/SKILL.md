---
name: test-driven-development
description: "Use when adding features or fixing bugs. Follow RED/GREEN/REFACTOR cycle. Write failing test first, implement minimal code to pass, then refactor."
---

# Test-Driven Development (TDD)

## Core Principle

Write tests BEFORE writing implementation code. Follow the RED → GREEN → REFACTOR cycle.

## When to Use This Skill

- Adding new features
- Fixing bugs
- Refactoring existing code
- User requests new functionality
- Implementing planned tasks

## The Iron Law

**TEST FIRST, CODE SECOND.**

Writing tests after code is NOT TDD. It's test-after-development (TAD) and misses TDD's benefits.

## Why TDD?

**Benefits:**
✅ Catches bugs early (before they exist)
✅ Forces you to think through design
✅ Creates better APIs (you're the first user)
✅ Provides safety net for refactoring
✅ Documentation through examples
✅ Higher confidence in changes

**Without TDD:**
❌ "It works on my machine" syndrome
❌ Fear of refactoring (might break things)
❌ Bugs discovered in production
❌ Unclear requirements until you code
❌ No safety net

## The RED → GREEN → REFACTOR Cycle

### 🔴 RED: Write a Failing Test

1. Think about what you want the code to do
2. Write a test that describes that behavior
3. Run the test - it MUST fail
4. Confirm it fails for the RIGHT reason

**Why it must fail first:**
- Proves the test actually tests something
- Confirms test setup is correct
- Verifies you're testing the right thing

### 🟢 GREEN: Make the Test Pass

1. Write the MINIMAL code to make the test pass
2. Don't worry about perfect code yet
3. Hardcoding is okay at this stage
4. Just make it green

**Why minimal:**
- Keeps you focused
- Prevents over-engineering
- Faster feedback loop

### 🔵 REFACTOR: Improve the Code

1. Now that test passes, improve the code
2. Remove duplication
3. Improve naming
4. Optimize if needed
5. Keep tests passing

**Why separate refactoring:**
- Tests provide safety net
- Can't break functionality if tests pass
- Cleaner code without fear

## TDD Protocol

### Step 1: Announce TDD Usage

```
I'm using the test-driven-development skill to implement this feature.

Following RED → GREEN → REFACTOR cycle.
```

### Step 2: RED - Write Failing Test

```
🔴 RED Phase: Writing failing test

Test: User registration returns 201 and token

test/Feature/AuthenticationTest.php:
```php
public function test_user_can_register_with_valid_data()
{
    $response = $this->postJson('/api/register', [
        'name' => 'John Doe',
        'email' => 'john@example.com',
        'password' => 'password123',
        'password_confirmation' => 'password123',
    ]);

    $response->assertStatus(201)
             ->assertJsonStructure(['token', 'user']);

    $this->assertDatabaseHas('users', [
        'email' => 'john@example.com'
    ]);
}
```

Running test (with database backup):
```bash
./scripts/safe-test.sh vendor/bin/paratest --filter=test_user_can_register
```

Result: ❌ FAILED
Error: Route [/api/register] not defined

✅ Test fails for the right reason (feature doesn't exist yet)
```

### Step 3: GREEN - Make Test Pass

```
🟢 GREEN Phase: Minimal implementation

Step 1: Create route
routes/api.php:
```php
Route::post('/register', [AuthController::class, 'register']);
```

Step 2: Create controller method
app/Http/Controllers/AuthController.php:
```php
public function register(Request $request)
{
    $validated = $request->validate([
        'name' => 'required|string|max:255',
        'email' => 'required|email|unique:users',
        'password' => 'required|min:8|confirmed',
    ]);

    $user = User::create([
        'name' => $validated['name'],
        'email' => $validated['email'],
        'password' => Hash::make($validated['password']),
    ]);

    $token = $user->createToken('auth_token')->plainTextToken;

    return response()->json([
        'user' => $user,
        'token' => $token
    ], 201);
}
```

Running test again:
```bash
./scripts/safe-test.sh vendor/bin/paratest --filter=test_user_can_register
```

Result: ✅ PASSED

🎉 Test is GREEN!
```

### Step 4: REFACTOR - Improve Code

```
🔵 REFACTOR Phase: Improving code

Issues identified:
1. Controller doing too much
2. Token creation logic could be extracted
3. Response format could be standardized

Refactoring:
1. Extract token creation to User model
app/Models/User.php:
```php
public function generateAuthToken(): string
{
    return $this->createToken('auth_token')->plainTextToken;
}
```

2. Extract response formatting
app/Http/Controllers/AuthController.php:
```php
public function register(Request $request)
{
    $validated = $request->validate([
        'name' => 'required|string|max:255',
        'email' => 'required|email|unique:users',
        'password' => 'required|min:8|confirmed',
    ]);

    $user = User::create([
        'name' => $validated['name'],
        'email' => $validated['email'],
        'password' => Hash::make($validated['password']),
    ]);

    return response()->json([
        'user' => $user,
        'token' => $user->generateAuthToken()
    ], 201);
}
```

Running test after refactor:
```bash
./scripts/safe-test.sh vendor/bin/paratest --filter=test_user_can_register
```

Result: ✅ STILL PASSED

✅ Refactoring successful (tests still green)
```

### Step 5: Repeat for Next Test

```
Moving to next test case...

🔴 RED: Registration with invalid email fails
[Write failing test]

🟢 GREEN: Add validation
[Make test pass]

🔵 REFACTOR: Extract validation to FormRequest
[Improve code while keeping tests green]

Continue cycle...
```

## TDD Examples by Feature Type

### Example 1: New API Endpoint

```
Feature: User login endpoint

🔴 RED:
test/Feature/AuthenticationTest.php:
```php
public function test_user_can_login_with_correct_credentials()
{
    $user = User::factory()->create([
        'email' => 'john@example.com',
        'password' => Hash::make('password123')
    ]);

    $response = $this->postJson('/api/login', [
        'email' => 'john@example.com',
        'password' => 'password123',
    ]);

    $response->assertStatus(200)
             ->assertJsonStructure(['token']);
}
```

Run: ❌ FAILS (route doesn't exist)

🟢 GREEN:
- Add route
- Add controller method
- Implement login logic

Run: ✅ PASSES

🔵 REFACTOR:
- Extract authentication logic
- Improve error messages
- Add rate limiting

Run: ✅ STILL PASSES
```

### Example 2: Bug Fix

```
Bug: User can login with wrong password

🔴 RED: Write test that exposes the bug
```php
public function test_user_cannot_login_with_wrong_password()
{
    $user = User::factory()->create([
        'email' => 'john@example.com',
        'password' => Hash::make('correct_password')
    ]);

    $response = $this->postJson('/api/login', [
        'email' => 'john@example.com',
        'password' => 'wrong_password',
    ]);

    $response->assertStatus(401)
             ->assertJson(['message' => 'Invalid credentials']);
}
```

Run: ❌ FAILS (bug exists - returns 200 instead of 401)

🟢 GREEN: Fix the bug
```php
public function login(Request $request)
{
    $credentials = $request->only('email', 'password');

    if (!Auth::attempt($credentials)) {
        return response()->json([
            'message' => 'Invalid credentials'
        ], 401);
    }

    $user = Auth::user();
    $token = $user->generateAuthToken();

    return response()->json(['token' => $token]);
}
```

Run: ✅ PASSES (bug fixed)

🔵 REFACTOR: Improve error handling
Run: ✅ STILL PASSES
```

### Example 3: Refactoring Existing Code

```
Goal: Refactor User model to use traits

🔴 RED: Write tests for existing functionality FIRST
```php
public function test_user_can_have_profile()
{
    $user = User::factory()->create();
    $profile = $user->profile()->create(['bio' => 'Hello']);

    $this->assertEquals('Hello', $user->profile->bio);
}

public function test_user_can_have_posts()
{
    $user = User::factory()->create();
    $post = $user->posts()->create(['title' => 'First Post']);

    $this->assertCount(1, $user->posts);
}
```

Run: ✅ PASSES (existing functionality works)

🟢 GREEN: Already green, skip to refactor

🔵 REFACTOR: Extract to traits
```php
// app/Models/Traits/HasProfile.php
trait HasProfile
{
    public function profile()
    {
        return $this->hasOne(Profile::class);
    }
}

// app/Models/Traits/HasPosts.php
trait HasPosts
{
    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}

// app/Models/User.php
class User extends Authenticatable
{
    use HasProfile, HasPosts;
}
```

Run: ✅ STILL PASSES (refactor successful)
```

## TDD Best Practices

### Test Naming

**Good names:**
- `test_user_can_register_with_valid_data`
- `test_registration_fails_with_invalid_email`
- `test_authenticated_user_can_access_profile`
- `test_unauthenticated_user_receives_401`

**Bad names:**
- `test_auth` (too vague)
- `test_1` (meaningless)
- `testUserStuff` (unclear)

### Test Structure (AAA Pattern)

```php
public function test_example()
{
    // Arrange: Set up test data
    $user = User::factory()->create();

    // Act: Perform the action
    $response = $this->actingAs($user)->getJson('/api/profile');

    // Assert: Verify the outcome
    $response->assertStatus(200);
    $this->assertEquals($user->id, $response['id']);
}
```

### Test Independence

Each test should be completely independent:

```php
// ✅ GOOD: Each test creates its own data
public function test_user_can_login()
{
    $user = User::factory()->create(['password' => Hash::make('password')]);
    // ... test login ...
}

public function test_user_can_logout()
{
    $user = User::factory()->create();
    // ... test logout ...
}

// ❌ BAD: Tests depend on order/shared state
class AuthTest extends TestCase
{
    private $user;

    protected function setUp(): void
    {
        parent::setUp();
        $this->user = User::factory()->create(); // Shared state
    }

    // These tests depend on setUp user
}
```

### Test One Thing

```php
// ✅ GOOD: Tests one specific behavior
public function test_registration_requires_email()
{
    $response = $this->postJson('/api/register', [
        'name' => 'John',
        // Missing email
        'password' => 'password',
    ]);

    $response->assertStatus(422)
             ->assertJsonValidationErrors('email');
}

// ❌ BAD: Tests multiple things
public function test_registration()
{
    // Tests multiple validations, success case, database insertion
    // If it fails, unclear which part failed
}
```

## TDD Anti-Patterns to Avoid

### ❌ Writing Tests After Code

```
BAD: "Let me code this quickly, I'll add tests later"
```

**Why bad**: Miss TDD benefits, tests become less useful

**Fix**: Write test first, no exceptions

### ❌ Testing Implementation Details

```php
// ❌ BAD: Tests internal implementation
public function test_user_repository_uses_query_builder()
{
    $repository = new UserRepository();
    $this->assertInstanceOf(QueryBuilder::class, $repository->getBuilder());
}
```

**Why bad**: Breaks when refactoring internal code

**Fix**: Test behavior, not implementation

```php
// ✅ GOOD: Tests behavior
public function test_can_find_user_by_email()
{
    $user = User::factory()->create(['email' => 'test@example.com']);

    $found = $this->repository->findByEmail('test@example.com');

    $this->assertEquals($user->id, $found->id);
}
```

### ❌ Making Tests Pass Too Quickly

```
BAD: Skip proper RED/GREEN cycle
```

**Why bad**: Might not test what you think

**Fix**: See test fail first, then make it pass

## Integration with Skills

**Use with:**
- `executing-plans` - Implement each task with TDD
- `database-backup` - Before running tests
- `code-review` - Review tests and code together

**TDD helps:**
- `brainstorming` - Think through edge cases
- `writing-plans` - Each task becomes a test
- `refactoring` - Safe to refactor with tests

## TDD Checklist

For each feature:
- [ ] Written failing test first (RED)
- [ ] Test fails for the right reason
- [ ] Written minimal code to pass (GREEN)
- [ ] Test now passes
- [ ] Refactored code while keeping tests green
- [ ] All existing tests still pass
- [ ] Test is independent (doesn't rely on other tests)
- [ ] Test has clear name describing behavior

## Authority

**This skill is based on:**
- Kent Beck's Test-Driven Development by Example
- Industry best practice: TDD proven to reduce bugs by 40-80%
- Professional standard: Used by Google, Microsoft, ThoughtWorks
- Empirical research: TDD code has fewer defects

**Social Proof**: All major tech companies use TDD for critical systems.

## Your Commitment

When implementing features:
- [ ] I will write tests BEFORE code
- [ ] I will follow RED → GREEN → REFACTOR
- [ ] I will see tests fail before making them pass
- [ ] I will refactor while keeping tests green
- [ ] I will use database backup before running tests

---

**Bottom Line**: TDD seems slower at first but is actually faster. Tests catch bugs immediately, not in production. Write tests first, always.
