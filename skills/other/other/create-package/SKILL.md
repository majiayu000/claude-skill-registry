---
name: create-package
description: Create a new monorepo package using the create-package CLI
---

# Create Package Skill

Use this skill when the user asks to create a new package in the monorepo.

## Overview

The `yarn create-package` command automates the creation of new monorepo packages by:

- Generating package scaffolding from the template package
- Setting up the package structure, configuration files, and dependencies
- Creating package.json with the provided name and description

## Required Arguments

- `--name` (or `-n`): The package name. Will be prefixed with "@ocap/" if not provided.
- `--description` (or `-d`): A short description of the package for package.json

## Usage Pattern

1. Ask the user for the package name and description if not provided
2. Run `yarn create-package --name <package-name> --description "<description>"`
3. Add any additional dependencies using `yarn workspace @ocap/<package-name> add <dep>`

## Example

```bash
# Create the package
yarn create-package --name my-package --description "A package for handling my feature"

# Add dependencies if needed
yarn workspace @ocap/my-package add some-dependency @ocap/kernel-agents
```

When adding monorepo dependencies like `@ocap/kernel-agents`, update the TypeScript references:

```jsonc
// packages/my-package/tsconfig.json and tsconfig.build.json
{
  "references": [{ "path": "../kernel-agents" }],
}
```

This creates a new package at `packages/my-package` with the name `@ocap/my-package`.

## Notes

- The package name will automatically be prefixed with "@ocap/" if not provided
- The created package is private by default
- The template is located at `packages/template-package/`
- All placeholder values in the template will be replaced with actual values
