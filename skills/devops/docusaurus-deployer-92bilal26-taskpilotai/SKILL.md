---
name: docusaurus-deployer
version: 1.2
description: This skill should be used when deploying a Docusaurus site to GitHub Pages. It automates the configuration, building, and deployment process, handling GitHub Pages setup, environment configuration, and CI/CD automation. Includes local validation before GitHub Actions triggering.
constitution_alignment: v4.0.1
---

# Docusaurus GitHub Pages Deployer

Automate building and deploying Docusaurus documentation sites to GitHub Pages with local validation before CI/CD triggering.

**Constitution Alignment**: This skill implements production deployment standards defined in Constitution v4.0.1 (Pillar 9: Universal Cloud-Native Deployment from Section I). All deployments must meet project quality gates before publication.

## What This Skill Does

1. **Project Analysis** - Examine Docusaurus structure and dependencies
2. **Local Configuration Validation** - Verify Docusaurus config and sidebars
3. **Local Build & Testing** - Build site locally and validate output
4. **Content Verification** - Check for broken links and syntax errors
5. **GitHub Pages Setup** - Configure repository and deployment settings
6. **CI/CD Automation** - Set up GitHub Actions workflows
7. **Deployment Verification** - Validate successful deployment

## When to Use This Skill

Deploy Docusaurus to GitHub Pages when:
- Setting up documentation deployment for the first time
- Making updates to documentation before publishing
- Updating deployment configuration
- Troubleshooting deployment issues
- Managing multiple documentation sites
- Ensuring documentation quality before production

## How to Use This Skill

Follow the **validate-locally-then-publish** workflow:

### Step 1: Prepare Repository Configuration
Gather GitHub organization/username, repository name, deployment target (user/project pages), and custom domain (optional).

### Step 2: Analyze Project Structure
Examine Docusaurus project:
```bash
ls -la path_to_docusaurus_project/
cat path_to_docusaurus_project/docusaurus.config.ts
cat path_to_docusaurus_project/sidebars.ts
```

Verify docusaurus.config.ts, sidebars.js/ts, package.json engines field, and dependencies exist.

For detailed configuration guidance, see `references/configuration-guide.md`.

### Step 3: Update Docusaurus Configuration
Update `docusaurus.config.ts` with GitHub Pages settings. See `references/configuration-guide.md` for complete configuration examples and guidelines based on deployment target (user vs. project pages).

### Step 4: Build and Validate Locally
Install dependencies, run type checking, build site, validate output, test locally, and verify content quality.

Execute:
```bash
npm ci
npm run typecheck
npm run build
npm run serve
```

For detailed validation procedures, see `references/local-validation-guide.md`.

### Step 5: Commit and Push to Main
After successful local validation:
```bash
git add .
git commit -m "Update documentation: [description]"
git push origin main
```

This triggers the GitHub Actions workflow.

### Step 6: Set Up GitHub Actions
Create `.github/workflows/deploy.yml` using the template in `references/deploy-workflow.yml`.

For detailed workflow configuration and troubleshooting, see `references/github-actions-guide.md`.

### Step 7: Configure GitHub Pages in Repository Settings
1. Go to **Settings → Pages**
2. Set source to **GitHub Actions** (or deploy from `gh-pages` branch)
3. Configure custom domain if needed
4. Enable branch protection on main branch

### Step 8: Verify Deployment
Check GitHub Actions workflow status in Actions tab, verify site loads at configured URL, and confirm all navigation works.

## Troubleshooting

For common issues and solutions, see `references/troubleshooting.md`, which covers:
- Build failures and type errors
- 404 errors after deployment
- Broken links and GitHub Actions issues
- Performance problems and content quality

## Bundled Resources

- `references/deploy-workflow.yml` - GitHub Actions workflow template
- `references/configuration-guide.md` - Detailed Docusaurus configuration
- `references/local-validation-guide.md` - Build and validation procedures
- `references/github-actions-guide.md` - CI/CD setup and configuration
- `references/troubleshooting.md` - Common issues and solutions
- `references/performance-standards.md` - Performance targets and best practices

## Performance Targets

- **Build time**: < 30 seconds (typical)
- **Page load**: < 3 seconds
- **Bundle size**: Optimized for documentation
- **Accessibility**: WCAG 2.1 AA compliance

## Quality Gates (Constitution v3.1.2)

Before deployment to production, verify:
- [ ] All content passes validation-auditor validation
- [ ] Local build completes without errors
- [ ] No broken links or missing resources
- [ ] TypeScript type checking passes
- [ ] Performance targets met
- [ ] Accessibility standards verified
- [ ] GitHub Actions workflow configured correctly

**Reference**: See `.specify/memory/constitution.md` deployment standards section for complete production deployment standards.

## Tools Used

- Node.js/npm (v20+)
- Docusaurus CLI
- TypeScript
- GitHub Actions
- GitHub Pages
