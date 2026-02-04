---
name: acc-getting-started-template
description: Generates Getting Started guides for PHP projects. Creates step-by-step tutorials for first-time users.
---

# Getting Started Template Generator

Generate beginner-friendly quick start guides.

## Document Structure

```markdown
# Getting Started

## Prerequisites
{what users need before starting}

## Installation
{step-by-step installation}

## Configuration
{basic config setup}

## Your First {Thing}
{hands-on tutorial}

## Next Steps
{where to go from here}
```

## Section Templates

### Prerequisites Section

```markdown
## Prerequisites

Before you begin, ensure you have:

- [ ] PHP 8.5 or higher
- [ ] Composer 2.0 or higher
- [ ] A database (PostgreSQL 16+ recommended)
- [ ] Basic PHP knowledge

### Verify Your Environment

```bash
# Check PHP version
php -v
# Expected: PHP 8.5.x

# Check Composer version
composer -V
# Expected: Composer version 2.x.x

# Check required extensions
php -m | grep -E "json|pdo|mbstring"
```
```

### Installation Section

```markdown
## Installation

### Step 1: Install via Composer

```bash
composer require vendor/package
```

### Step 2: Copy Configuration (optional)

```bash
cp vendor/vendor/package/config/config.php config/package.php
```

### Step 3: Set Environment Variables

Add to your `.env` file:

```bash
PACKAGE_API_KEY=your-api-key-here
PACKAGE_DEBUG=false
```

### Step 4: Verify Installation

```bash
php -r "require 'vendor/autoload.php'; echo 'OK';"
```

You should see `OK` if everything is installed correctly.
```

### Configuration Section

```markdown
## Configuration

### Basic Configuration

Create `config/package.php`:

```php
<?php

return [
    'api_key' => env('PACKAGE_API_KEY'),
    'debug' => env('PACKAGE_DEBUG', false),
    'timeout' => 30,
];
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `api_key` | string | - | Your API key (required) |
| `debug` | bool | false | Enable debug mode |
| `timeout` | int | 30 | Request timeout in seconds |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PACKAGE_API_KEY` | Yes | Your API key |
| `PACKAGE_DEBUG` | No | Enable debug logging |
```

### Tutorial Section

```markdown
## Your First {Operation}

Let's create your first {thing} step by step.

### Step 1: Create the {Thing}

Create a new file `example.php`:

```php
<?php

declare(strict_types=1);

require 'vendor/autoload.php';

use Vendor\Package\Client;

// Initialize the client
$client = new Client([
    'api_key' => 'your-api-key',
]);

echo "Client initialized!\n";
```

Run it:

```bash
php example.php
# Output: Client initialized!
```

### Step 2: Perform an Action

Add to your file:

```php
// Create a resource
$result = $client->create([
    'name' => 'My First Item',
    'type' => 'example',
]);

echo "Created: " . $result->id . "\n";
```

Run it:

```bash
php example.php
# Output:
# Client initialized!
# Created: item_abc123
```

### Step 3: Retrieve the Result

Add to your file:

```php
// Retrieve the resource
$item = $client->get($result->id);

echo "Name: " . $item->name . "\n";
echo "Status: " . $item->status . "\n";
```

Run it:

```bash
php example.php
# Output:
# Client initialized!
# Created: item_abc123
# Name: My First Item
# Status: active
```

### Complete Example

Here's the complete code:

```php
<?php

declare(strict_types=1);

require 'vendor/autoload.php';

use Vendor\Package\Client;

// Initialize
$client = new Client([
    'api_key' => 'your-api-key',
]);

// Create
$result = $client->create([
    'name' => 'My First Item',
    'type' => 'example',
]);

// Retrieve
$item = $client->get($result->id);

// Output
echo "ID: " . $item->id . "\n";
echo "Name: " . $item->name . "\n";
echo "Status: " . $item->status . "\n";
```
```

### Next Steps Section

```markdown
## Next Steps

Congratulations! You've completed the getting started guide. Here's what to explore next:

### Learn More

- 📖 [Configuration Guide](configuration.md) — Advanced configuration options
- 🔧 [API Reference](api/README.md) — Complete API documentation
- 💡 [Examples](examples/) — More code examples

### Common Use Cases

| Use Case | Guide |
|----------|-------|
| Authentication | [Auth Guide](guides/authentication.md) |
| Error Handling | [Error Guide](guides/errors.md) |
| Testing | [Testing Guide](guides/testing.md) |

### Get Help

- 📚 [FAQ](faq.md) — Frequently asked questions
- 🐛 [Troubleshooting](troubleshooting.md) — Common issues
- 💬 [Community](https://github.com/vendor/package/discussions) — Ask questions
- 🐙 [GitHub Issues](https://github.com/vendor/package/issues) — Report bugs
```

## Complete Example

```markdown
# Getting Started with Awesome Package

This guide will help you install and use Awesome Package in under 5 minutes.

## Prerequisites

Before you begin, ensure you have:

- [ ] PHP 8.5 or higher
- [ ] Composer 2.0 or higher

```bash
# Verify requirements
php -v && composer -V
```

## Installation

```bash
composer require vendor/awesome-package
```

## Your First Request

Create `hello.php`:

```php
<?php

declare(strict_types=1);

require 'vendor/autoload.php';

use Vendor\AwesomePackage\Client;

$client = new Client();
$response = $client->ping();

echo "Server says: " . $response->message . "\n";
```

Run it:

```bash
php hello.php
# Output: Server says: pong
```

## Create Something Useful

Now let's create a real resource:

```php
<?php

declare(strict_types=1);

require 'vendor/autoload.php';

use Vendor\AwesomePackage\Client;
use Vendor\AwesomePackage\Model\Widget;

$client = new Client(['api_key' => 'your-key']);

// Create a widget
$widget = $client->widgets->create(
    new Widget(
        name: 'My Widget',
        color: 'blue'
    )
);

echo "Created widget: {$widget->id}\n";

// List all widgets
$widgets = $client->widgets->list();

foreach ($widgets as $w) {
    echo "- {$w->name} ({$w->color})\n";
}
```

## Next Steps

- 📖 [Full Documentation](docs/README.md)
- 🔧 [Configuration Options](docs/configuration.md)
- 💡 [More Examples](docs/examples/)
```

## Generation Instructions

When generating Getting Started guides:

1. **Keep it simple** — Minimum steps to first success
2. **Show don't tell** — Code examples over prose
3. **Test all examples** — Ensure they run as shown
4. **Provide expected output** — Users know if it works
5. **Link to more info** — Next steps for deeper learning
6. **Use checkboxes** — For prerequisites
7. **Progressive complexity** — Build on each step
