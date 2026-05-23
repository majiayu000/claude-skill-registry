---
name: file-uploads
description: Production-grade secure file upload pipeline with multi-stage validation, malware scanning (ClamAV), hash-based duplicate detection, and race condition protection using distributed locks.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: security
  time: 6h
  source: drift-masterguide
---

# Secure Upload Pipeline

Production-grade file upload handling with validation, malware scanning, and duplicate detection.

## When to Use This Skill

- Building file upload endpoints that handle untrusted input
- Need malware scanning before processing files
- Want to prevent duplicate file processing
- Handling concurrent uploads of the same file

## Core Concepts

File uploads are attack vectors. The solution is a multi-stage validation pipeline that fails fast and checks cheap things first:

```
Upload Request
    ↓
[1] Size + Type Check (instant)
    ↓
[2] Content Signature Validation (ms)
    ↓
[3] Malware Scan - ClamAV (50-200ms)
    ↓
[4] Hash-Based Duplicate Check (ms)
    ↓
[5] Race Condition Lock (Redis)
    ↓
[6] Upload to Storage
    ↓
[7] Clear Lock + Return URL
```

Key principle: Check limits BEFORE upload to prevent wasted processing.

## Implementation

### Python (FastAPI)

```python
import hashlib
from typing import Optional, Dict
from fastapi import UploadFile, HTTPException

class FileValidator:
    def __init__(self):
        self.max_size = 10 * 1024 * 1024  # 10MB
        self.allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
        self.malware_scanner = MalwareScannerService()
    
    async def validate_file(self, file: UploadFile) -> Dict:
        """Multi-stage file validation"""
        validation_details = {
            "filename": file.filename,
            "content_type": file.content_type,
            "checks_passed": []
        }
        
        # Check 1: File size (before reading content)
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > self.max_size:
            return {
                "valid": False,
                "error": f"File too large ({file_size / 1024 / 1024:.1f}MB). Max 10MB.",
                "validation_details": validation_details
            }
        
        if file_size == 0:
            return {"valid": False, "error": "File is empty."}
        
        validation_details["checks_passed"].append("size_check")
        
        # Check 2: MIME type
        if file.content_type not in self.allowed_types:
            return {
                "valid": False,
                "error": f"Invalid file type ({file.content_type})."
            }
        
        validation_details["checks_passed"].append("type_check")
        
        # Check 3: Content signature (PDF magic bytes)
        if file.content_type == 'application/pdf':
            header = await file.read(4)
            file.file.seek(0)
            
            if header != b'%PDF':
                return {"valid": False, "error": "File appears corrupted."}
            
            validation_details["checks_passed"].append("pdf_signature_check")
        
        # Check 4: Malware scan
        scan_result = await self.malware_scanner.scan_file(file)
        
        if not scan_result['safe']:
            return {
                "valid": False,
                "error": f"Security threat detected: {scan_result.get('threat_found')}"
            }
        
        validation_details["checks_passed"].append("malware_scan")
        
        return {"valid": True, "error": None, "validation_details": validation_details}


class MalwareScannerService:
    """ClamAV integration with graceful degradation"""
    
    def __init__(self):
        self.enabled = os.getenv('CLAMAV_ENABLED', 'true').lower() == 'true'
        self.client = None
        
        if self.enabled:
            try:
                import clamd
                self.client = clamd.ClamdNetworkSocket(
                    host=os.getenv('CLAMAV_HOST', 'localhost'),
                    port=int(os.getenv('CLAMAV_PORT', '3310'))
                )
                self.client.ping()
            except Exception as e:
                logger.warning(f"ClamAV not available: {e}")
                self.enabled = False
    
    async def scan_file(self, file: UploadFile) -> Dict:
        if not self.enabled or not self.client:
            return {"safe": True, "scan_performed": False}
        
        try:
            from io import BytesIO
            file_content = await file.read()
            file.file.seek(0)
            
            result = self.client.instream(BytesIO(file_content))
            status, threat = result.get('stream', ('ERROR', 'Unknown'))
            
            if status == 'OK':
                return {"safe": True, "scan_performed": True}
            elif status == 'FOUND':
                logger.warning(f"MALWARE: {file.filename} - {threat}")
                return {"safe": False, "threat_found": threat, "scan_performed": True}
            else:
                return {"safe": False, "threat_found": f"Scan error: {status}"}
                
        except Exception as e:
            # Fail-safe: reject if scan fails
            return {"safe": False, "threat_found": f"Scan failed: {str(e)}"}


class DuplicateDetector:
    """Hash-based duplicate detection with race protection"""
    
    def calculate_file_hash(self, file_content: bytes) -> str:
        return hashlib.sha256(file_content).hexdigest()
    
    async def check_duplicate(self, account_id: str, file_hash: str) -> Optional[Dict]:
        result = self.client.table("files").select("id").eq(
            "account_id", account_id
        ).eq("file_hash", file_hash).execute()
        
        if result.data:
            return {"type": "file_hash", "message": "Exact duplicate detected"}
        return None
    
    async def mark_processing(self, account_id: str, file_hash: str, ttl: int = 300):
        """Mark file as being processed (prevents concurrent processing)"""
        key = f"processing:{account_id}:{file_hash}"
        self.redis.setex(key, ttl, "1")
    
    async def is_processing(self, account_id: str, file_hash: str) -> bool:
        key = f"processing:{account_id}:{file_hash}"
        return self.redis.exists(key) > 0
    
    async def clear_processing(self, account_id: str, file_hash: str):
        key = f"processing:{account_id}:{file_hash}"
        self.redis.delete(key)
```

### TypeScript

```typescript
import { createHash } from 'crypto';

interface ValidationResult {
  valid: boolean;
  error?: string;
  checksPassed: string[];
}

class FileValidator {
  private maxSize = 10 * 1024 * 1024; // 10MB
  private allowedTypes = ['application/pdf', 'image/jpeg', 'image/png'];

  async validate(file: File): Promise<ValidationResult> {
    const checksPassed: string[] = [];

    // Check 1: Size
    if (file.size > this.maxSize) {
      return { valid: false, error: 'File too large', checksPassed };
    }
    if (file.size === 0) {
      return { valid: false, error: 'File is empty', checksPassed };
    }
    checksPassed.push('size_check');

    // Check 2: MIME type
    if (!this.allowedTypes.includes(file.type)) {
      return { valid: false, error: 'Invalid file type', checksPassed };
    }
    checksPassed.push('type_check');

    // Check 3: Content signature
    if (file.type === 'application/pdf') {
      const header = await this.readHeader(file, 4);
      if (header !== '%PDF') {
        return { valid: false, error: 'File appears corrupted', checksPassed };
      }
      checksPassed.push('pdf_signature_check');
    }

    return { valid: true, checksPassed };
  }

  private async readHeader(file: File, bytes: number): Promise<string> {
    const slice = file.slice(0, bytes);
    const buffer = await slice.arrayBuffer();
    return new TextDecoder().decode(buffer);
  }
}

class DuplicateDetector {
  async calculateHash(file: File): Promise<string> {
    const buffer = await file.arrayBuffer();
    const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
    return Array.from(new Uint8Array(hashBuffer))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
  }
}
```

## Usage Examples

### Complete Upload Endpoint

```python
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    auth: AuthenticatedUser = Depends(get_current_user),
):
    # Check limits FIRST
    allowed, details = usage_service.check_limit(auth.id, 'file_upload')
    if not allowed:
        raise HTTPException(status_code=429, detail=details)
    
    # Stage 1-3: Validate
    validation = await file_validator.validate_file(file)
    if not validation['valid']:
        raise HTTPException(status_code=400, detail=validation['error'])
    
    # Stage 4: Hash for duplicate detection
    file.file.seek(0)
    file_content = await file.read()
    file_hash = duplicate_detector.calculate_file_hash(file_content)
    file.file.seek(0)
    
    # Check duplicate
    duplicate = await duplicate_detector.check_duplicate(auth.account_id, file_hash)
    if duplicate:
        raise HTTPException(status_code=409, detail=duplicate)
    
    # Stage 5: Race protection
    if await duplicate_detector.is_processing(auth.account_id, file_hash):
        raise HTTPException(status_code=409, detail="File is being processed")
    
    await duplicate_detector.mark_processing(auth.account_id, file_hash, ttl=300)
    
    try:
        # Stage 6: Upload
        file_url = await storage_service.upload_file(file, auth.id)
    finally:
        # Stage 7: Clear lock
        await duplicate_detector.clear_processing(auth.account_id, file_hash)
    
    return {"success": True, "file_url": file_url, "file_hash": file_hash}
```

## Best Practices

1. Check limits BEFORE upload - Don't waste bandwidth on files that will be rejected
2. TTL on processing markers - If upload crashes, marker auto-expires (300s default)
3. ClamAV graceful degradation - Don't block uploads if scanner is down
4. Hash before upload - Calculate hash from memory, not after storage write
5. Fail-safe on scan errors - Reject file if malware scan fails

## Common Mistakes

- Processing files before checking usage limits
- No TTL on processing markers (stuck forever if crash)
- Blocking uploads when ClamAV is unavailable
- Calculating hash after storage write (wasted upload)
- Allowing uploads when malware scan fails

## Related Patterns

- rate-limiting - Rate limit upload endpoints
- distributed-lock - Coordinate concurrent uploads
- validation-quarantine - Quarantine suspicious files
