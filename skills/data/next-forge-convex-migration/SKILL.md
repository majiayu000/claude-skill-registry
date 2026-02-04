---
name: next-forge-convex-migration
description: Automate full migration from single Next.js/Convex app to Next Forge Turborepo monorepo with programmatic Vercel deployment, API key setup via marketplace, and browser-based testing
---

# Next Forge Convex Migration Skill

## Purpose

Fully automated migration from a single Next.js application with Convex backend to a Next Forge Turborepo monorepo, including:
- Programmatic Next Forge setup and configuration
- Complete Prisma/PostgreSQL removal
- Convex backend integration (schema + functions)
- Vercel marketplace integration for API keys
- Automated Doppler secret management
- End-to-end Vercel deployment
- Browser-based testing and validation

## When to Use This Skill

Use this skill when:
- Migrating from single Next.js app to Next Forge monorepo
- Current project uses Convex backend
- Need to remove Prisma/PostgreSQL dependencies
- Want programmatic Vercel deployment setup
- Need automated API key configuration via Vercel marketplace
- Require browser-based testing validation

**DO NOT use this skill when:**
- Project doesn't use Convex (uses Prisma/PostgreSQL)
- Not migrating to Next Forge
- Manual deployment preferred

## Prerequisites

**Required Tools:**
```bash
- node >= 18
- pnpm >= 10
- bun >= 1.1.0
- git
- vercel CLI
- doppler CLI
- playwright
```

**Environment Setup:**
```bash
# Verify tools
node --version    # >= 18
pnpm --version    # >= 10
bun --version     # >= 1.1.0
vercel --version  # latest
doppler --version # latest

# Login to services
vercel login
doppler login
```

**Required Access:**
- Vercel account with deployment permissions
- Doppler project with secret access
- GitHub repository access
- Convex project access
- Clerk authentication keys

## Migration Workflow

### Phase 0: Knowledge Base & Foundation

**Step 0.1: Create and Copy Knowledge Base**

IMPORTANT: This must be done FIRST before all other phases.

```bash
# Verify knowledge base exists in current project
ls docs/FREO_KNOWLEDGE_BASE.md
# Should exist with 20,000+ words

# Copy to new project
cp docs/FREO_KNOWLEDGE_BASE.md [NEW_PROJECT_PATH]/docs/

# Verify copy
cat [NEW_PROJECT_PATH]/docs/FREO_KNOWLEDGE_BASE.md | wc -w
# Should show 20,000+ words
```

**What the knowledge base contains:**
- Company overview and brand identity
- Brand colors (Primary Blue, Safety Orange, Success Green, etc.)
- User personas (5 detailed personas)
- Common workflows (4 critical workflows)
- Compliance standards (AS1418, AS2550)
- Email template specifications
- Storybook category structure
- AI SDK 6 integration points (24 tools across 5 categories)
- Vercel AI Gateway configuration details

**Why this is first:**
The knowledge base provides context for all subsequent phases - email templates use brand colors, Storybook follows brand guidelines, AI tools implement workflows, documentation reflects personas.

### Phase 1: Project Analysis

**Step 1.1: Analyze Current Project**

```bash
# Navigate to current project
cd [CURRENT_PROJECT_PATH]

# Verify Convex backend
ls convex/schema.ts convex/_generated/
# Should show schema and generated API

# Count Convex function files
find convex -type f -name "*.ts" | wc -l
# Expected: 100+ files

# Check environment variables
doppler secrets --config prd
```

**Step 1.2: Verify Prerequisites**

Create TodoWrite checklist:
```javascript
TodoWrite({
  todos: [
    { content: "Verify Convex backend exists (schema.ts + functions)", status: "pending", activeForm: "Verifying Convex backend" },
    { content: "Check Doppler configuration and secrets", status: "pending", activeForm: "Checking Doppler" },
    { content: "Verify Vercel CLI authentication", status: "pending", activeForm: "Verifying Vercel CLI" },
    { content: "Confirm GitHub repository access", status: "pending", activeForm: "Confirming GitHub access" },
    { content: "Validate current deployment URL", status: "pending", activeForm: "Validating deployment" }
  ]
});
```

### Phase 2: Clone and Setup Next Forge

**Step 2.1: Clone Next Forge**

```bash
# Clone to sibling directory
cd [PARENT_DIRECTORY]
git clone https://github.com/vercel/next-forge.git [NEW_PROJECT_NAME]
cd [NEW_PROJECT_NAME]

# Install dependencies
pnpm install
```

**Step 2.2: Remove Unused Apps**

```bash
# Remove unnecessary apps (keep only app, web, api)
rm -rf apps/docs
rm -rf apps/email
rm -rf apps/storybook
rm -rf apps/studio

# Verify removal
ls apps/
# Should show: api, app, web
```

**Step 2.3: Update Root Configuration**

Update `package.json`:
```json
{
  "name": "[NEW_PROJECT_NAME]",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev": "turbo dev --parallel",
    "dev:convex": "bunx convex dev",
    "build": "turbo build",
    "deploy:convex": "bunx convex deploy",
    "test:e2e": "bunx playwright test"
  }
}
```

Update `turbo.json`:
```json
{
  "pipeline": {
    "build": {
      "outputs": [".next/**", "dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "app#dev": {
      "dependsOn": ["^build"]
    },
    "web#dev": {
      "dependsOn": ["^build"]
    },
    "api#dev": {
      "dependsOn": ["^build"]
    }
  }
}
```

### Phase 3: Remove Prisma/PostgreSQL

**Step 3.1: Delete Database Package**

```bash
# Remove database package entirely
rm -rf packages/database

# Verify deletion
ls packages/ | grep database
# Should return empty
```

**Step 3.2: Remove Database Dependencies**

Update `apps/app/package.json`:
```bash
# Remove @repo/database dependency
sed -i '' '/"@repo\/database":/d' apps/app/package.json
```

Update `apps/api/package.json`:
```bash
# Remove @repo/database dependency
sed -i '' '/"@repo\/database":/d' apps/api/package.json
```

**Step 3.3: Remove Database Imports**

```bash
# Find all @repo/database imports
grep -r "@repo/database" apps/ --include="*.ts" --include="*.tsx"

# Remove imports automatically
find apps/ -type f \( -name "*.ts" -o -name "*.tsx" \) \
  -exec sed -i '' '/import.*@repo\/database/d' {} +

# Clean up empty lines
find apps/ -type f \( -name "*.ts" -o -name "*.tsx" \) \
  -exec sed -i '' '/^$/N;/^\n$/d' {} +
```

**Step 3.4: Rebuild Dependencies**

```bash
# Clean node_modules
pnpm clean

# Reinstall without database package
pnpm install
```

### Phase 4: Integrate Convex Backend

**Step 4.1: Install Convex Dependencies**

```bash
# Root project
pnpm add convex

# Apps
cd apps/app && pnpm add convex convex-helpers
cd ../api && pnpm add convex
cd ../..
```

**Step 4.2: Copy Convex Backend**

```bash
# Copy entire Convex directory
cp -r [CURRENT_PROJECT_PATH]/convex ./

# Verify copy
ls convex/
# Should show schema.ts and all function directories
```

**Step 4.3: Create Convex Configuration**

Create `convex.json`:
```json
{
  "node": "22.11.0",
  "generateCommonJSApi": false,
  "functions": "convex/"
}
```

Update root `tsconfig.json`:
```json
{
  "include": ["convex/**/*"],
  "compilerOptions": {
    "paths": {
      "convex/*": ["./convex/*"]
    }
  }
}
```

**Step 4.4: Create Convex Provider**

Create `apps/app/lib/convex-provider.tsx`:
```typescript
"use client";

import { ConvexProvider, ConvexReactClient } from "convex/react";
import { type ReactNode } from "react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({ children }: { children: ReactNode }) {
  return <ConvexProvider client={convex}>{children}</ConvexProvider>;
}
```

Update `apps/app/app/layout.tsx`:
```typescript
import { ConvexClientProvider } from "@/lib/convex-provider";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html>
      <body>
        <ConvexClientProvider>
          {children}
        </ConvexClientProvider>
      </body>
    </html>
  );
}
```

### Phase 4.5: React Email Templates

**Step 4.5.1: Install React Email**

```bash
cd packages/email
pnpm add @react-email/components react-email
```

**Step 4.5.2: Copy Email Templates**

```bash
# Copy welcome email template
cp [CURRENT_PROJECT_PATH]/packages/email/templates/welcome.tsx packages/email/templates/

# Copy document expiry alert template
cp [CURRENT_PROJECT_PATH]/packages/email/templates/document-expiry-alert.tsx packages/email/templates/

# Verify templates
ls packages/email/templates/
# Should show: welcome.tsx, document-expiry-alert.tsx
```

**Step 4.5.3: Configure React Email**

Create `packages/email/.react-email/config.js`:
```javascript
module.exports = {
  dir: './templates',
  port: 3002,
  open: false,
};
```

Update `packages/email/package.json`:
```json
{
  "scripts": {
    "dev": "react-email dev",
    "build": "react-email build",
    "export": "react-email export"
  }
}
```

### Phase 4.6: Storybook with Brand Guidelines

**Step 4.6.1: Install Storybook**

```bash
cd apps/app
pnpm add -D storybook @storybook/addon-essentials @storybook/addon-a11y @storybook/addon-themes @storybook/nextjs
bunx storybook@latest init --type nextjs --skip-install
```

**Step 4.6.2: Copy Storybook Configuration**

```bash
# Copy Storybook config and stories
cp -r [CURRENT_PROJECT_PATH]/apps/app/.storybook apps/app/
cp -r [CURRENT_PROJECT_PATH]/apps/app/stories apps/app/

# Verify copy
ls apps/app/.storybook/
ls apps/app/stories/Brand/
# Should show Colors.stories.tsx
```

**Step 4.6.3: Verify Storybook Theme**

Ensure `.storybook/preview.ts` contains FREO brand defaults:
- Default theme: "dark"
- Dark background: #0F172A (FREO primary)
- Story sort order: Brand → Components

### Phase 4.7: AI SDK 6 Integration

**Step 4.7.1: Install AI SDK 6**

```bash
# Root project
pnpm add ai @ai-sdk/anthropic @ai-sdk/openai @ai-sdk/google zod

# Apps
cd apps/app
pnpm add ai @ai-sdk/anthropic @ai-sdk/openai @ai-sdk/google zod

cd ../api
pnpm add ai @ai-sdk/anthropic @ai-sdk/openai @ai-sdk/google zod
```

**Step 4.7.2: Copy AI Tools and Gateway Config**

```bash
# Copy AI tools directory (24 tools)
cp -r [CURRENT_PROJECT_PATH]/apps/app/lib/ai apps/app/lib/

# Verify 24 tools
cat apps/app/lib/ai/tools.ts | grep "export const" | wc -l
# Should show 24

# Verify gateway config
grep "aiModels" apps/app/lib/ai/gateway-config.ts
# Should show model configurations
```

**Step 4.7.3: AI Tool Categories**

Verify all 5 categories are present:
1. Document Processing (4 tools)
2. Compliance Assistant (4 tools)
3. Fleet Intelligence (4 tools)
4. Knowledge Assistant (4 tools)
5. Report Generation (4 tools)

### Phase 4.8: Documentation Generation

**Step 4.8.1: Copy User Documentation**

```bash
# Copy getting started guide
cp [CURRENT_PROJECT_PATH]/docs/getting-started.md docs/

# Copy API reference
cp [CURRENT_PROJECT_PATH]/docs/api-reference.md docs/

# Verify documentation
ls docs/
# Should show: FREO_KNOWLEDGE_BASE.md, getting-started.md, api-reference.md
```

**Step 4.8.2: Verify Documentation Contents**

```bash
# Check getting started has all sections
grep -E "^##" docs/getting-started.md
# Should show: Quick Start, Core Concepts, Key Features, etc.

# Check API reference has all endpoints
grep -E "^###" docs/api-reference.md
# Should show: Documents, Cranes, Jobs, Compliance, AI Assistant, Webhooks
```

### Phase 5: Migrate Application Code

**Step 5.1: Copy Core Application Files**

```bash
# Copy application pages
cp -r [CURRENT_PROJECT_PATH]/app/* apps/app/app/

# Copy components
cp -r [CURRENT_PROJECT_PATH]/components/* packages/design-system/components/

# Copy lib utilities
cp -r [CURRENT_PROJECT_PATH]/lib/* apps/app/lib/

# Copy hooks
cp -r [CURRENT_PROJECT_PATH]/hooks/* apps/app/hooks/
```

**Step 5.2: Update Import Paths**

```bash
# Update Convex import paths (remove @/ prefix for monorepo)
find apps/app -type f \( -name "*.ts" -o -name "*.tsx" \) \
  -exec sed -i '' 's|@/convex/_generated/api|convex/_generated/api|g' {} +

# Update component imports for design-system
find apps/app -type f \( -name "*.ts" -o -name "*.tsx" \) \
  -exec sed -i '' 's|@/components/ui|@repo/design-system/components|g' {} +
```

**Step 5.3: Verify Imports**

```bash
# Check for broken imports
pnpm turbo typecheck

# Fix any remaining import errors manually
# Common patterns:
# - @/convex → convex
# - @/components → @repo/design-system/components
# - @/lib → ../lib or @/lib (depending on app structure)
```

### Phase 6: Programmatic Vercel Setup

**Step 6.1: Initialize Vercel Project**

```bash
# Create Vercel project programmatically
vercel --yes --force

# Link to existing project (if needed)
vercel link
```

**Step 6.2: Configure Vercel via API**

Use Vercel API to configure project settings:

```bash
# Get Vercel token
VERCEL_TOKEN=$(vercel whoami --token)

# Get project ID
PROJECT_ID=$(vercel inspect --token "$VERCEL_TOKEN" | grep "Project ID" | awk '{print $3}')

# Configure build settings via API
curl -X PATCH "https://api.vercel.com/v9/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "buildCommand": "pnpm turbo build",
    "framework": "nextjs",
    "installCommand": "pnpm install"
  }'
```

**Step 6.3: Vercel Marketplace Integration**

Programmatically add integrations via Vercel API:

```bash
# Add Convex integration
curl -X POST "https://api.vercel.com/v1/integrations" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "convex",
    "projectId": "'"$PROJECT_ID"'"
  }'

# Add Sentry integration
curl -X POST "https://api.vercel.com/v1/integrations" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "sentry",
    "projectId": "'"$PROJECT_ID"'"
  }'

# Add Clerk integration
curl -X POST "https://api.vercel.com/v1/integrations" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "clerk",
    "projectId": "'"$PROJECT_ID"'"
  }'
```

**Step 6.4: Set Environment Variables via Doppler**

```bash
# Export secrets from current Doppler project
cd [CURRENT_PROJECT_PATH]
doppler secrets download --config prd --format env > /tmp/secrets.env

# Import to new Doppler project
cd [NEW_PROJECT_PATH]
doppler setup
doppler secrets upload /tmp/secrets.env --config prd

# Sync to Vercel automatically
doppler secrets download --config prd --format vercel | vercel env add production

# Cleanup
rm /tmp/secrets.env
```

**Step 6.5: Configure Vercel Environment Variables**

Set additional Vercel-specific variables:

```bash
# Set Convex URL
vercel env add NEXT_PUBLIC_CONVEX_URL production <<< "[CONVEX_URL]"

# Set Clerk keys
vercel env add NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY production <<< "[CLERK_KEY]"
vercel env add CLERK_SECRET_KEY production <<< "[CLERK_SECRET]"

# Verify environment variables
vercel env ls
```

### Phase 7: Automated Testing

**Step 7.1: Copy E2E Tests**

```bash
# Copy Playwright tests
cp -r [CURRENT_PROJECT_PATH]/e2e ./
cp [CURRENT_PROJECT_PATH]/playwright.config.ts ./

# Install Playwright
pnpm add -D @playwright/test
bunx playwright install
```

**Step 7.2: Update Playwright Configuration**

Update `playwright.config.ts` for monorepo:
```typescript
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  webServer: {
    command: "pnpm dev",
    port: 3000,
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
  projects: [
    { name: "chromium", use: { browserName: "chromium" } },
  ],
});
```

**Step 7.3: Run Local Tests**

```bash
# Start development server
pnpm dev &
DEV_PID=$!

# Wait for server to be ready
sleep 30

# Run E2E tests
pnpm test:e2e

# Stop development server
kill $DEV_PID
```

**Step 7.4: Deploy to Preview and Test**

```bash
# Deploy to preview
PREVIEW_URL=$(vercel --yes | grep "https://" | tail -1)

# Run tests against preview
PLAYWRIGHT_TEST_BASE_URL="$PREVIEW_URL" pnpm test:e2e
```

### Phase 8: Browser-Based Validation

**Step 8.1: Use Browser Tools for Manual Verification**

Use the `mcp__plugin_superpowers-chrome_chrome__use_browser` tool to verify deployment:

```javascript
// Navigate to preview deployment
use_browser({
  action: "navigate",
  payload: "[PREVIEW_URL]"
});

// Take screenshot of homepage
use_browser({
  action: "screenshot",
  payload: "/tmp/homepage-preview.png"
});

// Verify authentication flow
use_browser({
  action: "click",
  selector: "//button[contains(text(), 'Sign In')]"
});

// Wait for Clerk sign-in modal
use_browser({
  action: "await_element",
  selector: "//div[@data-clerk-modal]",
  timeout: 5000
});

// Take screenshot of sign-in
use_browser({
  action: "screenshot",
  payload: "/tmp/signin-preview.png"
});
```

**Step 8.2: Automated Browser Checks**

Create browser check script:

```typescript
// e2e/browser-validation.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Browser Validation", () => {
  test("homepage loads successfully", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveTitle(/FREO Cranes/i);
  });

  test("Clerk authentication loads", async ({ page }) => {
    await page.goto("/");
    const clerkLoaded = await page.evaluate(() => {
      return typeof (window as any).Clerk !== "undefined";
    });
    expect(clerkLoaded).toBe(true);
  });

  test("Convex connection works", async ({ page }) => {
    await page.goto("/");
    await page.waitForTimeout(2000);

    const errors: string[] = [];
    page.on("console", (msg) => {
      if (msg.type() === "error") errors.push(msg.text());
    });

    const convexErrors = errors.filter(e => e.includes("Convex"));
    expect(convexErrors).toHaveLength(0);
  });
});
```

Run browser validation:
```bash
pnpm test:e2e e2e/browser-validation.spec.ts
```

### Phase 9: Production Deployment

**Step 9.1: Deploy to Production**

```bash
# Deploy using Doppler secrets
doppler run --config prd -- vercel --prod --yes
```

**Step 9.2: Switch Domain**

Use Vercel API to update domain:

```bash
# Get Vercel token and project IDs
VERCEL_TOKEN=$(vercel whoami --token)
OLD_PROJECT_ID="[OLD_PROJECT_ID]"
NEW_PROJECT_ID=$(vercel inspect --token "$VERCEL_TOKEN" | grep "Project ID" | awk '{print $3}')

# Remove domain from old project
curl -X DELETE "https://api.vercel.com/v9/projects/$OLD_PROJECT_ID/domains/freo.aliaslabs.ai" \
  -H "Authorization: Bearer $VERCEL_TOKEN"

# Add domain to new project
curl -X POST "https://api.vercel.com/v9/projects/$NEW_PROJECT_ID/domains" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "freo.aliaslabs.ai"
  }'

# Wait for DNS propagation
sleep 60

# Verify domain
curl -I https://freo.aliaslabs.ai
```

**Step 9.3: Production Smoke Tests**

Run E2E tests against production:

```bash
PLAYWRIGHT_TEST_BASE_URL="https://freo.aliaslabs.ai" pnpm test:e2e
```

**Step 9.4: Browser-Based Production Verification**

```javascript
// Verify production deployment
use_browser({
  action: "navigate",
  payload: "https://freo.aliaslabs.ai"
});

// Take screenshot
use_browser({
  action: "screenshot",
  payload: "/tmp/production-homepage.png"
});

// Extract page text
const pageContent = use_browser({
  action: "extract",
  selector: "//body",
  payload: "text"
});

// Verify no errors
const hasErrors = pageContent.includes("Application error") ||
                  pageContent.includes("500") ||
                  pageContent.includes("404");

if (hasErrors) {
  throw new Error("Production deployment has errors!");
}
```

### Phase 10: Post-Migration Validation

**Step 10.1: Monitoring Setup**

```bash
# Verify Sentry is receiving events
curl "https://sentry.io/api/0/projects/[ORG]/[PROJECT]/events/" \
  -H "Authorization: Bearer [SENTRY_TOKEN]"

# Check Vercel Analytics
vercel logs [DEPLOYMENT_URL]

# Monitor Convex Dashboard
open "https://dashboard.convex.dev"
```

**Step 10.2: Final Checklist**

Create final validation TodoWrite:

```javascript
TodoWrite({
  todos: [
    { content: "Verify production homepage loads", status: "pending", activeForm: "Checking homepage" },
    { content: "Test user authentication flow", status: "pending", activeForm: "Testing authentication" },
    { content: "Verify document upload works", status: "pending", activeForm: "Testing document upload" },
    { content: "Check Convex real-time updates", status: "pending", activeForm: "Checking real-time" },
    { content: "Verify search functionality", status: "pending", activeForm: "Testing search" },
    { content: "Test mobile responsiveness", status: "pending", activeForm: "Testing mobile" },
    { content: "Check error tracking (Sentry)", status: "pending", activeForm: "Verifying Sentry" },
    { content: "Verify analytics (Vercel)", status: "pending", activeForm: "Checking analytics" },
    { content: "Monitor performance metrics", status: "pending", activeForm: "Monitoring performance" },
    { content: "Document migration completion", status: "pending", activeForm: "Creating documentation" }
  ]
});
```

## Error Handling

### Common Issues and Solutions

**Issue 1: Convex Connection Failures**

```bash
# Verify Convex deployment
bunx convex env

# Re-deploy if needed
bunx convex deploy --prod

# Update environment variables
vercel env add NEXT_PUBLIC_CONVEX_URL production
```

**Issue 2: Clerk Authentication Not Working**

```bash
# Verify Clerk keys
echo $NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
echo $CLERK_SECRET_KEY

# Check Clerk dashboard domain configuration
open "https://dashboard.clerk.com"
```

**Issue 3: Build Failures**

```bash
# Clear Turbo cache
pnpm turbo clean

# Rebuild
pnpm turbo build --force

# Check build logs
vercel logs
```

**Issue 4: Missing Environment Variables**

```bash
# Re-sync from Doppler
doppler secrets download --config prd --format vercel | vercel env add production

# Redeploy
vercel --prod --yes
```

## Rollback Procedure

**If critical issues occur:**

### Quick Rollback (< 5 minutes)

```bash
# 1. Revert domain via Vercel API
VERCEL_TOKEN=$(vercel whoami --token)
OLD_PROJECT_ID="[OLD_PROJECT_ID]"
NEW_PROJECT_ID="[NEW_PROJECT_ID]"

# Remove from new project
curl -X DELETE "https://api.vercel.com/v9/projects/$NEW_PROJECT_ID/domains/freo.aliaslabs.ai" \
  -H "Authorization: Bearer $VERCEL_TOKEN"

# Add back to old project
curl -X POST "https://api.vercel.com/v9/projects/$OLD_PROJECT_ID/domains" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "freo.aliaslabs.ai"
  }'

# 2. Verify rollback
curl -I https://freo.aliaslabs.ai

# 3. Investigate issues
vercel logs [NEW_DEPLOYMENT_URL]
```

## Success Metrics

**Technical Validation:**
- [ ] All 3 apps build without errors
- [ ] Zero Prisma/PostgreSQL dependencies
- [ ] Convex backend fully operational
- [ ] All environment variables configured
- [ ] E2E tests passing (45+ tests)
- [ ] Production deployment successful

**Functional Validation:**
- [ ] User authentication works
- [ ] Document management works
- [ ] Search functionality works
- [ ] Real-time updates work
- [ ] Mobile responsive

**Performance Validation:**
- [ ] Homepage load time < 3 seconds
- [ ] Convex query latency < 50ms
- [ ] Lighthouse score > 90
- [ ] Zero memory leaks

## Notes

**Prerequisites Verification:**
Always verify prerequisites before starting migration:

```bash
# Check current project has Convex
test -f convex/schema.ts || echo "ERROR: No Convex schema found"

# Verify Doppler access
doppler secrets --config prd | wc -l
# Should show 40+ secrets

# Verify Vercel CLI
vercel whoami
# Should show username

# Check GitHub access
git remote -v
# Should show repository URL
```

**Automation Tips:**
- Use `set -e` in bash scripts to fail fast
- Always verify operations before proceeding
- Create backups before destructive operations
- Use TodoWrite to track progress
- Log all operations for debugging

**Best Practices:**
- Test locally before deploying
- Use preview deployments for validation
- Monitor error tracking (Sentry)
- Keep rollback procedure ready
- Document any custom changes

## Example Usage

```bash
# Full migration example
cd /Users/alias/Documents/GitHub

# Step 1: Clone Next Forge
git clone https://github.com/vercel/next-forge.git freo-cranes-staging
cd freo-cranes-staging

# Step 2: Run automated migration
# (Use this skill to guide the process)

# Step 3: Verify locally
pnpm dev

# Step 4: Deploy to Vercel
doppler run --config prd -- vercel --prod --yes

# Step 5: Browser validation
# (Use browser tools as shown above)

# Step 6: Switch domain
# (Use Vercel API as shown above)
```

## Related Skills

- **vercel-auto-deploy**: For standard Vercel deployments
- **superpowers-chrome:browsing**: For browser-based testing
- **test-driven-development**: For writing tests during migration

## Version History

- **v1.0.0** (2025-11-20): Initial skill creation with full automation
