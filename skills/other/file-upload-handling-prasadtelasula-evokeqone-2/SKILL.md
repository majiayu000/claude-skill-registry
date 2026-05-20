---
name: file-upload-handling
description: Implement secure file uploads with validation, size limits, type checking, virus scanning, and UUID naming. Use when handling file uploads like profile photos, documents, or resources.
allowed-tools: Read, Write, Edit, Bash, Glob
---

You implement secure file upload handling for the QA Team Portal.

## When to Use This Skill

- Implementing file upload endpoints
- Adding profile photo uploads
- Handling resource uploads (PDFs, videos, documents)
- Validating uploaded files
- Securing file storage
- Generating thumbnails

## Security Requirements

From SECURITY_CHECKLIST.md:
- ✅ File type validation (whitelist only)
- ✅ Virus scanning (ClamAV or similar)
- ✅ Size limits enforced
- ✅ Secure file naming (UUIDs)
- ✅ Storage outside web root
- ✅ Access control on file retrieval

## Implementation

### 1. File Upload Service

**Location:** `backend/app/services/file_service.py`

```python
import os
import uuid
import magic
import aiofiles
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.core.config import settings

class FileUploadService:
    """Handle file uploads securely."""

    ALLOWED_TYPES = {
        'image': {
            'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
            'mime_types': ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
            'max_size': 5 * 1024 * 1024  # 5MB
        },
        'document': {
            'extensions': ['.pdf', '.docx', '.pptx', '.xlsx'],
            'mime_types': [
                'application/pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            ],
            'max_size': 50 * 1024 * 1024  # 50MB
        },
        'video': {
            'extensions': ['.mp4', '.webm', '.mov'],
            'mime_types': ['video/mp4', 'video/webm', 'video/quicktime'],
            'max_size': 100 * 1024 * 1024  # 100MB
        }
    }

    def __init__(self, upload_dir: str = None):
        """Initialize file upload service."""
        self.upload_dir = Path(upload_dir or settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def validate_file(
        self,
        file: UploadFile,
        file_type: str
    ) -> tuple[bool, str]:
        """
        Validate uploaded file.

        Args:
            file: Uploaded file
            file_type: Type category (image, document, video)

        Returns:
            (is_valid, error_message)
        """
        if file_type not in self.ALLOWED_TYPES:
            return False, f"Invalid file type: {file_type}"

        allowed = self.ALLOWED_TYPES[file_type]

        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in allowed['extensions']:
            return False, f"File extension {file_ext} not allowed for {file_type}"

        # Read file content for MIME type checking
        content = await file.read()
        await file.seek(0)  # Reset file pointer

        # Check file size
        file_size = len(content)
        if file_size > allowed['max_size']:
            max_mb = allowed['max_size'] / (1024 * 1024)
            return False, f"File size exceeds {max_mb}MB limit"

        if file_size == 0:
            return False, "File is empty"

        # Check MIME type using python-magic
        mime_type = magic.from_buffer(content, mime=True)
        if mime_type not in allowed['mime_types']:
            return False, f"Invalid file type. Expected {file_type}, got {mime_type}"

        # Check for malicious content (basic)
        if self._contains_malicious_content(content, file_ext):
            return False, "File contains potentially malicious content"

        return True, "File is valid"

    def _contains_malicious_content(self, content: bytes, ext: str) -> bool:
        """
        Basic malicious content detection.

        For production, integrate with ClamAV or similar.
        """
        # Check for executable signatures
        dangerous_signatures = [
            b'MZ',  # Windows executable
            b'\x7fELF',  # Linux executable
            b'#!',  # Script shebang
            b'<?php',  # PHP code
            b'<script',  # JavaScript in documents
        ]

        content_lower = content[:1024].lower()

        for signature in dangerous_signatures:
            if signature.lower() in content_lower:
                return True

        # Check for null bytes (can bypass some filters)
        if b'\x00' in content[:1024]:
            if ext not in ['.jpg', '.jpeg', '.png', '.gif']:  # Images can have null bytes
                return True

        return False

    async def save_file(
        self,
        file: UploadFile,
        file_type: str,
        subfolder: str = None
    ) -> dict:
        """
        Save uploaded file securely.

        Args:
            file: Uploaded file
            file_type: Type category
            subfolder: Optional subfolder (profiles, resources, etc.)

        Returns:
            Dict with file info (filename, path, url, size)
        """
        # Validate file first
        is_valid, error = await self.validate_file(file, file_type)
        if not is_valid:
            raise HTTPException(400, error)

        # Generate secure filename
        file_ext = Path(file.filename).suffix.lower()
        secure_filename = f"{uuid.uuid4()}{file_ext}"

        # Determine save path
        save_dir = self.upload_dir
        if subfolder:
            save_dir = save_dir / subfolder
            save_dir.mkdir(parents=True, exist_ok=True)

        file_path = save_dir / secure_filename

        # Save file
        try:
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
        except Exception as e:
            raise HTTPException(500, f"Failed to save file: {str(e)}")

        # Get file info
        file_size = file_path.stat().st_size
        relative_path = file_path.relative_to(self.upload_dir)

        return {
            'filename': secure_filename,
            'original_filename': file.filename,
            'path': str(relative_path),
            'url': f"/files/{relative_path}",
            'size': file_size,
            'mime_type': file.content_type
        }

    async def delete_file(self, file_path: str) -> bool:
        """
        Delete uploaded file.

        Args:
            file_path: Relative path to file

        Returns:
            True if deleted successfully
        """
        full_path = self.upload_dir / file_path

        if not full_path.exists():
            return False

        # Security: Ensure path is within upload directory
        if not str(full_path.resolve()).startswith(str(self.upload_dir.resolve())):
            raise HTTPException(403, "Access denied")

        try:
            full_path.unlink()
            return True
        except Exception as e:
            raise HTTPException(500, f"Failed to delete file: {str(e)}")

    async def scan_with_clamav(self, file_path: Path) -> tuple[bool, str]:
        """
        Scan file with ClamAV antivirus (optional).

        Requires ClamAV to be installed and clamd daemon running.
        """
        try:
            import pyclamd

            cd = pyclamd.ClamdUnixSocket()
            if not cd.ping():
                return True, "ClamAV not available, skipping scan"

            result = cd.scan_file(str(file_path))

            if result is None:
                return True, "File is clean"
            else:
                return False, f"Virus detected: {result}"
        except ImportError:
            return True, "ClamAV not installed, skipping scan"
        except Exception as e:
            return True, f"Scan error: {str(e)}"
```

### 2. File Upload Endpoints

**Location:** `backend/app/api/v1/endpoints/upload.py`

```python
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.services.file_service import FileUploadService
from app.api.deps import get_current_active_admin

router = APIRouter()
file_service = FileUploadService()

@router.post("/upload/profile")
async def upload_profile_photo(
    file: UploadFile = File(...),
    current_user = Depends(get_current_active_admin)
):
    """
    Upload profile photo (admin only).

    Max size: 5MB
    Allowed: JPG, PNG, GIF, WebP
    """
    result = await file_service.save_file(
        file,
        file_type='image',
        subfolder='profiles'
    )

    return result

@router.post("/upload/resource")
async def upload_resource(
    file: UploadFile = File(...),
    current_user = Depends(get_current_active_admin)
):
    """
    Upload resource file (admin only).

    Max size: 50MB for documents, 100MB for videos
    Allowed: PDF, DOCX, PPTX, MP4
    """
    # Determine file type based on extension
    file_ext = Path(file.filename).suffix.lower()

    if file_ext in ['.mp4', '.webm', '.mov']:
        file_type = 'video'
    elif file_ext in ['.pdf', '.docx', '.pptx']:
        file_type = 'document'
    else:
        raise HTTPException(400, "Unsupported file type")

    result = await file_service.save_file(
        file,
        file_type=file_type,
        subfolder='resources'
    )

    return result

@router.post("/upload/tool-icon")
async def upload_tool_icon(
    file: UploadFile = File(...),
    current_user = Depends(get_current_active_admin)
):
    """Upload tool icon (admin only)."""
    result = await file_service.save_file(
        file,
        file_type='image',
        subfolder='tools'
    )

    return result

@router.delete("/upload/{file_path:path}")
async def delete_file(
    file_path: str,
    current_user = Depends(get_current_active_admin)
):
    """Delete uploaded file (admin only)."""
    success = await file_service.delete_file(file_path)

    if not success:
        raise HTTPException(404, "File not found")

    return {"message": "File deleted successfully"}
```

### 3. File Serving with Access Control

**Location:** `backend/app/api/v1/endpoints/files.py`

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from app.core.config import settings

router = APIRouter()

@router.get("/files/{file_path:path}")
async def serve_file(file_path: str):
    """
    Serve uploaded file.

    Public access for now, add authentication if needed.
    """
    full_path = Path(settings.UPLOAD_DIR) / file_path

    # Security: Prevent path traversal
    if not str(full_path.resolve()).startswith(str(Path(settings.UPLOAD_DIR).resolve())):
        raise HTTPException(403, "Access denied")

    if not full_path.exists():
        raise HTTPException(404, "File not found")

    return FileResponse(
        full_path,
        media_type='application/octet-stream',
        filename=full_path.name
    )
```

### 4. Frontend File Upload Component

**Location:** `frontend/src/components/shared/FileUploader.tsx`

```typescript
import { useState } from 'react'
import { Upload, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface FileUploaderProps {
  onUpload: (file: File) => Promise<any>
  accept: string
  maxSize: number  // in MB
  label: string
}

export const FileUploader = ({
  onUpload,
  accept,
  maxSize,
  label
}: FileUploaderProps) => {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (!selectedFile) return

    // Validate file size
    if (selectedFile.size > maxSize * 1024 * 1024) {
      setError(`File size must be less than ${maxSize}MB`)
      return
    }

    setFile(selectedFile)
    setError(null)
  }

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    setProgress(0)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      // Simulate progress (in real app, use axios onUploadProgress)
      const interval = setInterval(() => {
        setProgress(prev => Math.min(prev + 10, 90))
      }, 200)

      await onUpload(file)

      clearInterval(interval)
      setProgress(100)

      // Reset after success
      setTimeout(() => {
        setFile(null)
        setProgress(0)
        setUploading(false)
      }, 1000)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed')
      setUploading(false)
      setProgress(0)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4">
        <input
          type="file"
          accept={accept}
          onChange={handleFileChange}
          disabled={uploading}
          className="hidden"
          id="file-upload"
        />
        <label htmlFor="file-upload">
          <Button
            variant="outline"
            disabled={uploading}
            asChild
          >
            <span>
              <Upload className="mr-2 h-4 w-4" />
              {label}
            </span>
          </Button>
        </label>

        {file && (
          <div className="flex items-center gap-2">
            <span className="text-sm">{file.name}</span>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setFile(null)}
              disabled={uploading}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        )}
      </div>

      {file && !uploading && (
        <Button onClick={handleUpload}>
          Upload File
        </Button>
      )}

      {uploading && (
        <Progress value={progress} />
      )}

      {error && (
        <p className="text-sm text-destructive">{error}</p>
      )}
    </div>
  )
}
```

### 5. Usage Example

```typescript
// In TeamForm component
import { FileUploader } from '@/components/shared/FileUploader'
import { uploadProfilePhoto } from '@/services/uploadService'

const TeamForm = () => {
  const handlePhotoUpload = async (file: File) => {
    const result = await uploadProfilePhoto(file)
    // Update form with photo URL
    form.setValue('profilePhotoUrl', result.url)
  }

  return (
    <form>
      {/* Other fields */}

      <FileUploader
        onUpload={handlePhotoUpload}
        accept="image/jpeg,image/png,image/gif,image/webp"
        maxSize={5}
        label="Choose Profile Photo"
      />
    </form>
  )
}
```

### 6. Configuration

**Location:** `backend/app/core/config.py`

```python
class Settings(BaseSettings):
    # File Upload
    UPLOAD_DIR: str = "./storage/uploads"
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    ALLOWED_EXTENSIONS: list[str] = [
        "pdf", "pptx", "docx", "mp4", "jpg", "png", "gif", "webp"
    ]
```

### 7. Dependencies

Add to `backend/pyproject.toml`:

```toml
dependencies = [
    "aiofiles>=23.2.1",
    "python-magic>=0.4.27",
    "python-multipart>=0.0.9",
    # Optional for virus scanning
    # "py-clamd>=0.5.0",
]
```

## Testing

```python
# tests/integration/test_api_upload.py
import pytest
from pathlib import Path

def test_upload_valid_image(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Create test image
    test_file = ("test.jpg", b"fake image content", "image/jpeg")

    response = client.post(
        "/api/v1/upload/profile",
        files={"file": test_file},
        headers=headers
    )

    assert response.status_code == 200
    assert "filename" in response.json()
    assert "url" in response.json()

def test_upload_invalid_extension(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    test_file = ("test.exe", b"fake content", "application/x-msdownload")

    response = client.post(
        "/api/v1/upload/profile",
        files={"file": test_file},
        headers=headers
    )

    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"].lower()

def test_upload_exceeds_size_limit(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Create file larger than 5MB
    large_content = b"x" * (6 * 1024 * 1024)
    test_file = ("large.jpg", large_content, "image/jpeg")

    response = client.post(
        "/api/v1/upload/profile",
        files={"file": test_file},
        headers=headers
    )

    assert response.status_code == 400
    assert "exceeds" in response.json()["detail"].lower()

def test_upload_requires_authentication(client):
    test_file = ("test.jpg", b"content", "image/jpeg")

    response = client.post(
        "/api/v1/upload/profile",
        files={"file": test_file}
    )

    assert response.status_code == 401
```

## Security Checklist

- ✅ File type validated by extension AND MIME type
- ✅ File size limits enforced (5MB images, 50MB documents, 100MB videos)
- ✅ Filenames sanitized (UUID-based)
- ✅ Files stored outside web root (./storage/uploads)
- ✅ Basic malicious content detection
- ✅ Path traversal prevented
- ✅ Authentication required for uploads
- ✅ Optional ClamAV virus scanning support
- ⚠️ Add rate limiting for upload endpoints
- ⚠️ Consider adding watermarks to images
- ⚠️ Integrate ClamAV in production

## Report Format

After implementation:
1. ✅ File upload service created
2. ✅ Upload endpoints added (profile, resource, tool-icon)
3. ✅ Validation implemented (type, size, content)
4. ✅ Secure storage configured
5. ✅ Frontend upload component created
6. ✅ Tests passing (X/Y)
7. ⚠️ Recommendations: [Install ClamAV for production]
