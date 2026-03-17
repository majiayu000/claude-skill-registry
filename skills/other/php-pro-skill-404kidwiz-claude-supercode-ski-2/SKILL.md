---
name: php-pro
description: PHP 8.2+ specialist with expertise in modern patterns, Composer ecosystem, and enterprise PHP development. Use when building PHP applications, optimizing performance, or modernizing legacy PHP code. Triggers include "PHP", "Composer", "PHP 8", "PSR", "Symfony components", "PHP performance".
---

# PHP Pro

## Purpose
Provides expert guidance on modern PHP development using PHP 8.2+ features, modern patterns, and the Composer ecosystem. Specializes in building enterprise-grade PHP applications with proper architecture and performance optimization.

## When to Use
- Building modern PHP applications
- Using PHP 8.2+ features (readonly, enums, attributes)
- Working with Composer and packages
- Implementing PSR standards
- Optimizing PHP performance
- Modernizing legacy PHP codebases
- Building APIs with pure PHP
- Using Symfony components standalone

## Quick Start
**Invoke this skill when:**
- Developing PHP 8.2+ applications
- Working with Composer packages
- Implementing PSR standards
- Optimizing PHP performance
- Modernizing legacy PHP

**Do NOT invoke when:**
- Laravel-specific development → use `/laravel-specialist`
- WordPress development → use `/wordpress-master`
- General API design → use `/api-designer`
- Database design → use `/database-administrator`

## Decision Framework
```
PHP Project Type?
├── Full Framework
│   ├── Rapid development → Laravel
│   └── Enterprise/Symfony → Symfony
├── Microframework
│   └── Slim / Mezzio
├── API Only
│   └── API Platform / Slim
└── Standalone Components
    └── Symfony Components + Composer
```

## Core Workflows

### 1. Modern PHP Setup
1. Install PHP 8.2+ with required extensions
2. Initialize Composer project
3. Configure PSR-4 autoloading
4. Set up coding standards (PHP-CS-Fixer, PHPStan)
5. Configure error handling
6. Implement dependency injection

### 2. PHP 8.2+ Feature Usage
1. Use readonly classes for DTOs
2. Apply enums for fixed value sets
3. Leverage attributes for metadata
4. Use named arguments for clarity
5. Implement intersection types
6. Apply null-safe operator

### 3. Performance Optimization
1. Enable OPcache with proper settings
2. Use preloading for stable code
3. Implement JIT where beneficial
4. Profile with Xdebug/Blackfire
5. Optimize database queries
6. Implement caching layers

## Best Practices
- Use strict types in all files (`declare(strict_types=1)`)
- Follow PSR-12 coding standards
- Use type hints for all parameters and returns
- Leverage Composer for autoloading
- Use PHPStan or Psalm for static analysis
- Write tests with PHPUnit or Pest

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| No type hints | Runtime errors | Use strict types |
| Global state | Hard to test | Dependency injection |
| Manual autoloading | Error-prone | Composer autoload |
| Suppressing errors (@) | Hidden bugs | Handle errors properly |
| No static analysis | Type bugs | PHPStan/Psalm |
