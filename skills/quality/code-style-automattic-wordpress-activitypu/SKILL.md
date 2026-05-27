---
name: code-style
description: PHP coding standards and WordPress patterns for ActivityPub plugin. Use when writing PHP code, creating classes, implementing WordPress hooks, or structuring plugin files.
---

# ActivityPub PHP Conventions

Plugin-specific conventions and architectural patterns for the ActivityPub plugin.

## Quick Reference

### File Naming
```
class-{name}.php         # Regular classes.
trait-{name}.php         # Traits.
interface-{name}.php     # Interfaces.
```

### Namespace Pattern
```php
namespace Activitypub;
namespace Activitypub\Transformer;
namespace Activitypub\Collection;
namespace Activitypub\Handler;
namespace Activitypub\Activity;
namespace Activitypub\Rest;
```

### Text Domain
Always use `'activitypub'` for translations:
```php
\__( 'Text', 'activitypub' );
\_e( 'Text', 'activitypub' );
```

### WordPress Global Functions
When in a namespace, always escape WordPress functions with backslash: `\get_option()`, `\add_action()`, etc.

## Comprehensive Standards

See [PHP Coding Standards](../../../docs/php-coding-standards.md) for complete WordPress coding standards.

See [PHP Class Structure](../../../docs/php-class-structure.md) for detailed directory organization.

## Directory Structure

```
includes/
├── class-*.php              # Core classes.
├── activity/                # Activity type classes.
├── collection/              # Collection classes.
├── handler/                 # Activity handlers.
├── rest/                    # REST API endpoints.
├── transformer/             # Content transformers.
└── wp-admin/                # Admin functionality.

integration/                 # Third-party integrations (root level).
```

## ActivityPub Architectural Patterns

### Transformers
Convert WordPress content into ActivityPub objects.

**When to use:** Converting posts, comments, users, or custom content types into ActivityPub format.

**Base class:** `includes/transformer/class-base.php`

**Pattern:**
```php
namespace Activitypub\Transformer;

class Custom extends Base {
    /**
     * Transform object to ActivityPub format.
     *
     * @return array The ActivityPub representation.
     */
    public function transform() {
        $object = parent::transform();
        // Custom transformation logic.
        return $object;
    }
}
```

**Examples:**
- `includes/transformer/class-post.php` - Post transformation.
- `includes/transformer/class-comment.php` - Comment transformation.
- `includes/transformer/class-event.php` - Event-specific transformation.

### Handlers
Process incoming ActivityPub activities from remote servers.

**When to use:** Processing incoming Follow, Like, Create, Delete, Update, etc. activities.

**Pattern:** Each handler processes one activity type from the inbox.

**Examples:**
- `includes/handler/class-follow.php` - Process Follow activities.
- `includes/handler/class-create.php` - Process Create activities.
- `includes/handler/class-delete.php` - Process Delete activities.
- `includes/handler/class-like.php` - Process Like activities.

### Collections
Implement ActivityPub collections (Followers, Following, etc.).

**When to use:** Exposing lists of actors, activities, or objects via ActivityPub.

**Examples:**
- `includes/collection/class-followers.php` - Followers collection.
- `includes/collection/class-following.php` - Following collection.

### REST API Controllers
Expose ActivityPub endpoints.

**Namespace:** `ACTIVITYPUB_REST_NAMESPACE`

**Examples:**
- `includes/rest/class-actors-controller.php` - Actor endpoint.
- `includes/rest/class-inbox-controller.php` - Inbox endpoint.
- `includes/rest/class-outbox-controller.php` - Outbox endpoint.
- `includes/rest/class-followers-controller.php` - Followers collection endpoint.

## Plugin-Specific Helper Functions

```php
// Get remote actor metadata.
$metadata = get_remote_metadata_by_actor( $actor_url );

// Convert ActivityPub object to URI string.
$uri = object_to_uri( $object );

// Enrich content with callbacks.
$content = enrich_content_data( $content, $pattern, $callback );

// Resolve WebFinger handle to actor URL.
$resource = Webfinger::resolve( $handle );

// Get user's ActivityPub actor URL.
$actor_url = get_author_posts_url( $user_id );

// Check if a post type is enabled for ActivityPub.
$enabled = \is_post_type_enabled( $post_type );
```

## Real Codebase Examples

**Core Classes:**
- `includes/class-activitypub.php` - Main plugin initialization.
- `includes/class-dispatcher.php` - Activity dispatching to followers.
- `includes/class-scheduler.php` - WP-Cron integration for async tasks.
- `includes/class-signature.php` - HTTP Signatures for federation.

**Activity Types:**
- `includes/activity/class-activity.php` - Base activity class.
- `includes/activity/class-follow.php` - Follow activity.
- `includes/activity/class-undo.php` - Undo activity.

**Integrations (see [Integration Patterns](../integrations/SKILL.md)):**
- `integration/class-woocommerce.php` - WooCommerce integration.
- `integration/class-buddypress.php` - BuddyPress integration.
- `integration/class-jetpack.php` - Jetpack integration.

## Common Initialization Patterns

### Static Initialization
```php
class Feature {
    /**
     * Initialize the class.
     */
    public static function init() {
        \add_action( 'init', array( self::class, 'register' ) );
        \add_filter( 'activitypub_activity_object', array( self::class, 'filter' ) );
    }
}
```

### Singleton Pattern
```php
class Manager {
    private static $instance = null;

    public static function get_instance() {
        if ( null === self::$instance ) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        $this->init();
    }
}
```

## Custom Hook Patterns

**Actions:**
```php
\do_action( 'activitypub_before_send_activity', $activity );
\do_action( 'activitypub_after_send_activity', $activity, $response );
\do_action( 'activitypub_inbox_received', $activity );
```

**Filters:**
```php
$activity = \apply_filters( 'activitypub_activity_object', $activity, $post );
$content = \apply_filters( 'activitypub_the_content', $content, $post );
$actor = \apply_filters( 'activitypub_actor_data', $actor, $user_id );
```
