---
name: acc-readme-template
description: Generates README.md files for PHP projects. Creates structured documentation with badges, installation, usage, and examples.
---

# README Template Generator

Generate professional README.md files for PHP projects.

## Template Structure

```markdown
# {Project Name}

{badges}

{one-line description}

## Features

{feature list with benefits}

## Requirements

{dependencies and versions}

## Installation

{composer command and setup steps}

## Quick Start

{minimal working example}

## Documentation

{links to detailed docs}

## Contributing

{link to CONTRIBUTING.md}

## Changelog

{link to CHANGELOG.md}

## License

{license type and link}
```

## Badge Templates

### Standard Badge Set

```markdown
[![CI](https://github.com/{owner}/{repo}/actions/workflows/ci.yml/badge.svg)](https://github.com/{owner}/{repo}/actions)
[![Coverage](https://codecov.io/gh/{owner}/{repo}/graph/badge.svg)](https://codecov.io/gh/{owner}/{repo})
[![Packagist](https://img.shields.io/packagist/v/{vendor}/{package}.svg)](https://packagist.org/packages/{vendor}/{package})
[![PHP](https://img.shields.io/packagist/php-v/{vendor}/{package}.svg)](https://packagist.org/packages/{vendor}/{package})
[![License](https://img.shields.io/github/license/{owner}/{repo}.svg)](LICENSE)
```

### Minimal Badge Set

```markdown
[![Build](https://img.shields.io/github/actions/workflow/status/{owner}/{repo}/ci.yml)](https://github.com/{owner}/{repo}/actions)
[![Version](https://img.shields.io/packagist/v/{vendor}/{package})](https://packagist.org/packages/{vendor}/{package})
```

## Section Templates

### Features Section

```markdown
## Features

- ✅ **Feature Name** — Brief description of benefit
- ✅ **Feature Name** — Brief description of benefit
- ✅ **Feature Name** — Brief description of benefit
- 🚧 **Coming Soon** — Planned feature
```

### Requirements Section

```markdown
## Requirements

- PHP 8.5+
- Composer 2.0+
- Extensions: ext-json, ext-pdo

### Optional

- Redis (for caching)
- RabbitMQ (for queuing)
```

### Installation Section (Basic)

```markdown
## Installation

```bash
composer require {vendor}/{package}
```
```

### Installation Section (With Config)

```markdown
## Installation

1. Install via Composer:

```bash
composer require {vendor}/{package}
```

2. Publish configuration (optional):

```bash
php artisan vendor:publish --provider="Vendor\Package\ServiceProvider"
```

3. Configure environment:

```bash
# .env
PACKAGE_API_KEY=your-key
PACKAGE_DEBUG=false
```
```

### Quick Start Section

```markdown
## Quick Start

```php
<?php

declare(strict_types=1);

use {Vendor}\{Package}\{MainClass};

// Initialize
${instance} = new {MainClass}();

// Basic operation
$result = ${instance}->doSomething('input');

// Output
echo $result->status; // "success"
```
```

### Documentation Section

```markdown
## Documentation

- 📖 [Getting Started](docs/getting-started.md)
- ⚙️ [Configuration](docs/configuration.md)
- 📚 [API Reference](docs/api/README.md)
- 💡 [Examples](docs/examples/)
- ❓ [FAQ](docs/faq.md)
```

### Contributing Section

```markdown
## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup
- Coding standards
- Testing guidelines
- Pull request process
```

### License Section

```markdown
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

## Complete Example

```markdown
# Awesome Package

[![CI](https://github.com/vendor/awesome-package/actions/workflows/ci.yml/badge.svg)](https://github.com/vendor/awesome-package/actions)
[![Coverage](https://codecov.io/gh/vendor/awesome-package/graph/badge.svg)](https://codecov.io/gh/vendor/awesome-package)
[![Packagist](https://img.shields.io/packagist/v/vendor/awesome-package.svg)](https://packagist.org/packages/vendor/awesome-package)
[![PHP](https://img.shields.io/packagist/php-v/vendor/awesome-package.svg)](https://packagist.org/packages/vendor/awesome-package)
[![License](https://img.shields.io/github/license/vendor/awesome-package.svg)](LICENSE)

A PHP library for processing awesome things with type safety and modern practices.

## Features

- ✅ **Type-Safe API** — Full PHP 8.5 type declarations
- ✅ **PSR Compliant** — PSR-4, PSR-7, PSR-12
- ✅ **Zero Dependencies** — No external runtime dependencies
- ✅ **Fully Tested** — 100% code coverage

## Requirements

- PHP 8.5+
- Composer 2.0+
- ext-json

## Installation

```bash
composer require vendor/awesome-package
```

## Quick Start

```php
<?php

declare(strict_types=1);

use Vendor\AwesomePackage\Processor;

$processor = new Processor();
$result = $processor->process(['data' => 'value']);

echo $result->status; // "success"
```

## Documentation

- 📖 [Getting Started](docs/getting-started.md)
- ⚙️ [Configuration](docs/configuration.md)
- 📚 [API Reference](docs/api/README.md)
- 💡 [Examples](docs/examples/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

MIT License - see [LICENSE](LICENSE) for details.
```

## Generation Instructions

When generating a README:

1. **Analyze** the project structure (`composer.json`, `src/`)
2. **Identify** main class/entry point
3. **Extract** dependencies and requirements
4. **Create** minimal working example
5. **Generate** appropriate badges
6. **Link** to existing documentation
7. **Verify** all links point to existing files
