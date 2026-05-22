---
name: wordpress-advanced-architecture
description: Advanced WordPress development with REST API endpoints, WP-CLI commands, performance optimization, and caching strategies for scalable applications.
progressive_disclosure:
  entry_point:
    summary: "Advanced WordPress development with REST API, WP-CLI, performance optimization, and caching strategies"
    when_to_use:
      - "Building custom REST API endpoints"
      - "Automating WordPress tasks with WP-CLI"
      - "Optimizing performance with caching and transients"
    quick_start:
      - "Register custom REST endpoints with permissions"
      - "Create WP-CLI commands for automation"
      - "Implement caching with transients and object cache"
---

# Advanced WordPress Architecture

Master advanced WordPress development patterns including REST API endpoints, WP-CLI commands, performance optimization, and caching strategies for scalable WordPress applications.

## 1. REST API Development

The WordPress REST API provides a powerful interface for creating custom endpoints with proper authentication, validation, and response formatting.

### Endpoint Registration with Namespacing

```php
add_action( 'rest_api_init', 'register_custom_rest_routes' );
function register_custom_rest_routes() {
    // Namespace: myplugin/v1 (enables versioning)
    $namespace = 'myplugin/v1';

    // GET /wp-json/myplugin/v1/books
    register_rest_route( $namespace, '/books', [
        'methods'  => 'GET',
        'callback' => 'get_books_callback',
        'permission_callback' => '__return_true', // Public endpoint
        'args' => [
            'per_page' => [
                'default' => 10,
                'validate_callback' => function( $param ) {
                    return is_numeric( $param ) && $param > 0 && $param <= 100;
                },
                'sanitize_callback' => 'absint',
            ],
            'page' => [
                'default' => 1,
                'validate_callback' => function( $param ) {
                    return is_numeric( $param ) && $param > 0;
                },
                'sanitize_callback' => 'absint',
            ],
        ],
    ]);

    // GET /wp-json/myplugin/v1/books/(?P<id>\d+)
    register_rest_route( $namespace, '/books/(?P<id>\d+)', [
        'methods'  => 'GET',
        'callback' => 'get_book_callback',
        'permission_callback' => '__return_true',
        'args' => [
            'id' => [
                'validate_callback' => function( $param ) {
                    return is_numeric( $param );
                },
                'sanitize_callback' => 'absint',
            ],
        ],
    ]);

    // POST /wp-json/myplugin/v1/books (authenticated)
    register_rest_route( $namespace, '/books', [
        'methods'  => 'POST',
        'callback' => 'create_book_callback',
        'permission_callback' => function() {
            return current_user_can( 'edit_posts' );
        },
        'args' => [
            'title' => [
                'required' => true,
                'type' => 'string',
                'validate_callback' => function( $param ) {
                    return is_string( $param ) && strlen( $param ) > 0;
                },
                'sanitize_callback' => 'sanitize_text_field',
            ],
            'content' => [
                'required' => false,
                'type' => 'string',
                'sanitize_callback' => 'wp_kses_post',
            ],
            'status' => [
                'default' => 'draft',
                'enum' => [ 'draft', 'publish', 'private' ],
            ],
        ],
    ]);

    // PUT /wp-json/myplugin/v1/books/(?P<id>\d+)
    register_rest_route( $namespace, '/books/(?P<id>\d+)', [
        'methods'  => 'PUT',
        'callback' => 'update_book_callback',
        'permission_callback' => function( $request ) {
            $book_id = $request->get_param( 'id' );
            return current_user_can( 'edit_post', $book_id );
        },
        'args' => [
            'id' => [
                'validate_callback' => function( $param ) {
                    return is_numeric( $param );
                },
                'sanitize_callback' => 'absint',
            ],
            'title' => [
                'type' => 'string',
                'sanitize_callback' => 'sanitize_text_field',
            ],
            'content' => [
                'type' => 'string',
                'sanitize_callback' => 'wp_kses_post',
            ],
        ],
    ]);

    // DELETE /wp-json/myplugin/v1/books/(?P<id>\d+)
    register_rest_route( $namespace, '/books/(?P<id>\d+)', [
        'methods'  => 'DELETE',
        'callback' => 'delete_book_callback',
        'permission_callback' => function( $request ) {
            $book_id = $request->get_param( 'id' );
            return current_user_can( 'delete_post', $book_id );
        },
        'args' => [
            'id' => [
                'validate_callback' => function( $param ) {
                    return is_numeric( $param );
                },
                'sanitize_callback' => 'absint',
            ],
        ],
    ]);
}
```

### Complete CRUD Implementation

```php
// GET /wp-json/myplugin/v1/books
function get_books_callback( $request ) {
    $per_page = $request->get_param( 'per_page' );
    $page = $request->get_param( 'page' );
    $offset = ( $page - 1 ) * $per_page;

    $args = [
        'post_type' => 'book',
        'posts_per_page' => $per_page,
        'offset' => $offset,
        'post_status' => 'publish',
    ];

    $query = new WP_Query( $args );

    if ( ! $query->have_posts() ) {
        return rest_ensure_response([
            'books' => [],
            'total' => 0,
            'page' => $page,
            'per_page' => $per_page,
        ]);
    }

    $books = [];
    while ( $query->have_posts() ) {
        $query->the_post();
        $books[] = [
            'id' => get_the_ID(),
            'title' => get_the_title(),
            'content' => get_the_content(),
            'author' => get_the_author(),
            'date' => get_the_date( 'c' ), // ISO 8601 format
            'link' => get_permalink(),
        ];
    }
    wp_reset_postdata();

    $response = rest_ensure_response([
        'books' => $books,
        'total' => $query->found_posts,
        'page' => $page,
        'per_page' => $per_page,
        'total_pages' => ceil( $query->found_posts / $per_page ),
    ]);

    // Add HATEOAS links
    $response->add_link( 'self', rest_url( "myplugin/v1/books?page={$page}&per_page={$per_page}" ) );

    if ( $page > 1 ) {
        $prev_page = $page - 1;
        $response->add_link( 'prev', rest_url( "myplugin/v1/books?page={$prev_page}&per_page={$per_page}" ) );
    }

    if ( $page < ceil( $query->found_posts / $per_page ) ) {
        $next_page = $page + 1;
        $response->add_link( 'next', rest_url( "myplugin/v1/books?page={$next_page}&per_page={$per_page}" ) );
    }

    return $response;
}

// GET /wp-json/myplugin/v1/books/123
function get_book_callback( $request ) {
    $book_id = $request->get_param( 'id' );
    $book = get_post( $book_id );

    if ( ! $book || 'book' !== $book->post_type ) {
        return new WP_Error(
            'book_not_found',
            'Book not found',
            [ 'status' => 404 ]
        );
    }

    $data = [
        'id' => $book->ID,
        'title' => $book->post_title,
        'content' => apply_filters( 'the_content', $book->post_content ),
        'excerpt' => $book->post_excerpt,
        'author' => get_the_author_meta( 'display_name', $book->post_author ),
        'date' => get_the_date( 'c', $book ),
        'modified' => get_the_modified_date( 'c', $book ),
        'status' => $book->post_status,
        'link' => get_permalink( $book ),
        'featured_image' => get_the_post_thumbnail_url( $book, 'large' ),
        'meta' => [
            'isbn' => get_post_meta( $book->ID, '_isbn', true ),
            'pages' => (int) get_post_meta( $book->ID, '_pages', true ),
        ],
    ];

    return rest_ensure_response( $data );
}

// POST /wp-json/myplugin/v1/books
function create_book_callback( $request ) {
    $title = $request->get_param( 'title' );
    $content = $request->get_param( 'content' );
    $status = $request->get_param( 'status' );

    $post_data = [
        'post_type' => 'book',
        'post_title' => $title,
        'post_content' => $content,
        'post_status' => $status,
        'post_author' => get_current_user_id(),
    ];

    $book_id = wp_insert_post( $post_data, true );

    if ( is_wp_error( $book_id ) ) {
        return new WP_Error(
            'book_creation_failed',
            $book_id->get_error_message(),
            [ 'status' => 500 ]
        );
    }

    // Add custom metadata if provided
    if ( $request->has_param( 'isbn' ) ) {
        update_post_meta( $book_id, '_isbn', sanitize_text_field( $request->get_param( 'isbn' ) ) );
    }

    if ( $request->has_param( 'pages' ) ) {
        update_post_meta( $book_id, '_pages', absint( $request->get_param( 'pages' ) ) );
    }

    $response = rest_ensure_response([
        'id' => $book_id,
        'title' => $title,
        'message' => 'Book created successfully',
        'link' => get_permalink( $book_id ),
    ]);

    $response->set_status( 201 ); // Created
    $response->header( 'Location', rest_url( "myplugin/v1/books/{$book_id}" ) );

    return $response;
}

// PUT /wp-json/myplugin/v1/books/123
function update_book_callback( $request ) {
    $book_id = $request->get_param( 'id' );
    $book = get_post( $book_id );

    if ( ! $book || 'book' !== $book->post_type ) {
        return new WP_Error(
            'book_not_found',
            'Book not found',
            [ 'status' => 404 ]
        );
    }

    $post_data = [ 'ID' => $book_id ];

    if ( $request->has_param( 'title' ) ) {
        $post_data['post_title'] = $request->get_param( 'title' );
    }

    if ( $request->has_param( 'content' ) ) {
        $post_data['post_content'] = $request->get_param( 'content' );
    }

    if ( $request->has_param( 'status' ) ) {
        $post_data['post_status'] = $request->get_param( 'status' );
    }

    $result = wp_update_post( $post_data, true );

    if ( is_wp_error( $result ) ) {
        return new WP_Error(
            'book_update_failed',
            $result->get_error_message(),
            [ 'status' => 500 ]
        );
    }

    return rest_ensure_response([
        'id' => $book_id,
        'message' => 'Book updated successfully',
        'link' => get_permalink( $book_id ),
    ]);
}

// DELETE /wp-json/myplugin/v1/books/123
function delete_book_callback( $request ) {
    $book_id = $request->get_param( 'id' );
    $book = get_post( $book_id );

    if ( ! $book || 'book' !== $book->post_type ) {
        return new WP_Error(
            'book_not_found',
            'Book not found',
            [ 'status' => 404 ]
        );
    }

    // Soft delete (trash) or hard delete
    $force = $request->get_param( 'force' );
    $result = wp_delete_post( $book_id, $force );

    if ( ! $result ) {
        return new WP_Error(
            'book_deletion_failed',
            'Failed to delete book',
            [ 'status' => 500 ]
        );
    }

    return rest_ensure_response([
        'deleted' => true,
        'id' => $book_id,
        'message' => $force ? 'Book permanently deleted' : 'Book moved to trash',
    ]);
}
```

### Controller Pattern for Complex Endpoints

For complex REST endpoints, use a controller class to organize logic:

```php
<?php
namespace MyPlugin\API;

class Books_Controller extends \WP_REST_Controller {

    protected $namespace = 'myplugin/v1';
    protected $rest_base = 'books';

    public function register_routes() {
        register_rest_route( $this->namespace, '/' . $this->rest_base, [
            [
                'methods'  => \WP_REST_Server::READABLE,
                'callback' => [ $this, 'get_items' ],
                'permission_callback' => [ $this, 'get_items_permissions_check' ],
                'args' => $this->get_collection_params(),
            ],
            [
                'methods'  => \WP_REST_Server::CREATABLE,
                'callback' => [ $this, 'create_item' ],
                'permission_callback' => [ $this, 'create_item_permissions_check' ],
                'args' => $this->get_endpoint_args_for_item_schema( \WP_REST_Server::CREATABLE ),
            ],
            'schema' => [ $this, 'get_public_item_schema' ],
        ]);

        register_rest_route( $this->namespace, '/' . $this->rest_base . '/(?P<id>[\d]+)', [
            'args' => [
                'id' => [
                    'description' => 'Unique identifier for the book',
                    'type' => 'integer',
                ],
            ],
            [
                'methods'  => \WP_REST_Server::READABLE,
                'callback' => [ $this, 'get_item' ],
                'permission_callback' => [ $this, 'get_item_permissions_check' ],
                'args' => [
                    'context' => $this->get_context_param( [ 'default' => 'view' ] ),
                ],
            ],
            [
                'methods'  => \WP_REST_Server::EDITABLE,
                'callback' => [ $this, 'update_item' ],
                'permission_callback' => [ $this, 'update_item_permissions_check' ],
                'args' => $this->get_endpoint_args_for_item_schema( \WP_REST_Server::EDITABLE ),
            ],
            [
                'methods'  => \WP_REST_Server::DELETABLE,
                'callback' => [ $this, 'delete_item' ],
                'permission_callback' => [ $this, 'delete_item_permissions_check' ],
                'args' => [
                    'force' => [
                        'type' => 'boolean',
                        'default' => false,
                        'description' => 'Whether to bypass trash and force deletion',
                    ],
                ],
            ],
            'schema' => [ $this, 'get_public_item_schema' ],
        ]);
    }

    public function get_items( $request ) {
        // Implementation similar to get_books_callback above
    }

    public function get_item( $request ) {
        // Implementation similar to get_book_callback above
    }

    public function create_item( $request ) {
        // Implementation similar to create_book_callback above
    }

    public function update_item( $request ) {
        // Implementation similar to update_book_callback above
    }

    public function delete_item( $request ) {
        // Implementation similar to delete_book_callback above
    }

    public function get_items_permissions_check( $request ) {
        return true; // Public endpoint
    }

    public function get_item_permissions_check( $request ) {
        return true; // Public endpoint
    }

    public function create_item_permissions_check( $request ) {
        return current_user_can( 'edit_posts' );
    }

    public function update_item_permissions_check( $request ) {
        $book_id = $request->get_param( 'id' );
        return current_user_can( 'edit_post', $book_id );
    }

    public function delete_item_permissions_check( $request ) {
        $book_id = $request->get_param( 'id' );
        return current_user_can( 'delete_post', $book_id );
    }

    public function get_public_item_schema() {
        if ( $this->schema ) {
            return $this->add_additional_fields_schema( $this->schema );
        }

        $schema = [
            '$schema'    => 'http://json-schema.org/draft-04/schema#',
            'title'      => 'book',
            'type'       => 'object',
            'properties' => [
                'id' => [
                    'description' => 'Unique identifier for the book',
                    'type'        => 'integer',
                    'context'     => [ 'view', 'edit', 'embed' ],
                    'readonly'    => true,
                ],
                'title' => [
                    'description' => 'The book title',
                    'type'        => 'string',
                    'context'     => [ 'view', 'edit', 'embed' ],
                    'required'    => true,
                ],
                'content' => [
                    'description' => 'The book content',
                    'type'        => 'string',
                    'context'     => [ 'view', 'edit' ],
                ],
                'status' => [
                    'description' => 'The book status',
                    'type'        => 'string',
                    'enum'        => [ 'draft', 'publish', 'private' ],
                    'context'     => [ 'view', 'edit' ],
                ],
            ],
        ];

        $this->schema = $schema;

        return $this->add_additional_fields_schema( $this->schema );
    }
}

// Register controller
add_action( 'rest_api_init', function() {
    $controller = new \MyPlugin\API\Books_Controller();
    $controller->register_routes();
});
```

### REST API Authentication

```php
// Application Passwords (WordPress 5.6+)
// Users generate passwords at /wp-admin/profile.php

// Example cURL request with authentication:
// curl -X POST https://example.com/wp-json/myplugin/v1/books \
//   -u username:application_password \
//   -H "Content-Type: application/json" \
//   -d '{"title":"New Book","content":"Book content"}'

// Cookie authentication for logged-in users (requires nonce)
add_action( 'rest_api_init', function() {
    // Add nonce to wp_localize_script
    wp_localize_script( 'my-ajax-script', 'wpApiSettings', [
        'root' => esc_url_raw( rest_url() ),
        'nonce' => wp_create_nonce( 'wp_rest' ),
    ]);
});

// JavaScript REST API call with nonce:
/*
fetch( wpApiSettings.root + 'myplugin/v1/books', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-WP-Nonce': wpApiSettings.nonce
    },
    body: JSON.stringify({
        title: 'New Book',
        content: 'Book content'
    })
}).then( response => response.json() )
  .then( data => console.log( data ) );
*/
```

## 2. WP-CLI Commands

WP-CLI enables automation of WordPress tasks through custom commands.

### Custom Command Registration

```php
<?php
namespace MyPlugin\CLI;

class Books_Command {

    /**
     * List all books.
     *
     * ## OPTIONS
     *
     * [--format=<format>]
     * : Render output in a particular format.
     * ---
     * default: table
     * options:
     *   - table
     *   - csv
     *   - json
     *   - yaml
     * ---
     *
     * [--status=<status>]
     * : Filter by post status.
     *
     * ## EXAMPLES
     *
     *     wp books list
     *     wp books list --format=json
     *     wp books list --status=publish
     *
     * @when after_wp_load
     */
    public function list( $args, $assoc_args ) {
        $defaults = [
            'format' => 'table',
            'status' => 'any',
        ];
        $assoc_args = wp_parse_args( $assoc_args, $defaults );

        $query_args = [
            'post_type' => 'book',
            'posts_per_page' => -1,
            'post_status' => $assoc_args['status'],
        ];

        $books = get_posts( $query_args );

        if ( empty( $books ) ) {
            \WP_CLI::warning( 'No books found.' );
            return;
        }

        $items = [];
        foreach ( $books as $book ) {
            $items[] = [
                'ID' => $book->ID,
                'Title' => $book->post_title,
                'Status' => $book->post_status,
                'Author' => get_the_author_meta( 'display_name', $book->post_author ),
                'Date' => get_the_date( 'Y-m-d H:i:s', $book ),
            ];
        }

        \WP_CLI\Utils\format_items( $assoc_args['format'], $items, [ 'ID', 'Title', 'Status', 'Author', 'Date' ] );

        \WP_CLI::success( sprintf( 'Found %d books.', count( $items ) ) );
    }

    /**
     * Create a new book.
     *
     * ## OPTIONS
     *
     * <title>
     * : The book title.
     *
     * [--content=<content>]
     * : The book content.
     *
     * [--status=<status>]
     * : The book status.
     * ---
     * default: draft
     * options:
     *   - draft
     *   - publish
     *   - private
     * ---
     *
     * [--isbn=<isbn>]
     * : The book ISBN.
     *
     * [--pages=<pages>]
     * : Number of pages.
     *
     * ## EXAMPLES
     *
     *     wp books create "My Book Title"
     *     wp books create "My Book" --status=publish --isbn=978-3-16-148410-0 --pages=350
     *
     * @when after_wp_load
     */
    public function create( $args, $assoc_args ) {
        $title = $args[0];

        $defaults = [
            'content' => '',
            'status' => 'draft',
        ];
        $assoc_args = wp_parse_args( $assoc_args, $defaults );

        $post_data = [
            'post_type' => 'book',
            'post_title' => $title,
            'post_content' => $assoc_args['content'],
            'post_status' => $assoc_args['status'],
            'post_author' => get_current_user_id(),
        ];

        $book_id = wp_insert_post( $post_data, true );

        if ( is_wp_error( $book_id ) ) {
            \WP_CLI::error( 'Failed to create book: ' . $book_id->get_error_message() );
        }

        // Add custom metadata
        if ( isset( $assoc_args['isbn'] ) ) {
            update_post_meta( $book_id, '_isbn', sanitize_text_field( $assoc_args['isbn'] ) );
        }

        if ( isset( $assoc_args['pages'] ) ) {
            update_post_meta( $book_id, '_pages', absint( $assoc_args['pages'] ) );
        }

        \WP_CLI::success( sprintf( 'Created book #%d: %s', $book_id, $title ) );
    }

    /**
     * Import books from CSV file.
     *
     * ## OPTIONS
     *
     * <file>
     * : Path to CSV file.
     *
     * [--dry-run]
     * : Preview import without creating books.
     *
     * ## EXAMPLES
     *
     *     wp books import books.csv
     *     wp books import books.csv --dry-run
     *
     * @when after_wp_load
     */
    public function import( $args, $assoc_args ) {
        $file = $args[0];
        $dry_run = isset( $assoc_args['dry-run'] );

        if ( ! file_exists( $file ) ) {
            \WP_CLI::error( 'File not found: ' . $file );
        }

        $csv = array_map( 'str_getcsv', file( $file ) );
        $header = array_shift( $csv );

        $total = count( $csv );
        $created = 0;

        \WP_CLI::log( sprintf( 'Processing %d books...', $total ) );

        $progress = \WP_CLI\Utils\make_progress_bar( 'Importing books', $total );

        foreach ( $csv as $row ) {
            $book = array_combine( $header, $row );

            if ( $dry_run ) {
                \WP_CLI::log( sprintf( 'Would create: %s', $book['title'] ) );
            } else {
                $post_data = [
                    'post_type' => 'book',
                    'post_title' => $book['title'],
                    'post_content' => $book['content'] ?? '',
                    'post_status' => $book['status'] ?? 'draft',
                ];

                $book_id = wp_insert_post( $post_data, true );

                if ( ! is_wp_error( $book_id ) ) {
                    if ( isset( $book['isbn'] ) ) {
                        update_post_meta( $book_id, '_isbn', $book['isbn'] );
                    }
                    $created++;
                }
            }

            $progress->tick();
        }

        $progress->finish();

        if ( $dry_run ) {
            \WP_CLI::success( sprintf( 'Dry run complete. Would create %d books.', $total ) );
        } else {
            \WP_CLI::success( sprintf( 'Imported %d of %d books.', $created, $total ) );
        }
    }

    /**
     * Generate sample books.
     *
     * ## OPTIONS
     *
     * [--count=<count>]
     * : Number of books to generate.
     * ---
     * default: 10
     * ---
     *
     * [--status=<status>]
     * : Book status.
     * ---
     * default: publish
     * ---
     *
     * ## EXAMPLES
     *
     *     wp books generate --count=50
     *     wp books generate --count=100 --status=draft
     *
     * @when after_wp_load
     */
    public function generate( $args, $assoc_args ) {
        $count = isset( $assoc_args['count'] ) ? absint( $assoc_args['count'] ) : 10;
        $status = isset( $assoc_args['status'] ) ? $assoc_args['status'] : 'publish';

        $progress = \WP_CLI\Utils\make_progress_bar( 'Generating books', $count );

        for ( $i = 1; $i <= $count; $i++ ) {
            $post_data = [
                'post_type' => 'book',
                'post_title' => sprintf( 'Sample Book %d', $i ),
                'post_content' => sprintf( 'This is sample book number %d.', $i ),
                'post_status' => $status,
            ];

            $book_id = wp_insert_post( $post_data );

            // Add random metadata
            update_post_meta( $book_id, '_isbn', sprintf( '978-3-16-%06d-0', rand( 100000, 999999 ) ) );
            update_post_meta( $book_id, '_pages', rand( 100, 500 ) );

            $progress->tick();
        }

        $progress->finish();

        \WP_CLI::success( sprintf( 'Generated %d books.', $count ) );
    }
}

// Register WP-CLI command
if ( defined( 'WP_CLI' ) && WP_CLI ) {
    \WP_CLI::add_command( 'books', 'MyPlugin\CLI\Books_Command' );
}
```

### Interactive Prompts and Confirmation

```php
/**
 * Delete all books (with confirmation).
 *
 * ## OPTIONS
 *
 * [--yes]
 * : Skip confirmation prompt.
 *
 * ## EXAMPLES
 *
 *     wp books delete-all
 *     wp books delete-all --yes
 *
 * @when after_wp_load
 */
public function delete_all( $args, $assoc_args ) {
    $books = get_posts([
        'post_type' => 'book',
        'posts_per_page' => -1,
        'fields' => 'ids',
    ]);

    $count = count( $books );

    if ( 0 === $count ) {
        \WP_CLI::warning( 'No books to delete.' );
        return;
    }

    // Prompt for confirmation unless --yes flag is provided
    \WP_CLI::confirm( sprintf( 'Are you sure you want to delete %d books?', $count ), $assoc_args );

    $progress = \WP_CLI\Utils\make_progress_bar( 'Deleting books', $count );

    foreach ( $books as $book_id ) {
        wp_delete_post( $book_id, true ); // Force delete
        $progress->tick();
    }

    $progress->finish();

    \WP_CLI::success( sprintf( 'Deleted %d books.', $count ) );
}
```

### Testing WP-CLI Commands

```bash
# List all WP-CLI commands
wp cli command-list

# Get help for custom command
wp help books
wp help books create

# Test commands
wp books list
wp books list --format=json
wp books create "Test Book" --status=publish
wp books generate --count=50
wp books import books.csv --dry-run
wp books delete-all --yes
```

## 3. Performance Optimization

### Transients API (Expiring Cache)

```php
// Store data with expiration
function get_popular_books() {
    $transient_key = 'popular_books';

    // Try to get cached value
    $popular_books = get_transient( $transient_key );

    if ( false === $popular_books ) {
        // Cache miss - fetch and store
        $popular_books = new WP_Query([
            'post_type' => 'book',
            'posts_per_page' => 10,
            'meta_key' => '_view_count',
            'orderby' => 'meta_value_num',
            'order' => 'DESC',
        ]);

        // Cache for 1 hour (3600 seconds)
        set_transient( $transient_key, $popular_books, HOUR_IN_SECONDS );
    }

    return $popular_books;
}

// Invalidate cache on post update
add_action( 'save_post_book', 'invalidate_books_cache' );
function invalidate_books_cache( $post_id ) {
    delete_transient( 'popular_books' );
}

// Site-specific transients (multisite)
set_site_transient( 'network_data', $data, DAY_IN_SECONDS );
$data = get_site_transient( 'network_data' );
delete_site_transient( 'network_data' );

// Clear all transients (cleanup)
global $wpdb;
$wpdb->query( "DELETE FROM $wpdb->options WHERE option_name LIKE '%_transient_%'" );
```

### Object Caching (Redis, Memcached)

```php
// WordPress Object Cache functions (wp_cache_*)
// Works with persistent cache (Redis/Memcached) if configured

// Add to cache
wp_cache_add( 'my_key', $data, 'my_group', 3600 );

// Get from cache
$data = wp_cache_get( 'my_key', 'my_group' );
if ( false === $data ) {
    // Cache miss - fetch and cache
    $data = expensive_database_query();
    wp_cache_set( 'my_key', $data, 'my_group', 3600 );
}

// Delete from cache
wp_cache_delete( 'my_key', 'my_group' );

// Flush entire cache
wp_cache_flush();

// Example: Cache user data
function get_user_books( $user_id ) {
    $cache_key = "user_{$user_id}_books";
    $cache_group = 'user_books';

    $books = wp_cache_get( $cache_key, $cache_group );

    if ( false === $books ) {
        $books = get_posts([
            'post_type' => 'book',
            'author' => $user_id,
            'posts_per_page' => -1,
        ]);

        wp_cache_set( $cache_key, $books, $cache_group, HOUR_IN_SECONDS );
    }

    return $books;
}

// Invalidate user cache on book update
add_action( 'save_post_book', 'invalidate_user_books_cache', 10, 2 );
function invalidate_user_books_cache( $post_id, $post ) {
    wp_cache_delete( "user_{$post->post_author}_books", 'user_books' );
}
```

### Redis Configuration (object-cache.php)

```php
// Install Redis plugin or drop-in
// Recommended: https://wordpress.org/plugins/redis-cache/

// Or manual configuration:
// wp-content/object-cache.php

<?php
// Redis configuration
global $redis_server;
$redis_server = [
    'host'     => '127.0.0.1',
    'port'     => 6379,
    'auth'     => '', // Password if required
    'database' => 0,  // Redis database number
];

// wp-config.php settings
define( 'WP_REDIS_HOST', '127.0.0.1' );
define( 'WP_REDIS_PORT', 6379 );
define( 'WP_REDIS_DATABASE', 0 );
define( 'WP_REDIS_TIMEOUT', 1 );
define( 'WP_REDIS_READ_TIMEOUT', 1 );
```

### Database Query Optimization

```php
// BAD: Multiple queries in loop
$posts = get_posts([ 'post_type' => 'book', 'posts_per_page' => -1 ]);
foreach ( $posts as $post ) {
    $author = get_user_by( 'id', $post->post_author ); // N+1 query problem
    $meta = get_post_meta( $post->ID, '_isbn', true ); // Another query per iteration
}

// GOOD: Pre-fetch data
$posts = get_posts([ 'post_type' => 'book', 'posts_per_page' => -1 ]);
$author_ids = wp_list_pluck( $posts, 'post_author' );
$authors = get_users([ 'include' => $author_ids ]); // Single query
$authors_by_id = [];
foreach ( $authors as $author ) {
    $authors_by_id[ $author->ID ] = $author;
}

// Pre-load all meta with update_meta_cache()
update_post_caches( $posts, 'book' );

foreach ( $posts as $post ) {
    $author = $authors_by_id[ $post->post_author ];
    $isbn = get_post_meta( $post->ID, '_isbn', true ); // Uses cache
}

// Custom queries with JOIN
global $wpdb;
$results = $wpdb->get_results("
    SELECT p.*, pm.meta_value as isbn
    FROM {$wpdb->posts} p
    LEFT JOIN {$wpdb->postmeta} pm ON p.ID = pm.post_id AND pm.meta_key = '_isbn'
    WHERE p.post_type = 'book'
    AND p.post_status = 'publish'
    ORDER BY p.post_date DESC
    LIMIT 10
");

// Add database indexes for frequently queried meta
global $wpdb;
$wpdb->query("
    CREATE INDEX meta_key_value ON {$wpdb->postmeta} (meta_key, meta_value(20))
");
```

### Lazy Loading and Pagination

```php
// Paginate large queries
function get_books_paginated( $page = 1, $per_page = 20 ) {
    $args = [
        'post_type' => 'book',
        'posts_per_page' => $per_page,
        'paged' => $page,
    ];

    return new WP_Query( $args );
}

// Infinite scroll with AJAX
add_action( 'wp_ajax_load_more_books', 'ajax_load_more_books' );
add_action( 'wp_ajax_nopriv_load_more_books', 'ajax_load_more_books' );
function ajax_load_more_books() {
    check_ajax_referer( 'load_more_nonce', 'nonce' );

    $page = isset( $_POST['page'] ) ? absint( $_POST['page'] ) : 1;
    $query = get_books_paginated( $page, 10 );

    if ( $query->have_posts() ) {
        ob_start();
        while ( $query->have_posts() ) {
            $query->the_post();
            get_template_part( 'template-parts/content', 'book' );
        }
        $html = ob_get_clean();

        wp_send_json_success([
            'html' => $html,
            'has_more' => $query->max_num_pages > $page,
        ]);
    } else {
        wp_send_json_error( 'No more books' );
    }
}

// Lazy load images (native HTML)
<img src="book-cover.jpg" loading="lazy" alt="Book Cover">
```

### Profiling with Query Monitor

```php
// Install Query Monitor plugin
// https://wordpress.org/plugins/query-monitor/

// Add custom timing measurements
do_action( 'qm/start', 'my_expensive_operation' );
// ... expensive code ...
do_action( 'qm/stop', 'my_expensive_operation' );

// Log custom data
do_action( 'qm/debug', 'Custom debug message' );
do_action( 'qm/info', $data_to_inspect );

// Benchmark queries
Query Monitor shows:
// - SQL queries (count, time, duplicates)
// - HTTP requests
// - Hooks and actions
// - PHP errors and notices
// - Template file hierarchy
// - Enqueued scripts/styles
```

## 4. Caching Strategies

### Fragment Caching

```php
// Cache HTML fragments
function render_book_grid() {
    $cache_key = 'book_grid_html';
    $html = get_transient( $cache_key );

    if ( false === $html ) {
        ob_start();

        $books = new WP_Query([
            'post_type' => 'book',
            'posts_per_page' => 12,
        ]);

        if ( $books->have_posts() ) {
            echo '<div class="book-grid">';
            while ( $books->have_posts() ) {
                $books->the_post();
                ?>
                <div class="book-item">
                    <h3><?php the_title(); ?></h3>
                    <?php the_post_thumbnail( 'medium' ); ?>
                </div>
                <?php
            }
            echo '</div>';
        }
        wp_reset_postdata();

        $html = ob_get_clean();
        set_transient( $cache_key, $html, HOUR_IN_SECONDS );
    }

    echo $html;
}
```

### Page Caching vs Object Caching

```php
/**
 * Page Caching:
 * - Caches entire HTML pages
 * - Fastest (serves static HTML)
 * - Plugins: WP Super Cache, W3 Total Cache, WP Rocket
 * - Bypassed for logged-in users
 *
 * Object Caching:
 * - Caches database queries and computed values
 * - Works for all users (logged-in and anonymous)
 * - Requires persistent cache backend (Redis, Memcached)
 * - Granular cache control
 */

// Example: Bypass page cache for dynamic content
header( 'Cache-Control: no-cache, must-revalidate, max-age=0' );

// Cache-Control headers for static assets
function add_cache_headers() {
    if ( is_admin() || is_user_logged_in() ) {
        return;
    }

    // Cache static pages for 1 hour
    if ( is_page() || is_single() ) {
        header( 'Cache-Control: public, max-age=3600' );
    }

    // Cache archives for 30 minutes
    if ( is_archive() || is_home() ) {
        header( 'Cache-Control: public, max-age=1800' );
    }
}
add_action( 'send_headers', 'add_cache_headers' );
```

### Cache Invalidation Patterns

```php
// Pattern 1: Time-based expiration
set_transient( 'data', $value, 12 * HOUR_IN_SECONDS );

// Pattern 2: Event-based invalidation
add_action( 'save_post_book', 'clear_book_caches' );
function clear_book_caches( $post_id ) {
    // Clear specific caches
    delete_transient( 'popular_books' );
    delete_transient( 'recent_books' );
    wp_cache_delete( "book_{$post_id}", 'books' );

    // Clear author cache
    $post = get_post( $post_id );
    wp_cache_delete( "user_{$post->post_author}_books", 'user_books' );
}

// Pattern 3: Versioned cache keys
function get_cache_version() {
    $version = wp_cache_get( 'cache_version', 'global' );
    if ( false === $version ) {
        $version = time();
        wp_cache_set( 'cache_version', $version, 'global' );
    }
    return $version;
}

function get_cached_data( $key ) {
    $version = get_cache_version();
    $versioned_key = "{$key}_v{$version}";
    return wp_cache_get( $versioned_key, 'my_group' );
}

function set_cached_data( $key, $data ) {
    $version = get_cache_version();
    $versioned_key = "{$key}_v{$version}";
    wp_cache_set( $versioned_key, $data, 'my_group', HOUR_IN_SECONDS );
}

function invalidate_all_caches() {
    // Increment version to invalidate all caches
    $new_version = time();
    wp_cache_set( 'cache_version', $new_version, 'global' );
}

// Pattern 4: Cache warming
add_action( 'save_post_book', 'warm_book_caches', 20 );
function warm_book_caches( $post_id ) {
    // Rebuild cache immediately after invalidation
    get_popular_books(); // Rebuilds transient
}
```

### CDN Integration

```php
// Rewrite asset URLs to CDN
add_filter( 'wp_get_attachment_url', 'cdn_rewrite_url' );
add_filter( 'wp_calculate_image_srcset', 'cdn_rewrite_srcset' );

function cdn_rewrite_url( $url ) {
    $cdn_domain = 'https://cdn.example.com';
    $site_url = site_url();

    // Only rewrite uploads directory
    if ( strpos( $url, '/wp-content/uploads/' ) !== false ) {
        return str_replace( $site_url, $cdn_domain, $url );
    }

    return $url;
}

function cdn_rewrite_srcset( $sources ) {
    if ( ! is_array( $sources ) ) {
        return $sources;
    }

    foreach ( $sources as &$source ) {
        $source['url'] = cdn_rewrite_url( $source['url'] );
    }

    return $sources;
}

// Purge CDN cache on content update
add_action( 'save_post', 'purge_cdn_cache' );
function purge_cdn_cache( $post_id ) {
    // Example: Cloudflare API
    $zone_id = 'your_zone_id';
    $api_key = 'your_api_key';
    $email = 'your@email.com';

    $url = get_permalink( $post_id );

    wp_remote_post( "https://api.cloudflare.com/client/v4/zones/{$zone_id}/purge_cache", [
        'headers' => [
            'X-Auth-Email' => $email,
            'X-Auth-Key' => $api_key,
            'Content-Type' => 'application/json',
        ],
        'body' => json_encode([
            'files' => [ $url ],
        ]),
    ]);
}
```

## 5. Advanced Database Patterns

### WP_Query Optimization

```php
// Use 'fields' parameter to limit data
$query = new WP_Query([
    'post_type' => 'book',
    'fields' => 'ids', // Only return IDs (faster)
]);

// Count queries
$count = new WP_Query([
    'post_type' => 'book',
    'posts_per_page' => -1,
    'fields' => 'ids',
    'no_found_rows' => true, // Skip SQL_CALC_FOUND_ROWS
    'update_post_meta_cache' => false,
    'update_post_term_cache' => false,
]);

// Complex meta queries with performance in mind
$query = new WP_Query([
    'post_type' => 'book',
    'meta_query' => [
        'relation' => 'AND',
        [
            'key' => '_pages',
            'value' => 200,
            'compare' => '>',
            'type' => 'NUMERIC',
        ],
        [
            'key' => '_rating',
            'value' => 4,
            'compare' => '>=',
            'type' => 'DECIMAL',
        ],
    ],
    'orderby' => 'meta_value_num',
    'order' => 'DESC',
]);
```

### Direct SQL for Complex Queries

```php
// When WP_Query is too slow, use direct SQL
global $wpdb;

// Get books with JOIN on multiple meta keys
$results = $wpdb->get_results("
    SELECT
        p.ID,
        p.post_title,
        pm1.meta_value as isbn,
        pm2.meta_value as pages,
        pm3.meta_value as rating
    FROM {$wpdb->posts} p
    LEFT JOIN {$wpdb->postmeta} pm1 ON p.ID = pm1.post_id AND pm1.meta_key = '_isbn'
    LEFT JOIN {$wpdb->postmeta} pm2 ON p.ID = pm2.post_id AND pm2.meta_key = '_pages'
    LEFT JOIN {$wpdb->postmeta} pm3 ON p.ID = pm3.post_id AND pm3.meta_key = '_rating'
    WHERE p.post_type = 'book'
    AND p.post_status = 'publish'
    AND CAST(pm2.meta_value AS UNSIGNED) > 200
    ORDER BY CAST(pm3.meta_value AS DECIMAL(3,2)) DESC
    LIMIT 20
");

// Use $wpdb->prepare() for dynamic values
$min_pages = 200;
$results = $wpdb->get_results( $wpdb->prepare("
    SELECT p.ID, p.post_title, pm.meta_value as pages
    FROM {$wpdb->posts} p
    INNER JOIN {$wpdb->postmeta} pm ON p.ID = pm.post_id
    WHERE p.post_type = 'book'
    AND pm.meta_key = '_pages'
    AND CAST(pm.meta_value AS UNSIGNED) > %d
    ORDER BY p.post_date DESC
", $min_pages ) );
```

### Database Indexing

```php
// Add custom indexes in plugin activation
register_activation_hook( __FILE__, 'create_custom_indexes' );
function create_custom_indexes() {
    global $wpdb;

    // Index on post_type and post_status (common filter)
    $wpdb->query("
        CREATE INDEX idx_post_type_status
        ON {$wpdb->posts} (post_type, post_status)
    ");

    // Index on meta_key and meta_value for frequent lookups
    $wpdb->query("
        CREATE INDEX idx_meta_key_value
        ON {$wpdb->postmeta} (meta_key, meta_value(191))
    ");

    // Composite index for date-based queries
    $wpdb->query("
        CREATE INDEX idx_post_type_date
        ON {$wpdb->posts} (post_type, post_date)
    ");
}

// Remove indexes on deactivation
register_deactivation_hook( __FILE__, 'remove_custom_indexes' );
function remove_custom_indexes() {
    global $wpdb;

    $wpdb->query( "DROP INDEX idx_post_type_status ON {$wpdb->posts}" );
    $wpdb->query( "DROP INDEX idx_meta_key_value ON {$wpdb->postmeta}" );
    $wpdb->query( "DROP INDEX idx_post_type_date ON {$wpdb->posts}" );
}
```

## 6. Multisite Development

### Network-Activated Plugins

```php
// Detect multisite
if ( is_multisite() ) {
    // Multisite-specific code
}

// Network-wide hooks
add_action( 'network_admin_menu', 'add_network_admin_page' );
function add_network_admin_page() {
    add_menu_page(
        'Network Settings',
        'My Plugin',
        'manage_network_options',
        'my-network-settings',
        'render_network_settings_page'
    );
}

// Network options (not site-specific)
add_site_option( 'my_network_setting', 'value' );
$value = get_site_option( 'my_network_setting' );
update_site_option( 'my_network_setting', 'new_value' );
delete_site_option( 'my_network_setting' );
```

### Cross-Site Operations

```php
// Switch to another site
$current_blog_id = get_current_blog_id();
switch_to_blog( 2 ); // Switch to site ID 2

// Perform operations on site 2
$posts = get_posts([ 'post_type' => 'book' ]);
update_option( 'my_option', 'value' );

// Always restore
restore_current_blog();

// Iterate all sites
$sites = get_sites([ 'number' => 999 ]);
foreach ( $sites as $site ) {
    switch_to_blog( $site->blog_id );

    // Do something on each site
    $count = wp_count_posts( 'book' );
    error_log( "Site {$site->blog_id} has {$count->publish} books" );

    restore_current_blog();
}
```

## 7. Best Practices

### Service-Oriented Architecture

```php
<?php
namespace MyPlugin\Services;

class BookService {

    private $cache;
    private $validator;

    public function __construct( CacheService $cache, ValidationService $validator ) {
        $this->cache = $cache;
        $this->validator = $validator;
    }

    public function get_book( $book_id ) {
        // Check cache first
        $cache_key = "book_{$book_id}";
        $book = $this->cache->get( $cache_key );

        if ( false === $book ) {
            $book = get_post( $book_id );

            if ( $book && 'book' === $book->post_type ) {
                $this->cache->set( $cache_key, $book, HOUR_IN_SECONDS );
            }
        }

        return $book;
    }

    public function create_book( $data ) {
        // Validate input
        $errors = $this->validator->validate_book_data( $data );
        if ( ! empty( $errors ) ) {
            return new \WP_Error( 'validation_failed', 'Validation failed', $errors );
        }

        // Create book
        $book_id = wp_insert_post([
            'post_type' => 'book',
            'post_title' => $data['title'],
            'post_content' => $data['content'],
            'post_status' => $data['status'],
        ]);

        if ( is_wp_error( $book_id ) ) {
            return $book_id;
        }

        // Clear related caches
        $this->cache->invalidate_group( 'books' );

        return $book_id;
    }
}

// Dependency injection container
class Container {
    private $services = [];

    public function register( $name, $service ) {
        $this->services[ $name ] = $service;
    }

    public function get( $name ) {
        if ( ! isset( $this->services[ $name ] ) ) {
            throw new \Exception( "Service not found: {$name}" );
        }

        return $this->services[ $name ];
    }
}

// Bootstrap
$container = new Container();
$container->register( 'cache', new CacheService() );
$container->register( 'validator', new ValidationService() );
$container->register( 'books', new BookService(
    $container->get( 'cache' ),
    $container->get( 'validator' )
) );
```

### Event-Driven Design

```php
// Fire custom events
do_action( 'myplugin_book_created', $book_id, $book_data );
do_action( 'myplugin_book_updated', $book_id, $old_data, $new_data );
do_action( 'myplugin_book_deleted', $book_id );

// Other plugins can listen
add_action( 'myplugin_book_created', function( $book_id, $book_data ) {
    // Send email notification
    // Update analytics
    // Sync to external service
}, 10, 2 );

// Use filters for modifiable data
$book_data = apply_filters( 'myplugin_before_book_save', $book_data, $book_id );
$notification_recipients = apply_filters( 'myplugin_notification_recipients', [ 'admin@example.com' ], $book_id );
```

### Scalability Considerations

```php
/**
 * Performance Checklist:
 *
 * 1. Database:
 *    - Use indexes on frequently queried columns
 *    - Avoid SELECT * queries (use specific fields)
 *    - Batch operations instead of loops
 *    - Use LIMIT for large datasets
 *
 * 2. Caching:
 *    - Implement object caching (Redis/Memcached)
 *    - Use transients for expensive operations
 *    - Fragment caching for HTML blocks
 *    - CDN for static assets
 *
 * 3. Queries:
 *    - Use 'fields' => 'ids' when possible
 *    - Set 'no_found_rows' => true if not paginating
 *    - Disable update_post_meta_cache and update_post_term_cache when not needed
 *
 * 4. Assets:
 *    - Minify and concatenate CSS/JS
 *    - Lazy load images
 *    - Use responsive images (srcset)
 *    - Defer non-critical JavaScript
 *
 * 5. Monitoring:
 *    - Use Query Monitor for development
 *    - New Relic or Application Insights for production
 *    - Monitor slow queries
 *    - Track cache hit rates
 */

// Example: Batch processing with WP-CLI
function process_books_batch() {
    $offset = 0;
    $batch_size = 100;

    do {
        $books = get_posts([
            'post_type' => 'book',
            'posts_per_page' => $batch_size,
            'offset' => $offset,
            'fields' => 'ids',
        ]);

        foreach ( $books as $book_id ) {
            // Process each book
            update_post_meta( $book_id, '_processed', time() );
        }

        $offset += $batch_size;

        // Prevent memory leaks
        wp_cache_flush();

    } while ( count( $books ) === $batch_size );
}
```

## Related Skills

When building advanced WordPress applications, consider these complementary skills (available in the skill library):

- **WordPress Plugin Fundamentals**: Core plugin architecture and hooks - essential foundation for custom REST endpoints and WP-CLI commands
- **WordPress Security & Data Validation**: Security best practices - critical for securing REST API endpoints and validating user input
- **WordPress Testing & QA**: Testing REST endpoints and WP-CLI - comprehensive testing strategies for advanced WordPress features
- **GraphQL**: Alternative to REST API - consider GraphQL as a modern alternative to WordPress REST API for complex data queries
- **Docker**: Development environment setup - containerize WordPress development for consistent and reproducible environments

## References

- [REST API Handbook](https://developer.wordpress.org/rest-api/) - Official REST API documentation
- [WP-CLI](https://wp-cli.org/) - Command-line interface for WordPress
- [Object Cache](https://developer.wordpress.org/reference/classes/wp_object_cache/) - WordPress object caching
- [Transients API](https://developer.wordpress.org/apis/transients/) - WordPress transients documentation
- [Query Monitor](https://querymonitor.com/) - Performance profiling plugin
- [Redis Object Cache](https://wordpress.org/plugins/redis-cache/) - Redis integration plugin
