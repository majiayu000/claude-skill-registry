# BDD Step Implementation Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-25

Write rstest-bdd step definitions and wire to fixtures.

## When to Activate

Use this skill when:
- After scenario design
- Implement steps
- Write step definitions
- BDD step implementation
- Wire fixtures

## Core Principles

### 1. Fixtures Over Hardcoding

Step definitions reference fixtures, never contain inline test data.

*Fixtures can be validated, centrally maintained, and reused across scenarios.*

### 2. Propose Before Create

When a fixture doesn't exist, propose it for review before creating.

*New fixtures should be intentional decisions, not implementation details.*

### 3. Pattern Matching Precision

Step patterns should be specific enough to avoid accidental matches.

*Ambiguous patterns cause confusing test failures.*

### 4. World State Management

Steps share state through a World struct, not global variables.

*Enables parallel test execution and clear state ownership.*

---

## Workflow

### Phase 1: Parse Feature File

Extract step patterns from the .feature file.

1. Read tests/features/{bead-id}.feature
2. Extract all Given/When/Then step text
3. Identify typed placeholders in steps
4. Group steps by type (Given, When, Then)

**Outputs:** List of unique step patterns, Parameter types for each step

### Phase 2: Match Existing Fixtures

Find fixtures for steps that need test data.

1. Scan tests/fixtures/ for available fixtures
2. Match step patterns to fixture data requirements
3. Note which steps need new fixtures
4. Document fixture gaps (don't create yet)

**Outputs:** Fixture mappings for steps, List of needed fixtures (for proposal)

### Phase 3: Write Step Definitions

Create Rust step definitions using rstest-bdd.

1. Create tests/steps/{feature-name}.rs file
2. Define World struct to hold scenario state
3. Write #[given], #[when], #[then] functions
4. Wire fixture parameters using #[fixture] attribute
5. Add parameter bindings for typed placeholders

**Outputs:** Step definition file, World struct definition

### Phase 4: Wire to Feature

Connect step definitions to feature file.

1. Add #[scenario] attribute linking to .feature file
2. Import fixtures with use statements
3. Verify all steps have implementations
4. Add module to tests/mod.rs

**Outputs:** Complete test module, Integration with test suite

---

## rstest-bdd Syntax Reference

### Step Macros

```rust
use rstest_bdd::{given, when, then, scenario, fixture};

#[given("pattern with <param:type>")]
fn step_name(world: &mut TestWorld, param: Type) {
    // Setup logic
}

#[when("action pattern")]
fn action_step(world: &mut TestWorld) {
    // Action logic
}

#[then("verification pattern")]
fn verify_step(world: &TestWorld) {
    // Assertions
}
```

### Parameter Types

| Gherkin | Rust Type | Binding |
|---------|-----------|---------|
| `<name:string>` | `String` | Direct |
| `<count:int>` | `i32` | Direct |
| `<price:float>` | `f64` | Direct |
| `<flag:word>` | `String` | Single word |
| Table | `Vec<HashMap<String, String>>` | Data table |

### Fixture Injection

```rust
#[fixture]
fn admin_user() -> User {
    serde_yaml::from_str(include_str!("../fixtures/users/admin.fixture.yaml"))
        .expect("admin fixture")
}

#[given("an admin user exists")]
fn admin_exists(world: &mut TestWorld, #[with(admin_user)] user: User) {
    world.user = Some(user);
}
```

### Scenario Binding

```rust
#[scenario(path = "tests/features/example.feature", 
           name = "Scenario Name")]
#[test]
fn example_scenario(world: TestWorld) {
    // Steps execute from feature file
}
```

---

## World Struct Pattern

Every test module needs a World struct to hold state:

```rust
#[derive(Default)]
struct TestWorld {
    // Setup state
    api_client: ApiClient,
    current_user: Option<User>,
    
    // Action results
    response: Option<Response>,
    error: Option<Error>,
    
    // Captured data for verification
    created_id: Option<String>,
}

impl TestWorld {
    fn new() -> Self {
        Self {
            api_client: ApiClient::new(test_config()),
            ..Default::default()
        }
    }
}
```

### State Flow

```
Given steps  -->  Set up world.* fields
When step    -->  Perform action, store result in world.*
Then steps   -->  Assert on world.* fields
```

---

## Patterns

| Pattern | When | Example |
|---------|------|---------|
| **Given Step** | Setup | `world.user = Some(user);` |
| **When Step** | Action | `world.result = api.create_user(&data);` |
| **Then Step** | Verify | `assert!(world.result.is_ok());` |
| **Fixture Injection** | Need test data | `#[with(admin_user)] user: User` |
| **Scenario Binding** | Connect to feature | `#[scenario(path = "...")]` |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Example | Instead |
|--------------|---------|---------|
| **Hardcoded Test Data** | `User { email: "test@test.com" }` | Load from fixture |
| **Creating Fixtures In Steps** | Writing .fixture.yaml during implementation | Propose fixtures, get review |
| **Generic Patterns** | `"I do something"` | `"I create a user with email"` |
| **Global State** | `static mut USER: Option<User>` | Use World struct |
| **Assertions in Given** | `assert!` in Given step | Move to Then step |

---

## Fixture Proposal Protocol

When a step needs a fixture that doesn't exist:

1. **Document the need** in bead notes:
   ```
   FIXTURE PROPOSAL: users/premium-user.fixture.yaml
   - Needed by: "Given a premium user exists" step
   - Fields: id, email, subscription_tier
   - Similar to: users/standard-user.fixture.yaml
   ```

2. **Create a placeholder** in step:
   ```rust
   #[given("a premium user exists")]
   fn premium_exists(world: &mut TestWorld) {
       todo!("Needs fixture: users/premium-user.fixture.yaml")
   }
   ```

3. **Continue with other steps** - don't block on fixture creation

4. **Create fixture** after review approval in separate task

---

## File Organization

```
tests/
  features/
    user-creation.feature
  steps/
    mod.rs              # pub mod user_creation;
    user_creation.rs    # Step definitions
  fixtures/
    users/
      admin.fixture.yaml
```

### Module Structure

```rust
// tests/steps/user_creation.rs
use rstest_bdd::{given, when, then, scenario, fixture};

mod fixtures;

#[derive(Default)]
struct TestWorld { /* ... */ }

// Step definitions...

#[scenario(path = "tests/features/user-creation.feature")]
#[test]
fn user_creation_scenario(_: TestWorld) {}
```

---

## Quality Checklist

Before completing step implementation:

- [ ] All steps from feature file have implementations
- [ ] World struct holds all shared scenario state
- [ ] Fixtures referenced for test data (no hardcoding)
- [ ] Missing fixtures documented for proposal
- [ ] Step patterns use specific domain language
- [ ] #[scenario] attribute links to feature file
- [ ] Module added to tests/mod.rs
- [ ] Tests compile and run (red initially is expected)

---

## Example: Complete Step File

```rust
// tests/steps/user_creation.rs
use rstest_bdd::{given, when, then, scenario, fixture};
use crate::api::UserApi;
use crate::models::User;

#[derive(Default)]
struct TestWorld {
    api: UserApi,
    existing_user: Option<User>,
    result: Result<User, anyhow::Error>,
}

#[fixture]
fn existing_user() -> User {
    serde_yaml::from_str(include_str!("../fixtures/users/existing.fixture.yaml"))
        .expect("existing user fixture")
}

#[given("a user exists with email <email:string>")]
fn user_exists(world: &mut TestWorld, #[with(existing_user)] user: User, email: String) {
    world.api.seed_user(&user);
    world.existing_user = Some(user);
}

#[given("no user exists with email <email:string>")]
fn no_user_exists(world: &mut TestWorld, email: String) {
    world.api.delete_user_by_email(&email).ok();
}

#[when("I create a user with email <email:string> and password <password:string>")]
fn create_user(world: &mut TestWorld, email: String, password: String) {
    world.result = world.api.create_user(&email, &password);
}

#[then("the user should be created successfully")]
fn user_created(world: &TestWorld) {
    assert!(world.result.is_ok(), "Expected success: {:?}", world.result);
}

#[then("the creation should fail with error <error:string>")]
fn creation_fails(world: &TestWorld, error: String) {
    let err = world.result.as_ref().expect_err("Expected failure");
    assert!(err.to_string().contains(&error), 
            "Expected error '{}' but got: {}", error, err);
}

#[scenario(path = "tests/features/user-creation.feature")]
#[test]
fn user_creation_scenarios(_: TestWorld) {}
```

---

## Next Steps

After completing step implementation:

1. Tests should compile but fail (RED state)
2. Invoke **bdd-red-green-refactor** skill for implementation
3. Iterate until all tests pass (GREEN)
4. Clean up code (REFACTOR)

---

## References

- [rstest-bdd documentation](https://github.com/oknozor/rstest-bdd)
- [docs/fixture-registry.md](../docs/fixture-registry.md) - Fixture structure
- [skills/bdd-scenario-design](../skills/bdd-scenario-design/) - Input feature files
- [skills/bdd-red-green-refactor](../skills/bdd-red-green-refactor/) - Next step in workflow
