---
name: monorepo-structure
description: Monorepo structure and package organization
---

# Repository Structure Rules

## Monorepo Organization

This is a monorepo for API client modules.

### Module Structure
```
package/
└── {vendor}/
    └── {module}/
        ├── api.yml
        ├── connectionProfile.yml
        ├── connectionState.yml
        ├── src/
        ├── test/
        └── package.json
```

### Types Repository (Optional)
- **Location**: `/types/` submodule
- **Contents**:
  - `types-core` - Core definitions
  - `types-{vendor}` - Vendor types
  - `types-core-{lang}` - Language-specific core
  - `types-{vendor}-{lang}` - Language-specific vendor

## File Paths

- Always use absolute paths
- Get root with `pwd` command
- Never use relative imports across modules
- Respect module boundaries

## Dependencies

- Each module is independent
- Share only through types repository
- No cross-module imports
- Version everything properly
