---
name: firestore-security-rules-generation
description: |
  Firestore Security Rules patterns for user-scoped access, RBAC with custom claims, multi-tenant isolation,
  field validation, immutable fields, and testing strategies. Includes rules syntax and best practices.
  Keywords: "security rules", "rbac", "multi-tenant", "validation", "firestore rules", "access control"
---

# Firestore Security Rules Generation

## Overview

Firestore Security Rules define who can access what data and under what conditions. Rules are enforced at the database level, providing a critical security layer.

## Rules Syntax Fundamentals

### Basic Structure

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Rules go here
  }
}
```

### Match Patterns

```
// Exact match
match /users/alice { }

// Wildcard (single document)
match /users/{userId} { }

// Recursive wildcard (all documents in subcollections)
match /users/{userId}/{document=**} { }
```

### Allow Operations

```
allow read;    // get() and list() operations
allow write;   // create(), update(), delete() operations

// Or be specific:
allow get;     // Read single document
allow list;    // Query/list documents
allow create;  // Create document
allow update;  // Update document
allow delete;  // Delete document
```

## Authentication Patterns

### User-Scoped Access

**Pattern**: Users can only access their own data

```
match /users/{userId} {
  allow read, write: if request.auth.uid == userId;
}

match /profiles/{profileId} {
  allow read: if true; // Public read
  allow write: if request.auth.uid == resource.data.ownerId;
}
```

### Authenticated Only

```
match /posts/{postId} {
  allow read: if request.auth != null;
  allow create: if request.auth != null;
}
```

### Public Read, Authenticated Write

```
match /posts/{postId} {
  allow read: if true; // Anyone can read
  allow create: if request.auth != null; // Must be logged in to create
  allow update, delete: if request.auth.uid == resource.data.authorId;
}
```

## Role-Based Access Control (RBAC)

### Custom Claims Pattern

**Set Claims** (Server-Side):
```typescript
await adminAuth.setCustomUserClaims(uid, { role: 'admin' });
```

**Rules**:
```
// Helper functions
function isAuthenticated() {
  return request.auth != null;
}

function hasRole(role) {
  return isAuthenticated() && request.auth.token.role == role;
}

function isAdmin() {
  return hasRole('admin');
}

// Admin-only collection
match /admin-data/{document} {
  allow read, write: if isAdmin();
}

// Role-based read access
match /posts/{postId} {
  allow read: if resource.data.visibility == 'public'
              || isAdmin()
              || hasRole('moderator');
}
```

### Multi-Role Rules

```
function hasAnyRole(roles) {
  return isAuthenticated() && request.auth.token.role in roles;
}

match /moderation/{docId} {
  allow read, write: if hasAnyRole(['admin', 'moderator']);
}
```

## Multi-Tenant Security

### Pattern 1: Tenant ID in Document

**Data Structure**:
```typescript
{
  id: "post1",
  tenantId: "tenant_abc",
  content: "...",
}
```

**Set Tenant Claim** (Server-Side):
```typescript
await adminAuth.setCustomUserClaims(uid, { tenantId: 'tenant_abc' });
```

**Rules**:
```
function belongsToTenant(tenantId) {
  return isAuthenticated() && request.auth.token.tenantId == tenantId;
}

match /posts/{postId} {
  allow read, write: if belongsToTenant(resource.data.tenantId);
}

// For creates (resource.data doesn't exist yet)
match /posts/{postId} {
  allow create: if isAuthenticated()
                && request.resource.data.tenantId == request.auth.token.tenantId;
}
```

### Pattern 2: Subcollection Per Tenant

```
tenants/tenant_abc/posts/post1
tenants/tenant_abc/users/user1
```

**Rules**:
```
match /tenants/{tenantId}/{document=**} {
  allow read, write: if request.auth.token.tenantId == tenantId;
}
```

## Field Validation

### Required Fields

```
function hasRequiredFields(fields) {
  return request.resource.data.keys().hasAll(fields);
}

match /posts/{postId} {
  allow create: if hasRequiredFields(['title', 'content', 'authorId', 'createdAt']);
}
```

### Data Type Validation

```
match /posts/{postId} {
  allow create: if request.resource.data.title is string
                && request.resource.data.title.size() > 0
                && request.resource.data.title.size() <= 200
                && request.resource.data.viewCount is int
                && request.resource.data.viewCount >= 0;
}
```

### Enum Validation

```
match /posts/{postId} {
  allow create, update: if request.resource.data.status in ['draft', 'published', 'archived'];
}
```

### Immutable Fields

```
function isImmutable(field) {
  return request.resource.data[field] == resource.data[field];
}

match /posts/{postId} {
  allow update: if isImmutable('authorId')
                && isImmutable('createdAt');
}
```

### Field Length Limits

```
match /posts/{postId} {
  allow create: if request.resource.data.title.size() >= 1
                && request.resource.data.title.size() <= 200
                && request.resource.data.content.size() >= 10
                && request.resource.data.content.size() <= 10000;
}
```

## Relationship Validation

### Reference Exists

```
match /comments/{commentId} {
  allow create: if exists(/databases/$(database)/documents/posts/$(request.resource.data.postId));
}
```

### Parent-Child Relationship

```
match /posts/{postId}/comments/{commentId} {
  allow read: if exists(/databases/$(database)/documents/posts/$(postId));
  allow create: if request.auth != null
                && exists(/databases/$(database)/documents/posts/$(postId));
}
```

## Advanced Patterns

### Conditional Access Based on Document State

```
match /posts/{postId} {
  // Anyone can read published posts
  allow read: if resource.data.status == 'published';

  // Author can read their own posts (any status)
  allow read: if request.auth.uid == resource.data.authorId;

  // Admins can read all
  allow read: if isAdmin();
}
```

### Rate Limiting (Approximate)

```
match /posts/{postId} {
  allow create: if request.auth != null
                && request.time < resource.data.lastPostTime + duration.value(1, 'm'); // 1 minute cooldown
}
```

**Note**: Firestore rules don't have built-in rate limiting. Use Cloud Functions for accurate rate limiting.

### Soft Delete Pattern

```
match /posts/{postId} {
  // Prevent actual deletion
  allow delete: if false;

  // Only allow marking as deleted
  allow update: if request.auth.uid == resource.data.authorId
                && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['deletedAt']);
}
```

## Complete Example

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // ========================================================================
    // HELPER FUNCTIONS
    // ========================================================================

    function isAuthenticated() {
      return request.auth != null;
    }

    function isOwner(userId) {
      return isAuthenticated() && request.auth.uid == userId;
    }

    function hasRole(role) {
      return isAuthenticated() && request.auth.token.role == role;
    }

    function isAdmin() {
      return hasRole('admin');
    }

    function hasRequiredFields(fields) {
      return request.resource.data.keys().hasAll(fields);
    }

    function isImmutable(field) {
      return request.resource.data[field] == resource.data[field];
    }

    // ========================================================================
    // USERS COLLECTION
    // ========================================================================

    match /users/{userId} {
      allow read: if isOwner(userId) || isAdmin();
      allow create: if isOwner(userId)
                    && hasRequiredFields(['email', 'displayName', 'createdAt']);
      allow update: if isOwner(userId)
                    && isImmutable('createdAt')
                    && (!('role' in request.resource.data) || isImmutable('role'));
      allow delete: if isAdmin();
    }

    // ========================================================================
    // POSTS COLLECTION
    // ========================================================================

    match /posts/{postId} {
      allow read: if resource.data.status == 'published'
                  || isOwner(resource.data.authorId)
                  || isAdmin();

      allow create: if isAuthenticated()
                    && request.resource.data.authorId == request.auth.uid
                    && hasRequiredFields(['title', 'content', 'authorId', 'status', 'createdAt'])
                    && request.resource.data.status in ['draft', 'published', 'archived']
                    && request.resource.data.title is string
                    && request.resource.data.title.size() > 0
                    && request.resource.data.title.size() <= 200;

      allow update: if (isOwner(resource.data.authorId) || isAdmin())
                    && isImmutable('authorId')
                    && isImmutable('createdAt');

      allow delete: if isOwner(resource.data.authorId) || isAdmin();
    }

    // ========================================================================
    // COMMENTS COLLECTION
    // ========================================================================

    match /comments/{commentId} {
      allow read: if true;

      allow create: if isAuthenticated()
                    && request.resource.data.authorId == request.auth.uid
                    && exists(/databases/$(database)/documents/posts/$(request.resource.data.postId))
                    && request.resource.data.content.size() > 0
                    && request.resource.data.content.size() <= 1000;

      allow update: if isOwner(resource.data.authorId)
                    && isImmutable('authorId')
                    && isImmutable('postId');

      allow delete: if isOwner(resource.data.authorId) || isAdmin();
    }
  }
}
```

## Testing Rules

### Local Testing with Emulator

```typescript
// firestore.rules.spec.ts
import { assertFails, assertSucceeds } from '@firebase/rules-unit-testing';
import { initializeTestEnvironment } from '@firebase/rules-unit-testing';

let testEnv;

beforeAll(async () => {
  testEnv = await initializeTestEnvironment({
    projectId: 'test-project',
    firestore: {
      rules: fs.readFileSync('firestore.rules', 'utf8'),
    },
  });
});

test('User can read their own profile', async () => {
  const alice = testEnv.authenticatedContext('alice');
  await assertSucceeds(alice.firestore().collection('users').doc('alice').get());
});

test('User cannot read other profiles', async () => {
  const alice = testEnv.authenticatedContext('alice');
  await assertFails(alice.firestore().collection('users').doc('bob').get());
});
```

## Deployment

```bash
# Deploy rules only
firebase deploy --only firestore:rules

# Validate rules before deploying
firebase firestore:rules:release
```

## Best Practices

✅ **Do**:
- Default deny, explicitly allow
- Validate all user input (types, sizes, ranges)
- Use helper functions for reusable logic
- Test rules locally before deploying
- Document complex rules with comments
- Use custom claims for RBAC (not Firestore lookups)
- Enforce immutable fields (createdAt, authorId)

❌ **Don't**:
- Use `allow read, write: if true` in production (except truly public data)
- Perform Firestore lookups in rules (slow, limited to 10 per request)
- Store sensitive data in custom claims (1000 byte limit)
- Skip field validation
- Forget to handle create vs update differences
- Use rules for rate limiting (use Cloud Functions)

## Common Pitfalls

**Issue**: `resource.data` is `null` on `create`
**Solution**: Use `request.resource.data` for creates

**Issue**: "Property is undefined" error
**Solution**: Check field exists first: `'field' in resource.data`

**Issue**: Rules too slow
**Solution**: Avoid `exists()` and `get()` calls, use custom claims instead

---

**Related Skills**: `firebase-authentication-patterns`, `firebase-admin-sdk-server-integration`
**Token Estimate**: ~1,400 tokens
