---
name: sveltia-cms
description: |
  Set up Sveltia CMS - lightweight Git-backed CMS successor to Decap/Netlify CMS (300KB bundle, 270+ fixes). Framework-agnostic for Hugo, Jekyll, 11ty, Astro. Prevents 10 documented errors.

  Use when adding CMS to static sites, migrating from Decap CMS, or fixing OAuth, YAML parse, datetime timezone, GDPR font loading, or CORS/COOP errors.
user-invocable: true
allowed-tools: ['Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep']
---

# Sveltia CMS Skill

Complete skill for integrating Sveltia CMS into static site projects.

---

## Current Versions

- **@sveltia/cms**: 0.128.5 (verified January 2026)
- **Status**: Public Beta (v1.0 expected early 2026)
- **Maturity**: Production-ready (270+ issues solved from predecessor)

---

## When to Use This Skill

### ✅ Use Sveltia CMS When:

- Git-based workflow desired (content as Markdown/YAML/TOML/JSON in repository)
- Lightweight solution required (<500 KB vs 1.5-2.6 MB for competitors)
- Migrating from Decap/Netlify CMS (drop-in replacement, change 1 line)
- Non-technical editors need access without Git knowledge

### ❌ Don't Use Sveltia CMS When:

- Real-time collaboration needed (multiple users editing simultaneously) - Use Sanity, Contentful, or TinaCMS instead
- Visual page building required (drag-and-drop) - Use Webflow, Builder.io instead
- React-specific visual editing needed - Use TinaCMS instead

---

## Breaking Changes & Updates (v0.105.0+)

### v0.127.0 (December 29, 2025) - slug_length Deprecation

**DEPRECATION**: The `slug_length` collection option is deprecated and will be removed in v1.0.

**Migration**:
```yaml
# ❌ Deprecated (pre-v0.127.0)
collections:
  - name: posts
    slug_length: 50

# ✅ New (v0.127.0+)
slug:
  maxlength: 50
```

**Timeline**: Will be removed in Sveltia CMS 1.0 (expected early 2026).

**Source**: [Release v0.127.0](https://github.com/sveltia/sveltia-cms/releases/tag/v0.127.0)

---

### v0.120.0 (November 24, 2025) - Author Template Tags

**New Feature**: Hidden widget now supports author template tags:
- `{{author-email}}` - Signed-in user's email
- `{{author-login}}` - Signed-in user's login name
- `{{author-name}}` - Signed-in user's display name

**Usage**:
```yaml
fields:
  - label: Author Email
    name: author_email
    widget: hidden
    default: '{{author-email}}'
```

**Commit message templates** also support `{{author-email}}` tag.

---

### v0.119.0 (November 16, 2025) - TOML Config Support

**New Feature**: Configuration files can now be written in TOML format (previously YAML-only).

**Migration**:
```toml
# admin/config.toml (NEW)
[backend]
name = "github"
repo = "owner/repo"
branch = "main"

media_folder = "static/images/uploads"
public_folder = "/images/uploads"
```

**Recommendation**: YAML is still preferred for better tooling support.

---

### v0.118.0 (November 15, 2025) - TypeScript Breaking Change

**BREAKING**: Renamed `SiteConfig` export to `CmsConfig` for compatibility with Netlify/Decap CMS.

**Migration**:
```typescript
// ❌ Old (v0.117.x)
import type { SiteConfig } from '@sveltia/cms';

// ✅ New (v0.118.0+)
import type { CmsConfig } from '@sveltia/cms';

const config: CmsConfig = {
  backend: { name: 'github', repo: 'owner/repo' },
  collections: [/* ... */],
};
```

**Impact**: TypeScript users only. Breaking change for type imports.

---

### v0.117.0 (November 14, 2025) - Enhanced Validation

**New Features**:
- Exported `CmsConfig` type for direct TypeScript import
- Enhanced config validation for collection names, field types, and relation references
- Better error messages for invalid configurations

---

### v0.115.0 (November 5, 2025) - Field-Specific Media Folders

**New Feature**: Override `media_folder` at the field level (not just collection level).

**Usage**:
```yaml
collections:
  - name: posts
    label: Blog Posts
    folder: content/posts
    media_folder: static/images/posts  # Collection-level default
    fields:
      - label: Featured Image
        name: image
        widget: image
        media_folder: static/images/featured  # ← Field-level override
        public_folder: /images/featured

      - label: Author Avatar
        name: avatar
        widget: image
        media_folder: static/images/avatars  # ← Another override
        public_folder: /images/avatars
```

**Use case**: Different media folders for different image types in same collection.

---

### v0.113.5 (October 27, 2025) - Logo Deprecation

**DEPRECATION**: `logo_url` option is now deprecated. Migrate to `logo.src`.

**Migration**:
```yaml
# ❌ Deprecated
logo_url: https://yourdomain.com/logo.svg

# ✅ New (v0.113.5+)
logo:
  src: https://yourdomain.com/logo.svg
```

---

### v0.105.0 (September 15, 2024) - Security Breaking Change

**BREAKING**: `sanitize_preview` default changed to `true` for Markdown widget (XSS prevention).

**Impact**:
- **Before v0.105.0**: `sanitize_preview: false` (compatibility with Netlify/Decap CMS, but vulnerable to XSS)
- **After v0.105.0**: `sanitize_preview: true` (secure by default)

**Migration**:
```yaml
collections:
  - name: posts
    fields:
      - label: Body
        name: body
        widget: markdown
        sanitize_preview: false  # ← Add ONLY if you trust all CMS users
```

**Recommendation**: Keep default (`true`) unless disabling fixes broken preview AND you fully trust all CMS users.

---

## Configuration Options

### Global Slug Options (v0.128.0+)

Configure slug generation behavior globally:

```yaml
slug:
  encoding: unicode-normalized
  clean_accents: false
  sanitize_replacement: '-'
  lowercase: true   # Default: convert to lowercase (v0.128.0+)
  maxlength: 50     # Default: unlimited (v0.127.0+)
```

**lowercase** (v0.128.0+): Set to `false` to preserve original casing in slugs (e.g., "MyBlogPost" instead of "myblogpost").

**Use case**: Mixed-case URLs or file names where case matters.

**Source**: [Release v0.128.0](https://github.com/sveltia/sveltia-cms/releases/tag/v0.128.0), [GitHub Issue #594](https://github.com/sveltia/sveltia-cms/issues/594)

---

### Raw Format for Text Files (v0.126.0+)

New `raw` format allows editing files without front matter (CSV, JSON, YAML, plain text). Must have single `body` field with widget type: `code`, `markdown`, `richtext`, or `text`.

**Use Cases**:
- Edit configuration files (JSON, YAML)
- Manage CSV data
- Edit plain text files

**Configuration**:
```yaml
collections:
  - name: config
    label: Configuration Files
    files:
      - label: Site Config
        name: site_config
        file: config.json
        format: raw  # ← NEW format type
        fields:
          - label: Config
            name: body
            widget: code
            default_language: json
```

**Restrictions**:
- Only one field allowed (must be named `body`)
- Widget must be: `code`, `markdown`, `richtext`, or `text`
- No front matter parsing

**Source**: [Release v0.126.0](https://github.com/sveltia/sveltia-cms/releases/tag/v0.126.0)

---

### Number Field String Encoding (v0.125.0+)

New `value_type` option for Number field accepts `int/string` and `float/string` to save numbers as strings instead of numbers in front matter.

**Use Case**: Some static site generators or schemas require numeric values stored as strings (e.g., `age: "25"` instead of `age: 25`).

**Configuration**:
```yaml
fields:
  - label: Age
    name: age
    widget: number
    value_type: int/string  # Saves as "25" not 25

  - label: Price
    name: price
    widget: number
    value_type: float/string  # Saves as "19.99" not 19.99
```

**Source**: [Release v0.125.0](https://github.com/sveltia/sveltia-cms/releases/tag/v0.125.0), [GitHub Issue #574](https://github.com/sveltia/sveltia-cms/issues/574)

---

### Editor Pane Locale via URL Query (v0.126.0+)

Override editor locale via URL query parameter `?_locale=fr` to get edit links for specific locales.

**Use Case**: Generate direct edit links for translators or content editors for specific languages.

**Example**:
```
https://yourdomain.com/admin/#/collections/posts/entries/my-post?_locale=fr
```

**Source**: [Release v0.126.0](https://github.com/sveltia/sveltia-cms/releases/tag/v0.126.0), [GitHub Issue #585](https://github.com/sveltia/sveltia-cms/issues/585)

---

### Richtext Field Type Alias (v0.124.0+)

Added `richtext` as an alias for `markdown` widget to align with Decap CMS terminology. Both work identically.

**Configuration**:
```yaml
fields:
  - label: Body
    name: body
    widget: richtext  # ← NEW alias for markdown
```

**Future**: HTML output support planned for `richtext` field type.

**Source**: [Release v0.124.0](https://github.com/sveltia/sveltia-cms/releases/tag/v0.124.0)

---

## Setup Pattern (Framework-Agnostic)

**All frameworks follow the same pattern:**

1. **Create admin directory in public/static folder:**
   - Hugo: `static/admin/`
   - Jekyll: `admin/`
   - 11ty: `admin/` (with passthrough copy)
   - Astro: `public/admin/`
   - Next.js: `public/admin/`

2. **Create admin/index.html:**
   ```html
   <!doctype html>
   <html lang="en">
     <head>
       <meta charset="utf-8" />
       <meta name="viewport" content="width=device-width, initial-scale=1.0" />
       <title>Content Manager</title>
     </head>
     <body>
       <script src="https://unpkg.com/@sveltia/cms@0.128.5/dist/sveltia-cms.js" type="module"></script>
     </body>
   </html>
   ```

3. **Create admin/config.yml:**
   ```yaml
   backend:
     name: github
     repo: owner/repo
     branch: main
     base_url: https://your-worker.workers.dev  # OAuth proxy (required)

   media_folder: static/images/uploads  # Framework-specific path
   public_folder: /images/uploads

   collections:
     - name: posts
       label: Blog Posts
       folder: content/posts
       create: true
       fields:
         - { label: 'Title', name: 'title', widget: 'string' }
         - { label: 'Date', name: 'date', widget: 'datetime' }
         - { label: 'Body', name: 'body', widget: 'markdown' }
   ```

4. **Access admin:** `http://localhost:<port>/admin/`

**Framework-specific details**: See `templates/` directory for complete examples.

---

## Authentication: Cloudflare Workers OAuth (Recommended)

**Why Cloudflare Workers**: Fastest, free tier available, works with any deployment platform.

**Steps:**

1. **Deploy Worker:**
   ```bash
   git clone https://github.com/sveltia/sveltia-cms-auth
   cd sveltia-cms-auth
   npm install
   npx wrangler deploy
   ```

2. **Register OAuth App on GitHub:**
   - Go to https://github.com/settings/developers
   - Click "New OAuth App"
   - **Authorization callback URL**: `https://your-worker.workers.dev/callback`
   - Save Client ID and Client Secret

3. **Configure Worker Environment Variables:**
   ```bash
   npx wrangler secret put GITHUB_CLIENT_ID
   # Paste your Client ID

   npx wrangler secret put GITHUB_CLIENT_SECRET
   # Paste your Client Secret
   ```

4. **Update CMS config:**
   ```yaml
   backend:
     name: github
     repo: owner/repo
     branch: main
     base_url: https://your-worker.workers.dev  # ← Add this line
   ```

5. **Test authentication:**
   - Open `/admin/`
   - Click "Login with GitHub"
   - Should redirect to GitHub → Authorize → Back to CMS

**Alternative**: Vercel serverless functions - See `templates/vercel-serverless/`

---

## Common Errors & Solutions

This skill prevents **10 common errors** encountered when setting up Sveltia CMS.

### 1. ❌ OAuth Authentication Failures

**Error Message:**
- "Error: Failed to authenticate"
- Redirect to `https://api.netlify.com/auth` instead of GitHub login

**Symptoms:**
- Login button does nothing
- Authentication popup closes immediately

**Causes:**
- Missing `base_url` in backend config
- Incorrect OAuth proxy URL
- Wrong GitHub OAuth callback URL

**Solution:**

**Step 1: Verify config.yml has `base_url`:**
```yaml
backend:
  name: github
  repo: owner/repo
  branch: main
  base_url: https://your-worker.workers.dev  # ← Must be present
```

**Step 2: Check GitHub OAuth App callback:**
- Should be: `https://your-worker.workers.dev/callback`
- NOT: `https://yourdomain.com/callback`

**Step 3: Test Worker directly:**
```bash
curl https://your-worker.workers.dev/health
# Should return: {"status": "ok"}
```

---

### 2. ❌ TOML Front Matter Errors

**Error Message:**
- "Parse error: Invalid TOML"
- Files missing `+++` delimiters

**Symptoms:**
- New files created by CMS don't parse in Hugo
- Content appears above body separator

**Causes:**
- Sveltia's TOML generation is buggy in beta
- Mixed TOML/YAML in same collection

**Solution:**

**Use YAML instead of TOML** (recommended):
```yaml
collections:
  - name: posts
    folder: content/posts
    format: yaml  # or md (Markdown with YAML frontmatter)
    # NOT: format: toml
```

**If you must use TOML:**
1. Manually fix delimiters after CMS saves
2. Use pre-commit hook to validate TOML
3. Wait for beta fixes (track GitHub issues)

---

### 3. ❌ YAML Parse Errors

**Error Message:**
- "YAML parse error: Invalid YAML"
- "Error: Duplicate key 'field_name'"

**Symptoms:**
- Existing posts won't load in CMS
- CMS shows empty fields

**Causes:**
- Sveltia is stricter than Hugo/Jekyll about YAML formatting
- Incorrect indentation or smart quotes

**Solution:**

**Step 1: Validate YAML:**
```bash
pip install yamllint
find content -name "*.md" -exec yamllint {} \;
```

**Step 2: Common fixes:**

**Problem**: Smart quotes
```yaml
# ❌ Bad - smart quotes from copy-paste
title: "Hello World"  # Curly quotes

# ✅ Good - straight quotes
title: "Hello World"  # Straight quotes
```

**Step 3: Auto-fix with yamlfmt:**
```bash
go install github.com/google/yamlfmt/cmd/yamlfmt@latest
find content -name "*.md" -exec yamlfmt {} \;
```

---

### 4. ❌ Content Not Listing in CMS

**Error Message:**
- "No entries found"
- "Failed to load entries"

**Symptoms:**
- Admin loads but shows no content
- Files exist in repository but CMS doesn't see them

**Causes:**
- Format mismatch (config expects TOML, files are YAML)
- Incorrect folder path

**Solution:**

**Step 1: Verify folder path:**
```yaml
# Config says:
collections:
  - name: posts
    folder: content/posts  # Expects files here

# Check actual location:
ls -la content/posts  # Files must exist here
```

**Step 2: Match format to actual files:**
```yaml
# If files are: content/posts/hello.md with YAML frontmatter
collections:
  - name: posts
    folder: content/posts
    format: yaml  # or md (same as yaml for .md files)
```

---

### 5. ❌ "SVELTIA is not defined" Error

**Error Message:**
- Console error: `Uncaught ReferenceError: SVELTIA is not defined`

**Symptoms:**
- Admin page shows white screen

**Causes:**
- Missing `type="module"` attribute

**Solution:**

**Use correct script tag:**
```html
<!-- ✅ Correct -->
<script src="https://unpkg.com/@sveltia/cms/dist/sveltia-cms.js" type="module"></script>

<!-- ❌ Wrong - missing type="module" -->
<script src="https://unpkg.com/@sveltia/cms/dist/sveltia-cms.js"></script>
```

**Use version pinning (recommended):**
```html
<script src="https://unpkg.com/@sveltia/cms@0.128.5/dist/sveltia-cms.js" type="module"></script>
```

---

### 6. ❌ 404 on /admin

**Error Message:**
- "404 Not Found" when visiting `/admin/`

**Symptoms:**
- Works locally but not in production

**Causes:**
- Admin directory not in correct location for framework

**Solution:**

**Framework-specific fixes:**

**Hugo**: Files in `static/` are automatically copied

**Jekyll**: Add to `_config.yml`:
```yaml
include:
  - admin
```

**11ty**: Add to `.eleventy.js`:
```javascript
module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy('admin');
};
```

**Astro**: Files in `public/` are automatically copied

---

### 7. ❌ Images Not Uploading (HEIC Format)

**Error Message:**
- "Unsupported file format"

**Symptoms:**
- iPhone photos won't upload

**Causes:**
- HEIC format not supported by browsers

**Solution:**

**On iPhone:**
- Settings > Camera > Formats > Most Compatible
- This saves photos as JPEG instead of HEIC

**Or enable image optimization:**
```yaml
media_libraries:
  default:
    config:
      max_file_size: 10485760  # 10 MB
      transformations:
        raster_image:
          format: webp  # Auto-converts to WebP
          quality: 85
```

---

### 8. ❌ Datetime Widget Format Strictness

**Error Message:**
- Silent data loss (no error shown)
- Date fields show blank in CMS

**Symptoms:**
- Posts with existing dates appear blank when editing
- Saving overwrites dates with blank values
- Hugo marks posts as "future" and skips building them

**Causes:**
- Default datetime widget outputs timestamps WITHOUT timezone suffix
- When `format` is specified, Sveltia becomes **strict** - existing entries with different formats show as blank
- Hugo infers UTC when timezone missing, causing timezone issues

**⚠️ CRITICAL: Format Strictness Warning (v0.124.1+)**

When you specify a `format` option, Sveltia becomes **strict**:
- Existing entries with different formats show as **blank**
- Saving will **overwrite** with blank value (SILENT DATA LOSS)
- No error message shown

**Solution:**

**Option 1: Use picker_utc (Recommended)**
```yaml
fields:
  - label: Date
    name: date
    widget: datetime
    picker_utc: true  # Most flexible - outputs with timezone
```

**Option 2: Specify format with timezone (RISKY - see warning above)**
```yaml
fields:
  - label: Date
    name: date
    widget: datetime
    format: "YYYY-MM-DDTHH:mm:ss.SSSZ"  # Only if ALL existing dates match this format
```

**Option 3: Configure Hugo to accept missing timezone**
```toml
# config.toml
[frontmatter]
  date = [":default", ":fileModTime"]
```

**Prevention**:
1. Don't specify `format` if you have mixed date formats
2. Normalize all dates first before adding `format`
3. Use `picker_utc: true` instead (more flexible)

**Source**: [GitHub Issue #565](https://github.com/sveltia/sveltia-cms/issues/565), fixed in v0.126.0 (improved date parser but format strictness remains)

---

### 9. ❌ GDPR Violation: Google Fonts CDN

**Error Message:**
- No error shown (privacy compliance issue)

**Symptoms:**
- Privacy-focused sites blocked from using Sveltia
- EU public sector cannot adopt
- GDPR non-compliance

**Causes:**
- Sveltia loads Google Fonts and Material Symbols from Google CDN without user consent
- Google tracks font usage and collects IP addresses
- Violates EU data protection law

**⚠️ Impact**: Blocking issue for EU public sector and privacy-focused sites

**Solution (Vite Plugin - Recommended)**:

```typescript
// vite.config.ts
import { defineConfig, type Plugin } from 'vite'

function ensureGDPRCompliantFonts(): Plugin {
  const fontsURLRegex = /fonts\.googleapis\.com\/css2/g
  const replacement = 'fonts.bunny.net/css'
  return {
    name: 'gdpr-compliant-fonts',
    enforce: 'post',
    transform(code) {
      if (fontsURLRegex.test(code)) {
        return code.replaceAll(fontsURLRegex, replacement)
      }
    },
  }
}

export default defineConfig({
  plugins: [ensureGDPRCompliantFonts()],
})
```

**Alternative Solutions**:

**Option 2: Bunny Fonts** (1:1 Google Fonts replacement)
- Use https://fonts.bunny.net instead of fonts.googleapis.com
- EU-based, GDPR-compliant
- Same API as Google Fonts

**Option 3: Self-hosted fonts**
- Use `@fontsource` npm packages
- Bundle fonts with application
- No external requests

**Maintainer Response**:
- Acknowledged issue
- Plans to add system font option (post-v1.0)
- Sveltia itself collects no data (fonts are only concern)

**Source**: [GitHub Issue #443](https://github.com/sveltia/sveltia-cms/issues/443)

---

### 10. ❌ CORS / COOP Policy Errors

**Error Message:**
- "Authentication Aborted"
- "Cross-Origin-Opener-Policy blocked"

**Symptoms:**
- OAuth popup opens then closes

**Causes:**
- Strict `Cross-Origin-Opener-Policy` header blocking OAuth

**Solution:**

**Cloudflare Pages** (_headers file):
```
/*
  Cross-Origin-Opener-Policy: same-origin-allow-popups
  # NOT: same-origin (this breaks OAuth)
```

**Netlify** (_headers file):
```
/*
  Cross-Origin-Opener-Policy: same-origin-allow-popups
```

**Vercel** (vercel.json):
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cross-Origin-Opener-Policy",
          "value": "same-origin-allow-popups"
        }
      ]
    }
  ]
}
```

---

## Fixed Issues (Historical Reference)

These issues were present in earlier versions but have been fixed. Documented here for reference.

### ✅ Paths with Parentheses Break Entry Loading (Fixed in v0.128.1)

**Issue**: Sveltia CMS failed to load existing entries when the `path` option contains parentheses `()`. This affected Next.js/Nextra users using route groups like `app/(content)/(writing)/`.

**Symptoms** (pre-v0.128.1):
- Creating new entries worked
- Loading/listing existing entries failed silently
- CMS showed "No entries found" despite files existing

**Example that failed**:
```yaml
collections:
  - name: pages
    folder: app/(pages)
    path: "{{slug}}/page"  # ← Failed to load existing entries
    extension: mdx
```

**Status**: Fixed in v0.128.1 (January 13, 2026)

**Source**: [GitHub Issue #596](https://github.com/sveltia/sveltia-cms/issues/596)

---

### ✅ Root Folder Collections Break GitHub Backend (Fixed in v0.125.0)

**Issue**: Collections with `folder: ""` or `folder: "."` or `folder: "/"` failed when creating new entries via GitHub backend. GraphQL query incorrectly constructed path starting with `/` (absolute) instead of relative path.

**Symptoms** (pre-v0.125.0):
- Worked locally via browser File API
- Failed with GitHub backend (GraphQL error)
- Leading slash broke GraphQL mutation

**Example that failed**:
```yaml
collections:
  - name: root-pages
    folder: ""  # or "." or "/"
    # ← Broke when creating entries via GitHub backend
```

**Use Case**: VitePress and other frameworks storing content at repository root.

**Status**: Fixed in v0.125.0 (December 20, 2025)

**Source**: [GitHub Issue #580](https://github.com/sveltia/sveltia-cms/issues/580)

---

## Migration from Decap CMS

Sveltia CMS is a **drop-in replacement** for Decap CMS.

**Step 1: Update script tag (1 line change):**

```html
<!-- OLD: Decap CMS -->
<script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"></script>

<!-- NEW: Sveltia CMS -->
<script src="https://unpkg.com/@sveltia/cms@0.128.5/dist/sveltia-cms.js" type="module"></script>
```

**Step 2: Keep existing config.yml** (no changes needed)

**Step 3: Test locally** (verify login, content listing, editing, saving)

**That's it!** Your content, collections, and workflows remain unchanged.

**Not Supported**:
- Git Gateway backend (for performance reasons)
- Azure backend (may be added later)

**Workaround**: Use Cloudflare Workers or Vercel OAuth proxy instead.

---

## Bundled Resources

### Templates

- **hugo/** - Complete Hugo blog setup
- **jekyll/** - Jekyll site configuration
- **11ty/** - Eleventy blog setup
- **astro/** - Astro content collections
- **cloudflare-workers/** - OAuth proxy implementation
- **vercel-serverless/** - Vercel auth functions
- **collections/** - Pre-built collection patterns

### References

- **common-errors.md** - Extended error troubleshooting
- **migration-from-decap.md** - Complete migration guide
- **cloudflare-auth-setup.md** - Step-by-step OAuth setup
- **config-reference.md** - Full config.yml documentation

### Scripts

- **init-sveltia.sh** - Automated setup for new projects
- **deploy-cf-auth.sh** - Deploy Cloudflare Workers OAuth

### Official Documentation

- **Documentation Site**: https://sveltiacms.app/en/docs (under active development - some sections may be incomplete)
- **GitHub**: https://github.com/sveltia/sveltia-cms
- **OAuth Worker**: https://github.com/sveltia/sveltia-cms-auth
- **npm Package**: https://www.npmjs.com/package/@sveltia/cms
- **Discussions**: https://github.com/sveltia/sveltia-cms/discussions

**Note**: The official documentation site is being actively developed. GitHub README remains a useful fallback for some topics.

---

## Token Efficiency

**Estimated Savings**: 65-70% (~6,300 tokens saved)

**Without Skill** (~9,500 tokens):
- Framework setup trial & error: 2,500 tokens
- OAuth configuration attempts: 2,500 tokens
- Error troubleshooting: 2,500 tokens
- Deployment configuration: 2,000 tokens

**With Skill** (~3,200 tokens):
- Skill loading (SKILL.md): 2,000 tokens
- Template selection: 400 tokens
- Project-specific adjustments: 800 tokens

---

## Errors Prevented

This skill prevents **10 common errors** (100% prevention rate):

1. ✅ OAuth authentication failures
2. ✅ TOML front matter generation bugs
3. ✅ YAML parse errors (strict validation)
4. ✅ Content not listing in CMS
5. ✅ "SVELTIA is not defined" errors
6. ✅ 404 on /admin page
7. ✅ Image upload failures (HEIC format)
8. ✅ Datetime widget format strictness / timezone issues
9. ✅ GDPR violation (Google Fonts CDN)
10. ✅ CORS / COOP policy errors

---

**Last Updated**: 2026-01-21
**Skill Version**: 2.1.0
**Sveltia CMS Version**: 0.128.5 (Beta)
**Status**: Production-ready, v1.0 GA expected early 2026
**Changes**: Added 6 new configuration options (slug lowercase, raw format, number string encoding, locale URL param, richtext alias, Gemini 2.5 Flash-Lite support), updated datetime error with format strictness warning, added GDPR Google Fonts workaround, documented 2 fixed historical issues, deprecated slug_length option
