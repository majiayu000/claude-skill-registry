# BDD Scenario Evolution Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-25

Maintain scenarios and fixtures as code evolves.

## When to Activate

Use this skill when:
- Requirements changed
- Update scenarios
- Scenario maintenance
- Fixture drift detected
- Refactor step definitions
- Code review scenario feedback

## Core Principles

### 1. Scenarios Track Requirements

When requirements change, scenarios must change; when scenarios diverge from requirements, scenarios are wrong.

*Scenarios are executable requirements, not independent artifacts.*

### 2. Preserve Regression Coverage

When updating scenarios, ensure previously-covered behaviors remain tested.

*Losing coverage creates regression risk.*

### 3. Step Definition Reuse

Similar steps across scenarios should use shared definitions.

*Duplication in step definitions leads to inconsistent behavior and maintenance burden.*

### 4. Fixture Currency

Fixtures must reflect current system state; stale fixtures cause false failures.

*Tests that fail due to outdated fixtures erode trust in the test suite.*

---

## Workflow

### Phase 1: Assess Change Scope

Understand what changed and its impact on scenarios.

1. Review the change (new requirement, bug fix, refactor)
2. Identify affected scenarios
3. Determine if change adds, modifies, or removes behavior
4. Check for fixture implications

**Outputs:** List of affected scenarios, Type of change, Fixture impact assessment

### Phase 2: Update Scenarios

Modify scenarios to reflect new reality.

1. For added behavior, create new scenarios
2. For modified behavior, update existing scenarios
3. For removed behavior, delete obsolete scenarios
4. Verify prose acceptance criteria still satisfied

**Outputs:** Updated feature files, Obsolete scenarios removed

### Phase 3: Update Step Definitions

Evolve step definitions to match scenarios.

1. Add new steps for new scenarios
2. Modify steps if behavior changed
3. Look for reuse opportunities across features
4. Remove orphan step definitions

**Outputs:** Updated step files, Consolidated step definitions

### Phase 4: Update Fixtures

Keep fixtures current with system.

1. Identify fixtures affected by change
2. Update fixture data to match new schema/format
3. Remove obsolete fixtures
4. Add new fixtures if needed (following proposal protocol)

**Outputs:** Current fixtures, Fixture registry updated

### Phase 5: Verify Coverage

Confirm no regression in test coverage.

1. Run full test suite
2. Review deleted scenarios for coverage gaps
3. Check if removed scenarios were intentional
4. Document any coverage reduction with justification

**Outputs:** All tests passing, Coverage verification

---

## Change Types

### Additive Change

Adding new functionality without modifying existing behavior.

| Step | Action |
|------|--------|
| Scenarios | Add new scenarios for new behaviors |
| Steps | Add new step definitions |
| Fixtures | Add new fixtures as needed |
| Existing | Leave unchanged |

### Behavioral Modification

Changing how existing functionality works.

| Step | Action |
|------|--------|
| Scenarios | Update expectations in existing scenarios |
| Steps | Modify step implementations |
| Fixtures | Update fixture data if format changed |
| Coverage | Should remain unchanged |

### Removal/Deprecation

Removing functionality from the system.

| Step | Action |
|------|--------|
| Scenarios | Delete scenarios for removed behavior |
| Steps | Remove orphan step definitions |
| Fixtures | Archive (move to deprecated/) |
| Coverage | Document intentional reduction |

---

## Patterns

| Pattern | When | Do |
|---------|------|-----|
| **Additive Change** | New functionality | Add scenarios, existing unchanged |
| **Behavioral Modification** | Changing existing | Update expectations in place |
| **Removal** | Deprecating | Delete scenarios, document why |
| **Refactoring Steps** | Duplicate steps | Extract to shared module |
| **Fixture Refresh** | Schema change | Update fixture data format |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| **Scenario Hoarding** | Keep obsolete scenarios | Delete, use VCS for history |
| **Copy-Paste Steps** | Duplicate definitions | Extract shared steps |
| **Fixture Neglect** | Ignore validation warnings | Treat as bugs |
| **Silent Coverage Reduction** | Remove without documenting | Always document why |
| **Scenario Drift** | Diverge from requirements | Reconcile after changes |

---

## Fixture Governance

### Fixture Lifecycle

```
PROPOSED -> ACTIVE -> DEPRECATED -> ARCHIVED -> DELETED
```

### Actions by State

| State | Location | Action |
|-------|----------|--------|
| Active | tests/fixtures/ | Normal use |
| Deprecated | tests/fixtures/ + deprecated tag | Warn on use |
| Archived | tests/fixtures/deprecated/ | Don't use, keep for reference |
| Deleted | Removed | Gone (in git history) |

### Deprecation Protocol

```yaml
# tests/fixtures/legacy/old-format.fixture.yaml
_meta:
  name: old-format
  deprecated: true
  deprecated_by: fixtures/new/current-format.fixture.yaml
  deprecated_reason: Schema updated in v2.0
```

---

## Step Definition Consolidation

### Identifying Duplicates

Look for:
- Same step text in multiple files
- Similar step text with minor variations
- Steps that could be parameterized

### Extraction Process

1. Create `tests/steps/shared/` directory
2. Move common steps to shared module
3. Update imports in feature-specific files
4. Remove duplicates
5. Run tests to verify

### Shared Steps Module

```rust
// tests/steps/shared/auth.rs
#[given("I am authenticated as <role:word>")]
pub fn authenticated_as(world: &mut TestWorld, role: String) {
    world.auth_token = get_token_for_role(&role);
}

#[given("I am not authenticated")]
pub fn not_authenticated(world: &mut TestWorld) {
    world.auth_token = None;
}
```

---

## Coverage Tracking

### Before Removing Scenarios

Ask:
1. Why was this scenario originally added?
2. Is the behavior it tests still needed?
3. If not, is there documentation of the decision?

### Documenting Coverage Changes

In bead notes:
```
COVERAGE CHANGE:
- Removed: "check payment should succeed" scenario
- Reason: Check payment support deprecated per ADR-042
- Risk Assessment: Low - feature unused for 6 months
- Approval: Product sign-off on 2026-01-15
```

### Coverage Review Triggers

- Deleting more than 2 scenarios
- Removing an entire feature file
- Refactoring that changes step behavior

---

## Quality Checklist

Before completing scenario evolution:

- [ ] Identified all affected scenarios
- [ ] Updated scenarios match new requirements
- [ ] Prose acceptance criteria still satisfied
- [ ] Step definitions consolidated (no duplicates)
- [ ] Fixtures updated to current schema
- [ ] Obsolete scenarios/steps/fixtures removed
- [ ] Coverage reduction documented if any
- [ ] Full test suite passes

---

## Example: Adding Email Verification

**Change:** Users now require email verification before activation.

### 1. Assess Impact

- Affected scenarios: User creation, user login
- Change type: Behavioral modification + addition
- Fixtures: Need pending-user, update active-user

### 2. Update Scenarios

```gherkin
# Before
Scenario: Creating user with valid data should succeed
  When I create a user with valid data
  Then the user should be created successfully
  And the user should be able to authenticate

# After
Scenario: Creating user with valid data should create pending user
  When I create a user with valid data
  Then the user should be created in pending state
  And the user should not be able to authenticate

Scenario: User should become active after email verification
  Given a pending user exists
  When the user verifies their email
  Then the user should become active
  And the user should be able to authenticate
```

### 3. Update Steps

- Modify creation step to check pending status
- Add verification step

### 4. Update Fixtures

```yaml
# New: tests/fixtures/users/pending-user.fixture.yaml
_meta:
  name: pending-user
  description: User awaiting email verification

id: "user-pending-001"
email: "pending@example.com"
status: "pending"
verified_at: null
```

### 5. Verify

```bash
$ cargo test
running 15 tests
... all pass
```

---

## References

- [docs/fixture-registry.md](../docs/fixture-registry.md) - Fixture governance
- [skills/bdd-scenario-design](../skills/bdd-scenario-design/) - Scenario creation
- [skills/fixture-validate](../skills/fixture-validate/) - Fixture validation
