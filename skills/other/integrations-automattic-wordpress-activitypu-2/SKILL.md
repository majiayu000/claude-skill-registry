---
name: integrations
description: Third-party WordPress plugin integration patterns. Use when adding new integrations, debugging compatibility with other plugins, or working with existing integrations.
---

# ActivityPub Integrations

This skill provides guidance on integrating the ActivityPub plugin with other WordPress plugins.

## Quick Reference

### Integration Location
All integrations live in the `integration/` directory.

**File naming:** `class-{plugin-name}.php` (following [PHP conventions](../code-style/SKILL.md))

### Available Integrations
- BuddyPress
- bbPress
- WooCommerce
- Jetpack
- The Events Calendar
- WP User Avatars
- And 13+ more

For complete directory structure and naming conventions, see [PHP Class Structure](../../../docs/php-class-structure.md).

## Creating New Integration

### Basic Integration Class

```php
<?php
namespace Activitypub\Integration;

class Plugin_Name {
    public static function init() {
        \add_filter( 'activitypub_transformer', array( self::class, 'custom_transformer' ), 10, 2 );
        \add_filter( 'activitypub_post_types', array( self::class, 'add_post_types' ) );
    }

    public static function custom_transformer( $transformer, $object ) {
        // Return custom transformer if needed.
        return $transformer;
    }

    public static function add_post_types( $post_types ) {
        // Add plugin's post types.
        $post_types[] = 'plugin_post_type';
        return $post_types;
    }
}
```

## Integration Patterns

### Adding Post Type Support

```php
public static function add_post_types( $post_types ) {
    $post_types[] = 'event';
    $post_types[] = 'product';
    return $post_types;
}
```

### Custom Transformers

```php
public static function transformer( $transformer, $object ) {
    if ( 'custom_type' === get_post_type( $object ) ) {
        require_once __DIR__ . '/transformer/class-custom.php';
        return new Transformer\Custom( $object );
    }
    return $transformer;
}
```

### Modifying Activities

```php
\add_filter( 'activitypub_activity_object', function( $object, $post ) {
    if ( 'product' === get_post_type( $post ) ) {
        $object['type']  = 'Product';
        $object['price'] = get_post_meta( $post->ID, 'price', true );
    }
    return $object;
}, 10, 2 );
```

## Testing Integrations

### Verify Integration Loading

```php
// Check if integration is active.
if ( class_exists( '\Activitypub\Integration\Plugin_Name' ) ) {
    // Integration loaded.
}
```

### Test Compatibility

1. Install target plugin
2. Activate ActivityPub
3. Check for conflicts
4. Verify custom post types work
5. Test federation of plugin content

## Common Integration Issues

### Plugin Detection
```php
// Multiple detection methods.
if ( defined( 'PLUGIN_VERSION' ) ) { }
if ( function_exists( 'plugin_function' ) ) { }
if ( class_exists( 'Plugin_Class' ) ) { }
```

### Hook Priority
```php
// Use appropriate priority.
add_filter( 'hook', 'callback', 20 ); // After plugin's filter.
```

### Namespace Conflicts
```php
// Use fully qualified names.
$object = new \Plugin\Namespace\Class();
```

## Existing Integrations

### BuddyPress
- Adds BuddyPress activity support
- Custom member transformers
- Group activity federation

### WooCommerce
- Product post type support
- Order activity notifications
- Customer review federation

### bbPress
- Forum topic federation
- Reply activities
- User forum profiles

## Best Practices

1. **Always check if plugin is active** before adding hooks
2. **Use late priority** for filters to override plugin defaults
3. **Test with multiple plugin versions**
4. **Document compatibility requirements**
5. **Handle plugin deactivation gracefully**
