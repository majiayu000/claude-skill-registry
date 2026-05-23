---
name: import-formatter
description: Format and organize import statements in code files. Use when imports are messy, unordered, or need to follow project conventions. Automatically groups imports by type (standard library, third-party, local) and sorts them alphabetically.
---

# Import Formatter Skill

## Instructions

1. Identify all import statements in the file
2. Group imports into three categories:
   - Standard library imports (Python stdlib, Node.js built-ins, etc.)
   - Third-party imports (from npm, pip, etc.)
   - Local/project imports (relative or absolute project paths)
3. Sort each group alphabetically
4. Add blank lines between groups (standard library, third-party, local)
5. Remove duplicate imports
6. Consolidate imports from the same module when possible
6. Preserve import aliases and type-only imports
7. Follow language-specific conventions (e.g., Python PEP 8, JavaScript ES6 modules)

## Examples

**Input (Python):**
```python
from typing import List, Dict
import os
from myapp.models import User
import requests
from typing import Optional
from myapp.utils import helper
```

**Output:**
```python
import os
from typing import Dict, List, Optional

import requests

from myapp.models import User
from myapp.utils import helper
```

**Input (JavaScript/TypeScript):**
```javascript
import { useState } from 'react'
import './styles.css'
import axios from 'axios'
import { Component } from './Component'
import { useEffect } from 'react'
```

**Output:**
```javascript
import { useEffect, useState } from 'react'

import axios from 'axios'

import { Component } from './Component'
import './styles.css'
```

## Language-Specific Rules

**Python:**
- Standard library first
- Third-party packages second
- Local imports last
- Use absolute imports when possible
- Group by package, then alphabetically

**JavaScript/TypeScript:**
- External packages first (node_modules)
- Internal modules second
- Relative imports last
- Side-effect imports (CSS, etc.) at the end
