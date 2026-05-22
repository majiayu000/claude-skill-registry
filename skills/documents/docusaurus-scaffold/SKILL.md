---
name: docusaurus-scaffold
description: |
  Scaffold and initialize a Docusaurus project with the specific structure for the Physical AI textbook.
  Agent: BookArchitect
version: 1.2.0
inputs:
  site_title:
    description: Title for the Docusaurus site
    required: false
    default: "Physical AI Book"
    example: "Physical AI Book"
  github_org:
    description: GitHub organization or username
    required: false
    default: "faiqahm"
    example: "faiqahm"
  repo_name:
    description: GitHub repository name
    required: false
    default: "hackathon_I_book"
    example: "hackathon_I_book"
  locales:
    description: Supported locales (comma-separated)
    required: false
    default: "en,ur"
    example: "en,ur,es"
  num_chapters:
    description: Number of chapters to scaffold
    required: false
    default: "3"
    example: "5"
---

# Docusaurus Scaffold

**Agent:** BookArchitect

Scaffold and initialize a Docusaurus project with the specific structure for the Physical AI textbook. Creates a complete documentation site with chapters, i18n support, and GitHub Pages deployment configuration.

## Quick Setup

```bash
# Full setup with defaults
.claude/skills/docusaurus-scaffold/scripts/setup.sh

# Custom configuration
.claude/skills/docusaurus-scaffold/scripts/setup.sh \
  --title "Physical AI Book" \
  --github-org faiqahm \
  --repo hackathon_I_book \
  --locales "en,ur" \
  --chapters 5

# Initialize and install dependencies
.claude/skills/docusaurus-scaffold/scripts/setup.sh --install

# Initialize, install, and start dev server
.claude/skills/docusaurus-scaffold/scripts/setup.sh --install --start
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--title TITLE` | Site title | `Physical AI Book` |
| `--github-org ORG` | GitHub org/username | `faiqahm` |
| `--repo NAME` | Repository name | `hackathon_I_book` |
| `--locales LOCALES` | Comma-separated locales | `en,ur` |
| `--chapters N` | Number of chapters | `3` |
| `--install` | Run npm install after setup | off |
| `--start` | Start dev server (requires --install) | off |
| `-h, --help` | Show help message | - |

## What It Creates

### 1. Project Structure

```
project/
├── docs/
│   ├── intro.md                 # Introduction/Welcome page
│   ├── chapter-1/
│   │   ├── _category_.json      # Chapter metadata
│   │   ├── index.md             # Chapter overview
│   │   ├── lesson-1.md          # Lesson content
│   │   └── lesson-2.md
│   ├── chapter-2/
│   │   └── ...
│   └── chapter-3/
│       └── ...
├── i18n/
│   └── ur/
│       ├── docusaurus-theme-classic/
│       │   ├── navbar.json
│       │   └── footer.json
│       └── docusaurus-plugin-content-docs/
│           └── current/
│               ├── intro.md
│               └── chapter-1/
│                   └── ...
├── src/
│   ├── css/
│   │   └── custom.css           # RTL support for Urdu
│   └── pages/
│       └── index.js             # Homepage redirect
├── static/
│   └── img/
│       └── favicon.svg
├── docusaurus.config.js         # Main configuration
├── sidebars.js                  # Sidebar configuration
└── package.json
```

### 2. Configuration Files

**docusaurus.config.js**
- GitHub Pages deployment settings
- i18n with RTL support for Urdu
- Navbar with locale dropdown
- Dark/light theme support

**sidebars.js**
- Auto-generated sidebar from docs folder
- Chapter organization with collapsible sections

### 3. Textbook Structure

Each chapter follows this structure:

```markdown
# Chapter N: Title

## Learning Objectives
- Objective 1
- Objective 2

## Prerequisites
- Prerequisite 1

## Content
(Main lesson content)

## Exercises
1. Exercise 1
2. Exercise 2

## Summary
Key takeaways from this chapter.

## Next Steps
Link to next chapter or related content.
```

### 4. i18n Support

- **English (en)**: Default locale, LTR
- **Urdu (ur)**: RTL support with custom CSS
- Translation files for navbar/footer
- Translated chapter content structure

## Bundled Resources

### 1. Docusaurus Configuration

**File**: `docusaurus.config.js`

```javascript
const config = {
  title: 'Physical AI Book',
  tagline: 'Learn Physical AI, ROS 2, and Robotics',
  favicon: 'img/favicon.svg',

  // GitHub Pages deployment
  url: 'https://faiqahm.github.io',
  baseUrl: '/hackathon_I_book/',
  organizationName: 'faiqahm',
  projectName: 'hackathon_I_book',

  // Enable Mermaid for Diagrams
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

  // i18n configuration
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: { label: 'English', direction: 'ltr' },
      ur: { label: 'اردو', direction: 'rtl', htmlLang: 'ur-PK' },
    },
  },
  // ... rest of config
};
```

### 2. RTL Styles for Urdu

**File**: `src/css/custom.css`

```css
/* RTL Support for Urdu */
html[dir='rtl'] {
  direction: rtl;
}

html[dir='rtl'] .navbar__items {
  flex-direction: row-reverse;
}

html[dir='rtl'] .markdown {
  text-align: right;
}

/* Urdu font family */
html[lang='ur'] {
  font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', serif;
}
```

### 3. Chapter Template

**File**: `docs/chapter-N/index.md`

```markdown
---
sidebar_position: N
---

# Chapter N: [Title]

## Learning Objectives

By the end of this chapter, you will be able to:
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## Prerequisites

Before starting this chapter, ensure you understand:
- Prerequisite 1
- Prerequisite 2

## Introduction

[Chapter introduction content]

## Key Concepts

### Concept 1
[Explanation]

### Concept 2
[Explanation]

## Hands-On Exercise

```python
# Example code
print("Hello, Physical AI!")
```

## Summary

In this chapter, we covered:
- Point 1
- Point 2
- Point 3

## Further Reading

- [Link 1](url)
- [Link 2](url)
```

### 4. Input Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `site_title` | No | `Physical AI Book` | Site title in navbar |
| `github_org` | No | `faiqahm` | GitHub organization |
| `repo_name` | No | `hackathon_I_book` | Repository name |
| `locales` | No | `en,ur` | Supported locales |
| `num_chapters` | No | `3` | Chapters to scaffold |

## Usage Instructions

### Step 1: Run Setup

```bash
.claude/skills/docusaurus-scaffold/scripts/setup.sh --install
```

### Step 2: Add Content

Edit the generated chapter files in `docs/`:
- `docs/intro.md` - Welcome page
- `docs/chapter-1/index.md` - Chapter 1
- `docs/chapter-2/index.md` - Chapter 2
- etc.

### Step 3: Add Translations

For Urdu translations, edit files in `i18n/ur/docusaurus-plugin-content-docs/current/`:
- Copy English content
- Translate to Urdu
- RTL styling is automatic

### Step 4: Test Locally

```bash
# English
npm start

# Urdu
npm start -- --locale ur
```

### Step 5: Build & Deploy

```bash
# Build all locales
npm run build

# Deploy to GitHub Pages
npm run deploy
```

## Verification Checklist

- [ ] `docusaurus.config.js` exists with correct settings
- [ ] `docs/` folder has intro and chapters
- [ ] `i18n/ur/` folder has translation structure
- [ ] `src/css/custom.css` has RTL styles
- [ ] `npm start` works without errors
- [ ] `npm run build` completes successfully
- [ ] Locale switcher appears in navbar

## Automated Testing

Run the test suite to validate skill functionality:

```bash
# Run all tests
.claude/skills/docusaurus-scaffold/scripts/test.sh
```

### Test Suite (18 assertions)

| Test | Description | Validates |
|------|-------------|-----------|
| 1 | --help flag works | CLI help output |
| 2 | package.json created | Basic scaffold |
| 3 | docusaurus.config.js created | Configuration |
| 4 | sidebars.js created | Sidebar config |
| 5 | docs/intro.md created | Introduction page |
| 6 | Chapter 1 with index.md | Chapter structure |
| 7 | Chapter 2 with index.md | Chapter structure |
| 8 | Chapter 3 with index.md | Chapter structure |
| 9 | Urdu navbar.json created | i18n translations |
| 10 | Urdu intro.md created | i18n content |
| 11 | RTL styles in custom.css | RTL support |
| 12 | Homepage redirect configured | Redirect component |
| 13 | Favicon created | Static assets |
| 14 | --chapters 5 creates 5 chapters | Custom chapter count |
| 15 | GitHub Actions workflow created | CI/CD pipeline |
| 16 | Mermaid in config and package.json | Diagram support |
| 17 | Chapter template has Mermaid | Diagram examples |
| 18 | --no-workflow skips workflow | Flag functionality |

### Test Script Features

- **Isolated execution**: Tests run in `/tmp/docusaurus-scaffold-test-$$`
- **Automatic cleanup**: Directory removed on exit via trap
- **Color-coded output**: PASS (green), FAIL (red), TEST (blue)
- **Summary report**: Pass/fail counts with exit code

### Example Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 Docusaurus Scaffold Test Suite
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[TEST] Test 1: --help flag works
[PASS] --help displays usage information
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Test Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Passed: 18
  Failed: 0

✓ All tests passed!
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Build fails with broken links** | Check internal links use relative paths |
| **Urdu text not RTL** | Verify `direction: 'rtl'` in config |
| **Sidebar not showing** | Check `_category_.json` in each chapter folder |
| **npm start fails** | Delete `node_modules`, run `npm install` |
| **Locale not switching** | Clear browser cache, check i18n config |

## Requirements

- Node.js 18+
- npm 8+
- Git (for deployment)

## Physical AI Textbook Chapters

The default scaffold creates these chapters:

| Chapter | Title | Topics |
|---------|-------|--------|
| Intro | Welcome to Physical AI | Overview, prerequisites, how to use |
| 1 | Introduction to Physical AI & ROS 2 | What is Physical AI, ROS 2 basics |
| 2 | Simulation with Gazebo | Virtual environments, robot simulation |
| 3 | Vision-Language-Action Models | VLA concepts, integration |

## Related

- [Docusaurus Documentation](https://docusaurus.io/docs)
- [GitHub Pages Deployment](https://docusaurus.io/docs/deployment#deploying-to-github-pages)
- Skill: `github-pages-deploy` - Deploy the site
- Skill: `urdu-rtl-styler` - Enhanced RTL styling
- Skill: `vercel-fastapi-link` - Backend API

## Changelog

### v1.2.0 (2026-01-02)
**Test Suite & Bug Fixes**

- Add comprehensive test suite (`scripts/test.sh`) with 18 assertions
- Tests run in isolated `/tmp` directory with automatic cleanup
- Color-coded test output with pass/fail summary
- **Bug fixes discovered during testing:**
  - Fix bash counter increment syntax for `set -e` compatibility
    - Changed `((PASSED++))` to `PASSED=$((PASSED + 1))`
    - Prevents script exit when incrementing from 0
  - Fix test cleanup to properly remove `.github` directory
    - Glob pattern `*` doesn't match dot-prefix directories
    - Use `rm -rf "$DIR"` instead of `rm -rf "$DIR"/*`

---

### v1.1.0 (2026-01-01)
**Enhanced Deployment & Diagrams**

- Add `--deploy` flag for automated GitHub Pages deployment
- Add `--build` flag to run build after install
- Bundle GitHub Actions workflow (`.github/workflows/deploy.yml`)
- Add Mermaid diagram support (`@docusaurus/theme-mermaid`)
- Add example Mermaid diagrams in chapter templates
- Add `--no-workflow` and `--no-mermaid` flags to skip features

---

### v1.0.0 (2026-01-01)
**Initial Release**

- Docusaurus project scaffolding
- Physical AI textbook chapter structure
- i18n support (English + Urdu RTL)
- GitHub Pages deployment configuration
- Custom CSS for RTL languages
- Chapter templates with learning objectives
