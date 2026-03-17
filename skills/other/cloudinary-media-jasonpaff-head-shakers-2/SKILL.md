---
name: cloudinary-media
description: Enforces project Cloudinary media conventions when working with image uploads, URL generation, transformations, social sharing images, and photo management components. This skill covers the complete media workflow including CloudinaryService operations, URL utilities, CldImage/CldUploadWidget components, path organization, type definitions, and Sentry integration.
---

# Cloudinary Media Skill

## Purpose

This skill enforces the project Cloudinary media conventions automatically during media-related development. It ensures consistent patterns for image uploads, URL transformations, social sharing images, photo management, error handling with Sentry, and proper type usage across the application.

## Activation

This skill activates when:

- Working with image uploads using `CldUploadWidget` or `CloudinaryService`
- Using `CldImage` component from `next-cloudinary` for image display
- Generating optimized URLs with `cloudinary.utils` functions
- Creating social sharing images (OG, Twitter) for SEO metadata
- Extracting publicIds or formats from Cloudinary URLs
- Implementing photo galleries, avatars, or image displays
- Working with `CloudinaryPhoto` type or related interfaces
- Using `CloudinaryPathBuilder` or `CLOUDINARY_PATHS` constants
- Implementing photo upload components with progress tracking
- Working with files in `src/lib/utils/cloudinary.utils.ts`
- Working with files in `src/lib/services/cloudinary.service.ts`
- Working with files in `src/lib/constants/cloudinary-paths.ts`
- Working with files in `src/types/cloudinary.types.ts`
- Working with files in `src/components/ui/cloudinary-*.tsx`

## Workflow

1. Detect Cloudinary work (file path contains `cloudinary`, imports from `next-cloudinary`, or uses cloudinary utilities)
2. Load `references/Cloudinary-Media-Conventions.md`
3. Generate/modify code following all conventions
4. Scan for violations of media patterns
5. Auto-fix all violations (no permission needed)
6. Report fixes applied

## Key Patterns

### Image Display

- Use `CldImage` from `next-cloudinary` for all Cloudinary images
- Pass `publicId` to `src` prop (not full URL)
- Always include `alt`, `crop`, `gravity`, `quality={'auto'}` props
- Use `sizes` prop for responsive images with `fill`
- Extract publicId using `extractPublicIdFromCloudinaryUrl()` when needed

### URL Generation

- Use `generateOpenGraphImageUrl()` for OG images (1200x630)
- Use `generateTwitterCardImageUrl()` for Twitter cards (800x418)
- Use `generateSocialImageUrl()` for platform-specific dimensions
- Use `extractFormatFromCloudinaryUrl()` to get file extensions
- All utilities include Sentry error logging with fallbacks

### Upload Service

- Use `CloudinaryService` static methods for server-side operations
- Use `deletePhotosByUrls()` for batch deletion with URL context
- Use `movePhotosToPermFolder()` to move temp uploads to permanent locations
- Use `getOptimizedUrl()` for programmatic URL generation
- All service methods use circuit breakers and retry logic

### Path Organization

- Use `CLOUDINARY_PATHS.FOLDERS` for base folder names
- Use `CloudinaryPathBuilder` functions for dynamic paths:
  - `bobbleheadPath(userId, collectionId, bobbleheadId)`
  - `collectionCoverPath(userId, collectionId)`
  - `profilePath(userId)`
  - `tempPath(userId)`
- Never hardcode folder paths directly

### Type Definitions

- Use `CloudinaryPhoto` interface for photo data
- Use `transformCloudinaryResult()` to convert upload results
- Use `PhotoUploadState` for tracking upload progress
- Use `FileUploadProgress` for individual file tracking
- Use type guards `isPersistedPhoto()` and `isTempPhoto()`

### Upload Components

- Use `CloudinaryPhotoUpload` component for photo management
- Configure `CldUploadWidget` with proper options and signature endpoint
- Implement optimistic updates with blob URLs during upload
- Handle upload errors with retry capability
- Support bulk selection and deletion

### Error Handling

- All utilities log errors to Sentry with operation context
- Return sensible fallbacks on error (default image, original URL)
- Use `createServiceError` for service-level errors
- Track upload failures with `uploadError` property

## References

- `references/Cloudinary-Media-Conventions.md` - Complete Cloudinary media conventions
