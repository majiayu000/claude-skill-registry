---
name: debugging-atmos
description: >-
  Use when troubleshooting Atmos configuration, deployment errors, or unexpected behavior. Covers debug logging,
  describing stacks/components, interpreting errors, and common issues with stack resolution and Atmos functions.
---

# Debugging Atmos

Techniques for troubleshooting Atmos configuration and deployment issues.

## Quick Debugging Commands

```bash
# See the fully-resolved YAML for a component
atmos describe component <component> -s <stack>

# Enable verbose debug logging
ATMOS_LOGS_LEVEL=debug atmos terraform plan <component> -s <stack>

# Validate all stack configurations
atmos validate stacks

# Reset local state and cache
atmos terraform clean <component> -s <stack>
```

## Inspecting Resolved Configuration

The most powerful debugging tool is `atmos describe stacks`, which shows the final YAML after all imports, merges, and
inheritance:

```bash
# Describe all components in a stack (most useful for debugging)
atmos describe stacks -s plat-use2-dev

# Describe all stacks (very large output)
atmos describe stacks

# Describe a specific component in a stack
atmos describe component vpc -s plat-use2-dev
```

The output includes the fully-resolved configuration for each component:

- **vars** - All variables with their final values
- **settings** - Component settings
- **metadata** - Component metadata (type, inheritance chain)
- **backend** - Terraform backend configuration
- **env** - Environment variables

### What to Look For

1. **Variable values** - Are vars what you expect? Check inheritance from catalog vs stack overrides
2. **Component resolution** - Is `metadata.component` pointing to the right root module?
3. **Backend configuration** - Is the S3 bucket/DynamoDB table correct?
4. **Atmos function results** - Have `!terraform.state` expressions resolved?

### Filtering with yq

Use `yq` to filter the YAML output and extract specific information:

```bash
# Get vars for a specific component
atmos describe stacks -s plat-use2-dev | yq '.components.terraform.vpc.vars'

# Get all component names in a stack
atmos describe stacks -s plat-use2-dev | yq '.components.terraform | keys'

# Check a specific variable across components
atmos describe stacks -s plat-use2-dev | yq '.components.terraform.*.vars.enabled'

# Get backend config for a component
atmos describe stacks -s plat-use2-dev | yq '.components.terraform.vpc.backend'
```

### Disabling Templates and Functions

To debug configuration before template/function processing, disable them:

```bash
# See raw config before Go templates are processed
atmos describe stacks -s plat-use2-dev --process-templates=false

# See config before Atmos functions (!terraform.state, etc.) are evaluated
atmos describe stacks -s plat-use2-dev --process-functions=false

# See completely raw config (no templates or functions)
atmos describe stacks -s plat-use2-dev --process-templates=false --process-functions=false
```

**Use cases:**

- **Debugging templates** - See the raw `{{ }}` expressions before evaluation
- **Debugging functions** - See `!terraform.state` expressions before they resolve
- **Faster iteration** - Skip slow `!terraform.state` lookups when debugging other issues
- **No authentication needed** - Functions like `!terraform.state` require AWS access; disable to debug without auth

### When to Use Each Command

| Command                                        | Use When                                                         |
| ---------------------------------------------- | ---------------------------------------------------------------- |
| `atmos describe stacks -s <stack>`             | Debugging a stack - see all components and their resolved config |
| `atmos describe stacks -s <stack> \| yq '...'` | Extract specific values from a stack                             |
| `atmos describe stacks`                        | Understanding full infrastructure (large output)                 |
| `atmos describe component <comp> -s <stack>`   | Focused debugging of a single component                          |

## Debug Logging

Enable debug logging for detailed Atmos operations:

```bash
ATMOS_LOGS_LEVEL=debug atmos terraform plan <component> -s <stack>
```

Debug output includes:

- Stack file loading and import resolution
- Variable inheritance chain
- Atmos function evaluation (`!terraform.state`, etc.)
- Provider configuration
- Backend initialization

### Log Levels

- `info` (default) - Normal operation
- `debug` - Detailed debugging information
- `trace` - Maximum verbosity (rarely needed)

## Common Issues

### Stack Not Found

**Error:** `stack 'xyz' not found`

**Debug:**

```bash
# List available stacks
ls stacks/orgs/acme/

# Check stack file exists
cat stacks/orgs/acme/<tenant>/<stage>/<region>/<layer>.yaml
```

**Common causes:**

- Typo in stack name
- Stack file doesn't exist
- Stack name doesn't match naming convention (`{tenant}-{region}-{stage}`)

### Component Not Found

**Error:** `component 'xyz' not found in stack`

**Debug:**

```bash
# Check component exists in filesystem
ls components/terraform/

# Check component is configured in stack
atmos describe stacks -s <stack> | grep -A5 "xyz:"
```

**Common causes:**

- Component not imported in stack file
- Missing catalog import
- Component name mismatch between catalog and stack

### Atmos Function Errors

**Error:** `error evaluating !terraform.state: ...`

**Debug:**

```bash
# Check the function syntax in your YAML
grep -r "!terraform.state" stacks/catalog/<component>/

# Verify the source component exists and has outputs
atmos describe component <source-component> -s <stack>

# Check if the source component has been deployed
atmos terraform plan <source-component> -s <stack>
```

**Common causes:**

- Source component not deployed yet (no state)
- Wrong output name
- Wrong stack name in cross-stack lookups
- Circular dependency

For Atmos function syntax and patterns, see the `atmos-functions` skill.

### Provider/Authentication Errors

**Error:** `error configuring provider` or `AccessDenied`

**Debug:**

```bash
# Check authentication is working
atmos auth login --provider acme-sso

# Verify identity resolution
ATMOS_LOGS_LEVEL=debug atmos terraform plan <component> -s <stack> 2>&1 | grep -i identity
```

For authentication issues, see the `atmos-auth` skill.

### Variable Inheritance Issues

**Problem:** Variable has unexpected value

**Debug:**

```bash
# See the full resolved config
atmos describe component <component> -s <stack>

# Check catalog defaults
cat stacks/catalog/<component>/defaults.yaml

# Check stack overrides
cat stacks/orgs/acme/<tenant>/<stage>/<region>/<layer>.yaml
```

**Inheritance order (later wins):**

1. Component defaults (in Terraform `variables.tf`)
2. Catalog defaults (`stacks/catalog/<component>/defaults.yaml`)
3. Mixin imports (`stacks/mixins/`)
4. Stack defaults (`stacks/orgs/acme/<tenant>/<stage>/_defaults.yaml`)
5. Stack-specific config (`stacks/orgs/acme/<tenant>/<stage>/<region>/<layer>.yaml`)

### State/Cache Issues

**Problem:** Atmos behaving strangely, stale configuration

**Fix:**

```bash
# Clean local Terraform state and cache
atmos terraform clean <component> -s <stack>

# Then re-run
atmos terraform plan <component> -s <stack>
```

This removes:

- `.terraform/` directory
- Rendered configuration files
- Provider cache

Use when:

- Provider versions are out of sync
- Module cache is corrupted
- Configuration changes aren't being picked up

## Validation

Validate all stack configurations before deployment:

```bash
atmos validate stacks
```

This checks:

- YAML syntax
- Required fields
- Schema compliance
- Import resolution

## Debugging Workflow

1. **Start with describe stacks** - `atmos describe stacks -s <stack>` to see all resolved YAML
2. **Check the basics** - Stack exists? Component configured? Imports correct?
3. **Enable debug logging** - `ATMOS_LOGS_LEVEL=debug` for detailed output
4. **Clean and retry** - `atmos terraform clean` to reset state
5. **Check authentication** - See `atmos-auth` skill if AWS errors
6. **Check functions** - See `atmos-functions` skill if `!terraform.state` errors
