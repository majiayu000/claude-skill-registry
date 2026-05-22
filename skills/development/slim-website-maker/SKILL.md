---
name: slim-website-maker
description: Autonomous website generator skill for creating customized Docusaurus documentation websites. Analyzes project content, generates intelligent website structure, and validates changes with iterative build testing until successful. Creates git branch and commits with clear messages. Auto-detects project type and customizes accordingly. Use when generating project documentation websites, creating content-driven sites, or automating website creation with build validation.
---

# SLIM Project Website Maker

## Overview

The SLIM Project Website Maker Skill is a comprehensive, semi-autonomous tool designed to generate professional Docusaurus documentation websites for any project. It analyzes your project content, creates intelligent customizations, and validates the website with iterative build testing to ensure everything works correctly.

**Key Features**:
- 🌐 **Universal Compatibility**: Works with any project type (Node, Python, Java, C++, Rust, Go, etc.)
- 🤖 **AI-Powered Analysis**: Understands project structure, purpose, and features from code and documentation
- ✅ **Iterative Build Validation**: Continuously builds and fixes errors until successful
- 🎨 **Smart Customization**: Generates project-specific content, navigation, and structure
- 🔒 **Git Safety**: Creates isolated branch, incremental commits, easy rollback
- 📋 **Semi-Autonomous**: Presents plan for approval before execution

## When to Use

- Creating documentation websites for software projects
- Generating professional project websites automatically
- Building content-driven sites based on existing materials
- Setting up Docusaurus websites with intelligent customization
- Preparing documentation for project launches or releases

## Dependencies

**None** - This skill works standalone with any project. No marketplace dependencies required.

## Prerequisites

- Git repository initialized
- Node.js and yarn installed
- Write access to project files
- Clean working directory (recommended)
- Optional: Source directory with project materials to analyze

## Interactive Workflow

### Step 1: Context Gathering

**I will verify your project setup and gather requirements:**

1. **Git Repository Check**:
   - Verify git repository exists
   - Check working directory status
   - Warn if there are uncommitted changes

2. **Destination Directory**:
   - Ask: "Where would you like me to create your website? Please provide the destination directory path."
   - Validate directory can be created
   - Check for existing content conflicts

3. **Source Content Analysis** (optional):
   - Ask: "Do you have a source directory containing project materials (code, documentation, PDFs, etc.) that I should analyze to customize your website? If yes, provide the path. Otherwise, I'll create a basic template for manual customization."
   - If provided, verify source directory exists and contains analyzable content

---

### Step 2: Project Analysis

**I will analyze your project to understand its purpose and structure:**

**When source directory is provided:**

1. **Content Discovery**:
   - Scan for README files, documentation, code files
   - Identify configuration files (package.json, requirements.txt, Cargo.toml, etc.)
   - Find existing documentation structure
   - Locate PDF documents and other materials

2. **Project Understanding**:
   - **Project name and purpose**: Extract from README, package.json, or other sources
   - **Key features**: Identify main functionalities and capabilities
   - **Target audience**: Determine if developer-focused, end-user, research, etc.
   - **Technology stack**: Programming languages, frameworks, dependencies
   - **Documentation patterns**: Current organization and content themes
   - **Project maturity**: Development stage and readiness

3. **Analysis Report**:
   - Present findings summary
   - Show discovered project metadata
   - List key features and capabilities found
   - Display proposed website structure

**When no source directory is provided:**
- Note that basic template will be created
- User will handle manual customization after setup

After analysis, I'll ask: **"Proceed with website generation plan? (yes/no)"**

---

### Step 3: Plan Generation

**I will generate a comprehensive website creation plan:**

Using the website-generation-plan template (`assets/website-generation-plan.md`), I'll create a plan showing:

**Plan Structure**:
```markdown
# Website Generation Plan: [Project Name]

## Summary
- Destination: [path]
- Source analysis: [Performed / Skipped]
- Project type: [Detected type(s)]
- Customization level: [AI-generated / Basic template]

## Website Structure

### Homepage
- Title: [Project Name]
- Description: [AI-generated summary]
- Key features: [List of highlights]

### Documentation Sections
| Section | Content | Source |
|---------|---------|--------|
| Getting Started | Installation, quick start | README analysis |
| User Guide | Usage patterns | Code analysis |
| Developer Docs | API, contributing | Project structure |
| ... | ... | ... |

### Navigation Configuration
- Main menu items: [List]
- Footer links: [List]
- Categories: [List]

## Customizations Applied
- Content population: [Details]
- Structure organization: [Details]
- Styling and branding: [Details]

## Git Strategy
Branch: website/[project-name]-docusaurus
Commits: 4 (setup, customization, content, validation)

## Build Validation Plan
1. Initial build test
2. Error detection and auto-fix loop (max 5 attempts)
3. Success confirmation

## Rollback Plan
git checkout main && git branch -D website/[branch-name]
```

---

### Step 4: Plan Approval

**I will present the plan and wait for your approval:**

**Options**:
1. **"yes"** - Approve and proceed with website generation
2. **"no"** - Cancel the operation
3. **"modify"** - Request specific changes to the plan

**If "modify"**:
- I'll ask what you'd like to adjust
- Options: change destination, modify structure, adjust customizations, change git branch name
- Regenerate plan with changes
- Present updated plan for approval

**Only after explicit "yes" approval will I proceed to execution.**

---

### Step 5: Git Branch Creation

**I will create a safe working branch:**

1. Generate branch name:
   - Auto: `website/[project-slug]-docusaurus`
   - Or use your custom branch name if provided

2. Create branch:
   ```bash
   git checkout -b website/project-name-docusaurus
   ```

3. Verify branch creation successful
4. Inform you of the branch name

**All changes will be isolated from your main branch.**

---

### Step 6: Template Setup

**I will clone and initialize the Docusaurus template:**

#### 6.1 Clone Template
```bash
git clone https://github.com/NASA-AMMOS/slim-docsite-template.git [destination-directory]
cd [destination-directory]
```

#### 6.2 Clean Git History
```bash
# Remove original git history
rm -rf .git

# Initialize fresh git repository
git init
git add .
git commit -m "Initial commit: Docusaurus template"
```

#### 6.3 Install Dependencies
```bash
yarn install
```

**Commit**: `"Website: Initialize Docusaurus template"`

---

### Step 7: Content Customization

**I will apply AI-generated customizations based on project analysis:**

#### 7.1 Homepage Customization
Using homepage-customization-guide (`assets/homepage-customization-guide.md`):

- Update `src/pages/index.js`:
  - Replace title with discovered project name
  - Generate project summary from analysis
  - Create feature highlights from identified capabilities
  - Customize hero section with project-specific messaging

**Commit**: `"Website: Customize homepage with project details"`

#### 7.2 Documentation Structure
Using docs-structure-guide (`assets/docs-structure-guide.md`):

- Organize `docs/` directory:
  - Create logical section hierarchy based on project structure
  - Generate Getting Started guide from README analysis
  - Create User Guide sections from usage patterns
  - Set up Developer Documentation if applicable
  - Generate placeholder content for identified gaps

- Populate content:
  - Extract and adapt existing documentation
  - Generate introductory content for each section
  - Create navigation-friendly structure
  - Ensure proper linking and references

**Commit**: `"Website: Create documentation structure and content"`

#### 7.3 Configuration Updates
Using config-customization-guide (`assets/config-customization-guide.md`):

- Update `docusaurus.config.js`:
  - Set site metadata (title, tagline, description)
  - Configure URL and base path
  - Set up navigation menus based on structure
  - Configure footer with project information
  - Add GitHub/repository links if found
  - Configure search if applicable

- Update `src/css/custom.css`:
  - Adjust color scheme if brand colors found
  - Customize typography if needed
  - Apply project-specific styling

**Commit**: `"Website: Configure site metadata and navigation"`

---

### Step 8: Validation with Iterative Build Loop

**I will run comprehensive build validation using build-validation-guide (`assets/build-validation-guide.md`):**

**CRITICAL: I will loop over the build process until it succeeds.**

#### Build Loop Algorithm:

```
START BUILD VALIDATION LOOP:

Loop (max 5 attempts):
  a. Run build command:
     yarn build

  b. If build SUCCEEDS → BREAK LOOP, continue to finalization

  c. If build FAILS:
     i.   Parse error output to identify issues:
          - Dependency errors (missing packages)
          - Configuration syntax errors (docusaurus.config.js)
          - Content errors (broken MDX, invalid frontmatter)
          - Path errors (broken links, missing files)
          - React component errors
          - Plugin configuration issues

     ii.  Attempt automatic fixes:
          - Install missing dependencies
          - Fix configuration syntax
          - Repair MDX syntax errors
          - Update broken links and paths
          - Fix React component issues
          - Adjust plugin configurations
          - Revert problematic customizations if needed

     iii. Commit fixes: "Website: Fix build errors (attempt N)"

     iv.  Re-run build (next loop iteration)

  d. If max attempts reached (5) and still failing:
     - Present errors to user
     - Provide manual fix guidance
     - Ask: "Continue despite build failures? (yes/no)"
     - If yes → proceed with warnings
     - If no → pause for manual intervention

END LOOP
```

**Example Build Loop Execution:**

```
Attempt 1: Running yarn build...
❌ Build failed: Module not found: '@docusaurus/plugin-content-docs'
   → Installing missing dependencies...
   → Running yarn install...
   ✓ Committed fixes

Attempt 2: Running yarn build...
❌ Build failed: Invalid frontmatter in docs/intro.md
   → Fixing MDX syntax errors...
   → Corrected frontmatter format
   ✓ Committed fixes

Attempt 3: Running yarn build...
❌ Build failed: Broken link to /docs/nonexistent
   → Fixing broken links...
   → Updated 3 documentation links
   ✓ Committed fixes

Attempt 4: Running yarn build...
✓ Build successful (yarn build - 45s)
   Loop complete after 4 attempts
```

#### Validation Report
```
Build Validation Results
========================
✓ Template cloned successfully
✓ Dependencies installed
✓ Build successful after 4 attempts (yarn build - 45s)
  - Attempt 1: Installed missing dependencies
  - Attempt 2: Fixed MDX syntax errors
  - Attempt 3: Fixed broken links
  - Attempt 4: Build succeeded

✓ Development server tested (http://localhost:3000)
✓ All navigation links working
✓ Content renders correctly

Status: PASS
Build Loop: 4 iterations, all errors auto-resolved
```

**If build succeeds**: Continue to finalization

**If build fails after 5 attempts**: Present errors and ask for user decision

After validation, I'll ask: **"Proceed to finalization? (yes/no)"**

---

### Step 9: Local Testing

**I will start the development server for verification:**

```bash
yarn start
```

**Testing Checklist:**
- ✓ Website loads at http://localhost:3000
- ✓ Homepage displays correctly
- ✓ Navigation menus work
- ✓ Documentation pages load
- ✓ Links and cross-references function
- ✓ Search works (if enabled)
- ✓ Responsive design verified

**I will inform you when the development server is ready for your review.**

---

### Step 10: Summary Report

**I will generate a comprehensive completion report:**

Using example-website-report (`assets/example-website-report.md`):

```markdown
# Website Generation Complete: [Project Name]

## Summary
✓ Docusaurus website created successfully
✓ 4 commits created
✓ All build validation checks passed
✓ Branch: website/project-name-docusaurus
✓ Development server running at http://localhost:3000

## Website Details
- **Destination**: [path]
- **Template**: NASA-AMMOS/slim-docsite-template
- **Customization**: AI-generated from project analysis
- **Documentation sections**: [count]
- **Pages created**: [count]

## Changes Applied
- Homepage: Customized with project-specific content
- Documentation: [count] sections organized
- Navigation: [count] menu items configured
- Styling: Project-appropriate theming applied

## Build Validation Results
✓ Build successful (yarn build)
✓ Development server tested
⚠ Warnings: [list or "None"]

## Git Information
Branch: website/project-name-docusaurus
Status: Clean (all committed)
Commits: 4 total

## Next Steps
1. Review website: http://localhost:3000
2. Customize content further if needed
3. Test all features and links
4. Set up deployment:
   - GitHub Pages (recommended)
   - Netlify, Vercel, or other platform
5. Create PR to merge to main branch

## Deployment Options

### GitHub Pages (Recommended)
```bash
# Push to GitHub
git remote add origin https://github.com/[username]/[repo].git
git push -u origin website/project-name-docusaurus

# Configure in GitHub Settings → Pages → GitHub Actions
# Pre-configured workflow will auto-deploy on merge to main
```

### Manual Deployment
```bash
# Build production bundle
yarn build

# Deploy to hosting provider
# Copy build/ directory to web server
```

## Rollback if needed
```bash
git checkout main
git branch -D website/project-name-docusaurus
```
```

**Final question**: **"Would you like help setting up deployment? (yes/no)"**

---

## Best Practices

### For Users
1. **Review generated content** - Verify accuracy of AI-generated descriptions
2. **Test thoroughly** - Check all links, navigation, and features
3. **Customize further** - Add project-specific details, branding, and content
4. **Set up deployment** - Use GitHub Pages or other hosting platform
5. **Maintain regularly** - Update documentation as project evolves

### For Safety
1. **Use git branches** - Never generate directly on main/master
2. **Commit recent work** - Ensure clean state before generation
3. **Review plan carefully** - Understand customizations before approval
4. **Test locally first** - Verify everything works before deploying

---

## FAQ

**Q: What if I don't have project materials to analyze?**
A: No problem! The skill will create a basic Docusaurus template that you can customize manually with guidance.

**Q: Can I customize the website after it's generated?**
A: Absolutely! The generated website is a standard Docusaurus project that you can fully customize.

**Q: What if the build fails after 5 attempts?**
A: The skill will present the errors and provide guidance for manual fixes. You can then continue or pause for intervention.

**Q: Can I use this for non-technical projects?**
A: Yes! The skill works with any type of project content, including business, research, creative, and educational materials.

**Q: How do I deploy the website?**
A: The skill provides deployment guidance. GitHub Pages is recommended and pre-configured via GitHub Actions workflow.

**Q: What if I want to undo the website generation?**
A: All changes are on a git branch. Simply:
```bash
git checkout main
git branch -D website/[branch-name]
```

**Q: Can I regenerate the website later?**
A: Yes! Run the skill again with updated source materials to regenerate with new content.

---

## Troubleshooting

**Issue: Git branch creation fails**
- **Cause**: Uncommitted changes or dirty working directory
- **Solution**:
  ```bash
  git status  # Check status
  git add . && git commit -m "Save work before website generation"
  ```

**Issue: Template clone fails**
- **Cause**: Network issues or GitHub access problems
- **Solution**: Check internet connection and GitHub repository accessibility

**Issue: Yarn install fails**
- **Cause**: Node.js or yarn not installed, or version incompatibility
- **Solution**:
  - Verify Node.js installation: `node --version`
  - Install yarn: `npm install -g yarn`
  - Check version requirements

**Issue: Build fails after generation**
- **Cause**: Customization errors or dependency issues
- **Solution**: Skill auto-fixes via build loop. If unsuccessful, check error messages and fix manually.

**Issue: Development server won't start**
- **Cause**: Port conflict (default: 3000) or dependency issues
- **Solution**:
  - Check port availability
  - Try different port: `yarn start --port 3001`
  - Reinstall dependencies: `rm -rf node_modules && yarn install`

**Issue: Broken links or missing pages**
- **Cause**: Content structure mismatch or incorrect paths
- **Solution**: Skill detects and fixes during build loop. Review navigation configuration if issues persist.

**Issue: Deployment fails**
- **Cause**: Configuration errors or GitHub Pages settings
- **Solution**:
  - Verify `docusaurus.config.js` URL and baseUrl settings
  - Check GitHub repository settings for Pages
  - Review workflow permissions

---

## Advanced Tips

### Partial Generation
To customize only specific parts:
1. Review plan carefully before approval
2. Request modifications to adjust scope
3. Example: "Only customize homepage, leave docs as template"

### Staged Customization
For complex projects, customize in stages:
1. Stage 1: Basic structure and homepage
2. Stage 2: Documentation content
3. Stage 3: Advanced features and styling

### Content Updates
To update website with new project content:
1. Run skill again with updated source directory
2. Compare new generation with existing
3. Merge desired updates

### Custom Styling
To apply custom branding:
1. Provide brand guidelines in source directory
2. Skill will detect and apply where possible
3. Further customize `src/css/custom.css` after generation

---

## Asset Files

This agent uses the following instruction guides (located in `assets/`):

1. **website-generation-plan.md** - Plan format template
2. **homepage-customization-guide.md** - Homepage content generation guide
3. **docs-structure-guide.md** - Documentation organization guide
4. **config-customization-guide.md** - Configuration and navigation setup
5. **build-validation-guide.md** - Build testing and error fixing guide
6. **example-website-report.md** - Completion report example

These guides provide instructions for runtime analysis and generation, ensuring flexibility across different project types.
