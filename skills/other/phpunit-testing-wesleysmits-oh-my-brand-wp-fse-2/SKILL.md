---
name: phpunit-testing
description: PHPUnit testing for PHP in Oh My Brand! theme. Test setup, mocking WordPress/ACF functions, testing helper functions and render templates. Use when writing unit tests for PHP code.
metadata:
  author: Wesley Smits
  version: "1.0.0"
---

# PHPUnit Testing

Unit testing PHP code with PHPUnit for the Oh My Brand! WordPress FSE theme.

---

## When to Use

- Testing block helper functions
- Testing render template logic
- Mocking WordPress globals and functions
- Mocking ACF field retrieval

---

## Configuration

| File | Template | Purpose |
|------|----------|---------|
| [phpunit.xml](references/phpunit.xml) | Test configuration | Test suites and coverage |
| [bootstrap.php](references/bootstrap.php) | Test bootstrap | WordPress function mocks |

---

## Test Templates

### Helper Function Tests

| Template | Purpose |
|----------|---------|
| [GalleryHelpersTest.php](references/GalleryHelpersTest.php) | Block attribute processing |
| [FaqHelpersTest.php](references/FaqHelpersTest.php) | JSON-LD generation, escaping |

### Mocking Tests

| Template | Purpose |
|----------|---------|
| [AcfBlockTest.php](references/AcfBlockTest.php) | Mock `get_field()` for ACF |
| [DataProviderTest.php](references/DataProviderTest.php) | Parameterized tests |

---

## Test Structure

```php
<?php

declare(strict_types=1);

namespace OMB\Tests\Blocks;

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

class ExampleTest extends TestCase
{
    #[Test]
    public function it_does_something(): void
    {
        // Arrange
        $input = [];

        // Act
        $result = some_function($input);

        // Assert
        $this->assertEmpty($result);
    }
}
```

---

## Mocking WordPress Functions

Add to `tests/php/bootstrap.php`:

```php
if (!function_exists('esc_html')) {
    function esc_html(string $text): string {
        return htmlspecialchars($text, ENT_QUOTES, 'UTF-8');
    }
}
```

Common mocks needed: `esc_html`, `esc_attr`, `esc_url`, `wp_kses_post`, `__`, `get_the_ID`, `get_block_wrapper_attributes`.

See [bootstrap.php](references/bootstrap.php) for complete mock list.

---

## Mocking ACF

Use static property pattern for `get_field`:

```php
private static array $mockFields = [];

public static function setUpBeforeClass(): void
{
    if (!function_exists('get_field')) {
        function get_field(string $field, $post_id = null) {
            return TestClass::getMockField($field);
        }
    }
}
```

See [AcfBlockTest.php](references/AcfBlockTest.php) for complete example.

---

## Data Providers

```php
use PHPUnit\Framework\Attributes\DataProvider;

#[Test]
#[DataProvider('alignmentProvider')]
public function it_applies_alignment(string $align, string $expected): void
{
    // Test with provided data
}

public static function alignmentProvider(): array
{
    return [
        'wide' => ['wide', 'alignwide'],
        'full' => ['full', 'alignfull'],
    ];
}
```

See [DataProviderTest.php](references/DataProviderTest.php) for more patterns.

---

## Running Tests

| Command | Purpose |
|---------|---------|
| `composer test` | Run all PHP tests |
| `composer test -- --filter ClassName` | Run specific class |
| `composer test -- --filter method_name` | Run specific test |
| `composer test -- --coverage-html coverage/` | With coverage report |
| `composer test -- --testdox` | Verbose output |
| `composer test -- --stop-on-failure` | Stop on first failure |

---

## Related Skills

- [php-standards](../php-standards/SKILL.md) - PHP coding conventions
- [vitest-testing](../vitest-testing/SKILL.md) - TypeScript unit testing
- [playwright-testing](../playwright-testing/SKILL.md) - E2E testing
- [native-block-development](../native-block-development/SKILL.md) - Block development

---

## References

- [PHPUnit Documentation](https://phpunit.de/documentation.html)
- [PHPUnit Attributes](https://docs.phpunit.de/en/11.0/attributes.html)
- [WordPress Testing Guide](https://make.wordpress.org/core/handbook/testing/)
