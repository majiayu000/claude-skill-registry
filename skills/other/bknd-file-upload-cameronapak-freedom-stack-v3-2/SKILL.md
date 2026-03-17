---
name: bknd-file-upload
description: Use when uploading files to Bknd storage. Covers MediaApi SDK methods (upload, uploadToEntity), REST endpoints, React integration with file inputs, progress tracking with XHR, browser upload patterns, and entity field attachments.
---

# File Upload

Upload files to Bknd storage using the MediaApi SDK or REST endpoints.

## Prerequisites

- Media module enabled in Bknd config
- Storage adapter configured (S3, R2, Cloudinary, or local)
- `bknd` package installed
- For entity uploads: target entity has `media()` field defined

## When to Use UI Mode

- Admin panel > Media section > drag-and-drop upload
- Quick testing of storage configuration
- One-off file uploads without code

## When to Use Code Mode

- Programmatic uploads from frontend
- Upload with progress tracking
- Attach files to entity records
- Custom upload UI components

## Step-by-Step: UI Approach

### Step 1: Open Admin Panel

Navigate to `http://localhost:7654` (or your Bknd URL).

### Step 2: Go to Media Section

Click "Media" in sidebar to access file management.

### Step 3: Upload Files

- Drag files into the upload area, OR
- Click "Upload" button and select files

### Step 4: Verify Upload

Files appear in the list with name, size, type, and date.

## Step-by-Step: Code Approach

### Basic File Upload

```typescript
import { Api } from "bknd";

const api = new Api({ host: "http://localhost:7654" });

// From File object (browser)
const input = document.querySelector('input[type="file"]');
const file = input.files[0];

const { ok, data, error } = await api.media.upload(file);

if (ok) {
  console.log("Uploaded:", data.name);
  console.log("Size:", data.meta.size);
  console.log("Type:", data.meta.type);
}
```

### Upload with Custom Filename

```typescript
const { ok, data } = await api.media.upload(file, {
  filename: "custom-name.png",
});
```

### Upload from URL

```typescript
// Direct URL string
const { ok, data } = await api.media.upload("https://example.com/image.png");

// Or from fetch Response
const response = await fetch("https://example.com/image.png");
const { ok, data } = await api.media.upload(response);
```

### Upload to Entity Field

Attach file directly to an entity record:

```typescript
// Assumes "posts" entity has a media() field called "cover_image"
const { ok, data } = await api.media.uploadToEntity(
  "posts",           // entity name
  123,               // record ID
  "cover_image",     // field name
  file,
  { overwrite: true }  // replace existing file
);

if (ok) {
  console.log("File attached:", data.result.cover_image);
}
```

## React Integration

### Simple File Input

```tsx
function FileUpload({ onUploaded }) {
  const { api } = useApp();  // or your Api instance
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError(null);

    const { ok, data, error } = await api.media.upload(file);

    setUploading(false);

    if (ok) {
      onUploaded(data);
    } else {
      setError(error?.message || "Upload failed");
    }
  };

  return (
    <div>
      <input
        type="file"
        onChange={handleChange}
        disabled={uploading}
      />
      {uploading && <span>Uploading...</span>}
      {error && <span style={{ color: "red" }}>{error}</span>}
    </div>
  );
}
```

### Image Upload with Preview

```tsx
function ImageUpload({ value, onChange }) {
  const { api } = useApp();
  const [preview, setPreview] = useState(value);
  const [uploading, setUploading] = useState(false);

  const handleChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Show local preview immediately
    const localUrl = URL.createObjectURL(file);
    setPreview(localUrl);

    setUploading(true);
    const { ok, data } = await api.media.upload(file);
    setUploading(false);

    if (ok) {
      // Clean up local preview
      URL.revokeObjectURL(localUrl);
      // Use server URL
      onChange(data.name);
    }
  };

  return (
    <div>
      {preview && (
        <img
          src={preview}
          alt="Preview"
          style={{ maxWidth: 200, opacity: uploading ? 0.5 : 1 }}
        />
      )}
      <input type="file" accept="image/*" onChange={handleChange} />
      {uploading && <span>Uploading...</span>}
    </div>
  );
}
```

### Upload with Progress Tracking

For large files, use XHR for progress:

```tsx
function ProgressUpload({ onUploaded }) {
  const { api } = useApp();
  const [progress, setProgress] = useState(0);
  const [uploading, setUploading] = useState(false);

  const uploadWithProgress = (file) => {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      const url = api.media.getFileUploadUrl({ path: file.name });

      xhr.upload.addEventListener("progress", (e) => {
        if (e.lengthComputable) {
          setProgress(Math.round((e.loaded / e.total) * 100));
        }
      });

      xhr.addEventListener("load", () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(JSON.parse(xhr.responseText));
        } else {
          reject(new Error(xhr.statusText));
        }
      });

      xhr.addEventListener("error", () => reject(new Error("Upload failed")));

      xhr.open("POST", url);
      xhr.setRequestHeader("Content-Type", file.type);

      // Add auth if using header transport
      const token = api.getAuthState().token;
      if (token) {
        xhr.setRequestHeader("Authorization", `Bearer ${token}`);
      }

      xhr.send(file);
    });
  };

  const handleChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setProgress(0);

    try {
      const result = await uploadWithProgress(file);
      onUploaded(result);
    } catch (err) {
      console.error("Upload failed:", err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleChange} disabled={uploading} />
      {uploading && (
        <div>
          <progress value={progress} max={100} />
          <span>{progress}%</span>
        </div>
      )}
    </div>
  );
}
```

### Avatar Upload Component

Complete avatar upload with entity attachment:

```tsx
function AvatarUpload({ userId, currentAvatar }) {
  const { api } = useApp();
  const [preview, setPreview] = useState(currentAvatar);
  const [uploading, setUploading] = useState(false);

  const handleChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate image
    if (!file.type.startsWith("image/")) {
      alert("Please select an image file");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      alert("Image must be under 5MB");
      return;
    }

    setPreview(URL.createObjectURL(file));
    setUploading(true);

    const { ok, data } = await api.media.uploadToEntity(
      "users",
      userId,
      "avatar",
      file,
      { overwrite: true }
    );

    setUploading(false);

    if (ok) {
      setPreview(data.result.avatar);
    }
  };

  return (
    <div>
      <img
        src={preview || "/default-avatar.png"}
        alt="Avatar"
        style={{
          width: 100,
          height: 100,
          borderRadius: "50%",
          opacity: uploading ? 0.5 : 1
        }}
      />
      <label>
        <input
          type="file"
          accept="image/*"
          onChange={handleChange}
          disabled={uploading}
          style={{ display: "none" }}
        />
        <button type="button" disabled={uploading}>
          {uploading ? "Uploading..." : "Change Avatar"}
        </button>
      </label>
    </div>
  );
}
```

## REST API

### Upload Endpoint

```bash
# Basic upload (filename in path)
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: image/png" \
  --data-binary @image.png \
  http://localhost:7654/api/media/upload/image.png

# Upload to entity field
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: image/jpeg" \
  --data-binary @photo.jpg \
  "http://localhost:7654/api/media/entity/users/123/avatar?overwrite=true"
```

### Response Format

```json
{
  "name": "image.png",
  "meta": {
    "type": "image/png",
    "size": 24680,
    "width": 800,
    "height": 600
  },
  "etag": "abc123...",
  "state": {
    "name": "image.png",
    "path": "image.png"
  }
}
```

## Entity Media Field

Define a media field to link files to records:

```typescript
import { em, entity, text, media } from "bknd";

const schema = em({
  posts: entity("posts", {
    title: text(),
    cover_image: media(),  // Stores file reference
  }),

  users: entity("users", {
    name: text(),
    avatar: media(),
  }),
});
```

Media fields store the filename, not the file content.

## Server-Side Upload

Upload files in Bknd server context (seeds, flows):

```typescript
// In seed function
export default defineConfig({
  options: {
    seed: async (ctx) => {
      const media = ctx.server?.modules.media;
      if (!media) return;

      // Upload from URL
      const response = await fetch("https://example.com/default-avatar.png");
      const buffer = await response.arrayBuffer();

      await media.adapter.putObject(
        "default-avatar.png",
        new Uint8Array(buffer)
      );
    },
  },
});
```

## Handling Upload Response

```typescript
const { ok, data, error } = await api.media.upload(file);

if (!ok) {
  // Handle error
  if (error?.status === 413) {
    console.error("File too large");
  } else if (error?.status === 401) {
    console.error("Not authenticated");
  } else if (error?.status === 403) {
    console.error("No upload permission");
  } else {
    console.error("Upload failed:", error?.message);
  }
  return;
}

// Success - use data
console.log("Filename:", data.name);
console.log("MIME type:", data.meta.type);
console.log("Size (bytes):", data.meta.size);

// For images
if (data.meta.width && data.meta.height) {
  console.log("Dimensions:", data.meta.width, "x", data.meta.height);
}
```

## Common Pitfalls

### File Too Large (413 Error)

**Problem:** Upload fails with 413 status.

**Fix:** Increase `body_max_size` in config:

```typescript
export default defineConfig({
  media: {
    enabled: true,
    body_max_size: 50 * 1024 * 1024,  // 50MB
    adapter: { ... },
  },
});
```

### Missing Content-Type Header

**Problem:** File uploaded with wrong MIME type.

**Fix:** Always set Content-Type in REST uploads:

```bash
# WRONG - no content type
curl -X POST --data-binary @image.png .../upload/image.png

# CORRECT
curl -X POST \
  -H "Content-Type: image/png" \
  --data-binary @image.png \
  .../upload/image.png
```

SDK handles this automatically from File object.

### CORS Errors

**Problem:** Browser blocks upload to S3.

**Fix:** Configure CORS on storage bucket (not Bknd):

```json
{
  "CORSRules": [{
    "AllowedOrigins": ["https://yourapp.com"],
    "AllowedMethods": ["GET", "PUT", "POST"],
    "AllowedHeaders": ["*"]
  }]
}
```

### Auth Token Missing in XHR Upload

**Problem:** 401 error when using XHR progress upload.

**Fix:** Add Authorization header:

```typescript
const token = api.getAuthState().token;
if (token) {
  xhr.setRequestHeader("Authorization", `Bearer ${token}`);
}
```

### Media Field Not Defined

**Problem:** `uploadToEntity` fails with "field not found".

**Fix:** Ensure entity has `media()` field:

```typescript
// WRONG - no media field
posts: entity("posts", {
  title: text(),
  cover_image: text(),  // This is just a string
}),

// CORRECT
posts: entity("posts", {
  title: text(),
  cover_image: media(),  // Proper media field
}),
```

### Memory Issues with Large Files

**Problem:** Browser crashes on large file upload.

**Fix:** Use streaming or chunked upload:

```typescript
// For very large files, consider chunked upload
// Bknd doesn't have native chunking, so use S3 presigned URLs
// or implement custom chunking endpoint
```

## Verification

Test upload works correctly:

```typescript
async function testUpload() {
  // 1. Check media enabled
  const { ok: listOk } = await api.media.listFiles();
  console.log("Media module enabled:", listOk);

  // 2. Test file upload
  const testFile = new File(["test"], "test.txt", { type: "text/plain" });
  const { ok, data, error } = await api.media.upload(testFile);
  console.log("Upload result:", ok ? data.name : error);

  // 3. Verify file exists
  const { data: files } = await api.media.listFiles();
  const exists = files.some(f => f.key === "test.txt");
  console.log("File in list:", exists);

  // 4. Clean up
  if (exists) {
    await api.media.deleteFile("test.txt");
    console.log("Test file deleted");
  }
}
```

## DOs and DON'Ts

**DO:**
- Validate file type/size before upload
- Show upload progress for large files
- Handle all error cases (401, 403, 413)
- Use `uploadToEntity` for entity attachments
- Clean up object URLs after upload completes
- Set appropriate `body_max_size` limit

**DON'T:**
- Upload without auth when permissions require it
- Forget Content-Type header in REST uploads
- Store sensitive files without access control
- Allow unlimited file sizes in production
- Use local adapter in production

## Related Skills

- **bknd-storage-config** - Configure storage backends
- **bknd-serve-files** - Serve uploaded files
- **bknd-add-field** - Add media field to entity
- **bknd-crud-update** - Update records with file references
- **bknd-assign-permissions** - Set media.create permission
