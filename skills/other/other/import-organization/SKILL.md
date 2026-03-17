---
name: import-organization
description: "Order imports by: built-in modules, external packages, internal modules, relative imports Use when maintaining consistent code style. Style category skill."
metadata:
  category: Style
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_import_organization
---

# Import Organization

Order imports by: built-in modules, external packages, internal modules, relative imports. Separate groups with blank lines. Alphabetize within groups. Prefer named imports over default imports for better refactoring. Use absolute imports for cross-module references, relative for within modules. Configure ESLint/Prettier to enforce import ordering automatically.