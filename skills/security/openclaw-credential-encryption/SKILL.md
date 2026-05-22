---
name: openclaw-credential-encryption
description: Encrypt OpenClaw runtime credentials with macOS Keychain integration, FileVault enforcement, and comprehensive protection for ~/.clawdbot/ directory and OAuth materials.
---

# OpenClaw Credential Encryption Skill

This skill provides comprehensive encryption and protection for OpenClaw runtime credentials, ensuring sensitive data is never stored in plaintext.

## When to Activate

- OpenClaw installation or configuration
- Security audit of credential storage
- After detecting plaintext credentials
- When implementing security hardening
- Before production deployment

## Credential Protection Strategy

### 1. macOS Keychain Integration

#### ✅ Recommended Approach

```bash
# Store credentials in macOS Keychain
security add-generic-password -a "openclaw" -s "discord_token" -w "your_discord_token_here"
security add-generic-password -a "openclaw" -s "anthropic_api_key" -w "your_api_key_here"
security add-generic-password -a "openclaw" -s "twilio_auth_token" -w "your_twilio_token"

# Retrieve credentials securely
security find-generic-password -a "openclaw" -s "discord_token" -w
```

#### ❌ Never Do This

```bash
# Hardcoded credentials in files
echo "DISCORD_TOKEN=abc123" > ~/.env
echo "API_KEY=sk-proj-xyz" >> ~/.env
```

### 2. File System Protection

#### Directory Hardening

```bash
# Secure ~/.clawdbot/ directory
chmod 700 ~/.clawdbot/
chmod 600 ~/.clawdbot/credentials/*
chmod 600 ~/.clawdbot/sessions/*
chmod 600 ~/.clawdbot/oauth.json

# Set immutable flag (optional)
chflags schg ~/.clawdbot/credentials/
```

#### FileVault Enforcement

```bash
# Check FileVault status
fdesetup status
# If disabled, enable:
sudo fdesetup enable -user $(whoami)
```

### 3. OAuth Material Encryption

#### OAuth JSON Protection

```bash
# Encrypt oauth.json with OpenSSL
openssl enc -aes-256-cbc -salt -in oauth.json -out oauth.json.enc
rm oauth.json

# Decrypt when needed
openssl enc -aes-256-cbc -d -in oauth.json.enc -out oauth.json
```

#### Keychain Alternative for OAuth

```bash
# Store OAuth tokens in Keychain
security add-generic-password -a "openclaw" -s "oauth_access_token" -w "$(cat oauth.json | jq -r '.access_token')"
security add-generic-password -a "openclaw" -s "oauth_refresh_token" -w "$(cat oauth.json | jq -r '.refresh_token')"
```

## Security Verification

### Credential Security Audit

```bash
# Check for plaintext credentials
echo "=== OpenClaw Credential Security Audit ==="

# Scan ~/.clawdbot/ directory
if [ -d ~/.clawdbot ]; then
  echo "📁 ~/.clawdbot/ directory found:"
  find ~/.clawdbot/ -type f -exec ls -la {} \; 2>/dev/null
  
  echo ""
  echo "🔍 Scanning for plaintext secrets:"
  grep -r "api[_-]?key\|password\|secret\|token" ~/.clawdbot/ 2>/dev/null || echo "✅ No plaintext secrets found"
else
  echo "✅ ~/.clawdbot/ directory not found"
fi

# Check for OAuth files
echo ""
echo "🔍 OAuth files:"
find ~ -name "oauth.json" -exec ls -la {} \; 2>/dev/null || echo "✅ No oauth.json files found"

# Check environment files
echo ""
echo "🔍 Environment files with OpenClaw references:"
find ~ -name ".env*" -exec grep -l "claw\|openclaw" {} \; 2>/dev/null || echo "✅ No OpenClaw env files found"
```

### Keychain Verification

```bash
# Verify Keychain credentials
echo "=== Keychain Credential Verification ==="
security find-generic-password -a "openclaw" -s "discord_token" -g 2>/dev/null && echo "✅ Discord token in Keychain" || echo "❌ Discord token not in Keychain"
security find-generic-password -a "openclaw" -s "anthropic_api_key" -g 2>/dev/null && echo "✅ Anthropic API key in Keychain" || echo "❌ Anthropic API key not in Keychain"
security find-generic-password -a "openclaw" -s "twilio_auth_token" -g 2>/dev/null && echo "✅ Twilio token in Keychain" || echo "❌ Twilio token not in Keychain"
```

## Migration Scripts

### Migrate to Keychain

```bash
#!/bin/bash
# migrate-credentials-to-keychain.sh

echo "🔐 Migrating OpenClaw credentials to macOS Keychain..."

# Backup existing credentials
if [ -d ~/.clawdbot/credentials ]; then
  cp -r ~/.clawdbot/credentials ~/.clawdbot/credentials.backup.$(date +%Y%m%d)
  echo "📋 Backed up existing credentials"
fi

# Migrate Discord token
if [ -f ~/.clawdbot/credentials/discord ]; then
  DISCORD_TOKEN=$(cat ~/.clawdbot/credentials/discord)
  security add-generic-password -a "openclaw" -s "discord_token" -w "$DISCORD_TOKEN"
  rm ~/.clawdbot/credentials/discord
  echo "✅ Migrated Discord token to Keychain"
fi

# Migrate API keys from environment
if [ -f ~/.env ]; then
  grep "ANTHROPIC_API_KEY" ~/.env && {
    API_KEY=$(grep "ANTHROPIC_API_KEY" ~/.env | cut -d'=' -f2)
    security add-generic-password -a "openclaw" -s "anthropic_api_key" -w "$API_KEY"
    sed -i '' '/ANTHROPIC_API_KEY/d' ~/.env
    echo "✅ Migrated Anthropic API key to Keychain"
  }
fi

echo "🎉 Credential migration complete!"
```

### Encrypt Existing OAuth

```bash
#!/bin/bash
# encrypt-oauth.sh

echo "🔐 Encrypting OAuth materials..."

# Find and encrypt OAuth files
find ~ -name "oauth.json" | while read oauth_file; do
  echo "🔒 Encrypting $oauth_file"
  openssl enc -aes-256-cbc -salt -in "$oauth_file" -out "$oauth_file.enc"
  rm "$oauth_file"
  echo "✅ Encrypted $oauth_file -> $oauth_file.enc"
done

echo "🎉 OAuth encryption complete!"
```

## Configuration Integration

### OpenClaw Configuration Updates

```bash
# Configure OpenClaw to use Keychain
openclaw config set security.credential_storage="keychain"
openclaw config set security.encryption_enabled=true
openclaw config set security.filevault_required=true
```

### Environment Template

```bash
# .env.template for OpenClaw
# Copy to .env.local and fill with Keychain references

# Discord (stored in Keychain)
# DISCORD_TOKEN=keychain://openclaw/discord_token

# Anthropic API (stored in Keychain)
# ANTHROPIC_API_KEY=keychain://openclaw/anthropic_api_key

# Twilio (stored in Keychain)
# TWILIO_AUTH_TOKEN=keychain://openclaw/twilio_auth_token
# TWILIO_ACCOUNT_SID=keychain://openclaw/twilio_account_sid
```

## Security Best Practices

### ✅ Always Do

- Store credentials in macOS Keychain
- Encrypt sensitive files with AES-256
- Use FileVault for full-disk encryption
- Set proper file permissions (700/600)
- Regularly audit credential storage
- Use credential rotation policies

### ❌ Never Do

- Store credentials in plaintext files
- Commit secrets to version control
- Use environment variables for production secrets
- Share credentials via unencrypted channels
- Disable FileVault on portable devices
- Ignore credential security warnings

## Monitoring and Alerts

### Credential Access Monitoring

```bash
# Monitor credential file access
sudo fs_usage | grep clawdbot

# Monitor Keychain access
log stream --predicate 'subsystem == "com.apple.security"' | grep keychain
```

### Automated Security Checks

```bash
# Daily security scan
echo "0 2 * * * /path/to/openclaw-credential-security-check.sh" | crontab -

# Security check script
#!/bin/bash
# openclaw-credential-security-check.sh

SECURITY_LOG="/var/log/openclaw-security.log"
DATE=$(date +%Y-%m-%d_%H:%M:%S)

echo "[$DATE] Running OpenClaw security check..." >> $SECURITY_LOG

# Check for plaintext credentials
if grep -r "api[_-]?key\|password\|secret\|token" ~/.clawdbot/ 2>/dev/null; then
  echo "[$DATE] ❌ CRITICAL: Plaintext credentials found!" >> $SECURITY_LOG
  # Send alert notification
  osascript -e 'display notification "Plaintext credentials detected in OpenClaw!" with title "Security Alert"'
else
  echo "[$DATE] ✅ No plaintext credentials found" >> $SECURITY_LOG
fi
```

This skill ensures comprehensive OpenClaw credential protection using industry-standard macOS security features and encryption practices.
