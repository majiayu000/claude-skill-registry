---
name: acc-psr-coding-style-knowledge
description: PSR-1 and PSR-12 coding standards knowledge base for PHP 8.5 projects. Provides quick reference for basic coding standard and extended coding style with detection patterns, examples, and antipattern identification. Use for code style audits and compliance reviews.
---

# PSR Coding Style Knowledge (PSR-1, PSR-12)

## Quick Reference

| Standard | Focus | Key Rules |
|----------|-------|-----------|
| PSR-1 | Basic Standard | Files, namespaces, class names |
| PSR-12 | Extended Style | Formatting, keywords, visibility |

## PSR-1: Basic Coding Standard

### 1. Files

| Rule | Requirement |
|------|-------------|
| Tags | MUST use `<?php` or `<?=` only |
| Encoding | MUST be UTF-8 without BOM |
| Side Effects | Files SHOULD declare symbols OR execute logic, not both |

### 2. Namespaces and Classes

| Rule | Requirement |
|------|-------------|
| Namespaces | MUST follow PSR-4 autoloading |
| Class Names | MUST be `StudlyCaps` (PascalCase) |
| Constants | MUST be `UPPER_CASE_WITH_UNDERSCORES` |
| Methods | MUST be `camelCase` |

### 3. Side Effects Detection

```php
// BAD: Mixing declarations and side effects
<?php
namespace App;

ini_set('display_errors', '1');  // Side effect!

class Logger { }

// GOOD: Separate files
// bootstrap.php
<?php
ini_set('display_errors', '1');
require 'vendor/autoload.php';

// Logger.php
<?php
declare(strict_types=1);

namespace App;

final readonly class Logger { }
```

## PSR-12: Extended Coding Style

### 1. General

| Rule | Requirement |
|------|-------------|
| PSR-1 | MUST follow PSR-1 |
| Indentation | MUST use 4 spaces (no tabs) |
| Line Length | SHOULD be ≤120 chars, MUST NOT hard wrap |
| Line Ending | MUST be Unix LF (`\n`) |
| Blank Line | MUST have one at end of file |
| Trailing Space | MUST NOT have trailing whitespace |

### 2. Files

```php
<?php

declare(strict_types=1);

namespace Vendor\Package;

use Vendor\Package\{ClassA as A, ClassB, ClassC as C};
use Vendor\Package\SomeNamespace\ClassD as D;

use function Vendor\Package\{functionA, functionB, functionC};
use const Vendor\Package\{ConstantA, ConstantB, ConstantC};

final readonly class ClassName extends ParentClass implements
    InterfaceA,
    InterfaceB,
    InterfaceC
{
    // class body
}
```

### 3. Keywords and Types

| Rule | Requirement |
|------|-------------|
| Keywords | MUST be lowercase (`true`, `false`, `null`) |
| Type Declarations | MUST be lowercase (`int`, `string`, `bool`) |
| Short Forms | MUST use `bool`, `int` (not `boolean`, `integer`) |

### 4. Classes, Properties, Methods

```php
<?php

declare(strict_types=1);

namespace App\Domain\Entity;

use App\Domain\ValueObject\Email;
use App\Domain\ValueObject\UserId;

final readonly class User
{
    public function __construct(
        private UserId $id,
        private Email $email,
        private string $name,
        private bool $isActive = true,
    ) {
    }

    public function getId(): UserId
    {
        return $this->id;
    }

    public function activate(): self
    {
        return new self(
            $this->id,
            $this->email,
            $this->name,
            true,
        );
    }
}
```

### 5. Control Structures

```php
<?php

// if-elseif-else
if ($expr1) {
    // if body
} elseif ($expr2) {
    // elseif body
} else {
    // else body
}

// switch
switch ($expr) {
    case 0:
        echo 'First case';
        break;
    case 1:
        echo 'Second case';
        // no break - intentional fall-through
    default:
        echo 'Default case';
        break;
}

// match (PHP 8.0+)
$result = match ($expr) {
    0 => 'First',
    1, 2 => 'Second or third',
    default => 'Other',
};

// while
while ($expr) {
    // body
}

// for
for ($i = 0; $i < 10; $i++) {
    // body
}

// foreach
foreach ($iterable as $key => $value) {
    // body
}

// try-catch-finally
try {
    // try body
} catch (FirstThrowableType $e) {
    // catch body
} catch (OtherThrowableType | AnotherThrowableType $e) {
    // multi-catch body
} finally {
    // finally body
}
```

### 6. Operators

```php
<?php

// Binary operators: space before and after
$sum = $a + $b;
$concat = $string1 . $string2;
$result = $condition ? $valueIfTrue : $valueIfFalse;

// Unary operators: no space
$i++;
--$j;
$negated = !$bool;

// Type casting: no space after cast
$intValue = (int) $floatValue;
$stringValue = (string) $intValue;
```

### 7. Closures and Arrow Functions

```php
<?php

// Closure
$closure = function (int $arg1, int $arg2) use ($var1, $var2): int {
    return $arg1 + $arg2 + $var1 + $var2;
};

// Long argument list
$longClosure = function (
    int $argument1,
    string $argument2,
    bool $argument3,
) use (
    $staticVar1,
    $staticVar2,
): bool {
    // body
};

// Arrow function (PHP 7.4+)
$multiply = fn(int $a, int $b): int => $a * $b;
```

### 8. Anonymous Classes

```php
<?php

$instance = new class extends ParentClass implements SomeInterface {
    use SomeTrait;

    public function __construct(
        private readonly int $value,
    ) {
    }
};
```

## Detection Patterns

### PSR-1 Violations

```bash
# Side effects in class files (functions like echo, print, header, etc.)
grep -rn "^[[:space:]]*\(echo\|print\|header\|session_start\|ini_set\)" --include="*.php" src/

# Non-StudlyCaps class names
grep -rn "^class [a-z]" --include="*.php" src/
grep -rn "^class [A-Z][a-z]*_" --include="*.php" src/

# Non-camelCase method names
grep -rn "function [A-Z]" --include="*.php" src/
grep -rn "function [a-z]*_[a-z]" --include="*.php" src/
```

### PSR-12 Violations

```bash
# Tab characters instead of spaces
grep -rn $'\t' --include="*.php" src/

# Trailing whitespace
grep -rn "[[:space:]]$" --include="*.php" src/

# Long keywords (boolean instead of bool)
grep -rn "boolean\|integer" --include="*.php" src/

# Missing space after keywords
grep -rn "\(if\|for\|foreach\|while\|switch\|catch\)(" --include="*.php" src/

# Opening brace on wrong line for classes
grep -rn "^class.*{$" --include="*.php" src/
```

## PHP_CodeSniffer Configuration

```xml
<?xml version="1.0"?>
<ruleset name="PSR-12">
    <description>PSR-12 coding standard</description>
    <rule ref="PSR12"/>

    <file>src</file>
    <file>tests</file>

    <exclude-pattern>vendor/*</exclude-pattern>

    <arg name="colors"/>
    <arg value="sp"/>
</ruleset>
```

## PHP-CS-Fixer Configuration

```php
<?php

declare(strict_types=1);

use PhpCsFixer\Config;
use PhpCsFixer\Finder;

$finder = Finder::create()
    ->in([
        __DIR__ . '/src',
        __DIR__ . '/tests',
    ])
    ->name('*.php');

return (new Config())
    ->setRiskyAllowed(true)
    ->setRules([
        '@PSR12' => true,
        '@PHP84Migration' => true,
        'declare_strict_types' => true,
        'final_class' => true,
        'class_attributes_separation' => [
            'elements' => ['method' => 'one'],
        ],
        'ordered_imports' => [
            'sort_algorithm' => 'alpha',
            'imports_order' => ['class', 'function', 'const'],
        ],
        'no_unused_imports' => true,
        'trailing_comma_in_multiline' => [
            'elements' => ['arguments', 'arrays', 'parameters'],
        ],
    ])
    ->setFinder($finder);
```

## Antipatterns

| Violation | PSR | Severity | Fix |
|-----------|-----|----------|-----|
| Mixed declarations and side effects | PSR-1 | CRITICAL | Separate into bootstrap file |
| snake_case class names | PSR-1 | CRITICAL | Rename to StudlyCaps |
| Tabs for indentation | PSR-12 | WARNING | Convert to 4 spaces |
| Boolean/integer type hints | PSR-12 | WARNING | Use bool/int |
| Missing strict_types | - | WARNING | Add declaration |
| Opening brace on same line | PSR-12 | INFO | Move to next line |
| Trailing whitespace | PSR-12 | INFO | Remove whitespace |

## Integration with DDD

### Domain Layer
```php
<?php

declare(strict_types=1);

namespace App\Domain\User\ValueObject;

// PSR-12 compliant Value Object
final readonly class Email
{
    private function __construct(
        private string $value,
    ) {
    }

    public static function fromString(string $email): self
    {
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new InvalidEmailException($email);
        }

        return new self($email);
    }

    public function toString(): string
    {
        return $this->value;
    }
}
```

### Application Layer
```php
<?php

declare(strict_types=1);

namespace App\Application\User\UseCase;

use App\Application\User\Command\CreateUserCommand;
use App\Domain\User\Entity\User;
use App\Domain\User\Repository\UserRepositoryInterface;

// PSR-12 compliant Use Case
final readonly class CreateUserHandler
{
    public function __construct(
        private UserRepositoryInterface $userRepository,
    ) {
    }

    public function __invoke(CreateUserCommand $command): void
    {
        $user = User::create(
            $command->email,
            $command->name,
        );

        $this->userRepository->save($user);
    }
}
```

## See Also

- `references/psr-1-basic.md` - Full PSR-1 specification
- `references/psr-12-extended.md` - Full PSR-12 specification
- `references/detection-patterns.md` - Comprehensive detection patterns
- `references/antipatterns.md` - Common violations with fixes
- `assets/report-template.md` - Compliance report template
