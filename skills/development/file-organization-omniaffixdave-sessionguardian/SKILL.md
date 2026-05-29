---
name: file-organization
description: Group related files together by feature or module rather than by type Use when maintaining consistent code style. Style category skill.
metadata:
  category: Style
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_file_organization
---

# File Organization

Group related files together by feature or module rather than by type. Within files, order: imports, type definitions, constants, main exports, helper functions. Keep files focused—if a file grows beyond ~300-400 lines, consider splitting. Use index files to provide clean public APIs. Consistent organization helps developers navigate the codebase.