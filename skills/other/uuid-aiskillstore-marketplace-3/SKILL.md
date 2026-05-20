---
name: uuid
description: 'UUID generation skill - Universally Unique Identifiers v4 and v7 for entity IDs. For ng-events construction site progress tracking system.'
---

# UUID - Universally Unique Identifiers

Trigger patterns: "UUID", "unique ID", "identifier", "v4", "v7", "uuidv4", "uuidv7"

## Overview

UUID library for generating RFC9562-compliant unique identifiers in JavaScript/TypeScript applications.

**Package**: uuid@13.0.0  
**Standard**: RFC9562 (formerly RFC4122)

## Core Functions

### 1. v4() - Random UUID (Most Common)

Generates a version 4 UUID using cryptographically secure random values.

```typescript
import { v4 as uuidv4 } from 'uuid';

// Generate random UUID
const taskId = uuidv4();
// '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d'

// Use in entity creation
interface Task {
  id: string;
  title: string;
  createdAt: Date;
}

function createTask(title: string): Task {
  return {
    id: uuidv4(),
    title,
    createdAt: new Date()
  };
}
```

**When to use**:
- Entity IDs (tasks, users, blueprints)
- Session IDs
- Request tracking IDs
- File upload IDs
- Any unique identifier needs

### 2. v7() - Timestamp-based UUID (Sortable)

Generates a version 7 UUID with Unix epoch timestamp for natural chronological sorting.

```typescript
import { v7 as uuidv7 } from 'uuid';

// Generate timestamp-based UUID
const orderId = uuidv7();
// '019a26ab-9a66-71a9-a89e-63c35fce4a5a'

// Multiple UUIDs are naturally sortable
const ids = Array.from({ length: 5 }, () => uuidv7());
// All IDs will be in chronological order

// Use for database primary keys
interface Order {
  id: string; // v7 UUID - sortable by creation time
  customerId: string;
  createdAt: Date;
}
```

**When to use**:
- Database primary keys requiring chronological sorting
- Event IDs in time-series data
- Log entry IDs
- Audit trail records
- Any scenario where temporal ordering matters

**Advantages**:
- Natural sort order by creation time
- Better database index performance
- Reduced fragmentation in B-tree indexes
- Compatible with UUID v4 in storage/APIs

## Real-World Examples

### Task Repository with UUID

```typescript
import { Injectable, inject } from '@angular/core';
import { Firestore, collection, doc, setDoc, getDoc } from '@angular/fire/firestore';
import { v4 as uuidv4 } from 'uuid';

export interface Task {
  id: string;
  blueprintId: string;
  title: string;
  description: string;
  status: 'pending' | 'in-progress' | 'completed';
  createdAt: Date;
  updatedAt: Date;
}

@Injectable({ providedIn: 'root' })
export class TaskRepository {
  private firestore = inject(Firestore);
  private tasksCollection = collection(this.firestore, 'tasks');
  
  /**
   * Create task with UUID v4
   */
  async create(task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>): Promise<Task> {
    const id = uuidv4(); // Generate unique ID
    const now = new Date();
    
    const newTask: Task = {
      ...task,
      id,
      createdAt: now,
      updatedAt: now
    };
    
    const docRef = doc(this.tasksCollection, id);
    await setDoc(docRef, newTask);
    
    return newTask;
  }
  
  /**
   * Get task by UUID
   */
  async findById(id: string): Promise<Task | null> {
    const docRef = doc(this.tasksCollection, id);
    const snapshot = await getDoc(docRef);
    
    if (!snapshot.exists()) {
      return null;
    }
    
    return { id: snapshot.id, ...snapshot.data() } as Task;
  }
}
```

### Audit Log with UUID v7

```typescript
import { Injectable, inject } from '@angular/core';
import { Firestore, collection, doc, setDoc } from '@angular/fire/firestore';
import { v7 as uuidv7 } from 'uuid';

export interface AuditLog {
  id: string; // v7 UUID for chronological sorting
  userId: string;
  action: string;
  resource: string;
  resourceId: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

@Injectable({ providedIn: 'root' })
export class AuditLogRepository {
  private firestore = inject(Firestore);
  private logsCollection = collection(this.firestore, 'auditLogs');
  
  /**
   * Create audit log with v7 UUID (sortable by time)
   */
  async log(
    userId: string,
    action: string,
    resource: string,
    resourceId: string,
    metadata?: Record<string, any>
  ): Promise<AuditLog> {
    const id = uuidv7(); // Timestamp-based UUID
    
    const log: AuditLog = {
      id,
      userId,
      action,
      resource,
      resourceId,
      timestamp: new Date(),
      metadata
    };
    
    const docRef = doc(this.logsCollection, id);
    await setDoc(docRef, log);
    
    return log;
  }
}
```

### Session Management

```typescript
import { Injectable } from '@angular/core';
import { v4 as uuidv4 } from 'uuid';

export interface Session {
  id: string;
  userId: string;
  token: string;
  createdAt: Date;
  expiresAt: Date;
}

@Injectable({ providedIn: 'root' })
export class SessionService {
  private sessions = new Map<string, Session>();
  
  /**
   * Create new session with UUID
   */
  createSession(userId: string, expiresInMs: number = 3600000): Session {
    const sessionId = uuidv4();
    const now = new Date();
    
    const session: Session = {
      id: sessionId,
      userId,
      token: this.generateToken(),
      createdAt: now,
      expiresAt: new Date(now.getTime() + expiresInMs)
    };
    
    this.sessions.set(sessionId, session);
    return session;
  }
  
  /**
   * Get session by ID
   */
  getSession(sessionId: string): Session | null {
    return this.sessions.get(sessionId) || null;
  }
  
  private generateToken(): string {
    return uuidv4(); // Use UUID as token
  }
}
```

### File Upload Tracking

```typescript
import { Injectable, signal } from '@angular/core';
import { v4 as uuidv4 } from 'uuid';

export interface FileUpload {
  id: string;
  fileName: string;
  fileSize: number;
  uploadedBy: string;
  uploadedAt: Date;
  status: 'pending' | 'uploading' | 'completed' | 'failed';
  progress: number;
  url?: string;
}

@Injectable({ providedIn: 'root' })
export class FileUploadService {
  private uploads = signal<Map<string, FileUpload>>(new Map());
  
  /**
   * Start file upload with UUID tracking
   */
  startUpload(file: File, userId: string): string {
    const uploadId = uuidv4();
    
    const upload: FileUpload = {
      id: uploadId,
      fileName: file.name,
      fileSize: file.size,
      uploadedBy: userId,
      uploadedAt: new Date(),
      status: 'pending',
      progress: 0
    };
    
    this.uploads.update(map => {
      map.set(uploadId, upload);
      return new Map(map);
    });
    
    return uploadId;
  }
  
  /**
   * Update upload progress
   */
  updateProgress(uploadId: string, progress: number): void {
    this.uploads.update(map => {
      const upload = map.get(uploadId);
      if (upload) {
        upload.progress = progress;
        upload.status = progress === 100 ? 'completed' : 'uploading';
        map.set(uploadId, upload);
      }
      return new Map(map);
    });
  }
  
  /**
   * Get upload by ID
   */
  getUpload(uploadId: string): FileUpload | undefined {
    return this.uploads().get(uploadId);
  }
}
```

## Best Practices

### 1. v4 for General Use, v7 for Time-Series

✅ **DO**: Choose based on use case
```typescript
// General entity IDs - use v4
const taskId = uuidv4();
const userId = uuidv4();

// Time-series or sortable IDs - use v7
const logId = uuidv7();
const eventId = uuidv7();
```

### 2. Use TypeScript Types

✅ **DO**: Define UUID brand types for safety
```typescript
type UUID = string & { readonly __brand: unique symbol };

interface Task {
  id: UUID;
  title: string;
}

function createTaskId(): UUID {
  return uuidv4() as UUID;
}
```

### 3. Validate UUIDs

✅ **DO**: Validate UUID format
```typescript
import { validate as uuidValidate, version as uuidVersion } from 'uuid';

function isValidUUID(id: string): boolean {
  return uuidValidate(id);
}

function isV4UUID(id: string): boolean {
  return uuidValidate(id) && uuidVersion(id) === 4;
}

function isV7UUID(id: string): boolean {
  return uuidValidate(id) && uuidVersion(id) === 7;
}
```

### 4. Don't Store UUIDs as Binary (Firestore)

✅ **DO**: Store as string in Firestore
```typescript
// Firestore automatically indexes string IDs
await setDoc(doc(collection, taskId), { /* data */ });
```

❌ **DON'T**: Convert to binary in Firestore
```typescript
// Unnecessary complexity in Firestore
const binaryId = Buffer.from(taskId.replace(/-/g, ''), 'hex');
```

## Performance Considerations

1. **Generation Speed**: v4 is slightly faster than v7
2. **Index Performance**: v7 provides better database index locality
3. **Storage**: Both require 36 bytes as string (128-bit + hyphens)
4. **Collision Probability**: Effectively zero for both versions

## CLI Usage

```bash
# Generate v4 UUID
$ npx uuid
ddeb27fb-d9a0-4624-be4d-4615062daed4

# Generate v7 UUID
$ npx uuid v7
019a26ab-9a66-71a9-a89e-63c35fce4a5a

# Generate multiple UUIDs
$ npx uuid && npx uuid && npx uuid
```

## Integration Checklist

- [ ] Install uuid@13.0.0
- [ ] Import v4 or v7 based on use case
- [ ] Use for entity IDs in repositories
- [ ] Validate UUIDs when receiving from external sources
- [ ] Store as strings in Firestore
- [ ] Add TypeScript types for type safety
- [ ] Document UUID version choice in code comments

## Anti-Patterns

❌ **Using Sequential IDs in Distributed Systems**:
```typescript
let counter = 0;
const id = `task-${++counter}`; // Race conditions, not globally unique
```

✅ **Use UUID**:
```typescript
const id = uuidv4(); // Globally unique, no coordination needed
```

---

❌ **Parsing UUID Parts Manually**:
```typescript
const timestamp = parseInt(uuid.substring(0, 8), 16); // Fragile
```

✅ **Use Library Functions**:
```typescript
import { parse, version } from 'uuid';
const ver = version(uuid); // Proper parsing
```

---

❌ **Generating UUIDs Client-Side for Security-Critical Operations**:
```typescript
const sessionToken = uuidv4(); // Predictable if not properly seeded
```

✅ **Generate Security Tokens Server-Side**:
```typescript
// Firebase Auth handles token generation securely
const token = await auth.currentUser.getIdToken();
```

## Cross-References

- **firebase-repository** - UUID for entity IDs
- **blueprint-integration** - Blueprint and member IDs
- **event-bus-integration** - Event ID generation
- **angular-component** - UUID in component state

## Package Information

- **Version**: 13.0.0
- **Repository**: https://github.com/uuidjs/uuid
- **RFC**: RFC9562 (UUID v7), RFC4122 (UUID v4)

---

**Version**: 1.0  
**Created**: 2025-12-25  
**Maintainer**: ng-events(GigHub) Development Team
