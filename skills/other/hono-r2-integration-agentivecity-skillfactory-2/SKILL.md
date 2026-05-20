---
name: "hono-r2-integration"
description: "Use this skill whenever the user wants to design, set up, or refactor Cloudflare R2 object storage usage in a Hono + TypeScript app running on Cloudflare Workers/Pages, including bucket bindings, upload/download flows, signed URLs, and folder-like organization."
---

# Hono + Cloudflare R2 Integration Skill

## Purpose

You are a specialized assistant for using **Cloudflare R2** (S3-compatible object storage)
inside a **Hono + TypeScript** app running on **Cloudflare Workers / Pages**.

Use this skill to:

- Wire **R2 bucket bindings** into a Hono app (`c.env.BUCKET`)
- Design **upload/download/delete** flows from Hono routes
- Structure **storage service** modules on top of R2
- Handle **content types**, metadata, and folder-like key prefixes
- Implement **presigned URL**-style access patterns where appropriate
- Work safely within Workers constraints (streaming, body limits)

Do **not** use this skill for:

- Hono app scaffolding → use `hono-app-scaffold`
- D1/database access → use `hono-d1-integration`
- Frontend file handling/UI → use frontend/Next skills

If `CLAUDE.md` exists, obey its rules for bucket naming, storage paths, and access patterns.

---

## When To Apply This Skill

Trigger this skill when the user asks for things like:

- “Use R2 to store files for this Hono API.”
- “Add upload/download endpoints backed by R2.”
- “Serve user avatars or documents from R2 in a Worker.”
- “Organize stored files by user/tenant/date.”
- “Refactor my raw R2 calls into a clean service.”

Avoid this skill when:

- Storage is not R2 (e.g., S3, Supabase Storage) for this service.
- The project doesn’t run on Cloudflare Workers/Pages.

---

## Runtime & Binding Assumptions

Assume:

- App runs on **Cloudflare Workers** or **Pages Functions**.
- R2 is configured as a binding in `wrangler.toml`, e.g.:

  ```toml
  [[r2_buckets]]
  binding = "BUCKET"
  bucket_name = "my-bucket"
  preview_bucket_name = "my-bucket-dev"
  ```

- In code, the bucket is available as `c.env.BUCKET` and has type `R2Bucket`.

We type Env and encapsulate R2 access in services where possible.

---

## Project Structure

This skill expects or creates something like:

```text
src/
  app.ts
  index.ts
  routes/
    v1/
      upload.routes.ts
      files.routes.ts
  storage/
    r2-client.ts       # helpers & Env typings
    file-storage.service.ts
  types/
    env.d.ts           # Env interface with BUCKET binding
```

Adjust paths to match the existing project.

---

## Typing Env and R2 Binding

Define Env with an R2 bucket binding:

```ts
// src/types/env.d.ts
export interface Env {
  BUCKET: R2Bucket;
  // other bindings (DB, KV, etc)
}
```

Integrate with Hono context typing:

```ts
// src/types/app.ts
import type { Env } from "./env";

export type AppContext = {
  Bindings: Env;
};
```

Use when creating the app:

```ts
import { Hono } from "hono";
import type { AppContext } from "./types/app";

export const app = new Hono<AppContext>();
```

This skill should ensure `c.env.BUCKET` is fully typed.

---

## R2 Helper Module

Create a small helper to access the bucket and wrap common operations:

```ts
// src/storage/r2-client.ts
import type { Env } from "../types/env";

export function getBucket(env: Env): R2Bucket {
  return env.BUCKET;
}

export type R2ObjectInfo = {
  key: string;
  size: number;
  uploaded: string;
  etag?: string;
  httpEtag?: string;
  checksums?: Record<string, string>;
};
```

This module can be extended with helper functions such as `putObject`, `getObject`, `deleteObject` etc., but often we call `bucket` methods directly from a service class.

---

## Storage Service Layer

Create a service that receives `Env` and encapsulates R2 operations.

```ts
// src/storage/file-storage.service.ts
import type { Env } from "../types/env";
import { getBucket } from "./r2-client";

export class FileStorageService {
  constructor(private env: Env) {}

  private bucket() {
    return getBucket(this.env);
  }

  buildKey(prefix: string, filename: string): string {
    // Example: "users/<prefix>/<filename>"
    return `${prefix}/${filename}`;
  }

  async uploadObject(
    prefix: string,
    filename: string,
    body: ReadableStream | ArrayBuffer | Uint8Array,
    contentType?: string,
  ) {
    const key = this.buildKey(prefix, filename);
    const bucket = this.bucket();

    const putResult = await bucket.put(key, body, {
      httpMetadata: contentType ? { contentType } : undefined,
    });

    return { key, etag: putResult?.etag };
  }

  async getObject(key: string) {
    const bucket = this.bucket();
    const obj = await bucket.get(key);
    if (!obj) return null;

    return {
      key,
      body: obj.body,
      size: obj.size,
      uploaded: obj.uploaded,
      httpMetadata: obj.httpMetadata,
    };
  }

  async deleteObject(key: string) {
    const bucket = this.bucket();
    await bucket.delete(key);
  }

  async list(prefix: string) {
    const bucket = this.bucket();
    const res = await bucket.list({ prefix });
    return res.objects;
  }
}
```

This skill should:

- Encourage key naming conventions: e.g., `users/<userId>/avatars/<file>` or `tenants/<tenantId>/...`
- Use Stream bodies (`obj.body`) correctly for Workers.

---

## Hono Routes: Upload & Download

### Upload Route Example

Supports `multipart/form-data` uploads using `c.req.parseBody()` or `c.req.formData()` depending on Hono version.

```ts
// src/routes/v1/upload.routes.ts
import { Hono } from "hono";
import type { AppContext } from "../../types/app";
import { FileStorageService } from "../../storage/file-storage.service";

export function uploadRoutes() {
  const app = new Hono<AppContext>();

  app.post("/files", async (c) => {
    const formData = await c.req.formData();
    const file = formData.get("file");

    if (!(file instanceof File)) {
      return c.json({ message: "file field is required" }, 400);
    }

    const userId = "anonymous"; // or from auth middleware, e.g. c.get("user").id

    const storage = new FileStorageService(c.env);
    const key = storage.buildKey(`users/${userId}`, file.name);

    const arrayBuffer = await file.arrayBuffer();

    await storage.uploadObject(`users/${userId}`, file.name, arrayBuffer, file.type);

    return c.json({ key }, 201);
  });

  return app;
}
```

This skill should:

- Recommend secure naming (no direct user input as raw key without sanitizing).
- Encourage deriving prefixes from authenticated user/tenant.

### Download Route Example

```ts
// src/routes/v1/files.routes.ts
import { Hono } from "hono";
import type { AppContext } from "../../types/app";
import { FileStorageService } from "../../storage/file-storage.service";

export function filesRoutes() {
  const app = new Hono<AppContext>();

  app.get("/files/:key", async (c) => {
    const keyParam = c.req.param("key");
    // You may want to decode / validate this; often we pass encoded keys or IDs instead
    const key = decodeURIComponent(keyParam);

    const storage = new FileStorageService(c.env);
    const obj = await storage.getObject(key);

    if (!obj) {
      return c.json({ message: "Not found" }, 404);
    }

    const headers: Record<string, string> = {};
    if (obj.httpMetadata?.contentType) {
      headers["Content-Type"] = obj.httpMetadata.contentType;
    }

    return new Response(obj.body, {
      status: 200,
      headers,
    });
  });

  return app;
}
```

**Important:** Exposing raw keys in URLs may not be ideal; many apps use an opaque ID that maps to a key. This skill can recommend a mapping layer if needed.

---

## Presigned-URL Style Patterns (Optional)

R2 doesn’t provide S3-style presigned URLs in the same way out of the box, but you can:

- Generate a short-lived signed token (JWT) containing the key + permission.
- Use a Hono route to validate that token and stream the object.

Example idea:

```ts
// pseudo-code
app.get("/download/:token", async (c) => {
  const token = c.req.param("token");
  const { key } = await verifyDownloadToken(token); // JWT or similar
  const storage = new FileStorageService(c.env);
  const obj = await storage.getObject(key);
  // stream object if valid
});
```

This skill should:

- Suggest this pattern when the user wants “presigned URLs” behavior.
- Defer actual token signing/verification to an auth/signing skill.

---

## Folder-Like Organization & Multi-Tenancy

This skill should help you design key schemes like:

- Per-user:
  - `users/<userId>/avatars/<filename>`
  - `users/<userId>/documents/<id>.pdf`
- Per-tenant:
  - `tenants/<tenantId>/exports/<timestamp>.json`
- Public vs private:
  - `public/<whatever>` vs `private/<userId>/<file>`

It should:

- Encourage not leaking sensitive identifiers where not needed.
- Suggest using random IDs or hashed filenames for users’ private content.

---

## Integration with Auth

When `hono-authentication` is present, this skill can:

- Use `c.get("user")` to determine `userId` or roles.
- Enforce access control for:
  - Upload (who can write to which prefixes)
  - Download (who can read which keys)

Example pattern:

```ts
const user = c.get("user");
if (!user) return c.json({ message: "Unauthorized" }, 401);

// build prefix from user.id
const prefix = `users/${user.id}`;
```

---

## Local Development & Testing

This skill may recommend:

- Using R2’s local dev via `wrangler dev` and preview buckets.
- Mocking `R2Bucket` methods in unit tests:

```ts
const mockBucket: Partial<R2Bucket> = {
  put: jest.fn().mockResolvedValue({ etag: "etag" } as any),
  get: jest.fn().mockResolvedValue(null),
  list: jest.fn().mockResolvedValue({ objects: [] } as any),
  delete: jest.fn().mockResolvedValue(undefined),
};
```

- For integration tests, run `wrangler dev` and hit endpoints that talk to R2 directly.

---

## Error Handling & Limits

This skill must consider:

- File size limits; large uploads should be constrained (and perhaps chunked in more advanced setups).
- Graceful error handling when bucket operations fail:

```ts
try {
  await bucket.put(key, body);
} catch (err) {
  console.error("R2 upload failed:", err);
  return c.json({ message: "Upload failed" }, 500);
}
```

- Avoid echoing internal R2 errors directly to clients.

---

## Example Prompts That Should Use This Skill

- “Store user uploads in R2 from this Hono API.”
- “Add endpoints to upload and download files using Cloudflare R2.”
- “Organize R2 keys by user/tenant in my Workers app.”
- “Refactor my R2 calls into a reusable service in Hono.”
- “Implement a safe download route for R2-stored documents.”

For these tasks, rely on this skill to build a **clean, typed, and secure R2 integration** inside your
Hono + Cloudflare Workers/Pages application.
