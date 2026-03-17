---
name: firebase-security
description: Firebase security rules patterns for Firestore and Storage. Use when writing or reviewing security rules.
license: MIT
---

# Firebase Security Rules

## When to Use

Activate when:

- Writing Firestore or Storage security rules
- Reviewing access control patterns
- Fixing permission denied errors
- Adding new collections or storage paths

## Project Files

| File              | Purpose                                      |
| ----------------- | -------------------------------------------- |
| `firestore.rules` | Firestore security rules                     |
| `storage.rules`   | Storage security rules (CREATE IF MISSING)   |
| `firebase.json`   | Firebase config (must reference rules files) |

## Firestore Rules Patterns

### Admin Check (Custom Claims)

```javascript
function isDisruptiveAdmin() {
  return (
    request.auth != null &&
    request.auth.token.groups != null &&
    request.auth.token.groups.hasAny(['disruptiveAdmin'])
  );
}
```

### Space Ownership (Custom Claims)

```javascript
function isSpaceOwner(spaceId) {
  return (
    request.auth != null &&
    request.auth.token.groups != null &&
    request.auth.token.groups.hasAny(['space_' + spaceId + '_owners'])
  );
}

function isSpaceHost(spaceId) {
  return (
    request.auth != null &&
    request.auth.token.groups != null &&
    request.auth.token.groups.hasAny(['space_' + spaceId + '_hosts'])
  );
}
```

### User Profile Pattern

```javascript
match /users/{userId} {
  // Individual profile reads (social features)
  allow get: if true;

  // Own profile read/write
  allow read, write: if request.auth != null && request.auth.uid == userId;

  // Authenticated user lists (with limit)
  allow list: if request.auth != null && request.query.limit <= 100;

  // Private subcollection
  match /private/{doc} {
    allow read, write: if request.auth != null && request.auth.uid == userId;
  }
}
```

### Space Access Pattern

```javascript
match /spaces/{spaceId} {
  // Public or explicitly accessible
  allow read: if !('isPublic' in resource.data) ||
                 resource.data.isPublic == true ||
                 resource.data.allowGuestUsers == true ||
                 (request.auth != null && isSpaceOwnerOrHost(spaceId));

  // Owner/admin write
  allow write: if isSpaceOwner(spaceId) || isDisruptiveAdmin();

  // Subcollections inherit space context
  match /chatMessages/{msgId} {
    allow read: if request.auth != null;
    allow create: if request.auth != null && request.resource.data.uid == request.auth.uid;
    allow update, delete: if request.auth != null &&
                            (resource.data.uid == request.auth.uid || isSpaceOwnerOrHost(spaceId));
  }
}
```

## Storage Rules Template

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Default avatars - public read only
    match /avatars/defaults/{fileName} {
      allow read: if true;
      allow write: if false;
    }

    // User avatars - owner write, public read
    match /avatars/{userId}/{fileName} {
      allow read: if true;
      allow write: if request.auth != null
                   && request.auth.uid == userId
                   && request.resource.size < 10 * 1024 * 1024
                   && request.resource.contentType.matches('model/gltf-binary');
    }
  }
}
```

## Security Checklist

### Before Production

- [ ] Remove any testing bypasses (search for `TESTING MODE`)
- [ ] Verify all callable functions check ownership
- [ ] Create `storage.rules` if using Storage
- [ ] Add `storage` section to `firebase.json`
- [ ] Test rules with Firebase emulator

### Common Vulnerabilities

| Issue                    | Fix                                                  |
| ------------------------ | ---------------------------------------------------- |
| No ownership check       | Add `isSpaceOwner()` or `request.auth.uid == userId` |
| Unlimited list queries   | Add `request.query.limit <= 100`                     |
| Error message leak       | Return generic errors to client                      |
| Testing bypasses in prod | Remove all `if (groupName === 'users') return true`  |

## Testing Rules

```bash
# Start emulator
firebase emulators:start --only firestore,storage

# Deploy rules only
firebase deploy --only firestore:rules,storage:rules
```

## Related Files

- `packages/shared/firebase/userPermissions.ts` - Client-side permission checks
- `packages/shared/firebase/firebaseStorage.js` - Storage operations
- `functions/src/analytics.js` - Needs ownership verification
