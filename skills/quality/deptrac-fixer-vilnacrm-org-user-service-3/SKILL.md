---
name: deptrac-fixer
description: Diagnose and fix Deptrac architectural violations automatically. Use when Deptrac reports dependency violations, layers are incorrectly coupled, or when refactoring code to respect hexagonal architecture boundaries. Never modifies deptrac.yaml - always fixes the code to match the architecture.
---

# Deptrac Fixer Skill

## Context (Input)

- `make deptrac` reports violations
- Error message contains "must not depend on"
- Domain layer has framework imports (Symfony, Doctrine, API Platform)
- Infrastructure directly calls Application handlers
- Any architectural boundary violation detected

## Task (Function)

Diagnose and fix Deptrac violations by refactoring code to respect hexagonal architecture boundaries.

**Success Criteria**: `make deptrac` outputs "✅ No violations found"

---

## Core Principle

**Fix the code, NEVER modify `deptrac.yaml`**

The architecture is correct. The code must conform to it, not vice versa.

---

## Quick Start: Fix a Violation

### Step 1: Run Deptrac

```bash
make deptrac
```

### Step 2: Parse Violation Message

```
Domain must not depend on Symfony
  src/Customer/Domain/Entity/Customer.php:8
    uses Symfony\Component\Validator\Constraints as Assert
```

**Extract:**

- **Violating Layer**: Domain
- **Forbidden Dependency**: Symfony
- **File & Line**: `src/Customer/Domain/Entity/Customer.php:8`
- **Violation Type**: `uses` (import statement)

### Step 3: Identify Fix Pattern

| Domain Depends On        | Fix Pattern         | Example File                                                                      |
| ------------------------ | ------------------- | --------------------------------------------------------------------------------- |
| Symfony Validator        | Move to YAML config | [01-domain-symfony-validation.php](examples/01-domain-symfony-validation.php)     |
| Doctrine (ODM/ORM)       | Use XML mapping     | [02-domain-doctrine-annotations.php](examples/02-domain-doctrine-annotations.php) |
| API Platform             | Move to YAML config | [03-domain-api-platform.php](examples/03-domain-api-platform.php)                 |
| Infrastructure → Handler | Use Command Bus     | [04-infrastructure-handler.php](examples/04-infrastructure-handler.php)           |

**See**: [REFERENCE.md](REFERENCE.md) for complete fix patterns and advanced scenarios.

### Step 4: Apply Fix

Follow the pattern from examples, then verify:

```bash
make deptrac
```

Repeat until: "✅ No violations found"

---

## Layer Dependency Rules

```
Domain ─────────────────> (NO dependencies)
           │
           │
Application ──────────> Domain + Infrastructure + Symfony + API Platform
           │
           │
Infrastructure ───────> Domain + Application + Symfony + Doctrine
```

**Allowed Dependencies:**

| Layer              | Can Depend On                                    |
| ------------------ | ------------------------------------------------ |
| **Domain**         | ❌ Nothing (pure PHP only)                       |
| **Application**    | ✅ Domain, Infrastructure, Symfony, API Platform |
| **Infrastructure** | ✅ Domain, Application, Symfony, Doctrine ORM    |

> Template examples use Doctrine ODM/MongoDB in places; apply the same patterns with Doctrine ORM and MySQL in this service.

**See**: [CODELY-STRUCTURE.md](CODELY-STRUCTURE.md) for complete directory hierarchy.

---

## Common Fix Patterns (Quick Reference)

### Pattern 1: Domain → Symfony Validator

❌ **Problem**: Validation annotations in Domain entity

```php
use Symfony\Component\Validator\Constraints as Assert;

class Customer {
    #[Assert\NotBlank]
    private string $name;
}
```

✅ **Solution**: Move validation to `config/validator/{Entity}.yaml`

---

### Pattern 2: Domain → Doctrine Annotations

❌ **Problem**: Doctrine attributes in Domain entity

```php
use Doctrine\ODM\MongoDB\Mapping\Annotations as ODM;

#[ODM\Document]
class Customer { }
```

✅ **Solution**: Create XML mapping in `config/doctrine/{Entity}.mongodb.xml`

---

### Pattern 3: Domain → API Platform

❌ **Problem**: API Platform attributes in Domain entity

```php
use ApiPlatform\Metadata\ApiResource;

#[ApiResource]
class Customer { }
```

✅ **Solution**: Create YAML config in `config/api_platform/resources/{entity}.yaml`

---

### Pattern 4: Infrastructure → Application Handler

❌ **Problem**: Direct handler call from Infrastructure

```php
class Repository {
    public function __construct(
        private SomeHandler $handler  // ❌ Circular dependency
    ) {}
}
```

✅ **Solution**: Use Command Bus pattern

```php
class Repository {
    public function __construct(
        private CommandBusInterface $commandBus  // ✅ Interface
    ) {}

    public function someMethod() {
        $this->commandBus->dispatch(new SomeCommand());
    }
}
```

**See**: [examples/](examples/) directory for complete, runnable examples.

---

## Diagnostic Workflow

When facing multiple violations:

### Step 1: Get All Violations

```bash
make deptrac > violations.txt
```

### Step 2: Categorize by Type

Group violations by layer pair:

- Domain → Symfony
- Domain → Doctrine
- Domain → API Platform
- Infrastructure → Application
- etc.

### Step 3: Fix in Priority Order

1. **Domain violations first** (most critical)
2. **Infrastructure violations** (circular dependencies)
3. **Application violations** (least common)

### Step 4: Verify Incrementally

```bash
# After each fix
make deptrac
```

Track progress: 15 violations → 10 → 5 → 0 ✅

---

## Constraints (Parameters)

### NEVER

- Modify `deptrac.yaml` to allow violations
- Disable Deptrac checks
- Add suppression comments
- Create "wrapper" classes to hide dependencies
- Move entire class to wrong layer just to satisfy Deptrac
- Use reflection or dynamic loading to bypass checks

### ALWAYS

- Fix the code to match the architecture
- Keep Domain layer pure (no framework imports)
- Use interfaces for cross-layer dependencies
- Move configuration to YAML/XML files
- Verify fixes with `make deptrac` after each change
- Check that tests still pass after refactoring

---

## Format (Output)

### Expected Deptrac Output

```
Deptrac

Checking dependencies...

✅ No violations found
```

### Expected CI Output

```
✅ CI checks successfully passed!
```

---

## Verification Checklist

After fixing violations:

- [ ] `make deptrac` shows 0 violations
- [ ] Domain entities have no framework imports
- [ ] Validation moved to `config/validator/`
- [ ] Doctrine mapping moved to `config/doctrine/`
- [ ] API Platform config moved to `config/api_platform/`
- [ ] Infrastructure uses Command Bus, not direct handler calls
- [ ] All tests still pass (`make all-tests`)
- [ ] `make ci` passes completely

---

## Related Skills

- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) - Understanding DDD patterns and layer responsibilities
- [api-platform-crud](../api-platform-crud/SKILL.md) - YAML-based API Platform configuration
- [database-migrations](../database-migrations/SKILL.md) - XML-based Doctrine mappings
- [complexity-management](../complexity-management/SKILL.md) - Refactoring without breaking architecture

---

## Quick Commands

```bash
# Run Deptrac analysis
make deptrac

# Check specific layer violations (if supported)
vendor/bin/deptrac analyze --report-uncovered

# Verify architecture after fixes
make deptrac && make ci
```

---

## Reference Documentation

For detailed patterns, examples, and troubleshooting:

- **[REFERENCE.md](REFERENCE.md)** - Complete fix patterns for all violation types
- **[CODELY-STRUCTURE.md](CODELY-STRUCTURE.md)** - Directory hierarchy and file placement rules
- **[examples/](examples/)** - Complete, runnable code examples:
  - `01-domain-symfony-validation.php` - Fixing Symfony validation violations
  - `02-domain-doctrine-annotations.php` - Removing Doctrine imports
  - `03-domain-api-platform.php` - Moving API Platform config
  - `04-infrastructure-handler.php` - Using Command Bus pattern

---

## Anti-Patterns to Avoid

### ❌ DON'T Modify deptrac.yaml

```yaml
# ❌ NEVER DO THIS
paths:
  - { collector: layer_domain, exclude: '.*Annotation.*' } # Hiding violations
```

### ❌ DON'T Create Wrapper Classes

```php
// ❌ BAD: Hiding framework dependency
class MyValidator {
    private SymfonyValidator $validator;  // Still violates!
}
```

### ❌ DON'T Move Classes to Wrong Layer

```php
// ❌ BAD: Moving Domain entity to Application to "fix" violation
// src/Application/Entity/Customer.php  // WRONG LAYER!
```

### ✅ DO Fix the Root Cause

- Extract validation to YAML
- Move configuration to XML
- Use interfaces and dependency inversion
- Respect layer responsibilities

---

## Success Criteria Summary

- ✅ Zero Deptrac violations
- ✅ Domain layer pure (no framework imports)
- ✅ All configuration externalized (YAML/XML)
- ✅ Proper use of Command Bus for cross-layer communication
- ✅ All tests passing
- ✅ CI pipeline green
