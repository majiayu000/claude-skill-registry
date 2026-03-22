---
name: TypeScript Editing
description: Edit TypeScript/JavaScript files using ts-morph. Manage classes, methods, properties, and imports with structured output. Designed for LLM use.
allowed-tools:
  - Bash
  - Read
---

# TypeScript Editing

This skill provides scripts to read and modify TypeScript/JavaScript files using ts-morph. All modification scripts automatically format the output with Prettier.

## Requirements

Peer dependencies (must be installed in consuming project):
- `ts-morph` - AST manipulation
- `prettier` - Code formatting

## Available Scripts

### Code Structure

#### List Structure

View the complete structure of a TypeScript/JavaScript file:

```bash
.claude/skills/typescript-editing/scripts/list-structure.cjs <file-path>
```

**Output format:**
```
Imports (1-5)
  import { Component } from '@angular/core' (1)
  import { UserService } from './services/user.service' (2)

interface User (7-12)
  property id: string (8)
  property name: string (9)
  property email: string (10)

class UserService (14-80)
  property apiUrl: string (16)
  constructor(private http: HttpClient) (18-22)
  method getUser(id: string): Promise<User> (24-35)
  method updateUser(user: User): Promise<void> (37-50)

function createDefaultUser(): User (82-88)

type UserRole = 'admin' | 'user' (90)

enum Status (92-96)
  member Active (93)
  member Inactive (94)
```

### Import Management

**Note:** All add operations are idempotent - they skip if the import already exists.

#### List Imports

List all imports in a file:

```bash
.claude/skills/typescript-editing/scripts/list-imports.cjs <file-path>
```

**Output format:**
```
import { Component } from '@angular/core' (1)
import { UserService } from './services/user.service' (2)
import * as fs from 'fs' (3)
import express from 'express' (4)
```

#### Add Import

Add an import statement (creates new or adds to existing):

```bash
# Add named imports
.claude/skills/typescript-editing/scripts/add-import.cjs <file-path> <module-path> --named="Component,Injectable"

# Add default import
.claude/skills/typescript-editing/scripts/add-import.cjs <file-path> <module-path> --default="express"

# Add namespace import
.claude/skills/typescript-editing/scripts/add-import.cjs <file-path> <module-path> --namespace="fs"

# Add type-only import
.claude/skills/typescript-editing/scripts/add-import.cjs <file-path> <module-path> --named="User" --type-only
```

**Output:**
```
Added import at line 5
# OR
Added 'Injectable' to existing import at line 1
# OR
Import already exists (skipped)
```

#### Remove Import

Remove a specific import by module path or identifier:

```bash
# Remove entire import statement by module path
.claude/skills/typescript-editing/scripts/remove-import.cjs <file-path> <module-path>

# Remove specific named import
.claude/skills/typescript-editing/scripts/remove-import.cjs <file-path> <identifier>
```

**Output:** Confirmation with line number

#### Remove Unused Imports

Remove all unused imports from a file:

```bash
.claude/skills/typescript-editing/scripts/remove-unused-imports.cjs <file-path>
```

**Output:** List of removed imports with line numbers

### Class Management

#### Add Method

Add a method to a class:

```bash
# Basic method (placeholder body)
.claude/skills/typescript-editing/scripts/add-method.cjs <file-path> <class-name> <method-name>

# With inline body
.claude/skills/typescript-editing/scripts/add-method.cjs <file-path> <class-name> getData \
  --return-type="string" --body="return this.data;"

# With body from file (auto-deleted after use)
.claude/skills/typescript-editing/scripts/add-method.cjs <file-path> <class-name> fetchUser \
  --async --params="id: string" --return-type="Promise<User>" \
  --body-file=/tmp/method-body.js

# With visibility and modifiers
.claude/skills/typescript-editing/scripts/add-method.cjs <file-path> <class-name> <method-name> \
  --visibility=private \
  --static \
  --async
```

**Options:**
- `--visibility` - public (default), private, or protected
- `--static` - Make method static
- `--async` - Make method async
- `--params` - Parameter list (e.g., "id: string, options?: Options")
- `--return-type` - Return type annotation
- `--body` - Method body (inline)
- `--body-file` - Read body from file (auto-deleted)

**Output:** Line numbers of created method

#### Add Property

Add a property to a class:

```bash
# Basic property
.claude/skills/typescript-editing/scripts/add-property.cjs <file-path> <class-name> <property-name> --type="string"

# With visibility and modifiers
.claude/skills/typescript-editing/scripts/add-property.cjs <file-path> <class-name> <property-name> \
  --type="User[]" \
  --visibility=private \
  --readonly

# With initial value
.claude/skills/typescript-editing/scripts/add-property.cjs <file-path> <class-name> <property-name> \
  --type="string" \
  --initial-value="'default'"

# Static property
.claude/skills/typescript-editing/scripts/add-property.cjs <file-path> <class-name> <property-name> \
  --type="number" \
  --static \
  --initial-value="0"
```

**Options:**
- `--type` - Type annotation (required)
- `--visibility` - public (default), private, or protected
- `--readonly` - Make property readonly
- `--static` - Make property static
- `--initial-value` - Initial value expression

**Output:** Line number of created property

#### Remove Method

Remove a method from a class:

```bash
.claude/skills/typescript-editing/scripts/remove-method.cjs <file-path> <class-name> <method-name>
```

**Output:** Confirmation with line numbers removed

#### Remove Property

Remove a property from a class:

```bash
.claude/skills/typescript-editing/scripts/remove-property.cjs <file-path> <class-name> <property-name>
```

**Output:** Confirmation with line number removed

#### Replace Method

Replace an entire method (signature and body), preserving decorators:

```bash
# Replace with inline body
.claude/skills/typescript-editing/scripts/replace-method.cjs <file-path> <class-name> <method-name> \
  --params="id: string" \
  --return-type="Promise<User>" \
  --body="return this.http.get<User>(\`\${this.baseUrl}/users/\${id}\`).toPromise();" \
  --async

# Replace with body from file (auto-deleted after use)
.claude/skills/typescript-editing/scripts/replace-method.cjs <file-path> <class-name> <method-name> \
  --async --params="id: string" --return-type="Promise<User>" \
  --body-file=/tmp/method-body.js

# With visibility and modifiers
.claude/skills/typescript-editing/scripts/replace-method.cjs <file-path> <class-name> <method-name> \
  --visibility=private \
  --static \
  --params="data: any" \
  --body="console.log(data);"
```

**Options:**
- `--visibility` - public (default), private, or protected
- `--static` - Make method static
- `--async` - Make method async
- `--params` - Parameter list (e.g., "id: string, options?: Options")
- `--return-type` - Return type annotation
- `--body` - Method body (inline)
- `--body-file` - Read body from file (auto-deleted)

**Output:** Line numbers of replaced method

**Note:** Decorators on the original method are automatically preserved.

#### Add Constructor

Add or replace a constructor in a class:

```bash
# Basic constructor
.claude/skills/typescript-editing/scripts/add-constructor.cjs <file-path> <class-name>

# With parameters
.claude/skills/typescript-editing/scripts/add-constructor.cjs <file-path> <class-name> \
  --params="private apiUrl: string, private timeout: number"

# With inline body
.claude/skills/typescript-editing/scripts/add-constructor.cjs <file-path> <class-name> \
  --params="apiUrl: string" \
  --body="this.apiUrl = apiUrl; console.log('initialized');"

# With body from file (auto-deleted after use)
.claude/skills/typescript-editing/scripts/add-constructor.cjs <file-path> <class-name> \
  --params="config: Config" \
  --body-file=/tmp/ctor-body.js
```

**Options:**
- `--params` - Constructor parameters
- `--body` - Constructor body (inline)
- `--body-file` - Read body from file (auto-deleted)

**Output:** Line numbers of created/replaced constructor

#### Add Decorator

Add a decorator to a class, method, or property:

```bash
# Add to class
.claude/skills/typescript-editing/scripts/add-decorator.cjs <file-path> <class-name> <decorator-name>

# Add to method
.claude/skills/typescript-editing/scripts/add-decorator.cjs <file-path> <class-name> <decorator-name> \
  --target=method \
  --method-name="login"

# Add to property
.claude/skills/typescript-editing/scripts/add-decorator.cjs <file-path> <class-name> <decorator-name> \
  --target=property \
  --property-name="apiUrl"

# With arguments
.claude/skills/typescript-editing/scripts/add-decorator.cjs <file-path> <class-name> "Endpoint" \
  --target=method \
  --method-name="getUser" \
  --args="'/api/users'"
```

**Options:**
- `--target` - class (default), method, or property
- `--method-name` - Target method name (when target=method)
- `--property-name` - Target property name (when target=property)
- `--args` - Decorator arguments

**Output:** Confirmation of decorator added

#### Rename Member

Rename a class member (method or property):

```bash
.claude/skills/typescript-editing/scripts/rename-member.cjs <file-path> <class-name> <old-name> <new-name>
```

**Output:** Confirmation with line number

## Design Notes

- **LLM-optimized**: Structured, concise output designed for programmatic consumption
- **Auto-formatting**: All modifications run Prettier for consistent formatting
- **Line numbers**: All operations return line numbers for LLM reference
- **Idempotent imports**: Import operations skip if already present
- **Safe operations**: Scripts validate file structure before making changes

## Example Workflow

```bash
# 1. View file structure
.claude/skills/typescript-editing/scripts/list-structure.cjs src/services/user.service.ts

# 2. Add missing imports
.claude/skills/typescript-editing/scripts/add-import.cjs src/services/user.service.ts "@angular/core" --named="Injectable"
.claude/skills/typescript-editing/scripts/add-import.cjs src/services/user.service.ts "./models/user" --named="User"

# 3. Add decorator to class
.claude/skills/typescript-editing/scripts/add-decorator.cjs src/services/user.service.ts "UserService" "Injectable"

# 4. Add a method
.claude/skills/typescript-editing/scripts/add-method.cjs src/services/user.service.ts "UserService" "deleteUser" \
  --params="id: string" \
  --return-type="Promise<void>" \
  --visibility=public \
  --async

# 5. Add a property
.claude/skills/typescript-editing/scripts/add-property.cjs src/services/user.service.ts "UserService" "cache" \
  --type="Map<string, User>" \
  --visibility=private \
  --initial-value="new Map()"

# 6. Remove unused imports
.claude/skills/typescript-editing/scripts/remove-unused-imports.cjs src/services/user.service.ts
```

## Body File Pattern

For complex method bodies with template literals, await expressions, or multi-line logic:

1. Write the method body to a temp file (e.g., `/tmp/method-body.js`)
2. Call the script with `--body-file=/tmp/method-body.js`
3. The file is automatically deleted after reading

This avoids shell escaping issues and works well with LLM parallel tool calls (Write + Bash in same message).

## Notes

- Supports both TypeScript (.ts, .tsx) and JavaScript (.js, .jsx) files
- Preserves existing code formatting through Prettier integration
- All scripts exit with non-zero status on errors
- Works with Angular, React, Node.js, and other TypeScript/JavaScript projects
