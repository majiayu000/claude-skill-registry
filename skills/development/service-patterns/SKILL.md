---
description: Service layer patterns for Ballee using BaseService, Result types, mappers, storage operations, soft delete handling, and proper error handling. Use when creating services, implementing CRUD operations, handling file uploads, or managing business logic.
version: "1.2.0"
updated: "2026-01-06"
---

# Service Patterns

## Service Structure

```typescript
import { BaseService } from '@kit/shared/services';
import type { Database } from '@kit/supabase/database';
import type { SupabaseClient } from '@supabase/supabase-js';

type ItemRow = Database['public']['Tables']['items']['Row'];
type ItemInsert = Database['public']['Tables']['items']['Insert'];
type ItemUpdate = Database['public']['Tables']['items']['Update'];

export class ItemService extends BaseService {
  constructor(client: SupabaseClient<Database>) {
    super(client, 'ItemService');
  }

  async getById(id: string): Promise<Result<ItemRow>> {
    const { data, error } = await this.client
      .from('items')
      .select('*')
      .eq('id', id)
      .single();

    if (error) {
      this.logger.error('Failed to get item', { id, error });
      return { success: false, error: new ServiceError(error.message, 'GET_FAILED') };
    }

    return { success: true, data };
  }

  async create(input: ItemInsert): Promise<Result<ItemRow>> {
    const { data, error } = await this.client
      .from('items')
      .insert(input)
      .select()
      .single();

    if (error) {
      this.logger.error('Failed to create item', { input, error });
      return { success: false, error: new ServiceError(error.message, 'CREATE_FAILED') };
    }

    this.logger.info('Item created', { id: data.id });
    return { success: true, data };
  }

  async update(id: string, input: ItemUpdate): Promise<Result<ItemRow>> {
    const { data, error } = await this.client
      .from('items')
      .update(input)
      .eq('id', id)
      .select()
      .single();

    if (error) {
      this.logger.error('Failed to update item', { id, input, error });
      return { success: false, error: new ServiceError(error.message, 'UPDATE_FAILED') };
    }

    return { success: true, data };
  }

  async delete(id: string): Promise<Result<void>> {
    const { error } = await this.client
      .from('items')
      .delete()
      .eq('id', id);

    if (error) {
      this.logger.error('Failed to delete item', { id, error });
      return { success: false, error: new ServiceError(error.message, 'DELETE_FAILED') };
    }

    return { success: true, data: undefined };
  }
}
```

## BaseService Query Helpers (RECOMMENDED)

Use these helpers in `BaseService` to reduce boilerplate. Located at `packages/shared/src/services/base.service.ts`.

### executeQuery - Single Record

```typescript
// Instead of manual try-catch-log pattern:
async getVenueById(id: string): Promise<Result<Venue>> {
  return this.executeQuery({
    method: 'getVenueById',
    context: { venueId: id },
    query: () => this.client.from('venues').select('*').eq('id', id).single(),
  });
}

// Handles: logging, error capture, Result wrapping
```

### executeQueryArray - Multiple Records

```typescript
async getVenuesByCity(city: string): Promise<Result<Venue[]>> {
  return this.executeQueryArray({
    method: 'getVenuesByCity',
    context: { city },
    query: () => this.client.from('venues').select('*').eq('city', city),
  });
}
```

### hasRelatedRecords - Existence Check

```typescript
// Check if entity has dependent records before delete
async canDeleteClient(clientId: string): Promise<boolean> {
  const hasEvents = await this.hasRelatedRecords('events', 'client_id', clientId);
  const hasProductions = await this.hasRelatedRecords('productions', 'client_id', clientId);
  return !hasEvents && !hasProductions;
}
```

### countRelatedRecords - Exact Count

```typescript
// Get exact count of related records
async getClientStats(clientId: string): Promise<{ eventCount: number; productionCount: number }> {
  const eventCount = await this.countRelatedRecords('events', 'client_id', clientId);
  const productionCount = await this.countRelatedRecords('productions', 'client_id', clientId);
  return { eventCount, productionCount };
}
```

### API Reference

```typescript
// Single record query with automatic error handling
protected async executeQuery<T>(options: {
  method: string;
  context: Record<string, unknown>;
  query: () => PostgrestSingleResponse<T>;
}): Promise<Result<T>>;

// Array query with automatic error handling
protected async executeQueryArray<T>(options: {
  method: string;
  context: Record<string, unknown>;
  query: () => PostgrestResponse<T[]>;
}): Promise<Result<T[]>>;

// Check if any related records exist
protected async hasRelatedRecords(
  table: string,
  column: string,
  value: string
): Promise<boolean>;

// Count related records
protected async countRelatedRecords(
  table: string,
  column: string,
  value: string
): Promise<number>
```

## Result Pattern

```typescript
// Type definition
type Result<T, E = ServiceError> =
  | { success: true; data: T }
  | { success: false; error: E };

// NEVER throw - always return Result
async create(data): Promise<Result<Item>> {
  if (error) {
    return { success: false, error: new ServiceError('msg', 'CODE') };
  }
  return { success: true, data: result };
}

// Using results
const result = await service.create(data);
if (!result.success) {
  // Handle error
  return { error: result.error.message };
}
// Use result.data
```

## Mapper Pattern

```typescript
// Form data → Database format
export class ItemMapper {
  static toDatabase(form: ItemFormData): ItemInsert {
    return {
      name: sanitizeText(form.name),
      email: form.email?.toLowerCase().trim(),
      amount: form.amount ? Math.round(form.amount * 100) : null, // cents
      date: form.date?.toISOString(),
    };
  }

  static toForm(row: ItemRow): ItemFormData {
    return {
      name: row.name,
      email: row.email,
      amount: row.amount ? row.amount / 100 : undefined, // dollars
      date: row.date ? new Date(row.date) : undefined,
    };
  }
}

// Sanitization helpers
function sanitizeText(value: string | null | undefined): string | null {
  if (!value) return null;
  return value.trim().replace(/\s+/g, ' ');
}

function sanitizeUrl(value: string | null | undefined): string | null {
  if (!value) return null;
  const url = value.trim();
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    return `https://${url}`;
  }
  return url;
}
```

## Multi-Table Operations

```typescript
export class OrderService extends BaseService {
  async createWithItems(
    orderData: OrderInsert,
    items: OrderItemInsert[]
  ): Promise<Result<Order>> {
    // Create order
    const orderResult = await this.create(orderData);
    if (!orderResult.success) return orderResult;

    // Create items with order_id
    const itemsWithOrderId = items.map(item => ({
      ...item,
      order_id: orderResult.data.id,
    }));

    const { error } = await this.client
      .from('order_items')
      .insert(itemsWithOrderId);

    if (error) {
      // Cleanup on failure
      await this.delete(orderResult.data.id);
      return { success: false, error: new ServiceError('Failed to create items', 'ITEMS_FAILED') };
    }

    return orderResult;
  }
}
```

## Service with Relations

```typescript
async getWithRelations(id: string): Promise<Result<ItemWithRelations>> {
  const { data, error } = await this.client
    .from('items')
    .select(`
      *,
      category:categories(*),
      tags:item_tags(tag:tags(*))
    `)
    .eq('id', id)
    .single();

  if (error) {
    return { success: false, error: new ServiceError(error.message, 'GET_FAILED') };
  }

  return { success: true, data };
}
```

## Logging Conventions

```typescript
// Info - successful operations
this.logger.info('Item created', { id: data.id, name: data.name });

// Warn - expected failures (validation, not found)
this.logger.warn('Item not found', { id });

// Error - unexpected failures
this.logger.error('Database error', { error, context: { id, input } });
```

## Soft Delete Pattern

**CRITICAL**: Tables with `deleted_at` columns must ALWAYS filter soft-deleted records in queries.

### Tables with Soft Delete

| Table | Has deleted_at | Notes |
|-------|---------------|-------|
| clients | Yes | Filter in all queries |
| conversations | Yes | Filter in all queries |
| messages | Yes + is_deleted | Uses boolean flag |
| organizations | Yes | Filter in all queries |
| profile_posts | Yes | Filter in all queries |
| cast_roles | Yes | Filter in all queries |

### Soft Delete Query Pattern

```typescript
// ✅ CORRECT - Always filter soft-deleted records
async getClientById(id: string): Promise<Result<Client>> {
  const { data, error } = await this.client
    .from('clients')
    .select('*')
    .eq('id', id)
    .is('deleted_at', null)  // REQUIRED for soft-delete tables!
    .single();
  // ...
}

// ✅ CORRECT - Soft delete instead of hard delete
async deleteClient(id: string): Promise<Result<void>> {
  const { error } = await this.client
    .from('clients')
    .update({ deleted_at: new Date().toISOString() })
    .eq('id', id)
    .is('deleted_at', null);  // Don't re-delete already deleted
  // ...
}

// ❌ WRONG - Missing soft delete filter
async getClientById(id: string): Promise<Result<Client>> {
  const { data, error } = await this.client
    .from('clients')
    .select('*')
    .eq('id', id)
    .single();  // BUG: May return soft-deleted record!
}

// ❌ WRONG - Hard delete on soft-delete table
async deleteClient(id: string): Promise<Result<void>> {
  const { error } = await this.client
    .from('clients')
    .delete()  // BUG: Should soft delete!
    .eq('id', id);
}
```

### BaseCrudService for Soft Delete

For services that need full CRUD with soft delete, use `BaseCrudService`:

```typescript
import { BaseCrudService } from '@kit/shared/services';

export class ClientService extends BaseCrudService<Client> {
  constructor(client: SupabaseClient<Database>) {
    super(client, {
      tableName: 'clients',
      entityName: 'Client',
      enableSoftDelete: true,
      // softDeleteColumn defaults to 'deleted_at'
    });
  }
  // Inherits: findById, findMany, create, update, delete (soft), softDelete
}
```

## Storage Service Pattern

Services that handle file uploads should use `StorageUrlService` for consistent signed URL generation.

### Service with Storage

```typescript
import { BaseService } from '@kit/shared/services';
import { Result, ServiceError } from '@kit/shared/result';
import {
  createStorageUrlService,
  SignedUrlExpiry,
  StorageBuckets,
  type StorageUrlService,
} from '@kit/shared/storage';
import type { Database } from '@kit/supabase/database';
import type { SupabaseClient } from '@supabase/supabase-js';

export class DocumentService extends BaseService {
  private storageService: StorageUrlService;

  constructor(client: SupabaseClient<Database>) {
    super(client);
    this.storageService = createStorageUrlService(client);
  }

  /**
   * Upload a document to storage and create database record
   */
  async uploadDocument(
    file: File,
    entityId: string,
    userId: string,
  ): Promise<Result<Document>> {
    const logContext = {
      method: 'uploadDocument',
      entityId,
      fileName: file.name,
      fileSize: file.size,
    };

    this.log('info', 'Starting document upload', logContext);

    try {
      // 1. Validate file
      const maxSize = 10 * 1024 * 1024; // 10MB
      if (file.size > maxSize) {
        return Result.fail(
          ServiceError.validation('File size exceeds 10MB limit'),
        );
      }

      const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
      if (!allowedTypes.includes(file.type)) {
        return Result.fail(
          ServiceError.validation('Invalid file type'),
        );
      }

      // 2. Generate storage path
      const timestamp = Date.now();
      const fileName = `${timestamp}_${file.name}`;
      const storagePath = `${entityId}/${fileName}`;

      // 3. Upload to storage using bucket constant
      const { error: uploadError } = await this.client.storage
        .from(StorageBuckets.VENUE_DOCUMENTS)  // Use constant!
        .upload(storagePath, file, {
          contentType: file.type,
          upsert: false,
        });

      if (uploadError) {
        this.log('error', 'Storage upload failed', {
          ...logContext,
          error: uploadError.message,
        });
        return Result.fail(ServiceError.database(uploadError.message));
      }

      // 4. Create database record
      const { data: document, error: dbError } = await this.client
        .from('documents')
        .insert({
          entity_id: entityId,
          storage_path: storagePath,
          file_name: file.name,
          file_size: file.size,
          mime_type: file.type,
          uploaded_by: userId,
        })
        .select()
        .single();

      if (dbError) {
        // Rollback: delete uploaded file
        await this.client.storage
          .from(StorageBuckets.VENUE_DOCUMENTS)
          .remove([storagePath]);

        return Result.fail(ServiceError.database(dbError.message));
      }

      this.log('info', 'Document uploaded successfully', {
        ...logContext,
        documentId: document.id,
      });

      return Result.ok(document);
    } catch (error) {
      return Result.fail(
        ServiceError.internal(
          error instanceof Error ? error.message : 'Unknown error',
        ),
      );
    }
  }

  /**
   * Get signed URL for document viewing/download
   * Uses centralized StorageUrlService
   */
  async getDocumentUrl(
    storagePath: string,
    expiresIn: number = SignedUrlExpiry.IMMEDIATE_DISPLAY,
  ): Promise<Result<string>> {
    return this.storageService.getSignedUrl(
      StorageBuckets.VENUE_DOCUMENTS,
      storagePath,
      { expiresIn },
    );
  }

  /**
   * Get documents with signed URLs (batch operation)
   */
  async getDocumentsWithUrls(entityId: string): Promise<Result<DocumentWithUrl[]>> {
    const { data, error } = await this.client
      .from('documents')
      .select('*')
      .eq('entity_id', entityId)
      .order('created_at', { ascending: false });

    if (error) {
      return Result.fail(ServiceError.database(error.message));
    }

    // Enrich with signed URLs (efficient batch operation)
    const docsWithUrls = await this.storageService.enrichWithSignedUrls(
      StorageBuckets.VENUE_DOCUMENTS,
      data || [],
      (doc) => doc.storage_path,
      (doc, url) => ({ ...doc, signedUrl: url }),
      { expiresIn: SignedUrlExpiry.IMMEDIATE_DISPLAY },
    );

    return Result.ok(docsWithUrls);
  }

  /**
   * Delete document from storage and database
   */
  async deleteDocument(documentId: string): Promise<Result<void>> {
    // 1. Fetch document to get storage path
    const { data: document, error: fetchError } = await this.client
      .from('documents')
      .select('storage_path')
      .eq('id', documentId)
      .single();

    if (fetchError) {
      return Result.fail(ServiceError.notFound('Document not found'));
    }

    // 2. Delete from storage
    const { error: storageError } = await this.client.storage
      .from(StorageBuckets.VENUE_DOCUMENTS)
      .remove([document.storage_path]);

    if (storageError) {
      this.log('warn', 'Failed to delete from storage', {
        documentId,
        error: storageError.message,
      });
      // Continue with database deletion
    }

    // 3. Delete database record
    const { error: deleteError } = await this.client
      .from('documents')
      .delete()
      .eq('id', documentId);

    if (deleteError) {
      return Result.fail(ServiceError.database(deleteError.message));
    }

    return Result.ok(undefined);
  }
}
```

### Storage Constants Reference

```typescript
// Bucket names - ALWAYS use these constants
import { StorageBuckets, SignedUrlExpiry } from '@kit/shared/storage';

// Account/Profile
StorageBuckets.ACCOUNT_IMAGE          // 'account_image'
StorageBuckets.PROFILE_MEDIA          // 'profile-media' (public bucket)
StorageBuckets.DANCER_MEDIA           // 'dancer-media'

// Documents
StorageBuckets.VENUE_DOCUMENTS        // 'venue-documents'
StorageBuckets.PRODUCTION_DOCUMENTS   // 'production-documents'
StorageBuckets.LEGAL_DOCUMENTS        // 'legal-documents'
StorageBuckets.REIMBURSEMENT_DOCUMENTS // 'reimbursement-documents'

// Legal/Compliance
StorageBuckets.CONTRACTS              // 'contracts'
StorageBuckets.IDENTITY_DOCUMENTS     // 'identity-documents'
StorageBuckets.INVOICE_PDFS           // 'invoice-pdfs'

// Expiry times - use instead of magic numbers
SignedUrlExpiry.IMMEDIATE_DISPLAY  // 3600 (1 hour) - UI display
SignedUrlExpiry.DOWNLOAD           // 86400 (24 hours) - download links
SignedUrlExpiry.PROFILE_PHOTO      // 604800 (7 days) - stored in DB
SignedUrlExpiry.ADMIN_REVIEW       // 86400 (24 hours) - admin viewing
SignedUrlExpiry.MAX                // 604800 (7 days) - Supabase limit
```

### Path Extraction Utilities

```typescript
import { extractStoragePath, StoragePathService, StorageBuckets } from '@kit/shared/storage';

// Extract path from signed URL, public URL, or bucket-prefixed path
const path = extractStoragePath(signedUrl, StorageBuckets.IDENTITY_DOCUMENTS);
// Result: 'user-123/doc.pdf' (bucket prefix stripped)

// Detect bucket from URL
const bucket = StoragePathService.detectBucket(url);

// Validate path (no traversal, not absolute)
const result = StoragePathService.validate(storagePath);
```

### Thumbnail Generation

```typescript
import { ThumbnailSizes, generatePublicThumbnailUrl } from '@kit/shared/storage';

// Preset sizes for signed URL transforms
ThumbnailSizes.SMALL   // { width: 100, height: 100, quality: 80 }
ThumbnailSizes.MEDIUM  // { width: 200, height: 200, quality: 80 }
ThumbnailSizes.LARGE   // { width: 400, height: 400, quality: 85 }
ThumbnailSizes.XLARGE  // { width: 800, height: 800, quality: 90 }

// For signed URLs - use transform option
const result = await storageService.getSignedUrl(bucket, path, {
  transform: ThumbnailSizes.MEDIUM,
});

// For public bucket URLs - use generatePublicThumbnailUrl
const thumbnailUrl = generatePublicThumbnailUrl(publicUrl, { width: 200, height: 200 });
```

### URL Storage Best Practice

**CRITICAL**: Always store raw storage paths in the database, never signed URLs (they expire).

```typescript
// ✅ CORRECT - Store raw path
await client.from('documents').insert({
  storage_path: 'user-123/photo.jpg',  // Raw path only
});

// ❌ WRONG - Storing signed URL (will expire!)
await client.from('documents').insert({
  file_url: signedUrl,  // This will break after expiry!
});
```

### Storage Anti-Patterns

```typescript
// ❌ WRONG - Hardcoded bucket name
.from('venue-documents')

// ✅ CORRECT - Use constant
.from(StorageBuckets.VENUE_DOCUMENTS)

// ❌ WRONG - Magic number for expiry
.createSignedUrl(path, 3600)

// ✅ CORRECT - Use constant
.createSignedUrl(path, SignedUrlExpiry.IMMEDIATE_DISPLAY)

// ❌ WRONG - getPublicUrl for private bucket (returns 403!)
const { data } = client.storage.from('private-bucket').getPublicUrl(path);

// ✅ CORRECT - Use signed URLs for private buckets
const result = await storageService.getSignedUrl(
  StorageBuckets.INVOICE_PDFS,
  path,
  { expiresIn: SignedUrlExpiry.DOWNLOAD },
);

// ❌ WRONG - Individual signed URLs in a loop
const docs = await Promise.all(
  documents.map(async (doc) => {
    const { data } = await client.storage
      .from('bucket')
      .createSignedUrl(doc.path, 3600);
    return { ...doc, url: data?.signedUrl };
  })
);

// ✅ CORRECT - Batch operation with enrichWithSignedUrls
const docsWithUrls = await storageService.enrichWithSignedUrls(
  StorageBuckets.VENUE_DOCUMENTS,
  documents,
  (doc) => doc.storage_path,
  (doc, url) => ({ ...doc, signedUrl: url }),
);
```

### Real Examples in Codebase

- `DancerMediaService`: `packages/features/dancers/src/services/dancer-media.service.ts`
- `ReimbursementDocumentService`: `packages/features/reimbursements/src/services/reimbursement-document.service.ts`
- `VenueDocumentService`: `apps/web/app/admin/venues/_lib/services/venue-document.service.ts`
- `PDFGenerationService`: `packages/features/invoices/src/services/pdf-generation.service.ts`

### PDF Generation Note

**IMPORTANT**: For PDF generation with `@react-pdf/renderer`, do NOT create Server Actions.
Use **API Routes** instead to avoid `hasOwnProperty` errors with React 19.

See `api-patterns` skill for the complete PDF generation pattern including:
- Streaming API Route pattern
- `sanitizeForPdf()` helper for Supabase data
- Client-side download utilities

Existing PDF routes:
- `/api/pdf/hire-order` - Admin hire order PDFs
- `/api/pdf/resume` - Dancer resume/CV PDFs

---

## Rules

1. **Never throw** - Always return `Result<T>`
2. **Use user client** - Not admin client for business logic
3. **Log everything** - Info for success, error for failures
4. **Type everything** - Use Database types from `database.types`
5. **Validate early** - Use Zod in actions, before calling service
6. **Use storage constants** - Never hardcode bucket names or expiry times
7. **Use StorageUrlService** - For consistent signed URL generation
8. **Batch storage operations** - Use `enrichWithSignedUrls` for multiple files
