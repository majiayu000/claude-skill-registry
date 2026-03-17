---
name: github-pages
description: GitHub Pages static site hosting - setup, configuration, custom domains, Jekyll, and deployment
---

# GitHub Pages Skill

Use when working with GitHub Pages static site hosting, generated from official GitHub documentation.

## When to Use This Skill

This skill should be triggered when:
- Creating or configuring a GitHub Pages site
- Setting up custom domains for GitHub Pages
- Configuring publishing sources (branch, folder, or GitHub Actions)
- Working with Jekyll themes and plugins
- Troubleshooting GitHub Pages deployment issues
- Setting up HTTPS for GitHub Pages sites
- Understanding GitHub Pages limitations and features

## Quick Reference

### Site Types

| Type | Repository Name | URL |
|------|-----------------|-----|
| User site | `<username>.github.io` | `https://<username>.github.io` |
| Organization site | `<org>.github.io` | `https://<org>.github.io` |
| Project site | Any name | `https://<username>.github.io/<repo>` |

### Publishing Sources

1. **Branch publishing** - Deploy from a specific branch (e.g., `main`, `gh-pages`)
2. **Folder publishing** - Deploy from `/` (root) or `/docs` folder
3. **GitHub Actions** - Custom workflow for building and deploying

### Common Patterns

#### Create a GitHub Pages site
```bash
# Create repository named <username>.github.io for user site
# Or any name for project site

# Add index.html or index.md
echo "# Hello World" > index.md
git add index.md
git commit -m "Initial GitHub Pages site"
git push
```

#### Configure publishing source
1. Go to repository Settings > Pages
2. Under "Build and deployment", select source:
   - "Deploy from a branch" for static files
   - "GitHub Actions" for custom builds
3. Select branch and folder if using branch deployment

#### Set up custom domain
```bash
# Add CNAME file to repository root
echo "example.com" > CNAME
git add CNAME && git commit -m "Add custom domain" && git push
```

DNS Configuration:
- **Apex domain** (example.com): Add A records pointing to GitHub IPs
- **Subdomain** (www.example.com): Add CNAME record pointing to `<username>.github.io`

GitHub IP addresses for A records:
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

#### Jekyll configuration
```yaml
# _config.yml
title: My Site
description: A GitHub Pages site
theme: minima
plugins:
  - jekyll-feed
  - jekyll-seo-tag
```

#### Custom GitHub Actions workflow
```yaml
# .github/workflows/pages.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: ["main"]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: |
          # Your build commands here
          npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

#### Disable Jekyll processing
```bash
# Add .nojekyll file for non-Jekyll static sites
touch .nojekyll
git add .nojekyll && git commit -m "Disable Jekyll" && git push
```

### Supported Static Site Generators

GitHub provides workflow templates for:
- Jekyll (default)
- Next.js
- Nuxt.js
- Gatsby
- Hugo
- Astro
- Eleventy (11ty)
- And more...

### Limitations

- No server-side languages (PHP, Ruby, Python)
- Repository size limits apply
- Bandwidth and build time limits for free tier
- Private repos require GitHub Pro/Team/Enterprise

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **getting_started.md** - Site creation, publishing sources, workflows, HTTPS (5 articles)
- **custom_domains.md** - Domain setup, DNS configuration (2 articles)
- **jekyll.md** - Jekyll integration, themes, plugins (2 articles)
- **troubleshooting.md** - 404 errors and common issues (1 article)

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with `references/getting_started.md` for foundational concepts on creating your first GitHub Pages site.

### For Custom Domains
See `references/custom_domains.md` for DNS configuration and HTTPS setup.

### For Jekyll Users
Check `references/jekyll.md` for theme customization and Jekyll-specific features.

### For Debugging
Review `references/troubleshooting.md` for common issues like 404 errors.

## Common Issues

### 404 Error
- Check repository visibility (must be public for free accounts)
- Verify publishing source is configured correctly
- Ensure index.html or index.md exists
- Wait up to 10 minutes for changes to propagate

### Build Failures
- Check Jekyll syntax in _config.yml
- Verify Gemfile dependencies are compatible
- Review GitHub Actions logs for errors

### Custom Domain Not Working
- Verify DNS records are correct
- Check CNAME file is in repository root
- Ensure HTTPS is enforced in repository settings
- DNS propagation can take up to 24 hours

## Notes

- This skill was generated from official GitHub documentation
- Reference files preserve the structure and examples from source docs
- Content fetched via GitHub's Article API for accuracy
- Last updated: January 2026

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper using GitHub's Article API
2. The skill will be rebuilt with the latest information

## Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Actions for Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
