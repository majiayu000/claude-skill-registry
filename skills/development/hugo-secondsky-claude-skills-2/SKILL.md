---
name: hugo
description: Hugo static site generator with Tailwind v4, headless CMS (Sveltia/Tina), Cloudflare deployment. Use for blogs, docs sites, or encountering theme installation, frontmatter, baseURL errors.

  Keywords: hugo, hugo-extended, static-site-generator, ssg, go-templates, papermod, goldmark, markdown, blog, documentation, docs-site, landing-page, sveltia-cms, tina-cms, headless-cms, cloudflare-workers, workers-static-assets, wrangler, hugo-server, hugo-build, frontmatter, yaml-frontmatter, toml-config, hugo-themes, hugo-modules, multilingual, i18n, github-actions, version-mismatch, baseurl-error, theme-not-found, tailwind, tailwind-v4, tailwind-css, hugo-pipes, postcss, css-framework, utility-css, hugo-tailwind, tailwind-integration, hugo-assets
license: MIT
metadata:
  version: "2.0.0"
  hugo_version: "0.152.2"
  tailwind_version: "4.1.16"
  last_verified: "2025-11-04"
  production_tested: true
  token_savings: "60-65%"
  errors_prevented: 15
  templates_included: 4
  references_included: 6
---

# Hugo Static Site Generator

**Status**: Production Ready | **Last Updated**: 2025-11-21
**Latest Version**: hugo@0.152.2+extended | **Build Speed**: <100ms

---

## Quick Start (5 Minutes)

### 1. Install Hugo Extended

**CRITICAL**: Always install Hugo **Extended** edition (not Standard) unless you're certain you don't need SCSS/Sass support. Most themes require Extended.

```bash
# macOS
brew install hugo

# Linux (Ubuntu/Debian)
wget https://github.com/gohugoio/hugo/releases/download/v0.152.2/hugo_extended_0.152.2_linux-amd64.deb
sudo dpkg -i hugo_extended_0.152.2_linux-amd64.deb

# Verify Extended edition
hugo version  # Should show "+extended"
```

**Why this matters:**
- Hugo Extended includes SCSS/Sass processing
- Most popular themes (PaperMod, Academic, Docsy) require Extended
- Standard edition will fail with "SCSS support not enabled" errors
- Extended has no downsides (same speed, same features + more)

### 2. Create New Hugo Site

```bash
# Use YAML format (not TOML) for better CMS compatibility
hugo new site my-blog --format yaml

# Initialize Git
cd my-blog
git init

# Add PaperMod theme (recommended for blogs)
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

**CRITICAL:**
- Use `--format yaml` to create hugo.yaml (not hugo.toml)
- YAML is required for Sveltia CMS and recommended for TinaCMS
- TOML has known bugs in Sveltia CMS beta
- Git submodules require `--recursive` flag when cloning later

### 3. Configure and Build

```yaml
# hugo.yaml - Minimal working configuration
baseURL: "https://example.com/"
title: "My Hugo Blog"
theme: "PaperMod"
languageCode: "en-us"
enableRobotsTXT: true

params:
  ShowReadingTime: true
  ShowShareButtons: true
  defaultTheme: auto  # Supports dark/light/auto
```

```bash
# Create first post
hugo new content posts/first-post.md

# Run development server (with live reload)
hugo server

# Build for production
hugo --minify

# Output is in public/ directory
```

---

## Critical Rules

### Always Do

✅ **Install Hugo Extended** (not Standard) - required for SCSS/Sass support in themes
✅ **Use YAML configuration** (`--format yaml`) - better CMS compatibility than TOML
✅ **Add themes as Git submodules** - easier updates and version control
✅ **Set correct baseURL** - prevents broken asset links on deployment
✅ **Pin Hugo version in CI/CD** - prevents version mismatch errors between local and deployment
✅ **Add `public/` to .gitignore** - build output should not be committed
✅ **Use `draft: false`** - drafts don't appear in production builds
✅ **Clone with `--recursive` flag** - ensures theme submodules are fetched
✅ **Use relative paths for images** - `/images/photo.jpg` not `../images/photo.jpg`
✅ **Test build before deploying** - catch errors locally with `hugo --minify`

### Never Do

❌ **Don't install Hugo Standard** - most themes require Extended edition
❌ **Don't use TOML config with Sveltia CMS** - has known bugs, use YAML instead
❌ **Don't commit `public/` directory** - it's generated output, not source code
❌ **Don't use different Hugo versions** - local vs CI/CD version mismatch causes errors
❌ **Don't forget `submodules: recursive`** - themes won't load in CI/CD
❌ **Don't hardcode production URLs** - use `-b $CF_PAGES_URL` or environment configs
❌ **Don't push `resources/_gen/`** - generated assets, should be in .gitignore
❌ **Don't use future dates carelessly** - posts won't publish until date passes
❌ **Don't skip `.hugo_build.lock`** - add to .gitignore
❌ **Don't mix YAML and TOML** - stick to one format throughout project

---

## Top 5 Errors Prevention

This skill prevents **15 documented errors**. Here are the top 5:

### Error #1: Version Mismatch (Hugo vs Hugo Extended)
**Error**: `Error: SCSS support not enabled`
**Prevention**: Always install Hugo Extended edition. Verify with `hugo version | grep extended`
**See**: `references/error-catalog.md` for full error list

### Error #2: baseURL Configuration Errors
**Error**: Broken CSS/JS/image links, 404s on all assets
**Prevention**: Use environment-specific configs or build flag: `hugo -b $CF_PAGES_URL`
**See**: `references/error-catalog.md` #2

### Error #3: Theme Not Found Errors
**Error**: `Error: module "PaperMod" not found`, blank site
**Prevention**: Set `theme: "PaperMod"` in hugo.yaml and run `git submodule update --init --recursive`
**See**: `references/error-catalog.md` #6

### Error #4: Hugo Version Mismatch (Local vs Deployment)
**Error**: Features work locally but fail in CI/CD, or vice versa
**Prevention**: Pin Hugo version everywhere (CI/CD, local docs, package.json if using npm)
**See**: `references/error-catalog.md` #4

### Error #5: Git Submodule Not Found in CI/CD
**Error**: Theme works locally but not in CI/CD, blank site on deployment
**Prevention**: Add `submodules: recursive` to checkout action in GitHub Actions
**See**: `references/error-catalog.md` #11

**For complete error catalog** (all 15 errors): See `references/error-catalog.md`

---

## Using Bundled Resources

**References** (`references/`):
- `setup-guide.md` - Complete Hugo setup walkthrough (installation, themes, deployment)
- `error-catalog.md` - All 15 common Hugo errors with solutions and prevention
- `common-patterns.md` - Best practices and patterns (taxonomies, content organization, multilingual)
- `cms-integration.md` - Sveltia CMS integration guide with configuration
- `tailwind-integration.md` - Tailwind CSS integration with Hugo Pipes
- `advanced-topics.md` - Advanced Hugo features (modules, data files, internationalization)

### Templates (templates/)

Complete, production-ready Hugo projects ready to copy:

- **`templates/hugo-blog/`** - Blog with PaperMod theme
  - Dark/light mode, search, tags, archives
  - Sveltia CMS pre-configured
  - wrangler.jsonc for Workers deployment
  - GitHub Actions workflow included
  - **Use when**: Building a personal blog, company blog, or news site

- **`templates/hugo-docs/`** - Documentation site with Hugo Book theme
  - Nested navigation, search, breadcrumbs
  - Sveltia CMS for docs editing
  - **Use when**: Creating technical documentation, knowledge bases, API docs

- **`templates/hugo-landing/`** - Landing page with custom layouts
  - Hero, features, testimonials, CTA sections
  - No theme dependency (custom layouts)
  - Optimized for conversions
  - **Use when**: Building marketing sites, product pages, portfolios

- **`templates/minimal-starter/`** - Bare-bones starter
  - No theme, clean slate
  - Setup guide for adding themes
  - Minimal configuration
  - **Use when**: Starting from scratch with full control

**Quick start with template:**
```bash
cp -r templates/hugo-blog/ my-new-blog/
cd my-new-blog
git submodule update --init --recursive
hugo server
```

### References (references/)

Detailed guides loaded when needed:

- **`references/setup-guide.md`** - Complete 7-step setup process
  - Installation and verification
  - Project scaffolding
  - Theme installation
  - Configuration options
  - Content creation
  - Build and development
  - Cloudflare Workers deployment
  - **Load when**: Setting up new Hugo project from scratch

- **`references/cms-integration.md`** - Headless CMS integration
  - Sveltia CMS setup (recommended) - 5 minutes
  - OAuth configuration for production
  - TinaCMS setup (not recommended)
  - Comparison and troubleshooting
  - **Load when**: Adding content management to Hugo site

- **`references/tailwind-integration.md`** - Tailwind CSS v4 integration
  - Hugo Pipes + PostCSS setup
  - Dark mode implementation (CSS-only and Alpine.js)
  - Typography and Forms plugins
  - Production optimization
  - Common issues and solutions
  - **Load when**: Integrating Tailwind CSS with Hugo

- **`references/common-patterns.md`** - 7 common project patterns
  - Blog with PaperMod
  - Documentation with Hugo Book
  - Landing pages
  - Multilingual sites
  - Portfolio sites
  - E-commerce (static)
  - Newsletter/blog
  - **Load when**: Choosing architecture for specific use case

- **`references/advanced-topics.md`** - Advanced Hugo features
  - Custom shortcodes
  - Image processing
  - Custom taxonomies
  - Data files (JSON/YAML/CSV)
  - Page bundles
  - Template overrides
  - Hugo Modules
  - **Load when**: User needs advanced customization

- **`references/error-catalog.md`** - All 15 documented errors
  - Complete error messages and solutions
  - Prevention strategies
  - Official sources cited
  - Troubleshooting guide
  - **Load when**: Debugging issues or preventing known errors

---

## Common Use Cases

### Use Case 1: Personal Blog
**Template**: `templates/hugo-blog/`
**Theme**: PaperMod
**Time to deploy**: 10 minutes
**Features**: Search, tags, dark mode, RSS, Sveltia CMS

```bash
cp -r templates/hugo-blog/ my-blog/
cd my-blog
git submodule update --init --recursive
hugo new content posts/first-post.md
hugo server
```

See `references/common-patterns.md` → Pattern 1

### Use Case 2: Technical Documentation
**Template**: `templates/hugo-docs/`
**Theme**: Hugo Book
**Time to deploy**: 10 minutes
**Features**: Nested navigation, search, breadcrumbs, multi-language

```bash
cp -r templates/hugo-docs/ docs-site/
cd docs-site
git submodule update --init --recursive
hugo new content docs/getting-started/installation.md
hugo server
```

See `references/common-patterns.md` → Pattern 2

### Use Case 3: Landing Page
**Template**: `templates/hugo-landing/`
**Theme**: None (custom layouts)
**Time to deploy**: 15 minutes
**Features**: Hero, features, testimonials, CTA, contact form

```bash
cp -r templates/hugo-landing/ landing/
cd landing
hugo server
```

See `references/common-patterns.md` → Pattern 3

### Use Case 4: Blog with Tailwind CSS v4
**Template**: Start with `templates/minimal-starter/`
**Integration**: Follow `references/tailwind-integration.md`
**Time to setup**: 30 minutes
**Features**: Custom design, utility-first CSS, dark mode

```bash
cp -r templates/minimal-starter/ tailwind-blog/
cd tailwind-blog
# Follow references/tailwind-integration.md for setup
```

See `references/tailwind-integration.md` → Quick Start

### Use Case 5: Multilingual Documentation
**Template**: `templates/hugo-docs/`
**Pattern**: Multilingual
**Time to setup**: 20 minutes
**Features**: Language switcher, translated content, per-language menus

See `references/common-patterns.md` → Pattern 4

---

## Cloudflare Workers Deployment

### Quick Deployment

**1. Create wrangler.jsonc:**
```jsonc
{
  "name": "my-hugo-site",
  "compatibility_date": "2025-01-29",
  "assets": {
    "directory": "./public",
    "html_handling": "auto-trailing-slash",
    "not_found_handling": "404-page"
  }
}
```

**2. Deploy:**
```bash
hugo --minify
bunx wrangler deploy
```

**For complete deployment guide:** See `references/setup-guide.md` → Step 7

---

## When to Load Detailed References

**Load `references/setup-guide.md` when:**
- User needs complete 7-step setup process
- User asks about configuration options
- User needs detailed installation instructions
- User asks about directory structure
- User needs GitHub Actions workflow

**Load `references/cms-integration.md` when:**
- User wants to add CMS to Hugo site
- User asks about Sveltia CMS setup
- User asks about TinaCMS (warn it's not recommended)
- User needs OAuth configuration
- User asks about content management

**Load `references/tailwind-integration.md` when:**
- User wants to integrate Tailwind CSS v4
- User asks about PostCSS setup
- User needs dark mode implementation
- User asks about Tailwind plugins
- User has CSS processing errors

**Load `references/common-patterns.md` when:**
- User asks "how do I build a [blog/docs/landing page]?"
- User needs architecture guidance
- User asks about multilingual sites
- User asks about portfolio sites
- User needs project structure examples

**Load `references/advanced-topics.md` when:**
- User asks about shortcodes
- User needs image processing
- User wants custom taxonomies
- User asks about data files
- User needs template customization

**Load `references/error-catalog.md` when:**
- User encounters an error
- User asks about troubleshooting
- User wants to prevent known issues
- User asks "what errors should I watch out for?"
- User has deployment issues

---

## Dependencies

**Required**:
- Hugo v0.149.0+ (Extended edition) - Static site generator

**Optional** (for deployment):
- wrangler v4.0.0+ - Cloudflare Workers deployment
- Git v2.0+ - Version control and theme submodules

**Optional** (for CMS):
- Sveltia CMS (latest) - Content management (CDN-based, no installation)

---

## Official Documentation

- **Hugo**: https://gohugo.io/documentation/
- **PaperMod Theme**: https://github.com/adityatelange/hugo-PaperMod/wiki
- **Hugo Book Theme**: https://github.com/alex-shpak/hugo-book
- **Sveltia CMS**: https://github.com/sveltia/sveltia-cms
- **Cloudflare Workers**: https://developers.cloudflare.com/workers/
- **Hugo Themes**: https://themes.gohugo.io/

---

## Package Versions (Verified 2025-11-04)

**Hugo**: v0.152.2+extended (October 24, 2025)
**PaperMod**: Latest (via Git submodule)
**Sveltia CMS**: Latest (via CDN)
**Wrangler**: v4.37.1+ (v4.45.3 available)

---

## Production Example

This skill is based on live testing:
- **Test Site**: https://hugo-blog-test.webfonts.workers.dev
- **Build Time**: 24ms (20 pages)
- **Deployment Time**: ~21 seconds
- **Errors**: 0 (all 15 known issues prevented)
- **Validation**: ✅ Hugo + PaperMod + Sveltia + Workers deployed successfully

---

## Complete Setup Checklist

Use this checklist to verify your setup:

- [ ] Hugo Extended v0.149.0+ installed (`hugo version` shows "+extended")
- [ ] Project created with `--format yaml` (hugo.yaml exists)
- [ ] Theme installed and configured (via Git submodule or Hugo Module)
- [ ] `baseURL` configured correctly in hugo.yaml
- [ ] `.gitignore` includes `public/` and `resources/_gen/`
- [ ] Sample content created and renders correctly
- [ ] Dev server runs without errors (`hugo server`)
- [ ] Production build succeeds (`hugo --minify`)
- [ ] wrangler.jsonc configured for Workers (if deploying)
- [ ] Sveltia CMS configured (if using CMS)
- [ ] GitHub Actions workflow configured (if using CI/CD)
- [ ] Deployed successfully (if deploying to Workers)

---

**Questions? Issues?**

1. Check `references/error-catalog.md` for all 15 documented errors and solutions
2. Verify all steps in the setup process
3. Use appropriate template from `templates/` directory
4. Load relevant reference guide for detailed information
5. Check official docs: https://gohugo.io/documentation/

---

**This skill provides production-ready Hugo setup with zero errors. All 15 common issues are documented and prevented.**
