---
name: scope-enforcement
description: |
  Scope enforcement system for Claude Code workflow in this application.
  Covers scope.json configuration, path validation, violation handling, and scope change workflow.
  Use this skill when validating file modifications against session scope.
allowed-tools: Read, Glob, Grep, Bash
version: 1.0.0
---

# Scope Enforcement Skill

Patterns for enforcing session scope in Claude Code development sessions.

## Architecture Overview

```
SCOPE ENFORCEMENT SYSTEM:

Scope Configuration:
.claude/sessions/{session-name}/scope.json
├── scope.core     # boolean - Core/app/scripts/migrations access
├── scope.theme    # string|false - Theme name or disabled
├── scope.plugins  # array|false - Plugin names or disabled
└── exceptions     # array - Override paths

Path Mapping:
scope.core = true  → core/**/* + app/**/* + scripts/**/* + migrations/**/*
scope.theme = "x"  → contents/themes/x/**/*
scope.plugins = [] → contents/plugins/{name}/**/*

Always Allowed:
.claude/sessions/**/*  # Session files always accessible

Validation Flow:
1. Read scope.json from session
2. Build allowed paths list
3. Check modified files against scope
4. If violation → BLOCK until resolved
5. If compliant → PROCEED

Integration Points:
├── code-reviewer (Layer 0 check)
├── /task:scope-change (scope modification)
├── product-manager (scope definition)
└── All development agents (scope respect)
```

## When to Use This Skill

- Validating file modifications against scope
- Understanding scope.json format
- Handling scope violations
- Requesting scope changes
- Implementing scope checks in agents

## scope.json Format

### Template Structure

```json
{
  "$schema": "Session Scope Configuration",
  "definedBy": "product-manager",
  "date": "YYYY-MM-DD",
  "scope": {
    "core": false,
    "theme": "theme-name",
    "plugins": false
  },
  "exceptions": [],
  "confirmedBy": "user",
  "confirmedAt": "YYYY-MM-DD"
}
```

### Scope Fields

| Field | Type | Description |
|-------|------|-------------|
| `scope.core` | `boolean` | Access to core/, app/, scripts/, migrations/ |
| `scope.theme` | `string\|false` | Theme name or disabled |
| `scope.plugins` | `array\|false` | Array of plugin names or disabled |
| `exceptions` | `array` | Specific paths to allow/deny |

### Path Mapping

```typescript
// scope.core = true
const corePaths = [
  'core/**/*',
  'app/**/*',
  'scripts/**/*',
  'migrations/**/*'
]

// scope.theme = "default"
const themePaths = [
  'contents/themes/default/**/*'
]

// scope.plugins = ["analytics", "payment"]
const pluginPaths = [
  'contents/plugins/analytics/**/*',
  'contents/plugins/payment/**/*'
]

// Always allowed
const alwaysAllowed = [
  '.claude/sessions/**/*'
]
```

## Common Scope Patterns

### 1. Feature in Existing Theme

Most common: Adding a feature to an existing theme.

```json
{
  "scope": {
    "core": false,
    "theme": "default",
    "plugins": false
  },
  "exceptions": []
}
```

**Allowed paths:**
- `.claude/sessions/**/*`
- `contents/themes/default/**/*`

### 2. Core Framework Change

Modifying core framework, migrations, or app routes.

```json
{
  "scope": {
    "core": true,
    "theme": false,
    "plugins": false
  },
  "exceptions": []
}
```

**Allowed paths:**
- `.claude/sessions/**/*`
- `core/**/*`
- `app/**/*`
- `scripts/**/*`
- `migrations/**/*`

### 3. Core + Theme Development

Full feature requiring both core changes and theme UI.

```json
{
  "scope": {
    "core": true,
    "theme": "default",
    "plugins": false
  },
  "exceptions": []
}
```

**Allowed paths:**
- `.claude/sessions/**/*`
- `core/**/*`
- `app/**/*`
- `scripts/**/*`
- `migrations/**/*`
- `contents/themes/default/**/*`

### 4. Plugin Development

Creating or modifying a specific plugin.

```json
{
  "scope": {
    "core": false,
    "theme": "plugin-sandbox",
    "plugins": ["my-plugin"]
  },
  "exceptions": []
}
```

**Allowed paths:**
- `.claude/sessions/**/*`
- `contents/themes/plugin-sandbox/**/*`
- `contents/plugins/my-plugin/**/*`

### 5. Full Access (Rare)

Maximum access for complex multi-area features.

```json
{
  "scope": {
    "core": true,
    "theme": "default",
    "plugins": ["analytics", "payment"]
  },
  "exceptions": []
}
```

### 6. Theme + Plugins (No Core)

Theme feature that uses plugins but doesn't modify core.

```json
{
  "scope": {
    "core": false,
    "theme": "default",
    "plugins": ["ai", "social-media-publisher"]
  },
  "exceptions": []
}
```

## Scope Validation Algorithm

```typescript
function validateScope(
  modifiedFiles: string[],
  scopeConfig: ScopeConfig
): ValidationResult {
  // Build allowed paths
  const allowedPaths: string[] = ['.claude/sessions/**/*']

  if (scopeConfig.scope.core) {
    allowedPaths.push(
      'core/**/*',
      'app/**/*',
      'scripts/**/*',
      'migrations/**/*'
    )
  }

  if (scopeConfig.scope.theme) {
    allowedPaths.push(
      `contents/themes/${scopeConfig.scope.theme}/**/*`
    )
  }

  if (Array.isArray(scopeConfig.scope.plugins)) {
    scopeConfig.scope.plugins.forEach(plugin => {
      allowedPaths.push(`contents/plugins/${plugin}/**/*`)
    })
  }

  // Add exceptions
  allowedPaths.push(...(scopeConfig.exceptions || []))

  // Check each file
  const violations: string[] = []

  for (const file of modifiedFiles) {
    const isAllowed = allowedPaths.some(pattern =>
      matchGlob(file, pattern)
    )

    if (!isAllowed) {
      violations.push(file)
    }
  }

  return {
    valid: violations.length === 0,
    violations,
    allowedPaths
  }
}
```

## code-reviewer Layer 0 Check

The code-reviewer agent performs scope validation as "Layer 0":

```typescript
// Layer 0: Session Scope Compliance (FIRST CHECK)

// 1. Read scope.json from session folder
const sessionPath = getSessionPathFromTaskContext()
const scopeConfig = JSON.parse(await Read(`${sessionPath}/scope.json`))

// 2. Build allowed paths
const allowedPaths = buildAllowedPaths(scopeConfig)

// 3. Check all modified files
const changedFiles = await getChangedFilesFromBranch()
const violations = []

for (const file of changedFiles) {
  const isAllowed = allowedPaths.some(pattern =>
    matchesGlob(file, pattern)
  )
  if (!isAllowed) {
    violations.push(file)
  }
}

// 4. If violations found, REJECT immediately
if (violations.length > 0) {
  console.log(`
🚨 SCOPE VIOLATION DETECTED 🚨

Session: ${sessionPath}
Scope Configuration:
- Core: ${scopeConfig.scope.core ? 'ALLOWED' : 'DENIED'}
- Theme: ${scopeConfig.scope.theme || 'NONE'}
- Plugins: ${JSON.stringify(scopeConfig.scope.plugins) || 'NONE'}

Files Outside Scope:
${violations.map(f => '- ' + f).join('\n')}

Required Action:
1. Revert modifications to files outside scope
2. OR request scope expansion via /task:scope-change
3. OR move logic to an allowed path

Review BLOCKED until scope violations are resolved.
  `)
  throw new Error('SCOPE_VIOLATION')
}
```

## Handling Scope Violations

### Option 1: Revert Changes

Remove modifications to files outside scope.

```bash
# Revert specific file
git checkout HEAD -- path/to/file

# Revert all out-of-scope changes
git checkout HEAD -- core/  # if core not allowed
```

### Option 2: Request Scope Change

Use `/task:scope-change` to expand scope.

```markdown
/task:scope-change .claude/sessions/2025-12-30-my-feature-v1/

I need to also modify:
- core/lib/services/my-service.ts (new service)
- migrations/020_new_table.sql (database change)

Reason: The feature requires core service layer changes
```

### Option 3: Move Logic

Refactor to place logic in allowed paths.

```typescript
// Instead of modifying core/lib/utils.ts
// Create theme-specific utility:
// contents/themes/default/lib/utils/my-utility.ts
```

## /task:scope-change Workflow

When scope needs to change mid-development:

```
1. Verify session has started development
2. Read ALL session files
3. Analyze scope change request vs progress
4. Identify rework implications
5. Ask user to confirm rework
6. Launch PM agent to update requirements
7. Launch Architect to update plan
8. Update progress.md with rework markers
9. Trigger code review if needed
```

### Scope Change Request Format

```markdown
/task:scope-change .claude/sessions/{session-name}/

Requested changes:
- Add core access for [reason]
- Add plugin "x" for [reason]

Impact analysis:
- Current progress: [phase X]
- Affected items: [list]
```

## Exceptions Usage

Exceptions allow specific paths regardless of scope rules:

```json
{
  "scope": {
    "core": false,
    "theme": "default",
    "plugins": false
  },
  "exceptions": [
    "core/lib/constants.ts",
    "app/api/v1/custom-endpoint/**/*"
  ]
}
```

**Use exceptions for:**
- Single files that need modification
- Specific endpoints outside normal scope
- Configuration files

**Avoid exceptions for:**
- Broad access (use scope.core instead)
- Multiple related files (expand scope)

## Scope Validation Script

```bash
# Validate files against session scope
python .claude/skills/scope-enforcement/scripts/validate-scope.py \
  --session ".claude/sessions/2025-12-30-feature-v1" \
  --files "core/lib/services/x.ts,contents/themes/default/lib/y.ts"
```

## Why Scope Enforcement Matters

1. **Prevents Accidental Modifications**
   - Core framework stays stable
   - Theme isolation maintained
   - Plugin boundaries respected

2. **Architectural Integrity**
   - Clear separation of concerns
   - Predictable code organization
   - Easier maintenance

3. **Multi-Theme/Plugin Safety**
   - Changes don't leak across themes
   - Plugins remain independent
   - No cross-contamination

4. **Future Updates**
   - Core updates can apply cleanly
   - Theme upgrades isolated
   - Plugin updates predictable

## Development Types

Scope is typically set based on development type:

| Development Type | core | theme | plugins |
|-----------------|------|-------|---------|
| Theme Feature | false | "name" | false |
| Core Feature | true | false | false |
| Core + Theme | true | "name" | false |
| Plugin Only | false | "sandbox" | ["name"] |
| Full Feature | true | "name" | [...] |

## Best Practices

### DO:
- Define scope at session start (product-manager)
- Validate scope before development begins
- Use smallest scope necessary
- Request scope change via official command
- Document scope decisions in context.md

### DON'T:
- Modify files outside scope
- Bypass scope validation
- Add exceptions for broad access
- Ignore scope violations
- Change scope.json directly (use /task:scope-change)

## Anti-Patterns

```typescript
// NEVER: Modify scope.json directly
fs.writeFileSync('scope.json', newScope)  // Use /task:scope-change

// NEVER: Ignore scope violations
if (scopeViolation) {
  continue  // WRONG - Must resolve violations
}

// NEVER: Use exceptions for broad access
{
  "exceptions": ["core/**/*"]  // WRONG - Use scope.core = true
}

// NEVER: Modify files then check scope
await modifyFile('core/lib/x.ts')  // Check BEFORE modifying
validateScope()

// NEVER: Skip scope check in code-reviewer
// Layer 0 is MANDATORY and FIRST
```

## Checklist

Before starting session development:

- [ ] scope.json exists in session folder
- [ ] scope.json has been reviewed
- [ ] User confirmed scope settings
- [ ] Allowed paths cover all planned modifications

During development:

- [ ] Verify file is in scope BEFORE modifying
- [ ] If out of scope, request change first
- [ ] Document scope decisions in context.md

If scope violation detected:

- [ ] STOP current work
- [ ] Identify all out-of-scope files
- [ ] Choose resolution (revert/change/move)
- [ ] Resolve BEFORE continuing

## Related Skills

- `session-management` - Session file structure including scope.json
- `plugins` - Plugin scope patterns
- `registry-system` - Registry paths and scope
- `documentation` - Scope documentation patterns
