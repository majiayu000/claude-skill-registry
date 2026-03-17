---
name: code-review
description: 当用户要求"审查代码"、"代码检查"、"检查bug"、"代码质量检查"、"发现问题"、"重构建议"，或者提到"代码审查"、"code review"、"审查"、"检查"时使用此技能。用于代码质量、潜在bug、性能问题、安全漏洞或改进机会的反馈。
version: 2.0.0
---

# Code Review Skill

Comprehensive code review guidance for Tauri + Rust + React applications with focus on quality, security, and maintainability.

## Overview

This skill provides systematic code review guidance covering:
- **Correctness**: Logic errors, edge cases, type safety
- **Performance**: Inefficient algorithms, resource leaks, optimization opportunities
- **Security**: SQL injection, XSS, unsafe operations, data validation
- **Maintainability**: Code duplication, naming, documentation, test coverage
- **Tauri-specific**: Command patterns, specta attributes, desktop app constraints
- **Project-specific**: Adherence to CLAUDE.md guidelines

## When This Skill Applies

This skill activates when:
- Reviewing pull requests or code changes
- Performing code quality checks
- Looking for bugs and issues
- Suggesting refactoring opportunities
- Auditing security vulnerabilities
- Checking performance bottlenecks
- Ensuring compliance with project standards

## Code Review Framework

### 1. Pre-Review Checklist

Before diving into code details:

```bash
# Check git diff context
git diff main...feature-branch
git log --oneline main..feature-branch

# Verify tests pass
cargo test
npm test

# Check formatting
cargo fmt --check
npm run lint
```

**Questions to answer:**
- [ ] What is the purpose of this change?
- [ ] What files are modified? (Use `git diff --stat`)
- [ ] Are there breaking changes?
- [ ] Is test coverage adequate?
- [ ] Does it follow project conventions?

### 2. Rust Backend Review

#### Command Pattern Review

**✅ Correct Tauri Command:**
```rust
#[tauri::command]
#[specta::specta]
pub async fn get_materials(
    state: State<'_, TauriAppState>,
) -> ApiResponse<Vec<Material>> {
    with_service(state, |ctx| async move {
        ctx.material_service.get_all().await
    })
    .await
}
```

**Checklist:**
- [ ] `#[tauri::command]` attribute present
- [ ] `#[specta::specta]` attribute present
- [ ] Return type is `ApiResponse<T>`
- [ ] Uses `with_service` helper or proper error handling
- [ ] Async functions properly use `await`

#### Error Handling Review

**✅ Good Error Handling:**
```rust
pub async fn create_formula(&self, dto: CreateFormulaDto) -> Result<Formula> {
    // Validate input
    if dto.name.is_empty() {
        return Err(anyhow!("名称不能为空"));
    }

    // Check for duplicates
    if self.exists_by_name(&dto.name).await? {
        return Err(anyhow!("配方名称已存在"));
    }

    // Create with transaction
    let mut tx = self.pool.begin().await?;
    let id = self.insert_internal(&dto, &mut tx).await?;
    tx.commit().await?;

    Ok(self.get_by_id(id).await?)
}
```

**Common Issues to Watch For:**
- ❌ Missing error propagation (`?` not used)
- ❌ Swallowing errors (`let _ = result`)
- ❌ Generic error messages without context
- ❌ Not using `.context()` for error chaining
- ❌ Forgetting to commit transactions

#### Database Query Review

**✅ Safe SQLx Query:**
```rust
sqlx::query_as!(
    Material,
    "SELECT code, name, price FROM materials WHERE code = ?",
    code
)
.fetch_one(&pool)
.await
```

**Common Issues:**
- ❌ `SELECT *` - specify columns explicitly
- ❌ N+1 queries in loops
- ❌ String concatenation in SQL (injection risk)
- ❌ Missing parameter binding
- ❌ No indexes on frequently queried fields

#### Performance Review

**Red Flags:**
```rust
// ❌ Blocking async runtime
std::thread::sleep(Duration::from_secs(10));

// ❌ Unnecessary cloning
let data = self.large_data.clone(); // Can use &LargeData

// ❌ Inefficient data structures
let mut items = Vec::new();
for item in huge_list {
    if items.contains(&item) { // O(n) lookup
        items.push(item);
    }
}

// ✅ Use HashSet for O(1) lookups
use std::collections::HashSet;
let mut items = HashSet::new();
```

**Performance Checklist:**
- [ ] Appropriate use of `Arc` vs `&` references
- [ ] Efficient data structures (HashMap, HashSet vs Vec)
- [ ] Parallel processing with `rayon` for CPU-bound tasks
- [ ] Caching for frequently accessed data
- [ ] No blocking calls in async context

### 3. React Frontend Review

#### Component Quality Review

**✅ Well-Structured Component:**
```typescript
import React, { useCallback, useMemo } from 'react';
import { message } from 'antd';

interface Props {
  formula: Formula;
  onUpdate: (id: number) => void;
}

export const FormulaCard: React.FC<Props> = React.memo(({ formula, onUpdate }) => {
  const totalCost = useMemo(
    () => formula.materials.reduce((sum, m) => sum + m.cost, 0),
    [formula.materials]
  );

  const handleUpdate = useCallback(() => {
    onUpdate(formula.id);
  }, [formula.id, onUpdate]);

  return (
    <div>
      <h3>{formula.name}</h3>
      <p>成本: {totalCost.toFixed(2)}</p>
      <Button onClick={handleUpdate}>更新</Button>
    </div>
  );
});
```

**Checklist:**
- [ ] Proper TypeScript types (no `any`)
- [ ] `React.memo` for performance
- [ ] `useCallback` for callbacks passed as props
- [ ] `useMemo` for expensive calculations
- [ ] No `console.log` (use `message` instead)
- [ ] Meaningful component names

#### Hooks Usage Review

**✅ Correct Hooks Usage:**
```typescript
export const useFormulas = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['formulas'],
    queryFn: () => commands.getFormulas(),
  });

  const createMutation = useMutation({
    mutationFn: (dto: CreateDto) => commands.createFormula(dto),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['formulas'] });
      message.success('创建成功');
    },
  });

  return { formulas: data, isLoading, createMutation };
};
```

**Common Issues:**
- ❌ Hooks called inside conditions/loops
- ❌ Missing dependencies in `useEffect`/`useCallback`
- ❌ State mutations instead of `setState`
- ❌ Using raw `invoke` instead of generated `commands`

### 4. Integration Review

#### Frontend-Backend Integration

**Type Safety Check:**
```typescript
// ✅ Using generated types
import type { Formula, Material } from '../bindings';
import { commands } from '../bindings';

const result = await commands.getFormula(123);
if (!result.success) {
    message.error(result.message);
    return;
}
const formula: Formula = result.data; // Type-safe!
```

**Issues to Watch:**
- ❌ Using `as any` type assertions
- ❌ Not checking `result.success`
- ❌ Missing error handling
- ❌ Inconsistent type naming (snake_case vs camelCase)

### 5. Security Review

#### Common Vulnerabilities

**SQL Injection:**
```rust
// ❌ VULNERABLE
let query = format!("SELECT * FROM materials WHERE name = '{}'", name);
sqlx::query(&query).fetch_one(&pool).await

// ✅ SAFE
sqlx::query_as!(
    Material,
    "SELECT * FROM materials WHERE name = ?",
    name
)
.fetch_one(&pool).await
```

**Input Validation:**
```rust
// ❌ No validation
pub fn create_material(name: String, price: f64) -> Result<Material> {
    // Direct insert without checks
}

// ✅ With validation
pub fn create_material(name: String, price: f64) -> Result<Material> {
    if name.is_empty() || name.len() > 100 {
        return Err(anyhow!("无效的原料名称"));
    }
    if price < 0.0 || price > 10000.0 {
        return Err(anyhow!("价格超出合理范围"));
    }
    // Proceed with creation
}
```

**Desktop App Security:**
- [ ] No hardcoded credentials
- [ ] Environment variables for secrets
- [ ] File path validation (prevent directory traversal)
- [ ] Safe handling of user-provided file paths

### 6. Testing Review

#### Test Coverage Check

```rust
// ✅ Good test coverage
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_cost() {
        // Normal case
        assert_eq!(calculate_cost(&materials), 100.0);

        // Edge cases
        assert_eq!(calculate_cost(&[]), 0.0);
        assert_eq!(calculate_cost(&[single_material]), single_material.cost);
    }

    #[test]
    fn test_negative_proportion_rejected() {
        let result = validate_proportion(-10.0);
        assert!(result.is_err());
    }
}
```

**Checklist:**
- [ ] Unit tests for business logic
- [ ] Edge cases covered (empty, null, negative values)
- [ ] Integration tests for database operations
- [ ] Error paths tested
- [ ] Mocking external dependencies

### 7. Documentation Review

**What to Check:**
- [ ] Public APIs have documentation comments
- [ ] Complex algorithms have explanations
- [ ] Non-obvious code has comments
- [ ] TODO/FIXME comments have associated issues
- [ ] README updated if behavior changed

## Code Review Comment Templates

### High Priority Issues

```markdown
## 🔴 Critical: [Issue Title]

**Location**: `src/file.rs:42`

**Problem**: [Clear description of the issue]

**Impact**: [Why this matters]

**Suggested Fix**:
```rust
// Show corrected code
```
```

### Medium Priority Issues

```markdown
## 🟡 Suggestion: [Title]

**Location**: `src/file.rs:123`

**Current Approach**: [What the code does now]

**Recommendation**: [Better approach]

**Benefits**:
- [Benefit 1]
- [Benefit 2]
```

### Minor Issues

```markdown
## 💡 Nitpick: [Title]

**Location**: `src/file.rs:200`

**Observation**: [Small improvement]

**Why it matters**: [Optional explanation]
```

## Common Issues by Category

### Rust Issues

| Issue | Pattern | Fix |
|-------|---------|-----|
| Missing unwrap context | `.unwrap()` | `.expect("Descriptive message")` or proper error handling |
| Cloning instead of borrowing | `.clone()` | Use `&T` reference |
| Blocking async runtime | `std::thread::sleep` | `tokio::time::sleep` |
| SQL injection risk | `format!("WHERE = {}", val)` | Use `?` parameter binding |
| N+1 query | Loop with query inside | Use JOIN or batch query |

### React Issues

| Issue | Pattern | Fix |
|-------|---------|-----|
| Console logging | `console.log()` | Use `message` component |
| Type assertion | `as any` | Use proper types |
| Missing deps | `useEffect(fn, [])` | Add all dependencies |
| Hook in condition | `if (condition) { useState() }` | Move to top level |
| Key prop issue | `key={index}` | Use unique ID |

## Review Workflow

### 1. Automated Checks (Do First)

```bash
# Run all automated checks
cargo test --all
cargo clippy -- -D warnings
cargo fmt --check
npm test
npm run lint
npm run type-check
```

### 2. Manual Review

1. **Read diff top-to-bottom**: Get overall picture
2. **Check critical paths**: Security, performance, correctness
3. **Verify tests**: Ensure adequate coverage
4. **Check documentation**: Is it up to date?
5. **Test manually**: If applicable, run the application

### 3. Provide Feedback

- **Be constructive**: Focus on improvement, not criticism
- **Explain why**: Help author understand the issue
- **Provide examples**: Show how to fix
- **Prioritize**: Mark critical vs. minor issues
- **Be polite**: Remember code reviews are learning opportunities

## Quick Reference

### Essential Commands

```bash
# Review changes
git diff main...feature-branch

# View specific file changes
git diff main..feature-branch -- src/file.rs

# Check commit history
git log --oneline main..feature-branch

# Run tests
cargo test
npm test

# Check formatting
cargo fmt --check
npm run lint
```

### Review Checklist

```
Backend (Rust):
- [ ] Tauri command attributes correct
- [ ] Error handling comprehensive
- [ ] SQL queries safe and optimized
- [ ] Performance considerations addressed
- [ ] No blocking calls in async context

Frontend (React):
- [ ] TypeScript types correct
- [ ] Hooks properly used
- [ ] No console.log
- [ ] Error handling with message
- [ ] Performance optimized

Integration:
- [ ] Type-safe command calls
- [ ] Proper error handling
- [ ] Consistent naming
- [ ] specta types generated

Testing:
- [ ] Unit tests present
- [ ] Edge cases covered
- [ ] Integration tests if needed
- [ ] Tests passing

Documentation:
- [ ] Public APIs documented
- [ ] Complex logic explained
- [ ] README updated
```

## When to Use This Skill

Activate this skill when:
- Reviewing pull requests
- Performing code quality audits
- Looking for bugs and issues
- Suggesting refactoring
- Checking for security vulnerabilities
- Ensuring project standard compliance
- Onboarding developers to codebase
