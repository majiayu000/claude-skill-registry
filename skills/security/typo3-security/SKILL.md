---
name: typo3-security
description: Security hardening checklist and best practices for TYPO3 v13/v14 installations, covering configuration, file permissions, and common vulnerabilities.
version: 2.0.0
typo3_compatibility: "13.0 - 14.x"
triggers:
  - security
  - hardening
  - permissions
  - authentication
  - vulnerabilities
---

# TYPO3 Security Hardening

> **Compatibility:** TYPO3 v13.x and v14.x (v14 preferred)
> All security configurations in this skill work on both v13 and v14.

## 1. Critical Configuration Settings

### `config/system/settings.php` (v13/v14 Compatible)

```php
<?php
return [
    'BE' => [
        // Disable debug in production
        'debug' => false,
        
        // Session security
        'lockIP' => 4,                    // Lock backend session to full IP
        'lockIPv6' => 8,                  // Lock to IPv6 prefix
        'sessionTimeout' => 3600,         // 1 hour session timeout
        'lockSSL' => true,                // Force HTTPS for backend
        
        // Password policy (enhanced in v13/v14)
        'passwordHashing' => [
            'className' => \TYPO3\CMS\Core\Crypto\PasswordHashing\Argon2idPasswordHash::class,
            'options' => [],
        ],
    ],
    
    'FE' => [
        'debug' => false,
        'lockIP' => 0,                    // Usually 0 for frontend (mobile users)
        'sessionTimeout' => 86400,
        'lockSSL' => true,
        'passwordHashing' => [
            'className' => \TYPO3\CMS\Core\Crypto\PasswordHashing\Argon2idPasswordHash::class,
            'options' => [],
        ],
    ],
    
    'SYS' => [
        // NEVER display errors in production
        'displayErrors' => 0,
        'devIPmask' => '',                // No dev IPs in production
        'errorHandlerErrors' => E_ALL & ~E_NOTICE & ~E_DEPRECATED,
        'exceptionalErrors' => E_ALL & ~E_NOTICE & ~E_WARNING & ~E_DEPRECATED,
        
        // Encryption key (generate unique per installation)
        'encryptionKey' => 'generate-unique-key-per-installation',
        
        // Trusted hosts pattern (CRITICAL)
        'trustedHostsPattern' => 'example\\.com|www\\.example\\.com',
        
        // File handling security
        'textfile_ext' => 'txt,html,htm,css,js,tmpl,ts,typoscript,xml,svg',
        'mediafile_ext' => 'gif,jpg,jpeg,png,webp,svg,pdf,mp3,mp4,webm',
        
        // Security features (v13/v14)
        'features' => [
            'security.backend.enforceReferrer' => true,
            'security.frontend.enforceContentSecurityPolicy' => true,
            'security.backend.enforceContentSecurityPolicy' => true,
        ],
    ],
    
    'LOG' => [
        'writerConfiguration' => [
            \Psr\Log\LogLevel::WARNING => [
                \TYPO3\CMS\Core\Log\Writer\FileWriter::class => [
                    'logFile' => 'var/log/typo3-warning.log',
                ],
            ],
            \Psr\Log\LogLevel::ERROR => [
                \TYPO3\CMS\Core\Log\Writer\FileWriter::class => [
                    'logFile' => 'var/log/typo3-error.log',
                ],
                \TYPO3\CMS\Core\Log\Writer\SyslogWriter::class => [],
            ],
        ],
    ],
];
```

## 2. Trusted Hosts Pattern

**CRITICAL**: Always configure `trustedHostsPattern` to prevent host header injection.

```php
// ❌ DANGEROUS - Allows any host
'trustedHostsPattern' => '.*',

// ✅ SECURE - Explicit host list
'trustedHostsPattern' => 'example\\.com|www\\.example\\.com',

// ✅ SECURE - Regex for subdomains
'trustedHostsPattern' => '(.*\\.)?example\\.com',

// Development with DDEV
'trustedHostsPattern' => '(.*\\.)?example\\.com|.*\\.ddev\\.site',
```

## 3. File System Security

### Directory Permissions

```bash
# Set correct ownership (adjust www-data to your web user)
chown -R www-data:www-data /var/www/html

# Directories: 2775 (group sticky)
find /var/www/html -type d -exec chmod 2775 {} \;

# Files: 664
find /var/www/html -type f -exec chmod 664 {} \;

# Configuration files: more restrictive
chmod 660 config/system/settings.php
chmod 660 config/system/additional.php

# var directory (writable)
chmod -R 2775 var/

# public/fileadmin (writable for uploads)
chmod -R 2775 public/fileadmin/
chmod -R 2775 public/typo3temp/
```

### Critical Files to Protect

Never expose these in `public/`:

```
❌ var/log/
❌ config/
❌ .env
❌ composer.json
❌ composer.lock
❌ .git/
❌ vendor/ (should be outside public)
```

### .htaccess Security (Apache)

```apache
# public/.htaccess additions

# Block access to hidden files
<FilesMatch "^\.">
    Require all denied
</FilesMatch>

# Block access to sensitive file types
<FilesMatch "\.(sql|sqlite|bak|backup|log|sh)$">
    Require all denied
</FilesMatch>

# Block PHP execution in upload directories
<Directory "fileadmin">
    <FilesMatch "\.php$">
        Require all denied
    </FilesMatch>
</Directory>

# Security headers
<IfModule mod_headers.c>
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
</IfModule>
```

### Nginx Security

```nginx
# Block hidden files
location ~ /\. {
    deny all;
}

# Block sensitive directories
location ~ ^/(config|var|vendor)/ {
    deny all;
}

# Block PHP in upload directories
location ~ ^/fileadmin/.*\.php$ {
    deny all;
}

# Security headers
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

## 4. Install Tool Security

### Disable Install Tool

```bash
# Remove enable file after installation
rm public/typo3conf/ENABLE_INSTALL_TOOL
```

### Secure Install Tool Password

Generate strong password and store securely:

```bash
# Generate random password
openssl rand -base64 32
```

Set the hashed password via the Install Tool or an environment-specific `config/system/additional.php`; never commit a placeholder or empty string.

### IP Restriction for Install Tool

```php
// config/system/additional.php
$GLOBALS['TYPO3_CONF_VARS']['BE']['installToolPassword'] = '$argon2id$...'; // hashed
```

## 5. Backend User Security

### Strong Password Policy (v13/v14)

```php
<?php
// ext_localconf.php of site extension
$GLOBALS['TYPO3_CONF_VARS']['BE']['passwordPolicy'] = 'default';
$GLOBALS['TYPO3_CONF_VARS']['BE']['passwordPolicies']['default'] = [
    'validators' => [
        \TYPO3\CMS\Core\PasswordPolicy\Validator\CorePasswordValidator::class => [
            'options' => [
                'minimumLength' => 12,
                'upperCaseCharacterRequired' => true,
                'lowerCaseCharacterRequired' => true,
                'digitCharacterRequired' => true,
                'specialCharacterRequired' => true,
            ],
        ],
        \TYPO3\CMS\Core\PasswordPolicy\Validator\NotCurrentPasswordValidator::class => [],
    ],
];
```

### Multi-Factor Authentication (Built-in v13/v14)

MFA is built into TYPO3 v13 and v14. Users can configure in:
**User Settings > Account Security**

Supported providers:
- TOTP (Time-based One-Time Password)
- Recovery Codes

```php
// Force MFA for all admin users (recommended)
// Backend user TSconfig
options.backendUserLanguage = default
```

### Backend Access Logging

```php
// Log all backend logins
$GLOBALS['TYPO3_CONF_VARS']['LOG']['TYPO3']['CMS']['Backend']['Authentication']['writerConfiguration'] = [
    \Psr\Log\LogLevel::INFO => [
        \TYPO3\CMS\Core\Log\Writer\FileWriter::class => [
            'logFile' => 'var/log/backend-auth.log',
        ],
    ],
];
```

## 6. Content Security Policy (CSP)

### Built-in CSP (v13/v14)

TYPO3 v13+ has built-in CSP support. Enable it:

```php
// config/system/settings.php
$GLOBALS['TYPO3_CONF_VARS']['SYS']['features']['security.frontend.enforceContentSecurityPolicy'] = true;
$GLOBALS['TYPO3_CONF_VARS']['SYS']['features']['security.backend.enforceContentSecurityPolicy'] = true;
```

### CSP Configuration via Events (v13/v14)

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\Directive;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\Event\PolicyMutatedEvent;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\UriValue;

#[AsEventListener(identifier: 'vendor-extension/csp-modification')]
final class ContentSecurityPolicyListener
{
    public function __invoke(PolicyMutatedEvent $event): void
    {
        // Only modify frontend policy
        if ($event->getScope()->type->isFrontend()) {
            $event->getCurrentPolicy()
                ->extend(Directive::ScriptSrc, new UriValue('https://cdn.example.com'))
                ->extend(Directive::StyleSrc, new UriValue('https://fonts.googleapis.com'));
        }
    }
}
```

### TypoScript CSP Headers (Alternative)

```typoscript
config.additionalHeaders {
    10.header = Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; frame-ancestors 'self';
}
```

## 7. SQL Injection Prevention

### ALWAYS Use QueryBuilder

```php
<?php
declare(strict_types=1);

// ❌ VULNERABLE - Never do this
$result = $connection->executeQuery(
    "SELECT * FROM pages WHERE uid = " . $_GET['id']
);

// ✅ SECURE - Use QueryBuilder with prepared statements
$queryBuilder = $this->connectionPool->getQueryBuilderForTable('pages');
$result = $queryBuilder
    ->select('*')
    ->from('pages')
    ->where(
        $queryBuilder->expr()->eq(
            'uid',
            $queryBuilder->createNamedParameter($id, \TYPO3\CMS\Core\Database\Connection::PARAM_INT)
        )
    )
    ->executeQuery();
```

### Extbase Repository Safety

```php
<?php
declare(strict_types=1);

// Extbase automatically escapes parameters
$query = $this->createQuery();
$query->matching(
    $query->equals('uid', $id)  // Safe - auto-escaped
);
```

## 8. XSS Prevention

### Fluid Templates

```html
<!-- ✅ SAFE - Auto-escaped -->
{variable}

<!-- ❌ DANGEROUS - Raw output -->
{variable -> f:format.raw()}

<!-- ✅ SAFE - Explicit escaping -->
{variable -> f:format.htmlspecialchars()}

<!-- For HTML content, use with caution -->
<f:format.html>{bodytext}</f:format.html>
```

### Backend Forms

TCA automatically handles escaping. For custom fields:

```php
'config' => [
    'type' => 'input',
    'max' => 255,
    // Input is automatically escaped
],
```

## 9. CSRF Protection

### Backend Requests (v13/v14)

TYPO3 backend automatically includes CSRF tokens. For custom AJAX:

```php
<?php
declare(strict_types=1);

use TYPO3\CMS\Core\FormProtection\FormProtectionFactory;

final class MyController
{
    public function __construct(
        private readonly FormProtectionFactory $formProtectionFactory,
    ) {}

    public function generateToken(): string
    {
        $formProtection = $this->formProtectionFactory->createFromRequest($this->request);
        return $formProtection->generateToken('myFormIdentifier');
    }

    public function validateToken(string $token): bool
    {
        $formProtection = $this->formProtectionFactory->createFromRequest($this->request);
        return $formProtection->validateToken($token, 'myFormIdentifier');
    }
}
```

### Frontend Forms (Extbase)

```html
<!-- Fluid form with CSRF -->
<f:form action="submit" controller="Contact" method="post">
    <f:form.hidden name="__trustedProperties" value="{trustedProperties}" />
    <!-- Form fields -->
</f:form>
```

## 10. Rate Limiting (v13/v14)

TYPO3 v13+ includes built-in rate limiting:

```php
// config/system/additional.php
$GLOBALS['TYPO3_CONF_VARS']['SYS']['features']['security.backend.rateLimiter'] = true;

// Configure rate limits
$GLOBALS['TYPO3_CONF_VARS']['BE']['loginRateLimit'] = 5;  // attempts per minute
```

## 11. Security Audit Checklist

### Before Go-Live

- [ ] `displayErrors` = 0
- [ ] `debug` = false (BE and FE)
- [ ] `trustedHostsPattern` configured
- [ ] Install Tool disabled
- [ ] HTTPS enforced (`lockSSL` = true)
- [ ] Strong backend passwords (12+ chars)
- [ ] MFA enabled for admins
- [ ] File permissions correct
- [ ] Sensitive directories protected
- [ ] Error logs to files, not screen
- [ ] Encryption key unique
- [ ] CSP enabled
- [ ] Rate limiting enabled

### Regular Maintenance

- [ ] Update TYPO3 core monthly
- [ ] Update extensions monthly
- [ ] Review security bulletins (https://typo3.org/security)
- [ ] Audit backend user accounts
- [ ] Review access logs
- [ ] Test backup restoration

### Monitoring

- [ ] Set up uptime monitoring
- [ ] Configure error alerting
- [ ] Monitor authentication failures
- [ ] Track file integrity (optional)

## 12. Security Resources

- **TYPO3 Security Team**: https://typo3.org/teams/security
- **Security Bulletins**: https://typo3.org/security/advisory
- **Security Guide**: https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Security/Index.html
- **v13 Security Features**: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-13/Index.html
- **v14 Security Features**: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-14/Index.html

---

## Credits & Attribution

This skill is based on the excellent TYPO3 best practices and methodology developed by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**. We are deeply grateful for their
outstanding contributions to the TYPO3 community and their commitment to sharing knowledge.

Netresearch has been a leading force in TYPO3 development, and their expertise has been
invaluable in shaping these guidelines. Thank you, Netresearch, for your exceptional work!

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
