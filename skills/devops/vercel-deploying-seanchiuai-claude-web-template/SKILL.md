---
name: "Vercel Deployment"
description: "Automatically deploys to Vercel production, uses Vercel MCP to fetch build logs, analyzes errors, fixes them, and retries until successful deployment. Use when deploying to production or fixing deployment issues."
tools: Bash, Read, Edit, Write
model: inherit
---

# Skill: Vercel Deployment

Complete guide for deploying Next.js applications to Vercel with automatic error fixing, environment configuration, and troubleshooting.

## When to Use

- Deploying Next.js app to Vercel production
- Fixing deployment build errors
- Configuring environment variables
- Setting up image optimization domains
- Troubleshooting production deployment issues
- Automating deploy-fix-redeploy loops

## Domain Knowledge

### Critical Patterns

#### Environment Variables Must Be Set in Dashboard (CRITICAL)

Environment variables for production deployments MUST be configured in the Vercel dashboard, not just in local `.env.local`.

**Where to set:**
1. Go to Vercel dashboard
2. Select your project
3. Settings → Environment Variables
4. Add variables for Production, Preview, and/or Development

**Common variables to set:**
```bash
# Convex
CONVEX_DEPLOYMENT=prod:your-deployment
NEXT_PUBLIC_CONVEX_URL=https://your-deployment.convex.cloud

# Clerk Auth
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_xxx
CLERK_SECRET_KEY=sk_live_xxx
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up

# Other services
STRIPE_SECRET_KEY=sk_live_xxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
```

**Why this matters:** Build will fail with "Missing environment variable" errors if not set in dashboard.

#### NEXT_PUBLIC_ Prefix for Client-Side Variables

Environment variables used in the browser MUST have the `NEXT_PUBLIC_` prefix.

```typescript
// ❌ Wrong - not available in browser
const apiUrl = process.env.API_URL;

// ✅ Correct - accessible in browser
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

**Rule:**
- **Server-only**: No prefix (e.g., `CLERK_SECRET_KEY`)
- **Client-accessible**: `NEXT_PUBLIC_` prefix (e.g., `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`)

**Why:** Next.js only bundles variables with `NEXT_PUBLIC_` prefix into the client bundle for security.

#### Image Domain Configuration

Next.js Image component requires remote domains to be configured in `next.config.ts`:

```typescript
// next.config.ts
const config = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'img.clerk.com',
      },
      {
        protocol: 'https',
        hostname: '*.convex.cloud',
      },
      {
        protocol: 'https',
        hostname: 'your-cdn.com',
      },
    ],
  },
};
```

**Why:** Vercel blocks unconfigured image domains for security and optimization.

#### Git Push Triggers Automatic Deployment

Vercel automatically deploys when you push to connected Git repository:

- **Main branch** → Production deployment
- **Other branches** → Preview deployment
- **Pull requests** → Preview deployment with unique URL

**Manual deployment:**
```bash
vercel --prod  # Deploy to production
vercel         # Deploy to preview
```

### Key Files

- **next.config.ts** - Next.js configuration (images, redirects, env vars)
- **.env.example** - Template for required environment variables
- **vercel.json** - Vercel deployment configuration (optional)
- **package.json** - Build scripts and dependencies

### Build Process

Vercel build process:

1. **Install dependencies** - `npm install` or equivalent
2. **Run build script** - `npm run build`
3. **Generate pages** - Static and dynamic routes
4. **Optimize assets** - Images, fonts, scripts
5. **Deploy** - Upload to CDN

**Build must succeed** for deployment to complete.

## Automatic Deployment Workflow

### Instructions

When requested to deploy to Vercel production with automatic error fixing:

1. **Initial Deployment Attempt**
   - Run `vercel --prod` to start production deployment
   - Wait for deployment to complete

2. **Error Detection & Analysis**
   - **CRITICAL**: Use Vercel MCP tool to fetch detailed logs:
     - The MCP logs provide much more detail than CLI output
   - Analyze the build logs to identify root cause:
     - Build errors (TypeScript, ESLint, compilation)
     - Runtime errors
     - Environment variable issues
     - Dependency problems
     - Configuration issues
   - Extract specific error messages

3. **Error Fixing**
   - Make minimal, targeted fixes to resolve the specific error

4. **Retry Deployment**
   - Run `vercel --prod` again with the fixes applied
   - Repeat steps until deployment succeeds

5. **Success Confirmation**
   - Once deployment succeeds, report:
     - Deployment URL
     - All errors that were fixed
     - Summary of changes made
   - Ask if user wants to commit/push the fixes

## Loop Exit Conditions

- ✅ Deployment succeeds
- ❌ SAME error occurs 5+ times (suggest manual intervention)
- ❌ User requests to stop

## Best Practices
- Make incremental fixes rather than large refactors
- Preserve user's code style and patterns when fixing

## Troubleshooting

### Issue: Build Fails with Missing Environment Variables

**Symptoms:**
- Build error: "Environment variable 'X' is not defined"
- Build succeeds locally but fails on Vercel
- Variables set in `.env.local` but not working in production

**Cause:** Environment variables not configured in Vercel dashboard

**Solution:**

1. Go to Vercel dashboard
2. Select project → Settings → Environment Variables
3. Add missing variables for Production environment
4. Redeploy (or trigger by pushing to Git)

**Check for correct prefix:**
- Client-side vars need `NEXT_PUBLIC_` prefix
- Server-side vars don't need prefix

**Frequency:** High (very common issue)

### Issue: Images Not Loading in Production

**Symptoms:**
- Images work locally
- Production shows broken image or error
- Console error: "Invalid src prop"

**Cause:** Image domains not configured in `next.config.ts`

**Solution:**

Add remote domains to `next.config.ts`:

```typescript
const config = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'your-image-host.com',
      },
    ],
  },
};
```

Common image hosts:
- Clerk: `img.clerk.com`
- Convex: `*.convex.cloud`
- Cloudinary: `res.cloudinary.com`

**Frequency:** Medium

### Issue: Build Succeeds Locally But Fails on Vercel

**Possible Causes:**

**1. TypeScript errors ignored locally**
- Solution: Run `npm run build` locally to catch errors
- Check `next.config.ts` for `typescript.ignoreBuildErrors`

**2. ESLint errors**
- Solution: Run `npm run lint` to check
- Fix errors or configure rules appropriately

**3. Missing dependencies**
- Solution: Ensure all imports are in `package.json` dependencies
- Run `npm install` to verify

**4. Environment-specific code**
- Solution: Check for hardcoded values that differ between environments
- Use environment variables for environment-specific config

**Frequency:** Medium

### Issue: Deployment Stuck or Taking Too Long

**Symptoms:**
- Deployment shows "Building..." for extended period
- No error messages
- Build logs show no progress

**Possible Causes:**

**1. Large dependencies**
- Solution: Check `package.json` for unnecessary large packages
- Consider code splitting or lazy loading

**2. Build timeout**
- Solution: Optimize build process
- Check for infinite loops in build scripts

**3. Vercel platform issue**
- Solution: Check Vercel status page
- Try redeploying after a few minutes

**Frequency:** Low

## Example Flow

**User:** "Deploy to production and fix any errors"


- Vercel MCP build logs are the PRIMARY source of error information
- CLI output alone is insufficient for proper error diagnosis
- Always wait for deployment to complete before fetching logs
- If errors require user input (like API keys), prompt user immediately

## References

- **Previous expertise**: `.claude/experts/vercel-expert/expertise.yaml`
- **Agent integration**: `.claude/agents/agent-vercel.md`
- **Official docs**: https://vercel.com/docs
