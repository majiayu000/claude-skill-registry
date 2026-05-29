---
name: inclusive-language
description: Use when writing code, documentation, or comments - always use accessible and respectful terminology
allowed-tools: []
model: opus
---

# Inclusive Language

## Overview

Use respectful, accessible language in all code and documentation.

**Core principle:** Words matter. Use inclusive terminology.

**This applies to:** Code, comments, documentation, commit messages, branch names, and all text.

## Terminology Guide

### Branch Names

| Instead of | Use |
|------------|-----|
| master | main |
| slave | replica, secondary, follower |

```bash
# Correct
git checkout main
git push origin main

# Repository default branch should be 'main'
```

### Access Control

| Instead of | Use |
|------------|-----|
| whitelist | allowlist, permitlist |
| blacklist | denylist, blocklist |

```typescript
// Correct
const allowlist = ['admin@example.com', 'user@example.com'];
const denylist = ['spam@example.com'];

function isAllowed(email: string): boolean {
  return allowlist.includes(email) && !denylist.includes(email);
}
```

### Primary/Secondary

| Instead of | Use |
|------------|-----|
| master/slave | primary/replica, primary/secondary, leader/follower |
| master (device) | primary, controller, host |
| slave (device) | secondary, peripheral, client |

```typescript
// Correct
interface DatabaseConfig {
  primary: ConnectionString;
  replicas: ConnectionString[];
}

class ReplicationManager {
  private leader: Node;
  private followers: Node[];
}
```

### Gendered Terms

| Instead of | Use |
|------------|-----|
| man hours | person hours, work hours |
| manpower | workforce, staffing |
| mankind | humanity, people |
| guys | everyone, folks, team |
| he/she (generic) | they |

```typescript
// Correct
/**
 * When a user logs in, they receive a session token.
 * The user can then use their token to access resources.
 */
```

### Ability-Related

| Instead of | Use |
|------------|-----|
| sanity check | validity check, confidence check |
| crazy/insane | unexpected, surprising |
| blind (as negative) | unaware, unnoticed |
| cripple | disable, limit |
| dumb | silent, without output |

```typescript
// Correct
function validateInput(data: unknown): boolean {
  // Perform validity check on input data
}

// Instead of "sanity check"
function confidenceCheck(result: Result): boolean {
  // Verify result is within expected bounds
}
```

### Violence-Related

| Instead of | Use |
|------------|-----|
| kill | stop, terminate, end |
| abort | cancel, stop |
| hit | access, call, reach |
| execute | run, perform |
| nuke | delete, remove, clear |

```typescript
// Correct
function terminateProcess(pid: number): void { }
function stopServer(): void { }
function cancelRequest(id: string): void { }

// Acceptable (industry standard)
function executeQuery(sql: string): Result { }
```

### Other Terms

| Instead of | Use |
|------------|-----|
| dummy | placeholder, sample |
| native | built-in, core |
| first-class | built-in, fully-supported |
| grandfather/legacy | established, existing |
| grandfathered in | exempted, pre-existing |

## Examples in Context

### Configuration

```typescript
// Correct
interface FeatureFlags {
  allowlist: string[];
  denylist: string[];
}

const replicationConfig = {
  primary: 'db-primary.example.com',
  replicas: [
    'db-replica-1.example.com',
    'db-replica-2.example.com',
  ],
};
```

### Documentation

```markdown
<!-- Correct -->
# Getting Started

When a user creates an account, they will receive a confirmation email.
They can then set up their profile using their preferred settings.

## Access Control

Use the allowlist to specify approved domains.
Use the denylist to block specific addresses.
```

### Comments

```typescript
// Correct
// Validity check: ensure the input meets expected format
if (!isValidFormat(input)) {
  throw new ValidationError('Input format is invalid');
}

// Confidence check: verify result is within expected bounds
if (result > MAX_EXPECTED || result < MIN_EXPECTED) {
  logger.warn('Result outside expected range');
}
```

### Error Messages

```typescript
// Correct
throw new Error('Email address is on the denylist');
throw new Error('Origin not in allowlist');
throw new Error('Request terminated due to timeout');
```

## Applying to Existing Code

When modifying existing code with non-inclusive terms:

### Small Scope (Same File)

If you're modifying a function that uses non-inclusive language:

1. Rename the term as part of your change
2. Update related documentation
3. Note in commit message: "Renamed to inclusive terminology"

### Large Scope (Multiple Files)

If renaming would touch many files:

1. Create a separate issue for the terminology update
2. Complete current work with existing terms
3. Schedule terminology update as future work

### API/Public Interface

If the term is in a public API:

1. Document the plan for deprecation
2. Add deprecated alias with new term
3. Migrate users over time
4. Remove deprecated term in major version

```typescript
// Transition approach
/** @deprecated Use allowlist instead */
export const whitelist = allowlist;

export const allowlist: string[] = [];
```

## Commit Messages and Branch Names

```bash
# Branch names
feature/issue-123-add-denylist-support  # Correct
fix/issue-456-update-replica-config     # Correct

# Commit messages
"Add email denylist validation"         # Correct
"Update replica failover logic"         # Correct
```

## Checklist

When writing or reviewing code:

- [ ] No master/slave terminology
- [ ] No whitelist/blacklist terminology
- [ ] No gendered language for generic users
- [ ] No ability-related negative terms
- [ ] Documentation uses inclusive language
- [ ] Variable/function names are inclusive
- [ ] Error messages are inclusive
- [ ] Comments are inclusive

## Resources

- Google Developer Style Guide: https://developers.google.com/style/inclusive-documentation
- Inclusive Naming Initiative: https://inclusivenaming.org/

## Integration

This skill is applied by:
- `issue-driven-development` - Step 7
- `comprehensive-review` - Style criterion

This skill ensures:
- Welcoming codebase
- Professional standards
- Accessibility for all contributors
