---
name: PHP Security Patterns
description: Use when essential PHP security patterns including input validation, SQL injection prevention, XSS protection, CSRF tokens, password hashing, secure session management, and defense-in-depth strategies for building secure PHP applications.
allowed-tools: []
---

# PHP Security Patterns

## Introduction

Security is paramount in PHP applications as they often handle sensitive user data,
authentication, and financial transactions. PHP's flexibility and dynamic nature
create opportunities for vulnerabilities if security best practices aren't followed.

Common PHP security vulnerabilities include SQL injection, cross-site scripting
(XSS), cross-site request forgery (CSRF), insecure password storage, session
hijacking, and file inclusion attacks. Each can lead to data breaches, unauthorized
access, or complete system compromise.

This skill covers input validation and sanitization, SQL injection prevention,
XSS protection, CSRF defense, secure password handling, session security, file
upload security, and defense-in-depth strategies.

## Input Validation and Sanitization

Input validation ensures data meets expected formats before processing, while
sanitization removes or encodes potentially dangerous content.

```php
<?php
declare(strict_types=1);

// Email validation
function validateEmail(string $email): bool {
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

// URL validation
function validateUrl(string $url): bool {
    return filter_var($url, FILTER_VALIDATE_URL) !== false;
}

// Integer validation
function validateInt(mixed $value, int $min = PHP_INT_MIN,
                     int $max = PHP_INT_MAX): ?int {
    $int = filter_var($value, FILTER_VALIDATE_INT, [
        'options' => [
            'min_range' => $min,
            'max_range' => $max,
        ],
    ]);

    return $int !== false ? $int : null;
}

// String sanitization
function sanitizeString(string $input): string {
    // Remove null bytes and control characters
    $sanitized = str_replace("\0", '', $input);
    $sanitized = preg_replace('/[\x00-\x1F\x7F]/u', '', $sanitized);
    return trim($sanitized);
}

// HTML sanitization (output encoding)
function sanitizeHtml(string $input): string {
    return htmlspecialchars($input, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}

// Example usage
class UserRegistration {
    private array $errors = [];

    public function validate(array $data): bool {
        // Validate email
        if (!isset($data['email']) || !validateEmail($data['email'])) {
            $this->errors[] = 'Invalid email address';
        }

        // Validate age
        $age = validateInt($data['age'] ?? null, 13, 120);
        if ($age === null) {
            $this->errors[] = 'Age must be between 13 and 120';
        }

        // Validate username (alphanumeric, 3-20 chars)
        $username = sanitizeString($data['username'] ?? '');
        if (!preg_match('/^[a-zA-Z0-9_]{3,20}$/', $username)) {
            $this->errors[] = 'Username must be 3-20 alphanumeric characters';
        }

        // Validate password strength
        if (!$this->validatePassword($data['password'] ?? '')) {
            $this->errors[] = 'Password must be at least 8 characters ' .
                'with mixed case and numbers';
        }

        return empty($this->errors);
    }

    private function validatePassword(string $password): bool {
        return strlen($password) >= 8
            && preg_match('/[A-Z]/', $password)
            && preg_match('/[a-z]/', $password)
            && preg_match('/[0-9]/', $password);
    }

    public function getErrors(): array {
        return $this->errors;
    }
}

// Whitelist validation for enums
function validateStatus(string $status): ?string {
    $allowed = ['pending', 'approved', 'rejected'];
    return in_array($status, $allowed, true) ? $status : null;
}

// Complex data validation
function validateUserData(array $data): array {
    $validated = [];

    // Required fields
    $validated['email'] = validateEmail($data['email'] ?? '')
        ? $data['email']
        : throw new InvalidArgumentException('Invalid email');

    // Optional fields with defaults
    $validated['age'] = validateInt($data['age'] ?? 0, 0, 150) ?? 18;
    $validated['name'] = sanitizeString($data['name'] ?? '');

    // Nested validation
    if (isset($data['address'])) {
        $validated['address'] = [
            'street' => sanitizeString($data['address']['street'] ?? ''),
            'city' => sanitizeString($data['address']['city'] ?? ''),
            'zip' => preg_match('/^\d{5}$/', $data['address']['zip'] ?? '')
                ? $data['address']['zip']
                : null,
        ];
    }

    return $validated;
}
```

Always validate input at the application boundary and sanitize before output to
prevent injection attacks.

## SQL Injection Prevention

SQL injection occurs when user input is directly interpolated into SQL queries,
allowing attackers to manipulate queries.

```php
<?php
declare(strict_types=1);

// UNSAFE: Direct string concatenation
function findUserUnsafe(PDO $pdo, string $email): ?array {
    // NEVER DO THIS - vulnerable to SQL injection
    $sql = "SELECT * FROM users WHERE email = '$email'";
    $result = $pdo->query($sql);
    return $result ? $result->fetch(PDO::FETCH_ASSOC) : null;
}

// SAFE: Prepared statements with PDO
function findUserSafe(PDO $pdo, string $email): ?array {
    $stmt = $pdo->prepare('SELECT * FROM users WHERE email = :email');
    $stmt->execute(['email' => $email]);
    $result = $stmt->fetch(PDO::FETCH_ASSOC);
    return $result !== false ? $result : null;
}

// Safe: Positional parameters
function findUserById(PDO $pdo, int $id): ?array {
    $stmt = $pdo->prepare('SELECT * FROM users WHERE id = ?');
    $stmt->execute([$id]);
    $result = $stmt->fetch(PDO::FETCH_ASSOC);
    return $result !== false ? $result : null;
}

// Safe: Multiple parameters
function findUsersByStatus(PDO $pdo, string $status, int $limit): array {
    $stmt = $pdo->prepare(
        'SELECT * FROM users WHERE status = :status LIMIT :limit'
    );
    $stmt->bindValue(':status', $status, PDO::PARAM_STR);
    $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
    $stmt->execute();
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// Safe: IN clause with placeholders
function findUsersByIds(PDO $pdo, array $ids): array {
    // Validate all IDs are integers
    $ids = array_filter($ids, 'is_int');
    if (empty($ids)) {
        return [];
    }

    // Create placeholders: ?,?,?
    $placeholders = implode(',', array_fill(0, count($ids), '?'));
    $sql = "SELECT * FROM users WHERE id IN ($placeholders)";

    $stmt = $pdo->prepare($sql);
    $stmt->execute($ids);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// Repository pattern with prepared statements
class UserRepository {
    public function __construct(
        private PDO $pdo
    ) {}

    public function find(int $id): ?array {
        $stmt = $this->pdo->prepare('SELECT * FROM users WHERE id = ?');
        $stmt->execute([$id]);
        $result = $stmt->fetch(PDO::FETCH_ASSOC);
        return $result !== false ? $result : null;
    }

    public function create(array $data): int {
        $stmt = $this->pdo->prepare(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)'
        );
        $stmt->execute([
            $data['name'],
            $data['email'],
            $data['password_hash'],
        ]);
        return (int) $this->pdo->lastInsertId();
    }

    public function update(int $id, array $data): bool {
        $stmt = $this->pdo->prepare(
            'UPDATE users SET name = ?, email = ? WHERE id = ?'
        );
        return $stmt->execute([
            $data['name'],
            $data['email'],
            $id,
        ]);
    }

    public function delete(int $id): bool {
        $stmt = $this->pdo->prepare('DELETE FROM users WHERE id = ?');
        return $stmt->execute([$id]);
    }

    public function search(string $query, int $limit = 10): array {
        $stmt = $this->pdo->prepare(
            'SELECT * FROM users WHERE name LIKE ? OR email LIKE ? LIMIT ?'
        );
        $pattern = "%$query%";
        $stmt->bindValue(1, $pattern, PDO::PARAM_STR);
        $stmt->bindValue(2, $pattern, PDO::PARAM_STR);
        $stmt->bindValue(3, $limit, PDO::PARAM_INT);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}

// Query builder with parameterization
class QueryBuilder {
    private array $where = [];
    private array $params = [];

    public function where(string $column, mixed $value): self {
        $placeholder = ':param' . count($this->params);
        $this->where[] = "$column = $placeholder";
        $this->params[$placeholder] = $value;
        return $this;
    }

    public function execute(PDO $pdo): array {
        $sql = 'SELECT * FROM users';
        if (!empty($this->where)) {
            $sql .= ' WHERE ' . implode(' AND ', $this->where);
        }

        $stmt = $pdo->prepare($sql);
        $stmt->execute($this->params);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}
```

Always use prepared statements with parameter binding - never concatenate user
input into SQL queries.

## Cross-Site Scripting (XSS) Prevention

XSS attacks inject malicious scripts into web pages viewed by other users. Proper
output encoding prevents script execution.

```php
<?php
declare(strict_types=1);

// HTML context escaping
function escapeHtml(string $text): string {
    return htmlspecialchars($text, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}

// JavaScript context escaping
function escapeJs(string $text): string {
    return json_encode($text, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT);
}

// URL parameter escaping
function escapeUrl(string $url): string {
    return urlencode($url);
}

// Attribute escaping
function escapeAttr(string $text): string {
    return htmlspecialchars($text, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}

// Safe template rendering
class SafeTemplate {
    private array $data = [];

    public function set(string $key, mixed $value): void {
        $this->data[$key] = $value;
    }

    public function render(string $template): string {
        // Extract and escape all variables
        extract(array_map(function($value) {
            if (is_string($value)) {
                return escapeHtml($value);
            }
            return $value;
        }, $this->data));

        ob_start();
        include $template;
        return ob_get_clean();
    }

    public function raw(string $key): string {
        // For trusted HTML - use sparingly
        return $this->data[$key] ?? '';
    }
}

// Example template usage
class CommentDisplay {
    public function renderComment(array $comment): string {
        $author = escapeHtml($comment['author']);
        $text = escapeHtml($comment['text']);
        $timestamp = escapeHtml($comment['timestamp']);

        return <<<HTML
        <div class="comment">
            <div class="author">{$author}</div>
            <div class="text">{$text}</div>
            <div class="timestamp">{$timestamp}</div>
        </div>
        HTML;
    }

    public function renderCommentWithLink(array $comment): string {
        $author = escapeHtml($comment['author']);
        $text = escapeHtml($comment['text']);
        $url = escapeAttr($comment['url'] ?? '#');

        return <<<HTML
        <div class="comment">
            <a href="{$url}">{$author}</a>
            <p>{$text}</p>
        </div>
        HTML;
    }
}

// Content Security Policy helper
class CspBuilder {
    private array $directives = [];

    public function defaultSrc(string ...$sources): self {
        $this->directives['default-src'] = $sources;
        return $this;
    }

    public function scriptSrc(string ...$sources): self {
        $this->directives['script-src'] = $sources;
        return $this;
    }

    public function styleSrc(string ...$sources): self {
        $this->directives['style-src'] = $sources;
        return $this;
    }

    public function imgSrc(string ...$sources): self {
        $this->directives['img-src'] = $sources;
        return $this;
    }

    public function build(): string {
        $parts = [];
        foreach ($this->directives as $directive => $sources) {
            $parts[] = $directive . ' ' . implode(' ', $sources);
        }
        return implode('; ', $parts);
    }

    public function sendHeader(): void {
        header('Content-Security-Policy: ' . $this->build());
    }
}

// Usage
$csp = new CspBuilder();
$csp->defaultSrc("'self'")
    ->scriptSrc("'self'", "'unsafe-inline'")
    ->styleSrc("'self'", 'https://fonts.googleapis.com')
    ->imgSrc("'self'", 'data:', 'https:')
    ->sendHeader();

// Rich text sanitization with HTML Purifier pattern
class HtmlSanitizer {
    private array $allowedTags = ['p', 'br', 'strong', 'em', 'a', 'ul', 'ol', 'li'];
    private array $allowedAttributes = ['a' => ['href', 'title']];

    public function sanitize(string $html): string {
        // Strip all tags except allowed
        $html = strip_tags($html, $this->allowedTags);

        // Parse and clean attributes
        $dom = new DOMDocument();
        @$dom->loadHTML('<?xml encoding="utf-8" ?>' . $html,
            LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD);

        $xpath = new DOMXPath($dom);

        // Remove dangerous attributes
        foreach ($xpath->query('//@*') as $attr) {
            $tagName = $attr->ownerElement->tagName;
            $attrName = $attr->name;

            if (!isset($this->allowedAttributes[$tagName])
                || !in_array($attrName, $this->allowedAttributes[$tagName])) {
                $attr->ownerElement->removeAttribute($attrName);
            }

            // Validate href attributes
            if ($attrName === 'href') {
                $href = $attr->value;
                if (!preg_match('/^https?:\/\//', $href)) {
                    $attr->ownerElement->removeAttribute($attrName);
                }
            }
        }

        return $dom->saveHTML();
    }
}
```

Always escape output based on context (HTML, JavaScript, URL, attribute) and
implement Content Security Policy headers.

## Cross-Site Request Forgery (CSRF) Prevention

CSRF attacks trick authenticated users into executing unwanted actions. Token
validation prevents unauthorized state-changing requests.

```php
<?php
declare(strict_types=1);

// CSRF token management
class CsrfProtection {
    private const TOKEN_NAME = 'csrf_token';
    private const TOKEN_LENGTH = 32;

    public function __construct(
        private string $sessionKey = '_csrf_tokens'
    ) {
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }
    }

    public function generateToken(string $action = 'default'): string {
        $token = bin2hex(random_bytes(self::TOKEN_LENGTH));

        if (!isset($_SESSION[$this->sessionKey])) {
            $_SESSION[$this->sessionKey] = [];
        }

        $_SESSION[$this->sessionKey][$action] = [
            'token' => $token,
            'expires' => time() + 3600, // 1 hour
        ];

        return $token;
    }

    public function validateToken(string $token,
                                  string $action = 'default'): bool {
        if (!isset($_SESSION[$this->sessionKey][$action])) {
            return false;
        }

        $stored = $_SESSION[$this->sessionKey][$action];

        // Check expiration
        if ($stored['expires'] < time()) {
            unset($_SESSION[$this->sessionKey][$action]);
            return false;
        }

        // Constant-time comparison
        $valid = hash_equals($stored['token'], $token);

        // One-time token - remove after use
        if ($valid) {
            unset($_SESSION[$this->sessionKey][$action]);
        }

        return $valid;
    }

    public function getTokenInput(string $action = 'default'): string {
        $token = $this->generateToken($action);
        $name = escapeAttr(self::TOKEN_NAME);
        $value = escapeAttr($token);
        return "<input type=\"hidden\" name=\"{$name}\" value=\"{$value}\">";
    }

    public function validateRequest(array $data,
                                    string $action = 'default'): bool {
        $token = $data[self::TOKEN_NAME] ?? '';
        return $this->validateToken($token, $action);
    }
}

// Middleware pattern
class CsrfMiddleware {
    public function __construct(
        private CsrfProtection $csrf
    ) {}

    public function handle(callable $next): mixed {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            if (!$this->csrf->validateRequest($_POST)) {
                http_response_code(403);
                throw new Exception('CSRF token validation failed');
            }
        }

        return $next();
    }
}

// Usage in forms
class FormRenderer {
    public function __construct(
        private CsrfProtection $csrf
    ) {}

    public function renderLoginForm(): string {
        $csrfField = $this->csrf->getTokenInput('login');

        return <<<HTML
        <form method="POST" action="/login">
            {$csrfField}
            <input type="email" name="email" required>
            <input type="password" name="password" required>
            <button type="submit">Login</button>
        </form>
        HTML;
    }

    public function renderDeleteForm(int $id): string {
        $csrfField = $this->csrf->getTokenInput('delete');

        return <<<HTML
        <form method="POST" action="/delete/{$id}">
            {$csrfField}
            <button type="submit" onclick="return confirm('Are you sure?')">
                Delete
            </button>
        </form>
        HTML;
    }
}

// Controller with CSRF validation
class UserController {
    public function __construct(
        private CsrfProtection $csrf,
        private UserRepository $users
    ) {}

    public function showForm(): void {
        $token = $this->csrf->generateToken('user_create');
        include 'user_form.php';
    }

    public function create(): void {
        if (!$this->csrf->validateRequest($_POST, 'user_create')) {
            http_response_code(403);
            die('CSRF validation failed');
        }

        // Process form...
        $this->users->create($_POST);
    }
}

// Double-submit cookie pattern (alternative)
class DoubleSubmitCsrf {
    private const COOKIE_NAME = 'csrf_token';

    public function generateToken(): string {
        $token = bin2hex(random_bytes(32));

        setcookie(
            self::COOKIE_NAME,
            $token,
            [
                'expires' => time() + 3600,
                'path' => '/',
                'domain' => '',
                'secure' => true,
                'httponly' => true,
                'samesite' => 'Strict',
            ]
        );

        return $token;
    }

    public function validateToken(string $token): bool {
        $cookieToken = $_COOKIE[self::COOKIE_NAME] ?? '';
        return hash_equals($cookieToken, $token);
    }
}
```

Implement CSRF protection for all state-changing operations (POST, PUT, DELETE)
using synchronized tokens or double-submit cookies.

## Secure Password Handling

Passwords must be hashed with strong algorithms and never stored in plain text.

```php
<?php
declare(strict_types=1);

// Password hashing with modern algorithms
class PasswordManager {
    private const MIN_LENGTH = 8;
    private const MAX_LENGTH = 128;

    public function hash(string $password): string {
        // Validate length
        if (strlen($password) < self::MIN_LENGTH ||
            strlen($password) > self::MAX_LENGTH) {
            throw new InvalidArgumentException('Invalid password length');
        }

        // Use bcrypt (PASSWORD_DEFAULT)
        return password_hash($password, PASSWORD_DEFAULT);
    }

    public function verify(string $password, string $hash): bool {
        return password_verify($password, $hash);
    }

    public function needsRehash(string $hash): bool {
        return password_needs_rehash($hash, PASSWORD_DEFAULT);
    }

    public function rehashIfNeeded(string $password, string $oldHash): ?string {
        if ($this->needsRehash($oldHash)) {
            return $this->hash($password);
        }
        return null;
    }
}

// Password strength validation
class PasswordValidator {
    public function validate(string $password): array {
        $errors = [];

        if (strlen($password) < 8) {
            $errors[] = 'Password must be at least 8 characters';
        }

        if (strlen($password) > 128) {
            $errors[] = 'Password must not exceed 128 characters';
        }

        if (!preg_match('/[A-Z]/', $password)) {
            $errors[] = 'Password must contain at least one uppercase letter';
        }

        if (!preg_match('/[a-z]/', $password)) {
            $errors[] = 'Password must contain at least one lowercase letter';
        }

        if (!preg_match('/[0-9]/', $password)) {
            $errors[] = 'Password must contain at least one number';
        }

        if (!preg_match('/[^A-Za-z0-9]/', $password)) {
            $errors[] = 'Password must contain at least one special character';
        }

        // Check against common passwords
        if ($this->isCommonPassword($password)) {
            $errors[] = 'Password is too common';
        }

        return $errors;
    }

    private function isCommonPassword(string $password): bool {
        $common = ['password', '123456', 'qwerty', 'admin', 'letmein'];
        return in_array(strtolower($password), $common, true);
    }

    public function calculateStrength(string $password): int {
        $strength = 0;

        if (strlen($password) >= 8) $strength += 1;
        if (strlen($password) >= 12) $strength += 1;
        if (preg_match('/[A-Z]/', $password)) $strength += 1;
        if (preg_match('/[a-z]/', $password)) $strength += 1;
        if (preg_match('/[0-9]/', $password)) $strength += 1;
        if (preg_match('/[^A-Za-z0-9]/', $password)) $strength += 1;

        return min($strength, 5); // 0-5 scale
    }
}

// Authentication service
class AuthService {
    public function __construct(
        private UserRepository $users,
        private PasswordManager $passwordManager
    ) {}

    public function register(string $email, string $password): int {
        $hash = $this->passwordManager->hash($password);
        return $this->users->create([
            'email' => $email,
            'password_hash' => $hash,
        ]);
    }

    public function authenticate(string $email, string $password): ?array {
        $user = $this->users->findByEmail($email);

        if (!$user) {
            // Prevent timing attacks - hash anyway
            $this->passwordManager->hash($password);
            return null;
        }

        if (!$this->passwordManager->verify($password, $user['password_hash'])) {
            return null;
        }

        // Check if password needs rehashing
        $newHash = $this->passwordManager->rehashIfNeeded(
            $password,
            $user['password_hash']
        );

        if ($newHash) {
            $this->users->updatePasswordHash($user['id'], $newHash);
        }

        return $user;
    }
}

// Password reset with secure tokens
class PasswordReset {
    private const TOKEN_EXPIRY = 3600; // 1 hour

    public function __construct(
        private UserRepository $users
    ) {}

    public function createResetToken(string $email): ?string {
        $user = $this->users->findByEmail($email);
        if (!$user) {
            return null;
        }

        $token = bin2hex(random_bytes(32));
        $hash = hash('sha256', $token);
        $expires = time() + self::TOKEN_EXPIRY;

        $this->users->storeResetToken($user['id'], $hash, $expires);

        return $token;
    }

    public function validateResetToken(string $token): ?int {
        $hash = hash('sha256', $token);
        $userId = $this->users->findUserByResetToken($hash);

        if (!$userId) {
            return null;
        }

        return $userId;
    }

    public function resetPassword(string $token, string $newPassword): bool {
        $userId = $this->validateResetToken($token);

        if (!$userId) {
            return false;
        }

        $passwordManager = new PasswordManager();
        $hash = $passwordManager->hash($newPassword);

        $this->users->updatePasswordHash($userId, $hash);
        $this->users->clearResetToken($userId);

        return true;
    }
}
```

Always use password_hash() with PASSWORD_DEFAULT, validate password strength,
and implement secure password reset flows.

## Session Security

Session hijacking and fixation attacks compromise user sessions. Proper session
management prevents unauthorized access.

```php
<?php
declare(strict_types=1);

// Secure session configuration
class SessionManager {
    public function start(): void {
        if (session_status() === PHP_SESSION_ACTIVE) {
            return;
        }

        // Configure session settings
        ini_set('session.cookie_httponly', '1');
        ini_set('session.cookie_secure', '1'); // HTTPS only
        ini_set('session.cookie_samesite', 'Strict');
        ini_set('session.use_strict_mode', '1');
        ini_set('session.use_only_cookies', '1');
        ini_set('session.cookie_lifetime', '0'); // Browser close

        session_start();

        // Regenerate session ID on login
        if (!isset($_SESSION['initiated'])) {
            session_regenerate_id(true);
            $_SESSION['initiated'] = true;
            $_SESSION['created_at'] = time();
            $_SESSION['user_agent'] = $_SERVER['HTTP_USER_AGENT'] ?? '';
            $_SESSION['ip_address'] = $_SERVER['REMOTE_ADDR'] ?? '';
        }

        // Validate session
        $this->validate();
    }

    private function validate(): void {
        // Check session age
        if (isset($_SESSION['created_at'])) {
            $age = time() - $_SESSION['created_at'];
            if ($age > 3600) { // 1 hour max session age
                $this->destroy();
                throw new Exception('Session expired');
            }
        }

        // Validate user agent (basic fingerprinting)
        if (isset($_SESSION['user_agent'])) {
            $currentAgent = $_SERVER['HTTP_USER_AGENT'] ?? '';
            if ($_SESSION['user_agent'] !== $currentAgent) {
                $this->destroy();
                throw new Exception('Session validation failed');
            }
        }

        // Regenerate ID periodically
        if (isset($_SESSION['last_regeneration'])) {
            $timeSinceRegen = time() - $_SESSION['last_regeneration'];
            if ($timeSinceRegen > 300) { // 5 minutes
                $this->regenerate();
            }
        }
    }

    public function regenerate(): void {
        session_regenerate_id(true);
        $_SESSION['last_regeneration'] = time();
    }

    public function destroy(): void {
        $_SESSION = [];

        if (isset($_COOKIE[session_name()])) {
            setcookie(
                session_name(),
                '',
                [
                    'expires' => time() - 3600,
                    'path' => '/',
                    'domain' => '',
                    'secure' => true,
                    'httponly' => true,
                    'samesite' => 'Strict',
                ]
            );
        }

        session_destroy();
    }

    public function set(string $key, mixed $value): void {
        $_SESSION[$key] = $value;
    }

    public function get(string $key, mixed $default = null): mixed {
        return $_SESSION[$key] ?? $default;
    }

    public function has(string $key): bool {
        return isset($_SESSION[$key]);
    }

    public function remove(string $key): void {
        unset($_SESSION[$key]);
    }
}

// Authentication with session management
class SecureAuth {
    public function __construct(
        private SessionManager $session,
        private UserRepository $users,
        private PasswordManager $password
    ) {}

    public function login(string $email, string $password): bool {
        $user = $this->users->findByEmail($email);

        if (!$user ||
            !$this->password->verify($password, $user['password_hash'])) {
            // Add delay to prevent timing attacks
            usleep(random_int(100000, 300000));
            return false;
        }

        // Regenerate session on login
        $this->session->regenerate();

        // Store minimal data
        $this->session->set('user_id', $user['id']);
        $this->session->set('logged_in_at', time());

        // Update last login
        $this->users->updateLastLogin($user['id']);

        return true;
    }

    public function logout(): void {
        $this->session->destroy();
    }

    public function isAuthenticated(): bool {
        return $this->session->has('user_id');
    }

    public function getCurrentUserId(): ?int {
        return $this->session->get('user_id');
    }

    public function requireAuth(): void {
        if (!$this->isAuthenticated()) {
            http_response_code(401);
            header('Location: /login');
            exit;
        }
    }
}

// Rate limiting for login attempts
class LoginRateLimiter {
    private const MAX_ATTEMPTS = 5;
    private const LOCKOUT_TIME = 900; // 15 minutes

    public function __construct(
        private string $storePath = '/tmp/login_attempts'
    ) {}

    public function recordAttempt(string $identifier): void {
        $file = $this->getAttemptFile($identifier);
        $attempts = $this->getAttempts($identifier);
        $attempts[] = time();
        file_put_contents($file, json_encode($attempts));
    }

    public function isLocked(string $identifier): bool {
        $attempts = $this->getAttempts($identifier);
        $recentAttempts = array_filter($attempts, fn($time) =>
            time() - $time < self::LOCKOUT_TIME
        );

        return count($recentAttempts) >= self::MAX_ATTEMPTS;
    }

    public function getRemainingTime(string $identifier): int {
        if (!$this->isLocked($identifier)) {
            return 0;
        }

        $attempts = $this->getAttempts($identifier);
        $oldestRecent = min(array_filter($attempts, fn($time) =>
            time() - $time < self::LOCKOUT_TIME
        ));

        return self::LOCKOUT_TIME - (time() - $oldestRecent);
    }

    public function reset(string $identifier): void {
        $file = $this->getAttemptFile($identifier);
        if (file_exists($file)) {
            unlink($file);
        }
    }

    private function getAttempts(string $identifier): array {
        $file = $this->getAttemptFile($identifier);
        if (!file_exists($file)) {
            return [];
        }

        $data = file_get_contents($file);
        return json_decode($data, true) ?: [];
    }

    private function getAttemptFile(string $identifier): string {
        $hash = hash('sha256', $identifier);
        return $this->storePath . '/' . $hash . '.json';
    }
}
```

Configure sessions with secure flags, regenerate session IDs on privilege changes,
and implement session validation and timeout.

## Best Practices

1. **Validate all inputs** at application boundaries before processing or storage
   to prevent injection attacks

2. **Use prepared statements exclusively** for database queries to eliminate SQL
   injection vulnerabilities

3. **Escape all outputs** based on context (HTML, JavaScript, URL, attribute)
   before rendering

4. **Implement CSRF protection** for all state-changing operations with
   synchronized tokens

5. **Hash passwords with modern algorithms** using password_hash() with
   PASSWORD_DEFAULT setting

6. **Configure secure session management** with httponly, secure, and samesite
   cookie flags

7. **Apply defense in depth** with multiple security layers rather than relying
   on single mechanisms

8. **Use Content Security Policy headers** to restrict resource loading and
   prevent XSS attacks

9. **Implement rate limiting** for authentication endpoints to prevent brute
   force attacks

10. **Keep dependencies updated** and regularly audit for known security
    vulnerabilities

## Common Pitfalls

1. **Trusting user input** without validation allows attackers to inject
   malicious data

2. **Using string concatenation for SQL** instead of prepared statements enables
   SQL injection

3. **Forgetting output encoding** in templates allows XSS attacks through
   user-generated content

4. **Skipping CSRF protection** on state-changing operations enables unauthorized
   actions

5. **Storing passwords in plain text** or using weak hashing algorithms
   compromises credentials

6. **Not regenerating session IDs** after login allows session fixation attacks

7. **Using inadequate randomness** for tokens with rand() instead of
   random_bytes()

8. **Exposing detailed error messages** to users reveals system internals to
   attackers

9. **Not implementing rate limiting** allows brute force and denial of service
   attacks

10. **Allowing unrestricted file uploads** without validation enables remote
    code execution

## When to Use This Skill

Apply security patterns throughout all PHP application development, not as an
afterthought but as core architectural concerns.

Use input validation at every entry point where external data enters the
application, including forms, APIs, and file uploads.

Implement SQL injection prevention whenever constructing database queries,
preferring ORMs or query builders with parameterization.

Apply XSS protection in all templates and views where user-generated content is
displayed to other users.

Use CSRF protection for all authenticated endpoints that perform state-changing
operations like create, update, or delete.

Implement secure session management for any application requiring user
authentication and authorization.

## Resources

- [OWASP PHP Security Cheat Sheet](<https://cheatsheetseries.owasp.org/cheatsheets/PHP_Configuration_Cheat_Sheet.html>)
- [PHP Security Guide](<https://www.php.net/manual/en/security.php>)
- [OWASP Top 10](<https://owasp.org/www-project-top-ten/>)
- [Paragon Initiative PHP Security Book](<https://paragonie.com/blog/2017/12/2018-guide-building-secure-php-software>)
- [PHP The Right Way Security](<https://phptherightway.com/#security>)
