---
name: wp-playground
description: "Use for WordPress Playground workflows: fast disposable WP instances in browser or locally via @wp-playground/cli, auto-mounting plugins/themes, switching WP/PHP versions, blueprints, and debugging with Xdebug."
compatibility: "Playground CLI requires Node.js 20.18+. Runs WP in WebAssembly with SQLite."
---

# WordPress Playground

## When to use

- Spin up a disposable WordPress to test a plugin/theme without full stack setup
- Run or iterate on Playground Blueprints (JSON) locally
- Build a reproducible snapshot for sharing or CI
- Switch WP/PHP versions quickly to reproduce issues
- Debug plugin/theme code with Xdebug in isolation

## Inputs required

- Node.js 20.18+ (`node -v`)
- Project path to mount
- Desired WP version/PHP version (optional)
- Blueprint location if using one
- Port preference (default 9400)

## Procedure

### 1) Quick local spin-up

```bash
cd /path/to/your-plugin-or-theme
npx @wp-playground/cli@latest server --auto-mount
```

Opens on http://localhost:9400. Auto-detects and installs plugin/theme.

**Common options:**

```bash
# Specify WP version
npx @wp-playground/cli@latest server --auto-mount --wp=6.9

# Specify PHP version
npx @wp-playground/cli@latest server --auto-mount --php=8.2

# Change port
npx @wp-playground/cli@latest server --auto-mount --port=9500
```

### 2) Manual mounts

For complex setups:

```bash
npx @wp-playground/cli@latest server \
  --mount=/path/to/plugin:/wordpress/wp-content/plugins/my-plugin \
  --mount=/path/to/theme:/wordpress/wp-content/themes/my-theme
```

### 3) Run a Blueprint

Blueprints define site setup in JSON:

```bash
# Run from local file
npx @wp-playground/cli@latest run-blueprint --blueprint=./my-blueprint.json

# Run from URL
npx @wp-playground/cli@latest run-blueprint --blueprint=https://example.com/blueprint.json
```

**Example blueprint.json:**

```json
{
  "landingPage": "/wp-admin/",
  "preferredVersions": {
    "php": "8.2",
    "wp": "6.9"
  },
  "steps": [
    {
      "step": "login",
      "username": "admin",
      "password": "password"
    },
    {
      "step": "installPlugin",
      "pluginZipFile": {
        "resource": "url",
        "url": "https://downloads.wordpress.org/plugin/query-monitor.zip"
      }
    },
    {
      "step": "activatePlugin",
      "pluginPath": "query-monitor/query-monitor.php"
    }
  ]
}
```

### 4) Build a snapshot

Create shareable ZIP:

```bash
npx @wp-playground/cli@latest build-snapshot \
  --blueprint=./setup.json \
  --outfile=./my-site.zip
```

### 5) Debug with Xdebug

```bash
npx @wp-playground/cli@latest server --auto-mount --xdebug
```

Connect your IDE (VS Code/PhpStorm) to the port shown in output.

### 6) Browser-only workflows

No CLI needed:

- **Quick preview:** `https://playground.wordpress.net/`
- **With blueprint:** `https://playground.wordpress.net/?blueprint-url=YOUR_JSON_URL`
- **Blueprint editor:** Use the live editor at playground.wordpress.net

### 7) Version testing matrix

Test across versions:

```bash
# Test on WP 6.8
npx @wp-playground/cli@latest server --auto-mount --wp=6.8

# Test on WP 6.9
npx @wp-playground/cli@latest server --auto-mount --wp=6.9

# Test on PHP 8.1
npx @wp-playground/cli@latest server --auto-mount --php=8.1
```

## Verification

- Plugin/theme appears in admin and is active
- For blueprints: re-run with `--verbosity=debug` to confirm steps executed
- Test the specific functionality you're debugging

## Failure modes / debugging

**CLI exits complaining about Node:**
- Upgrade to Node.js 20.18+

**Mount not applied:**
- Use absolute paths
- Add `--verbosity=debug`

**Blueprint cannot read local assets:**
- Add `--blueprint-may-read-adjacent-files`

**Port already used:**
- Change with `--port=9500`

**Slow/locked UI:**
- Try disabling or enabling `--experimental-multi-worker`

## Limitations

Playground uses WebAssembly + SQLite, so:
- No MySQL (uses SQLite)
- Some PHP extensions may not work
- Not suitable for production data

## Escalation

If PHP extensions or native DB access are required:
- Fall back to wp-env, Docker, or Local

Consult:
- [WordPress Playground Docs](https://wordpress.github.io/wordpress-playground/)
- [Playground GitHub](https://github.com/WordPress/wordpress-playground)
