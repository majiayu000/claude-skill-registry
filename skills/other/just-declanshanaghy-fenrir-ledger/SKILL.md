---
name: just
description: Use `just` to save and run project-specific commands. Use when the user mentions `justfile`, `recipe`, or needs a simple alternative to `make` for task automation.
attribution: Imported from https://github.com/disler/bowser — credit to @disler
---

# Just Command Runner

[GitHub Repository](https://github.com/casey/just)

`just` is a handy way to save and run project-specific commands. It's a command runner, not a build system, avoiding much of `make`'s complexity.

## Instructions

### Prerequisites

- `just` must be installed: `brew install just`
- Commands are stored in a `justfile` (or `Justfile`).

#### Common Settings (`set ...`)

You can configure `just` behavior at the top of your `justfile`:
- `set shell := ["bash", "-c"]`: Change the default shell.
- `set dotenv-load`: Automatically load `.env` files.
- `set allow-duplicate-recipes`: Allow overriding recipes.
- `set fallback`: Search for `justfile` in parent directories.
- `set quiet`: Don't echo commands by default.

## Example Justfiles

For complete reference, see these templates:
- [Node.js + Docker](examples/node-docker.just)
- [Python + Venv](examples/python-venv.just)
- [Bun + TypeScript](examples/bun-typescript.just)
- [Astral UV + Python](examples/uv-python.just)
- [Multi-Module / Advanced](examples/multi-module.just)

## Workflow

1. **Create a `justfile`**:
   Define recipes at the top level of your project. **Always include a `default` recipe that lists available commands:**
   ```just
   default:
     @just --list
   ```
   ```just
   # The default recipe (runs when calling `just` with no args)
   default:
     just --list

   # A basic recipe
   test:
     cargo test

   # A recipe with parameters
   build target:
     echo "Building {{target}}..."
     cc main.c -o {{target}}
   ```

2. **Run Recipes**:
   - Run the default recipe: `just`
   - Run a specific recipe: `just <recipe>`
   - Pass arguments to a recipe: `just build my-app`
   - List all available recipes: `just --list`

3. **Advanced Features**:
   - **Dependencies**: `test: build` (runs `build` before `test`).
   - **Shebang Recipes**: Use other languages like Python or Node inside a recipe.
     ```just
     python-task:
       #!/usr/bin/env python3
       print("Hello from Python!")
     ```
   - **Dotenv**: `set dotenv-load` at the top of the file to load `.env`.

## Examples

### Example 1: Standard Development Justfile

User request:
```
Create a justfile for my Node project to handle lint, test, and dev
```

You would:
1. Create a `justfile`:
   ```just
   default:
     @just --list

   lint:
     npm run lint

   test:
     npm test

   dev:
     npm run dev
   ```
2. Tell the user they can now run `just dev` or `just test`.

### Example 2: Recipe with Parameters

User request:
```
Add a recipe to just to deploy to a specific environment
```

You would:
1. Edit the `justfile`:
   ```just
   deploy env:
     echo "Deploying to {{env}}..."
     ./scripts/deploy.sh --target {{env}}
   ```
2. Inform the user they can run `just deploy production`.

### Example 3: Listing Recipes

User request:
```
What commands are available in this project?
```

You would:
1. Run `just --list` to see available recipes and their comments.
