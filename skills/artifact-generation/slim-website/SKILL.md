---
name: slim-website
description: AI-powered website generator that analyzes your project content and creates customized Docusaurus documentation websites. Use when you want to automatically generate a professional website based on your project's code, documentation, and other materials. Handles content analysis, template customization, and intelligent website structure generation. Can also create basic template websites without content analysis. Use for project documentation websites, content-driven sites, automated documentation generation, or when you need a professional website that reflects your project's actual content and structure.
---

# AI-Powered Website Generator

## Overview

Generate intelligent, customized Docusaurus documentation websites by analyzing your project content. This skill combines AI-powered content analysis with professional template customization to create websites that accurately reflect your project's purpose, features, and structure.

Unlike simple template cloning, this skill understands your project by analyzing code, documentation, PDFs, and other materials, then generates a tailored website with appropriate content, navigation, and organization.

## Prerequisites

- **Git**: For cloning the Docusaurus template repository
- **Node.js and yarn**: For installing dependencies and running the development server
- **Project materials** (optional): Source directory containing code, documentation, or other project files to analyze
- **GitHub account** (optional): For deployment to GitHub Pages

## Interactive Workflow

### Step 1: Gather User Requirements

Ask the user to specify their setup preferences:

**Required Question:**
"Where would you like me to create your website? Please provide the destination directory path where the Docusaurus website should be built."

**Optional Question:**
"Do you have a source directory containing project materials (code, documentation, PDFs, etc.) that I should analyze to customize your website? If yes, please provide the path. If you skip this, I'll create a basic template website for you to customize manually."

**Validation:**
- Ensure destination directory path is provided
- Verify destination directory exists or can be created
- If source directory is provided, verify it exists and contains analyzable content

### Step 2: Content Analysis Mode Selection

Based on user responses, proceed with the appropriate mode:

**Mode A: AI-Customized Website** (when source directory provided)
- Analyze source directory content
- Generate project-specific customizations
- Create tailored navigation and content structure

**Mode B: Basic Template Website** (when no source directory provided)
- Clone template repository as-is
- Provide basic customization guidance
- User handles manual customization

### Step 3: Source Content Analysis (Mode A Only)

When source directory is provided, perform comprehensive analysis:

**Content Discovery:**
1. **Scan directory structure** recursively for relevant files:
   - Code files (*.py, *.js, *.java, *.cpp, *.md, etc.)
   - Documentation files (README.md, docs/, *.txt, *.rst)
   - Configuration files (package.json, requirements.txt, Dockerfile)
   - PDF documents and other documentation materials

2. **File Type Processing:**
   - **README files**: Extract project name, description, installation instructions, usage examples
   - **Code files**: Understand technology stack, main functionality, API structure
   - **Documentation**: Identify existing documentation organization and content themes
   - **Configuration files**: Determine dependencies, build processes, deployment methods
   - **PDFs**: Extract key information about project purpose and features

**Project Understanding:**
Extract and synthesize:
- **Project name and purpose**: What does this project do?
- **Key features and capabilities**: What are the main functionalities?
- **Target audience**: Developers, end-users, researchers, etc.
- **Technology stack**: Programming languages, frameworks, dependencies
- **Documentation structure**: How is information currently organized?
- **Project maturity**: Development stage, stability, production readiness

### Step 4: Template Preparation

**Clone the Docusaurus Template:**
```bash
git clone https://github.com/NASA-AMMOS/slim-docsite-template.git [destination-directory]
cd [destination-directory]
```

**Clean and Initialize:**
```bash
# Remove original git history
rm -rf .git

# Initialize fresh git repository
git init
git add .
git commit -m "Initial commit: Docusaurus website template"

# Install dependencies
yarn install
```

### Step 5: Intelligent Customization (Mode A Only)

When content analysis was performed, customize the template based on findings:

**Homepage Customization (`src/pages/index.js`):**
- Update project title with discovered project name
- Replace template description with AI-generated project summary
- Customize hero section with project-specific messaging
- Update feature highlights based on analyzed capabilities

**Documentation Structure (`docs/` directory):**
- **Organize content** based on discovered documentation patterns
- **Create section hierarchy** matching project's logical structure
- **Generate placeholder content** for identified documentation gaps
- **Preserve existing documentation** by incorporating analyzed content

**Navigation Configuration (`docusaurus.config.js`):**
- **Update site metadata**: title, tagline, URL, organization info
- **Configure navigation menus** based on content structure
- **Set up appropriate categories** for documentation sections
- **Configure search and social links** if discoverable from source

**Content Population:**
- **API documentation**: Generate structure if code analysis reveals API patterns
- **User guides**: Create sections based on discovered usage patterns
- **Developer documentation**: Include setup and contribution guides if applicable
- **About section**: Populate with project purpose and team information

**Styling and Branding:**
- **Update colors and themes** if brand information is discoverable
- **Customize logos and icons** if assets are found in source directory
- **Adjust typography** to match project's documentation style

### Step 6: Basic Setup (Mode B - Template Only)

When no source analysis is performed:

**Provide Manual Customization Guidance:**
1. **Key files to customize:**
   - `src/pages/index.js`: Homepage content and branding
   - `docs/`: Documentation content and structure
   - `docusaurus.config.js`: Site configuration and navigation
   - `src/css/custom.css`: Styling and themes

2. **Essential customizations:**
   - Update project name, title, and description
   - Replace template content with your project information
   - Organize documentation structure for your needs
   - Customize navigation menus and categories

### Step 7: Local Testing and Validation

**Start Development Server:**
```bash
yarn start
```

**Validation Checklist:**
- Website loads correctly at `http://localhost:3000`
- Navigation menus work properly
- Content displays as expected
- Search functionality operates (if enabled)
- Responsive design works on different screen sizes

**Customization Verification (Mode A):**
- Project-specific content appears correctly
- Generated navigation matches project structure
- AI-customized sections reflect actual project features
- Documentation organization makes logical sense

### Step 8: Deployment Setup

**GitHub Pages Deployment (Recommended):**

1. **Create GitHub Repository:**
   ```bash
   # If not already done
   git remote add origin https://github.com/[username]/[repository-name].git
   git branch -M main
   git push -u origin main
   ```

2. **Configure GitHub Pages:**
   - Go to repository Settings → Pages
   - Select "GitHub Actions" as source
   - The pre-configured workflow will automatically deploy on pushes to main

3. **Manual Deployment (Alternative):**
   ```bash
   # Using SSH
   USE_SSH=true yarn deploy

   # Using HTTPS
   GIT_USER=[username] yarn deploy
   ```

**Other Deployment Options:**
- Netlify: Connect repository for automatic deployments
- Vercel: Import project for serverless hosting
- Self-hosted: Build static files with `yarn build` and serve from any web server

### Step 9: Success Confirmation and Next Steps

**Confirm Completion:**
- ✅ Website created successfully in destination directory
- ✅ Dependencies installed and development server working
- ✅ Content customized appropriately (Mode A) or ready for manual customization (Mode B)
- ✅ Deployment guidance provided

**Provide Next Steps:**
1. **Content Refinement**: Review and edit AI-generated content for accuracy
2. **Additional Customization**: Further branding, styling, or structural changes
3. **Content Addition**: Add more documentation, blog posts, or pages as needed
4. **Deployment**: Set up automatic deployment if desired
5. **Maintenance**: Regular updates and content improvements

## Content Analysis Capabilities

**Supported File Types:**
- **Code**: Python, JavaScript, Java, C++, Go, Rust, and other common programming languages
- **Documentation**: Markdown, reStructuredText, plain text, HTML
- **Configuration**: JSON, YAML, TOML, XML, Dockerfile, package manifests
- **Academic**: PDF documents, LaTeX files, research papers
- **Web**: HTML, CSS, React components

**Analysis Insights:**
- **Project Architecture**: Understanding of codebase structure and organization
- **Feature Discovery**: Identification of key capabilities and functionalities
- **Documentation Gaps**: Areas where additional documentation would be valuable
- **User Journey**: How different audiences interact with the project
- **Technology Integration**: Dependencies, frameworks, and deployment requirements

## Customization Features

**Intelligent Content Generation:**
- Project-specific homepage with relevant messaging
- Appropriate documentation hierarchy and navigation
- Feature descriptions based on actual project capabilities
- User guides tailored to project's target audience

**Smart Organization:**
- Documentation sections that match project structure
- Navigation menus reflecting logical information architecture
- Content categorization based on user needs analysis
- Integration of existing documentation with generated content

**Adaptive Styling:**
- Theme selections appropriate for project type and audience
- Color schemes that complement existing project branding
- Typography choices that enhance readability and professionalism

## FAQ

**Q: What happens if my source directory is very large?**
A: The analysis focuses on key files and representative samples. Very large directories are processed efficiently by analyzing file patterns and focusing on documentation-rich areas.

**Q: Can I customize the website after it's generated?**
A: Absolutely! The generated website is a standard Docusaurus project that you can fully customize. The AI analysis provides a strong starting point that you can refine further.

**Q: What if the AI analysis misunderstands my project?**
A: The generated content serves as a foundation. Review all AI-generated content and edit as needed to ensure accuracy and completeness.

**Q: Can I use this skill for non-technical projects?**
A: Yes! The analysis works with any type of project content, including business documents, research materials, creative projects, and educational content.

**Q: What if I don't have a source directory to analyze?**
A: No problem! The skill will create a basic Docusaurus template that you can customize manually. You'll get the same professional website framework with guidance on how to customize it.

## Troubleshooting

**Content Analysis Issues:**
- **Empty or minimal analysis**: Ensure source directory contains meaningful files (README, documentation, code)
- **Incorrect project understanding**: Review source materials and consider adding a README or project description file
- **Missing key features**: Manually edit generated content to include overlooked aspects

**Template Setup Problems:**
- **Git clone fails**: Check internet connection and GitHub repository accessibility
- **Yarn install fails**: Ensure Node.js and yarn are properly installed
- **Development server won't start**: Check for port conflicts (default: 3000) and dependency issues

**Deployment Issues:**
- **GitHub Pages not working**: Verify repository settings and workflow configuration
- **Build failures**: Check for content or configuration errors in customized files
- **Access problems**: Ensure repository is public or deployment permissions are configured

**Performance Optimization:**
- **Large file processing**: Consider excluding unnecessary files from analysis
- **Slow build times**: Review generated content for optimization opportunities
- **Memory issues**: Process source directories in smaller segments if needed

## Assets Available

- **Docusaurus Template**: Complete professional website framework with documentation, blog, and deployment setup
- **Content Analysis Engine**: AI-powered understanding of diverse project materials
- **Customization Logic**: Intelligent template population based on project characteristics
- **Deployment Workflows**: Pre-configured GitHub Actions and manual deployment options

For advanced Docusaurus customization beyond the AI-generated setup, see the [Docusaurus Customization Guide](assets/docusaurus-guide.md).