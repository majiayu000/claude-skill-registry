---
name: deno
description: Deno 2 development workflow including testing with permissions and JSR package management. Use when working with Deno projects, setting up new Deno applications, or when the user mentions Deno, JSR, or modern JavaScript/TypeScript development.
---

# Deno Development

## Version Requirements
- Always use Deno 2

## Testing
- Use `deno test -P` for running tests with permissions granted
- The `-P` flag allows permissions described in `deno.json` during testing.
- Define test permissions in the `test` section of `deno.json`.

## Package Management
- Use JSR (JavaScript Registry) for package dependencies https://jsr.io/
- JSR is the modern package registry for JavaScript and TypeScript

## Common Commands

### Adding Dependencies
```bash
# Add from JSR
deno add jsr:@std/log
deno add jsr:@std/path

# Add from npm (when necessary)
deno add npm:express
```

### Running Tests
```bash
# Run all tests with permissions
deno test -P

# Run specific test file
deno test -P test/example.test.ts
```

### Running Applications
```bash
# Run with limited permissions - AVOID -A unless absolutely necessary
deno run --allow-read=. main.ts
deno run --allow-net --allow-read=./public server.ts
deno run --allow-env --allow-read=. config.ts

# for `export default { fetch }`
deno serve serve.ts

# Use permission sets from deno.json
deno run -P main.ts
```

## Configuration with deno.json

### Permission Sets
Define permission sets in deno.json for consistent security:

```json
{
  "permissions": {
    "default": {
      "read": ["."],
      "env": {
        "allow": ["NODE_ENV", "PORT"],
        "deny": ["SECRET_KEY"],
        "ignore": ["TEMP_*"]
      }
    },
    "server": {
      "read": ["./public"],
      "net": ["localhost:8000", "deno.land"],
      "env": {
        "allow": ["DATABASE_URL", "API_KEY"]
      }
    }
  }
}
```

### Test Permissions
Configure test permissions in deno.json:

```json
{
  "test": {
    "permissions": {
      "read": ["."],
      "net": true
    }
  }
}
```

## Best Practices
- NEVER use `-A` (all permissions) unless absolutely necessary
- Always use the most restrictive permissions possible
- Use `--allow-read=.` instead of `--allow-read` to limit to current directory
- Use permission sets in deno.json for consistent security
- Define test permissions in deno.json under the `test` section
- Use `env.allow`, `env.deny`, and `env.ignore` for fine-grained environment variable control (`read.ignore` also available)
- Do not use `import` statements with full URLs for external dependencies. Instead, use `deno add` first.
- Leverage Deno's built-in security features
- Use JSR for package discovery and management
