---
name: vendure-entity-reviewing
description: Review Vendure entities for missing VendureEntity inheritance, improper decorators, missing migrations, index violations, and TypeORM anti-patterns. Use when reviewing entity PRs or auditing data models.
version: 1.0.0
---

# Vendure Entity Reviewing

## Purpose

Audit Vendure entities for violations and TypeORM anti-patterns.

## Review Workflow

### Step 1: Identify Entity Files

```bash
# Find entity files
find . -name "*.entity.ts"

# Find migration files
find . -name "*migration*.ts" -o -name "*Migration*.ts"
```

### Step 2: Run Automated Checks

```bash
# === CRITICAL VIOLATIONS ===

# Not extending VendureEntity
grep -rn "export class.*Entity" --include="*.entity.ts" | grep -v "extends VendureEntity"

# Missing @Entity decorator
grep -rn "export class.*Entity" --include="*.entity.ts" | grep -v "@Entity"

# Direct repository injection (should use TransactionalConnection)
grep -rn "@InjectRepository" --include="*.service.ts"

# === HIGH PRIORITY ===

# Missing indexes on foreign keys
grep -rn "@ManyToOne\|@OneToMany" --include="*.entity.ts" -B 2 | grep -v "@Index"

# Missing DeepPartial constructor
grep -rn "export class.*extends VendureEntity" --include="*.entity.ts" -A 5 | grep -v "DeepPartial"

# Using 'any' type
grep -rn ": any" --include="*.entity.ts"

# === MEDIUM PRIORITY ===

# Missing nullable specification
grep -rn "@Column()" --include="*.entity.ts" | head -20

# Date stored as string (should be timestamp)
grep -rn "type: 'varchar'.*[dD]ate\|[dD]ate.*type: 'varchar'" --include="*.entity.ts"
```

### Step 3: Manual Review Checklist

#### Entity Structure

- [ ] Extends VendureEntity
- [ ] @Entity() decorator present
- [ ] DeepPartial<T> constructor
- [ ] Proper column types
- [ ] Nullable specified where needed

#### Relations

- [ ] @Index on foreign key columns
- [ ] Cascade options appropriate
- [ ] OnDelete behavior specified
- [ ] Eager loading only where necessary

#### Migrations

- [ ] Migration file exists for new entities
- [ ] Migration has both up() and down()
- [ ] Indexes created in migration
- [ ] Column types match entity

---

## Severity Classification

### CRITICAL (Must Fix)

- Not extending VendureEntity
- Missing @Entity decorator
- Direct repository injection
- No migration for schema change

### HIGH (Should Fix)

- Missing index on foreign key
- No DeepPartial constructor
- Using any type
- Missing onDelete behavior

### MEDIUM (Should Fix)

- Missing nullable specification
- Date stored as string
- No column default values

---

## Common Violations

### 1. Not Extending VendureEntity

**Violation:**

```typescript
@Entity()
export class MyEntity {
  // Missing extends!
  @PrimaryGeneratedColumn()
  id: number;
}
```

**Fix:**

```typescript
@Entity()
export class MyEntity extends VendureEntity {
  constructor(input?: DeepPartial<MyEntity>) {
    super(input);
  }
}
```

### 2. Missing Index on Foreign Key

**Violation:**

```typescript
@ManyToOne(() => Product)
product: Product;

@Column()
productId: number;  // No index!
```

**Fix:**

```typescript
@Index()
@ManyToOne(() => Product)
product: Product;

@Column()
productId: number;
```

### 3. Direct Repository Injection

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

  async find(ctx: RequestContext) {
    return this.connection.getRepository(ctx, MyEntity).find();
  }
}
```

### 4. Missing DeepPartial Constructor

**Violation:**

```typescript
@Entity()
export class MyEntity extends VendureEntity {
  @Column()
  name: string;
  // No constructor!
}
```

**Fix:**

```typescript
@Entity()
export class MyEntity extends VendureEntity {
  constructor(input?: DeepPartial<MyEntity>) {
    super(input);
  }

  @Column()
  name: string;
}
```

### 5. Using Any Type

**Violation:**

```typescript
@Column({ type: 'simple-json' })
metadata: any;  // No type safety!
```

**Fix:**

```typescript
interface MyMetadata {
  key: string;
  value: number;
}

@Column({ type: 'simple-json', nullable: true })
metadata: MyMetadata | null;
```

---

## Quick Detection Commands

```bash
# All-in-one entity audit
echo "=== CRITICAL: Not extending VendureEntity ===" && \
grep -rn "export class.*Entity" --include="*.entity.ts" | grep -v "extends VendureEntity" && \
echo "" && \
echo "=== HIGH: Missing @Index ===" && \
grep -rn "@ManyToOne" --include="*.entity.ts" -B 2 | grep -v "@Index" && \
echo "" && \
echo "=== MEDIUM: Using any ===" && \
grep -rn ": any" --include="*.entity.ts"
```

---

## Migration Review Checklist

When entity changes, verify:

- [ ] Migration file created
- [ ] Table/columns match entity
- [ ] Indexes created for foreign keys
- [ ] down() properly reverses up()
- [ ] No data loss in down()
- [ ] Column types correct (int, varchar, timestamp, etc.)

---

## Review Output Template

```markdown
## Entity Review: [Entity Name]

### Summary

[Overview of entity quality]

### Critical Issues (Must Fix)

- [ ] [Issue] - `file:line`

### High Priority

- [ ] [Issue] - `file:line`

### Passed Checks

- [x] Extends VendureEntity
- [x] @Entity decorator present
- [x] Migration exists

### Recommendations

- [Suggestions]
```

---

## Cross-Reference

All rules match patterns in **vendure-entity-writing** skill.

---

## Related Skills

- **vendure-entity-writing** - Entity patterns
- **vendure-plugin-reviewing** - Plugin-level review
