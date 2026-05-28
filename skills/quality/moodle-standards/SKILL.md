---
name: moodle-coding-standards
description: Moodle coding standards with PSR-12 compliance and Frankenstyle naming. Use when developing Moodle plugins, writing PHP code for Moodle, or ensuring code quality compliance.
---

# Moodle Coding Standards

Write compliant Moodle plugin code following PSR-12 and Moodle-specific conventions.

## When to Use This Skill

- Creating new Moodle plugins
- Writing PHP code for Moodle
- Code review and quality checks
- Understanding Frankenstyle naming

See [reference.md](reference.md) for complete standards.

## Key Rules

### Frankenstyle Naming
```
plugintype_pluginname
local_mymodule
mod_assignment
block_myblock
```

### File Headers
```php
<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software...

namespace local_mymodule;

defined('MOODLE_INTERNAL') || die();
```

### Class Naming
```php
// Class in local/mymodule/classes/helper.php
namespace local_mymodule;
class helper {
    // Methods use snake_case
    public function get_user_data() {
    }
}
```

## Quick Checks

- [ ] File header with license
- [ ] `defined('MOODLE_INTERNAL') || die();`
- [ ] Proper namespace
- [ ] PSR-12 formatting
- [ ] No direct DB queries (use DML)
