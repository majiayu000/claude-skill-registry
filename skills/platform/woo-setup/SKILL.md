---
name: woo-setup
description: Install WooCommerce, configure the development stack, and set up a local dev environment with WP-CLI, Docker, or wp-env. Use when setting up a new WooCommerce project or development environment.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Installation & Environment Setup

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.woocommerce.com/docs/` for the getting started guide
2. Web-search `site:developer.wordpress.org cli commands` for WP-CLI reference
3. Web-search `woocommerce system requirements latest version` for current requirements

## System Requirements

### Minimum Stack

| Component | Requirement |
|-----------|-------------|
| PHP | 7.4+ (8.0–8.3 recommended) |
| MySQL | 8.0+ |
| MariaDB | 10.4+ |
| WordPress | 6.4+ |
| WooCommerce | 9.x (latest) |
| HTTPS | Required for payment gateways |
| max_execution_time | 120+ seconds |
| memory_limit | 256M+ |

### Recommended PHP Extensions

`curl`, `gd`, `intl`, `mbstring`, `openssl`, `xml`, `zip`, `sodium`, `imagick`

## Local Development Options

### wp-env (Official WordPress)

WordPress's official Docker-based local environment:
- `npm -g i @wordpress/env` then `wp-env start`
- Configured via `.wp-env.json` in project root
- Supports specifying WordPress version, plugins, themes, PHP version
- Includes WP-CLI access: `wp-env run cli wp <command>`

### Docker Compose

Custom Docker setup with `wordpress`, `mysql`/`mariadb`, optional `phpmyadmin`, `mailhog` containers. Mount plugin/theme directories into the WordPress container.

### Local by Flywheel / DDEV / Lando

GUI or CLI tools that provision WordPress-ready environments with configurable PHP, MySQL, and web server versions.

## WP-CLI Setup

### Essential WooCommerce Commands

- `wp plugin install woocommerce --activate` — install and activate
- `wp wc update` — run WooCommerce database migrations
- `wp wc setting list general` — view store settings
- `wp wc product list` — list products
- `wp wc order list` — list orders
- `wp wc tool run install_pages` — create default WooCommerce pages (shop, cart, checkout)

### Scaffold a WooCommerce Extension

- `wp scaffold plugin my-woo-extension` — generate boilerplate plugin
- Add WooCommerce headers: `WC requires at least`, `WC tested up to`

## Project Bootstrapping

### Recommended Plugin Structure

```
my-woo-extension/
├── my-woo-extension.php          # Main plugin file with headers
├── includes/                     # PHP classes
├── src/                          # Namespaced source (PSR-4 autoloaded)
├── assets/
│   ├── css/
│   └── js/
├── templates/                    # Overridable templates
├── languages/                    # i18n .pot/.po/.mo files
├── tests/                        # PHPUnit tests
├── composer.json                 # Dependencies + autoloading
├── package.json                  # JS build tooling (if blocks)
└── readme.txt                    # WordPress.org plugin header
```

### Main Plugin File Headers

Required headers for WooCommerce extensions:
- `Plugin Name`, `Plugin URI`, `Description`, `Version`, `Author`, `License`
- `WC requires at least: 8.0` — minimum WooCommerce version
- `WC tested up to: 9.5` — tested WooCommerce version
- `Requires Plugins: woocommerce` — WordPress 6.5+ dependency declaration

### HPOS Compatibility Declaration

Every new extension must declare HPOS compatibility:
```php
add_action( 'before_woocommerce_init', function() {
    if ( class_exists( \Automattic\WooCommerce\Utilities\FeaturesUtil::class ) ) {
        \Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility(
            'custom_order_tables', __FILE__, true
        );
    }
});
```

## Best Practices

- Always declare HPOS (`custom_order_tables`) compatibility in new extensions
- Use Composer autoloading (PSR-4) for namespaced classes
- Set `WC requires at least` and `WC tested up to` headers
- Use `wp-env` or Docker for reproducible development environments
- Run `wp wc tool run install_pages` after fresh WooCommerce install

Fetch the WooCommerce getting started guide and WP-CLI docs for exact commands and configuration options before setting up.
