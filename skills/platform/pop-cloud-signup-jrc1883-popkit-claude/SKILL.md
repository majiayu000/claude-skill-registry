---
name: cloud-signup
description: Create PopKit Cloud account, generate API key, and configure local connection
---

# PopKit Cloud Signup

Create a new PopKit Cloud account and obtain an API key for enhanced semantic intelligence features.

## When to Use

- User runs `/popkit:cloud signup`
- User wants to enable cloud enhancements (semantic routing, pattern learning)
- User needs to create an account to access cloud features

## Input

User provides (via AskUserQuestion):

- Email address
- Password (minimum 8 characters)

Optional flags:

- `--skip-test`: Skip connection testing after signup

## Process

### 1. Check for Existing Configuration

Before starting signup, check if user already has cloud config:

```python
from pathlib import Path
import json
import os

config_path = Path.home() / ".claude/popkit/cloud-config.json"

# Check config file
if config_path.exists():
    with open(config_path) as f:
        config = json.load(f)
        email = config.get("email")

    print(f"⚠️  Existing cloud config found for {email}")

    # Use AskUserQuestion to confirm
    # question: "You already have a cloud account. What would you like to do?"
    # options:
    #   1. "Continue with new signup" (will overwrite existing)
    #   2. "Login to existing account" (invoke pop-cloud-login skill)
    #   3. "Cancel"

# Check environment variable
if os.environ.get("POPKIT_API_KEY"):
    print("⚠️  POPKIT_API_KEY environment variable is already set")
    # Continue with signup but note it will be overridden
```

### 2. Collect User Credentials

Use AskUserQuestion for email, then custom text input for password:

**Email Collection:**

```
Use AskUserQuestion tool with:
- question: "What email would you like to use for your PopKit Cloud account?"
- header: "Email"
- options:
  1. label: "Enter email", description: "Type your email address"
- multiSelect: false
```

After user selects "Enter email", they'll be prompted for custom input.

**Password Collection:**

```
Use AskUserQuestion tool with:
- question: "Create a password for your account (minimum 8 characters)"
- header: "Password"
- options:
  1. label: "Enter password", description: "Type your password (will be hidden)"
- multiSelect: false
```

**Validation:**

- Email: Must contain @ and valid domain
- Password: Minimum 8 characters, no maximum

### 3. Create Account via Cloud API

Send signup request to PopKit Cloud:

```python
import requests
import json

# Signup endpoint
url = "https://api.thehouseofdeals.com/v1/auth/signup"

# Request payload
payload = {
    "email": email,
    "password": password
}

# Send request
try:
    response = requests.post(url, json=payload, timeout=10)

    if response.status_code == 201:
        # Success
        data = response.json()
        api_key = data["api_key"]
        user_id = data["user_id"]
        tier = data.get("tier", "free")

        print(f"✅ Account created successfully")
        print(f"User ID: {user_id}")
        print(f"Tier: {tier}")

    elif response.status_code == 409:
        # Email already registered
        print("❌ Signup failed: Email already registered")
        print("\nTry logging in instead:")
        print("  /popkit:cloud login")
        return

    elif response.status_code == 400:
        # Validation error
        error = response.json().get("error", "Invalid input")
        print(f"❌ Signup failed: {error}")
        return

    else:
        # Other error
        print(f"❌ Signup failed: HTTP {response.status_code}")
        print(f"Error: {response.text}")
        return

except requests.exceptions.Timeout:
    print("❌ Signup failed: Request timed out")
    print("Check your internet connection and try again")
    return

except requests.exceptions.ConnectionError:
    print("❌ Signup failed: Could not connect to PopKit Cloud")
    print("Check your internet connection and try again")
    return

except Exception as e:
    print(f"❌ Signup failed: {e}")
    return
```

### 4. Save API Key Locally

Store API key securely in local config file:

```python
from pathlib import Path
import json
import os

# Config directory
config_dir = Path.home() / ".claude/popkit"
config_dir.mkdir(parents=True, exist_ok=True)

# Config file
config_path = config_dir / "cloud-config.json"

# Prepare config
config = {
    "api_key": api_key,
    "email": email,
    "user_id": user_id,
    "tier": tier,
    "created_at": "2025-12-26T00:00:00Z"  # Use current timestamp
}

# Save config
with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

# Set restrictive permissions (Unix/Mac only)
try:
    os.chmod(config_path, 0o600)
    print(f"🔒 API key saved securely: {config_path}")
except Exception:
    # Windows doesn't support chmod the same way
    print(f"✅ API key saved: {config_path}")
```

### 5. Test Connection

Verify the API key works by querying cloud status:

```python
import requests

# Use cloud_client.py from power-mode
# (packages/popkit-core/power-mode/cloud_client.py)

try:
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(
        "https://api.thehouseofdeals.com/v1/health",
        headers=headers,
        timeout=5
    )

    if response.status_code == 200:
        data = response.json()
        latency_ms = response.elapsed.total_seconds() * 1000

        print(f"✅ Cloud connection verified ({latency_ms:.0f}ms)")

    else:
        print(f"⚠️  Warning: Could not verify connection (HTTP {response.status_code})")
        print("Your account was created, but there may be a connection issue")

except Exception as e:
    print(f"⚠️  Warning: Could not test connection: {e}")
    print("Your account was created successfully")
```

### 6. Display Setup Instructions

Show user how to use their new API key:

````markdown
✅ PopKit Cloud Account Created

**Email:** user@example.com
**API Key:** pk_live_abc123def456... (last 6 chars shown)
**Tier:** Free (100 requests/day)
**Config:** ~/.claude/popkit/cloud-config.json

---

## Quick Start

### Option 1: Use config file (recommended)

Your API key is already saved in `~/.claude/popkit/cloud-config.json`.
PopKit will automatically use it for cloud enhancements.

**Verify connection:**

```bash
/popkit:cloud status
```
````

### Option 2: Set environment variable

For maximum portability, export the API key:

```bash
# Add to ~/.bashrc or ~/.zshrc
export POPKIT_API_KEY="pk_live_abc123def456..."
```

Then restart your shell or run:

```bash
source ~/.bashrc  # or ~/.zshrc
```

---

## What's Enhanced?

With your API key configured, PopKit now has:

### Core Workflows (Always Available)

✅ All development commands and skills work without API key

### Cloud Enhancements (Now Active)

✅ **Semantic agent routing** - Better agent selection via embeddings
✅ **Community pattern learning** - Learn from other developers' solutions
✅ **Cloud knowledge base** - Access shared documentation and patterns
✅ **Cross-project insights** - Recommendations based on similar projects

---

## Usage Limits

**Free Tier:**

- 100 API requests/day
- Unlimited local execution
- All workflows available

Need more? Upgrade at: `/popkit:upgrade`

---

## Next Steps

1. **Verify connection:**

   ```bash
   /popkit:cloud status
   ```

2. **Test semantic routing:**

   ```bash
   /popkit:next  # Uses embeddings to recommend next action
   ```

3. **View account info:**
   ```bash
   /popkit:account
   ```

---

## Security Notes

- API key stored with chmod 600 (user read/write only)
- Password never stored locally
- All requests use HTTPS
- Config file: `~/.claude/popkit/cloud-config.json`

**To disconnect:**

```bash
/popkit:cloud logout
```

````

### 7. Handle Errors

Common error scenarios:

**Email Already Registered (409):**
```markdown
❌ Signup Failed

**Error:** Email already registered

This email is already associated with a PopKit Cloud account.

Try logging in instead:
```bash
/popkit:cloud login
````

Or use a different email address.

````

**Invalid Email/Password (400):**
```markdown
❌ Signup Failed

**Error:** Invalid email or password

Requirements:
- Email: Must be valid format (contains @ and domain)
- Password: Minimum 8 characters

Please try again with valid credentials.
````

**Connection Timeout:**

```markdown
❌ Signup Failed

**Error:** Request timed out

Could not connect to PopKit Cloud within 10 seconds.

Please check:

1. Your internet connection
2. Firewall/proxy settings
3. Cloud status: https://status.thehouseofdeals.com

Try again in a moment.
```

**Unknown Error:**

```markdown
❌ Signup Failed

**Error:** {error_message}

If this persists, please:

1. Report the issue: `/popkit:bug report`
2. Check cloud status: https://status.thehouseofdeals.com
3. Contact support: joseph@thehouseofdeals.com
```

## Output

### Success Case

````markdown
✅ PopKit Cloud Account Created

**Email:** user@example.com
**API Key:** **\*\***def456 (saved securely)
**Tier:** Free (100 requests/day)

### Quick Start

1. **Verify connection:**
   ```bash
   /popkit:cloud status
   ```
````

2. **Cloud enhancements now active:**
   - Semantic agent routing ✅
   - Community pattern learning ✅
   - Cloud knowledge base ✅
   - Cross-project insights ✅

**Config file:** ~/.claude/popkit/cloud-config.json

Run `/popkit:account` for detailed account info.

````

### Failure Case

```markdown
❌ Signup Failed

**Error:** Email already registered

Try logging in instead:
```bash
/popkit:cloud login
````

```

## Related Skills

- `pop-cloud-login` - Login to existing account
- `pop-cloud-status` - Check connection status
- `pop-cloud-logout` - Disconnect from cloud

## Security

**API Key Storage:**
- File: `~/.claude/popkit/cloud-config.json`
- Permissions: chmod 600 (user read/write only)
- Never logged in full (only last 6 chars shown)

**Password Handling:**
- Never stored locally
- Only transmitted to cloud API over HTTPS
- Never logged or printed

**Best Practices:**
- Use strong passwords (16+ characters recommended)
- Don't share API keys
- Use `/popkit:cloud logout` when switching accounts
```
