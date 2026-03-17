---
name: file-upload
description: Complete guide for implementing file uploads in IntelliFill with React-dropzone frontend, Multer backend, file validation, Bull queue processing, and security best practices
---

# File Upload Skill - IntelliFill

This skill provides comprehensive patterns for implementing secure file uploads in the IntelliFill project, covering frontend drag-and-drop, backend processing, validation, queue management, and security.

---

## Table of Contents

1. [Frontend: React-Dropzone Integration](#frontend-react-dropzone-integration)
2. [Backend: Multer Configuration](#backend-multer-configuration)
3. [File Validation & Security](#file-validation--security)
4. [Upload Progress Tracking](#upload-progress-tracking)
5. [Bull Queue Integration](#bull-queue-integration)
6. [Error Handling Patterns](#error-handling-patterns)
7. [Complete Implementation Examples](#complete-implementation-examples)
8. [Testing Strategies](#testing-strategies)

---

## Frontend: React-Dropzone Integration

### Base File Upload Component

**Location**: `quikadmin-web/src/components/features/file-upload-zone.tsx`

The project uses a reusable `FileUploadZone` component built on `react-dropzone`:

```typescript
import { useDropzone, type FileRejection, type DropzoneOptions } from "react-dropzone"
import { Upload, File, X, AlertCircle, CheckCircle2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"

interface FileUploadZoneProps {
  onFilesAccepted: (files: File[]) => void
  onFilesRejected?: (rejections: FileRejection[]) => void
  accept?: DropzoneOptions["accept"]
  maxSize?: number
  maxFiles?: number
  multiple?: boolean
  disabled?: boolean
  showFileList?: boolean
  uploadProgress?: number
  children?: React.ReactNode
}

export function FileUploadZone({
  onFilesAccepted,
  onFilesRejected,
  accept,
  maxSize = 10 * 1024 * 1024, // 10MB default
  maxFiles = 1,
  multiple = false,
  disabled = false,
  showFileList = true,
  uploadProgress,
  children,
}: FileUploadZoneProps) {
  const [acceptedFiles, setAcceptedFiles] = React.useState<File[]>([])
  const [rejectedFiles, setRejectedFiles] = React.useState<FileRejection[]>([])

  const onDrop = React.useCallback(
    (accepted: File[], rejected: FileRejection[]) => {
      setAcceptedFiles(accepted)
      setRejectedFiles(rejected)

      if (accepted.length > 0) {
        onFilesAccepted(accepted)
      }

      if (rejected.length > 0 && onFilesRejected) {
        onFilesRejected(rejected)
      }
    },
    [onFilesAccepted, onFilesRejected]
  )

  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject,
  } = useDropzone({
    onDrop,
    accept,
    maxSize,
    maxFiles,
    multiple,
    disabled,
  })

  return (
    <div data-slot="file-upload-zone" className="space-y-4">
      {/* Drop Zone */}
      <div
        {...getRootProps()}
        className={cn(
          "relative flex flex-col items-center justify-center gap-4 rounded-lg border-2 border-dashed p-8 transition-colors cursor-pointer",
          "hover:border-primary hover:bg-accent/50",
          isDragActive && "border-primary bg-accent/50",
          isDragAccept && "border-green-500 bg-green-50",
          isDragReject && "border-red-500 bg-red-50",
          disabled && "opacity-50 cursor-not-allowed pointer-events-none"
        )}
      >
        <input {...getInputProps()} />
        <Upload className="h-8 w-8 text-primary" />
        <p className="text-sm font-medium">
          {isDragActive ? "Drop files here" : "Drag and drop files here, or click to browse"}
        </p>
      </div>

      {/* Upload Progress */}
      {uploadProgress !== undefined && uploadProgress > 0 && uploadProgress < 100 && (
        <Progress value={uploadProgress} showPercentage label="Uploading..." />
      )}

      {/* Accepted Files List */}
      {showFileList && acceptedFiles.length > 0 && (
        <div className="space-y-2">
          {acceptedFiles.map((file, index) => (
            <div key={index} className="flex items-center gap-3 rounded-lg border p-3">
              <CheckCircle2 className="h-5 w-5 text-green-500" />
              <p className="text-sm font-medium">{file.name}</p>
            </div>
          ))}
        </div>
      )}

      {/* Rejected Files List */}
      {rejectedFiles.length > 0 && (
        <div className="space-y-2">
          {rejectedFiles.map(({ file, errors }, index) => (
            <div key={index} className="flex items-start gap-3 rounded-lg border border-destructive p-3">
              <AlertCircle className="h-5 w-5 text-destructive" />
              <div>
                <p className="text-sm font-medium">{file.name}</p>
                <ul className="text-xs text-destructive">
                  {errors.map((error) => (
                    <li key={error.code}>{error.message}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
```

### Usage Examples

#### PDF Upload (Single File)

```typescript
<FileUploadZone
  onFilesAccepted={(files) => handlePDFUpload(files[0])}
  accept={{ 'application/pdf': ['.pdf'] }}
  maxSize={10 * 1024 * 1024} // 10MB
  maxFiles={1}
  uploadProgress={uploadProgress}
/>
```

#### Document Upload (Multiple Files)

```typescript
<FileUploadZone
  multiple
  maxFiles={5}
  onFilesAccepted={handleMultipleUpload}
  onFilesRejected={(rejections) => {
    toast.error(`${rejections.length} files rejected`)
  }}
  accept={{
    'application/pdf': ['.pdf'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'text/plain': ['.txt'],
  }}
  maxSize={50 * 1024 * 1024} // 50MB for knowledge base docs
/>
```

#### Image Upload

```typescript
<FileUploadZone
  onFilesAccepted={handleImageUpload}
  accept={{
    'image/jpeg': ['.jpg', '.jpeg'],
    'image/png': ['.png'],
    'image/tiff': ['.tif', '.tiff'],
  }}
  maxSize={5 * 1024 * 1024} // 5MB
/>
```

---

## Backend: Multer Configuration

### Standard Multer Configuration

**Location**: `quikadmin/src/api/*.routes.ts`

IntelliFill uses different Multer configurations based on upload type:

#### 1. PDF Form Upload (10MB Limit)

```typescript
import multer from 'multer';
import path from 'path';

// Basic configuration for form PDFs
const upload = multer({
  dest: 'uploads/',
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
  fileFilter: (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();
    if (ext === '.pdf') {
      cb(null, true);
    } else {
      cb(new Error('Only PDF forms are supported'));
    }
  }
});

// Usage in route
router.post('/upload', authenticateSupabase, upload.single('form'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'Form file is required' });
  }

  // File available at req.file.path
  const filePath = req.file.path;
  // Process file...
});
```

#### 2. Knowledge Base Documents (50MB Limit)

```typescript
import multer from 'multer';
import path from 'path';

// Enhanced configuration with custom storage
const storage = multer.diskStorage({
  destination: 'uploads/knowledge/',
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
    const ext = path.extname(file.originalname).toLowerCase();
    cb(null, `knowledge-${uniqueSuffix}${ext}`);
  },
});

const upload = multer({
  storage,
  limits: {
    fileSize: 50 * 1024 * 1024, // 50MB limit for knowledge documents
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['.pdf', '.docx', '.doc', '.txt', '.csv'];
    const ext = path.extname(file.originalname).toLowerCase();
    if (allowedTypes.includes(ext)) {
      cb(null, true);
    } else {
      cb(new Error(`File type ${ext} not supported for knowledge base`));
    }
  },
});

// Usage in route
router.post(
  '/sources/upload',
  authenticateSupabase,
  validateOrganization,
  upload.single('document'),
  async (req: Request, res: Response) => {
    if (!req.file) {
      return res.status(400).json({ error: 'Document file is required' });
    }

    // File metadata
    const { path, originalname, size, mimetype } = req.file;

    // Store in database
    const source = await prisma.documentSource.create({
      data: {
        organizationId: req.organizationId,
        userId: req.user.id,
        title: req.body.title,
        filename: originalname,
        fileSize: size,
        mimeType: mimetype,
        storageUrl: path,
        status: 'PENDING',
      },
    });

    res.status(201).json({ success: true, source });
  }
);
```

#### 3. Memory-Optimized Configuration (Large Files)

```typescript
import multer from 'multer';
import * as fs from 'fs/promises';

// For files that need immediate processing
const upload = multer({
  storage: multer.memoryStorage(), // Store in memory for immediate access
  limits: {
    fileSize: 10 * 1024 * 1024,
    files: 1,
  },
  fileFilter: (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();
    if (['.pdf', '.png', '.jpg'].includes(ext)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'));
    }
  },
});

router.post('/process', upload.single('document'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  // File buffer available at req.file.buffer
  const buffer = req.file.buffer;

  // Process immediately without saving to disk
  const result = await processBuffer(buffer);

  res.json({ success: true, result });
});
```

### Multer Error Handling

```typescript
import { MulterError } from 'multer';

router.post('/upload', upload.single('file'), (err, req, res, next) => {
  if (err instanceof MulterError) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({
        error: 'File too large',
        maxSize: '10MB'
      });
    }
    if (err.code === 'LIMIT_FILE_COUNT') {
      return res.status(400).json({
        error: 'Too many files',
        maxFiles: 5
      });
    }
    return res.status(400).json({ error: err.message });
  }

  if (err) {
    return res.status(400).json({ error: err.message });
  }

  next();
}, async (req, res) => {
  // Normal upload handler
});
```

---

## File Validation & Security

### Comprehensive File Validation Service

**Location**: `quikadmin/src/services/fileValidation.service.ts`

IntelliFill includes a production-ready file validation service:

```typescript
import { FileValidationService } from '@/services/fileValidation.service';

const validationService = new FileValidationService({
  maxFileSize: 10 * 1024 * 1024, // 10MB
  maxPages: 50,
  allowedMimeTypes: [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
  ],
});

// In upload route
router.post('/upload', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  // Read file buffer
  const buffer = await fs.readFile(req.file.path);

  // Validate file
  const validation = await validationService.validateFile(
    buffer,
    req.file.originalname,
    req.file.mimetype
  );

  if (!validation.isValid) {
    // Delete invalid file
    await fs.unlink(req.file.path);
    return res.status(400).json({
      error: 'File validation failed',
      details: validation.errors,
      securityFlags: validation.securityFlags,
    });
  }

  // Log security flags for monitoring
  if (validation.securityFlags.length > 0) {
    logger.warn('File upload security flags', {
      filename: validation.sanitizedFilename,
      flags: validation.securityFlags,
      userId: req.user.id,
    });
  }

  // Proceed with processing
  // Use validation.sanitizedFilename for safe storage
});
```

### Key Validation Features

1. **Magic Number Validation**: Detects actual file type regardless of extension
2. **Path Traversal Prevention**: Sanitizes filenames to prevent directory attacks
3. **PDF Security Scanning**: Detects JavaScript, embedded files, suspicious patterns
4. **MIME Type Verification**: Ensures declared type matches actual content
5. **File Size Limits**: Enforces maximum file sizes
6. **Extension Validation**: Verifies extension matches MIME type

### Security Best Practices

```typescript
// 1. Always sanitize filenames
const sanitizedName = validationService.sanitizeFilename(file.originalname);

// 2. Generate unique filenames to prevent overwrites
const uniqueName = `${Date.now()}-${crypto.randomBytes(8).toString('hex')}-${sanitizedName}`;

// 3. Use file hashing for deduplication
const fileHash = validationService.generateFileHash(buffer);

// 4. Check for path traversal
if (validationService.hasPathTraversal(filename)) {
  throw new Error('Invalid filename: path traversal detected');
}

// 5. Validate against allowed extensions
if (!validationService.validateExtension(filename, 'application/pdf')) {
  throw new Error('File extension does not match PDF type');
}
```

### PDF-Specific Validation

```typescript
// Deep PDF validation
const pdfValidation = await validationService.validatePDF(buffer);

if (!pdfValidation.isValid) {
  logger.error('Dangerous PDF detected', {
    errors: pdfValidation.errors,
    flags: pdfValidation.flags,
  });
  return res.status(400).json({
    error: 'PDF contains potentially dangerous content',
    details: pdfValidation.errors,
  });
}

// Check for specific threats
if (pdfValidation.flags.includes('PDF_CONTAINS_JAVASCRIPT')) {
  // Reject PDFs with JavaScript
  return res.status(400).json({
    error: 'PDFs with JavaScript are not allowed',
  });
}

if (pdfValidation.flags.includes('PDF_HAS_EMBEDDED_FILES')) {
  // Allow but log for monitoring
  logger.warn('PDF contains embedded files', {
    filename: sanitizedName,
    userId: req.user.id,
  });
}
```

---

## Upload Progress Tracking

### Frontend: Progress State Management

```typescript
// Create upload store
import { create } from 'zustand';

interface UploadState {
  progress: number;
  uploading: boolean;
  error: string | null;

  setProgress: (progress: number) => void;
  setUploading: (uploading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

export const useUploadStore = create<UploadState>((set) => ({
  progress: 0,
  uploading: false,
  error: null,

  setProgress: (progress) => set({ progress }),
  setUploading: (uploading) => set({ uploading }),
  setError: (error) => set({ error }),
  reset: () => set({ progress: 0, uploading: false, error: null }),
}));
```

### Frontend: Upload with Progress

```typescript
import axios from 'axios';
import { useUploadStore } from '@/stores/uploadStore';

async function uploadWithProgress(file: File) {
  const { setProgress, setUploading, setError } = useUploadStore.getState();

  const formData = new FormData();
  formData.append('document', file);

  setUploading(true);
  setError(null);
  setProgress(0);

  try {
    const response = await axios.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / (progressEvent.total || 1)
        );
        setProgress(percentCompleted);
      },
    });

    setProgress(100);
    return response.data;
  } catch (error) {
    setError(error.message);
    throw error;
  } finally {
    setUploading(false);
  }
}
```

### Frontend: Progress UI Component

```typescript
function UploadProgress() {
  const { progress, uploading, error } = useUploadStore();

  if (!uploading && progress === 0) return null;

  return (
    <div className="space-y-2">
      {error ? (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : (
        <>
          <Progress value={progress} />
          <p className="text-sm text-muted-foreground">
            Uploading... {progress}%
          </p>
        </>
      )}
    </div>
  );
}
```

### Backend: Processing Status

```typescript
// Update document status during processing
router.get('/documents/:id/status', authenticateSupabase, async (req, res) => {
  const { id } = req.params;
  const userId = req.user.id;

  const document = await prisma.document.findFirst({
    where: { id, userId },
    select: {
      id: true,
      fileName: true,
      status: true,
      confidence: true,
      processedAt: true,
    },
  });

  if (!document) {
    return res.status(404).json({ error: 'Document not found' });
  }

  // Try to find associated job status
  let jobStatus = null;
  try {
    const job = await getJobStatus(id);
    if (job) {
      jobStatus = {
        progress: job.progress,
        state: job.status,
        created: job.created_at,
      };
    }
  } catch (error) {
    logger.warn('Failed to fetch queue status:', error);
  }

  res.json({
    success: true,
    document,
    job: jobStatus,
  });
});
```

---

## Bull Queue Integration

### Document Queue Configuration

**Location**: `quikadmin/src/queues/documentQueue.ts`

```typescript
import Bull from 'bull';
import { logger } from '../utils/logger';

export interface DocumentProcessingJob {
  documentId: string;
  userId: string;
  filePath: string;
  options?: {
    extractTables?: boolean;
    ocrEnabled?: boolean;
    language?: string;
    confidenceThreshold?: number;
  };
}

const redisConfig = {
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
};

// Create document processing queue
export const documentQueue = new Bull<DocumentProcessingJob>('document-processing', {
  redis: redisConfig,
  defaultJobOptions: {
    removeOnComplete: 100, // Keep last 100 completed jobs
    removeOnFail: 50, // Keep last 50 failed jobs
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
  },
});

// Process document jobs
documentQueue.process(async (job) => {
  const { documentId, filePath, options } = job.data;

  try {
    // Update progress
    await job.progress(10);
    logger.info(`Processing document ${documentId}`);

    // Parse document
    await job.progress(30);
    const parsedContent = await parser.parse(filePath);

    // Extract data
    await job.progress(50);
    const extractedData = await extractor.extract(parsedContent);

    // Map fields
    await job.progress(70);
    const mappedFields = await mapper.mapFields(extractedData, []);

    // Complete
    await job.progress(100);

    return {
      documentId,
      status: 'completed',
      extractedData,
      mappedFields,
      processingTime: Date.now() - job.timestamp,
    };
  } catch (error) {
    logger.error(`Failed to process document ${documentId}:`, error);
    throw error;
  }
});

// Event handlers
documentQueue.on('completed', (job, result) => {
  logger.info(`Job ${job.id} completed`, { documentId: result.documentId });
});

documentQueue.on('failed', (job, err) => {
  logger.error(`Job ${job.id} failed:`, err);
});

// Get job status
export async function getJobStatus(jobId: string) {
  const job = await documentQueue.getJob(jobId);

  if (!job) {
    return null;
  }

  return {
    id: job.id,
    type: 'document_processing',
    status: await job.getState(),
    progress: job.progress(),
    created_at: new Date(job.timestamp),
    started_at: job.processedOn ? new Date(job.processedOn) : undefined,
    completed_at: job.finishedOn ? new Date(job.finishedOn) : undefined,
    result: job.returnvalue,
    error: job.failedReason,
  };
}
```

### Adding Jobs to Queue

```typescript
import { documentQueue } from '@/queues/documentQueue';

// In upload route
router.post('/upload', authenticateSupabase, upload.single('document'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  const userId = req.user.id;

  // Validate file
  const buffer = await fs.readFile(req.file.path);
  const validation = await validationService.validateFile(
    buffer,
    req.file.originalname,
    req.file.mimetype
  );

  if (!validation.isValid) {
    await fs.unlink(req.file.path);
    return res.status(400).json({ error: 'Invalid file', details: validation.errors });
  }

  // Create document record
  const document = await prisma.document.create({
    data: {
      userId,
      fileName: validation.sanitizedFilename,
      fileType: validation.detectedMimeType || req.file.mimetype,
      fileSize: req.file.size,
      storageUrl: req.file.path,
      status: 'PENDING',
    },
  });

  // Add to processing queue
  const job = await documentQueue.add({
    documentId: document.id,
    userId,
    filePath: req.file.path,
    options: {
      extractTables: true,
      ocrEnabled: true,
      language: 'eng',
    },
  });

  res.status(201).json({
    success: true,
    document: {
      id: document.id,
      fileName: document.fileName,
      status: document.status,
    },
    job: {
      id: job.id,
      status: 'queued',
    },
    statusUrl: `/api/documents/${document.id}/status`,
  });
});
```

### Batch Processing

```typescript
export const batchQueue = new Bull<BatchProcessingJob>('batch-processing', {
  redis: redisConfig,
  defaultJobOptions: {
    removeOnComplete: 50,
    removeOnFail: 25,
    attempts: 2,
  },
});

interface BatchProcessingJob {
  documentIds: string[];
  userId: string;
  targetFormId?: string;
  options?: {
    parallel?: boolean;
    stopOnError?: boolean;
  };
}

// Process batch jobs
batchQueue.process(async (job) => {
  const { documentIds, userId, options } = job.data;
  const results = [];

  for (let i = 0; i < documentIds.length; i++) {
    const progress = Math.round((i / documentIds.length) * 100);
    await job.progress(progress);

    // Add individual document to processing queue
    const childJob = await documentQueue.add({
      documentId: documentIds[i],
      userId,
      filePath: `pending`, // Fetched from database
      options: {},
    });

    // Wait for completion if not parallel
    if (!options?.parallel) {
      const result = await childJob.finished();
      results.push(result);

      // Stop on error if configured
      if (options?.stopOnError && result.status === 'failed') {
        break;
      }
    } else {
      results.push({ documentId: documentIds[i], jobId: childJob.id });
    }
  }

  await job.progress(100);
  return {
    batchId: job.id,
    documentsProcessed: results.length,
    results,
  };
});
```

---

## Error Handling Patterns

### Frontend Error Handling

```typescript
import { toast } from '@/components/ui/use-toast';

async function handleUpload(files: File[]) {
  const { setUploading, setError, reset } = useUploadStore.getState();

  reset();

  try {
    setUploading(true);

    for (const file of files) {
      const result = await uploadWithProgress(file);

      toast({
        title: 'Upload successful',
        description: `${file.name} uploaded successfully`,
      });
    }
  } catch (error) {
    const message = error.response?.data?.error || error.message || 'Upload failed';

    setError(message);

    toast({
      title: 'Upload failed',
      description: message,
      variant: 'destructive',
    });

    logger.error('Upload error:', error);
  } finally {
    setUploading(false);
  }
}
```

### Backend Error Handling

```typescript
router.post('/upload', authenticateSupabase, upload.single('file'), async (req, res, next) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // Validate file
    const buffer = await fs.readFile(req.file.path);
    const validation = await validationService.validateFile(
      buffer,
      req.file.originalname,
      req.file.mimetype
    );

    if (!validation.isValid) {
      // Cleanup
      await fs.unlink(req.file.path).catch(() => {});

      return res.status(400).json({
        error: 'File validation failed',
        details: validation.errors,
        securityFlags: validation.securityFlags,
      });
    }

    // Process file...

  } catch (error) {
    // Cleanup on error
    if (req.file?.path) {
      await fs.unlink(req.file.path).catch(() => {});
    }

    logger.error('Upload error:', {
      error,
      userId: req.user?.id,
      filename: req.file?.originalname,
    });

    next(error);
  }
});

// Global error handler
app.use((err, req, res, next) => {
  if (err instanceof MulterError) {
    return res.status(400).json({
      error: 'Upload error',
      message: err.message,
      code: err.code,
    });
  }

  if (err.message?.includes('validation')) {
    return res.status(400).json({
      error: 'Validation error',
      message: err.message,
    });
  }

  logger.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});
```

### Queue Error Handling

```typescript
documentQueue.on('failed', async (job, err) => {
  logger.error(`Job ${job.id} failed:`, {
    error: err,
    documentId: job.data.documentId,
    attempts: job.attemptsMade,
  });

  // Update document status
  try {
    await prisma.document.update({
      where: { id: job.data.documentId },
      data: {
        status: 'FAILED',
        errorMessage: err.message,
      },
    });
  } catch (dbError) {
    logger.error('Failed to update document status:', dbError);
  }

  // Notify user via websocket or email
  // await notifyUser(job.data.userId, 'Document processing failed');
});

documentQueue.on('stalled', (job) => {
  logger.warn(`Job ${job.id} stalled`, {
    documentId: job.data.documentId,
  });
});
```

---

## Complete Implementation Examples

### Example 1: Simple PDF Upload Page

```typescript
// pages/Upload.tsx
import { useState } from 'react';
import { FileUploadZone } from '@/components/features/file-upload-zone';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { useUploadStore } from '@/stores/uploadStore';
import { uploadDocument } from '@/services/documentService';

export function UploadPage() {
  const { progress, uploading } = useUploadStore();
  const [uploadedDocs, setUploadedDocs] = useState([]);

  const handleUpload = async (files: File[]) => {
    for (const file of files) {
      const result = await uploadDocument(file);
      setUploadedDocs(prev => [...prev, result]);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <Card>
        <CardHeader>
          <h2 className="text-2xl font-bold">Upload Documents</h2>
        </CardHeader>
        <CardContent>
          <FileUploadZone
            onFilesAccepted={handleUpload}
            accept={{ 'application/pdf': ['.pdf'] }}
            maxSize={10 * 1024 * 1024}
            uploadProgress={progress}
            disabled={uploading}
          />

          {uploadedDocs.length > 0 && (
            <div className="mt-6">
              <h3 className="font-semibold mb-2">Uploaded Documents</h3>
              <ul className="space-y-2">
                {uploadedDocs.map(doc => (
                  <li key={doc.id}>{doc.fileName} - {doc.status}</li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
```

### Example 2: Knowledge Base Upload with Processing

```typescript
// services/knowledgeService.ts
import axios from 'axios';
import { useUploadStore } from '@/stores/uploadStore';

export async function uploadKnowledgeDocument(file: File, title: string) {
  const { setProgress, setUploading, setError } = useUploadStore.getState();

  const formData = new FormData();
  formData.append('document', file);
  formData.append('title', title);

  setUploading(true);
  setError(null);

  try {
    const response = await axios.post('/api/knowledge/sources/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (e) => {
        const percent = Math.round((e.loaded * 100) / (e.total || 1));
        setProgress(percent);
      },
    });

    return response.data;
  } catch (error) {
    setError(error.response?.data?.error || 'Upload failed');
    throw error;
  } finally {
    setUploading(false);
  }
}

// Component
function KnowledgeUpload() {
  const [title, setTitle] = useState('');
  const { progress, uploading, error } = useUploadStore();

  const handleUpload = async (files: File[]) => {
    const file = files[0];

    try {
      const result = await uploadKnowledgeDocument(file, title || file.name);
      toast({ title: 'Upload successful', description: result.message });
    } catch (error) {
      toast({ title: 'Upload failed', variant: 'destructive' });
    }
  };

  return (
    <div className="space-y-4">
      <Input
        placeholder="Document title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <FileUploadZone
        onFilesAccepted={handleUpload}
        accept={{
          'application/pdf': ['.pdf'],
          'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
          'text/plain': ['.txt'],
        }}
        maxSize={50 * 1024 * 1024}
        uploadProgress={progress}
        disabled={uploading || !title}
      />

      {error && <Alert variant="destructive">{error}</Alert>}
    </div>
  );
}
```

---

## Testing Strategies

### Frontend Tests

```typescript
// components/FileUploadZone.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { FileUploadZone } from './file-upload-zone';

describe('FileUploadZone', () => {
  it('accepts valid PDF files', async () => {
    const onFilesAccepted = vi.fn();

    render(
      <FileUploadZone
        onFilesAccepted={onFilesAccepted}
        accept={{ 'application/pdf': ['.pdf'] }}
      />
    );

    const file = new File(['content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText('File upload input');

    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(onFilesAccepted).toHaveBeenCalledWith([file]);
    });
  });

  it('rejects files exceeding size limit', async () => {
    const onFilesRejected = vi.fn();

    render(
      <FileUploadZone
        onFilesAccepted={vi.fn()}
        onFilesRejected={onFilesRejected}
        maxSize={1024} // 1KB
      />
    );

    const largeFile = new File(['x'.repeat(2048)], 'large.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText('File upload input');

    fireEvent.change(input, { target: { files: [largeFile] } });

    await waitFor(() => {
      expect(onFilesRejected).toHaveBeenCalled();
    });
  });
});
```

### Backend Tests

```typescript
// api/documents.routes.test.ts
import request from 'supertest';
import { app } from '../app';
import * as fs from 'fs/promises';

describe('POST /api/documents/upload', () => {
  it('uploads valid PDF file', async () => {
    const response = await request(app)
      .post('/api/documents/upload')
      .set('Authorization', `Bearer ${validToken}`)
      .attach('document', 'test/fixtures/valid.pdf')
      .expect(201);

    expect(response.body.success).toBe(true);
    expect(response.body.document.id).toBeDefined();
  });

  it('rejects non-PDF files', async () => {
    const response = await request(app)
      .post('/api/documents/upload')
      .set('Authorization', `Bearer ${validToken}`)
      .attach('document', 'test/fixtures/test.txt')
      .expect(400);

    expect(response.body.error).toContain('Only PDF forms are supported');
  });

  it('rejects files exceeding size limit', async () => {
    // Create 15MB file (exceeds 10MB limit)
    const largePath = 'test/fixtures/large.pdf';
    await fs.writeFile(largePath, Buffer.alloc(15 * 1024 * 1024));

    const response = await request(app)
      .post('/api/documents/upload')
      .set('Authorization', `Bearer ${validToken}`)
      .attach('document', largePath)
      .expect(400);

    expect(response.body.error).toContain('File too large');

    await fs.unlink(largePath);
  });
});
```

### Validation Service Tests

```typescript
// services/fileValidation.service.test.ts
import { FileValidationService } from '../fileValidation.service';
import * as fs from 'fs/promises';

describe('FileValidationService', () => {
  const service = new FileValidationService();

  it('detects PDF magic numbers', async () => {
    const buffer = await fs.readFile('test/fixtures/valid.pdf');
    const result = await service.validateFile(buffer, 'test.pdf', 'application/pdf');

    expect(result.isValid).toBe(true);
    expect(result.detectedMimeType).toBe('application/pdf');
  });

  it('rejects files with mismatched MIME types', async () => {
    const buffer = Buffer.from('plain text');
    const result = await service.validateFile(buffer, 'fake.pdf', 'application/pdf');

    expect(result.isValid).toBe(false);
    expect(result.securityFlags).toContain('MIME_TYPE_MISMATCH');
  });

  it('sanitizes dangerous filenames', () => {
    const dangerous = '../../../etc/passwd';
    const sanitized = service.sanitizeFilename(dangerous);

    expect(sanitized).not.toContain('..');
    expect(sanitized).not.toContain('/');
  });

  it('detects JavaScript in PDFs', async () => {
    const pdfWithJS = Buffer.from('%PDF-1.4\n/JavaScript (alert(1))');
    const result = await service.validatePDF(pdfWithJS);

    expect(result.isValid).toBe(false);
    expect(result.flags).toContain('PDF_CONTAINS_JAVASCRIPT');
  });
});
```

---

## Key Takeaways

1. **Frontend**: Use `FileUploadZone` component with react-dropzone for consistent UI
2. **Backend**: Configure Multer based on file type and size requirements
3. **Security**: Always validate files with `FileValidationService` before processing
4. **Progress**: Track upload progress with Zustand store and axios `onUploadProgress`
5. **Queues**: Use Bull queues for async processing with progress tracking
6. **Error Handling**: Implement comprehensive error handling at all layers
7. **Testing**: Test validation, upload, and error scenarios

---

## Related Files

**Frontend:**
- `quikadmin-web/src/components/features/file-upload-zone.tsx`
- `quikadmin-web/src/stores/uploadStore.ts`
- `quikadmin-web/src/services/documentService.ts`

**Backend:**
- `quikadmin/src/api/documents.routes.ts`
- `quikadmin/src/api/knowledge.routes.ts`
- `quikadmin/src/services/fileValidation.service.ts`
- `quikadmin/src/queues/documentQueue.ts`

**Configuration:**
- `quikadmin/package.json` (multer, bull dependencies)
- `quikadmin-web/package.json` (react-dropzone dependency)
