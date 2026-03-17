---
name: defense-in-depth
description: "Use when implementing validation or safety checks. Multi-layer validation approach prevents bugs through redundant safeguards. Makes bugs structurally impossible."
---

# Defense in Depth

## Core Principle

**Make bugs structurally impossible through multiple independent layers of validation.**

## Overview

Single-layer protection is insufficient. Defense in depth adds multiple independent validation layers so that if one fails, others catch the problem. Different code paths require different validations.

## When to Use This Skill

- Implementing data validation
- Adding safety checks
- Preventing invalid state bugs
- Handling user input
- Processing external data
- Critical operations that must not fail

## The Four Layers

### Layer 1: Entry Point Validation

**Purpose:** Reject bad input at API boundaries

**Where:** Controllers, API endpoints, function entry points

**What to validate:**
- Type correctness
- Required fields present
- Format validity (email, phone, etc.)
- Basic constraints (min/max, length)

**Example:**
```php
// Laravel Controller
public function createUser(Request $request)
{
    // Layer 1: Entry point validation
    $validated = $request->validate([
        'email' => 'required|email|max:255',
        'password' => 'required|min:8',
        'age' => 'required|integer|min:18',
    ]);

    // Continue with business logic...
}
```

### Layer 2: Business Logic Validation

**Purpose:** Enforce operational requirements

**Where:** Service classes, domain logic

**What to validate:**
- Business rules
- State transitions
- Relationships
- Domain constraints

**Example:**
```php
// UserService
public function createUser(array $data): User
{
    // Layer 2: Business logic validation
    if ($this->userRepository->emailExists($data['email'])) {
        throw new ValidationException('Email already registered');
    }

    if ($data['age'] < 18) {
        throw new ValidationException('Must be 18 or older');
    }

    // Create user...
}
```

### Layer 3: Environment Guards

**Purpose:** Context-specific safety checks

**Where:** Before operations, database queries, external calls

**What to check:**
- Database connection exists
- Required services available
- File permissions correct
- Network connectivity
- Resource limits

**Example:**
```php
public function processPayment(Payment $payment): void
{
    // Layer 3: Environment guards
    if (app()->environment('production') && !config('payment.gateway_enabled')) {
        throw new RuntimeException('Payment gateway not configured for production');
    }

    if ($payment->amount > config('payment.max_amount')) {
        throw new RuntimeException('Payment exceeds maximum allowed amount');
    }

    // Process payment...
}
```

### Layer 4: Debug Instrumentation

**Purpose:** Forensic logging for debugging

**Where:** Throughout critical paths

**What to log:**
- Input values
- State transitions
- Decision points
- Output values

**Example:**
```php
public function transferFunds(Account $from, Account $to, float $amount): void
{
    // Layer 4: Debug instrumentation
    Log::info('Transfer initiated', [
        'from_account' => $from->id,
        'to_account' => $to->id,
        'amount' => $amount,
        'from_balance_before' => $from->balance,
        'to_balance_before' => $to->balance,
    ]);

    // Perform transfer...

    Log::info('Transfer completed', [
        'from_balance_after' => $from->balance,
        'to_balance_after' => $to->balance,
    ]);
}
```

## Complete Example: User Registration

```php
// Layer 1: Entry Point Validation (Controller)
public function register(RegisterRequest $request)
{
    // FormRequest handles basic validation:
    // - email format
    // - password strength
    // - required fields

    $validated = $request->validated();

    $user = $this->userService->register($validated);

    return response()->json(['user' => $user], 201);
}

// Layer 2: Business Logic Validation (Service)
public function register(array $data): User
{
    // Business rule: Email must be unique
    if ($this->userRepository->emailExists($data['email'])) {
        throw new DuplicateEmailException('Email already registered');
    }

    // Business rule: Domain not blacklisted
    $domain = substr($data['email'], strpos($data['email'], '@') + 1);
    if ($this->isBlacklistedDomain($domain)) {
        throw new ValidationException('Email domain not allowed');
    }

    // Business rule: Age requirement
    if (isset($data['birthdate'])) {
        $age = Carbon::parse($data['birthdate'])->age;
        if ($age < 18) {
            throw new ValidationException('Must be 18 or older to register');
        }
    }

    return $this->createUser($data);
}

// Layer 3: Environment Guards (Repository/Model)
protected function createUser(array $data): User
{
    // Environment guard: Database connection
    if (!DB::connection()->getPdo()) {
        throw new DatabaseException('Database connection not available');
    }

    // Environment guard: Email service available
    if (!app('email')->isAvailable()) {
        throw new ServiceException('Email service unavailable');
    }

    // Layer 4: Debug instrumentation
    Log::info('Creating user', [
        'email' => $data['email'],
        'timestamp' => now(),
    ]);

    $user = User::create([
        'email' => $data['email'],
        'password' => Hash::make($data['password']),
    ]);

    Log::info('User created', [
        'user_id' => $user->id,
        'email' => $user->email,
    ]);

    return $user;
}
```

## Why All Layers Matter

### Scenario: Layer 1 Only

```php
// Only entry point validation
public function createUser(Request $request)
{
    $validated = $request->validate(['email' => 'required|email']);

    // ❌ Problem: Email could be duplicate
    // ❌ Problem: Domain could be blacklisted
    // ❌ Problem: Database could be down
    // ❌ Problem: No logging for debugging

    User::create($validated);
}
```

### Scenario: All Layers

```php
// Layer 1: Entry validation
$validated = $request->validate(['email' => 'required|email']);

// Layer 2: Business validation
if ($this->emailExists($validated['email'])) {
    throw new ValidationException('Duplicate email');
}

// Layer 3: Environment guard
if (!DB::connection()->getPdo()) {
    throw new DatabaseException('Database unavailable');
}

// Layer 4: Instrumentation
Log::info('Creating user', ['email' => $validated['email']]);

// ✅ Now protected against multiple failure modes
User::create($validated);
```

## Common Validation Patterns

### Email Validation (All Layers)

```php
// Layer 1: Format
'email' => 'required|email'

// Layer 2: Business rules
- Unique in database
- Domain not blacklisted
- Not a disposable email service

// Layer 3: Environment
- Email service available
- SMTP configured

// Layer 4: Logging
- Log email (sanitized)
- Log validation results
```

### Payment Processing (All Layers)

```php
// Layer 1: Input validation
'amount' => 'required|numeric|min:0.01'
'currency' => 'required|in:USD,EUR,GBP'

// Layer 2: Business rules
- Amount within limits
- Account has sufficient funds
- Payment method valid

// Layer 3: Environment
- Payment gateway available
- SSL certificate valid
- Fraud detection service up

// Layer 4: Logging
- Log all payment attempts
- Log amounts and currencies
- Log success/failure
```

### File Upload (All Layers)

```php
// Layer 1: Input validation
'file' => 'required|file|max:10240|mimes:jpg,png,pdf'

// Layer 2: Business rules
- User has upload quota remaining
- File name not duplicate
- Content passes virus scan

// Layer 3: Environment
- Disk space available
- Directory writable
- Virus scanner available

// Layer 4: Logging
- Log file details
- Log storage location
- Log processing results
```

## Real-World Impact

**Example from Production:**

**Before Defense in Depth:**
```php
// Only basic validation
public function updateProfile(Request $request, User $user)
{
    $data = $request->validate(['bio' => 'string|max:500']);
    $user->update($data);
}

// Bug: User could set bio to another user's email, causing privacy leak
// Bug: Bio could contain SQL injection (if used raw elsewhere)
// Bug: No logging meant debugging was impossible
```

**After Defense in Depth:**
```php
public function updateProfile(Request $request, User $user)
{
    // Layer 1: Input validation
    $data = $request->validate([
        'bio' => 'string|max:500',
    ]);

    // Layer 2: Business validation
    if ($this->containsSensitiveData($data['bio'])) {
        throw new ValidationException('Bio contains restricted content');
    }

    // Layer 3: Environment guard
    if (!$user->can('update', $user)) {
        throw new UnauthorizedException();
    }

    // Layer 4: Instrumentation
    Log::info('Profile update', [
        'user_id' => $user->id,
        'old_bio' => $user->bio,
        'new_bio' => $data['bio'],
    ]);

    $user->update($data);

    Log::info('Profile updated successfully', ['user_id' => $user->id]);
}

// ✅ Protected against multiple attack vectors
// ✅ Logging helps debug issues
```

## Integration with Other Skills

**Use with:**
- `test-driven-development` - Write tests for each layer
- `code-review` - Verify all layers present
- `systematic-debugging` - Logs help identify which layer failed

**Complements:**
- `database-backup` - Another safety layer
- `verification-before-completion` - Validate defenses work

## Checklist for Defense in Depth

For any data processing or critical operation:

- [ ] **Layer 1**: Entry point validation implemented?
- [ ] **Layer 2**: Business logic validation implemented?
- [ ] **Layer 3**: Environment guards in place?
- [ ] **Layer 4**: Debug logging added?
- [ ] Tested each layer independently?
- [ ] Tested with invalid data at each layer?
- [ ] Verified logging captures useful information?

## Common Mistakes

### Mistake 1: Only One Layer

```php
// ❌ Only validates at entry
public function createOrder(Request $request)
{
    $validated = $request->validate(['product_id' => 'required']);
    Order::create($validated);
}

// Missing: Business rules, environment checks, logging
```

### Mistake 2: Duplicate Validation Logic

```php
// ❌ Same validation in every layer (violates DRY)
// Layer 1
$request->validate(['email' => 'email']);

// Layer 2
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) { ... }

// ✅ Different validations per layer
// Layer 1: Format
// Layer 2: Business rules (uniqueness, blacklist)
```

### Mistake 3: No Logging

```php
// ❌ No instrumentation
public function criticalOperation()
{
    // Complex logic
    // No logs
}

// ✅ Add logging
Log::info('Critical operation started');
// Complex logic
Log::info('Critical operation completed');
```

## Authority

**This skill is based on:**
- Security best practice: Defense in depth principle
- Industry standard: Multiple validation layers prevent bugs
- Real production experience: Single-layer validation fails
- Evidence-based: Reduces bugs by catching at multiple points

**Social Proof**: Major companies (Google, Amazon, Microsoft) use layered validation.

## Your Commitment

When implementing validation:
- [ ] I will implement ALL four layers
- [ ] I will not rely on a single validation point
- [ ] I will add appropriate logging
- [ ] I will test each layer independently
- [ ] I will make bugs structurally impossible

---

**Bottom Line**: One layer of validation is not enough. Different layers catch different problems. Implement all four layers to make bugs structurally impossible.
