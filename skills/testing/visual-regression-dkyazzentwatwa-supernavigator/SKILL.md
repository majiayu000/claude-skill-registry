---
name: visual-regression
description: Setup visual regression testing with Storybook stories, configuration, and CI/CD workflows. Supports Chromatic, Percy, BackstopJS. Auto-invoke when user says "set up visual regression", "add Chromatic tests", "add screenshot testing", or "set up Percy".
allowed-tools: Read, Write, Bash, Glob
version: 1.0.0
triggers:
  - "set up visual regression"
  - "add chromatic tests"
  - "create visual tests"
  - "configure visual regression"
  - "add screenshot testing"
  - "set up percy"
  - "add backstopjs"
---

# Visual Regression Testing Setup Skill

---

## Skill Purpose

Generate complete visual regression testing setup with Storybook stories, configuration files, and CI/CD workflows.

**Supports**: Chromatic, Percy, BackstopJS
**Frameworks**: React, Vue, Svelte (TypeScript/JavaScript)
**CI/CD**: GitHub Actions, GitLab CI, CircleCI

---

## What This Skill Does

1. **Detects existing setup**: Storybook version, VR tool, CI platform
2. **Validates component**: Extract props, variants, states
3. **Generates stories**: Complete `.stories.tsx` with all variants
4. **Creates config files**: Chromatic, Percy, or BackstopJS configuration
5. **Sets up CI/CD**: Auto-generate workflow files
6. **Provides instructions**: Next steps for API tokens, first baseline

---

## Workflow

### Step 1: Validate Project Setup

**Execute**: `vr_setup_validator.py`

**Check**:
- Framework (React/Vue/Svelte) from package.json
- Existing Storybook config (.storybook/ directory)
- Existing VR tool (chromatic, percy, backstopjs in dependencies)
- CI platform (.github/, .gitlab-ci.yml, .circleci/)
- Component file exists and is valid

**Output**:
```json
{
  "framework": "react",
  "storybook_version": "7.6.0",
  "vr_tool": "chromatic",
  "ci_platform": "github",
  "component": {
    "path": "src/components/ProfileCard.tsx",
    "name": "ProfileCard",
    "props": [...],
    "valid": true
  },
  "dependencies": {
    "installed": ["@storybook/react", "@storybook/addon-essentials"],
    "missing": ["chromatic", "@chromatic-com/storybook"]
  }
}
```

**If Storybook not found**: Ask user if they want to install Storybook first, provide setup instructions.

**If multiple VR tools found**: Ask user which to use (Chromatic recommended).

---

### Step 2: Generate Storybook Stories

**Execute**: `story_generator.py`

**Process**:
1. Parse component file (TypeScript/JSX/Vue SFC)
2. Extract props, prop types, default values
3. Identify variants (size, variant, disabled, etc.)
4. Generate story file from template
5. Add accessibility tests (@storybook/addon-a11y)
6. Add interaction tests (if @storybook/test available)

**Template**: `templates/story-template.tsx.j2`

**Example output** (`ProfileCard.stories.tsx`):
```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { ProfileCard } from './ProfileCard';

const meta = {
  title: 'Components/ProfileCard',
  component: ProfileCard,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    size: { control: 'select', options: ['sm', 'md', 'lg'] },
    variant: { control: 'select', options: ['default', 'compact'] },
  },
} satisfies Meta<typeof ProfileCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    name: 'John Doe',
    avatar: 'https://example.com/avatar.jpg',
    bio: 'Software Engineer',
    size: 'md',
    variant: 'default',
  },
};

export const Small: Story = {
  args: {
    ...Default.args,
    size: 'sm',
  },
};

export const Large: Story = {
  args: {
    ...Default.args,
    size: 'lg',
  },
};

export const Compact: Story = {
  args: {
    ...Default.args,
    variant: 'compact',
  },
};

// Accessibility test
Default.parameters = {
  a11y: {
    config: {
      rules: [
        { id: 'color-contrast', enabled: true },
        { id: 'label', enabled: true },
      ],
    },
  },
};
```

**Write to**: `{component_directory}/{ComponentName}.stories.tsx`

---

### Step 3: Generate Configuration Files

**Execute**: `chromatic_config_generator.py` (or percy/backstop equivalent)

#### For Chromatic:

**Generate 3 files**:

1. **chromatic.config.json**:
```json
{
  "projectId": "<PROJECT_ID_PLACEHOLDER>",
  "buildScriptName": "build-storybook",
  "exitZeroOnChanges": true,
  "exitOnceUploaded": true,
  "onlyChanged": true,
  "externals": ["public/**"],
  "skip": "dependabot/**",
  "ignoreLastBuildOnBranch": "main"
}
```

2. **Update .storybook/main.js** (add addon):
```javascript
module.exports = {
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@chromatic-com/storybook', // ← Added
    '@storybook/addon-interactions',
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
};
```

3. **Update package.json** (add scripts):
```json
{
  "scripts": {
    "chromatic": "npx chromatic",
    "chromatic:ci": "npx chromatic --exit-zero-on-changes"
  }
}
```

**For Percy**: Generate `.percy.yml` instead
**For BackstopJS**: Generate `backstop.config.js` instead

---

### Step 4: Generate CI/CD Workflow

**Execute**: `ci_workflow_generator.py`

**Detect CI platform** from existing files:
- `.github/workflows/` → GitHub Actions
- `.gitlab-ci.yml` → GitLab CI
- `.circleci/config.yml` → CircleCI
- None → Ask user, default to GitHub Actions

#### GitHub Actions Example:

**Generate**: `.github/workflows/chromatic.yml`

```yaml
name: Visual Regression Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Required for Chromatic

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run Chromatic
        uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          exitZeroOnChanges: true
          onlyChanged: true
```

**For GitLab CI**: Add job to `.gitlab-ci.yml`
**For CircleCI**: Add job to `.circleci/config.yml`

---

### Step 5: Provide Setup Instructions

**Output to user**:

````markdown
✅ Visual regression testing setup complete!

## Files Created/Modified

✅ {ComponentName}.stories.tsx (Storybook story with variants)
✅ chromatic.config.json (Chromatic configuration)
✅ .storybook/main.js (Added @chromatic-com/storybook addon)
✅ package.json (Added chromatic scripts)
✅ .github/workflows/chromatic.yml (CI workflow)

## Next Steps

### 1. Install Dependencies

```bash
npm install --save-dev chromatic @chromatic-com/storybook
```

### 2. Create Chromatic Project

1. Go to https://www.chromatic.com/start
2. Sign in with GitHub
3. Create new project
4. Copy project token

### 3. Add Secret to GitHub

1. Go to repository Settings → Secrets and variables → Actions
2. Create secret: `CHROMATIC_PROJECT_TOKEN`
3. Paste your project token

### 4. Update chromatic.config.json

Replace `<PROJECT_ID_PLACEHOLDER>` with your actual project ID from Chromatic dashboard.

### 5. Create Baseline

```bash
npm run chromatic
```

This captures the initial screenshots as your baseline.

### 6. Test Visual Regression

1. Make a visual change to ProfileCard
2. Commit and push
3. CI will run Chromatic automatically
4. Review changes in Chromatic dashboard

## Documentation

See `.agent/sops/testing/visual-regression-setup.md` for detailed workflow.

## Troubleshooting

**Storybook build fails**: Ensure all component dependencies are installed
**Chromatic upload fails**: Check project token in secrets
**No changes detected**: Chromatic only runs on changed stories (use `--force-rebuild` to test)
````

---

## Predefined Functions Reference

### vr_setup_validator.py

```python
def detect_storybook_config(project_root: str) -> dict
def detect_vr_tool(project_root: str) -> str
def validate_component_path(component_path: str) -> dict
def check_dependencies(project_root: str) -> dict
```

**Returns**: Validation report with detected setup and missing dependencies

### story_generator.py

```python
def analyze_component(component_path: str, framework: str) -> dict
def generate_story(component_info: dict, template_path: str) -> str
def create_accessibility_tests(component_info: dict) -> str
def create_interaction_tests(component_info: dict) -> str
```

**Returns**: Generated story file content

### chromatic_config_generator.py

```python
def generate_chromatic_config(project_info: dict) -> str
def generate_storybook_config(existing_config: dict) -> str
def generate_package_scripts(existing_scripts: dict) -> dict
def generate_percy_config(project_info: dict) -> str  # Percy alternative
def generate_backstop_config(project_info: dict) -> str  # BackstopJS alternative
```

**Returns**: Configuration file contents as strings

### ci_workflow_generator.py

```python
def detect_ci_platform(project_root: str) -> str
def generate_github_workflow(project_info: dict) -> str
def generate_gitlab_ci(project_info: dict) -> str
def generate_circleci_config(project_info: dict) -> str
```

**Returns**: CI workflow file contents

---

## Templates Reference

- **story-template.tsx.j2**: React/TypeScript story template
- **story-template.vue.j2**: Vue SFC story template
- **chromatic-config.json.j2**: Chromatic configuration
- **percy-config.yml.j2**: Percy configuration
- **github-workflow.yml.j2**: GitHub Actions workflow
- **gitlab-ci.yml.j2**: GitLab CI job
- **storybook-main.js.j2**: Storybook addon configuration

---

## Examples

### Example 1: Simple Component

```
User: "Set up visual regression for ProfileCard component"

→ Detects: React, existing Storybook, no VR tool
→ Generates: ProfileCard.stories.tsx with 4 variants
→ Creates: Chromatic config, GitHub workflow
→ Outputs: Setup instructions
```

See: `examples/simple-component-vr.md`

### Example 2: Full Design System

```
User: "Set up visual regression for entire design system"

→ Detects: React, Storybook, components in src/components/
→ Generates: Stories for all components (Button, Input, Card, etc.)
→ Creates: Chromatic config with design token validation
→ Outputs: Bulk setup instructions
```

See: `examples/design-system-vr.md`

### Example 3: Existing Storybook

```
User: "Add Chromatic to existing Storybook"

→ Detects: Storybook v7, existing stories
→ Adds: @chromatic-com/storybook addon
→ Creates: Chromatic config, CI workflow
→ Preserves: Existing stories and configuration
```

See: `examples/existing-storybook-vr.md`

---

## Integration with product-design Skill

After `product-design` generates implementation plan, suggest visual regression:

```
"Implementation plan created! Consider setting up visual regression testing:

  'Set up visual regression for {ComponentName}'

This ensures pixel-perfect implementation and prevents visual drift."
```

---

## Tool Comparison

### Chromatic (Recommended)
- ✅ Purpose-built for Storybook
- ✅ Component-focused testing
- ✅ UI review workflow
- ✅ Free tier: 5,000 snapshots/month
- ❌ Requires cloud service

### Percy
- ✅ Multi-framework support
- ✅ Responsive testing
- ✅ Visual reviews
- ❌ More expensive
- ❌ Less Storybook-specific

### BackstopJS
- ✅ Open source, self-hosted
- ✅ No cloud dependency
- ✅ Free
- ❌ More manual setup
- ❌ Less automation

**Default**: Chromatic (best Storybook integration)

---

## Error Handling

### Component Not Found
```
Error: Component file not found at {path}

Please provide correct path:
  "Set up visual regression for src/components/ProfileCard.tsx"
```

### Storybook Not Installed
```
Storybook not detected. Install first:

  npm install --save-dev @storybook/react @storybook/addon-essentials
  npx storybook init

Then retry: "Set up visual regression for ProfileCard"
```

### Multiple VR Tools Detected
```
Multiple VR tools found: chromatic, percy

Which should I use?
  - "Use Chromatic for visual regression"
  - "Use Percy for visual regression"
```

---

## Best Practices

1. **Start with key components**: Don't test everything, focus on design system primitives
2. **Use interaction tests**: Combine visual + functional testing
3. **Baseline on main**: Always merge baselines to main branch
4. **Review changes**: Don't auto-accept visual changes
5. **Test states**: Capture hover, focus, error states
6. **Accessibility**: Include a11y tests in all stories

---

## Token Efficiency

**Traditional approach** (50k tokens):
1. Read Storybook docs (20k)
2. Read Chromatic docs (15k)
3. Write stories manually (10k)
4. Configure CI (5k)

**With visual-regression skill** (3k tokens):
1. Skill auto-invokes (0 tokens)
2. Instructions load (3k tokens)
3. Functions execute (0 tokens)

**Savings**: 94% (47k tokens)

---

## Version History

- **v3.3.0**: Initial release with Chromatic support
- **Future**: Percy, BackstopJS, Vue, Svelte support

---

**Last Updated**: 2025-10-21
**Skill Type**: Project-specific
**Generator**: nav-skill-creator (self-improving)
