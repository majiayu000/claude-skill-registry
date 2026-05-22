---
name: laravel-dusk
description: Laravel Dusk - Browser automation and testing API for Laravel applications. Use when writing browser tests, automating UI testing, testing JavaScript interactions, or implementing end-to-end tests in Laravel.
---
## When to Use This Skill

This skill should be triggered when:
- Writing or debugging browser automation tests for Laravel
- Testing user interfaces and JavaScript interactions
- Implementing end-to-end (E2E) testing workflows
- Setting up automated UI testing in Laravel applications
- Working with form submissions, authentication flows, or page navigation tests
- Configuring ChromeDriver or alternative browser drivers
- Using the Page Object pattern for test organization
- Testing Vue.js components or waiting for JavaScript events
- Troubleshooting browser test failures or timing issues

## Key Concepts

### Dusk Selectors vs CSS Selectors

**Dusk selectors** (recommended) use HTML `dusk` attributes that won't change with UI updates:
- More stable than CSS classes or IDs
- Explicitly mark elements for testing
- Use `@` prefix in tests: `$browser->click('@submit-button')`
- Add to HTML: `<button dusk="submit-button">Submit</button>`

**CSS selectors** are more brittle but sometimes necessary:
- `.class-name`, `#id`, `div > button`
- Can break when HTML structure changes
- Use when you don't control the HTML

### Waiting Strategies

**Always wait explicitly** rather than using arbitrary pauses:
- `waitFor('.selector')` - Wait for element to exist
- `waitUntilMissing('.selector')` - Wait for element to disappear
- `waitForText('text')` - Wait for text to appear
- `waitUntil('condition')` - Wait for JavaScript condition
- `whenAvailable('.selector', callback)` - Run callback when available

### Page Objects

Organize complex test logic into **Page classes**:
- Define URL, assertions, and element selectors
- Create reusable methods for page-specific actions
- Improve test readability and maintainability
- Generate with: `php artisan dusk:page PageName`

### Browser Macros

Define **reusable browser methods** for common patterns:
- Register in service provider's `boot()` method
- Use across all tests
- Chain like built-in methods
- Example: scrolling, modal interactions, custom assertions

## Working with This Skill

### For Beginners

1. **Start with basic tests**: Use simple `visit()`, `type()`, `press()`, and `assertSee()` methods
2. **Use Dusk selectors**: Add `dusk` attributes to your HTML for stable selectors
3. **Learn waiting**: Always use `waitFor()` instead of `pause()` for reliable tests
4. **Run tests**: Execute with `php artisan dusk` to see results

### For Intermediate Users

1. **Implement Page Objects**: Organize complex tests with the Page pattern
2. **Use database traits**: Choose between `DatabaseMigrations` or `DatabaseTruncation`
3. **Create browser macros**: Define reusable methods for common workflows
4. **Test authentication**: Use `loginAs()` to bypass login screens
5. **Handle JavaScript**: Use `waitUntil()` for dynamic content and AJAX

### For Advanced Users

1. **Multi-browser testing**: Test real-time features with multiple browsers
2. **Custom waiting logic**: Use `waitUsing()` for complex conditions
3. **Component pattern**: Create reusable components for shared UI elements
4. **CI/CD integration**: Set up Dusk in GitHub Actions, Travis CI, or other platforms
5. **Alternative drivers**: Configure Selenium Grid or other browsers beyond ChromeDriver

### Navigation Tips

- **Quick examples**: Check the Quick Reference section above for common patterns
- **Method documentation**: See `other.md` for complete API reference
- **Assertions list**: Reference file contains all 70+ available assertions
- **Configuration**: Check reference file for environment setup and driver options
- **Best practices**: Look for "Best Practices" section in reference documentation

## Installation & Setup

```bash
# Install Laravel Dusk
composer require laravel/dusk --dev

# Run installation
php artisan dusk:install

# Update ChromeDriver
php artisan dusk:chrome-driver

# Make binaries executable (Unix)
chmod -R 0755 vendor/laravel/dusk/bin/

# Run tests
php artisan dusk
```

## Common Commands

```bash
# Generate new test
php artisan dusk:make LoginTest

# Generate page object
php artisan dusk:page Dashboard

# Generate component
php artisan dusk:component Modal

# Run all tests
php artisan dusk

# Run specific test
php artisan dusk tests/Browser/LoginTest.php

# Run failed tests only
php artisan dusk:fails

# Run with filter
php artisan dusk --group=authentication

# Update ChromeDriver
php artisan dusk:chrome-driver --detect
```

## Resources

### Official Documentation
- Laravel Dusk Documentation: https://laravel.com/docs/12.x/dusk
- API Reference: See `references/other.md` for complete method listings

### Common Patterns in Reference Files

The reference documentation includes:
- 70+ assertion methods with descriptions
- Complete form interaction API
- Waiting strategies and timing best practices
- Page Object pattern examples
- Browser macro definitions
- CI/CD configuration examples
- Environment-specific test setup

## Best Practices

1. **Use Dusk selectors** (`dusk` attributes) instead of CSS classes for stability
2. **Wait explicitly** with `waitFor()` methods instead of arbitrary `pause()`
3. **Organize with Page Objects** for complex test scenarios
4. **Leverage database truncation** for faster test execution
5. **Create browser macros** for frequently repeated actions
6. **Scope selectors** with `with()` or `elsewhere()` for specific page regions
7. **Test user behavior** rather than implementation details
8. **Use authentication shortcuts** like `loginAs()` to skip login flows
9. **Take screenshots** with `screenshot()` for debugging failures
10. **Group related tests** and use `--group` flag for targeted execution

## Notes

- Laravel Dusk uses ChromeDriver by default (no Selenium/JDK required)
- Supports alternative browsers via Selenium WebDriver protocol
- Tests are stored in `tests/Browser` directory
- Page objects go in `tests/Browser/Pages`
- Screenshots saved to `tests/Browser/screenshots` on failure
- Console logs saved to `tests/Browser/console` for debugging


---

## References

**Quick Reference:** `read .claude/skills/laravel-dusk/references/quick-reference.md`
**Reference Files:** `read .claude/skills/laravel-dusk/references/reference-files.md`
**Troubleshooting:** `read .claude/skills/laravel-dusk/references/troubleshooting.md`
