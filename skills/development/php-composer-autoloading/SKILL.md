---
name: PHP Composer and Autoloading
description: Use when composer package management and PSR-4 autoloading including dependency management, autoload strategies, package creation, version constraints, and patterns for modern PHP project organization and distribution.
allowed-tools: []
---

# PHP Composer and Autoloading

## Introduction

Composer is PHP's de facto dependency manager, handling package installation,
autoloading, and version management. PSR-4 autoloading eliminates manual
require statements by automatically loading classes based on namespace and file
structure conventions.

Composer revolutionized PHP development by providing standardized dependency
management similar to npm, pip, or Maven. Combined with PSR-4 autoloading,
Composer enables modern PHP projects to organize code cleanly, share packages
easily, and manage dependencies reliably.

This skill covers Composer basics, dependency management, autoloading strategies,
package creation, semantic versioning, and best practices for maintainable PHP
projects.

## Composer Basics

Composer manages project dependencies through composer.json configuration and
installs packages into the vendor directory.

```json
{
    "name": "company/project",
    "description": "Project description",
    "type": "project",
    "require": {
        "php": ">=8.1",
        "symfony/console": "^6.0",
        "guzzlehttp/guzzle": "^7.5",
        "monolog/monolog": "^3.0"
    },
    "require-dev": {
        "phpunit/phpunit": "^10.0",
        "phpstan/phpstan": "^1.10",
        "squizlabs/php_codesniffer": "^3.7"
    },
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    },
    "autoload-dev": {
        "psr-4": {
            "Tests\\": "tests/"
        }
    },
    "scripts": {
        "test": "phpunit",
        "lint": "phpcs",
        "analyse": "phpstan analyse"
    },
    "config": {
        "optimize-autoloader": true,
        "sort-packages": true
    }
}
```

```bash
# Install dependencies
composer install

# Install specific package
composer require symfony/http-foundation

# Install development dependency
composer require --dev symfony/var-dumper

# Update dependencies
composer update

# Update specific package
composer update monolog/monolog

# Remove package
composer remove guzzlehttp/guzzle

# Show installed packages
composer show

# Show outdated packages
composer outdated

# Validate composer.json
composer validate

# Run script
composer test
```

Composer creates composer.lock to lock exact dependency versions, ensuring
consistent installations across environments.

## PSR-4 Autoloading

PSR-4 autoloading maps namespaces to directories, automatically loading classes
without manual require statements.

```php
<?php
// composer.json autoload configuration
{
    "autoload": {
        "psr-4": {
            "App\\": "src/",
            "App\\Controllers\\": "src/Controllers/",
            "App\\Models\\": "src/Models/"
        }
    }
}

// Directory structure
// src/
//   User.php
//   Controllers/
//     UserController.php
//   Models/
//     UserModel.php

// src/User.php
namespace App;

class User {
    public function __construct(
        public string $name,
        public string $email
    ) {}
}

// src/Controllers/UserController.php
namespace App\Controllers;

use App\User;
use App\Models\UserModel;

class UserController {
    public function show(int $id): User {
        $model = new UserModel();
        return $model->find($id);
    }
}

// src/Models/UserModel.php
namespace App\Models;

use App\User;

class UserModel {
    public function find(int $id): User {
        return new User("Alice", "alice@example.com");
    }
}

// index.php - Composer autoloader
require __DIR__ . '/vendor/autoload.php';

use App\Controllers\UserController;

$controller = new UserController();
$user = $controller->show(1);

echo $user->name; // "Alice"
```

```php
<?php
// Multiple autoload strategies
{
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        },
        "classmap": [
            "database/seeds",
            "database/factories"
        ],
        "files": [
            "src/helpers.php"
        ]
    }
}

// Regenerate autoloader after changes
// composer dump-autoload

// Optimize autoloader for production
// composer dump-autoload --optimize
// composer dump-autoload --classmap-authoritative
```

PSR-4 eliminates require statements and enables consistent project structure
across PHP projects.

## Version Constraints and Dependency Management

Semantic versioning and version constraints control which package versions
Composer installs and updates.

```json
{
    "require": {
        "vendor/package": "1.2.3",
        "vendor/exact": "1.0.0",
        "vendor/caret": "^2.0",
        "vendor/tilde": "~3.1",
        "vendor/wildcard": "4.*",
        "vendor/range": ">=5.0 <6.0",
        "vendor/latest": "dev-master",
        "vendor/branch": "dev-feature-x",
        "vendor/stability": "1.0@beta"
    }
}
```

Version constraint patterns:

- `1.2.3` - Exact version
- `^1.2.3` - Caret: >=1.2.3 <2.0.0 (compatible)
- `~1.2.3` - Tilde: >=1.2.3 <1.3.0 (similar)
- `1.*` - Wildcard: >=1.0.0 <2.0.0
- `>=1.0 <2.0` - Range: explicit min/max
- `dev-master` - Development branch
- `1.0@beta` - Specific stability

```json
{
    "require": {
        "symfony/console": "^6.0",
        "monolog/monolog": "^3.0",
        "guzzlehttp/guzzle": "^7.5"
    },
    "minimum-stability": "stable",
    "prefer-stable": true
}
```

```bash
# Show why package installed
composer why vendor/package

# Show what depends on package
composer depends vendor/package

# Show what package provides
composer show --all vendor/package

# Check for security vulnerabilities
composer audit

# Show platform requirements
composer check-platform-reqs

# Diagnose issues
composer diagnose
```

Semantic versioning (MAJOR.MINOR.PATCH) communicates breaking changes,
features, and fixes in version numbers.

## Creating Packages

Creating reusable Composer packages enables code sharing across projects and
with the community.

```json
{
    "name": "company/http-client",
    "description": "HTTP client wrapper",
    "type": "library",
    "keywords": ["http", "client", "api"],
    "license": "MIT",
    "authors": [
        {
            "name": "Developer Name",
            "email": "dev@example.com"
        }
    ],
    "require": {
        "php": ">=8.1",
        "guzzlehttp/guzzle": "^7.5"
    },
    "require-dev": {
        "phpunit/phpunit": "^10.0"
    },
    "autoload": {
        "psr-4": {
            "Company\\HttpClient\\": "src/"
        }
    },
    "autoload-dev": {
        "psr-4": {
            "Tests\\": "tests/"
        }
    }
}
```

```php
<?php
// src/Client.php
namespace Company\HttpClient;

use GuzzleHttp\Client as GuzzleClient;

class Client {
    private GuzzleClient $client;

    public function __construct(string $baseUrl) {
        $this->client = new GuzzleClient(['base_uri' => $baseUrl]);
    }

    public function get(string $path): array {
        $response = $this->client->get($path);
        return json_decode($response->getBody(), true);
    }

    public function post(string $path, array $data): array {
        $response = $this->client->post($path, ['json' => $data]);
        return json_decode($response->getBody(), true);
    }
}

// tests/ClientTest.php
namespace Tests;

use Company\HttpClient\Client;
use PHPUnit\Framework\TestCase;

class ClientTest extends TestCase {
    public function testCanCreateClient(): void {
        $client = new Client('https://api.example.com');
        $this->assertInstanceOf(Client::class, $client);
    }
}
```

```bash
# Validate package
composer validate

# Initialize new package
composer init

# Publish to Packagist
# 1. Create GitHub repository
# 2. Push code with composer.json
# 3. Submit to packagist.org

# Private packages
# Add to composer.json:
{
    "repositories": [
        {
            "type": "vcs",
            "url": "https://github.com/company/private-package"
        }
    ]
}
```

Well-designed packages follow PSR standards, include tests, and provide clear
documentation.

## Autoload Optimization

Optimizing autoloading improves production performance by reducing file system
lookups.

```bash
# Generate optimized autoloader
composer dump-autoload --optimize

# Classmap authoritative (no file system checks)
composer dump-autoload --classmap-authoritative

# APCu cache (requires apcu extension)
composer dump-autoload --apcu
```

```json
{
    "config": {
        "optimize-autoloader": true,
        "classmap-authoritative": true,
        "apcu-autoloader": true
    }
}
```

```php
<?php
// Autoload optimization levels

// 1. Default PSR-4 (checks file system)
// Slowest, flexible

// 2. Optimized (builds class map)
// Fast, checks file system if not in map

// 3. Authoritative (class map only)
// Fastest, no file system checks
// Use in production

// Measure impact
$start = microtime(true);

// Autoload many classes
for ($i = 0; $i < 1000; $i++) {
    $class = "App\\Service$i";
    if (class_exists($class)) {
        // Use class
    }
}

$duration = microtime(true) - $start;
echo "Duration: $duration seconds\n";
```

Authoritative classmap provides best performance but requires regeneration after
code changes.

## Composer Scripts and Platform

Composer scripts automate common development tasks and check platform
requirements.

```json
{
    "scripts": {
        "test": "phpunit",
        "test:unit": "phpunit --testsuite=unit",
        "test:integration": "phpunit --testsuite=integration",
        "lint": "phpcs --standard=PSR12 src",
        "lint:fix": "phpcbf --standard=PSR12 src",
        "analyse": "phpstan analyse src --level=max",
        "check": [
            "@lint",
            "@analyse",
            "@test"
        ],
        "post-install-cmd": [
            "@php artisan key:generate --ansi"
        ],
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=public --ansi"
        ]
    },
    "scripts-descriptions": {
        "test": "Run all tests",
        "lint": "Check code style",
        "check": "Run all checks"
    }
}
```

```json
{
    "require": {
        "php": "^8.1",
        "ext-pdo": "*",
        "ext-mbstring": "*",
        "ext-intl": "*"
    },
    "suggest": {
        "ext-redis": "For Redis cache support",
        "ext-imagick": "For image manipulation"
    },
    "platform": {
        "php": "8.1.0"
    },
    "platform-check": true
}
```

```bash
# Run script
composer test
composer run-script test

# Run with arguments
composer test -- --filter=UserTest

# List scripts
composer run-script --list

# Check platform requirements
composer check-platform-reqs
```

Scripts enable CI/CD integration and consistent development workflows across
team members.

## Monorepo and Path Repositories

Managing multiple related packages in a single repository using path
repositories.

```json
{
    "name": "company/monorepo",
    "repositories": [
        {
            "type": "path",
            "url": "./packages/http-client"
        },
        {
            "type": "path",
            "url": "./packages/database"
        },
        {
            "type": "path",
            "url": "./packages/auth"
        }
    ],
    "require": {
        "company/http-client": "@dev",
        "company/database": "@dev",
        "company/auth": "@dev"
    }
}
```

```text
monorepo/
├── composer.json
├── packages/
│   ├── http-client/
│   │   ├── composer.json
│   │   └── src/
│   ├── database/
│   │   ├── composer.json
│   │   └── src/
│   └── auth/
│       ├── composer.json
│       └── src/
└── vendor/
```

```json
// packages/http-client/composer.json
{
    "name": "company/http-client",
    "autoload": {
        "psr-4": {
            "Company\\HttpClient\\": "src/"
        }
    }
}

// packages/auth/composer.json
{
    "name": "company/auth",
    "require": {
        "company/http-client": "^1.0"
    },
    "autoload": {
        "psr-4": {
            "Company\\Auth\\": "src/"
        }
    }
}
```

Path repositories enable local development of interdependent packages without
publishing.

## Best Practices

1. **Commit composer.lock to version control** to ensure consistent dependency
   versions across environments

2. **Use caret constraints for dependencies** (^1.2.3) to allow compatible
   updates while preventing breaking changes

3. **Separate runtime and development dependencies** using require and
   require-dev for smaller production installs

4. **Optimize autoloader for production** with --classmap-authoritative to
   eliminate file system checks

5. **Follow PSR-4 autoloading conventions** with namespace-to-directory mapping
   for consistency

6. **Specify minimum PHP version and extensions** in require section to catch
   compatibility issues early

7. **Use scripts for common tasks** to standardize development workflows across
   team members

8. **Keep dependencies updated** by regularly running composer outdated and
   updating packages

9. **Validate composer.json regularly** with composer validate to catch
   configuration errors

10. **Use semantic versioning for packages** to communicate changes clearly and
    enable automatic updates

## Common Pitfalls

1. **Not committing composer.lock** causes different dependency versions across
   environments and unpredictable behavior

2. **Using exact version constraints** (1.2.3) prevents security updates and bug
   fixes from being installed

3. **Running composer update blindly** can introduce breaking changes; review
   updates before applying

4. **Mixing PSR-4 with manual requires** defeats autoloading purpose and creates
   maintenance burden

5. **Not optimizing autoloader for production** causes performance degradation
   from file system checks

6. **Ignoring composer.json validation errors** leads to installation failures
   and hard-to-debug issues

7. **Not specifying PHP version requirements** allows installation on
   incompatible PHP versions

8. **Using global Composer for project-specific packages** creates conflicts and
   version mismatches

9. **Not using --no-dev flag in production** installs unnecessary development
   dependencies

10. **Forgetting to run dump-autoload** after adding new classes causes class
    not found errors

## When to Use This Skill

Use Composer for any modern PHP project to manage dependencies, autoloading, and
package distribution professionally.

Apply PSR-4 autoloading when organizing project code to eliminate manual require
statements and follow industry standards.

Employ version constraints when managing dependencies to balance stability with
security updates and bug fixes.

Create packages when building reusable functionality that could benefit multiple
projects or the wider community.

Leverage Composer scripts for CI/CD pipelines, development workflows, and
automated testing to ensure consistency.

## Resources

- [Composer Documentation](<https://getcomposer.org/doc/>)
- [PSR-4 Autoloading Standard](<https://www.php-fig.org/psr/psr-4/>)
- [Packagist - PHP Package Repository](<https://packagist.org/>)
- [Semantic Versioning](<https://semver.org/>)
- [Composer Best Practices](<https://blog.martinhujer.cz/17-tips-for-using-composer-efficiently/>)
