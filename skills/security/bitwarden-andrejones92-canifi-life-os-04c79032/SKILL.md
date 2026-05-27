---
name: bitwarden
description: Open-source password manager with self-hosting option.
category: utilities
---
# Bitwarden Skill

Open-source password manager with self-hosting option.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/bitwarden/install.sh | bash
```

Or manually:
```bash
cp -r skills/bitwarden ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BW_SESSION "your_session_key"
canifi-env set BW_CLIENTID "your_client_id"
canifi-env set BW_CLIENTSECRET "your_client_secret"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities

1. **Get Secrets**: Retrieve passwords and items
2. **Store Credentials**: Save login information
3. **Generate Passwords**: Create secure passwords
4. **Organization Vaults**: Manage team secrets
5. **Send Files**: Secure file sharing

## Usage Examples

### Get Password
```
User: "Get my GitHub password"
Assistant: Retrieves from Bitwarden
```

### Create Item
```
User: "Save this login to Bitwarden"
Assistant: Creates vault item
```

### Generate Password
```
User: "Generate a 20-character password"
Assistant: Creates secure password
```

### Send File
```
User: "Share this file securely"
Assistant: Creates Bitwarden Send
```

## Authentication Flow

1. API key authentication
2. CLI session-based
3. Self-hosted support
4. Two-step login supported

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Session Expired | Timeout | Re-authenticate |
| Item Not Found | Wrong search | Check vault |
| Access Denied | Permissions | Verify access |
| Sync Failed | Connection | Retry |

## Notes

- Open source
- Self-host option
- Bitwarden Send
- Organizations
- CLI available (bw)
- Secrets Manager
