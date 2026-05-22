---
name: check-repository-pattern
description: Validates database access follows repository pattern, detects god-trait regression, ensures focused repositories
user-invocable: true
---

# Check Repository Pattern Skill

## Purpose
Quick validation that database access follows the repository pattern (commit 6f3efef). Detects god-trait regression and ensures proper use of focused repositories.

## CLAUDE.md Compliance
- ✅ Enforces SOLID principles (Single Responsibility)
- ✅ Validates focused repository usage
- ✅ Prevents monolithic database patterns

## Usage
Run this skill:
- Before committing database changes
- Daily pre-commit validation
- After adding new repositories
- When reviewing database-related PRs

## Prerequisites
- ripgrep (`rg`)

## Commands

### Quick Check (Fast)
```bash
# Check for repository pattern compliance
echo "🔍 Checking repository pattern..."

# 1. Check for DatabaseProvider god-trait (FORBIDDEN)
if rg "trait DatabaseProvider|impl DatabaseProvider" src/ --type rust --quiet; then
    echo "❌ FAIL: DatabaseProvider god-trait detected!"
    rg "DatabaseProvider" src/ --type rust -n | head -10
    exit 1
else
    echo "✓ PASS: No DatabaseProvider god-trait"
fi

# 2. Verify repository directory exists
if [ -d "src/database/repositories" ]; then
    REPO_COUNT=$(ls -1 src/database/repositories/*_repository.rs 2>/dev/null | wc -l)
    echo "✓ PASS: $REPO_COUNT repository files found"
else
    echo "❌ FAIL: Repository directory missing!"
    exit 1
fi

# 3. Check for direct database access in routes (anti-pattern)
if rg "sqlx::query|\.execute\(|\.fetch" src/routes/ --type rust --quiet; then
    echo "⚠️  WARNING: Direct database access in routes detected"
    rg "sqlx::query" src/routes/ --type rust -n | head -5
else
    echo "✓ PASS: No direct database access in routes"
fi

# 4. Verify repository usage
REPO_USAGE=$(rg "Repository" src/routes/ src/protocols/ --type rust | wc -l)
echo "✓ Repository usage: $REPO_USAGE references"

echo ""
echo "✅ Repository pattern check PASSED"
```

## Success Criteria
- ✅ Zero DatabaseProvider trait references
- ✅ All 13 repository files exist
- ✅ Repository files have <25 methods each
- ✅ No direct database access in routes/protocols
- ✅ Repository usage > 50 references

## Expected Output (Success)
```
🔍 Checking repository pattern...
✓ PASS: No DatabaseProvider god-trait
✓ PASS: 13 repository files found
✓ PASS: No direct database access in routes
✓ Repository usage: 127 references

✅ Repository pattern check PASSED
```

## Fixing Violations

### Remove god-trait usage
```rust
// ❌ Before
async fn handler(
    Extension(db): Extension<Arc<dyn DatabaseProvider>>,
) -> AppResult<Json<User>> {
    let user = db.get_user(id).await?;
    Ok(Json(user))
}

// ✅ After
async fn handler(
    Extension(user_repo): Extension<Arc<dyn UserRepository>>,
) -> AppResult<Json<User>> {
    let user = user_repo.get_by_id(id).await?
        .ok_or(AppError::new(
            ErrorCode::ResourceNotFound,
            format!("User {} not found", id)
        ))?;
    Ok(Json(user))
}
```

### Replace direct database access
```rust
// ❌ Before (direct sqlx usage in route)
async fn get_user(
    Extension(pool): Extension<Arc<Pool<Database>>>,
    Path(id): Path<Uuid>,
) -> AppResult<Json<User>> {
    let user = sqlx::query_as::<_, User>(
        "SELECT * FROM users WHERE id = $1"
    )
    .bind(id)
    .fetch_one(&*pool)
    .await?;
    Ok(Json(user))
}

// ✅ After (use repository)
async fn get_user(
    Extension(user_repo): Extension<Arc<dyn UserRepository>>,
    Path(id): Path<Uuid>,
) -> AppResult<Json<User>> {
    let user = user_repo.get_by_id(id).await?
        .ok_or(AppError::new(
            ErrorCode::ResourceNotFound,
            format!("User {} not found", id)
        ))?;
    Ok(Json(user))
}
```

## Related Files
- `src/database/repositories/mod.rs` - Repository traits
- `src/database/repositories/*_repository.rs` - 13 implementations
- Commit 6f3efef - Repository pattern migration

## Related Agents
- `repository-pattern-guardian` - Comprehensive repository validation

## Quick Reference

```bash
# One-line check
rg "trait DatabaseProvider" src/ --type rust && echo "FAIL" || echo "PASS"

# Check repository count
ls -1 src/database/repositories/*_repository.rs | wc -l

# Check for direct database access
rg "sqlx::query" src/routes/ --type rust && echo "WARNING" || echo "PASS"

# Repository usage count
rg "Repository" src/routes/ src/protocols/ --type rust | wc -l
```
