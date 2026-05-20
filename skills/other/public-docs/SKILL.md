---
hidden: true
noIndex: true
---

# skill

A comprehensive guide for editing GitBook documentation in external environments like Cursor, Claude Code, or other text editors. This skill provides all the formatting syntax, configuration options, and best practices needed to create and maintain GitBook content outside the GitBook web interface.

### When to Use This Skill

Use this skill when working with GitBook documentation through:

* Git-synced repositories (GitHub, GitLab)
* Local markdown editors
* IDE integrations
* Command-line tools
* Any environment where you're editing GitBook content as files rather than through the GitBook UI

### Quick Reference

#### GitBook Content Structure

GitBook organizes content through pages, spaces, and collections:

* **Pages** are individual markdown files that make up your documentation
* **Spaces** are collections of pages organized into a documentation site
* **Collections** are groups of spaces

**File structure:**

```
/
  .gitbook/
    assets/              # GitBook-managed images and files
    includes/            # Reusable content blocks
    vars.yaml            # Space-level variables
  .gitbook.yaml          # Configuration
  README.md              # Homepage
  SUMMARY.md             # Table of contents
  getting-started/       # Section folder
    installation.md
    quickstart.md
  api-reference/
    authentication.md
    endpoints.md
```

**Frontmatter fields:**

```markdown
---
description: Page description for SEO
icon: book-open
hidden: true
vars:
  page_variable: value
if: visitor.claims.unsigned.condition
layout:
  width: default  # or 'wide'
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---
```

**Variables and expressions:**

* Space variables: `/.gitbook/vars.yaml`
* Page variables: Frontmatter `vars:`
* Expression syntax: `<code class="expression">space.vars.variableName</code>`

**Most common custom blocks:**

* `{% tabs %}...{% endtabs %}` for alternatives
* `{% hint style="..." %}...{% endhint %}` for callouts
* `{% stepper %}...{% endstepper %}` for sequential steps
* `<details>...<summary>...</details>` for expandable content

**Links:**

* External: `[text](https://example.com)`
* Internal: Use relative paths like `[text](page.md)` or `[text](../folder/page.md)`

**Key reminders:**

* Read SUMMARY.md first when working with existing content to understand structure
* Test in GitBook after editing locally
* Keep SUMMARY.md synchronized with your file structure
* Variables are defined in `.gitbook/vars.yaml` (space-level) or page frontmatter (page-level)
* OpenAPI specs must be uploaded via API/CLI/UI, not embedded in markdown

### When to Use Which Block

Choose the right GitBook block for your content needs:

| Need                                       | Use                         | Why                                                                   |
| ------------------------------------------ | --------------------------- | --------------------------------------------------------------------- |
| Sequential, ordered instructions           | `{% stepper %}`             | Guides users through multi-step processes with clear progression      |
| Alternative options (languages, platforms) | `{% tabs %}`                | Lets users choose their relevant option without cluttering the page   |
| Optional or detailed information           | `<details>` (Expandable)    | Keeps page scannable while providing depth for interested readers     |
| Important warnings or tips                 | `{% hint %}`                | Draws attention with colored styling (info, warning, danger, success) |
| Side-by-side comparisons                   | `{% columns %}`             | Shows related information in parallel (max 2 columns)                 |
| Timeline or changelog                      | `{% updates %}`             | Displays dated entries in reverse chronological order                 |
| Visual navigation cards                    | `<table data-view="cards">` | Creates clickable card grid for section navigation                    |
| Downloadable files                         | `{% file %}`                | Provides files with captions and descriptions                         |
| Call-to-action links                       | `<a class="button">`        | Highlights primary or secondary actions                               |
| Reusable content across pages              | `{% include %}`             | Maintains consistency for repeated content blocks                     |
| Dynamic content                            | `<code class="expression">` | Displays variable values that update automatically                    |

**Variable scope decision:**

| If variable is...          | Define it as...                      | Access with...            |
| -------------------------- | ------------------------------------ | ------------------------- |
| Used across multiple pages | Space-level in `/.gitbook/vars.yaml` | `space.vars.variableName` |
| Specific to one page       | Page-level in frontmatter `vars:`    | `page.vars.variableName`  |

### Working with Existing Content

When working with an existing GitBook space that's synced to Git, follow this workflow to understand the structure:

1. **Read SUMMARY.md first** - This file contains the complete table of contents and navigation structure. It shows you:
   * All pages and their hierarchy
   * Page groups and organization
   * The relative paths to each markdown file
2. **If SUMMARY.md doesn't exist** - GitBook has inferred the structure from your directory layout. Browse the directory structure to understand how pages are organized.
3. **Check .gitbook.yaml** - Review this file to understand:
   * Where the root documentation directory is located
   * Any custom paths for README.md or SUMMARY.md
   * Existing redirects
4. **Explore .gitbook/assets/** - Contains all uploaded images and files referenced in the documentation
5. **Check .gitbook/vars.yaml** - Contains space-level variables if any are defined

This approach ensures you understand the existing structure before making changes, helping you maintain consistency and avoid breaking internal links.

### Configuration Files

#### .gitbook.yaml

The `.gitbook.yaml` file configures your GitBook space. It should be placed at the root of your documentation directory (or in a subdirectory if using monorepos).

**Basic structure:**

```yaml
root: ./

structure:
  readme: ./README.md
  summary: ./SUMMARY.md

redirects:
  old-page: new-page.md
  help: support.md
```

**Configuration options:**

* `root`: The root directory for your documentation (default: `./`)
* `structure.readme`: Path to your homepage (default: `./README.md`)
* `structure.summary`: Path to your table of contents (default: `./SUMMARY.md`)
* `redirects`: Key-value pairs mapping old URLs to new page paths

**Monorepo support:**

For repositories with multiple documentation projects:

```
/
  packages/
    docs/
      .gitbook.yaml
      README.md
      SUMMARY.md
    api/
      .gitbook.yaml
      README.md
      SUMMARY.md
```

When setting up Git Sync, configure the "Project directory" to point to the subdirectory containing the `.gitbook.yaml` file.

**Important notes:**

* Paths in `.gitbook.yaml` are relative to the `root` option
* Redirects defined here are space-specific (apply only to this space)
* For site-wide redirects across multiple spaces, use the GitBook UI instead
* When using Git Sync, manage the README file only through your repository to avoid conflicts

### The .gitbook Directory

When using Git Sync, GitBook creates a `.gitbook` directory in your repository to store assets, variables, and generated content.

**Directory structure:**

```
.gitbook/
  assets/          # Uploaded images and files
  includes/        # Reusable content blocks (exported as individual .md files)
  vars.yaml        # Space-level variables
```

**Important notes about .gitbook:**

* **Assets**: Images and files uploaded through the GitBook UI are stored in `.gitbook/assets/`
* **Reusable content**: Each reusable content block is exported as a separate markdown file in `.gitbook/includes/`
* **Variables**: Space-level variables are stored in `.gitbook/vars.yaml` as key-value pairs
* **References**: Pages reference reusable content using `{% include "/reusable-content/rc12345" %}`
* **Images**: Markdown pages reference images like `![alt](../.gitbook/assets/image-name.svg)`
* **Table of contents**: The `.gitbook/includes` folder and its files may appear in your space's table of contents. You may need to manually hide them from the TOC if this happens.
* **Location**: In monorepos, the `.gitbook` directory is created in the root of each synced space (not necessarily the repository root)

#### SUMMARY.md

The `SUMMARY.md` file defines your table of contents and navigation structure. It's a markdown file with a specific format that mirrors the sidebar navigation in GitBook.

**Basic structure:**

```markdown
# Summary

## Use headings to create page groups like this one

* [First page's title](page1/README.md)
    * [Some child page](page1/page1-1.md)
    * [Some other child page](page1/page1-2.md)
* [Second page's title](page2/README.md)
    * [Some child page](page2/page2-1.md)
    * [Some other child page](page2/page2-2.md)

## A second page group

* [Another page](another-page.md)
```

**Key rules:**

* Use `#` for the main title (commonly "Table of contents" or "Summary")
* Use `##` headings to create page groups (section headers in the sidebar)
* Use `*` for unordered lists to define pages and subpages
* Indent with spaces (not tabs) to create nested/child pages
* Each list item should be a markdown link: `[Link text](path/to/file.md)`
* Paths are relative to the location specified in `.gitbook.yaml` (typically the root)

**Page link titles (optional):**

You can define a different title for the sidebar navigation versus the page itself:

```markdown
# Summary

* [Page main title](page.md "Page link title")
```

The text in quotes ("Page link title") will be used in:

* The table of contents sidebar
* Pagination buttons at the bottom of pages
* Any relative links to that page

**Important notes:**

* SUMMARY.md is optional. If not provided, GitBook infers structure from your folder hierarchy
* You cannot reference the same markdown file twice in SUMMARY.md (each page has only one URL)
* GitBook updates SUMMARY.md automatically when you edit through the GitBook UI
* The file structure reflects exactly what users see in the navigation sidebar

### Markdown Formatting

GitBook uses GitHub Flavored Markdown with custom extensions.

**Standard markdown:**

```markdown
# Heading 1
## Heading 2
### Heading 3

**bold text**
*italic text*
`inline code`

- Bullet list item
- Another item
  - Nested item

1. Numbered list
2. Second item

[Link text](https://example.com)
[Internal link](getting-started.md)
```

**Code blocks:**

````markdown
```javascript
const foo = 'bar';
console.log(foo);
```
````

**Code blocks with titles:**

````markdown
{% code title="index.js" %}
```javascript
const foo = 'bar';
console.log(foo);
```
{% endcode %}
````

**Inline links:**

* External links: `[text](https://example.com)`
* Internal pages: Use relative file paths like `[text](page.md)`, `[text](../folder/page.md)`, or `[text](subfolder/page.md)`
* Email: `[text](mailto:email@example.com)`

**Math/TeX:**

```markdown
Inline formula: $$E = mc^2$$

Block formula:

$$
E = mc^2
$$
```

### Page Frontmatter

GitBook supports YAML frontmatter at the top of markdown files to configure page-specific settings. Frontmatter must be placed at the very beginning of the file, before any content.

**Available frontmatter fields:**

```markdown
---
description: Page description used for SEO and page previews
icon: book-open
hidden: true
vars:
  page_variable: value
  another_var: another value
if: visitor.claims.unsigned.isPremium
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---
```

**Field descriptions:**

*   **`description:`** - Page description text. Supports multiline with `>-` syntax:

    ```yaml
    description: >-
      This is a longer description
      that spans multiple lines
    ```
* **`icon:`** - Icon name from Font Awesome (e.g., `book-open`, `bolt`, `stars`, `icons`, `brackets-curly`)
* **`hidden: true`** - Hides the page from the table of contents in published documentation
*   **`vars:`** - Page-level variables (key-value pairs) that can be referenced in expressions:

    ```yaml
    vars:
      version: v1.2.3
      api_key: example_key
    ```
*   **`if:`** - Adaptive content visibility condition. Controls when the page is visible based on visitor attributes:

    ```yaml
    if: visitor.claims.unsigned.isPremium
    ```

    **Note:** While adaptive content conditions can be set in frontmatter, it's recommended to configure them through the GitBook UI for better maintainability and team visibility.
*   **`layout:`** - Controls page layout and which elements are visible. This maps to the "Page Options" settings in the GitBook UI:

    * **`width:`** - Page content width
      * `default` - Standard content width
      * `wide` - Wider content area (automatically widens full-width blocks like tables and code)
    * **`title.visible:`** - Show/hide the page title (boolean: `true` or `false`)
    * **`description.visible:`** - Show/hide the page description (boolean: `true` or `false`)
    * **`tableOfContents.visible:`** - Show/hide the left sidebar table of contents (boolean: `true` or `false`)
    * **`outline.visible:`** - Show/hide the right sidebar page outline/headings (boolean: `true` or `false`)
    * **`pagination.visible:`** - Show/hide next/previous page navigation links (boolean: `true` or `false`)
    * **`metadata.visible:`** - Show/hide page metadata section (boolean: `true` or `false`)

    Example for a landing page with minimal chrome:

    ```yaml
    layout:
      width: wide
      title:
        visible: true
      description:
        visible: true
      tableOfContents:
        visible: false
      outline:
        visible: false
      pagination:
        visible: false
    ```

**Example complete frontmatter:**

```markdown
---
description: Create reusable variables that can be referenced in pages and spaces
icon: icons
vars:
  latest_version: v3.0.4
  support_email: help@example.com
layout:
  width: wide
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Your Page Title

Page content starts here...
```

### Variables and Expressions

GitBook supports variables that can be dynamically displayed in your content using expressions. Variables can be defined at the space level or page level.

#### Variable Storage

**Space-level variables** are stored in `/.gitbook/vars.yaml` at the root of your documentation:

```yaml
# .gitbook/vars.yaml
food: apple
latest_version: v3.0.4
company_name: Acme Corp
```

**Page-level variables** are stored in the page's frontmatter under `vars:`:

```markdown
---
vars:
  page_food: orange
  page_version: v2.1.0
---
```

#### Using Variables with Expressions

Expressions allow you to reference and display variable values dynamically in your content. Expressions use JavaScript syntax and are wrapped in `<code class="expression">` tags.

**Syntax:**

```markdown
<code class="expression">JavaScript expression here</code>
```

**Examples:**

```markdown
<!-- Simple expression -->
<code class="expression">1 + 1</code>

<!-- Reference a space-level variable -->
<code class="expression">space.vars.latest_version</code>

<!-- String concatenation with variable -->
<code class="expression">"My favorite food is " + space.vars.food</code>

<!-- Reference a page-level variable -->
<code class="expression">page.vars.page_food</code>

<!-- Conditional logic -->
<code class="expression">space.vars.latest_version === "v3.0.4" ? "Latest" : "Outdated"</code>
```

**Variable references:**

* `space.vars.variableName` - Access space-level variables defined in `/.gitbook/vars.yaml`
* `page.vars.variableName` - Access page-level variables defined in the page's frontmatter

**Important notes:**

* Variable definitions (the actual variable storage) are managed through:
  * `/.gitbook/vars.yaml` for space-level variables
  * Page frontmatter `vars:` for page-level variables
* Expressions can contain any valid JavaScript code and are evaluated when the page is rendered
* When editing locally, you can create space variables by editing `/.gitbook/vars.yaml` and page variables by adding them to frontmatter
* The GitBook UI provides a visual editor for managing variables, but they are fully editable in markdown files

### GitBook Custom Blocks

GitBook extends standard markdown with custom block syntax using tags like `{% tabs %}`, `{% hint %}`, etc. These blocks enable rich, interactive documentation features.

#### Tabs

Use tabs to present alternative content like different programming languages or platform-specific instructions.

**When to use:** Comparing alternatives (code in different languages, platform-specific commands, configuration options).

**Syntax:**

````markdown
{% tabs %}
{% tab title="JavaScript" %}
```javascript
const greeting = 'Hello World';
console.log(greeting);
```
{% endtab %}

{% tab title="Python" %}
```python
greeting = "Hello World"
print(greeting)
```
{% endtab %}
{% endtabs %}
````

#### Stepper

Use steppers for sequential, multi-step processes where order matters.

**When to use:** Tutorials, installation guides, how-to guides, onboarding checklists, any sequential process.

**Syntax:**

```markdown
{% stepper %}
{% step %}
## First step

Complete the initial setup by installing the required dependencies.
{% endstep %}

{% step %}
## Second step

Configure your environment variables in the `.env` file.
{% endstep %}

{% step %}
## Third step

Run the application with `npm start`.
{% endstep %}
{% endstepper %}
```

#### Hints

Use hints to highlight important information without disrupting flow. Supported styles: `info`, `warning`, `danger`, `success`.

**When to use:** Supplementary information, call-outs, best practices, warnings, troubleshooting tips.

**Syntax:**

```markdown
{% hint style="info" %}
This is an informational hint with helpful context.
{% endhint %}

{% hint style="warning" %}
Be careful when running this command in production.
{% endhint %}

{% hint style="danger" %}
This action cannot be undone. Make sure you have backups.
{% endhint %}

{% hint style="success" %}
Your configuration has been saved successfully!
{% endhint %}
```

#### Expandable

Use expandable sections for optional content that doesn't need to be visible by default.

**When to use:** Optional deep-dives, advanced explanations, lengthy logs, FAQ answers, content that would clutter the page.

**Syntax:**

````markdown
<details>
<summary>Advanced Configuration Options</summary>

Here you can find detailed information about advanced settings that most users won't need.

```yaml
advanced:
  option1: value1
  option2: value2
```
</details>
````

#### Columns

Use columns to present content side-by-side (2 columns maximum).

**When to use:** Side-by-side comparisons (pros vs cons), before/after examples, parallel instructions.

**Syntax:**

```markdown
{% columns %}
{% column %}
### Before

Old implementation that was inefficient.
{% endcolumn %}

{% column %}
### After

New optimized approach with better performance.
{% endcolumn %}
{% endcolumns %}
```

#### Updates

Use updates blocks for product updates, release notes, or changelogs.

**When to use:** Changelog pages, release notes, version updates, product announcements.

**Syntax:**

```markdown
{% updates format="full" %}
{% update date="2024-01-15" %}
# Version 2.0 Released

We've added new features including dark mode and improved search.
{% endupdate %}

{% update date="2024-01-01" %}
# Bug Fixes

Fixed several issues reported by the community.
{% endupdate %}
{% endupdates %}
```

#### Cards

Use cards to create visual, clickable navigation elements. Cards are HTML tables with special attributes.

**When to use:** Dashboards, feature overviews, linking to related pages, showcasing multiple resources.

**Syntax:**

```markdown
<table data-view="cards">
    <thead>
        <tr>
            <th>Title</th>
            <th data-card-target data-type="content-ref">Target</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Getting Started Guide</td>
            <td><a href="getting-started/quickstart.md">Quick Start</a></td>
        </tr>
        <tr>
            <td>API Reference</td>
            <td><a href="api-reference/overview.md">API Docs</a></td>
        </tr>
        <tr>
            <td>Examples</td>
            <td><a href="/spaces/abc1234/pages/jkl1121">Code Examples</a></td>
        </tr>
    </tbody>
</table>
```

#### Embeds

Use embeds to include external content like videos, interactive demos, or social media.

**When to use:** Demonstration videos, interactive code sandboxes, tweets, external rich media.

**Syntax:**

```markdown
{% embed url="https://www.youtube.com/watch?v=dQw4w9WgXcQ" %}

{% embed url="https://codepen.io/username/pen/example" %}
```

#### Files

Use file blocks to provide downloadable files with captions.

**Syntax:**

```markdown
{% file src="https://example.com/document.pdf" %}
Complete documentation in PDF format.
{% endfile %}
```

#### Buttons

Use buttons for clear call-to-action links. Supported styles: `primary` and `secondary`.

**When to use:** Download links, "Try it now" actions, external resource navigation.

**Syntax:**

```markdown
<a href="https://example.com/download" class="button primary">Download Now</a>

<a href="https://docs.example.com" class="button secondary">View Documentation</a>
```

**Buttons with icons:**

```markdown
<a href="https://github.com/user/repo" class="button primary" data-icon="github">View on GitHub</a>
```

Icons use Font Awesome names (without the `fa-` prefix).

#### Icons

Inline icons from Font Awesome can enhance text readability.

**When to use:** Visual indicators, status icons, improving scannability.

**Syntax:**

```markdown
<i class="fa-check">check</i> Feature enabled
<i class="fa-warning">warning</i> Requires configuration
<i class="fa-info-circle">info</i> Learn more
```

#### Reusable Content

Reusable content blocks let you sync content across multiple pages.

**When to use:** Call-to-actions, disclaimers, repeated instructions, any content that needs to stay consistent across pages.

**Syntax:**

```markdown
{% include "/reusable-content/rc12345" %}
```

Note: Reusable content blocks are different from pages. They're created through the GitBook UI and given unique IDs.

#### OpenAPI Specifications

OpenAPI specifications enable interactive, testable API documentation in GitBook. However, OpenAPI specs cannot be added directly to markdown files.

**How to add OpenAPI specs:**

OpenAPI specifications must be uploaded through one of these methods:

1. **GitBook API** - Use the [OpenAPI endpoints](https://docs.gitbook.com/developers/gitbook-api/api-reference/openapi) to programmatically upload specs
2. **GitBook CLI** - Use the `gitbook openapi` command
3. **GitBook UI** - Upload specs through the web interface

**Once uploaded**, you can reference API methods in your markdown using the OpenAPI block syntax:

```markdown
{% openapi src="https://api.example.com/openapi.json" path="/users" method="get" %}
[https://api.example.com/openapi.json](https://api.example.com/openapi.json)
{% endopenapi %}
```

**Important notes:**

* You cannot embed OpenAPI spec content directly in markdown files
* The `src` URL must point to an already-uploaded OpenAPI specification
* For more information, see the [GitBook OpenAPI documentation](https://docs.gitbook.com/api-references/openapi)

### Nested Markdown in Custom Blocks

Markdown formatting works inside custom block tags. Maintain standard markdown syntax within custom blocks:

````markdown
{% tabs %}
{% tab title="Example" %}
This tab contains markdown:

- Bullet points work
  - Nested bullets too
- **Bold text** and *italic text*
- `inline code`

```javascript
// Code blocks work too
const example = true;
```
{% endtab %}
{% endtabs %}
````

### Common Pitfalls

**File organization:**

* Don't reference the same markdown file twice in SUMMARY.md
* Keep file paths consistent between SUMMARY.md and actual file locations
* Use relative paths consistently

**Configuration conflicts:**

* When using Git Sync, manage README.md only through your repository
* Keep .gitbook.yaml at the correct root level for your project
* Test redirects after moving or renaming files

**Markdown formatting:**

* Tables and columns are discouraged (use custom blocks instead)
* Avoid excessive nested lists (keep hierarchy simple)
* Don't mix tab/space indentation in SUMMARY.md

**Custom blocks:**

* Always close blocks properly (`{% endtab %}`, `{% endhint %}`, etc.)
* Match opening and closing tags exactly
* Test custom blocks in GitBook after editing locally

### Working with Git Sync

When GitBook is synced with Git:

1. Changes in Git automatically update GitBook
2. Changes in GitBook automatically commit to Git
3. GitBook maintains SUMMARY.md based on UI edits
4. Merge conflicts should be resolved in Git

**Best practices:**

* Make structural changes (navigation) through SUMMARY.md in Git
* Make content changes either in Git or GitBook UI (be consistent)
* Review auto-generated commits from GitBook
* Use branch-based workflows for significant updates
* Test changes in a preview before merging to main

### Example Complete Page

Here's a complete example showing multiple GitBook features:

````
```markdown
# API Authentication Guide

Learn how to authenticate with our API using API keys or OAuth 2.0.

{% hint style="info" %}
All API requests require authentication. Choose the method that best fits your use case.
{% endhint %}

## Authentication Methods

{% tabs %}
{% tab title="API Key" %}
The simplest authentication method. Include your API key in the request header:
```bash
curl -H "X-API-Key: your-api-key" https://api.example.com/v1/users
```

{% hint style="warning" %} 
Never commit API keys to version control. Use environment variables instead. 
{% endhint %} 
{% endtab %}

{% tab title="OAuth 2.0" %}
More secure for user-facing applications:

{% stepper %}
{% step %}
## Register your application
Get your client ID and secret from the developer dashboard. 
{% endstep %}

{% step %}
## Request authorization
Redirect users to our OAuth endpoint. 
{% endstep %}

{% step %}
Exchange code for token

Use the authorization code to get an access token. 
{% endstep %} 
{% endstepper %} 
{% endtab %} 
{% endtabs %}

## Rate Limits
{% columns %}
{% column %}
### Free Tier
1,000 requests/hour
10,000 requests/day 
{% endcolumn %}

{% column %}
### Pro Tier
10,000 requests/hour
100,000 requests/day 
{% endcolumn %}
{% endcolumns %}
<details>
<summary>Need higher limits?</summary>

Contact our sales team to discuss enterprise plans with custom rate limits and SLAs.
</details>

<a href="https://example.com/signup" class="button primary" data-icon="rocket">Get Started</a>
````
