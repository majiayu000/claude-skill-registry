---
name: sveltia-cms
description: Sveltia CMS Git-backed content management (Decap/Netlify CMS successor). 5x smaller bundle (300 KB), GraphQL performance, solves 260+ issues. Use for static sites (Hugo, Jekyll, 11ty, Gatsby, Astro, Next.js), blogs, docs, i18n, or encountering OAuth errors, TOML/YAML issues, CORS problems, content listing errors.
license: MIT
allowed-tools: ['Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep']
metadata:
  token_savings: "60-65%"
  errors_prevented: 8
  package_version: "0.113.5"
  last_verified: "2025-10-29"
  frameworks: ["Hugo", "Jekyll", "11ty", "Gatsby", "Astro", "Next.js", "SvelteKit", "Framework-agnostic"]
  deployment: ["Cloudflare Workers", "Vercel", "Netlify", "GitHub Pages", "Cloudflare Pages"]
---

# Sveltia CMS Skill

Complete skill for integrating Sveltia CMS into static site projects.

---

## What is Sveltia CMS?

**Sveltia CMS** is a Git-based lightweight headless content management system built from scratch as the modern successor to Decap CMS (formerly Netlify CMS). It provides a fast, intuitive editing interface for content stored in Git repositories.

### Key Features

1. **Lightweight & Fast**
   - Bundle size: <500 KB (minified/brotlied) vs 1.5-2.6 MB for competitors
   - Built with Svelte compiler (no virtual DOM overhead)
   - Uses GraphQL APIs for instant content fetching
   - Relevance-based search across all content

2. **Modern User Experience**
   - Intuitive admin interface with full viewport utilization
   - Dark mode support (follows system preferences)
   - Mobile and tablet optimized
   - Drag-and-drop file uploads with multiple file support
   - Real-time preview with instant updates

3. **Git-Native Architecture**
   - Content stored as Markdown, MDX, YAML, TOML, or JSON
   - Full version control and change history
   - No vendor lock-in - content lives with code
   - Supports GitHub, GitLab, Gitea, Forgejo backends

4. **Framework-Agnostic**
   - Served as vanilla JavaScript bundle
   - Works with Hugo, Jekyll, 11ty, Gatsby, Astro, Next.js, SvelteKit
   - No React, Vue, or framework runtime dependencies
   - Compatible with any static site generator

5. **First-Class Internationalization**
   - Multiple language support built-in
   - One-click DeepL translation integration
   - Locale switching while editing
   - Flexible i18n structures (files, folders, single file)

6. **Built-In Image Optimization**
   - Automatic WebP conversion
   - Client-side resizing and optimization
   - SVG optimization support
   - Configurable quality and dimensions

### Current Versions

- **@sveltia/cms**: 0.113.5 (October 2025)
- **Status**: Public Beta (v1.0 expected early 2026)
- **Maturity**: Production-ready (265+ issues solved from predecessor)

---

## When to Use This Skill

### ✅ Use Sveltia CMS When:

1. **Building Static Sites**
   - Hugo blogs and documentation
   - Jekyll sites and GitHub Pages
   - 11ty (Eleventy) projects
   - Gatsby marketing sites
   - Astro content-heavy sites

2. **Non-Technical Editors Need Access**
   - Marketing teams managing pages
   - Authors writing blog posts
   - Content teams without Git knowledge
   - Clients needing easy content updates

3. **Git-Based Workflow Desired**
   - Content versioning through Git
   - Content review through pull requests
   - Content lives with code in repository
   - CI/CD integration for deployments

4. **Lightweight Solution Required**
   - Performance-sensitive projects
   - Mobile-first editing needed
   - Quick load times critical
   - Minimal bundle size important

5. **Migrating from Decap/Netlify CMS**
   - Existing config.yml can be reused
   - Drop-in replacement (change 1 line)
   - Better performance and UX
   - Active maintenance and bug fixes

### ❌ Don't Use Sveltia CMS When:

1. **Real-Time Collaboration Needed**
   - Multiple users editing simultaneously (Google Docs-style)
   - Use Sanity, Contentful, or TinaCMS instead

2. **Visual Page Building Required**
   - Drag-and-drop page builders needed
   - Use Webflow, Builder.io, or TinaCMS (React) instead

3. **Highly Dynamic Data**
   - E-commerce with real-time inventory
   - Real-time dashboards or analytics
   - Use traditional databases (D1, PostgreSQL) instead

4. **React-Specific Visual Editing Needed**
   - In-context component editing
   - Use TinaCMS instead (React-focused)

### Sveltia CMS vs TinaCMS

**Use Sveltia** for:
- Hugo, Jekyll, 11ty, Gatsby (non-React SSGs)
- Traditional CMS admin panel UX
- Lightweight bundle requirements
- Framework-agnostic projects

**Use TinaCMS** for:
- React, Next.js, Astro (React components)
- Visual in-context editing
- Schema-driven type-safe content
- Modern developer experience with TypeScript

**Both are valid** - Sveltia complements TinaCMS for different use cases.

---

## Quick Start

**Load `references/framework-setup.md` for complete framework-specific setup** (Hugo, Jekyll, 11ty, Astro, Next.js, Gatsby, SvelteKit).

### Basic Setup Steps (Framework-Agnostic)

1. **Create admin directory** in your public folder (e.g., `static/admin`, `public/admin`)
2. **Create `admin/index.html`** with Sveltia CMS script tag
3. **Create `admin/config.yml`** with backend and collections
4. **Set up authentication** → See `references/authentication-guide.md`
5. **Test locally** by visiting `/admin/`

**Templates available** in `templates/` directory for each framework.

---

## Authentication Setup

**Load `references/authentication-guide.md` for complete OAuth setup instructions**.

### Quick Overview

| Method | Best For | Complexity |
|--------|----------|-----------|
| Cloudflare Workers | All deployments | Easy ⭐ |
| Vercel Serverless | Vercel projects | Medium |
| Local Development | Dev only | Easy |

**Recommended**: Cloudflare Workers OAuth (official, fast, free)

**Templates**: See `templates/cloudflare-workers/` and `templates/vercel-serverless/`

---

## Configuration

**Load `references/configuration-guide.md` for complete config.yml documentation, collection patterns, and i18n setup**.

### Essential Config Structure

```yaml
backend:
  name: github
  repo: owner/repo
  branch: main
  base_url: https://your-worker.workers.dev

media_folder: static/images
public_folder: /images

collections:
  - name: posts
    label: Blog Posts
    folder: content/posts
    create: true
    fields:
      - { label: Title, name: title, widget: string }
      - { label: Body, name: body, widget: markdown }
```

**Collection templates** available in `templates/collections/` for blogs, docs, and landing pages.

**i18n support**: Multiple files, folders, or single file structures - see reference guide.

---

## Common Errors & Solutions

This skill prevents **8 common errors**. Top 3 shown below - **load `references/error-catalog.md` for all 8 with complete solutions**.

### 1. ❌ OAuth Authentication Failures

**Error**: "Error: Failed to authenticate" / redirects to wrong domain

**Quick Fix:**
- Verify `base_url` in `config.yml` points to your OAuth proxy
- Check GitHub OAuth callback URL matches Worker URL
- Test Worker: `curl https://your-worker.workers.dev/health`

**→ Load `references/error-catalog.md` Error #1 for complete solution**

---

### 2. ❌ Content Not Listing in CMS

**Error**: "No entries found" / empty content list

**Quick Fix:**
- Verify `folder` path matches actual file location
- Match `format` to actual file format (yaml vs toml)
- Check file extensions match config

**→ Load `references/error-catalog.md` Error #4 for complete solution**

---

### 3. ❌ CORS / COOP Policy Errors

**Error**: "Authentication Aborted" / OAuth popup closes

**Quick Fix:**
- Set `Cross-Origin-Opener-Policy: same-origin-allow-popups` in headers
- Add OAuth proxy to CSP `connect-src`

**→ Load `references/error-catalog.md` Error #8 for complete solution**

---

**All 8 errors with detailed solutions:** See `references/error-catalog.md`

---

## Migration from Decap CMS

Sveltia is a **drop-in replacement** - just change the script tag!

```html
<!-- OLD: Decap CMS -->
<script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"></script>

<!-- NEW: Sveltia CMS -->
<script src="https://unpkg.com/@sveltia/cms/dist/sveltia-cms.js" type="module"></script>
```

Your existing `config.yml` works as-is. **Load `references/migration-from-decap.md` for complete migration guide and testing checklist**.

---

## Deployment

**Load `references/deployment-guide.md` for platform-specific deployment instructions** (Cloudflare Pages, Vercel, Netlify, GitHub Pages).

### Quick Deployment Checklist

- [ ] Admin directory in correct public folder
- [ ] OAuth proxy deployed and configured
- [ ] `base_url` set in config.yml
- [ ] Build command configured
- [ ] Test `/admin/` route after deployment

---

## When to Load References

**Load `references/framework-setup.md` when:**
- User needs framework-specific setup (Hugo, Jekyll, 11ty, Astro, etc.)
- Setting up new Sveltia CMS installation
- Troubleshooting framework-specific admin directory issues

**Load `references/authentication-guide.md` when:**
- Setting up GitHub OAuth authentication
- Deploying Cloudflare Workers OAuth proxy
- Troubleshooting authentication errors
- User asks about `base_url` configuration

**Load `references/configuration-guide.md` when:**
- User needs complete `config.yml` examples
- Setting up collections, fields, or widgets
- Configuring media uploads, i18n, or workflows
- User asks about specific configuration options

**Load `references/error-catalog.md` when:**
- User encounters any errors during setup
- Troubleshooting authentication, parsing, or deployment issues
- User reports errors beyond the top 3 shown above

**Load `references/deployment-guide.md` when:**
- Deploying to Cloudflare Pages, Netlify, or Vercel
- Setting up OAuth proxy deployment
- Troubleshooting production deployment issues

**Load `references/migration-from-decap.md` when:**
- Migrating from Decap CMS / Netlify CMS
- User asks about compatibility or migration steps

---

## Resources

**Templates**: `templates/hugo/`, `templates/jekyll/`, `templates/cloudflare-workers/`
**Official Docs**: https://github.com/sveltia/sveltia-cms
**OAuth Worker**: https://github.com/sveltia/sveltia-cms-auth

---

## Package Information

**Current Version**: @sveltia/cms@0.113.5 (October 2025)
**Status**: Production-ready, v1.0 expected early 2026

---

**Last Updated**: 2025-10-24
