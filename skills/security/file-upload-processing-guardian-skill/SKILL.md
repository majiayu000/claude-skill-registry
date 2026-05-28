---
name: file-upload-processing-guardian
description: Offensive file upload and processing security and reliability enforcement. Triggered when implementing file uploads, reviewing Multer configuration, debugging upload failures, validating file types, or optimizing storage. Scans for security vulnerabilities, file size exploits, MIME type spoofing, path traversal, and storage efficiency issues. Produces auto-scan reports with security hardening recommendations.
---

# File Upload & Processing Guardian

**Mission:** Prevent file upload vulnerabilities and ensure reliable file processing through proactive security scanning and best practice enforcement. This skill operates in **offensive mode** - finding potential exploits and optimization opportunities before they cause issues.

## Activation Triggers

- Implementing file upload endpoints
- "File upload not working"
- MIME type validation errors
- File size limit exceeded errors
- Storage path configuration
- Multer middleware setup
- CloudConvert integration issues
- Temporary file cleanup problems
- Path traversal vulnerability review
- Production file upload deployment

## Tech Stack Awareness

This skill is specialized for **PDFLab's tech stack**:

- **Express.js** with TypeScript
- **Multer** for multipart/form-data handling
- **CloudConvert API v3** for PDF processing
- **Local file storage** (backend/storage/)
- **Bull queue** for async processing
- **1-hour auto-cleanup** for temporary files

## Scan Methodology

### 1. Initial Context Gathering

**Ask if not provided:**
- "Show me your Multer configuration"
- "What file types are you accepting?"
- "What's the maximum file size?"
- "Where are files stored?"
- "How are files cleaned up?"
- "Is this for guest or authenticated users?"

### 2. Critical Security Scan

Execute ALL checks in this section. Each is based on real security incidents.

#### 🔴 CRITICAL: File Type Validation

**Historical Vulnerability:** Malicious file upload bypassing MIME type checks

**Scan for:**
- [ ] MIME type whitelist (not blacklist)
- [ ] File extension validation
- [ ] Magic number verification (first bytes of file)
- [ ] Content-Type header validation
- [ ] File signature verification for PDFs

**Red flags:**
```typescript
// ❌ Accepting all file types
const upload = multer({ dest: 'uploads/' })  // No filter!

// ❌ Trusting client-provided MIME type only
fileFilter: (req, file, cb) => {
  if (file.mimetype === 'application/pdf') {
    cb(null, true)  // Error! Client can fake this
  }
}

// ❌ Extension blacklist (bypass via double extension)
if (filename.endsWith('.exe') || filename.endsWith('.sh')) {
  reject()  // Error! Can use .pdf.exe
}

// ❌ No validation at all
app.post('/upload', upload.single('file'), (req, res) => {
  // req.file saved without validation!
})
```

**Hardening:**
```typescript
// ✅ Whitelist MIME types + extension check
import path from 'path'

const ALLOWED_MIME_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // DOCX
  'application/vnd.openxmlformats-officedocument.presentationml.presentation', // PPTX
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' // XLSX
]

const ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.pptx', '.xlsx']

const fileFilter = (
  req: Request,
  file: Express.Multer.File,
  cb: multer.FileFilterCallback
) => {
  // 1. Check MIME type
  if (!ALLOWED_MIME_TYPES.includes(file.mimetype)) {
    return cb(new Error(`Invalid file type: ${file.mimetype}`))
  }

  // 2. Check extension
  const ext = path.extname(file.originalname).toLowerCase()
  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    return cb(new Error(`Invalid file extension: ${ext}`))
  }

  // 3. Check filename for path traversal
  if (file.originalname.includes('..') || file.originalname.includes('/')) {
    return cb(new Error('Invalid filename'))
  }

  cb(null, true)
}

const upload = multer({
  storage: diskStorage,
  fileFilter,
  limits: { fileSize: 500 * 1024 * 1024 } // 500MB max
})

// ✅ Additional: Magic number verification (PDF signature)
import fs from 'fs/promises'

async function verifyPdfSignature(filepath: string): Promise<boolean> {
  const buffer = await fs.readFile(filepath, { encoding: 'binary', start: 0, end: 4 })
  return buffer === '%PDF'  // PDF magic number
}

// After upload, verify:
const isPdf = await verifyPdfSignature(req.file.path)
if (!isPdf) {
  await fs.unlink(req.file.path)  // Delete fake file
  throw new Error('File is not a valid PDF')
}
```

**PDF-specific signatures:**
- PDF: `%PDF` (first 4 bytes)
- DOCX: `PK` (ZIP signature, first 2 bytes)
- XLSX: `PK` (ZIP signature)
- PPTX: `PK` (ZIP signature)

#### 🔴 CRITICAL: Path Traversal Prevention

**Historical Vulnerability:** Attacker uploads file with `../../../etc/passwd` filename

**Scan for:**
- [ ] Filename sanitization
- [ ] Custom filename generation (UUIDs)
- [ ] Directory traversal patterns (`..`, `/`, `\`)
- [ ] Absolute paths in upload destination
- [ ] symlink attacks

**Red flags:**
```typescript
// ❌ Using original filename without sanitization
const storage = multer.diskStorage({
  destination: 'uploads/',
  filename: (req, file, cb) => {
    cb(null, file.originalname)  // Error! Path traversal risk
  }
})

// ❌ Relative path in destination
destination: './uploads'  // Error! Can change if cwd changes

// ❌ User-controlled subdirectory
destination: `uploads/${req.body.userId}/`  // Error! req.body.userId = '../../../tmp'
```

**Hardening:**
```typescript
// ✅ UUID-based filenames + sanitized original name
import { v4 as uuidv4 } from 'uuid'
import path from 'path'
import sanitize from 'sanitize-filename'

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // Use absolute path
    const uploadDir = path.join(__dirname, '../../storage/uploads')
    cb(null, uploadDir)
  },
  filename: (req, file, cb) => {
    // Generate safe filename: uuid-sanitized-original.ext
    const sanitizedName = sanitize(file.originalname)
    const ext = path.extname(sanitizedName)
    const basename = path.basename(sanitizedName, ext)
    const safeFilename = `${uuidv4()}-${basename}${ext}`
    cb(null, safeFilename)
  }
})

// ✅ User-specific directory with validation
import fs from 'fs/promises'

async function getUserUploadDir(userId: string): Promise<string> {
  // Validate userId is UUID (no path traversal)
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(userId)) {
    throw new Error('Invalid user ID')
  }

  const baseDir = path.join(__dirname, '../../storage/uploads')
  const userDir = path.join(baseDir, userId)

  // Create directory if doesn't exist
  await fs.mkdir(userDir, { recursive: true })

  return userDir
}
```

#### 🔴 CRITICAL: File Size Limits & DoS Prevention

**Historical Vulnerability:** Attacker uploads 10GB file, crashes server

**Scan for:**
- [ ] Global file size limit (Multer)
- [ ] Per-user plan limits (Free: 10MB, Pro: 100MB, Enterprise: 500MB)
- [ ] Total upload size limit (multiple files)
- [ ] Request body size limit (Express)
- [ ] Rate limiting on upload endpoint
- [ ] Disk space monitoring

**Red flags:**
```typescript
// ❌ No file size limit
const upload = multer({ dest: 'uploads/' })  // No limits!

// ❌ Too large global limit
limits: { fileSize: 10 * 1024 * 1024 * 1024 }  // 10GB! DoS risk

// ❌ No per-user plan enforcement
// Free user can upload 500MB files

// ❌ No rate limiting
app.post('/upload', upload.single('file'), handler)  // Can spam uploads
```

**Hardening:**
```typescript
// ✅ Plan-based file size limits
import { User, UserPlan } from '@/models/User'

function getMaxFileSize(plan: UserPlan): number {
  switch (plan) {
    case UserPlan.FREE: return 10 * 1024 * 1024       // 10MB
    case UserPlan.STARTER: return 25 * 1024 * 1024    // 25MB
    case UserPlan.PRO: return 100 * 1024 * 1024       // 100MB
    case UserPlan.ENTERPRISE: return 500 * 1024 * 1024 // 500MB
    default: return 10 * 1024 * 1024
  }
}

// ✅ Dynamic Multer instance with user plan
export function createUploadMiddleware(user: User) {
  const maxFileSize = getMaxFileSize(user.plan)

  return multer({
    storage: diskStorage,
    fileFilter,
    limits: {
      fileSize: maxFileSize,
      files: 1  // Single file upload
    }
  })
}

// Usage
app.post('/upload', authMiddleware, async (req, res, next) => {
  const user = req.user as User
  const upload = createUploadMiddleware(user).single('file')

  upload(req, res, (err) => {
    if (err instanceof multer.MulterError) {
      if (err.code === 'LIMIT_FILE_SIZE') {
        const maxSize = getMaxFileSize(user.plan)
        return res.status(413).json({
          error: 'File too large',
          maxSize,
          userPlan: user.plan
        })
      }
    }
    next(err)
  })
})

// ✅ Express body size limit
import express from 'express'

app.use(express.json({ limit: '10mb' }))  // Prevent JSON DoS
app.use(express.urlencoded({ extended: true, limit: '10mb' }))

// ✅ Rate limiting
import rateLimit from 'express-rate-limit'

const uploadLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 50,  // 50 uploads per 15 min
  message: 'Too many uploads, please try again later'
})

app.post('/upload', uploadLimiter, authMiddleware, uploadHandler)

// ✅ Disk space monitoring
import checkDiskSpace from 'check-disk-space'

async function checkStorageSpace(): Promise<void> {
  const diskSpace = await checkDiskSpace('/var/storage')
  const freeSpaceGB = diskSpace.free / (1024 * 1024 * 1024)

  if (freeSpaceGB < 5) {  // Less than 5GB free
    console.error('⚠️ Low disk space:', freeSpaceGB.toFixed(2), 'GB')
    // Send alert to monitoring system
  }
}

// Run every hour
setInterval(checkStorageSpace, 60 * 60 * 1000)
```

#### 🟡 HIGH: Temporary File Cleanup

**Historical Issue:** Disk filled with orphaned temp files (cleanup job failed)

**Scan for:**
- [ ] Automatic cleanup job (Bull queue or cron)
- [ ] Cleanup on upload failure
- [ ] Cleanup on conversion completion
- [ ] Expires_at timestamp on jobs
- [ ] Orphaned file detection
- [ ] Cleanup logs and monitoring

**Red flags:**
```typescript
// ❌ No cleanup on error
app.post('/upload', upload.single('file'), async (req, res) => {
  try {
    await processFile(req.file.path)
  } catch (error) {
    res.status(500).json({ error })
    // File left on disk!
  }
})

// ❌ Manual cleanup (not reliable)
// "Remember to delete files older than 1 hour"
// (Never happens in practice)

// ❌ No orphaned file detection
// Files without database records accumulate
```

**Hardening:**
```typescript
// ✅ Cleanup on error
import fs from 'fs/promises'

app.post('/upload', upload.single('file'), async (req, res) => {
  try {
    await processFile(req.file.path)
  } catch (error) {
    // Clean up on error
    await fs.unlink(req.file.path).catch(console.error)
    res.status(500).json({ error })
  }
})

// ✅ Automatic cleanup job (Bull queue)
// backend/src/jobs/cleanup.job.ts
import { Queue, Worker } from 'bullmq'
import { ConversionJob, JobStatus } from '@/models/ConversionJob'
import { Op } from 'sequelize'
import fs from 'fs/promises'
import path from 'path'

const cleanupQueue = new Queue('cleanup', {
  connection: redisConnection
})

// Schedule cleanup every hour
cleanupQueue.add(
  'cleanup-expired-files',
  {},
  { repeat: { every: 60 * 60 * 1000 } }  // 1 hour
)

const cleanupWorker = new Worker('cleanup', async (job) => {
  console.log('🧹 Running file cleanup job...')

  // 1. Find expired jobs (created > 1 hour ago)
  const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000)
  const expiredJobs = await ConversionJob.findAll({
    where: {
      created_at: { [Op.lt]: oneHourAgo },
      status: { [Op.in]: [JobStatus.COMPLETED, JobStatus.FAILED] }
    }
  })

  let deletedFiles = 0
  let deletedSize = 0

  for (const job of expiredJobs) {
    try {
      // Delete input file
      if (job.input_file) {
        const stat = await fs.stat(job.input_file)
        await fs.unlink(job.input_file)
        deletedSize += stat.size
        deletedFiles++
      }

      // Delete output file
      if (job.output_file) {
        const stat = await fs.stat(job.output_file)
        await fs.unlink(job.output_file)
        deletedSize += stat.size
        deletedFiles++
      }

      // Delete job from database
      await job.destroy()
    } catch (error) {
      console.error(`Failed to clean up job ${job.id}:`, error)
    }
  }

  console.log(`✅ Cleanup complete: ${deletedFiles} files, ${(deletedSize / 1024 / 1024).toFixed(2)} MB`)
  return { deletedFiles, deletedSize }
}, { connection: redisConnection })

// ✅ Orphaned file detection
async function findOrphanedFiles(): Promise<string[]> {
  const uploadDir = path.join(__dirname, '../../storage/uploads')
  const allFiles = await fs.readdir(uploadDir, { recursive: true })

  const orphanedFiles: string[] = []

  for (const file of allFiles) {
    const fullPath = path.join(uploadDir, file)

    // Check if file exists in database
    const jobWithFile = await ConversionJob.findOne({
      where: {
        [Op.or]: [
          { input_file: fullPath },
          { output_file: fullPath }
        ]
      }
    })

    if (!jobWithFile) {
      orphanedFiles.push(fullPath)
    }
  }

  return orphanedFiles
}

// Run weekly
setInterval(async () => {
  const orphaned = await findOrphanedFiles()
  console.log(`Found ${orphaned.length} orphaned files`)
  // Delete or alert
}, 7 * 24 * 60 * 60 * 1000)
```

#### 🟡 HIGH: CloudConvert Integration (SDK DOWNLOAD METHOD DOESN'T WORK)

**Historical Issue:** CloudConvert SDK download method failed in production - "Download not available" errors (Oct 2025)

**Production Lesson Learned**: CloudConvert SDK's `job.wait()` and download methods don't work as documented. SDK download method is not available in the API. Must use native Node.js `https.get()` to download files from export task URL.

**⚠️ CRITICAL: CloudConvert SDK Download Workaround (MANDATORY)**

**CloudConvert SDK Limitations:**
```typescript
// ❌ DOESN'T WORK: SDK download method (not in official API)
const download = await job.wait();
const stream = cloudConvert.download(download.url);
// Error: download() method doesn't exist in SDK

// ❌ DOESN'T WORK: Direct file access
const file = exportTask.result.files[0];
const fileContent = await cloudConvert.download(file.id);
// Error: No download method available

// ✅ WORKS: Native HTTPS request to export URL
import https from 'https';
import fs from 'fs';

const exportTask = completedJob.tasks.find(t => t.name === 'export-my-file');
const fileUrl = exportTask.result.files[0].url;  // HTTPS URL from CloudConvert

const outputPath = inputPath.replace('.pdf', `.${outputFormat}`);
const fileStream = fs.createWriteStream(outputPath);

https.get(fileUrl, (response) => {
  response.pipe(fileStream);
  fileStream.on('finish', () => {
    fileStream.close();
    console.log('✅ File downloaded successfully');
  });
}).on('error', (err) => {
  fs.unlink(outputPath);  // Delete partial file
  throw new Error(`Download failed: ${err.message}`);
});
```

**Scan for:**
- [ ] **CRITICAL: NOT using SDK download method (it doesn't exist)**
- [ ] **CRITICAL: Using native https.get() for file downloads**
- [ ] API key validation
- [ ] Sandbox vs production mode (CLOUDCONVERT_SANDBOX=false)
- [ ] Error handling for all CloudConvert operations
- [ ] Webhook signature verification
- [ ] Job timeout handling (max 10 minutes)
- [ ] Retry logic for transient failures
- [ ] File download error handling (partial files)

**Red flags that WILL cause production failure:**
- ❌ Using `cloudConvert.download()` method (doesn't exist)
- ❌ No error handling for API calls
- ❌ Waiting forever for job (no timeout)
- ❌ Using sandbox in production
- ❌ No webhook signature verification
- ❌ No download error handling (partial files left on disk)

**Before vs After (Real Production Issue):**
```typescript
// ❌ BROKEN: Tried using SDK download method
const job = await cloudconvert.jobs.wait(jobId);
const download = await job.download();  // Error: Method doesn't exist
// Result: All conversions failing with "Download not available"

// ✅ FIXED: Using native HTTPS download
const exportTask = job.tasks.find(t => t.operation === 'export/url');
const fileUrl = exportTask.result.files[0].url;

await new Promise((resolve, reject) => {
  https.get(fileUrl, (response) => {
    const fileStream = fs.createWriteStream(outputPath);
    response.pipe(fileStream);
    fileStream.on('finish', () => {
      fileStream.close();
      resolve(outputPath);
    });
  }).on('error', reject);
});
// Result: Downloads working, conversions successful
```

**Hardening:**
```typescript
// ✅ Comprehensive error handling
import CloudConvert from 'cloudconvert'

export class CloudConvertService {
  private client: CloudConvert

  constructor() {
    const apiKey = process.env.CLOUDCONVERT_API_KEY
    if (!apiKey) {
      throw new Error('CLOUDCONVERT_API_KEY not set')
    }

    this.client = new CloudConvert(apiKey, false)  // Production mode
  }

  async convertPdf(
    inputPath: string,
    outputFormat: 'pptx' | 'docx' | 'xlsx' | 'png',
    jobId: string
  ): Promise<string> {
    try {
      // 1. Create job with timeout
      const job = await Promise.race([
        this.client.jobs.create({
          tasks: {
            'import-my-file': {
              operation: 'import/upload'
            },
            'convert-my-file': {
              operation: 'convert',
              input: 'import-my-file',
              output_format: outputFormat,
              engine: 'office',  // Best for PDF conversion
              pdf_a: false
            },
            'export-my-file': {
              operation: 'export/url',
              input: 'convert-my-file'
            }
          },
          tag: jobId  // Track job in CloudConvert
        }),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('CloudConvert job creation timeout')), 30000)
        )
      ]) as any

      // 2. Upload file
      const uploadTask = job.tasks.find((t: any) => t.name === 'import-my-file')
      await this.client.tasks.upload(uploadTask, fs.createReadStream(inputPath))

      // 3. Wait for completion with timeout (max 10 minutes)
      const completedJob = await Promise.race([
        this.client.jobs.wait(job.id),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('CloudConvert job timeout')), 10 * 60 * 1000)
        )
      ]) as any

      // 4. Download result
      const exportTask = completedJob.tasks.find((t: any) => t.name === 'export-my-file')
      const fileUrl = exportTask.result.files[0].url

      const outputPath = inputPath.replace('.pdf', `.${outputFormat}`)
      await this.downloadFile(fileUrl, outputPath)

      return outputPath
    } catch (error) {
      console.error('CloudConvert error:', error)

      // Retry logic for transient errors
      if (error.code === 'ECONNRESET' || error.code === 'ETIMEDOUT') {
        console.log('Retrying CloudConvert job...')
        return this.convertPdf(inputPath, outputFormat, jobId)  // Retry once
      }

      throw new Error(`CloudConvert conversion failed: ${error.message}`)
    }
  }

  private async downloadFile(url: string, outputPath: string): Promise<void> {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`Download failed: ${response.statusText}`)
    }

    const buffer = await response.arrayBuffer()
    await fs.writeFile(outputPath, Buffer.from(buffer))
  }
}

// ✅ Webhook signature verification
import crypto from 'crypto'

app.post('/webhook/cloudconvert', (req, res) => {
  const signature = req.headers['cloudconvert-signature'] as string
  const signingSecret = process.env.CLOUDCONVERT_WEBHOOK_SECRET

  // Verify signature
  const expectedSignature = crypto
    .createHmac('sha256', signingSecret)
    .update(JSON.stringify(req.body))
    .digest('hex')

  if (signature !== expectedSignature) {
    return res.status(401).json({ error: 'Invalid signature' })
  }

  // Process webhook
  const { event, job } = req.body
  if (event === 'job.finished') {
    // Update job status in database
  }

  res.status(200).send('OK')
})
```

#### 🟠 MEDIUM: File Download Security

**Historical Issue:** Users downloading other users' files via job ID guessing

**Scan for:**
- [ ] Ownership verification before download
- [ ] Signed URLs with expiration
- [ ] Content-Disposition header (force download)
- [ ] MIME type verification
- [ ] Rate limiting on downloads

**Red flags:**
```typescript
// ❌ No ownership check
app.get('/download/:jobId', async (req, res) => {
  const job = await ConversionJob.findByPk(req.params.jobId)
  res.download(job.output_file)  // Anyone can download any job!
})

// ❌ Inline display of potentially dangerous files
res.setHeader('Content-Disposition', 'inline')  // Opens in browser

// ❌ No expiration on download links
// Links work forever → can share publicly
```

**Hardening:**
```typescript
// ✅ Ownership verification + signed URLs
import jwt from 'jsonwebtoken'

// Generate signed download URL (expires in 1 hour)
export function generateDownloadUrl(jobId: string, userId: string): string {
  const token = jwt.sign(
    { jobId, userId },
    process.env.JWT_SECRET!,
    { expiresIn: '1h' }
  )
  return `/api/download/${jobId}?token=${token}`
}

// Download endpoint with verification
app.get('/download/:jobId', async (req, res) => {
  try {
    // 1. Verify token
    const token = req.query.token as string
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as { jobId: string, userId: string }

    // 2. Verify job ownership
    const job = await ConversionJob.findByPk(req.params.jobId)
    if (!job || job.user_id !== decoded.userId) {
      return res.status(403).json({ error: 'Forbidden' })
    }

    // 3. Verify file exists
    if (!job.output_file || !(await fs.access(job.output_file).then(() => true).catch(() => false))) {
      return res.status(404).json({ error: 'File not found' })
    }

    // 4. Force download (not inline)
    res.setHeader('Content-Disposition', `attachment; filename="${job.file_name}"`)
    res.setHeader('Content-Type', getMimeType(job.output_file))

    // 5. Stream file
    const stream = fs.createReadStream(job.output_file)
    stream.pipe(res)
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Download link expired' })
    }
    res.status(500).json({ error: 'Download failed' })
  }
})

function getMimeType(filename: string): string {
  const ext = path.extname(filename).toLowerCase()
  const mimeTypes: Record<string, string> = {
    '.pdf': 'application/pdf',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.png': 'image/png'
  }
  return mimeTypes[ext] || 'application/octet-stream'
}
```

### 3. Production Readiness Checklist

Generate this checklist in the auto-scan report:

```
FILE UPLOAD SECURITY SCORE: X/10

✅ MIME type + extension + magic number validation
✅ Path traversal prevention (UUIDs + sanitization)
✅ File size limits enforced (plan-based)
✅ Rate limiting on upload endpoint
✅ Automatic cleanup job (1-hour retention)
✅ Ownership verification on downloads
⚠️  Missing: Disk space monitoring
⚠️  Missing: Orphaned file detection
❌ Critical: No CloudConvert timeout handling
❌ Security: Download URLs don't expire

RISK LEVEL: [LOW/MEDIUM/HIGH/CRITICAL]
BLOCKERS: X critical issues must be resolved
OPTIMIZATIONS: Y efficiency wins available
```

## Output Format: Auto-Scan Report

```
═══════════════════════════════════════════════
🛡️ FILE UPLOAD & PROCESSING GUARDIAN - SCAN RESULTS
═══════════════════════════════════════════════

📊 SCAN SCOPE
• Multer version: 1.4.5-lts.1
• Storage: Local disk (backend/storage/)
• Max file size: 500MB (Enterprise plan)
• Allowed types: PDF, DOCX, PPTX, XLSX
• Cleanup: 1-hour auto-delete

🚨 CRITICAL FINDINGS: [count]

⚠️  HIGH PRIORITY: [count]

💡 OPTIMIZATIONS: [count]

🔐 SECURITY AUDIT:
✅ File type validation: MIME + extension + magic number
✅ Path traversal: UUID filenames + sanitization
✅ Size limits: Plan-based enforcement
❌ Download security: No expiration on URLs
⚠️  Rate limiting: Upload endpoint limited (50/15min)

⚡ STORAGE EFFICIENCY:
Current usage: 2.3 GB
Cleanup frequency: Every 1 hour
Average retention: 45 minutes
Orphaned files: 0

═══════════════════════════════════════════════
FINAL VERDICT
═══════════════════════════════════════════════
Production Ready: [YES/NO/BLOCKED]
Risk Level: [LOW/MEDIUM/HIGH/CRITICAL]
Estimated Fix Time: [X hours]

NEXT ACTIONS:
1. [Most critical fix]
2. [Second priority]
3. [Optional optimization]

═══════════════════════════════════════════════
```

## Key Principles

1. **Defense in depth:** Multiple validation layers (MIME + extension + magic number)
2. **Never trust client input:** Filenames, MIME types, sizes all can be spoofed
3. **Plan-based limits:** Free ≠ Enterprise, enforce quota
4. **Automatic cleanup:** Don't rely on manual deletion
5. **Ownership verification:** Users can only access their own files
6. **Expiring download URLs:** Time-limited access with JWT

## Quick Reference: Common Fixes

```bash
# Install dependencies
npm install multer sanitize-filename check-disk-space

# Check disk usage
df -h /var/storage

# Find large files
find backend/storage -type f -size +100M

# Count orphaned files
find backend/storage -type f -mtime +1  # Older than 1 day

# Test CloudConvert API
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.cloudconvert.com/v2/users/me
```

## PDFLab-Specific Patterns

**backend/src/middleware/upload.middleware.ts:**
- Use `createUploadMiddleware(user)` for plan-based limits
- Apply fileFilter for MIME + extension validation
- Use UUID filenames in user-specific directories

**backend/src/jobs/cleanup.job.ts:**
- Run every hour via Bull queue
- Delete files older than 1 hour
- Log cleanup metrics (files deleted, size freed)

**backend/src/services/cloudconvert.service.ts:**
- Wrap all CloudConvert calls in try/catch
- Add 10-minute timeout on job.wait()
- Retry transient errors once
- Use production mode (CLOUDCONVERT_SANDBOX=false)

**backend/src/controllers/conversion.controller.ts:**
- Verify ownership before download
- Generate signed URLs with 1-hour expiration
- Force download with Content-Disposition: attachment
- Stream files instead of res.sendFile()
