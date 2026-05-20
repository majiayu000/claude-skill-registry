---
name: gemini-auth
description: Setup and manage Gemini CLI authentication methods including OAuth, API keys, and Vertex AI. Use when configuring Gemini access, switching auth methods, or troubleshooting authentication issues.
---

# Gemini Authentication Management

Comprehensive authentication setup and management for Gemini CLI, supporting OAuth, API keys, and Vertex AI.

## Authentication Methods

### 1. Google OAuth (Free Tier)

**Benefits:**
- No API key management
- 60 requests/minute
- 1,000 requests/day
- Access to Gemini 2.5 Pro
- 1M token context window

```bash
# Initial setup
gemini
# Opens browser for Google account login

# Check auth status
gemini auth status

# Refresh token
gemini auth refresh

# Logout
gemini auth logout
```

### 2. API Key Setup

**Benefits:**
- Programmatic access
- No browser required
- Scriptable workflows

```bash
# Get API key from https://aistudio.google.com/

# Method 1: Environment variable
export GEMINI_API_KEY="your-api-key-here"

# Method 2: User config file
mkdir -p ~/.gemini
echo 'GEMINI_API_KEY="your-api-key-here"' > ~/.gemini/.env
chmod 600 ~/.gemini/.env

# Method 3: Project config
mkdir -p ./.gemini
echo 'GEMINI_API_KEY="your-api-key-here"' > ./.gemini/.env
echo '.gemini/' >> .gitignore

# Verify (auto-execute test)
gemini --yolo -p "Test authentication and report status"
```

### 3. Vertex AI (Enterprise)

**Benefits:**
- Enterprise security
- Higher rate limits
- Advanced features
- Service account support

```bash
# Setup Google Cloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Configure project
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"

# Service account setup
gcloud iam service-accounts create gemini-cli \
  --display-name="Gemini CLI Service Account"

gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
  --member="serviceAccount:gemini-cli@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud iam service-accounts keys create ~/gemini-sa-key.json \
  --iam-account=gemini-cli@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com

export GOOGLE_APPLICATION_CREDENTIALS="~/gemini-sa-key.json"

# Test connection (auto-execute)
gemini --yolo -p "Test Vertex AI authentication and report project details"
```

## Authentication Configuration

### Priority Order

Gemini CLI checks authentication in this order:
1. Command-line flags
2. Environment variables
3. Project .gemini/.env
4. User ~/.gemini/.env
5. OAuth tokens
6. Interactive prompt

### Configuration File

```json
// ~/.gemini/config.json
{
  "auth": {
    "method": "oauth",  // oauth, apikey, vertex
    "autoRefresh": true,
    "timeout": 30000
  },
  "apiKey": {
    "source": "env",  // env, file, prompt
    "envVar": "GEMINI_API_KEY",
    "filePath": "~/.gemini/.env"
  },
  "vertex": {
    "project": "auto",  // auto, specific-project-id
    "location": "us-central1",
    "credentials": "auto"  // auto, path/to/key.json
  }
}
```

## Workflow Scripts

### Multi-Account Management

```bash
#!/bin/bash
# Switch between multiple accounts

switch_gemini_account() {
  local account=$1
  
  case $account in
    personal)
      unset GEMINI_API_KEY
      unset GOOGLE_APPLICATION_CREDENTIALS
      gemini auth logout
      gemini  # Trigger OAuth
      ;;
    
    work)
      export GEMINI_API_KEY="$(pass show gemini/work-api-key)"
      unset GOOGLE_APPLICATION_CREDENTIALS
      ;;
    
    enterprise)
      unset GEMINI_API_KEY
      export GOOGLE_CLOUD_PROJECT="company-project"
      export GOOGLE_APPLICATION_CREDENTIALS="~/keys/company-sa.json"
      ;;
    
    *)
      echo "Unknown account: $account"
      echo "Available: personal, work, enterprise"
      return 1
      ;;
  esac
  
  echo "Switched to $account account"
  # Auto-validate authentication with YOLO mode
  gemini --yolo -p "Test authentication and report current auth method and quota status"
}

# Automated account testing
test_all_accounts() {
  for account in personal work enterprise; do
    echo "Testing $account account..."
    switch_gemini_account "$account"
    gemini --yolo -p "Quick test: what is 2+2? Also report account type and remaining quota."
  done
}

# Usage
switch_gemini_account personal
```

### Secure API Key Storage

```bash
#!/bin/bash
# Secure API key management with pass

# Install pass (password store)
sudo apt-get install pass  # Debian/Ubuntu
brew install pass          # macOS

# Initialize pass
gpg --gen-key
pass init your-email@example.com

# Store API key securely
pass insert gemini/api-key

# Use in scripts
export GEMINI_API_KEY="$(pass show gemini/api-key)"

# Or with keychain (macOS)
security add-generic-password \
  -a "$USER" \
  -s "gemini-api-key" \
  -w "your-api-key-here"

# Retrieve from keychain
export GEMINI_API_KEY="$(security find-generic-password -s 'gemini-api-key' -w)"
```

### Rate Limit Management

```bash
#!/bin/bash
# Handle rate limits gracefully

gemini_with_retry() {
  local prompt="$1"
  local use_yolo="${2:-false}"
  local max_retries=3
  local retry_delay=60
  
  local yolo_flag=""
  if [ "$use_yolo" = "true" ]; then
    yolo_flag="--yolo"
  fi
  
  for i in $(seq 1 $max_retries); do
    if gemini $yolo_flag -p "$prompt"; then
      return 0
    else
      if [ $i -lt $max_retries ]; then
        echo "Rate limited. Waiting ${retry_delay}s before retry $((i+1))/${max_retries}..."
        sleep $retry_delay
        retry_delay=$((retry_delay * 2))  # Exponential backoff
      fi
    fi
  done
  
  echo "Failed after $max_retries retries"
  return 1
}

# YOLO-enabled retry for automated workflows
gemini_yolo_retry() {
  local prompt="$1"
  gemini_with_retry "$prompt" true
}

# Track usage
track_gemini_usage() {
  local log_file="~/.gemini/usage.log"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  echo "$timestamp - Request made" >> "$log_file"
  
  # Count today's requests
  local today=$(date '+%Y-%m-%d')
  local count=$(grep "$today" "$log_file" | wc -l)
  
  echo "Requests today: $count/1000"
  
  if [ $count -ge 950 ]; then
    echo "WARNING: Approaching daily limit!"
  fi
}
```

## Troubleshooting

### Debug Authentication

```bash
# Enable debug mode
export GEMINI_DEBUG=true

# Check all auth sources
gemini auth debug

# Test each method
gemini auth test oauth
gemini auth test apikey
gemini auth test vertex
```

### Common Issues

1. **OAuth Token Expired**
```bash
rm -rf ~/.gemini/auth/tokens
gemini auth refresh
```

2. **API Key Not Found**
```bash
# Check environment
echo $GEMINI_API_KEY

# Check files
cat ~/.gemini/.env
cat ./.gemini/.env

# Validate key
curl -H "x-api-key: $GEMINI_API_KEY" \
  https://generativelanguage.googleapis.com/v1/models
```

3. **Vertex AI Permissions**
```bash
# Check service account
gcloud auth list

# Verify roles
gcloud projects get-iam-policy $GOOGLE_CLOUD_PROJECT \
  --flatten="bindings[].members" \
  --filter="bindings.members:gemini-cli@"

# Test API access
gcloud ai models list --region=$GOOGLE_CLOUD_LOCATION
```

## Security Best Practices

### API Key Security

```bash
# Never commit keys
echo '.env' >> .gitignore
echo '.gemini/' >> .gitignore
echo '*.key' >> .gitignore
echo '*.json' >> .gitignore  # For service account keys

# Use environment-specific keys
if [ "$ENV" = "production" ]; then
  export GEMINI_API_KEY="$PROD_GEMINI_KEY"
else
  export GEMINI_API_KEY="$DEV_GEMINI_KEY"
fi

# Rotate keys regularly
rotate_api_key() {
  local old_key=$GEMINI_API_KEY
  local new_key=$(generate_new_key)  # Your key generation
  
  export GEMINI_API_KEY=$new_key
  
  if gemini -p "Test new key"; then
    revoke_old_key $old_key
    echo "Key rotated successfully"
  else
    export GEMINI_API_KEY=$old_key
    echo "Rotation failed, reverting"
  fi
}
```

### Audit Logging

```bash
#!/bin/bash
# Log all Gemini CLI usage

audit_gemini() {
  local log_dir="~/.gemini/audit"
  mkdir -p "$log_dir"
  
  local log_file="${log_dir}/$(date '+%Y-%m-%d').log"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  local user=$(whoami)
  local auth_method="unknown"
  
  if [ -n "$GEMINI_API_KEY" ]; then
    auth_method="apikey"
  elif [ -n "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    auth_method="vertex"
  elif [ -f "~/.gemini/auth/tokens" ]; then
    auth_method="oauth"
  fi
  
  echo "$timestamp | $user | $auth_method | $*" >> "$log_file"
  
  # Execute original command
  gemini "$@"
}

alias gemini='audit_gemini'
```

## Integration Examples

### CI/CD Pipeline

```yaml
# GitHub Actions
name: Gemini Analysis
on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '20'
      
      - name: Install Gemini CLI
        run: npm install -g @google/gemini-cli
      
      - name: Analyze Code
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          gemini --yolo -p "Analyze code quality, generate test reports, and create improvement suggestions"
```

### Docker Integration

```dockerfile
# Dockerfile
FROM node:20-alpine

# Install Gemini CLI
RUN npm install -g @google/gemini-cli

# Copy credentials (build-time)
ARG GEMINI_API_KEY
ENV GEMINI_API_KEY=$GEMINI_API_KEY

# Or mount at runtime
# docker run -v ~/.gemini:/root/.gemini ...

WORKDIR /app
COPY . .

CMD ["gemini", "--yolo", "-p", "Analyze application and generate comprehensive report"]
```

## Related Skills

- `gemini-cli`: Main Gemini CLI integration
- `gemini-chat`: Interactive chat sessions
- `gemini-tools`: Tool execution workflows
- `gemini-mcp`: MCP server management