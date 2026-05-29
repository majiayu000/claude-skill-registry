---
name: structure-check
description: Use when validating project structure during Standards Audit phase. Detects package type from package.json metasaver.projectType, loads structure rules from domain skills (react-app-structure, prisma-database, contracts-package), scans created/modified files, and reports violations with fix suggestions. File types: .tsx, .ts, directory layouts.
---

# Structure Check Skill

**Purpose:** Validate files are in correct locations per MetaSaver domain patterns.

**Input:** List of created/modified file paths
**Output:** Violations report with fix suggestions

---

## Workflow

1. Read `package.json` → extract `metasaver.projectType`
2. Map package type → structure rules (see tables below)
3. Scan file paths → check against rules
4. Report violations → with suggested fixes
5. Return verdict: PASS/FAIL

**Output format:**

```
STRUCTURE AUDIT: {package-name}
Package Type: {type}

✅ PASS: {count} files OK
❌ VIOLATIONS: {count} files

VIOLATION: {file-path}
  Rule: {description}
  Fix: {suggested-action}

VERDICT: PASS|FAIL
```

---

## Package Type Detection

```typescript
const projectType =
  JSON.parse(readFile("package.json")).metasaver?.projectType || "unknown";
```

| Type             | Domain Skill        | Skip if unknown |
| ---------------- | ------------------- | --------------- |
| `web-standalone` | react-app-structure | -               |
| `database`       | prisma-database     | -               |
| `contracts`      | contracts-package   | -               |
| `unknown`        | (no validation)     | ✅              |

---

## Structure Rules by Package Type

### React App (`web-standalone`)

**Allowed locations:**

| Path            | Content                    | Forbidden                      |
| --------------- | -------------------------- | ------------------------------ |
| `src/features/` | Components, hooks, queries | -                              |
| `src/pages/`    | Thin wrappers (5-15 lines) | Business logic                 |
| `src/config/`   | Config (auth, site, menu)  | -                              |
| `src/lib/`      | API client, utilities      | Auth config                    |
| `src/types/`    | **NOT ALLOWED**            | All types (use contracts)      |
| `src/assets/`   | Logo, icons                | -                              |
| `public/`       | Favicon only               | Logos (belongs in src/assets/) |

**Common violations:**

| Pattern                  | Fix                                          |
| ------------------------ | -------------------------------------------- |
| `src/pages/*/Form.tsx`   | Move to `src/features/{domain}/components/`  |
| `src/types/*.ts`         | Delete, import from `@metasaver/*-contracts` |
| `src/lib/auth-config.ts` | Move to `src/config/auth-config.ts`          |

---

### Database (`database`)

**Allowed files:**

| Path                   | Required | Forbidden              |
| ---------------------- | -------- | ---------------------- |
| `prisma/schema.prisma` | ✅       | -                      |
| `prisma/seed/`         | ✅       | -                      |
| `src/index.ts`         | ✅       | -                      |
| `src/client.ts`        | ✅       | -                      |
| `src/types.ts`         | ✅       | -                      |
| `src/{other}.ts`       | ❌       | No extra files allowed |

**Common violations:**

| Pattern            | Fix                                |
| ------------------ | ---------------------------------- |
| `src/utils/*.ts`   | Move to external utilities package |
| `src/helpers/*.ts` | Move to external utilities package |
| `prisma/types.ts`  | Move to `src/types.ts`             |

---

### Contracts (`contracts`)

**Allowed structure:**

| Path                         | Required | Forbidden          |
| ---------------------------- | -------- | ------------------ |
| `src/index.ts`               | ✅       | -                  |
| `src/shared/`                | Optional | -                  |
| `src/{entity}/index.ts`      | ✅       | -                  |
| `src/{entity}/types.ts`      | ✅       | -                  |
| `src/{entity}/validation.ts` | ✅       | -                  |
| `src/{entity}/{other}.ts`    | ❌       | Only 3 files above |

**Common violations:**

| Pattern                 | Fix                       |
| ----------------------- | ------------------------- |
| `src/{entity}/utils.ts` | Move to utilities package |
| `src/common/*.ts`       | Move to `src/shared/`     |

---

## Edge Cases

**No package.json:**

```
⚠️ WARNING: No package.json found
   Recommendation: Add package.json with metasaver.projectType
```

**Unknown package type:**

```
⚠️ SKIP: No structure validation rules
   Recommendation: Add metasaver.projectType to package.json
```

**No violations:**

```
✅ PASS: All {count} files in correct locations
VERDICT: PASS
```

---

## Examples

### Example 1: React App Violations

```
Input: ["src/pages/UserForm.tsx", "src/types/user.ts"]

STRUCTURE AUDIT: admin-portal
Package Type: web-standalone

❌ VIOLATIONS: 2 files

VIOLATION: src/pages/UserForm.tsx
  Rule: React UI components belong in /features/{feature}/components/
  Fix: Move to src/features/users/components/UserForm.tsx

VIOLATION: src/types/user.ts
  Rule: Types come from contracts packages, not src/types/
  Fix: Delete file, import from @metasaver/admin-contracts

VERDICT: FAIL (2 violations)
```

### Example 2: Database (Pass)

```
Input: ["src/index.ts", "src/client.ts", "src/types.ts"]

STRUCTURE AUDIT: rugby-crm-database
Package Type: database

✅ PASS: All 3 files in correct locations
VERDICT: PASS
```

### Example 3: Contracts Violation

```
Input: ["src/user/types.ts", "src/user/utils.ts"]

STRUCTURE AUDIT: rugby-crm-contracts
Package Type: contracts

❌ VIOLATIONS: 1 file

VIOLATION: src/user/utils.ts
  Rule: Entity folders may only contain types.ts, validation.ts, index.ts
  Fix: Move to separate utilities package or delete if unused

VERDICT: FAIL (1 violation)
```
