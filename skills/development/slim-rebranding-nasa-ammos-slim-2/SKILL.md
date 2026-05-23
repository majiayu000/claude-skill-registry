---
name: slim-rebranding
description: Rebranding agent for branding the slim framework for a new project customized for a specific domain. main. Use this skill whenever you'd like to leverage the Slim Marketplace framework for a customized project, but you don't want to keep the slim branding.
---

# SLIM Website Rebranding

## Workflow

### Step 1: Input Collection
- Collect project name, tagline, logo, organization details
- Ask about external registry imports and local marketplace handling

### Step 2: Git Branch
- Create branch: `rebrand/website-{old-slug}-to-{new-slug}`

### Step 3: Update Configuration
- Update `docusaurus.config.js` fields: title, tagline, url, baseUrl, organizationName, projectName
- Update `brandingConfig`: logoPath, hero settings, marketplace settings
- Update `slimConfig.registries` if external imports requested
- Place logo file if provided

### Step 4: Registry Processing
- Fetch external registry URLs if requested
- Insert external registry entries with `external_only: true` and `repository.url` into `docusaurus.config.js` section for `slimConfig`
- Clear local marketplace `.claude-plugin/marketplace.json` and `static/data/registry.json` based on user choice

### Step 5: Documentation Generation
- Generate `docs/contribute/submit-best-practice.md`
- Generate `docs/faq/README.md`
- Generate `docs/about/README.md`

### Step 6: Final Updates
- Update `README.md` references
- Update `package.json` if needed
- Run `npm install; npm run build`
- Commit changes

## Dependencies
- `src/utils/brandingUtils.js`
- `src/hooks/useBrandingConfig.js`

## Prerequisites
- SLIM-based Docusaurus website
- Git repository initialized
- Node.js and npm installed
