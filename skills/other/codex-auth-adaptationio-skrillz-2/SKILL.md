---
name: codex-auth
description: Setup and manage OpenAI Codex CLI authentication including ChatGPT Plus/Pro OAuth, API keys, and multi-account management. Use when configuring Codex access, switching accounts, or troubleshooting authentication.
---

# Codex Authentication Management

Comprehensive authentication setup and management for OpenAI Codex CLI, supporting ChatGPT OAuth and API keys.

**Last Updated**: December 2025 (GPT-5.2 Release)

## Authentication Methods

### 1. ChatGPT Plus/Pro (Recommended)

**Benefits:**
- No API key management
- Includes GPT-5.1-Codex-Max and GPT-5.2 access
- 4x more usage with Codex-Mini
- Seamless browser authentication
- Automatic token refresh
- Access to GPT-5.2 Pro for maximum accuracy

```bash
# Initial login
codex login
# Opens browser for ChatGPT authentication

# Check login status
codex exec "Am I authenticated? What account am I using?"

# Logout
codex logout
```

### 2. API Key Setup

**Benefits:**
- Programmatic access
- No browser required
- Scriptable workflows
- CI/CD integration

```bash
# Method 1: Environment variable
export OPENAI_API_KEY="sk-your-api-key-here"

# Verify
codex exec "Test authentication"

# Method 2: Config file
mkdir -p ~/.codex
cat > ~/.codex/config.toml << 'EOF'
api_key = "sk-your-api-key-here"
EOF
chmod 600 ~/.codex/config.toml

# Method 3: Per-project config
mkdir -p .codex
echo 'api_key = "sk-project-specific-key"' > .codex/config.toml
echo '.codex/' >> .gitignore
```

## Authentication Configuration

### Priority Order

Codex checks authentication in this order:
1. Command-line config overrides (`-c api_key="..."`)
2. Environment variable `OPENAI_API_KEY`
3. Project config `.codex/config.toml`
4. User config `~/.codex/config.toml`
5. OAuth credentials (from `codex login`)

### Configuration File

```toml
# ~/.codex/config.toml

# API Key (alternative to OAuth)
api_key = "sk-your-api-key-here"

# Default model (December 2025)
model = "gpt-5.1-codex-max"  # Default for agentic coding
# Alternative models:
# model = "gpt-5.2"          # Latest general model (400K context)
# model = "gpt-5.2-pro"      # Maximum accuracy

# Default approval mode
ask_for_approval = "never"  # Full automation

# Default sandbox mode
sandbox = "workspace-write"

# Enable features
search = true

# Organization (if using organization API key)
organization = "org-your-org-id"

# GPT-5.2 specific settings
reasoning_effort = "high"  # medium, high, xhigh (Pro only)
compact = false            # Enable context compaction

# Additional settings
[features]
web_search = true
multimodal = true
mcp = true
```

## Multi-Account Management

### Switching Between Accounts

```bash
#!/bin/bash
# Switch between multiple OpenAI accounts

switch_codex_account() {
  local account=$1

  case $account in
    personal)
      unset OPENAI_API_KEY
      codex logout
      codex login
      echo "Switched to personal ChatGPT account"
      ;;

    work)
      export OPENAI_API_KEY="$(pass show openai/work-api-key)"
      echo "Switched to work API key"
      ;;

    project)
      # Use project-specific key from .codex/config.toml
      unset OPENAI_API_KEY
      echo "Using project config in .codex/config.toml"
      ;;

    ci)
      export OPENAI_API_KEY="$CI_OPENAI_API_KEY"
      echo "Switched to CI/CD API key"
      ;;

    *)
      echo "Unknown account: $account"
      echo "Available: personal, work, project, ci"
      return 1
      ;;
  esac

  # Verify authentication
  codex exec --dangerously-bypass-approvals-and-sandbox \
    "Confirm: What account am I using and what models are available?"
}

# Usage
switch_codex_account personal
```

### Automated Account Testing

```bash
#!/bin/bash
# Test all configured accounts

test_all_accounts() {
  for account in personal work project; do
    echo "=== Testing $account account ==="
    switch_codex_account "$account"

    if codex exec "Quick test: 2+2?" 2>/dev/null; then
      echo "✓ $account account working"
    else
      echo "✗ $account account failed"
    fi

    echo ""
  done
}

# Usage
test_all_accounts
```

## Secure API Key Storage

### Using pass (Password Store)

```bash
#!/bin/bash
# Secure API key management with pass

# Install pass
sudo apt-get install pass  # Debian/Ubuntu
brew install pass          # macOS

# Initialize pass
gpg --gen-key
pass init your-email@example.com

# Store API key
pass insert openai/personal-key
pass insert openai/work-key
pass insert openai/ci-key

# Use in scripts
export OPENAI_API_KEY="$(pass show openai/personal-key)"

# Verify
codex exec "Test authentication"
```

### Using macOS Keychain

```bash
#!/bin/bash
# Store in macOS Keychain

# Add API key
security add-generic-password \
  -a "$USER" \
  -s "openai-api-key" \
  -w "sk-your-api-key-here"

# Retrieve from keychain
export OPENAI_API_KEY="$(security find-generic-password -s 'openai-api-key' -w)"

# Use with Codex
codex exec "Verify authentication"
```

### Environment-Specific Keys

```bash
#!/bin/bash
# Use different keys for different environments

# Development
if [ "$ENV" = "development" ]; then
  export OPENAI_API_KEY="$DEV_OPENAI_KEY"
# Staging
elif [ "$ENV" = "staging" ]; then
  export OPENAI_API_KEY="$STAGING_OPENAI_KEY"
# Production
elif [ "$ENV" = "production" ]; then
  export OPENAI_API_KEY="$PROD_OPENAI_KEY"
fi

# Verify which environment
codex exec "What environment am I in based on my API key?"
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/codex-automation.yml
name: Codex Automation
on: [push, pull_request]

jobs:
  codex-analysis:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install Codex CLI
        run: npm install -g @openai/codex

      - name: Run Codex Analysis
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          codex exec --dangerously-bypass-approvals-and-sandbox \
            --json \
            "Analyze code quality, run tests, fix issues" \
            > analysis.json

      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: codex-analysis
          path: analysis.json
```

### Docker Integration

```dockerfile
# Dockerfile with Codex CLI
FROM node:20-alpine

# Install Codex CLI
RUN npm install -g @openai/codex

# Build-time API key (not recommended for production)
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Or mount config at runtime
# docker run -v ~/.codex:/root/.codex ...

WORKDIR /app
COPY . .

# Run Codex automation
CMD ["codex", "exec", "--dangerously-bypass-approvals-and-sandbox", "Analyze and improve code"]
```

### GitLab CI

```yaml
# .gitlab-ci.yml
codex_automation:
  image: node:20
  before_script:
    - npm install -g @openai/codex
  script:
    - >
      codex exec --dangerously-bypass-approvals-and-sandbox
      --json "Run comprehensive analysis"
      > analysis.json
  artifacts:
    paths:
      - analysis.json
  variables:
    OPENAI_API_KEY: $OPENAI_API_KEY  # Set in GitLab CI/CD settings
```

## Troubleshooting

### Debug Authentication

```bash
# Check current authentication
codex exec "What authentication method am I using?"

# Verify API key format
echo $OPENAI_API_KEY | grep -E '^sk-[a-zA-Z0-9]{48}$' && echo "Valid format" || echo "Invalid format"

# Test with simple prompt
codex exec --dangerously-bypass-approvals-and-sandbox "Echo: Authentication test"

# Check config file
cat ~/.codex/config.toml

# Verify environment
env | grep OPENAI
```

### Common Issues

**1. Authentication Failed**
```bash
# Clear stored credentials
codex logout
rm -rf ~/.codex/credentials

# Re-authenticate
codex login

# Or set API key
export OPENAI_API_KEY="sk-your-key"
```

**2. Invalid API Key**
```bash
# Verify key format (should start with sk-)
echo $OPENAI_API_KEY | cut -c1-3

# Test key directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq .

# Regenerate key at https://platform.openai.com/api-keys
```

**3. Rate Limiting**
```bash
# Check rate limits with headers
curl -I https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | grep -i rate

# Use organization API key for higher limits
# Set in ~/.codex/config.toml:
# organization = "org-your-org-id"
```

**4. Wrong Account**
```bash
# Check which account is active
codex exec "What account/organization am I using?"

# Switch accounts
codex logout
codex login  # Re-authenticate with correct account
```

## Security Best Practices

### API Key Security

```bash
# Never commit keys
echo '.codex/' >> .gitignore
echo '.env' >> .gitignore
echo '*.key' >> .gitignore

# Restrict file permissions
chmod 600 ~/.codex/config.toml

# Use environment variables in production
# Never hardcode keys in scripts

# Rotate keys regularly
rotate_api_key() {
  local old_key=$OPENAI_API_KEY

  echo "Visit https://platform.openai.com/api-keys to generate new key"
  read -p "Enter new API key: " new_key

  export OPENAI_API_KEY=$new_key

  if codex exec "Test new key"; then
    echo "New key works. Remember to revoke old key."
  else
    export OPENAI_API_KEY=$old_key
    echo "New key failed. Reverted to old key."
  fi
}
```

### Audit Logging

```bash
#!/bin/bash
# Log all Codex usage for audit trail

audit_codex() {
  local log_dir="~/.codex/audit"
  mkdir -p "$log_dir"

  local log_file="${log_dir}/$(date '+%Y-%m-%d').log"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  local user=$(whoami)

  # Determine auth method
  local auth_method="unknown"
  if [ -n "$OPENAI_API_KEY" ]; then
    auth_method="api_key"
  elif [ -f ~/.codex/credentials ]; then
    auth_method="oauth"
  fi

  # Log the operation
  echo "$timestamp | $user | $auth_method | $*" >> "$log_file"

  # Execute Codex
  codex "$@"
}

# Use instead of codex
alias codex='audit_codex'
```

### Least Privilege

```bash
# Create limited-scope API key for specific tasks
# Use organization settings to restrict:
# - Models available
# - Rate limits
# - Permissions

# In CI/CD, use minimal permissions
# Don't use personal API key in CI/CD

# Use different keys for different purposes:
# - Development key (higher limits, unrestricted)
# - CI/CD key (restricted, specific models only)
# - Production key (highly restricted)
```

## Configuration Profiles

```toml
# ~/.codex/config.toml with multiple profiles (December 2025)

# Default configuration
model = "gpt-5.1-codex-max"  # Best for agentic coding
ask_for_approval = "on-request"

# Safe profile for exploration
[profiles.safe]
model = "o4-mini"
ask_for_approval = "untrusted"
sandbox = "read-only"

# Development profile
[profiles.dev]
model = "gpt-5.1-codex-max"
ask_for_approval = "on-failure"
sandbox = "workspace-write"
search = true

# Full automation profile
[profiles.auto]
model = "gpt-5.1-codex-max"
ask_for_approval = "never"
sandbox = "danger-full-access"
search = true

# CI/CD profile
[profiles.ci]
model = "gpt-5.1-codex-mini"  # Cost-efficient
ask_for_approval = "never"
sandbox = "workspace-write"

# GPT-5.2 profiles (NEW December 2025)
[profiles.gpt52]
model = "gpt-5.2"
ask_for_approval = "never"
sandbox = "workspace-write"
search = true

[profiles.gpt52-pro]
model = "gpt-5.2-pro"
reasoning_effort = "xhigh"
ask_for_approval = "on-request"
sandbox = "workspace-write"

[profiles.long-context]
model = "gpt-5.2"
compact = true  # Enable context compaction for 400K context
ask_for_approval = "never"
```

## Usage with Profiles

```bash
# Use profile
codex exec -p dev "Develop new feature"

# Override profile settings
codex exec -p auto -m o3 "Complex task with reasoning"

# Per-project profile
# .codex/config.toml
[profiles.project]
model = "gpt-5.1-codex"
api_key = "sk-project-specific-key"
```

## Related Skills

- `codex-cli`: Main Codex CLI integration
- `codex-chat`: Interactive workflows
- `codex-tools`: Tool execution patterns
- `codex-review`: Code review workflows
- `codex-git`: Git-aware development

## Updates

```bash
# Update Codex CLI
npm update -g @openai/codex

# Check version
codex --version

# Test authentication after update
codex exec "Authentication test after update"
```
