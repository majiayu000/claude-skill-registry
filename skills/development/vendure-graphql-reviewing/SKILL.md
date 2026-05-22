---
name: vendure-graphql-reviewing
description: Review Vendure GraphQL resolvers for missing RequestContext, improper permissions, DTO violations, and schema extension issues. Use when reviewing GraphQL PRs or auditing API quality.
version: 1.0.0
---

# Vendure GraphQL Reviewing

## Purpose

Audit Vendure GraphQL resolvers and schema extensions for violations and anti-patterns.

## Review Workflow

### Step 1: Identify GraphQL Files

```bash
# Find resolver files
find . -name "*.resolver.ts"

# Find schema files
find . -name "schema.ts" -o -name "*.graphql"
```

### Step 2: Run Automated Checks

```bash
# === CRITICAL VIOLATIONS ===

# Missing @Ctx() RequestContext
grep -rn "@Query\|@Mutation" --include="*.resolver.ts" -A 5 | grep -v "@Ctx()"

# Missing @Resolver decorator
grep -rn "export class.*Resolver" --include="*.resolver.ts" | grep -v "@Resolver"

# Missing @Allow permissions
grep -rn "@Query\|@Mutation" --include="*.resolver.ts" -A 3 | grep -v "@Allow"

# === HIGH PRIORITY ===

# Direct entity returns (should use DTOs or proper types)
grep -rn "Promise<.*Entity>" --include="*.resolver.ts"

# Missing @Transaction on mutations
grep -rn "@Mutation" --include="*.resolver.ts" -A 2 | grep -v "@Transaction"

# InputMaybe not handled correctly
grep -rn "!== undefined" --include="*.service.ts" | grep -v "&& .* !== null"

# === MEDIUM PRIORITY ===

# Hardcoded permission strings
grep -rn "@Allow(['\"]" --include="*.resolver.ts"

# Missing error handling
grep -rn "async.*@Ctx" --include="*.resolver.ts" -A 10 | grep -v "throw\|catch\|try"
```

### Step 3: Manual Review Checklist

#### Schema

- [ ] Uses gql template literal
- [ ] Input types for all mutations
- [ ] Proper type definitions
- [ ] Admin vs Shop separation clear
- [ ] No sensitive fields in Shop API

#### Resolvers

- [ ] @Resolver() decorator present
- [ ] @Ctx() ctx: RequestContext on all methods
- [ ] @Allow() with appropriate permissions
- [ ] @Transaction() on mutations
- [ ] Service injection (not direct DB access)

#### Security

- [ ] Shop API doesn't expose admin data
- [ ] Owner permission checked for user resources
- [ ] Input validation present
- [ ] Error messages don't leak sensitive info

---

## Severity Classification

### CRITICAL (Must Fix)

- Missing RequestContext parameter
- No permission decorators
- Shop API exposes admin data
- Direct database access in resolvers

### HIGH (Should Fix)

- Missing @Transaction on mutations
- InputMaybe not handled correctly
- No error handling
- Entity types returned directly

### MEDIUM (Should Fix)

- Missing input validation
- Poor error messages
- Inconsistent naming

---

## Common Violations

### 1. Missing RequestContext

**Violation:**

```typescript
@Query()
@Allow(Permission.ReadSettings)
async myQuery(): Promise<MyEntity[]> {  // No ctx!
  return this.service.findAll();
}
```

**Fix:**

```typescript
@Query()
@Allow(Permission.ReadSettings)
async myQuery(@Ctx() ctx: RequestContext): Promise<MyEntity[]> {
  return this.service.findAll(ctx);
}
```

### 2. Missing Permission Decorator

**Violation:**

```typescript
@Query()
async myQuery(@Ctx() ctx: RequestContext): Promise<MyEntity[]> {
  // No @Allow - anyone can call this!
  return this.service.findAll(ctx);
}
```

**Fix:**

```typescript
@Query()
@Allow(Permission.ReadSettings)  // Explicit permission
async myQuery(@Ctx() ctx: RequestContext): Promise<MyEntity[]> {
  return this.service.findAll(ctx);
}
```

### 3. InputMaybe Bug

**Violation:**

```typescript
// Only checks undefined, null passes through!
if (input.name !== undefined) {
  entity.name = input.name;
}
```

**Fix:**

```typescript
// Check both undefined AND null
if (input.name !== undefined && input.name !== null) {
  entity.name = input.name;
}
```

### 4. Missing Transaction

**Violation:**

```typescript
@Mutation()
@Allow(Permission.UpdateSettings)
async updateData(@Ctx() ctx: RequestContext, @Args() args): Promise<MyEntity> {
  // No @Transaction - partial updates possible on error!
  await this.service.updateA(ctx, args);
  await this.service.updateB(ctx, args);  // If this fails, A is updated
}
```

**Fix:**

```typescript
@Mutation()
@Transaction()  // Atomic operation
@Allow(Permission.UpdateSettings)
async updateData(@Ctx() ctx: RequestContext, @Args() args): Promise<MyEntity> {
  await this.service.updateA(ctx, args);
  await this.service.updateB(ctx, args);
}
```

### 5. Shop API Leaking Admin Data

**Violation:**

```typescript
// Shop schema
const shopSchema = gql`
  type User {
    id: ID!
    email: String!
    internalNotes: String! # Admin-only field exposed!
  }
`;
```

**Fix:**

```typescript
// Shop schema - limited fields
const shopSchema = gql`
  type User {
    id: ID!
    email: String!
    # internalNotes excluded
  }
`;
```

---

## Quick Detection Commands

```bash
# All-in-one GraphQL audit
echo "=== CRITICAL: Missing @Ctx ===" && \
grep -rn "@Query\|@Mutation" --include="*.resolver.ts" -A 5 | grep -v "@Ctx" | head -20 && \
echo "" && \
echo "=== HIGH: Missing @Allow ===" && \
grep -rn "@Query\|@Mutation" --include="*.resolver.ts" -A 3 | grep -v "@Allow" | head -20 && \
echo "" && \
echo "=== MEDIUM: InputMaybe issues ===" && \
grep -rn "!== undefined" --include="*.ts" | grep -v "&& .* !== null" | head -20
```

---

## Review Output Template

```markdown
## GraphQL Review: [Component Name]

### Summary

[Overview of GraphQL code quality]

### Critical Issues (Must Fix)

- [ ] [Issue] - `file:line`

### High Priority

- [ ] [Issue] - `file:line`

### Passed Checks

- [x] All resolvers have @Resolver decorator
- [x] RequestContext passed consistently
- [x] Permissions declared

### Recommendations

- [Suggestions]
```

---

## Cross-Reference

All rules match patterns in **vendure-graphql-writing** skill.

---

## Related Skills

- **vendure-graphql-writing** - GraphQL patterns
- **vendure-plugin-reviewing** - Plugin-level review
