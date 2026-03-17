---
name: "cloudflare-r2-bucket-management-and-access"
description: "Use this skill to configure Cloudflare R2 buckets, access control, lifecycle policies, public/private assets, and integration with Hono Workers using read/write/delete/list operations and signed-access patterns."
---

# Cloudflare R2 Bucket Management & Access Skill

## Purpose

You are the assistant responsible for **managing R2 storage in production** including:

- Bucket provisioning & environment separation
- Public/private access strategy
- Upload/download/stream patterns
- Lifecycle rules & retention policies
- Signed URL access patterns
- Asset optimization + access performance

Use this skill when handling Cloudflare **R2 + Hono Worker integration** beyond basic uploads.

Do **not** use this skill for:

- D1 schema or migrations → `cloudflare-d1-migrations-and-production-seeding`
- Core Hono routing → `hono-app-scaffold`
- Auth logic → `hono-authentication`


---

## Environment-Aware Bucket Setup

This skill knows how to structure R2 per environment:

```toml
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket-dev"
preview_bucket_name = "my-bucket-dev"

[env.staging]
[[env.staging.r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket-staging"

[env.production]
[[env.production.r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket-prod"
```

Claude should:

- Default to **separate buckets per environment**
- Suggest mirroring structure between staging & prod
- Prevent mixing prod bucket during dev


---

## R2 Access Permission Strategy

R2 can be accessed in multiple ways — this skill helps choose between:

| Mode | Use Case |
|---|---|
| **Private (default)** | User uploads, internal assets |
| **Public Read** | Images, static assets, public files |
| **Signed-access URLs** | Limited-time external file sharing |
| **Proxy download route via Hono** | Controlled rule-based access |

This skill selects approach based on context.

**Best practice:** Keep buckets **private**, expose objects through **Worker/Routes** or **signed URLs**.


---

## Private Access (Recommended Default)

Use Cloudflare Worker as controlled access:

```ts
app.get("/file/:key", async (c) => {
  const key = decodeURIComponent(c.req.param("key"));

  const obj = await c.env.BUCKET.get(key);
  if (!obj) return c.notFound();

  return new Response(obj.body, {
    headers: { "Content-Type": obj.httpMetadata?.contentType ?? "application/octet-stream" }
  });
});
```

This enables auth-check:

```ts
if (!c.get("user")) return c.json({ auth: false }, 401);
```


---

## Public Access Mode

Enable public read with bucket policy:

```bash
wrangler r2 bucket policy put BUCKET << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "r2:GetObject",
      "Resource": "BUCKET/*"
    }
  ]
}
EOF
```

Use only for assets intended to be publicly hosted (CDN optimized).


---

## Upload Handling (secure)

```ts
const file = await c.req.formData().then(f => f.get("file") as File);
const key = `users/${c.get("user")?.id}/${Date.now()}-${file.name}`;

await c.env.BUCKET.put(key, await file.arrayBuffer(), {
  httpMetadata: { contentType: file.type }
});

return c.json({ key, url: `/file/${encodeURIComponent(key)}` });
```

The skill ensures safe naming conventions:

- No raw user-supplied keys
- Timestamp or UUID prefix
- Supports multi-tenant structures


---

## R2 Lifecycle Policies

Claude may apply retention or expiration policy suggestions:

| Policy | Benefit |
|---|---|
| Auto-delete after X days | Temporary file cleanup |
| Move to cold storage after X | Cost reduction |
| Prevent overwrite unless flagged | Audit safety |

Example JSON policy reference:

```json
{
  "Rules": [
    {
      "ID": "auto-expire-temp",
      "Filter": { "Prefix": "temp/" },
      "Expiration": { "Days": 30 }
    }
  ]
}
```


---

## Signed URL Access (download/share)

Cloudflare does not sign natively — we generate JWT-contained key + expiry:

```ts
import { SignJWT, jwtVerify } from "jose";

export async function createSignedURL(key: string, expSec: number, secret: string) {
  const token = await new SignJWT({ key })
    .setProtectedHeader({ alg: "HS256" })
    .setExpirationTime(Math.floor(Date.now()/1000) + expSec)
    .sign(new TextEncoder().encode(secret));

  return `/download/${token}`;
}

app.get("/download/:token", async (c) => {
  const secret = c.env.JWT_SECRET;
  const { payload } = await jwtVerify(c.req.param("token"), new TextEncoder().encode(secret));
  const obj = await c.env.BUCKET.get(payload.key);
  if(!obj) return c.notFound();
  return new Response(obj.body);
});
```

This simulates **presigned URLs safely**.


---

## Directory-like Prefixing

Claude may suggest folder-style structure for organization:

```
/public/assets/*
/users/[id]/uploads/*
/tenants/[id]/invoices/*
/tmp/uploads/*
```

Naming rules enforced by this skill:

- Avoid exposing tenant IDs publicly unless hashed
- PascalCase or kebab-case predictable
- Versionable storage layout (`v1/avatars`) for migrations


---

## Listing + Search

```ts
const result = await c.env.BUCKET.list({ prefix: `users/${id}/` });
return c.json(result.objects.map(o => ({ key: o.key, size: o.size, date: o.uploaded })));
```

Skill advises pagination if results exceed limits.


---

## CI/CD Hooks For R2 Deployments

This skill suggests combining with future CI/CD workflow:

```bash
wrangler deploy --env production
```
Then apply bucket policy or migration tasks post-deploy.

For automation:
- cache invalidation
- namespace provisioning
- retention checks


---

## Example Prompts That Activate This Skill

- “Store files in R2 with security rules.”  
- “Make public CDN bucket for static assets.”  
- “Generate signed URLs for temporary downloads.”  
- “Organize tenant bucket structure cleanly.”  
- “Set expiration policy for old file uploads.”  


---

## Interactions With Other Skills

| Skill | How it connects |
|---|---|
| `hono-r2-integration` | This skill expands it with policy, access control, public/private modes |
| `cloudflare-worker-deployment` | Ensures R2 bindings are correctly mapped across envs |
| `cloudflare-d1-migrations-and-production-seeding` | Not DB schema — but both require env-controlled versioning |
| `hono-authentication` | User-based folder ownership, signed URL verification |
