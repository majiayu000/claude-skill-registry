---
name: acc-code-examples-template
description: Generates code examples for PHP documentation. Creates minimal, copy-paste ready examples with expected output.
---

# Code Examples Template Generator

Generate effective code examples for documentation.

## Example Principles

### The Three Types

| Type | Purpose | Length | Use When |
|------|---------|--------|----------|
| **Minimal** | Show single concept | 5-10 lines | Teaching one thing |
| **Complete** | Show full usage | 20-50 lines | Production reference |
| **Progressive** | Build complexity | 3+ examples | Tutorial style |

## Example Templates

### Minimal Example

```php
<?php

use Vendor\Package\Client;

$client = new Client();
$result = $client->process('data');

echo $result->status; // "success"
```

**Characteristics:**
- Single concept
- No error handling
- Shows expected output
- Copy-paste ready

### Complete Example

```php
<?php

declare(strict_types=1);

require 'vendor/autoload.php';

use Vendor\Package\Client;
use Vendor\Package\Config;
use Vendor\Package\Exception\ClientException;

// Configuration
$config = new Config(
    apiKey: getenv('API_KEY') ?: throw new RuntimeException('API_KEY required'),
    timeout: 30,
    retries: 3,
);

// Initialize client
$client = new Client($config);

try {
    // Make request
    $result = $client->process([
        'data' => 'input value',
        'options' => ['validate' => true],
    ]);

    // Handle success
    echo "Status: {$result->status}\n";
    echo "ID: {$result->id}\n";

} catch (ClientException $e) {
    // Handle error
    echo "Error: {$e->getMessage()}\n";
    exit(1);
}

/* Output:
Status: success
ID: res_abc123
*/
```

**Characteristics:**
- Full imports
- Error handling
- Configuration
- Comments for sections
- Expected output

### Progressive Example

```markdown
## Basic Usage

Start with the simplest case:

```php
$client = new Client();
$result = $client->ping();
// "pong"
```

## With Configuration

Add configuration options:

```php
$client = new Client([
    'timeout' => 30,
]);
$result = $client->ping();
// "pong"
```

## With Authentication

Add authentication:

```php
$client = new Client([
    'api_key' => 'your-key',
    'timeout' => 30,
]);
$result = $client->process('data');
// {"status": "success", "id": "..."}
```

## Production Ready

Full example with error handling:

```php
try {
    $client = new Client([
        'api_key' => getenv('API_KEY'),
        'timeout' => 30,
        'retries' => 3,
    ]);

    $result = $client->process('data');
    echo $result->status;

} catch (ClientException $e) {
    error_log($e->getMessage());
    exit(1);
}
```
```

## Example Patterns

### Before/After Pattern

```markdown
### Refactoring Example

**Before (Anti-pattern):**

```php
// ❌ Don't do this
$data = file_get_contents('data.json');
$json = json_decode($data);
if ($json === null) {
    die('Invalid JSON');
}
```

**After (Recommended):**

```php
// ✅ Do this instead
use Vendor\Package\JsonLoader;

$loader = new JsonLoader();
$data = $loader->load('data.json');
// Throws JsonException on invalid data
```
```

### Input/Output Pattern

```markdown
### String Transformation

**Input:**
```php
$input = "Hello World";
```

**Code:**
```php
$result = $transformer->slugify($input);
```

**Output:**
```php
$result = "hello-world";
```
```

### Comparison Pattern

```markdown
### Framework Comparison

**Symfony:**
```php
use Symfony\Component\HttpFoundation\Response;

return new Response('Hello', 200);
```

**Laravel:**
```php
return response('Hello', 200);
```

**Native:**
```php
http_response_code(200);
echo 'Hello';
```
```

## Code Block Guidelines

### Language Tags

```markdown
```php      # PHP code
```bash     # Shell commands
```json     # JSON data
```yaml     # YAML config
```sql      # Database queries
```diff     # Code changes
```

### Highlighting Important Parts

```php
<?php

$client = new Client([
    // highlight-next-line
    'api_key' => 'your-key',  // <-- This is important
    'timeout' => 30,
]);
```

### Showing Line Numbers

```markdown
```php {1,3-5}
<?php                           // Line 1
                               // Line 2
$config = new Config();        // Line 3
$config->setTimeout(30);       // Line 4
$config->setRetries(3);        // Line 5
```
```

## Common Patterns

### CRUD Operations

```markdown
### Create

```php
$item = $client->items->create([
    'name' => 'New Item',
    'price' => 99.99,
]);
echo $item->id; // "item_abc123"
```

### Read

```php
$item = $client->items->get('item_abc123');
echo $item->name; // "New Item"
```

### Update

```php
$item = $client->items->update('item_abc123', [
    'price' => 79.99,
]);
echo $item->price; // 79.99
```

### Delete

```php
$client->items->delete('item_abc123');
// No return value, throws on error
```

### List

```php
$items = $client->items->list(['limit' => 10]);
foreach ($items as $item) {
    echo "{$item->name}: {$item->price}\n";
}
```
```

### Error Handling

```markdown
### Handling Errors

```php
use Vendor\Package\Exception\{
    NotFoundException,
    ValidationException,
    RateLimitException,
};

try {
    $result = $client->process($data);

} catch (NotFoundException $e) {
    // Resource doesn't exist
    echo "Not found: {$e->getMessage()}";

} catch (ValidationException $e) {
    // Invalid input
    foreach ($e->getErrors() as $field => $messages) {
        echo "{$field}: " . implode(', ', $messages) . "\n";
    }

} catch (RateLimitException $e) {
    // Too many requests
    sleep($e->getRetryAfter());
    // Retry...
}
```
```

### Async Operations

```markdown
### Async Processing

```php
// Start async job
$job = $client->jobs->create([
    'type' => 'export',
    'params' => ['format' => 'csv'],
]);

echo "Job started: {$job->id}\n";

// Poll for completion
while ($job->status !== 'completed') {
    sleep(5);
    $job = $client->jobs->get($job->id);
    echo "Status: {$job->status}\n";
}

// Get result
$result = $client->jobs->getResult($job->id);
file_put_contents('export.csv', $result->content);
```
```

## Quality Checklist

### Every Example Should

- [ ] Run without modification (except config)
- [ ] Show expected output
- [ ] Use realistic data (not foo/bar)
- [ ] Include necessary imports
- [ ] Follow PSR-12 style
- [ ] Match current API version

### Avoid

- [ ] Abstract examples that don't run
- [ ] Missing `<?php` tag when standalone
- [ ] Outdated syntax or deprecated methods
- [ ] Foo/Bar/Baz placeholder names
- [ ] Missing required configuration
- [ ] Unexplained magic values

## Generation Instructions

When generating code examples:

1. **Choose example type** based on purpose
2. **Use realistic data** (emails, names, prices)
3. **Include expected output** in comments
4. **Show imports** when needed
5. **Add error handling** in complete examples
6. **Test examples** actually run
7. **Match coding style** of the project
