---
name: sayt-code
description: >
  How to write .say.cue / .say.yaml — the ordered-map rule pattern, built-in
  generators (auto-gomplate, auto-cue), CUE basics.
  Use when setting up code generation rules, linting rules, or CUE-based configuration.
user-invocable: false
---

# generate / lint — CUE + gomplate Configuration

`sayt generate` runs code generation rules. `sayt lint` runs lightweight verification rules. Both are driven by configuration in `.say.{cue,yaml,toml,nu}` files.

## How It Works

1. sayt loads and merges all `.say.*` config files in the current directory
2. The merged config also includes sayt's built-in `config.cue` which provides default rules
3. For `generate`: executes each rule's `cmds` in order, passing them through nushell
4. For `lint`: executes each rule's `cmds`, which must produce no outputs (validation only)

### Config Loading Order

sayt finds files matching `.say.{cue,yaml,yml,json,toml,nu}` and merges them:
- `.say.nu` files are executed as nushell scripts (their output is piped to CUE)
- All other files are passed to `cue export` for unified evaluation
- sayt's own `config.cue` provides default schemas and built-in rules

## Configuration Schema

### `say.generate.rules`

Rules are defined via an ordered map (`rulemap`) that gets flattened to a list:

```yaml
say:
  generate:
    rulemap:
      my-rule:
        cmds:
          - do: "buf generate"
            outputs: ["gen/"]
```

Each rule has:
- **`cmds`** — Array of nushell command blocks
- **`cmds[].do`** — The nushell expression to run inside `do { ... }`
- **`cmds[].use`** (optional) — A nushell module to import before running
- **`cmds[].args`** (optional) — Additional arguments
- **`cmds[].outputs`** (optional) — Files/dirs the command produces
- **`cmds[].inputs`** (optional) — Files/dirs the command depends on

### `say.lint.rules`

Same structure as generate rules, but lint commands must not produce output files:

```yaml
say:
  lint:
    rulemap:
      check-formatting:
        cmds:
          - do: "prettier --check ."
```

### The Ordered Map Pattern (`#MapAsList`)

sayt uses an "ordered map" pattern for rules. Keys allow granular modification:

- **Add**: Introduce a new unique key
- **Modify**: Reference an existing key to merge/update fields
- **Delete**: Set an existing key to `null`
- **Order**: Control position via the optional `priority` field

```yaml
say:
  generate:
    rulemap:
      # Delete a built-in rule
      "auto-cue": null
      # Add a custom rule
      my-protobuf:
        priority: 10
        cmds:
          - do: "buf generate"
```

## Built-in Rules

### `auto-gomplate` (generate)

Finds `*.tmpl` files and processes them with gomplate, using CUE data:

```
*.tmpl → gomplate (with data from matching *.cue) → output file
```

For example: `Dockerfile.tmpl` + `Dockerfile.cue` → `Dockerfile`

### `auto-cue` (generate)

Finds `*.cue` files whose stem matches an existing file, then exports the CUE to overwrite that file:

```
compose.cue (if compose.yaml exists) → cue export → compose.yaml
```

### `auto-cue` (lint)

Validates that CUE-generated files match their CUE definitions:

```
compose.cue + compose.yaml → cue vet (must pass)
```

## CUE Basics for sayt Config

CUE is sayt's native configuration language. Key concepts:

```cue
package say

say: {
  generate: {
    rulemap: {
      "my-rule": {
        cmds: [{
          do: "echo hello"
        }]
      }
    }
  }
}
```

- CUE unifies values (merges rather than overwrites)
- Default values use `*value | type` syntax
- Null deletion works via the ordered map pattern

## `.say.yaml` Examples

**Disable built-in CUE generation:**
```yaml
say:
  generate:
    rulemap: { "auto-cue": null }
```

**Add a protobuf generation rule:**
```yaml
say:
  generate:
    rulemap:
      protobuf:
        cmds:
          - do: "buf generate ../../libraries/xproto"
            outputs: ["gen/"]
```

**Add a custom lint rule:**
```yaml
say:
  lint:
    rulemap:
      eslint:
        cmds:
          - do: "pnpm eslint ."
```

## `.say.cue` Examples

**Custom generate rule in CUE:**
```cue
package say

say: generate: rulemap: "generate-types": {
  cmds: [{
    do: "openapi-typescript api.yaml -o types.ts"
    outputs: ["types.ts"]
    inputs: ["api.yaml"]
  }]
}
```

**Using gomplate with custom data:**
```cue
package say

say: generate: rulemap: "render-config": {
  cmds: [{
    use: "./gomplate.nu"
    do:  "gomplate auto-gomplate | ignore"
  }]
}
```

## `.say.nu` for Dynamic Config

For configuration that needs runtime logic, use `.say.nu`:

```nushell
# .say.nu — Dynamic config generation
# Output YAML/JSON that gets merged with other .say.* files
{
  say: {
    generate: {
      rulemap: {
        dynamic-rule: {
          cmds: [{
            do: $"echo (date now | format date '%Y')"
          }]
        }
      }
    }
  }
} | to yaml
```

## The `--force` Flag

`sayt generate --force` sets `SAY_GENERATE_ARGS_FORCE=true` in the environment. Rules can check this to overwrite existing files:

```nushell
# In a rule's do block
save --force=($env.SAY_GENERATE_ARGS_FORCE? | default false) output.yaml
```

## Current flags

!`sayt help generate 2>&1 || true`
!`sayt help lint 2>&1 || true`
