---
name: convex-file-storage
displayName: Convex File Storage
description: Complete file handling including upload flows, serving files via URL, storing generated files from actions, deletion, and accessing file metadata from system tables
version: 1.0.0
author: Convex
tags: [convex, file-storage, uploads, images, files]
---

# Convex File Storage

Handle file uploads, storage, serving, and management in Convex applications with proper patterns for images, documents, and generated files.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: https://docs.convex.dev/file-storage
- Upload Files: https://docs.convex.dev/file-storage/upload-files
- Serve Files: https://docs.convex.dev/file-storage/serve-files
- For broader context: https://docs.convex.dev/llms.txt

## Instructions

### File Storage Overview

Convex provides built-in file storage with:
- Automatic URL generation for serving files
- Support for any file type (images, PDFs, videos, etc.)
- File metadata via the `_storage` system table
- Integration with mutations and actions

### Generating Upload URLs

```typescript
// convex/files.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const generateUploadUrl = mutation({
  args: {},
  returns: v.string(),
  handler: async (ctx) => {
    return await ctx.storage.generateUploadUrl();
  },
});
```

### Client-Side Upload

```typescript
// React component
import { useMutation } from "convex/react";
import { api } from "../convex/_generated/api";
import { useState } from "react";

function FileUploader() {
  const generateUploadUrl = useMutation(api.files.generateUploadUrl);
  const saveFile = useMutation(api.files.saveFile);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      // Step 1: Get upload URL
      const uploadUrl = await generateUploadUrl();

      // Step 2: Upload file to storage
      const result = await fetch(uploadUrl, {
        method: "POST",
        headers: { "Content-Type": file.type },
        body: file,
      });

      const { storageId } = await result.json();

      // Step 3: Save file reference to database
      await saveFile({
        storageId,
        fileName: file.name,
        fileType: file.type,
        fileSize: file.size,
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        onChange={handleUpload}
        disabled={uploading}
      />
      {uploading && <p>Uploading...</p>}
    </div>
  );
}
```

### Saving File References

```typescript
// convex/files.ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const saveFile = mutation({
  args: {
    storageId: v.id("_storage"),
    fileName: v.string(),
    fileType: v.string(),
    fileSize: v.number(),
  },
  returns: v.id("files"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("files", {
      storageId: args.storageId,
      fileName: args.fileName,
      fileType: args.fileType,
      fileSize: args.fileSize,
      uploadedAt: Date.now(),
    });
  },
});
```

### Serving Files via URL

```typescript
// convex/files.ts
export const getFileUrl = query({
  args: { storageId: v.id("_storage") },
  returns: v.union(v.string(), v.null()),
  handler: async (ctx, args) => {
    return await ctx.storage.getUrl(args.storageId);
  },
});

// Get file with URL
export const getFile = query({
  args: { fileId: v.id("files") },
  returns: v.union(
    v.object({
      _id: v.id("files"),
      fileName: v.string(),
      fileType: v.string(),
      fileSize: v.number(),
      url: v.union(v.string(), v.null()),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    const file = await ctx.db.get(args.fileId);
    if (!file) return null;

    const url = await ctx.storage.getUrl(file.storageId);
    
    return {
      _id: file._id,
      fileName: file.fileName,
      fileType: file.fileType,
      fileSize: file.fileSize,
      url,
    };
  },
});
```

### Displaying Files in React

```typescript
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function FileDisplay({ fileId }: { fileId: Id<"files"> }) {
  const file = useQuery(api.files.getFile, { fileId });

  if (!file) return <div>Loading...</div>;
  if (!file.url) return <div>File not found</div>;

  // Handle different file types
  if (file.fileType.startsWith("image/")) {
    return <img src={file.url} alt={file.fileName} />;
  }

  if (file.fileType === "application/pdf") {
    return (
      <iframe
        src={file.url}
        title={file.fileName}
        width="100%"
        height="600px"
      />
    );
  }

  return (
    <a href={file.url} download={file.fileName}>
      Download {file.fileName}
    </a>
  );
}
```

### Storing Generated Files from Actions

```typescript
// convex/generate.ts
"use node";

import { action } from "./_generated/server";
import { v } from "convex/values";
import { api } from "./_generated/api";

export const generatePDF = action({
  args: { content: v.string() },
  returns: v.id("_storage"),
  handler: async (ctx, args) => {
    // Generate PDF (example using a library)
    const pdfBuffer = await generatePDFFromContent(args.content);

    // Convert to Blob
    const blob = new Blob([pdfBuffer], { type: "application/pdf" });

    // Store in Convex
    const storageId = await ctx.storage.store(blob);

    return storageId;
  },
});

// Generate and save image
export const generateImage = action({
  args: { prompt: v.string() },
  returns: v.id("_storage"),
  handler: async (ctx, args) => {
    // Call external API to generate image
    const response = await fetch("https://api.example.com/generate", {
      method: "POST",
      body: JSON.stringify({ prompt: args.prompt }),
    });

    const imageBuffer = await response.arrayBuffer();
    const blob = new Blob([imageBuffer], { type: "image/png" });

    return await ctx.storage.store(blob);
  },
});
```

### Accessing File Metadata

```typescript
// convex/files.ts
import { query } from "./_generated/server";
import { v } from "convex/values";
import { Id } from "./_generated/dataModel";

type FileMetadata = {
  _id: Id<"_storage">;
  _creationTime: number;
  contentType?: string;
  sha256: string;
  size: number;
};

export const getFileMetadata = query({
  args: { storageId: v.id("_storage") },
  returns: v.union(
    v.object({
      _id: v.id("_storage"),
      _creationTime: v.number(),
      contentType: v.optional(v.string()),
      sha256: v.string(),
      size: v.number(),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    const metadata = await ctx.db.system.get(args.storageId);
    return metadata as FileMetadata | null;
  },
});
```

### Deleting Files

```typescript
// convex/files.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const deleteFile = mutation({
  args: { fileId: v.id("files") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const file = await ctx.db.get(args.fileId);
    if (!file) return null;

    // Delete from storage
    await ctx.storage.delete(file.storageId);

    // Delete database record
    await ctx.db.delete(args.fileId);

    return null;
  },
});
```

### Image Upload with Preview

```typescript
import { useMutation } from "convex/react";
import { api } from "../convex/_generated/api";
import { useState, useRef } from "react";

function ImageUploader({ onUpload }: { onUpload: (id: Id<"files">) => void }) {
  const generateUploadUrl = useMutation(api.files.generateUploadUrl);
  const saveFile = useMutation(api.files.saveFile);
  const [preview, setPreview] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith("image/")) {
      alert("Please select an image file");
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert("File size must be less than 10MB");
      return;
    }

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target?.result as string);
    reader.readAsDataURL(file);

    // Upload
    setUploading(true);
    try {
      const uploadUrl = await generateUploadUrl();
      const result = await fetch(uploadUrl, {
        method: "POST",
        headers: { "Content-Type": file.type },
        body: file,
      });

      const { storageId } = await result.json();
      const fileId = await saveFile({
        storageId,
        fileName: file.name,
        fileType: file.type,
        fileSize: file.size,
      });

      onUpload(fileId);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        onChange={handleFileSelect}
        style={{ display: "none" }}
      />
      
      <button
        onClick={() => inputRef.current?.click()}
        disabled={uploading}
      >
        {uploading ? "Uploading..." : "Select Image"}
      </button>

      {preview && (
        <img
          src={preview}
          alt="Preview"
          style={{ maxWidth: 200, marginTop: 10 }}
        />
      )}
    </div>
  );
}
```

## Examples

### Schema for File Storage

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  files: defineTable({
    storageId: v.id("_storage"),
    fileName: v.string(),
    fileType: v.string(),
    fileSize: v.number(),
    uploadedBy: v.id("users"),
    uploadedAt: v.number(),
  })
    .index("by_user", ["uploadedBy"])
    .index("by_type", ["fileType"]),

  // User avatars
  users: defineTable({
    name: v.string(),
    email: v.string(),
    avatarStorageId: v.optional(v.id("_storage")),
  }),

  // Posts with images
  posts: defineTable({
    authorId: v.id("users"),
    content: v.string(),
    imageStorageIds: v.array(v.id("_storage")),
    createdAt: v.number(),
  }).index("by_author", ["authorId"]),
});
```

## Best Practices

- Never run `npx convex deploy` unless explicitly instructed
- Never run any git commands unless explicitly instructed
- Validate file types and sizes on the client before uploading
- Store file metadata (name, type, size) in your own table
- Use the `_storage` system table only for Convex metadata
- Delete storage files when deleting database references
- Use appropriate Content-Type headers when uploading
- Consider image optimization for large images

## Common Pitfalls

1. **Not setting Content-Type header** - Files may not serve correctly
2. **Forgetting to delete storage** - Orphaned files waste storage
3. **Not validating file types** - Security risk for malicious uploads
4. **Large file uploads without progress** - Poor UX for users
5. **Using deprecated getMetadata** - Use ctx.db.system.get instead

## References

- Convex Documentation: https://docs.convex.dev/
- Convex LLMs.txt: https://docs.convex.dev/llms.txt
- File Storage: https://docs.convex.dev/file-storage
- Upload Files: https://docs.convex.dev/file-storage/upload-files
- Serve Files: https://docs.convex.dev/file-storage/serve-files
