---
name: netlify-integration
description: Deploy and manage Netlify projects using Next.js with serverless functions, environment variables, and continuous deployment. Use this skill when working with Netlify deployments, configuring netlify.toml, managing Netlify Functions, debugging webhooks, setting environment variables, or troubleshooting deployment issues for Next.js applications on Netlify. Essential for Twilio-Aldea and similar serverless SMS/telephony projects. v2.0 includes official Netlify documentation, production patterns from Twilio-Aldea (webhook timeout solutions, background functions), and TypeScript code examples.
---

# Netlify Integration

## When to Use This Skill

Use this skill when you need to:

**Deployment & Configuration:**
- Deploy a Next.js application to Netlify
- Configure `netlify.toml` for build settings, functions, redirects, or headers
- Set up environment variables in Netlify Dashboard or CLI
- Configure continuous deployment from Git (GitHub, GitLab, Bitbucket)

**Functions Development:**
- Create Netlify serverless functions
- Handle webhooks (Twilio, Telnyx, Stripe, etc.)
- Debug function timeout issues (10s limit on free tier, 26s on Pro)
- Implement background processing for long-running tasks

**Troubleshooting:**
- Fix webhook timeout errors (especially for SMS/telephony apps)
- Debug "Function not found" (404) errors
- Resolve environment variable issues
- Fix build failures or deployment errors

**SMS/Telephony Projects:**
- Working on projects like Twilio-Aldea that handle SMS webhooks
- Implementing immediate webhook acknowledgment + background processing
- Validating webhook signatures (Twilio, Telnyx)

## Quick Reference

### 1. Basic Netlify Function Handler

```typescript
import type { Handler, HandlerEvent, HandlerContext } from "@netlify/functions";

export const handler: Handler = async (
  event: HandlerEvent,
  context: HandlerContext
) => {
  try {
    const body = JSON.parse(event.body || "{}");

    // Process request
    console.log("Request received:", body);

    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ success: true }),
    };
  } catch (error) {
    console.error("Error:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Internal server error" }),
    };
  }
};
```

### 2. Webhook with Immediate Response (Critical Pattern)

**Solves the 60% message loss problem - return 200 immediately, process async:**

```typescript
export const handler: Handler = async (event, context) => {
  // Validate webhook signature
  const isValid = validateWebhook(event);
  if (!isValid) {
    return { statusCode: 401, body: "Unauthorized" };
  }

  // IMMEDIATE: Return 200 OK (< 200ms)
  const response = {
    statusCode: 200,
    body: JSON.stringify({ received: true }),
  };

  // BACKGROUND: Process async (don't await)
  processWebhookAsync(event.body).catch(console.error);

  return response;
};
```

### 3. Essential netlify.toml for Next.js

```toml
[build]
  command = "npm run build"
  publish = ".next"

[build.environment]
  NODE_VERSION = "18"
  NEXT_TELEMETRY_DISABLED = "1"

[[plugins]]
  package = "@netlify/plugin-nextjs"

[functions]
  directory = ".netlify/functions"
  node_bundler = "esbuild"

# API rewrites
[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
  force = true

# Security headers
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
```

### 4. Environment Variables Setup (CLI)

**Prerequisites - Link Project First:**
```bash
# Option 1: Interactive linking
netlify link

# Option 2: Manual linking (create .netlify/state.json)
mkdir -p .netlify
echo '{"siteId":"YOUR-SITE-ID-HERE"}' > .netlify/state.json

# Find your site ID
netlify sites:list  # Shows all sites with their IDs

# Verify link worked
netlify status
```

**Managing Environment Variables:**
```bash
# Set single variable (use --force to skip confirmation)
netlify env:set VARIABLE_NAME value
netlify env:set VARIABLE_NAME "value with spaces" --force

# Set for specific context (production, deploy-preview, branch-deploy, dev)
netlify env:set VARIABLE_NAME value --context production

# Import from .env file
netlify env:import .env.production

# List all variables
netlify env:list

# Get specific variable value
netlify env:get VARIABLE_NAME

# Delete variable
netlify env:unset VARIABLE_NAME

# Clone variables from another site
netlify env:clone --from OTHER_SITE_ID
```

**Bulk Add Example (from shell):**
```bash
# Add multiple env vars in sequence
netlify env:set API_KEY "sk-xxx" --force
netlify env:set ENABLE_FEATURE "true" --force
netlify env:set NEXT_PUBLIC_APP_URL "https://myapp.netlify.app" --force
```

**Note:** After adding/changing env vars, you may need to trigger a redeploy for changes to take effect in production.

### 5. Function Timeout Configuration

```toml
[functions]
  directory = ".netlify/functions"
  timeout = 10  # Default for all functions

# Increase timeout for specific function
[[functions."webhook"]]
  timeout = 26  # Max for Pro tier (10s for free)
```

### 6. Raw Body Parsing for Signature Validation

**Critical for Twilio/Telnyx webhook signature validation:**

```typescript
export const config = {
  api: {
    bodyParser: false,  // Disable Next.js body parsing
  },
};

async function readRawBody(req: NextApiRequest): Promise<string> {
  return new Promise<string>((resolve, reject) => {
    let data = '';
    req.setEncoding('utf8');
    req.on('data', (chunk) => { data += chunk; });
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const rawBody = await readRawBody(req);

  // Validate signature with raw body
  const isValid = validateSignature(rawBody, req.headers['x-twilio-signature']);
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  // Process webhook...
}
```

### 7. Database Error Logging Pattern

```typescript
export const handler: Handler = async (event) => {
  try {
    await processMessage(data);
    return { statusCode: 200, body: 'Success' };
  } catch (error: unknown) {
    const err = error instanceof Error ? error : new Error(String(error));
    console.error('[Function] Error:', err);

    // Log to database for visibility
    await supabase.from('processing_errors').insert({
      error_message: err.message,
      error_stack: err.stack,
      created_at: new Date().toISOString(),
    });

    return { statusCode: 500, body: `Error: ${err.message}` };
  }
};
```

### 8. Connection Pooling Pattern

```typescript
// Reuse connections across function invocations
let supabaseClient: any = null;

function getSupabaseClient() {
  if (!supabaseClient) {
    supabaseClient = createClient(
      process.env.SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_KEY!
    );
  }
  return supabaseClient;
}

export const handler: Handler = async (event, context) => {
  const supabase = getSupabaseClient();
  // Use cached client - reduces cold start time
};
```

### 9. Dynamic Base URL Detection

```typescript
function getBaseUrl(req: NextApiRequest): string {
  const proto = (req.headers['x-forwarded-proto'] as string) || 'https';
  const host = (req.headers['x-forwarded-host'] as string) || (req.headers.host as string);
  return `${proto}://${host}`;
}

// Works in production, preview deploys, and localhost
const baseUrl = getBaseUrl(req);
const backgroundUrl = `${baseUrl}/.netlify/functions/background`;
```

### 10. Input Validation with Zod

```typescript
import { z } from "zod";

const WebhookSchema = z.object({
  from: z.string().min(10).max(15),
  to: z.string().min(10).max(15),
  body: z.string().min(1).max(1600),
  messageId: z.string().uuid(),
});

export const handler: Handler = async (event, context) => {
  try {
    const data = JSON.parse(event.body || "{}");
    const validated = WebhookSchema.parse(data);

    await processMessage(validated);
    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: "Validation failed", details: error.errors }),
      };
    }
    throw error;
  }
};
```

## Key Concepts

### Netlify Functions
- **Serverless functions** that run on AWS Lambda
- Located in `.netlify/functions/` directory
- Support Node.js, TypeScript, Go
- **Timeout limits**: 10s (free tier), 26s (Pro tier)
- **Background functions**: Name with `-background.ts` suffix for 15-minute timeout

### netlify.toml
- **File-based configuration** for Netlify deployments
- Place in repository root
- Controls build settings, functions, redirects, headers
- Supports **context-specific** configs (production, deploy-preview, branch-deploy)

### Environment Variables
- **Server-side**: Access via `process.env.VARIABLE_NAME` (any name)
- **Client-side**: Must prefix with `NEXT_PUBLIC_` to expose to browser
- Set in **Netlify Dashboard** (Site Settings → Environment Variables) or via CLI
- **Never commit** `.env` files to Git

### Webhook Timeout Problem
- SMS providers (Twilio/Telnyx) require response within **10 seconds**
- AI processing takes **15-25 seconds**
- **Solution**: Return 200 immediately, process async in background function
- **Result**: 0% timeout rate (from 60% failure)

### Background Functions
- Automatically detected by filename: `function-name-background.ts`
- **15-minute timeout** (vs 10-26s for regular functions)
- Perfect for long-running AI processing, data processing, etc.
- No additional configuration needed

### Next.js + Netlify Integration
- Requires `@netlify/plugin-nextjs` plugin
- Handles ISR, SSR, and static page generation
- API routes automatically converted to serverless functions
- Custom functions go in `.netlify/functions/` (separate from `pages/api/`)

## Reference Files

### Core Configuration
- **`references/netlify_config.md`** - Complete netlify.toml reference with all configuration options (build, functions, redirects, headers, contexts)
- **`references/environment_variables.md`** - Environment variable management, scopes, client vs server, bulk import/export

### Functions Development
- **`references/functions_best_practices.md`** - Patterns for functions: async processing, error handling, security, database operations, monitoring
- **`references/production-patterns.md`** - 8 real-world patterns from Twilio-Aldea production (webhook timeouts, background processing, error logging)

### Troubleshooting
- **`references/debugging.md`** - Comprehensive debugging guide for build failures, function errors, webhook issues, database problems

### Official Netlify Documentation
- **`references/official-docs/functions.md`** - Complete Netlify Functions guide with handler types, event structure, deployment
- **`references/official-docs/environment-variables.md`** - Environment variable configuration, scopes, runtime access
- **`references/official-docs/netlify-toml.md`** - File-based configuration reference
- **`references/official-docs/nextjs.md`** - Next.js framework integration, ISR, SSR, optimization

### Code Examples
- **`assets/examples/webhook-function.ts`** - Webhook handler with immediate response pattern
- **`assets/examples/background-function.ts`** - Background function for long-running processing
- **`assets/examples/netlify.toml`** - Complete configuration example with comments
- **`assets/examples/api-route.ts`** - Next.js API route with raw body parsing and signature validation

### Project-Specific
- **`references/twilio_aldea_specific.md`** - Patterns specific to Twilio-Aldea SMS platform (webhook handling, session management, unified provider interface)

### GitHub Repository (NEW)

#### `references/github/README.md`
Official Netlify CLI README from GitHub (netlify/cli, 1,752 stars)

#### `references/github/issues.md`
12 GitHub issues showing common problems and solutions:
- Build failures and deployment errors
- Environment variable issues
- Function timeout problems
- Redirects and routing configuration
- Local development setup

#### `references/github/CHANGELOG.md`
Complete version history with breaking changes and new features

#### `references/github/releases.md`
1,203 GitHub releases with detailed CLI changelog

#### `references/github/file_structure.md`
Repository structure (871 files) showing CLI source code organization

## Working with This Skill

### For Beginners

**Start here if you're new to Netlify:**

1. **Deploy your first app:**
   - Review the "Initial Deployment (Git Integration)" section below
   - Follow the step-by-step workflow
   - Use Quick Reference #3 as your starting `netlify.toml` template

2. **Understand the basics:**
   - Read `references/official-docs/functions.md` for Netlify Functions basics
   - Review the simple examples in Quick Reference (#1, #4)
   - Study `references/official-docs/environment-variables.md` for environment setup

3. **Create your first function:**
   - Copy the Basic Function Handler example (#1)
   - Place in `.netlify/functions/hello.ts`
   - Deploy and test at `https://yoursite.netlify.app/.netlify/functions/hello`

### For Intermediate Users

**Already familiar with Netlify basics:**

1. **Implement production patterns:**
   - Study `references/production-patterns.md` for real-world examples
   - Implement Pattern 1 (immediate response + background processing) if handling webhooks
   - Review Pattern 5 (error logging to database) for better monitoring

2. **Optimize your setup:**
   - Add connection pooling (#8) to reduce cold starts
   - Implement proper error handling with database logging (#7)
   - Add input validation with Zod (#10)

3. **Handle complex scenarios:**
   - Learn raw body parsing (#6) for webhook signature validation
   - Configure context-specific builds in `netlify.toml`
   - Set up proxy patterns for API calls (Pattern 4 in production-patterns.md)

### For Advanced Users

**Building production-grade serverless apps:**

1. **Master webhook handling:**
   - Deep dive into `references/production-patterns.md` Pattern 1 (webhook timeout solution)
   - Implement signature validation for Twilio/Telnyx webhooks
   - Design multi-function architectures (API routes + background functions)

2. **Performance optimization:**
   - Study cold start reduction techniques in `references/functions_best_practices.md`
   - Implement lazy loading for heavy dependencies
   - Configure function memory and timeout appropriately

3. **Advanced debugging:**
   - Use structured logging patterns for better observability
   - Implement performance metrics tracking
   - Set up comprehensive error logging with database persistence

4. **Multi-environment setup:**
   - Configure context-specific environments (production, staging, development)
   - Manage environment variables across contexts
   - Implement feature flags and A/B testing patterns

## Common Workflows

### Deploying a Next.js App to Netlify

1. **Prepare repository:**
   ```bash
   # Add netlify.toml (use Quick Reference #3 as template)
   # Add .env.example with all required variables
   git add netlify.toml .env.example
   git commit -m "Add Netlify configuration"
   git push origin main
   ```

2. **Connect to Netlify:**
   - Visit Netlify Dashboard → "Add new site" → "Import an existing project"
   - Select Git provider and repository
   - Build settings auto-detected via netlify.toml

3. **Set environment variables:**
   ```bash
   netlify env:set VARIABLE_NAME value
   # Or use Netlify Dashboard: Site Settings → Environment Variables
   ```

4. **Deploy:**
   - Automatic on git push, or manual: `netlify deploy --prod`

### Fixing Webhook Timeout Issues

**Symptom:** 60% message loss, 504 Gateway Timeout errors

**Solution:**
1. Identify if processing takes > 10 seconds
2. Implement immediate response pattern (Quick Reference #2)
3. Create background function with `-background.ts` suffix
4. Move long-running processing to background function
5. Test with: `netlify dev` locally

**See:** `references/production-patterns.md` Pattern 1 for complete implementation

### Debugging Function Errors

1. **Check function logs:**
   ```bash
   netlify functions:log function-name --stream
   ```

2. **Add structured logging:**
   ```typescript
   console.log(JSON.stringify({
     timestamp: new Date().toISOString(),
     level: "error",
     message: "Error details",
     context: { requestId: context.requestId }
   }));
   ```

3. **Test locally:**
   ```bash
   netlify dev
   # Test at http://localhost:8888/.netlify/functions/function-name
   ```

4. **Review common issues:**
   - See `references/debugging.md` for comprehensive troubleshooting guide

## Version History

- **v2.0** (2025-11-01) - Enhanced with official Netlify documentation, production patterns from Twilio-Aldea, TypeScript examples, webhook timeout solutions, and comprehensive Next.js integration guide. Added 10 practical Quick Reference examples extracted from real production code.
- **v1.0** - Initial skill creation with deployment workflows, configuration, functions development, debugging

## Additional Resources

**Official Documentation:**
- [Netlify Functions](https://docs.netlify.com/functions/overview/)
- [Next.js on Netlify](https://docs.netlify.com/integrations/frameworks/next-js/)
- [Environment Variables](https://docs.netlify.com/environment-variables/overview/)

**Netlify CLI:**
- Install: `npm install -g netlify-cli`
- Login: `netlify login`
- Docs: `netlify help`

**Helper Scripts:**
- `scripts/check_deployment.sh` - Check deployment status and health
- `scripts/setup_env_vars.sh` - Bulk configure environment variables
- `scripts/test_function_locally.sh` - Test Netlify functions locally
