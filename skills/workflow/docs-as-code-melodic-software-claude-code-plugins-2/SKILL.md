---
name: docs-as-code
description: Documentation pipeline automation and docs-as-code workflows
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Docs-as-Code Skill

## When to Use This Skill

Use this skill when:

- **Docs As Code tasks** - Working on documentation pipeline automation and docs-as-code workflows
- **Planning or design** - Need guidance on Docs As Code approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Implement documentation-as-code workflows with automated pipelines, version control, and CI/CD integration.

## MANDATORY: Documentation-First Approach

Before implementing docs-as-code:

1. **Invoke `docs-management` skill** for documentation patterns
2. **Verify tooling versions** via MCP servers (context7 for docusaurus/mkdocs)
3. **Base guidance on current best practices**

## Docs-as-Code Philosophy

```text
Docs-as-Code Principles:

┌─────────────────────────────────────────────────────────────────────────────┐
│  1. Version Control                                                          │
│     - Docs live alongside code in the same repository                        │
│     - Changes tracked with meaningful commit messages                        │
│     - Branch-based workflow for documentation updates                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  2. Review Process                                                           │
│     - Pull requests for documentation changes                                │
│     - Technical review by subject matter experts                             │
│     - Style review by technical writers                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  3. Automated Testing                                                        │
│     - Linting for style and grammar                                          │
│     - Link validation                                                        │
│     - Build verification                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  4. Continuous Deployment                                                    │
│     - Automatic publishing on merge                                          │
│     - Preview deployments for PRs                                            │
│     - Versioned documentation releases                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Documentation Tooling Comparison

| Tool | Language | Best For | Build Speed |
|------|----------|----------|-------------|
| **Docusaurus** | JS/React | Product docs, versioning | Fast |
| **MkDocs** | Python | Technical docs, Material theme | Fast |
| **Sphinx** | Python | API docs, reStructuredText | Medium |
| **Hugo** | Go | Large sites, speed | Very Fast |
| **Astro** | JS | Modern sites, MDX | Fast |
| **VitePress** | JS/Vue | Vue ecosystem | Very Fast |
| **Jekyll** | Ruby | GitHub Pages native | Medium |

## Project Structure

### Docusaurus Structure

```text
docs/
├── docusaurus.config.js        # Main configuration
├── sidebars.js                 # Navigation structure
├── package.json                # Dependencies
├── docs/                       # Documentation content
│   ├── intro.md
│   ├── getting-started/
│   │   ├── installation.md
│   │   └── configuration.md
│   ├── guides/
│   │   ├── quick-start.md
│   │   └── advanced.md
│   └── api/
│       └── reference.md
├── blog/                       # Blog posts (optional)
├── src/
│   ├── components/             # React components
│   ├── css/                    # Custom styles
│   └── pages/                  # Custom pages
├── static/                     # Static assets
│   └── img/
└── versioned_docs/             # Version snapshots
    ├── version-1.0/
    └── version-2.0/
```

### MkDocs Structure

```text
docs/
├── mkdocs.yml                  # Configuration
├── docs/
│   ├── index.md
│   ├── getting-started/
│   │   ├── installation.md
│   │   └── configuration.md
│   ├── user-guide/
│   │   └── features.md
│   ├── reference/
│   │   └── api.md
│   └── about/
│       └── changelog.md
├── overrides/                  # Theme customization
│   ├── main.html
│   └── partials/
└── requirements.txt            # Python dependencies
```

## Configuration Templates

### Docusaurus Configuration

```javascript
// docusaurus.config.js
const config = {
  title: 'Project Name',
  tagline: 'Project tagline',
  url: 'https://docs.example.com',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'organization',
  projectName: 'project',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/org/project/edit/main/docs/',
          showLastUpdateAuthor: true,
          showLastUpdateTime: true,
          versions: {
            current: {
              label: 'Next',
              path: 'next',
            },
          },
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/org/project/edit/main/docs/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Project',
      logo: {
        alt: 'Project Logo',
        src: 'img/logo.svg',
      },
      items: [
        { type: 'doc', docId: 'intro', position: 'left', label: 'Docs' },
        { to: '/blog', label: 'Blog', position: 'left' },
        { type: 'docsVersionDropdown', position: 'right' },
        { href: 'https://github.com/org/project', label: 'GitHub', position: 'right' },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [{ label: 'Getting Started', to: '/docs/intro' }],
        },
        {
          title: 'Community',
          items: [{ label: 'Discord', href: 'https://discord.gg/xxx' }],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Organization.`,
    },
    prism: {
      theme: require('prism-react-renderer/themes/github'),
      darkTheme: require('prism-react-renderer/themes/dracula'),
      additionalLanguages: ['csharp', 'powershell', 'bash'],
    },
    algolia: {
      appId: 'YOUR_APP_ID',
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'project',
    },
  },
};

module.exports = config;
```

### MkDocs Configuration

```yaml
# mkdocs.yml
site_name: Project Documentation
site_url: https://docs.example.com
repo_url: https://github.com/org/project
repo_name: org/project
edit_uri: edit/main/docs/

theme:
  name: material
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.indexes
    - toc.follow
    - content.code.copy
    - content.code.annotate
    - search.suggest
    - search.highlight

plugins:
  - search
  - git-revision-date-localized:
      enable_creation_date: true
  - minify:
      minify_html: true
  - mike:
      version_selector: true
      css_dir: css
      javascript_dir: js

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - admonition
  - pymdownx.details
  - attr_list
  - md_in_html
  - toc:
      permalink: true

nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/installation.md
    - Configuration: getting-started/configuration.md
  - User Guide:
    - Features: user-guide/features.md
  - Reference:
    - API: reference/api.md
  - About:
    - Changelog: about/changelog.md

extra:
  version:
    provider: mike
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/org/project
```

## CI/CD Pipeline Templates

### GitHub Actions for Docusaurus

```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - '.github/workflows/docs.yml'
  pull_request:
    branches: [main]
    paths:
      - 'docs/**'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: docs/package-lock.json

      - name: Install dependencies
        working-directory: docs
        run: npm ci

      - name: Lint Markdown
        run: npx markdownlint-cli2 "docs/**/*.md"

      - name: Check links
        working-directory: docs
        run: npm run check-links

  build:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v5

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: docs/package-lock.json

      - name: Install dependencies
        working-directory: docs
        run: npm ci

      - name: Build
        working-directory: docs
        run: npm run build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs/build

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

  preview:
    if: github.event_name == 'pull_request'
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy preview
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: docs/build
          destination_dir: pr-preview/${{ github.event.number }}

      - name: Comment preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '📚 Documentation preview: https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}/pr-preview/${{ github.event.number }}/'
            })
```

### Azure DevOps for MkDocs

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - docs/**

pool:
  vmImage: 'ubuntu-latest'

variables:
  pythonVersion: '3.11'

stages:
  - stage: Validate
    jobs:
      - job: Lint
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '$(pythonVersion)'

          - script: |
              pip install -r docs/requirements.txt
              pip install markdownlint-cli2
            displayName: 'Install dependencies'

          - script: markdownlint-cli2 "docs/**/*.md"
            displayName: 'Lint Markdown'

  - stage: Build
    dependsOn: Validate
    jobs:
      - job: Build
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '$(pythonVersion)'

          - script: pip install -r docs/requirements.txt
            displayName: 'Install dependencies'

          - script: mkdocs build --strict
            displayName: 'Build documentation'

          - publish: site
            artifact: documentation

  - stage: Deploy
    dependsOn: Build
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: Deploy
        environment: production
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  artifact: documentation

                - task: AzureStaticWebApp@0
                  inputs:
                    app_location: '$(Pipeline.Workspace)/documentation'
                    azure_static_web_apps_api_token: $(AZURE_STATIC_WEB_APPS_TOKEN)
```

## Documentation Linting

### Markdownlint Configuration

```json
// .markdownlint.json
{
  "default": true,
  "MD001": true,
  "MD003": { "style": "atx" },
  "MD004": { "style": "dash" },
  "MD007": { "indent": 2 },
  "MD009": true,
  "MD010": true,
  "MD012": true,
  "MD013": { "line_length": 120, "code_blocks": false, "tables": false },
  "MD022": { "lines_above": 1, "lines_below": 1 },
  "MD024": { "siblings_only": true },
  "MD025": { "front_matter_title": "" },
  "MD026": { "punctuation": ".,;:!" },
  "MD029": { "style": "ordered" },
  "MD030": { "ul_single": 1, "ol_single": 1, "ul_multi": 1, "ol_multi": 1 },
  "MD033": { "allowed_elements": ["details", "summary", "kbd", "br"] },
  "MD035": { "style": "---" },
  "MD036": false,
  "MD040": true,
  "MD041": true,
  "MD046": { "style": "fenced" },
  "MD048": { "style": "backtick" }
}
```

### Vale Configuration

```yaml
# .vale.ini
StylesPath = styles

MinAlertLevel = suggestion

Packages = Microsoft, write-good, proselint

[*.md]
BasedOnStyles = Vale, Microsoft, write-good

# Ignore code blocks
BlockIgnores = (?s) *(`{3}.*?`{3})

# Custom rules
Microsoft.Contractions = NO
Microsoft.HeadingPunctuation = YES
write-good.Passive = YES
write-good.Weasel = YES
write-good.TooWordy = YES
```

## Living Documentation

### Generating API Docs from Code

```csharp
// API Documentation Generation with XML Comments
/// <summary>
/// Manages user authentication and authorization.
/// </summary>
/// <remarks>
/// <para>
/// This service handles all authentication flows including:
/// <list type="bullet">
///   <item>Password-based authentication</item>
///   <item>OAuth 2.0 / OpenID Connect</item>
///   <item>API key authentication</item>
/// </list>
/// </para>
/// </remarks>
/// <example>
/// <code>
/// var result = await authService.AuthenticateAsync(credentials);
/// if (result.IsSuccess)
/// {
///     var token = result.Value.AccessToken;
/// }
/// </code>
/// </example>
public interface IAuthenticationService
{
    /// <summary>
    /// Authenticates a user with the provided credentials.
    /// </summary>
    /// <param name="credentials">The authentication credentials.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>
    /// A result containing the authentication response on success,
    /// or an error on failure.
    /// </returns>
    /// <exception cref="AuthenticationException">
    /// Thrown when authentication fails due to invalid credentials.
    /// </exception>
    Task<Result<AuthenticationResponse>> AuthenticateAsync(
        AuthenticationCredentials credentials,
        CancellationToken cancellationToken = default);
}
```

### OpenAPI Documentation Generation

```csharp
// Program.cs - Swagger/OpenAPI configuration
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Project API",
        Version = "v1",
        Description = "API documentation for the Project",
        Contact = new OpenApiContact
        {
            Name = "API Support",
            Email = "api@example.com",
            Url = new Uri("https://docs.example.com")
        },
        License = new OpenApiLicense
        {
            Name = "MIT",
            Url = new Uri("https://opensource.org/licenses/MIT")
        }
    });

    // Include XML comments
    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    options.IncludeXmlComments(xmlPath);

    // Security definitions
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "JWT Authorization header using the Bearer scheme.",
        Name = "Authorization",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.Http,
        Scheme = "bearer"
    });

    options.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            Array.Empty<string>()
        }
    });
});
```

## Documentation Testing

### Link Checking

```javascript
// check-links.mjs
import { remark } from 'remark';
import remarkLintNoDeadUrls from 'remark-lint-no-dead-urls';
import { read } from 'to-vfile';
import { glob } from 'glob';
import { reporter } from 'vfile-reporter';

const files = await glob('docs/**/*.md');

for (const file of files) {
  const result = await remark()
    .use(remarkLintNoDeadUrls, {
      skipLocalhost: true,
      skipOffline: true,
    })
    .process(await read(file));

  console.error(reporter(result));
}
```

### Screenshot Testing

```typescript
// docs.spec.ts - Playwright screenshot tests
import { test, expect } from '@playwright/test';

test.describe('Documentation Screenshots', () => {
  test('homepage renders correctly', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage.png');
  });

  test('API reference page', async ({ page }) => {
    await page.goto('/docs/api/reference');
    await expect(page.locator('.api-content')).toBeVisible();
    await expect(page).toHaveScreenshot('api-reference.png');
  });

  test('dark mode toggle', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-theme-toggle]');
    await expect(page).toHaveScreenshot('homepage-dark.png');
  });
});
```

## Best Practices

### Content Organization

| Practice | Description |
|----------|-------------|
| **Single Source of Truth** | Each concept documented in one place |
| **Progressive Disclosure** | Start simple, link to details |
| **Consistent Structure** | Same sections across similar pages |
| **Clear Navigation** | Logical hierarchy, breadcrumbs |
| **Search Optimization** | Good headings, keywords, descriptions |

### Writing Guidelines

1. **Use active voice**: "Configure the setting" not "The setting should be configured"
2. **Be concise**: Remove unnecessary words
3. **Use examples**: Show, don't just tell
4. **Maintain consistency**: Same terms throughout
5. **Update regularly**: Documentation rots quickly

### Versioning Strategy

```text
Documentation Versioning:

Option 1: Version Folders (Docusaurus/MkDocs mike)
├── docs/
│   ├── version-1.0/
│   ├── version-2.0/
│   └── current/

Option 2: Branch-based
├── main (current)
├── v1.x
└── v2.x

Option 3: Git Tags
├── v1.0.0
├── v2.0.0
└── latest

Recommendation: Use tool-native versioning (Docusaurus versioned_docs, mike for MkDocs)
```

## Workflow

When implementing docs-as-code:

1. **Choose Tooling**: Select SSG based on team skills and requirements
2. **Set Up Structure**: Create organized folder hierarchy
3. **Configure CI/CD**: Automated builds, previews, deployments
4. **Add Linting**: Markdown linting, link checking, spell check
5. **Enable Reviews**: PR-based workflow with tech writer review
6. **Deploy Versioning**: Set up version management strategy
7. **Monitor Analytics**: Track usage, search queries, gaps

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
