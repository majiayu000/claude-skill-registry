---
name: acc-psr-autoloading-knowledge
description: PSR-4 autoloading standard knowledge base for PHP 8.5 projects. Provides quick reference for namespace-to-path mapping, composer.json configuration, directory structure, and common mistakes. Use for autoloading audits and project structure reviews.
---

# PSR-4 Autoloading Knowledge

## Quick Reference

| Concept | Description |
|---------|-------------|
| **Namespace Prefix** | Maps to a base directory |
| **FQCN** | Fully Qualified Class Name |
| **Path Mapping** | Namespace → Directory → File |

## Core Concept

PSR-4 defines how to autoload classes from file paths based on their fully qualified class name.

```
Namespace Prefix    → Base Directory
Acme\Log\           → ./src/

FQCN                → File Path
Acme\Log\Writer\FileWriter → ./src/Writer/FileWriter.php
```

## Namespace to Path Mapping

### The Formula

```
File Path = Base Directory + (FQCN - Namespace Prefix) + .php

Where:
- Namespace separators (\) → Directory separators (/)
- Class name → File name with .php extension
```

### Examples

| FQCN | Namespace Prefix | Base Directory | File Path |
|------|------------------|----------------|-----------|
| `App\Entity\User` | `App\` | `src/` | `src/Entity/User.php` |
| `App\Domain\User\Entity\User` | `App\` | `src/` | `src/Domain/User/Entity/User.php` |
| `Vendor\Package\SubNs\ClassName` | `Vendor\Package\` | `lib/` | `lib/SubNs/ClassName.php` |

## Composer Configuration

### Basic Setup

```json
{
    "autoload": {
        "psr-4": {
            "App\\": "src/",
            "App\\Tests\\": "tests/"
        }
    }
}
```

### Multiple Directories

```json
{
    "autoload": {
        "psr-4": {
            "App\\": ["src/", "lib/"]
        }
    }
}
```

### DDD Project Structure

```json
{
    "autoload": {
        "psr-4": {
            "App\\": "src/",
            "App\\Domain\\": "src/Domain/",
            "App\\Application\\": "src/Application/",
            "App\\Infrastructure\\": "src/Infrastructure/",
            "App\\Presentation\\": "src/Presentation/"
        }
    },
    "autoload-dev": {
        "psr-4": {
            "App\\Tests\\": "tests/"
        }
    }
}
```

### Symfony Bundle Structure

```json
{
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

### Laravel Package Structure

```json
{
    "autoload": {
        "psr-4": {
            "Vendor\\Package\\": "src/"
        }
    }
}
```

## Directory Structure Examples

### Standard DDD Layout

```
project/
├── composer.json
├── src/
│   ├── Domain/
│   │   └── User/
│   │       ├── Entity/
│   │       │   └── User.php           # App\Domain\User\Entity\User
│   │       ├── ValueObject/
│   │       │   └── Email.php          # App\Domain\User\ValueObject\Email
│   │       ├── Repository/
│   │       │   └── UserRepositoryInterface.php
│   │       └── Event/
│   │           └── UserCreated.php
│   ├── Application/
│   │   └── User/
│   │       ├── Command/
│   │       │   └── CreateUserCommand.php
│   │       └── Handler/
│   │           └── CreateUserHandler.php
│   ├── Infrastructure/
│   │   └── Persistence/
│   │       └── Doctrine/
│   │           └── UserRepository.php
│   └── Presentation/
│       └── Api/
│           └── Controller/
│               └── UserController.php
└── tests/
    └── Unit/
        └── Domain/
            └── User/
                └── Entity/
                    └── UserTest.php   # App\Tests\Unit\Domain\User\Entity\UserTest
```

### Class Examples

```php
// src/Domain/User/Entity/User.php
<?php

declare(strict_types=1);

namespace App\Domain\User\Entity;

use App\Domain\User\ValueObject\Email;
use App\Domain\User\ValueObject\UserId;

final class User
{
    // ...
}
```

```php
// src/Domain/User/ValueObject/Email.php
<?php

declare(strict_types=1);

namespace App\Domain\User\ValueObject;

final readonly class Email
{
    // ...
}
```

## Detection Patterns

### Find Mismatched Namespaces

```bash
# Extract namespace from files and compare with path
for file in $(find src -name "*.php"); do
    namespace=$(grep -m1 "^namespace" "$file" | sed 's/namespace //;s/;//')
    expected_ns="App\\$(dirname ${file#src/} | tr '/' '\\')"
    if [ "$namespace" != "$expected_ns" ]; then
        echo "Mismatch: $file"
        echo "  Found:    $namespace"
        echo "  Expected: $expected_ns"
    fi
done
```

### Find Classes Without Namespace

```bash
# Files with class but no namespace
grep -rL "^namespace" --include="*.php" src/ | \
    xargs grep -l "^class\|^interface\|^trait\|^enum"
```

### Find Incorrect Class Names

```bash
# Class name doesn't match filename
for file in $(find src -name "*.php"); do
    filename=$(basename "$file" .php)
    if ! grep -q "^\(class\|interface\|trait\|enum\) $filename" "$file"; then
        echo "Mismatch: $file (expected class/interface/trait/enum $filename)"
    fi
done
```

### Validate Composer Autoload

```bash
# Dump autoload and check for errors
composer dump-autoload --strict 2>&1 | grep -i "warning\|error"

# Validate composer.json
composer validate --strict
```

## Common Mistakes

### 1. Namespace vs Path Mismatch

```php
// File: src/Domain/User/Entity/User.php
// BAD: Namespace doesn't match path
namespace App\User\Entity;  // Missing "Domain"

// GOOD: Namespace matches path
namespace App\Domain\User\Entity;
```

### 2. Class Name vs Filename Mismatch

```php
// File: src/Domain/UserEntity.php
// BAD: Class name doesn't match filename
class User { }

// GOOD: Class name matches filename
class UserEntity { }
```

### 3. Case Sensitivity Issues

```php
// File: src/Domain/User/Entity/user.php (lowercase)
// BAD: Will fail on case-sensitive filesystems (Linux)
namespace App\Domain\User\Entity;
class User { }

// GOOD: Filename should be User.php (PascalCase)
```

### 4. Missing Trailing Backslash

```json
// BAD: Missing trailing backslash
{
    "autoload": {
        "psr-4": {
            "App": "src/"
        }
    }
}

// GOOD: Include trailing backslash
{
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

### 5. Incorrect Directory Separator

```json
// BAD: Using backslash in path (Windows-only)
{
    "autoload": {
        "psr-4": {
            "App\\": "src\\"
        }
    }
}

// GOOD: Use forward slash (cross-platform)
{
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

## Verification Commands

```bash
# Regenerate autoload files
composer dump-autoload

# Optimize autoload (production)
composer dump-autoload --optimize

# Validate and show issues
composer dump-autoload --strict

# Test class loading
php -r "require 'vendor/autoload.php'; new App\Domain\User\Entity\User();"
```

## PHP-CS-Fixer Rules

```php
<?php

return (new PhpCsFixer\Config())
    ->setRules([
        // PSR-4 related rules
        'single_class_element_per_statement' => true,
        'single_import_per_statement' => true,
        'ordered_imports' => [
            'sort_algorithm' => 'alpha',
        ],
        'no_unused_imports' => true,
        'fully_qualified_strict_types' => true,
    ]);
```

## Integration with DDD Layers

### Layer Mapping

| Layer | Namespace | Directory |
|-------|-----------|-----------|
| Domain | `App\Domain\{Context}\` | `src/Domain/{Context}/` |
| Application | `App\Application\{Context}\` | `src/Application/{Context}/` |
| Infrastructure | `App\Infrastructure\` | `src/Infrastructure/` |
| Presentation | `App\Presentation\` | `src/Presentation/` |

### Component Mapping

| Component | Namespace Pattern | Directory Pattern |
|-----------|-------------------|-------------------|
| Entity | `App\Domain\{Context}\Entity\` | `src/Domain/{Context}/Entity/` |
| Value Object | `App\Domain\{Context}\ValueObject\` | `src/Domain/{Context}/ValueObject/` |
| Repository | `App\Domain\{Context}\Repository\` | `src/Domain/{Context}/Repository/` |
| Service | `App\Domain\{Context}\Service\` | `src/Domain/{Context}/Service/` |
| Command | `App\Application\{Context}\Command\` | `src/Application/{Context}/Command/` |
| Query | `App\Application\{Context}\Query\` | `src/Application/{Context}/Query/` |
| Handler | `App\Application\{Context}\Handler\` | `src/Application/{Context}/Handler/` |

## See Also

- `references/psr-4-standard.md` - Full PSR-4 specification
- `references/composer-integration.md` - Composer autoload configuration
- `references/directory-structure.md` - Project structure examples
- `references/antipatterns.md` - Common mistakes and fixes
- `assets/report-template.md` - Audit report template
