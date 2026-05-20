---
name: media-library
description: |
  WordPress-style media management system for this Next.js application.
  Covers MediaService CRUD, file upload, tag system, duplicate detection,
  MediaLibrary modal, MediaSelector form field, and block editor integration.
  Use this skill when working with media uploads, browsing, or selection.
allowed-tools: Read, Glob, Grep, Bash
version: 1.0.0
---

# Media Library Skill

WordPress-style media management system with full CRUD API, reusable modal, form field component, and block editor integration.

## Architecture Overview

```
MEDIA LIBRARY SYSTEM:

Core Layer (packages/core/):
├── src/lib/permissions/system.ts  # media.read/upload/update/delete (core system permissions)
├── src/
│   ├── components/media/
│   │   ├── MediaLibrary.tsx      # Main modal (browse, upload, select)
│   │   ├── MediaGrid.tsx         # Grid view with thumbnails
│   │   ├── MediaList.tsx         # List/table view
│   │   ├── MediaCard.tsx         # Individual media card
│   │   ├── MediaToolbar.tsx      # Search, filter, sort, view toggle
│   │   ├── MediaDetailPanel.tsx  # Right sidebar detail/edit panel
│   │   ├── MediaUploadZone.tsx   # Drag & drop upload area
│   │   ├── MediaSelector.tsx     # Form field component for entities
│   │   ├── MediaTagFilter.tsx    # Tag filter chips
│   │   └── index.ts              # Re-exports
│   ├── hooks/
│   │   ├── useMedia.ts           # TanStack Query hooks (CRUD + tags)
│   │   └── useMediaUpload.ts     # Upload hook with progress tracking
│   ├── lib/
│   │   ├── media/
│   │   │   ├── types.ts          # Media, MediaTag, MediaListOptions
│   │   │   ├── schemas.ts        # Zod validation schemas
│   │   │   └── utils.ts          # formatFileSize, getMediaType, etc.
│   │   └── services/
│   │       └── media.service.ts  # MediaService (CRUD, tags, duplicates)
│   └── types/
│       └── blocks.ts             # FieldType includes 'media-library'
│
├── migrations/
│   └── 021_media.sql             # Media + media_tags + media_tag_relations

API Layer (apps/dev/app/api/v1/):
├── media/
│   ├── route.ts                  # GET (list), POST (create)
│   ├── upload/route.ts           # POST (file upload)
│   ├── check-duplicates/route.ts # POST (hash check)
│   └── [id]/
│       ├── route.ts              # GET, PATCH, DELETE
│       └── tags/route.ts         # GET, POST, DELETE media tags
└── media-tags/
    └── route.ts                  # GET all tags

Dashboard (apps/dev/app/dashboard/(main)/media/):
└── page.tsx                      # Dashboard media page

Flow:
Upload → API → MediaService → DB → TanStack Query Cache → UI
```

> **Context-Aware Paths:** Core layer components and services are in `packages/core/`.
> API routes are in the app layer. Dashboard page is theme-provided.
> See `core-theme-responsibilities` skill for complete rules.

## When to Use This Skill

- Adding media upload functionality to a feature
- Integrating media selection into entity forms
- Adding `type: 'media-library'` fields to page builder blocks
- Working with the MediaLibrary modal or MediaSelector component
- Implementing media tag filtering or organization
- Debugging upload, duplicate detection, or media API issues
- Configuring upload size limits or accepted file types

## Media Type Definition

```typescript
interface Media {
  id: string
  userId: string
  teamId: string
  filename: string
  originalFilename: string
  mimeType: string
  fileSize: number
  url: string
  thumbnailUrl?: string
  width?: number
  height?: number
  title?: string
  alt?: string
  caption?: string
  hash?: string
  status: 'active' | 'archived'
  metadata?: Record<string, unknown>
  createdAt: string
  updatedAt: string
}

interface MediaTag {
  id: string
  name: string
  slug: string
  createdAt: string
}

interface MediaListOptions {
  limit?: number          // Default: 50
  offset?: number         // Default: 0
  orderBy?: string        // Default: 'createdAt'
  orderDir?: 'asc' | 'desc'  // Default: 'desc'
  type?: 'all' | 'image' | 'video'
  search?: string         // Searches filename, title, alt
  tagIds?: string[]       // Filter by tag IDs
}
```

## API Endpoints

| Method | Endpoint | Description | Auth Scope |
|--------|----------|-------------|------------|
| GET | `/api/v1/media` | List media (paginated, filterable) | `media:read` |
| POST | `/api/v1/media` | Create media record | `media:write` |
| POST | `/api/v1/media/upload` | Upload files | `media:write` |
| POST | `/api/v1/media/check-duplicates` | Check for duplicates by hash | `media:read` |
| GET | `/api/v1/media/[id]` | Get single media item | `media:read` |
| PATCH | `/api/v1/media/[id]` | Update media metadata | `media:write` |
| DELETE | `/api/v1/media/[id]` | Delete media item | `media:delete` |
| GET | `/api/v1/media/[id]/tags` | Get tags for a media item | `media:read` |
| POST | `/api/v1/media/[id]/tags` | Add tags to media | `media:write` |
| DELETE | `/api/v1/media/[id]/tags` | Remove tags from media | `media:write` |
| GET | `/api/v1/media-tags` | List all available tags | `media:read` |

All endpoints support dual authentication (session cookie + API key via `x-api-key` header).

### Query Parameters for GET /api/v1/media

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | number | 50 | Items per page |
| `offset` | number | 0 | Pagination offset |
| `orderBy` | string | `createdAt` | Sort field (`createdAt`, `filename`, `fileSize`, `mimeType`) |
| `orderDir` | string | `desc` | Sort direction (`asc`, `desc`) |
| `type` | string | `all` | Filter: `all`, `image`, `video` |
| `search` | string | - | Search in filename, title, alt |
| `tagIds` | string | - | Comma-separated tag IDs |

## MediaService

Static class following the service-layer pattern with RLS integration:

```typescript
// core/lib/services/media.service.ts

export class MediaService {
  // CRUD operations
  static async getById(id: string, userId: string): Promise<Media | null>
  static async list(userId: string, options?: MediaListOptions): Promise<ListResult<Media>>
  static async create(userId: string, teamId: string, data: CreateMedia): Promise<Media>
  static async update(id: string, userId: string, data: UpdateMedia): Promise<Media>
  static async delete(id: string, userId: string): Promise<boolean>

  // Tag operations
  static async getTags(mediaId: string, userId: string): Promise<MediaTag[]>
  static async addTag(mediaId: string, tagId: string, userId: string): Promise<void>
  static async removeTag(mediaId: string, tagId: string, userId: string): Promise<void>
  static async getAllTags(userId: string): Promise<MediaTag[]>

  // Duplicate detection
  static async checkDuplicates(hashes: string[], userId: string): Promise<Media[]>
}
```

## TanStack Query Hooks

### Query Hooks

```typescript
import {
  useMediaList,
  useMediaItem,
  useMediaTags,
  useMediaItemTags,
} from '@/core/hooks/useMedia'

// List media with filters (paginated)
const { data, isLoading, error } = useMediaList({
  limit: 50,
  offset: 0,
  type: 'image',
  search: 'hero',
  orderBy: 'createdAt',
  orderDir: 'desc',
  tagIds: ['tag-1', 'tag-2'],
})

// Single media item (enabled when id is truthy)
const { data: media } = useMediaItem(selectedId)

// All available tags
const { data: tags } = useMediaTags()

// Tags for a specific media item
const { data: mediaTags } = useMediaItemTags(mediaId)
```

### Mutation Hooks

```typescript
import {
  useCreateMedia,
  useUpdateMedia,
  useDeleteMedia,
  useAddMediaTag,
  useRemoveMediaTag,
} from '@/core/hooks/useMedia'

// Create media record
const createMutation = useCreateMedia()
await createMutation.mutateAsync({ filename, url, mimeType, fileSize })

// Update media metadata
const updateMutation = useUpdateMedia()
await updateMutation.mutateAsync({ id: 'media-123', title: 'New Title', alt: 'Alt text' })

// Delete media
const deleteMutation = useDeleteMedia()
await deleteMutation.mutateAsync('media-123')

// Tag management
const addTagMutation = useAddMediaTag()
await addTagMutation.mutateAsync({ mediaId: 'media-123', tagId: 'tag-456' })

const removeTagMutation = useRemoveMediaTag()
await removeTagMutation.mutateAsync({ mediaId: 'media-123', tagId: 'tag-456' })
```

### Upload Hook

```typescript
import { useMediaUpload } from '@/core/hooks/useMediaUpload'

const { upload, progress, isUploading, error } = useMediaUpload()

// Upload a file with progress tracking
const media = await upload(file)
console.log(`Upload progress: ${progress}%`)
```

### Query Key Conventions

```typescript
// Media query keys follow the standard pattern:
['media', filters]              // Media list with filters
['media', id]                   // Single media item
['media-tags']                  // All tags
['media', mediaId, 'tags']     // Tags for specific media
```

## Component Usage

### MediaLibrary Modal

Full-featured modal for browsing, uploading, and selecting media:

```typescript
import { MediaLibrary } from '@/core/components/media'

// Single selection mode
<MediaLibrary
  isOpen={isModalOpen}
  onClose={() => setIsModalOpen(false)}
  onSelect={(media: Media) => {
    setSelectedImage(media.url)
  }}
  mode="single"
  allowedTypes={['image']}
/>

// Multiple selection mode
<MediaLibrary
  isOpen={isModalOpen}
  onClose={() => setIsModalOpen(false)}
  onSelect={(mediaItems: Media[]) => {
    setGalleryImages(mediaItems.map(m => m.url))
  }}
  mode="multiple"
  allowedTypes={['image', 'video']}
  maxSelections={10}
/>
```

**MediaLibrary Props:**

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `isOpen` | `boolean` | Yes | Controls modal visibility |
| `onClose` | `() => void` | Yes | Callback when modal closes |
| `onSelect` | `(media: Media \| Media[]) => void` | Yes | Callback with selected media |
| `mode` | `'single' \| 'multiple'` | No | Selection mode (default: `'single'`) |
| `allowedTypes` | `string[]` | No | Restrict to `['image']`, `['video']`, or both |
| `maxSelections` | `number` | No | Max items in multiple mode |

### MediaSelector Form Field

Drop-in form component for entity fields:

```typescript
import { MediaSelector } from '@/core/components/media'

// In an entity form
<MediaSelector
  value={formData.featuredImageId}
  onChange={(id) => setFormData({ ...formData, featuredImageId: id })}
  type="image"
/>

// For video selection
<MediaSelector
  value={formData.videoId}
  onChange={(id) => setFormData({ ...formData, videoId: id })}
  type="video"
/>
```

**MediaSelector Props:**

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `value` | `string \| null` | Yes | Current media ID |
| `onChange` | `(id: string \| null) => void` | Yes | Callback when selection changes |
| `type` | `'image' \| 'video'` | No | Restrict selectable media type |

## Block Editor Integration

### Field Type: 'media-library'

In block field definitions, use `type: 'media-library'` to open the full MediaLibrary modal instead of a simple file input:

```typescript
// contents/themes/{theme}/blocks/hero/fields.ts
import type { FieldDefinition } from '@/core/types/blocks'

const customDesignFields: FieldDefinition[] = [
  {
    name: 'backgroundImage',
    label: 'Background Image',
    type: 'media-library',    // Opens MediaLibrary modal
    tab: 'design',
  },
]
```

### How MediaLibraryField Works

The `MediaLibraryField` component renders based on state:

1. **Empty state** - Shows "Browse Media Library" prompt button
2. **On click** - Opens the full `MediaLibrary` modal
3. **After selection** - Shows image preview with hover overlay (Change / Remove buttons)
4. **Storage** - Stores the URL string (not media ID) in block data

### In Array Sub-Fields

Media library fields also work inside array (repeatable) items:

```typescript
// Array field with media sub-field
{
  name: 'slides',
  label: 'Slides',
  type: 'array',
  tab: 'content',
  itemFields: [
    { name: 'image', label: 'Slide Image', type: 'media-library', tab: 'content' },
    { name: 'title', label: 'Title', type: 'text', tab: 'content' },
    { name: 'description', label: 'Description', type: 'textarea', tab: 'content' },
  ],
}
```

### Block Schema with Media

```typescript
// contents/themes/{theme}/blocks/hero/schema.ts
import { z } from 'zod'
import { baseBlockSchema } from '@/core/types/blocks'

export const schema = baseBlockSchema.merge(z.object({
  backgroundImage: z.string().url().optional(),   // URL from MediaLibrary
  overlayOpacity: z.number().min(0).max(100).default(50),
}))
```

## Upload Configuration

### app.config.ts

```typescript
// contents/themes/{theme}/config/app.config.ts
export const appConfig = {
  // ... other config

  media: {
    maxSizeMB: 10,                    // General max size
    maxSizeImageMB: 10,               // Image-specific max
    maxSizeVideoMB: 50,               // Video-specific max
    acceptedTypes: ['image/*', 'video/*'],
    allowedMimeTypes: [
      'image/jpeg',
      'image/png',
      'image/gif',
      'image/webp',
      'image/svg+xml',
      'video/mp4',
      'video/webm',
    ],
  },
}
```

### Upload Flow

```
1. User drops file on MediaUploadZone (or clicks to browse)
2. Client-side validation: file size, MIME type
3. Client computes file hash (SHA-256)
4. POST /api/v1/media/check-duplicates with hash
5. If duplicate found: prompt user (skip/replace/upload anyway)
6. POST /api/v1/media/upload with FormData
7. Server validates, stores file, creates DB record
8. TanStack Query cache invalidated, UI updates
```

## Database Schema

### Migration: 021_media.sql

```sql
-- Media items table
CREATE TABLE IF NOT EXISTS "media" (
  "id" TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  "userId" TEXT NOT NULL REFERENCES "user"(id),
  "teamId" TEXT NOT NULL REFERENCES "team"(id),
  "filename" VARCHAR(500) NOT NULL,
  "originalFilename" VARCHAR(500) NOT NULL,
  "mimeType" VARCHAR(100) NOT NULL,
  "fileSize" INTEGER NOT NULL,
  "url" TEXT NOT NULL,
  "thumbnailUrl" TEXT,
  "width" INTEGER,
  "height" INTEGER,
  "title" VARCHAR(500),
  "alt" VARCHAR(500),
  "caption" TEXT,
  "hash" VARCHAR(128),
  "status" VARCHAR(20) NOT NULL DEFAULT 'active',
  "metadata" JSONB DEFAULT '{}'::jsonb,
  "createdAt" TIMESTAMPTZ NOT NULL DEFAULT now(),
  "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Media tags table
CREATE TABLE IF NOT EXISTS "media_tags" (
  "id" TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  "name" VARCHAR(100) NOT NULL,
  "slug" VARCHAR(100) NOT NULL UNIQUE,
  "createdAt" TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Many-to-many relation: media <-> tags
CREATE TABLE IF NOT EXISTS "media_tag_relations" (
  "mediaId" TEXT NOT NULL REFERENCES "media"(id) ON DELETE CASCADE,
  "tagId" TEXT NOT NULL REFERENCES "media_tags"(id) ON DELETE CASCADE,
  PRIMARY KEY ("mediaId", "tagId")
);

-- Indexes
CREATE INDEX "idx_media_userId" ON "media"("userId");
CREATE INDEX "idx_media_teamId" ON "media"("teamId");
CREATE INDEX "idx_media_hash" ON "media"("hash");
CREATE INDEX "idx_media_status" ON "media"("status");
CREATE INDEX "idx_media_mimeType" ON "media"("mimeType");
CREATE INDEX "idx_media_tag_relations_tagId" ON "media_tag_relations"("tagId");
```

## Internationalization

### i18n Namespace: `media`

60+ translation keys in `en` and `es` locales.

```typescript
// Usage in components
const t = useTranslations('media')

t('title')              // "Media Library"
t('upload')             // "Upload"
t('dragDrop')           // "Drag & drop files here"
t('noResults')          // "No media found"
t('confirmDelete')      // "Are you sure you want to delete this media?"
t('filters.allTypes')   // "All Types"
t('filters.images')     // "Images"
t('filters.videos')     // "Videos"
t('detail.title')       // "Title"
t('detail.alt')         // "Alt Text"
t('detail.caption')     // "Caption"
t('detail.fileSize')    // "File Size"
t('detail.dimensions')  // "Dimensions"
t('detail.uploadedAt')  // "Uploaded At"
t('tags.addTag')        // "Add Tag"
t('tags.removeTag')     // "Remove Tag"
```

### Block Editor i18n Keys

```typescript
// Namespace: admin.blockEditor.form
t('changeImage')        // "Change"
t('removeImage')        // "Remove"
t('browseMedia')        // "Browse Media Library"
```

## Testing

### Cypress API Tests

File: `media-crud.cy.ts` (20+ test cases)

```typescript
// Tests cover:
// - List media with pagination
// - List media with type filter (image, video)
// - List media with search
// - List media with tag filter
// - List media with sorting
// - Create media record
// - Upload file
// - Get single media
// - Update media metadata (title, alt, caption)
// - Delete media
// - Duplicate detection via hash
// - Add/remove tags
// - Permission checks (media:read, media:write, media:delete)
// - Dual auth (session + API key)
```

### Jest Unit Tests

```
media.service.test.ts   # Service layer unit tests
schemas.test.ts         # Zod schema validation tests
utils.test.ts           # Utility function tests (formatFileSize, getMediaType, etc.)
```

### data-cy Selectors

Defined in `media.selectors.ts` and `block-editor.selectors.ts`:

```typescript
// media.selectors.ts
export const MEDIA_SELECTORS = {
  library: {
    modal: 'media-library-modal',
    grid: 'media-grid',
    list: 'media-list',
    card: 'media-card',
    toolbar: 'media-toolbar',
    searchInput: 'media-search-input',
    typeFilter: 'media-type-filter',
    sortSelect: 'media-sort-select',
    viewToggle: 'media-view-toggle',
    uploadZone: 'media-upload-zone',
    detailPanel: 'media-detail-panel',
    selectBtn: 'media-select-btn',
    deleteBtn: 'media-delete-btn',
  },
  selector: {
    container: 'media-selector',
    preview: 'media-selector-preview',
    browseBtn: 'media-selector-browse',
    removeBtn: 'media-selector-remove',
  },
  tags: {
    filter: 'media-tag-filter',
    chip: 'media-tag-chip',
    addBtn: 'media-tag-add',
    removeBtn: 'media-tag-remove',
  },
} as const

// block-editor.selectors.ts (additions)
export const BLOCK_EDITOR_SELECTORS = {
  // ... existing selectors
  mediaField: {
    container: 'block-media-field',
    preview: 'block-media-preview',
    browseBtn: 'block-media-browse',
    changeBtn: 'block-media-change',
    removeBtn: 'block-media-remove',
  },
} as const
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `core/src/components/media/MediaLibrary.tsx` | Main modal component |
| `core/src/components/media/MediaSelector.tsx` | Form field component |
| `core/src/components/media/MediaUploadZone.tsx` | Drag & drop upload |
| `core/src/hooks/useMedia.ts` | TanStack Query hooks (CRUD + tags) |
| `core/src/hooks/useMediaUpload.ts` | Upload with progress |
| `core/src/lib/media/types.ts` | TypeScript type definitions |
| `core/src/lib/media/schemas.ts` | Zod validation schemas |
| `core/src/lib/media/utils.ts` | Utility functions |
| `core/src/lib/services/media.service.ts` | MediaService (CRUD, tags, duplicates) |
| `core/src/types/blocks.ts` | FieldType with `'media-library'` |
| `core/migrations/021_media.sql` | Database migration |
| `apps/dev/app/api/v1/media/route.ts` | List + create endpoints |
| `apps/dev/app/api/v1/media/upload/route.ts` | File upload endpoint |
| `apps/dev/app/api/v1/media/[id]/route.ts` | Single item CRUD |
| `apps/dev/app/api/v1/media/[id]/tags/route.ts` | Media tag management |
| `apps/dev/app/api/v1/media-tags/route.ts` | All tags endpoint |
| `apps/dev/app/dashboard/(main)/media/page.tsx` | Dashboard page |

## Anti-Patterns

```typescript
// NEVER: Use type 'image' in block fields when you want the media library
{
  name: 'backgroundImage',
  type: 'image',              // Opens basic file input
}

// CORRECT: Use type 'media-library' for full media library experience
{
  name: 'backgroundImage',
  type: 'media-library',      // Opens MediaLibrary modal
}

// NEVER: Store media ID in block data (blocks store URLs)
onSelect={(media) => {
  updateBlockData({ backgroundImage: media.id })  // WRONG
}}

// CORRECT: Store URL in block data
onSelect={(media) => {
  updateBlockData({ backgroundImage: media.url })  // Correct
}}

// NEVER: Bypass MediaService for direct DB queries
const media = await queryWithRLS('SELECT * FROM "media" WHERE id = $1', [id], userId)

// CORRECT: Use MediaService
const media = await MediaService.getById(id, userId)

// NEVER: Skip duplicate check before upload
const result = await upload(file)  // Might create duplicates

// CORRECT: Check for duplicates first (useMediaUpload handles this)
const { upload } = useMediaUpload()  // Built-in duplicate detection
const result = await upload(file)

// NEVER: Hardcode file size limits
if (file.size > 10 * 1024 * 1024) { ... }

// CORRECT: Read from app.config.ts
import { appConfig } from '@/contents/themes/{theme}/config/app.config'
if (file.size > appConfig.media.maxSizeImageMB * 1024 * 1024) { ... }

// NEVER: Skip i18n for media UI strings
<Button>Upload</Button>

// CORRECT: Use translation keys
<Button>{t('upload')}</Button>

// NEVER: Forget data-cy selectors on interactive elements
<Button onClick={handleUpload}>Upload</Button>

// CORRECT: Include data-cy
<Button data-cy={sel(MEDIA_SELECTORS.library.uploadZone)} onClick={handleUpload}>
  {t('upload')}
</Button>
```

## Checklist

### Adding Media Selection to an Entity

- [ ] Import `MediaSelector` from `@/core/components/media`
- [ ] Add media field to entity form with proper `value` and `onChange`
- [ ] Add corresponding database column (TEXT for media ID or URL)
- [ ] Add i18n keys for the field label and description
- [ ] Add `data-cy` selector for the media field

### Adding Media to a Block

- [ ] Use `type: 'media-library'` in field definition (not `type: 'image'`)
- [ ] Add `.url().optional()` Zod schema field for the URL
- [ ] Store URL string in block data (not media ID)
- [ ] Add i18n keys if custom labels needed
- [ ] Test in block editor: empty state, selection, change, remove

### Creating Custom Media Workflow

- [ ] Use TanStack Query hooks from `useMedia.ts` (not raw fetch)
- [ ] Handle loading states with proper skeleton/spinner
- [ ] Handle error states with user-friendly messages
- [ ] Invalidate media queries after mutations
- [ ] Respect upload limits from `app.config.ts`
- [ ] Include duplicate detection via hash check
- [ ] All UI text uses `media` i18n namespace
- [ ] All interactive elements have `data-cy` selectors

### API Integration

- [ ] Uses dual auth (session + API key)
- [ ] Validates input with Zod schemas
- [ ] Respects `media:read`, `media:write`, `media:delete` scopes
- [ ] Pagination parameters handled correctly
- [ ] File upload uses `FormData` (not JSON)
- [ ] Response follows standard `{ data, total, limit, offset }` format

## Related Skills

- `page-builder-blocks` - Block field type `'media-library'` integration
- `entity-system` - MediaSelector for entity forms
- `tanstack-query` - useMedia hooks follow TanStack Query patterns
- `cypress-api` - Media API test patterns
- `how-to:handle-file-uploads` - Upload component and API guide
- `service-layer` - MediaService follows static class pattern with RLS
- `i18n-nextintl` - `media` namespace translations
- `cypress-selectors` - `MEDIA_SELECTORS` and `BLOCK_EDITOR_SELECTORS`
- `zod-validation` - Media schema validation patterns
- `database-migrations` - `021_media.sql` migration structure
