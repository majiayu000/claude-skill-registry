---
name: acc-troubleshooting-template
description: Generates troubleshooting guides and FAQ sections for PHP projects. Creates problem-solution documentation.
---

# Troubleshooting Template Generator

Generate helpful troubleshooting guides and FAQ documentation.

## Document Structure

```markdown
# Troubleshooting

## Quick Fixes
{common issues with quick solutions}

## Installation Issues
{installation problems}

## Configuration Issues
{config problems}

## Runtime Errors
{errors during execution}

## FAQ
{frequently asked questions}

## Getting Help
{how to report issues}
```

## Section Templates

### Quick Fixes Section

```markdown
## Quick Fixes

### Reset to Known Good State

```bash
# Clear cache
rm -rf var/cache/*

# Reinstall dependencies
rm -rf vendor/ composer.lock
composer install

# Verify installation
php vendor/bin/package verify
```

### Check Common Issues

| Symptom | Quick Fix |
|---------|-----------|
| "Class not found" | Run `composer dump-autoload` |
| Permission denied | Run `chmod -R 755 var/` |
| Config not loading | Check `.env` file exists |
| Connection refused | Verify service is running |
```

### Installation Issues Section

```markdown
## Installation Issues

### Composer Install Fails

**Symptom:**
```
Your requirements could not be resolved to an installable set of packages.
```

**Solutions:**

1. **Update Composer:**
   ```bash
   composer self-update
   ```

2. **Clear Composer cache:**
   ```bash
   composer clear-cache
   ```

3. **Check PHP version:**
   ```bash
   php -v
   # Must be 8.5 or higher
   ```

4. **Check required extensions:**
   ```bash
   php -m | grep -E "json|pdo|mbstring"
   ```

---

### Extension Not Found

**Symptom:**
```
PHP Fatal error: Uncaught Error: Call to undefined function json_encode()
```

**Solution:**

Install missing PHP extension:

```bash
# Ubuntu/Debian
sudo apt-get install php8.5-json

# macOS with Homebrew
brew install php@8.5

# Verify
php -m | grep json
```
```

### Configuration Issues Section

```markdown
## Configuration Issues

### Environment Variables Not Loading

**Symptom:**
```
API key not configured
```

**Checklist:**

1. **Verify `.env` file exists:**
   ```bash
   ls -la .env
   ```

2. **Check variable is set:**
   ```bash
   grep "PACKAGE_API_KEY" .env
   ```

3. **Verify no syntax errors:**
   ```bash
   # Values with spaces need quotes
   PACKAGE_NAME="My App Name"  # ✅ Correct
   PACKAGE_NAME=My App Name    # ❌ Wrong
   ```

4. **Clear config cache:**
   ```bash
   php artisan config:clear  # Laravel
   rm var/cache/config.php   # Other frameworks
   ```

---

### Invalid Configuration Value

**Symptom:**
```
Configuration error: 'timeout' must be a positive integer
```

**Solution:**

Check `config/package.php`:

```php
// ❌ Wrong
'timeout' => '30',  // String instead of int

// ✅ Correct
'timeout' => 30,    // Integer
```
```

### Runtime Errors Section

```markdown
## Runtime Errors

### Connection Timeout

**Symptom:**
```
Error: Connection timed out after 30 seconds
```

**Possible Causes:**

1. **Network issues** — Check connectivity
2. **Firewall blocking** — Check outbound rules
3. **Service down** — Check status page
4. **Timeout too short** — Increase timeout

**Solutions:**

```php
// Increase timeout
$client = new Client([
    'timeout' => 60,  // 60 seconds
]);
```

```bash
# Test connectivity
curl -v https://api.example.com/health
```

---

### Rate Limit Exceeded

**Symptom:**
```json
{
    "error": {
        "code": "RATE_LIMITED",
        "message": "Too many requests"
    }
}
```

**Solutions:**

1. **Implement backoff:**
   ```php
   $client = new Client([
       'retry' => [
           'max_attempts' => 3,
           'delay' => 1000,  // ms
       ],
   ]);
   ```

2. **Cache responses:**
   ```php
   $cache = new RedisCache();
   $client = new Client(['cache' => $cache]);
   ```

3. **Upgrade plan** for higher limits

---

### Memory Limit Exceeded

**Symptom:**
```
PHP Fatal error: Allowed memory size of 134217728 bytes exhausted
```

**Solutions:**

1. **Process in batches:**
   ```php
   foreach ($client->paginate(100) as $batch) {
       process($batch);
   }
   ```

2. **Increase memory limit:**
   ```php
   ini_set('memory_limit', '256M');
   ```

3. **Use generators:**
   ```php
   foreach ($client->stream() as $item) {
       yield process($item);
   }
   ```
```

### FAQ Section

```markdown
## FAQ

### General

<details>
<summary><strong>Q: What PHP version is required?</strong></summary>

PHP 8.5 or higher is required. Check your version:

```bash
php -v
```
</details>

<details>
<summary><strong>Q: Is this library production-ready?</strong></summary>

Yes, the library is used in production by many projects. We follow semantic versioning and maintain backward compatibility within major versions.
</details>

### Configuration

<details>
<summary><strong>Q: How do I configure multiple environments?</strong></summary>

Use environment-specific `.env` files:

```bash
.env           # Base configuration
.env.local     # Local overrides (not committed)
.env.test      # Test environment
.env.prod      # Production environment
```
</details>

<details>
<summary><strong>Q: Can I use environment variables directly?</strong></summary>

Yes, you can pass configuration directly:

```php
$client = new Client([
    'api_key' => getenv('MY_API_KEY'),
]);
```
</details>

### Performance

<details>
<summary><strong>Q: How can I improve performance?</strong></summary>

1. **Enable caching** — Reduces API calls
2. **Use connection pooling** — Reuse connections
3. **Batch requests** — Reduce round trips
4. **Use async** — Parallel processing

```php
$client = new Client([
    'cache' => new RedisCache(),
    'pool_size' => 10,
]);
```
</details>
```

### Getting Help Section

```markdown
## Getting Help

### Before Asking for Help

1. **Search existing issues:** [GitHub Issues](https://github.com/vendor/package/issues)
2. **Check documentation:** [Docs](https://docs.example.com)
3. **Review changelog:** [CHANGELOG.md](CHANGELOG.md)

### Collect Debug Information

Run this command and include output in your issue:

```bash
php -v
composer show vendor/package
php -m | grep -E "json|pdo|curl"
```

### Report a Bug

Create an issue with:

1. **Description** — What happened?
2. **Expected** — What should have happened?
3. **Steps to reproduce** — How can we reproduce it?
4. **Environment** — PHP version, OS, package version
5. **Error message** — Full stack trace

### Ask a Question

- 💬 [GitHub Discussions](https://github.com/vendor/package/discussions)
- 📚 [Stack Overflow](https://stackoverflow.com/questions/tagged/package-name)
```

## Complete Example

```markdown
# Troubleshooting

## Quick Fixes

| Problem | Solution |
|---------|----------|
| Class not found | `composer dump-autoload` |
| Permission denied | `chmod -R 755 var/` |
| Config missing | Check `.env` exists |

## Common Errors

### "Invalid API Key"

**Symptom:**
```
Error: Invalid API key provided
```

**Solutions:**

1. Verify key in `.env`:
   ```bash
   grep "API_KEY" .env
   ```

2. Check for extra whitespace:
   ```
   API_KEY=abc123   # ✅ No quotes needed
   API_KEY= abc123  # ❌ Extra space
   ```

3. Regenerate key at [dashboard](https://example.com/dashboard)

## FAQ

<details>
<summary><strong>Q: Why am I getting rate limited?</strong></summary>

Free tier allows 100 requests/hour. Upgrade for more.
</details>

## Get Help

- 📖 [Documentation](docs/)
- 🐛 [Report Bug](https://github.com/vendor/package/issues/new)
- 💬 [Ask Question](https://github.com/vendor/package/discussions)
```

## Generation Instructions

When generating troubleshooting docs:

1. **Start with symptoms** — What user sees
2. **Explain causes** — Why it happens
3. **Provide solutions** — Step-by-step fixes
4. **Include verification** — How to confirm fix
5. **Use collapsible FAQ** — Reduce scrolling
6. **Link to help** — Where to get more support
