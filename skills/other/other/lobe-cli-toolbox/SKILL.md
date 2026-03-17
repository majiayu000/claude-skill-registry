---
name: lobe-cli-toolbox
version: "1.0.0"
description: LobeHub CLI Toolbox - AI-powered command-line tools including lobe-commit (ChatGPT Git commits with Gitmoji), lobe-i18n (automated internationalization), and lobe-label (GitHub label management)
---

# LobeHub CLI Toolbox

AI CLI Toolbox containing multiple command-line tools powered by ChatGPT/LangChain for enhancing git commit and i18n workflow efficiency.

## When to Use

- Generating conventional commit messages with AI and Gitmoji
- Setting up automated Git commit hooks
- Automating internationalization translation workflows
- Translating JSON locale files to multiple languages
- Translating Markdown documentation files
- Copying GitHub issue labels between repositories
- Building CLI applications with React-based terminal UIs

## Core Tools

### 1. Lobe Commit (`@lobehub/commit-cli`)

AI-powered Git commit message generator using ChatGPT with Gitmoji formatting.

### 2. Lobe i18n (`@lobehub/i18n-cli`)

Automated internationalization tool leveraging ChatGPT for translation workflows.

### 3. Lobe Label (`@lobehub/label-cli`)

GitHub issue label management - copy labels from template repositories.

### 4. Supporting Libraries

- `@lobehub/cli-ui` - UI components for CLI applications
- `@lobehub/cli-shebang` - Shebang handling utilities

---

## Lobe Commit

### Installation

```bash
npm install -g @lobehub/commit-cli
```

**Requirement**: Node.js ≥ 18

### Commands

| Command | Flag | Purpose |
|---------|------|---------|
| Interactive commit | `--hook` | Generate message via prompts |
| AI generation | `-a, --ai` | Use ChatGPT for auto-generation |
| Configuration | `-o, --option` | Setup preferences |
| Git hook setup | `-i, --init` | Initialize as commit hook |
| Remove hook | `-r, --remove` | Uninstall commit hook |
| List types | `-l, --list` | Display supported commit types |
| Version | `-V, --version` | Show installed version |
| Help | `-h, --help` | Display basic options |

### Basic Usage

```bash
# Stage files and generate commit
git add <files>
lobe-commit

# Or use the short alias
lobe

# Set up as git hook
lobe-commit --init
git commit  # Triggers workflow automatically
```

### Configuration

Access settings via:
```bash
lobe-commit --option
```

**Key Settings:**
- OpenAI Token (required for AI mode)
- GitHub Token (for private repo issue linking)
- API Forwarding (custom OpenAI endpoints)

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `includeWhy` | boolean | false | Explain change motivations |
| `messageTemplate` | string | "$msg" | Custom message format |
| `oneLineCommit` | boolean | false | Single-line output |
| `useFullGitmoji` | boolean | false | Full emoji specification |

### File Filtering

Create `.lobecommitignore` to exclude files from analysis:

```gitignore
# Lock files
package-lock.json
yarn.lock
pnpm-lock.yaml

# Build artifacts
dist/
build/

# Minified files
*.min.js
*.min.css
```

Default filters include: lock files, binaries, build artifacts, minified files.

### Message Templates

Use placeholders for customization:
```bash
# Link to issue number
"$msg (#123)"

# Add scope prefix
"[frontend] $msg"
```

### Operating Modes

**AI Mode**: ChatGPT generates complete conventional commit messages with Gitmoji

**Editor Mode**: Interactive prompts guide selection of:
- Commit type
- Scope
- Subject
- Linked issues

### Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | Yes (AI mode) | OpenAI authentication |
| `GITHUB_TOKEN` | No | Private repo issue linking |

---

## Lobe i18n

### Installation

```bash
npm install -g @lobehub/i18n-cli
```

**Requirement**: Node.js ≥ 18

### Commands

| Command | Purpose |
|---------|---------|
| `lobe-i18n` | Translate locale/JSON files |
| `lobe-i18n locale` | Same as above |
| `lobe-i18n md` | Translate Markdown files |
| `lobe-i18n lint` | Validate translation accuracy |
| `lobe-i18n --with-md` | Run locale and markdown translation together |
| `lobe-i18n -o` | Interactive configuration setup |
| `lobe-i18n -c ./config.js` | Use custom configuration file |

### Configuration Setup

Run interactive setup:
```bash
lobe-i18n -o
```

Or create config file manually (supports cosmiconfig):
- `package.json` (under `i18n` property)
- `.i18nrc`, `.i18nrc.json`, `.i18nrc.yaml`
- `.i18nrc.js`, `.i18nrc.cjs`

### Locale Configuration

```javascript
const { defineConfig } = require('@lobehub/i18n-cli');

module.exports = defineConfig({
  // Required
  entry: 'locales/en_US.json',
  entryLocale: 'en_US',
  output: 'locales',
  outputLocales: ['zh_CN', 'ja_JP', 'ko_KR'],

  // Optional
  modelName: 'gpt-3.5-turbo',
  keyStyle: 'nested',  // 'nested', 'flat', or 'auto'
  reference: 'Technical documentation context',
  saveImmediately: true,
  temperature: 0,
  topP: 1,
  concurrency: 5,
  splitToken: 2000,
  experimental: {
    jsonMode: true
  }
});
```

### Configuration Properties

**Required:**
| Property | Type | Description |
|----------|------|-------------|
| `entry` | string | Source file/folder path |
| `entryLocale` | string | Reference language identifier |
| `output` | string | Destination directory |
| `outputLocales` | string[] | Target language array |

**Optional:**
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `modelName` | string | `gpt-3.5-turbo` | AI model selection |
| `keyStyle` | string | `auto` | Key resolution style |
| `reference` | string | - | Context for translations |
| `saveImmediately` | boolean | false | Persist after each chunk |
| `temperature` | number | 0 | Sampling parameter |
| `topP` | number | 1 | Nucleus sampling threshold |
| `concurrency` | number | 5 | Parallel request limit |
| `splitToken` | number | - | Token split threshold |

### Markdown Configuration

```javascript
module.exports = defineConfig({
  // Entry/Output
  entry: 'docs/**/*.md',
  entryLocale: 'en_US',
  entryExtension: '.md',
  outputLocales: ['zh_CN', 'ja_JP'],
  outputExtensions: (locale) => `.${locale}.md`,

  // Processing
  mode: 'mdast',  // 'string' or 'mdast'
  translateCode: false,
  includeMatter: false,
  exclude: ['node_modules/**', 'dist/**']
});
```

### File Structure Patterns

**Flat Structure:**
```
locales/
├── en_US.json
├── zh_CN.json
└── ja_JP.json
```

Configuration: `entry: "locales/en_US.json"`

**Tree Structure:**
```
locales/
├── en_US/
│   ├── common.json
│   └── header.json
├── zh_CN/
└── ja_JP/
```

Configuration: `entry: "locales/en_US"`

### Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | Yes | OpenAI authentication token |
| `OPENAI_PROXY_URL` | No | API proxy endpoint |

Default proxy: `https://api.openai.com/v1`

### Key Features

- Automatic file splitting (no token limit concerns)
- Incremental updates (only new content)
- Single-file and folder organizational modes
- Flat and tree-structured locale support
- Customizable model, proxy, temperature settings
- Markdown file translation
- Translation quality linting

---

## Lobe Label

### Installation

```bash
npm install -g @lobehub/label-cli
```

**Requirement**: Node.js ≥ 18

### Commands

| Option | Short | Purpose |
|--------|-------|---------|
| `--config` | `-o` | Initialize configuration |
| `--target` | `-t` | Destination repository |
| `--source` | `-s` | Source repository |

**Default source**: `canisminor1990/canisminor-template`

### Usage Examples

```bash
# Copy from default template to target
lobe-label -t lobehub/chat

# Copy from custom source to target
lobe-label -t lobehub/chat -s lobehub/commit

# Configure settings
lobe-label --config
```

---

## Technical Stack

- **Language**: TypeScript (96.4%)
- **Package Manager**: Bun (recommended)
- **Workspace**: pnpm monorepo structure
- **Key Dependencies**: LangChain.js, Ink (React for terminal UIs)

## Project Statistics

- 383 GitHub stars
- 60 forks
- MIT licensed
- 421 commits
- 15 contributors
- 143 releases

---

## Complete Workflow Examples

### Example 1: AI-Powered Commit Workflow

```bash
# Initial setup
npm install -g @lobehub/commit-cli

# Configure OpenAI
lobe-commit --option
# Enter your OPENAI_API_KEY

# Set up as git hook
lobe-commit --init

# Normal git workflow
git add .
git commit
# AI generates: ✨ feat(auth): add OAuth2 login support
```

### Example 2: Internationalization Workflow

```bash
# Install
npm install -g @lobehub/i18n-cli

# Create config
cat > .i18nrc.json << 'EOF'
{
  "entry": "locales/en_US.json",
  "entryLocale": "en_US",
  "output": "locales",
  "outputLocales": ["zh_CN", "ja_JP", "ko_KR", "de_DE"],
  "modelName": "gpt-4",
  "concurrency": 3
}
EOF

# Set API key
export OPENAI_API_KEY=sk-...

# Run translation
lobe-i18n

# Translate markdown docs too
lobe-i18n md

# Validate translations
lobe-i18n lint
```

### Example 3: GitHub Label Management

```bash
# Install
npm install -g @lobehub/label-cli

# Copy labels from template to new repo
lobe-label -t myorg/new-project

# Copy labels from existing repo to another
lobe-label -s lobehub/lobe-chat -t myorg/new-project
```

### Example 4: Full Project Setup

```bash
# Install all tools
npm install -g @lobehub/commit-cli @lobehub/i18n-cli @lobehub/label-cli

# Initialize new project
mkdir my-project && cd my-project
git init

# Set up commit hooks
lobe-commit --init

# Configure i18n
lobe-i18n -o

# Copy labels from template
lobe-label -t myorg/my-project
```

---

## CLI UI Components

For building your own CLI tools, use `@lobehub/cli-ui`:

```typescript
import { Header, Panel, Spinner } from '@lobehub/cli-ui';
import { render } from 'ink';

// React-based terminal UI
render(
  <Panel>
    <Header title="My CLI Tool" />
    <Spinner text="Processing..." />
  </Panel>
);
```

---

## Development Setup

```bash
# Clone repository
git clone https://github.com/lobehub/lobe-cli-toolbox.git
cd lobe-cli-toolbox

# Install dependencies (bun recommended)
bun install

# Work on specific package
cd packages/lobe-commit
bun dev

# Or use pnpm
pnpm install
pnpm dev
```

---

## Migration Notes

### From OpenCommit to Lobe Commit

Rename configuration file:
```bash
mv .opencommitignore .lobecommitignore
```

Most settings transfer directly.

---

## Resources

- **Repository**: https://github.com/lobehub/lobe-cli-toolbox
- **NPM Packages**:
  - [@lobehub/commit-cli](https://www.npmjs.com/package/@lobehub/commit-cli)
  - [@lobehub/i18n-cli](https://www.npmjs.com/package/@lobehub/i18n-cli)
  - [@lobehub/label-cli](https://www.npmjs.com/package/@lobehub/label-cli)
  - [@lobehub/cli-ui](https://www.npmjs.com/package/@lobehub/cli-ui)
- **License**: MIT
- **Author**: LobeHub

---

## Troubleshooting

### Common Issues

**"OPENAI_API_KEY not found"**
```bash
export OPENAI_API_KEY=sk-your-key-here
# Or configure via tool
lobe-commit --option
lobe-i18n -o
```

**"Rate limit exceeded"**
- Reduce concurrency in i18n config
- Use `gpt-3.5-turbo` instead of `gpt-4`

**"Token limit exceeded"**
- Tool automatically splits large files
- Adjust `splitToken` if needed

**Git hook not triggering**
```bash
# Reinstall hook
lobe-commit --remove
lobe-commit --init
```

**Custom API endpoint**
```bash
export OPENAI_PROXY_URL=https://your-proxy.com/v1
```
