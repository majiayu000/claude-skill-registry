---
name: slim-rebranding
description: Comprehensive workflow for rebranding SLIM-based Docusaurus websites for domain-specific projects. Handles hero customization, registry imports from external SLIM instances, page template generation, and complete website configuration. Creates customized SLIM forks with domain-specific branding, marketplace entries, and documentation. Includes detailed plan templates and step-by-step guides with git workflow and iterative build testing.
---

# SLIM Website Rebranding

## Overview

The SLIM Website Rebranding skill is a comprehensive workflow designed to help users fork and rebrand SLIM-based Docusaurus documentation websites for their own domain-specific projects. It provides templates, guides, and step-by-step instructions for creating customized SLIM instances with unique branding, curated marketplace entries, and tailored documentation.

## When to Use

- Forking SLIM for a domain-specific project or organization
- Creating a customized best practices hub for your team
- Rebranding SLIM with your project's identity and logo
- Building a curated marketplace from multiple SLIM sources
- Launching a new best practices website based on SLIM architecture

## Workflow

### Step 1: Context Gathering & Detection

**Verify your SLIM website setup and extract current metadata:**

1. **Git Repository Check**:
   - Verify git repository exists and is clean

2. **Docusaurus Website Detection**:
   - Verify this is a Docusaurus-based website

3. **Current Metadata Extraction**:
   - Read `docusaurus.config.js`:
     - Extract current title (project name)
     - Extract current tagline
     - Extract url and baseUrl
   - Read `static/data/registry.json`:
     - Count skills, agents, MCP servers
     - Identify entry naming pattern (e.g., "slim-*" prefix)
   - Read `package.json`:
     - Extract package name
     - Extract description

4. **Website Structure Verification**:
   - Verify hero component exists: `src/components/HubHero.js`
   - Verify registry exists: `static/data/registry.json`
   - Verify marketplace structure: `static/marketplace/`
   - Verify documentation pages: `docs/contribute/`, `docs/faq/`, `docs/about/`

---

### Step 2: SLIM Website Questionnaire

**Answer essential questions specific to SLIM website rebranding:**

Using the SLIM website questionnaire template (`assets/slim-website-questionnaire.md`), answer up to 10 questions:

1. **Current project name** (auto-detected): Confirmed as "{DETECTED_NAME}"
2. **New project name**: What should the new project name be? (e.g., "AutoDocs", "TeamHub", "DevBestPractices")
3. **New tagline**: What should the new tagline be? (leave blank to keep current: "{CURRENT_TAGLINE}")
4. **New logo file**: Upload logo file (SVG/PNG) or leave blank to auto-generate from Phosphor icons
5. **Project purpose/domain**: Describe your project's purpose in 2-3 sentences (for About page)
6. **Team/organization info**: Who maintains this project? (organization name, GitHub org, contact info)
7. **Import from external SLIM instances?**: Do you want to import best practices from other SLIM instances? (yes/no, default: no)
8. **GitHub URLs for import** (if yes to #7): Provide comma-separated GitHub URLs (e.g., "https://github.com/NASA-AMMOS/slim, https://github.com/other-org/slim-fork")
9. **Keep existing marketplace entries?**: Keep current local marketplace entries? (yes/no, default: no - fresh start)
10. **Git branch name**: Custom git branch name or leave blank for auto-generated (default: `rebrand/website-{old-slug}-to-{new-slug}`)

**Automatic Defaults** (no questions needed):
- **Hero corners**: Always remove 4 corner feature sidebars
- **Page generation**: Always generate contribute, FAQ, and about page templates
- **Empty marketplace**: Always handle gracefully with friendly UI
- **Build validation**: Always run iterative build loop

**Output Example**:
```
Questionnaire complete:
- New name: "AutoDocs"
- New tagline: "AI-powered documentation automation for software projects"
- Logo: Auto-generate from Phosphor icons (project keywords: "docs", "automation")
- Project purpose: "AutoDocs helps development teams automate documentation..."
- Organization: "AutoDocs Team (https://github.com/autodocs)"
- Import from: https://github.com/NASA-AMMOS/slim
- Keep existing: no (fresh start)
- Branch: rebrand/website-slim-to-autodocs
```

---

### Step 3: Discovery & Import Phase

**Scan your SLIM website structure and optionally import from external sources:**

#### A. Website Structure Discovery

1. **Hero Component Analysis**:
   - Read `src/components/HubHero.js`
   - Identify corner features array (lines 57-78)
   - Identify corner feature rendering (lines 83-88)
   - Identify logo path (line 93)
   - Identify tagline text (lines 96-98)

2. **CSS Analysis**:
   - Read `src/css/custom.css`
   - Identify corner feature styles (~lines 501-675)
   - Note: These styles will be removed

3. **Current Registry Analysis**:
   - Read `static/data/registry.json`
   - Count local vs external entries
   - Identify naming patterns
   - Note dependencies between entries

4. **Marketplace Analysis**:
   - Scan `static/marketplace/skills/`
   - Scan `static/marketplace/agents/`
   - Scan `static/marketplace/mcp-servers/`
   - Count local files vs external references

#### B. External Registry Import (if requested)

**Using the registry import guide (`assets/registry-import-guide.md`):**

**For each GitHub URL provided**:

1. **Parse GitHub URL**:
   ```
   Input: https://github.com/NASA-AMMOS/slim
   Extract: org="NASA-AMMOS", repo="slim"
   ```

2. **Construct Raw URL**:
   ```
   https://raw.githubusercontent.com/NASA-AMMOS/slim/main/static/data/registry.json
   ```

3. **Fetch External Registry**:
   - Send HTTP GET request
   - Handle errors (404, network failures)
   - Parse JSON
   - Validate structure

4. **Transform Entries** (using existing `external_only: true` support):
   - For each skill/agent/mcp in external registry:
     ```json
     {
       "name": "autodocs-readme",  // Renamed from "slim-readme"
       "displayName": "README Writer",
       "description": "...",
       "category": "documentation",
       "tags": ["..."],
       "lastUpdated": "2024-08-02",
       "skill_file_url": "https://raw.githubusercontent.com/NASA-AMMOS/slim/main/static/marketplace/skills/slim-readme/SKILL.md",
       "external_only": true,  // NEW: marks as external
       "repository": {  // NEW: points to source
         "url": "https://github.com/NASA-AMMOS/slim",
         "type": "git"
       },
       "type": "skill",
       "example": "..."
     }
     ```
   - Rename: "slim-*" → "{new-project-name}-*"
   - Add `external_only: true` flag
   - Add `repository.url` field
   - Keep original `skill_file_url` (points to external source)

5. **Merge & Deduplicate**:
   - Combine all imported entries
   - Remove duplicates by name
   - Sort alphabetically

**Validation**:
- Verify all transformed entries have required fields
- Validate `skill_file_url` accessibility (HTTP HEAD requests)
- Report import statistics

**Output Example**:
```
Discovery Results:
✓ Hero component: 4 corner sidebars identified (will be removed)
✓ CSS styles: ~175 lines of corner styling (will be removed)
✓ Current registry: 14 local skills, 2 local agents, 1 external MCP
✓ Marketplace: 16 local item folders

Import Results:
✓ Fetched registry from: https://github.com/NASA-AMMOS/slim
✓ Imported 17 entries (14 skills, 2 agents, 1 MCP)
✓ Transformed: "slim-*" → "autodocs-*"
✓ All entries marked as external_only: true
✓ All skill_file_url validated and accessible
```

---

### Step 4: Plan Generation

**Generate a comprehensive SLIM website rebranding plan:**

Using the SLIM rebrand plan template (`assets/rebrand-plan-template.md`), create a detailed plan:

**Plan Structure**:
```markdown
# SLIM Website Rebranding Plan: SLIM → AutoDocs

## Summary
- Hero section: Remove 4 corners, update logo/tagline
- Registry: Import 17 external entries, clear 16 local entries
- Marketplace: Clear local folders (fresh start)
- Pages: Generate contribute, FAQ, about from templates
- Configuration: Update 3 files (docusaurus.config.js, package.json, etc.)
- Build: Validate with iterative build loop

## Changes by Section

### 1. Hero Section Modifications
| Component | Current | New | Risk |
|-----------|---------|-----|------|
| Logo | /img/logo.svg | Auto-generate (Phosphor: "file-doc") | Low |
| Tagline | "Modernizing software..." | "AI-powered documentation..." | Low |
| Corner features | 4 sidebars (top-left, bottom-left, top-right, bottom-right) | REMOVED | Medium |
| Corner CSS | ~175 lines (custom.css lines 501-675) | REMOVED | Low |
| Center layout | Logo, tagline, 3 buttons, search | PRESERVED | Low |

### 2. Registry & Marketplace Changes
| Action | Details | Count | Risk |
|--------|---------|-------|------|
| Import external | NASA-AMMOS/slim | 17 entries | Low |
| Transform names | "slim-*" → "autodocs-*" | 17 renamed | Low |
| Mark as external | Add external_only: true + repository.url | 17 marked | Low |
| Clear local registry | Remove all local entries | 16 removed | High |
| Clear marketplace folders | Delete skills/, agents/, mcp-servers/ contents | 16 folders | High |

**Note**: Existing `generate-claude-marketplace.js` already handles `external_only: true` entries correctly (lines 40-56, 86-103, 129-147). No build script changes needed.

### 3. Page Template Generation
| Page | Template | Customizations | Risk |
|------|----------|----------------|------|
| docs/contribute/submit-best-practice.md | Contribution workflow | AutoDocs specifics, GitHub links | Low |
| docs/faq/README.md | Standard Q&A | Project description, use cases | Low |
| docs/about/README.md | Project overview | Purpose, team info, features | Low |

### 4. Configuration Updates
| File | Changes | Risk |
|------|---------|------|
| docusaurus.config.js | title: "AutoDocs", tagline, url, baseUrl | High |
| package.json | name: "autodocs-website", description | Medium |
| README.md (if exists) | Update project references | Low |

### 5. Empty Marketplace Handling
| Component | Changes | Risk |
|-----------|---------|------|
| SkillBrowser.js | Add empty state check + friendly message | Low |
| src/components/ | Empty state component (if allItems.length === 0) | Low |

### 6. Build Validation
| Step | Details | Risk |
|------|---------|------|
| npm run build | Iterative loop (max 5 attempts) | Medium |
| Auto-fix errors | Import paths, syntax, config issues | Medium |
| Final validation | Ensure clean build | Low |

## Git Strategy
- Branch: rebrand/website-slim-to-autodocs
- Commits: 6 incremental commits
  1. Rebrand: Update hero section (remove corners, update branding)
  2. Rebrand: Update registry and marketplace (import external entries)
  3. Rebrand: Generate page templates (contribute, FAQ, about)
  4. Rebrand: Update configuration files
  5. Rebrand: Handle empty marketplace in SkillBrowser
  6. Rebrand: Fix build errors (if any, iterative fixes)

## Risk Assessment
- High Risk: 2 items (clear local registry, clear marketplace folders)
- Medium Risk: 4 items (corner removal, config updates, build validation)
- Low Risk: 12 items

## Rollback Plan
```bash
git checkout main
git branch -D rebrand/website-slim-to-autodocs
```
All changes are isolated on branch. Easy to discard if needed.

## Success Criteria
✓ Hero displays without corner sidebars
✓ Logo and tagline updated (or auto-generated)
✓ Registry contains 17 external entries (autodocs-* prefix)
✓ Marketplace folders empty (or only external references)
✓ Pages render correctly (contribute, FAQ, about)
✓ Build succeeds: npm run build
✓ Empty marketplace shows friendly UI message
```

**After creating the plan**: **Review and approve this plan before proceeding (yes/no/modify)**

---

### Step 5: Plan Approval

**Review the plan and provide explicit approval:**

**Options**:
1. **"yes"** - Approve and proceed with rebranding
2. **"no"** - Cancel the operation
3. **"modify"** - Request specific changes to the plan

**If "modify"**:
- Specify what you'd like to adjust
- Options:
  - Keep certain local marketplace entries
  - Change import sources
  - Modify logo generation
  - Adjust page templates
  - Change git branch name
- Regenerate plan with changes
- Present updated plan for approval

**Only after explicit "yes" approval should you proceed to execution.**

---

### Step 6: Git Branch Creation

**Create a safe working branch:**

1. Generate branch name:
   - Auto: `rebrand/website-{old-slug}-to-{new-slug}`
   - Example: `rebrand/website-slim-to-autodocs`
   - Or use your custom branch name from questionnaire

2. Create branch:
   ```bash
   git checkout -b rebrand/website-slim-to-autodocs
   ```

3. Verify branch creation successful
4. Inform you of the branch name

**All changes will be isolated from your main branch.**

---

### Step 7: Execute Changes

**Apply changes in 6 safe, incremental sub-steps:**

#### 7.1 Hero Section Modifications

**Using hero customization guide (`assets/hero-customization-guide.md`):**

**File: `src/components/HubHero.js`**:
1. Remove lines 57-78 (cornerFeatures array definition)
2. Remove lines 83-88 (corner features mapping/rendering)
3. Update line 93 (logo path):
   - If user uploaded logo: `/img/autodocs-logo.svg`
   - If auto-generated: `/img/logo.svg` (will be replaced with Phosphor icon)
4. Update lines 96-98 (tagline text):
   ```jsx
   <p style={{ padding: "15px", fontSize: "1.1rem", paddingBottom: "30px" }}>
     AI-powered documentation automation for software projects.
   </p>
   ```

**File: `src/css/custom.css`**:
1. Remove corner feature styles (estimated lines 501-675)
   - Remove `.corner-feature` class
   - Remove `.corner-top-left`, `.corner-bottom-left`, etc.
   - Remove associated media queries

**Logo Handling**:
- **If user uploaded**: Copy to `static/img/`
- **If auto-generate**:
  - Use Phosphor Icons Guide (`assets/phosphor-icons-guide.md`)
  - Extract keywords from project name: "AutoDocs" → "file-doc" or "files"
  - Fetch SVG from Phosphor CDN: `https://unpkg.com/@phosphor-icons/web@2.0.3/src/regular/file-doc.svg`
  - Save as `static/img/logo.svg`
  - Generate favicon from SVG

**Validation**:
- Verify JSX syntax (HubHero.js)
- Verify CSS syntax (custom.css)
- Verify logo file exists

**Commit**: `"Rebrand: Update hero section (remove corners, update branding)"`

---

#### 7.2 Registry & Marketplace Updates

**Using registry import guide (`assets/registry-import-guide.md`):**

**If importing external registries**:

1. **Fetch & Transform** (already done in Step 3):
   - Use transformed entries from discovery phase
   - Entries already have `external_only: true` and `repository.url`

2. **Clear Local Entries** (if "keep existing" = no):
   - Empty `static/marketplace/skills/` (except `.gitkeep`)
   - Empty `static/marketplace/agents/` (except `.gitkeep`)
   - Empty `static/marketplace/mcp-servers/` (except `.gitkeep`)
   - Or: Create `.gitkeep` files if they don't exist

3. **Write New Registry**:
   - Write `static/data/registry.json` with:
     - Imported external entries (with external_only: true)
     - Or empty arrays if no imports
     ```json
     {
       "skills": [...imported and transformed...],
       "agents": [...imported and transformed...],
       "mcp": [...imported and transformed...]
     }
     ```

**If NOT importing** (fresh start):
- Write empty registry:
  ```json
  {
    "skills": [],
    "agents": [],
    "mcp": []
  }
  ```
- Clear marketplace folders

**Validation**:
- Verify registry.json is valid JSON
- Verify all `skill_file_url` in external entries are accessible (if network available)
- Verify marketplace folders are empty or have .gitkeep

**Commit**: `"Rebrand: Update registry and marketplace (import external entries)" `

**Note**: The existing `generate-claude-marketplace.js` already handles `external_only: true` entries (lines 40-56 for skills, 86-103 for agents, 129-147 for MCPs). It will:
- Skip external entries when building local marketplace.json
- Show appropriate install instructions in UI
- No changes to build script needed!

---

#### 7.3 Page Template Generation

**Using page template guide (`assets/page-template-guide.md`):**

**File 1: `docs/contribute/submit-best-practice.md`**:

Generate from template with substitutions:
- `{PROJECT_NAME}` → "AutoDocs"
- `{GITHUB_ISSUES_URL}` → inferred from repository or asked
- `{GITHUB_DISCUSSIONS_URL}` → inferred or asked
- `{CUSTOM_RESOURCES}` → from user's "project purpose" input

Example output:
```markdown
---
sidebar_position: 1
---

# Submit a Best Practice

Want to share your expertise with the AutoDocs community? Here's how to contribute.

## Quick Start

**3 simple steps:**

1. **Create an issue** - [Start here](https://github.com/autodocs/autodocs/issues) to discuss your idea
2. **Build your contribution** - Create a skill, agent, or guide
3. **Submit a pull request** - We'll review and help you merge it

[... rest of template ...]
```

**File 2: `docs/faq/README.md`**:

Generate from template with substitutions:
- `{PROJECT_NAME}` → "AutoDocs"
- `{PROJECT_DESCRIPTION}` → from user's "project purpose" input
- `{USE_CASES}` → inferred from project purpose
- `{PREREQUISITES}` → "Node.js, npm, basic command line knowledge"
- `{CUSTOM_FAQ}` → additional Q&A if provided

**File 3: `docs/about/README.md`**:

Generate from template with substitutions:
- `{PROJECT_NAME}` → "AutoDocs"
- `{TAGLINE}` → "AI-powered documentation automation..."
- `{PROJECT_DESCRIPTION}` → from user input
- `{FEATURES}` → inferred or from user input ("1. Automatic README generation", "2. API docs from code", etc.)
- `{TEAM_INFO}` → from user's "organization" input
- `{RESOURCES}` → inferred (GitHub, docs site, etc.)

**Validation**:
- Verify markdown syntax
- Verify frontmatter is correct
- Verify all internal links are valid
- Verify placeholders are replaced

**Commit**: `"Rebrand: Generate page templates (contribute, FAQ, about)"`

---

#### 7.4 Configuration Updates

**File 1: `docusaurus.config.js`**:

Update configuration object:
```javascript
{
  title: 'AutoDocs',  // was 'SLIM'
  tagline: 'AI-powered documentation automation for software projects',
  url: 'https://autodocs-team.github.io',  // prompt user or infer
  baseUrl: '/autodocs/',  // infer from project name
  organizationName: 'autodocs-team',  // from user input
  projectName: 'autodocs',  // from user input
  // ... rest preserved
}
```

**File 2: `package.json`**:

Update fields:
```json
{
  "name": "autodocs-website",
  "description": "AutoDocs documentation website and best practices hub",
  "homepage": "https://autodocs-team.github.io/autodocs",
  // ... rest preserved
}
```

**File 3: `README.md` (if exists)**:

Replace "SLIM" references with "AutoDocs" using intelligent text replacement:
- Whole-word matching (avoid partial matches)
- Preserve case patterns (SLIM → AUTODOCS, Slim → AutoDocs, slim → autodocs)
- Update links and URLs

**Validation**:
- Verify JavaScript syntax (docusaurus.config.js)
- Verify JSON syntax (package.json)
- Verify URLs are well-formed
- Verify markdown syntax (README.md)

**Commit**: `"Rebrand: Update configuration files"`

---

#### 7.5 Empty Marketplace Handling

**Using empty marketplace guide (`assets/empty-marketplace-guide.md`):**

**File: `src/components/SkillBrowser.js`**:

Add empty state handling after data loading (around line 970-1000):

```javascript
// After loading registry data
if (allItems.length === 0) {
  return (
    <Container className="mt-5">
      <Card className="text-center p-5 shadow-sm">
        <Card.Body>
          <div style={{ fontSize: "4rem", marginBottom: "1rem" }}>
            📦
          </div>
          <h3>No best practices available yet</h3>
          <p className="text-muted mb-4" style={{ maxWidth: "500px", margin: "0 auto 1.5rem" }}>
            Get started by importing from other SLIM instances or creating your own!
          </p>
          <div>
            <Button
              variant="primary"
              onClick={() => window.location.href = '/docs/contribute/submit-best-practice'}
              className="me-2"
            >
              Learn How to Contribute
            </Button>
            <Button
              variant="outline-secondary"
              onClick={() => window.location.href = '/docs/about'}
            >
              About {PROJECT_NAME}
            </Button>
          </div>
        </Card.Body>
      </Card>
    </Container>
  );
}

// ... rest of SkillBrowser component
```

**Validation**:
- Verify React/JSX syntax
- Verify links are correct (`/docs/contribute/submit-best-practice`, `/docs/about`)
- Test rendering (if possible)

**Commit**: `"Rebrand: Handle empty marketplace in SkillBrowser"`

**Note**: The existing `generate-claude-marketplace.js` already handles empty arrays gracefully. It will generate valid `marketplace.json` with empty plugins array if no local entries exist.

---

#### 7.6 Build Validation (Iterative Loop)

**Using linter validation guide (`assets/linter-validation-guide.md`):**

**A. Pre-Build Linting**:

1. **JSON Validation**:
   ```bash
   node -e "JSON.parse(require('fs').readFileSync('static/data/registry.json', 'utf8'))"
   ```

2. **JavaScript/React Validation**:
   - If ESLint detected: `npx eslint src/components/HubHero.js src/components/SkillBrowser.js`
   - Auto-fix if possible: `npx eslint --fix`

3. **CSS Validation**:
   - Basic syntax check on custom.css

**B. Iterative Build Loop** (max 5 attempts):

```
Attempt 1:
  Run: npm run build

  If SUCCEEDS → DONE, proceed to validation report

  If FAILS:
    1. Parse error output:
       - Import errors (broken paths)
       - React syntax errors
       - Missing dependencies
       - CSS errors
       - Config errors

    2. Attempt automatic fixes:
       - Fix import paths in modified files
       - Update component props if needed
       - Fix JSX syntax errors
       - Restore configs if corrupted

    3. Commit fixes: "Rebrand: Fix build errors (attempt 1)"

    4. Retry → Attempt 2

Attempt 2-5: Repeat process

If max attempts reached (5) and still failing:
  - Present errors to user with context
  - Provide manual fix guidance
  - Ask: "Continue despite build failures? (yes/no)"
  - If yes → proceed with warnings
  - If no → pause for manual intervention
```

**Example Execution**:
```
Attempt 1: Running build...
✓ Build successful (npm run build - 35s)
  No errors detected
```

Or:
```
Attempt 1: Running build...
❌ Build failed: Cannot resolve './components/CornerFeature' in HubHero.js
   → Auto-fixing: Removed orphaned import statement
   ✓ Committed fixes

Attempt 2: Running build...
✓ Build successful (npm run build - 38s)
  Loop complete after 2 attempts
```

**C. Validation Report**:
```
Validation Results
==================
✓ All JSON files valid (1 file: registry.json)
✓ React components valid (2 files modified)
✓ CSS files valid (1 file: custom.css)
✓ Build successful after 2 attempts (npm run build - 38s)
  - Attempt 1: Fixed orphaned import (1 file)
  - Attempt 2: Build succeeded

Status: PASS
Build Loop: 2 iterations, all errors auto-resolved
```

**If build succeeds**: Continue to Step 9

**If build fails after 5 attempts**: Present errors and ask for user decision

---

### Step 8: Validation & Testing

**Covered by Step 7.6 - Build Validation**

All validation happens as part of the iterative build loop. This step number is preserved for consistency with the original workflow structure.

---

### Step 9: Summary Report

**Generate a comprehensive completion report:**

```markdown
# SLIM Website Rebranding Complete: SLIM → AutoDocs

## Summary
✓ 18 files modified
✓ 6 commits created
✓ All validation checks passed
✓ Branch: rebrand/website-slim-to-autodocs

## Changes Applied

### Hero Section
- Removed: 4 corner sidebars (lines 57-78, 83-88 in HubHero.js)
- Removed: ~175 lines of corner CSS (custom.css)
- Updated: Logo (auto-generated from Phosphor: "file-doc")
- Updated: Tagline ("AI-powered documentation automation for software projects")
- Preserved: Center layout (logo, tagline, buttons, search)

### Registry & Marketplace
- Imported: 17 entries from NASA-AMMOS/slim
  - 14 skills: autodocs-readme, autodocs-license, autodocs-changelog, ...
  - 2 agents: autodocs-rebranding-agent, autodocs-website-maker-agent
  - 1 MCP: autodocs-github-mcp-server
- Transformed: All entries marked with external_only: true
- Repository links: All point to https://github.com/NASA-AMMOS/slim
- Cleared: Local marketplace folders (fresh start)
- New registry: 17 external entries, 0 local entries

### Page Templates
- Generated: docs/contribute/submit-best-practice.md (AutoDocs contribution workflow)
- Generated: docs/faq/README.md (AutoDocs Q&A with domain-specific content)
- Generated: docs/about/README.md (AutoDocs overview with team info)

### Configuration
- Updated: docusaurus.config.js (title: "AutoDocs", tagline, url, baseUrl)
- Updated: package.json (name: "autodocs-website", description)
- Updated: README.md (SLIM → AutoDocs references)

### Empty Marketplace Handling
- Added: Empty state component in SkillBrowser.js
- Renders: Friendly message when allItems.length === 0
- Provides: "Learn How to Contribute" and "About AutoDocs" buttons

### Build Validation
✓ Build successful after 2 attempts (npm run build - 38s)
  - Attempt 1: Fixed orphaned import (1 file)
  - Attempt 2: Build succeeded
✓ All linters passed
✓ No warnings or errors

## Git Information
Branch: rebrand/website-slim-to-autodocs
Status: Clean (all committed)
Commits:
1. Rebrand: Update hero section (remove corners, update branding)
2. Rebrand: Update registry and marketplace (import external entries)
3. Rebrand: Generate page templates (contribute, FAQ, about)
4. Rebrand: Update configuration files
5. Rebrand: Handle empty marketplace in SkillBrowser
6. Rebrand: Fix build errors (attempt 1)

## Next Steps

### 1. Review Changes Locally
```bash
cd /path/to/rebrand-agent
git diff main...rebrand/website-slim-to-autodocs
```

### 2. Test Website Locally
```bash
npm start
# Preview at http://localhost:3000/autodocs/
```

**Test Checklist**:
- ✓ Hero section displays without corner sidebars
- ✓ Logo and tagline are updated
- ✓ Marketplace shows 17 imported entries (if any)
- ✓ Empty marketplace shows friendly message (if applicable)
- ✓ All pages render: contribute, FAQ, about
- ✓ Navigation works
- ✓ Search functions correctly
- ✓ External entries show correct install instructions

### 3. Deploy Preview (Optional)
Enable GitHub Pages on your fork:
```
Settings → Pages → Source: gh-pages branch
Preview: https://autodocs-team.github.io/autodocs/
```

### 4. Create Pull Request
```bash
gh pr create \
  --title "Rebrand: SLIM → AutoDocs" \
  --body "Complete SLIM website rebrand including hero, registry, and page templates.\n\nSee commits for detailed changes."
```

### 5. Merge to Main
After testing and approval:
```bash
git checkout main
git merge rebrand/website-slim-to-autodocs
git push origin main
```

## Rollback if Needed
```bash
git checkout main
git branch -D rebrand/website-slim-to-autodocs
```

All changes are isolated on the branch and can be easily discarded.

## Support & Documentation
- AutoDocs About: /docs/about
- Contribution Guide: /docs/contribute/submit-best-practice
- FAQ: /docs/faq
- GitHub: https://github.com/autodocs-team/autodocs
```

---

### Step 10: Next Steps Prompt

**Consider if you'd like help with any next steps:**

**Question**: "Would you like help with any of the following?"

**Options**:
1. **Test the website locally** - I can guide you through running `npm start` and testing
2. **Create a pull request** - I can help create a PR using `gh` CLI
3. **Deploy to GitHub Pages** - I can help configure GitHub Pages deployment
4. **Create a new SLIM best practice** - Share your customized instance (proceeds to Step 11)
5. **None** - I'm all set, thanks!

If user selects **"Create a new SLIM best practice"** → Proceed to Step 11

Otherwise → End workflow

---

### Step 11: Create SLIM Best Practice (Optional)

**Using create-best-practice guide (`assets/create-best-practice-guide.md`):**

**Create a new SLIM best practice to share your customized instance:**

1. **Check for slim-skill-creator availability**:
   - Search for `slim-skill-creator` in installed skills
   - Or check if available in marketplace

2. **If NOT available**:
   ```
   The slim-skill-creator is not installed. Would you like to install it?

   Install with:
   /plugin install slim-skill-creator@slim-marketplace

   After installation, you can run this step again or manually invoke:
   "Help me create a new SLIM best practice for my AutoDocs website"
   ```

3. **If available**:
   ```
   Great! The slim-skill-creator is available. I'll help you create a new best practice.

   What type of best practice would you like to create?
   1. Skill - A reusable workflow or template
   2. Agent - An autonomous multi-step process
   3. MCP Server - Integration with external services

   Recommended: "Agent" - to share your complete SLIM website rebanding workflow
   ```

4. **Invoke slim-skill-creator**:
   - If user selects "Agent":
     ```
     I'm invoking the slim-skill-creator to create a new agent best practice
     for your AutoDocs customized SLIM instance.

     Context being provided:
     - Type: Agent
     - Name: autodocs-website-template
     - Description: Customized SLIM instance for documentation automation
     - Base: Your rebranded website at rebrand/website-slim-to-autodocs
     - Registry: 17 imported best practices
     - Documentation: Custom contribute, FAQ, about pages

     The slim-skill-creator will now guide you through the rest of the process...
     ```
   - Hand off to slim-skill-creator with context

5. **If user declines**:
   ```
   No problem! You can create a best practice later by running:

   /plugin install slim-skill-creator@slim-marketplace

   Then: "Help me create a new SLIM best practice"
   ```

**End of workflow**

---

## Best Practices

### For Users

1. **Start with a clean git state** - Commit or stash changes before rebranding
2. **Test locally first** - Always run `npm start` and test thoroughly before deploying
3. **Review the plan carefully** - Understand what will be changed, especially high-risk items
4. **Keep backups** - The git branch isolation provides rollback capability
5. **Customize page templates** - After generation, edit contribute/FAQ/about to your specific needs
6. **Import selectively** - You can import from multiple SLIM instances and cherry-pick entries
7. **Start fresh** - For most forks, starting with an empty marketplace is cleaner than keeping all SLIM entries

### For Implementation

1. **Always validate before committing** - Never commit broken JSON, JSX, or CSS
2. **Leverage existing infrastructure** - Use `external_only: true` support already in codebase
3. **Provide helpful error messages** - Guide users to fix issues if auto-fix fails
4. **Preserve user work** - Never delete uncommitted changes
5. **Test external URLs** - Verify `skill_file_url` accessibility before trusting imports
6. **Handle edge cases** - Empty marketplace, no imports, missing logo, etc.
7. **Iterative build loop** - Keep trying to fix build errors up to 5 attempts

---

## Troubleshooting

### Common Issues

**Q: Build fails after rebranding**
A: Check the build error output. Common causes:
- Orphaned import statements (removed components)
- Incorrect file paths
- Syntax errors in modified files
- Use the iterative build loop to auto-fix these (up to 5 attempts)

**Q: External registry import fails**
A: Check:
- GitHub URL is correct and accessible
- Registry.json exists at `static/data/registry.json` in target repo
- Network connection is stable
- The workflow will skip failed imports and continue

**Q: Logo doesn't generate correctly**
A: The agent uses Phosphor Icons. If auto-generation fails:
- Upload your own logo file
- Or manually place logo in `static/img/logo.svg` after rebranding
- Supported formats: SVG, PNG

**Q: Empty marketplace shows error instead of friendly message**
A: Verify:
- SkillBrowser.js has the empty state component
- registry.json is valid JSON (even if empty arrays)
- Build succeeded without errors

**Q: Want to keep some local entries while importing**
A: When asked "Keep existing marketplace entries?" say "yes"
- The agent will merge imported + existing
- Deduplication by name (imported takes precedence)

---

## Asset Files Reference

This agent uses 6 asset files for detailed instructions:

1. **slim-website-questionnaire.md** - SLIM-specific rebranding questions
2. **registry-import-guide.md** - External registry fetch/transform logic with `external_only: true` examples
3. **hero-customization-guide.md** - HubHero.js and CSS modification instructions
4. **page-template-guide.md** - Templates for contribute, FAQ, and about pages
5. **empty-marketplace-guide.md** - SkillBrowser.js empty state handling
6. **create-best-practice-guide.md** - Step 11 slim-skill-creator integration instructions

All asset files are located in `assets/` directory relative to this AGENT.md file.

---

## Version History

- **v2.0.0** (2025-01-05): Refactored to focus on SLIM website rebranding specifically
  - Added hero customization (remove corner sidebars)
  - Added registry import from external SLIM instances
  - Added page template generation (contribute, FAQ, about)
  - Added empty marketplace handling
  - Added slim-skill-creator integration (Step 11)
  - Leverages existing `external_only: true` support in codebase
  - 11-step workflow tailored to SLIM/Docusaurus websites

- **v1.0.0** (2024-??-??): Original general-purpose rebranding agent
  - Universal compatibility (any codebase)
  - 10-step workflow
  - Phosphor Icons integration
  - Iterative build validation

---

## License

This agent is part of the SLIM (Software Lifecycle Improvement & Modernization) project.

See repository LICENSE file for details.

---

## Contributing

Found a bug or have a suggestion? Create an issue or submit a pull request!

See `docs/contribute/submit-best-practice.md` after rebranding for contribution guidelines.
