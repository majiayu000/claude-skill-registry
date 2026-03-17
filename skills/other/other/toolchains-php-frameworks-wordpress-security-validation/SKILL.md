---
name: wordpress-security-validation
description: Security-first WordPress development with nonces, sanitization, validation, and escaping to prevent XSS, CSRF, and SQL injection vulnerabilities.
progressive_disclosure:
  entry_point:
    summary: "Security-first WordPress development with nonces, sanitization, validation, and escaping for robust plugin/theme security"
    when_to_use:
      - "Processing user input in forms or AJAX"
      - "Displaying untrusted content safely"
      - "Implementing capability checks and permissions"
    quick_start:
      - "Sanitize on input with sanitize_* functions"
      - "Validate for logic with validation rules"
      - "Escape on output with esc_* functions"
---

# WordPress Security & Data Validation

**Version:** 1.0.0
**Target:** WordPress 6.7+ | PHP 8.3+
**Skill Level:** Intermediate to Advanced

## Overview

Security is not optional in WordPress development—it's fundamental. This skill teaches the **three-layer security model** that prevents XSS, CSRF, SQL injection, and other common web vulnerabilities through proper input sanitization, business logic validation, and output escaping.

**The Golden Rule:** "Sanitize on input, validate for logic, escape on output."

### Why This Matters

Every year, thousands of WordPress sites are compromised due to security vulnerabilities in plugins and themes. Most of these attacks exploit one of three weaknesses:

1. **XSS (Cross-Site Scripting):** Malicious JavaScript injected through unsanitized output
2. **CSRF (Cross-Site Request Forgery):** Unauthorized actions performed on behalf of authenticated users
3. **SQL Injection:** Database manipulation through unsanitized database queries

This skill provides **complete, production-ready patterns** for preventing all three attack vectors.

---

## The Three-Layer Security Model

WordPress security follows a defense-in-depth strategy with three distinct layers:

```
User Input → [1. SANITIZE] → [2. VALIDATE] → Process → [3. ESCAPE] → Output
```

### Layer 1: Sanitization (Input Cleaning)
**Purpose:** Remove dangerous characters and normalize data format
**When:** Immediately upon receiving user input
**Example:** `sanitize_text_field($_POST['username'])`

### Layer 2: Validation (Logic Checks)
**Purpose:** Ensure data meets business requirements
**When:** After sanitization, before processing
**Example:** `if (!is_email($email)) { /* error */ }`

### Layer 3: Escaping (Output Protection)
**Purpose:** Prevent XSS by encoding special characters
**When:** Every time you output data to browser
**Example:** `echo esc_html($user_input);`

**Critical Distinction:**
- **Sanitization** removes/transforms invalid data (changes the value)
- **Validation** checks if data is acceptable (returns true/false)
- **Escaping** makes data safe for display (context-specific encoding)

---

## 1. Nonces: CSRF Protection

### What Are Nonces?

Nonces (Numbers Used Once) are cryptographic tokens that verify a request originated from your site, not a malicious external source. They prevent **Cross-Site Request Forgery (CSRF)** attacks.

**How CSRF Attacks Work:**
```html
<!-- Attacker's malicious site: evil.com -->
<img src="https://yoursite.com/wp-admin/admin.php?action=delete_user&id=1">
<!-- If user is logged into yoursite.com, this executes! -->
```

**How Nonces Prevent CSRF:**
```html
<!-- Legitimate request with nonce -->
<form action="admin.php?action=delete_user&id=1" method="POST">
    <?php wp_nonce_field('delete_user_1', 'delete_nonce'); ?>
    <button>Delete User</button>
</form>

<!-- Attacker cannot generate valid nonce (tied to user session) -->
```

### Nonce Implementation Patterns

#### Pattern 1: Form Nonces (Most Common)

**BEFORE (Vulnerable):**
```php
// Vulnerable form processing
if (isset($_POST['submit'])) {
    $user_id = absint($_POST['user_id']);
    delete_user($user_id); // ⚠️ CSRF vulnerable!
}
```

**AFTER (Secure):**
```php
// Generate nonce in form
<form method="post" action="">
    <?php wp_nonce_field('delete_user_action', 'delete_user_nonce'); ?>
    <input type="hidden" name="user_id" value="42">
    <button type="submit" name="submit">Delete User</button>
</form>

// Verify nonce on submission
if (isset($_POST['submit'])) {
    // Security check #1: Verify nonce
    if (!isset($_POST['delete_user_nonce']) ||
        !wp_verify_nonce($_POST['delete_user_nonce'], 'delete_user_action')) {
        wp_die('Security check failed: Invalid nonce');
    }

    // Security check #2: Capability check
    if (!current_user_can('delete_users')) {
        wp_die('You do not have permission to delete users');
    }

    // Now safe to process
    $user_id = absint($_POST['user_id']);
    wp_delete_user($user_id);
}
```

**Key Functions:**
- `wp_nonce_field($action, $name)` - Generates hidden nonce field
- `wp_verify_nonce($nonce, $action)` - Verifies nonce validity

#### Pattern 2: URL Nonces

**Use Case:** Delete/trash links, admin actions

```php
// Generate nonce URL
$delete_url = wp_nonce_url(
    admin_url('admin.php?action=delete_post&post_id=123'),
    'delete_post_123',  // Action (must be unique)
    'delete_nonce'      // Query parameter name
);

echo '<a href="' . esc_url($delete_url) . '">Delete Post</a>';

// Verify nonce in handler
add_action('admin_action_delete_post', 'handle_delete_post');
function handle_delete_post() {
    // Verify nonce from URL
    if (!isset($_GET['delete_nonce']) ||
        !wp_verify_nonce($_GET['delete_nonce'], 'delete_post_123')) {
        wp_die('Invalid security token');
    }

    // Verify capability
    $post_id = absint($_GET['post_id']);
    if (!current_user_can('delete_post', $post_id)) {
        wp_die('You cannot delete this post');
    }

    // Delete post
    wp_delete_post($post_id, true); // true = force delete

    // Redirect with success message
    wp_redirect(add_query_arg('message', 'deleted', wp_get_referer()));
    exit;
}
```

#### Pattern 3: AJAX Nonces

**Use Case:** Frontend AJAX requests

**BEFORE (Vulnerable):**
```javascript
// ⚠️ Vulnerable AJAX request
jQuery.post(ajaxurl, {
    action: 'update_user_meta',
    user_id: 42,
    meta_key: 'favorite_color',
    meta_value: 'blue'
}, function(response) {
    console.log(response);
});
```

**AFTER (Secure):**

**PHP (Enqueue script with nonce):**
```php
add_action('wp_enqueue_scripts', 'enqueue_ajax_script');
function enqueue_ajax_script() {
    wp_enqueue_script('my-ajax-script',
        plugin_dir_url(__FILE__) . 'js/ajax.js',
        ['jquery'],
        '1.0.0',
        true
    );

    // Pass nonce and AJAX URL to JavaScript
    wp_localize_script('my-ajax-script', 'myAjax', [
        'ajaxurl' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('my_ajax_nonce'), // Generate nonce
    ]);
}

// AJAX handler with nonce verification
add_action('wp_ajax_update_user_meta', 'handle_ajax_update');
function handle_ajax_update() {
    // Verify nonce
    check_ajax_referer('my_ajax_nonce', 'nonce');

    // Verify capability
    if (!current_user_can('edit_users')) {
        wp_send_json_error(['message' => 'Permission denied']);
    }

    // Sanitize input
    $user_id = absint($_POST['user_id']);
    $meta_key = sanitize_key($_POST['meta_key']);
    $meta_value = sanitize_text_field($_POST['meta_value']);

    // Update meta
    update_user_meta($user_id, $meta_key, $meta_value);

    wp_send_json_success(['message' => 'Updated successfully']);
}
```

**JavaScript (Use nonce in AJAX):**
```javascript
jQuery(document).ready(function($) {
    $('#update-button').on('click', function() {
        $.post(myAjax.ajaxurl, {
            action: 'update_user_meta',
            nonce: myAjax.nonce,  // Include nonce
            user_id: 42,
            meta_key: 'favorite_color',
            meta_value: 'blue'
        }, function(response) {
            if (response.success) {
                console.log(response.data.message);
            } else {
                console.error(response.data.message);
            }
        });
    });
});
```

**Key Functions:**
- `wp_create_nonce($action)` - Generate nonce token
- `check_ajax_referer($action, $query_arg)` - Verify AJAX nonce (dies on failure)
- `wp_send_json_success($data)` - Send JSON success response
- `wp_send_json_error($data)` - Send JSON error response

### Nonce Best Practices

✅ **DO:**
- Use unique action names (e.g., `delete_post_$post_id`, not just `delete`)
- Always verify nonces BEFORE processing any data
- Combine nonce checks with capability checks
- Use specific nonce functions (`check_ajax_referer` for AJAX)

❌ **DON'T:**
- Reuse the same nonce action for multiple operations
- Skip nonce verification for "read-only" operations
- Trust nonce verification alone (always check capabilities too)
- Store nonces in cookies or URLs for long-term use (they expire)

**Nonce Lifespan:** WordPress nonces expire after 24 hours by default (12 hours in each direction due to time window).

---

## 2. Sanitization Functions Reference

Sanitization **transforms** user input into a safe format by removing or encoding dangerous characters. It's the **first line of defense** against malicious data.

### Core Sanitization Functions

| Function | Use Case | Example Input | Output |
|----------|----------|---------------|--------|
| `sanitize_text_field()` | Single-line text (usernames, titles) | `"Hello <script>alert('xss')</script>"` | `"Hello alert('xss')"` |
| `sanitize_email()` | Email addresses | `"user@example.com<script>"` | `"user@example.com"` |
| `sanitize_url()` / `esc_url_raw()` | URLs (for storage) | `"javascript:alert('xss')"` | `""` (blocked) |
| `sanitize_key()` | Array keys, meta keys | `"my key!"` | `"my_key"` |
| `sanitize_file_name()` | File uploads | `"../../etc/passwd"` | `"..etcpasswd"` |
| `absint()` | Positive integers | `"-5"`, `"42abc"` | `5`, `42` |
| `intval()` | Any integer | `"-5"`, `"42.7"` | `-5`, `42` |
| `floatval()` | Floating-point numbers | `"3.14abc"` | `3.14` |
| `wp_kses_post()` | HTML content (allows safe tags) | `"<p>Safe</p><script>Bad</script>"` | `"<p>Safe</p>"` |
| `wp_kses()` | HTML with custom allowed tags | See below | Custom filtering |
| `sanitize_textarea_field()` | Multi-line text | `"Line 1\nLine 2<script>"` | `"Line 1\nLine 2"` |
| `sanitize_title()` | Post slugs | `"Hello World!"` | `"hello-world"` |

### Detailed Examples

#### Text Sanitization

```php
// Single-line text (removes HTML, line breaks, extra whitespace)
$username = sanitize_text_field($_POST['username']);
// Input: "  John <b>Doe</b>\n"
// Output: "John Doe"

// Multi-line text (preserves line breaks, removes HTML)
$bio = sanitize_textarea_field($_POST['bio']);
// Input: "Line 1\nLine 2<script>alert('xss')</script>"
// Output: "Line 1\nLine 2alert('xss')"

// Email (validates format and removes invalid characters)
$email = sanitize_email($_POST['email']);
// Input: "user@EXAMPLE.com <script>"
// Output: "user@example.com"

// URL (removes dangerous protocols)
$website = esc_url_raw($_POST['website']);
// Input: "javascript:alert('xss')"
// Output: "" (blocked protocol)
// Input: "http://example.com"
// Output: "http://example.com"
```

#### Numeric Sanitization

```php
// Positive integers only (absolute value)
$post_id = absint($_POST['post_id']);
// Input: "-5", "42", "123abc"
// Output: 5, 42, 123

// Any integer (preserves negative)
$temperature = intval($_POST['temperature']);
// Input: "-5", "42.7", "99abc"
// Output: -5, 42, 99

// Floating-point numbers
$price = floatval($_POST['price']);
// Input: "19.99", "20.5abc"
// Output: 19.99, 20.5
```

#### HTML Sanitization

**wp_kses_post() - Allow WordPress Post Editor Tags:**
```php
$content = wp_kses_post($_POST['content']);
// Allows: <p>, <a>, <strong>, <em>, <ul>, <ol>, <li>, <blockquote>, <img>, etc.
// Blocks: <script>, <iframe>, <object>, <embed>, <form>

// Input: "<p>Safe content</p><script>alert('xss')</script>"
// Output: "<p>Safe content</p>alert('xss')"
```

**wp_kses() - Custom Allowed Tags:**
```php
// Define allowed tags and attributes
$allowed_html = [
    'a' => [
        'href' => true,
        'title' => true,
        'target' => true,
    ],
    'strong' => [],
    'em' => [],
    'br' => [],
];

$clean_html = wp_kses($_POST['content'], $allowed_html);

// Input: "<a href='#' onclick='alert(1)'>Link</a><script>Bad</script>"
// Output: "<a href='#'>Link</a>Bad" (onclick removed, script stripped)
```

**Strip All HTML:**
```php
$plain_text = wp_strip_all_tags($_POST['content']);
// Input: "<p>Hello <b>World</b></p>"
// Output: "Hello World"
```

#### File Upload Sanitization

```php
// Sanitize filename (removes path traversal, special characters)
$safe_filename = sanitize_file_name($_FILES['upload']['name']);
// Input: "../../etc/passwd", "my file!.php"
// Output: "..etcpasswd", "my-file.php"

// Complete file upload example
if (isset($_FILES['user_avatar'])) {
    // Verify nonce first!
    if (!wp_verify_nonce($_POST['upload_nonce'], 'upload_avatar')) {
        wp_die('Security check failed');
    }

    // Sanitize filename
    $filename = sanitize_file_name($_FILES['user_avatar']['name']);

    // Validate file type
    $allowed_types = ['image/jpeg', 'image/png', 'image/gif'];
    $file_type = $_FILES['user_avatar']['type'];

    if (!in_array($file_type, $allowed_types)) {
        wp_die('Invalid file type. Only JPG, PNG, GIF allowed.');
    }

    // Use WordPress upload handler (handles security)
    $upload = wp_handle_upload($_FILES['user_avatar'], [
        'test_form' => false,
        'mimes' => [
            'jpg|jpeg' => 'image/jpeg',
            'png' => 'image/png',
            'gif' => 'image/gif',
        ],
    ]);

    if (isset($upload['error'])) {
        wp_die('Upload failed: ' . $upload['error']);
    }

    // Store uploaded file URL
    $avatar_url = $upload['url'];
    update_user_meta(get_current_user_id(), 'avatar_url', $avatar_url);
}
```

#### Array Sanitization

```php
// Sanitize array of text fields
$tags = array_map('sanitize_text_field', $_POST['tags']);
// Input: ['tag1', '<script>tag2</script>', 'tag3']
// Output: ['tag1', 'tag2', 'tag3']

// Sanitize array of integers
$ids = array_map('absint', $_POST['post_ids']);
// Input: ['1', '2abc', '-5']
// Output: [1, 2, 5]

// Sanitize array of emails
$emails = array_map('sanitize_email', $_POST['email_list']);
```

### Custom Sanitization Callbacks

```php
// Register setting with sanitization callback
register_setting('my_plugin_options', 'my_plugin_settings', [
    'type' => 'array',
    'sanitize_callback' => 'my_plugin_sanitize_settings',
]);

function my_plugin_sanitize_settings($input) {
    $sanitized = [];

    // Sanitize API key (alphanumeric only)
    if (isset($input['api_key'])) {
        $sanitized['api_key'] = preg_replace('/[^a-zA-Z0-9]/', '', $input['api_key']);
    }

    // Sanitize boolean checkbox
    $sanitized['enable_feature'] = isset($input['enable_feature']) ? 1 : 0;

    // Sanitize color (hex format)
    if (isset($input['primary_color'])) {
        $color = sanitize_hex_color($input['primary_color']);
        $sanitized['primary_color'] = $color ? $color : '#000000';
    }

    // Sanitize select option (whitelist)
    $allowed_modes = ['mode1', 'mode2', 'mode3'];
    if (isset($input['mode']) && in_array($input['mode'], $allowed_modes)) {
        $sanitized['mode'] = $input['mode'];
    } else {
        $sanitized['mode'] = 'mode1'; // Default
    }

    return $sanitized;
}
```

---

## 3. Validation Patterns

Validation ensures data meets **business logic requirements** after sanitization. Unlike sanitization (which transforms data), validation **returns true/false**.

### Built-in Validation Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `is_email($email)` | Valid email format | `is_email('user@example.com')` → `true` |
| `is_numeric($value)` | Numeric string | `is_numeric('42')` → `true` |
| `is_int($value)` | Integer type | `is_int(42)` → `true` |
| `is_array($value)` | Array type | `is_array([1,2,3])` → `true` |
| `is_user_logged_in()` | User authentication | `is_user_logged_in()` → `true/false` |
| `username_exists($user)` | Username exists | `username_exists('admin')` → `user_id` or `null` |
| `email_exists($email)` | Email exists | `email_exists('user@example.com')` → `user_id` or `false` |

### Validation Examples

#### Email Validation

```php
$email = sanitize_email($_POST['email']);

// Validate format
if (!is_email($email)) {
    $errors[] = 'Invalid email address format';
}

// Validate uniqueness (for registration)
if (email_exists($email)) {
    $errors[] = 'Email address already registered';
}
```

#### Numeric Range Validation

```php
$age = absint($_POST['age']);

// Validate range
if ($age < 18 || $age > 100) {
    $errors[] = 'Age must be between 18 and 100';
}

// Validate positive number
if ($quantity <= 0) {
    $errors[] = 'Quantity must be greater than zero';
}
```

#### String Length Validation

```php
$username = sanitize_text_field($_POST['username']);

// Validate minimum length
if (strlen($username) < 3) {
    $errors[] = 'Username must be at least 3 characters';
}

// Validate maximum length
if (strlen($username) > 20) {
    $errors[] = 'Username cannot exceed 20 characters';
}
```

#### Required Field Validation

```php
// Check if field exists and is not empty
if (empty($_POST['title']) || trim($_POST['title']) === '') {
    $errors[] = 'Title is required';
}

// Alternative: isset() + non-empty check
if (!isset($_POST['terms']) || $_POST['terms'] !== 'accepted') {
    $errors[] = 'You must accept the terms and conditions';
}
```

#### Pattern Matching (Regex)

```php
$phone = sanitize_text_field($_POST['phone']);

// Validate phone format (US format: (555) 123-4567)
if (!preg_match('/^\(\d{3}\) \d{3}-\d{4}$/', $phone)) {
    $errors[] = 'Phone must be in format: (555) 123-4567';
}

// Validate alphanumeric only
$product_code = sanitize_text_field($_POST['product_code']);
if (!preg_match('/^[a-zA-Z0-9]+$/', $product_code)) {
    $errors[] = 'Product code must contain only letters and numbers';
}
```

#### Multi-Field Validation

```php
function validate_registration_form($data) {
    $errors = [];

    // Email validation
    $email = sanitize_email($data['email']);
    if (!is_email($email)) {
        $errors['email'] = 'Invalid email address';
    } elseif (email_exists($email)) {
        $errors['email'] = 'Email already registered';
    }

    // Username validation
    $username = sanitize_text_field($data['username']);
    if (strlen($username) < 3) {
        $errors['username'] = 'Username too short (minimum 3 characters)';
    } elseif (username_exists($username)) {
        $errors['username'] = 'Username already taken';
    }

    // Password validation
    if (strlen($data['password']) < 8) {
        $errors['password'] = 'Password must be at least 8 characters';
    }

    // Password confirmation
    if ($data['password'] !== $data['password_confirm']) {
        $errors['password_confirm'] = 'Passwords do not match';
    }

    // Age validation
    $age = absint($data['age']);
    if ($age < 18) {
        $errors['age'] = 'You must be 18 or older to register';
    }

    return empty($errors) ? true : $errors;
}

// Usage
$result = validate_registration_form($_POST);
if ($result === true) {
    // Process registration
} else {
    // Display errors
    foreach ($result as $field => $error) {
        echo "<p class='error'>$error</p>";
    }
}
```

### Custom Validation Rules

```php
// Validate URL is from allowed domain
function validate_allowed_domain($url) {
    $allowed_domains = ['example.com', 'wordpress.org'];
    $host = parse_url($url, PHP_URL_HOST);

    return in_array($host, $allowed_domains);
}

// Validate date format and range
function validate_date($date_string) {
    $date = DateTime::createFromFormat('Y-m-d', $date_string);

    if (!$date) {
        return false; // Invalid format
    }

    // Check date is not in the past
    $now = new DateTime();
    if ($date < $now) {
        return false;
    }

    return true;
}

// Validate credit card (Luhn algorithm)
function validate_credit_card($number) {
    $number = preg_replace('/\D/', '', $number); // Remove non-digits

    if (strlen($number) < 13 || strlen($number) > 19) {
        return false;
    }

    $sum = 0;
    $double = false;

    for ($i = strlen($number) - 1; $i >= 0; $i--) {
        $digit = (int) $number[$i];

        if ($double) {
            $digit *= 2;
            if ($digit > 9) {
                $digit -= 9;
            }
        }

        $sum += $digit;
        $double = !$double;
    }

    return ($sum % 10) === 0;
}
```

---

## 4. Output Escaping Reference

Escaping prevents **XSS (Cross-Site Scripting)** by encoding special characters before output. This is the **final security layer**.

### Core Escaping Functions

| Function | Context | Escapes | Example Use |
|----------|---------|---------|-------------|
| `esc_html()` | HTML content | `< > & " '` | `echo esc_html($user_input);` |
| `esc_attr()` | HTML attributes | `< > & " '` | `<input value="<?php echo esc_attr($value); ?>">` |
| `esc_url()` | HTML href/src | Dangerous protocols | `<a href="<?php echo esc_url($link); ?>">` |
| `esc_js()` | JavaScript strings | `' " \ /` | `<script>var msg = '<?php echo esc_js($message); ?>';</script>` |
| `esc_sql()` | **DEPRECATED** (use `$wpdb->prepare()`) | SQL special chars | ❌ Don't use |
| `esc_textarea()` | Textarea content | `< > &` | `<textarea><?php echo esc_textarea($content); ?></textarea>` |

### Detailed Escaping Examples

#### HTML Content Escaping

```php
// Escape HTML content (converts special characters to entities)
$user_comment = "<script>alert('XSS')</script>Hello";
echo esc_html($user_comment);
// Output: &lt;script&gt;alert('XSS')&lt;/script&gt;Hello
// Browser displays: <script>alert('XSS')</script>Hello (as text, not code)

// WRONG: No escaping
echo $user_comment; // ⚠️ Executes JavaScript!
```

#### HTML Attribute Escaping

```php
// Escape attribute values
$title = 'My "Awesome" Title';
?>
<input type="text"
       value="<?php echo esc_attr($title); ?>"
       placeholder="<?php echo esc_attr($placeholder); ?>">
<!-- Output: value="My &quot;Awesome&quot; Title" -->

<!-- WRONG: No escaping -->
<input value="<?php echo $title; ?>">
<!-- Output: <input value="My "Awesome" Title"> (breaks HTML!) -->
```

#### URL Escaping

```php
// Escape URLs (blocks dangerous protocols)
$user_url = "javascript:alert('XSS')";
echo '<a href="' . esc_url($user_url) . '">Link</a>';
// Output: <a href="">Link</a> (javascript: protocol blocked)

// Safe URL
$safe_url = "https://example.com";
echo '<a href="' . esc_url($safe_url) . '">Link</a>';
// Output: <a href="https://example.com">Link</a>

// WRONG: No escaping
echo '<a href="' . $user_url . '">Link</a>'; // ⚠️ XSS vulnerability!
```

#### JavaScript Escaping

```php
// Escape JavaScript strings
$user_message = "It's \"dangerous\" to trust user input";
?>
<script>
    var message = '<?php echo esc_js($user_message); ?>';
    alert(message);
</script>
<!-- Output: var message = 'It\'s \"dangerous\" to trust user input'; -->

<!-- WRONG: No escaping -->
<script>
    var message = '<?php echo $user_message; ?>'; // ⚠️ Breaks JavaScript!
</script>
```

#### Textarea Escaping

```php
// Escape textarea content
$bio = "Line 1\nLine 2 <script>alert('XSS')</script>";
?>
<textarea><?php echo esc_textarea($bio); ?></textarea>
<!-- Output preserves line breaks, escapes HTML -->

<!-- WRONG: Using esc_html() in textarea -->
<textarea><?php echo esc_html($bio); ?></textarea>
<!-- ⚠️ Line breaks converted to &lt;br&gt; (not displayed correctly) -->
```

### Context-Specific Escaping

#### HTML Context

```php
// Paragraph content
echo '<p>' . esc_html($user_content) . '</p>';

// Link text
echo '<a href="' . esc_url($url) . '">' . esc_html($link_text) . '</a>';

// Image alt text
echo '<img src="' . esc_url($image_url) . '" alt="' . esc_attr($alt_text) . '">';
```

#### Attribute Context

```php
// Data attributes
echo '<div data-user-id="' . esc_attr($user_id) . '"
           data-username="' . esc_attr($username) . '"></div>';

// Class names (use sanitize_html_class)
echo '<div class="' . esc_attr(sanitize_html_class($class)) . '"></div>';

// Style attribute (dangerous - avoid if possible)
$safe_color = sanitize_hex_color($user_color); // Validate first
echo '<div style="color: ' . esc_attr($safe_color) . ';"></div>';
```

#### JavaScript Context

```php
// Inline JavaScript (avoid if possible, use wp_localize_script instead)
<script>
    var config = {
        username: '<?php echo esc_js($username); ?>',
        apiUrl: '<?php echo esc_js(admin_url('admin-ajax.php')); ?>'
    };
</script>

// BETTER: Use wp_localize_script
wp_localize_script('my-script', 'myConfig', [
    'username' => $username, // Automatically JSON-encoded
    'apiUrl' => admin_url('admin-ajax.php'),
]);
```

### Internationalization + Escaping

```php
// Translate and escape
echo esc_html__('Welcome User', 'my-plugin');

// Translate with variable, then escape
$message = sprintf(
    __('Hello %s, you have %d new messages', 'my-plugin'),
    esc_html($username),
    absint($message_count)
);
echo $message;

// Escape translatable attributes
<input placeholder="<?php echo esc_attr__('Enter your name', 'my-plugin'); ?>">

// Allow HTML in translations (use wp_kses_post)
$welcome_html = __('Welcome to <strong>My Plugin</strong>!', 'my-plugin');
echo wp_kses_post($welcome_html);
```

### Common Escaping Mistakes

❌ **WRONG:**
```php
// Double-escaping (displays HTML entities to user)
echo esc_html(esc_html($content)); // ⚠️ Displays &amp;lt;script&amp;gt;

// Wrong function for context
echo '<a href="' . esc_html($url) . '">Link</a>'; // ⚠️ Use esc_url()

// No escaping in JavaScript
echo "<script>var x = '$user_input';</script>"; // ⚠️ Use esc_js()

// Escaping before storage (store raw, escape on output)
update_option('setting', esc_html($value)); // ⚠️ Escape on output, not input
```

✅ **CORRECT:**
```php
// Escape once, on output
echo esc_html($content);

// Use correct function for context
echo '<a href="' . esc_url($url) . '">' . esc_html($text) . '</a>';

// Escape JavaScript properly
wp_localize_script('script', 'data', ['value' => $user_input]);

// Store raw, escape on output
update_option('setting', $value); // Store raw
echo esc_html(get_option('setting')); // Escape on output
```

---

## 5. Capability Checks (Authorization)

Capability checks ensure users have **permission** to perform actions. Always combine with nonce verification.

### Built-in Capabilities

| Capability | Description | Default Roles |
|------------|-------------|---------------|
| `read` | View content | All logged-in users |
| `edit_posts` | Create/edit own posts | Author, Editor, Admin |
| `edit_published_posts` | Edit published posts | Editor, Admin |
| `delete_posts` | Delete own posts | Author, Editor, Admin |
| `manage_options` | Manage site settings | Admin only |
| `upload_files` | Upload media | Author, Editor, Admin |
| `edit_users` | Edit user accounts | Admin only |
| `delete_users` | Delete users | Admin only |
| `install_plugins` | Install/activate plugins | Admin only |
| `switch_themes` | Change themes | Admin only |

### Capability Check Patterns

#### Basic Capability Check

```php
// Check if user is logged in
if (!is_user_logged_in()) {
    wp_die('You must be logged in to access this page');
}

// Check if user has capability
if (!current_user_can('manage_options')) {
    wp_die('You do not have permission to manage settings');
}

// Check if user can edit specific post
$post_id = absint($_GET['post_id']);
if (!current_user_can('edit_post', $post_id)) {
    wp_die('You cannot edit this post');
}
```

#### Complete Security Example

```php
add_action('admin_post_update_settings', 'handle_settings_update');
function handle_settings_update() {
    // 1. Check if user is logged in
    if (!is_user_logged_in()) {
        wp_die('You must be logged in');
    }

    // 2. Verify nonce
    if (!isset($_POST['settings_nonce']) ||
        !wp_verify_nonce($_POST['settings_nonce'], 'update_settings')) {
        wp_die('Security check failed');
    }

    // 3. Check user capability
    if (!current_user_can('manage_options')) {
        wp_die('You do not have permission to update settings');
    }

    // 4. Sanitize input
    $api_key = sanitize_text_field($_POST['api_key']);
    $enable_feature = isset($_POST['enable_feature']) ? 1 : 0;

    // 5. Validate data
    if (strlen($api_key) < 10) {
        wp_die('API key must be at least 10 characters');
    }

    // 6. Update options
    update_option('my_plugin_api_key', $api_key);
    update_option('my_plugin_enable_feature', $enable_feature);

    // 7. Redirect with success message
    wp_redirect(add_query_arg('message', 'updated', wp_get_referer()));
    exit;
}
```

#### Post-Specific Capabilities

```php
// Check if user can edit specific post
$post_id = absint($_POST['post_id']);
if (!current_user_can('edit_post', $post_id)) {
    wp_send_json_error(['message' => 'You cannot edit this post']);
}

// Check if user can delete specific post
if (!current_user_can('delete_post', $post_id)) {
    wp_send_json_error(['message' => 'You cannot delete this post']);
}

// Check if user can publish posts
if (!current_user_can('publish_posts')) {
    wp_send_json_error(['message' => 'You cannot publish posts']);
}
```

#### Custom Capabilities

```php
// Register custom role with custom capability
add_action('init', 'register_custom_role');
function register_custom_role() {
    add_role('store_manager', 'Store Manager', [
        'read' => true,
        'edit_posts' => true,
        'manage_products' => true, // Custom capability
    ]);
}

// Add custom capability to existing role
$role = get_role('editor');
$role->add_cap('manage_products');

// Check custom capability
if (current_user_can('manage_products')) {
    // Allow product management
}
```

---

## 6. SQL Injection Prevention

**CRITICAL:** Never trust user input in SQL queries. Always use `$wpdb->prepare()`.

### The Problem: SQL Injection

**BEFORE (Vulnerable):**
```php
global $wpdb;

// ⚠️ CRITICAL VULNERABILITY - SQL INJECTION!
$user_id = $_GET['user_id'];
$results = $wpdb->get_results(
    "SELECT * FROM {$wpdb->posts} WHERE post_author = $user_id"
);

// Attacker can inject SQL:
// ?user_id=1 OR 1=1 -- (returns all posts)
// ?user_id=1; DROP TABLE wp_posts; -- (deletes table!)
```

**AFTER (Secure):**
```php
global $wpdb;

// ✅ SECURE - Using prepared statements
$user_id = absint($_GET['user_id']); // Sanitize first
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_author = %d",
        $user_id
    )
);
```

### Prepared Statement Placeholders

| Placeholder | Type | Example |
|-------------|------|---------|
| `%s` | String | `"SELECT * FROM table WHERE name = %s"` |
| `%d` | Integer | `"SELECT * FROM table WHERE id = %d"` |
| `%f` | Float | `"SELECT * FROM table WHERE price = %f"` |

### Complete Examples

#### SELECT Query

```php
global $wpdb;

$email = sanitize_email($_POST['email']);

// Prepared statement (prevents SQL injection)
$user = $wpdb->get_row(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->users} WHERE user_email = %s",
        $email
    )
);

if ($user) {
    echo "User found: " . esc_html($user->user_login);
}
```

#### INSERT Query

```php
global $wpdb;

// Use wpdb->insert() (automatically prepares)
$result = $wpdb->insert(
    $wpdb->prefix . 'my_table',
    [
        'title' => sanitize_text_field($_POST['title']),
        'content' => wp_kses_post($_POST['content']),
        'user_id' => absint($_POST['user_id']),
        'price' => floatval($_POST['price']),
        'created_at' => current_time('mysql'),
    ],
    ['%s', '%s', '%d', '%f', '%s'] // Format specifiers
);

if ($result === false) {
    wp_die('Database insert failed: ' . $wpdb->last_error);
}

$inserted_id = $wpdb->insert_id;
```

#### UPDATE Query

```php
global $wpdb;

$wpdb->update(
    $wpdb->prefix . 'my_table',
    [
        'title' => sanitize_text_field($_POST['title']), // New values
        'updated_at' => current_time('mysql'),
    ],
    ['id' => absint($_POST['id'])], // WHERE condition
    ['%s', '%s'], // Format for new values
    ['%d']        // Format for WHERE condition
);
```

#### DELETE Query

```php
global $wpdb;

$wpdb->delete(
    $wpdb->prefix . 'my_table',
    ['id' => absint($_POST['id'])],
    ['%d']
);
```

#### Complex WHERE Clause

```php
global $wpdb;

$status = sanitize_text_field($_POST['status']);
$min_price = floatval($_POST['min_price']);

// Multiple placeholders
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->prefix}products
         WHERE status = %s AND price >= %f
         ORDER BY created_at DESC
         LIMIT %d",
        $status,
        $min_price,
        10 // LIMIT value
    )
);
```

### Common SQL Injection Mistakes

❌ **WRONG:**
```php
// String concatenation (vulnerable!)
$sql = "SELECT * FROM table WHERE name = '" . $_POST['name'] . "'";

// Using esc_sql() (deprecated and insufficient)
$sql = "SELECT * FROM table WHERE name = '" . esc_sql($_POST['name']) . "'";

// Not using placeholders
$wpdb->query("DELETE FROM table WHERE id = $id"); // ⚠️ Vulnerable
```

✅ **CORRECT:**
```php
// Always use $wpdb->prepare()
$wpdb->get_results($wpdb->prepare(
    "SELECT * FROM table WHERE name = %s",
    $_POST['name']
));

// Use wpdb methods (insert, update, delete)
$wpdb->insert('table', ['name' => $_POST['name']], ['%s']);
```

---

## 7. Common Vulnerabilities & Attack Scenarios

### XSS (Cross-Site Scripting)

**Attack Scenario:**
```php
// Vulnerable code
echo "Welcome, " . $_GET['username'];
// Attacker visits: ?username=<script>alert(document.cookie)</script>
// Browser executes JavaScript, stealing session cookies
```

**Prevention:**
```php
// Escape output
echo "Welcome, " . esc_html($_GET['username']);
// Output: Welcome, &lt;script&gt;alert(document.cookie)&lt;/script&gt;
```

### CSRF (Cross-Site Request Forgery)

**Attack Scenario:**
```html
<!-- Attacker's site (evil.com) -->
<img src="https://yoursite.com/wp-admin/admin.php?action=delete_all_posts">
<!-- If admin is logged in, this executes without their knowledge! -->
```

**Prevention:**
```php
// Require nonce verification
if (!wp_verify_nonce($_GET['nonce'], 'delete_all_posts')) {
    wp_die('Invalid security token');
}
```

### SQL Injection

**Attack Scenario:**
```php
// Vulnerable code
$wpdb->query("DELETE FROM posts WHERE id = " . $_GET['id']);
// Attacker visits: ?id=1 OR 1=1
// Deletes ALL posts!
```

**Prevention:**
```php
// Use prepared statements
$wpdb->query($wpdb->prepare(
    "DELETE FROM posts WHERE id = %d",
    absint($_GET['id'])
));
```

### File Upload Attack

**Attack Scenario:**
```php
// Vulnerable code
move_uploaded_file($_FILES['file']['tmp_name'], 'uploads/' . $_FILES['file']['name']);
// Attacker uploads: malicious.php
// Executes: https://yoursite.com/uploads/malicious.php
```

**Prevention:**
```php
// Validate file type and use wp_handle_upload()
$allowed_types = ['image/jpeg', 'image/png'];
if (!in_array($_FILES['file']['type'], $allowed_types)) {
    wp_die('Invalid file type');
}

$upload = wp_handle_upload($_FILES['file'], ['test_form' => false]);
```

### Path Traversal

**Attack Scenario:**
```php
// Vulnerable code
include($_GET['template'] . '.php');
// Attacker visits: ?template=../../../../etc/passwd
```

**Prevention:**
```php
// Whitelist allowed templates
$allowed_templates = ['template1', 'template2'];
$template = sanitize_file_name($_GET['template']);

if (in_array($template, $allowed_templates)) {
    include($template . '.php');
}
```

---

## 8. Complete Security Implementation Example

```php
<?php
/**
 * Secure Form Handling Example
 * Demonstrates all security layers: nonces, sanitization, validation, escaping
 */

// 1. Display Form (with nonce)
function display_user_profile_form() {
    $user_id = get_current_user_id();
    $user_data = get_user_meta($user_id, 'profile_data', true);

    ?>
    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
        <input type="hidden" name="action" value="update_user_profile">
        <?php wp_nonce_field('update_profile_' . $user_id, 'profile_nonce'); ?>

        <label>
            Display Name:
            <input type="text"
                   name="display_name"
                   value="<?php echo esc_attr($user_data['display_name'] ?? ''); ?>"
                   required>
        </label>

        <label>
            Email:
            <input type="email"
                   name="email"
                   value="<?php echo esc_attr($user_data['email'] ?? ''); ?>"
                   required>
        </label>

        <label>
            Bio:
            <textarea name="bio"><?php echo esc_textarea($user_data['bio'] ?? ''); ?></textarea>
        </label>

        <label>
            Website:
            <input type="url"
                   name="website"
                   value="<?php echo esc_attr($user_data['website'] ?? ''); ?>">
        </label>

        <button type="submit">Update Profile</button>
    </form>
    <?php
}

// 2. Process Form (with full security)
add_action('admin_post_update_user_profile', 'handle_profile_update');
function handle_profile_update() {
    // SECURITY LAYER 1: Authentication
    if (!is_user_logged_in()) {
        wp_die('You must be logged in to update your profile');
    }

    $user_id = get_current_user_id();

    // SECURITY LAYER 2: Nonce Verification
    if (!isset($_POST['profile_nonce']) ||
        !wp_verify_nonce($_POST['profile_nonce'], 'update_profile_' . $user_id)) {
        wp_die('Security check failed: Invalid nonce');
    }

    // SECURITY LAYER 3: Capability Check
    if (!current_user_can('edit_user', $user_id)) {
        wp_die('You do not have permission to update this profile');
    }

    // SECURITY LAYER 4: Sanitization
    $display_name = sanitize_text_field($_POST['display_name']);
    $email = sanitize_email($_POST['email']);
    $bio = sanitize_textarea_field($_POST['bio']);
    $website = esc_url_raw($_POST['website']);

    // SECURITY LAYER 5: Validation
    $errors = [];

    if (empty($display_name) || strlen($display_name) < 3) {
        $errors[] = 'Display name must be at least 3 characters';
    }

    if (!is_email($email)) {
        $errors[] = 'Invalid email address';
    }

    if (!empty($website) && !filter_var($website, FILTER_VALIDATE_URL)) {
        $errors[] = 'Invalid website URL';
    }

    if (!empty($errors)) {
        wp_die(implode('<br>', array_map('esc_html', $errors)));
    }

    // SECURITY LAYER 6: Process Data
    $profile_data = [
        'display_name' => $display_name,
        'email' => $email,
        'bio' => $bio,
        'website' => $website,
    ];

    update_user_meta($user_id, 'profile_data', $profile_data);

    // SECURITY LAYER 7: Safe Redirect
    wp_redirect(add_query_arg('message', 'profile_updated', wp_get_referer()));
    exit;
}

// 3. Display Success Message (with escaping)
add_action('admin_notices', 'show_profile_update_notice');
function show_profile_update_notice() {
    if (isset($_GET['message']) && $_GET['message'] === 'profile_updated') {
        echo '<div class="notice notice-success is-dismissible">';
        echo '<p>' . esc_html__('Profile updated successfully!', 'my-plugin') . '</p>';
        echo '</div>';
    }
}
```

---

## 9. Security Checklist

Use this checklist for every WordPress feature you implement:

### Input Security (Forms, AJAX, APIs)
- [ ] Nonce verification implemented (`wp_verify_nonce()`)
- [ ] Capability check performed (`current_user_can()`)
- [ ] All input sanitized with appropriate functions
- [ ] All input validated for business logic
- [ ] File uploads use `wp_handle_upload()`
- [ ] File types whitelisted, not blacklisted

### Output Security (Templates, APIs)
- [ ] All dynamic content escaped with `esc_html()`, `esc_attr()`, etc.
- [ ] URLs escaped with `esc_url()`
- [ ] JavaScript variables use `wp_localize_script()` or `esc_js()`
- [ ] No raw `echo $_POST` or `echo $_GET`

### Database Security
- [ ] All queries use `$wpdb->prepare()`
- [ ] No string concatenation in SQL
- [ ] Use `$wpdb->insert()`, `$wpdb->update()`, `$wpdb->delete()`
- [ ] Table names use `$wpdb->prefix`

### Session Security
- [ ] User authentication checked (`is_user_logged_in()`)
- [ ] User roles validated (`current_user_can()`)
- [ ] Sensitive operations require re-authentication
- [ ] Session data never stored in GET parameters

### Code Quality
- [ ] No `eval()`, `assert()`, or `create_function()`
- [ ] No `extract()` on user input
- [ ] Error messages don't reveal system information
- [ ] Debug mode disabled in production (`WP_DEBUG = false`)

---

## 10. Testing Your Security Implementation

### Manual Testing Checklist

**1. Test Nonce Expiration:**
```bash
# Generate form with nonce, wait 25 hours, submit
# Expected: "Security check failed" error
```

**2. Test CSRF Protection:**
```html
<!-- Create external form pointing to your site -->
<form action="https://yoursite.com/wp-admin/admin-post.php" method="POST">
    <input name="action" value="your_action">
    <button>Submit</button>
</form>
<!-- Expected: Nonce verification fails -->
```

**3. Test XSS Prevention:**
```
Input: <script>alert('XSS')</script>
Expected Output: &lt;script&gt;alert('XSS')&lt;/script&gt; (as text)
```

**4. Test SQL Injection:**
```
Input: 1 OR 1=1
Expected: Treats as literal string, no SQL execution
```

**5. Test Capability Bypass:**
```php
// Log in as subscriber (low-privilege user)
// Try to access admin-only features
// Expected: "You do not have permission" error
```

### Automated Security Testing

**Install Security Scanner:**
```bash
# WPScan (CLI tool)
gem install wpscan
wpscan --url https://yoursite.com --enumerate vp

# Sucuri Security Plugin
wp plugin install sucuri-scanner --activate
```

**Run PHP Code Sniffer:**
```bash
# Check for security issues
vendor/bin/phpcs --standard=WordPress-Extra,WordPress-VIP-Go
```

---

## 11. Related Skills & Resources

### Prerequisites
- **PHP Fundamentals** - Understanding PHP syntax, types, functions
- **WordPress Plugin Fundamentals** - Hooks, actions, filters, plugin structure

### Advanced Topics
- **WordPress Testing & QA** - Security-focused testing strategies
- **WordPress REST API** - API endpoint security
- **WordPress Performance** - Secure caching strategies

### External Resources
- [WordPress Security Handbook](https://developer.wordpress.org/apis/security/)
- [Plugin Security Best Practices](https://developer.wordpress.org/plugins/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [WordPress Plugin Security Testing](https://make.wordpress.org/plugins/handbook/security/)

### Security Plugins for Testing
- **Wordfence Security** - Firewall and malware scanner
- **Sucuri Security** - Security auditing and monitoring
- **iThemes Security** - Security hardening and monitoring

---

## Quick Reference Card

```php
// ============================================
// NONCES (CSRF Protection)
// ============================================

// Forms
wp_nonce_field('action_name', 'nonce_field_name');
wp_verify_nonce($_POST['nonce_field_name'], 'action_name');

// URLs
wp_nonce_url($url, 'action_name', 'nonce_param');
wp_verify_nonce($_GET['nonce_param'], 'action_name');

// AJAX
wp_create_nonce('ajax_action');
check_ajax_referer('ajax_action', 'nonce');

// ============================================
// SANITIZATION (Input Cleaning)
// ============================================

sanitize_text_field()    // Single-line text
sanitize_textarea_field()// Multi-line text
sanitize_email()         // Email addresses
esc_url_raw()           // URLs (for storage)
sanitize_file_name()    // File names
absint()                // Positive integers
wp_kses_post()          // HTML content

// ============================================
// VALIDATION (Logic Checks)
// ============================================

is_email($email)        // Valid email format
is_numeric($value)      // Numeric value
strlen($str) >= 3       // Minimum length
preg_match($pattern)    // Pattern matching
in_array($value, $allowed) // Whitelist check

// ============================================
// ESCAPING (Output Protection)
// ============================================

esc_html()              // HTML content
esc_attr()              // HTML attributes
esc_url()               // URLs (output)
esc_js()                // JavaScript strings
esc_textarea()          // Textarea content

// ============================================
// CAPABILITIES (Authorization)
// ============================================

is_user_logged_in()
current_user_can('capability')
current_user_can('edit_post', $post_id)

// ============================================
// SQL INJECTION PREVENTION
// ============================================

$wpdb->prepare("SELECT * FROM table WHERE id = %d", $id);
$wpdb->insert($table, $data, $format);
$wpdb->update($table, $data, $where, $format, $where_format);
```

---

**Remember:** Security is not a feature—it's a requirement. Every line of code that handles user input or displays data must follow these principles. When in doubt, sanitize, validate, and escape.
