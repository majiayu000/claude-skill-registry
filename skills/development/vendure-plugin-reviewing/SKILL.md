---
name: vendure-plugin-reviewing
description: Review Vendure plugins for best practices violations. Detects missing decorators, improper DI, hardcoded config, lifecycle hook issues, and service anti-patterns. Use when reviewing plugin PRs or auditing plugin quality.
version: 1.0.0
---

# Vendure Plugin Reviewing

## Purpose

Audit Vendure plugins for violations of best practices, security issues, and anti-patterns.

## When NOT to Use

- Creating new plugins (use vendure-plugin-writing)
- GraphQL-only review (use vendure-graphql-reviewing)
- Entity-only review (use vendure-entity-reviewing)

---

## Review Workflow

### Step 1: Identify Plugin Files

```bash
# Find all plugin files
find . -name "*.plugin.ts" -o -name "*-plugin.ts"

# Find all service files
find . -name "*.service.ts"

# Find all entity files
find . -name "*.entity.ts"
```

### Step 2: Run Automated Checks

```bash
# === CRITICAL VIOLATIONS ===

# Missing @VendurePlugin decorator
grep -rn "export class.*Plugin" --include="*plugin.ts" | grep -v "@VendurePlugin"

# Missing PluginCommonModule import
grep -rn "@VendurePlugin" --include="*plugin.ts" -A 10 | grep -v "PluginCommonModule"

# Direct database access (bypassing TransactionalConnection)
grep -rn "getRepository\|createQueryBuilder\|getConnection" --include="*.service.ts" | grep -v "TransactionalConnection"

# === HIGH PRIORITY ===

# Missing @Injectable on services
grep -rn "export class.*Service" --include="*.service.ts" | grep -v "@Injectable"

# Hardcoded configuration values
grep -rn "localhost\|127.0.0.1\|apiKey.*=.*['\"]" --include="*.plugin.ts" --include="*.service.ts"

# Missing RequestContext parameter
grep -rn "async.*\(" --include="*.service.ts" | grep -v "ctx.*RequestContext\|RequestContext.*ctx"

# === MEDIUM PRIORITY ===

# Missing init() static method
grep -rn "export class.*Plugin" --include="*plugin.ts" -A 20 | grep -v "static init"

# Missing default options
grep -rn "this.options = options" --include="*plugin.ts" | grep -v "...default\|...options"

# Missing lifecycle cleanup
grep -rn "onApplicationBootstrap" --include="*plugin.ts" | xargs -I{} sh -c 'grep -L "onApplicationShutdown" {} 2>/dev/null'
```

### Step 3: Manual Review Checklist

#### Plugin Structure

- [ ] @VendurePlugin decorator present
- [ ] PluginCommonModule in imports
- [ ] All entities in entities array
- [ ] All services in providers array
- [ ] Static init() method with defaults
- [ ] Options interface with types

#### Services

- [ ] @Injectable() decorator on all services
- [ ] RequestContext as first parameter
- [ ] TransactionalConnection for DB access
- [ ] No direct TypeORM repository access
- [ ] Proper error handling

#### Lifecycle

- [ ] OnApplicationBootstrap if initialization needed
- [ ] OnApplicationShutdown if cleanup needed
- [ ] Async/await on lifecycle methods
- [ ] Strategy init() calls in bootstrap

#### Configuration

- [ ] Options interface defined
- [ ] Default values for all options
- [ ] No hardcoded secrets
- [ ] Environment variable usage for sensitive data

---

## Severity Classification

### CRITICAL (Must Fix Before Merge)

- Missing @VendurePlugin decorator
- Direct database access bypassing services
- Missing PluginCommonModule import
- Hardcoded secrets or API keys
- Security vulnerabilities

### HIGH (Should Fix Before Merge)

- Missing @Injectable decorator
- Missing RequestContext in service methods
- Hardcoded configuration values
- Missing error handling
- No default options

### MEDIUM (Should Fix)

- Missing lifecycle cleanup (shutdown)
- No configuration validation
- Poor naming conventions
- Missing TypeScript types

### LOW (Suggestions)

- Missing documentation
- Could use better error messages
- Performance improvements possible

---

## Review Output Template

```markdown
## Vendure Plugin Review: [Plugin Name]

### Summary

[Brief overview of plugin purpose and review findings]

### Critical Issues (Must Fix)

- [ ] [Issue description] - `file:line`

### High Priority

- [ ] [Issue description] - `file:line`

### Medium Priority

- [ ] [Issue description] - `file:line`

### Passed Checks

- [x] @VendurePlugin decorator present
- [x] PluginCommonModule imported
- [x] All services @Injectable

### Recommendations

- [Improvement suggestions]
```

---

## Common Violations

### 1. Missing PluginCommonModule

**Violation:**

```typescript
@VendurePlugin({
  imports: [],  // Missing PluginCommonModule!
  providers: [MyService],
})
```

**Fix:**

```typescript
@VendurePlugin({
  imports: [PluginCommonModule],
  providers: [MyService],
})
```

### 2. Direct Database Access

**Violation:**

```typescript
@Injectable()
export class MyService {
  constructor(
    @InjectRepository(MyEntity) // WRONG
    private repo: Repository<MyEntity>,
  ) {}
}
```

**Fix:**

```typescript
@Injectable()
export class MyService {
  constructor(
    private connection: TransactionalConnection, // CORRECT
  ) {}

  async findAll(ctx: RequestContext) {
    return this.connection.getRepository(ctx, MyEntity).find();
  }
}
```

### 3. Missing RequestContext

**Violation:**

```typescript
async findAll(): Promise<MyEntity[]> {  // Missing ctx!
  return this.connection.getRepository(MyEntity).find();
}
```

**Fix:**

```typescript
async findAll(ctx: RequestContext): Promise<MyEntity[]> {
  return this.connection.getRepository(ctx, MyEntity).find();
}
```

### 4. Hardcoded Options

**Violation:**

```typescript
static init(options: MyOptions): typeof MyPlugin {
  this.options = options;  // No defaults!
  return MyPlugin;
}
```

**Fix:**

```typescript
static init(options: MyOptions = {}): typeof MyPlugin {
  this.options = {
    ...defaultOptions,  // Always merge with defaults
    ...options,
  };
  return MyPlugin;
}
```

### 5. Strategy Without Lifecycle

**Violation:**

```typescript
static init(options: { strategy: MyStrategy }) {
  this.options = options;
  // Strategy init() never called!
}
```

**Fix:**

```typescript
async onApplicationBootstrap(): Promise<void> {
  if (typeof MyPlugin.options.strategy.init === 'function') {
    await MyPlugin.options.strategy.init(this.injector);
  }
}
```

---

## Quick Detection Commands

```bash
# All-in-one audit script
echo "=== CRITICAL ===" && \
grep -rn "export class.*Plugin" --include="*plugin.ts" | grep -v "@VendurePlugin" && \
echo "=== HIGH ===" && \
grep -rn "export class.*Service" --include="*.service.ts" | grep -v "@Injectable" && \
echo "=== MEDIUM ===" && \
grep -rn "TODO\|FIXME\|HACK" --include="*.ts"
```

---

## Cross-Reference

All rules in this skill match patterns documented in **vendure-plugin-writing** skill.

When reviewing, verify the plugin follows the patterns in:

- vendure-plugin-writing (plugin structure)
- vendure-graphql-writing (if has API extensions)
- vendure-entity-writing (if has entities)
- vendure-admin-ui-writing (if has UI extensions)

---

## Related Skills

- **vendure-plugin-writing** - Plugin creation patterns
- **vendure-graphql-reviewing** - GraphQL-specific review
- **vendure-entity-reviewing** - Entity-specific review
- **vendure-admin-ui-reviewing** - UI-specific review
