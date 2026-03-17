---
name: bknd-production-config
description: Use when preparing a Bknd application for production deployment. Covers security hardening, environment configuration, isProduction flag, JWT settings, Guard enablement, CORS, media storage, and production checklist.
---

# Configure for Production

Prepare and secure your Bknd application for production deployment.

## Prerequisites

- Working Bknd application tested locally
- Database provisioned (see `bknd-database-provision`)
- Hosting platform selected (see `bknd-deploy-hosting`)

## When to Use UI Mode

- Viewing current configuration in admin panel
- Verifying Guard settings are active
- Checking auth configuration

## When to Use Code Mode

- All production configuration changes
- Setting environment variables
- Configuring security settings
- Setting up adapters

## Code Approach

### Step 1: Enable Production Mode

Set `isProduction: true` to disable development features:

```typescript
// bknd.config.ts
export default {
  app: (env) => ({
    connection: { url: env.DB_URL },
    isProduction: true,  // or env.NODE_ENV === "production"
  }),
};
```

**What `isProduction: true` does:**
- Disables schema auto-sync (prevents accidental migrations)
- Hides detailed error messages from API responses
- Disables admin panel modifications (read-only)
- Enables stricter security defaults

### Step 2: Configure JWT Authentication

**Critical:** Never use default or weak JWT secrets in production.

```typescript
export default {
  app: (env) => ({
    connection: { url: env.DB_URL },
    isProduction: true,
    auth: {
      jwt: {
        secret: env.JWT_SECRET,  // Required, min 32 chars
        alg: "HS256",            // Or "HS384", "HS512"
        expires: "7d",           // Token lifetime
        issuer: "my-app",        // Optional, identifies token source
        fields: ["id", "email", "role"],  // Claims in token
      },
      cookie: {
        httpOnly: true,          // Prevent XSS access
        secure: true,            // HTTPS only
        sameSite: "strict",      // CSRF protection
        expires: 604800,         // 7 days in seconds
      },
    },
  }),
};
```

**Generate secure secret:**

```bash
# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# OpenSSL
openssl rand -hex 32
```

### Step 3: Enable Guard (Authorization)

```typescript
export default {
  app: (env) => ({
    connection: { url: env.DB_URL },
    isProduction: true,
    config: {
      guard: {
        enabled: true,  // Enforce all permissions
      },
    },
  }),
};
```

Without Guard enabled, all authenticated users have full access.

### Step 4: Configure CORS

```typescript
export default {
  app: (env) => ({
    // ...
    config: {
      server: {
        cors: {
          origin: env.ALLOWED_ORIGINS?.split(",") ?? ["https://myapp.com"],
          credentials: true,  // Allow cookies
          methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
        },
      },
    },
  }),
};
```

### Step 5: Configure Media Storage

**Never use local storage in production serverless.** Use cloud providers:

```typescript
// AWS S3
export default {
  app: (env) => ({
    // ...
    config: {
      media: {
        enabled: true,
        body_max_size: 10 * 1024 * 1024,  // 10MB max upload
        adapter: {
          type: "s3",
          config: {
            bucket: env.S3_BUCKET,
            region: env.S3_REGION,
            accessKeyId: env.S3_ACCESS_KEY,
            secretAccessKey: env.S3_SECRET_KEY,
          },
        },
      },
    },
  }),
};

// Cloudflare R2
config: {
  media: {
    adapter: {
      type: "r2",
      config: { bucket: env.R2_BUCKET },
    },
  },
}

// Cloudinary
config: {
  media: {
    adapter: {
      type: "cloudinary",
      config: {
        cloudName: env.CLOUDINARY_CLOUD,
        apiKey: env.CLOUDINARY_KEY,
        apiSecret: env.CLOUDINARY_SECRET,
      },
    },
  },
}
```

---

## Complete Production Configuration

```typescript
// bknd.config.ts
import type { CliBkndConfig } from "bknd";
import { em, entity, text, relation, enumm } from "bknd";

const schema = em(
  {
    users: entity("users", {
      email: text().required().unique(),
      name: text(),
      role: enumm(["admin", "user"]).default("user"),
    }),
    posts: entity("posts", {
      title: text().required(),
      content: text(),
      published: enumm(["draft", "published"]).default("draft"),
    }),
  },
  ({ users, posts }) => ({
    post_author: relation(posts, users),  // posts.author_id -> users
  })
);

type Database = (typeof schema)["DB"];
declare module "bknd" {
  interface DB extends Database {}
}

export default {
  app: (env) => ({
    // Database
    connection: {
      url: env.DB_URL,
      authToken: env.DB_TOKEN,
    },

    // Schema
    schema,

    // Production mode
    isProduction: env.NODE_ENV === "production",

    // Authentication
    auth: {
      enabled: true,
      jwt: {
        secret: env.JWT_SECRET,
        alg: "HS256",
        expires: "7d",
        fields: ["id", "email", "role"],
      },
      cookie: {
        httpOnly: true,
        secure: env.NODE_ENV === "production",
        sameSite: "strict",
        expires: 604800,
      },
      strategies: {
        password: {
          enabled: true,
          hashing: "bcrypt",
          rounds: 12,
          minLength: 8,
        },
      },
      allow_register: true,
      default_role_register: "user",
    },

    // Authorization
    config: {
      guard: {
        enabled: true,
      },
      roles: {
        admin: {
          implicit_allow: true,  // Full access
        },
        user: {
          implicit_allow: false,
          permissions: [
            "data.posts.read",
            {
              permission: "data.posts.create",
              effect: "allow",
            },
            {
              permission: "data.posts.update",
              effect: "filter",
              condition: { author_id: "@user.id" },
            },
            {
              permission: "data.posts.delete",
              effect: "filter",
              condition: { author_id: "@user.id" },
            },
          ],
        },
        anonymous: {
          implicit_allow: false,
          is_default: true,  // Unauthenticated users
          permissions: [
            {
              permission: "data.posts.read",
              effect: "filter",
              condition: { published: "published" },
            },
          ],
        },
      },

      // Media storage
      media: {
        enabled: true,
        body_max_size: 10 * 1024 * 1024,
        adapter: {
          type: "s3",
          config: {
            bucket: env.S3_BUCKET,
            region: env.S3_REGION,
            accessKeyId: env.S3_ACCESS_KEY,
            secretAccessKey: env.S3_SECRET_KEY,
          },
        },
      },

      // CORS
      server: {
        cors: {
          origin: env.ALLOWED_ORIGINS?.split(",") ?? [],
          credentials: true,
        },
      },
    },
  }),
} satisfies CliBkndConfig;
```

---

## Environment Variables Template

Create `.env.production` or set in your platform:

```bash
# Required
NODE_ENV=production
DB_URL=libsql://your-db.turso.io
DB_TOKEN=your-turso-token
JWT_SECRET=your-64-char-random-secret-here-generate-with-openssl

# CORS
ALLOWED_ORIGINS=https://myapp.com,https://www.myapp.com

# Media Storage (S3)
S3_BUCKET=my-bucket
S3_REGION=us-east-1
S3_ACCESS_KEY=AKIA...
S3_SECRET_KEY=secret...

# Or Cloudinary
CLOUDINARY_CLOUD=my-cloud
CLOUDINARY_KEY=123456
CLOUDINARY_SECRET=secret

# OAuth (if used)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
```

---

## Security Checklist

### Authentication

- [ ] JWT secret is 32+ characters, randomly generated
- [ ] JWT secret stored in environment variable, not code
- [ ] Cookie `httpOnly: true` set
- [ ] Cookie `secure: true` in production (HTTPS)
- [ ] Cookie `sameSite: "strict"` or `"lax"`
- [ ] Password hashing uses bcrypt with rounds >= 10
- [ ] Minimum password length enforced (8+ chars)

### Authorization

- [ ] Guard enabled (`guard.enabled: true`)
- [ ] Default role defined for anonymous users
- [ ] Admin role does NOT use `implicit_allow` unless intended
- [ ] Sensitive entities have explicit permissions
- [ ] Row-level security filters user-owned data

### Data

- [ ] `isProduction: true` set
- [ ] Database credentials in environment variables
- [ ] No test/seed data in production
- [ ] Backups configured for database

### Media

- [ ] Cloud storage configured (not local filesystem)
- [ ] Storage credentials in environment variables
- [ ] CORS configured on storage bucket
- [ ] Max upload size limited (`body_max_size`)

### Network

- [ ] CORS origins explicitly listed (no wildcard `*`)
- [ ] HTTPS enforced (via platform/proxy)
- [ ] API rate limiting configured (if needed)

---

## Platform-Specific Security

### Cloudflare Workers

```typescript
// Secrets set via wrangler
// wrangler secret put JWT_SECRET
// wrangler secret put DB_TOKEN

export default hybrid<CloudflareBkndConfig>({
  app: (env) => ({
    connection: d1Sqlite({ binding: env.DB }),
    isProduction: true,
    auth: {
      jwt: { secret: env.JWT_SECRET },
      cookie: {
        httpOnly: true,
        secure: true,
        sameSite: "strict",
      },
    },
  }),
});
```

### Vercel

```bash
# Set via Vercel CLI or dashboard
vercel env add JWT_SECRET production
vercel env add DB_URL production
vercel env add DB_TOKEN production
```

### Docker

```yaml
# docker-compose.yml
services:
  bknd:
    environment:
      - NODE_ENV=production
      - JWT_SECRET=${JWT_SECRET}  # From .env or host
    # Never put secrets directly in docker-compose.yml
```

---

## Testing Production Config Locally

Test with production-like settings before deploying:

```bash
# Create .env.production.local (gitignored)
NODE_ENV=production
DB_URL=libsql://test-db.turso.io
DB_TOKEN=test-token
JWT_SECRET=test-secret-min-32-characters-here

# Run with production env
NODE_ENV=production bun run index.ts

# Or source the file
source .env.production.local && bun run index.ts
```

**Verify:**
1. Admin panel is read-only (no schema changes)
2. API errors don't expose stack traces
3. Auth requires valid JWT
4. Guard enforces permissions

---

## Common Pitfalls

### "JWT_SECRET required" Error

**Problem:** Auth fails at startup

**Fix:** Ensure JWT_SECRET is set and accessible:
```bash
# Check env is loaded
echo $JWT_SECRET

# Cloudflare: set secret
wrangler secret put JWT_SECRET

# Docker: pass env
docker run -e JWT_SECRET="your-secret" ...
```

### Guard Not Enforcing Permissions

**Problem:** Users can access everything

**Fix:** Ensure Guard is enabled:
```typescript
config: {
  guard: {
    enabled: true,  // Must be true!
  },
}
```

### Cookies Not Set (CORS Issues)

**Problem:** Auth works in Postman but not browser

**Fix:**
```typescript
auth: {
  cookie: {
    sameSite: "lax",  // "strict" may block OAuth redirects
    secure: true,
  },
},
config: {
  server: {
    cors: {
      origin: ["https://your-frontend.com"],  // Explicit, not "*"
      credentials: true,
    },
  },
}
```

### Admin Panel Allows Changes

**Problem:** Schema can be modified in production

**Fix:** Set `isProduction: true`:
```typescript
isProduction: true,  // Locks admin to read-only
```

### Detailed Errors Exposed

**Problem:** API returns stack traces

**Fix:** `isProduction: true` hides internal errors. Also check for custom error handlers exposing details.

---

## DOs and DON'Ts

**DO:**
- Set `isProduction: true` in production
- Generate cryptographically secure JWT secrets (32+ chars)
- Enable Guard for authorization
- Use cloud storage for media
- Set explicit CORS origins
- Use environment variables for all secrets
- Test production config locally first
- Enable HTTPS (via platform/proxy)
- Set cookie `secure: true` and `httpOnly: true`

**DON'T:**
- Use default or weak JWT secrets
- Commit secrets to version control
- Use wildcard (`*`) CORS origins
- Leave Guard disabled in production
- Use local filesystem storage in serverless
- Expose detailed error messages
- Skip the security checklist
- Use `sha256` password hashing (use `bcrypt`)
- Set `implicit_allow: true` on non-admin roles

---

## Related Skills

- **bknd-deploy-hosting** - Deploy to hosting platforms
- **bknd-database-provision** - Set up production database
- **bknd-env-config** - Environment variable setup
- **bknd-setup-auth** - Authentication configuration
- **bknd-create-role** - Define authorization roles
- **bknd-storage-config** - Media storage setup
