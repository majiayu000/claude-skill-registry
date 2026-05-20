---
name: Nuxt Studio
description: This skill should be used when the user asks to "set up Nuxt Studio", "configure Studio OAuth", "deploy Studio to Cloudflare", "add visual editor to Nuxt", "configure studio.domain.com subdomain", "Studio authentication", "Nuxt CMS", or mentions visual content editing, Nuxt Studio module, TipTap editor, Monaco editor, or content management for Nuxt websites.
version: 1.0.0
license: MIT
---

# Nuxt Studio Setup and Deployment

## Overview

Nuxt Studio is a free, open-source visual content editor for Nuxt Content websites that enables content editing directly in production. It provides multiple editor types (Monaco code editor, TipTap visual WYSIWYG editor, Form-based editor), OAuth authentication (GitHub/GitLab/Google), and Git-based content management with commit integration.

**Primary use case**: Add visual CMS capabilities to existing Nuxt Content websites, typically deployed to a subdomain like `studio.domain.com` or `cms.domain.com`.

## When to Use This Skill

Use this skill when users need to:
- Set up Nuxt Studio for the first time on a Nuxt Content website
- Configure OAuth authentication for Studio access
- Deploy Studio to Cloudflare Pages or Workers with custom subdomain
- Troubleshoot Studio authentication, build, or deployment issues
- Configure editor types or customize Studio behavior
- Integrate Studio with existing Nuxt v3/v4 applications

## Prerequisites Check

Before proceeding with Studio setup, verify these requirements:

1. **Nuxt Version**: ≥3.x (Studio requires Nuxt 3)
2. **@nuxt/content Module**: ≥2.x (required dependency)
3. **Node.js**: ≥18.x recommended
4. **Cloudflare Account**: Required for Cloudflare deployment (optional for other platforms)

**Check Nuxt Content installation**:
```bash
# Verify @nuxt/content is installed
grep "@nuxt/content" package.json

# Check nuxt.config.ts for content module
grep "modules.*content" nuxt.config.ts
```

If Nuxt Content is not installed, install it first:
```bash
npx nuxi module add content
```

## Installation

### 1. Install Nuxt Studio Module

Install the latest beta version (v1.0.0-beta.3 as of December 2025):

```bash
npx nuxi module add nuxt-studio@beta
```

This adds `@nuxt/studio` to `devDependencies` and configures the module in `nuxt.config.ts`.

### 2. Verify Module Configuration

Check that `nuxt.config.ts` includes the Studio module:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: [
    '@nuxt/content',
    '@nuxt/studio'  // Added automatically
  ]
})
```

### 3. Start Development Mode

Run the development server to test Studio locally:

```bash
npm run dev
# or
bun dev
```

Access Studio at `http://localhost:3000/_studio` (development mode).

## OAuth Authentication Setup

Studio requires OAuth authentication for production deployments. Choose one provider:

### Supported Providers

- **GitHub OAuth**: Best for public repositories and GitHub-hosted projects
- **GitLab OAuth**: Ideal for self-hosted GitLab instances
- **Google OAuth**: Universal option for any setup

### Quick OAuth Configuration

For detailed OAuth setup instructions for each provider, load **`references/oauth-providers.md`**.

**Environment variables pattern** (all providers):
```bash
# GitHub
NUXT_OAUTH_GITHUB_CLIENT_ID=your_client_id
NUXT_OAUTH_GITHUB_CLIENT_SECRET=your_client_secret

# GitLab
NUXT_OAUTH_GITLAB_CLIENT_ID=your_client_id
NUXT_OAUTH_GITLAB_CLIENT_SECRET=your_client_secret

# Google
NUXT_OAUTH_GOOGLE_CLIENT_ID=your_client_id
NUXT_OAUTH_GOOGLE_CLIENT_SECRET=your_client_secret
```

**Callback URL pattern**:
```
https://studio.yourdomain.com/api/auth/callback/[provider]
```

Replace `[provider]` with: `github`, `gitlab`, or `google`.

For complete OAuth app creation steps, consult **`references/oauth-providers.md`**.

## Cloudflare Deployment

Studio works excellently on Cloudflare Pages and Workers. Use the Cloudflare deployment for:
- Serverless edge deployment
- Custom subdomain routing (e.g., `studio.domain.com`)
- Environment variable management via dashboard
- Automatic builds from Git

### Cloudflare Setup Overview

1. **Configure Nitro preset** for Cloudflare in `nuxt.config.ts`
2. **Create or update `wrangler.toml`** for Workers deployment (optional)
3. **Set environment variables** on Cloudflare dashboard
4. **Configure custom domain** and subdomain routing
5. **Deploy** via Cloudflare Pages or Workers

For complete Cloudflare deployment instructions, load **`references/cloudflare-deployment.md`**.

### Quick Cloudflare Configuration

Set the Cloudflare Pages preset:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxt/content', '@nuxt/studio'],

  nitro: {
    preset: 'cloudflare-pages'
  }
})
```

For Workers deployment with custom subdomain routing, see **`references/cloudflare-deployment.md`**.

## Editor Types

Studio provides three editor types that can be configured per content type:

1. **Monaco Editor**: Code editor for markdown, YAML, JSON
2. **TipTap Editor**: Visual WYSIWYG editor with MDC component support (default)
3. **Form Editor**: Schema-driven form for YAML/JSON files

### Configure Default Editor

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  studio: {
    editor: {
      default: 'tiptap'  // or 'monaco' or 'form'
    }
  }
})
```

For detailed editor configuration options, load **`references/editor-configuration.md`**.

## Subdomain Configuration

Deploy Studio to a subdomain for production use:

**Common patterns**:
- `studio.yourdomain.com`
- `cms.yourdomain.com`
- `edit.yourdomain.com`
- `admin.yourdomain.com`

### DNS Setup

1. Add a CNAME record in your DNS provider
2. Point subdomain to Cloudflare Pages deployment
3. Configure custom domain in Cloudflare Pages settings

For complete subdomain setup with Cloudflare, load **`references/subdomain-setup.md`**.

## Top 5 Common Errors

### 1. OAuth Redirect URI Mismatch

**Error**: Authentication loop or "redirect_uri_mismatch" error

**Cause**: OAuth app callback URL doesn't match actual deployment URL

**Solution**:
```
Ensure OAuth app callback URL is:
https://studio.yourdomain.com/api/auth/callback/[provider]

Not:
https://yourdomain.com/api/auth/callback/[provider]
```

### 2. Module Not Found: @nuxt/studio

**Error**: `Cannot find module '@nuxt/studio'`

**Cause**: Studio module not installed or installed incorrectly

**Solution**:
```bash
npx nuxi module add nuxt-studio@beta
# or
npm install -D @nuxt/studio
```

### 3. Cloudflare Pages Build Failure

**Error**: Build fails with "Incompatible module" or runtime errors

**Cause**: Nitro preset not configured for Cloudflare

**Solution**:
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  nitro: {
    preset: 'cloudflare-pages'
  }
})
```

### 4. Authentication Loop After Login

**Error**: Redirects to login repeatedly after successful OAuth

**Cause**: Session cookies not persisting due to domain mismatch

**Solution**:
- Verify `NUXT_PUBLIC_STUDIO_URL` environment variable matches deployment URL
- Check cookie settings in browser (must allow third-party cookies for OAuth)
- Ensure deployment URL uses HTTPS (not HTTP)

### 5. Subdomain Routing Not Working

**Error**: Studio loads on main domain instead of subdomain

**Cause**: DNS/wrangler configuration incorrect

**Solution**:
- Verify CNAME record points to Cloudflare Pages
- Check custom domain configuration in Cloudflare dashboard
- For Workers: verify `wrangler.toml` routes configuration

For complete error catalog and solutions, load **`references/troubleshooting.md`**.

## Working with Templates

The skill includes working configuration templates:

- **`templates/nuxt.config.ts`**: Complete Studio module configuration
- **`templates/wrangler.toml`**: Cloudflare Workers deployment config
- **`templates/studio-auth-github.ts`**: GitHub OAuth implementation
- **`templates/studio-auth-gitlab.ts`**: GitLab OAuth implementation
- **`templates/studio-auth-google.ts`**: Google OAuth implementation

Use these as starting points for your Studio setup.

## Development Workflow

### Local Development

1. Install Studio module: `npx nuxi module add nuxt-studio@beta`
2. Start dev server: `npm run dev`
3. Access Studio: `http://localhost:3000/_studio`
4. Edit content visually
5. Commit changes from Studio UI

### Production Deployment

1. Configure OAuth provider (GitHub/GitLab/Google)
2. Set environment variables on deployment platform
3. Configure Nitro preset for target platform
4. Deploy to Cloudflare Pages/Workers or other platform
5. Set up custom subdomain
6. Test authentication and content editing

## Validation Checklist

Before deploying Studio to production:

- [ ] Nuxt Content installed and configured (≥v2.x)
- [ ] Nuxt version ≥3.x
- [ ] @nuxt/studio module installed
- [ ] OAuth provider configured with valid credentials
- [ ] Environment variables set correctly
- [ ] Nitro preset configured for deployment platform
- [ ] Custom subdomain DNS configured
- [ ] Callback URLs match deployment URL
- [ ] Studio accessible at subdomain URL
- [ ] Authentication working correctly
- [ ] Content editing and commit functionality tested

## When to Load References

Load reference files when working on specific aspects:

- **OAuth setup**: Load `references/oauth-providers.md` for detailed GitHub/GitLab/Google OAuth app creation
- **Cloudflare deployment**: Load `references/cloudflare-deployment.md` for complete Cloudflare Pages/Workers setup with wrangler, custom domains, and environment variables
- **Editor configuration**: Load `references/editor-configuration.md` for Monaco/TipTap/Form editor customization
- **Subdomain setup**: Load `references/subdomain-setup.md` for DNS and routing configuration
- **Troubleshooting**: Load `references/troubleshooting.md` for comprehensive error solutions and debugging

## Utility Scripts

Use the included scripts for common operations:

- **`scripts/check-prerequisites.sh`**: Verify Nuxt Content and version requirements
- **`scripts/validate-config.sh`**: Check nuxt.config.ts Studio configuration
- **`scripts/test-oauth.sh`**: Test OAuth environment variables setup

Run scripts with:
```bash
bash $CLAUDE_PLUGIN_ROOT/skills/nuxt-studio/scripts/script-name.sh
```

## Integration with Other Skills

This skill works well with:

- **nuxt-content**: Prerequisites for Studio (content module required)
- **nuxt-v4**: Core Nuxt framework knowledge for configuration
- **cloudflare-worker-base**: Cloudflare deployment fundamentals
- **better-auth**: Alternative authentication patterns if custom auth needed

## Additional Resources

- **Nuxt Studio Repository**: https://github.com/nuxt-content/studio
- **Nuxt Content Documentation**: https://content.nuxt.com
- **Cloudflare Pages**: https://pages.cloudflare.com
- **OAuth Documentation**: GitHub/GitLab/Google developer docs

## Version Information

- **Nuxt Studio**: v1.0.0-beta.3 (latest as of December 2025)
- **Nuxt**: ≥3.x required
- **@nuxt/content**: ≥2.x required
- **Node.js**: ≥18.x recommended

For the latest version information, check: https://github.com/nuxt-content/studio/releases

---

**Next steps**: After Studio is configured, test the deployment thoroughly, ensure OAuth authentication works correctly, and verify that content editing and Git commits function as expected.
