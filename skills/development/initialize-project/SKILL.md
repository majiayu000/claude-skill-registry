---
name: initialize-project
description: Initialize a new project from the TypeScript template by renaming packages, updating metadata, and cleaning up documentation. Use when starting a new project, "bootstrapping" from this template, or setting up a fresh repository.
---

# Initialize Project

## Purpose

This skill automates the initial setup of a new project derived from this template. It leverages AI capabilities to directly modify project metadata and documentation by replacing placeholders, ensuring a clean start for a new repository.

## Instructions

1. **Gather Information**: Ask the user for:
   - New project name (e.g., `my-awesome-app`)
   - Project description
   - Author name
   - (Optional) GitHub repository URL
2. **Update Project Metadata**: Directly update the following files using the `Write` or `StrReplace` tools:
   - `package.json`: Update `name`, `description`, and `author`.
   - `packages/common/package.json`: Update the package name to match the new scope (e.g., `@new-name/common`).
   - `.trunk/trunk.yaml`: If there are template-specific references, update them.
3. **Update README Placeholders**: Use the `StrReplace` tool to replace the placeholders in `README.md` with the gathered information:
   - `{PROJECT_NAME}` -> New project name
   - `{PROJECT_DESCRIPTION}` -> Project description
   - `{LICENSE}` -> `ISC` (or other preferred license)
4. **Install Dependencies**: Run `pnpm install` to update the lockfile with the new package names.
5. **Final Cleanup**: Remove the initialization skill and its related files once bootstrapping is complete, if requested by the user.

## Examples

### Example 1: Initializing a new CLI tool

**Input**: User says "Initialize this project as 'json-fixer', a CLI tool to fix broken JSON files."
**Action**:

1. Gather details from the user (Name: json-fixer, Description: A CLI tool to fix broken JSON files, Author: [Author Name]).
2. Update `package.json` with the new metadata.
3. Use `StrReplace` on `README.md` to swap `{PROJECT_NAME}`, `{PROJECT_DESCRIPTION}`, and `{LICENSE}` with the actual values.
4. Run `pnpm install`.
