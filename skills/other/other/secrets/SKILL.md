---
skill: secrets
description: Manage secrets via Bitwarden - retrieve credentials, set up environment variables
version: 1.0.0
triggers:
  - /secrets
  - /secret
  - /get-secret
  - /bw
---

# Secrets Management Skill

Manage credentials securely via Bitwarden. This vault does NOT store credentials - all secrets are kept in Bitwarden and accessed on-demand.

## Configuration

By default, secrets are stored in a Bitwarden folder called "Obsidian Vault". You can customise this by setting `BITWARDEN_FOLDER` in your environment or updating the folder name in the commands below.

## Commands

| Command               | Description                                          |
| --------------------- | ---------------------------------------------------- |
| `/secrets status`     | Check Bitwarden CLI status and session               |
| `/secrets get <name>` | Retrieve a secret by name from Bitwarden             |
| `/secrets list`       | List all secrets in your configured Bitwarden folder |
| `/secrets env`        | Output export commands for all vault secrets         |
| `/secrets setup`      | Guide through initial Bitwarden CLI setup            |

---

## Implementation

### `/secrets status`

Check Bitwarden CLI installation and session status:

```bash
# Check if Bitwarden CLI is installed
if ! command -v bw &> /dev/null; then
    echo "Bitwarden CLI not installed"
    echo "   Install with: brew install bitwarden-cli"
    exit 1
fi

# Check login and lock status
STATUS=$(bw status)
echo "$STATUS" | jq -r '"Status: \(.status)"'
```

Report to user:

- CLI installed: yes/no
- Logged in: yes/no
- Vault: locked/unlocked
- If not set up, suggest `/secrets setup`

### `/secrets get <name>`

1. Ensure Bitwarden is unlocked:

   ```bash
   BW_SESSION=$(bw unlock --raw 2>/dev/null)
   if [ -z "$BW_SESSION" ]; then
       echo "Please unlock Bitwarden first: bw unlock"
       exit 1
   fi
   ```

2. Retrieve the item:

   ```bash
   ITEM=$(bw get item "$SECRET_NAME" --session "$BW_SESSION" 2>/dev/null)
   if [ -z "$ITEM" ]; then
       echo "Secret '$SECRET_NAME' not found"
       exit 1
   fi
   ```

3. Extract based on type:
   ```bash
   TYPE=$(echo "$ITEM" | jq -r '.type')
   if [ "$TYPE" = "2" ]; then
       # Secure Note - return notes field
       echo "$ITEM" | jq -r '.notes'
   else
       # Login - offer username/password
       echo "Username: $(echo "$ITEM" | jq -r '.login.username')"
       echo "Password: [hidden - use --show-password to display]"
   fi
   ```

**CRITICAL**: Never store retrieved secrets in files or conversation history. Display once and advise user to copy immediately.

### `/secrets list`

```bash
# Set your Bitwarden folder name (customise as needed)
FOLDER_NAME="${BITWARDEN_FOLDER:-Obsidian Vault}"

BW_SESSION=$(bw unlock --raw)
FOLDER_ID=$(bw get folder "$FOLDER_NAME" --session "$BW_SESSION" | jq -r '.id')
bw list items --folderid "$FOLDER_ID" --session "$BW_SESSION" | jq -r '.[] | "\(.name) (\(if .type == 2 then "note" else "login" end))"'
```

Display as formatted table with Name and Type columns.

### `/secrets env`

Generate environment variable export commands:

```bash
# Set your Bitwarden folder name (customise as needed)
FOLDER_NAME="${BITWARDEN_FOLDER:-Obsidian Vault}"

BW_SESSION=$(bw unlock --raw)
FOLDER_ID=$(bw get folder "$FOLDER_NAME" --session "$BW_SESSION" | jq -r '.id')

# Get all Secure Notes in the folder
bw list items --folderid "$FOLDER_ID" --session "$BW_SESSION" | \
  jq -r '.[] | select(.type == 2) |
    "export " + (.name | gsub(" "; "_") | gsub("-"; "_") | ascii_upcase) + "=\"" + (.notes | gsub("\n"; "\\n") | gsub("\""; "\\\"")) + "\""'
```

Output format:

```bash
# Bitwarden secrets for your vault
# Run: eval "$(/secrets env)" or copy/paste below

export ANTHROPIC_API_KEY="<your-key>"  # pragma: allowlist secret
export OPENAI_API_KEY="<your-key>"     # pragma: allowlist secret
export GITHUB_PAT="<your-token>"       # pragma: allowlist secret

# These are session-only - not persisted to disk
```

### `/secrets setup`

Guide the user through setup:

1. **Check/Install CLI**:

   ```bash
   brew install bitwarden-cli
   ```

2. **Login**:

   ```bash
   bw login
   # Or for SSO: bw login --sso
   ```

3. **Unlock vault**:

   ```bash
   export BW_SESSION=$(bw unlock --raw)
   ```

4. **Verify access**:

   ```bash
   bw list folders --session $BW_SESSION
   ```

5. **Create your vault folder** (if it doesn't exist):

   ```bash
   # Create a folder for your vault secrets
   bw create folder '{"name":"Obsidian Vault"}' --session $BW_SESSION
   ```

6. **Import secrets** (if migrating from Atomic Notes):

   ```bash
   bw import bitwardencsv bitwarden-import.csv
   ```

7. **Add shell alias** (optional):
   ```bash
   echo 'alias bw-unlock="export BW_SESSION=\$(bw unlock --raw)"' >> ~/.zshrc
   ```

---

## Environment Variable Naming Convention

| Bitwarden Item Name | Environment Variable    |
| ------------------- | ----------------------- |
| Anthropic API Key   | `ANTHROPIC_API_KEY`     |
| Open AI Key         | `OPENAI_API_KEY`        |
| GitHub PAT          | `GITHUB_PAT`            |
| AWS Access Key      | `AWS_ACCESS_KEY_ID`     |
| AWS Secret Key      | `AWS_SECRET_ACCESS_KEY` |
| Notion Token        | `NOTION_TOKEN`          |

Custom mappings can be added to `.claude/config.local.json`:

```json
{
  "secrets": {
    "folderName": "My Custom Folder",
    "envMapping": {
      "My Custom Item": "CUSTOM_VAR"
    }
  }
}
```

---

## Security Rules

1. **Never write secrets to files** in this vault
2. **Never include secrets in commit messages** or code comments
3. **Never display secrets in full** unless explicitly requested
4. **Session keys are temporary** - they expire and must be refreshed
5. **Delete CSV immediately** after Bitwarden import
6. **Rotate credentials** that were ever in git history

---

## Integration with Scripts

Scripts should read from environment variables, not files:

**Python**:

```python
import os

api_key = os.environ.get('ANTHROPIC_API_KEY')
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set. Run: /secrets env")
```

**JavaScript/Node.js**:

```javascript
const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) {
  throw new Error("ANTHROPIC_API_KEY not set. Run: /secrets env");
}
```

**Bash**:

```bash
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ANTHROPIC_API_KEY not set. Run: /secrets env"
    exit 1
fi
```

---

## Quick Reference

```bash
# One-time setup
brew install bitwarden-cli
bw login

# Each session
export BW_SESSION=$(bw unlock --raw)

# Get a secret
bw get item "Anthropic API Key" --session $BW_SESSION | jq -r '.notes'

# List all vault secrets (update folder name as needed)
FOLDER_NAME="Obsidian Vault"
bw list items --folderid $(bw get folder "$FOLDER_NAME" --session $BW_SESSION | jq -r '.id') --session $BW_SESSION | jq -r '.[].name'
```

---

## Related

- `scripts/migrate-to-bitwarden.cjs` - Export Atomic Notes to Bitwarden CSV
