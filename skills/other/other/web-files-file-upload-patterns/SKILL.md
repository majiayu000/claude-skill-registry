---
name: web-files-file-upload-patterns
description: File upload patterns - drag-drop dropzones, chunked/resumable uploads, S3 presigned URLs, file validation (MIME type, magic bytes), progress tracking, image preview, accessibility (ARIA)
---

# File Upload Patterns

> **Quick Guide:** Use drag-and-drop dropzones with fallback file inputs for uploads. Validate files client-side (MIME + magic bytes) AND server-side. For files >5MB use chunked uploads with progress tracking. Upload directly to S3 using presigned URLs to avoid server bottlenecks. Always implement proper accessibility with keyboard support and ARIA announcements.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST validate files BOTH client-side AND server-side - client validation is UX only, not security)**

**(You MUST use magic bytes detection for security-critical uploads - MIME types and extensions can be spoofed)**

**(You MUST cleanup object URLs with `URL.revokeObjectURL()` to prevent memory leaks)**

**(You MUST provide keyboard support for dropzones - Enter/Space to open file dialog)**

**(You MUST use presigned URLs for S3 uploads - never proxy large files through your server)**

</critical_requirements>

---

**Auto-detection:** file upload, dropzone, drag-drop, react-dropzone, useDropzone, Uppy, TUS protocol, presigned URL, multipart upload, file validation, magic bytes, MIME type, progress indicator, upload progress, XHR upload, S3 upload, file input, aria-label upload

**When to use:**

- Building file upload interfaces (single or multi-file)
- Implementing drag-and-drop upload areas
- Uploading to S3 or cloud storage directly from browser
- Validating file types before upload
- Showing upload progress with speed/ETA
- Handling large file uploads with chunking/resumable support
- Creating accessible file upload components

**Key patterns covered:**

- Drag-and-drop dropzone with file input fallback
- File list management with status tracking
- Client-side validation (MIME type, magic bytes, dimensions)
- Progress tracking with XHR (speed, ETA)
- S3 presigned URL uploads (single + multipart)
- Chunked and resumable uploads
- Image preview with object URL cleanup
- Full accessibility (ARIA, keyboard, announcements)

**When NOT to use:**

- Server-side file processing (use backend skills)
- File storage architecture (use infrastructure skills)
- Video/audio streaming (use media handling skills)

**Detailed Resources:**

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

File uploads are deceptively complex. A simple file input works for basic cases, but production apps need validation, progress feedback, error handling, and accessibility. The key insight is that **client-side validation is for UX, not security** - always validate on the server.

**Core Principles:**

1. **Defense in depth** - Validate extension + MIME type + magic bytes + server-side
2. **Progressive enhancement** - Drag-drop enhances but doesn't replace click-to-browse
3. **Direct uploads** - Use presigned URLs to upload to S3 directly, not through your server
4. **Chunked for reliability** - Large files need chunking for resumability and progress
5. **Accessibility first** - Keyboard navigation and screen reader support from day one

**File Size Strategy:**

| File Size | Upload Method       | Progress UI            | Storage Pattern      |
| --------- | ------------------- | ---------------------- | -------------------- |
| < 5MB     | Single request      | Spinner or bar         | Direct presigned PUT |
| 5-50MB    | Single request      | Progress bar           | Presigned PUT        |
| 50MB-5GB  | Chunked             | Progress + ETA         | Multipart presigned  |
| > 5GB     | Chunked + resumable | Progress + ETA + pause | Multipart required   |

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic Dropzone Component

Build a dropzone with drag-and-drop support and fallback file input for accessibility.

#### Constants and Types

```typescript
// file-dropzone.tsx
import { useState, useRef, useCallback } from "react";
import type { DragEvent, ChangeEvent, ReactNode } from "react";

type DropzoneState = "idle" | "drag-over" | "drag-reject";

interface FileDropzoneProps {
  onFilesSelected: (files: File[]) => void;
  accept?: string[];
  multiple?: boolean;
  maxFiles?: number;
  disabled?: boolean;
  children?: ReactNode;
}

const DEFAULT_MAX_FILES = 10;
```

#### Implementation

```typescript
export function FileDropzone({
  onFilesSelected,
  accept = [],
  multiple = true,
  maxFiles = DEFAULT_MAX_FILES,
  disabled = false,
  children,
}: FileDropzoneProps) {
  const [state, setState] = useState<DropzoneState>('idle');
  const inputRef = useRef<HTMLInputElement>(null);

  const acceptString = accept.join(',');

  const isValidType = useCallback(
    (file: File): boolean => {
      if (accept.length === 0) return true;
      return accept.some((type) => {
        if (type.startsWith('.')) {
          return file.name.toLowerCase().endsWith(type.toLowerCase());
        }
        if (type.endsWith('/*')) {
          return file.type.startsWith(type.replace('/*', '/'));
        }
        return file.type === type;
      });
    },
    [accept]
  );

  const handleDrop = useCallback(
    (event: DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      event.stopPropagation();
      setState('idle');

      if (disabled) return;

      const droppedFiles = Array.from(event.dataTransfer.files);
      const validFiles = droppedFiles.filter(isValidType);
      const filesToProcess = multiple
        ? validFiles.slice(0, maxFiles)
        : validFiles.slice(0, 1);

      if (filesToProcess.length > 0) {
        onFilesSelected(filesToProcess);
      }
    },
    [disabled, isValidType, multiple, maxFiles, onFilesSelected]
  );

  const handleInputChange = useCallback(
    (event: ChangeEvent<HTMLInputElement>) => {
      const files = event.target.files;
      if (!files) return;

      const fileArray = Array.from(files);
      const filesToProcess = multiple
        ? fileArray.slice(0, maxFiles)
        : fileArray.slice(0, 1);

      onFilesSelected(filesToProcess);

      // Reset input to allow selecting same file again
      event.target.value = '';
    },
    [multiple, maxFiles, onFilesSelected]
  );

  const openFileDialog = useCallback(() => {
    if (!disabled) {
      inputRef.current?.click();
    }
  }, [disabled]);

  return (
    <div
      data-state={state}
      data-disabled={disabled || undefined}
      onDragEnter={(e) => {
        e.preventDefault();
        if (!disabled) setState('drag-over');
      }}
      onDragLeave={(e) => {
        e.preventDefault();
        setState('idle');
      }}
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      onClick={openFileDialog}
      role="button"
      tabIndex={disabled ? -1 : 0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openFileDialog();
        }
      }}
      aria-label="File upload area. Click or drag files to upload."
      aria-disabled={disabled}
    >
      <input
        ref={inputRef}
        type="file"
        accept={acceptString}
        multiple={multiple}
        onChange={handleInputChange}
        disabled={disabled}
        aria-hidden="true"
        tabIndex={-1}
        style={{ display: 'none' }}
      />
      {children}
    </div>
  );
}
```

**Why good:** Keyboard accessible with role="button" and Enter/Space handling, drag-drop enhances but doesn't replace click, file input hidden but functional for screen readers, resets input value to allow re-selecting same file, type validation before processing

---

### Pattern 2: File List Management Hook

Track multiple files with status, progress, and preview URLs.

#### Implementation

```typescript
// use-file-list.ts
import { useState, useCallback } from "react";

interface FileWithId {
  id: string;
  file: File;
  preview?: string;
  status: "pending" | "uploading" | "success" | "error";
  progress: number;
  error?: string;
}

interface UseFileListOptions {
  maxFiles?: number;
  maxSizeBytes?: number;
  allowDuplicates?: boolean;
}

const DEFAULT_MAX_SIZE_BYTES = 10 * 1024 * 1024; // 10MB

export function useFileList(options: UseFileListOptions = {}) {
  const {
    maxFiles = 10,
    maxSizeBytes = DEFAULT_MAX_SIZE_BYTES,
    allowDuplicates = false,
  } = options;

  const [files, setFiles] = useState<FileWithId[]>([]);

  const generateId = (): string => {
    return `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
  };

  const addFiles = useCallback(
    (
      newFiles: File[],
    ): {
      added: FileWithId[];
      rejected: Array<{ file: File; reason: string }>;
    } => {
      const added: FileWithId[] = [];
      const rejected: Array<{ file: File; reason: string }> = [];

      setFiles((current) => {
        const availableSlots = maxFiles - current.length;
        let slotsUsed = 0;

        for (const file of newFiles) {
          if (slotsUsed >= availableSlots) {
            rejected.push({ file, reason: "Maximum files limit reached" });
            continue;
          }

          if (file.size > maxSizeBytes) {
            const maxMB = maxSizeBytes / 1024 / 1024;
            rejected.push({ file, reason: `File exceeds ${maxMB}MB limit` });
            continue;
          }

          if (!allowDuplicates) {
            const isDuplicate = current.some(
              (existing) =>
                existing.file.name === file.name &&
                existing.file.size === file.size,
            );
            if (isDuplicate) {
              rejected.push({ file, reason: "Duplicate file" });
              continue;
            }
          }

          const fileWithId: FileWithId = {
            id: generateId(),
            file,
            status: "pending",
            progress: 0,
          };

          added.push(fileWithId);
          slotsUsed++;
        }

        return [...current, ...added];
      });

      return { added, rejected };
    },
    [maxFiles, maxSizeBytes, allowDuplicates],
  );

  const removeFile = useCallback((id: string) => {
    setFiles((current) => {
      const file = current.find((f) => f.id === id);
      if (file?.preview) {
        URL.revokeObjectURL(file.preview);
      }
      return current.filter((f) => f.id !== id);
    });
  }, []);

  const updateFile = useCallback((id: string, updates: Partial<FileWithId>) => {
    setFiles((current) =>
      current.map((f) => (f.id === id ? { ...f, ...updates } : f)),
    );
  }, []);

  const clearFiles = useCallback(() => {
    setFiles((current) => {
      current.forEach((f) => {
        if (f.preview) URL.revokeObjectURL(f.preview);
      });
      return [];
    });
  }, []);

  return {
    files,
    addFiles,
    removeFile,
    updateFile,
    clearFiles,
    hasFiles: files.length > 0,
    canAddMore: files.length < maxFiles,
  };
}
```

**Why good:** Tracks file status and progress per-file, cleans up object URLs on remove/clear to prevent memory leaks, validates size and duplicates before adding, returns rejected files with reasons for user feedback

---

### Pattern 3: Upload Progress with XHR

Track upload progress, speed, and estimated time remaining.

#### Implementation

```typescript
// use-upload-progress.ts
import { useState, useCallback, useRef } from "react";

interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
  speed: number; // bytes per second
  remainingTime: number; // seconds
}

const SPEED_SAMPLE_SIZE = 5;

export function useUploadProgress() {
  const [progress, setProgress] = useState<UploadProgress | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const xhrRef = useRef<XMLHttpRequest | null>(null);
  const speedSamplesRef = useRef<number[]>([]);
  const lastLoadedRef = useRef(0);
  const lastTimeRef = useRef(0);

  const calculateSpeed = useCallback((loaded: number, time: number): number => {
    const timeDelta = time - lastTimeRef.current;
    const loadedDelta = loaded - lastLoadedRef.current;

    if (timeDelta > 0) {
      const currentSpeed = (loadedDelta / timeDelta) * 1000;
      speedSamplesRef.current.push(currentSpeed);

      if (speedSamplesRef.current.length > SPEED_SAMPLE_SIZE) {
        speedSamplesRef.current.shift();
      }
    }

    lastLoadedRef.current = loaded;
    lastTimeRef.current = time;

    const sum = speedSamplesRef.current.reduce((a, b) => a + b, 0);
    return sum / speedSamplesRef.current.length || 0;
  }, []);

  const upload = useCallback(
    (file: File, url: string): Promise<Response> => {
      return new Promise((resolve, reject) => {
        setUploading(true);
        setError(null);
        speedSamplesRef.current = [];
        lastLoadedRef.current = 0;
        lastTimeRef.current = performance.now();

        const xhr = new XMLHttpRequest();
        xhrRef.current = xhr;

        xhr.upload.addEventListener("progress", (event) => {
          if (event.lengthComputable) {
            const speed = calculateSpeed(event.loaded, performance.now());
            const remaining = event.total - event.loaded;
            const remainingTime = speed > 0 ? remaining / speed : 0;

            setProgress({
              loaded: event.loaded,
              total: event.total,
              percentage: Math.round((event.loaded / event.total) * 100),
              speed,
              remainingTime,
            });
          }
        });

        xhr.addEventListener("load", () => {
          setUploading(false);
          if (xhr.status >= 200 && xhr.status < 300) {
            resolve(new Response(xhr.response, { status: xhr.status }));
          } else {
            const err = new Error(`Upload failed: ${xhr.status}`);
            setError(err.message);
            reject(err);
          }
        });

        xhr.addEventListener("error", () => {
          setUploading(false);
          const err = new Error("Upload failed");
          setError(err.message);
          reject(err);
        });

        xhr.addEventListener("abort", () => {
          setUploading(false);
          reject(new Error("Upload aborted"));
        });

        xhr.open("POST", url);
        xhr.send(file);
      });
    },
    [calculateSpeed],
  );

  const abort = useCallback(() => {
    xhrRef.current?.abort();
    xhrRef.current = null;
  }, []);

  return { progress, uploading, error, upload, abort };
}
```

**Why good:** Uses XHR for progress events (fetch doesn't support upload progress), calculates rolling average speed for smooth display, provides abort capability, tracks remaining time for UX

---

### Pattern 4: Magic Bytes File Type Detection

Validate file types by reading actual content, not just extension or MIME type.

#### Implementation

```typescript
// file-type-detection.ts
interface FileSignature {
  mime: string;
  extension: string;
  signature: number[];
}

const FILE_SIGNATURES: FileSignature[] = [
  // Images
  { mime: "image/jpeg", extension: "jpg", signature: [0xff, 0xd8, 0xff] },
  {
    mime: "image/png",
    extension: "png",
    signature: [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a],
  },
  { mime: "image/gif", extension: "gif", signature: [0x47, 0x49, 0x46, 0x38] },
  {
    mime: "image/webp",
    extension: "webp",
    signature: [0x52, 0x49, 0x46, 0x46],
  },
  // Documents
  {
    mime: "application/pdf",
    extension: "pdf",
    signature: [0x25, 0x50, 0x44, 0x46],
  }, // %PDF
  // Archives
  {
    mime: "application/zip",
    extension: "zip",
    signature: [0x50, 0x4b, 0x03, 0x04],
  },
];

interface DetectionResult {
  mime: string;
  extension: string;
  confidence: "high" | "medium" | "low";
}

export async function detectFileType(
  file: File,
): Promise<DetectionResult | null> {
  const HEADER_SIZE = 12;
  const buffer = await file.slice(0, HEADER_SIZE).arrayBuffer();
  const bytes = new Uint8Array(buffer);

  for (const sig of FILE_SIGNATURES) {
    const matches = sig.signature.every((byte, index) => bytes[index] === byte);

    if (matches) {
      return {
        mime: sig.mime,
        extension: sig.extension,
        confidence: sig.signature.length >= 4 ? "high" : "medium",
      };
    }
  }

  // Fallback to extension-based detection
  const ext = file.name.split(".").pop()?.toLowerCase();
  if (ext) {
    return {
      mime: file.type || "application/octet-stream",
      extension: ext,
      confidence: "low",
    };
  }

  return null;
}

export async function validateFileType(
  file: File,
  allowedTypes: string[],
): Promise<{ valid: boolean; error?: string }> {
  const detected = await detectFileType(file);

  if (!detected) {
    return { valid: false, error: "Unable to detect file type" };
  }

  const isAllowed = allowedTypes.some((type) => {
    if (type.endsWith("/*")) {
      return detected.mime.startsWith(type.replace("/*", "/"));
    }
    return detected.mime === type;
  });

  if (!isAllowed) {
    return {
      valid: false,
      error: `File type ${detected.mime} is not allowed`,
    };
  }

  return { valid: true };
}
```

**Why good:** Reads actual file bytes not just metadata, handles common image/document/archive formats, provides confidence level, can detect spoofed files where extension doesn't match content

---

### Pattern 5: S3 Presigned URL Upload

Upload directly to S3 from the browser using presigned URLs.

#### Client-Side Upload

```typescript
// s3-upload.ts
interface S3UploadCredentials {
  url: string;
  fields: Record<string, string>;
}

interface S3UploadOptions {
  onProgress?: (progress: number) => void;
  abortSignal?: AbortSignal;
}

export async function uploadToS3(
  file: File,
  credentials: S3UploadCredentials,
  options: S3UploadOptions = {},
): Promise<string> {
  const { url, fields } = credentials;

  const formData = new FormData();

  // Add presigned fields first (order matters for S3)
  Object.entries(fields).forEach(([key, value]) => {
    formData.append(key, value);
  });

  // File must be last
  formData.append("file", file);

  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    if (options.abortSignal) {
      options.abortSignal.addEventListener("abort", () => xhr.abort());
    }

    xhr.upload.addEventListener("progress", (event) => {
      if (event.lengthComputable) {
        options.onProgress?.(Math.round((event.loaded / event.total) * 100));
      }
    });

    xhr.addEventListener("load", () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        const fileUrl = `${url}${fields.key}`;
        resolve(fileUrl);
      } else {
        reject(new Error(`Upload failed: ${xhr.status}`));
      }
    });

    xhr.addEventListener("error", () => reject(new Error("Upload failed")));
    xhr.addEventListener("abort", () => reject(new Error("Upload aborted")));

    xhr.open("POST", url);
    xhr.send(formData);
  });
}
```

#### Server-Side Presign (Hono)

```typescript
// routes/upload.ts
import { Hono } from "hono";
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { z } from "zod";
import { zValidator } from "@hono/zod-validator";

const PRESIGNED_URL_EXPIRY_SECONDS = 3600;
const MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024; // 100MB

const presignRequestSchema = z.object({
  fileName: z.string().min(1),
  fileType: z.string().min(1),
  fileSize: z.number().max(MAX_FILE_SIZE_BYTES),
});

const app = new Hono();

app.post(
  "/api/upload/presign",
  zValidator("json", presignRequestSchema),
  async (c) => {
    const { fileName, fileType, fileSize } = c.req.valid("json");
    const userId = c.get("userId");

    const timestamp = Date.now();
    const sanitizedName = fileName.replace(/[^a-zA-Z0-9.-]/g, "_");
    const key = `uploads/${userId}/${timestamp}-${sanitizedName}`;

    const command = new PutObjectCommand({
      Bucket: process.env.S3_BUCKET!,
      Key: key,
      ContentType: fileType,
      ContentLength: fileSize,
    });

    const presignedUrl = await getSignedUrl(s3Client, command, {
      expiresIn: PRESIGNED_URL_EXPIRY_SECONDS,
    });

    return c.json({
      uploadUrl: presignedUrl,
      key,
      expiresAt: new Date(
        Date.now() + PRESIGNED_URL_EXPIRY_SECONDS * 1000,
      ).toISOString(),
    });
  },
);

export { app as uploadRoutes };
```

**Why good:** Uploads directly to S3 bypassing server bandwidth, presigned URLs are time-limited for security, sanitizes filename to prevent injection, includes expiration time for client to handle

</patterns>

---

<integration>

## Integration Guide

**Works with:**

- **React Hook Form**: Use dropzone inside form, validate before submit
- **React Query**: Manage upload mutations with retry/cache
- **Zustand**: Track global upload queue state
- **Hono**: Generate presigned URLs server-side

**React Hook Form Integration:**

```typescript
import { useForm, Controller } from 'react-hook-form';

function FormWithUpload() {
  const { control, handleSubmit } = useForm();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Controller
        name="files"
        control={control}
        rules={{ required: 'Please select at least one file' }}
        render={({ field, fieldState }) => (
          <>
            <FileDropzone
              onFilesSelected={(files) => field.onChange(files)}
            />
            {fieldState.error && <span>{fieldState.error.message}</span>}
          </>
        )}
      />
    </form>
  );
}
```

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Not validating files on server - client validation can be bypassed completely
- Trusting MIME type or extension alone - both can be spoofed; use magic bytes
- Not cleaning up object URLs - causes memory leaks with `URL.createObjectURL`
- Proxying large files through server - bottlenecks server; use presigned URLs
- No keyboard support for dropzones - accessibility violation

**Medium Priority Issues:**

- No progress feedback for large uploads - users don't know if it's working
- Using fetch for uploads - no progress events; use XHR
- Not handling upload abort - users can't cancel stuck uploads
- Long presigned URL expiration - security risk; keep under 1 hour

**Common Mistakes:**

- Not resetting file input after selection - can't select same file twice
- Using `e.stopPropagation()` without `e.preventDefault()` on drop - browser opens file
- Loading entire file into memory for validation - only read first bytes
- Fake progress bars - show real progress or spinner, not fake animation

**Gotchas & Edge Cases:**

- Safari handles drag events differently - test cross-browser
- Mobile has no drag-drop - ensure click-to-browse works
- CORS required for direct S3 uploads - configure bucket policy
- Large files may cause browser tab to freeze - use chunked upload
- EXIF orientation in photos - images may appear rotated

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST validate files BOTH client-side AND server-side - client validation is UX only, not security)**

**(You MUST use magic bytes detection for security-critical uploads - MIME types and extensions can be spoofed)**

**(You MUST cleanup object URLs with `URL.revokeObjectURL()` to prevent memory leaks)**

**(You MUST provide keyboard support for dropzones - Enter/Space to open file dialog)**

**(You MUST use presigned URLs for S3 uploads - never proxy large files through your server)**

**Failure to follow these rules will create security vulnerabilities, memory leaks, and accessibility issues.**

</critical_reminders>
