---
name: discrepancies
description: View and manage code-to-spec discrepancies. Detects API changes, function signature mismatches, and documentation gaps. Supports brownfield analysis and code-spec comparison.
---

# Discrepancies Command

View and manage documentation discrepancies. Supports two modes:
1. **Code-to-Spec**: Real-time discrepancies between code and specs
2. **Brownfield**: Documentation gaps detected by brownfield analysis

## Usage

```bash
# Brownfield discrepancies (documentation gaps)
/sw:discrepancies                  # List pending brownfield discrepancies
/sw:discrepancies --module payment # Filter by module name
/sw:discrepancies --type missing-docs    # Filter by type
/sw:discrepancies --priority critical    # Filter by priority
/sw:discrepancies show DISC-0001   # View details
/sw:discrepancies ignore DISC-0001 "False positive"  # Ignore with reason

# Code-to-spec discrepancies (legacy)
/sw:discrepancies --check          # Run code-spec check now
/sw:discrepancies --severity major # Filter by severity
```

## Arguments

**Brownfield mode (default)**:
- `--module <name>`: Filter by module name (e.g., "payment-service")
- `--type <type>`: Filter by type: `missing-docs`, `stale-docs`, `knowledge-gap`, `orphan-doc`, `missing-adr`
- `--priority <level>`: Filter by priority: `critical`, `high`, `medium`, `low`
- `--status <status>`: Filter by status: `pending`, `in-progress`, `resolved`, `ignored`

**Code-to-spec mode**:
- `--check`: Run discrepancy detection now
- `--severity <level>`: Filter by severity: `trivial`, `minor`, `major`, `breaking`

**Common**:
- `--json`: Output as JSON for scripting

## Subcommands

### list (default)

Lists detected discrepancies with severity, type, and description.

```
🔍 DETECTED DISCREPANCIES (5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISC-0001   ❌ BREAKING   api-route          POST /api/users removed
DISC-0002   ⚠️ MAJOR      function-signature  getUserById params changed
DISC-0003   ⚠️ MINOR      api-route          GET /api/orders path changed
DISC-0004   ✅ TRIVIAL    type-definition    User type updated
DISC-0005   ⚠️ MAJOR      api-route          New DELETE /api/users/:id

Use '/sw:discrepancies show <id>' to view details
Use '/sw:discrepancies accept <id>' to apply patch
```

### show <id>

Shows full discrepancy details with recommended action and patch.

```
🔍 DISCREPANCY DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID:          DISC-0002
Type:        function-signature
Category:    modified
Severity:    ⚠️ major
Risk:        medium

Spec Value:  getUserById(id: string): User
Code Value:  getUserById(id: string, options?: Options): User | null

Spec File:   docs/api.md:45
Code File:   src/services/user.ts:123

Description: Function signature has changed from documented version.
             Code is the source of truth - specs should be updated.

Recommended: 👀 review-required
Patch Available: Yes

Use '/sw:discrepancies accept DISC-0002' to apply patch
Use '/sw:discrepancies dismiss DISC-0002' to mark intentional
```

### check

Run discrepancy detection immediately.

```
🔍 Running discrepancy check...

Analyzing:
  ✓ TypeScript functions: 156 exported
  ✓ Type definitions: 89 exported
  ✓ API routes: 34 detected

Comparing against specs:
  ✓ Parsed 12 spec files

Results:
  Found 5 discrepancies
  - Breaking: 1
  - Major: 2
  - Minor: 1
  - Trivial: 1

Use '/sw:discrepancies' to view list
```

### accept <id>

Apply the recommended patch to update specs.

```
🔧 Applying patch for DISC-0002...

File:    docs/api.md
Line:    45
Change:  getUserById(id: string): User
      →  getUserById(id: string, options?: Options): User | null

✅ Patch applied successfully
Remaining: 4 discrepancies
```

### dismiss <id>

Mark a discrepancy as intentional (won't be flagged again).

```
✅ Dismissed DISC-0002 (marked as intentional)
Remaining: 4 discrepancies
```

## Related

- `/sw:sync-monitor`: Dashboard showing discrepancy count
- `/sw:notifications`: View discrepancy notifications
