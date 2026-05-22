---
name: github-actions
description: Create and configure GitHub Actions. Use when building custom actions, setting up runners, implementing security practices, or publishing to the marketplace.
---

# GitHub Actions

Activate when creating, modifying, troubleshooting, or optimizing GitHub Actions components. This skill covers action development, marketplace integration, and best practices.

## When to Use This Skill

Activate when:
- Creating custom GitHub Actions (JavaScript, Docker, or composite)
- Publishing actions to GitHub Marketplace
- Configuring action metadata and inputs/outputs
- Implementing action security and permissions
- Troubleshooting action execution
- Selecting or evaluating marketplace actions
- Optimizing action performance and reliability

## Action Types

### JavaScript Actions

Execute directly on runners with fast startup and cross-platform compatibility.

**Structure:**
```
my-action/
├── action.yml        # Metadata and interface
├── index.js          # Entry point
├── package.json      # Dependencies
└── node_modules/     # Bundled dependencies
```

**Key Requirements:**
- Use `@actions/core` for inputs/outputs
- Use `@actions/github` for GitHub API access
- Bundle all dependencies (use @vercel/ncc)
- Support Node.js LTS versions

**Example action.yml:**
```yaml
name: 'My JavaScript Action'
description: 'Performs custom task'
inputs:
  token:
    description: 'GitHub token'
    required: true
  config:
    description: 'Configuration file path'
    required: false
    default: 'config.yml'
outputs:
  result:
    description: 'Action result'
runs:
  using: 'node20'
  main: 'dist/index.js'
```

### Docker Container Actions

Provide consistent execution environment with all dependencies packaged.

**Structure:**
```
my-action/
├── action.yml
├── Dockerfile
├── entrypoint.sh
└── src/
```

**Key Requirements:**
- Use lightweight base images (Alpine when possible)
- Set proper file permissions
- Handle signals gracefully
- Output to STDOUT/STDERR correctly

**Example Dockerfile:**
```dockerfile
FROM alpine:3.18

RUN apk add --no-cache bash curl jq

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

### Composite Actions

Combine multiple steps and actions into reusable units.

**Structure:**
```yaml
name: 'Setup Environment'
description: 'Configure development environment'
inputs:
  node-version:
    description: 'Node.js version'
    required: false
    default: '20'
runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    - run: npm ci
      shell: bash
    - run: npm run build
      shell: bash
```

## Action Metadata (action.yml)

### Required Fields

```yaml
name: 'Action Name'           # Marketplace display name
description: 'What it does'   # Clear, concise purpose
runs:                         # Execution configuration
  using: 'node20'            # or 'docker' or 'composite'
```

### Optional Fields

```yaml
author: 'Your Name'
branding:                    # Marketplace icon/color
  icon: 'activity'
  color: 'blue'
inputs:                      # Define all inputs
  input-name:
    description: 'Purpose'
    required: true
    default: 'value'
outputs:                     # Define all outputs
  output-name:
    description: 'What it contains'
```

## Inputs and Outputs

### Reading Inputs

**JavaScript:**
```javascript
const core = require('@actions/core');
const token = core.getInput('token', { required: true });
const config = core.getInput('config') || 'default.yml';
```

**Shell:**
```bash
TOKEN="${{ inputs.token }}"
CONFIG="${{ inputs.config }}"
```

### Setting Outputs

**JavaScript:**
```javascript
core.setOutput('result', 'success');
core.setOutput('artifact-url', artifactUrl);
```

**Shell:**
```bash
echo "result=success" >> $GITHUB_OUTPUT
echo "artifact-url=$ARTIFACT_URL" >> $GITHUB_OUTPUT
```

## GitHub Actions Toolkit

Essential npm packages for JavaScript actions:

### @actions/core
```javascript
const core = require('@actions/core');

// Inputs/Outputs
const input = core.getInput('name');
core.setOutput('name', value);

// Logging
core.info('Information message');
core.warning('Warning message');
core.error('Error message');
core.debug('Debug message');

// Grouping
core.startGroup('Group name');
// ... operations
core.endGroup();

// Failure
core.setFailed('Action failed: reason');

// Secrets
core.setSecret('sensitive-value');  // Masks in logs

// Environment
core.exportVariable('VAR_NAME', 'value');
```

### @actions/github
```javascript
const github = require('@actions/github');

// Context
const context = github.context;
console.log(context.repo);        // { owner, repo }
console.log(context.sha);         // Commit SHA
console.log(context.ref);         // Branch/tag ref
console.log(context.actor);       // Triggering user
console.log(context.payload);     // Webhook payload

// Octokit client
const token = core.getInput('token');
const octokit = github.getOctokit(token);

// API operations
const { data: issues } = await octokit.rest.issues.listForRepo({
  owner: context.repo.owner,
  repo: context.repo.repo,
  state: 'open'
});
```

### @actions/exec
```javascript
const exec = require('@actions/exec');

// Execute commands
await exec.exec('npm', ['install']);

// Capture output
let output = '';
await exec.exec('git', ['log', '--oneline'], {
  listeners: {
    stdout: (data) => { output += data.toString(); }
  }
});
```

## Security Best Practices

### Input Validation

Always validate and sanitize inputs:
```javascript
const core = require('@actions/core');

function validateInput(input) {
  // Check for command injection
  if (/[;&|`$()]/.test(input)) {
    throw new Error('Invalid characters in input');
  }
  return input;
}

const userInput = core.getInput('user-input');
const safeInput = validateInput(userInput);
```

### Token Permissions

Request minimal required permissions:
```yaml
permissions:
  contents: read           # Read repository
  pull-requests: write     # Comment on PRs
  issues: write           # Create issues
```

### Secret Handling

```javascript
// Mask secrets in logs
core.setSecret(sensitiveValue);

// Never log tokens
core.debug(`Token: ${token}`);  // ❌ WRONG
core.debug('Token received');   // ✅ CORRECT

// Secure token usage
const octokit = github.getOctokit(token);
// Token automatically included in requests
```

### Dependency Security

```bash
# Audit dependencies
npm audit

# Use specific versions
npm install @actions/core@1.10.0

# Bundle dependencies
npm install -g @vercel/ncc
ncc build index.js -o dist
```

## Marketplace Publishing

### Prerequisites

- Public repository
- action.yml in repository root
- README.md with usage examples
- LICENSE file
- Repository topics (optional)

### Publishing Process

1. Create release with semantic version tag:
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

2. Create GitHub Release from tag
3. Check "Publish this Action to GitHub Marketplace"
4. Select primary category
5. Verify branding icon/color

### Version Management

Use semantic versioning with major version tags:
```bash
# Release v1.2.3
git tag -a v1.2.3 -m "Release v1.2.3"
git tag -fa v1 -m "Update v1 to v1.2.3"
git push origin v1.2.3 v1 --force
```

Users reference by major version:
```yaml
- uses: owner/action@v1  # Tracks latest v1.x.x
```

## Testing Actions Locally

Use `act` for local testing (see act skill):
```bash
# Test action in current directory
act -j test

# Test with specific event
act push

# Test with secrets
act -s GITHUB_TOKEN=ghp_xxx
```

## Common Patterns

### Matrix Testing Action

```yaml
# action.yml
name: 'Matrix Test Runner'
description: 'Run tests across multiple configurations'
inputs:
  matrix-config:
    description: 'JSON matrix configuration'
    required: true
runs:
  using: 'composite'
  steps:
    - run: |
        echo "Testing with config: ${{ inputs.matrix-config }}"
        # Parse and execute tests
      shell: bash
```

### Cache Management Action

```javascript
const core = require('@actions/core');
const cache = require('@actions/cache');

async function run() {
  const paths = [
    'node_modules',
    '.npm'
  ];

  const key = `deps-${process.platform}-${hashFiles('package-lock.json')}`;

  // Restore cache
  const cacheKey = await cache.restoreCache(paths, key);

  if (!cacheKey) {
    core.info('Cache miss, installing dependencies');
    await exec.exec('npm', ['ci']);
    await cache.saveCache(paths, key);
  } else {
    core.info(`Cache hit: ${cacheKey}`);
  }
}
```

### Artifact Upload Action

```javascript
const artifact = require('@actions/artifact');

async function uploadArtifact() {
  const artifactClient = artifact.create();
  const files = [
    'dist/bundle.js',
    'dist/styles.css'
  ];

  const rootDirectory = 'dist';
  const options = {
    continueOnError: false
  };

  const uploadResponse = await artifactClient.uploadArtifact(
    'build-artifacts',
    files,
    rootDirectory,
    options
  );

  core.setOutput('artifact-id', uploadResponse.artifactId);
}
```

## Troubleshooting

### Action Not Found

- Verify repository is public or accessible
- Check action.yml exists in repository root
- Confirm version tag exists

### Permission Denied

```yaml
# Add required permissions to workflow
permissions:
  contents: write
  pull-requests: write
```

### Node Modules Missing

- Bundle dependencies with ncc
- Check dist/ folder is committed
- Verify node_modules excluded from .gitignore for dist/

### Docker Action Fails

- Check Dockerfile syntax
- Verify entrypoint has execute permissions
- Test container locally: `docker build -t test . && docker run test`

## Anti-Fabrication Requirements

- Execute Read or Glob tools to verify action files exist before claiming structure
- Use Bash to test commands before documenting syntax
- Validate action.yml schema against actual files using tool analysis
- Execute actual API calls with @actions/github before documenting responses
- Test permission configurations in real workflows before recommending settings
- Never claim action capabilities without reading actual implementation code
- Report actual npm audit results when discussing security, not fabricated vulnerability counts
