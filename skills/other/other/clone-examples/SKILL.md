---
name: compact-core:clone-examples
description: Use when starting a new Midnight project, cloning example contracts (counter, tokens, NFTs, DEX), scaffolding from OpenZeppelin templates, or bootstrapping a Compact contract development environment with working starter code.
---

# Clone Examples

> Catalog of cloneable Compact contract examples and starter projects

## Usage

### Listing Examples

Read `references/catalog.yaml` to browse available examples.
Filter by tags, source, or compatibility requirements.

### Cloning Examples

Always use shallow clone to minimize download size:

```bash
git clone --depth 1 <clone_url> <destination>
```

**Before cloning**: If the user hasn't specified a destination directory, ask where they'd like to clone the repository.

For examples where `path` is not `/`, guide the user to the specific file or directory after cloning.

### Compatibility Check

Before recommending an example, use `/midnight-tooling:midnight-compatibility` to verify the user's environment matches the example's `compatibility` requirements. Warn if versions differ or are incompatible.

## References

- [catalog.yaml](references/catalog.yaml) - Full example catalog
