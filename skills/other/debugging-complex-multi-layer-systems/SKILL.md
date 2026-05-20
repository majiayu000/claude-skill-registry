---
name: debugging-complex-multi-layer-systems
description: A reasoning pattern for diagnosing and fixing bugs that span multiple abstraction layers in complex systems.
---

# Layered Bug Diagnosis Pattern

Use this reasoning pattern when fixing one bug reveals another bug in the same operation, or when debugging complex multi-layer systems.

## Pattern Recognition Triggers

Invoke this pattern when:

- Fixing a bug doesn't resolve the user-visible issue
- Test case passes but integration still fails
- Error messages change after initial fix (sign of layered issues)
- Operation involves 3+ abstraction layers (UI → Service → Data → External)
- Symptoms appear in one layer but root cause may be elsewhere

## Core Methodology

### Phase 1: Map the Layers

Identify all abstraction layers involved in the failing operation:

```
Example: iMi PR Worktree Creation

Layer 1: CLI Command Handler (main.rs::handle_review_command)
         ↓ calls
Layer 2: Worktree Manager (worktree.rs::create_pr_worktree_with_gh)
         ↓ calls
Layer 3: Git Manager (git.rs::checkout_pr)
         ↓ calls
Layer 4: External Tools (gh CLI, git commands)
         ↓ affects
Layer 5: Filesystem State (directories, .git metadata)
```

**Key Question:** Which layer owns each symptom?

- Wrong repository location → Layer 2 (Worktree Manager resolution)
- Branch checkout side effect → Layer 3 (Git Manager implementation)

### Phase 2: Symptom Assignment

Map each observable symptom to its originating layer:

| Symptom                             | Layer | Type           |
| ----------------------------------- | ----- | -------------- |
| Worktree created in wrong directory | 2     | Architectural  |
| Trunk switched to PR branch         | 3     | Implementation |
| "Branch already used" error         | 3     | Implementation |

**Pattern:** Architectural issues (wrong entity, wrong location) originate in higher layers. Implementation issues (side effects, race conditions) originate in lower layers.

### Phase 3: Fix Order Strategy

**Rule:** Fix top-down (highest layer first)

**Rationale:**

- Higher layer bugs often make lower layer bugs untestable
- Architectural fixes clarify constraints for implementation fixes
- Lower layer fixes may become unnecessary once architecture corrects

**Example Sequence:**

1. Fix Layer 2: Resolve to correct repository before operations
2. Test → reveals Layer 3 bug
3. Fix Layer 3: Fetch PR without checkout side effect
4. Test → operation succeeds

**Anti-pattern:** Fixing Layer 3 first

- Worktree created in correct repo (Layer 2 fixed)
- But trunk still gets corrupted (Layer 3 unfixed)
- Now debugging corruption in the _right_ repo instead of wrong repo
- Wastes time on compounded issues

### Phase 4: Isolation Testing

After each layer fix, test **only that layer's contract**:

```rust
// Layer 2 test: Repository resolution
#[test]
fn test_resolve_repo_from_github_format() {
    let manager = create_test_manager();
    let resolved = manager.resolve_repo_name(Some("YIC-Triumph/trinote2.0")).await?;
    assert_eq!(resolved, "trinote2.0");

    let db_repo = manager.db.get_repository(&resolved).await?.unwrap();
    assert!(db_repo.remote_url.contains("YIC-Triumph/trinote2.0"));
}

// Layer 3 test: PR fetch without checkout
#[test]
fn test_fetch_pr_without_trunk_corruption() {
    let repo = setup_test_repo();
    let trunk_branch = get_current_branch(&repo);

    git_manager.checkout_pr(&repo_path, 458, &worktree_path)?;

    let trunk_branch_after = get_current_branch(&repo);
    assert_eq!(trunk_branch, trunk_branch_after); // Trunk unchanged
    assert!(worktree_path.exists()); // Worktree created
}
```

### Phase 5: Integration Validation

Only after all layer fixes, run end-to-end test:

```rust
#[tokio::test]
async fn test_pr_worktree_cross_repo_integration() {
    // Setup: User in repo A
    env::set_current_dir("/home/delorenj/code/iMi/trunk-main")?;

    // Action: Create PR worktree in repo B
    let result = manager.create_review_worktree(458, Some("YIC-Triumph/trinote2.0")).await?;

    // Verify Layer 2: Correct repo
    assert!(result.starts_with("/home/delorenj/code/trinote2.0/pr-458"));

    // Verify Layer 3: No trunk corruption
    let repo_b_trunk = Repository::open("/home/delorenj/code/trinote2.0/trunk-main")?;
    assert_eq!(get_current_branch(&repo_b_trunk), "main");

    let repo_a_trunk = Repository::open("/home/delorenj/code/iMi/trunk-main")?;
    assert_eq!(get_current_branch(&repo_a_trunk), "main");
}
```

## Diagnostic Decision Tree

```
[Symptom: Operation fails with error X]
    ↓
[Run operation, capture full error trace]
    ↓
[Identify deepest layer in stack trace]
    ↓
[Is error in expected layer for this symptom?]
    ├─ Yes → Single-layer bug, fix directly
    └─ No → Layered bug, start mapping
        ↓
    [Map all layers involved]
        ↓
    [Identify symptoms at each layer]
        ↓
    [Start fixing from highest layer]
        ↓
    [Test layer contract]
        ├─ Pass → Move to next layer
        └─ Fail → Iterate on current layer
            ↓
        [All layers fixed?]
            ├─ No → Continue fixing next layer
            └─ Yes → Integration test
```

## Common Layer Patterns

### Data Layer Issues

**Symptoms:** Wrong entity retrieved, missing relationships, stale cache
**Fix Strategy:** Query validation, cache invalidation, data integrity checks

### Business Logic Layer Issues

**Symptoms:** Wrong calculation, incorrect state transition, missing validation
**Fix Strategy:** Unit tests for edge cases, state machine verification

### API/Interface Layer Issues

**Symptoms:** Wrong parameters passed, incorrect serialization, broken contracts
**Fix Strategy:** Contract tests, schema validation, integration tests

### External System Layer Issues

**Symptoms:** Unexpected side effects, race conditions, resource conflicts
**Fix Strategy:** Isolation (don't rely on side effects), idempotency, retries

## Real-World Example: This iMi Bug

### Initial State

- User reports: PR worktree created in wrong repository

### Layer Mapping

```
Layer 1: CLI (main.rs) ✓ Correct - passes repo argument
Layer 2: Manager (worktree.rs) ✗ Bug - uses current_dir() instead of resolving repo
Layer 3: Git (git.rs) ✗ Hidden bug - gh pr checkout has side effect
Layer 4: External (gh CLI) ✓ Correct - works as designed
```

### Fix Sequence

1. **Fixed Layer 2 first:** Resolve repo from database before operations
   - Test: `imi pr 458 YIC-Triumph/trinote2.0` from iMi directory
   - Result: Error changed - now trying to create in trinote2.0 but getting "branch already used"

2. **This revealed Layer 3 bug:** Side effect in checkout_pr
   - Investigation: `gh pr checkout` was switching trunk to PR branch
   - Root cause: Checkout happens in trunk directory before worktree creation

3. **Fixed Layer 3:** Replace checkout with fetch
   - Changed from: `gh pr checkout` (side effect)
   - Changed to: `gh pr view` + `git fetch` (no side effect)
   - Test: Trunk remains on main, worktree created successfully

### Lessons

- Fixing Layer 2 first was correct - architectural before implementation
- Layer 3 bug was untestable until Layer 2 worked correctly
- Both bugs were necessary to fix, but order mattered for efficiency

## Anti-Patterns to Avoid

### 1. Bottom-Up Fixing

**Mistake:** Start with lowest layer because "it's simpler"
**Problem:** Higher layer bug may make lower layer fix irrelevant

### 2. Shotgun Debugging

**Mistake:** Change multiple layers simultaneously
**Problem:** Can't isolate which fix resolved which symptom

### 3. Symptom Whack-a-Mole

**Mistake:** Fix each new error as it appears without mapping layers
**Problem:** Never address root architectural issues

### 4. Premature Integration Testing

**Mistake:** Only run end-to-end tests, no layer isolation
**Problem:** Can't determine which layer failed when integration breaks

## Documentation Template

When encountering layered bugs, document:

```markdown
## Bug Report: [Operation] fails with [Symptom]

### Layer Mapping

- Layer N: [Component] - Status: [✓/✗] - Issue: [description]
- Layer N-1: [Component] - Status: [✓/✗] - Issue: [description]
  ...

### Fix Order

1. Fixed [Layer X]: [What changed]
   - Test result: [Pass/Fail/Revealed Layer Y bug]
2. Fixed [Layer Y]: [What changed]
   - Test result: [Pass/Fail]

### Root Causes

- [Layer X]: [Architectural/Implementation] - [Reason]
- [Layer Y]: [Architectural/Implementation] - [Reason]

### Tests Added

- [Layer X contract test]: `test_name_x()`
- [Layer Y contract test]: `test_name_y()`
- [Integration test]: `test_name_integration()`
```

## Related Skills

- `git-state-recovery`: For Layer 5 (filesystem state) issues
- `ecosystem-patterns`: For architectural layer decisions
- `debugging`: For investigation techniques at each layer
